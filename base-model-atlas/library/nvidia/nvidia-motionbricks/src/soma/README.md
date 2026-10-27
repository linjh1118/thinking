---
library_name: pytorch
tags:
  - nvidia
  - motionbricks
  - soma
  - rigplay
  - motion-generation
  - pose-conditioned
  - animation
---

# MotionBricks SOMA

[Project page](https://nvlabs.github.io/motionbricks/) · [Paper](https://arxiv.org/abs/2604.24833)

## Model Description

MotionBricks SOMA generates human skeletal motion from recent motion, target poses, and
root-motion constraints. Applications can feed generated motion back into the model and update
targets to produce continuous locomotion and transitions between authored poses.

NVIDIA developed `MotionBricks-SOMA-RP-v1` for the 30-joint SOMA skeleton using Bones RigPlay 1
(RP1) motion data. The checkpoint contains a pose tokenizer and decoder, a pose predictor, and a
root predictor. Together, these components generate skeletal motion from the supplied constraints.

The package includes single-precision (FP32) weights in SafeTensors format, configuration,
normalization statistics, and skeleton metadata. A training pipeline is not included.

This model is intended for commercial and non-commercial motion-generation applications.

### Where to Start

To run MotionBricks in an application, start with the [SOMA ONNX model and runtime](https://github.com/NVlabs/motionbricks/blob/main/docs/soma_model.md).
Use the checkpoints on this page to work with the individual PyTorch components or create
ONNX exports. [Download the complete SOMA package](#download-and-files), then follow the
[exporter guide](https://github.com/NVlabs/motionbricks/blob/main/tools/onnx/README.md).

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

MotionBricks SOMA is intended for developers and researchers building interactive human animation
and motion previews for robotics and simulation. Applications can generate transitions between
authored poses or update targets to guide locomotion. Generated motion is not validated for
physical robot control.

## Model Package

The SOMA model package contains SafeTensors weights, their supporting metadata, and this model card.
Derived Open Neural Network Exchange (ONNX) exports and runtime software are maintained in the
MotionBricks software repository.

The checkpoint package is organized under [`soma/` in the MotionBricks model repository](https://huggingface.co/nvidia/MotionBricks/tree/main/soma). The three SOMA components are used together. The separate `g1/` package is not covered by this card.

This card identifies the checkpoint as `MotionBricks-SOMA-RP-v1`. The accompanying software
release is v0.2.0. The checkpoint name and software version describe different artifacts.

## References

T. Wang, O. Dionne, M. De Ruyter, D. Minor, D. Rempe, K. Zhao, M. Petrovich, Y. Yuan, C. Li, Z. Luo, B. Robison, X. Blackwell, B. Antoniazzi, X. B. Peng, Y. Zhu and S. Yuen. **MotionBricks: Scalable Real-Time Motions with Modular Latent Generative Model and Smart Primitives**, 2026. [ACM Transactions on Graphics](https://doi.org/10.1145/3811334). [arXiv:2604.24833](https://arxiv.org/abs/2604.24833).

## Download and Files

Download the complete [`soma/` folder](https://huggingface.co/nvidia/MotionBricks/tree/main/soma)
and keep its directory structure intact. It contains separate directories for the pose
vector-quantized variational autoencoder (VQ-VAE), pose predictor, and root predictor.
No archive extraction is needed.

Each component includes `checkpoints/model-step=1500000.safetensors`, a JSON metadata sidecar,
and supporting configuration files. Normalization arrays and skeleton metadata define the
motion representation. Joint data is stored in `joints.npy`. Keep these files with the weights.

Use the [manifest](https://huggingface.co/nvidia/MotionBricks/blob/main/soma/manifest.json) to
identify package files and the [checksums](https://huggingface.co/nvidia/MotionBricks/blob/main/soma/SHA256SUMS)
to verify their integrity.

The package omits optimizer, scheduler, callback, and training-loop state. It provides weights
for inference or fine-tuning initialization with a compatible implementation, not exact
resumption of the original training run.

| Property | Value |
| --- | --- |
| Model family | MotionBricks |
| Task | Pose-conditioned motion generation and inbetweening |
| Skeleton | SOMA, 30 joints |
| Training dataset | RP1 |
| FPS | 30 |
| Checkpoint components | Pose VQ-VAE, pose masked motion model, root masked motion model |
| Checkpoint step | 1,500,000 for each component |
| Training precision | FP32 |
| Weight format | SafeTensors, `.safetensors` |

## Model Architecture

**Architecture Type:** Modular latent generative model.

**Network Architecture:** A pose vector-quantized variational autoencoder (VQ-VAE) encodes and decodes motion tokens. One transformer predicts motion tokens. Another predicts root motion and duration. The SOMA tokenizer uses five heads with 16 codes per head and 32 dimensions per head.

**Base Model:** The SOMA components were trained from scratch on RP1 motion. They are distinct from the original G1 model weights.

**Number of Model Parameters:** Approximately 200 million across the three components. The component counts below are rounded.

| Component | Approximate parameters |
| --- | ---: |
| Pose VQ-VAE | 23.4 million |
| Pose predictor | 136.5 million |
| Root predictor | 40.4 million |

Smart Primitives and locomotion controllers supply constraints at the application level. Text prompts are outside this model's conditioning interface. See the [MotionBricks paper](https://arxiv.org/abs/2604.24833) for the method. The paper reports experiments with the model configurations and datasets specified there.

## Inputs

**Input Type(s):** Skeletal-motion features, pose constraints, root-motion constraints, motion-token IDs, conditioning masks and duration constraints. There are no text, image, video or scene-geometry inputs in these checkpoint interfaces.

**Input Format(s):** Numeric tensors consumed by the matching PyTorch implementation. Motion features are FP32 with bundled normalization statistics. Token IDs and lengths are integers. Dense constraint and padding masks are Boolean.

**Input Parameters:** Component-specific batched tensor shapes are listed below. `N` is batch size, `L` is the number of motion-token positions and `T = 4L` is the number of frames.

**Other Properties Related to Input:** Generation uses 6 to 16 tokens, corresponding to 24 to 64 frames at 30 Hz. Shorter sequences can be padded with valid-length masks. The root predictor uses eight boundary frames, four context frames and four target frames. Practical batch sizes depend on memory and implementation. These are checkpoint-component interfaces after feature preparation. An application's pose interface or exported graph can differ.

For joint ordering, coordinates, normalization and reconstruction, use the matching MotionBricks implementation and package metadata.

### Pose VQ-VAE: tokenizer and decoder

| Tensor | Direction | Shape | Description |
| --- | --- | --- | --- |
| Pose features | Encoder input | `(N, T, 268)` | Root height, 29 non-root joint positions with three values each, and 30 joint rotations with six values each |
| Motion codes | Encoder output / decoder input | `(N, L, 5)` | Five codebook heads, each with IDs from 0 through 15 |
| Target pose features | Decoder input | `(N, T, 268)` | Pose constraints in the same representation |
| Target pose mask | Decoder input | `(N, T)` | Frames containing pose constraints |
| Local root velocity | Decoder input | `(N, T, 2)` | Ground root-motion conditioning |
| Valid-token mask | Decoder input, optional | `(N, L)` | Valid positions for padded sequences |
| Reconstructed motion | Decoder output | `(N, T, 365)` | Four local-root features, 87 joint-position values, 180 rotation values, 90 joint-velocity values and four foot-contact features |

Each token represents four frames. The quantized latent has 160 values per token, five heads times 32 values. The table uses separate per-head code IDs. The implementation also supports packing them into one integer per token.

### Pose predictor

| Tensor | Direction | Shape | Description |
| --- | --- | --- | --- |
| Motion tokens | Input | `(N, L, 5)` | IDs from 0 through 15, or mask ID 16 for unknown codes |
| Root trajectory | Input | `(N, T, 4)` | Ground root position and two-component heading, without root height |
| Pose constraints | Input | `(N, T, 268)` | Root height, joint positions and 6D rotations |
| Pose constraint mask | Input | `(N, T)` | Frames with supplied pose constraints |
| Valid token count | Input | `(N, 1)` | One length from 6 to 16 per sample |
| Pose-code logits | Output | `(N, L, 5, 16)` | Scores over each head's codebook. Selected codes feed the decoder. |

### Root predictor

Each sample can have its own constraints and duration.

| Tensor | Direction | Shape | Description |
| --- | --- | --- | --- |
| Global root constraints | Input | `(N, 8, 5)` | Root position with three values and heading with two values |
| Local root constraints | Input | `(N, 8, 4)` | Root angular velocity, ground velocity and height |
| Pose constraints | Input | `(N, 8, 268)` | Root height, joint positions and 6D rotations |
| Constraint masks | Input | Three tensors of `(N, 8)` | One mask for each constraint tensor above |
| Requested token count | Input | `(N, 1)` | Duration from 6 to 16, or unknown-duration token 18 |
| Allowed durations | Input, optional | `(N, 11)` | Flags for token counts from 6 to 16 |
| Duration logits | Output | `(N, 12)` | Eleven duration scores and an out-of-reach class |
| Predicted token count | Output | `(N,)` | Selected duration. Generation disables the out-of-reach class. |
| Predicted global root | Output | `(N, 64, 5)` | Padded root trajectory. Valid length is four times each sample's token count. |

## Outputs

**Output Type(s):** Motion codes and logits, reconstructed skeletal-motion features, root-motion predictions and valid duration. See the component tables above.

**Output Format(s):** Numeric tensors. Predicted motion features and root motion are FP32. Code IDs and selected lengths are integers. After denormalization and skeletal reconstruction, outputs can be represented as root translations `(N, T, 3)` and joint rotation matrices `(N, T, 30, 3, 3)`.

**Output Parameters:** The component tables specify dimensions and valid lengths. Output motion is represented at 30 Hz. Respect valid-length information rather than treating padded frames as generated content.

**Other Properties Related to Output:** Longer motion requires repeated generation. Predictions may become context for a later call. Export precision and backend can change results. The checkpoint interfaces are not the same as the derived ONNX interfaces.

The model was trained using NVIDIA GPUs. The CPU-based export utility converts these checkpoints
to ONNX. Its successful execution is not a real-time inference benchmark or a CPU-versus-GPU
performance comparison.

## Software Integration

**Runtime Engine(s):** PyTorch with the matching MotionBricks implementation, configuration,
normalization statistics, and skeleton metadata. The exporter requires Python 3.12,
PyTorch 2.14.0+cpu, NumPy 1.26.4, ONNX 1.23.2, and SafeTensors 0.8.0.

**Supported Hardware Microarchitecture Compatibility:** The exporter runs on the CPU.
A specific CPU model, minimum-memory requirement, and broader compatibility matrix are
not documented. For ONNX runtime requirements, see the [SOMA ONNX card](https://github.com/NVlabs/motionbricks/blob/main/docs/soma_model.md).

**Supported Operating System(s):** We tested checkpoint-to-ONNX conversion on Windows.
Tests on other operating systems are not reported.

The integration of foundation and fine-tuned models into AI systems requires additional testing using use-case-specific data to ensure safe and effective deployment. Following the V-model methodology, iterative testing and validation at both unit and system levels are essential to mitigate risks, meet technical and functional requirements, and ensure compliance with safety and ethical standards before deployment.

The [exporter](https://github.com/NVlabs/motionbricks/blob/main/tools/onnx/README.md) accepts the downloaded checkpoint folder.
Its loader checks required file sizes and SHA-256 hashes, reads SafeTensors weights,
and disables NumPy pickle loading. Keep the checkpoint and exporter versions matched.
Do not load untrusted checkpoints. These checks do not replace security scans or
validation in your application.

## Release Date

Hugging Face 10/23/2026 via the [MotionBricks SOMA checkpoint package](https://huggingface.co/nvidia/MotionBricks/tree/main/soma).

## Model Versions

`MotionBricks-SOMA-RP-v1` contains the three FP32 components at training step 1,500,000.
The [manifest](https://huggingface.co/nvidia/MotionBricks/blob/main/soma/manifest.json) and
[checksums](https://huggingface.co/nvidia/MotionBricks/blob/main/soma/SHA256SUMS) identify the package files.

The components are used together. The MotionBricks exporter combines them into FP32 or
mixed FP16 ONNX models. Those models have a [separate card](https://github.com/NVlabs/motionbricks/blob/main/docs/soma_model.md) and tensor
interface. Use that interface when integrating the ONNX runtime. The checkpoint-component
tensors are not interchangeable with the ONNX interface.

## Training, Testing and Evaluation Datasets

### Training Dataset

**Name/Identifier:** Bones RigPlay 1 (RP1).

**Data Modality:** Other: human skeletal motion capture, represented on the 30-joint SOMA skeleton at 30 Hz. Training used motion features without text embeddings.

**Training Data Size:** 313,526 human-motion clips in the selected training subset. The source
corpus contains approximately 350,000 clips and 700 hours of motion. The source-corpus duration
is not the selected training-subset duration.

**Data Collection Method:** Automatic/Sensors. Human performances were recorded in a motion-capture studio by Bones, then provided as skeletal motion. Training uses the processed uniform SOMA representation, not data captured directly on the SOMA skeleton.

**Labeling Method:** Automatic/Sensors for the captured skeletal motion, followed by automated preparation into uniform skeletal features. These motion-only runs use pose/motion values as their learning data and do not consume text embeddings or text annotations. The source dataset can include additional annotations, but those are not model conditioning inputs.

**Properties:** Training uses uniform SOMA motion features at 30 Hz, random first headings, and
random crops of up to 15 seconds. Root motion and joint features provide the motion representation.
Text embeddings and text augmentation are disabled. This package does not redistribute the
training corpus.

**Linguistic Characteristics:** Not applicable to the motion-feature inputs. Associated text
descriptions are dataset metadata, not model conditioning inputs.

All three checkpoint components were trained in FP32.

### Testing Dataset

**Name, Size and Role:** We used 313,526 clips for training and a separate, selected set of
4,881 clips for validation and evaluation during training. No clips are shared between these
sets. The 4,881 clips are a selection from the held-out pool, not the entire pool. A separate
untouched final-test set, a performer-disjoint split, and the selected subset's duration are
not documented.

**Data Collection Method:** Automatic/Sensors, from the same Bones studio motion-capture source and processed SOMA representation as the training set.

**Labeling Method:** Automatic/Sensors for captured skeletal motion, followed by automated preparation into the same motion features used for training. Text annotations are not consumed by the recorded motion-only validation path.

**Properties:** The validation inputs are 30 Hz skeletal-motion features in the same uniform SOMA
representation as the training inputs. Linguistic characteristics are not applicable to these
motion-only inputs. Disjoint clips alone do not rule out other forms of data leakage.

### Evaluation Dataset and Results

**Name/Size:** Evaluation uses the same 4,881-clip RP1 subset described under
[Testing Dataset](#testing-dataset). It is not an additional independent test set.

**Benchmark Score:** A complete end-to-end benchmark of these SOMA checkpoints is not included
with this package.

**Data Collection Method:** Automatic/Sensors. Same studio-captured Bones motion source, processed into the uniform SOMA representation.

**Labeling Method:** Automatic/Sensors for captured skeletal motion, with automated preparation into uniform motion features. Evaluation uses motion rather than text-conditioned labels.

**Properties:** Human skeletal motion represented on SOMA at 30 Hz. Linguistic characteristics
are not applicable to these motion-only inputs. Text annotations are not consumed. The selected
subset's duration is unspecified.

**Recorded Results:** The available evidence covers training-time observations and checkpoint
conversion, not a complete final-checkpoint benchmark.

| Check | Available evidence |
| --- | --- |
| Tokenizer | Reconstruction and foot-skating metrics recorded during training |
| Root predictor | Validation recorded during training |
| Pose predictor | Training loss recorded, without a complete validation result |
| Original checkpoints | Validated and exported in July 2026 |
| SafeTensors conversion | Tested on Windows with CPU PyTorch. See [Inference](#inference) for the environment. |

The [MotionBricks paper](https://arxiv.org/abs/2604.24833) reports method-level experiments with
the model and dataset configurations specified there. Those results are not an end-to-end
benchmark of this package.

## Inference

**Acceleration Engine:** The checkpoint implementation and exporter use PyTorch.
The exporter runs on the CPU. The separate ONNX runtime uses TensorRT 10.8.

**Test Hardware Set-Up:** We tested checkpoint-to-ONNX conversion on Windows using CPU PyTorch.
The CPU model, conversion time, and checkpoint-runtime latency and throughput are not reported.
The [ONNX card](https://github.com/NVlabs/motionbricks/blob/main/docs/soma_model.md) describes the separate Windows and RTX 4090 runtime.
Neither successful export nor runtime execution establishes safe physical robot tracking.

## Limitations

- Output is specific to the SOMA joint layout and proportions.
- Longer motion requires repeated generation from a short context window.
- Targets guide motion, but the model does not receive scene geometry. Applications handle obstacles and target placement.
- Generated motion can contain pose or contact artifacts and vary with numerical precision and inference backend.
- Kinematic motion generation does not establish physical feasibility or successful tracking by a robot controller.

## Ethical Considerations

NVIDIA believes Trustworthy AI is a shared responsibility and we have established policies and practices to enable development for a wide array of AI applications. Developers should work with their internal model team to ensure this model meets requirements for the relevant industry and use case and addresses unforeseen product misuse.

For more detailed information on ethical considerations for this model, see the [Bias](#bias-subcard), [Explainability](#explainability-subcard), [Safety & Security](#safety-and-security-subcard) and [Privacy](#privacy-subcard) subcards below.

Please report model quality, risk, security vulnerabilities or NVIDIA AI Concerns [here](https://www.nvidia.com/en-us/support/submit-security-vulnerability/).

## Bias Subcard

| Field | Response |
| --- | --- |
| Participation considerations from adversely impacted groups in model design and testing | Not reported. |
| Measures taken to mitigate unwanted bias | Specific measured mitigation is not reported. Applications should evaluate motion quality for their users and motion conditions. |
| Bias Metric, if measured | Demographic and body/motion coverage comparisons are not reported. |

The fixed SOMA representation does not establish equivalent quality across body proportions or motion categories.

## Explainability Subcard

| Field | Response |
| --- | --- |
| Intended Task/Domain | Pose-conditioned human skeletal motion generation and inbetweening. |
| Model Type | Modular latent generative model, with transformer predictors and learned pose tokenizer and decoder. |
| Intended Users | Developers and researchers building animation, robotics, and simulation workflows. |
| Output | Motion codes and logits, root predictions, duration and reconstructed skeletal-motion features, as detailed in the component tables. |
| Describe how the model works | The tokenizer represents motion as discrete codes. Pose and root predictors use recent motion and target constraints to predict a transition. The decoder and matching reconstruction produce skeletal motion. Applications can reuse the output as context. |
| Groups tested to produce comparable outcomes | Demographic subgroup comparisons are not reported. |
| Technical Limitations and Mitigation | Fixed skeleton, short context, no scene-geometry input and backend/precision variation. Validate application-specific motion, target placement and any physical execution separately. |
| Verified to have met prescribed NVIDIA quality standards | Yes |
| Performance Metrics | See [Evaluation Dataset and Results](#evaluation-dataset-and-results) for training metrics and [Inference](#inference) for runtime evidence. |
| Potential Known Risks | Pose/contact artifacts, unwanted motion under out-of-distribution constraints, and unsafe physical interpretation if generated poses are treated as validated robot commands. |
| Licensing | Use of this model is governed by the [NVIDIA Open Model Agreement](https://www.nvidia.com/en-us/agreements/enterprise-software/nvidia-open-model-agreement/). See [License and Terms of Use](#license-and-terms-of-use) for separate software and sample-data terms. |

## Privacy Subcard

Training used RP1 skeletal motion collected by Bones and supplied to NVIDIA under a negotiated data license. NVIDIA processed the motion into the SOMA representation.

The datasets used to train this model were reviewed before release. Training used motion features, not text annotations or interactions with this model.

The package does not include the training corpus. Local execution does not eliminate privacy risks associated with training data.

Please review [NVIDIA’s Privacy Policy](https://www.nvidia.com/en-us/about-nvidia/privacy-policy/) for more information.

## Safety and Security Subcard

| Field | Response |
| --- | --- |
| Model Application Fields | Industrial/Machinery and Robotics, Media & Entertainment. Generated motion is not validated for physical robot control. |
| Life-critical impact | Generated skeletal motion is not a validated physical controller. Misuse as robot commands can create physical risk. |
| Use Case Restrictions | Use of this model is governed by the [NVIDIA Open Model Agreement](https://www.nvidia.com/en-us/agreements/enterprise-software/nvidia-open-model-agreement/). See [License and Terms of Use](#license-and-terms-of-use) for separate software and sample-data terms. |
| Model and dataset restrictions | This package does not include the RP1 training corpus. Access to the dataset is governed separately from the model weights. |

Evaluate generated motion in the intended application. Physical execution requires a separate tracking and safety system. Hash verification and checkpoint loading alone do not establish complete security or safe downstream behavior.

