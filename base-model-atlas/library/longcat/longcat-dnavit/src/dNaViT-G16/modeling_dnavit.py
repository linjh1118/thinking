"""dNaViT: discrete native-resolution visual tokenizer.

A Qwen3-VL-based 32x encoder (G16/G64 product quantizer, ResMod feature
enhancement) with a ViT pixel decoder. Images are encoded into discrete ids
and reconstructed at the original resolution by the pixel decoder.

Only the inference path is implemented; every parameter lives in
``model.safetensors`` next to this file.
"""

from dataclasses import dataclass

import torch
import torch.nn as nn
import torch.nn.functional as F
from einops.layers.torch import Rearrange
from PIL import Image
from timm.layers import Mlp
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


@dataclass
class EncodeOutput:
    """Discrete tokenizer output (raster token ids plus codebook-space features)."""

    indices: torch.Tensor
    out_grid_thw: torch.Tensor
    quants: torch.Tensor
    codebook_quant: torch.Tensor


class dNaViTTokenizer(PreTrainedModel):
    """dNaViT discrete tokenizer: encoder + product quantizer + pixel decoder.

    ``forward`` and ``decode`` return the pixel-decoder reconstruction at the
    input resolution.
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
        """Images -> pixel-decoder reconstructions (list of PIL images)."""
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
        """Discrete ids -> pixel-decoder reconstructions (list of PIL images)."""
        idx = indices
        if idx.dim() == 4:
            idx = idx.reshape(idx.shape[0], -1, idx.shape[-1])
        if idx.dim() == 2:
            idx = idx.unsqueeze(0)
        return [self._to_pil(self._pixel_decode(idx[b:b + 1],
                                                int(grid_h), int(grid_w))[0])
                for b in range(idx.shape[0])]

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

    @staticmethod
    def _to_pil(tensor):
        if tensor.dim() == 4:
            tensor = tensor[0]
        array = ((tensor + 1.0) * (255 / 2)).clip(0, 255).to(torch.uint8)
        return Image.fromarray(array.permute(1, 2, 0).cpu().numpy())
