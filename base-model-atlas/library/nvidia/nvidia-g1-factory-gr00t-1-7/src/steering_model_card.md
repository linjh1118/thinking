---
license: other
license_name: nvidia-open-model-license
license_link: https://www.nvidia.com/en-us/agreements/enterprise-software/nvidia-open-model-license/
tags:
  - robotics
  - reinforcement-learning
  - gr00t
  - unitree-g1
  - isaaclab-arena
base_model: nvidia/G1-Factory-GR00T-1.7
base_model_relation: adapter
---

# Isaac-RLPT GR00T N1.7 G1 Factory PushButton: DSRL steering policy

## Model Overview

### Description:

Isaac-RLPT GR00T N1.7 G1 Factory PushButton DSRL is a steering policy, trained with reinforcement learning, that raises the success rate of the frozen GR00T N1.7 G1 policy ([G1-Factory-GR00T-1.7](https://huggingface.co/nvidia/G1-Factory-GR00T-1.7)) on the G1 Factory (IsaacLab-Arena) PushButton task, in which a Unitree G1 humanoid walks to a console and presses a red button. GR00T generates actions by denoising a Gaussian noise sample; DSRL (diffusion steering with reinforcement learning) trains a small actor that chooses that noise instead of sampling it, steering the frozen policy toward better actions without changing any of its weights. It is the post-trained reference policy of the RL Post-Training (RLPT) workflow.

This model is ready for commercial or non-commercial use.

**Developer:** NVIDIA.

### License/Terms of Use:

[NVIDIA Open Model License](https://www.nvidia.com/en-us/agreements/enterprise-software/nvidia-open-model-license/).

### Deployment Geography:

Global.

### Use Case:

Robotics researchers and developers use this policy to reproduce and study the improvement that reinforcement-learning post-training adds to a frozen vision-language-action policy in simulation, by comparing it with the paired baseline under the same evaluation.

### Release Date:

Hugging Face 10/19/2026 via [Isaac-RLPT-GR00T-1.7-G1-Factory-PushButton-DSRL](https://huggingface.co/nvidia/Isaac-RLPT-GR00T-1.7-G1-Factory-PushButton-DSRL).

## References(s):

- [Isaac-RLPT-GR00T-1.7-G1-Factory-PushButton-DSRL on Hugging Face](https://huggingface.co/nvidia/Isaac-RLPT-GR00T-1.7-G1-Factory-PushButton-DSRL)
- [G1-Factory-GR00T-1.7 on Hugging Face](https://huggingface.co/nvidia/G1-Factory-GR00T-1.7), the frozen base policy
- [Steering Your Diffusion Policy with Latent Space Reinforcement Learning (DSRL)](https://arxiv.org/abs/2506.15799)
- [GR00T N1: An Open Foundation Model for Generalist Humanoid Robots](https://arxiv.org/abs/2503.14734)

## Model Architecture:

**Architecture Type:** Transformer.

**Network Architecture:** A transformer actor with a tanh-squashed Gaussian output, conditioned on the robot's 31-dimensional joint state and a 768-dimensional DINOv2 embedding of the head-camera image. It outputs the initial noise from which the frozen GR00T N1.7 policy generates its action chunk. It was trained with soft actor-critic (SAC) using an ensemble of transformer critics, which ship with the checkpoint as training state; only the actor acts at inference.

**Number of Model Parameters:** 6,442,182 in the steering actor, which runs on top of the frozen 3,144,016,000-parameter base policy.

Keeping the base weights frozen does not by itself preserve every capability or safety property of the base policy.

## Input(s):

**Input Type(s):** Image, Tabular, Text.

**Input Format(s):** One head-camera RGB image as `uint8` [480, 640, 3], from which a 768-dimensional DINOv2 embedding is computed for the actor; a 31-dimensional `float32` upper-body joint state; the task instruction "Walk to the console and press the red button", used by the base policy.

**Input Parameters:** Image: two-dimensional (2D); state: one-dimensional (1D); text: one-dimensional (1D).

**Other Properties Related to Input:** The base policy expects the native 640 x 480 head-camera frame. The steering actor's output is a [40, 35] noise tensor bounded to [-2, 2]; evaluation must use the same bound as training, because a different bound rescales every steering action.

## Output(s):

**Output Type(s):** Tabular.

**Output Format(s):** Continuous floating-point vectors.

**Output Parameters:** The actor outputs a [40, 35] steering noise tensor bounded to [-2, 2]. The frozen base policy generates a chunk of 40 actions, each 35-dimensional.

**Other Properties Related to Output:** Each action contains left arm (7), right arm (7), left hand (7), right hand (7) and waist (3) joint targets, a base-height command (1) and a navigation command (3); a separate whole-body balance controller turns the last two into leg motion.

Our AI models are designed and/or optimized to run on NVIDIA GPU-accelerated systems. By leveraging NVIDIA’s hardware (e.g. GPU cores) and software frameworks (e.g., CUDA libraries), the model achieves faster training and inference times compared to CPU-only solutions. <br>

## Software Integration:

**Runtime Engine(s):** PyTorch.

**Supported Hardware Microarchitecture Compatibility:** NVIDIA Lovelace.

**Supported Operating System(s):** Linux.

The reference simulator is G1 Factory (IsaacLab-Arena) on Isaac Sim 6.2 and Isaac Lab 3.0 with Python 3.12. Integration into a physical robot or another task requires use-case-specific behavior and safety validation; simulated success alone does not establish safe deployment.

The integration of foundation and fine-tuned models into AI systems requires additional testing using use-case-specific data to ensure safe and effective deployment. Following the V-model methodology, iterative testing and validation at both unit and system levels are essential to mitigate risks, meet technical and functional requirements, and ensure compliance with safety and ethical standards before deployment.

## Model Version(s):

Isaac-RLPT-GR00T-1.7-G1-Factory-PushButton-DSRL v1: the steering actor saved after 72,488 environment steps of training; per-file SHA-256 checksums in `SHA256SUMS`. It requires G1-Factory-GR00T-1.7 v1 as its base policy.

The steering actor integrates with the frozen G1-Factory-GR00T-1.7 v1 policy in the RLPT IsaacLab-Arena workflow. It uses the robot joint state and DINOv2 image embedding to produce the steering-noise tensor consumed by the base policy; retain the documented steering bound and base-policy processor and normalization statistics.

## Training, Testing, and Evaluation Datasets:

### Training Dataset:

**Data Modality:** Image, other (robot joint states, actions, simulator rewards and episode outcomes).

**Training Data Size:** 253 recorded episodes and 72,488 environment steps of simulated PushButton experience, as recorded in the released checkpoint's `72488/manifest.json`.

**Video Training Data Size:** [Less than 10,000 Hours]

**Image Training Data Size:** [Less than a Million Images]

**Text Training Data Size:** [Less than a Billion Tokens]

**Non-Audio, Image, Text Training Data Size:** Robot joint-state and action trajectories from the same simulated experience.

**Data Collection Method by dataset:** Synthetic

**Labeling Method by dataset:** Automated

**Properties:** The released checkpoint's manifest records 253 episodes and 72,488 environment steps of synthetic PushButton experience containing camera images, numerical robot states/actions, simulator rewards and episode outcomes; the frozen base policy uses the English instruction "Walk to the console and press the red button". The actor was trained online in G1 Factory with one PushButton scene, using DSRL with SAC: a reward of 1 for task success and 0 otherwise, a steering bound of 2.0, an actor initialized with zero mean and log standard deviation -0.46, Gaussian warm-up latents, an entropy coefficient fixed at 0.05, a KL penalty that keeps the actor's noise near a Gaussian prior with standard deviation 0.63, 40 noise latents per decision and seed 0, for 80,000 environment steps. The released checkpoint was saved at 72,488 environment steps and chosen by its in-training evaluation.

### Testing Dataset:

**Data Collection Method by dataset:** Synthetic

**Labeling Method by dataset:** Automated

**Data Modality:** Image, Text, Other (numerical robot states, actions and simulator-generated task outcomes).

**Properties:** Checkpoint selection used a 20-episode synthetic simulation evaluation during training, on scenes seeded from 7000, followed by the separate 300-episode evaluation reported below. The workflow uses head-camera RGB images, numerical robot states/actions and the English instruction "Walk to the console and press the red button"; the simulator labels each episode with its task outcome.

### Evaluation Dataset:

**Data Modality:** Other (simulated robot episodes and their task outcomes).

**Data Collection Method by dataset:** Synthetic

**Labeling Method by dataset:** Automated

**Properties:** 300 seeded synthetic simulated episodes of the PushButton task (seeds 5050–5199 and 6000–6149), containing robot state, actions and task outcomes, scored for both the steered and the frozen base policy. The task uses the English instruction "Walk to the console and press the red button". An episode succeeds when the task's success condition fires within 1000 simulator steps (20 s).

**Benchmark Score:** PushButton success rate 82.0% (246/300) with this steering actor, against 61.3% (184/300) for the frozen base policy on the same episodes, one scene at a time.

## Inference:

**Acceleration Engine:** PyTorch.

**Test Hardware Set-Up (GPU Architecture, Model):** NVIDIA Ada Lovelace L40S

One GPU with 48 GB runs the simulator, frozen base policy and steering actor; a 50-episode evaluation with one scene takes about 45 minutes.

The actor samples its steering noise stochastically at evaluation, and the base policy uses its own processor and normalization statistics. The evaluation commands are documented in the RLPT repository's G1 Factory workflow and in the Hugging Face model card.

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
| Intended Task/Domain: | The G1 Factory PushButton task with a Unitree G1 humanoid, in simulation. |
| Model Type: | Reinforcement-learning steering actor (DSRL) for a frozen NVIDIA GR00T N1.7 vision-language-action model. |
| Intended Users: | Developers, researchers and community working on robot foundation models and their post-training. |
| Output: | A [40, 35] steering noise tensor bounded to [-2, 2]; from it the frozen base policy generates chunks of 35-dimensional whole-body actions. |
| Describe how the model works: | A transformer actor reads the robot's joint state and a DINOv2 embedding of the camera image and chooses the noise from which the frozen GR00T policy generates its actions; it was trained with soft actor-critic on a sparse task-success reward in simulation. |
| List the groups (or group characteristics) for which this was tested to produce comparable outcomes: | Not Applicable |
| Technical Limitations & Mitigation: | <div align="left">This model is not tested or intended for use in mission-critical applications that require functional safety. It was trained and evaluated entirely in simulation and has not been validated on physical hardware. Limitations include, but are not limited to:<br>- The model may underperform in environments, object configurations or task variations that differ from the training distribution.<br>- Performance may degrade under visual conditions or camera viewpoints not represented during training.<br>- Success rates depend on the simulator, camera, processor configuration and checkpoint pairing used for evaluation.<br><br>Risk: Underperformance in scenes, layouts or lighting that differ from the evaluated task.<br>Mitigation: Evaluate on the target task and conditions, and fine-tune or post-train with representative data.<br><br>Risk: Performance degradation when transferring from simulation to physical robots.<br>Mitigation: Perform embodiment-specific adaptation and validation on representative real-world tasks before deployment.<br><br>Risk: Collisions, object drops or task failures outside the evaluated task distribution.<br>Mitigation: Deploy external safety mechanisms, collision checking, human supervision and runtime monitoring.<br><br>Risk: Evaluating with a steering bound different from training rescales every steering action and changes behavior.<br>Mitigation: Evaluate with the training settings documented in this card.</div> |
| Verified to have met prescribed NVIDIA quality standards: | Yes |
| Performance Metrics: | Task success rate in closed-loop simulation evaluation on PushButton: 82.0% (246/300) with the steering actor, against 61.3% (184/300) for the frozen base policy on the same 300 seeded episodes, one scene at a time. |
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

PushButton success rate in the G1 Factory simulator (Isaac Sim 6.2, Isaac Lab 3.0), one scene at a time, stochastic steering actor, native camera image, success when the button-press condition fires within a 1000-step (20 s) limit.
Both policies are scored on the same 300 held-out episodes: each episode resets the scene and the policy noise from a fixed seed, seeds 5050–5199 and 6000–6149, none of which were used during training or to choose this checkpoint.
This evaluation uses the RLPT DSRL evaluator and differs from G1 Factory's published base evaluation, which reports 42% for PushButton.

| Policy | Episodes | Success rate |
|---|---|---|
| GR00T N1.7 alone | 300 | 61.3% (184/300) |
| GR00T N1.7 + this steering policy | 300 | **82.0% (246/300)** |

The difference is 20.7 points (95% interval about +13.9 to +27.4 points).

## Training

| Setting | Value |
|---|---|
| Algorithm | DSRL with SAC (`algorithm=dsrl_sac`) |
| Environment steps | 72,488 of an 80,000-step run |
| Steering bound | `dsrl.noise_action_bound=2.0` |
| Actor initialization | mean at zero, log standard deviation −0.46 (`policy.official_policy_init=true policy.log_std_init=-0.46`) |
| Warm-up | Gaussian latents (`dsrl.warmup_exploration=normal`) |
| Reward | 1 on success, 0 otherwise (`env.success_reward=1.0 env.failure_reward=0.0`) |
| Entropy coefficient | fixed at 0.05 (`algorithm.ent_coef=0.05`) |
| Prior regularization | KL to a Gaussian latent prior with standard deviation 0.63 (`algorithm.train_actor_with_prior_kl=true algorithm.latent_prior_std=0.63`) |
| Latents per decision | `training.chunk_size=40` |
| Seed | 0 |
| Code | Isaac RLPT v0.1 |

These are the settings of `example_workflows/g1_arena_posttraining/scripts/reproduce_results.sh dsrl PushButton 0` with `algorithm.train_actor_with_prior_kl=true algorithm.latent_prior_std=0.63` added.
The checkpoint was chosen by its in-training evaluation (65% of 20 episodes, the best of the run's 17 evaluations, on scenes seeded separately from the held-out ones); its actor fingerprint matches the evaluated actor.

## Files

| Path | Contents |
|---|---|
| `72488/learner.pt` | SAC learner state (actor, critics, optimizer); what `training.load_dir` reads |
| `72488/policy_state.pt` | the published actor weights |
| `72488/manifest.json` | step counters and the in-training evaluation of this checkpoint |
| `fingerprints.jsonl` | SHA-256 of the actor at every evaluation and save; this checkpoint's actor is `7afe19e2…` |
| `evaluation_summary.json` | the in-training evaluations of the run |
| `SHA256SUMS` | checksums of every other file |

## Usage

From the Isaac RLPT repository with the G1 Factory simulator installed (`docs/pages/workflows/g1_arena.md`).
Each command scores 50 held-out episodes (seeds 5000–5049) and ends with a line containing `SR=<success rate>%`.

```bash
hf download nvidia/G1-Factory-GR00T-1.7 --local-dir checkpoints/G1-Factory-GR00T-1.7
hf download nvidia/Isaac-RLPT-GR00T-1.7-G1-Factory-PushButton-DSRL --local-dir checkpoints/Isaac-RLPT-GR00T-1.7-G1-Factory-PushButton-DSRL
export POSTTRAIN_BASE_CKPT=$PWD/checkpoints/G1-Factory-GR00T-1.7

# Before: the frozen policy.
uv run bash example_workflows/g1_arena_posttraining/scripts/reproduce_results.sh base PushButton

# After: the frozen policy steered by this checkpoint.
uv run bash example_workflows/g1_arena_posttraining/scripts/reproduce_results.sh rescore PushButton \
  checkpoints/Isaac-RLPT-GR00T-1.7-G1-Factory-PushButton-DSRL/72488
```

The scoring command applies the training settings above; an evaluation with a different `dsrl.noise_action_bound` from training rescales every steering action and gives a wrong result.

