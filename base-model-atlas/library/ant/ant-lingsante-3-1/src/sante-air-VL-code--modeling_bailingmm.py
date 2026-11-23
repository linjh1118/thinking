#!/usr/bin/env python3
# coding=utf-8
# Copyright (c) Ant Group. All rights reserved.

import copy
import glob
import os
from typing import Any, Dict, Optional, Tuple

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from transformers import GenerationConfig

from bailingmm.common.logger import logger
from bailingmm.common.utils import is_url
from bailingmm.models.bailingmm.configuration_bailingmm import BailingMMConfig
from bailingmm.models.bailingmm.llm_builder import build_llm_model
from bailingmm.models.bailingmm.loss_func_utils import get_loss_func
from bailingmm.models.bailingmm.qwen2_utils import prepare_inputs_embeds
from bailingmm.models.blip2_models.blip2 import Blip2Base  # noqa
from bailingmm.models.dynamic_imports import Qwen3MoeVisionTransformer  # noqa
from bailingmm.models.dynamic_imports import WhisperEncoder  # noqa
from bailingmm.models.qwen2_5_vit import Qwen2_5_VisionTransformer  # noqa
from bailingmm.models.qwen2vl_vit import Qwen2VisionTransformer  # noqa
from bailingmm.utils.global_context import context as antmmf_context

# vision encoder
from bailingmm.models.siglip_encoder import SigLipVisionTower  # noqa

# audio encoder
from .audio_encoder import SANMEncoder
from .modeling_utils import (
    Transpose,
    encode_audio_segments,
    get_model_input_handler,
)

VISION_ENCODER_CLASS_DICT = {
    "SigLipVisionTower": SigLipVisionTower,
    "Qwen2VisionTransformer": Qwen2VisionTransformer,
    "Qwen2_5_VisionTransformer": Qwen2_5_VisionTransformer,
    "Qwen3MoeVisionTransformer": Qwen3MoeVisionTransformer,
}

AUDIO_ENCODER_CLASS_DICT = {
    "sanm": SANMEncoder,
    "whisper_large_v3": WhisperEncoder,
}

def _antmmf_finalize_model_grads_func(model, num_tokens=None):
    """Finalize model grads for BailingMM with CP support for vision encoder.

    This function handles gradient all-reduce across context parallel ranks for
    vision encoder parameters when sequence parallel is enabled.
    """
    from megatron.core.distributed import finalize_model_grads
    from megatron.core import parallel_state

    if not (parallel_state.is_pipeline_first_stage() and model[0].module.module.vision.config.sequence_parallel):
        finalize_model_grads(model, num_tokens)
        return

    # All-reduce gradients before finalize (excluding merger)
    for name, param in model[0].module.module.vision.named_parameters():
        if hasattr(param, 'main_grad') and 'merger' not in name:
            torch.distributed.all_reduce(param.main_grad, group=parallel_state.get_context_parallel_group())

    finalize_model_grads(model, num_tokens)

    # All-reduce gradients after finalize
    for name, param in model[0].module.module.vision.named_parameters():
        if hasattr(param, 'main_grad'):
            torch.distributed.all_reduce(param.main_grad, group=parallel_state.get_context_parallel_group())

