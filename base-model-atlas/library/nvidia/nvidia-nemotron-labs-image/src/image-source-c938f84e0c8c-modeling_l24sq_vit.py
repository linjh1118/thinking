# SPDX-FileCopyrightText: Copyright (c) 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: LicenseRef-NvidiaProprietary
#
# Use of this file is governed by the NVIDIA License in the repository root
# (LICENSE).

"""HuggingFace-style model for the L24-SQ Llama ViT tokenizer.

Self-contained: the encoder/decoder/quantizer modules below mirror
`transcoder.models.llamabsqvit_anyres` but do not import the training tree.

The top-level class :class:`L24SQViTModel` is a :class:`transformers.PreTrainedModel`
subclass and exposes the practical inference APIs:

* :meth:`encode` / :meth:`decode` — single-shape (B, 3, H, W) tensor batches.
* :meth:`pack_encode` / :meth:`pack_decode` — variable-resolution batches
  served by FlashAttention varlen kernels (packing attention). Inputs and
  outputs are Python lists of per-image tensors.
* :meth:`batch_encode` / :meth:`batch_decode` — variable-resolution batches
  padded to the same spatial size and processed with standard batched
  attention (no FlashAttention dependency). Inputs are Python lists of
  per-image tensors; outputs mirror the ``encode`` / ``decode`` dict format
  plus per-image ``grid_sizes`` for automatic output cropping.
* :meth:`reconstruct` / :meth:`reconstruct_packed` — encode→decode shortcuts.
* :meth:`preprocess_image` / :meth:`postprocess_image` — pad/normalise helpers
  matching the training-time data pipeline.

All tokenisation outputs are integer codebook indices (long tensors) plus the
patch-grid sizes, so they can be fed straight into downstream LMs.
"""

from __future__ import annotations

from contextlib import nullcontext
from typing import Iterable, List, Optional, Sequence, Tuple, Union

import torch
import torch.nn as nn
import torch.nn.functional as F
from einops import rearrange
from transformers import PreTrainedModel

from .configuration_l24sq_vit import L24SQViTConfig

try:
    from flash_attn import flash_attn_varlen_func  # type: ignore

    HAS_FLASH_ATTN = True
except ImportError:  # pragma: no cover - optional dependency
    flash_attn_varlen_func = None
    HAS_FLASH_ATTN = False


# ---------------------------------------------------------------------------
# RoPE + attention primitives
# ---------------------------------------------------------------------------


def build_2d_rope_cache(
    grid_h: int,
    grid_w: int,
    head_dim: int,
    theta: float = 10000.0,
    device: Optional[torch.device] = None,
    dtype: torch.dtype = torch.float32,
) -> Tuple[torch.Tensor, torch.Tensor]:
    assert head_dim % 4 == 0, f"head_dim must be divisible by 4, got {head_dim}"
    dim_half = head_dim // 2
    dim_quarter = head_dim // 4

    inv_freq = 1.0 / (
        theta ** (torch.arange(0, dim_quarter, device=device, dtype=torch.float32) * 2 / dim_half)
    )
    h_pos = torch.arange(grid_h, device=device, dtype=torch.float32)
    w_pos = torch.arange(grid_w, device=device, dtype=torch.float32)

    angles_h = torch.outer(h_pos, inv_freq)
    angles_w = torch.outer(w_pos, inv_freq)
    angles_h = angles_h[:, None, :].expand(grid_h, grid_w, dim_quarter).reshape(-1, dim_quarter)
    angles_w = angles_w[None, :, :].expand(grid_h, grid_w, dim_quarter).reshape(-1, dim_quarter)

    emb_h = torch.cat([angles_h, angles_h], dim=-1)
    emb_w = torch.cat([angles_w, angles_w], dim=-1)
    cos = torch.cat([emb_h.cos(), emb_w.cos()], dim=-1)
    sin = torch.cat([emb_h.sin(), emb_w.sin()], dim=-1)
    return cos.to(dtype=dtype), sin.to(dtype=dtype)


def _rotate_half(x: torch.Tensor) -> torch.Tensor:
    x1, x2 = x.chunk(2, dim=-1)
    return torch.cat([-x2, x1], dim=-1)


