---
license: other
license_name: nvidia-open-model-license
license_link: >-
  https://www.nvidia.com/en-us/agreements/enterprise-software/nvidia-open-model-license/
pipeline_tag: robotics
tags:
- simulation
- surgical-robotics
- video-generation
- world-model
- forward-dynamics
- inverse-dynamics
- policy
- policy-evaluation
- imitation-learning
- healthcare-robotics
base_model:
- nvidia/Cosmos3-Nano
datasets:
- nvidia/PhysicalAI-Robotics-Open-H-Embodiment
library_name: nv-medtech
---

<div align="center">
  <div align="center">
  <a href="https://github.com/NVIDIA-Medtech/Cosmos3-H-Embodied-Nano">
    <img src="https://img.shields.io/badge/GitHub-Cosmos3--H--Embodied--Nano-grey?logo=GitHub" alt="Runtime Badge">
  </a>
  <a href="https://huggingface.co/nvidia/Cosmos3-Nano">
    <img src="https://img.shields.io/badge/Model-Cosmos3--Nano-blue?logo=huggingface" alt="Base Model Badge">
  </a>
  <a href="https://huggingface.co/datasets/nvidia/PhysicalAI-Robotics-Open-H-Embodiment">
    <img src="https://img.shields.io/badge/Dataset-Open--H--Embodiment-brightgreen?logo=huggingface" alt="Dataset Badge">
  </a>
</div>
</div>

# Cosmos3-H-Embodied-Nano

