---
library_name: pytorch
tags:
  - nvidia
  - motionbricks
  - motion-generation
  - pose-conditioned
  - robotics
  - animation
---

# MotionBricks

[Project page](https://nvlabs.github.io/motionbricks/) · [Paper](https://arxiv.org/abs/2604.24833)

MotionBricks generates motion in real time for humanoid robots and human characters.
Give it the character's recent poses and the poses it should reach next, and it
generates the movement connecting them.

Smart Primitives turn target poses into reusable building blocks for navigation
and object interactions, without retraining the model. The accompanying software
includes SOMA and Unitree G1 demos built with Newton and Warp, plus tools for
creating your own primitives and scenes.

## Models

This repository contains pretrained SafeTensors weights for two model families:

| Model | Use | Details |
| --- | --- | --- |
| SOMA | Generate human motion on the SOMA skeleton. | [Model card](soma/README.md) |
| Unitree G1 | Generate motion for the Unitree G1 humanoid. | [Model card](g1/README.md) |

Each folder includes the model's weights, configuration and supporting files.
Keep them together. The SOMA and G1 files are not interchangeable.

## Get started

**To try the demos**, start with the [MotionBricks software](https://github.com/NVlabs/motionbricks).
It includes ready-to-use ONNX models, so you do not need to download these
checkpoints to run it. The TensorRT demo runtime requires an NVIDIA GPU.

**To export ONNX models or build another runtime**, download the weight packages:

```sh
hf download nvidia/MotionBricks --local-dir MotionBricks
```

For just one model, add `--include "soma/*"` or `--include "g1/*"`.
The files are already unpacked. Follow the software's `tools/onnx` guide to export
them, using the matching family folder.

## Model details and limitations

The family cards explain each model's inputs, outputs, training data, evaluation
and limitations. Each model uses three networks together. These weight
packages are not Transformers `from_pretrained` models, and this repository does
not include a training pipeline or the full training data. The packages contain
weights and inference metadata, not the optimizer and training-loop state needed
to resume the original training runs.

The G1 package does not include the original demo motion bank, `out/G1-clip.ckpt`.
Demo motion examples are separate from the model weights.

MotionBricks generates motion, not a controller for a physical robot. Running the
motion on hardware requires a separate tracking controller, robot-limit checks
and safety validation.

## File verification

Each model folder includes a file manifest and SHA-256 checksums:

- SOMA: [manifest](soma/manifest.json) · [checksums](https://huggingface.co/nvidia/MotionBricks/blob/main/soma/SHA256SUMS)
- Unitree G1: [manifest](g1/manifest.json) · [checksums](https://huggingface.co/nvidia/MotionBricks/blob/main/g1/SHA256SUMS)

## Terms

- **Models:** the SOMA and G1 weights use the [NVIDIA Open Model Agreement](https://www.nvidia.com/en-us/agreements/enterprise-software/nvidia-open-model-agreement/). It permits commercial use and redistribution of modified models, subject to its terms.
- **Software:** the accompanying MotionBricks code uses [Apache 2.0](https://github.com/NVlabs/motionbricks/blob/main/LICENSE).
- **Motion samples:** the separately bundled BONES samples and listed derivatives use the [NVIDIA Sample Data Evaluation License](https://github.com/NVlabs/motionbricks/blob/main/assets/motions/LICENSE.txt), for internal evaluation and testing of NVIDIA technologies. See the [sample notice](https://github.com/NVlabs/motionbricks/blob/main/assets/motions/README.md) for the exact files covered.

The model agreement does not replace the software, sample-data or third-party asset terms. This repository does not include the sample motions or the training dataset.
