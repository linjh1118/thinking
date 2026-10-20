---
license: openmdw-1.1
base_model: Qwen/Qwen-Image-Edit
---
# Model Overview

### Description:
`cdf-sim2real-smt-solderlight` transforms Omniverse-rendered synthetic printed-circuit-board (PCB) component crops into restrained raked solder-light automated-optical-inspection (AOI) style images for inspection data augmentation. The release is an NVIDIA fine-tuned version of the Qwen-Image-Edit image-to-image diffusion pipeline (diffusion transformer, Qwen2.5-VL text encoder, Qwen-Image VAE, tokenizer, image processor, and scheduler configuration), specialized for Omniverse-rendered printed-circuit-board (PCB) component-crop → solder-light style transfer. `cdf-sim2real-smt-solderlight` v1.0.0 was developed by NVIDIA as part of the CDF sim-to-real inspection-data augmentation pipeline. This model is ready for commercial or non-commercial use.<br>

### License/Terms of Use:

Governing Terms: Use of this model is governed by the [OpenMDW License Agreement, Version 1.1 (OpenMDW-1.1)](https://openmdw.ai/license/1-1). Additional Information: [Apache License, Version 2.0](https://huggingface.co/Qwen/Qwen-Image-Edit) applies to the upstream Qwen-Image-Edit components.

### Deployment Geography:
Global<br>

### Use Case:
NVIDIA engineers and researchers building printed-circuit-board (PCB) inspection / automated optical inspection (AOI) systems that need restrained raked solder-light component-crop imagery for data augmentation and sim-to-real workflow development. The model converts Omniverse-rendered synthetic printed-circuit-board (PCB) component crops into the target solder-light AOI style while preserving component identity, crop geometry, markings, and body shape. This model is **not** intended to be the primary inspection decision-maker; it is a sim-to-real data-translation step. Inspection pass/fail decisions must come from a downstream inspection model with human review.<br>

### Release Date:
Github 10/20/2026 via https://github.com/NVIDIA/paidf-augmentation

## References(s):
- Qwen-Image-Edit base model — https://huggingface.co/Qwen/Qwen-Image-Edit
- Qwen2.5-VL text encoder — https://huggingface.co/Qwen/Qwen2.5-VL-7B-Instruct
- LoRA: Hu et al., "LoRA: Low-Rank Adaptation of Large Language Models," 2021 — https://arxiv.org/abs/2106.09685
- Diffusers library — https://github.com/huggingface/diffusers<br>

## Model Architecture:
**Architecture Type:** Transformer (diffusion transformer with cross-modal conditioning)<br>

**Network Architecture:** This release is a self-contained HuggingFace `diffusers` pipeline directory, located under `model/` in this repository. All of the following components are redistributed as part of the release artifact:
- `model/transformer/` *(NVIDIA fine-tuned, redistributed)*: the upstream Qwen-Image-Edit flow-matching image-to-image diffusion transformer, fine-tuned by NVIDIA on the attention and feed-forward projections of `QwenImageTransformerBlock` (`to_q`, `to_k`, `to_v`, `to_out.0`, the cross-attention `add_{q,k,v}_proj` / `to_add_out`, and `img_mlp` / `txt_mlp` projections).
- `model/text_encoder/` *(redistributed unmodified)*: Qwen2.5-VL; attends over both the input image and the instruction prompt.
- `model/vae/` *(redistributed unmodified)*: Qwen-Image VAE.
- `model/tokenizer/`, `model/processor/`, `model/scheduler/`, and `model/model_index.json` *(redistributed unmodified)*: Qwen-Image-Edit tokenizer, image processor, scheduler configuration, and pipeline entry point.
- Fine-tuning methodology: NVIDIA fine-tuned the transformer using LoRA (rank 16, alpha 16, dropout 0.0, ~1.7 × 10^8 parameters introduced during training). Training used the paired clean-prompt solder-light dataset for 3000 steps with batch size 1, learning rate 1e-4, seed 0, bf16 precision, gradient checkpointing, and Qwen-Image's resolution-aware time-shift schedule. The final LoRA adapter was fused into the base `Qwen/Qwen-Image-Edit` pipeline at scale 1.0 in bf16, so the released artifact is a standalone diffusers pipeline that requires no separate adapter file at inference time.
- The pipeline can be loaded directly with `diffusers.QwenImageEditPipeline.from_pretrained("nvidia/cdf-sim2real-smt-solderlight", subfolder="model")`, or by pointing `from_pretrained` at a local copy of the `model/` directory.<br>

**This model was developed based on Qwen-Image-Edit.**<br>

**Number of model parameters:** Approximately ~2.0 × 10^10 (20B) total parameters in the released checkpoint. Of these, ~1.7 × 10^8 (170M) LoRA parameters in the diffusion transformer were trained by NVIDIA and then fused into the released transformer; the remaining parameters come from the upstream Qwen-Image-Edit pipeline (transformer + Qwen2.5-VL text encoder + Qwen-Image VAE) and are redistributed unmodified.<br>

## Input(s):
**Input Type(s):** Image, Text<br>

**Input Format(s):**
- Image: PNG / JPG, Red, Green, Blue (RGB)
- Text: UTF-8 instruction prompt (English)<br>

**Input Parameters:**
- Image: Two-Dimensional (2D)
- Text: One-Dimensional (1D)<br>

**Other Properties Related to Input:** Fine-tuned at target area 262,144 pixels (~0.5 MP, approximately 512×512 for square crops); other resolutions are accepted by the underlying diffusers pipeline but NVIDIA fine-tuning was not performed at them, so style fidelity may degrade. Input must be a single Omniverse-rendered synthetic printed-circuit-board (PCB) component crop similar to the solder-light source distribution used during training. The accompanying instruction prompt is the fixed English sentence used during training; the trained prompt is:

> "Render this PCB component crop as a restrained raked solder-light AOI inspection photograph. Keep the exact source geometry, crop, markings, and component body shape. Apply bright orange-red and cobalt-blue specular highlights only to existing solder pads, exposed leads, endcaps, pins, and metallic contacts. Keep plastic or ceramic IC bodies and large matte component centers dark, flat, and non-emissive; no fiery rings, halos, glow, speckled noise, or texture blooms on component bodies. Do not add any new letters, labels, logos, captions, watermarks, borders, or decorative graphics."

The instruction prompt is fixed and not user-configurable. The only input a user provides is the Omniverse-rendered synthetic printed-circuit-board (PCB) image to be processed; the model performs an image-constrained relighting edit of that image, not free-text text-to-image generation. This is a deliberate guardrail: the model was fine-tuned on this single instruction only, so the prompt is locked and cannot be a vector for misuse.

<br>

## Output(s)

**Output Type(s):** Image<br>

**Output Format(s):** PNG; Red, Green, Blue (RGB)<br>

**Output Parameters:** Two-Dimensional (2D)<br>

**Other Properties Related to Output:** Output resolution follows the input dimensions after preprocessing to the training target area. The output keeps the source component geometry and markings while applying the target solder-light AOI style.<br>

Our AI models are designed and/or optimized to run on NVIDIA GPU-accelerated systems. By leveraging NVIDIA's hardware (e.g. GPU cores) and software frameworks (e.g., CUDA libraries), the model achieves faster training and inference times compared to CPU-only solutions.<br>

## Software Integration:
**Runtime Engine(s):**
- PyTorch (via HuggingFace `diffusers` `QwenImageEditPipeline`)<br>

**Supported Hardware Microarchitecture Compatibility:**
NVIDIA Ampere (A100) <br>
NVIDIA Hopper (H100) <br>
NVIDIA Lovelace (RTX 40-series) <br>

**Supported Operating System(s):**
- Linux<br>

The integration of foundation and fine-tuned models into AI systems requires additional testing using use-case-specific data to ensure safe and effective deployment. Following the V-model methodology, iterative testing and validation at both unit and system levels are essential to mitigate risks, meet technical and functional requirements, and ensure compliance with safety and ethical standards before deployment.<br>

## Model Version(s):
v1.0.0 — `cdf-sim2real-smt-solderlight:v1` (NVIDIA clean-prompt LoRA fine-tune of the upstream `Qwen/Qwen-Image-Edit` pipeline, trained for 3000 steps and fused at scale 1.0). The released artifact is a self-contained HuggingFace `diffusers` pipeline directory stored under `model/` and containing `transformer/`, `text_encoder/`, `vae/`, `tokenizer/`, `processor/`, `scheduler/`, and `model_index.json`.<br>

## Training, Testing, and Evaluation Datasets:

### Dataset Overview
- Total Number of Datasets: 1 (paired Omniverse-rendered synthetic printed-circuit-board (PCB) component-crop inputs and pseudo-target solder-light AOI outputs; NVIDIA-internal)
- Total Size: 364 paired component crops, paired by matching filenames (364 Omniverse-rendered synthetic printed-circuit-board (PCB) component-crop inputs + 364 pseudo-target solder-light AOI outputs), ~512×512 each
- Dataset partition: Training only; no separate validation or test split is packaged with this run — evaluation is qualitative side-by-side review using a packaged preview report and internal visual inspection.
- Time period for data collection: September – October 2026<br>

## Training Dataset:

### Data Modality:
- Image
- Text (fixed instruction prompt)<br>

** Image Training Data Size

* [Less than a Million Images]

** Text Training Data Size

* [Less than a Billion Tokens]

** Data Collection Method by dataset
- Hybrid: Synthetic, Machine Generated (curated Omniverse-rendered synthetic printed-circuit-board (PCB) component-crop inputs plus machine-generated Qwen-Image-Edit pseudo-targets on the same inputs).

** Labeling Method by dataset
- Not Applicable — paired-image translation is supervised by the pseudo-target image itself; no per-image label is required beyond the fixed instruction prompt.

**Properties:** 364 paired component crops with Omniverse-rendered synthetic printed-circuit-board (PCB) component crops as input and Qwen-Image-Edit pseudo-target solder-light AOI output as target. Modality: image + a fixed English instruction prompt. Content nature: synthetic renders and machine-generated images of inanimate printed-circuit-board (PCB) components (NVIDIA-internal). Nine visually unsuitable samples were manually excluded from the packaged dataset and preview report. No personal data, no copyright-protected web content, no machine-generated text/speech. No human subjects are depicted.<br>

### Testing Dataset:
Data Collection Method by dataset:
* [Not Applicable]

Labeling Method by dataset:
* [Not Applicable]

**Properties** Not Applicable — no separate packaged test split is included for this run. <br>

### Evaluation Dataset:

** Data Collection Method by dataset
- Curated internal Omniverse-rendered synthetic printed-circuit-board (PCB) component-crop inputs plus machine-generated Qwen-Image-Edit pseudo-targets.

** Labeling Method by dataset
- Not Applicable

** Properties:** Qualitative evaluation uses a packaged side-by-side preview report for inspection of input and pseudo-target pairs, plus internal visual inspection of generated samples for geometry preservation and restrained solder-light style fidelity. No separate ground-truth human-photograph evaluation set is packaged with this release.<br>

## Inference:
**Acceleration Engine:** PyTorch (native, bf16 weights) via `diffusers.QwenImageEditPipeline.from_pretrained(..., subfolder="model")`, loaded directly from the released `model/` pipeline directory.<br>

**Test Hardware:**
- NVIDIA H100
- NVIDIA A100<br>

## Ethical Considerations:
NVIDIA believes Trustworthy AI is a shared responsibility and we have established policies and practices to enable development for a wide array of AI applications. Developers should work with their internal model team to ensure this model meets requirements for the relevant industry and use case and addresses unforeseen product misuse.<br>

Please make sure you have proper rights and permissions for all input image and video content; if image or video includes people, personal health information, or intellectual property, the image or video generated will not blur or maintain proportions of image subjects included.<br>

Users are responsible for model inputs and outputs. Users are responsible for ensuring safe integration of this model, including implementing guardrails as well as other safety mechanisms, prior to deployment.<br>

For more detailed information on ethical considerations for this model, please see the Bias, Explainability, Privacy, and Safety & Security subcards [Bias](BIAS.md), [Explainability](EXPLAINABILITY.md), [Privacy](PRIVACY.md), and [Safety & Security](SAFETY.md) subcards.<br>

Please report model quality, risk, security vulnerabilities or NVIDIA AI Concerns [here](https://www.nvidia.com/en-us/support/submit-security-vulnerability/).<br>
