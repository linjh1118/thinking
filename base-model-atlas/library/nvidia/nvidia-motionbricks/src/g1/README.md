---
library_name: pytorch
tags:
  - nvidia
  - motionbricks
  - unitree-g1
  - motion-generation
  - pose-conditioned
  - robotics
---

# MotionBricks Unitree G1

[Project page](https://nvlabs.github.io/motionbricks/) · [Paper](https://arxiv.org/abs/2604.24833) · [Original G1 implementation](https://github.com/NVlabs/GR00T-WholeBodyControl/tree/main/motionbricks)

## Model Description

MotionBricks Unitree G1 generates robot reference motion from recent motion, target poses,
and root-motion constraints. Applications can update targets and feed generated motion back
into the model to produce continuous locomotion and transitions. A separate controller is
needed to execute that motion on a physical robot.

NVIDIA developed the original pretrained weights for the MotionBricks
subproject in GR00T Whole-Body Control. This package stores those weights in SafeTensors format.
The model uses a 34-joint skeletal representation of Unitree G1, with separate components for
pose tokenization, pose prediction, and root-motion prediction. Its pose tokenizer is a
vector-quantized variational autoencoder (VQ-VAE).

This model is intended for commercial and non-commercial motion-generation applications.

### Where to Start

To run MotionBricks in an application, start with the [G1 ONNX model and runtime](https://github.com/NVlabs/motionbricks/blob/main/docs/unitree_g1_model.md).
Use the checkpoints on this page to work with the individual PyTorch components or create
ONNX exports. [Download the complete G1 package](#download-and-files), then follow the
[exporter guide](https://github.com/NVlabs/motionbricks/blob/main/tools/onnx/README.md). A training pipeline is not included.

| Property | Value |
| --- | --- |
| Model family | MotionBricks |
| Model version | MotionBricks-G1-RP-v1 |
| Task | Pose-conditioned robot motion generation and inbetweening |
| Robot | Unitree G1, floating pelvis and 29 joint angles |
| Skeleton | Unitree G1, 34 model joints |
| FPS | 30 |
| Checkpoint components | Pose VQ-VAE, pose model, root model |
| Checkpoint step | 2,000,000 for each model |
| Weight format | SafeTensors (`.safetensors`) |

## License and Terms of Use

Use of this model is governed by the [NVIDIA Open Model Agreement](https://www.nvidia.com/en-us/agreements/enterprise-software/nvidia-open-model-agreement/).
It permits commercial use and redistribution of modified models, subject to the agreement's terms.

- The accompanying software uses [Apache 2.0](https://github.com/NVlabs/motionbricks/blob/main/LICENSE).
- The listed Bones-derived human BVH and G1 CSV samples use the
  [NVIDIA Sample Data Evaluation License](https://github.com/NVlabs/motionbricks/blob/main/assets/motions/LICENSE.txt).
  They are for internal evaluation and testing of NVIDIA technologies. See the
  [sample notice](https://github.com/NVlabs/motionbricks/blob/main/assets/motions/README.md) for the exact files covered.
- Robot assets and third-party dependencies retain their [respective licenses](https://github.com/NVlabs/motionbricks/tree/main/licenses).

## Deployment Geography

Global.

## Intended Uses

**Use Case:** Pose-conditioned G1 reference-motion generation for animation, robotics simulation,
and downstream control experiments.

**Intended Users:** Developers and researchers integrating G1 motion generation into their applications.
Generated motion is not validated for physical robot control.

## Model Package

This card covers `MotionBricks-G1-RP-v1` in the
[`g1/` folder](https://huggingface.co/nvidia/MotionBricks/tree/main/g1).
The SOMA package is documented separately.

The weights come from the original
[GR00T Whole-Body Control implementation](https://github.com/NVlabs/GR00T-WholeBodyControl/tree/b042411fae38ee4d1af9aac82a37a1f8d14d6dd0/motionbricks/out).
They are stored in SafeTensors format with numeric skeleton arrays. The accompanying Open Neural Network Exchange (ONNX)
export changes the runtime interface, not the training of these weights.

## References

T. Wang, O. Dionne, M. De Ruyter, D. Minor, D. Rempe, K. Zhao, M. Petrovich,
Y. Yuan, C. Li, Z. Luo, B. Robison, X. Blackwell, B. Antoniazzi, X. B. Peng,
Y. Zhu, and S. Yuen, **MotionBricks: Scalable Real-Time Motions with
Modular Latent Generative Model and Smart Primitives**, 2026.
[ACM Transactions on Graphics](https://doi.org/10.1145/3811334). [arXiv:2604.24833](https://arxiv.org/abs/2604.24833).

## Download and Files

Download the G1 model files from the shared MotionBricks repository:

```sh
hf download nvidia/MotionBricks --include "g1/*" --local-dir MotionBricks
```

The expanded files preserve the original `out/` layout under `g1/`. No archive
extraction is required.

| Component | Location within the `g1/` folder |
| --- | --- |
| Pose VQ-VAE | `out/motionbricks_vqvae/version_1/` |
| Pose model | `out/motionbricks_pose/version_1/` |
| Root model | `out/motionbricks_root/version_1/` |

Each model directory contains `checkpoints/model-step=2000000.safetensors`, a
JSON metadata sidecar, saved configuration, numeric normalization arrays, and
skeleton metadata. Skeleton arrays use `joints.npy` and `parents.npy`. Keep these
files together. The original demo motion bank, `out/G1-clip.ckpt`, is not included.
It is not one of the three neural-network checkpoints. The original demo requires that
separate motion bank.

[manifest.json](https://huggingface.co/nvidia/MotionBricks/blob/main/g1/manifest.json) records each included file's size and SHA-256.
[SHA256SUMS](https://huggingface.co/nvidia/MotionBricks/blob/main/g1/SHA256SUMS) provides the checksums for the expanded model files.

## Model Architecture

**Architecture Type:** Modular latent generative model.

**Network Architecture:** Transformer-based pose and root predictors with a learned pose
tokenizer and decoder. Recent motion, target poses, root constraints, and allowed duration
condition generation. The pose predictor produces motion codes, which the decoder turns into
skeletal-motion features. The root predictor generates root motion and duration.

**Base Model:** The original G1 components were trained from scratch on RP1 motion retargeted
to G1. This release reuses those weights without retraining and packages them in SafeTensors
format.

The model operates on the G1 skeletal representation. Application code converts between
skeletal motion and the robot's joint angles.

The original G1 tokenizer uses eight heads with 10 codes per head and 32
dimensions per head. Use the matching G1 bundle and configuration for
reproduction.

**Number of Model Parameters:** Approximately 195 million across the three components. The
component counts below are rounded.

| Component | Approximate parameters |
| --- | --- |
| Pose VQ-VAE | 23.8 million |
| Pose predictor | 136.6 million |
| Root predictor | 34.1 million |

## Inputs

**Input Type(s):** Skeletal-motion features, pose constraints, root-motion constraints, motion-token
IDs, conditioning masks, and duration constraints. Text, images, audio, and video are not inputs
to these checkpoint components.

**Input Format(s):** Numeric PyTorch tensors. Motion features use 32-bit floating point (FP32) with the bundled
normalization statistics. Token IDs and lengths are integers. Constraint and padding masks are
Boolean.

**Input Parameters:** The component tables below specify the tensor shapes and meanings.

**Other Properties Related to Input:** Context and target poses supply constraints on a short
generation. The root predictor receives four context poses and four target poses. All components
require their matching configuration and normalization statistics.

The three checkpoint components use the tensor interfaces below. `N` is the
batch size, `L` is the number of motion-token positions, and `T = 4L` is the
number of frames. Generation uses 6 to 16 tokens (24 to 64 frames) at 30 Hz.
Shorter sequences can be padded and accompanied by their valid lengths.
The checkpoint networks support batching. The practical batch size depends
on memory and the inference implementation.

These are component-level interfaces after feature preparation. An application's pose
interface or exported graph can differ.

For joint ordering, coordinate conventions, normalization, and motion
reconstruction, use the matching MotionBricks implementation and the bundled
configuration and skeleton metadata.

### Pose VQ-VAE: tokenizer and decoder

| Tensor | Direction | Shape | Description |
| --- | --- | --- | --- |
| Pose features | Encoder input | `(N, T, 304)` | Root height, 33 non-root joint positions (3 values each), and 34 joint rotations (6 values each) |
| Motion codes | Encoder output / decoder input | `(N, L, 8)` | Eight codebook heads. Each ID is in `0…9` |
| Target pose features | Decoder input | `(N, T, 304)` | Pose constraints in the same feature representation |
| Target pose mask | Decoder input | `(N, T)` | Which frames contain pose constraints |
| Local root velocity | Decoder input | `(N, T, 2)` | Ground root-motion conditioning |
| Valid-token mask | Decoder input, optional | `(N, L)` | Valid positions when decoding padded sequences |
| Reconstructed motion | Decoder output | `(N, T, 413)` | Local-root features (4), joint positions (99), 6D rotations (204), joint velocities (102), and foot-contact features (4) |

Each token represents four frames. The quantized latent has 256 values per
token (eight heads × 32 values). The table uses separate per-head code IDs.
The implementation also supports packing them into one integer per token.

### Pose predictor

| Tensor | Direction | Shape | Description |
| --- | --- | --- | --- |
| Motion tokens | Input | `(N, L, 8)` | Code IDs `0…9`, or mask ID `10` for unknown codes |
| Root trajectory | Input | `(N, T, 4)` | Ground root position and two-component heading, without root height |
| Pose constraints | Input | `(N, T, 304)` | Root height, joint positions, and 6D rotations |
| Pose constraint mask | Input | `(N, T)` | Frames with supplied pose constraints |
| Valid token count | Input | `(N, 1)` | One length in `6…16` per sample |
| Pose-code logits | Output | `(N, L, 8, 10)` | Scores over each head's codebook. Selected codes feed the decoder |

### Root predictor

The root predictor receives eight boundary frames: four context frames and
four target frames. Each sample can have its own constraints and duration.

| Tensor | Direction | Shape | Description |
| --- | --- | --- | --- |
| Global root constraints | Input | `(N, 8, 5)` | Root position (3) and heading (2) |
| Local root constraints | Input | `(N, 8, 4)` | Root angular velocity (1), ground velocity (2), and height (1) |
| Pose constraints | Input | `(N, 8, 304)` | Root height, joint positions, and 6D rotations |
| Constraint masks | Input | Three tensors of `(N, 8)` | One mask for each of the preceding constraint tensors |
| Requested token count | Input | `(N, 1)` | A specified duration in `6…16`, or the unknown-duration token `18` |
| Allowed durations | Input, optional | `(N, 11)` | Flags for the allowed token counts `6…16` |
| Duration logits | Output | `(N, 12)` | Eleven duration scores plus an out-of-reach class |
| Predicted token count | Output | `(N,)` | Selected duration. Generation disables the out-of-reach class |
| Predicted global root | Output | `(N, 64, 5)` | Padded root trajectory. Each sample's valid length is four times its token count |

## Outputs

**Output Type(s):** Motion codes and logits, reconstructed skeletal-motion features, root-motion
predictions, and valid duration.

**Output Format(s):** Numeric PyTorch tensors. Motion features and root predictions use FP32.
Motion codes and selected lengths are integers.

**Output Parameters:** The component tables above specify each output's shape and meaning.
Output motion is represented at 30 Hz. Valid-length information distinguishes generated motion
from padding.

**Other Properties Related to Output:** Longer motion requires repeated generation. Generated
motion can supply the next context. The checkpoint-component interfaces differ from the joint
coordinate interface of the combined ONNX export.

Together, the components generate root and body motion features. After
denormalization and skeletal reconstruction, motion can be represented as
root translations `(N, T, 3)` and joint rotation matrices
`(N, T, 34, 3, 3)`. The matching kinematic conversion can derive the robot's
29 joint angles.

## Software Integration

**Runtime Engine(s):** PyTorch with the matching MotionBricks implementation, configuration,
normalization statistics, and skeleton metadata. The exporter requires Python 3.12,
PyTorch 2.14.0+cpu, NumPy 1.26.4, ONNX 1.23.2, and SafeTensors 0.8.0.

**Supported Hardware Microarchitecture Compatibility:** The exporter runs on the CPU.
A specific CPU model, minimum-memory requirement, and broader compatibility matrix are
not documented. For ONNX runtime requirements, see the [G1 ONNX card](https://github.com/NVlabs/motionbricks/blob/main/docs/unitree_g1_model.md).

**Supported Operating System(s):** We tested checkpoint-to-ONNX conversion on Windows.
Tests on other operating systems are not reported.

The integration of foundation and fine-tuned models into AI systems requires additional testing using use-case-specific data to ensure safe and effective deployment. Following the V-model methodology, iterative testing and validation at both unit and system levels are essential to mitigate risks, meet technical and functional requirements, and ensure compliance with safety and ethical standards before deployment.

The [exporter](https://github.com/NVlabs/motionbricks/blob/main/tools/onnx/README.md) accepts the downloaded checkpoint folder.
Its loader checks required file sizes and SHA-256 hashes, reads SafeTensors weights,
and disables NumPy pickle loading. Keep the checkpoint and exporter versions matched.
Do not load untrusted checkpoints. These checks do not replace security scans or
validation in your application.

The [original implementation](https://github.com/NVlabs/GR00T-WholeBodyControl/tree/main/motionbricks)
provides model lineage and the earlier checkpoint-based demo. Its original PyTorch checkpoint
loader is not directly compatible with this SafeTensors package.

The package omits optimizer, scheduler, callback, and training-loop state. It provides weights
for inference or fine-tuning initialization with a compatible implementation, not exact
resumption of the original training run.

## Release Date

Hugging Face 10/23/2026 via the [MotionBricks G1 checkpoint package](https://huggingface.co/nvidia/MotionBricks/tree/main/g1).

## Model Versions

`MotionBricks-G1-RP-v1` contains the three original G1 components at training step 2,000,000.
The [manifest](https://huggingface.co/nvidia/MotionBricks/blob/main/g1/manifest.json) and
[checksums](https://huggingface.co/nvidia/MotionBricks/blob/main/g1/SHA256SUMS) identify the package files.
The accompanying software release is v0.2.0.

The components are used together. The MotionBricks exporter combines them into FP32 or
mixed 16-bit floating-point (FP16) ONNX models. Those models have a [separate card](https://github.com/NVlabs/motionbricks/blob/main/docs/unitree_g1_model.md) and a
joint-coordinate interface. The export reuses the existing weights without retraining.
It is not a newly trained joint-angle model.

## Training, Testing and Evaluation Datasets

### Training Dataset

**Name/Identifier:** Bones RigPlay 1 (RP1).

**Data Modality:** Other: human motion capture retargeted to the 34-joint Unitree G1
skeleton at 30 Hz. The model consumes motion features without text embeddings.

**Training Data Size:** 313,526 selected training clips. The approximately 700 hours describe
the source corpus, not the selected training subset.

**Data Collection Method:** Automatic/Sensors. Bones captured human performances in a studio and
supplied skeletal motion. NVIDIA used [SOMA Retargeter](https://github.com/NVIDIA/soma-retargeter)
to retarget that motion to G1, then converted it into model features. This preparation is not
direct robot recording.

**Labeling Method:** Automatic/Sensors for captured skeletal motion, followed by automated
retargeting and feature preparation. Text annotations are not model conditioning
inputs in the supplied motion-only configuration.

**Properties:** G1 skeletal motion with a capture T-pose and dual-root
representation, derived from a source corpus of approximately 350,000 RP1
clips and 700 hours of motion.

**Linguistic Characteristics:** Not applicable to the motion-feature inputs. Associated text
descriptions are dataset metadata, not model conditioning inputs.

### Testing Dataset

**Name, Size and Role:** We used 313,526 clips for training and a separate, selected set of
4,881 clips for validation and evaluation during training. No clips are shared between these
sets. The 4,881 clips are a selection from the held-out pool, not the entire pool. A separate
untouched final-test set, a performer-disjoint split, and the selected subset's duration are
not documented.

**Data Collection Method:** Automatic/Sensors, from the same Bones studio motion-capture source
as the training set. NVIDIA retargeted the human motion to the G1 representation.

**Labeling Method:** Automatic/Sensors for captured skeletal motion, followed by automated
retargeting and feature preparation.

**Properties:** The validation inputs are 30 Hz skeletal-motion features on the 34-joint G1
representation. Text descriptions are selection metadata, not conditioning inputs. Linguistic
characteristics are not applicable to these motion-only inputs. Disjoint clips alone do not rule out other forms of data leakage.

### Evaluation Dataset and Results

**Name/Size:** Evaluation uses the same 4,881-clip RP1 subset described under
[Testing Dataset](#testing-dataset). It is not an additional independent test set.

**Benchmark Score:** A complete quantitative evaluation report for these checkpoint files
is not included with this package.

**Data Collection Method:** Automatic/Sensors, using the same studio-captured human motion
retargeted to G1.

**Labeling Method:** Automatic/Sensors for captured skeletal motion, followed by automated
retargeting and feature preparation.

**Properties:** Evaluation uses the same 30 Hz G1 skeletal-motion representation as training.
Text descriptions are selection metadata, not conditioning inputs. Linguistic characteristics
are not applicable to the motion-only inputs. The subset's duration is unspecified.

**Recorded Results:** The package includes training-step metadata and tested export support,
but no complete checkpoint-specific quality score table.

| Check | Available evidence |
| --- | --- |
| Training progress | All three checkpoints record global step 2,000,000. This is training metadata, not a quality or safety score. |
| Checkpoint conversion | Checkpoint-to-ONNX conversion tested on Windows with CPU PyTorch. See [Inference](#inference). |
| Method evaluation | The [MotionBricks paper](https://arxiv.org/abs/2604.24833) reports experiments with its specified configurations, including separately trained benchmark models. |

The paper's benchmark dataset sizes and scores are not measurements of this packaged G1 application.

## Inference

**Acceleration Engine:** The checkpoint implementation and exporter use PyTorch.
The exporter runs on the CPU. The separate ONNX runtime uses TensorRT 10.8.

**Test Hardware Set-Up:** We tested checkpoint-to-ONNX conversion on Windows using CPU PyTorch.
The CPU model, conversion time, and checkpoint-runtime latency and throughput are not reported.
The [ONNX card](https://github.com/NVlabs/motionbricks/blob/main/docs/unitree_g1_model.md) describes the separate Windows and RTX 4090 runtime.
Neither successful export nor runtime execution establishes safe physical robot tracking.

## Limitations

- The model is specific to the bundled G1 kinematics and hinge order.
- The generated poses do not enforce dynamic balance, actuator limits,
  collision avoidance, or physical contact tracking.
- Physical execution needs a downstream controller and application-specific
  validation.
- Generation uses a short sequence of context and target poses. Longer motion requires
  repeated generation.
- Numerical precision and backend differences can accumulate through feedback.
- Scene geometry and text prompts are outside the model's conditioning interface.

## Ethical Considerations

NVIDIA believes Trustworthy AI is a shared responsibility and we have
established policies and practices to enable development for a wide array of
AI applications. Developers should work with their internal model team to
ensure this model meets requirements for the relevant industry and use case
and addresses unforeseen product misuse.

For more detailed information, see the [Bias](#bias-subcard),
[Explainability](#explainability-subcard), [Privacy](#privacy-subcard) and
[Safety & Security](#safety-and-security-subcard) subcards below.

Please report model quality, risk, security vulnerabilities or NVIDIA AI
Concerns [here](https://www.nvidia.com/en-us/support/submit-security-vulnerability/).

## Bias Subcard

| Field | Response |
| --- | --- |
| Participation considerations from adversely impacted groups in model design and testing | Not reported for these original G1 checkpoints. |
| Measures taken to mitigate unwanted bias | A specific measured bias mitigation is not reported. Applications should evaluate the motion conditions and users relevant to their use case. |
| Bias Metric, if measured | Demographic subgroup and motion-category comparisons are not reported for this checkpoint package. |

Retargeting motion to one robot skeleton does not establish equal performance
across source performers, motion categories or target constraints.

## Explainability Subcard

| Field | Response |
| --- | --- |
| Intended Task/Domain | Pose-conditioned G1 motion generation and inbetweening for robotics simulation, animation previews and control experiments. |
| Model Type | Modular latent generative model with transformer predictors and a learned motion tokenizer and decoder. |
| Intended Users | Developers and researchers integrating G1 kinematic motion generation. |
| Output | Motion codes and logits, root predictions, duration and reconstructed skeletal-motion features, as specified in the component tensor tables. |
| Describe how the model works | Recent motion and target constraints condition root and pose predictors. The learned tokenizer represents motion with discrete codes, and the decoder reconstructs motion features. Matching application code converts the 34-joint representation to G1 root transforms and 29 joint angles. |
| Groups tested to produce comparable outcomes | Demographic subgroup comparisons are not reported. |
| Technical Limitations and Mitigation | Fixed G1 kinematics, short context, no scene-geometry input and backend/precision variation. Validate constraints, motion quality, limits, contacts and any physical execution separately. |
| Verified to have met prescribed NVIDIA quality standards | Yes |
| Performance Metrics | See [Evaluation Dataset and Results](#evaluation-dataset-and-results) for evaluation evidence and [Inference](#inference) for runtime evidence. |
| Potential Known Risks | Invalid or implausible poses, accumulated feedback artifacts and unsafe physical execution if generated references are treated as validated robot commands. |
| Licensing | Use of this model is governed by the [NVIDIA Open Model Agreement](https://www.nvidia.com/en-us/agreements/enterprise-software/nvidia-open-model-agreement/). See [License and Terms of Use](#license-and-terms-of-use) for separate software and sample-data terms. |

## Privacy Subcard

Training used RP1 skeletal motion collected by Bones and supplied to NVIDIA under a negotiated data license. NVIDIA retargeted the motion to Unitree G1.

The datasets used to train this model were reviewed before release. Training used motion features, not text annotations or interactions with this model.

The package does not include the training corpus. Local execution does not eliminate privacy risks associated with training data.

Please review [NVIDIA’s Privacy Policy](https://www.nvidia.com/en-us/about-nvidia/privacy-policy/) for more information.

## Safety and Security Subcard

| Field | Response |
| --- | --- |
| Model Application Fields | Industrial/Machinery and Robotics, Media & Entertainment. Generated motion is not validated for physical robot control. |
| Life-critical impact | The model generates kinematic reference motion, not a safety-certified robot policy. Feeding unvalidated motion to physical hardware can cause collision, damage or injury. |
| Use Case Restrictions | Use of this model is governed by the [NVIDIA Open Model Agreement](https://www.nvidia.com/en-us/agreements/enterprise-software/nvidia-open-model-agreement/). See [License and Terms of Use](#license-and-terms-of-use) for separate software and sample-data terms. |
| Model and dataset restrictions | The pretrained package does not provide the original training corpus or demo motion bank. Rights to model weights and separately supplied motion examples are distinct. No claim about original access-control practices is inferred from this package. |

For physical execution, use a downstream controller with appropriate joint and
actuator limits, collision and contact handling, fall protection and
application-specific safety validation. The accompanying Newton integration
is a kinematic preview and does not establish successful tracking on a
physical G1.