def _rotate_half_2d(x: torch.Tensor) -> torch.Tensor:
    d = x.shape[-1]
    return torch.cat(
        [_rotate_half(x[..., : d // 2]), _rotate_half(x[..., d // 2 :])],
        dim=-1,
    )


def apply_2d_rope_packed(q: torch.Tensor, k: torch.Tensor, cos: torch.Tensor, sin: torch.Tensor):
    cos = cos[:, None, :].to(q.dtype)
    sin = sin[:, None, :].to(q.dtype)
    q = q * cos + _rotate_half_2d(q) * sin
    k = k * cos + _rotate_half_2d(k) * sin
    return q, k


def build_cu_seqlens(lengths: Sequence[int], device: torch.device) -> torch.Tensor:
    cu = [0]
    total = 0
    for length in lengths:
        total += int(length)
        cu.append(total)
    return torch.tensor(cu, dtype=torch.int32, device=device)


def split_packed(x: torch.Tensor, lengths: Sequence[int]) -> List[torch.Tensor]:
    outputs = []
    start = 0
    for length in lengths:
        end = start + int(length)
        outputs.append(x[start:end])
        start = end
    return outputs


# ---------------------------------------------------------------------------
# Llama-style transformer blocks (packed / varlen)
# ---------------------------------------------------------------------------


class RMSNorm(nn.Module):
    def __init__(self, dim: int, eps: float = 1e-6):
        super().__init__()
        self.eps = eps
        self.weight = nn.Parameter(torch.ones(dim))

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x_float = x.float()
        normed = x_float * torch.rsqrt(x_float.pow(2).mean(-1, keepdim=True) + self.eps)
        return normed.to(dtype=x.dtype) * self.weight.to(dtype=x.dtype)


class SwiGLUMLP(nn.Module):
    def __init__(self, dim: int, mlp_ratio: float = 4.0):
        super().__init__()
        raw_hidden = int(dim * mlp_ratio * 2 / 3)
        hidden = (raw_hidden + 63) // 64 * 64
        self.gate_proj = nn.Linear(dim, hidden, bias=False)
        self.up_proj = nn.Linear(dim, hidden, bias=False)
        self.down_proj = nn.Linear(hidden, dim, bias=False)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.down_proj(F.silu(self.gate_proj(x)) * self.up_proj(x))


class PackedLlamaSelfAttention(nn.Module):
    def __init__(self, dim: int, num_heads: int):
        super().__init__()
        assert dim % num_heads == 0
        self.num_heads = num_heads
        self.head_dim = dim // num_heads
        self.dim = dim
        self.q_proj = nn.Linear(dim, dim, bias=False)
        self.k_proj = nn.Linear(dim, dim, bias=False)
        self.v_proj = nn.Linear(dim, dim, bias=False)
        self.out_proj = nn.Linear(dim, dim, bias=False)

    def forward(
        self,
        x: torch.Tensor,
        cu_seqlens: torch.Tensor,
        max_seqlen: int,
        cos: torch.Tensor,
        sin: torch.Tensor,
    ) -> torch.Tensor:
        q = self.q_proj(x).reshape(x.shape[0], self.num_heads, self.head_dim)
        k = self.k_proj(x).reshape(x.shape[0], self.num_heads, self.head_dim)
        v = self.v_proj(x).reshape(x.shape[0], self.num_heads, self.head_dim)
        q, k = apply_2d_rope_packed(q, k, cos, sin)

        if HAS_FLASH_ATTN and x.is_cuda and q.dtype in (torch.float16, torch.bfloat16):
            out = flash_attn_varlen_func(
                q.contiguous(),
                k.contiguous(),
                v.contiguous(),
                cu_seqlens_q=cu_seqlens,
                cu_seqlens_k=cu_seqlens,
                max_seqlen_q=max_seqlen,
                max_seqlen_k=max_seqlen,
                dropout_p=0.0,
                causal=False,
            )
        else:
            parts = []
            for start, end in zip(cu_seqlens[:-1].tolist(), cu_seqlens[1:].tolist()):
                q_i = q[start:end].transpose(0, 1).unsqueeze(0)
                k_i = k[start:end].transpose(0, 1).unsqueeze(0)
                v_i = v[start:end].transpose(0, 1).unsqueeze(0)
                out_i = F.scaled_dot_product_attention(q_i, k_i, v_i, dropout_p=0.0, is_causal=False)
                parts.append(out_i.squeeze(0).transpose(0, 1))
            out = torch.cat(parts, dim=0)

        out = out.reshape(x.shape[0], self.dim)
        return self.out_proj(out)


class PackedLlamaViTBlock(nn.Module):
    def __init__(self, dim: int, num_heads: int, mlp_ratio: float = 4.0):
        super().__init__()
        self.norm1 = RMSNorm(dim)
        self.attn = PackedLlamaSelfAttention(dim, num_heads)
        self.norm2 = RMSNorm(dim)
        self.mlp = SwiGLUMLP(dim, mlp_ratio)

    def forward(
        self,
        x: torch.Tensor,
        cu_seqlens: torch.Tensor,
        max_seqlen: int,
        cos: torch.Tensor,
        sin: torch.Tensor,
    ) -> torch.Tensor:
        x = x + self.attn(self.norm1(x), cu_seqlens, max_seqlen, cos, sin)
        x = x + self.mlp(self.norm2(x))
        return x


# ---------------------------------------------------------------------------
# Encoder / decoder
# ---------------------------------------------------------------------------


class LlamaTransformerEncoder(nn.Module):
    def __init__(
        self,
        patch_size: int,
        width: int,
        layers: int,
        heads: int,
        mlp_ratio: float,
        vit_rope_theta: float = 10000.0,
    ):
        super().__init__()
        self.patch_size = (patch_size, patch_size)
        self.width = width
        self.head_dim = width // heads
        self.rope_theta = vit_rope_theta
        self._rope_cache: dict = {}

        self.patch_embed = nn.Conv2d(
            in_channels=3,
            out_channels=width,
            kernel_size=self.patch_size,
            stride=self.patch_size,
            bias=True,
        )
        self.blocks = nn.ModuleList(
            [PackedLlamaViTBlock(width, heads, mlp_ratio) for _ in range(layers)]
        )
        self.norm = RMSNorm(width)

    def _get_rope_cache(self, grid_size, device: torch.device, dtype: torch.dtype):
        key = (grid_size[0], grid_size[1], device.type, device.index, dtype)
        if key not in self._rope_cache:
            self._rope_cache[key] = build_2d_rope_cache(
                grid_size[0], grid_size[1], self.head_dim, self.rope_theta, device=device, dtype=dtype
            )
        return self._rope_cache[key]

    def _build_rope(self, grid_sizes, device, dtype):
        cos_parts, sin_parts = [], []
        for grid_size in grid_sizes:
            cos, sin = self._get_rope_cache(grid_size, device, dtype)
            cos_parts.append(cos)
            sin_parts.append(sin)
        return torch.cat(cos_parts, dim=0), torch.cat(sin_parts, dim=0)

    def _pack(self, x):
        if isinstance(x, torch.Tensor):
            feat = self.patch_embed(x)
            batch, _, gh, gw = feat.shape
            lengths = [gh * gw] * batch
            grid_sizes = [(gh, gw)] * batch
            packed = rearrange(feat, "b c h w -> (b h w) c")
            return packed, lengths, grid_sizes, False

        packed_parts, lengths, grid_sizes = [], [], []
        for image in x:
            feat = self.patch_embed(image.unsqueeze(0))
            gh, gw = feat.shape[-2:]
            packed_parts.append(rearrange(feat, "1 c h w -> (h w) c"))
            lengths.append(gh * gw)
            grid_sizes.append((gh, gw))
        return torch.cat(packed_parts, dim=0), lengths, grid_sizes, True

    def forward(self, x):
        packed, lengths, grid_sizes, input_is_list = self._pack(x)
        cu_seqlens = build_cu_seqlens(lengths, packed.device)
        max_seqlen = max(lengths)
        cos, sin = self._build_rope(grid_sizes, packed.device, packed.dtype)
        for block in self.blocks:
            packed = block(packed, cu_seqlens, max_seqlen, cos, sin)
        packed = self.norm(packed)
        meta = {
            "lengths": lengths,
            "grid_sizes": grid_sizes,
            "input_is_list": input_is_list,
            "batch_size": len(lengths),
        }
        if not input_is_list:
            seq_len = lengths[0]
            packed = packed.view(meta["batch_size"], seq_len, -1)
        return packed, meta


class LlamaTransformerDecoder(nn.Module):
    def __init__(
        self,
        patch_size: int,
        width: int,
        layers: int,
        heads: int,
        mlp_ratio: float,
        use_ffn_output: bool = True,
        dim_ffn_output: int = 3072,
        vit_rope_theta: float = 10000.0,
        out_inner_feat: bool = False,
        out_inner_depth: Optional[int] = None,
        out_inner_dim: Optional[int] = None,
    ):
        super().__init__()
        self.patch_size = (patch_size, patch_size)
        self.width = width
        self.head_dim = width // heads
        self.rope_theta = vit_rope_theta
        self.out_inner_feat = out_inner_feat
        self.out_inner_depth = out_inner_depth
        self._rope_cache: dict = {}

        self.blocks = nn.ModuleList(
            [PackedLlamaViTBlock(width, heads, mlp_ratio) for _ in range(layers)]
        )
        if self.out_inner_feat:
            if out_inner_dim is None or out_inner_depth is None:
                raise ValueError("out_inner_dim/out_inner_depth required when out_inner_feat=True")
            self.distill_mlp = nn.Sequential(
                nn.Linear(width, width * 4),
                nn.SiLU(),
                nn.Linear(width * 4, width * 4),
                nn.SiLU(),
                nn.Linear(width * 4, out_inner_dim),
            )
        self.norm = RMSNorm(width)
        self.use_ffn_output = use_ffn_output
        if use_ffn_output:
            self.ffn = nn.Sequential(nn.Linear(width, dim_ffn_output), nn.Tanh())
            conv_in_features = dim_ffn_output
        else:
            self.ffn = nn.Identity()
            conv_in_features = width
        self.conv_out = nn.Linear(
            conv_in_features, 3 * self.patch_size[0] * self.patch_size[1], bias=True
        )

    def _get_rope_cache(self, grid_size, device, dtype):
        key = (grid_size[0], grid_size[1], device.type, device.index, dtype)
        if key not in self._rope_cache:
            self._rope_cache[key] = build_2d_rope_cache(
                grid_size[0], grid_size[1], self.head_dim, self.rope_theta, device=device, dtype=dtype
            )
        return self._rope_cache[key]

    def _build_rope(self, grid_sizes, device, dtype):
        cos_parts, sin_parts = [], []
        for grid_size in grid_sizes:
            cos, sin = self._get_rope_cache(grid_size, device, dtype)
            cos_parts.append(cos)
            sin_parts.append(sin)
        return torch.cat(cos_parts, dim=0), torch.cat(sin_parts, dim=0)

    def _pack(self, x, grid_sizes):
        if x.ndim == 3:
            batch, seq_len, dim = x.shape
            grid = grid_sizes[0] if isinstance(grid_sizes, (list, tuple)) else grid_sizes
            if grid[0] * grid[1] != seq_len:
                raise ValueError(f"grid_size {grid} mismatches token count {seq_len}")
            return (
                x.reshape(batch * seq_len, dim),
                [seq_len] * batch,
                [tuple(grid)] * batch,
                False,
            )
        if x.ndim == 2:
            lengths = [gh * gw for gh, gw in grid_sizes]
            return x, lengths, [tuple(g) for g in grid_sizes], True
        raise ValueError(f"Unsupported decoder input shape {tuple(x.shape)}")

    def _unpack(self, packed: torch.Tensor, grid_sizes):
        images = []
        lengths = [gh * gw for gh, gw in grid_sizes]
        for tokens, (gh, gw) in zip(split_packed(packed, lengths), grid_sizes):
            image = rearrange(
                tokens,
                "(hh ww) (c sh sw) -> c (hh sh) (ww sw)",
                hh=gh,
                ww=gw,
                sh=self.patch_size[0],
                sw=self.patch_size[1],
            )
            images.append(image)
        return images

    def forward(self, x: torch.Tensor, grid_sizes):
        x, lengths, grid_sizes, return_list = self._pack(x, grid_sizes)
        cu_seqlens = build_cu_seqlens(lengths, x.device)
        max_seqlen = max(lengths)
        cos, sin = self._build_rope(grid_sizes, x.device, x.dtype)

        for block in self.blocks:
            x = block(x, cu_seqlens, max_seqlen, cos, sin)
        x = self.norm(x)
        x = self.ffn(x)
        x = self.conv_out(x)
        images = self._unpack(x, grid_sizes)
        if not return_list:
            return torch.stack(images, dim=0)
        return images


# ---------------------------------------------------------------------------
# Vector quantizer (inference-only forward path)
# ---------------------------------------------------------------------------


class VectorQuantizer(nn.Module):
    def __init__(self, n_embed: int, embed_dim: int, l2_norm: bool = True):
        super().__init__()
        self.n_embed = n_embed
        self.embed_dim = embed_dim
        self.l2_norm = l2_norm
        self.embedding = nn.Embedding(n_embed, embed_dim)

    @torch.no_grad()
    def encode(self, z: torch.Tensor, chunk_size: int = 4096) -> torch.Tensor:
        """z: [N, D] → indices [N]

        The nearest-neighbour search produces an [N, codebook_size] distance
        matrix.  With a large codebook (196 560 entries) this becomes the
        dominant memory consumer.  ``chunk_size`` caps the rows materialised at
        once: peak extra memory is ``chunk_size × codebook_size × 4`` bytes
        (≈ 3.2 GB at the default of 4 096), regardless of total token count.
        """
        if self.l2_norm:
            z = F.normalize(z, dim=-1)
            cb = F.normalize(self.embedding.weight, dim=-1)
            if z.shape[0] <= chunk_size:
                return torch.argmin(-z @ cb.t(), dim=1)
            return torch.cat([
                torch.argmin(-z[i:i + chunk_size] @ cb.t(), dim=1)
                for i in range(0, z.shape[0], chunk_size)
            ])
        else:
            cb_sq = torch.sum(self.embedding.weight ** 2, dim=1)
            if z.shape[0] <= chunk_size:
                d = (torch.sum(z ** 2, dim=1, keepdim=True) + cb_sq
                     - 2 * z @ self.embedding.weight.t())
                return torch.argmin(d, dim=1)
            return torch.cat([
                torch.argmin(
                    torch.sum(z[i:i + chunk_size] ** 2, dim=1, keepdim=True) + cb_sq
                    - 2 * z[i:i + chunk_size] @ self.embedding.weight.t(),
                    dim=1,
                )
                for i in range(0, z.shape[0], chunk_size)
            ])

    def lookup(self, indices: torch.Tensor) -> torch.Tensor:
        z_q = self.embedding(indices)
        if self.l2_norm:
            z_q = F.normalize(z_q, dim=-1)
        return z_q


# ---------------------------------------------------------------------------
# HuggingFace PreTrainedModel wrapper
# ---------------------------------------------------------------------------


class L24SQViTModel(PreTrainedModel):
    """Vector-quantised Llama-ViT image tokenizer (Leech-lattice codebook)."""

    config_class = L24SQViTConfig
    base_model_prefix = "l24sq_vit"
    main_input_name = "pixel_values"
    supports_gradient_checkpointing = False

    def __init__(self, config: L24SQViTConfig):
        super().__init__(config)
        self.encoder = LlamaTransformerEncoder(
            patch_size=config.patch_size,
            width=config.width,
            layers=config.layers,
            heads=config.heads,
            mlp_ratio=config.mlp_ratio,
            vit_rope_theta=config.vit_rope_theta,
        )
        self.decoder = LlamaTransformerDecoder(
            patch_size=config.patch_size,
            width=config.width,
            layers=config.layers,
            heads=config.heads,
            mlp_ratio=config.mlp_ratio,
            use_ffn_output=config.use_ffn_output,
            dim_ffn_output=config.dim_ffn_output,
            vit_rope_theta=config.vit_rope_theta,
            out_inner_feat=config.distill_depth is not None,
            out_inner_depth=config.distill_depth,
            out_inner_dim=config.distill_output_dim,
        )
        self.quantize = VectorQuantizer(
            n_embed=config.n_embed, embed_dim=config.embed_dim, l2_norm=config.l2_norm
        )
        self.quant_embed = nn.Linear(config.width, config.embed_dim)
        self.post_quant_embed = nn.Linear(config.embed_dim, config.width)

        self.post_init()

    # ---- meta helpers ----------------------------------------------------

    @property
    def patch_size(self) -> int:
        return self.config.patch_size

    @property
    def size_divisor(self) -> int:
        return int(self.config.size_divisor)

    @property
    def codebook_size(self) -> int:
        return int(self.config.n_embed)

    # ---- image (pre|post)processing -------------------------------------

    def preprocess_image(
        self,
        image: torch.Tensor,
        input_range: str = "unit",
        pad_mode: str = "replicate",
    ) -> torch.Tensor:
        """Normalise a ``[3, H, W]`` image tensor and pad to the patch grid.

        Args:
            image: ``[C, H, W]`` float tensor.
            input_range: ``"unit"`` if pixels are in ``[0, 1]`` (e.g. from
                ``torchvision.transforms.ToTensor``); ``"signed"`` if they are
                already in ``[-1, 1]``. Conversion follows ``config.zero_mean``.
            pad_mode: passed to ``F.pad`` for size-divisor padding.
        """
        if image.ndim != 3:
            raise ValueError(f"Expected [C, H, W] tensor, got {tuple(image.shape)}")
        if input_range not in ("unit", "signed"):
            raise ValueError(f"input_range must be 'unit' or 'signed', got {input_range}")
        x = image
        if self.config.zero_mean and input_range == "unit":
            x = x * 2.0 - 1.0
        elif not self.config.zero_mean and input_range == "signed":
            x = (x + 1.0) * 0.5
        return _pad_to_multiple(x, self.size_divisor, pad_mode=pad_mode)

    def postprocess_image(self, image: torch.Tensor) -> torch.Tensor:
        """Clamp decoder output to ``config.clamp_range``."""
        lo, hi = self.config.clamp_range
        return image.clamp(lo, hi)

    # ---- core encode/decode ---------------------------------------------

    @torch.no_grad()
    def encode(
        self, pixel_values: torch.Tensor, return_dict: bool = True
    ) -> Union[Tuple, dict]:
        """Encode a uniform-shape batch ``[B, 3, H, W]``.

        Returns dict with:
          * ``indices``   – ``[B, N]`` long codebook indices (N = grid_h * grid_w).
          * ``quant``     – ``[B, N, embed_dim]`` post-quantisation embeddings.
          * ``grid_size`` – ``(grid_h, grid_w)`` tuple.
        """
        if pixel_values.ndim != 4:
            raise ValueError(f"encode expects [B, 3, H, W], got {tuple(pixel_values.shape)}")
        h, meta = self.encoder(pixel_values)
        z = self.quant_embed(h)
        batch, seq_len, dim = z.shape
        indices = self.quantize.encode(z.reshape(-1, dim)).view(batch, seq_len)
        quant = self.quantize.lookup(indices)
        result = {
            "indices": indices,
            "quant": quant,
            "grid_size": meta["grid_sizes"][0],
            "grid_sizes": meta["grid_sizes"],
            "lengths": meta["lengths"],
        }
        return result if return_dict else (indices, quant, result["grid_size"])

    @torch.no_grad()
    def decode(
        self,
        indices: Optional[torch.Tensor] = None,
        grid_size: Optional[Tuple[int, int]] = None,
        quant: Optional[torch.Tensor] = None,
    ) -> torch.Tensor:
        """Decode a uniform-shape batch back to images ``[B, 3, H, W]``.

        Pass either ``indices`` (``[B, N]``) plus ``grid_size`` or pre-looked-up
        ``quant`` embeddings (``[B, N, embed_dim]``) plus ``grid_size``.
        """
        if quant is None:
            if indices is None or grid_size is None:
                raise ValueError("Provide either quant or (indices, grid_size).")
            quant = self.quantize.lookup(indices)
        elif grid_size is None:
            raise ValueError("grid_size is required when passing quant directly.")

        h = self.post_quant_embed(quant)
        images = self.decoder(h, grid_sizes=[grid_size])
        return self.postprocess_image(images)

    # ---- packed-attention batch encode/decode ---------------------------

    @torch.no_grad()
    def pack_encode(
        self, images: Sequence[torch.Tensor]
    ) -> dict:
        """Variable-resolution batch encode using packing attention.

        Args:
            images: list of ``[3, H_i, W_i]`` tensors. Each ``H_i``/``W_i`` must
                already be a multiple of ``self.patch_size`` (use
                :meth:`preprocess_image` to pad first).
        Returns dict:
            * ``indices_packed`` – ``[sum_i N_i]`` long tensor of indices.
            * ``quant_packed``   – ``[sum_i N_i, embed_dim]`` embeddings.
            * ``indices_list``   – per-image ``[N_i]`` long tensors.
            * ``grid_sizes``     – list of ``(gh, gw)``.
            * ``lengths``        – list of ``N_i = gh*gw``.
        """
        images = [img for img in images]
        h, meta = self.encoder(images)
        z = self.quant_embed(h)
        indices_packed = self.quantize.encode(z)
        quant_packed = self.quantize.lookup(indices_packed)
        indices_list = split_packed(indices_packed, meta["lengths"])
        return {
            "indices_packed": indices_packed,
            "quant_packed": quant_packed,
            "indices_list": indices_list,
            "grid_sizes": meta["grid_sizes"],
            "lengths": meta["lengths"],
        }

    @torch.no_grad()
    def pack_decode(
        self,
        indices_list: Optional[Sequence[torch.Tensor]] = None,
        grid_sizes: Optional[Sequence[Tuple[int, int]]] = None,
        indices_packed: Optional[torch.Tensor] = None,
        quant_packed: Optional[torch.Tensor] = None,
        lengths: Optional[Sequence[int]] = None,
    ) -> List[torch.Tensor]:
        """Variable-resolution batch decode using packing attention.

        Accepts either a list of per-image index tensors *or* a packed indices/
        quant tensor plus ``lengths``. Returns a list of ``[3, H_i, W_i]``
        decoded images.
        """
        if quant_packed is None:
            if indices_packed is None:
                if indices_list is None or grid_sizes is None:
                    raise ValueError(
                        "Provide one of: indices_list+grid_sizes, indices_packed+grid_sizes+lengths, "
                        "or quant_packed+grid_sizes+lengths."
                    )
                indices_packed = torch.cat([idx.view(-1) for idx in indices_list], dim=0)
                lengths = [idx.numel() for idx in indices_list]
            quant_packed = self.quantize.lookup(indices_packed)
        if grid_sizes is None or lengths is None:
            raise ValueError("grid_sizes and lengths are required for packed decoding.")

        h = self.post_quant_embed(quant_packed)
        images = self.decoder(h, grid_sizes=list(grid_sizes))
        return [self.postprocess_image(img) for img in images]

    # ---- padded-batch encode/decode -------------------------------------

    @torch.no_grad()
    def batch_encode(self, images: Sequence[torch.Tensor]) -> dict:
        """Variable-resolution batch encode by padding to the max spatial size.

        All images are zero-padded to ``(max_H, max_W)`` and processed as a
        single uniform batch with standard batched attention — no FlashAttention
        dependency.

        Args:
            images: list of ``[3, H_i, W_i]`` tensors. Each ``H_i``/``W_i`` must
                already be a multiple of ``self.patch_size`` (use
                :meth:`preprocess_image` to pad first).
        Returns dict:
            * ``indices``          – ``[B, N_max]`` long codebook indices.
            * ``quant``            – ``[B, N_max, embed_dim]`` post-quant embeddings.
            * ``grid_sizes``       – list of per-image ``(gh_i, gw_i)`` *original* sizes.
            * ``padded_grid_size`` – ``(gh_max, gw_max)`` shared size used for padding.
        """
        max_h = max(img.shape[-2] for img in images)
        max_w = max(img.shape[-1] for img in images)
        orig_grid_sizes = [
            (img.shape[-2] // self.patch_size, img.shape[-1] // self.patch_size)
            for img in images
        ]
        padded = torch.stack(
            [F.pad(img, (0, max_w - img.shape[-1], 0, max_h - img.shape[-2])) for img in images],
            dim=0,
        )
        enc = self.encode(padded)
        return {
            "indices": enc["indices"],
            "quant": enc["quant"],
            "grid_sizes": orig_grid_sizes,
            "padded_grid_size": enc["grid_size"],
        }

    @torch.no_grad()
    def batch_decode(
        self,
        indices: Optional[torch.Tensor] = None,
        padded_grid_size: Optional[Tuple[int, int]] = None,
        grid_sizes: Optional[Sequence[Tuple[int, int]]] = None,
        quant: Optional[torch.Tensor] = None,
    ) -> List[torch.Tensor]:
        """Decode a padded batch back to variable-resolution images.

        Decodes the full padded spatial extent and crops each image to its
        original size according to ``grid_sizes``.

        Args:
            indices:          ``[B, N_max]`` long indices (mutually exclusive with ``quant``).
            padded_grid_size: ``(gh_max, gw_max)`` required when passing ``indices``.
            grid_sizes:       per-image original ``(gh_i, gw_i)`` list for cropping.
            quant:            ``[B, N_max, embed_dim]`` pre-looked-up embeddings.
        Returns:
            List of ``[3, H_i, W_i]`` decoded and cropped image tensors.
        """
        if grid_sizes is None:
            raise ValueError("grid_sizes is required for batch_decode.")
        if quant is None:
            if indices is None or padded_grid_size is None:
                raise ValueError("Provide either quant or (indices, padded_grid_size).")
            quant = self.quantize.lookup(indices)
        elif padded_grid_size is None:
            gh_max = max(gs[0] for gs in grid_sizes)
            gw_max = max(gs[1] for gs in grid_sizes)
            padded_grid_size = (gh_max, gw_max)

        recon = self.decode(quant=quant, grid_size=padded_grid_size)  # [B, 3, max_H, max_W]
        return [
            recon[i, :, : gh * self.patch_size, : gw * self.patch_size]
            for i, (gh, gw) in enumerate(grid_sizes)
        ]

    # ---- reconstruct shortcuts ------------------------------------------

    @torch.no_grad()
    def reconstruct(self, pixel_values: torch.Tensor) -> torch.Tensor:
        out = self.encode(pixel_values)
        return self.decode(quant=out["quant"], grid_size=out["grid_size"])

    @torch.no_grad()
    def reconstruct_packed(self, images: Sequence[torch.Tensor]) -> List[torch.Tensor]:
        out = self.pack_encode(images)
        return self.pack_decode(
            quant_packed=out["quant_packed"],
            grid_sizes=out["grid_sizes"],
            lengths=out["lengths"],
        )

    # ---- HF default forward ---------------------------------------------

    def forward(self, pixel_values: torch.Tensor, **kwargs) -> torch.Tensor:
        return self.reconstruct(pixel_values)


# ---------------------------------------------------------------------------
# Standalone helpers
# ---------------------------------------------------------------------------


def _pad_to_multiple(image: torch.Tensor, divisor: int, pad_mode: str = "replicate") -> torch.Tensor:
    if divisor is None or divisor <= 1:
        return image
    _, h, w = image.shape
    th = ((h + divisor - 1) // divisor) * divisor
    tw = ((w + divisor - 1) // divisor) * divisor
    pad_h, pad_w = th - h, tw - w
    if pad_h == 0 and pad_w == 0:
        return image
    if pad_mode == "constant":
        return F.pad(image, (0, pad_w, 0, pad_h), mode="constant", value=0.0)
    return F.pad(image, (0, pad_w, 0, pad_h), mode=pad_mode)
