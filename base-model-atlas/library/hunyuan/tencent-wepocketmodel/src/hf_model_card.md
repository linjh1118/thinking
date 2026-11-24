---
pipeline_tag: image-text-to-text
tags:
- wepocketmodel
- multimodal
- on-device
- multimodal-embedding
- mrl
- structured-decision
license: apache-2.0
---

# WePocketModel 1.0 4B

[![GitHub WePocketModel](https://img.shields.io/badge/GitHub-WePocketModel-181717?logo=github&logoColor=white)](https://github.com/Tencent/WePocketModel)
[![Hugging Face 4B GGUF](https://img.shields.io/badge/Hugging%20Face-4B%20GGUF-E0A800?logo=huggingface&logoColor=white)](https://huggingface.co/tencent/WePocketModel1.0-4B-GGUF)
[![Hugging Face 2B safetensors](https://img.shields.io/badge/Hugging%20Face-2B%20safetensors-E0A800?logo=huggingface&logoColor=white)](https://huggingface.co/tencent/WePocketModel1.0-2B)
[![Hugging Face 2B GGUF](https://img.shields.io/badge/Hugging%20Face-2B%20GGUF-E0A800?logo=huggingface&logoColor=white)](https://huggingface.co/tencent/WePocketModel1.0-2B-GGUF)

WePocketModel (WePM) is a vision-language model family developed by WeChat AI, Tencent for on-device applications. A shared backbone and vision encoder support three capabilities in a single model.

| Capability | Input and output |
| --- | --- |
| **Generation** | Generates text from text, images, or interleaved text and images for tasks such as OCR, image captioning, and visual question answering. |
| **Embedding** | Encodes text and images into L2-normalized vectors for retrieval and candidate ranking. The 4B checkpoint has a full embedding dimension of 2,048. |
| **Decision** | Evaluates application state and questions to return structured choices, ordinal scores, or binary judgments. |

This repository contains the 4B safetensors checkpoint for the WePM Transformers runtime.

WePM uses Multi-Granularity Visual Budgeting (MGVB) to allocate visual tokens across global, regional, and fine-grained views. The runtime uses separate learned slots for embedding and decision. [Architecture overview](https://github.com/Tencent/WePocketModel#reconciling-conflicts-in-a-unified-model)

## Quick Start

### Install and run on CUDA

Clone the WePM inference code and install the dependencies in a Python 3.10–3.13 environment. This example uses PyTorch for CUDA 12.8.

```bash
git clone https://github.com/Tencent/WePocketModel.git
cd WePocketModel
python -m venv .venv
source .venv/bin/activate
python -m pip install torch==2.10.0 torchvision==0.25.0 \
  --index-url https://download.pytorch.org/whl/cu128
python -m pip install -r inference/requirements.txt
bash examples/gpu/generation/run.sh single_text
```

The example defaults to `tencent/WePocketModel1.0-4B`. It downloads the checkpoint into the Hugging Face cache on the first run and writes a timestamped JSON result.

### Run the other tasks

```bash
bash examples/gpu/generation/run.sh interleaved
bash examples/gpu/embedding/run.sh
bash examples/gpu/decision/run.sh
```

For CPU inference, follow the [CPU installation instructions](https://github.com/Tencent/WePocketModel/blob/main/inference/README.md#installation), then use the matching script under `examples/cpu/`.

```bash
bash examples/cpu/generation/run.sh single_text
```

See the [examples guide](https://github.com/Tencent/WePocketModel/blob/main/examples/README.md) for the input files and the [inference guide](https://github.com/Tencent/WePocketModel/blob/main/inference/README.md) for CLI arguments and request formats.

### Matryoshka embeddings

WePM supports **Matryoshka Representation Learning (MRL)** for multimodal embeddings. Select **64, 128, 256, 512, 1,024, or 2,048** dimensions with `--embedding-dim`. The runtime L2-normalizes the selected prefix of the embedding projection. The CLI defaults to 2,048 dimensions.

```bash
python inference/infer.py \
  --model tencent/WePocketModel1.0-4B --task embed \
  --prompt "A photo of a red square." --embedding-dim 256 \
  --output results/wepm-4b-embedding-256.json
```

On CPU, use `inference/infer_cpu.py` with the same arguments.

## Checkpoint and Runtime

Download the whole repository to use a local checkpoint.

```bash
hf download tencent/WePocketModel1.0-4B --local-dir checkpoints/WePocketModel1.0-4B
export WEPM_MODEL="$PWD/checkpoints/WePocketModel1.0-4B"
```

| Files | Purpose |
| --- | --- |
| `model-00001-of-00005.safetensors` through `model-00005-of-00005.safetensors` and `model.safetensors.index.json` | Sharded backbone weights and the shard index. |
| `unimodel_aux.safetensors` | Visual budgeting and task-specific weights, including the embedding and decision heads. Keep this file alongside the backbone shards. |
| Config, tokenizer, processor, chat template, `runtime_sources/`, and `export_complete.json` | Model configuration, input processing, runtime sources, and published weight checksums. |

The WePM runtime uses BF16 on CUDA and FP32 on CPU. The project recommends at least 16 GB of GPU memory for CUDA inference or 24 GiB of system memory for CPU inference. Actual usage depends on inputs, the number of generated tokens, and runtime overhead. [Hardware and precision guide](https://github.com/Tencent/WePocketModel#hardware-and-precision-4b)

## Evaluation

[![WePM benchmark comparison across Embedding, Generation, and Decision](assets/wepm_single_results.png)](assets/wepm_single_results.png)

*Benchmark results for the WePM model family across embedding, generation, and structured decision tasks.*

## Intended Use and Limitations

WePM is intended for local applications that combine multimodal retrieval, generation, and structured decisions. Application developers should evaluate output quality on representative inputs and validate structured decisions before using them to trigger actions.

The project reports BF16 weight memory for the model comparison. Deployment memory also includes activations, the KV cache, and framework overhead. [Memory and evaluation methodology](https://github.com/Tencent/WePocketModel#heterogeneous-capability-density-hcd)

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