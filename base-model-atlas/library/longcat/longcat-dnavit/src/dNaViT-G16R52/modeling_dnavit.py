"""dNaViT: discrete native-resolution tokenizer with a flow-matching refiner.

This file is the complete inference implementation of
``dNaViT-G16`` -- a Qwen3-VL-based 32x visual tokenizer (G16 product
quantizer, ResMod feature enhancement, ViT pixel decoder) followed by a
flow-matching refiner that reconstructs 2x super-resolved pixels.

Only the inference path is implemented; every parameter lives in
``model.safetensors`` next to this file.
"""

import math
from dataclasses import dataclass

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from einops import rearrange
from einops.layers.torch import Rearrange
from PIL import Image
from timm.layers import Mlp
from torchvision.transforms import ToPILImage, ToTensor
from transformers import PreTrainedModel
from transformers.models.qwen3_vl.configuration_qwen3_vl import Qwen3VLVisionConfig
from transformers.models.qwen3_vl.modeling_qwen3_vl import Qwen3VLVisionModel

from .configuration_dnavit import DNaViTConfig

try:
    import flash_attn_interface  # noqa: F401  (FlashAttention-3)
    _HAS_FLASH_ATTN_3 = True
except Exception:
    _HAS_FLASH_ATTN_3 = False

try:
    import flash_attn  # noqa: F401  (FlashAttention-2)
    _HAS_FLASH_ATTN_2 = True
except Exception:
    _HAS_FLASH_ATTN_2 = False

#: FlashAttention is used for packed variable-length attention when importable;
#: otherwise every attention falls back to ``scaled_dot_product_attention``.
FLASH_ATTN_AVAILABLE = _HAS_FLASH_ATTN_2 or _HAS_FLASH_ATTN_3

LLM_TOKEN_INDICATOR = 3
OUTPUT_IMAGE_INDICATOR = 2
IMAGE_POSITION_OFFSET = 65536


# ---------------------------------------------------------------------------
# shared helpers
# ---------------------------------------------------------------------------



# ---------------------------------------------------------------------------
# encoder: Qwen3-VL vision blocks -> ResMod
# ---------------------------------------------------------------------------


class RMSNorm(nn.Module):
    def __init__(self, dim: int, eps: float = 1e-6):
        super().__init__()
        self.eps = eps
        self.weight = nn.Parameter(torch.ones(dim))

    @torch.amp.autocast(device_type="cuda", enabled=False)
    def forward(self, x):
        dtype = x.dtype
        x = x.float()
        x = x * torch.rsqrt(x.pow(2).mean(-1, keepdim=True) + self.eps)
        return (x * self.weight).to(dtype)


class ResModLayer(nn.Module):
    def __init__(self, dim: int, num_heads: int, mlp_ratio: float = 4.0):
        super().__init__()
        self.norm1 = nn.LayerNorm(dim)
        self.attn = ResModAttention(dim, num_heads)
        self.norm2 = nn.LayerNorm(dim)
        self.mlp = ResModMLP(dim, int(dim * mlp_ratio))

    def forward(self, x, cu_seqlens=None):
        x = x + self.attn(self.norm1(x), cu_seqlens=cu_seqlens)
        return x + self.mlp(self.norm2(x))


class ResModMLP(nn.Module):
    def __init__(self, in_features: int, hidden_features: int):
        super().__init__()
        self.norm = nn.LayerNorm(in_features, eps=1e-6)
        self.act = nn.GELU(approximate="tanh")
        self.w0 = nn.Linear(in_features, hidden_features)
        self.w1 = nn.Linear(in_features, hidden_features)
        self.w2 = nn.Linear(hidden_features, in_features)

    def forward(self, x):
        x = self.norm(x)
        return self.w2(self.act(self.w0(x)) * self.w1(x))


class ResModAttention(nn.Module):
    def __init__(self, dim: int, num_heads: int):
        super().__init__()
        self.num_heads = num_heads
        self.head_dim = dim // num_heads
        self.scale = self.head_dim ** -0.5
        self.qkv = nn.Linear(dim, dim * 3, bias=False)
        self.q_bias = nn.Parameter(torch.zeros(dim))
        self.v_bias = nn.Parameter(torch.zeros(dim))
        self.proj = nn.Linear(dim, dim)

    def forward(self, x, cu_seqlens=None):
        seq_total = x.shape[0]
        qkv_bias = torch.cat((self.q_bias, torch.zeros_like(self.q_bias), self.v_bias))
        qkv = F.linear(x, self.qkv.weight, qkv_bias)
        q, k, v = qkv.reshape(seq_total, 3, self.num_heads, self.head_dim).permute(1, 0, 2, 3).unbind(0)
        out = _varlen_attention(q, k, v, cu_seqlens)
        return self.proj(out.reshape(seq_total, -1))


