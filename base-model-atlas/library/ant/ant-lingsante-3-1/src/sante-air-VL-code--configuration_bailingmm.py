#!/usr/bin/env python3
# coding=utf-8
# Copyright (c) Ant Group. All rights reserved.

from typing import Dict

from transformers.configuration_utils import PretrainedConfig


class ModelConfig(PretrainedConfig):
    model_type = "bailing_mm"

    def __init__(self, type: str, args: Dict, freeze: bool, half: bool = False, megatron_args: Dict = None, **kwargs):
        self.type = type
        self.args = args
        self.freeze = freeze
        self.half = half
        self.megatron_args = megatron_args

        super().__init__(**kwargs)


class BailingMMConfig(PretrainedConfig):
    model_type = "bailing_mm"

    def __init__(
        self,
        image_size=224,
        num_query_token=32,
        num_query_token_video=64,
        num_query_token_audio=32,
        num_decoder_image_token=1024,
        num_decoder_audio_token=512,
        max_txt_len=32,
        mlp_depth=1,
        add_position_emb=False,
        loss_weight=False,
        tune_word_embeddings=False,
        llm_config: ModelConfig = None,
        pool_after_mlp=False,
        norm_query_embeds=True,
        norm_ds_embeds=True,
        use_second_last_layer_feature=False,
        vit_train_last_layer=None,
        copy_ori_embedding=False,
        use_multi_patch=False,
        multi_patch_pooling=False,
        audio_vocab_size=4099,
        add_audio_token=False,
        vision_config: ModelConfig = None,
        audio_config: ModelConfig = None,
        loss_func: str = None,
        use_llm_3drope: str = None,
        offload_threshold_value: int = 150 * 1024 * 1024,
        offload_activation_dataset: list = None,
        vision_compression_type: str = None,
        vision_compression_keep_ratio: float = 0.25,
        vision_compression_window_size: int = 2,
        vision_compression_pack_mode: str = "boost",
        vision_compression_position: str = "after_bridge",
        **kwargs,
    ):
        self.audio_config = self._parse_model_config(audio_config)
        self.vision_config = self._parse_model_config(vision_config)
        self.llm_config = self._parse_model_config(llm_config)
        self.image_size = image_size
        self.num_query_token = num_query_token
        self.num_query_token_video = num_query_token_video
        self.num_query_token_audio = num_query_token_audio
        self.num_decoder_image_token = num_decoder_image_token
        self.num_decoder_audio_token = num_decoder_audio_token
        self.mlp_depth = mlp_depth
        self.add_position_emb = add_position_emb
        self.tune_word_embeddings = tune_word_embeddings
        self.vit_train_last_layer = vit_train_last_layer
        self.use_second_last_layer_feature = use_second_last_layer_feature
        self.copy_ori_embedding = copy_ori_embedding
        self.use_multi_patch = use_multi_patch
        self.multi_patch_pooling = multi_patch_pooling
        self.max_txt_len = max_txt_len
        self.loss_weight = loss_weight
        self.pool_after_mlp = pool_after_mlp
        self.norm_query_embeds = norm_query_embeds
        self.norm_ds_embeds = norm_ds_embeds
        self.audio_vocab_size = audio_vocab_size
        self.add_audio_token = add_audio_token
        self.loss_func = loss_func
        self.use_llm_3drope = use_llm_3drope
        self.offload_threshold_value = offload_threshold_value
        self.vision_compression_type = vision_compression_type
        self.vision_compression_keep_ratio = vision_compression_keep_ratio
        self.vision_compression_window_size = vision_compression_window_size
        if vision_compression_pack_mode not in {"boost", "preserve"}:
            raise ValueError(
                f"Invalid vision_compression_pack_mode: {vision_compression_pack_mode!r}. "
                "Expected one of ['boost', 'preserve']."
            )
        if vision_compression_pack_mode == "preserve" and vision_compression_type is None:
            # preserve 模式只是 VisionZip 的 packing 节奏开关；缺少 vision_compression_type
            # 时既不会真正压缩，也无 cache rewrite 写入 pack_length，但 PostProcessor.concat
            # 仍会切到 dynamic padding 分支截短 packed-sample，悄无声息地偏离 baseline。
            raise ValueError(
                "vision_compression_pack_mode='preserve' requires vision_compression_type "
                "to be set (e.g. 'visionzip'). preserve 是 VisionZip 的 packing 节奏开关，"
                "不能单独使用 —— 请设置 vision_compression_type，或将 pack_mode 改回 'boost'。"
            )
        self.vision_compression_pack_mode = vision_compression_pack_mode
        if vision_compression_position not in {"after_bridge", "before_bridge"}:
            raise ValueError(
                f"Invalid vision_compression_position: {vision_compression_position!r}. "
                "Expected one of ['after_bridge', 'before_bridge']."
            )
        if vision_compression_position == "before_bridge" and vision_compression_type is None:
            # before_bridge 仅在启用 VisionZip 时有意义：它决定 compressor 是在 linear_proj
            # (vision→LLM 维度的 bridge) 之前还是之后调用，缺少 vision_compression_type 时
            # 整条压缩路径都不存在，该开关无效果。
            raise ValueError(
                "vision_compression_position='before_bridge' requires vision_compression_type "
                "to be set (e.g. 'visionzip')."
            )
        self.vision_compression_position = vision_compression_position
        if offload_activation_dataset is None:
            offload_activation_dataset = []
        self.offload_activation_dataset = offload_activation_dataset
        super().__init__(**kwargs)

    def _parse_model_config(self, ori_config):
        config = ori_config
        if isinstance(ori_config, dict):
            config = ModelConfig(**ori_config)
        return config
