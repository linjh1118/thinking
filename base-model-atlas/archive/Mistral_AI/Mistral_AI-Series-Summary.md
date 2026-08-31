---
title: "Mistral AI — Series Summary"
type: model-note
tags: [model-note, base-model, series, mistral-ai]
created: 2026-08-31
updated: 2026-08-31
---

# Mistral AI — Series Summary

> [!tldr]
> 欧洲开放模型路线：稀疏 MoE、轻量部署、multimodal 与 agentic coding。

## 主干时间线

| 时间 | 模型 | 关键变化 | 一手来源 |
|---|---|---|---|
| 2023-09 | Mistral 7B | 小尺寸开放模型的效率标杆。 | [Official release](https://mistral.ai/news/announcing-mistral-7b) |
| 2023-12 | Mixtral 8x7B | 稀疏 MoE 以较低激活参数提升能力。 | [Official release](https://mistral.ai/news/mixtral-of-experts) |
| 2024-02 | Mistral Large | 首代闭源旗舰进入复杂任务。 | [Official release](https://mistral.ai/news/mistral-large) |
| 2024-07 | Mistral Large 2 | 128K、多语言与 function calling。 | [Official release](https://mistral.ai/news/mistral-large-2407) |
| 2025-05 | Mistral Medium 3 | multimodal 与 enterprise cost/performance。 | [Official release](https://mistral.ai/news/mistral-medium-3) |
| 2025-08 | Mistral Medium 3.1 | 长任务、同步 tool calling 与 agentic coding。 | [Official release](https://mistral.ai/models/) |
| 2025-12 | Mistral Large 3 | 开放权重通用多模态旗舰。 | [Official release](https://mistral.ai/models/) |
| 2026-03 | Mistral Small 4 | 统一 reasoning、multimodal 与 agentic coding。 | [Official release](https://mistral.ai/news/mistral-small-4/) |

## 编辑判断

- 这里只收主干正代与改变路线的关键节点，不把每个尺寸、API snapshot 或专项 SKU 拆成正代。
- 训练数据、参数和消融只在官方技术报告明确披露时记录；闭源发布不做架构猜测。
- 当前旗舰详见 [[2512_Mistral_Large_3/Mistral-Large-3|Mistral Large 3]]。
