"""Decision Index native-engine adapter using the released Transformers readout."""
from io import BytesIO
from pathlib import Path

from PIL import Image
from decision_index.engines.base import Engine, Unsupported as KitUnsupported
from decision_index.vision.images import load

from .model import SingVLS1, Unsupported, PUBLIC_IMAGE_MAX_PIXELS


class D3Engine(Engine):
    name = "sing-vl-s1"
    latency = "One native Transformers prediction including input preparation; model loading excluded."

    def __init__(self, model, device="cuda:0", image_root=None,
                 image_max_pixels=PUBLIC_IMAGE_MAX_PIXELS, **options):
        super().__init__(**options)
        self.image_root = image_root
        self.native = SingVLS1(model, device=device, image_max_pixels=image_max_pixels)
        self.provenance = {
            "kind": "native-transformers", "model": str(Path(model).resolve()),
            "max_pixels": image_max_pixels,
            "image_resize": "native Sing VL S1 processor: preserve aspect ratio, patch-grid rounding, RGB bicubic resize, 1.6 MP cap",
            "attention": "prefix-bidirectional full attention, causal GDN, no KV cache",
            "max_images": 4, "text_max_tokens": 65536, "vision_max_tokens": 10000,
        }

    def __call__(self, state, questions, images=(), prompt=None):
        decoded = []
        for ref in images:
            with Image.open(BytesIO(load(ref, self.image_root))) as image:
                decoded.append(image.copy())
        try:
            response, details = self.native.predict(state, questions, decoded)
        except Unsupported as exc:
            raise KitUnsupported(str(exc)) from exc
        grids = next(iter(details.values())).get("image_grid_thw")
        factor = self.native.image_factor
        raw = {"details": details, "prompt_metadata": prompt,
               "image_pixels": [int(t*h*w*factor*factor/self.native.merge_size**2) for t,h,w in grids or []],
               "image_tokens": next(iter(details.values())).get("image_tokens", 0)}
        return response, raw

    def runtime(self):
        return self.native.runtime()

    def close(self):
        del self.native
