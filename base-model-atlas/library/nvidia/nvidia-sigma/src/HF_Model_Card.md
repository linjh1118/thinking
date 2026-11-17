---
library_name: transformers
license: other
license_name: nvidia-nemotron-open-model-license
license_link: >-
  https://www.nvidia.com/en-us/agreements/enterprise-software/nvidia-nemotron-open-model-license/
pipeline_tag: text-generation
language:
- en
tags:
- nvidia
- pytorch
- nemotron-labs
---

# Nemotron-Labs-Sigma-8B

## Model Overview

## Description

Nemotron-Labs-Sigma-8B is a 8-billion-parameter continuous
diffusion language model. Instead of generating text one token at a time, it
denoises Gaussian noise in a low-dimensional (16-D) continuous token-embedding
space, where the denoiser network and the token embeddings are learned jointly
by likelihood optimization. Text is decoded in parallel blocks: each block of
tokens is refined over a configurable number of denoising steps (Denoising
Diffusion Probabilistic Model (DDPM) or Denoising Diffusion Implicit Model
(DDIM) samplers) with self-conditioning, while previously committed tokens are
reused through a standard key-value (KV) cache. Fewer steps trade a little
quality for large speedups, and the smooth continuous representation makes the
model amenable to few-step distillation and trajectory steering.

