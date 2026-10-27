
from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass
from typing import Optional, Union
import torch
from torch import nn
from transformers.utils.generic import check_model_inputs
from transformers.activations import ACT2FN
from transformers.cache_utils import Cache, DynamicCache
from transformers.integrations import use_kernel_forward_from_hub
from transformers.masking_utils import create_causal_mask, create_sliding_window_causal_mask
from transformers.modeling_flash_attention_utils import FlashAttentionKwargs
from transformers.modeling_layers import GradientCheckpointingLayer
from transformers.modeling_outputs import BaseModelOutputWithPast
from transformers.modeling_rope_utils import ROPE_INIT_FUNCTIONS, dynamic_rope_update
from transformers.modeling_utils import ALL_ATTENTION_FUNCTIONS, PreTrainedModel
from transformers.processing_utils import Unpack
from transformers.utils import TransformersKwargs, auto_docstring
from .configuration_nlduni import MinistralDLMConfig

def rotate_half(x):
    x1 = x[..., :x.shape[-1] // 2]
    x2 = x[..., x.shape[-1] // 2:]
    return torch.cat((-x2, x1), dim=-1)

def apply_rotary_pos_emb(q, k, cos, sin, position_ids=None, unsqueeze_dim=1):
    cos = cos.unsqueeze(unsqueeze_dim)
    sin = sin.unsqueeze(unsqueeze_dim)
    q_embed = q * cos + rotate_half(q) * sin
    k_embed = k * cos + rotate_half(k) * sin
    return (q_embed, k_embed)

def repeat_kv(hidden_states: torch.Tensor, n_rep: int) -> torch.Tensor:
    (batch, num_key_value_heads, slen, head_dim) = hidden_states.shape
    if n_rep == 1:
        return hidden_states
    hidden_states = hidden_states[:, :, None, :, :].expand(batch, num_key_value_heads, n_rep, slen, head_dim)
    return hidden_states.reshape(batch, num_key_value_heads * n_rep, slen, head_dim)

def eager_attention_forward(module: nn.Module, query: torch.Tensor, key: torch.Tensor, value: torch.Tensor, attention_mask: Optional[torch.Tensor], scaling: float, dropout: float=0.0, **kwargs: Unpack[TransformersKwargs]):
    key_states = repeat_kv(key, module.num_key_value_groups)
    value_states = repeat_kv(value, module.num_key_value_groups)
    attn_weights = torch.matmul(query, key_states.transpose(2, 3)) * scaling
    if attention_mask is not None:
        causal_mask = attention_mask[:, :, :, :key_states.shape[-2]]
        attn_weights = attn_weights + causal_mask
    attn_weights = nn.functional.softmax(attn_weights, dim=-1, dtype=torch.float32).to(query.dtype)
    attn_weights = nn.functional.dropout(attn_weights, p=dropout, training=False)
    attn_output = torch.matmul(attn_weights, value_states)
    attn_output = attn_output.transpose(1, 2).contiguous()
    return (attn_output, attn_weights)

def _get_llama_4_attn_scale(positions_ids: torch.Tensor, beta: float, max_position_embeddings: int) -> torch.Tensor:
    scaling = 1 + beta * torch.log(1 + torch.floor(positions_ids / max_position_embeddings))
    return scaling.unsqueeze(-1)

@dataclass(frozen=True, slots=True)
class _MixedTokenRoutingPlan:
    mask: torch.Tensor
    understanding_indices: torch.Tensor
    generation_indices: torch.Tensor

    @classmethod
    def from_mask(cls, mask: torch.Tensor) -> '_MixedTokenRoutingPlan':
        flat_mask = mask.reshape(-1)
        return cls(mask=mask, understanding_indices=(~flat_mask).nonzero(as_tuple=False).flatten(), generation_indices=flat_mask.nonzero(as_tuple=False).flatten())
TokenRouting = Optional[Union[bool, _MixedTokenRoutingPlan]]

def _resolve_dual_tower_layers(config: MinistralDLMConfig) -> int:
    num_hidden_layers = config.num_hidden_layers
    configured = 18
    if configured is None:
        return num_hidden_layers
    if isinstance(configured, bool) or not isinstance(configured, int):
        raise TypeError('dual_tower_layers must be an integer')
    if not 0 <= configured <= num_hidden_layers:
        raise ValueError(f'dual_tower_layers must be between 0 and num_hidden_layers ({num_hidden_layers}), got {configured}')
    return configured

def _routing_mask(routing: TokenRouting, hidden_states: torch.Tensor) -> torch.Tensor:
    if routing is None:
        return torch.zeros(hidden_states.shape[:2], dtype=torch.bool, device=hidden_states.device)
    if routing is True:
        return torch.ones(hidden_states.shape[:2], dtype=torch.bool, device=hidden_states.device)
    return routing.mask

def _create_split_tower_block_mask(block_mask, *, current_routing: torch.Tensor, cached_routing: torch.Tensor):
    from torch.nn.attention.flex_attention import BlockMask, create_block_mask
    if isinstance(block_mask, str):
        if block_mask != 'full':
            raise ValueError(f'Unsupported attention block-mask sentinel: {block_mask}')
        base_mask_mod = None
        query_length = current_routing.shape[1]
        key_value_length = cached_routing.shape[1] + query_length
        block_size = 128
    elif isinstance(block_mask, BlockMask):
        base_mask_mod = block_mask.mask_mod
        (query_length, key_value_length) = block_mask.seq_lengths
        block_size = block_mask.BLOCK_SIZE
    else:
        raise TypeError("partial dual-tower FlexAttention requires an explicit BlockMask or the 'full' sentinel")
    current_length = current_routing.shape[1]
    cached_length = cached_routing.shape[1]
    if query_length < current_length:
        raise ValueError(f'FlexAttention block-mask query length is shorter than routing: {query_length} < {current_length}')
    if key_value_length < cached_length + current_length:
        raise ValueError(f'FlexAttention block-mask key/value length is shorter than cached and current routing: {key_value_length} < {cached_length + current_length}')
    query_routing = torch.nn.functional.pad(current_routing, (0, query_length - current_length), value=False)
    key_value_routing = torch.cat((cached_routing, current_routing), dim=1)
    key_value_routing = torch.nn.functional.pad(key_value_routing, (0, key_value_length - key_value_routing.shape[1]), value=False)

    def split_tower_mask(b, h, q_idx, kv_idx):
        same_tower = query_routing[b, q_idx] == key_value_routing[b, kv_idx]
        same_tower = same_tower | (q_idx >= current_length)
        if base_mask_mod is None:
            return same_tower
        return base_mask_mod(b, h, q_idx, kv_idx) & same_tower
    return create_block_mask(split_tower_mask, B=current_routing.shape[0], H=None, Q_LEN=query_length, KV_LEN=key_value_length, device=current_routing.device, BLOCK_SIZE=block_size)

def _canonicalize_token_routing(routing: Optional[torch.Tensor], hidden_states: torch.Tensor, *, dual_tower: bool) -> TokenRouting:
    if routing is None:
        return None
    if not torch.is_tensor(routing) or routing.ndim != 2:
        raise TypeError('routing must be a rank-2 tensor with shape [batch, sequence]')
    if tuple(routing.shape) != tuple(hidden_states.shape[:2]):
        raise ValueError(f'routing must match the transformer token shape: expected {tuple(hidden_states.shape[:2])}, got {tuple(routing.shape)}')
    if routing.device != hidden_states.device:
        raise ValueError('routing and transformer hidden states must share a device')
    if routing.dtype == torch.bool:
        normalized = routing
    elif routing.dtype in {torch.uint8, torch.int8, torch.int16, torch.int32, torch.int64}:
        if bool(((routing != 0) & (routing != 1)).any()):
            raise ValueError('routing values must be binary (0 for U, 1 for G)')
        normalized = routing.to(dtype=torch.bool)
    else:
        raise TypeError('routing must have boolean or integer dtype')
    has_generation_route = bool(normalized.any())
    if has_generation_route and (not dual_tower):
        raise ValueError('routing selects G but config.dual_tower is false')
    if not has_generation_route:
        return None
    if bool(normalized.all()):
        return True
    return _MixedTokenRoutingPlan.from_mask(normalized)

def _routed_module(hidden_states: torch.Tensor, routing: TokenRouting, understanding_module: Callable[[torch.Tensor], torch.Tensor], generation_module: Optional[Callable[[torch.Tensor], torch.Tensor]]) -> torch.Tensor:
    if routing is None:
        return understanding_module(hidden_states)
    if routing is True:
        if generation_module is None:
            raise RuntimeError('G routing requires generation-tower parameters')
        return generation_module(hidden_states)
    if generation_module is None:
        raise RuntimeError('mixed routing requires generation-tower parameters')
    if not isinstance(routing, _MixedTokenRoutingPlan):
        raise TypeError('mixed routing must use a canonical dispatch plan')
    flat_hidden = hidden_states.reshape(-1, hidden_states.shape[-1])
    understanding_output = understanding_module(flat_hidden.index_select(0, routing.understanding_indices))
    generation_output = generation_module(flat_hidden.index_select(0, routing.generation_indices))
    flat_output = understanding_output.new_empty((flat_hidden.shape[0], *understanding_output.shape[1:]))
    flat_output = flat_output.index_copy(0, routing.understanding_indices, understanding_output)
    flat_output = flat_output.index_copy(0, routing.generation_indices, generation_output)
    return flat_output.reshape(*hidden_states.shape[:-1], *flat_output.shape[1:])

class Ministral3Attention(nn.Module):

    def __init__(self, config: MinistralDLMConfig, layer_idx: int):
        super().__init__()
        self.config = config
        self.layer_idx = layer_idx
        self.split_tower = layer_idx >= _resolve_dual_tower_layers(config)
        self.head_dim = getattr(config, 'head_dim', None) or config.hidden_size // config.num_attention_heads
        self.num_key_value_groups = config.num_attention_heads // config.num_key_value_heads
        self.scaling = self.head_dim ** -0.5
        self.attention_dropout = config.attention_dropout
        self.is_causal = True
        self.q_proj = nn.Linear(config.hidden_size, config.num_attention_heads * self.head_dim, bias=False)
        self.k_proj = nn.Linear(config.hidden_size, config.num_key_value_heads * self.head_dim, bias=False)
        self.v_proj = nn.Linear(config.hidden_size, config.num_key_value_heads * self.head_dim, bias=False)
        self.o_proj = nn.Linear(config.num_attention_heads * self.head_dim, config.hidden_size, bias=False)
        self.q_proj_gen = nn.Linear(config.hidden_size, config.num_attention_heads * self.head_dim, bias=False)
        self.k_proj_gen = nn.Linear(config.hidden_size, config.num_key_value_heads * self.head_dim, bias=False)
        self.v_proj_gen = nn.Linear(config.hidden_size, config.num_key_value_heads * self.head_dim, bias=False)
        self.o_proj_gen = nn.Linear(config.num_attention_heads * self.head_dim, config.hidden_size, bias=False)
        self.diffusion_lm = config.diffusion_lm

    def _project_qkv(self, hidden_states: torch.Tensor, routing: TokenRouting) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        return (_routed_module(hidden_states, routing, self.q_proj, getattr(self, 'q_proj_gen', None)), _routed_module(hidden_states, routing, self.k_proj, getattr(self, 'k_proj_gen', None)), _routed_module(hidden_states, routing, self.v_proj, getattr(self, 'v_proj_gen', None)))

    def _project_output(self, hidden_states: torch.Tensor, routing: TokenRouting) -> torch.Tensor:
        return _routed_module(hidden_states, routing, self.o_proj, getattr(self, 'o_proj_gen', None))

    def forward(self, hidden_states: torch.Tensor, position_embeddings: tuple[torch.Tensor, torch.Tensor], attention_mask: Optional[torch.Tensor], past_key_values: Optional[Cache]=None, cache_position: Optional[torch.LongTensor]=None, use_cache: Optional[bool]=False, routing: TokenRouting=None, **kwargs: Unpack[FlashAttentionKwargs]) -> tuple[torch.Tensor, Optional[torch.Tensor]]:
        input_shape = hidden_states.shape[:-1]
        hidden_shape = (*input_shape, -1, self.head_dim)
        (query_states, key_states, value_states) = self._project_qkv(hidden_states, routing)
        query_states = query_states.view(hidden_shape).transpose(1, 2)
        key_states = key_states.view(hidden_shape).transpose(1, 2)
        value_states = value_states.view(hidden_shape).transpose(1, 2)
        (cos, sin) = position_embeddings
        (query_states, key_states) = apply_rotary_pos_emb(query_states, key_states, cos, sin)
        query_states = query_states * _get_llama_4_attn_scale(cache_position, self.config.rope_parameters.get('llama_4_scaling_beta'), self.config.rope_parameters.get('original_max_position_embeddings')).to(query_states.dtype)
        if past_key_values is not None:
            if use_cache:
                cache_kwargs = {'sin': sin, 'cos': cos, 'cache_position': cache_position}
                (key_states, value_states) = past_key_values.update(key_states, value_states, self.layer_idx, cache_kwargs)
            else:
                (old_k, old_v) = (past_key_values.layers[self.layer_idx].keys, past_key_values.layers[self.layer_idx].values)
                key_states = torch.cat([old_k, key_states], dim=-2)
                value_states = torch.cat([old_v, value_states], dim=-2)
        attention_interface: Callable = eager_attention_forward
        if self.config._attn_implementation != 'eager':
            attention_interface = ALL_ATTENTION_FUNCTIONS[self.config._attn_implementation]
        if self.diffusion_lm:
            (attn_output, attn_weights) = attention_interface(self, query_states, key_states, value_states, None, dropout=0.0, scaling=self.scaling, is_causal=False, **kwargs)
        else:
            (attn_output, attn_weights) = attention_interface(self, query_states, key_states, value_states, attention_mask, dropout=0.0, scaling=self.scaling, sliding_window=getattr(self.config, 'sliding_window', None), **kwargs)
        attn_output = attn_output.reshape(*input_shape, -1).contiguous()
        attn_output = self._project_output(attn_output, routing)
        return (attn_output, attn_weights)

class Ministral3MLP(nn.Module):

    def __init__(self, config):
        super().__init__()
        self.config = config
        self.hidden_size = config.hidden_size
        self.intermediate_size = config.intermediate_size
        self.gate_proj = nn.Linear(self.hidden_size, self.intermediate_size, bias=False)
        self.up_proj = nn.Linear(self.hidden_size, self.intermediate_size, bias=False)
        self.down_proj = nn.Linear(self.intermediate_size, self.hidden_size, bias=False)
        self.gate_proj_gen = nn.Linear(self.hidden_size, self.intermediate_size, bias=False)
        self.up_proj_gen = nn.Linear(self.hidden_size, self.intermediate_size, bias=False)
        self.down_proj_gen = nn.Linear(self.intermediate_size, self.hidden_size, bias=False)
        self.act_fn = ACT2FN[config.hidden_act]

    def _understanding_forward(self, hidden_states: torch.Tensor) -> torch.Tensor:
        return self.down_proj(self.act_fn(self.gate_proj(hidden_states)) * self.up_proj(hidden_states))

    def _generation_forward(self, hidden_states: torch.Tensor) -> torch.Tensor:
        return self.down_proj_gen(self.act_fn(self.gate_proj_gen(hidden_states)) * self.up_proj_gen(hidden_states))

    def forward(self, hidden_states: torch.Tensor, routing: TokenRouting=None) -> torch.Tensor:
        generation_module = self._generation_forward if hasattr(self, 'gate_proj_gen') else None
        return _routed_module(hidden_states, routing, self._understanding_forward, generation_module)

@use_kernel_forward_from_hub('RMSNorm')
class Ministral3RMSNorm(nn.Module):

    def __init__(self, hidden_size, eps=1e-06):
        super().__init__()
        self.weight = nn.Parameter(torch.ones(hidden_size))
        self.variance_epsilon = eps

    def forward(self, hidden_states):
        input_dtype = hidden_states.dtype
        hidden_states = hidden_states.to(torch.float32)
        variance = hidden_states.pow(2).mean(-1, keepdim=True)
        hidden_states = hidden_states * torch.rsqrt(variance + self.variance_epsilon)
        return self.weight * hidden_states.to(input_dtype)

    def extra_repr(self):
        return f'{tuple(self.weight.shape)}, eps={self.variance_epsilon}'

class Ministral3DecoderLayer(GradientCheckpointingLayer):

    def __init__(self, config: MinistralDLMConfig, layer_idx: int):
        super().__init__()
        self.hidden_size = config.hidden_size
        from .attention import MinistralFlexAttention
        attn_class = MinistralFlexAttention
        self.self_attn = attn_class(config=config, layer_idx=layer_idx)
        self.mlp = Ministral3MLP(config)
        self.input_layernorm = Ministral3RMSNorm(config.hidden_size, eps=config.rms_norm_eps)
        self.post_attention_layernorm = Ministral3RMSNorm(config.hidden_size, eps=config.rms_norm_eps)
        self.input_layernorm_gen = Ministral3RMSNorm(config.hidden_size, eps=config.rms_norm_eps)
        self.post_attention_layernorm_gen = Ministral3RMSNorm(config.hidden_size, eps=config.rms_norm_eps)

    def forward(self, hidden_states: torch.Tensor, attention_mask: Optional[torch.Tensor]=None, position_ids: Optional[torch.LongTensor]=None, past_key_values: Optional[Cache]=None, use_cache: Optional[bool]=False, cache_position: Optional[torch.LongTensor]=None, position_embeddings: Optional[tuple[torch.Tensor, torch.Tensor]]=None, routing: TokenRouting=None, **kwargs: Unpack[TransformersKwargs]) -> torch.Tensor:
        residual = hidden_states
        hidden_states = _routed_module(hidden_states, routing, self.input_layernorm, getattr(self, 'input_layernorm_gen', None))
        (hidden_states, _) = self.self_attn(hidden_states=hidden_states, attention_mask=attention_mask, position_ids=position_ids, past_key_values=past_key_values, use_cache=use_cache, cache_position=cache_position, position_embeddings=position_embeddings, routing=routing, **kwargs)
        hidden_states = residual + hidden_states
        residual = hidden_states
        hidden_states = _routed_module(hidden_states, routing, self.post_attention_layernorm, getattr(self, 'post_attention_layernorm_gen', None))
        hidden_states = self.mlp(hidden_states, routing=routing)
        hidden_states = residual + hidden_states
        return hidden_states

class Ministral3PreTrainedModel(PreTrainedModel):
    config: MinistralDLMConfig
    base_model_prefix = 'model'
    supports_gradient_checkpointing = True
    _no_split_modules = ['Ministral3DecoderLayer']
    _skip_keys_device_placement = ['past_key_values']
    _supports_flash_attn = True
    _supports_sdpa = True
    _supports_flex_attn = True
    _can_compile_fullgraph = True
    _supports_attention_backend = True
    _can_record_outputs = {'hidden_states': Ministral3DecoderLayer, 'attentions': Ministral3Attention}

class Ministral3RotaryEmbedding(nn.Module):
    inv_freq: torch.Tensor

    def __init__(self, config: MinistralDLMConfig, device=None):
        super().__init__()
        self.max_seq_len_cached = config.max_position_embeddings
        self.original_max_seq_len = config.max_position_embeddings
        self.config = config
        self.rope_type = self.config.rope_parameters['rope_type']
        rope_init_fn: Callable = self.compute_default_rope_parameters
        if self.rope_type != 'default':
            rope_init_fn = ROPE_INIT_FUNCTIONS[self.rope_type]
        (inv_freq, self.attention_scaling) = rope_init_fn(self.config, device)
        self.register_buffer('inv_freq', inv_freq, persistent=False)
        self.original_inv_freq = inv_freq

    @staticmethod
    def compute_default_rope_parameters(config: Optional[MinistralDLMConfig]=None, device: Optional['torch.device']=None, seq_len: Optional[int]=None) -> tuple['torch.Tensor', float]:
        base = config.rope_parameters['rope_theta']
        dim = getattr(config, 'head_dim', None) or config.hidden_size // config.num_attention_heads
        attention_factor = 1.0
        inv_freq = 1.0 / base ** (torch.arange(0, dim, 2, dtype=torch.int64).to(device=device, dtype=torch.float) / dim)
        return (inv_freq, attention_factor)

    @torch.no_grad()
    @dynamic_rope_update
    def forward(self, x, position_ids):
        with torch.autocast(device_type=x.device.type, enabled=False):
            inv_freq_expanded = self.inv_freq[None, :, None].float().expand(position_ids.shape[0], -1, 1).to(x.device)
            position_ids_expanded = position_ids[:, None, :].float()
            freqs = (inv_freq_expanded.float() @ position_ids_expanded.float()).transpose(1, 2)
            emb = torch.cat((freqs, freqs), dim=-1)
            cos = emb.cos() * self.attention_scaling
            sin = emb.sin() * self.attention_scaling
        return (cos.to(dtype=x.dtype), sin.to(dtype=x.dtype))

class Ministral3Model(Ministral3PreTrainedModel):

    def __init__(self, config: MinistralDLMConfig):
        super().__init__(config)
        self.padding_idx = config.pad_token_id
        self.vocab_size = config.vocab_size
        self.dual_tower_layers = _resolve_dual_tower_layers(config)
        self._layer_loop_config = None
        self.embed_tokens = nn.Embedding(config.vocab_size, config.hidden_size, self.padding_idx)
        self.layers = nn.ModuleList([Ministral3DecoderLayer(config, layer_idx) for layer_idx in range(config.num_hidden_layers)])
        self.norm = Ministral3RMSNorm(config.hidden_size, eps=config.rms_norm_eps)
        self.norm_gen = Ministral3RMSNorm(config.hidden_size, eps=config.rms_norm_eps)
        self.rotary_emb = Ministral3RotaryEmbedding(config=config)
        self.gradient_checkpointing = False
        self.post_init()

    @check_model_inputs
    def forward(self, input_ids: Optional[torch.LongTensor]=None, attention_mask: Optional[torch.Tensor]=None, position_ids: Optional[torch.LongTensor]=None, past_key_values: Optional[Cache]=None, inputs_embeds: Optional[torch.FloatTensor]=None, use_cache: Optional[bool]=None, cache_position: Optional[torch.LongTensor]=None, input_embeddings: Optional[torch.FloatTensor]=None, routing: Optional[torch.Tensor]=None, modality_indices: Optional[torch.Tensor]=None, loop_k: Optional[int]=None, loop_depths: Optional[torch.LongTensor]=None, **kwargs: Unpack[TransformersKwargs]) -> BaseModelOutputWithPast:
        if input_embeddings is not None:
            inputs_embeds = input_embeddings
            input_embeddings = None
        if (input_ids is None) ^ (inputs_embeds is not None):
            raise ValueError('You must specify exactly one of input_ids or inputs_embeds')
        if inputs_embeds is None:
            inputs_embeds = self.embed_tokens(input_ids)
        single_stream_call = kwargs.get('single_stream_image_diffusion', False)
        if single_stream_call is None:
            single_stream_call = False
        if not isinstance(single_stream_call, bool):
            raise TypeError('single_stream_image_diffusion must be boolean')
        use_layer_loop = self._layer_loop_config is not None and single_stream_call
        if loop_k is not None or loop_depths is not None:
            raise ValueError('loop_k and loop_depths require an active single-stream looped_layer_execution call')
        resolved_loop_depths = None
        loop_visits = 1
        dual_tower = True
        partial_dual_tower = dual_tower and self.dual_tower_layers < self.config.num_hidden_layers
        if dual_tower and modality_indices is not None:
            modality_routing = _canonicalize_token_routing(modality_indices, inputs_embeds, dual_tower=dual_tower)
            if routing is None:
                canonical_routing = modality_routing
            else:
                canonical_routing = _canonicalize_token_routing(routing, inputs_embeds, dual_tower=dual_tower)
                if not torch.equal(routing.to(dtype=torch.bool), modality_indices.to(dtype=torch.bool)):
                    raise ValueError('routing and deprecated modality_indices alias must select identical U/G tokens when both are provided')
        else:
            canonical_routing = _canonicalize_token_routing(routing, inputs_embeds, dual_tower=dual_tower)
        if use_cache and past_key_values is None:
            past_key_values = DynamicCache()
        past_seen_tokens = past_key_values.get_seq_length() if past_key_values is not None and (partial_dual_tower or cache_position is None) else 0
        stored_cached_routing = getattr(past_key_values, '_nlduni_dual_tower_routing', None)
        track_dual_tower_routing = partial_dual_tower and (canonical_routing is not None or stored_cached_routing is not None)
        current_routing = _routing_mask(canonical_routing, inputs_embeds) if track_dual_tower_routing else None
        cached_routing = stored_cached_routing
        if track_dual_tower_routing and cached_routing is None:
            cached_routing = torch.zeros(current_routing.shape[0], past_seen_tokens, dtype=torch.bool, device=current_routing.device)
        elif track_dual_tower_routing and tuple(cached_routing.shape) != (current_routing.shape[0], past_seen_tokens):
            raise ValueError(f'cached dual-tower routing must match the KV cache shape: expected {(current_routing.shape[0], past_seen_tokens)}, got {tuple(cached_routing.shape)}')
        elif track_dual_tower_routing and cached_routing.device != current_routing.device:
            raise ValueError('cached dual-tower routing and inputs must share a device')
        if track_dual_tower_routing and past_key_values is not None:
            past_key_values._nlduni_dual_tower_routing = cached_routing
            past_key_values._nlduni_dual_tower_has_generation = bool(getattr(past_key_values, '_nlduni_dual_tower_has_generation', False))
        if cache_position is None:
            cache_position = torch.arange(past_seen_tokens, past_seen_tokens + inputs_embeds.shape[1], device=inputs_embeds.device)
        if position_ids is None:
            position_ids = cache_position.unsqueeze(0)
        if kwargs.get('use_causal_mask', False):
            mask_function = create_causal_mask if self.config.sliding_window is None else create_sliding_window_causal_mask
            causal_mask = mask_function(config=self.config, input_embeds=inputs_embeds, attention_mask=attention_mask, cache_position=cache_position, past_key_values=past_key_values, position_ids=position_ids)
        else:
            causal_mask = None
        hidden_states = inputs_embeds
        position_embeddings = self.rotary_emb(hidden_states, position_ids=position_ids)
        split_layer_kwargs = None
        has_split_layers = track_dual_tower_routing
        if has_split_layers and kwargs.get('overwrite_attn_impl') != 'flash_attn' and (kwargs.get('overwrite_block_mask') is not None):
            split_layer_kwargs = dict(kwargs)
            split_layer_kwargs['overwrite_block_mask'] = _create_split_tower_block_mask(kwargs['overwrite_block_mask'], current_routing=current_routing, cached_routing=cached_routing)
        for (layer_idx, decoder_layer) in enumerate(self.layers[:self.config.num_hidden_layers]):
            layer_kwargs = split_layer_kwargs if split_layer_kwargs is not None and layer_idx >= self.dual_tower_layers else kwargs
            hidden_states = decoder_layer(hidden_states, attention_mask=causal_mask, position_ids=position_ids, past_key_values=past_key_values, use_cache=use_cache, cache_position=cache_position, position_embeddings=position_embeddings, routing=canonical_routing, **layer_kwargs)
        if track_dual_tower_routing and use_cache and (past_key_values is not None):
            past_key_values._nlduni_dual_tower_routing = torch.cat((cached_routing, current_routing), dim=1)
            past_key_values._nlduni_dual_tower_has_generation = past_key_values._nlduni_dual_tower_has_generation or canonical_routing is not None
        hidden_states = _routed_module(hidden_states, canonical_routing, self.norm, getattr(self, 'norm_gen', None))
        return BaseModelOutputWithPast(last_hidden_state=hidden_states, past_key_values=past_key_values if use_cache else None)
