# Copyright (c) 2026, NVIDIA CORPORATION. All rights reserved.
#
# Licensed under the NVIDIA Open Model License; see the LICENSE section of the
# model card for terms.

"""Configuration for Nemotron-Labs-Sigma models."""

try:  # transformers >= 5
    from transformers import PreTrainedConfig as _PretrainedConfig
except ImportError:  # transformers 4.x
    from transformers import PretrainedConfig as _PretrainedConfig


_DEFAULT_ROPE_PARAMETERS = {
    "rope_type": "yarn",
    "type": "yarn",
    "rope_theta": 1000000.0,
    "factor": 16.0,
    "original_max_position_embeddings": 16384,
    "beta_fast": 32.0,
    "beta_slow": 1.0,
    "mscale": 1.0,
    "mscale_all_dim": 1.0,
    "llama_4_scaling_beta": 0.1,
}


class NemotronLabsSigmaConfig(_PretrainedConfig):
    """Config for a continuous diffusion language model.

    The model denoises Gaussian noise in a low-dimensional (``embed_dim``)
    continuous token-embedding space with a Ministral-style decoder backbone,
    and decodes ``block_size``-token blocks in parallel.
    """

    model_type = "nemotron_labs_sigma"

    def __init__(
        self,
        vocab_size=131072,
        hidden_size=4096,
        intermediate_size=14336,
        num_hidden_layers=34,
        num_attention_heads=32,
        num_key_value_heads=8,
        head_dim=128,
        hidden_act="silu",
        max_position_embeddings=4096,
        rms_norm_eps=1e-5,
        rope_theta=1000000.0,
        rope_parameters=None,
        embed_dim=16,
        block_size=32,
        replaid_selfcond=True,
        replaid_clean_ar_embedding=True,
        replaid_disable_output_prior=False,
        replaid_disable_time_conditioning=False,
        initializer_range=0.02,
        tie_word_embeddings=False,
        pad_token_id=None,
        bos_token_id=1,
        eos_token_id=2,
        **kwargs,
    ):
        self.vocab_size = vocab_size
        self.hidden_size = hidden_size
        self.intermediate_size = intermediate_size
        self.num_hidden_layers = num_hidden_layers
        self.num_attention_heads = num_attention_heads
        self.num_key_value_heads = num_key_value_heads
        self.head_dim = head_dim
        self.hidden_act = hidden_act
        self.max_position_embeddings = max_position_embeddings
        self.rms_norm_eps = rms_norm_eps
        self.rope_theta = rope_theta
        rope_parameters = dict(rope_parameters or _DEFAULT_ROPE_PARAMETERS)
        rope_parameters.setdefault("rope_theta", rope_theta)
        self.rope_parameters = rope_parameters
        # transformers 4.x reads YaRN settings from `rope_scaling`.
        self.rope_scaling = dict(rope_parameters)
        self.schedule_parameterization = kwargs.pop("schedule_parameterization", "legacy")
        self.schedule_degree = kwargs.pop("schedule_degree", 32)
        self.embed_dim = embed_dim
        self.block_size = block_size
        self.replaid_selfcond = replaid_selfcond
        self.replaid_clean_ar_embedding = replaid_clean_ar_embedding
        self.replaid_disable_output_prior = replaid_disable_output_prior
        self.replaid_disable_time_conditioning = replaid_disable_time_conditioning
        self.initializer_range = initializer_range
        # Distilled (Phased DMD) variants: fixed native inference contract.
        self.native_family = kwargs.pop("native_family", None)
        self.native_nfe = kwargs.pop("native_nfe", None)
        self.include_ar_head = kwargs.pop("include_ar_head", False)
        super().__init__(
            tie_word_embeddings=tie_word_embeddings,
            pad_token_id=pad_token_id,
            bos_token_id=bos_token_id,
            eos_token_id=eos_token_id,
            **kwargs,
        )


def config_3b(**kwargs):
    return NemotronLabsSigmaConfig(
        hidden_size=3072,
        intermediate_size=9216,
        num_hidden_layers=26,
        **kwargs,
    )


def config_8b(**kwargs):
    return NemotronLabsSigmaConfig(
        hidden_size=4096,
        intermediate_size=14336,
        num_hidden_layers=34,
        **kwargs,
    )
