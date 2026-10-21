---
license: other
license_name: nvidia-open-model-license
license_link: >-
  https://www.nvidia.com/en-us/agreements/enterprise-software/nvidia-open-model-license/
pipeline_tag: image-to-video
tags:
- simulation
- surgical-robotics
- video-generation
- real-time
- interactive
- autoregressive
- policy-evaluation
- vla-evaluation
- healthcare-robotics
- world-model
base_model:
- nvidia/Cosmos3-Nano
- nvidia/Cosmos3-H-Embodied-Nano
datasets:
- nvidia/PhysicalAI-Robotics-Open-H-Embodiment
library_name: nv-medtech
---

<div align="center">
  <div align="center">
  <a href="https://github.com/isaac-for-healthcare/Cosmos3-H-Dreams">
    <img src="https://img.shields.io/badge/GitHub-Cosmos3--H--Dreams-grey?logo=GitHub" alt="Runtime Badge">
  </a>
  <a href="https://huggingface.co/nvidia/Cosmos3-H-Embodied-Nano">
    <img src="https://img.shields.io/badge/Model-Cosmos3--H--Embodied--Nano-blue?logo=huggingface" alt="Teacher Model Badge">
  </a>
  <a href="https://huggingface.co/datasets/nvidia/PhysicalAI-Robotics-Open-H-Embodiment">
    <img src="https://img.shields.io/badge/Dataset-Open--H--Embodiment-brightgreen?logo=huggingface" alt="Dataset Badge">
  </a>
</div>
</div>

# Cosmos3-H-Dreams

## Description
Cosmos3-H-Dreams is a real-time, action-conditioned surgical world model for the CMR Surgical Versius robotic system. It is fine-tuned on CMR Surgical Versius clinical cholecystectomy data and distilled into a causal, few-step student for interactive, streaming video generation. Given a single endoscopic camera frame, a short history of recent robot commands and a stream of future kinematic and control commands for both arms, the model generates the resulting endoscopic video autoregressively.

The model is intended for surgical robotics policy evaluation in simulation, interactive (teleoperated) world-model exploration and synthetic data generation for robotic cholecystectomy, before transitioning to a physical system.

