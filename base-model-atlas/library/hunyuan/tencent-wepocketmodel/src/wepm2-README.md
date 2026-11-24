---
tags:
- wepocketmodel
- multimodal
- on-device
- multimodal-embedding
- mrl
- structured-decision
license: apache-2.0
base_model:
- Qwen/Qwen3.5-2B
---

# WePocketModel 1.0 2B

[![GitHub WePocketModel](https://img.shields.io/badge/GitHub-WePocketModel-181717?logo=github&logoColor=white)](https://github.com/Tencent/WePocketModel)
[![Hugging Face 2B GGUF](https://img.shields.io/badge/Hugging%20Face-2B%20GGUF-E0A800?logo=huggingface&logoColor=white)](https://huggingface.co/tencent/WePocketModel1.0-2B-GGUF)
[![Hugging Face 4B safetensors](https://img.shields.io/badge/Hugging%20Face-4B%20safetensors-E0A800?logo=huggingface&logoColor=white)](https://huggingface.co/tencent/WePocketModel1.0-4B)
[![Hugging Face 4B GGUF](https://img.shields.io/badge/Hugging%20Face-4B%20GGUF-E0A800?logo=huggingface&logoColor=white)](https://huggingface.co/tencent/WePocketModel1.0-4B-GGUF)

## Model Overview

WePocketModel (WePM) is a vision-language model family developed by WeChat AI, Tencent for on-device applications. A shared backbone and vision encoder support three capabilities in a single model.

This is the Safetensors release of WePocketModel 1.0 2B for the WePM Transformers runtime.

| Capability | Input and output |
| --- | --- |
| **Generation** | Generates text from text, images, or interleaved text and images for tasks such as OCR, image captioning, and visual question answering. |
| **Embedding** | Encodes text and images into L2-normalized vectors for retrieval and candidate ranking. The full embedding dimension is 2,048. |
| **Decision** | Evaluates application state and questions to return structured choices, ordinal scores, or binary judgments. |

## Quick Start

### Install and run on CUDA

Clone the [WePM inference code](https://github.com/Tencent/WePocketModel) and set up Python 3.10–3.13. This example installs PyTorch for CUDA 12.8.

```bash
git clone https://github.com/Tencent/WePocketModel.git
cd WePocketModel
python -m venv .venv
source .venv/bin/activate
python -m pip install torch==2.10.0 torchvision==0.25.0 \
  --index-url https://download.pytorch.org/whl/cu128
python -m pip install -r inference/requirements.txt

export WEPM_MODEL=tencent/WePocketModel1.0-2B
bash examples/gpu/generation/run.sh single_text
```

The first run downloads the checkpoint into the Hugging Face cache. Each example writes a timestamped JSON result.

### Run on CPU

Follow the [CPU installation instructions](https://github.com/Tencent/WePocketModel/blob/main/inference/README.md#installation). From the WePM checkout, select this checkpoint and run the CPU example.

```bash
export WEPM_MODEL=tencent/WePocketModel1.0-2B
bash examples/cpu/generation/run.sh single_text
```

### Run multimodal generation, embedding, and decision

```bash
bash examples/gpu/generation/run.sh interleaved
bash examples/gpu/embedding/run.sh
bash examples/gpu/decision/run.sh
```

Use the matching scripts under `examples/cpu/` on CPU. See the [examples guide](https://github.com/Tencent/WePocketModel/blob/main/examples/README.md) for sample inputs and the [inference guide](https://github.com/Tencent/WePocketModel/blob/main/inference/README.md) for CLI arguments and request formats.

### Matryoshka embeddings

WePM supports **Matryoshka Representation Learning (MRL)** for multimodal embeddings. Select **64, 128, 256, 512, 1,024, or 2,048** dimensions with `--embedding-dim`. The runtime L2-normalizes the selected prefix of the embedding projection. The CLI defaults to 2,048 dimensions.

```bash
python inference/infer.py \
  --model tencent/WePocketModel1.0-2B --task embed \
  --prompt "A photo of a red square." --embedding-dim 256 \
  --output results/wepm-2b-embedding-256.json
```

On CPU, use `inference/infer_cpu.py` with the same arguments.

## Checkpoint and Runtime

Download the complete checkpoint to use it from a local directory.

```bash
hf download tencent/WePocketModel1.0-2B --local-dir checkpoints/WePocketModel1.0-2B
export WEPM_MODEL="$PWD/checkpoints/WePocketModel1.0-2B"
```

| Files | Purpose |
| --- | --- |
| `model-00001-of-00003.safetensors` through `model-00003-of-00003.safetensors` and `model.safetensors.index.json` | Backbone weights and the shard index. |
| `unimodel_aux.safetensors` | Visual budgeting and task weights, including the embedding and decision heads. |
| Config, tokenizer, processor, chat template, `runtime_sources/`, and `export_complete.json` | Input processing, runtime sources, and published weight checksums. |

The checkpoint contains 2.23 billion parameters and approximately 4.47 GB of BF16 weights on disk. The WePM runtime uses BF16 on CUDA and FP32 on CPU. Runtime memory depends on the device, inputs, and generation length.

## Evaluation

[![WePM benchmark comparison across Embedding, Generation, and Decision](assets/wepm_single_results.png)](assets/wepm_single_results.png)

*Benchmark results for the WePM model family across embedding, generation, and structured decision tasks.*

## Intended Use and Limitations

WePM is intended for local applications that combine multimodal retrieval, generation, and structured decisions. Application developers should evaluate output quality on representative inputs and validate structured decisions before using them to trigger actions.

## License and Citation

The WePM inference code is licensed under [Apache 2.0](https://github.com/Tencent/WePocketModel/blob/main/LICENSE).

The model weights in this repository are licensed under the [Apache License 2.0](LICENSE.txt). The listed third-party components retain their original licenses.

If you find our work useful, please cite it as:

```
@misc{wepm2026,
  title = {WePM: Hierarchical Conflict Reconciliation for Unified MLLMs},
  author = {{WeChat AI, Tencent}},
  year = {2026},
  howpublished = {Technical Report},
  url = {https://arxiv.org/abs/2611.27365}
}
```