class ResMod(nn.Module):
    """Tap -> fuse -> modulate, with an internal 2x2 merger into refiner space."""

    def __init__(self, hidden_size: int, layer_idx_list, depth: int, num_heads: int,
                 mlp_ratio: float, output_dim: int, input_merge_size: int):
        super().__init__()
        self.hidden_size = int(hidden_size)
        self.output_dim = int(output_dim)
        self.input_merge_size = int(input_merge_size)
        self.layer_idx_list = [int(i) for i in layer_idx_list]
        self.tap_lns = nn.ModuleList([nn.LayerNorm(hidden_size) for _ in self.layer_idx_list])
        self.fuser = nn.Linear(len(self.layer_idx_list) * hidden_size, hidden_size)
        self.blocks = nn.ModuleList([
            ResModLayer(dim=hidden_size, num_heads=num_heads, mlp_ratio=mlp_ratio)
            for _ in range(depth)])
        self.internal_merger = nn.Linear(self.input_merge_size * hidden_size, self.output_dim)
        self.final_ln = nn.LayerNorm(self.output_dim)
        self.sft_proj = nn.Linear(self.output_dim, self.output_dim * 2)

        nn.init.zeros_(self.sft_proj.weight)
        nn.init.zeros_(self.sft_proj.bias)
        nn.init.xavier_uniform_(self.fuser.weight, gain=1.0 / (2 ** 0.5))
        nn.init.zeros_(self.fuser.bias)

    def forward(self, taps, target, cu_seqlens=None):
        normalized = [ln(t) for ln, t in zip(self.tap_lns, taps)]
        x = self.fuser(torch.cat(normalized, dim=-1))
        for block in self.blocks:
            x = block(x, cu_seqlens=cu_seqlens)
        ms2 = self.input_merge_size
        x = x.reshape(x.shape[0] // ms2, ms2 * self.hidden_size)
        x = self.final_ln(self.internal_merger(x))
        scale, shift = self.sft_proj(x).chunk(2, dim=-1)
        return target * (1.0 + scale) + shift


class UnifiedEncoder(nn.Module):
    """Qwen3-VL vision blocks + frozen patch merger + ResMod."""

    def __init__(self, config):
        super().__init__()
        self.patch_size = int(config.patch_size)
        self.spatial_merge_size = int(config.spatial_merge_size)
        self.temporal_patch_size = int(config.temporal_patch_size)

        vision_config = dict(config.vision_config)
        vision_config.pop("model_type", None)
        vision_config = Qwen3VLVisionConfig(**vision_config)
        # The Qwen3-VL tower keeps SDPA (its packing path is validated in SDPA);
        # FlashAttention is used by the packed refiner / decoder attention below.
        vision_config._attn_implementation = "sdpa"
        vit = Qwen3VLVisionModel(vision_config)
        self.vit = vit
        self.blocks = vit.blocks
        vit.blocks = nn.ModuleList()
        self.merger = vit.merger
        vit.merger = nn.Identity()
        vit.deepstack_merger_list = nn.ModuleList()
        self.merger.requires_grad_(False)

        self.width = int(vision_config.hidden_size)
        self.merger_out_dim = int(vision_config.out_hidden_size)
        self.res_mod = ResMod(
            hidden_size=self.width,
            layer_idx_list=config.res_mod["layer_idx_list"],
            depth=int(config.res_mod["depth"]),
            num_heads=int(config.res_mod["num_heads"]),
            mlp_ratio=float(config.res_mod["mlp_ratio"]),
            output_dim=self.merger_out_dim,
            input_merge_size=self.spatial_merge_size ** 2,
        )
        self._res_mod_layer_set = set(self.res_mod.layer_idx_list)

    def _patchify(self, image):
        """(C, H, W) -> ((gh*gw, C*T*ps*ps), (gh, gw)) in Qwen's patch order."""
        ps, temporal, merge = self.patch_size, self.temporal_patch_size, self.spatial_merge_size
        channels, height, width = image.shape
        gh, gw = height // ps, width // ps
        x = image.unsqueeze(0).unsqueeze(2).expand(1, channels, temporal, height, width).contiguous()
        x = x.view(1, channels, temporal, gh // merge, merge, ps, gw // merge, merge, ps)
        x = x.permute(0, 3, 6, 4, 7, 1, 2, 5, 8).contiguous()
        return x.view(gh * gw, channels * temporal * ps * ps), (gh, gw)

    def forward(self, images, image_grid_thw):
        """Encode a list of ``(3, H, W)`` images into packed ResMod features."""
        device = images[0].device
        grid_thw = image_grid_thw.to(device=device, dtype=torch.long)
        flats = []
        for image, row in zip(images, grid_thw):
            flat, (gh, gw) = self._patchify(image)
            if int(row[1]) != gh or int(row[2]) != gw:
                raise ValueError("image_grid_thw row mismatches image patch grid.")
            flats.append(flat)
        flat = torch.cat(flats, dim=0)

        vit = self.vit
        hidden = vit.patch_embed(flat)
        hidden = hidden + vit.fast_pos_embed_interpolate(grid_thw).to(
            device=hidden.device, dtype=hidden.dtype)
        rotary = vit.rot_pos_emb(grid_thw).to(hidden.device)
        emb = torch.cat((rotary, rotary), dim=-1)
        position_embeddings = (emb.cos(), emb.sin())
        cu_seqlens = torch.repeat_interleave(
            grid_thw[:, 1] * grid_thw[:, 2], grid_thw[:, 0]).cumsum(dim=0, dtype=torch.int32)
        cu_seqlens = F.pad(cu_seqlens, (1, 0), value=0)

        taps = [hidden] if 1 in self._res_mod_layer_set else []
        for i, block in enumerate(self.blocks):
            hidden = block(hidden, cu_seqlens=cu_seqlens, position_embeddings=position_embeddings)
            if (i + 2) in self._res_mod_layer_set:
                taps.append(hidden)

        merged = self.merger(hidden)
        z = self.res_mod(taps, merged, cu_seqlens=cu_seqlens)
        ms2 = self.spatial_merge_size ** 2
        return z, (cu_seqlens // ms2).to(cu_seqlens.dtype)

# ---------------------------------------------------------------------------
# vector quantizer: product quantization over the encoder features
# ---------------------------------------------------------------------------


def _compute_distances(z_flat: torch.Tensor, codebook: torch.Tensor) -> torch.Tensor:
    codebook_t = codebook.t()
    z_norm_sq = z_flat.pow(2).sum(dim=1, keepdim=True)
    c_norm_sq = codebook_t.pow(2).sum(dim=0, keepdim=True)
    return torch.addmm(z_norm_sq + c_norm_sq, z_flat, codebook_t, alpha=-2.0)


class Codebook(nn.Module):
    def __init__(self, size: int, dim: int):
        super().__init__()
        self.embedding = nn.Embedding(size, dim)
        self.embedding.weight.requires_grad_(False)


class ProductQuantizer(nn.Module):
    """UniTok-style product quantizer: ``num_groups`` parallel codebooks."""

    def __init__(self, in_dim: int, out_dim: int, code_dim: int, num_groups: int,
                 codebook_size: int, proj_hidden: int):
        super().__init__()
        self.code_dim = int(code_dim)
        self.num_groups = int(num_groups)
        self.sub_dim = self.code_dim // self.num_groups
        self.codebook_size = int(codebook_size)

        self.in_proj = nn.Sequential(
            RMSNorm(in_dim),
            nn.Linear(in_dim, proj_hidden),
            nn.GELU(),
            nn.Linear(proj_hidden, code_dim),
        )
        self.out_proj = nn.Sequential(
            RMSNorm(code_dim),
            nn.Linear(code_dim, proj_hidden),
            nn.GELU(),
            nn.Linear(proj_hidden, out_dim),
        )
        self.codebooks = nn.ModuleList([
            Codebook(self.codebook_size, self.sub_dim) for _ in range(self.num_groups)])

    def _quantize_group(self, group: int, z: torch.Tensor):
        flat = z.reshape(-1, z.shape[-1]).float()
        codebook = self.codebooks[group].embedding.weight
        indices = _compute_distances(flat, codebook).argmin(dim=-1)
        return F.embedding(indices, codebook).reshape(z.shape), indices.reshape(z.shape[:-1])

    def forward(self, z: torch.Tensor):
        z = z.float()
        z_proj = self.in_proj(z)
        chunks = z_proj.split(self.sub_dim, dim=-1)

        quant_chunks, codes = [], []
        for group, chunk in enumerate(chunks):
            quant, indices = self._quantize_group(group, chunk)
            quant_chunks.append(quant)
            codes.append(indices.unsqueeze(-1))

        quant = torch.cat(quant_chunks, dim=-1)
        quants_ste = z_proj + (quant - z_proj).detach()
        return self.out_proj(quants_ste), torch.cat(codes, dim=-1), quants_ste

    def codebook_embeddings(self, indices: torch.Tensor) -> torch.Tensor:
        """``(..., num_groups)`` ids -> concatenated codebook embeddings (code_dim)."""
        return torch.cat([F.embedding(indices[..., g], self.codebooks[g].embedding.weight)
                          for g in range(self.num_groups)], dim=-1)

    def get_codebook_entry(self, indices: torch.Tensor) -> torch.Tensor:
        return self.out_proj(self.codebook_embeddings(indices))

# ---------------------------------------------------------------------------
# pixel decoder: ViT decoder over the token grid
# ---------------------------------------------------------------------------


class TokenUnmerger(nn.Module):
    """Expand one merged token back into ``ms2`` tokens (pre-decoder)."""

    def __init__(self, dim: int, ms2: int):
        super().__init__()
        self.dim = int(dim)
        self.ms2 = int(ms2)
        self.proj = nn.Linear(self.dim, self.ms2 * self.dim)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        y = self.proj(x)
        if x.dim() == 2:
            return y.view(x.shape[0], self.ms2, self.dim).reshape(x.shape[0] * self.ms2, self.dim)
        batch, length, _ = x.shape
        return y.view(batch, length, self.ms2, self.dim).reshape(batch, length * self.ms2, self.dim)


class DecoderAttention(nn.Module):
    def __init__(self, dim: int, num_heads: int):
        super().__init__()
        self.num_heads = num_heads
        self.head_dim = dim // num_heads
        self.qkv = nn.Linear(dim, dim * 3, bias=True)
        self.proj = nn.Linear(dim, dim)

    def forward(self, x, cu_seqlens):
        seq_total, dim = x.shape
        qkv = self.qkv(x).reshape(seq_total, 3, self.num_heads, self.head_dim)
        q, k, v = qkv.permute(1, 0, 2, 3).unbind(0)
        return self.proj(_varlen_attention(q, k, v, cu_seqlens).reshape(seq_total, dim))


class DecoderBlock(nn.Module):
    def __init__(self, dim: int, num_heads: int, mlp_ratio: float):
        super().__init__()
        self.norm1 = nn.LayerNorm(dim)
        self.attn = DecoderAttention(dim, num_heads)
        self.norm2 = nn.LayerNorm(dim)
        self.mlp = Mlp(in_features=dim, hidden_features=int(dim * mlp_ratio),
                       act_layer=nn.GELU, drop=0.0)

    def forward(self, x, cu_seqlens=None):
        x = x + self.attn(self.norm1(x), cu_seqlens)
        return x + self.mlp(self.norm2(x))


class PixelDecoder(nn.Module):
    """ViT pixel decoder over packed variable-resolution token grids."""

    def __init__(self, config):
        super().__init__()
        self.width = int(config.pixel_decoder["width"])
        self.patch_size = int(config.pixel_decoder["patch_size"])
        self.grid_size = int(config.image_size) // self.patch_size
        num_layers = int(config.pixel_decoder["num_layers"])
        num_heads = int(config.pixel_decoder["num_heads"])
        mlp_ratio = float(config.pixel_decoder["mlp_ratio"])

        scale = self.width ** -0.5
        self.class_embedding = nn.Parameter(scale * torch.randn(1, self.width))
        self.positional_embedding = nn.Parameter(
            scale * torch.randn(self.grid_size ** 2 + 1, self.width))
        self.ln_pre = nn.LayerNorm(self.width)
        self.transformer = nn.ModuleList([
            DecoderBlock(self.width, num_heads, mlp_ratio) for _ in range(num_layers)])
        self.ln_post = nn.LayerNorm(self.width)
        self.ffn = nn.Sequential(
            nn.Conv2d(self.width, self.patch_size * self.patch_size * 3, 1, padding=0, bias=True),
            Rearrange("b (p1 p2 c) h w -> b c (h p1) (w p2)",
                      p1=self.patch_size, p2=self.patch_size),
        )
        self.conv_out = nn.Conv2d(3, 3, 3, padding=1, bias=True)

    def _interp_pos_embed(self, grid_h, grid_w, dtype):
        if grid_h == self.grid_size and grid_w == self.grid_size:
            return self.positional_embedding.to(dtype)
        cls_pos = self.positional_embedding[:1]
        spatial = self.positional_embedding[1:].reshape(self.grid_size, self.grid_size, self.width)
        spatial = spatial.permute(2, 0, 1).unsqueeze(0)
        interp = F.interpolate(spatial, size=(grid_h, grid_w), mode="bicubic",
                               align_corners=False).squeeze(0).permute(1, 2, 0)
        return torch.cat([cls_pos, interp.reshape(grid_h * grid_w, self.width)], dim=0).to(dtype)

    def forward(self, z_quantized, image_grid_thw=None):
        dtype = z_quantized.dtype
        cls = self.class_embedding.to(dtype)
        static = image_grid_thw is None
        if static:
            batch, length, _ = z_quantized.shape
            if length != self.grid_size * self.grid_size:
                raise ValueError(f"Decoder expects L={self.grid_size ** 2}; got {length}.")
            blocks = [(z_quantized[b], self.grid_size, self.grid_size) for b in range(batch)]
        else:
            grid_thw = image_grid_thw.to(z_quantized.device, dtype=torch.long)
            blocks, offset = [], 0
            for row in grid_thw:
                h_i, w_i = int(row[1]), int(row[2])
                length = h_i * w_i
                blocks.append((z_quantized[offset:offset + length], h_i, w_i))
                offset += length

        chunks, cu, boundaries = [], [0], []
        for img, h_i, w_i in blocks:
            pos = self._interp_pos_embed(h_i, w_i, dtype)
            chunks.append(torch.cat([cls, img], dim=0) + pos)
            cu.append(cu[-1] + h_i * w_i + 1)
            boundaries.append((h_i, w_i, h_i * w_i + 1))

        x = self.ln_pre(torch.cat(chunks, dim=0))
        cu_seqlens = torch.tensor(cu, dtype=torch.int32, device=z_quantized.device)
        for block in self.transformer:
            x = block(x, cu_seqlens=cu_seqlens)
        x = self.ln_post(x)

        if static:
            batch = z_quantized.shape[0]
            feats = x.view(batch, self.grid_size * self.grid_size + 1, self.width)[:, 1:]
            feats = feats.permute(0, 2, 1).reshape(batch, self.width, self.grid_size, self.grid_size)
            return self.conv_out(self.ffn(feats.contiguous()))

        recon, offset = [], 0
        for (h_i, w_i, length_with_cls) in boundaries:
            img_x = x[offset + 1: offset + length_with_cls]
            spatial = img_x.permute(1, 0).reshape(1, self.width, h_i, w_i)
            recon.append(self.conv_out(self.ffn(spatial.contiguous())).squeeze(0))
            offset += length_with_cls
        return recon

# ---------------------------------------------------------------------------
# refiner: flow-matching DiT, condition path, samplers and VAE decoder
# ---------------------------------------------------------------------------


@dataclass
class RefinerConfig:
    emb_dim: int = 4608
    num_layers: int = 34
    num_heads: int = 18
    intermediate_size: int = 12288
    adanln_dim: int = 512
    in_channels: int = 128
    rope_theta: int = 5000000
    mrope_section: tuple = (24, 20, 20)
    norm_eps: float = 1e-5
    cond_code_dim: int = 4096
    cond_channels: int = 4096
    inject_interval: int = 4
    num_resblocks: int = 1
    incontext_adapter_depth: int = 2
    incontext_adapter_heads: int = 16
    incontext_adapter_dim: int = 2048


class DiTRMSNorm(nn.Module):
    def __init__(self, dim: int, eps: float = 1e-6) -> None:
        super().__init__()
        self.weight = nn.Parameter(torch.ones(dim))
        self.eps = eps

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return F.rms_norm(x, self.weight.shape, self.weight, self.eps)


class MRoPE(nn.Module):
    def __init__(self, head_dim: int, base: int, mrope_section) -> None:
        super().__init__()
        inv_freq = 1.0 / (base ** (torch.arange(0, head_dim, 2, dtype=torch.float32) / head_dim))
        self.register_buffer("inv_freq", inv_freq, persistent=False)
        self.mrope_section = tuple(mrope_section)
        self.head_dim = head_dim

    @torch.no_grad()
    def forward(self, position_ids: torch.Tensor):
        batch_size, seq_len, _ = position_ids.shape
        pos = position_ids.permute(2, 0, 1).to(dtype=torch.float32)
        inv_freq = self.inv_freq.to(dtype=torch.float32)[None, None, :, None].expand(
            3, batch_size, -1, 1).to(pos.device)
        freqs = (inv_freq @ pos.unsqueeze(2)).transpose(2, 3)

        freqs_t = freqs[0].clone()
        for axis, offset in ((1, 1), (2, 2)):
            length = self.mrope_section[axis] * 3
            idx = torch.arange(offset, length, 3, device=freqs_t.device)
            freqs_t[..., idx] = freqs[axis][..., idx]

        emb = torch.cat((freqs_t, freqs_t), dim=-1)
        return emb.cos(), emb.sin()


class DiTAttention(nn.Module):
    def __init__(self, hidden_size: int, num_heads: int, eps: float = 1e-5) -> None:
        super().__init__()
        self.hidden_size = hidden_size
        self.num_heads = num_heads
        self.head_dim = hidden_size // num_heads
        self.qkv = nn.Linear(hidden_size, hidden_size * 3, bias=False)
        self.norm_q = DiTRMSNorm(self.head_dim, eps=eps)
        self.norm_k = DiTRMSNorm(self.head_dim, eps=eps)
        self.o = nn.Linear(hidden_size, hidden_size, bias=False)

    def forward(self, x, cos, sin, cu_seqlens):
        batch_size, seq_len, _ = x.shape
        qkv = self.qkv(x).view(batch_size, seq_len, 3, self.num_heads, self.head_dim)
        q, k, v = qkv.unbind(dim=2)
        q = self.norm_q(q).transpose(1, 2)
        k = self.norm_k(k).transpose(1, 2)
        v = v.transpose(1, 2)
        q, k = _apply_rotary_pos_emb(q, k, cos, sin)
        out = _varlen_attention(q[0].transpose(0, 1).contiguous(),
                                k[0].transpose(0, 1).contiguous(),
                                v[0].transpose(0, 1).contiguous(), cu_seqlens)
        return self.o(out.reshape(out.shape[0], -1).unsqueeze(0))


class DiTMLP(nn.Module):
    def __init__(self, dim: int, hidden_dim: int) -> None:
        super().__init__()
        self.w1 = nn.Linear(dim, hidden_dim, bias=False)
        self.w2 = nn.Linear(hidden_dim, dim, bias=False)
        self.w3 = nn.Linear(dim, hidden_dim, bias=False)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.w2(F.silu(self.w1(x)) * self.w3(x))


class DiTBlock(nn.Module):
    def __init__(self, hidden_size, intermediate_size, num_heads, norm_eps, adanln_dim) -> None:
        super().__init__()
        self.attention = DiTAttention(hidden_size, num_heads, eps=1e-5)
        self.feed_forward = DiTMLP(hidden_size, intermediate_size)
        self.attention_norm1 = DiTRMSNorm(hidden_size, eps=norm_eps)
        self.ffn_norm1 = DiTRMSNorm(hidden_size, eps=norm_eps)
        self.attention_norm2 = DiTRMSNorm(hidden_size, eps=norm_eps)
        self.ffn_norm2 = DiTRMSNorm(hidden_size, eps=norm_eps)
        self.adaln_modulation = nn.Linear(adanln_dim, 4 * hidden_size, bias=True)

    def forward(self, x, cos, sin, adaln_input, cu_seqlens):
        scale_msa, gate_msa, scale_mlp, gate_mlp = self.adaln_modulation(adaln_input).chunk(4, dim=-1)
        gate_msa = torch.tanh(gate_msa)
        gate_mlp = torch.tanh(gate_mlp)
        scale_msa = 1.0 + scale_msa
        scale_mlp = 1.0 + scale_mlp
        attn_out = self.attention(self.attention_norm1(x) * scale_msa, cos, sin, cu_seqlens)
        x = x + gate_msa * self.attention_norm2(attn_out)
        x = x + gate_mlp * self.ffn_norm2(self.feed_forward(self.ffn_norm1(x) * scale_mlp))
        return x


class TimestepEmbedding(nn.Module):
    def __init__(self, dim: int, input_range) -> None:
        super().__init__()
        self.dim = dim
        self.range_min, self.range_max = input_range
        self.mlp_in = nn.Linear(dim, dim, bias=True)
        self.mlp_out = nn.Linear(dim, dim, bias=True)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = x.to(torch.float32)
        scaled = 1e4 * (x - self.range_min) / (self.range_max - self.range_min)
        emb = _sinusoidal_embedding(scaled, self.dim)
        emb = emb.to(self.mlp_in.weight.dtype)
        return self.mlp_out(F.silu(self.mlp_in(emb)))


class DiTFinalLayer(nn.Module):
    def __init__(self, hidden_size: int, out_channels: int, adanln_dim: int) -> None:
        super().__init__()
        self.norm_final = nn.LayerNorm(hidden_size, eps=1e-6, elementwise_affine=False)
        self.linear = nn.Linear(hidden_size, out_channels, bias=True)
        self.adaln_modulation = nn.Linear(adanln_dim, hidden_size, bias=True)

    def forward(self, x: torch.Tensor, c: torch.Tensor) -> torch.Tensor:
        scale = 1.0 + self.adaln_modulation(F.silu(c))
        return self.linear(self.norm_final(x) * scale)


class RefinerDiT(nn.Module):
    """Flow-matching transformer over a packed text+image sequence."""

    def __init__(self, config: RefinerConfig) -> None:
        super().__init__()
        self.config = config
        self.patch_size = 2
        head_dim = config.emb_dim // config.num_heads

        self.input_proj = nn.Linear(config.in_channels, config.emb_dim, bias=True)
        self.t_embedding = TimestepEmbedding(config.emb_dim, input_range=(0.0, 1.0))
        self.adaln_proj = nn.Linear(config.emb_dim, config.adanln_dim, bias=True)
        self.embed_image_indicator = nn.Embedding(2, config.emb_dim)
        self.rotary_emb = MRoPE(head_dim=head_dim, base=config.rope_theta,
                                mrope_section=config.mrope_section)
        self.layers = nn.ModuleList([
            DiTBlock(hidden_size=config.emb_dim,
                     intermediate_size=config.intermediate_size,
                     num_heads=config.num_heads,
                     norm_eps=config.norm_eps,
                     adanln_dim=config.adanln_dim)
            for _ in range(config.num_layers)])
        self.final_layer = DiTFinalLayer(hidden_size=config.emb_dim,
                                         out_channels=config.in_channels,
                                         adanln_dim=config.adanln_dim)

    def forward(self, llm_features, x, t, position_ids, indicator, cu_seqlens,
                inject_fn=None, inject_layers=None):
        """Predict the flow-matching velocity for the image tokens.

        ``llm_features`` is the already-projected context (``emb_dim``); image
        token positions hold zeros and are masked out, so only the text slots
        contribute context.
        """
        param_dtype = self.input_proj.weight.dtype
        x = x.to(param_dtype)
        t = t.to(param_dtype)
        llm_features = llm_features.to(param_dtype)

        indicator = indicator.to(torch.long)
        image_bool = indicator == OUTPUT_IMAGE_INDICATOR
        llm_token_mask = (indicator == LLM_TOKEN_INDICATOR).to(x.dtype).unsqueeze(-1)
        output_image_mask = image_bool.to(x.dtype).unsqueeze(-1)

        do_inject = inject_fn is not None and inject_layers is not None

        def _add_img(hidden, point):
            residual = inject_fn(point).to(hidden.dtype)
            hidden = hidden.clone()
            hidden[image_bool] = hidden[image_bool] + residual.reshape(-1, residual.shape[-1])
            return hidden

        llm_features = llm_features * llm_token_mask
        x = x * output_image_mask
        if do_inject and -2 in inject_layers:
            x = _add_img(x, -2)
        x = self.input_proj(x) * output_image_mask

        t_cond = self.t_embedding(t)
        if t.dim() == 1:
            t_cond = t_cond.unsqueeze(1)
        adaln_input = F.silu(self.adaln_proj(t_cond))

        h = x + llm_features
        h = h + self.embed_image_indicator(image_bool.to(torch.long))
        if do_inject and -1 in inject_layers:
            h = _add_img(h, -1)

        cos, sin = self.rotary_emb(position_ids)
        cos = cos.to(h.dtype)
        sin = sin.to(h.dtype)

        for i, layer in enumerate(self.layers):
            h = layer(h, cos, sin, adaln_input, cu_seqlens)
            if do_inject and i in inject_layers:
                h = _add_img(h, i)

        return self.final_layer(h, c=adaln_input).to(torch.float32)


# ---------------------------------------------------------------------------
# refiner conditioning (RepAR-style additive injection + in-context adapter)
# ---------------------------------------------------------------------------


class ConditionRMSNorm(nn.Module):
    def __init__(self, dim: int, eps: float = 1e-6):
        super().__init__()
        self.eps = eps
        self.weight = nn.Parameter(torch.ones(dim))

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        dtype = x.dtype
        x = x.float()
        x = x * torch.rsqrt(x.pow(2).mean(-1, keepdim=True) + self.eps)
        return (x * self.weight.float()).to(dtype)


class ConditionResBlock(nn.Module):
    """Time-modulated residual MLP (zero-initialised adaLN gate)."""

    def __init__(self, channels: int, time_dim: int):
        super().__init__()
        self.in_ln = nn.LayerNorm(channels, elementwise_affine=False, eps=1e-6)
        self.mlp = nn.Sequential(
            nn.Linear(channels, channels, bias=True),
            nn.SiLU(),
            nn.Linear(channels, channels, bias=True),
        )
        self.adaLN_modulation = nn.Sequential(
            nn.SiLU(), nn.Linear(time_dim, 3 * channels, bias=True))
        nn.init.zeros_(self.adaLN_modulation[1].weight)
        nn.init.zeros_(self.adaLN_modulation[1].bias)

    def forward(self, x: torch.Tensor, y: torch.Tensor) -> torch.Tensor:
        shift, scale, gate = self.adaLN_modulation(y).chunk(3, dim=-1)
        if shift.dim() == 2:
            shift = shift.unsqueeze(1)
            scale = scale.unsqueeze(1)
            gate = gate.unsqueeze(1)
        return x + gate * self.mlp(modulate(self.in_ln(x), shift, scale))


class ConditionEncoder(nn.Module):
    """``z_q`` (codebook space) -> time-selective condition tokens."""

    def __init__(self, code_dim: int, cond_width: int, time_dim: int, num_resblocks: int = 1):
        super().__init__()
        self.code_dim = code_dim
        self.cond_width = cond_width
        self.norm = ConditionRMSNorm(code_dim)
        self.time_mlp = nn.Sequential(nn.SiLU(), nn.Linear(time_dim, 3 * code_dim, bias=True))
        self.in_proj = nn.Linear(code_dim, cond_width)
        self.resblocks = nn.ModuleList(
            [ConditionResBlock(cond_width, time_dim) for _ in range(max(1, num_resblocks))])
        nn.init.zeros_(self.time_mlp[1].weight)
        nn.init.zeros_(self.time_mlp[1].bias)
        with torch.no_grad():
            self.time_mlp[1].bias[2 * code_dim:].fill_(4.0)

    @staticmethod
    def _film_apply(h, s, b, g):
        return (h * (1 + s.unsqueeze(1)) + b.unsqueeze(1)) * torch.sigmoid(g.unsqueeze(1))

    def refine(self, h: torch.Tensor, y: torch.Tensor) -> torch.Tensor:
        h = self.in_proj(h)
        for block in self.resblocks:
            h = block(h, y)
        return h


class InjectionHead(nn.Module):
    """adaLN(time) + zero-init linear -> additive residual at one DiT layer."""

    def __init__(self, cond_dim: int, time_dim: int, out_dim: int):
        super().__init__()
        self.norm_final = ConditionRMSNorm(cond_dim)
        self.linear = nn.Linear(cond_dim, out_dim, bias=True)
        self.adaLN_modulation = nn.Sequential(nn.SiLU(), nn.Linear(time_dim, 2 * cond_dim, bias=True))
        nn.init.zeros_(self.linear.weight)
        nn.init.zeros_(self.linear.bias)

    def forward(self, x: torch.Tensor, c: torch.Tensor) -> torch.Tensor:
        shift, scale = self.adaLN_modulation(c).chunk(2, dim=-1)
        if shift.dim() == 2:
            shift = shift.unsqueeze(1)
            scale = scale.unsqueeze(1)
        return self.linear(modulate(self.norm_final(x), shift, scale))


class AdapterBlock(nn.Module):
    def __init__(self, dim: int, heads: int, mlp_ratio: int = 4):
        super().__init__()
        self.heads = heads
        self.norm1 = nn.LayerNorm(dim)
        self.qkv = nn.Linear(dim, 3 * dim)
        self.proj = nn.Linear(dim, dim)
        self.norm2 = nn.LayerNorm(dim)
        self.mlp = nn.Sequential(
            nn.Linear(dim, dim * mlp_ratio), nn.GELU(), nn.Linear(dim * mlp_ratio, dim))

    def forward(self, x: torch.Tensor, attn_mask=None) -> torch.Tensor:
        batch, seq, dim = x.shape
        qkv = self.qkv(self.norm1(x)).reshape(batch, seq, 3, self.heads, dim // self.heads)
        q, k, v = qkv.permute(2, 0, 3, 1, 4).unbind(0)
        o = F.scaled_dot_product_attention(q, k, v, attn_mask=attn_mask)
        x = x + self.proj(o.transpose(1, 2).reshape(batch, seq, dim))
        return x + self.mlp(self.norm2(x))


class IncontextAdapter(nn.Module):
    """``z_q`` -> pseudo-text context tokens of DiT width (token count preserved)."""

    def __init__(self, code_dim: int, features: int, depth: int, heads: int, inner_dim: int):
        super().__init__()
        self.in_proj = nn.Linear(code_dim, inner_dim)
        self.blocks = nn.ModuleList([AdapterBlock(inner_dim, heads) for _ in range(depth)])
        self.norm_out = nn.LayerNorm(inner_dim)
        self.out_proj = nn.Linear(inner_dim, features)
        nn.init.zeros_(self.out_proj.bias)
        nn.init.normal_(self.out_proj.weight, std=0.02)

    @staticmethod
    def _block_diag_mask(seqlens, device) -> torch.Tensor:
        total = int(sum(seqlens))
        mask = torch.zeros(total, total, dtype=torch.bool, device=device)
        offset = 0
        for length in seqlens:
            mask[offset:offset + length, offset:offset + length] = True
            offset += length
        return mask

    def forward(self, z_cat: torch.Tensor, seqlens=None) -> torch.Tensor:
        h = self.in_proj(z_cat)
        attn_mask = None
        if seqlens is not None and len(seqlens) > 1:
            attn_mask = self._block_diag_mask(seqlens, z_cat.device)[None, None]
        for block in self.blocks:
            h = block(h, attn_mask=attn_mask)
        return self.out_proj(self.norm_out(h))


class Refiner(nn.Module):
    """Flow-matching refiner: condition encoder + DiT + VAE decoder."""

    def __init__(self, config):
        super().__init__()
        self.config = RefinerConfig(**config.refiner)
        self.dit = RefinerDiT(self.config)
        self.code_dim = self.config.cond_code_dim
        emb_dim = self.config.emb_dim
        time_dim = self.config.adanln_dim

        self.inject_points = [i for i in range(self.config.num_layers)
                              if i % self.config.inject_interval == 0]
        self.point_to_head = {p: k for k, p in enumerate(self.inject_points)}
        self.cond_encoder = ConditionEncoder(
            self.config.cond_code_dim, self.config.cond_channels, time_dim=time_dim,
            num_resblocks=self.config.num_resblocks)
        self.heads = nn.ModuleList([
            InjectionHead(self.config.cond_channels, time_dim, emb_dim)
            for _ in self.inject_points])
        self.latent_head = InjectionHead(self.config.cond_channels, time_dim,
                                         self.config.in_channels)
        self.incontext_adapter = IncontextAdapter(
            self.config.cond_code_dim, emb_dim, depth=self.config.incontext_adapter_depth,
            heads=self.config.incontext_adapter_heads,
            inner_dim=self.config.incontext_adapter_dim)

        self.vae = RefinerVAE(latent_channels=int(config.vae["latent_channels"]))
        self.scheduler = FlowMatchScheduler()
        self.sampler = config.decode_sampler
        self.num_inference_steps = int(config.decode_num_inference_steps)
        self.seed = int(config.decode_seed)
        self.schedule_steps = int(config.one_step_schedule_steps)
        self.sr_scale = int(config.fixed_sr_scale)
        self.dtype = torch.bfloat16

    def _time_cond_per_sample(self, t_samples, device, dtype):
        return F.silu(self.dit.adaln_proj(self.dit.t_embedding(t_samples.to(dtype)))).to(dtype)

    def forward(self, llm_features, x, t, position_ids, indicator, cu_seqlens,
                z_q_packed, z_grid_list, img_grid_list, t_samples):
        device = x.device
        dtype = self.cond_encoder.in_proj.weight.dtype
        z_q_packed = z_q_packed.to(dtype)
        n = len(img_grid_list)
        cond_encoder = self.cond_encoder
        z_lens = [int(g[0]) * int(g[1]) for g in z_grid_list]

        c_vec = self._time_cond_per_sample(t_samples, device, dtype)

        z_all = cond_encoder.norm(z_q_packed)
        s_all, b_all, g_all = cond_encoder.time_mlp(c_vec).chunk(3, dim=-1)
        cond_interp = []
        offset = 0
        for i in range(n):
            h = z_all[:, offset:offset + z_lens[i]]
            offset += z_lens[i]
            h = cond_encoder._film_apply(h, s_all[i:i + 1], b_all[i:i + 1], g_all[i:i + 1])
            z_h, z_w = int(z_grid_list[i][0]), int(z_grid_list[i][1])
            t_h, t_w = int(img_grid_list[i][0]), int(img_grid_list[i][1])
            h = h.transpose(1, 2).reshape(1, self.code_dim, z_h, z_w)
            if (z_h, z_w) != (t_h, t_w):
                h = F.interpolate(h.float(), size=(t_h, t_w), mode="bilinear",
                                  align_corners=False).to(dtype)
            cond_interp.append(h.reshape(1, self.code_dim, t_h * t_w).transpose(1, 2))

        cond_cat = torch.cat(cond_interp, dim=1)
        c_segs = [c_vec[i:i + 1].expand(cond_interp[i].shape[1], -1) for i in range(n)]
        c_packed = torch.cat(c_segs, dim=0).unsqueeze(0)
        cond_packed = cond_encoder.refine(cond_cat, c_packed)

        def inject_fn(point):
            if point == -2:
                return self.latent_head(cond_packed, c_packed)
            return self.heads[self.point_to_head[point]](cond_packed, c_packed)

        context = self.incontext_adapter(z_q_packed, seqlens=z_lens)
        text_bool = indicator == LLM_TOKEN_INDICATOR
        llm_features = llm_features.clone()
        llm_features[text_bool] = context.reshape(-1, context.shape[-1]).to(llm_features.dtype)

        layers = set(self.inject_points)
        layers.add(-2)
        return self.dit(llm_features=llm_features, x=x, t=t, position_ids=position_ids,
                        indicator=indicator, cu_seqlens=cu_seqlens,
                        inject_fn=inject_fn, inject_layers=layers)

    def _empty_ctx(self, z_q):
        return z_q.new_zeros(1, z_q.shape[1], self.config.emb_dim)

    def _noise(self, shape, seed, device):
        generator = torch.Generator("cpu").manual_seed(int(seed))
        return torch.randn(shape, generator=generator, dtype=torch.float32).to(
            device=device, dtype=self.dtype)

    @torch.no_grad()
    def generate(self, z_q, z_grid, height, width):
        """Run the sampler for one condition grid and decode with the VAE."""
        height, width = int(height), int(width)
        steps = self.num_inference_steps
        if self.sampler == "one_step" and steps != 1:
            raise ValueError(f"one_step export requires 1 evaluation, got {steps}")

        patch = self.dit.patch_size * 8
        if height % patch or width % patch:
            raise ValueError(f"target size {width}x{height} must be divisible by {patch}")
        if z_q.dim() == 2:
            z_q = z_q.unsqueeze(0)
        if z_q.shape[1] != int(z_grid[0]) * int(z_grid[1]):
            raise ValueError(f"z_q length {z_q.shape[1]} != grid product {z_grid}")

        device = z_q.device
        batch = z_q.shape[0]
        z_q_list = [z_q[i:i + 1] for i in range(batch)]
        z_grid_list = [tuple(z_grid)] * batch
        context_list = [self._empty_ctx(z) for z in z_q_list]
        latent_h, latent_w = height // patch, width // patch
        latents = [self._noise((1, latent_h * latent_w, self.config.in_channels),
                               self.seed + i, device) for i in range(batch)]

        schedule_steps = self.schedule_steps if self.sampler == "one_step" else steps
        self.scheduler.set_timesteps(schedule_steps, denoising_strength=1.0,
                                     image_resolution=(height, width))
        for step in range(steps):
            timestep = self.scheduler.timesteps[step]
            preds = refiner_packed_forward(
                self, patch, latents, context_list, [float(timestep)] * batch,
                z_q_list, z_grid_list, [height] * batch, [width] * batch)
            if self.sampler == "native":
                latents = [self.scheduler.step(pred, timestep, latent)
                           for pred, latent in zip(preds, latents)]
            else:
                sigma = float(self.scheduler.sigmas[step])
                latents = [latent - sigma * pred for pred, latent in zip(preds, latents)]

        images = [self.vae.decode_latents(latent, height, width, self.dtype)
                  for latent in latents]
        return torch.cat(images, dim=0)

# ---------------------------------------------------------------------------
# VAE decoder
# ---------------------------------------------------------------------------

LATENT_SHIFT = (
    0.01984364, 0.10149707, 0.29689495, 0.27188619, -0.21445648, -0.15979549,
    0.05021099, -0.15083604, -0.15360136, -0.20131799, 0.01922352, 0.0622626,
    0.10140969, -0.06739428, 0.3758261, -0.233712, 0.35164491, -0.02590912,
    -0.0271935, -0.10833897, -0.1476848, -0.01130957, -0.2298372, 0.23526423,
    -0.10893522, 0.11957631, 0.04047799, 0.3134589, -0.17225064, -0.18646109,
    -0.34691978, -0.03571246, 0.02583857, 0.10190072, 0.28402294, 0.26952152,
    -0.21634675, -0.17938656, 0.04358909, -0.15007621, -0.1548502, -0.18971131,
    0.02710861, 0.05609494, 0.10697846, -0.06854968, 0.38167698, -0.24269937,
    0.35705471, -0.03063305, -0.02946109, -0.11244286, -0.14336038, -0.01362137,
    -0.21863696, 0.23228983, -0.11739769, 0.11693044, 0.02563311, 0.31356594,
    -0.17420591, -0.19006285, -0.34905377, -0.04025005, 0.01924137, 0.07652984,
    0.2995608, 0.2628057, -0.22011674, -0.12715361, 0.04879879, -0.14075719,
    -0.15935895, -0.2123584, 0.01974813, 0.05523547, 0.10011992, -0.06428964,
    0.37781868, -0.21491644, 0.34254215, -0.03153528, -0.0310082, -0.10761415,
    -0.14730405, -0.02475182, -0.2285588, 0.2515081, -0.10445128, 0.12446,
    0.07062869, 0.30880162, -0.18016875, -0.18869164, -0.34533499, -0.0129177,
    0.02578168, 0.07993659, 0.28642181, 0.26038408, -0.22459419, -0.14820155,
    0.04059549, -0.14043529, -0.16111187, -0.2020305, 0.02602069, 0.04852717,
    0.10432153, -0.06309942, 0.38402443, -0.22397003, 0.34814481, -0.03774432,
    -0.03381438, -0.11245691, -0.14128767, -0.02853208, -0.21752016, 0.24872463,
    -0.11399775, 0.1222687, 0.05620835, 0.309178, -0.18065738, -0.19401479,
    -0.34495114, -0.01760592,
)

LATENT_SCALE = (
    1.63933691, 1.70204478, 1.73642566, 1.90004803, 1.6675316, 1.69059584,
    1.56853198, 1.62314944, 1.89106626, 1.58086668, 1.60822129, 1.60962993,
    1.63322129, 1.56074359, 1.73419528, 1.7919265, 1.64040632, 1.66802808,
    1.60390303, 1.75480492, 1.63187587, 1.64334594, 1.61722884, 1.60146046,
    1.63459219, 1.55291476, 1.68771497, 1.68415657, 1.78966054, 1.66631641,
    1.65626686, 1.65976433, 1.63487607, 1.69513249, 1.72933756, 1.91310663,
    1.67035057, 1.72286863, 1.56719251, 1.61934825, 1.88628859, 1.56911539,
    1.59455129, 1.60829869, 1.62470611, 1.56052853, 1.73677003, 1.77563606,
    1.63732541, 1.66370527, 1.59508952, 1.75153949, 1.63029275, 1.64517667,
    1.61659342, 1.59722044, 1.64103121, 1.5408531, 1.68610394, 1.67772755,
    1.78998563, 1.66621713, 1.65458955, 1.66041308, 1.64710857, 1.68163503,
    1.74000294, 1.92784786, 1.67411194, 1.67395548, 1.57406532, 1.62199356,
    1.87618195, 1.5584375, 1.57438785, 1.61711053, 1.63094305, 1.55644029,
    1.73124302, 1.80666627, 1.6463621, 1.65932006, 1.60816188, 1.75682671,
    1.64695873, 1.63121722, 1.61380832, 1.60478651, 1.63396035, 1.53505068,
    1.65534289, 1.67132281, 1.80317197, 1.6767314, 1.65700938, 1.68426259,
    1.65339716, 1.67540638, 1.73298504, 1.94067348, 1.67893609, 1.70635117,
    1.5730906, 1.61928553, 1.87148809, 1.56244866, 1.56697152, 1.61584394,
    1.62759496, 1.55480378, 1.73484107, 1.79055143, 1.64688773, 1.66121492,
    1.60135887, 1.75254572, 1.64798332, 1.62989921, 1.61381592, 1.60792883,
    1.63939668, 1.53075757, 1.65371318, 1.66801185, 1.80029087, 1.67591476,
    1.65655173, 1.68533454,
)


class VAEResnetBlock(nn.Module):
    def __init__(self, in_channels: int, out_channels: int):
        super().__init__()
        self.norm1 = nn.GroupNorm(32, in_channels, eps=1e-6, affine=True)
        self.conv1 = nn.Conv2d(in_channels, out_channels, 3, stride=1, padding=1)
        self.norm2 = nn.GroupNorm(32, out_channels, eps=1e-6, affine=True)
        self.conv2 = nn.Conv2d(out_channels, out_channels, 3, stride=1, padding=1)
        self.nonlinearity = nn.SiLU()
        self.conv_shortcut = (
            nn.Conv2d(in_channels, out_channels, 1, stride=1, padding=0)
            if in_channels != out_channels else None)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        h = self.conv1(self.nonlinearity(self.norm1(x)))
        h = self.conv2(self.nonlinearity(self.norm2(h)))
        if self.conv_shortcut is not None:
            x = self.conv_shortcut(x.contiguous())
        return x + h


class VAEAttention(nn.Module):
    def __init__(self, dim: int, num_heads: int):
        super().__init__()
        self.num_heads = num_heads
        self.head_dim = dim // num_heads
        self.group_norm = nn.GroupNorm(32, dim, eps=1e-6, affine=True)
        self.to_q = nn.Linear(dim, dim, bias=True)
        self.to_k = nn.Linear(dim, dim, bias=True)
        self.to_v = nn.Linear(dim, dim, bias=True)
        self.to_out = nn.ModuleList([nn.Linear(dim, dim), nn.Dropout(0.0)])

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        residual = x
        batch, channels, height, width = x.shape
        h = x.view(batch, channels, height * width).transpose(1, 2)
        h = self.group_norm(h.transpose(1, 2)).transpose(1, 2)

        q = self.to_q(h).view(batch, -1, self.num_heads, self.head_dim).transpose(1, 2)
        k = self.to_k(h).view(batch, -1, self.num_heads, self.head_dim).transpose(1, 2)
        v = self.to_v(h).view(batch, -1, self.num_heads, self.head_dim).transpose(1, 2)
        out = F.scaled_dot_product_attention(q, k, v, attn_mask=None, dropout_p=0.0, is_causal=False)
        out = out.transpose(1, 2).reshape(batch, -1, self.num_heads * self.head_dim).to(q.dtype)
        out = self.to_out[1](self.to_out[0](out))
        return out.transpose(-1, -2).reshape(batch, channels, height, width) + residual


class VAEUpsample(nn.Module):
    def __init__(self, channels: int):
        super().__init__()
        self.conv = nn.Conv2d(channels, channels, 3, padding=1, bias=True)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        dtype = x.dtype
        if dtype == torch.bfloat16:
            x = x.to(torch.float32)
        x = F.interpolate(x, scale_factor=2.0, mode="nearest")
        if dtype == torch.bfloat16:
            x = x.to(dtype)
        return self.conv(x)


class VAEDecoder(nn.Module):
    """VAE decoder (latent 32ch -> RGB, 16x spatial upsampling)."""

    def __init__(self, latent_channels: int = 32):
        super().__init__()
        block_out_channels = (128, 256, 512, 512)
        self.conv_in = nn.Conv2d(latent_channels, block_out_channels[-1], 3, padding=1)

        self.mid_block = nn.Module()
        self.mid_block.resnets = nn.ModuleList([
            VAEResnetBlock(512, 512), VAEResnetBlock(512, 512)])
        self.mid_block.attentions = nn.ModuleList([VAEAttention(512, num_heads=1)])

        reversed_channels = list(reversed(block_out_channels))
        blocks = []
        for i in range(len(block_out_channels)):
            in_channels = reversed_channels[i - 1] if i > 0 else reversed_channels[0]
            out_channels = reversed_channels[i]
            resnets = nn.ModuleList([
                VAEResnetBlock(in_channels if j == 0 else out_channels, out_channels)
                for j in range(3)])
            upsamplers = (nn.ModuleList([VAEUpsample(out_channels)])
                          if i < len(block_out_channels) - 1 else None)
            block = nn.Module()
            block.resnets = resnets
            block.upsamplers = upsamplers
            blocks.append(block)
        self.up_blocks = nn.ModuleList(blocks)

        self.conv_norm_out = nn.GroupNorm(32, block_out_channels[0], eps=1e-6)
        self.conv_act = nn.SiLU()
        self.conv_out = nn.Conv2d(block_out_channels[0], 3, 3, padding=1)

    def forward(self, sample: torch.Tensor) -> torch.Tensor:
        sample = self.conv_in(sample)
        sample = self.mid_block.resnets[0](sample)
        sample = self.mid_block.attentions[0](sample)
        sample = self.mid_block.resnets[1](sample)
        for block in self.up_blocks:
            for resnet in block.resnets:
                sample = resnet(sample)
            if block.upsamplers is not None:
                sample = block.upsamplers[0](sample)
        return self.conv_out(self.conv_act(self.conv_norm_out(sample)))


class RefinerVAE(nn.Module):
    def __init__(self, latent_channels: int = 32):
        super().__init__()
        self.post_quant_conv = nn.Conv2d(latent_channels, latent_channels, 1)
        self.decoder = VAEDecoder(latent_channels)

    def decode_latents(self, latents: torch.Tensor, height: int, width: int,
                       torch_dtype: torch.dtype) -> torch.Tensor:
        shift = torch.tensor(LATENT_SHIFT, dtype=torch.float32, device=latents.device)
        scale = torch.tensor(LATENT_SCALE, dtype=torch.float32, device=latents.device)
        latents = latents.float() * scale + shift
        latents = rearrange(latents, "B (H W) (P Q C) -> B C (H P) (W Q)",
                            P=2, Q=2, H=height // 16, W=width // 16)
        latents = latents.to(torch.bfloat16).to(torch_dtype)
        return self.decoder(self.post_quant_conv(latents))


# ---------------------------------------------------------------------------
# flow-matching sampler
# ---------------------------------------------------------------------------

class FlowMatchScheduler:
    """Log-SNR sigma table with Euler steps in sigma space."""

    def __init__(self) -> None:
        self.num_train_timesteps = 1000

    @staticmethod
    def _build_sigmas(num_inference_steps=50, denoising_strength=1.0,
                                image_resolution=(1024, 1024), mu=0.0, std=1.5):
        num_pixels = image_resolution[0] * image_resolution[1]
        mean = mu + 0.5 * math.log(num_pixels / (512 * 512))
        logsnr_min, logsnr_max = -15.0, 18.0
        t_min = 1.0 / (1 + math.exp(0.5 * logsnr_max))
        t_max = 1.0 / (1 + math.exp(0.5 * logsnr_min))
        step_intervals = torch.linspace(0.0, denoising_strength, num_inference_steps + 1,
                                        dtype=torch.float64)
        sigmas = []
        for i in range(num_inference_steps + 1):
            z = torch.special.ndtri(step_intervals[i])
            y = mean + std * z
            t_ = 1 - torch.special.expit(y)
            t_ = t_.clamp(t_min, t_max)
            sigmas.append(float(t_.to(torch.float32)))
        sigmas = torch.tensor(sigmas, dtype=torch.float32)
        one_minus_t = (1 - sigmas)[:-1].flip(0)
        sigma_start = one_minus_t[0] * denoising_strength
        if one_minus_t[0] > 0:
            one_minus_t = one_minus_t * (sigma_start / one_minus_t[0])
        sigmas = sigmas.flip(dims=(0,))
        timesteps = sigmas[:-1]
        sigmas = (1 - sigmas)[:-1]
        return sigmas, timesteps

    def set_timesteps(self, num_inference_steps=100, denoising_strength=1.0, **kwargs):
        self.sigmas, self.timesteps = self._build_sigmas(
            num_inference_steps=num_inference_steps,
            denoising_strength=denoising_strength,
            **kwargs)

    def step(self, model_output, timestep, sample):
        if isinstance(timestep, torch.Tensor):
            timestep = timestep.cpu()
        timestep_id = torch.argmin((self.timesteps - timestep).abs())
        sigma = self.sigmas[timestep_id]
        sigma_next = 0 if timestep_id + 1 >= len(self.timesteps) else self.sigmas[timestep_id + 1]
        return sample + model_output * (sigma_next - sigma)


# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# model
# ---------------------------------------------------------------------------


# model API
# ---------------------------------------------------------------------------


@dataclass
class EncodeOutput:
    """Discrete tokenizer output (raster token ids plus codebook-space features)."""

    indices: torch.Tensor
    out_grid_thw: torch.Tensor
    quants: torch.Tensor
    codebook_quant: torch.Tensor


class dNaViTTokenizer(PreTrainedModel):
    """dNaViT: discrete tokenizer with a conditional flow-matching refiner.

    Holds the vision encoder, product quantizer, pixel decoder, token unmerger
    and the refiner (DiT + VAE decoder). ``forward`` and ``decode`` run both the
    pixel decoder and the refiner and return the color-fixed refiner output.
    """

    config_class = DNaViTConfig

    def __init__(self, config: DNaViTConfig):
        super().__init__(config)
        self.torch_dtype = torch.bfloat16
        self.encoder = UnifiedEncoder(config)
        self.quantizer = ProductQuantizer(
            in_dim=self.encoder.merger_out_dim,
            out_dim=int(config.pixel_decoder["width"]),
            code_dim=int(config.quantizer["code_dim"]),
            num_groups=int(config.quantizer["num_groups"]),
            codebook_size=int(config.quantizer["codebook_size"]),
            proj_hidden=int(config.quantizer["proj_hidden"]),
        )
        self.pixel_decoder = PixelDecoder(config)
        self.unmerger = TokenUnmerger(self.pixel_decoder.width,
                                      self.encoder.spatial_merge_size ** 2)
        self.refiner = Refiner(config)

    @property
    def patch_size(self) -> int:
        return self.encoder.patch_size

    @property
    def spatial_merge_size(self) -> int:
        return self.encoder.spatial_merge_size

    # ---- tokenizer -------------------------------------------------------
    @torch.no_grad()
    def encode(self, pixel_values, grid_thw=None) -> EncodeOutput:
        """Encode images into discrete ids plus codebook-space features.

        ``pixel_values`` is a list of ``(3, H, W)`` tensors in ``[-1, 1]``;
        ``grid_thw`` is a ``(B, 3)`` patch grid (derived from the tensors when
        omitted).
        """
        if grid_thw is None:
            grid_thw = torch.tensor(
                [[1, int(t.shape[-2]) // self.patch_size, int(t.shape[-1]) // self.patch_size]
                 for t in pixel_values], dtype=torch.long)
        elif not torch.is_tensor(grid_thw):
            grid_thw = torch.as_tensor(grid_thw, dtype=torch.long)
        grid_thw = grid_thw.to(self.device)

        device_type = self.device.type
        with torch.autocast(device_type, dtype=self.torch_dtype,
                            enabled=(device_type == "cuda")):
            z, _ = self.encoder(pixel_values, grid_thw)
            quants, codes, codebook_quant = self.quantizer(z)
        return EncodeOutput(
            indices=codes.long(),
            out_grid_thw=self._merged_grid(grid_thw),
            quants=quants,
            codebook_quant=codebook_quant,
        )

    @torch.no_grad()
    def forward(self, pixel_values, image_grid_thw=None):
        """Images -> color-fixed refiner reconstructions (list of PIL images)."""
        images = [self._round_input(t.to(self.device, self.torch_dtype))
                  for t in pixel_values]
        out = self.encode(images, image_grid_thw)
        grids = out.out_grid_thw
        sizes = [int(row[1]) * int(row[2]) for row in grids]
        flat = out.indices.reshape(-1, out.indices.shape[-1])
        return [self.decode(chunk, int(grids[i][1]), int(grids[i][2]))[0]
                for i, chunk in enumerate(torch.split(flat, sizes))]

    @torch.no_grad()
    def decode(self, indices, grid_h, grid_w):
        """Discrete ids -> color-fixed refiner reconstructions (list of PIL images)."""
        idx = indices
        if idx.dim() == 4:
            idx = idx.reshape(idx.shape[0], -1, idx.shape[-1])
        if idx.dim() == 2:
            idx = idx.unsqueeze(0)
        grid = torch.tensor([[1, int(grid_h), int(grid_w)]] * idx.shape[0], dtype=torch.long)
        return self._render(idx, grid)

    # ---- internals -------------------------------------------------------
    def _merged_grid(self, grid_thw):
        grid = grid_thw.clone().long()
        grid[:, 1] //= self.spatial_merge_size
        grid[:, 2] //= self.spatial_merge_size
        return grid

    def _round_input(self, x):
        multiple = self.patch_size * self.spatial_merge_size
        height, width = int(x.shape[-2]), int(x.shape[-1])
        h = (height + multiple - 1) // multiple * multiple
        w = (width + multiple - 1) // multiple * multiple
        if (h, w) != (height, width):
            x = F.interpolate(x.unsqueeze(0), size=(h, w), mode="bicubic",
                              align_corners=False, antialias=True)[0]
        return x

    def _indices_to_codebook_quant(self, indices, grid_h, grid_w):
        idx = indices.to(device=self.device, dtype=torch.long)
        grid_h, grid_w = int(grid_h), int(grid_w)
        groups = self.quantizer.num_groups
        if idx.dim() == 2:
            idx = idx.reshape(1, grid_h * grid_w, groups)
        elif idx.dim() == 3:
            idx = idx.reshape(idx.shape[0], grid_h * grid_w, groups)
        elif idx.dim() == 4:
            if tuple(idx.shape[1:3]) != (grid_h, grid_w):
                raise ValueError(f"indices grid {tuple(idx.shape[1:3])} != {(grid_h, grid_w)}")
            idx = idx.reshape(idx.shape[0], grid_h * grid_w, groups)
        else:
            raise ValueError(f"indices must be 2D/3D/4D, got {tuple(idx.shape)}")
        z_q = self.quantizer.codebook_embeddings(idx)
        return z_q.to(device=self.device, dtype=self.torch_dtype)

    def _pixel_decode(self, indices, grid_h, grid_w):
        device_type = self.device.type
        with torch.autocast(device_type, dtype=self.torch_dtype,
                            enabled=(device_type == "cuda")):
            batch = indices.shape[0]
            flat = indices.reshape(batch, grid_h * grid_w, indices.shape[-1])
            z = self.quantizer.get_codebook_entry(flat).reshape(
                batch, grid_h * grid_w, self.pixel_decoder.width)
            z = self.unmerger(z)
            uh, uw = grid_h * self.spatial_merge_size, grid_w * self.spatial_merge_size
            if uh == self.pixel_decoder.grid_size and uw == self.pixel_decoder.grid_size:
                return self.pixel_decoder(z, image_grid_thw=None)
            grid = torch.tensor([[1, uh, uw]] * batch, device=z.device, dtype=torch.long)
            out = self.pixel_decoder(z.reshape(batch * uh * uw, z.shape[-1]),
                                     image_grid_thw=grid)
            return torch.stack(list(out), dim=0)

    def _render(self, indices, out_grid_thw):
        images = []
        for b in range(indices.shape[0]):
            gh, gw = int(out_grid_thw[b][1]), int(out_grid_thw[b][2])
            idx = indices[b:b + 1].to(self.device)
            z_q = self._indices_to_codebook_quant(idx, gh, gw)
            height = gh * self.patch_size * self.spatial_merge_size * self.refiner.sr_scale
            width = gw * self.patch_size * self.spatial_merge_size * self.refiner.sr_scale
            rec = self.refiner.generate(z_q, (gh, gw), height, width)
            ref = self._pixel_decode(idx, gh, gw)
            rec_image = self._to_pil(rec[0])
            ref_image = self._to_pil(ref[0]).resize(rec_image.size)
            images.append(_wavelet_color_fix(rec_image, ref_image))
        return images

    @staticmethod
    def _to_pil(tensor):
        if tensor.dim() == 4:
            tensor = tensor[0]
        array = ((tensor + 1.0) * (255 / 2)).clip(0, 255).to(torch.uint8)
        return Image.fromarray(array.permute(1, 2, 0).cpu().numpy())

# ---------------------------------------------------------------------------
# shared utilities
# ---------------------------------------------------------------------------


def _rotate_half(x: torch.Tensor) -> torch.Tensor:
    half = x.shape[-1] // 2
    return torch.cat((-x[..., half:], x[..., :half]), dim=-1)


def _apply_rotary_pos_emb(q, k, cos, sin):
    cos = cos.unsqueeze(1)
    sin = sin.unsqueeze(1)
    return (q * cos) + (_rotate_half(q) * sin), (k * cos) + (_rotate_half(k) * sin)


def _sinusoidal_embedding(t: torch.Tensor, dim: int, scale: float = 1e4) -> torch.Tensor:
    t = t.to(torch.float32)
    half = dim // 2
    freq = math.log(scale) / (half - 1)
    freq = torch.exp(torch.arange(half, dtype=torch.float32, device=t.device) * -freq)
    emb = torch.cat([torch.sin(t.unsqueeze(-1) * freq), torch.cos(t.unsqueeze(-1) * freq)], dim=-1)
    if dim % 2 == 1:
        emb = F.pad(emb, (0, 1))
    return emb


def modulate(x: torch.Tensor, shift: torch.Tensor, scale: torch.Tensor) -> torch.Tensor:
    return x * (1 + scale) + shift


def _varlen_attention(q, k, v, cu_seqlens):
    """Block-diagonal attention over packed ``(tokens, heads, head_dim)`` tensors.

    Prefers FlashAttention-3, then FlashAttention-2; falls back to per-segment
    ``scaled_dot_product_attention`` when neither is installed (e.g. CPU or a
    torch-only environment).
    """
    if FLASH_ATTN_AVAILABLE and q.is_cuda and q.dtype in (torch.float16, torch.bfloat16):
        max_seqlen = int((cu_seqlens[1:] - cu_seqlens[:-1]).max().item())
        if _HAS_FLASH_ATTN_3:
            out = flash_attn_interface.flash_attn_varlen_func(
                q, k, v, cu_seqlens_q=cu_seqlens, cu_seqlens_k=cu_seqlens,
                max_seqlen_q=max_seqlen, max_seqlen_k=max_seqlen,
                softmax_scale=None, causal=False, window_size=(-1, -1))
            return out[0] if isinstance(out, tuple) else out
        return flash_attn.flash_attn_varlen_func(
            q, k, v, cu_seqlens_q=cu_seqlens, cu_seqlens_k=cu_seqlens,
            max_seqlen_q=max_seqlen, max_seqlen_k=max_seqlen,
            softmax_scale=None, causal=False, window_size=(-1, -1))

    outs = []
    for i in range(cu_seqlens.numel() - 1):
        qs, qe = int(cu_seqlens[i]), int(cu_seqlens[i + 1])
        q_i = q[qs:qe].transpose(0, 1).unsqueeze(0)
        k_i = k[qs:qe].transpose(0, 1).unsqueeze(0)
        v_i = v[qs:qe].transpose(0, 1).unsqueeze(0)
        outs.append(F.scaled_dot_product_attention(q_i, k_i, v_i).squeeze(0).transpose(0, 1))
    return torch.cat(outs, dim=0)


def build_packed_layout(text_len, grid_h, grid_w, device):
    """Packed ``text + image`` sample layout used by the refiner."""
    img_len = grid_h * grid_w
    length = text_len + img_len
    h_idx = torch.arange(grid_h, device=device).view(-1, 1).expand(grid_h, grid_w).reshape(-1)
    w_idx = torch.arange(grid_w, device=device).view(1, -1).expand(grid_h, grid_w).reshape(-1)
    image_pos = torch.stack([torch.zeros_like(h_idx), h_idx, w_idx], dim=1) + IMAGE_POSITION_OFFSET

    position_ids = torch.zeros(1, length, 3, dtype=torch.long, device=device)
    if text_len > 0:
        tp = torch.arange(text_len, device=device)
        position_ids[0, :text_len] = torch.stack([tp, tp, tp], dim=1)
    position_ids[0, text_len:] = image_pos

    indicator = torch.zeros(1, length, dtype=torch.long, device=device)
    indicator[0, :text_len] = LLM_TOKEN_INDICATOR
    indicator[0, text_len:] = OUTPUT_IMAGE_INDICATOR
    return {"position_ids": position_ids, "indicator": indicator,
            "text_len": text_len, "img_len": img_len, "length": length}


def refiner_packed_forward(refiner, patch, latents_list, context_list, t_list,
                           z_q_list, z_grid_list, height_list, width_list):
    """Run one packed multi-sample refiner forward; returns per-sample velocities."""
    device = latents_list[0].device
    n = len(latents_list)
    channels = latents_list[0].shape[-1]
    context_dim = context_list[0].shape[-1]

    seg_lens, img_slices = [], []
    seqs_x, seqs_pos, seqs_ind, seqs_t = [], [], [], []
    img_grid_list, offset = [], 0
    for i in range(n):
        gh = height_list[i] // patch
        gw = width_list[i] // patch
        img_grid_list.append((gh, gw))
        text_len = context_list[i].shape[1]
        layout = build_packed_layout(text_len, gh, gw, device)
        length = layout["length"]
        x_seg = torch.cat([torch.zeros(1, text_len, channels, dtype=latents_list[i].dtype, device=device),
                           latents_list[i]], dim=1)
        seqs_x.append(x_seg)
        seqs_pos.append(layout["position_ids"])
        seqs_ind.append(layout["indicator"])
        seqs_t.append(torch.full((1, length), float(t_list[i]), dtype=torch.float32, device=device))
        seg_lens.append(length)
        img_slices.append((offset + text_len, offset + text_len + layout["img_len"]))
        offset += length

    x = torch.cat(seqs_x, dim=1)
    position_ids = torch.cat(seqs_pos, dim=1)
    indicator = torch.cat(seqs_ind, dim=1)
    t_packed = torch.cat(seqs_t, dim=1)

    context = torch.zeros(1, x.shape[1], context_dim, dtype=context_list[0].dtype, device=device)
    for i in range(n):
        start = sum(seg_lens[:i])
        text_len = context_list[i].shape[1]
        context[0, start:start + text_len] = context_list[i][0]

    z_q_packed = torch.cat(z_q_list, dim=1)
    cu_seqlens = torch.tensor([0] + seg_lens, dtype=torch.int32, device=device).cumsum(0).to(torch.int32)
    t_samples = torch.tensor([float(v) for v in t_list], dtype=torch.float32, device=device)

    out = refiner(llm_features=context, x=x, t=t_packed, position_ids=position_ids,
                  indicator=indicator, cu_seqlens=cu_seqlens, z_q_packed=z_q_packed,
                  z_grid_list=z_grid_list, img_grid_list=img_grid_list, t_samples=t_samples)
    return [-out[:, start:end] for (start, end) in img_slices]


def _wavelet_color_fix(target: Image.Image, source: Image.Image) -> Image.Image:
    to_tensor = ToTensor()
    target_tensor = to_tensor(target).unsqueeze(0)
    source_tensor = to_tensor(source).unsqueeze(0)

    content_high, content_low = _wavelet_decompose(target_tensor)
    del content_low
    style_high, style_low = _wavelet_decompose(source_tensor)
    del style_high
    result = content_high + style_low
    return ToPILImage()(result.squeeze(0).clamp_(0.0, 1.0))


def _wavelet_decompose(image: torch.Tensor, levels: int = 5):
    high = torch.zeros_like(image)
    for i in range(levels):
        radius = 2 ** i
        low = _wavelet_blur(image, radius)
        high = high + (image - low)
        image = low
    return high, image


def _wavelet_blur(image: torch.Tensor, radius: int) -> torch.Tensor:
    kernel = torch.tensor(
        [[0.0625, 0.125, 0.0625], [0.125, 0.25, 0.125], [0.0625, 0.125, 0.0625]],
        dtype=image.dtype, device=image.device)
    kernel = kernel[None, None].repeat(3, 1, 1, 1)
    image = F.pad(image, (radius, radius, radius, radius), mode="replicate")
    return F.conv2d(image, kernel, groups=3, dilation=radius)
