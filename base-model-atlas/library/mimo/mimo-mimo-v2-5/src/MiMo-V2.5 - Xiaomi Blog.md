---
title: "MiMo-V2.5 | Xiaomi"
source: "https://mimo.xiaomi.com/mimo-v2-5/"
author:
published: 2026-04-22
created: 2026-06-11
description:
tags:
  - "clippings"
---
## Introducing MiMo-V2.5

Today, we are releasing MiMo-V2.5, a major step forward in agentic capability and multimodal understanding. With native visual and audio understanding, MiMo-V2.5 reasons seamlessly across modalities, surpasses MiMo-V2-Pro in agentic performance, and supports up to 1 million tokens of context.

MiMo-V2.5 is a 310B-parameter Sparse MoE model (15B active) trained on 48T tokens. Its language backbone inherits from [MiMo-V2-Flash](https://github.com/XiaomiMiMo/MiMo-V2-Flash) 's hybrid sliding-window attention architecture, augmented with dedicated visual and audio encoders (both pretrained in-house) connected through lightweight projectors.

![MiMo-V2.5 architecture diagram](https://mimo.xiaomi.com/mimo-v2-5/assets/architecture.svg)

MiMo-V2.5 architecture.

Training goes through five stages: *text pre-training* on diverse corpora to build the LLM backbone; *projector warmup* to align the audio and visual projectors with the language model; *multimodal pre-training* at scale on high-quality cross-modal data; *supervised fine-tuning and agentic post-training*, during which the context window is progressively extended from 32K to 256K to 1M; and finally *RL and [MOPD](https://arxiv.org/html/2601.02780v2#S4)*, which further strengthens perception, reasoning, and agentic capabilities.

Together, these stages yield a single model that sees, hears, and acts on what it perceives — one that understands everything and gets things done.

---

## Best-in-Class Agency

On the agentic benchmarks that matter most for real-world deployment, MiMo-V2.5 delivers best-in-class performance:

MiMo-V2.5 MiMo-V2-Pro Kimi K2.6 DeepSeek-V4-Flash Claude Opus 4.6 Gemini 3.1 Pro GPT-5.4

Coding Agent

Coding

71.8

MiMo-V2.5: 71.8

71.5

MiMo-V2-Pro: 71.5

77.1

Claude Opus 4.6: 77.1

67.8

Gemini 3.1 Pro: 67.8

MiMo Coding Bench

62.3

MiMo-V2.5: 62.3

57.8

MiMo-V2-Pro: 57.8

62.3

Kimi K2.6: 62.3

57.8

DeepSeek-V4-Flash: 57.8

70.8

Claude Opus 4.6: 70.8

57.8

Gemini 3.1 Pro: 57.8

60.3

GPT-5.4: 60.3

Claw-Eval Text

65.8

MiMo-V2.5: 65.8

57.1

MiMo-V2-Pro: 57.1

66.7

Kimi K2.6: 66.7

56.9

DeepSeek-V4-Flash: 56.9

65.4

Claude Opus 4.6: 65.4

68.5

Gemini 3.1 Pro: 68.5

Terminal-Bench 2.0

56.1

MiMo-V2.5: 56.1

55.0

MiMo-V2-Pro: 55.0

58.6

Kimi K2.6: 58.6

52.6

DeepSeek-V4-Flash: 52.6

57.3

Claude Opus 4.6: 57.3

54.2

Gemini 3.1 Pro: 54.2

57.7

GPT-5.4: 57.7

SWE-Bench Pro

In our internal **MiMo Coding Bench**, MiMo-V2.5 delivers strong results on everyday coding tasks, closing the gap with frontier models and matching MiMo-V2.5-Pro at half the cost.

On **Claw-Eval**, a benchmark for daily agentic tasks, MiMo-V2.5 achieves a 62.3 on the general subset, placing it at the Pareto frontier of performance and efficiency.

These results highlight what makes MiMo-V2.5 unique: frontier-level agentic capability with high token efficiency.

## Sharper Perception, Longer Horizon

MiMo-V2.5 delivers sharper perception for precise visual reasoning, complex chart analysis, and deep multimodal understanding, with native support for up to 1 million tokens of context.

MiMo-V2.5 MiMo-V2-Omni Kimi K2.6 Claude Opus 4.6 Claude Sonnet 4.6 Gemini 3 Pro GPT-5.4

Image Understanding

81.0

MiMo-V2.5: 81.0

80.1

MiMo-V2-Omni: 80.1

80.4

Kimi K2.6: 80.4

77.4

Claude Opus 4.6: 77.4

81.4

Gemini 3 Pro: 81.4

CharXiv RQ

77.9

MiMo-V2.5: 77.9

76.8

MiMo-V2-Omni: 76.8

79.4

Kimi K2.6: 79.4

73.9

Claude Opus 4.6: 73.9

81.0

Gemini 3 Pro: 81.0

81.2

GPT-5.4: 81.2

MMMU-Pro

88.5

MiMo-V2.5: 88.5

83.3

MiMo-V2-Omni: 83.3

86.4

Gemini 3 Pro: 86.4

HR-Bench (4k)

87.2

MiMo-V2.5: 87.2

86.7

MiMo-V2-Omni: 86.7

89.0

GPT-5.4: 89.0

OmniDocBench

Multimodal Agent

Video Understanding

23.8

MiMo-V2.5: 23.8

15.8

MiMo-V2-Omni: 15.8

18.8

Kimi K2.6: 18.8

24.8

Claude Opus 4.6: 24.8

23.8

Claude Sonnet 4.6: 23.8

25.7

GPT-5.4: 25.7

Claw-Eval Multimodal

87.7

MiMo-V2.5: 87.7

85.3

MiMo-V2-Omni: 85.3

88.4

Gemini 3 Pro: 88.4

Video-MME

83.5

MiMo-V2.5: 83.5

80.5

MiMo-V2-Omni: 80.5

84.2

Gemini 3 Pro: 84.2

DailyOmni

64.0

MiMo-V2.5: 64.0

59.5

MiMo-V2-Omni: 59.5

64.2

Gemini 3 Pro: 64.2

VideoHolmes

Across image, video, and multimodal agentic tasks, MiMo-V2.5 stays level with frontier closed-source models — matching Gemini 3 Pro on video, Claude Sonnet 4.6 on multimodal agentic work, and staying competitive across image and document understanding. All from one unified model.

## Open Source

The MiMo-V2.5 series is now fully open-sourced. Weights, tokenizer, and the full model card are available on Hugging Face.

| Model | Total Params | Active Params | Context | Precision | Download |
| --- | --- | --- | --- | --- | --- |
| MiMo-V2.5-Base | 310B | 15B | 256K | FP8 (E4M3) Mixed | [Hugging Face](https://huggingface.co/XiaomiMiMo/MiMo-V2.5-Base) |
| MiMo-V2.5 | 310B | 15B | 1M | FP8 (E4M3) Mixed | [Hugging Face](https://huggingface.co/XiaomiMiMo/MiMo-V2.5) |

## Token Plan Update

Alongside stronger models, your Token Plan gets better too. Rates are now simpler and lower:

- **MiMo-V2.5** — 1x (1 token = 1 credit)
- **MiMo-V2.5-Pro** — 2x (1 token = 2 credits)

From today onward, Token Plans no longer charge a multiplier for the 1M-token context window. [Order your Token Plan now](https://platform.xiaomimimo.com/docs/tokenplan/subscription).

## What's Next

MiMo-V2.5 brings frontier agency and native multimodality into the same model, at a price point that makes both practical for production. We are already training the next generation with deeper reasoning, tighter tool integration, and richer real-world grounding. In the meantime, [try it in AI Studio](https://aistudio.xiaomimimo.com/) or [access the API](https://platform.xiaomimimo.com/) — we cannot wait to see what you build.
