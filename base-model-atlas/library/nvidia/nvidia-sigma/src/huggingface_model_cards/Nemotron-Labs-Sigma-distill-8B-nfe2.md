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

# Nemotron-Labs-Sigma-distill-8B-nfe2

## Model Overview

## Description

Nemotron-Labs-Sigma-distill-8B-nfe2 is an 8 billion-parameter continuous diffusion language
model distilled for fast few-step generation. It was produced with Phased
Distribution Matching Distillation (Phased DMD) from a multiscale SUSReg-regularized 8B teacher of the same Nemotron-Labs-Sigma architecture family (MS-SUSReg-8B). This is the same MS-SUSReg lineage as the released Nemotron-Labs-Sigma-8B base model.

The student generates a 32-token block in exactly **2 denoising function
evaluations (NFE)** plus one final readout, using the native `fresh_x0` sampler
with self-conditioning carry. The number of denoising steps is fixed by
training: this variant is trained for NFE=2 only, and the bundled inference
code intentionally does not expose an arbitrary step override (other step
counts would evaluate untrained phase endpoints). Sibling variants are
published for NFE = 2, 4, 8 and 16 per model size.

This model is ready for commercial or non-commercial use.

## License/Terms of Use

Use of this model is governed by the [NVIDIA Nemotron Open Model License](https://www.nvidia.com/en-us/agreements/enterprise-software/nvidia-nemotron-open-model-license/).

## Deployment Geography

Global

## Use Case

Researchers and developers who need fast, few-step text generation from
diffusion language models: latency-sensitive generation research, speculative
and parallel decoding studies, and deployment-oriented experimentation. The
model runs offline on the user's own hardware; NVIDIA hosts no service.

## Release Date

- Hugging Face 11/12/2026 via https://huggingface.co/nvidia/Nemotron-Labs-Sigma-distill-8B-nfe2

## References

- [Large Language Continuous Diffusion Models](https://arxiv.org/abs/2610.02665) (arXiv:2610.02665, 2026).

## Model Architecture

- **Architecture Type:** Transformer
- **Network Architecture:** Other: Ministral-style decoder-only Transformer (grouped-query attention, SwiGLU, rotary position embeddings; 34 layers, 4,096 hidden) with a continuous-diffusion generation head (16-D continuous token-embedding space) and a preserved auxiliary AR readout head.
- **Number of model parameters:** 8 billion (8B)
- **This model was developed based on:** Phased DMD distillation of a Nemotron-Labs-Sigma 8B teacher (see Description).

## Input

- **Input Type(s):** Text
- **Input Format(s):** String
- **Input Parameters:** One-Dimensional (1D): Sequences
- **Other Properties Related to Input:** Maximum context length of 4,096 tokens (prompt plus generated tokens). Plain-text prompts; best used with few-shot or benchmark-style prompting. Supported language: English.

## Output

- **Output Type(s):** Text
- **Output Format:** String
- **Output Parameters:** One-Dimensional (1D): Sequences
- **Other Properties Related to Output:** Up to 4,096 tokens total. Text is generated in 32-token blocks; each block costs exactly NFE+1 = 3 denoiser calls. Generation stops at caller-provided stop strings (checked after each completed block) or at the token budget; there is no token-ID EOS stopping.

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

repo = "nvidia/Nemotron-Labs-Sigma-distill-8B-nfe2"
tokenizer = AutoTokenizer.from_pretrained(repo, trust_remote_code=True)
model = AutoModel.from_pretrained(repo, trust_remote_code=True)
model = model.cuda().to(torch.bfloat16).eval()

prompt = "def fibonacci(n):"
input_ids = tokenizer(prompt, return_tensors="pt").input_ids.cuda()

# steps is fixed to the native NFE (2) by the checkpoint; do not override.
out_ids, nfe = model.generate(
    input_ids,
    max_new_tokens=256,
    stop_strings=["\nclass", "\ndef"],  # optional block-level stopping
    tokenizer=tokenizer,
)
print(tokenizer.decode(out_ids[0, input_ids.shape[1]:], skip_special_tokens=True))
print(f"[Number of Function Evaluations (NFE)={nfe}]")
```

## Evaluation Results

> Accuracy in percent, reported as **mean +/- 2 standard errors over 10 generation
> seeds** at the model's native NFE, CFG 1, score temperature 1, 32-token blocks.
> Source: the 10-November restricted-release handoff's verified ten-seed, six-task
> statistics.

| Benchmark | Score (%) |
|---|---|
| GSM8K (CoT) | 80.17 +/- 0.55 |
| MATH (Minerva) | 55.72 +/- 0.31 |
| HumanEval | 48.17 +/- 0.91 |
| HumanEval+ | 45.24 +/- 0.94 |
| MBPP | 37.52 +/- 1.12 |
| MBPP+ | 51.30 +/- 0.96 |
| Six-task mean | 53.02 +/- 0.52 |

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
