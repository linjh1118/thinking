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

# Nemotron-Labs-Sigma-distill-spec-3B

## Model Overview

## Description

Nemotron-Labs-Sigma-distill-spec-3B is a 3 billion-parameter continuous diffusion language model trained
for **self-speculative decoding**. It was produced by Phased Distribution
Matching Distillation (Phased DMD) from a multiscale SUSReg-regularized 3B
teacher of the same Nemotron-Labs-Sigma architecture family (MS-SUSReg-3B),
then continued with an LK acceptance objective ("X25") so that its one-call diffusion
draft is accepted more often by its own AR path.

Unlike the `-distill-*` siblings, which are deployed as pure few-step
blockwise diffusion samplers, this checkpoint is trained so that its diffusion
head drafts a block of 32 tokens that its own autoregressive
head then verifies. Each drafting round costs
1 diffusion call, and accepted tokens are
emitted without a further forward pass. Both heads are therefore required and
both are shipped in this repository.

Self-conditioning is **off**: the underlying distilled student was trained SC-off,
and the one-call draft never self-conditions, as in serving.

This model is ready for commercial or non-commercial use.

## License/Terms of Use

Use of this model is governed by the
[NVIDIA Nemotron Open Model License](https://www.nvidia.com/en-us/agreements/enterprise-software/nvidia-nemotron-open-model-license/).

## Release Date

- Hugging Face 11/12/2026 via https://huggingface.co/nvidia/Nemotron-Labs-Sigma-distill-spec-3B

## References

- [Large Language Continuous Diffusion Models](https://arxiv.org/abs/2610.02665) (arXiv:2610.02665, 2026).

## Model Architecture

- **Architecture Type:** Continuous diffusion language model (decoder-only backbone)
- **Network Architecture:** Nemotron-Labs-Sigma (26 layers,
  hidden size 3072, FFN 9216,
  32 query / 8 key-value heads,
  head dim 128, RMSNorm, SwiGLU, YaRN RoPE)
- **Token embedding space:** 16-dimensional continuous
- **Noise schedule:** monotone degree-32 Bernstein (Bezier) map
  with learned gamma endpoints [-5.4150, 4.8549]
- **Heads:** diffusion head (drafting) + autoregressive head (verification)
- **Parameters:** ~3B

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
- Student step: 600 (uniform weight average of P34 and P35, 600 updates each)
- Source export sha256: `fe2880f02d0fe9ed`

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

> Self-speculative decoding is measured by **mean accepted length (AL) per
> verification round, excluding the bonus token** (higher is better; it is a
> throughput measure, not an accuracy measure): a round commits AL+1 tokens.
> The AR bootstrap round is excluded, and the test sets are restricted to the
> prompts on which neither model loops nor hits the generation cap, so the
> prompt counts below are smaller than the full benchmark sizes.
> Note that the `distill-spec-8B` card reports a **bonus-inclusive** AL on the
> full prompt sets; the two numbers are not directly comparable.
> Single evaluation snapshot from the release handoff.

| Benchmark | Prompts | Mean accepted length | Speedup over AR |
|---|---|---|---|
| GSM8K (CoT) | 1303 | 10.49 | 3.28x |
| HumanEval | 158 | 7.90 | 2.61x |
| MBPP | 499 | 9.21 | 2.61x |
| SPEED-Bench | 703 | 5.25 | 1.98x |

Accepted lengths are paired against the pre-acceptance-training Phased-DMD4 student over the prompts that neither model loops or caps on; acceptance training raises them by 14.9%, 14.1% and 15.4% on GSM8K, HumanEval and MBPP. Speedups are throughput relative to this model's own autoregressive decoding, measured with SGLang in BF16 on one NVIDIA GB200, one request at a time. AR-decoding accuracy is unchanged by acceptance training.

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
