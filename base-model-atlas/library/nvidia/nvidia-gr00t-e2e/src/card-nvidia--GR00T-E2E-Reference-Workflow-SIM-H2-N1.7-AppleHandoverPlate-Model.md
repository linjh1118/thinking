---
license: other
license_name: nvidia-open-model-license
license_link: LICENSE
library_name: gr00t
base_model: nvidia/GR00T-N1.7-3B
datasets:
- nvidia/GR00T-E2E-Reference-Workflow-SIM-H2-N1.7-AppleHandoverPlate-Dataset
tags:
- robotics
- gr00t-n1.7
- isaac-lab
- simulation
- unitree-h2
- apple-handover
---

**Transparency cards:** [Overview](overview.md) · [Bias](bias.md) · [Explainability](explainability.md) · [Privacy](privacy.md) · [Safety](safety.md)

# Model Overview

### Description:

`GR00T-E2E-Reference-Workflow-SIM-H2-N1.7-AppleHandoverPlate-Model` is a fine-tuned NVIDIA Isaac GR00T N1.7 model for a simulated Unitree H2 Plus humanoid with Sharpa hands: pick up an apple with the left hand, transfer it to the right hand, and release it onto a plate.<br><br>
Isaac `GR00T N1.7-3B` is the medium-sized version of the model, built using pretrained vision and language encoders. It uses a flow-matching action transformer to model a chunk of actions conditioned on vision, language, and proprioception.<br><br>
This model was developed and built wholly by NVIDIA.

This model is ready for commercial or non-commercial use.

### License/Terms of Use:

