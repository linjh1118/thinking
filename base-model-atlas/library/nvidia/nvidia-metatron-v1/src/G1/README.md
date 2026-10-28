# Metatron v1 — G1

Native PyTorch inference package for the Unitree G1, including policy weights,
portable resolved configuration and reconstruction recipe. This is the
SAMP-capable G1 policy, not a SOMA policy or a resumable training checkpoint.

See [MODEL_CARD.md](MODEL_CARD.md) for architecture, inputs, scene limitations,
training provenance and safe use. [LICENSE.pdf](LICENSE.pdf) and
[NOTICE.txt](NOTICE.txt) must accompany redistributed model artifacts; code is
Apache-2.0 and third-party data/assets keep their own terms.

From a compatible ProtoMotions checkout with MuJoCo dependencies installed:

```bash
python scripts/download_metatron.py
python protomotions/inference_agent.py --simulator mujoco --num-envs 1 \
  --checkpoint data/pretrained_models/metatron/G1/inference_last.ckpt \
  --inference-config examples/inference/metatron.py
```

The helper pins the Hub revision and verifies every file. It includes the
license and model card. `--configs-only` downloads the small sidecars for config
tests, not a runnable policy. Avoid mixing files from different revisions.
The current native preset cycles idle/location/steering/reaching with `X` and
masks scene inputs. Use the separate `demo/model.onnx` and its paired application
for the scene-capable browser interface; a generic native re-export is not the
same graph. `racer/network.onnx` is the six-robot browser interface.

No training data, recovery clips or robot meshes are included here. Robot and
example motion assets are supplied separately by ProtoMotions under their own terms.
