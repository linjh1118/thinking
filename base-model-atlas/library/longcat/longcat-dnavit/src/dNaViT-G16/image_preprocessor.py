"""Image preprocessing for dNaViT."""

import numpy as np
import torch
from PIL import Image
from transformers.image_processing_utils import BaseImageProcessor, BatchFeature


class dNaViTImageProcessor(BaseImageProcessor):
    """RGB images -> normalized pixel values plus the tokenizer patch grid."""

    model_input_names = ["pixel_values", "image_grid_thw"]

    def __init__(self, patch_size=16, spatial_merge_size=2, image_mean=None,
                 image_std=None, **kwargs):
        super().__init__(**kwargs)
        self.patch_size = int(patch_size)
        self.spatial_merge_size = int(spatial_merge_size)
        self.image_mean = list(image_mean or (0.5, 0.5, 0.5))
        self.image_std = list(image_std or (0.5, 0.5, 0.5))

    def preprocess(self, images, **kwargs):
        if isinstance(images, Image.Image):
            images = [images]

        multiple = self.patch_size * self.spatial_merge_size
        mean = torch.tensor(self.image_mean, dtype=torch.float32).view(3, 1, 1)
        std = torch.tensor(self.image_std, dtype=torch.float32).view(3, 1, 1)

        pixel_values, grids = [], []
        for image in images:
            image = image.convert("RGB")
            array = np.asarray(image).astype(np.float32) / 255.0
            tensor = torch.from_numpy(array).permute(2, 0, 1)
            pixel_values.append((tensor - mean) / std)
            height = (image.height + multiple - 1) // multiple * multiple
            width = (image.width + multiple - 1) // multiple * multiple
            grids.append([1, height // self.patch_size, width // self.patch_size])

        return BatchFeature(data={
            "pixel_values": pixel_values,
            "image_grid_thw": torch.tensor(grids, dtype=torch.long),
        })
