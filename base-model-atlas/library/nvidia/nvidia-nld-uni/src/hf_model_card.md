---
library_name: transformers
pipeline_tag: any-to-any
tags:
  - custom_code
  - image-text-to-text
  - text-to-image
  - image-to-image
---

# Nemotron-Labs-Diffusion-Uni-8B

## Description

NLD-Uni is a unified multimodal model for image understanding and image generation. It combines a diffusion language model with specialized visual components and a mixture-of-transformers design. Understanding and generation use distinct transformer parameter paths within a common multimodal framework.

For image understanding, NLD-Uni encodes images into continuous visual features and generates text responses. For image generation, it models discrete visual tokens through iterative diffusion and decodes those tokens into RGB images. The architecture supports autoregressive and blockwise diffusion decoding for text, as well as image-conditioned generation and editing when enabled by the checkpoint and inference implementation.

This card describes the NLD-Uni architecture generally.

## Environment

Install the dependencies in `requirements.txt` with Python 3.13 and CUDA 12.6. Install PyTorch before building FlashAttention:

```bash
pip install -r requirements.txt
pip install --no-build-isolation flash-attn==2.8.0.post2
```

Validated on an NVIDIA H100 80 GB. The eight BF16 weight shards contain all 1,557 active model tensors. `weights_manifest.json` records their hashes.

## Python inference

```python
import torch
from transformers import AutoModelForCausalLM

model = AutoModelForCausalLM.from_pretrained(
    '/path/to/hf_checkpoint',  # or 'organization/model-name'
    trust_remote_code=True,
    torch_dtype=torch.bfloat16,
).to('cuda').eval()

image = model.text_to_image('A red ceramic mug on a wooden table.', seed=42)
image.save('mug.png')

edited = model.image_edit(image, 'Change the mug to blue.', seed=42)
edited.save('blue_mug.png')

answer = model.generate('What color is the mug?', image=edited)
print(answer)
```

Image inputs accept Pillow images or local file paths. Image methods return Pillow images; `generate` returns text by default. Token IDs can be supplied through `input_ids` for text prompts, and `return_token_ids=True` returns the generated token tensor. The `inference.py` command exposes each task.

## Minimal command-line inference

```bash
python inference.py /path/to/hf_checkpoint --task t2i --prompt 'A red mug.' --output mug.png
python inference.py /path/to/hf_checkpoint --task edit --image mug.png --prompt 'Make the mug blue.' --output blue.png
python inference.py /path/to/hf_checkpoint --task understand --image blue.png --prompt 'What color is the mug?'
```

Replace the model argument with the published Hugging Face model ID for remote loading. The standalone script only uses Transformers and this repository's model code.


### License/Terms of Use

