<h1 align="center">Unified Pocket Models for In-App Multimodal Intelligence</h1>

<h3 align="center">WePocketModel (WePM)</h3>

<p align="center">
  <a href="https://arxiv.org/abs/2611.27365"><img src="https://img.shields.io/badge/Paper-Technical%20Report-EA4335" alt="Technical report (PDF)"></a>
  <a href="https://huggingface.co/collections/tencent/wepocketmodel"><img src="assert/hf_badge.png" width="199" height="20" alt="Hugging Face: WePocketModel"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-Apache%202.0-blue" alt="License: Apache 2.0"></a>
</p>

<p align="center">
  <strong><a href="https://github.com/Tencent/WePocketModel/blob/b62890f565342bbda76c7442b934e23cfb420f4a/README.md">WePM 1.0</a></strong>
</p>

<p align="center">
  <sub><a href="#model-introduction">Overview</a> &nbsp;·&nbsp; <a href="#quick-start">Get started</a> &nbsp;·&nbsp; <a href="#project-resources">Resources</a> &nbsp;|&nbsp; <a href="README_zh.md">中文</a> · English</sub>
</p>

## News

- **2026-11-23** · **WePM 1.0 is now open source.** Download the 2B and 4B [model weights](#model-weights) in Transformers and GGUF formats, try the [inference quick start](#quick-start), and read the [technical report](https://arxiv.org/abs/2611.27365).

## Model Introduction

On-device AI applications rarely depend on a single capability. A personal assistant may need multimodal retrieval to find local content, generation to understand and respond, and decision making to route the next action. Deploying a separate specialist for each path duplicates vision encoders and language backbones, increasing resident memory, system complexity and the cost of keeping intelligence always available on device.

**WePM** is a unified multimodal model family with **2B and 4B** variants, designed around a different principle: one compact vision–language backbone should support multiple capability families without sacrificing their individual quality. A single set of parameters provides:

- **Representation** — L2-normalized multimodal embeddings for image retrieval, text retrieval and candidate ranking.
- **Generation** — OCR, image captioning, visual question answering, summarization and assistant responses.
- **Decision** — typed outputs for option selection, ordinal scoring and binary judgment.

In BF16, the shared 4B backbone occupies approximately 8 GB of weight memory. More importantly, it replaces several independently resident models with one common foundation for local multimodal applications.

<p align="center">
  <a href="assert/wepm_function.png"><img src="assert/wepm_function_preview.webp" width="640" alt="WePM capabilities and applications"></a>
</p>

### Reconciling Conflicts in a Unified Model

Simply mixing heterogeneous tasks does not make them compatible. WePM identifies conflicts at three levels: different tasks require different visual granularity, their datasets provide different forms of supervision, and their losses operate at different scales and training rhythms. WePM reconciles these conflicts with three complementary components:

- **MGVB (Multi-Granularity Visual Budgeting)** organizes visual evidence into global, regional and fine-grained token banks under a fixed total visual-token budget. Regional and fine-grained selection is conditioned on available textual context, with a query-independent fallback when no text is provided, enabling complementary evidence across spatial scales.
- **ULKD (Unified Listwise Knowledge Distillation)** supplements native generation and embedding supervision using two frozen capability-specific teachers. It combines on-policy token-level KL distillation along student-generated trajectories with candidate-list KL distillation and projected representation alignment, transferring complementary soft supervision into one shared student.
- **SEMO (Stable and Efficient Multitask Optimization)** combines fixed task-loss weights with predefined task-exposure schedules to control each task’s contribution to the joint update. It executes sequential batch-wise forward/backward passes at unchanged model parameters, releasing each computation graph after backward and accumulating gradients before one joint optimizer update, preserving the specified joint gradient while reducing activation memory.

Together, these designs align visual evidence, learning signals and optimization dynamics within one compact backbone. Inference shares one vision encoder and one multimodal LLM backbone across all three tasks. Embedding appends a learned E slot, then projects and L2-normalizes its hidden state. Decision appends a separate learned J slot and maps its hidden state to candidate logits with a direct head. Generation uses autoregressive decoding without a soft slot.

<p align="center">
  <img src="assert/wepm_architecture.png" width="1000" alt="WePM inference and training architecture with MGVB, ULKD and SEMO">
</p>

## Performance Across Three Capability Families

The evaluation includes both WePM-4B and WePM-2B across three capability families. **Embedding** covers 30 benchmarks and 10 models, **Generation** covers 39 benchmarks and 10 models, and **Decision (JEV)** covers 7 benchmarks and 22 models.

<p align="center">
  <a href="assert/performance.png"><img src="assert/performance_preview.webp" width="1080" alt="WePM-4B and WePM-2B benchmark comparisons across 30 Embedding, 39 Generation and 7 Decision (JEV) benchmarks, with WePM-4B ranked first overall in each category"></a>
</p>

WePM-4B ranks first overall in each capability family based on aggregate scores across its benchmarks. These results show that one shared 4B backbone can support competitive embedding, generation and decision capabilities together.

## Heterogeneous Capability Density (HCD)

Benchmark quality alone does not capture the central constraint of on-device deployment: **how much usable intelligence can remain resident within a fixed memory budget?** We introduce **Heterogeneous Capability Density (HCD)** to jointly account for capability breadth, capability quality and resident inference memory.

<p align="center">
  <img src="assert/hcd_formula.png" width="640" alt="HCD = (number of capability families above the usability threshold) x (aggregate capability quality) / (resident inference memory)">
</p>

HCD counts capability families rather than individual benchmarks. For example, OCR, captioning and visual question answering all contribute to Generation instead of being counted as three separate capabilities. A higher HCD therefore indicates that a model delivers broader and stronger usable intelligence per unit of resident memory—not merely that it has been evaluated on more tasks.

<p align="center">
  <img src="assert/memory_vs_quality.png" width="640" alt="Harmonic performance versus BF16 weight memory for WePM-4B (HCD=0.244) and six independent three-model compositions">
</p>

The comparison pairs independent generation and embedding models with the same d3-4.5B decision model. WePM-4B reaches approximately 65.1% harmonic performance with about 8 GB of BF16 weight memory, yielding an HCD of 0.244. The six independent three-model compositions require roughly 21–43 GB, with harmonic performance of approximately 64.2–64.8% and HCD values of 0.045–0.092. In this comparison, WePM-4B achieves higher harmonic performance with substantially less weight memory, delivering approximately 2.7–5.4× the HCD of the independent compositions.

The memory values and HCD comparison above use BF16 weights only, not full runtime memory. KV cache, activations, framework overhead and runtime fragmentation are excluded.

## Applications

WePM is intended as a shared local intelligence layer rather than a collection of benchmark-specific interfaces. The following demos run fully on device, keeping personal images, text and interaction data local.

### 1. Personal Agent

A single resident WePM-4B supports the complete local workflow: it retrieves relevant personal content, understands multimodal context, generates a grounded response and makes the typed decision that routes the next step. Retrieval, generation and decision are composed within one model instead of being dispatched to separate services.

<div align="center">

https://github.com/user-attachments/assets/1bfb56b3-5f62-4ce0-a26e-a90e34bd8449

</div>

<!-- TBD: capture device, memory footprint, precision and latency numbers for this demo. -->

### 2. On-Device Game Assistant

The same WePM-4B interprets game frames and interface text, retrieves local knowledge and interaction history, generates contextual suggestions, and performs option judgment or action routing. This turns one continuously resident model into a complete multimodal game assistant without separately loading vision, retrieval and decision models.

<div align="center">

https://github.com/user-attachments/assets/4384a5c4-30a7-42da-8fe3-750285c1fa3e

</div>

## Inference

This repository provides the inference runtime and runnable examples for text generation from text and images, multimodal embeddings, and structured decisions.

### Model weights

| Model size | Transformers (safetensors) | GGUF (CPU) |
| --- | --- | --- |
| 2B | [WePocketModel1.0-2B](https://huggingface.co/tencent/WePocketModel1.0-2B) | [WePocketModel1.0-2B-GGUF](https://huggingface.co/tencent/WePocketModel1.0-2B-GGUF) |
| 4B | [WePocketModel1.0-4B](https://huggingface.co/tencent/WePocketModel1.0-4B) | [WePocketModel1.0-4B-GGUF](https://huggingface.co/tencent/WePocketModel1.0-4B-GGUF) |

Run with a Hugging Face model ID from the table or a local checkpoint directory. Set `WEPM_MODEL` in the examples or pass `--model` to the CLI. By default, the examples use `tencent/WePocketModel1.0-4B`.

### Quick start

Clone the repository and create a Python 3.10–3.13 environment.

```bash
git clone https://github.com/Tencent/WePocketModel
cd WePocketModel
python -m venv .venv
source .venv/bin/activate
```

Install the PyTorch build for your device. On NVIDIA GPUs, use the CUDA wheel index compatible with your setup. This example uses CUDA 12.8.

```bash
python -m pip install torch==2.10.0 torchvision==0.25.0 \
  --index-url https://download.pytorch.org/whl/cu128
python -m pip install -r inference/requirements.txt

bash examples/gpu/generation/run.sh single_text
```

For Transformers on CPU, use the CPU wheel index.

```bash
python -m pip install torch==2.10.0 torchvision==0.25.0 \
  --index-url https://download.pytorch.org/whl/cpu
python -m pip install -r inference/requirements.txt

WEPM_MODEL=tencent/WePocketModel1.0-2B bash examples/cpu/generation/run.sh single_text
```

For GGUF on CPU, use the same CPU PyTorch build, install the optional dependencies, and build the native runtime. The build requires Git, CMake 3.20 or later, and a C++17 compiler.

```bash
python -m pip install -r inference/requirements-gguf.txt
python inference/build_gguf.py

WEPM_MODEL=tencent/WePocketModel1.0-4B-GGUF bash examples/cpu/generation/run.sh single_text
```

The first run with a Hugging Face model ID downloads a complete snapshot into the Hub cache. To use a local copy, see the [checkpoint download instructions](checkpoints/README.md). The generation scripts also accept `single_image` and `interleaved`. See the [runnable examples](examples/README.md) for embeddings and decisions and the [inference guide](inference/README.md) for CLI flags, multimodal inputs, and raw training exports.

### Hardware and precision (4B)

| Backend | Device | Precision | Memory guidance |
| --- | --- | --- | --- |
| Transformers | NVIDIA GPU | BF16 | ≈8.5 GiB of weights. 16 GiB VRAM recommended. |
| Transformers | CPU | FP32 | ≈17 GiB of weights. 24 GiB system RAM recommended. |
| GGUF | CPU | Q4_K_M or BF16 language weights, FP32 vision and task compute | The 4B Q4_K_M language file and shared multimodal weights occupy ≈3.19 GiB on disk. |

Actual memory use depends on the input and context length. GGUF weight file size describes storage. Runtime RAM also includes the vision and task modules, context, and working buffers. See the [GGUF guide](inference/README.md#gguf-on-cpu) for variants and context settings.

## Project resources

[Model weights](#model-weights) · [Checkpoint downloads](checkpoints/README.md) · [Inference guide](inference/README.md) · [Runnable examples](examples/README.md)

## Citation

If you find this work useful, please consider citing it:

```bibtex
@misc{wepm2026,
  title = {WePM: Hierarchical Conflict Reconciliation for Unified MLLMs},
  author = {{WeChat AI, Tencent}},
  year = {2026},
  howpublished = {Technical Report},
  url = {https://arxiv.org/abs/2611.27365}
}
```

## License

The code made publicly available by Tencent in this repository is licensed under the Apache License, Version 2.0. See [LICENSE](LICENSE) for the complete terms and Tencent copyright notice.

This code license does not declare a license for model weights. Consult the license provided in each Hugging Face model repository for the applicable weight terms. Third-party components remain subject to their original licenses.
