# Metatron v1

## License

Model license: NVIDIA Open Model License

The model weights, checkpoints, serialized model configurations and exported
models are licensed under the [NVIDIA Open Model License](LICENSE.pdf).
See [NOTICE.txt](NOTICE.txt) for attribution.

- Deployment Geography: Global.
- Use Case: Researchers and developers running G1 motion control, recovery and
  interaction in compatible simulators or supervised real-G1 deployment workflows.
- Release: Metatron v1; native package hosted in `nvidia/Metatron-v1/G1`.
  Use the pinned revision selected by the ProtoMotions download helper. No public
  ProtoMotions release tag is asserted by this model card.
 Include both files when
redistributing these artifacts.

ProtoMotions source code remains Apache-2.0. Training datasets and robot assets
have separate terms; this model license does not grant rights to those materials.

## Overview

Metatron v1 is a Unitree G1 policy for motion control, recovery and
scene-conditioned interaction. It supports sparse motion goals, velocity
commands and scene inputs.

| Field | Value |
| --- | --- |
| Family | MaskedMimic spherical conditional VAE |
| Robot | Unitree G1, 29 actions |
| Motion corpus | BONES, AMASS/LAFAN, recovery and SAMP interaction data |
| Primary checkpoint | `inference_last.ckpt` |

## Intended Use

- Control G1 motion from partial future-pose and velocity commands.
- Perform recovery and scene-conditioned interaction.
- Run in simulation or deploy on a real Unitree G1.

## Training

- Training simulator: **IsaacLab**.
- Training method: supervised imitation from frozen motion-tracking, recovery
  and scene-interaction experts.
- Training data: BONES, AMASS/LAFAN, fall recovery and SAMP scene interaction.
- Architecture: 64-dimensional spherical latent, six-layer, four-head,
  1024-wide Transformer prior and conditioned action decoder.

## Inputs and Outputs

The policy consumes current and historical robot state and actions, masked
global/local future-pose targets, style samples, planar velocity commands and up
to two scene-box tokens. It outputs 29 raw actions, converted to motor commands
by the configured G1 PD mapping. Inference uses the learned prior without
external teachers.

The exact body/joint order, history layout, normalization, model dimensions and
action mapping are stored in `resolved_configs.json`.

## Software Integration

Native inference uses PyTorch and ProtoMotions, with simulator dependencies from
the matching ProtoMotions checkout. Linux is the native reference environment;
this is not a claim that every backend, OS or GPU has been qualified. Browser
exports and their runtime requirements are documented in the repository's
[main model card](../README.md).

## Artifacts

- `inference_last.ckpt`: policy weights and normalization statistics, including
  the posterior; optimizer state is omitted.
- `resolved_configs.json`: authoritative native inference configuration.
- `experiment_config.py` and `config.yaml`: configuration reconstruction code
  and arguments.
- `provenance.json`: artifact integrity metadata.

## Runtime Support

- Training simulator: **IsaacLab**.
- Simulator expectation: **Expected to transfer**.
- Also works in other simulators, including **MuJoCo**, and on the **real G1**.
- Preserve the trained observation, action, history and control-rate contracts.

For native playback, install ProtoMotions and its MuJoCo requirements, then run
from the repository root (the helper downloads a pinned package from this Hub):

```bash
python scripts/download_metatron.py
python protomotions/inference_agent.py --simulator mujoco --num-envs 1 \
  --checkpoint data/pretrained_models/metatron/G1/inference_last.ckpt \
  --inference-config examples/inference/metatron.py
```

The bundled native preset supports empty scenes and cycles
idle/location/steering/reaching with `X`.

### Scene Support

The **weights retain scene conditioning**. The PyTorch prior accepts
`scene_box_corners` (two boxes, eight XYZ corners each, in the root-heading
frame) and `scene_box_mask` (`true` means visible). Our separately pre-exported
39-input ONNX includes the original scene preprocessing and also retains this
capability. A scene-capable host must supply the matching object measurements.

The **native preset and generic re-export disable scenes**: the bundled
observation functions always produce zero corner tokens and false visibility
masks. Running `deployment/export_to_onnx.py` on this checkpoint preserves the
weights but builds that scene-disabled observation path. It does not reproduce
the scene-capable 39-input ONNX. The preset rejects a furniture scene file
rather than silently ignoring it.

This distinction is intentional: these weights support scenes, but this
package does not add a scene provider or a SAMP training recipe to ProtoMotions.

## Limitations

- This is an inference checkpoint, not a resumable training checkpoint.
- Training datasets and furniture assets are not included.
- The basic student recipes do not reproduce the full multi-expert training run.
- Recovery and interaction can fail depending on goals, initialization and
  physics. Hardware deployment requires robot-side safety limits, supervision
  and an emergency-stop mechanism.

## Provenance

This package contains the SAMP-capable G1 policy used for the Metatron web demo,
with its configuration adapted to the current ProtoMotions runtime.

## Evaluation and Responsible Use

The release tests exercise native configuration loading, finite actions through
MuJoCo rollout/reset, frozen normalization parity and scene-input sensitivity.
These are integration checks, not a comprehensive task-success or safety benchmark.
No native throughput or task-success aggregate is published in this card.

| Area | Scope and limitations |
| --- | --- |
| Bias | Coverage follows the motion corpora and expert rollouts; no demographic fairness evaluation is claimed. |
| Explainability | A learned conditional policy maps state and partial goals to actions; attention and latent variables are not explanations or guarantees. |
| Privacy | The package contains model tensors/configs, not raw participant records or motion datasets. No formal privacy guarantee or leakage audit is claimed. |
| Safety & Security | Not a safety controller. Validate observations, limits and recovery on the intended platform; use supervision and emergency stops on hardware. Load only trusted, verified checkpoint/config packages. |

Training motion sources are listed above. Labels are expert actions produced in
simulation for supervised imitation. Corpus splits, collection protocols and
demographic breakdowns are not included in this release; consult the source
dataset documentation and licenses. Testing here refers to release integration
checks, not an independently curated held-out benchmark. No training motion,
recovery clip, furniture asset or dataset license is redistributed by this package.

## References

- [ProtoMotions source and citation](https://github.com/NVlabs/ProtoMotions)
- [MaskedMimic](https://research.nvidia.com/labs/par/maskedmimic/)
