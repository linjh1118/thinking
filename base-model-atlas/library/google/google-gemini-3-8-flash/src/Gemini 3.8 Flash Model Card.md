# Gemini 3.8 Flash — Official Model Card 阅读版

> 官方原页：<https://deepmind.google/models/model-cards/gemini-3-8-flash/>
>
> 发布时间：2026-09-02
>
> 本文件是便于 Obsidian 与静态站阅读的结构化摘录；原始 HTML 快照保存在同目录。

![Official evaluation matrix](assets/official-evals.jpg)

## Model information

- **Description**: Gemini 3.8 Flash is the next iteration in the Gemini 3 family. It builds on Gemini 3.7 Flash and advances software engineering and agentic knowledge workflows.
- **Dependency / architecture**: based on Gemini 3.7 Flash; architecture details defer to the 3.7 Flash model card.
- **Inputs**: text, images, audio and video, with up to 1M-token context.
- **Outputs**: text, with up to 64K tokens.
- **Effort control**: configurable effort levels trade quality against cost and latency.

## Distribution

Google lists Gemini app, Gemini Enterprise Agent Platform, Google AI Studio, Gemini API, Google AI Mode and Google Antigravity as distribution channels.

## Intended usage

The model targets cost-effective, general-purpose production agents, especially software engineering, agent tasks and complex knowledge workflows.

## Selected evaluation results

| Evaluation | Gemini 3.8 Flash | Gemini 3.7 Flash |
|---|---:|---:|
| DeepSWE v1.1 | 73.7% | 65.3% |
| Terminal-bench 2.1 | 89.4% | 85.8% |
| Terminal-bench 4.0 | 19.1% | 11.2% |
| OSWorld-2.0 | 59.0% | 50.6% |
| Vals Finance Agent v2 | 61.4% | 59.0% |
| BioMysteryBench · Human Difficult | 56.5% | 43.5% |
| LABBench2 | 86.2% | 82.1% |
| HLE-Verified | 54.9% | 53.6% |

The official chart lists an introductory price of $0.75 per million input tokens and $3.75 per million output tokens through 2026-12-31, followed by regular prices of $1.50 and $7.50.

## Limitations

- Foundation-model limitations such as hallucinations remain.
- Higher effort may consume more tokens.
- Occasional slowness or timeouts may occur.
- Knowledge cutoff is March 2026, but some domains may remain limited to January 2025.

## Safety summary

Compared with Gemini 3.7 Flash, text-to-text safety changes by -0.4pp, multilingual safety by +5.4pp, image-to-text safety by 0.0pp, tone by +0.2pp and unjustified refusals by +1.1pp. Lower is better for the safety and refusal measures; Google explicitly notes a slight multilingual-safety regression.

Specialist manual red teaming found no egregious concerns, and child-safety launch thresholds were met. Google states that 3.8 Flash has no meaningful new capabilities or material increase relative to 3.7 Flash in the Frontier Safety Framework domains and is therefore also unlikely to reach tracked or critical capability levels.
