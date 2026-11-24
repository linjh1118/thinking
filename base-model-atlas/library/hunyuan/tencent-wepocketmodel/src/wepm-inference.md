# WePM Inference

WePM `task_slots_v1` runs with Transformers on CPU or CUDA and with a native GGUF language backend on CPU. Both backends use the WePM vision encoder, MGVB, independent embedding and decision slots, and trained task heads.

Supported tasks:

- `generate`: text or multimodal generation
- `embed`: L2-normalized multimodal embeddings
- `decision`: structured choice, score, and binary judgment

## Installation

Create a Python 3.10–3.13 environment and install the PyTorch build for the target device.

NVIDIA GPU (CUDA 12.8 example):

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install torch==2.10.0 torchvision==0.25.0 \
  --index-url https://download.pytorch.org/whl/cu128
python -m pip install -r inference/requirements.txt
```

CPU:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install torch==2.10.0 torchvision==0.25.0 \
  --index-url https://download.pytorch.org/whl/cpu
python -m pip install -r inference/requirements.txt
```

`Pillow` handles standard images and `pillow-heif` decodes the unmodified HEIC files bundled with the examples.

## Model download and local directory

`--model` accepts a Hugging Face model repository ID or a local checkpoint directory. The default is `tencent/WePocketModel1.0-4B`. To switch between compatible 2B and 4B Transformers checkpoints, change `--model` to the desired checkpoint. On CPU, a snapshot or directory containing a GGUF `bundle.json` selects the GGUF backend. See the [model table](../README.md#model-weights) for the 2B and 4B repository IDs in both formats.

Both backends use the Python runtime included in this inference repository by default. If an export requires custom task code, review its `runtime_sources/` directory and pass `--trust-model-code` to execute that code with your user permissions. This applies to local directories and Hub snapshots. For Hub models, use `--revision` with the commit you reviewed.

The first online run downloads a complete snapshot, including the auxiliary weights and runtime sources, into the standard Hugging Face cache. Later runs reuse cached files, but may check the repository for updates. Use `--revision` to pin a tag or commit, `--cache-dir` to select a cache location, and `--local-files-only` (or `HF_HUB_OFFLINE=1`) to prohibit network access. Downloads finish before the inference timeout starts and before CUDA resources are allocated.

To download ahead of time into a local directory:

```bash
hf download tencent/WePocketModel1.0-4B --local-dir checkpoints/WePocketModel1.0-4B
```

Pass `--model checkpoints/WePocketModel1.0-4B` to load that directory without network access.

A complete local model directory contains:

```text
huggingface/
├── config.json
├── model-*.safetensors
├── model.safetensors.index.json
├── unimodel_aux.safetensors
├── tokenizer.json
├── tokenizer_config.json
├── processor_config.json
├── chat_template.jinja
├── runtime_sources/
└── export_complete.json
```

Keep `unimodel_aux.safetensors` alongside the backbone weights. The Transformers backend uses the export's `runtime_sources/` only with `--trust-model-code`. A release can also contain a single `model.safetensors` file without a shard index.

A raw `task_slots_v1` training export has a `model.safetensors.index.json` that points to both the backbone shards and `model-unimodel.safetensors`. Pass its Hugging Face export directory directly as `--model`. The loader separates the task weights from the backbone without copying any tensors.

CUDA waits for free memory equal to the selected checkpoint's weight files plus 2 GiB by default. This is a loading threshold. Actual peak usage depends on the input and generation length. Use `--min-free-gib` to override the threshold.

## GGUF on CPU

Install the optional GGUF requirements and build the native library on the target machine. The build requires Git, CMake 3.20 or later, and a C++17 compiler. It fetches the pinned llama.cpp revision. For an offline build, pass `--llama-source` with that revision already available locally.

```bash
python -m pip install -r inference/requirements-gguf.txt
python inference/build_gguf.py
```

Pass a GGUF Hugging Face repository ID, such as `tencent/WePocketModel1.0-4B-GGUF`, or a local directory. A complete WePM GGUF bundle contains `bundle.json`, the language weights, `multimodal-BF16.gguf`, and the accompanying tokenizer, processor, and runtime assets.

```bash
python inference/infer_cpu.py --model /path/to/wepm-gguf --task both \
  --prompt "Introduce yourself in one sentence." --output results/gguf.json
```

The language weights default to Q4_K_M. Use `--gguf-variant bf16` for BF16 language weights. The shared visual and task tensors are stored in BF16 and computed in FP32. To override discovery of the native library, use `--gguf-library` or `WEPM_GGUF_LIBRARY`. Keep its companion shared libraries in the same directory.

## Simple input

Use `--prompt` for one text item and repeat `--image` for one or more images. In this compact form, images are placed before the text.

```bash
CUDA_VISIBLE_DEVICES=0 python inference/infer.py \
  --model tencent/WePocketModel1.0-4B --task generate \
  --prompt "Describe this image." --image /path/to/image.png \
  --output results/generation.json
```

For CPU, use `inference/infer_cpu.py` and add `--threads 8`.

## Ordered multimodal input

Use `--content-json` when text and images must retain an explicit order. Relative image paths are resolved from the JSON file's directory.

```json
{
  "content": [
    {"type": "text", "text": "Inspect the first image:"},
    {"type": "image", "path": "../images/first.heic"},
    {"type": "text", "text": "Compare it with the second image:"},
    {"type": "image", "path": "../images/second.heic"},
    {"type": "text", "text": "Summarize the differences."}
  ]
}
```

```bash
CUDA_VISIBLE_DEVICES=0 python inference/infer.py \
  --model tencent/WePocketModel1.0-4B --task generate \
  --content-json /path/to/content.json \
  --output results/interleaved.json
```

`--content-json` cannot be combined with `--prompt` or `--image`.

## Structured decision

```bash
CUDA_VISIBLE_DEVICES=0 python inference/infer.py \
  --model tencent/WePocketModel1.0-4B --task decision \
  --decision-json examples/gpu/demo_data/decision/request.json \
  --output results/decision.json
```

The decision request uses `state` for the content being evaluated and `questions.q` for the task definition. Supported types are `choice`, `score`, and `noul`.

## Main arguments

| Argument | Description |
| --- | --- |
| `--model` | Hugging Face repository ID, local Transformers export, or CPU GGUF bundle. Defaults to `tencent/WePocketModel1.0-4B` |
| `--trust-model-code` | Execute Python from the selected export’s `runtime_sources/` directory. Defaults to the runtime shipped with this inference repository |
| `--revision` | Hub branch, tag, or commit; pin a commit for reproducible inference |
| `--cache-dir` | Hugging Face cache directory; otherwise use the standard Hub cache |
| `--local-files-only` | Do not access the network; fail if the requested snapshot is not cached |
| `--min-free-gib` | CUDA free-memory threshold before loading. Defaults to checkpoint size plus 2 GiB |
| `--task` | `generate`, `embed`, `both`, or `decision` |
| `--prompt` | Simple text input |
| `--image` | Simple local image input; may be repeated |
| `--content-json` | Ordered text/image content for generation or embedding |
| `--decision-json` | Structured decision request; required only for `decision` |
| `--max-new-tokens` | Generation length from 1 to 512 |
| `--embedding-dim` | Dimension supported by the chosen checkpoint; defaults to its full embedding dimension (2048 for the current 4B export) |
| `--threads` | CPU compute threads; default 8 |
| `--gguf-variant` | GGUF language weights. Accepts `q4` (default) or `bf16` |
| `--gguf-library` | Override the path to the native GGUF runtime |
| `--context-size` | GGUF context budget for input and generated tokens. Defaults to 4096 |
| `--timeout` | Request interruption after 1–1800 seconds, starting after model download (default 1200). Native calls can delay interruption until they return |
| `--output` | Required path for a new JSON result. Concurrent writes to the same path allow only one to succeed |

Each invocation processes one request, writes a JSON result, releases the model, and exits. See [`examples/`](../examples) for complete GPU and CPU cases.