Cosmos3-H-Dreams is the successor of Cosmos-H-Dreams ([arXiv:2608.24199](https://arxiv.org/abs/2608.24199)), which was based on Cosmos-Predict2.5. Cosmos3-H-Dreams is based on Cosmos3-H-Embodied-Nano, which is in turn based on the NVIDIA Cosmos3-Nano world foundation model for physical AI.

This model is ready for commercial or non-commercial use.

## License/Terms of Use
GOVERNING DOWNLOAD TERMS: Use of the model is governed by the [NVIDIA Open Model License Agreement](https://www.nvidia.com/en-us/agreements/enterprise-software/nvidia-open-model-license/).

Additional Information: Use of the [Cosmos3-H-Embodied-Nano](https://huggingface.co/nvidia/Cosmos3-H-Embodied-Nano) base model is governed by the [NVIDIA Open Model License Agreement](https://www.nvidia.com/en-us/agreements/enterprise-software/nvidia-open-model-license/).

## Deployment Geography
Global

## Use Case
Primarily intended for surgical robotics researchers, healthcare AI developers, academic institutions and surgical robotics companies exploring real-time surgical world models, surgical robotics policy evaluation and synthetic data generation for the CMR Surgical Versius system.

## Release Date
- **GitHub:** 10/20/2026 via https://github.com/isaac-for-healthcare/Cosmos3-H-Dreams
- **Huggingface:** 10/20/2026 via https://huggingface.co/nvidia/Cosmos3-H-Dreams


## Reference(s)
Cosmos-H-Dreams (predecessor model): [arXiv:2608.24199](https://arxiv.org/abs/2608.24199)

Direct base model: [nvidia/Cosmos3-H-Embodied-Nano](https://huggingface.co/nvidia/Cosmos3-H-Embodied-Nano)

Base model of Cosmos3-H-Embodied-Nano: [nvidia/Cosmos3-Nano](https://huggingface.co/nvidia/Cosmos3-Nano)

Self-Forcing (causal video diffusion distillation): Huang, X., Li, Z., He, G., Zhou, M., Shechtman, E. (2025). Self Forcing: Bridging the Train-Test Gap in Autoregressive Video Diffusion (arXiv:2506.08009) [Preprint]. arXiv. https://arxiv.org/abs/2506.08009

Distribution Matching Distillation: Yin, T., Gharbi, M., Park, T., Zhang, R., Shechtman, E., Durand, F., Freeman, W. T. (2024). Improved Distribution Matching Distillation for Fast Image Synthesis (arXiv:2405.14867) [Preprint]. arXiv. https://arxiv.org/abs/2405.14867

## Model Architecture
Architecture Type: Mixture-of-Transformers (MoT)
Network Architecture: Cosmos3-Nano unified Mixture-of-Transformers (a Qwen3-VL-8B-Instruct reasoning tower plus a latent-diffusion generation expert with shared multimodal attention), inherited through Cosmos3-H-Embodied-Nano, operating on Wan2.2 VAE latents (4x temporal, 16x16 spatial compression), with action embedding/projection layers for kinematic conditioning; distilled from a bidirectional teacher into a block-causal, 4-step autoregressive student with a KV cache.

**This model was developed based on Cosmos3-H-Embodied-Nano** (which is based on Cosmos3-Nano).

**Number of model parameters:** ~1.5 × 10^10 (15.17B)

Cosmos3-H-Dreams was produced in three phases:
1. **Initialization from Cosmos3-H-Embodied-Nano:** Cosmos3-H-Embodied-Nano is a Cosmos3-Nano action-conditioned checkpoint post-trained on the Open-H-Embodiment dataset for multiple surgical robot embodiments, with up to 16 past action transitions as clean action history. It provides the initialization.
2. **CMR cholecystectomy teacher fine-tuning:** The action interface for the CMR Versius embodiment (embodiment domain 25 of 32) was extended from 20 to 28 dimensions per time step by adding electrosurgical energy and thumbstick controls for both arms. Pretrained pose/jaw weights were preserved and the new control inputs were zero-initialized. A bidirectional teacher was fine-tuned on Versius cholecystectomy data first with a 24-frame horizon (2,000 iterations), then with a 72-frame horizon (4,400 iterations).
3. **Real-time distillation:** The bidirectional 72-frame teacher (35 sampling steps) was distilled into a block-causal student using causal teacher forcing (1,000 iterations), followed by Self-Forcing with distribution-matching distillation (300 iterations) against the fixed bidirectional teacher. The resulting student generates video autoregressively with a KV cache and 4 denoising steps per latent frame.

At inference, the conditioning frame and the optional action history (up to 16 transitions, 1.6 s) are prefilled into the KV cache once. Each subsequent latent frame consumes the next 4 future action vectors (0.4 s at 10 Hz) and produces 4 new video frames, enabling streaming rollout.

## Input
- **Input Type(s):** Image (camera frame), numerical action vectors (future time steps)
- **Input Format(s):** Red, Green, Blue (RGB) frame, numeric vectors
- **Input Parameters:** Image: Two-Dimensional (2D) image frame; Vector: One-Dimensional (1D) sequence of 28-dimensional (28D) action vectors (up to 16 history + 72 future per rollout window, at 10 Hz)
- **Other Properties Related to Input:**
- **Recommended resolution:** The model operates at 832x480. A 16:9-like aspect ratio is recommended; input frames are resized to the model resolution.
- **Action vector:** 14 dimensions per arm (left arm 0–13, right arm 14–27): anchor-relative translation (3), anchor-relative 6D rotation (6), jaw (1), electrosurgical energy active (1), thumbstick button (1), thumbstick axes (2). Internally zero-padded to 64 channels; CMR Versius embodiment domain 25.
- **Pre-processing:** Pose channels follow the anchor-relative hybrid action representation of Cosmos3-H-Embodied-Nano (history and future commands are expressed relative to the pose at the conditioning frame), including the recorded hand-motion scaling, and are quantile-normalized and clipped to ±1.5. Binary controls (energy, thumbstick button) are 0/1 and are set if pressed at any time within each 100 ms step. Thumbstick axes are scaled by training-set maximum absolute values. The action history is optional (0–16 steps) and must consist of genuine, contiguous past commands.

## Output
- **Output Type(s):** Video
- **Output Format:** mp4
- **Output Parameters:** Three-Dimensional (3D) (height, width, time)
- **Other Properties Related to Output:**
  - By default, the model generates 72 future frames at 10 Hz (7.2 s) at 832x480, streamed in chunks of 4 frames (0.4 s). Through a continued or re-anchored autoregressive loop, longer surgical trajectories can be generated.
  - No additional post-processing is strictly required.

Our AI models are designed and/or optimized to run on NVIDIA GPU-accelerated systems. By leveraging NVIDIA’s hardware (e.g. GPU cores) and software frameworks (e.g., CUDA libraries), the model achieves faster training and inference times compared to CPU-only solutions.

## Software Integration
**Runtime Engine(s):**
- [Cosmos3-H-Dreams](https://github.com/isaac-for-healthcare/Cosmos3-H-Dreams) — the streaming-inference library that serves the distilled student in real time (static-shape KV cache, `torch.compile` + CUDA Graphs, few-step diffusion, lightweight LightTAE decoder, and the keyboard/Quest serving stack).
- [Cosmos 3](https://github.com/nvidia/cosmos) — the training/base runtime. Not required for running Cosmos3-H-Dreams inference.

**Supported Hardware Microarchitecture Compatibility:**
- NVIDIA Blackwell
- NVIDIA Hopper

Note: Training and native inference were performed in BF16 (Brain Floating Point 16) mixed precision (weights are exported as FP32 (32-bit floating point)). Other precisions and quantization have not been qualified.

**Preferred/Supported Operating System(s):**
Linux (We have not tested on other operating systems.)

The integration of foundation and fine-tuned models into AI systems requires additional testing using use-case-specific data to ensure safe and effective deployment. Following the V-model methodology, iterative testing and validation at both unit and system levels are essential to mitigate risks, meet technical and functional requirements, and ensure compliance with safety and ethical standards before deployment.

## Model Version(s)
**v1.0 (based on Cosmos3-H-Embodied-Nano; fine-tuned on CMR Surgical Versius cholecystectomy data with exactly two instruments visible; 28D action space with H16 action history; distilled 4-step causal student)**

Developers may integrate the model into a real-time or offline evaluation system by providing an initial video frame, the recent command history and a stream of future Versius kinematic and control commands, for example from a surgical policy model or a teleoperation device.

## Training, Testing, and Evaluation Datasets

**Initialization data:** Open-H-Embodiment community-generated dataset (multiple surgical robot embodiments; used for the action-conditioned post-training of Cosmos3-H-Embodied-Nano, the checkpoint used for initialization).

**Fine-tuning and distillation data:** CMR Surgical Versius clinical cholecystectomy recordings (source: 4,792 episodes, ~17 million frames at 60 Hz, 1080p), subsampled to 10 Hz.

- **Sample selection:** Only samples with exactly two instruments visible in the endoscopic view were retained. In addition, both instruments had to be engaged for every native 60 Hz row of each history and future window, with consistent instrument linkage and hand-motion scaling. The canonical instrument pairing is a grasper (left arm) and a hook (right arm). Windows with active camera commands (thumbstick deflection above a fixed threshold) were excluded.
- **Total size (training):** 64 recordings, ~526 unique minutes of video (183,528 window starts for the 24-frame horizon; ~436 minutes / 106,820 window starts for the 72-frame horizon used in distillation). Windows overlap.
- **Dataset partition:** Episode-level split into training and held-out validation/test (~98% / ~2% of unique minutes); held-out recordings are ~10.6 minutes from 10 recordings.

### Training Dataset
- **Data Modality** [Video] [Kinematics]
- **Video Size** [Less than 10,000 Hours]
- **Kinematics Size** [Less than 10,000 Hours]
- **Link:** Proprietary (CMR Surgical Versius clinical data); Open-H-Embodiment dataset for initialization
- **Data Collection Method:** Manually-Collected
- **Labeling Method:** Hybrid: Automated, Manually-Labeled
- **Properties:**
  - Surgeons teleoperated the CMR Surgical Versius robot; procedures were recorded as synchronized endoscopic video and robot telemetry. Action labels are derived automatically from the robot telemetry; instrument visibility was labeled manually.
  - ~526 unique minutes from 64 recordings of robotic cholecystectomy, at 10 Hz, 832x480.
  - Each sample pairs one conditioning frame with up to 16 past and 24 or 72 future 28D action vectors and the corresponding future video frames.

### Testing Dataset
- **Link:** Held-out portion of the CMR Surgical Versius cholecystectomy data (not used for training).
- **Data Collection Method:** Manually-Collected
- **Labeling Method:** Hybrid: Automated, Manually-Labeled
- **Properties:**
  - **Data count:** 10 held-out recordings, ~10.6 unique minutes (around 6,400 frames at 10 Hz). Fixed evaluation panels drawn from these recordings contain 48 quality cases plus 12 action-control cases each.
  - **Modalities:** Video (endoscopic RGB, 832x480 at 10 Hz) and kinematics (time-synchronized 28D robot action vectors for both arms, derived from robot telemetry). No audio or text.
  - **Nature of content:** Intra-abdominal endoscopic video and robot telemetry from clinical robotic cholecystectomy procedures on human patients performed with the CMR Surgical Versius system. The content is health-related (surgical) data; it shows anatomy and surgical instruments, not faces or other identifying views of people.
  - **Linguistic characteristics:** Not applicable. The data contains no natural-language text or speech.

### Evaluation Dataset
- **Link:** Held-out portion of the CMR Surgical Versius cholecystectomy data, using cases never seen during training.
- **Data Collection Method:** Manually-Collected
- **Labeling Method:** Hybrid: Automated, Manually-Labeled
- **Properties:**
  - **Data count:** Two fixed held-out panels (exactly-two-instruments-visible and legacy selection), each with 48 quality cases plus 12 action-control cases (120 cases in total), each case being 1 conditioning frame plus 72 target frames (7.2 s); additional rotation probes (neutral, ±5° and ±15° tool rotations) and 30.4 s continuous rollouts were used for visual review.
  - **Modalities:** Video (endoscopic RGB, 832x480 at 10 Hz) and kinematics (time-synchronized 28D robot action vectors for both arms). No audio or text.
  - **Nature of content:** Intra-abdominal endoscopic video and robot telemetry from held-out clinical robotic cholecystectomy procedures on human patients (CMR Surgical Versius system). The content is health-related (surgical) data; it shows anatomy and surgical instruments, not faces or other identifying views of people.
  - **Linguistic characteristics:** Not applicable. The data contains no natural-language text or speech.

**Key performance:** The model generates surgical robotic video that responds to the kinematic and control commands of both arms, given an initial frame and an action trajectory recorded from a surgeon or produced by a surgical robotic policy model.


## Inference
**Acceleration Engine:** [PyTorch](https://pytorch.org/), [FlashDreams](https://github.com/NVIDIA/flashdreams)

**Test Hardware:** Real-time interactive serving validated on a single NVIDIA Blackwell RTX PRO 6000 (edge target) and on NVIDIA Blackwell DGX Spark; also runs on NVIDIA Hopper H100.

**Performance:**

| GPU | Resolution (W x H) | Diffusion steps | Inference FPS |
|---|---|---:|---:|
| RTX PRO 6000 Blackwell Workstation Edition | 832 x 480 | 4 | 30.0 |
| RTX PRO 6000 Blackwell Workstation Edition | 832 x 480 | 2 | 43.2 |
| RTX PRO 6000 Blackwell Max-Q Workstation Edition | 832 x 480 | 4 | 20.2 |
| RTX PRO 6000 Blackwell Max-Q Workstation Edition | 832 x 480 | 2 | 31.2 |
| DGX Spark | 512 x 288 | 2 | 16.9 |

Note: On DGX Spark, the model was served at a reduced 512 x 288 resolution; the native operating resolution is 832 x 480.

**Usage:**
- See [FlashDreams](https://github.com/flashdreams) for real-time streaming inference and the interactive keyboard/Meta Quest serving stack.
- See [Cosmos3-H-Embodied-Nano](https://huggingface.co/nvidia/Cosmos3-H-Embodied-Nano) and [Cosmos 3](https://github.com/nvidia/cosmos) for further details on the base models and training.


## Ethical Considerations
NVIDIA believes Trustworthy AI is a shared responsibility and we have established policies and practices to enable development for a wide array of AI applications.  When downloaded or used in accordance with our terms of service, developers should work with their internal model team to ensure this model meets requirements for the relevant industry and use case and addresses unforeseen product misuse.

Please make sure you have proper rights and permissions for all input image and video content; if image or video includes people, personal health information, or intellectual property, the image or video generated will not blur or maintain proportions of image subjects included.

For more detailed information on ethical considerations for this model, please see the Model Card++ for Bias, Explainability, Safety & Security, and Privacy Subcards.

Please report model quality, risk, security vulnerabilities or NVIDIA AI Concerns [here](https://www.nvidia.com/en-us/support/submit-security-vulnerability/).
