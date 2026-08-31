---
title: "Microsoft · Phi — Series Summary"
type: model-note
tags: [model-note, base-model, series, microsoft]
created: 2026-08-31
updated: 2026-08-31
---

# Microsoft · Phi — Series Summary

> [!tldr]
> 用高质量合成数据把复杂 reasoning 压进小模型。

## 主干时间线

| 时间 | 模型 | 关键变化 | 一手来源 |
|---|---|---|---|
| 2023-06 | Phi-1 | textbook-quality data 验证小模型 scaling。 | [Official release](https://www.microsoft.com/en-us/research/publication/textbooks-are-all-you-need/) |
| 2023-12 | Phi-2 | 2.7B 小模型的数据质量路线。 | [Official release](https://www.microsoft.com/en-us/research/blog/phi-2-the-surprising-power-of-small-language-models/) |
| 2024-04 | Phi-3 | 端侧可部署的小语言模型 family。 | [Official release](https://azure.microsoft.com/en-us/blog/introducing-phi-3-redefining-whats-possible-with-slms/) |
| 2024-12 | Phi-4 | 14B 模型在 STEM reasoning 超越 teacher。 | [Official release](https://www.microsoft.com/en-us/research/publication/phi-4-technical-report/) |
| 2025-07 | Phi-4 Reasoning | SFT + RL 的高效复杂推理。 | [Official release](https://www.microsoft.com/en-us/research/articles/phi-reasoning-once-again-redefining-what-is-possible-with-small-and-efficient-ai/) |
| 2026-03 | Phi-4 Reasoning Vision | 15B 混合 reasoning/non-reasoning 多模态模型。 | [Official release](https://www.microsoft.com/en-us/research/blog/phi-4-reasoning-vision-and-the-lessons-of-training-a-multimodal-reasoning-model/) |

## 编辑判断

- 这里只收主干正代与改变路线的关键节点，不把每个尺寸、API snapshot 或专项 SKU 拆成正代。
- 训练数据、参数和消融只在官方技术报告明确披露时记录；闭源发布不做架构猜测。
- 当前旗舰详见 [[2603_Phi_4_Reasoning_Vision/Phi-4-Reasoning-Vision|Phi-4 Reasoning Vision]]。
