---
license: other
license_name: nvidia-open-model-license
license_link: LICENSE
library_name: gr00t
base_model: nvidia/GR00T-N1.7-3B
---

**Transparency cards:** [Overview](overview.md) · [Bias](bias.md) · [Explainability](explainability.md) · [Privacy](privacy.md) · [Safety](safety.md)

# Model Overview

### Description:

`GR00T-E2E-Reference-Workflow-SIM-G1-N1.7-AppletoPlate-Model` is a fine-tuned NVIDIA Isaac GR00T N1.7 model for a simulated Unitree G1 whole-body humanoid task: navigate to, pick up, and place an apple on a plate.<br><br>
Isaac `GR00T N1.7-3B` is the medium-sized version of the model, built using pretrained vision and language encoders. It uses a flow-matching action transformer to model a chunk of actions conditioned on vision, language, and proprioception.<br><br>
This model is ready for commercial or non-commercial use.

### License/Terms of Use:

NVIDIA Open Model License (https://www.nvidia.com/en-us/agreements/enterprise-software/nvidia-open-model-license/)

### Deployment Geography:

Global.

### Use Case: 

Robotics researchers and developers can evaluate and adapt a G1 apple-to-plate manipulation policy in the Isaac Lab simulation workflow.

### Release Date:

Hugging Face 10/01/2026 via [nvidia/GR00T-E2E-Reference-Workflow-SIM-G1-N1.7-AppletoPlate-Model](https://huggingface.co/nvidia/GR00T-E2E-Reference-Workflow-SIM-G1-N1.7-AppletoPlate-Model)

## References(s):

[Staged model](https://huggingface.co/nvidia/GR00T-E2E-Reference-Workflow-SIM-G1-N1.7-AppletoPlate-Model/tree/d3075997eb71095238324746f0507f5d707cd895)

[Staged dataset](https://huggingface.co/datasets/nvidia/GR00T-E2E-Reference-Workflow-SIM-G1-N1.7-AppletoPlate-Dataset/tree/36234f4b48dad27f218d8e29ec7710ad5a90b48c)

[G1 simulation workflow](https://github.com/nvidia-isaac/GR00T-E2E-Reference-Workflow/blob/release/v0.2/docs/workflows/g1-static-apple.md)

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
3,144,016,000 parameters reported by staging safetensors metadata (approximately 3B).



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

**Other Properties Related to Input:** 640x480 RGB egocentric camera feed, uint8 format, no alpha channel, 8-bit color depth. Proprioceptive state is a 31-dimensional vector (left/right arm, left/right hand, waist joints — legs excluded). The model configuration records a 256 x 256 target and 230 x 230 crop setting. The saved evaluation transform applies letterbox padding, resizing to a 256-pixel shortest edge, a 0.95 fractional center crop, and resizing again. Use the released processor configuration and normalization.

## Output(s)

**Output Type(s):** Tabular
**Output Format(s):** Continuous floating-point action vectors.
**Output Parameters:** Two-Dimensional (2D) <br>
**Other Properties Related to Output:** 35-dimensional action per timestep (the 31-dimensional arm/hand/waist state dims plus a 1-dimensional base-height command and a 3-dimensional navigation command), with an action horizon of 40. The policy does not directly predict leg joint targets; locomotion is handled via the base-height and navigation commands. The dataset stores a raw 43-D full-body action column; the model's padded maximum action dimension is 132. Neither is the selected 35-D policy action.

Our AI models are designed and/or optimized to run on NVIDIA GPU-accelerated systems. By leveraging NVIDIA's hardware (e.g. GPU cores) and software frameworks (e.g., CUDA libraries), the model achieves faster training and inference times compared to CPU-only solutions. <br>

Per-group training configuration specifies ABSOLUTE, NON_EEF actions; final runtime handling requires confirmation because another configuration flag sets use_relative_action=true.

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

GR00T-E2E-Reference-Workflow-SIM-G1-N1.7-AppletoPlate-Model v0.2, checkpoint at training step 55,000.

The checkpoint integrates as a PyTorch policy in the G1 simulation workflow, using the released processor configuration and normalization to map camera images, robot state and the task instruction to the documented 35-dimensional action chunks; a separate whole-body controller handles locomotion.

This repository ships the full training-resume state (`optimizer.pt`, `scheduler.pt`, `rng_state.pth`, `trainer_state.json`, `training_args.bin`, `wandb_config.json`) in addition to the inference weights.


## Training, Testing, and Evaluation Datasets:

### Training Dataset:

Trained with dataset [nvidia/GR00T-E2E-Reference-Workflow-SIM-G1-N1.7-AppletoPlate-Dataset](https://huggingface.co/datasets/nvidia/GR00T-E2E-Reference-Workflow-SIM-G1-N1.7-AppletoPlate-Dataset)

**Data Modality:** Image, Video, Text, Other: robot state and actions.

**Training Data Size:** 2,500 generated demonstrations; seed demonstrations are not extra training episodes.

**Video Training Data Size:** [Less than 10,000 Hours]

**Image Training Data Size:** [Less than a Million Images]

**Text Training Data Size:** [Less than a Billion Tokens]

**Non-Audio, Image, Text Training Data Size:** 330,175 time-indexed records in the generated LeRobot dataset.

**Data Collection Method by dataset:** [Hybrid: Manually-Collected, Synthetic]

The 2,500 training demonstrations were generated by Isaac AutoData from 25 human teleoperation seed demonstrations collected in simulation using an XR headset. The 25 seeds were not added as 25 extra training episodes.

**Labeling Method by dataset:** [Hybrid: Manually-Labeled, Automated]

Seed demonstration labels (task description) were human-assigned; generated demonstrations inherit the same task label automatically from their seed via Isaac AutoData.

**Properties:** 2,500 synthetic demonstrations with 330,175 time-indexed records, containing RGB camera images/video, numerical robot states/actions and the English task instruction "move the apple to the plate", inherited from human-labeled simulation seeds.

Trained for 55,000 steps; global batch size 10; gradient accumulation 1; learning rate `1e-4` (cosine schedule); one GPU; bf16; DeepSpeed stage 2. Vision-language backbone (LLM) frozen; vision encoder, projector, VLLN, and diffusion action head trained. Training loss decreased from `1.2822` at step 10 to `0.0107` at step 55,000.

### Testing Dataset:

**Data Collection Method by dataset:** [Not Applicable]

**Labeling Method by dataset:** [Not Applicable]

**Properties:** No separate held-out testing dataset was supplied (0 held-out demonstration episodes); all 2,500 generated demonstrations are in the training split. The data consists of synthetic simulation camera images/video, numerical robot states/actions and the English task instruction "move the apple to the plate". Closed-loop simulation evaluation is described separately below.

### Evaluation Dataset:

**Data Modality:** Other: Robot Simulation

**Data Collection Method by dataset:** [Synthetic]

Simulated G1 robot

**Labeling Method by dataset:** [Not Applicable]

**Properties:** 10,000 synthetic G1 simulation episodes of apple-to-plate manipulation. Apple XY reset jitter is +/- 0.02 m; the plate is fixed. Success requires the apple placed on the plate with low motion and confirmed contact. Linguistic characteristics: the policy is conditioned on the English instruction "move the apple to the plate"; simulation outcomes are numerical success/failure labels.

**Benchmark Score:** **9,842 / 10,000 successes (98.42%)**, 158 failures, in closed-loop simulation evaluation. Apple XY reset jitter was +/- 0.02 m; the plate was fixed. Success requires the apple placed on the plate with low motion and confirmed contact. These results do not establish real-robot safety or broad out-of-distribution robustness. See the machine-readable evaluation summary at `evaluation/summary.json` in the model repository.

## Inference:

**Acceleration Engine:** PyTorch

**Test Hardware Set-Up (GPU Architecture, Model):** 
* NVIDIA Ada Lovelace RTX 6000

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
