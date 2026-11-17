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

# Nemotron-Labs-Sigma-distill-spec-8B

## Model Overview

## Description

Nemotron-Labs-Sigma-distill-spec-8B is an 8 billion-parameter continuous diffusion language model trained
for **self-speculative decoding**. It was produced by Phased Distribution
Matching Distillation (Phased DMD) from a multiscale SUSReg-regularized 8B
teacher bank of the same Nemotron-Labs-Sigma architecture family
(MS-SUSReg-8B), then further trained with an acceptance objective (X3) that directly optimizes how many
drafted tokens the verifier accepts.

Unlike the `-distill-*` siblings, which are deployed as pure few-step
blockwise diffusion samplers, this checkpoint is trained so that its diffusion
head drafts a block of 32 tokens that its own autoregressive
head then verifies. Each drafting round costs
1 diffusion call, and accepted tokens are
emitted without a further forward pass. Both heads are therefore required and
both are shipped in this repository.

Self-conditioning is **off** for this model (it was trained SC-off); do not
enable it at inference.

This model is ready for commercial or non-commercial use.

## License/Terms of Use

Use of this model is governed by the
[NVIDIA Nemotron Open Model License](https://www.nvidia.com/en-us/agreements/enterprise-software/nvidia-nemotron-open-model-license/).

## Release Date

- Hugging Face 11/12/2026 via https://huggingface.co/nvidia/Nemotron-Labs-Sigma-distill-spec-8B

## References

- [Large Language Continuous Diffusion Models](https://arxiv.org/abs/2610.02665) (arXiv:2610.02665, 2026).

## Model Architecture

- **Architecture Type:** Continuous diffusion language model (decoder-only backbone)
- **Network Architecture:** Nemotron-Labs-Sigma (34 layers,
  hidden size 4096, FFN 14336,
  32 query / 8 key-value heads,
  head dim 128, RMSNorm, SwiGLU, YaRN RoPE)
- **Token embedding space:** 16-dimensional continuous
- **Noise schedule:** monotone degree-32 Bernstein (Bezier) map
  with learned gamma endpoints [-5.0565, 4.907]
- **Heads:** diffusion head (drafting) + autoregressive head (verification)
- **Parameters:** ~8B

## Input

- **Input Type(s):** Text
- **Input Format:** String
- **Input Parameters:** One-Dimensional (1D): Sequences
- **Other Properties Related to Input:** Up to 4096 tokens total.

## Output

- **Output Type(s):** Text
- **Output Format:** String
- **Output Parameters:** One-Dimensional (1D): Sequences
- **Other Properties Related to Output:** Up to 4096 tokens
  total. Tokens are drafted in blocks of 32 and accepted by the
  model's own AR head; the number of tokens emitted per round is data dependent.

## Software Integration

- **Runtime Engine(s):** PyTorch (>= 2.4) with Hugging Face Transformers (>= 4.55),
  loading this repository's inference code via `trust_remote_code`
- **Supported Hardware:** NVIDIA GPU-accelerated systems (bfloat16). CPU
  inference is not supported.

## Model Version(s)

- Native NFE: 2
- Student step: 600 (uniform weight average of S8A and S8B at update 600)
- Source export sha256: `abd1d35278e0f7e0`

### Self-speculative decoding

The diffusion head drafts a block, the model's own AR head verifies it, and the
returned text is **exactly the greedy autoregressive output** -- acceptance changes
only how many tokens each round commits, never which tokens. Both heads ship in
this repository and both are required.

```python
out_ids, stats = model.generate_speculative(
    input_ids,
    max_new_tokens=256,
    return_stats=True,        # rounds, accepted, mean_accepted_length
)
print(tokenizer.decode(out_ids[0, input_ids.shape[1]:], skip_special_tokens=True))
print(f"[mean accepted length = {stats['mean_accepted_length']:.2f}]")
```

`draft_width` and `diffusion_calls_per_round` default to this checkpoint's trained
contract (see `generation_config.json`); drafts never use self-conditioning or
guidance, matching how the model was trained and served.

## Evaluation Results

> Self-speculative decoding is measured by **mean accepted length per
> verification round, including the bonus token** (higher is better; it is a
> throughput measure, not an accuracy measure). The AR bootstrap round is
> excluded. Single evaluation snapshot from the release handoff.

| Benchmark | Prompts | Mean accepted length |
|---|---|---|
| HumanEval | 164 | 7.91 |
| GSM8K (CoT) | 1319 | 11.86 |
| MBPP | 500 | 13.37 |

Selection: User-selected step-600 bank SoftCE SC-off SelfSpec checkpoint; GSM8K accepted length is its within-arm maximum among completed steps 100-600.

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