This is the *base* (pretrained) model. It is intended as a starting point for research on parallel-decoding language generation, fine-tuning, and distillation, not as an instruction-following assistant; for chat and instruction following, use the corresponding [instruct variant](https://huggingface.co/nvidia/Nemotron-Labs-Sigma-8B-instruct).

This model is ready for commercial or non-commercial use.

## Highlights

- Continuous-space diffusion language modeling at 8B scale with reasoning
  accuracy competitive with state-of-the-art masked (discrete) diffusion LMs.
- Block-parallel decoding: whole blocks of tokens are denoised together;
  sampling quality holds up well down to few denoising steps per block.
- Efficient DDPM/DDIM-based samplers with self-conditioning and optional
  classifier-free guidance, implemented in plain PyTorch in this repository.
- Standard `transformers` loading via `trust_remote_code`; no custom kernels,
  flash-attention, or training framework required for inference.

## License/Terms of Use

Use of this model is governed by the [NVIDIA Nemotron Open Model License](https://www.nvidia.com/en-us/agreements/enterprise-software/nvidia-nemotron-open-model-license/).

## Deployment Geography

Global

## Use Case

Researchers and developers studying diffusion-based parallel text generation: pretraining-quality base model for research on sampling, few-step distillation, trajectory steering, and fine-tuning into downstream assistants. The model runs offline on the user's own hardware; NVIDIA hosts no service.

## Release Date

- Hugging Face 11/12/2026 via https://huggingface.co/nvidia/Nemotron-Labs-Sigma-8B

## References

- [Large Language Continuous Diffusion Models](https://arxiv.org/abs/2610.02665) (arXiv:2610.02665, 2026).

## Model Architecture

- **Architecture Type:** Transformer
- **Network Architecture:** Other: Ministral-style decoder-only Transformer (grouped-query attention, SwiGLU, rotary position embeddings) with a continuous-diffusion generation head (16-D continuous token-embedding space, learned jointly with the denoiser).
- **Number of model parameters:** 8 billion (8B)


## Input

- **Input Type(s):** Text
- **Input Format(s):** String
- **Input Parameters:** One-Dimensional (1D): Sequences
- **Other Properties Related to Input:** Maximum context length of 4,096 tokens (prompt plus generated tokens). Plain-text prompts; the base model is best used with few-shot or benchmark-style prompting. Supported language: English.

## Output

- **Output Type(s):** Text
- **Output Format:** String
- **Output Parameters:** One-Dimensional (1D): Sequences
- **Other Properties Related to Output:** Up to 4,096 tokens total (prompt plus generation). Text is generated in parallel blocks (default 64 tokens per block) with a configurable number of denoising steps per block (Number of Function Evaluations (NFE) = steps + 1 per block); fewer steps give faster generation at some quality cost.

Our AI models are designed and/or optimized to run on NVIDIA GPU-accelerated systems. By leveraging NVIDIA's hardware (e.g. GPU cores) and software frameworks (e.g., CUDA libraries), the model achieves faster training and inference times compared to CPU-only solutions.

## Software Integration

- **Runtime Engine(s):** PyTorch (>= 2.4) with Hugging Face Transformers (>= 4.55), loading this repository's inference code via `trust_remote_code`
- **Supported Hardware Microarchitecture Compatibility:** NVIDIA Ampere, NVIDIA Blackwell, NVIDIA Hopper, NVIDIA Lovelace
- **Preferred/Supported Operating System(s):** Linux

Run the model on a CUDA-capable NVIDIA GPU in bfloat16. CPU inference is not
supported: the diffusion sampler is numerically degraded on CPU and produces
unusable output.

The integration of foundation and fine-tuned models into AI systems requires additional testing using use-case-specific data to ensure safe and effective deployment. Following the V-model methodology, iterative testing and validation at both unit and system levels are essential to mitigate risks, meet technical and functional requirements, and ensure compliance with safety and ethical standards before deployment.

## Model Version(s)

- v1.0

## Environment

```bash
torch>=2.4
transformers>=4.55
```

A CUDA-capable NVIDIA GPU is required (bfloat16); CPU inference is not supported.

## Generate with This Model

```python
import torch
from transformers import AutoModel, AutoTokenizer

repo = "nvidia/Nemotron-Labs-Sigma-8B"
tokenizer = AutoTokenizer.from_pretrained(repo, trust_remote_code=True)
model = AutoModel.from_pretrained(repo, trust_remote_code=True)
model = model.cuda().to(torch.bfloat16).eval()

prompt = "The capital of France is"
input_ids = tokenizer(prompt, return_tensors="pt").input_ids.cuda()

out_ids, nfe = model.generate(
    input_ids,
    max_new_tokens=128,
    sampler="ddim",           # recommended (DDPM degenerates at low steps)
    time_schedule="log_snr",  # noise grid used by the internal evals
    steps=32,                 # denoising steps per 32-token block
    block_length=32,          # tokens decoded in parallel
    guidance_scale=3.0,       # classifier-free guidance
    score_temp=0.3,           # see the table below for other step counts
)
print(tokenizer.decode(out_ids[0, input_ids.shape[1]:], skip_special_tokens=True))
print(f"[Number of Function Evaluations (NFE)={nfe}]")
```

### Recommended sampler settings

Per-budget settings follow the paper's few-step results table and apply to **both model sizes,
base and instruct**. Use the DDIM sampler on the `log_snr` grid with 32-token blocks; lower step
counts need stronger score temperature to stay stable.

| Denoising steps | Classifier-free guidance | Score temperature |
|---|---|---|
| DDIM-32 | 3 | 0.3 |
| DDIM-16 | 3 | 0.4 |
| DDIM-8 | 3 | 0.6 |
| DDIM-4 | 2 | 0.8 |

Below roughly 16 steps the pretrained models lose quality noticeably; for few-step generation
prefer the distilled `-distill-*` variants, which are trained for a fixed step count and need
neither guidance nor score-temperature tuning.

## Evaluation Results

Benchmark results for this model family, averaged over multiple generation
seeds, are reported in the technical report:
[Large Language Continuous Diffusion Models](https://arxiv.org/abs/2610.02665).

## Training, Testing, and Evaluation Datasets

### Training Dataset

- **Data Modality:** Text
- **Text Training Data Size:** 1 Trillion to 10 Trillion Tokens
- **Data Collection Method by dataset:** Hybrid: Automated, Manually-Collected
- **Labeling Method by dataset:** Hybrid: Automated, Manually-Labeled

**Properties:** The model was trained on an internal NVIDIA text corpus of approximately 1.3 trillion
tokens in total (about 1 trillion tokens of autoregressive initialization followed by about 0.3
trillion tokens of continuous-diffusion training). The corpus consists of curated English text from
webpages, articles, dialogue, code, and other written materials spanning domains such as math,
science, legal, and finance. It is the same training corpus used for the released
Nemotron-Labs-Diffusion model family; the training data is not distributed.

### Testing Dataset

- **Data Collection Method by dataset:** Hybrid: Automated, Manually-Collected
- **Labeling Method by dataset:** Hybrid: Automated, Manually-Labeled

**Properties:** Held-out splits of the training corpus and public benchmark suites were used for
testing during development. These comprise English text covering reasoning, math, and code tasks.

### Evaluation Dataset

- **Data Collection Method by dataset:** Hybrid: Automated, Manually-Collected
- **Labeling Method by dataset:** Hybrid: Automated, Manually-Labeled

**Properties:** Public academic benchmarks for reasoning and code generation: GSM8K (grade-school
math word problems), MBPP and MBPP+ (Python programming problems), and HumanEval (Python code
synthesis). These are English-language benchmark datasets with reference answers or unit tests.

## Inference

- **Acceleration Engine:** PyTorch
- **Test Hardware:** NVIDIA Hopper H100

Measured generation throughput: roughly 120-140 tokens/s for 256 generated tokens with the DDPM
sampler at 32 denoising steps per 64-token block on a single NVIDIA Hopper H100 (bfloat16).

## Ethical Considerations

NVIDIA believes Trustworthy AI is a shared responsibility and we have established policies and practices to enable development for a wide array of AI applications. Developers should work with their internal model team to ensure this model meets requirements for the relevant industry and use case and addresses unforeseen product misuse.

For more detailed information on ethical considerations for this model, please see the Model Card++ [Bias](./model_cards/bias.md), [Explainability](./model_cards/explainability.md), [Safety & Security](./model_cards/safety.md), and [Privacy](./model_cards/privacy.md) Subcards.

Please report model quality, risk, security vulnerabilities or NVIDIA AI Concerns [here](https://www.nvidia.com/en-us/support/submit-security-vulnerability/).

## Citations

```bibtex
@article{nemotronlabssigma2026,
  title       = {Large Language Continuous Diffusion Models},
  author      = {Zhihan Yang and Wei Guo and Jean-Marie Lemercier and Simon Welker and
                 Mohammad Mahdi Kamani and Yonggan Fu and Sajad Norouzi and Julius Berner and
                 Tomas Geffner and Karsten Kreis and Yongxin Chen and Molei Tao and
                 John Thickstun and Pavlo Molchanov and Ante Juki{\'c} and Arash Vahdat and
                 Morteza Mardani},
  journal     = {arXiv preprint arXiv:2610.02665},
  year        = {2026},
  url         = {https://arxiv.org/abs/2610.02665}
}
```