NVIDIA Open Model License (https://www.nvidia.com/en-us/agreements/enterprise-software/nvidia-open-model-license/)

### Deployment Geography:

Global.

### Use Case: 

Robotics researchers and developers can train and evaluate policies for H2 Plus bimanual apple pick, handover and placement in simulation.

### Release Date:

Hugging Face 10/01/2026 via [nvidia/GR00T-E2E-Reference-Workflow-SIM-H2-N1.7-AppleHandoverPlate-Model](https://huggingface.co/nvidia/GR00T-E2E-Reference-Workflow-SIM-H2-N1.7-AppleHandoverPlate-Model)

## References(s):

H2 Plus workflow: https://github.com/nvidia-isaac/GR00T-E2E-Reference-Workflow/blob/release/v0.2/docs/workflows/h2-pick-handover-place.md

GR00T N1 White Paper: "[GR00T N1: An Open Foundation Model for Generalist Humanoid Robots](https://arxiv.org/abs/2503.14734)." (2025).

Liu, Xingchao, and Chengyue Gong. "[Flow Straight and Fast: Learning to Generate and Transfer Data with Rectified Flow](https://arxiv.org/abs/2209.03003)." The Eleventh International Conference on Learning Representations.

Flow Matching Policy: Black, Kevin, et al. "[π0: A Vision-Language-Action Flow Model for General Robot Control](https://arxiv.org/abs/2410.24164)." arXiv preprint (2024).


## Model Architecture:

**Architecture Type:** Transformer

GR00T N1.7 uses a Cosmos-Reason2-2B vision-language backbone based on the Qwen3-VL architecture, replacing the Eagle backbone used in N1.6. It uses a flow-matching action transformer to model chunks of actions conditioned on vision, language, and proprioception.

RGB camera frames and language instructions are encoded by the Cosmos-Reason2-2B vision-language backbone. Image preprocessing follows the checkpoint's released processor configuration. Robot proprioception is encoded using a multi-layer perceptron (MLP) indexed by the embodiment ID. To handle variable-dimension proprioception, inputs are padded to a configurable max length before feeding into the MLP.

Actions are encoded and velocity predictions are decoded by an MLP, one per unique embodiment. The flow-matching transformer is implemented as a diffusion transformer (DiT), with diffusion-step conditioning implemented using adaptive layer normalization (AdaLN).

**Network Architecture:** GR00T N1.7 with a Cosmos-Reason2-2B vision-language backbone and a flow-matching Diffusion Transformer (DiT) action head.

![image/png](https://github.com/NVIDIA/Isaac-GR00T/blob/main/media/model-architecture.png?raw=true)
The schematic diagram is shown in the illustration above.

**Number of Model Parameters:**
3B



## Input(s):

**Input Type(s):** Image, Tabular, Text.

**Input Format(s):**
* Vision: RGB uint8 image frames from robot cameras<br>
* State: Floating-point tensor<br>
* Language Instruction: String<br>
* Embodiment ID: Integer indicating which of the training embodiments is observed<br>

**Input Parameters:**
* Vision: Two-Dimensional (2D) - Red, Green, Blue (RGB) image<br>
* State: One-Dimensional (1D) - Floating number vector<br>
* Language Instruction: One-Dimensional (1D) - String<br>
* Embodiment ID: One-Dimensional (1D) - Integer<br>

**Other Properties Related to Input:** Head-camera RGB video feed, uint8 format, no alpha channel, 8-bit color depth. Proprioceptive state is a 75-dimensional joint state vector. The checkpoint model and processor configurations specify a 256 x 256 image target, a 230 x 230 crop setting, and normalization. Use the released processor configuration.

## Output(s)

**Output Type(s):** Tabular
**Output Format(s):** Continuous floating-point action vectors.
**Output Parameters:** Two-Dimensional (2D) <br>
**Other Properties Related to Output:** 61-dimensional policy action per timestep (14 arm + 44 hand + 3 navigation-command values), with an action horizon of 40. The stored 75-joint dataset target and the policy's 61-dimensional action are not interchangeable.

Our AI models are designed and/or optimized to run on NVIDIA GPU-accelerated systems. By leveraging NVIDIA's hardware (e.g. GPU cores) and software frameworks (e.g., CUDA libraries), the model achieves faster training and inference times compared to CPU-only solutions. <br>

## Software Integration:

**Runtime Engine(s):** PyTorch (safetensors checkpoint)

**Supported Hardware Microarchitecture Compatibility:**
* NVIDIA Ampere
* NVIDIA Blackwell
* NVIDIA Hopper
* NVIDIA Jetson
* NVIDIA Lovelace

**Supported Operating System(s):** Linux

The integration of foundation and fine-tuned models into AI systems requires additional testing using use-case-specific data to ensure safe and effective deployment. Following the V-model methodology, iterative testing and validation at both unit and system levels are essential to mitigate risks, meet technical and functional requirements, and ensure compliance with safety and ethical standards before deployment.

## Model Version(s):

GR00T-E2E-Reference-Workflow-SIM-H2-N1.7-AppleHandoverPlate-Model v0.2, checkpoint-10000.

The checkpoint integrates as a PyTorch policy in the H2 Plus simulation workflow, using the released processor configuration and normalization to map camera images, robot state and the task instruction to the documented 61-dimensional action chunks.

This is an inference checkpoint release: optimizer, scheduler, RNG, and trainer resume state are intentionally not included. Use the Isaac GR00T checkout at revision `4b1dca9d88d2a0b9ea5a65aa61c82ff89f5c4f0e`; the backbone identifier is `nvidia/Cosmos-Reason2-2B`, and its pinned revision is recorded in `training_provenance.json`.


## Training, Testing, and Evaluation Datasets:

### Training Dataset:

Trained with dataset [nvidia/GR00T-E2E-Reference-Workflow-SIM-H2-N1.7-AppleHandoverPlate-Dataset](https://huggingface.co/datasets/nvidia/GR00T-E2E-Reference-Workflow-SIM-H2-N1.7-AppleHandoverPlate-Dataset)

**Data Modality:** Image, Video, Text, Other: robot state and actions.

**Training Data Size:** 1,000 generated demonstrations; seed demonstrations are not extra training episodes.

**Video Training Data Size:** [Less than 10,000 Hours]

**Image Training Data Size:** [1 Million to 1 Billion Images]

**Text Training Data Size:** [Less than a Billion Tokens]

**Non-Audio, Image, Text Training Data Size:** 1,178,888 time-indexed records in the generated LeRobot dataset.

**Data Collection Method by dataset:** [Hybrid: Manually-Collected, Synthetic]

The 1,000 training demonstrations were generated by Isaac AutoData from 10 human teleoperation seed demonstrations collected in simulation using an XR headset. The 10 seeds were not added as 10 extra training episodes.

**Labeling Method by dataset:** [Hybrid: Manually-Labeled, Automated]

Seed demonstration labels (task description) were human-assigned; generated demonstrations inherit the same task label automatically from their seed via Isaac AutoData.

**Properties:** 1,000 synthetic demonstrations with 1,178,888 time-indexed records, containing RGB camera images/video, numerical robot states/actions and the English task instruction "move the apple to the plate", inherited from human-labeled simulation seeds.

10,000 training steps; batch size 32; gradient accumulation 1; learning rate `1e-4`. One NVIDIA RTX 5880 Ada 48 GB GPU. Final reported training loss: `0.0138`. Visual encoder and LLM frozen; projector and diffusion components trained.

### Testing Dataset:

**Data Collection Method by dataset:** [Not Applicable]

**Labeling Method by dataset:** [Not Applicable]

**Properties:** No separate held-out testing dataset was supplied (0 held-out demonstration episodes); all 1,000 generated demonstrations are in the training split. The data consists of synthetic simulation camera images/video, numerical robot states/actions and the English task instruction "move the apple to the plate". Closed-loop simulation evaluation is described separately below.

### Evaluation Dataset:

**Data Modality:** Other: Robot Simulation

**Data Collection Method by dataset:** [Synthetic]

Simulated H2 Plus robot

**Labeling Method by dataset:** [Not Applicable]

**Properties:** 500 synthetic H2 Plus simulation episodes of apple handover and plate placement, evaluated in five 100-episode batches with seeds 5301-5305. Each episode has a 30-second simulated-time budget at 100 Hz control. Apple XY reset jitter is +/- 0.02 m; the plate is fixed. Success requires settled placement on the plate with hands clear. The policy is conditioned on the English instruction "move the apple to the plate"; simulation outcomes are numerical success/failure labels.

**Benchmark Score:** **369 / 500 successes (73.8%)**, 131 failures, and zero runtime errors, over 500 simulation episodes (five independent 100-episode batches, seeds 5301–5305, scoring 77%, 73%, 76%, 73%, and 70% respectively). Each episode had a 30-second simulated-time budget at 100 Hz control. Apple XY reset jitter was +/- 0.02 m; the plate was fixed. Success requires final settled placement on the plate with hands clear, not merely completing an intermediate grasp or handover milestone. These results do not establish real-robot safety or broad out-of-distribution robustness. See the machine-readable evaluation summary at `evaluation/summary.json` in the model repository.

## Inference:

**Acceleration Engine:** PyTorch

**Test Hardware Set-Up (GPU Architecture, Model):** 
* NVIDIA Ada Lovelace RTX 5880

### Resources

* NVIDIA Isaac GR00T repository: https://github.com/NVIDIA/Isaac-GR00T
* Base model: https://huggingface.co/nvidia/GR00T-N1.7-3B
* GR00T N1.7 collection: https://huggingface.co/collections/nvidia/gr00t-n17
* Paper: https://arxiv.org/abs/2503.14734
* Blogpost: https://nvidianews.nvidia.com/news/foundation-model-isaac-robotics-platform
* Fine-tuning guide: https://github.com/NVIDIA/Isaac-GR00T/blob/main/getting_started/finetune_new_embodiment.md

## Ethical Considerations:

NVIDIA believes Trustworthy AI is a shared responsibility and we have established policies and practices to enable development for a wide array of AI applications.  Developers should work with their internal model team to ensure this model meets requirements for the relevant industry and use case and addresses unforeseen product misuse.  

Please make sure you have proper rights and permissions for all input image and video content; if image or video includes people, personal health information, or intellectual property, the image or video generated will not blur or maintain proportions of image subjects included. 

For more detailed information on ethical considerations for this model, please see the [Bias](bias.md), [Explainability](explainability.md), [Safety & Security](safety.md), and [Privacy](privacy.md) subcards.  

Please report model quality, risk, security vulnerabilities or NVIDIA AI Concerns [here](https://www.nvidia.com/en-us/support/submit-security-vulnerability/).

## Notices

Licensed by NVIDIA Corporation under the NVIDIA Open Model License

Built on NVIDIA Cosmos

See [LICENSE](LICENSE) and [NOTICE](NOTICE).
