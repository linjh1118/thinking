"""Configuration for dNaViT: discrete tokenizer + flow-matching refiner."""

from transformers import PretrainedConfig


class DNaViTConfig(PretrainedConfig):
    model_type = "dnavit"

    def __init__(
        self,
        vision_config=None,
        image_size=256,
        patch_size=16,
        spatial_merge_size=2,
        temporal_patch_size=2,
        res_mod=None,
        quantizer=None,
        pixel_decoder=None,
        refiner=None,
        vae=None,
        decode_sampler="native",
        decode_num_inference_steps=52,
        decode_seed=0,
        fixed_sr_scale=2,
        one_step_schedule_steps=52,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.vision_config = dict(vision_config or {})
        self.image_size = int(image_size)
        self.patch_size = int(patch_size)
        self.spatial_merge_size = int(spatial_merge_size)
        self.temporal_patch_size = int(temporal_patch_size)
        self.res_mod = dict(res_mod or {})
        self.quantizer = dict(quantizer or {})
        self.pixel_decoder = dict(pixel_decoder or {})
        self.refiner = dict(refiner or {})
        self.vae = dict(vae or {})
        self.decode_sampler = decode_sampler
        self.decode_num_inference_steps = int(decode_num_inference_steps)
        self.decode_seed = int(decode_seed)
        self.fixed_sr_scale = int(fixed_sr_scale)
        self.one_step_schedule_steps = int(one_step_schedule_steps)

        if decode_sampler not in ("native", "one_step"):
            raise ValueError(f"Unknown decode_sampler: {decode_sampler!r}")
        if decode_sampler == "one_step" and self.decode_num_inference_steps != 1:
            raise ValueError("decode_sampler='one_step' requires decode_num_inference_steps=1")
        if self.fixed_sr_scale < 1:
            raise ValueError(f"fixed_sr_scale must be positive, got {fixed_sr_scale}")