GOVERNING TERMS: Use of this model is governed by the [NVIDIA Open Source License Agreement](https://huggingface.co/nvidia/NL-Diffusion-Image/raw/main/LICENSE).

## Deployment Geography

Global, subject to the governing release terms.

## Use Case

NLD-Uni is intended for research and evaluation of unified multimodal systems, including:

- Visual question answering and image-grounded reasoning.
- Document, chart, and scene-text understanding.
- Visual grounding and interface localization using task-specific prompts and output formats.
- Text-to-image generation.
- Image-conditioned generation and editing for checkpoints trained for these tasks.

## Release Date

GitLab 10/17/2026 via [NLD-Uni](https://gitlab-master.nvidia.com/shufanl/nld-uni).

## Model Architecture

**Architecture Type:** Transformer

**Network Architecture:** Diffusion language model with understanding and generation transformer paths, a continuous visual encoder for understanding, and a discrete image tokenizer for generation.

**Language-model foundation:** Nemotron diffusion language model.

## Input

**Input Type(s):** Text and images.

**Input Format(s):** Text strings and image objects or tensors accepted by the supplied processor.

**Input Parameters:** One-dimensional text-token sequences and two-dimensional image content, represented internally as visual features or discrete image tokens according to the task.

**Other Properties Related to Input:** Context length, image resolution, visual-token budget, and preprocessing are checkpoint- and task-dependent. The released inference configuration defines the supported limits; a universal 900-token prompt limit is not specified for the architecture.

## Output

**Output Type(s):**

- Text
- Image

**Output Format(s):**

- **Text:** `.json` (UTF-8 JSON records containing generated text).
- **Image:** `.png` (RGB images).

These serialized formats are implemented by `validate.py`. The inference API returns text strings or token IDs for understanding and decoded image objects or tensors for generation. Grounding outputs follow the requested coordinate or location-token format.

**Output Parameters:** One-dimensional token sequences or images with height, width, and three color channels. Tensor layout and pixel range are defined by the inference API.

**Other Properties Related to Output:** Text output length and generated image resolution depend on the checkpoint and inference settings. Configurations for 1,024 × 1,024 image generation are implemented; the release should list its validated resolutions.

## Software Integration

NLD-Uni’s native implementation uses PyTorch with CUDA-accelerated execution. The codebase also includes a dedicated SGLang integration for the image-understanding and text-generation path. This does not establish SGLang support for the image-generation path.

**Runtime Engine(s):**

- PyTorch for native multimodal inference.
- SGLang with the NLD-Uni/LaVida RADIO-H adapter for supported understanding configurations.

**Reference Platform:** Linux with NVIDIA CUDA GPUs.

**Reference Evaluation Hardware:** NVIDIA H100 (Hopper).

## Model Version(s)

- **NLD-Uni:** Unified image-understanding and image-generation architecture based on LaVida-O.

Training stage, checkpoint revision, tokenizer revision, and inference configuration are part of the identity of an evaluated model. Results from earlier LaVida-O or image-only diffusion models should retain their original model names.

# Training and Evaluation Datasets

## Training Dataset

More than 100M image-text pairs.

**Data Collection Method by dataset**

- Hybrid: Automated, Manually-Collected, Synthetic

**Labeling Method by dataset**

- Hybrid: Automated, Manually-Labeled, Synthetic

## Evaluation Datasets

### Documented Functional Validation Dataset

- **Modalities:** Text and RGB images.
- **Nature of content:** Synthetic everyday-object, animal, and landscape scenes; text-to-image prompts, edit instructions, and image-understanding questions. The generated images are used as inputs to subsequent editing and understanding tasks.
- **Linguistic characteristics:** English prompts, edit instructions, questions, and recorded answers.
- **Collection and labeling:** Three scripted scene cases in `validate.py`; model-generated images and answers were manually inspected for prompt alignment and editing fidelity.

Counts and results are recorded in [VALIDATION.md](VALIDATION.md), [validation.json](validation.json), and [examples/results.json](examples/results.json). These are functional smoke tests, not measurements of benchmark accuracy.

### Benchmark Evaluation Properties

The benchmark suite below covers image and text inputs, including mathematical and scientific questions, documents, charts, scene text, interfaces, referring expressions, and image-generation prompts. OCRBenchV2-EN identifies an English subset; the exact language coverage of the other evaluated splits must be documented from the evaluation records.

### Image Understanding

The evaluation suite should identify the following benchmarks and splits explicitly:

| Benchmark | Evaluation target | Primary reporting requirement |
|---|---|---|
| MathVista_MINI | Visual mathematical reasoning | Full 1,000-example accuracy; identify answer-extraction judge |
| MMMU_DEV_VAL | Multidisciplinary visual reasoning | Report development and validation splits separately |
| AI2D_TEST | Diagram understanding | Accuracy and image/prompt protocol |
| ChartQA_TEST | Chart question answering | Relaxed accuracy and subset aggregation |
| DocVQA_VAL | Document question answering | ANLS |
| TextVQA_VAL | Scene-text question answering | VQA accuracy with specified normalization |
| RealWorldQA | Real-world visual understanding | Accuracy |
| InfoVQA_VAL | Infographic question answering | ANLS |
| ScienceQA_TEST | Science question answering | Identify the image-containing subset when used |
| ScreenSpot-Pro | Interface grounding | Point-localization accuracy; separate first-pass and crop-refined results |
| RefCOCO | Referring-expression grounding | IoU ≥ 0.5 accuracy for val, testA, and testB; disclose the native LOC protocol |
| OCRBenchV2-EN | OCR and document understanding | Official English category aggregation |

### Image Generation

| Benchmark | Evaluation target | Primary metric |
|---|---|---|
| GenEval | Object presence, counts, colors, positions, and attribute binding | Overall and category scores |
| DPG-Bench | Alignment with detailed compositional prompts | Overall and category scores |
| MJHQ-30K | Generated-image distribution and quality | FID; any additional preference metric must identify its model and version |

Evaluation should identify the exact checkpoint, prompt processing, image preprocessing, decoding parameters, seed policy, sample count, and evaluator version. Report reasoning and non-reasoning results separately. Tokenizer reconstruction evaluation, if performed, should be identified separately from end-to-end image-generation quality.

## Key Considerations

NLD-Uni can produce incorrect text, inaccurate grounding coordinates, and synthetic images that do not fully follow the prompt. Generated content may reflect biases in training data or contain inappropriate material. Image-conditioned outputs may change details that users intended to preserve.

Applications should be evaluated on their intended tasks and data, with appropriate input and output controls. Model outputs should not be treated as verified factual evidence solely because they are fluent or visually plausible.

## Inference

**Native Engine:** PyTorch.

**Understanding Serving Integration:** SGLang with the model-specific adapter, for validated configurations.

**Reference Precision:** BF16 where supported by the selected implementation.

**Reference Hardware:** NVIDIA H100.

Use the model-specific tokenizer, processor, chat template, and task interface. Image understanding uses the continuous visual encoder; image generation uses the discrete image-token pipeline. Runtime optimizations, including CUDA graphs, should be evaluated with the exact checkpoint and decode configuration before publishing accuracy or speed claims.

## Ethical Considerations

NVIDIA believes trustworthy AI is a shared responsibility. Developers should evaluate NLD-Uni for the intended application, including potential errors, bias, privacy concerns, and misuse of generated content.

Users should have appropriate rights and permissions for input images and other supplied content. Generated or edited images may alter identities, text, object proportions, or scene details. Applications should communicate the synthetic nature of generated content where appropriate.

Users are responsible for model inputs and outputs and for implementing appropriate safeguards before deployment.

Report model quality concerns, security vulnerabilities, or NVIDIA AI concerns through [NVIDIA’s reporting channel](https://www.nvidia.com/en-us/support/submit-security-vulnerability/).