class BailingMM(Blip2Base):
    PRETRAINED_MODEL_CONFIG_DICT = {
        "bailing_mm_pretrain": "configs/models/blip2/bailing_mm_pretrain_interleave.yaml",
        "bailing_mm_pretrain_llama3_eva_clip_400m": "configs/models/blip2/bailing_mm_pretrain_interleave_llama3_eva_clip_400m.yaml",
        "bailing_mm_pretrain_llama3_eva_clip_400m_448": "configs/models/blip2/bailing_mm_pretrain_interleave_llama3_eva_clip_400m_448.yaml",
        "bailing_mm_pretrain_llama3_eva_clip_400m_448_multi_patch": "configs/models/blip2/bailing_mm_pretrain_interleave_llama3_eva_clip_400m_448_multi_patch.yaml",
        "bailing_mm_pretrain_llama3.1_eva_clip_400m": "configs/models/blip2/bailing_mm_pretrain_interleave_llama3_1_eva_clip_400m.yaml",
        "bailing_mm_pretrain_llama3.1_eva_clip_400m_448": "configs/models/blip2/bailing_mm_pretrain_interleave_llama3_1_eva_clip_400m_448.yaml",
        "bailing_mm_pretrain_llama3.1_eva_clip_400m_448_multi_patch": "configs/models/blip2/bailing_mm_pretrain_interleave_llama3_1_eva_clip_400m_448_multi_patch.yaml",
        "bailing_mm_pretrain_llama3.1_70b_eva_clip_400m": "configs/models/blip2/bailing_mm_pretrain_interleave_llama3_1_70b_eva_clip_400m.yaml",
        "bailing_mm_pretrain_llama3.1_70b_eva_clip_400m_448": "configs/models/blip2/bailing_mm_pretrain_interleave_llama3_1_70b_eva_clip_400m_448.yaml",
        "bailing_mm_pretrain_llama3.1_70b_eva_clip_400m_448_multi_patch": "configs/models/blip2/bailing_mm_pretrain_interleave_llama3_1_70b_eva_clip_400m_448_multi_patch.yaml",
        "bailing_mm_pretrain_bailingv4_siglip_400m_448": "configs/models/blip2/bailing_mm_pretrain_interleave_bailingv4_siglip_400m_448.yaml",
        "bailing_mm_pretrain_bailingv4_siglip_400m_448_multi_patch": "configs/models/blip2/bailing_mm_pretrain_interleave_bailingv4_siglip_400m_448_multi_patch.yaml",
        "bailing_mm_pretrain_llama3.1_internvit_6b_448": "configs/models/blip2/bailing_mm_pretrain_interleave_llama3_1_internvit_6b_448.yaml",
        "bailing_mm_pretrain_llama3.1_internvit_6b_448_multi_patch": "configs/models/blip2/bailing_mm_pretrain_interleave_llama3_1_internvit_6b_448_multi_patch.yaml",
        "bailing_mm_pretrain_llama3.1_vit_600m": "configs/models/blip2/bailing_mm_pretrain_interleave_llama3_1_vit_600m.yaml",
        "bailing_mm_pretrain_llama3.1_70b_vit_600m": "configs/models/blip2/bailing_mm_pretrain_interleave_llama3_1_70b_vit_600m.yaml",
        "bailing_mm_pretrain_llama3.3_70b_vit_600m": "configs/models/blip2/bailing_mm_pretrain_interleave_llama3_3_70b_vit_600m.yaml",
        "bailing_mm_pretrain_bailingv4_vit_600m": "configs/models/blip2/bailing_mm_pretrain_interleave_bailingv4_vit_600m.yaml",
        "bailing_mm_pretrain_qwen2_5_3b_vit2_5_600m": "configs/models/blip2/bailing_mm_pretrain_interleave_qwen2_5_3b_vit2_5_600m.yaml",
        "bailing_mm_pretrain_qwen2_5_7b_vit2_5_600m": "configs/models/blip2/bailing_mm_pretrain_interleave_qwen2_5_7b_vit2_5_600m.yaml",
    }

    def __init__(self, config: BailingMMConfig, **kwargs):
        super().__init__()
        self.config: BailingMMConfig = config
        self.pre_process = kwargs['pre_process']
        self.post_process = kwargs['post_process']
        self.vp_stage = kwargs['vp_stage']
        self.share_embeddings_and_output_weights = False
        self.negative_prompt = {}
        self.pool_after_mlp = self.config.pool_after_mlp
        self.num_query_token = self.config.num_query_token
        self.num_query_token_video = self.config.num_query_token_video
        self.num_query_token_audio = self.config.num_query_token_audio
        self.norm_ds_embeds = self.config.norm_ds_embeds
        logger.dist_all(f"norm_ds_embeds: {self.norm_ds_embeds}")
        self.vision = None
        self.audio = None
        self.linear_proj = None
        self.linear_proj_audio = None
        self.use_deepstack = False
        if self.pre_process:
            if self.config.vision_config:
                self.bilinear_interpolation = self.config.vision_config.args.get("bilinear_interpolation", False)
                self.freeze_mme = self.config.vision_config.freeze
                self.freeze_vision_proj = getattr(self.config.vision_config, "freeze_proj", False)
                vision_encoder_args = copy.deepcopy(self.config.vision_config.args)
                self.use_deepstack = vision_encoder_args.pop("use_deepstack", False)
                if self.use_deepstack:
                    logger.info("Warnings: use deepstack, which is only supported for qwen3_moe_vit!")
                
                self.vision = VISION_ENCODER_CLASS_DICT[self.config.vision_config.type].from_pretrained(
                    vision_encoder_args.pop('model_path'),
                    use_deepstack=self.use_deepstack,
                    freeze=self.freeze_mme,
                    image_size=self.config.image_size,
                    trust_remote_code=True,
                    force_download=True,
                    **vision_encoder_args,
                )
                if self.freeze_mme:
                    self.vision.eval()
                    for param in self.vision.parameters():
                        param.requires_grad = False

                # The logic related to VIT preprocessing has been moved to the
                # antvl/data/processor/post_processor.PostProcessor._preprocess_vision_features. This requires the
                # vision_encoder.config
                antmmf_context.vision_encoder = self.vision

            if self.config.audio_config:
                if self.config.audio_config.type == "SANMEncoder":
                    # for backward compatibility.
                    self.config.audio_config.type = "sanm"
                self.audio = AUDIO_ENCODER_CLASS_DICT[self.config.audio_config.type].from_pretrained(
                    self.config.audio_config.args['model_path'],
                    self.config.audio_config.args.get("sequence_parallel", False),
                    **self.config.audio_config.args.get("model_config_dict", {}).get(
                        f"audio_encoder_config_{self.config.audio_config.type}", {}
                    ),
                )
                self.audio.offload_activation_layers = self.config.audio_config.args.get(
                    "offload_activation_layers", None
                )
                self.audio.offload_conv_ln = self.config.audio_config.args.get("offload_conv_ln", True)
                self.audio.disable_multi_stream_in_offload = self.config.audio_config.args.get(
                    "disable_multi_stream_in_offload", True
                )
        # TODO(chengxiao):跨机pipeline，最后的rank上无法访问ckpt的话会导致model_config无法获取
        from bailingmm.models.bailingmm_megatron.bailingmm_throughput import get_model_config_for_throughput
        get_model_config_for_throughput(self.config)
        # ******* llm init *******
        self.llm_type = self.config.llm_config.type
        self.use_vl_model = config.llm_config.args.get("use_vl_model", False)
        from megatron.training import get_args

        args = get_args()
        args.finalize_model_grads_func = _antmmf_finalize_model_grads_func
        self.model_config, self.model, self.tokenizer, num_new_tokens = build_llm_model(
            self.config,
            use_vl_model=self.use_vl_model,
            pre_process=self.pre_process,
            post_process=self.post_process,
            vp_stage=self.vp_stage,
        )

        # init embedding for new tokens
        if num_new_tokens > 0 and self.config.copy_ori_embedding:
            input_embeddings = self.model.get_input_embeddings().weight.data
            output_embeddings = self.model.get_output_embeddings().weight.data

            self.ori_input_embeddings = input_embeddings.detach().clone()  # for sft
            self.ori_output_embeddings = output_embeddings.detach().clone()  # for sft
            self.num_new_tokens = num_new_tokens

            input_embeddings_avg = input_embeddings[:-num_new_tokens].mean(dim=0, keepdim=True)
            output_embeddings_avg = output_embeddings[:-num_new_tokens].mean(dim=0, keepdim=True)

            input_embeddings[-num_new_tokens:] = input_embeddings_avg
            output_embeddings[-num_new_tokens:] = output_embeddings_avg

        # 默认llm_model 的参数全部freeze. 后面可选择加peft或全参数训练
        for name, param in self.model.named_parameters():
            param.requires_grad = False

        if self.config.llm_config.half:
            self.model.half()

        if self.config.llm_config.freeze:
            self.model.eval()

            if self.config.tune_word_embeddings is True:
                if self.llm_type in ["llama3", "Qwen2ForCausalLM", "Qwen2VLForConditionalGeneration"]:
                    self.model.model.embed_tokens.float()
                elif self.llm_type in ["bailingv4"]:
                    self.model.glm.word_embeddings.float()
                try:
                    self.model.lm_head.float()
                except Exception:
                    logger.exception("lm_head not in glm_model !")
                # open word_embeddings and all heads
                for name, param in self.model.named_parameters():
                    if (
                        "word_embeddings" in name
                        or "lm_head" in name
                        or "embed_tokens" in name
                        or "image_head" in name
                        or "audio_head" in name
                    ):
                        logger.info("set " + str(name) + " return grad !")
                        param.requires_grad = True
        else:
            for name, param in self.model.named_parameters():
                param.requires_grad = True

        # ******* proj init *******
        if self.pre_process:
            if self.vision:
                mlp_modules_img = [nn.Linear(self.vision.image_emb_dim, self.model.config.hidden_size)]
                for _ in range(1, self.config.mlp_depth):
                    mlp_modules_img.append(nn.GELU())
                    mlp_modules_img.append(nn.Linear(self.model.config.hidden_size, self.model.config.hidden_size))
                self.linear_proj = nn.Sequential(*mlp_modules_img)

                # Vision token compression module
                self.vision_compressor = None
                if self.config.vision_compression_type is not None:
                    from bailingmm.models.bailingmm.vision_compressor import VisionTokenCompressor
                    spatial_merge_size = (
                        self.vision.config.spatial_merge_size
                        if hasattr(self.vision.config, "spatial_merge_size")
                        else 2
                    )
                    # before_bridge: compressor 在 linear_proj 之前调用，处理的是 vision encoder
                    # 直出的 feature（image_emb_dim 维），spatial_pool 路径会按此 reshape。
                    # after_bridge (默认 / 旧行为): 在 linear_proj 之后调用，处理 LLM hidden_size。
                    self.vision_compression_position = getattr(
                        self.config, "vision_compression_position", "after_bridge"
                    )
                    if self.vision_compression_position == "before_bridge":
                        compressor_hidden_size = self.vision.image_emb_dim
                    else:
                        compressor_hidden_size = self.model.config.hidden_size
                    self.vision_compressor = VisionTokenCompressor(
                        hidden_size=compressor_hidden_size,
                        spatial_merge_size=spatial_merge_size,
                        compression_type=self.config.vision_compression_type,
                        keep_ratio=self.config.vision_compression_keep_ratio,
                        window_size=self.config.vision_compression_window_size,
                        scale_factor=2.0,
                    )
                    self._vision_attention_scores_warned = False
                    logger.dist(
                        f"vision_compression_pack_mode: "
                        f"{getattr(self.config, 'vision_compression_pack_mode', 'boost')}, "
                        f"vision_compression_position: {self.vision_compression_position}"
                    )

            if self.audio:
                self.audio_downsampler_args = {
                    "kernel_size": self.config.audio_config.args['audio_ds_kernel_size'],
                    "stride": self.config.audio_config.args['audio_ds_stride'],
                    "padding": self.config.audio_config.args['audio_ds_kernel_size'] // 2,
                }
                audio_encoder_proj = torch.nn.Conv1d(
                    self.audio.audio_emb_dim,
                    self.model.config.hidden_size,
                    **self.audio_downsampler_args,
                )

                mlp_modules_audio = [audio_encoder_proj, Transpose(-1, -2)]
                for _ in range(1, self.config.mlp_depth):
                    mlp_modules_audio.append(nn.GELU())
                    mlp_modules_audio.append(nn.Linear(self.model.config.hidden_size, self.model.config.hidden_size))
                # Revert to a conv-style permutation.
                mlp_modules_audio.append(Transpose(-1, -2))
                self.linear_proj_audio = nn.Sequential(*mlp_modules_audio)

        self.add_position_emb = self.config.add_position_emb

        self.max_txt_len = self.config.max_txt_len
        self.loss_weight = self.config.loss_weight
        logger.dist_all(f"debug model is {self}")
        logger.dist(f"use_llm_3drope: {self.config.use_llm_3drope}")

    def set_input_tensor(self, input_tensor) -> None:
        """Sets input tensor to the model.
        See megatron.model.transformer.set_input_tensor()
        Args:
            input_tensor (Tensor): Sets the input tensor for the model.
        """
        # This is usually handled in schedules.py but some inference code still
        # gives us non-lists or None
        if not isinstance(input_tensor, list):
            input_tensor = [input_tensor]
        assert len(input_tensor) == 1, 'input_tensor should only be length 1 for gpt/bert'
        self.model.set_input_tensor(input_tensor[0])

    def load_checkpoint(self, url_or_filename, skip_param=None, tmp_save_ckpt_path=None):
        """
        Load from a finetuned checkpoint.
        This should expect no mismatch in the model keys and the checkpoint keys.
        """
        if is_url(url_or_filename):
            raise NotImplementedError('cannot download ckpt from url')
        elif url_or_filename.startswith('aistudio://'):
            from aistudio_checkpoint.aistudio_base_checkpointer import (
                load_checkpoint as ais_load_ckpt,
            )

            dir_path = ais_load_ckpt(resuming_path=url_or_filename)
            # assuming there is only one pt file under the path.
            files = os.listdir(dir_path)
            pth_files = [f for f in files if f.endswith('.pt') or f.endswith('.pth')]
            if pth_files:
                ckpt_file = pth_files[0]
            else:
                raise FileNotFoundError(
                    f"The ckpt file in dir_path '{dir_path}' doesn't exist. Please check and run again"
                )
            ckpt_path = os.path.join(dir_path, ckpt_file)
            with open(ckpt_path, "rb") as f:
                checkpoint = torch.load(f, map_location="cpu", weights_only=False)
        elif os.path.isfile(url_or_filename):
            with open(url_or_filename, "rb") as f:
                checkpoint = torch.load(f, map_location="cpu", weights_only=False)
        else:
            raise RuntimeError(f"checkpoint url or path '{url_or_filename}' is invalid")
        if "model" in checkpoint.keys():
            state_dict = checkpoint["model"]
        else:
            state_dict = checkpoint
        if skip_param is not None:
            new_state_dict = {}
            for key in state_dict:
                if key.split(".")[0] in skip_param:
                    continue
                new_state_dict[key] = state_dict[key]
            state_dict = new_state_dict
        delete_keys = []
        for key in state_dict:
            if "vision" in key and ("freqs_cos" in key or "freqs_sin" in key or "position_ids" in key):
                delete_keys.append(key)
        for key in delete_keys:
            del state_dict[key]

        if self.config.vision_config.type == "siglip":
            logger.dist_all("Checking position embedding shapes for siglip...")
            num_positions, embed_dim = self.vision.vision_tower.vision_model.embeddings.position_embedding.weight.shape
            new_state_dict = {}
            for k, v in state_dict.items():
                if "vision_" in k and "position_embedding" in k:
                    if v.shape[0] != num_positions:
                        logger.dist_all(
                            f"Resizing position embedding of pretrained backbone in siglip.. from {v.shape[0]} to {num_positions}."
                        )
                        logger.dist_all(f"Old pos embed shape: {v.shape}")
                        new_state_dict[k] = self.vision.vision_tower.vision_model.resize_pos_embeddings_in_checkpoint(v)
                        logger.dist_all(f"New pos embed shape: {new_state_dict[k].shape}")
                    else:
                        logger.dist_all("No reshape on the pos embed required for the pretrained checkpoint.")
                else:
                    new_state_dict[k] = v
            state_dict = new_state_dict

        if "vision.visual.pos_embed" in state_dict:
            pos_embed_checkpoint = state_dict["vision.visual.pos_embed"]
            embedding_size = pos_embed_checkpoint.shape[-1]
            num_patches = self.vision.visual.patch_embed.num_patches
            num_extra_tokens = self.vision.visual.pos_embed.shape[-2] - num_patches
            # height (== width) for the checkpoint position embedding
            orig_size = int((pos_embed_checkpoint.shape[-2] - num_extra_tokens) ** 0.5)
            # height (== width) for the new position embedding
            new_size = int(num_patches**0.5)
            # class_token and dist_token are kept unchanged
            if orig_size != new_size:
                logger.dist_all("Position interpolate from %dx%d to %dx%d" % (orig_size, orig_size, new_size, new_size))
                extra_tokens = pos_embed_checkpoint[:, :num_extra_tokens]
                # only the position tokens are interpolated
                pos_tokens = pos_embed_checkpoint[:, num_extra_tokens:]
                pos_tokens = pos_tokens.reshape(-1, orig_size, orig_size, embedding_size).permute(0, 3, 1, 2)
                pos_tokens_dtype = pos_tokens.dtype
                pos_tokens = torch.nn.functional.interpolate(
                    pos_tokens.to(torch.float32), size=(new_size, new_size), mode="bicubic", align_corners=False
                )
                pos_tokens = pos_tokens.to(pos_tokens_dtype)
                pos_tokens = pos_tokens.permute(0, 2, 3, 1).flatten(1, 2)
                new_pos_embed = torch.cat((extra_tokens, pos_tokens), dim=1)
                state_dict["vision_.visual.pos_embed"] = new_pos_embed
                patch_embed_proj = state_dict["vision_.visual.patch_embed.proj.weight"]
                patch_size = self.vision.visual.patch_embed.patch_size
                state_dict["vision_.visual.patch_embed.proj.weight"] = torch.nn.functional.interpolate(
                    patch_embed_proj.float(), size=patch_size, mode="bicubic", align_corners=False
                )
        param_need = {}
        for key, p in self.named_parameters():
            if (
                "word_embeddings" in key
                or "lm_head" in key
                or "embed_tokens" in key
                or "image_head" in key
                or "audio_head" in key
                or "linear_proj_audio" in key
            ):
                param_need[key] = p
        param_need["glm_model.lm_head.weight"] = self.model.lm_head.weight
        for key in state_dict:
            if (
                "word_embeddings" in key
                or "lm_head" in key
                or "embed_tokens" in key
                or "image_head" in key
                or "audio_head" in key
                or "linear_proj_audio" in key
            ) and key in param_need:
                if param_need[key].size(0) != state_dict[key].size(0):
                    logger.dist_all(f"param_update: {key}")
                    logger.dist_all(f"  need_size: {param_need[key].size()}")
                    logger.dist_all(f"  before_size: {state_dict[key].size()}")
                    min_size = min(param_need[key].size(0), state_dict[key].size(0))
                    value_bak = state_dict[key].clone().detach()
                    state_dict[key] = param_need[key].clone().detach()
                    state_dict[key][:min_size, :] = value_bak[:min_size, :]
                    state_dict[key][min_size:, :] = torch.nn.init.xavier_normal_(state_dict[key][min_size:, :])
                    logger.dist_all(f"  after_size: {state_dict[key].size()}")
                elif len(param_need[key].size()) > 1 and param_need[key].size(1) != state_dict[key].size(1):
                    logger.dist_all(f"param_update: {key}")
                    logger.dist_all(f"  need_size: {param_need[key].size()}")
                    logger.dist_all(f"  before_size: {state_dict[key].size()}")
                    min_size = min(param_need[key].size(1), state_dict[key].size(1))
                    value_bak = state_dict[key].clone().detach()
                    state_dict[key] = param_need[key].clone().detach()
                    state_dict[key][:, :min_size] = value_bak[:, :min_size]
                    state_dict[key][:, min_size:] = torch.nn.init.xavier_normal_(state_dict[key][:, min_size:])
                    logger.dist_all(f"  after_size: {state_dict[key].size()}")

        msg = self.load_state_dict(state_dict, strict=False)
        logger.dist_all(f"Missing keys: {msg.missing_keys}")
        logger.dist_all(f"Unexpected keys: {msg.unexpected_keys}")
        logger.dist_all(f"load checkpoint from {url_or_filename}")
        return msg

    def encode_audio_post_processing(self, audio_embeds: torch.Tensor, audio_compress=3):
        # audio_embeds(-1, length, dim)
        batch_size = audio_embeds.size(0)
        real_length = audio_embeds.size(1)
        dim = audio_embeds.size(2)
        valid_length = real_length // audio_compress * audio_compress
        audio_embeds = audio_embeds[:, :valid_length, :].view(
            batch_size, valid_length // audio_compress, dim * audio_compress
        )
        return audio_embeds

    def resize_word_embedding(self, loading_info, glm_model, glm_model_original):
        if len(loading_info['mismatched_keys']) != 0:
            logger.dist_all(f"mismatched keys: {loading_info['mismatched_keys']}")
            bin_files = glob.glob(os.path.join(glm_model, '**', '*.bin'), recursive=True)
            ori_model = {}
            for bin_file in bin_files:
                logger.dist_all(f"resize_word_embedding loading: {bin_file}")
                tmp_model = torch.load(bin_file, map_location="cpu")
                ori_model.update(tmp_model)
            model_backbone_dict = glm_model_original.state_dict()
            update_dict = {}
            for mismatched_item in loading_info['mismatched_keys']:
                param_name = mismatched_item[0]
                if (
                    "word_embeddings.weight" in param_name
                    or "lm_head.weight" in param_name
                    or "image_head.weight" in param_name
                    or "audio_head.weight" in param_name
                ):
                    ori_params = ori_model[param_name]
                    ori_num_tokens, ori_embedding_dim = ori_params.size()

                    if param_name not in glm_model_original.state_dict():
                        param_name = 'glm.' + param_name
                    update_dict[param_name] = glm_model_original.state_dict()[param_name]
                    new_num_tokens, new_embedding_dim = update_dict[param_name].size()
                    num_tokens_to_copy = min(ori_num_tokens, new_num_tokens)
                    update_dict[param_name][:num_tokens_to_copy, :] = ori_params[:num_tokens_to_copy, :]
                    logger.dist_all(f"mismatched keys {param_name} update !")
                else:
                    raise NotImplementedError

            model_backbone_dict.update(update_dict)
            glm_model_original.load_state_dict(model_backbone_dict)
            del ori_model
            import gc

            gc.collect()
            logger.dist_all('*' * 50)
        return glm_model_original

    def _prepare_audio_inputs(self, audios, device) -> Dict[str, Any]:
        audio_feats = audios["audio_feats"].to(device)
        assert self.audio is not None
        assert self.linear_proj_audio is not None
        with torch.set_grad_enabled(not self.config.audio_config.freeze):
            inputs_opt_audio, _, audio_feats_lengths = encode_audio_segments(
                encoder=self.audio,
                proj_layer=self.linear_proj_audio,
                downsampler_args=self.audio_downsampler_args,
                wav_feats=audio_feats,
                wav_feats_lengths=audios["audio_feats_lengths"],
                offload_activation_layers=audios.get("offload_activation_layers"),
                freeze_proj=getattr(self.config.audio_config, "freeze_proj", False)
            )
        if self.config.norm_query_embeds:
            inputs_opt_audio = F.normalize(inputs_opt_audio, dim=2)  # [-1, 256, 2048]
        if self.config.llm_config.half:
            inputs_opt_audio = inputs_opt_audio.half()
        return {
            "query_embeds_audio": inputs_opt_audio,
            "query_embeds_audio_lengths": audio_feats_lengths,
            "placeholder_audio_loc_lens": audios["audio_placeholder_loc_lens"],
        }

    def _prepare_vision_inputs(self):
        # TODO(mingyang): implement vision inputs
        pass

    def _replace_vision_position_ids(
        self,
        position_ids: torch.Tensor,
        vision_pos_ids: torch.Tensor,
        input_ids: torch.Tensor,
        packed_seq_params=None,
        vision_token_counts=None,
    ) -> torch.Tensor:
        """Replace only vision-token position_ids with compressor positions.

        The dataloader has already built packed-sequence-aware position_ids.
        Rebuilding the full sequence here would lose packed sample boundaries.
        Instead, keep all text/pad positions unchanged and only replace
        contiguous vision placeholder spans with VisionZip positions plus the
        original span's temporal offset.

        Args:
            position_ids: original position_ids from dataloader, shape
                [3, bs, seq_len] or [1, 3, bs, seq_len]
            vision_pos_ids: [3, num_vision_tokens] relative 3D positions from compressor
            input_ids: [bs, seq_len] input token ids
            packed_seq_params: optional PackedSeqParams with cu_seqlens
            vision_token_counts: compressed token count for each original vision grid

        Returns:
            [3, bs, seq_len] position_ids with vision spans replaced
        """
        if vision_pos_ids is None:
            return position_ids
        if position_ids is None:
            raise ValueError(
                "Vision compression requires precomputed position_ids so vision "
                "positions can be replaced without losing packed sequence boundaries."
            )
        if input_ids is None:
            return position_ids

        if position_ids.dim() == 4:
            if position_ids.shape[0] != 1:
                raise ValueError(f"Unsupported position_ids shape for vision compression: {position_ids.shape}")
            position_ids = position_ids[0]
        if position_ids.dim() != 3:
            raise ValueError(f"Unsupported position_ids shape for vision compression: {position_ids.shape}")

        # Get vision placeholder token IDs
        image_token_id = getattr(self.config, "image_patch_token", None)
        if image_token_id is None and hasattr(self.model.config, "image_patch_token"):
            image_token_id = self.model.config.image_patch_token
        if image_token_id is None:
            image_token_id = getattr(self.config, "image_token_id", None)

        video_token_id = getattr(self.config, "video_token_id", None)
        if video_token_id is None and hasattr(self.model.config, "video_token_id"):
            video_token_id = self.model.config.video_token_id

        if image_token_id is None:
            return position_ids

        bs, seq_len = input_ids.shape
        device = input_ids.device
        merged = position_ids.clone()
        vision_pos_ids = vision_pos_ids.to(device=device, dtype=merged.dtype)

        # Build vision mask (image + video placeholder tokens)
        is_vision = input_ids == image_token_id
        if video_token_id is not None:
            is_vision = is_vision | (input_ids == video_token_id)

        segment_boundaries = [0, seq_len]
        if packed_seq_params is not None:
            cu_seqlens = getattr(packed_seq_params, "cu_seqlens_q_padded", None)
            if cu_seqlens is None:
                cu_seqlens = getattr(packed_seq_params, "cu_seqlens_q", None)
            if cu_seqlens is not None:
                segment_boundaries = cu_seqlens.detach().to(device="cpu", dtype=torch.long).tolist()
                segment_boundaries = sorted(set(max(0, min(seq_len, int(x))) for x in segment_boundaries))
                if not segment_boundaries or segment_boundaries[0] != 0:
                    segment_boundaries = [0] + segment_boundaries
                if segment_boundaries[-1] != seq_len:
                    segment_boundaries.append(seq_len)

        vision_token_offset = 0
        vision_grid_offset = 0
        if vision_token_counts is not None:
            vision_token_counts = [int(count) for count in vision_token_counts]

        for b in range(bs):
            vis_mask_b = is_vision[b]
            vision_idx = vision_token_offset
            grid_idx = vision_grid_offset
            for seg_start, seg_end in zip(segment_boundaries[:-1], segment_boundaries[1:]):
                if seg_end <= seg_start:
                    continue
                vision_indices = vis_mask_b[seg_start:seg_end].nonzero(as_tuple=True)[0] + seg_start
                if vision_indices.numel() == 0:
                    continue

                span_start = vision_indices[0].item()
                prev_idx = span_start
                for idx in vision_indices[1:].tolist() + [None]:
                    if idx is None or idx != prev_idx + 1:
                        span_end = prev_idx + 1
                        chunk_start = span_start
                        while chunk_start < span_end:
                            if vision_token_counts is None:
                                chunk_len = span_end - chunk_start
                            else:
                                while grid_idx < len(vision_token_counts) and vision_token_counts[grid_idx] == 0:
                                    grid_idx += 1
                                if grid_idx >= len(vision_token_counts):
                                    raise ValueError(
                                        "Vision placeholder spans exceed compressed grid token counts: "
                                        f"span_start={span_start}, span_end={span_end}"
                                    )
                                chunk_len = vision_token_counts[grid_idx]
                                grid_idx += 1
                                if chunk_start + chunk_len > span_end:
                                    raise ValueError(
                                        "A compressed vision grid crosses a non-vision boundary: "
                                        f"chunk_start={chunk_start}, chunk_len={chunk_len}, span_end={span_end}"
                                    )

                            rel_pos = vision_pos_ids[:, vision_idx : vision_idx + chunk_len]
                            if rel_pos.shape[1] != chunk_len:
                                raise ValueError(
                                    "Vision position_ids length is shorter than compressed vision token count: "
                                    f"need {chunk_len}, got {rel_pos.shape[1]}"
                                )
                            base = position_ids[0, b, chunk_start]
                            chunk_end = chunk_start + chunk_len
                            merged[:, b, chunk_start:chunk_end] = rel_pos + base
                            vision_idx += chunk_len
                            chunk_start = chunk_end
                        span_start = idx
                    prev_idx = idx if idx is not None else prev_idx

            vision_token_offset = vision_idx
            vision_grid_offset = grid_idx

        if vision_token_offset != vision_pos_ids.shape[1]:
            raise ValueError(
                "Compressed vision token count does not match placeholder token count: "
                f"consumed {vision_token_offset}, available {vision_pos_ids.shape[1]}"
            )
        if vision_token_counts is not None and vision_grid_offset != len(vision_token_counts):
            raise ValueError(
                "Compressed grid token counts do not match placeholder spans: "
                f"consumed {vision_grid_offset}, available {len(vision_token_counts)}"
            )

        return merged

    @staticmethod
    def _count_grid_thw_entries(grid_thw) -> int:
        if grid_thw is None:
            return 0
        if isinstance(grid_thw, torch.Tensor):
            if grid_thw.numel() == 0:
                return 0
            return grid_thw.reshape(-1, 3).shape[0]

        count = 0
        for grid in grid_thw:
            if grid is None:
                continue
            if isinstance(grid, torch.Tensor):
                if grid.numel() > 0:
                    count += grid.reshape(-1, 3).shape[0]
                continue
            try:
                grid_tensor = torch.as_tensor(grid)
                if grid_tensor.numel() > 0:
                    count += grid_tensor.reshape(-1, 3).shape[0]
            except (TypeError, ValueError):
                continue
        return count

    def _unpack_vision_encoder_output(self, vision_output):
        if isinstance(vision_output, (tuple, list)):
            if len(vision_output) == 2:
                return vision_output[0], vision_output[1]
            if len(vision_output) > 0:
                self._warn_missing_vision_attention_scores()
                return vision_output[0], None

        self._warn_missing_vision_attention_scores()
        return vision_output, None

    def _warn_missing_vision_attention_scores(self):
        if getattr(self, "_vision_attention_scores_warned", False):
            return
        logger.warning(
            "VisionZip requested ViT attention scores, but the active vision encoder did not return them. "
            "Falling back to feature-norm scoring for vision token compression."
        )
        self._vision_attention_scores_warned = True

    def forward(self, samples):
        if_calc_loss = samples.get("if_calc_loss", True)
        use_cache = samples.get("use_cache", False)
        data_type_mask = samples.get("data_type_mask", None)
        activation_offload_args = {"audio": [], "image": []}  # dataset_type: layers
        dataset_type = samples.get("dataset_type", None)
        if samples.get("audio", None) is not None:
            audios = {
                k: torch.from_numpy(v) if isinstance(v, np.ndarray) else v for k, v in samples["audio"].items()
            }  # audio_feats以外的项都是numpy array，这是为了绕过FSDP将所有tensor都to cuda的操作
        else:
            audios = None
        device = torch.cuda.current_device()
        image_grid_thw = samples.get("image_grid_thw", None)  # [1, 1, N]
        video_grid_thw = samples.get("video_grid_thw", None)  # [1, 1, N]
        image_embeds = samples.get("image_embeds", None)
        video_embeds = samples.get("video_embeds", None)
        compression_vision_pos_ids = None
        compression_vision_token_counts = None
        activation_offload_args = {"image": None, "audio": None}
        image_exist = (
            self.pre_process
            and image_grid_thw is not None
            and any(_image_grid_thw is not None for _image_grid_thw in image_grid_thw)
        )
        deepstack_feature_lists = None
        video_exist = (
            self.pre_process
            and video_grid_thw is not None
            and any(_video_grid_thw is not None for _video_grid_thw in video_grid_thw)
        )
        if self.pre_process and image_exist and self.vision.offload_activation_layers is not None:
            from bailingmm.utils.activation_offload_utils import should_offload_activation
            
            offload_threshold_value = getattr(self.config, "offload_threshold_value", 150 * 1024 * 1024)
            _, activation_offload_args = should_offload_activation(
                samples=samples,
                audio_config=self.audio,
                vision_config=self.vision,
                offload_threshold_value=offload_threshold_value
            )
            if audios is not None:
                audios["offload_activation_layers"] = activation_offload_args["audio"]
        if image_exist or video_exist:  # contain vision inputs
            # feature was preprocessed in sequence_packing_wrapper
            vision_attention_scores = None
            vision_img_tokens = samples.get("vision_img_tokens", None)
            vision_video_tokens = samples.get("vision_video_tokens", None)
            vision_grid_thw_array = torch.squeeze(samples.get("vision_grid_thw_array", None), 0)
            vision_pixel_values = torch.squeeze(samples.get("vision_pixel_values", None), 0)
            original_seq_len = samples.get('vision_pixel_origin_len', None) # only support mbs=1
            if self.config.vision_config.type == "Qwen3MoeVisionTransformer":
                vision_pos_ids = torch.squeeze(samples.get("vision_pos_ids", None), 0)
                vision_idx_tensor = torch.squeeze(samples.get("vision_idx_tensor", None), 0)
                vision_weight_tensor = torch.squeeze(samples.get("vision_weight_tensor", None), 0)
                vision_cu_seqlens = torch.squeeze(samples.get("vision_cu_seqlens", None), 0)
            elif self.config.vision_config.type == "Qwen2_5_VisionTransformer":
                vision_pos_ids = torch.squeeze(samples.get("vision_pos_ids", None), 0)
                vision_window_index = torch.squeeze(samples.get("vision_window_index", None), 0)
                vision_cu_window_seqlens = torch.squeeze(samples.get("vision_cu_window_seqlens", None), 0)
            if isinstance(vision_img_tokens, list):
                vision_img_tokens = sum(t for t in vision_img_tokens if t)
            if isinstance(vision_video_tokens, list):
                vision_video_tokens = sum(t for t in vision_video_tokens if t)
                
            with torch.cuda.amp.autocast(dtype=torch.bfloat16):
                with torch.set_grad_enabled(not self.freeze_mme):
                    if self.config.vision_config.type == "Qwen3MoeVisionTransformer":
                        if self.use_deepstack:
                            pixel_embeds, deepstack_feature_lists = self.vision(
                                hidden_states=vision_pixel_values,
                                grid_thw=vision_grid_thw_array,
                                vision_pos_ids=vision_pos_ids,
                                idx_tensor=vision_idx_tensor,
                                weight_tensor=vision_weight_tensor,
                                cu_seqlens=vision_cu_seqlens,
                                activation_offload_layers=activation_offload_args["image"],
                            )
                        else:
                            pixel_embeds = self.vision(
                                hidden_states=vision_pixel_values,
                                grid_thw=vision_grid_thw_array,
                                vision_pos_ids=vision_pos_ids,
                                idx_tensor=vision_idx_tensor,
                                weight_tensor=vision_weight_tensor,
                                cu_seqlens=vision_cu_seqlens,
                                activation_offload_layers=activation_offload_args["image"],
                                return_attention_scores=self.vision_compressor is not None,
                                original_seq_len=original_seq_len,
                            )
                        if self.vision_compressor is not None:
                            pixel_embeds, vision_attention_scores = self._unpack_vision_encoder_output(pixel_embeds)
                    elif self.config.vision_config.type == "Qwen2VisionTransformer":
                        pixel_embeds = self.vision(
                            hidden_states=vision_pixel_values,
                            grid_thw=vision_grid_thw_array,
                            return_attention_scores=self.vision_compressor is not None,
                        )
                        if self.vision_compressor is not None:
                            pixel_embeds, vision_attention_scores = self._unpack_vision_encoder_output(pixel_embeds)
                    elif self.config.vision_config.type == "Qwen2_5_VisionTransformer":
                        assert original_seq_len is None, 'Qwen2_5_VisionTransformer not support original_seq_len'
                        pixel_embeds = self.vision(
                            hidden_states=vision_pixel_values,
                            grid_thw=vision_grid_thw_array,
                            vision_pos_ids=vision_pos_ids,
                            window_index=vision_window_index,
                            cu_window_seqlens=vision_cu_window_seqlens,
                            activation_offload_layers=activation_offload_args["image"],
                        )
                # Vision token compression (before bridge) —— 在 linear_proj 之前用 vision
                # encoder 直出 feature 做压缩，省 linear_proj/normalize 的算力（减少到 K 个
                # token 才参与后续投影）。after_bridge 则保持旧行为：先 linear_proj 再压缩。
                compressor_position = getattr(self, "vision_compression_position", "after_bridge")
                if self.vision_compressor is not None and compressor_position == "before_bridge":
                    n_image_grids = self._count_grid_thw_entries(image_grid_thw) if image_exist else 0
                    pixel_embeds, compression_vision_pos_ids, comp_meta = self.vision_compressor(
                        features=pixel_embeds,
                        grid_thw=vision_grid_thw_array,
                        n_image_grids=n_image_grids,
                        token_scores=vision_attention_scores,
                    )
                    vision_img_tokens = comp_meta["img_tokens"]
                    vision_video_tokens = comp_meta["video_tokens"]
                    compression_vision_token_counts = comp_meta.get("grid_tokens", None)

                # linear_proj place outside encoder freeze
                if self.use_deepstack:
                    ds_sizes = [e.shape[0] for e in deepstack_feature_lists]
                with torch.set_grad_enabled(not self.freeze_vision_proj):
                    from atorch.utils.te_checkpoint import checkpoint
                    use_checkpoint = self.config.vision_config.args.get("use_vision_checkpoint", False)
                    if use_checkpoint:
                        pixel_embeds = checkpoint(
                            lambda hs: self.linear_proj(hs),
                            pixel_embeds,
                            use_reentrant=True,
                            offload=True,
                            disable_multi_stream_in_offload=True
                        )
                    else:
                        pixel_embeds = self.linear_proj(pixel_embeds)

                    if self.use_deepstack:
                        deepstack_feature_lists = torch.cat(deepstack_feature_lists,dim=0)
                        deepstack_feature_lists = self.linear_proj(deepstack_feature_lists)

                # Vision token compression (after bridge, default / legacy behavior)
                if self.vision_compressor is not None and compressor_position == "after_bridge":
                    n_image_grids = self._count_grid_thw_entries(image_grid_thw) if image_exist else 0
                    pixel_embeds, compression_vision_pos_ids, comp_meta = self.vision_compressor(
                        features=pixel_embeds,
                        grid_thw=vision_grid_thw_array,
                        n_image_grids=n_image_grids,
                        token_scores=vision_attention_scores,
                    )
                    vision_img_tokens = comp_meta["img_tokens"]
                    vision_video_tokens = comp_meta["video_tokens"]
                    compression_vision_token_counts = comp_meta.get("grid_tokens", None)

                if self.config.norm_query_embeds:
                    pixel_embeds = F.normalize(pixel_embeds, dim=-1)
                    if self.use_deepstack and self.norm_ds_embeds:
                        deepstack_feature_lists = F.normalize(deepstack_feature_lists, dim=-1)

                if self.use_deepstack:
                    deepstack_feature_lists = torch.split(deepstack_feature_lists, ds_sizes, dim=0)
            if image_exist:
                image_embeds = pixel_embeds[:vision_img_tokens,]
                
            if video_exist:
                video_embeds = pixel_embeds[-vision_video_tokens:,]
        if self.pre_process and audios is not None:
            with torch.cuda.amp.autocast(dtype=torch.bfloat16):
                inputs_audio = self._prepare_audio_inputs(audios, device)
        else:
            inputs_audio = {}

        labels = samples.get("labels", None)
        if torch.is_tensor(labels):
            labels = labels.to(device)
        text_ids = samples.get("input_ids", None)
        if text_ids is not None:
            text_ids = text_ids.long().to(device)
        if samples.get("attention_mask_for_mrope", None) is not None:
            attention_mask = samples["attention_mask_for_mrope"].to(device)
        else:
            attention_mask = samples["attention_mask"].to(device) if samples["attention_mask"] is not None else None

        attention_mask_for_mrope = None # used to compute postion_ids, unused after postion_ids computed in datalodaer
        packed_seq_params = samples.get("packed_seq_params", None)

        if "position_ids" in samples and samples["position_ids"] is not None:
            position_ids = samples["position_ids"].long().to(device)
        else:
            position_ids = None

        weights = None
        if self.loss_weight and samples.get("weights", None) is not None:
            weights = samples["weights"][0]
            if isinstance(weights, list):
                weights = torch.tensor(weights, dtype=torch.float32, device=device)
            else:
                weights = weights.to(dtype=torch.float32, device=device)

        # TODO(cangzhi yipei weiyi): debug togather
        '''
        if query_embeds_image is None and query_embeds_video is None:
            image_mask = None
        else:
            image_mask = samples["image_mask"]
        if inputs_audio:
            audio_mask = samples["audio_mask"]
        else:
            audio_mask = None
        '''
        image_mask = samples.get("image_mask", None)
        audio_mask = samples.get("audio_mask", None)

        labels = labels if if_calc_loss is True else None
        loss_sample = None
        data_type_loss = {}

        # Prepare visual_pos_masks for deepstack
        visual_pos_masks = None
        if self.use_deepstack and deepstack_feature_lists is not None:
            image_token_id = self.model.config.image_token_id
            video_token_id = self.model.config.video_token_id

            image_pos_mask = (text_ids == image_token_id)  # [batch, seq_len]
            video_pos_mask = (text_ids == video_token_id)  # [batch, seq_len]

            if image_exist and video_exist:
                visual_pos_masks = image_pos_mask | video_pos_mask

                visual_mask_1d = visual_pos_masks[0]  # [seq_len], batch=0 (sequence packing mbs=1)
                image_mask_in_visual = image_pos_mask[0][visual_mask_1d]  # [num_visual] 中哪些是 image
                video_mask_in_visual = video_pos_mask[0][visual_mask_1d]  # [num_visual] 中哪些是 video

                reordered_features = []
                for ds_feat in deepstack_feature_lists:
                    img_feat = ds_feat[:vision_img_tokens]
                    vid_feat = ds_feat[vision_img_tokens:]
                    joint = ds_feat.new_zeros(visual_mask_1d.sum(), ds_feat.shape[-1])
                    joint[image_mask_in_visual] = img_feat
                    joint[video_mask_in_visual] = vid_feat
                    reordered_features.append(joint)
                deepstack_feature_lists = reordered_features

            elif image_exist:
                visual_pos_masks = image_pos_mask
            elif video_exist:
                visual_pos_masks = video_pos_mask

        # with torch.cuda.amp.autocast(dtype=torch.bfloat16):
        if self.llm_type not in ["bailingv4", "bailing_moe_v2", "bailing_moe_v2_flash", "bailing_moe_v3"]:
            inputs = get_model_input_handler(self.config.llm_config.type)(
                model=self.model,
                input_ids=text_ids,
                position_ids=position_ids,
                attention_mask=attention_mask,
                query_embeds_image=image_embeds,  # imagePatch embeds
                query_embeds_video=video_embeds,  # video embeds
                **inputs_audio,  # audio inputs
                target_embeds=None,  # target image/audioPatch embeds
                image_grid_thw=image_grid_thw,
                image_grid_thw_video=video_grid_thw,
                use_cache=use_cache,
                use_vl_model=self.use_vl_model,
                use_llm_3drope=self.config.use_llm_3drope,
                attention_mask_for_mrope=attention_mask_for_mrope,
                packed_seq_params=packed_seq_params,
                deepstack_features=deepstack_feature_lists,
                visual_pos_masks=visual_pos_masks,
            )
            outputs = self.model(
                **inputs,
            )
            loss = get_loss_func(self.config.loss_func)(
                vocab_size=self.model_config.vocab_size,
                logits=outputs.logits,
                labels=labels,
                weights=weights,
            )
        else:
            # If vision compression is active, replace only vision-token
            # position_ids and keep dataloader-computed packed text positions.
            if compression_vision_pos_ids is not None:
                position_ids = self._replace_vision_position_ids(
                    position_ids,
                    compression_vision_pos_ids,
                    text_ids,
                    packed_seq_params,
                    compression_vision_token_counts,
                )
                image_grid_thw = None
                video_grid_thw = None

            outputs = self.model(
                input_ids=text_ids,
                query_embeds_image=image_embeds,  # imagePatch embeds
                query_embeds_video=video_embeds,  # video embeds
                data_type_mask=data_type_mask,
                **inputs_audio,  # audio inputs
                target_embeds=None,  # target image/audioPatch embeds
                position_ids=position_ids,
                attention_mask=attention_mask,
                image_mask=image_mask,
                audio_mask=audio_mask,
                labels=labels,
                weights=weights,
                # is_pretrain=self.is_pretrain,
                image_grid_thw=image_grid_thw,
                image_grid_thw_video=video_grid_thw,
                packed_seq_params=packed_seq_params,
                loss_mask=samples.get("loss_mask", None),
                moe_padding_mask=samples.get("moe_padding_mask", None),
                loss_weights=samples.get("loss_weights", None),
                loss_weight_normalizer=samples.get("loss_weight_normalizer", None),
                extra_block_kwargs=samples.get("extra_block_kwargs", None),
                deepstack_features=deepstack_feature_lists,
                visual_pos_masks=visual_pos_masks,
            )
            return outputs

        if isinstance(loss, dict):
            loss_sample = loss['loss_sample']
            loss = loss['loss']
            logits = outputs["logits"]

        return {"loss": loss, "logits": outputs.logits, "loss_sample": loss_sample, "data_type_loss": data_type_loss}

    @torch.no_grad()
    def generate(
        self,
        samples,
        use_nucleus_sampling=False,
        num_beams=5,
        max_length=None,
        max_new_tokens=None,
        min_length=1,
        top_p=0.9,
        top_k=40,
        repetition_penalty=1.0,
        length_penalty=1,
        no_repeat_ngram_size=0,
        num_captions=1,
        temperature=1,
        llama_return_dict=False,
        target_modality="text",
        negative_prompt=None,
        return_logits=False,
        use_cache=True,
        is_audio_generation_mode=False,
    ):
        """
        Args:
            samples (dict): A dictionary containing the following keys:
                - image (torch.Tensor): A tensor of shape (batch_size, 3, H, W)
            use_nucleus_sampling (bool): Whether to use nucleus sampling. If False, use top-k sampling.
            num_beams (int): Number of beams for beam search. 1 means no beam search.
            max_length (int): The maximum length of the sequence to be generated.
            min_length (int): The minimum length of the sequence to be generated.
            top_p (float): The cumulative probability for nucleus sampling.
            repetition_penalty (float): The parameter for repetition penalty. 1.0 means no penalty.
            num_captions (int): Number of captions to be generated for each image.
        Returns:
            captions (list): A list of strings of length batch_size * num_captions.
        """
        device = samples["input_ids"].device
        pixel_values = samples.get("pixel_values", None)
        pixel_values_videos = samples.get("pixel_values_videos", None)
        image_grid_thw = samples.get("image_grid_thw", None)
        video_grid_thw = samples.get("video_grid_thw", None)
        if image_grid_thw is not None and pixel_values is not None:
            if isinstance(pixel_values, list):
                pixel_values = torch.tensor(pixel_values, device=device)
            if isinstance(image_grid_thw, list):
                image_grid_thw_array = []
                for image_grid_thw_ in samples["image_grid_thw"]:
                    image_grid_thw_array.extend(image_grid_thw_)
                image_grid_thw = torch.tensor(image_grid_thw_array, device=device)
        if video_grid_thw is not None and pixel_values_videos is not None:
            if isinstance(pixel_values_videos, list):
                pixel_values_videos = torch.tensor(pixel_values_videos, device=device)
            if isinstance(video_grid_thw, list):
                video_grid_thw_array = []
                for video_grid_thw_ in samples["video_grid_thw"]:
                    video_grid_thw_array.extend(video_grid_thw_)
                video_grid_thw = torch.tensor(video_grid_thw, device=device)
        # image_embeds
        if image_grid_thw is not None:
            with torch.cuda.amp.autocast(dtype=torch.bfloat16):
                image_embeds = self.vision(
                    hidden_states=pixel_values,
                    grid_thw=image_grid_thw,
                )
            image_embeds = self.linear_proj(image_embeds)
            if self.config.norm_query_embeds:
                image_embeds = F.normalize(image_embeds, dim=-1)
        if video_grid_thw is not None:
            with torch.cuda.amp.autocast(dtype=torch.bfloat16):
                video_embeds = self.vision(
                    hidden_states=pixel_values_videos,
                    grid_thw=video_grid_thw,
                )
            if self.config.norm_query_embeds:
                video_embeds = F.normalize(video_embeds, dim=-1)

        audios = samples.get("audio", None)

        if audios and audios.get("audio_feats") is not None:
            audios["audio_feats"] = audios["audio_feats"].to(dtype=torch.bfloat16)
        if audios is not None:
            inputs_audio = self._prepare_audio_inputs(audios, device)
        else:
            inputs_audio = {}

        inputs = {}
        inputs["input_ids"] = samples["input_ids"].to(device)
        if "position_ids" in samples and samples["position_ids"] is not None:
            inputs["position_ids"] = samples["position_ids"].to(device)
        else:
            inputs["position_ids"] = None
        if self.llm_type in ["llama7b", "llama3", "bailingv4", "qwen2"]:
            inputs["attention_mask"] = samples["generation_attention_mask"].to(device)
        else:
            inputs["generation_attention_mask"] = samples["generation_attention_mask"].to(device)
        # inputs["query_embeds_visual"] = inputs_opt_visual

        if max_length is None and max_new_tokens is None:
            max_new_tokens = self.max_txt_len

        generation_config = GenerationConfig.from_dict(
            {
                "do_sample": use_nucleus_sampling,
                "num_beams": num_beams,
                "max_length": max_length,
                "max_new_tokens": max_new_tokens,
                "min_length": min_length,
                "eos_token_id": self.model.gen_terminator,
                "top_p": top_p,
                "top_k": top_k,
                "repetition_penalty": repetition_penalty,
                "no_repeat_ngram_size": no_repeat_ngram_size,
                "length_penalty": length_penalty,
                "num_captions": num_captions,
                "temperature": temperature,
                "return_dict_in_generate": llama_return_dict,
                "output_scores": llama_return_dict,
                "use_cache": use_cache,
            }
        )

        if target_modality == "image":
            pass
            # TODO image generation here

        elif target_modality in ["text", "audio"]:
            inputs["query_embeds_image"] = image_embeds
            inputs["query_embeds_video"] = video_embeds

            inputs.update(inputs_audio)
            inputs["image_grid_thw"] = image_grid_thw
            inputs["image_grid_thw_video"] = video_grid_thw

            with torch.cuda.amp.autocast(dtype=torch.bfloat16):
                if self.llm_type in ["llama7b", "llama3"]:
                    output = self.model.generate(
                        **inputs, generation_config=generation_config, is_audio_generation_mode=is_audio_generation_mode
                    )
                else:
                    if inputs.get("inputs_embeds") is None:
                        inputs_embeds = prepare_inputs_embeds(
                            model=self.model,
                            input_ids=inputs.get("input_ids"),
                            query_embeds_image=inputs.get("query_embeds_image"),  # imagePatch embeds
                            query_embeds_video=inputs.get("query_embeds_video"),  # video embeds
                            **inputs_audio,  # audioPatch embeds
                            target_embeds=None,  # target image/audioPatch embeds
                            position_ids=inputs.get("position_ids"),
                            attention_mask=inputs.get("attention_mask"),
                            image_grid_thw=inputs.get("image_grid_thw"),
                            image_grid_thw_video=inputs.get("image_grid_thw_video"),
                        )
                        inputs["inputs_embeds"] = inputs_embeds
                    output = self.model.generate(
                        **inputs, generation_config=generation_config, is_audio_generation_mode=is_audio_generation_mode
                    )

            if llama_return_dict:
                return output

            if self.llm_type not in ["llama7b", "llama3", "bailingv4", "qwen2"]:
                self.null_id = self.tokenizer.convert_tokens_to_ids("")
                # set tokens larger than special tokens to '', to avoid "piece id is out if range"
                output[output >= self.model_config.image_patch_token] = self.null_id
                # to visualize output_string
                # results_world = tokens.tolist()
                # logger.dist_all(self.llm_tokenizer.batch_decode(results_world))

        # post process
        output_dict = None
        if negative_prompt:
            output = output[: output.shape[0] // 2]
        if target_modality == "image":
            pass
            # TODO image generation here
        elif target_modality == "audio":
            pass
            # TODO audio generation here
        if output_dict is not None:
            return output_dict
        else:
            return output

    def auto_configure_device_map(self, dist_gpu_nums, num_trans_layers: int = 48, is_peft_model=False):
        # transformer.layers 默认占用 48 层；其他层默认放入cuda:0
        # lora引入后模型的结构及命名会改变
        layer_prefix = "base_model.model." if is_peft_model else ""
        per_gpu_layers = (num_trans_layers + 5) / dist_gpu_nums - 1
        # 设备映射表
        device_map = {
            f"{layer_prefix}glm.word_embeddings": 0,
            f"{layer_prefix}glm.transformer.final_layernorm": dist_gpu_nums - 1,
            f"{layer_prefix}glm.transformer.position_embeddings": 0,
            f"{layer_prefix}glm.transformer.block_position_embeddings": 0,
            f"{layer_prefix}lm_head": dist_gpu_nums - 1,
        }
        current_device_used = 0
        gpu_target = 1
        for i in range(num_trans_layers):
            if current_device_used >= per_gpu_layers:
                gpu_target += 1
                current_device_used = 0
            # 超过gpu总数默认放到最后一层
            if gpu_target > (dist_gpu_nums - 1):
                gpu_target = dist_gpu_nums - 1
            device_map[f"{layer_prefix}glm.transformer.layers.{i}"] = gpu_target
            current_device_used += 1
        return device_map

    def sft_initialize_vision_tokenizer(self):
        if self.config.copy_ori_embedding and self.num_new_tokens > 0:
            input_embeddings = self.model.get_input_embeddings().weight.data
            output_embeddings = self.model.get_output_embeddings().weight.data

            input_embeddings[: -self.num_new_tokens] = self.ori_input_embeddings[: -self.num_new_tokens]
            output_embeddings[: -self.num_new_tokens] = self.ori_output_embeddings[: -self.num_new_tokens]

    @classmethod
    def from_config(cls, cfg, **kwargs):
        # model = cls(BailingMMConfig(cfg))
        model = cls(cfg, **kwargs)

        # copy original llm word embedding
        model.sft_initialize_vision_tokenizer()

        return model

    def get_optimizer_params(
        self, weight_decay, lr_scale=1, visual_encoder_lr_scale=1.0, tuner_lr_scale=1.0, all_no_decay=True
    ):

        vit_num_layers = self.vision.get_num_layer()
        logger.info(f"lr scale: {lr_scale}")
        lr_scales = list(lr_scale ** (vit_num_layers - i) for i in range(vit_num_layers + 1))

        parameter_group_names = {}
        parameter_group_vars = {}

        for name, param in self.named_parameters():
            logger.dist_all(f"{name}: {param.shape}")

            if not param.requires_grad:
                continue  # frozen weights

            if all_no_decay:
                group_name = "no_decay"
                this_weight_decay = 0.0
            elif any(
                (
                    name.endswith("ls1"),
                    name.endswith("ls2"),
                    "input_layernorm" in name,
                    "post_attention_layernorm" in name,
                    name.endswith("bias"),
                    name.endswith("norm.weight"),
                    name.endswith("norm1.weight"),
                    name.endswith("norm2.weight"),
                    "ln_q" in name,
                    "ln_kv" in name,
                    "ln_post" in name,
                )
            ):
                group_name = "no_decay"
                this_weight_decay = 0.0
            else:
                group_name = "decay"
                this_weight_decay = weight_decay

            if name == 'proj':
                group_name = f"proj_{group_name}"

            if 'vision' in name:
                layer_id = self.vision.get_num_layer(name.replace('vision.', ''))
                group_name = "vit_layer_%d_%s" % (layer_id, group_name)
            else:
                layer_id = None

            # if 'Resampler' in name:
            #     group_name = f"resampler_{group_name}"

            if 'glm_model' in name:
                group_name = f"glm_{group_name}"

            if group_name not in parameter_group_names:
                if layer_id is not None:
                    scale = lr_scales[layer_id]
                    scale = scale * visual_encoder_lr_scale
                # elif group_name.startswith('resampler_'):
                #     scale = visual_encoder_lr_scale * tuner_lr_scale
                #     logger.info(f"Setting resampler lr scale to {scale}")
                elif group_name.startswith('glm_'):
                    scale = 1
                    logger.info(f"Setting text_lr_scale to {scale}")
                elif group_name.startswith('proj_'):
                    scale = visual_encoder_lr_scale * tuner_lr_scale
                    logger.info(f"Setting proj lr scale to {scale}")
                else:
                    scale = 1
                logger.dist_all(f"Optimizer {group_name}: {scale}")
                parameter_group_names[group_name] = {"weight_decay": this_weight_decay, "params": [], "lr_scale": scale}
                parameter_group_vars[group_name] = {"weight_decay": this_weight_decay, "params": [], "lr_scale": scale}
                # logger.info(f"{group_name}: lr scale {scale}")
            parameter_group_vars[group_name]["params"].append(param)
            parameter_group_names[group_name]["params"].append(name)
        for group_name in parameter_group_names.keys():
            logger.dist_all(
                f"---------------{group_name}: {parameter_group_names[group_name]['lr_scale']}---------------"
            )
            for param_name in parameter_group_names[group_name]['params']:
                logger.dist_all(f"{group_name}: {param_name}")
        # import json
        # logger.dist_all("Param groups = %s" % json.dumps(parameter_group_names, indent=2))
        optim_params = list(parameter_group_vars.values())
        # logger.info(f"Optimizing {num_optimized_parameters_visual} visual parameters.")
        # logger.info(f"Optimizing {num_optimized_parameters}({num_optimized_parameters/total_parameters*100:.2f}% of {total_parameters}) parameters.")
        return optim_params

    def sharded_state_dict(
        self,
        prefix: str = '',
        sharded_offsets: Tuple[Tuple[int, int, int]] = (),
        metadata: Optional[dict] = None,
    ):
        """
            1. load: sharded_state_dict (ShardedStateDict): state dict of the existing model
                populated with ShardedTensors. Used as a mapping to determine which
                parts of global tensors stored in the checkpoint should be loaded.
            2. save:
            state_dict['model'] = (model[0].sharded_state_dict()
                                   if use_dist_ckpt else
                                   model[0].state_dict_for_save_checkpoint())
            `keep_vars=True` is passed to module.state_dict so that optimizer states
        can be sharded later on.

            TODO: this function is used by save
        """
        logger.info(f"sharded_state_dict is called {metadata=}")
        from megatron.core.transformer.utils import (
            make_sharded_tensors_for_checkpoint,
            sharded_state_dict_default,
        )

        sharded_state_dict = {}
        # Save parameters
        self._save_to_state_dict(sharded_state_dict, '', keep_vars=True)
        # need megatron modify optimizer save
        # return model.state_dict()
        # TODO: DCP format is on developing
        sharded_state_dict = make_sharded_tensors_for_checkpoint(
            sharded_state_dict, prefix, sharded_offsets=sharded_offsets
        )
        # Recurse into submodules
        for name, module in self.named_children():
            sharded_state_dict.update(sharded_state_dict_default(module, f'{prefix}{name}.', sharded_offsets, metadata))
        # mapping: use ShardedTensorFactory for load from different ckpt
        # on dcp: decoder.layers.3.self_attention.linear_proj.weight  etc
        # on model: model.decoder.layers.3.self_attention.linear_proj.weight  etc
        # 首次从语言模型的DCP恢复时，没有vision、audio的参数，无法使用dcp恢复，需要转换为torchbin
        #

        return sharded_state_dict

    def state_dict_for_save_checkpoint(self, prefix='', keep_vars=False):
        # save format=torch,torch dcp
        return self.state_dict(prefix=prefix, keep_vars=keep_vars)

    def shared_embedding_or_output_weight(self): # -> Tensor:
        """Gets the embedding weight or output logit weights when share input embedding and
        output weights set to True or when use Multi-Token Prediction (MTP) feature.
        Returns:
            Tensor: During pre processing or MTP process it returns the input embeddings weight.
            Otherwise, during post processing it returns the final output layers weight.
        """
        if self.model.pre_process:
            assert hasattr(
                self.model, 'embedding'
            ), f"embedding is needed in this pipeline stage, but it is not initialized."
            return self.model.embedding.word_embeddings.weight
        elif self.model.mtp_process and self.model.mtp_block_spec.mtp_block_type in ('m', 'n') and getattr(self.model, 'embedding', None):
            return self.model.embedding.word_embeddings.weight
        elif self.model.post_process:
            return self.model.output_layer.weight
        return None
