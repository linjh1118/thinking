---
license: openmdw-1.1
base_model: nvidia/Cosmos3-Nano
---

# Model Overview

### Description:
Cosmos AnomalyGen — Mobile Phone Screen (UC3) generates synthetic mobile-phone-screen anomaly images by inpainting a user-supplied binary mask onto a clean reference screen image, conditioned on one of three trained defect types (oil, scratch, stain). The release ships only the few-shot-finetuned modules — a set of per-defect-type LoRA adapters — which plug into the frozen Cosmos3-Nano diffusion backbone (also using a frozen Wan2.2 VAE tokenizer and a frozen Qwen3-VL text encoder) at inference time. Cosmos AnomalyGen — UC3 v1.2.0 was developed by NVIDIA as part of the Cosmos AnomalyGen pipeline. This model is ready for commercial or non-commercial use.<br>

### License/Terms of Use:

**GOVERNING DOWNLOAD TERMS:** Use of the model is governed by the [OpenMDW License Agreement, version 1.1](https://openmdw.ai/license/1-1/).<br>

**ADDITIONAL INFORMATION:** The Cosmos3-Nano base model is governed by [OpenMDW License Agreement, version 1.1](https://openmdw.ai/license/1-1/). The training framework uses components governed by [Apache License, Version 2.0](https://www.apache.org/licenses/LICENSE-2.0).<br>

### Deployment Geography:
Global<br>

### Use Case:
Industrial visual-inspection teams responsible for mobile-phone-screen QA who have very few (≤5 per defect type) real anomaly examples. The model produces large-scale synthetic anomaly datasets (clean screen + binary mask → realistic oil / scratch / stain image) for training downstream defect-detection or segmentation models, including downstream consumers via the pseudo-labeling export path (COCO instance annotations and per-class classification layout).<br>

### Release Date:
Github 10/20/2026 via https://github.com/NVIDIA/cdf-anomalygen<br>

## References(s):
- Cosmos Framework — https://github.com/NVIDIA/cosmos-framework
- Cosmos3-Nano — https://huggingface.co/nvidia/Cosmos3-Nano
- Wan2.2 VAE tokenizer — https://huggingface.co/Wan-AI/Wan2.2-TI2V-5B
- Qwen3-VL-8B-Instruct tokenizer — https://huggingface.co/Qwen/Qwen3-VL-8B-Instruct
- LoRA: Low-Rank Adaptation of Large Language Models — paper: https://arxiv.org/abs/2106.09685
- Mobile Screen dataset — https://universe.roboflow.com/vu-thi-thu-huyen/mobile-screen<br>

## Model Architecture:
**Architecture Type:** Transformer (diffusion MoT backbone with learnable per-defect-type conditioning modules)<br>

**Network Architecture:**
- `per_class_lora` *(trainable, included in this release)*: per-defect-type LoRA adapters (rank 8, alpha 8) on the four generation-expert attention projections (`q_proj_moe_gen`, `k_proj_moe_gen`, `v_proj_moe_gen`, `o_proj_moe_gen`) of all 36 layers — three pairs trained for UC3: `Phone+oil`, `Phone+scratch`, `Phone+stain`; each generation token is routed to the adapter of its defect type.
- `tokenizer` *(frozen, not redistributed in this release)*: Wan2.2 VAE (16× spatial compression, 48 latent channels); weights are loaded from the separately downloaded `Wan-AI/Wan2.2-TI2V-5B` checkpoint at inference time.
- `text_encoder` *(frozen, not redistributed in this release)*: the Qwen3-VL-8B reasoner tower of Cosmos3-Nano, with the `Qwen/Qwen3-VL-8B-Instruct` tokenizer.
- These modules condition the **frozen** Cosmos3-Nano Mixture-of-Transformers (MoT) diffusion denoiser (36 layers, hidden size 4096) at inference time.<br>

**This model was developed based on Cosmos3-Nano.**<br>

**Number of model parameters:** Approximately 2.3×10^7 (23.0 million) trainable parameters in the released modules — `per_class_lora` ≈ 7.67M per `<texture>+<anomaly_type>` pair (rank-8 adapters on 4 projections × 36 layers) × 3 pairs = 23,003,136. The trainable modules are distributed as the `model/iter_000012000.pt` checkpoint file. The frozen Cosmos3-Nano base contributes ~1.6×10^10 (16 billion) parameters used at inference time but **not** redistributed in this release.<br>


## Input(s):
**Input Type(s):** Image, Binary Mask, Text<br>

**Input Format(s):**
- Image: PNG / JPG, Red, Green, Blue (RGB)
- Binary Mask: PNG / JPG, single-channel binary (0 = background, 255 = anomaly region; binarized at threshold 127)
- Text: anomaly-type string in the form `<texture>+<anomaly_type>` (one of `Phone+oil`, `Phone+scratch`, `Phone+stain`)<br>

**Input Parameters:**
- Image: Two-Dimensional (2D)
- Mask: Two-Dimensional (2D)
- Text: One-Dimensional (1D)<br>

**Other Properties Related to Input:** Input clean image and paired mask must have the same dimensions; the model was trained on defect-centred crops at variable model input sizes (256 / 512 / 1024 / 1536 px) and inference is run with the same crop geometry, so there is no fixed input resolution. `anomaly_type` must exactly match one of the three pairs trained for this UC3 checkpoint — passing an unsupported defect string is rejected by `anomalygen/scripts/texture/generate.py` against this checkpoint's recipe `anomaly_types` (the checkpoint carries a geometry stamp and refuses a recipe that differs from the one it trained under). The mask should ideally cover a contiguous defect region that resembles the trained mask distribution; the optional Automatic Mask Placement (AMP) tool, or the default Agentic Mask Generation (AMG) stage, can constrain placement to legal ROIs.<br>

## Output(s)

**Output Type(s):** Image<br>

**Output Format(s):** PNG; Red, Green, Blue (RGB)<br>

**Output Parameters:** Two-Dimensional (2D)<br>

**Other Properties Related to Output:** RGB synthetic anomaly image at the native resolution of the input clean image. Anomaly content is generated inside the user-supplied mask region; the inpainted patch is pasted back onto the clean reference image so non-masked pixels remain identical to the input. Optionally Poisson blending can be enabled. Generation metadata (per-sample guidance, crop_ratio, seed, etc.) is written to `texture_ft_generation_result.csv` alongside the images; samples rejected by the default content-safety guardrail are listed in `guardrail_blocked.csv`.<br>

Our AI models are designed and/or optimized to run on NVIDIA GPU-accelerated systems. By leveraging NVIDIA's hardware (e.g. GPU cores) and software frameworks (e.g., CUDA libraries), the model achieves faster training and inference times compared to CPU-only solutions.<br>

## Software Integration:
**Runtime Engine(s):**
- PyTorch (via the Cosmos Framework / Cosmos3-Nano pipeline)
- Cosmos AnomalyGen scripts (`anomalygen/scripts/texture/generate.py`, torchrun-based)
- Downstream dataset export via pseudo-labeling (`anomalygen/scripts/texture/pseudo_label.py`; COCO instance annotations + classification layout)<br>

**Supported Hardware Microarchitecture Compatibility:**
- NVIDIA Ampere A100
- NVIDIA Hopper H100
- NVIDIA RTX PRO 6000 Blackwell<br>

**Supported Operating System(s):**
- Linux<br>

The integration of foundation and fine-tuned models into AI systems requires additional testing using use-case-specific data to ensure safe and effective deployment. Following the V-model methodology, iterative testing and validation at both unit and system levels are essential to mitigate risks, meet technical and functional requirements, and ensure compliance with safety and ethical standards before deployment.<br>

## Model Version(s):
v1.2.0 — `uc3-phone-screen-nano-iter12000` (trained 15,000 iterations, best checkpoint at 12,000; released artifacts are the `model/iter_000012000.pt` checkpoint file containing finetuned modules only, its `iter_000012000.pt.sha256` digest sidecar, and its `exp_texture_ft_phone_screen.yaml` training recipe).<br>

## Training, Testing, and Evaluation Datasets:

### Dataset Overview
- Total Number of Datasets: 2 (Roboflow `vu-thi-thu-huyen/mobile-screen` + Hugging Face `nvidia/Cosmos-AnomalyGen-Glass-Masks`)
- Total Size: 15 anomaly RGB images + 15 paired binary masks + 20 clean reference screen images (clean images are used at inference time, not as supervised training targets)
- Dataset partition: 100% Training (few-shot fine-tuning regime; no held-out validation or test split)<br>

## Public Datasets
- `vu-thi-thu-huyen/mobile-screen` — Roboflow Universe, https://universe.roboflow.com/vu-thi-thu-huyen/mobile-screen — source of mobile-phone-screen RGB images (anomaly and clean).
- `nvidia/Cosmos-AnomalyGen-Glass-Masks` — Hugging Face — source of binary defect masks and `defect_spec.jsonl`.<br>

## Training Dataset:

### Data Modality:
- Image<br>

### Training Data Size:
- Less than a Million Images (15 anomaly images + 15 paired masks; 5 per defect type × 3 types)

** Data Collection Method by dataset
- Hybrid: Manually-Collected, Automatic/Sensors

** Labeling Method by dataset
- Manually-Labeled

**Properties:** 15 RGB images of mobile phone screens spanning three defect categories — `oil` (5 images), `scratch` (5 images), `stain` (5 images) — each paired with a per-defect binary mask. Clean screen images from the same Roboflow source are used as inpainting references at inference time. No personal data, copyrighted content (other than the Roboflow CC-licensed source), or human subjects are present in the dataset.<br>

### Testing Dataset:
Not Applicable — the model is qualitatively evaluated via the `ValidationKPI` validation callback (inpainted samples logged every N training steps) rather than against a held-out test split.<br>

### Evaluation Dataset:
Not Applicable — no held-out evaluation dataset. The model is evaluated qualitatively during training via the `ValidationKPI` validation callback, plus FID, nearest-neighbour metrics (`nn_score`, `mnn_score`) and anomaly-quality metrics (`completeness`, `precision`, `boundary_iou`) logged at each validation step. See the [Explainability](EXPLAINABILITY.md) subcard for performance metric details.<br>

## Inference:
**Acceleration Engine:** PyTorch (native, BF16). Multi-GPU data-parallel inference is supported via `torchrun --nproc_per_node=<N>` with the `anomalygen_texture_ft` experiment.<br>

**Test Hardware:**
- NVIDIA Ampere A100
- NVIDIA Hopper H100
- NVIDIA RTX PRO 6000 Blackwell<br>

## Ethical Considerations:
NVIDIA believes Trustworthy AI is a shared responsibility and we have established policies and practices to enable development for a wide array of AI applications. Developers should work with their internal model team to ensure this model meets requirements for the relevant industry and use case and addresses unforeseen product misuse.<br>

Please make sure you have proper rights and permissions for all input image and video content.<br>

Users are responsible for model inputs and outputs. Users are responsible for ensuring safe integration of this model, including implementing guardrails as well as other safety mechanisms, prior to deployment.<br>

For more detailed information on ethical considerations for this model, please see the [Bias](BIAS.md), [Explainability](EXPLAINABILITY.md), [Privacy](PRIVACY.md), and [Safety & Security](SAFETY.md) subcards.<br>

Please report model quality, risk, security vulnerabilities or NVIDIA AI Concerns [here](https://www.nvidia.com/en-us/support/submit-security-vulnerability/).<br>