## Description
Cosmos3-H-Embodied-Nano is [Cosmos3-Nano](https://huggingface.co/nvidia/Cosmos3-Nano) (16B) post-trained for 50,000 iterations on the [Open-H-Embodiment](https://huggingface.co/datasets/nvidia/PhysicalAI-Robotics-Open-H-Embodiment) surgical robotics data (15 dataset families) jointly for **forward dynamics**, **inverse dynamics** and **policy**, with up to 16 past actions as clean conditioning. It is a single Mixture-of-Transformers (MoT) that couples video, action, and text in one multimodal sequence. One model predicts robot actions and endoscopic video for dVRK-style and other surgical robots on 2.4 s clips (25 frames and 24 actions at 10 Hz):

- **Forward dynamics:** first frame and actions → video.
- **Inverse dynamics:** video → actions.
- **Policy:** first frame, text (task instruction) and action history → actions and video.

The three tasks are mixed 0.4 / 0.2 / 0.4 (forward dynamics / inverse dynamics / policy) during training. Because they are conditioning patterns of one shared model, a single checkpoint learns both directions of the surgical world–action relationship. It can be used directly in any of the three modes or fine-tuned further, for example on a single mode or on a new robot. For more information on the base model, please view the [Cosmos3-Nano Model Card](https://huggingface.co/nvidia/Cosmos3-Nano).

Cosmos3-H-Embodied-Nano is the successor of [Cosmos-H-Surgical-Simulator](https://huggingface.co/nvidia/Cosmos-H-Surgical-Simulator), which was a **forward-dynamics-only** surgical simulator built on the 2B-parameter Cosmos-Predict2.5 diffusion transformer. Cosmos3-H-Embodied-Nano moves to the larger Cosmos3 MoT architecture and to joint training of forward dynamics, inverse dynamics and policy.

The model is intended for surgical world-model generation, closed-loop evaluation and imitation-learning of surgical robotics policies, video-to-kinematics (inverse-dynamics) action labeling, and synthetic-data generation prior to deployment on a physical system.

This model is ready for commercial or non-commercial use.

## License/Terms of Use
GOVERNING DOWNLOAD TERMS: Use of the model is governed by the [NVIDIA Open Model License Agreement](https://www.nvidia.com/en-us/agreements/enterprise-software/nvidia-open-model-license/).

Additional Information: Use of the [Cosmos3-Nano](https://huggingface.co/nvidia/Cosmos3-Nano) base model is governed by the [NVIDIA Open Model License Agreement](https://www.nvidia.com/en-us/agreements/enterprise-software/nvidia-open-model-license/).

## Deployment Geography
Global

## Use Case
Primarily intended for surgical robotics researchers, healthcare AI developers, academic institutions, and surgical robotics companies exploring surgical world modeling, closed-loop surgical policy evaluation, imitation learning, inverse-dynamics action labeling of surgical video, and synthetic data generation. It can be served directly in any of its three modes (including through the HTTP policy server) or used as the initialization for fine-tuning on a single mode or on new surgical robot data.

## Release Date
- **GitHub:** 10/20/2026 via https://github.com/NVIDIA-Medtech/Cosmos3-H-Embodied-Nano
- **Huggingface:** 10/20/2026 via https://huggingface.co/nvidia/Cosmos3-H-Embodied-Nano

## Reference(s)
NVIDIA Cosmos Team. (2026). Cosmos 3: Omnimodal World Models for physical AI [Technical report]. NVIDIA. https://research.nvidia.com/labs/cosmos-lab/cosmos3/technical-report.pdf

```bibtex
@techreport{nvidia2026cosmos3,
  title  = {Cosmos 3: Omnimodal World Models for physical AI},
  author = {{NVIDIA Cosmos Team}},
  year   = {2026},
  url    = {https://research.nvidia.com/labs/cosmos-lab/cosmos3/technical-report.pdf}
}
```

Source code: [NVIDIA-Medtech/Cosmos3-H-Embodied-Nano](https://github.com/NVIDIA-Medtech/Cosmos3-H-Embodied-Nano) (plugin package `cosmos3_h_embodied` on [cosmos-framework](https://github.com/NVIDIA/cosmos-framework))

Base model: [nvidia/Cosmos3-Nano](https://huggingface.co/nvidia/Cosmos3-Nano)

Dataset: [nvidia/PhysicalAI-Robotics-Open-H-Embodiment](https://huggingface.co/datasets/nvidia/PhysicalAI-Robotics-Open-H-Embodiment)

Cosmos-H-Surgical-Simulator (forward-dynamics-only predecessor model): [nvidia/Cosmos-H-Surgical-Simulator](https://huggingface.co/nvidia/Cosmos-H-Surgical-Simulator), described in: Ali, A., Bai, J., Bala, M., Balaji, Y., Blakeman, A., Cai, T., Cao, J., Cao, T., Cha, E., Chao, Y.-W., Chattopadhyay, P., Chen, M., Chen, Y., Cheng, S., Cui, Y., Diamond, J., Ding, Y., Fan, J., Fan, L., Feng, L., Ferroni, F., Fidler, S., Fu, X., Gao, R., Ge, Y., Gu, J., … Zhu, Y. (2025). World Simulation with Video Foundation Models for Physical AI (arXiv:2511.00062) [Preprint]. arXiv. https://doi.org/10.48550/arXiv.2511.00062

## Model Architecture
Architecture Type: Mixture-of-Transformers (MoT)
Network Architecture: Unified world foundation model that couples a Reasoner (vision-language) tower and a Generator (world-simulator / diffusion) tower which share multimodal attention over one interleaved sequence of video, action, and text tokens. Actions are consumed and (in inverse-dynamics / policy modes) predicted through dedicated, embodiment-specific action projections.

**Number of Model Parameters:** 16 billion (the official Cosmos3-Nano size; see [nvidia/Cosmos3-Nano](https://huggingface.co/nvidia/Cosmos3-Nano)). The Cosmos3-Nano MoT couples a Qwen3-VL-8B reasoning tower with a diffusion generation expert. Post-training updates the diffusion generation expert, the timestep embedder, the video-latent and action input/output projections, and the action modality embedding (approximately 7 billion parameters); the reasoning tower is frozen.

**This model was developed based on Cosmos3-Nano.**

Cosmos3-H-Embodied-Nano post-trains Cosmos3-Nano, a world foundation model whose backbone is a Qwen3-VL-8B reasoning tower plus a diffusion generation expert (a Mixture-of-Transformers that natively supports text2image, text2video, image2video, and the action modes forward dynamics, inverse dynamics, and policy). Video is tokenized in latent space with the Wan2.2 video tokenizer (spatial compression 16×, temporal compression 4×, 2×2 spatial patchification). Actions enter and exit the shared sequence through domain-aware linear projections: `action2llm` embeds the action vector into the model's token space, `llm2action` is the action-prediction head trained by the inverse-dynamics and policy modes, and a learned action modality embedding tags the action tokens. An embodiment ID (one of 32 slots) selects the action input and output projections for each robot.

The three modes are **not** separate models, they are different clean-vs-noised token masks over the one shared sequence:
- **Forward dynamics:** the first frame and the action tokens are clean conditioning; the model denoises the future video, i.e. p(video | frame₀, actions).
- **Inverse dynamics:** all video frames are clean conditioning; the model denoises the actions, i.e. p(actions | video).
- **Policy:** the first frame, the text and the action history are clean conditioning; the model denoises **both** future actions and video, i.e. p(actions, video | frame₀, text, action history).

Training mixes the three modes 0.4 / 0.2 / 0.4 (forward dynamics / inverse dynamics / policy). In all modes up to 16 past action steps, expressed in the current pose's frame, are given as clean conditioning (shorter at episode boundaries). Dataset families are mixed by rank: each GPU rank serves one family, with families allocated according to fixed mixture ratios.

**Action representation:** per arm and step, the end-effector pose relative to the current pose (translation as a world-frame offset, rotation in the current pose's frame as a 6D representation) and the gripper command, i.e. 20 values for a two-arm robot. Each dataset family is normalized with its own statistics (1st/99th percentiles mapped to [-1, 1], clipped at ±1.5). At the model input, every action is zero-padded to `max_action_dim` = 64 channels, and the padded channels are masked (`action_channel_masking`).

## Input
- **Input Type(s):** Image (surgical video frame) or video, a stream of numerical action vectors (future actions and/or up to 16 past actions), and Text (task instruction)
- **Input Format(s):** Red, Green, Blue (RGB) frames, numeric vector, text string
- **Input Parameters:** Image: Two-Dimensional (2D) video frames; Video: Three-Dimensional (3D); Vector: stream of action vectors (20 values per step for a two-arm robot, zero-padded to 64 at the model input; 24 future steps per clip plus up to 16 past steps); Text: One-Dimensional (1D) prompt
- **Other Properties Related to Input:**
  - **Which inputs are used depends on the mode.** Forward dynamics conditions on the first frame and the actions; inverse dynamics conditions on the observed video; policy conditions on the first frame, the text and the action history.
  - **Text:** the task instruction, prefixed with a short description of the robot and setting for each dataset.
  - **Resolution:** The model operates at the Cosmos3 256p resolution tier. Input frames are automatically resized (aspect ratio preserved) to the closest-aspect target of that tier (width × height): 320 × 192 (16:9), 320 × 256 (4:3), or 256 × 256 (1:1).
  - **Temporal window:** 2.4 s clips: 25 frames (1 context + 24) and 24 action steps at 10 Hz.
  - **Pre-processing:** Action values are normalized with precomputed per-dataset-family statistics (1st/99th percentiles to [-1, 1]); the embodiment ID selects the action projections.

## Output
- **Output Type(s):** Depends on mode, a sequence of generated video frames (forward dynamics / policy) and/or a sequence of predicted action vectors (inverse dynamics / policy)
- **Output Format:** mp4 / RGB frames; numeric action vectors
- **Output Parameters:** Video: Three-Dimensional (3D); Action: One-Dimensional (1D) per timestep
- **Other Properties Related to Output:**
  - Each prediction covers one 2.4 s clip: 24 future frames and/or 24 action steps at 10 Hz.
  - The HTTP policy server takes the current frame, the caption and up to 16 past (normalized) actions and returns 24 denormalized actions together with the predicted video.
  - No additional post-processing is strictly required.

Our AI models are designed and/or optimized to run on NVIDIA GPU-accelerated systems. By leveraging NVIDIA’s hardware (e.g. GPU cores) and software frameworks (e.g., CUDA libraries), the model achieves faster training and inference times compared to CPU-only solutions.

## Software Integration
**Runtime Engine(s):**
- [cosmos-framework](https://github.com/NVIDIA/cosmos-framework) — the Cosmos3 training and inference runtime (unmodified; validated at revision `7cfaf78`).
- [Cosmos3-H-Embodied-Nano](https://github.com/NVIDIA-Medtech/Cosmos3-H-Embodied-Nano) plugin package `cosmos3_h_embodied` — Open-H data loading with action history, the training recipe of the released checkpoint, dataset-driven evaluation, and an HTTP policy server.

**Supported Hardware Microarchitecture Compatibility:**
- NVIDIA Ampere
- NVIDIA Blackwell
- NVIDIA Hopper

Note: Only BF16 (Brain Floating Point 16) precision is tested. Other precisions like FP16 (16-bit floating point) or FP32 (32-bit floating point) are not officially supported.

**Preferred/Supported Operating System(s):**
Linux (We have not tested on other operating systems.)

The integration of foundation and fine-tuned models into AI systems requires additional testing using use-case-specific data to ensure safe and effective deployment. Following the V-model methodology, iterative testing and validation at both unit and system levels are essential to mitigate risks, meet technical and functional requirements, and ensure compliance with safety and ethical standards before deployment.

## Model Version(s)
**v1.0 (based on Cosmos3-Nano; post-trained on the Open-H-Embodiment surgical mixture for 50,000 iterations jointly on forward dynamics, inverse dynamics and policy (mixed 0.4 / 0.2 / 0.4); up to 16 past actions as conditioning; 256-pixel resolution tier)**

Released as `c3-h-e-n_model_bf16.safetensors` (the network weights in BF16), which `tools/convert_checkpoint_to_dcp.py` converts to a distributed checkpoint (DCP) for cosmos-framework.

Developers may integrate the model by (a) using it directly in a chosen mode: forward dynamics to generate surgical video from a first frame and actions, inverse dynamics to label actions from video, or policy to produce actions and video from a frame, text and action history (for example through the HTTP policy server), or (b) fine-tuning it on their own LeRobot-format data, on a single mode or on all three.

## Training, Testing, and Evaluation Datasets

**Initialization:** NVIDIA-pretrained Cosmos3-Nano world foundation model.

**Post-training data:** Open-H-Embodiment community-generated surgical robotics dataset.

- **Mixture:** 15 dataset families with 55 dataset roots, sampled by fixed per-family mixture ratios. Families (approximate share of the mixture): JHU dVRK (≈32%), CMR Versius clinical procedures: cholecystectomy, hysterectomy, inguinal hernia, prostatectomy (≈20%), Óbuda dVRK (≈9%), Rob Surgical (≈8%), Turin MITIC (≈7%), Stanford dVRK (≈7%), Hamlyn dVRK (≈4%), USTC dVRK (≈4%), JHU SutureBot monocular (≈4%), UCSD dVRK (≈2%), UC Berkeley dVRK (≈2%), JHU STAR imitation learning (≈1%), JHU SMARTS (≈1%), TU Dresden TUNDRA (<1%), and CMR Versius dry-box peg transfer (<0.1%).
- **Public availability:** 11 of the 15 families are on Hugging Face. Four families (USTC dVRK, JHU SutureBot monocular, JHU STAR imitation learning, CMR Versius dry-box peg transfer) and three of the JHU dVRK roots are not public; some captions and one video stream were also never published.
- **Dataset partition:** ≈95% training, ≈5% held-out validation.

### Training Dataset
- **Data Modality** [Video] [Kinematics] [Text]
- **Video Size** [Less than 10,000 Hours]
- **Kinematics Size** [Less than 10,000 Hours]
- **Text Size** [Less than 10,000 Hours]
- **Link:** [Open-H multi-embodiment surgical robotics dataset](https://huggingface.co/datasets/nvidia/PhysicalAI-Robotics-Open-H-Embodiment) (public part; see above for the non-public families).
- **Data Collection Method:** Manually-Collected
- **Labeling Method:** Manually-Labeled
- **Properties:**
  - Human experts teleoperated the surgical robotic arms; motion was recorded as synchronized video and kinematics pairs. Each clip additionally carries a text language annotation (task instruction) used as conditioning.
  - The Text modality consists of per-clip language annotations time-synchronized with the video and kinematics demonstrations, so its size is reported on the same duration bucket as the aligned video/kinematics rather than a token count (Open-H describes the corpus as synchronized demonstrations "spanning language annotations, video observations, and kinematic trajectories"). It is not a standalone free-text corpus.
  - Multi-institution, multi-embodiment surgical coverage; each dataset family has its own action normalization statistics and embodiment ID.

### Testing Dataset
- **Link:** Held-out ≈5% validation split of the Open-H-Embodiment surgical mixture.
- **Data Collection Method:** Manually-Collected
- **Labeling Method:** Manually-Labeled
- **Properties:**
  - Frames and episodes never seen during training, held out for evaluation.

### Evaluation Dataset
- **Link:** Held-out ≈5% validation split of the Open-H-Embodiment surgical mixture (frames/episodes never seen during training).
- **Data Collection Method:** Manually-Collected
- **Labeling Method:** Manually-Labeled
- **Properties:**
  - Held-out episodes used for per-family, per-mode evaluation.

**Key performance:** The model is evaluated per dataset family on the held-out validation split in all three modes: generated-video quality as PSNR against ground truth (forward dynamics and policy) and action accuracy as mean squared error in normalized action space (inverse dynamics and policy).

## Quantitative Evaluation

All results are on data held out from training. The protocol, metric definitions, per-dataset tables and commands to reproduce them are in the [evaluation document](https://github.com/NVIDIA-Medtech/Cosmos3-H-Embodied-Nano/blob/main/cosmos3_h_embodied/README_EVALUATION.md).

### All three modes

One model, three modes, each run on 2.4 s clips (25 frames, 24 actions) held out from training: 64 clips evenly spaced over the validation split of each of the 10 public dataset families with held-out episodes (640 clips). Action MSE is in normalized action space (each dimension mapped to [-1, 1]); the baseline predicts the mean recorded action chunk of the family for every clip. The policy is sampled 4 times per clip (mean, and best of 4 as in the Cosmos 3 paper).

| Mode | Metric | All (640 clips) | dVRK (9 families) | CMR Versius |
|:---|:---|:---:|:---:|:---:|
| Forward dynamics | Video PSNR ↑ | 26.1 | 26.9 | 18.6 |
| Inverse dynamics | Action MSE ↓ | 0.009 | 0.008 | 0.019 |
| Policy | Action MSE ↓, mean / best of 4 | 0.052 / 0.033 | 0.046 / 0.031 | 0.101 / 0.056 |
| | Video PSNR ↑, mean / best of 4 | 23.0 / 23.9 | 23.7 / 24.6 | 16.7 / 17.8 |
| Baseline (mean trajectory) | Action MSE ↓ | 0.075 | 0.073 | 0.091 |

- Inverse dynamics is 8.6× below the baseline, on every family, although it got only 20% of the training samples (forward dynamics and policy 40% each).
- The policy's mean is 31% below the baseline, its best of 4 56%; on CMR Versius the mean is above the baseline, the best of 4 below.
- The video generated with the recorded actions is 3.1 dB closer to the recording than the video generated with the policy's own actions (9 of 10 families), consistent with the generated video following the actions it is conditioned on.

### Forward dynamics compared with Cosmos-H-Surgical-Simulator

Cosmos-H-Surgical-Simulator is a forward-dynamics model, so only this mode can be compared. Both released checkpoints are rolled out autoregressively from the same frames of episodes held out by both models, with the recorded actions and each model's released inference settings, 2 seeds per episode, and scored against the same recorded frames at 176 rows (this model's output height). Bold: significantly better (paired test p < 0.05, or ≥ 95% of bootstrap resamples for FID/FVD).

| Domain | Metric | Cosmos3-H-Embodied-Nano | Cosmos-H-Surgical-Simulator |
|:---|:---|:---:|:---:|
| dVRK, 4.8 s (17 episodes, 5 families) | FDS (L1) ↓ | **0.049** | 0.061 |
| | SSIM ↑ | **0.818** | 0.784 |
| | PSNR ↑ | **26.53** | 24.52 |
| | Dynamic PSNR ↑ | **21.08** | 19.33 |
| | FID ↓ / FVD ↓ | 43.9 / 173 | 44.5 / 191 |
| CMR Versius, 7.2 s (64 episodes, 4 procedures) | FDS (L1) ↓ | 0.193 | 0.191 |
| | SSIM ↑ | 0.369 | **0.377** |
| | PSNR ↑ | 17.17 | 17.14 |
| | Dynamic PSNR ↑ | 14.91 | 14.85 |
| | GATC ↑ | **0.488** | 0.441 |
| | TCD (px) ↓ | 74.1 | **66.4** |
| | FID ↓ | **44.3** | 55.4 |
| | FVD ↓ | 274 | **225** |
| CMR Versius, 31.2 s (22 episodes) | FID ↓ at 0–6 s / 24–31 s | **64** / 218 | 71 / **159** |
| | FVD ↓ at 0–6 s / 24–31 s | 501 / 1765 | **428** / **961** |
| | PSNR ↑ at 24–31 s | 13.24 | 13.12 |
| | GATC ↑ / TCD (px) ↓, whole rollout | 0.217 / 128 | 0.233 / **99** |

- **dVRK:** better on every per-pixel metric (dynamic PSNR +1.75 dB, better in 88% of the rollouts); FID and FVD on par.
- **CMR Versius, 7.2 s:** per-pixel metrics on par; tools look more like the recorded ones (GATC +0.047) and single frames are more realistic (FID −11), while Cosmos-H-Surgical-Simulator's motion is closer to the recording (FVD) and the segmenter finds more of its tools (TCD).
- **Long rollouts (limitation):** up to about 6 s the models are on par; after that this model's frames get blurrier and Cosmos-H-Surgical-Simulator degrades more slowly (FID, FVD, TCD). This model was trained on single 2.4 s clips.
- Pixel and distribution metrics are dominated by static tissue and do not measure directly how well the generated instruments follow the commanded actions.

**Metrics:**
- **Video PSNR**: peak signal-to-noise ratio between generated and recorded frames (higher is better).
- **Action MSE**: mean squared error of the 24 predicted actions in normalized action space, each dimension mapped to [-1, 1] by the family's 1st/99th percentiles (lower is better).
- **FDS (L1)**: Frame Decay Score - mean per-frame L1 distance between generated and recorded frames in [-1, 1] (lower is better).
- **Dynamic PSNR**: PSNR over the 20% of pixels that change most in the recorded video (higher is better).
- **GATC**: Ground-truth Anchored Tool Consistency - correlation of the tool regions (Medical-SAM3 masks) of generated and recorded frames, weighted by tool presence (higher is better).
- **TCD**: Tool Centroid Distance - distance in pixels between matched tool centroids of generated and recorded frames, unmatched tools penalized (lower is better).
- **FID / FVD**: Fréchet distance between Inception-v3 frame / I3D clip features of generated and recorded videos (lower is better).

## Inference
**Acceleration Engine:** [PyTorch](https://pytorch.org/); distributed inference with FSDP sharding and BF16, via cosmos-framework.

**Test Hardware:** NVIDIA Hopper H100. Also runs on other NVIDIA Ampere and NVIDIA Blackwell-class GPUs.

**Usage:**
- See the [Cosmos3-H-Embodied-Nano repository](https://github.com/NVIDIA-Medtech/Cosmos3-H-Embodied-Nano) for installation on [cosmos-framework](https://github.com/NVIDIA/cosmos-framework), checkpoint conversion, evaluation, the HTTP policy server, and fine-tuning on your own data.
- Released weights: [nvidia/Cosmos3-H-Embodied-Nano](https://huggingface.co/nvidia/Cosmos3-H-Embodied-Nano) (`c3-h-e-n_model_bf16.safetensors`).

## Ethical Considerations
NVIDIA believes Trustworthy AI is a shared responsibility and we have established policies and practices to enable development for a wide array of AI applications.  When downloaded or used in accordance with our terms of service, developers should work with their internal model team to ensure this model meets requirements for the relevant industry and use case and addresses unforeseen product misuse.

Please make sure you have proper rights and permissions for all input image and video content; if image or video includes people, personal health information, or intellectual property, the image or video generated will not blur or maintain proportions of image subjects included.

For more detailed information on ethical considerations for this model, please see the Model Card++ for Bias, Explainability, Safety & Security, and Privacy Subcards.

Please report model quality, risk, security vulnerabilities or NVIDIA AI Concerns [here](https://www.nvidia.com/en-us/support/submit-security-vulnerability/).
