---
title: "DeepSeek AI — Series Summary"
type: model-note
tags: [model-note, base-model, series, deepseek-ai]
created: 2026-08-31
updated: 2026-08-31
---

# DeepSeek AI — Series Summary

> [!tldr]
> MLA/MoE 训练效率、开放 reasoning RL 与 agentic tool-use 是三条主轴。

## 主干时间线

| 时间 | 模型 | 关键变化 | 一手来源 |
|---|---|---|---|
| 2024-01 | DeepSeek LLM | 开放 dense 基模与训练 recipe 起点。 | [Official repo / model card](https://github.com/deepseek-ai/DeepSeek-LLM) |
| 2024-05 | DeepSeek-V2 | MLA + DeepSeekMoE 显著降低训练/推理成本。 | [Official repo / model card](https://github.com/deepseek-ai/DeepSeek-V2) |
| 2024-09 | DeepSeek-V2.5 | 通用与 coder 模型合并。 | [Official docs](https://api-docs.deepseek.com/news/news0905) |
| 2024-12 | DeepSeek-V3 | 671B/37B active、14.8T tokens 与 FP8 训练。 | [Official docs](https://api-docs.deepseek.com/news/news1226) |
| 2025-01 | DeepSeek-R1 | 大规模 RL 与极少标注的开放 reasoning 路线。 | [Official docs](https://api-docs.deepseek.com/news/news250120/) |
| 2025-08 | DeepSeek-V3.1 | hybrid inference 与 agent/tool-use 后训练。 | [Official docs](https://api-docs.deepseek.com/news/news250821/) |
| 2025-12 | DeepSeek-V3.2 | DSA 与 thinking-in-tool-use。 | [Official docs](https://api-docs.deepseek.com/news/news251201/) |
| 2026-04 | DeepSeek-V4 | Pro / Flash 分层并原生适配 agent API。 | [Official docs](https://api-docs.deepseek.com/updates/) |
| 2026-08 | DeepSeek-V4 Pro | GA 版本强化 production agent 与 Responses API。 | [Official docs](https://api-docs.deepseek.com/updates/) |

## 编辑判断

- 这里只收主干正代与改变路线的关键节点，不把每个尺寸、API snapshot 或专项 SKU 拆成正代。
- 训练数据、参数和消融只在官方技术报告明确披露时记录；闭源发布不做架构猜测。
- 当前旗舰详见 [[2608_DeepSeek_V4_Pro/DeepSeek-V4-Pro|DeepSeek-V4-Pro]]。
