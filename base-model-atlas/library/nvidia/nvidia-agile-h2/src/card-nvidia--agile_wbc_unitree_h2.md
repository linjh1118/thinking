---
license: other
license_name: nvidia-open-model-license
license_link: LICENSE
---

**Transparency cards:** [Overview](overview.md) · [Bias](bias.md) · [Explainability](explainability.md) · [Privacy](privacy.md) · [Safety](safety.md)

# Model Overview

### Description:

Agile WBC for Unitree H2 Plus is a whole-body control system for humanoid robots, focused on smooth, stable and accurate locomotion.
The staged package contains agile_velocity.onnx, agile_velocity.yaml and agile_velocity_initial_values.safetensors.

This model is ready for commercial or non-commercial use.

### License/Terms of Use:

NVIDIA Open Model License ([license text](https://www.nvidia.com/en-us/agreements/enterprise-software/nvidia-open-model-license/))

### Deployment Geography:

Global.

### Use Case:

The Agile policy serves as a locomotion API, enabling roboticists and researchers in academia and industry to integrate it with upper-body controllers. This supports use cases such as whole-body teleoperation and collection of loco-manipulation data.

### Release Date:

Hugging Face 10/01/2026 via [nvidia/agile_wbc_unitree_h2](https://huggingface.co/nvidia/agile_wbc_unitree_h2)

## References(s):

[AGILE WBC](https://github.com/nvidia-isaac/WBC-AGILE)


## Model Architecture:

**Architecture Type:** Other - Multilayer Perceptron (MLP)

**Network Architecture:** 255 inputs, hidden layers [256, 256, 128] with ELU, and 14 outputs.

**Number of Model Parameters:** 166,030

The trained policy manages the H2 Plus legs and waist. Other joints, including the upper body, hands and head, remain available to separate controllers. This enables integration with inverse-kinematics or learned upper-body controllers.

## Input(s):

**Input Type(s):** Tabular

**Input Format(s):** Tensor (float32).

**Input Parameters:** Root angular velocity [1,3], root quaternion [1,4], base velocity [1,3], joint positions [1,31] and joint velocities [1,31]. Feedback inputs include five-step histories for angular velocity, projected gravity, velocity commands, controlled joint positions/velocities and actions, plus previous action [1,14].

**Other Properties Related to Input:** The policy consumes five-step histories of numerical robot proprioception, commands and actions; preserve the exported graph's joint ordering and feedback-state shapes.

## Output(s)

**Output Type(s):** Tabular

**Output Format(s):** Tensor (float32).

**Output Parameters:** joint_pos [1,14], joint_pos_kp_gains [1,14], and joint_pos_kd_gains [1,14], covering 12 leg joints plus waist roll and pitch. The exported graph also returns history tensors and previous-action state for feedback.

**Other Properties Related to Output:** Position targets and proportional/derivative gains control 14 leg-and-waist joints. The exported history tensors and previous-action state are fed back on the next control step.

Our AI models are designed and/or optimized to run on NVIDIA GPU-accelerated systems. By leveraging NVIDIA's hardware (e.g. GPU cores) and software frameworks (e.g., CUDA libraries), the model achieves faster training and inference times compared to CPU-only solutions.

## Software Integration:

**Runtime Engine(s):** ONNX backend; exported ONNX opset 20.

**Supported Hardware Microarchitecture Compatibility:** NVIDIA Lovelace.

Other tested hardware is listed under Inference.

**Supported Operating System(s):** Linux (Ubuntu)

The integration of foundation and fine-tuned models into AI systems requires additional testing using use-case-specific data to ensure safe and effective deployment. Following the V-model methodology, iterative testing and validation at both unit and system levels are essential to mitigate risks, meet technical and functional requirements, and ensure compliance with safety and ethical standards before deployment.

## Model Version(s):

agile_wbc_unitree_h2, exported policy Velocity-H2-History-v0.

The exported ONNX policy integrates as the locomotion component of GR00T E2E Reference Workflow v0.2. Use the accompanying configuration and initial values to preserve joint mappings and feedback state while combining it with a separate upper-body controller.

[https://huggingface.co/nvidia/agile_wbc_unitree_h2](https://huggingface.co/nvidia/agile_wbc_unitree_h2)

## Training, Testing, and Evaluation Datasets:

### Training Dataset:

**Data Modality:** Other: numerical robot states, commands, actions and simulation rewards.

**Non-Audio, Image, Text Training Data Size:** Online simulation rollouts rather than a fixed collected dataset.

**Data Collection Method by dataset:** Synthetic

**Labeling Method by dataset:** Automated

**Properties:** PPO training rollouts generated in Isaac Lab simulation for Unitree H2 Plus locomotion. The policy learns from numerical proprioception, commands, actions and simulator-generated rewards; the data has no linguistic content. No collected demonstration dataset was used.

### Testing Dataset:

**Data Modality:** Other: numerical robot states, commands and actions.

**Data Collection Method by dataset:** Synthetic

**Labeling Method by dataset:** Automated

**Properties:** Testing used the same simulation environment as training. The test data consists of simulated robot states, commands and actions with no linguistic content.

### Evaluation Dataset:

**Data Modality:** Other: numerical robot states, commands and actions.

**Data Collection Method by dataset:** Hybrid: Synthetic, Automatic/Sensors

**Labeling Method by dataset:** Automated (simulation).

**Properties:** Evaluation used the same simulation environment and physical H2 Plus hardware. The observations and control outputs are numerical robot data with no linguistic content.

**Benchmark Score:** Final training telemetry reported 0.125 m/s XY velocity error and 0.313 rad/s yaw error.

## Inference:

**Acceleration Engine:** ONNX Runtime

**Test Hardware Set-Up (GPU Architecture, Model):**
* NVIDIA Ada Lovelace L40
* NVIDIA Ada Lovelace RTX 6000
* NVIDIA Jetson Thor

## Model Limitations:

This model is not tested or intended for mission-critical applications that require functional safety. Use in those applications is at the user's own risk and responsibility, including implementing necessary guardrails and safety mechanisms.

The policy may be ineffective on floor types outside its training domain, such as slippery surfaces. Mitigation requires validation and, where necessary, retraining with representative friction coefficients.

The policy may not be robust to external disturbances. Mitigations include independent safety controls, runtime monitoring and validation under representative disturbances.

The policy may not work with every upper-body controller or highly dynamic upper-body movement. Test with small movements first and gradually expand to the required workspace.

## Ethical Considerations:

NVIDIA believes Trustworthy AI is a shared responsibility and we have established policies and practices to enable development for a wide array of AI applications. Developers should work with their internal model team to ensure this model meets requirements for the relevant industry and use case and addresses unforeseen product misuse.

For more detailed information on ethical considerations for this model, please see the [Bias](bias.md), [Explainability](explainability.md), [Safety & Security](safety.md), and [Privacy](privacy.md) subcards.  

Please report model quality, risk, security vulnerabilities or NVIDIA AI Concerns here ([https://www.nvidia.com/en-us/support/submit-security-vulnerability/](https://www.nvidia.com/en-us/support/submit-security-vulnerability/)).

## Notices

Licensed by NVIDIA Corporation under the NVIDIA Open Model License

See [LICENSE](LICENSE) and [NOTICE](NOTICE).
