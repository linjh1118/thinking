---
title: "OpenAI · GPT — Series Summary"
type: model-note
tags: [model-note, base-model, series, openai]
created: 2026-08-31
updated: 2026-09-04
---

# OpenAI · GPT — Series Summary

> [!tldr]
> 从通用 next-token scaling 走向统一 reasoning、工具调用与专业工作基座。

## 主干时间线

| 时间 | 模型 | 关键变化 | 一手来源 |
|---|---|---|---|
| 2018-06 | GPT-1 | 生成式预训练证明统一语言建模可迁移。 | [Official release](https://openai.com/index/language-unsupervised/) |
| 2019-02 | GPT-2 | 规模、WebText 与 zero-shot 能力开始联动。 | [Official release](https://openai.com/index/better-language-models/) |
| 2020-05 | GPT-3 | few-shot prompting 成为通用接口。 | [Technical report](https://arxiv.org/abs/2005.14165) |
| 2022-11 | GPT-3.5 | 指令对齐与对话产品化形成规模效应。 | [Official release](https://openai.com/index/chatgpt/) |
| 2023-03 | GPT-4 | 多模态与高可靠复杂任务能力跃迁。 | [Official release](https://openai.com/research/gpt-4) |
| 2024-05 | GPT-4o | 原生 omni 交互与低时延统一。 | [Official release](https://openai.com/index/hello-gpt-4o/) |
| 2025-08 | GPT-5 | reasoning、fast path 与工具能力统一。 | [Official docs](https://developers.openai.com/api/docs/models/gpt-5) |
| 2025-11 | GPT-5.1 | 强化 coding 与 agentic task。 | [Official docs](https://developers.openai.com/api/docs/models/gpt-5.1) |
| 2025-12 | GPT-5.2 | 面向专业工作的可配置推理旗舰。 | [Official docs](https://developers.openai.com/api/docs/models/gpt-5.2) |
| 2026-03 | GPT-5.4 | 1.05M context 与 computer use 进入通用旗舰。 | [Official docs](https://developers.openai.com/api/docs/models/gpt-5.4) |
| 2026-04 | GPT-5.5 | 复杂 coding 与专业工作质量上移。 | [Official docs](https://developers.openai.com/api/docs/models/gpt-5.5) |
| 2026-08 | GPT-5.6 Sol | Sol / Terra / Luna 分层，旗舰统一到 1.05M context。 | [Official docs](https://developers.openai.com/api/docs/models/gpt-5.6-sol) |
| 2026-09 | GPT-6 Astra | 异步工具、过程 steering、跨 context 状态与 Critical cyber capability，把主线推向跨软件长时程执行。 | [Launch page](https://openai.com/index/gpt-6-astra/) |

## 编辑判断

- 这里只收主干正代与改变路线的关键节点，不把每个尺寸、API snapshot 或专项 SKU 拆成正代。
- 训练数据、参数和消融只在官方技术报告明确披露时记录；闭源发布不做架构猜测。
- 当前旗舰详见 [[2609_GPT_6_Astra/GPT-6-Astra|GPT-6 Astra]]。
