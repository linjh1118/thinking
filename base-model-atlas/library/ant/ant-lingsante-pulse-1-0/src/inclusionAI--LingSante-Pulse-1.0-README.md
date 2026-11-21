---
license: mit
pipeline_tag: feature-extraction
tags:
  - physiological-signals
  - time-series
  - pytorch
---

# LingSante-Pulse

Physiological signal encoder, released under the [MIT license](LICENSE).
Install the separate inference-code package before using these model assets.

## Usage

The model repository is
[inclusionAI/LingSante-Pulse-1.0](https://huggingface.co/inclusionAI/LingSante-Pulse-1.0).
After publication, this complete example downloads the model on first use:

```python
import numpy as np
from lingsante_pulse import LingSantePulse

model = LingSantePulse.from_pretrained()
x = np.random.default_rng(42).normal(size=(2, 1, 1280)).astype(np.float32)
features = model.encode(x, sample_rate=128, channels=[{"modality": "ECG", "lead": "II"}])
print(features["cls"].shape)         # [2, 256]
print(features["patch_mean"].shape)  # [2, 256]
```

To load downloaded assets from the current model directory instead, use
`LingSantePulse.from_pretrained(".", local_files_only=True)`.
`revision` pins a commit and `local_files_only=True` uses local/cached assets.

## Files and interface

- `model.safetensors`: encoder parameters.
- `config.json`: model format and automatic file-integrity checks.
- `channels.npz`: fixed channel-condition vectors and names.
- `channels.json`: physical descriptions of the channel identities.

Inputs use `[T]`, `[C,T]`, `[B,C,T]`, or aligned channel dicts. Specify the actual
sampling rate and physical channel identities. The code package handles fixed
128-Hz preprocessing, observed samples, and storage-padding masks.

CLS and observed-valid PatchMean are returned separately as `[B,C*256]`, with
channels concatenated in input order. `return_tokens=True` also returns ordered
patch features and validity masks at 0.25-s intervals. These are signal
representations; task-specific prediction heads are not included.

## Channel-vector provenance

The fixed vectors were generated with
[BAAI/bge-small-en-v1.5](https://huggingface.co/BAAI/bge-small-en-v1.5/tree/5c38ec7c405ec4b44b94cc5a9bb96e735b38267a),
using CLS pooling and L2 normalization. Only the resulting vectors are included;
no upstream encoder code, weights, or tokenizer is distributed here.
