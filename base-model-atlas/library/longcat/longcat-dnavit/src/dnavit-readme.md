<div align="center">
  <img src="assets/longcat_logo.svg" width="280" alt="LongCat Logo" />
  <h1>dNaViT</h1>
  <p><strong>Meituan LongCat Team</strong></p>
  <p>
    <a href="https://lixiaotong97.github.io/dNaViT/">Project Page</a> ·
    <a href="https://github.com/meituan-longcat/LongCat-Next">Code &amp; Training</a>
  </p>
</div>

**dNaViT** is a family of native-resolution visual tokenizers with spatial
stride **32**. Each model encodes images into discrete codes; the G16 and G64
models reconstruct them with a **ViT pixel decoder** at the aligned input
resolution, and the G16R1 and G16R52 models decode G16 codes with a
**code-conditioned Refiner** at 2× the aligned input height and width.

[![dNaViT overview: a shared discrete visual vocabulary](assets/figures/figure-1-teaser.png)](assets/figures/figure-1-teaser.pdf)

**A shared visual vocabulary.** dNaViT connects reconstruction, understanding, generation, and editing through discrete visual codes. The overview includes downstream systems beyond this tokenizer release.

[**dNaViT: Discrete Codes are General-Purpose Visual Representations**](https://lixiaotong97.github.io/dNaViT/)
turns native-resolution images into discrete visual primitives analogous to
language tokens. Building on [LongCat-Next](https://github.com/meituan-longcat/LongCat-Next),
it provides a shared discrete interface for reconstruction, classification,
multimodal understanding, generation, and editing.

A frozen Qwen3-VL vision encoder supplies semantic features. A lightweight
**Residual Modulator (ResMod)** adds reconstruction-aware detail, and **grouped
product quantization** maps the features to discrete codes. Progressive training
uses semantic and pixel reconstruction objectives to balance the representation.
The decoder can reconstruct pixels directly or use a code-conditioned Refiner
to improve perceptual quality.

<details>
<summary><strong>More examples: understanding, generation, and editing</strong></summary>

[![Qualitative downstream examples using the dNaViT discrete representation](assets/figures/figure-2-showcase.png)](assets/figures/figure-2-showcase.pdf)

**Downstream showcases.** These examples illustrate the full dNaViT research system. They require separately trained downstream models and are not outputs of the tokenizer release alone.

</details>

## Model Family

| Model | Quantization groups | Image decoder | Output size |
| :--- | ---: | :--- | :--- |
| [dNaViT-G16](dNaViT-G16) | 16 | ViT pixel decoder | Aligned input size |
| [dNaViT-G16R1](dNaViT-G16R1) | 16 | One-step Refiner | 2× aligned input size |
| [dNaViT-G16R52](dNaViT-G16R52) | 16 | 52-step Refiner | 2× aligned input size |
| [dNaViT-G64](dNaViT-G64) | 64 | ViT pixel decoder | Aligned input size |

Each subdirectory contains one model. R1 and R52 identify the Refiner's
sampling budget; both use a G16 token layout. The paper refers to the refined
G16 variant as **dNaViT-G16-R**.

## Model Details

[![dNaViT architecture with ResMod and semantic and pixel reconstruction branches](assets/figures/figure-3-architecture.png)](assets/figures/figure-3-architecture.pdf)

**Tokenizer architecture.** A frozen vision encoder and ResMod supply reconstruction-aware semantic features; grouped quantization and dual reconstruction objectives learn a shared discrete representation.

[![Grouped product quantization and discrete visual interfaces](assets/figures/figure-4-tokenization.png)](assets/figures/figure-4-tokenization.pdf)

**Discrete-code interface.** Each spatial position contains one index per quantization group. The downstream language-model interfaces shown in the figure require additional components.

Components shared by all models:

| Component | Specification |
| :--- | :--- |
| Vision encoder | Qwen3-VL vision tower, 27 layers, hidden size 1,152 |
| ResMod | Intermediate-layer residual feature modulation |
| Spatial stride | 32, from 16-pixel patches and 2 × 2 merging |
| Codebook embedding dimension | 4,096 total |
| ViT pixel decoder | 24 layers, hidden size 1,152, patch size 16 |

Per-model differences:

| | G16 | G64 | G16R1 | G16R52 |
| :--- | :--- | :--- | :--- | :--- |
| Quantization | 16 groups, 16,384 entries per group | 64 groups, 4,096 entries per group | Same as G16 | Same as G16 |
| Codebook embedding per group | 256 | 64 | 256 | 256 |
| Discrete code payload per spatial position¹ | 224 bits | 768 bits | 224 bits | 224 bits |
| Refiner | — | — | 34-layer DiT, hidden size 4,608, 18 attention heads | 34-layer DiT, hidden size 4,608, 18 attention heads |
| VAE decoder | — | — | 32 latent channels | 32 latent channels |
| Refiner evaluations | — | — | 1 per image | 52 per image |
| Output dimensions | Aligned input height and width | Aligned input height and width | 2 × aligned input height and width | 2 × aligned input height and width |

¹ Excluding storage overhead.

For an aligned image of height `H` and width `W`, the code grid is
`H/32 × W/32`. Each grid position contains one code index per quantization
group. Increasing the group count increases the code payload while keeping
the number of spatial positions unchanged.

### Code-Conditioned Refiner (G16R1, G16R52)

The Refiner conditions directly on **discrete codebook embeddings** through
global context tokens and time-conditioned spatial residuals. It requires no
text prompt. For example, a 512 × 512 input produces a 1024 × 1024
reconstruction.

- **G16R52** uses the default native flow-matching sampler, which performs 52
  Euler updates in sigma space.
- **G16R1** is a one-step student distilled from a multi-step teacher with
  adversarial supervision. Its default sampler performs one Refiner velocity
  evaluation; the 52-step schedule stored in its configuration defines the
  distillation schedule, not 52 inference evaluations. Tokenization and VAE
  decoding also contribute to end-to-end latency.

## Reconstruction Examples

[![Code-conditioned Refiner and G16, G64, R52 and R1 reconstruction examples](assets/figures/figure-6-refiner.png)](assets/figures/figure-6-refiner.pdf)

**Refiner and reconstruction comparison.** The paper figure illustrates code-conditioned flow decoding and compares G16 and G64 pixel-decoder reconstructions with the 52-step Refiner and the one-step Refiner.

## Quick Start

Use Python 3.10 or newer with a CUDA-compatible PyTorch installation.
The project documents PyTorch 2.6.0 and Transformers 4.57.0 as its tested
versions. With PyTorch and torchvision installed, install the inference
dependencies:

```bash
pip install "transformers==4.57.0" timm einops pillow numpy safetensors
```

FlashAttention 2/3 is optional for these HF inference exports: the vision
tower uses SDPA, and packed decoder attention falls back to PyTorch SDPA
when FlashAttention is unavailable.

### Reconstruct an image

```python
import torch
from PIL import Image
from huggingface_hub import snapshot_download
from transformers import AutoImageProcessor, AutoModel

variant = "dNaViT-G16"  # dNaViT-G16, dNaViT-G16R1, dNaViT-G16R52, or dNaViT-G64
local_dir = snapshot_download(
    "meituan-longcat/LongCat-Next", allow_patterns=f"dNaViT/{variant}/*",
)
model_id = f"{local_dir}/dNaViT/{variant}"

# Refiner models (G16R1, G16R52) load in BF16; G16 and G64 use the default dtype.
is_refiner = variant in ("dNaViT-G16R1", "dNaViT-G16R52")
load_kwargs = {"torch_dtype": torch.bfloat16} if is_refiner else {}

processor = AutoImageProcessor.from_pretrained(model_id, trust_remote_code=True)
model = AutoModel.from_pretrained(
    model_id, trust_remote_code=True, **load_kwargs,
).to("cuda").eval()

image = Image.open("input.png").convert("RGB")
inputs = processor(images=image)

with torch.inference_mode():
    reconstructions = model(**inputs)

reconstructions[0].save("reconstruction.png")
```

`model_id` can be any local directory containing one model's files. Each
model directory includes its tokenizer weights and implementation; a separate
Qwen3-VL checkpoint is not needed for this inference example.

The processor returns a **list** of normalized image tensors and an
`image_grid_thw` tensor. The model's `forward` handles device transfer and
resizes each image's height and width up to a multiple of 32. It returns a
list of RGB `PIL.Image` objects.

The output dimensions are `ceil(H/32) * 32` by `ceil(W/32) * 32` in height
and width for G16 and G64, and `2 * ceil(H/32) * 32` by `2 * ceil(W/32) * 32`
for G16R1 and G16R52. With the pixel decoder, images already aligned to 32
pixels retain their dimensions. The Refiner uses a fixed noise seed of
`decode_seed=0` by default. To select a different seed, pass `decode_seed=42`,
for example, when calling `AutoModel.from_pretrained`.

### Encode and decode discrete codes

The lower-level `encode` API expects image dimensions aligned to 32 pixels
and normalized tensors already on the model's device. This single-image
example explicitly aligns the image before preprocessing:

```python
width, height = image.size
aligned_image = image.resize(
    ((width + 31) // 32 * 32, (height + 31) // 32 * 32),
    resample=Image.Resampling.BICUBIC,
)
token_inputs = processor(images=aligned_image)
pixels = [
    tensor.to(device=model.device, dtype=torch.bfloat16)
    for tensor in token_inputs["pixel_values"]
]

with torch.inference_mode():
    encoded = model.encode(pixels, token_inputs["image_grid_thw"])
    indices = encoded.indices
    grid_h, grid_w = (int(v) for v in encoded.out_grid_thw[0, 1:])
    reconstruction = model.decode(indices, grid_h, grid_w)[0]

print(indices.shape)
reconstruction.save("decoded.png")
```

- `encoded.indices`: integer code IDs of shape `(N, G)` and
  `N = grid_h * grid_w` for one image. `G = 16` with values in `[0, 16383]`
  for G16, G16R1, and G16R52; `G = 64` with values in `[0, 4095]` for G64.
- `encoded.out_grid_thw`: `(B, 3)` token-grid dimensions `[1, grid_h, grid_w]`.
- `encoded.codebook_quant`: codebook-space features of shape `(N, 4096)`.
- `encoded.quants`: decoder-projected features of shape `(N, 1152)`.

For G16 and G64, `decode` returns ViT pixel-decoder reconstructions at
`(grid_h * 32, grid_w * 32)` in height and width. For G16R1 and G16R52,
`decode` reconstructs the codebook embeddings from the IDs, runs the Refiner,
and returns images at `(2 * grid_h * 32, 2 * grid_w * 32)`.

For multiple images, `encode` packs their token sequences together. Split the
IDs using each image's `grid_h * grid_w` before decoding images with different
grid sizes; `forward` already handles this unpacking.

### Precision and memory

**G16 and G64.** The export contains BF16 linear/convolution weights and FP32
codebook, normalization, and embedding tensors. CUDA inference uses internal
BF16 autocast. Use the default loading dtype; explicitly requesting
`torch_dtype=torch.bfloat16` also casts FP32 tensors, including codebooks, and
can change discrete token assignments through rounding.

**G16R1 and G16R52.** Load these Refiner exports with
`torch_dtype=torch.bfloat16` as shown above. The weights include both BF16 and
FP32 tensors; this loading option also casts the FP32 tensors. GPU memory
requirements grow with image resolution, and the 2× output increases the
Refiner's spatial workload. Start with one image and a moderate input size.

## Reported Reconstruction Results

The following results are reported in the dNaViT manuscript and the project's
README. They use the **G16/G64 ViT pixel decoders without Refiner
enhancement**, with spatial stride 32. They are not Refiner benchmark results
and should not be attributed to G16R1 or G16R52; Refiner decoding changes both
the image decoder and the output resolution. See the
[project page](https://lixiaotong97.github.io/dNaViT/) for qualitative Refiner
examples and the method description.

### ImageNet validation

Evaluation uses all **50,000 ImageNet validation images**. Higher is better
for PSNR and SSIM.

| Model | Resolution | Spatial positions | PSNR (dB) ↑ | SSIM ↑ |
| :--- | :--- | ---: | ---: | ---: |
| G16 | 256 × 256 | 64 | 22.82 | 0.64 |
| G16 | 512 × 512 | 256 | 25.47 | 0.71 |
| G16 | 1024 × 1024 | 1,024 | 28.93 | 0.81 |
| G64 | 256 × 256 | 64 | 25.41 | 0.76 |
| G64 | 512 × 512 | 256 | 28.12 | 0.81 |
| G64 | 1024 × 1024 | 1,024 | 32.90 | 0.91 |

Spatial positions exclude the quantization-group dimension. G16 and G64 differ
in training configuration and duration, so their comparison is not a controlled
ablation of group count.

### TokBench

Scores are macro-averages over the three official instance-scale buckets.
T-ACC and T-NED are percentages; F-Sim is cosine similarity. Higher is better
for all three metrics.

| Model | Resolution | T-ACC (%) ↑ | T-NED (%) ↑ | F-Sim ↑ |
| :--- | :--- | ---: | ---: | ---: |
| G16 | 512 × 512 | 33.58 | 52.43 | 0.34 |
| G16 | 1024 × 1024 | 45.05 | 62.75 | 0.41 |
| G64 | 512 × 512 | 51.69 | 68.72 | 0.54 |
| G64 | 1024 × 1024 | 63.08 | 78.27 | 0.67 |

## Intended Use and Scope

This release supports visual tokenization, image reconstruction, and research
on discrete visual representations. The codes can serve as an interface for
downstream models, but this release does not include a language model or a
text-to-image or image-editing application. The paper's dNaViT-8B understanding,
generation, and editing results require additional model components and training.

Quantization and pixel decoding are lossy, and the generative Refiner can
introduce plausible detail; fine text, faces, and small structures in a
reconstruction may differ from the source image.

## Citation

```bibtex
@misc{li2026dnavitdiscretecodesgeneralpurposevisual,
      title={dNaViT: Discrete Codes are General-Purpose Visual Representations},
      author={Xiaotong Li and Zhengrong Yue and Xu Huang and Jialv Zou and
              Minhao Jing and Wenhao Yan and Haodong Li and Hai Huang and
              Bo Zhao and Yan Feng and Peng Pei and Xunliang Cai},
      year={2026},
}
```

## License

The project's license is **Apache-2.0**. Third-party components and externally
downloaded model weights remain subject to their respective licenses.
