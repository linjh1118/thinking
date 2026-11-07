---
license: other
license_name: nvidia-open-model-license
license_link: https://www.nvidia.com/en-us/agreements/enterprise-software/nvidia-open-model-license/
tags:
  - robotics
  - gr00t
  - vision-language-action
  - unitree-g1
  - isaaclab-arena
datasets:
  - nvidia/G1-Factory-Benchmark
base_model: nvidia/GR00T-N1.7-3B
base_model_relation: finetune
---

# G1-Factory-GR00T-1.7: GR00T N1.7 for the Unitree G1 humanoid

## Model Overview

### Description:

G1-Factory-GR00T-1.7 is a GR00T N1.7 vision-language-action policy fine-tuned for a Unitree G1 humanoid on the nine G1 Factory simulation tasks.
From a head-camera image, the robot's upper-body joint state and a language instruction, it predicts chunks of whole-body actions.
It was fine-tuned on the [G1-Factory-Benchmark](https://huggingface.co/datasets/nvidia/G1-Factory-Benchmark) demonstrations and runs in the [G1 Factory](https://huggingface.co/datasets/nvidia/G1-Factory) simulation scenes.
It can also be used as a base policy for reinforcement-learning post-training.

This model is ready for commercial or non-commercial use.

**Developer:** NVIDIA.

### License/Terms of Use:

[NVIDIA Open Model License](https://www.nvidia.com/en-us/agreements/enterprise-software/nvidia-open-model-license/).

### Deployment Geography:

Global.

### Use Case:

Robotics researchers and developers use this policy to perform and evaluate the nine G1 Factory tasks in simulation.
It also serves as a reference baseline and as a starting point for further fine-tuning or reinforcement-learning post-training.

### Release Date:

Hugging Face 10/19/2026 via [G1-Factory-GR00T-1.7](https://huggingface.co/nvidia/G1-Factory-GR00T-1.7).

## References(s):

- [G1-Factory-GR00T-1.7 on Hugging Face](https://huggingface.co/nvidia/G1-Factory-GR00T-1.7)
- [nvidia/G1-Factory-Benchmark](https://huggingface.co/datasets/nvidia/G1-Factory-Benchmark), the demonstration dataset this policy was fine-tuned on
- [nvidia/G1-Factory](https://huggingface.co/datasets/nvidia/G1-Factory), the simulation scenes and assets used to run and evaluate the policy
- [nvidia/GR00T-N1.7-3B](https://huggingface.co/nvidia/GR00T-N1.7-3B), the base model this policy was fine-tuned from
- [GR00T N1: An Open Foundation Model for Generalist Humanoid Robots](https://arxiv.org/abs/2503.14734)
- [nvidia/Cosmos-Reason2-2B](https://huggingface.co/nvidia/Cosmos-Reason2-2B), the vision-language backbone

## Model Architecture:

**Architecture Type:** Transformer.

**Network Architecture:** GR00T N1.7 (`Gr00tN1d7`): an `nvidia/Cosmos-Reason2-2B` vision-language backbone, a 4-layer vision-language self-attention module, and a 32-layer flow-matching action transformer that generates actions in 4 denoising steps.
The language backbone is frozen; the vision encoder, projector and action head are fine-tuned.

**Number of Model Parameters:** 3,144,016,000.

## Input(s):

**Input Type(s):** Image, Tabular, Text.

**Input Format(s):** One head-camera RGB image (`ego_view`) as `uint8` [480, 640, 3]; a 31-dimensional `float32` upper-body joint state (left arm 7, right arm 7, left hand 7, right hand 7, waist 3); one English task instruction per task (for example, PushButton: "Walk to the console and press the red button").

**Input Parameters:** Image: two-dimensional (2D); state: one-dimensional (1D); text: one-dimensional (1D).

**Other Properties Related to Input:** The policy expects the native 640 x 480 head-camera frame.
Resizing the image before the model's own processor degrades success.
State and action normalization come from the checkpoint's saved statistics and processor configuration.

## Output(s):

**Output Type(s):** Tabular.

**Output Format(s):** Continuous floating-point vectors.

**Output Parameters:** A chunk of 40 actions, each 35-dimensional.

**Other Properties Related to Output:** Each action contains left arm (7), right arm (7), left hand (7), right hand (7) and waist (3) joint targets, a base-height command (1) and a navigation command (3).
A separate whole-body balance controller turns the last two into leg motion.

Our AI models are designed and/or optimized to run on NVIDIA GPU-accelerated systems. By leveraging NVIDIA’s hardware (e.g. GPU cores) and software frameworks (e.g., CUDA libraries), the model achieves faster training and inference times compared to CPU-only solutions. <br>

## Software Integration:

**Runtime Engine(s):** PyTorch.

**Supported Hardware Microarchitecture Compatibility:** NVIDIA Lovelace.

**Supported Operating System(s):** Linux.

The reference simulator is [G1 Factory](https://huggingface.co/datasets/nvidia/G1-Factory) (IsaacLab-Arena) on Isaac Sim 6.2 and Isaac Lab 3.0 with Python 3.12.
Integration into a physical robot or another task requires use-case-specific behavior and safety validation.
Simulated success alone does not establish safe deployment.

The integration of foundation and fine-tuned models into AI systems requires additional testing using use-case-specific data to ensure safe and effective deployment. Following the V-model methodology, iterative testing and validation at both unit and system levels are essential to mitigate risks, meet technical and functional requirements, and ensure compliance with safety and ethical standards before deployment.

## Model Version(s):

G1-Factory-GR00T-1.7 v1: GR00T N1.7 fine-tuned for 20,000 steps; per-file SHA-256 checksums in `SHA256SUMS`.

The checkpoint is a standard GR00T N1.7 checkpoint.
It consumes the head-camera image, robot joint state and English task instruction, and returns action chunks using the included processor configuration, normalization statistics and embodiment mapping.

## Training, Testing, and Evaluation Datasets:

### Training Dataset:

**Link:** [nvidia/G1-Factory-Benchmark](https://huggingface.co/datasets/nvidia/G1-Factory-Benchmark)

**Data Modality:** Image, text, other (robot joint states and actions).

**Training Data Size:** 900 teleoperated demonstrations, 100 per task, in LeRobot format (about 400,000 frames recorded at 50 Hz).

**Video Training Data Size:** [Less than 10,000 Hours]

**Image Training Data Size:** [Less than a Million Images]

**Text Training Data Size:** [Less than a Billion Tokens]

**Non-Audio, Image, Text Training Data Size:** Robot joint-state and action trajectories accompanying each demonstration.

**Data Collection Method by dataset:** Manually-Collected

**Labeling Method by dataset:** Automated

**Properties:** Nine task-specific teleoperation datasets for a Unitree G1 humanoid in G1 Factory.
Each episode contains a 640 x 480 head-camera RGB video, numerical robot states and actions, and an English task instruction.
The nine tasks are BoxLift, BoxLiftFloor, BoxTableToShelfPnP, DrillLift, DrillLiftObs, DrillPnP, PickDrillFromHolder, PushButton and PushShelfForward.
Fine-tuning ran for 20,000 steps with global batch size 32 on eight GPUs, AdamW at learning rate 1e-4 with a cosine schedule and 5% warm-up, weight decay 1e-5, state dropout 0.2 and seed 42.

### Testing Dataset:

**Data Collection Method by dataset:** Synthetic

**Labeling Method by dataset:** Automated

**Data Modality:** Image, Text, Other (numerical robot states, actions and simulator-generated task outcomes).

**Properties:** The nine-task benchmark contains 900 synthetic simulation episodes in G1 Factory, 100 per task, from G1 Factory's own evaluation.
The tasks are BoxLift, BoxLiftFloor, BoxTableToShelfPnP, DrillLift, DrillLiftObs, DrillPnP, PickDrillFromHolder, PushButton and PushShelfForward.
The policy consumes head-camera RGB images, numerical robot joint states and English task instructions and generates numerical actions.
The simulator labels each episode with its task outcome.
Per-task success rates are listed under Results.

### Evaluation Dataset:

**Data Modality:** Other (simulated robot episodes and their task outcomes).

**Data Collection Method by dataset:** Synthetic

**Labeling Method by dataset:** Automated

**Properties:** 100 synthetic simulated episodes of the G1 Factory PushButton task from G1 Factory's own evaluation, containing robot state, actions and task outcomes.
The task uses the English instruction "Walk to the console and press the red button".
An episode succeeds when the task's success condition fires within the 20-second episode.

**Benchmark Score:** PushButton success rate 42% in G1 Factory's own evaluation (100 episodes).

## Inference:

**Acceleration Engine:** PyTorch.

**Test Hardware Set-Up (GPU Architecture, Model):** NVIDIA Ada Lovelace L40 and L40S

One GPU with 48 GB runs the simulator and policy.
A 50-episode evaluation with one scene takes about 45 minutes.

Inference requires the checkpoint's normalization statistics, embodiment mapping and processor configuration, all included in the repository.

## Ethical Considerations:

NVIDIA believes Trustworthy AI is a shared responsibility and we have established policies and practices to enable development for a wide array of AI applications. Developers should work with their internal model team to ensure this model meets requirements for the relevant industry and use case and addresses unforeseen product misuse.

Please make sure you have proper rights and permissions for all input image and video content; if image or video includes people, personal health information, or intellectual property, the image or video generated will not blur or maintain proportions of image subjects included.

For more detailed information on ethical considerations for this model, please see the Bias, Explainability, Safety & Security, and Privacy subcards below.

Please report model quality, risk, security vulnerabilities or NVIDIA AI Concerns [here](https://www.nvidia.com/en-us/support/submit-security-vulnerability/).

## Bias Subcard

| Field | Response |
| --- | --- |
| Participation considerations from adversely impacted groups [protected classes](https://calcivilrights.ca.gov/disputeresolution/protected-characteristics/) in model design and testing: | None |
| Bias Metric (If Measured): | None |
| Measures taken to mitigate against unwanted bias: | None |

## Explainability Subcard

| Field | Response |
| --- | --- |
| Intended Task/Domain: | Humanoid robot locomanipulation on nine G1 Factory tasks with a Unitree G1, in simulation. |
| Model Type: | Robot vision-language-action model, fine-tuned from NVIDIA GR00T N1.7. |
| Intended Users: | Developers, researchers and community working on robot foundation models, their fine-tuning and their post-training. |
| Output: | Chunks of 35-dimensional whole-body actions: arm, hand and waist joint targets plus base-height and navigation commands. |
| Describe how the model works: | Accepts a head-camera image, the robot's joint state and a language instruction, then generates an action chunk by denoising Gaussian noise with a flow-matching action transformer. |
| List the groups (or group characteristics) for which this was tested to produce comparable outcomes: | Not Applicable |
| Technical Limitations & Mitigation: | <div align="left">This model is not tested or intended for use in mission-critical applications that require functional safety. It was trained and evaluated entirely in simulation and has not been validated on physical hardware. Limitations include, but are not limited to:<br>- The model may underperform in environments, object configurations or task variations that differ from the training distribution.<br>- Performance may degrade under visual conditions or camera viewpoints not represented during training.<br>- Success rates depend on the simulator, camera, processor configuration and checkpoint pairing used for evaluation.<br><br>Risk: Underperformance in scenes, layouts or lighting that differ from the evaluated task.<br>Mitigation: Evaluate on the target task and conditions, and fine-tune or post-train with representative data.<br><br>Risk: Performance degradation when transferring from simulation to physical robots.<br>Mitigation: Perform embodiment-specific adaptation and validation on representative real-world tasks before deployment.<br><br>Risk: Collisions, object drops or task failures outside the evaluated task distribution.<br>Mitigation: Deploy external safety mechanisms, collision checking, human supervision and runtime monitoring.</div> |
| Verified to have met prescribed NVIDIA quality standards: | Yes |
| Performance Metrics: | Task success rate in closed-loop simulation evaluation: 42% on PushButton (100 episodes) in G1 Factory's own evaluation; 69.4% averaged over the nine tasks. |
| Potential Known Risks: | This model is not tested or intended for use in mission critical applications that require functional safety. It has been evaluated only in simulation and must not be deployed to physical hardware without independent safety and behavior qualification. The use of the model in those applications is at the user's own risk and sole responsibility, including taking the necessary steps to add needed guardrails or safety mechanisms prior to deployment. |
| Licensing: | [NVIDIA Open Model License](https://www.nvidia.com/en-us/agreements/enterprise-software/nvidia-open-model-license/). |

## Safety and Security Subcard

| Field | Response |
| --- | --- |
| Model Application Field(s): | Robotics |
| Describe the life critical impact (if present). | This model is not tested or intended for use in mission critical applications that require functional safety. The use of the model in those applications is at the user's own risk and sole responsibility, including taking the necessary steps to add needed guardrails or safety mechanisms prior to deployment. This model was trained and evaluated only in simulation and must not be deployed to physical hardware without independent safety and behavior qualification. |
| Use Case Restrictions: | [NVIDIA Open Model License](https://www.nvidia.com/en-us/agreements/enterprise-software/nvidia-open-model-license/). |
| Model and dataset restrictions: | The Principle of least privilege (PoLP) is applied limiting access for dataset generation and model development.  Restrictions enforce dataset access during training, and dataset license constraints adhered to. |

## Privacy Subcard

The datasets used to train this model were reviewed before release. Please review NVIDIA’s Privacy Policy (https://www.nvidia.com/en-us/about-nvidia/privacy-policy/) for more information.

## Results

Success rate of the base checkpoint in G1 Factory's own evaluation (100 episodes per task, CPU physics, 20-second episodes), as reported by [G1 Factory](https://github.com/NVlabs/G1-Factory).

| Task | Success rate |
|---|---|
| BoxLift | 98% |
| BoxLiftFloor | 96% |
| BoxTableToShelfPnP | 77% |
| DrillLift | 66% |
| DrillLiftObs | 75% |
| DrillPnP | 69% |
| PickDrillFromHolder | 44% |
| PushButton | 42% |
| PushShelfForward | 58% |
| Overall | 69.4% |

## Files

| Path | Contents |
|---|---|
| `config.json`, `embodiment_id.json`, `processor_config.json`, `statistics.json` | model, embodiment, processor and normalization settings |
| `model-0000{1,2}-of-00002.safetensors`, `model.safetensors.index.json` | weights |
| `experiment_cfg/` | the fine-tuning configuration and dataset statistics |
| `SHA256SUMS` | checksums of every other file |

## Usage

Loading requires access to the gated `nvidia/Cosmos-Reason2-2B` model on Hugging Face (`hf auth login` or `HF_TOKEN`).
Download the checkpoint:

```bash
hf download nvidia/G1-Factory-GR00T-1.7 --local-dir checkpoints/G1-Factory-GR00T-1.7
```

Load it as a GR00T N1.7 policy with the [Isaac-GR00T](https://github.com/NVIDIA/Isaac-GR00T) N1.7 code, using the `new_embodiment` embodiment tag (the tag the checkpoint was fine-tuned with; see `embodiment_id.json` and `processor_config.json`).
Each call takes one `ego_view` head-camera frame, the five state groups `left_arm`, `right_arm`, `left_hand`, `right_hand` and `waist`, and the task instruction.
It returns 40 future actions for the groups `left_arm`, `right_arm`, `left_hand`, `right_hand`, `waist`, `base_height_command` and `navigate_command`.
