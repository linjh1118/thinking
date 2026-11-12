"""Configuration for dNaViT visual tokenizers."""

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
