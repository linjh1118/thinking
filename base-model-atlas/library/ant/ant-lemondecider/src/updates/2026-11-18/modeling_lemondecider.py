"""LemonDecider inference-only architecture. See LICENSE and NOTICE."""
from dataclasses import dataclass
import torch
from transformers.modeling_utils import PreTrainedModel
from transformers.utils import ModelOutput
from transformers.models.qwen3_5.modeling_qwen3_5 import Qwen3_5Model, Qwen3_5Attention
from .configuration_lemondecider import LemonDeciderConfig


@dataclass
class LemonDeciderOutput(ModelOutput):
    logits: torch.Tensor | None = None


class LemonDeciderForDecisionClassification(PreTrainedModel):
    config_class = LemonDeciderConfig
    base_model_prefix = 'backbone'
    _no_split_modules = ['Qwen3_5DecoderLayer', 'Qwen3_5VisionBlock']
    _supports_sdpa = True
    _supports_cache_class = False

    def __init__(self, config):
        super().__init__(config)
        config.text_config.is_causal = False
        self.backbone = Qwen3_5Model(config)
        self.backbone.language_model.config.is_causal = False
        for module in self.backbone.language_model.modules():
            if isinstance(module, Qwen3_5Attention):
                module.is_causal = False
        self.readout = torch.nn.Linear(config.text_config.hidden_size, config.max_options, bias=False)
        self.post_init()

    def get_input_embeddings(self):
        return self.backbone.get_input_embeddings()

    def set_input_embeddings(self, value):
        self.backbone.set_input_embeddings(value)

    def forward(self, input_ids=None, attention_mask=None, option_counts=None,
                readout_positions=None, return_dict=True, **kwargs):
        if input_ids is None or input_ids.ndim != 2 or not input_ids.shape[1]:
            raise ValueError('Expected nonempty input_ids [batch, length]')
        if input_ids.shape[1] > self.config.max_input_length:
            raise ValueError('Input exceeds context capacity; truncation is disabled')
        if attention_mask is None:
            attention_mask = torch.ones_like(input_ids)
        if attention_mask.shape != input_ids.shape or not bool((attention_mask[:, -1] == 1).all()):
            raise ValueError('Left-padded input with a valid final position is required')
        if readout_positions is None or option_counts is None:
            raise ValueError('Use the bundled DecisionModel to prepare decision inputs')
        positions = torch.as_tensor(readout_positions, device=input_ids.device)
        counts = torch.as_tensor(option_counts, device=input_ids.device)
        if (positions.dtype == torch.bool or positions.is_floating_point() or
                positions.ndim != 2 or positions.shape[1] != 2 or not len(positions)):
            raise ValueError('Invalid readout positions')
        if counts.dtype == torch.bool or counts.is_floating_point() or counts.shape != (len(positions),):
            raise ValueError('Invalid option counts')
        rows, cols = positions[:, 0], positions[:, 1]
        if not bool(((rows >= 0) & (rows < input_ids.shape[0]) &
                     (cols >= 0) & (cols < input_ids.shape[1])).all()):
            raise ValueError('Readout positions out of bounds')
        if not bool(attention_mask[rows, cols].bool().all()):
            raise ValueError('Readout position is padding')
        if bool(torch.bincount(rows, minlength=input_ids.shape[0]).eq(0).any()):
            raise ValueError('Every input needs a readout')
        if not bool(((counts >= 1) & (counts <= self.config.max_options)).all()):
            raise ValueError('Option count out of bounds')
        if kwargs.pop('use_cache', False) or kwargs.get('past_key_values') is not None:
            raise ValueError('Cached generation is not supported')
        if set(kwargs) - {'mm_token_type_ids', 'position_ids'}:
            raise ValueError('Unsupported model inputs; this runtime is text-only')
        media_types = kwargs.get('mm_token_type_ids')
        if media_types is not None and (media_types.shape != input_ids.shape or bool(media_types.ne(0).any())):
            raise ValueError('Only text token types are supported')
        output = self.backbone(input_ids=input_ids, attention_mask=attention_mask,
                               use_cache=False, return_dict=True, **kwargs)
        logits = self.readout(output.last_hidden_state[rows, cols]).float()
        invalid = torch.arange(self.config.max_options, device=logits.device)[None] >= counts[:, None]
        logits = logits.masked_fill(invalid, -1e9)
        return LemonDeciderOutput(logits=logits) if return_dict else (logits,)
