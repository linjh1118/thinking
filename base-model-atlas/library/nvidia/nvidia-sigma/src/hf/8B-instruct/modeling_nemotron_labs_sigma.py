# Copyright (c) 2026, NVIDIA CORPORATION. All rights reserved.
#
# Licensed under the NVIDIA Open Model License; see the LICENSE section of the
# model card for terms.

"""Nemotron-Labs-Sigma: continuous diffusion language model.

The model generates text block-by-block. For each block it denoises a Gaussian
sample in a low-dimensional (``embed_dim``) continuous token-embedding space,
conditioning a Ministral-style decoder backbone on the noisy block, the log-SNR
``gamma`` of the current step, an optional self-conditioning estimate, and a
KV-cached clean prefix. Inference needs only ``torch`` and ``transformers``.
"""

import math
from typing import Optional

import torch
import torch.nn.functional as F
from torch import nn

from transformers import PreTrainedModel

from .configuration_nemotron_labs_sigma import (
    NemotronLabsSigmaConfig,
)


# ---------------------------------------------------------------------------
# Rotary embedding (YaRN)
# ---------------------------------------------------------------------------


def _yarn_inv_freq(config) -> torch.Tensor:
    p = config.rope_parameters
    base = float(p["rope_theta"])
    dim = config.head_dim
    # When original_max_position_embeddings is given, the effective scaling
    # factor is the ratio to max_position_embeddings (DeepSeek-V3-style YaRN;
    # this is the exact geometry the model was trained with at 4096 context),
    # not the nominal "factor" entry.
    orig_max = float(p["original_max_position_embeddings"])
    factor = float(config.max_position_embeddings) / orig_max
    beta_fast = float(p["beta_fast"])
    beta_slow = float(p["beta_slow"])

    pos_freqs = base ** (torch.arange(0, dim, 2, dtype=torch.float32) / dim)
    inv_freq_extrapolation = 1.0 / pos_freqs
    inv_freq_interpolation = 1.0 / (factor * pos_freqs)

    def correction_dim(num_rotations):
        return dim * math.log(orig_max / (num_rotations * 2 * math.pi)) / (2 * math.log(base))

    low = max(math.floor(correction_dim(beta_fast)), 0)
    high = min(math.ceil(correction_dim(beta_slow)), dim - 1)
    ramp = (torch.arange(dim // 2, dtype=torch.float32) - low) / max(high - low, 0.001)
    extrapolation_factor = 1.0 - ramp.clamp(0.0, 1.0)
    return (
        inv_freq_interpolation * (1.0 - extrapolation_factor)
        + inv_freq_extrapolation * extrapolation_factor
    )


class NLCDRotaryEmbedding(nn.Module):
    def __init__(self, config):
        super().__init__()
        self.register_buffer("inv_freq", _yarn_inv_freq(config), persistent=False)
        p = config.rope_parameters

        def mscale(scale, m):
            return 0.1 * m * math.log(scale) + 1.0 if scale > 1.0 else 1.0

        self.attention_scaling = mscale(p["factor"], p["mscale"]) / mscale(
            p["factor"], p["mscale_all_dim"]
        )

    @torch.no_grad()
    def forward(self, position_ids: torch.Tensor, dtype: torch.dtype):
        # position_ids: [B, L] -> cos/sin [B, L, head_dim], computed in fp32.
        inv_freq = self.inv_freq[None, :, None].float().expand(position_ids.shape[0], -1, 1)
        pos = position_ids[:, None, :].float()
        freqs = (inv_freq @ pos).transpose(1, 2)
        emb = torch.cat((freqs, freqs), dim=-1)
        cos = emb.cos() * self.attention_scaling
        sin = emb.sin() * self.attention_scaling
        return cos.to(dtype), sin.to(dtype)


def _rotate_half(x):
    x1 = x[..., : x.shape[-1] // 2]
    x2 = x[..., x.shape[-1] // 2 :]
    return torch.cat((-x2, x1), dim=-1)


def _apply_rotary(q, k, cos, sin):
    cos = cos.unsqueeze(1)
    sin = sin.unsqueeze(1)
    q = (q * cos) + (_rotate_half(q) * sin)
    k = (k * cos) + (_rotate_half(k) * sin)
    return q, k


# ---------------------------------------------------------------------------
# Backbone
# ---------------------------------------------------------------------------


class NLCDRMSNorm(nn.Module):
    def __init__(self, hidden_size, eps):
        super().__init__()
        self.weight = nn.Parameter(torch.ones(hidden_size))
        self.variance_epsilon = eps

    def forward(self, x):
        dtype = x.dtype
        x = x.to(torch.float32)
        x = x * torch.rsqrt(x.pow(2).mean(-1, keepdim=True) + self.variance_epsilon)
        return self.weight * x.to(dtype)


class NLCDMLP(nn.Module):
    def __init__(self, config):
        super().__init__()
        self.gate_proj = nn.Linear(config.hidden_size, config.intermediate_size, bias=False)
        self.up_proj = nn.Linear(config.hidden_size, config.intermediate_size, bias=False)
        self.down_proj = nn.Linear(config.intermediate_size, config.hidden_size, bias=False)

    def forward(self, x):
        return self.down_proj(F.silu(self.gate_proj(x)) * self.up_proj(x))


class KVCache:
    """Per-layer clean-prefix KV cache for block-diffusion sampling."""

    def __init__(self, num_layers):
        self.keys = [None] * num_layers
        self.values = [None] * num_layers

    def seq_length(self):
        return 0 if self.keys[0] is None else self.keys[0].shape[-2]

    def read(self, layer_idx, k, v):
        """Return cache + current K/V without storing the current block."""
        if self.keys[layer_idx] is None:
            return k, v
        return (
            torch.cat([self.keys[layer_idx], k], dim=-2),
            torch.cat([self.values[layer_idx], v], dim=-2),
        )

    def write(self, layer_idx, k, v):
        """Append the current (clean) K/V to the cache and return the total."""
        k_all, v_all = self.read(layer_idx, k, v)
        self.keys[layer_idx] = k_all
        self.values[layer_idx] = v_all
        return k_all, v_all

    def trim(self, length):
        """Drop cached entries beyond `length`.

        Speculative decoding writes a whole drafted block, then keeps only the
        verified prefix; the discarded entries must not stay visible.
        """
        for i in range(len(self.keys)):
            if self.keys[i] is not None:
                self.keys[i] = self.keys[i][..., :length, :]
                self.values[i] = self.values[i][..., :length, :]


class NLCDAttention(nn.Module):
    def __init__(self, config, layer_idx):
        super().__init__()
        self.layer_idx = layer_idx
        self.head_dim = config.head_dim
        self.num_heads = config.num_attention_heads
        self.num_kv_heads = config.num_key_value_heads
        self.num_kv_groups = self.num_heads // self.num_kv_heads
        self.scaling = self.head_dim**-0.5
        self.llama4_beta = config.rope_parameters["llama_4_scaling_beta"]
        self.llama4_orig_max = config.rope_parameters["original_max_position_embeddings"]
        h = config.hidden_size
        self.q_proj = nn.Linear(h, self.num_heads * self.head_dim, bias=False)
        self.k_proj = nn.Linear(h, self.num_kv_heads * self.head_dim, bias=False)
        self.v_proj = nn.Linear(h, self.num_kv_heads * self.head_dim, bias=False)
        self.o_proj = nn.Linear(self.num_heads * self.head_dim, h, bias=False)

    def forward(self, hidden, cos, sin, storage_positions, attn_mask, cache, cache_mode):
        b, q_len, _ = hidden.shape
        q = self.q_proj(hidden).view(b, q_len, -1, self.head_dim).transpose(1, 2)
        k = self.k_proj(hidden).view(b, q_len, -1, self.head_dim).transpose(1, 2)
        v = self.v_proj(hidden).view(b, q_len, -1, self.head_dim).transpose(1, 2)
        q, k = _apply_rotary(q, k, cos, sin)

        # Long-context query scaling (identity for positions < original_max).
        scale = 1.0 + self.llama4_beta * torch.log(
            1.0 + torch.floor(storage_positions.float() / self.llama4_orig_max)
        )
        q = q * scale.view(1, 1, -1, 1).to(q.dtype)

        if cache is not None:
            if cache_mode == "write":
                k, v = cache.write(self.layer_idx, k, v)
            else:
                k, v = cache.read(self.layer_idx, k, v)

        k = k.repeat_interleave(self.num_kv_groups, dim=1)
        v = v.repeat_interleave(self.num_kv_groups, dim=1)
        out = F.scaled_dot_product_attention(q, k, v, attn_mask=attn_mask, scale=self.scaling)
        out = out.transpose(1, 2).reshape(b, q_len, -1)
        return self.o_proj(out)


class NLCDDecoderLayer(nn.Module):
    def __init__(self, config, layer_idx):
        super().__init__()
        self.self_attn = NLCDAttention(config, layer_idx)
        self.mlp = NLCDMLP(config)
        self.input_layernorm = NLCDRMSNorm(config.hidden_size, config.rms_norm_eps)
        self.post_attention_layernorm = NLCDRMSNorm(config.hidden_size, config.rms_norm_eps)

    def forward(self, hidden, cos, sin, storage_positions, attn_mask, cache, cache_mode):
        hidden = hidden + self.self_attn(
            self.input_layernorm(hidden), cos, sin, storage_positions, attn_mask, cache, cache_mode
        )
        hidden = hidden + self.mlp(self.post_attention_layernorm(hidden))
        return hidden


class NLCDEncoder(nn.Module):
    def __init__(self, config):
        super().__init__()
        self.embed_tokens = nn.Embedding(config.vocab_size, config.hidden_size)
        self.layers = nn.ModuleList(
            NLCDDecoderLayer(config, i) for i in range(config.num_hidden_layers)
        )
        self.norm = NLCDRMSNorm(config.hidden_size, config.rms_norm_eps)
        self.rotary_emb = NLCDRotaryEmbedding(config)

    def forward(self, inputs_embeds, position_ids, storage_positions, attn_mask, cache, cache_mode):
        cos, sin = self.rotary_emb(position_ids, inputs_embeds.dtype)
        hidden = inputs_embeds
        for layer in self.layers:
            hidden = layer(hidden, cos, sin, storage_positions, attn_mask, cache, cache_mode)
        return self.norm(hidden)


# ---------------------------------------------------------------------------
# Diffusion modules
# ---------------------------------------------------------------------------


class NLCDBernsteinNoiseSchedule(nn.Module):
    """Monotone degree-N Bernstein (Bezier) map t -> gamma_tilde in [0, 1].

    This is the parameterization used by the MS-SUSReg lineage: the free
    parameter is the vector of simplex increments, whose cumulative sum gives
    the Bezier control points. Uniform increments reproduce s(t) = t.
    """

    def __init__(self, degree=32):
        super().__init__()
        self.degree = int(degree)
        self.increment_values = nn.Parameter(
            torch.full((self.degree,), 1.0 / self.degree)
        )

    def increments(self):
        return self.increment_values.double()

    def control_points(self):
        inc = self.increments()
        return torch.cat((inc.new_zeros(1), inc.cumsum(dim=0)))

    @staticmethod
    def _de_casteljau(t, control_points):
        t = t.double()
        values = control_points.double().expand(t.numel(), -1)
        flat_t = t.reshape(-1, 1)
        one_minus_t = 1.0 - flat_t
        for remaining in range(control_points.numel() - 1, 0, -1):
            values = (
                one_minus_t * values[:, :remaining]
                + flat_t * values[:, 1 : remaining + 1]
            )
        return values[:, 0].reshape(t.shape)

    def forward(self, t):
        return self._de_casteljau(t, self.control_points())


class NLCDNoiseSchedule(nn.Module):
    """Legacy learned monotone map t -> gamma_tilde in [0, 1] (kept for
    checkpoint compatibility; the default edm_sigma sampler does not
    evaluate it)."""

    def __init__(self):
        super().__init__()
        self.W1 = nn.Parameter(torch.randn(1024, 1))
        self.b1 = nn.Parameter(torch.randn(1024))
        self.W2 = nn.Parameter(torch.randn(1, 1024))

    def forward(self, t):
        w1 = F.softplus(self.W1.double())
        w2 = 0.01 * F.softplus(self.W2.double())

        def g(x):
            h = x[:, None] - 0.5
            h = torch.tanh(h @ w1.T + self.b1[None, :].double())
            return (h @ w2.T)[:, 0]

        zero = torch.zeros(1, dtype=torch.float64, device=t.device)
        one = torch.ones(1, dtype=torch.float64, device=t.device)
        return (g(t.double()) - g(zero)) / (g(one) - g(zero))


class NLCDGammaBounds(nn.Module):
    """Legacy gamma endpoints stored as two scalar parameters."""

    def __init__(self, gamma_0=-3.0, gamma_1=6.0):
        super().__init__()
        self.gamma_0 = nn.Parameter(torch.tensor(float(gamma_0)))
        self.gamma_1 = nn.Parameter(torch.tensor(float(gamma_1)))

    def forward(self):
        return self.gamma_0.double(), self.gamma_1.double()


class NLCDProjectedGammaBounds(nn.Module):
    """Gamma endpoints stored as a single 2-vector (MS-SUSReg lineage)."""

    def __init__(self, gamma_0=-3.0, gamma_1=6.0):
        super().__init__()
        self.endpoint_values = nn.Parameter(
            torch.tensor([float(gamma_0), float(gamma_1)])
        )

    def forward(self):
        return (
            self.endpoint_values[0].double(),
            self.endpoint_values[1].double(),
        )


class NLCDEmbeddingMatrix(nn.Module):
    """Vocabulary embedding matrix E in R^{V x embed_dim}, rows on the unit sphere."""

    def __init__(self, vocab_size, embed_dim):
        super().__init__()
        matrix = torch.randn(vocab_size, embed_dim)
        matrix /= matrix.norm(p=2, dim=1, keepdim=True)
        self.matrix = nn.Parameter(matrix)

    def forward(self):
        m = self.matrix.float()
        return m / (torch.linalg.norm(m, dim=1, keepdim=True) + 1e-8)


def _gamma_embed(gamma, dim=64):
    freqs = torch.linspace(-5.0, 5.0, dim // 2, device=gamma.device).exp()
    ang = freqs * gamma.unsqueeze(-1)
    return torch.cat([ang.sin(), ang.cos()], dim=-1)


# ---------------------------------------------------------------------------
# Model
# ---------------------------------------------------------------------------


class NemotronLabsSigmaModel(PreTrainedModel):
    config_class = NemotronLabsSigmaConfig
    base_model_prefix = "cdlm"
    _no_split_modules = ["NLCDDecoderLayer"]
    _keys_to_ignore_on_load_unexpected = [r"ar_head\..*"]

    def __init__(self, config):
        super().__init__(config)
        self.encoder = NLCDEncoder(config)
        self.diffusion_head = nn.Linear(config.hidden_size, config.vocab_size, bias=False)
        # Two schedule parameterizations exist in the wild. The MS-SUSReg
        # lineage stores Bernstein increments and a gamma endpoint 2-vector;
        # earlier checkpoints store an MLP schedule and two gamma scalars.
        if getattr(config, "schedule_parameterization", "legacy") == "projected_bernstein":
            self.noise_schedule = NLCDBernsteinNoiseSchedule(
                degree=getattr(config, "schedule_degree", 32)
            )
            self.gamma_bounds = NLCDProjectedGammaBounds()
        else:
            self.noise_schedule = NLCDNoiseSchedule()
            self.gamma_bounds = NLCDGammaBounds()
        self.replaid_embedding_matrix = NLCDEmbeddingMatrix(config.vocab_size, config.embed_dim)
        self.replaid_input_linear = nn.Linear(config.embed_dim, config.hidden_size, bias=False)
        if config.replaid_selfcond:
            self.replaid_selfcond_linear = nn.Linear(
                config.embed_dim, config.hidden_size, bias=False
            )
        self.replaid_gamma_linear = nn.Linear(64, config.hidden_size, bias=False)
        if getattr(config, "include_ar_head", False):
            # Distilled (Phased DMD) exports preserve the separate AR readout
            # head alongside the diffusion head, per the release contract.
            # It is not evaluated by the diffusion sampling path.
            self.ar_head = nn.Linear(config.hidden_size, config.vocab_size, bias=False)
        self.post_init()

    def _init_weights(self, module):
        # Inference-only release: weights always come from the checkpoint.
        # A real initializer here is unnecessary and, on some transformers
        # versions, re-runs after checkpoint loading and corrupts the weights.
        pass

    # -- internals ----------------------------------------------------------

    @property
    def _enc_dtype(self):
        return self.diffusion_head.weight.dtype

    def _encode_clean(self, token_ids, start, position_ids, key_valid, cache):
        """Run committed tokens through the backbone causally and append to cache.

        key_valid: [B, start + L] bool validity of every cached key incl. new ones.
        """
        b, length = token_ids.shape
        device = token_ids.device
        q_global = start + torch.arange(length, device=device)
        k_global = torch.arange(start + length, device=device)
        mask = q_global[None, :, None] >= k_global[None, None, :]
        mask = mask & key_valid[:, None, :]
        return self.encoder(
            self.encoder.embed_tokens(token_ids),
            position_ids=position_ids,
            storage_positions=q_global,
            attn_mask=mask.unsqueeze(1),
            cache=cache,
            cache_mode="write",
        )

    def _denoise_block(
        self,
        z,
        gamma_t,
        cache,
        key_valid,
        block_position_ids,
        embedding_matrix,
        x_selfcond,
        guidance_scale,
    ):
        """One denoiser evaluation.

        Returns ``(cond_logits, x_guided, cond_mean, nfe)`` in fp32:

        * ``cond_logits`` - the CONDITIONAL logits. Guidance shapes the embedding
          estimate that drives the transition, never the discrete readout.
        * ``x_guided``    - the guided embedding estimate, for the transition only.
        * ``cond_mean``   - the raw conditional mean, which is what gets carried
          as self-conditioning. Guidance and score temperature are extrapolations
          and must never be fed back.

        The unconditional branch sees neither the clean context nor the
        self-conditioning signal.
        """
        cfg = self.config
        b, block, ed = z.shape
        device = z.device
        context_len = cache.seq_length()

        gamma_tok = gamma_t.reshape(1, 1).expand(b, block)
        alpha_sq = torch.sigmoid(-gamma_tok)
        sigma_sq = torch.sigmoid(gamma_tok)
        alpha = alpha_sq.sqrt()

        z_var = alpha_sq / ed + sigma_sq
        x_in = (z / z_var.sqrt().unsqueeze(-1)).float()
        h = F.linear(x_in, self.replaid_input_linear.weight.float())
        h_uncond = h                      # captured BEFORE self-conditioning
        if cfg.replaid_selfcond and x_selfcond is not None:
            h = h + F.linear(
                x_selfcond.float() * math.sqrt(ed), self.replaid_selfcond_linear.weight.float()
            )
        if not cfg.replaid_disable_time_conditioning:
            t_emb = F.linear(
                _gamma_embed(gamma_tok.float(), 64), self.replaid_gamma_linear.weight.float()
            )
            h = h + t_emb
            h_uncond = h_uncond + t_emb
        h = h.to(self._enc_dtype)
        h_uncond = h_uncond.to(self._enc_dtype)
        storage_positions = context_len + torch.arange(block, device=device)

        def head(hidden, z_local):
            logits = self.diffusion_head(hidden).float()
            if not cfg.replaid_disable_output_prior:
                z_scaled = (alpha / sigma_sq).unsqueeze(-1).float() * z_local.float()
                logits = logits + z_scaled @ embedding_matrix.t()
            return logits

        # Conditional pass: noised block attends the full clean prefix (KV cache,
        # read-only) and bidirectionally within itself.
        kv_len = context_len + block
        mask = torch.ones(b, block, kv_len, dtype=torch.bool, device=device)
        mask[:, :, :context_len] = key_valid[:, None, :]
        hidden = self.encoder(
            h,
            position_ids=block_position_ids,
            storage_positions=storage_positions,
            attn_mask=mask.unsqueeze(1),
            cache=cache,
            cache_mode="read",
        )
        logits = head(hidden, z)
        nfe = 1

        cond_mean = F.softmax(logits, dim=-1) @ embedding_matrix

        w = float(guidance_scale)
        if w != 1.0:
            # Unconditional pass: no clean context (block-only, bidirectional)
            # and no self-conditioning. RoPE is relative, so absolute offsets
            # cancel.
            hidden_u = self.encoder(
                h_uncond,
                position_ids=block_position_ids,
                storage_positions=storage_positions,
                attn_mask=None,
                cache=None,
                cache_mode=None,
            )
            logits_u = head(hidden_u, z)
            nfe += 1
            x_u = F.softmax(logits_u, dim=-1) @ embedding_matrix
            x_guided = x_u + w * (cond_mean - x_u)
        else:
            x_guided = cond_mean
        return logits, x_guided, cond_mean, nfe

    @staticmethod
    def _edm_sigma_gamma_grid(steps, gamma_0, gamma_1, rho, device):
        sigma_max = torch.exp(gamma_1 / 2.0)
        sigma_min = torch.exp(gamma_0 / 2.0)
        i = torch.arange(steps + 1, device=device, dtype=torch.float64)
        sigma = (
            sigma_max ** (1.0 / rho)
            + i / max(steps, 1) * (sigma_min ** (1.0 / rho) - sigma_max ** (1.0 / rho))
        ) ** rho
        return 2.0 * torch.log(sigma.clamp(min=1e-30))

    @staticmethod
    def _log_snr_gamma_grid(steps, gamma_0, gamma_1, device):
        # Linear interpolation in VP gamma (negative log-SNR), from gamma_1
        # (noisy) to gamma_0 (clean); matches the internal 'log_snr' schedule.
        # The grid is built in fp64: linspace otherwise falls back to the default
        # dtype and the step endpoints drift from the evaluation sampler's.
        return torch.linspace(
            gamma_1.double(), gamma_0.double(), steps + 1,
            device=device, dtype=torch.float64,
        )

    def forward(self, input_ids=None, **kwargs):
        raise NotImplementedError(
            "This model is sampled iteratively; use `model.generate(...)`."
        )

    # -- public sampling API -------------------------------------------------

    @torch.no_grad()
    def generate(
        self,
        input_ids: torch.LongTensor,
        attention_mask: Optional[torch.Tensor] = None,
        max_new_tokens: int = 128,
        steps: Optional[int] = None,
        block_length: Optional[int] = None,
        sampler: Optional[str] = None,
        score_temp: float = 0.75,
        time_rho: float = 7.0,
        time_schedule: str = "edm_sigma",
        guidance_scale: float = 1.0,
        last_step_sampling: str = "argmax",
        generator: Optional[torch.Generator] = None,
        stop_strings: Optional[list] = None,
        tokenizer=None,
    ):
        """Block-diffusion sampling.

        Args:
            input_ids: [B, prompt_len] prompt token ids (left-padded if batched;
                pass ``attention_mask`` for padded batches).
            max_new_tokens: number of tokens to generate.
            steps: denoising steps per block. The model is evaluated once per
                step plus a final readout (NFE per block = steps + 1, doubled
                when guidance_scale != 1).
            block_length: tokens decoded in parallel per block.
            sampler: 'ddpm' (ancestral, default) or 'ddim' (deterministic).
            score_temp: epsilon rescale (legacy score temperature). 1.0 = off.
            guidance_scale: classifier-free guidance in clean-embedding space
                (1.0 = off; costs one extra forward per step).
            last_step_sampling: 'argmax' or 'softmax' readout at the final step.
            generator: optional torch.Generator for reproducible sampling.
            time_schedule: 'edm_sigma' (Karras rho-warped grid) or 'log_snr'
                (linear in gamma).

        Recommended settings (match the internal evaluation recipes):
            sampler='ddim', time_schedule='log_snr', block_length=32,
            steps=32, guidance_scale=3.0, score_temp=0.3 (0.2 at steps>=64). DDPM at 64 steps or fewer often degenerates
            with these presets; prefer DDIM.

        Returns:
            (token_ids [B, prompt_len + max_new_tokens], nfe)

        Distilled (Phased DMD) variants: when the config carries
        ``native_family='phased_dmd'`` the sampling contract is fixed by the
        checkpoint. ``steps`` defaults to ``config.native_nfe`` and may not be
        overridden (an untrained phase endpoint would be evaluated).
        sampler='fresh_x0' (each transition re-noises the current clean
        prediction with fresh Gaussian noise at the next level), log_snr
        schedule, guidance 1.0, score_temp 1.0, 32-token blocks and argmax
        readout are the native settings; see ``generation_config.json``.

        Stopping: there is no token-ID EOS stopping. If ``stop_strings`` and
        ``tokenizer`` are given (batch size 1), the decoded generation is
        checked after each completed block, before the cache advances, and
        sampling stops once any stop string appears; the returned sequence is
        then trimmed to the tokens actually generated. Otherwise the model
        always fills ``max_new_tokens`` tokens.
        """
        native = getattr(self.config, "native_family", None) == "phased_dmd"
        if native:
            native_nfe = int(self.config.native_nfe)
            if steps is None:
                steps = native_nfe
            if steps != native_nfe:
                raise ValueError(
                    f"This Phased DMD distilled variant is trained for exactly "
                    f"NFE={native_nfe}; an arbitrary NFE override would evaluate "
                    f"an untrained phase endpoint. Pass steps={native_nfe} or "
                    f"steps=None."
                )
            if sampler is None:
                sampler = "fresh_x0"
        if steps is None:
            steps = 32
        if sampler is None:
            sampler = "ddpm"
        if sampler not in ("ddpm", "ddim", "fresh_x0"):
            raise ValueError("sampler must be 'ddpm', 'ddim' or 'fresh_x0'.")
        if sampler == "fresh_x0" and not native:
            raise ValueError(
                "sampler='fresh_x0' is the native sampler of Phased DMD "
                "distilled variants (config.native_family='phased_dmd')."
            )
        if stop_strings is not None:
            if tokenizer is None:
                raise ValueError("stop_strings requires a tokenizer.")
            if input_ids.shape[0] != 1:
                raise ValueError("stop-string stopping supports batch size 1.")
            stop_strings = [str(x) for x in stop_strings]
        if time_schedule not in ("edm_sigma", "log_snr"):
            raise ValueError("time_schedule must be 'edm_sigma' or 'log_snr'.")
        if max_new_tokens <= 0:
            return input_ids, 0
        device = input_ids.device
        b, prompt_len = input_ids.shape
        if block_length is None:
            block_length = self.config.block_size if native else 64
        block = int(block_length)

        if attention_mask is None:
            key_valid = torch.ones(b, prompt_len, dtype=torch.bool, device=device)
        else:
            key_valid = attention_mask.to(device=device, dtype=torch.bool)
        prompt_position_ids = (key_valid.long().cumsum(dim=1) - 1).clamp_min(0)
        prompt_lengths = key_valid.long().sum(dim=1)

        gamma_0, gamma_1 = self.gamma_bounds()
        embedding_matrix = self.replaid_embedding_matrix().float()
        if time_schedule == "log_snr":
            gamma_grid = self._log_snr_gamma_grid(steps, gamma_0, gamma_1, device)
        else:
            gamma_grid = self._edm_sigma_gamma_grid(steps, gamma_0, gamma_1, time_rho, device)

        cache = KVCache(self.config.num_hidden_layers)
        self._encode_clean(input_ids, 0, prompt_position_ids, key_valid, cache)

        pad_id = self.config.pad_token_id if self.config.pad_token_id is not None else 0
        clean_ids = input_ids.clone()
        generated = 0
        nfe = 0
        num_blocks = math.ceil(max_new_tokens / block)

        for block_idx in range(num_blocks):
            clean_ids = torch.cat(
                [clean_ids, torch.full((b, block), pad_id, dtype=clean_ids.dtype, device=device)],
                dim=1,
            )
            block_start = clean_ids.shape[1] - block
            block_position_ids = (
                prompt_lengths[:, None]
                + generated
                + torch.arange(block, device=device, dtype=torch.long)[None, :]
            )

            z = torch.randn(b, block, self.config.embed_dim, device=device,
                            dtype=torch.float64, generator=generator)
            x_selfcond = None

            for i in range(steps + 1):
                gamma_t = gamma_grid[i : i + 1]
                logits, x_reconst, cond_mean, used = self._denoise_block(
                    z, gamma_t, cache, key_valid, block_position_ids,
                    embedding_matrix, x_selfcond, guidance_scale,
                )
                nfe += used

                if i == steps:
                    if last_step_sampling == "softmax":
                        probs = F.softmax(logits, dim=-1)
                        token_ids = torch.multinomial(
                            probs.reshape(-1, probs.shape[-1]), 1, generator=generator
                        ).reshape(b, block)
                    else:
                        token_ids = logits.argmax(dim=-1)
                    clean_ids[:, block_start : block_start + block] = token_ids
                    generated += block
                    break

                # Guidance and score temperature are extrapolations; the
                # self-conditioning signal is the raw conditional mean.
                x_selfcond = cond_mean.detach().float()

                alpha_sq_t = torch.sigmoid(-gamma_t)
                sigma_t = torch.sigmoid(gamma_t).sqrt()
                alpha_t = alpha_sq_t.sqrt()
                x64 = x_reconst.double()
                epsilon = (z - alpha_t * x64) / sigma_t.clamp(min=1e-8)
                if score_temp != 1.0:
                    epsilon = epsilon / float(score_temp)
                    x64 = (z - sigma_t * epsilon) / alpha_t.clamp(min=1e-8)

                gamma_s = gamma_grid[i + 1 : i + 2]
                alpha_sq_s = torch.sigmoid(-gamma_s)
                alpha_s = alpha_sq_s.sqrt()
                sigma_s = torch.sigmoid(gamma_s).sqrt()
                if sampler == "ddpm":
                    c = -torch.expm1(gamma_s - gamma_t)
                    noise = torch.randn(z.shape, device=device, dtype=z.dtype,
                                        generator=generator)
                    z = (
                        (1.0 - c) * (alpha_sq_s / alpha_sq_t).sqrt() * z
                        + c * alpha_s * x64
                        + (c * (1.0 - alpha_sq_s)).clamp(min=0).sqrt() * noise
                    )
                elif sampler == "fresh_x0":
                    # Native Phased DMD transition: re-noise the current clean
                    # prediction with FRESH Gaussian noise at the next level
                    # ('fresh_call' transport). Ported from the pinned runtime
                    # contract; see provenance/parity receipts.
                    noise = torch.randn(z.shape, device=device, dtype=z.dtype,
                                        generator=generator)
                    z = alpha_s * x64 + sigma_s * noise
                else:  # ddim
                    z = alpha_s * x64 + sigma_s * epsilon

            # Delimiter stopping: inspect the decoded generation after each
            # completed block, before the cache advances (matches the release
            # evaluation harness semantics).
            if stop_strings:
                text = tokenizer.decode(
                    clean_ids[0, prompt_len : prompt_len + min(generated, max_new_tokens)].tolist(),
                    skip_special_tokens=True,
                )
                if any(delimiter in text for delimiter in stop_strings):
                    break

            if block_idx + 1 < num_blocks:
                new_valid = torch.ones(b, block, dtype=torch.bool, device=device)
                key_valid = torch.cat([key_valid, new_valid], dim=1)
                self._encode_clean(
                    clean_ids[:, block_start : block_start + block],
                    block_start,
                    block_position_ids,
                    key_valid,
                    cache,
                )

        return clean_ids[:, : prompt_len + min(generated, max_new_tokens)], nfe

    # -- self-speculative decoding ------------------------------------------

    @torch.no_grad()
    def generate_speculative(
        self,
        input_ids: torch.LongTensor,
        attention_mask: Optional[torch.Tensor] = None,
        max_new_tokens: int = 128,
        draft_width: Optional[int] = None,
        diffusion_calls_per_round: int = 1,
        stop_strings: Optional[list] = None,
        tokenizer=None,
        generator: Optional[torch.Generator] = None,
        return_stats: bool = False,
    ):
        """Self-speculative decoding: the diffusion head drafts, the AR head verifies.

        One backbone carries both streams, so the model is its own drafter. Each
        round runs `diffusion_calls_per_round` denoiser call(s) from pure noise to
        propose a block of `draft_width` tokens, scores that block with the AR head
        in a single causal pass, keeps the longest prefix on which the two agree,
        and appends one token of the AR head's own choosing.

        **The result is exactly the model's greedy AR output** -- acceptance only
        changes how many tokens each round commits, never which tokens. Speed, not
        quality, is what varies.

        Drafts never use self-conditioning and never use guidance, matching the
        serving contract these checkpoints were trained and evaluated under.

        Returns `(ids, stats)` when `return_stats`, else `ids`. `stats` reports
        `rounds`, `accepted` (drafted tokens accepted, excluding bonus tokens),
        `committed`, and `mean_accepted_length` -- the paper's AL, which counts
        accepted draft tokens per round and excludes the bonus token.
        """
        if not getattr(self.config, "include_ar_head", False) or not hasattr(self, "ar_head"):
            raise ValueError(
                "Self-speculative decoding needs the AR verification head. This "
                "checkpoint ships diffusion weights only; use generate() instead."
            )
        if input_ids.shape[0] != 1:
            raise ValueError("Self-speculative decoding supports batch size 1.")
        if stop_strings is not None and tokenizer is None:
            raise ValueError("stop_strings requires a tokenizer.")
        if max_new_tokens <= 0:
            return (input_ids, {}) if return_stats else input_ids

        gen_cfg = getattr(self, "generation_config", None)
        if draft_width is None:
            draft_width = int(getattr(gen_cfg, "draft_width", 0) or self.config.block_size)
        block = int(draft_width)
        device = input_ids.device
        b = 1

        if attention_mask is None:
            key_valid = torch.ones(b, input_ids.shape[1], dtype=torch.bool, device=device)
        else:
            key_valid = attention_mask.to(device=device, dtype=torch.bool)
        prompt_position_ids = (key_valid.long().cumsum(dim=1) - 1).clamp_min(0)
        prompt_lengths = key_valid.long().sum(dim=1)
        prompt_len = input_ids.shape[1]

        gamma_0, gamma_1 = self.gamma_bounds()
        embedding_matrix = self.replaid_embedding_matrix().float()
        grid = self._log_snr_gamma_grid(diffusion_calls_per_round, gamma_0, gamma_1, device)

        cache = KVCache(self.config.num_hidden_layers)
        hidden = self._encode_clean(input_ids, 0, prompt_position_ids, key_valid, cache)
        # AR prediction for the next position comes from the last committed token.
        next_ar = self.ar_head(hidden[:, -1]).argmax(dim=-1)        # [B]

        clean_ids = input_ids.clone()
        rounds = accepted_total = committed = 0

        while committed < max_new_tokens:
            committed_len = clean_ids.shape[1]
            block_position_ids = (
                prompt_lengths[:, None]
                + committed
                + torch.arange(block, device=device, dtype=torch.long)[None, :]
            )

            # 1. Draft: denoise a whole block from pure noise. No self-conditioning,
            #    no guidance -- the drafts were trained and served that way.
            z = torch.randn(b, block, self.config.embed_dim, device=device,
                            dtype=torch.float64, generator=generator)
            x_selfcond = None
            for i in range(diffusion_calls_per_round):
                logits, x_reconst, _cond_mean, _ = self._denoise_block(
                    z, grid[i : i + 1], cache, key_valid, block_position_ids,
                    embedding_matrix, x_selfcond, 1.0,
                )
                if i + 1 < diffusion_calls_per_round:
                    gamma_s = grid[i + 1 : i + 2]
                    noise = torch.randn(z.shape, device=device, dtype=z.dtype,
                                        generator=generator)
                    z = (torch.sigmoid(-gamma_s).sqrt() * x_reconst.double()
                         + torch.sigmoid(gamma_s).sqrt() * noise)
            draft = logits.argmax(dim=-1)                            # [B, block]

            # 2. Verify: one causal pass over the draft, writing to the cache. The
            #    accepted prefix keeps its keys; the rest is trimmed below.
            draft_valid = torch.cat(
                [key_valid, torch.ones(b, block, dtype=torch.bool, device=device)], dim=1
            )
            h = self._encode_clean(draft, committed_len, block_position_ids, draft_valid, cache)
            ar_pred = self.ar_head(h).argmax(dim=-1)                 # [B, block]

            # 3. Accept the longest agreeing prefix. next_ar predicts draft[0];
            #    ar_pred[j] predicts draft[j+1].
            expected = torch.cat([next_ar[:, None], ar_pred[:, :-1]], dim=1)
            agree = (draft == expected)[0]
            k = int(torch.cumprod(agree.long(), dim=0).sum().item())  # leading run of True
            bonus = (next_ar if k == 0 else ar_pred[:, k - 1])        # AR's own token

            take = min(k + 1, max_new_tokens - committed)
            new_ids = torch.cat([draft[:, :k], bonus[:, None]], dim=1)[:, :take]
            clean_ids = torch.cat([clean_ids, new_ids], dim=1)
            accepted_total += min(k, take)
            committed += take
            rounds += 1

            # 4. Cache: keep the verified prefix, drop the rest, then encode the
            #    bonus token (a different id at that position, so its keys differ).
            cache.trim(committed_len + min(k, take))
            key_valid = torch.cat(
                [key_valid, torch.ones(b, min(k, take), dtype=torch.bool, device=device)], dim=1
            )
            if take == k + 1:
                bonus_pos = prompt_lengths[:, None] + (committed - 1)
                key_valid = torch.cat(
                    [key_valid, torch.ones(b, 1, dtype=torch.bool, device=device)], dim=1
                )
                hidden = self._encode_clean(
                    bonus[:, None], clean_ids.shape[1] - 1, bonus_pos, key_valid, cache
                )
                next_ar = self.ar_head(hidden[:, -1]).argmax(dim=-1)
            elif k > 0:
                next_ar = ar_pred[:, take - 1]

            if stop_strings:
                text = tokenizer.decode(
                    clean_ids[0, prompt_len:].tolist(), skip_special_tokens=True
                )
                if any(s in text for s in stop_strings):
                    break

        out = clean_ids[:, : prompt_len + min(committed, max_new_tokens)]
        if not return_stats:
            return out
        return out, {
            "rounds": rounds,
            "accepted": accepted_total,
            "committed": committed,
            "mean_accepted_length": (accepted_total / rounds) if rounds else 0.0,
        }
