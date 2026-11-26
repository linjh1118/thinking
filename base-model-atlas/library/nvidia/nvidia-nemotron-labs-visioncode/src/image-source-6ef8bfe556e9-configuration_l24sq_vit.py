# SPDX-FileCopyrightText: Copyright (c) 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: LicenseRef-NvidiaProprietary
#
# Use of this file is governed by the NVIDIA License in the repository root
# (LICENSE).

"""HuggingFace-style configuration for the L24-SQ Llama ViT tokenizer."""

from __future__ import annotations

from typing import Tuple

from transformers import PretrainedConfig


class L24SQViTConfig(PretrainedConfig):
    """Config for the Llama-ViT VQ tokenizer with Leech-lattice codebook.

    Matches `transcoder.models.llamabsqvit_anyres.VITVQModel` initialised from
    `configs/tokenizer/l24sq_ll_p16x16_min256x256_max1024x1024.yaml`.
    """

    model_type = "l24sq_vit"

    def __init__(
        self,
        # ViT backbone
        patch_size: int = 16,
        width: int = 1024,
        layers: int = 24,
        heads: int = 16,
        mlp_ratio: float = 4.0,
        vit_rope_theta: float = 10000.0,
        image_size: int = 256,
        # Decoder head
        use_ffn_output: bool = True,
        dim_ffn_output: int = 3072,
        # Quantizer
        n_embed: int = 196_560,
        embed_dim: int = 24,
        l2_norm: bool = True,
        # Distill head (kept so the conv_out / distill_mlp weights load cleanly)
        distill_depth: int = 3,
        distill_output_dim: int | None = None,
        # Input normalisation
        zero_mean: bool = True,
        size_divisor: int = 16,
        clamp_range: Tuple[float, float] = (-1.0, 1.0),
        **kwargs,
    ):
        self.patch_size = patch_size
        self.width = width
        self.layers = layers
        self.heads = heads
        self.mlp_ratio = mlp_ratio
        self.vit_rope_theta = vit_rope_theta
        self.image_size = image_size
        self.use_ffn_output = use_ffn_output
        self.dim_ffn_output = dim_ffn_output
        self.n_embed = n_embed
        self.embed_dim = embed_dim
        self.l2_norm = l2_norm
        self.distill_depth = distill_depth
        self.distill_output_dim = distill_output_dim
        self.zero_mean = zero_mean
        self.size_divisor = size_divisor
        self.clamp_range = tuple(clamp_range)
        super().__init__(**kwargs)
