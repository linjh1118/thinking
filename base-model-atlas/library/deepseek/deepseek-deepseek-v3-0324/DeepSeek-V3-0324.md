---
title: "DeepSeek-V3-0324 — DeepSeek 主线精读"
type: model-note
authors: ["DeepSeek-AI"]
year: 2025
venue: "Official release / model card"
url: "https://api-docs.deepseek.com/news/news250325/"
tags: [model-note, base-model, deepseek, mainline]
status: read
rating: 5
topic: "13_base_model"
created: 2026-08-31
updated: 2026-08-31
---

# DeepSeek-V3-0324 — DeepSeek 主线精读

> [!tldr]
> 0324 是 V3 的关键 post-training checkpoint：没有换架构，却大幅抬高推理、前端、中文写作与函数调用，是“同底座能力迁移”的清晰样本。

## 谱系定位

- 发布时间：**2025-03**
- 团队：**DeepSeek AI**
- Atlas 口径：**主线正代 / 关键主部署 checkpoint**
- 官方入口：[一手发布页](https://api-docs.deepseek.com/news/news250325/)

0324 是 V3 的关键 post-training checkpoint：没有换架构，却大幅抬高推理、前端、中文写作与函数调用，是“同底座能力迁移”的清晰样本。

## 关键规格与证据

| 指标 | 含义 |
|---|---|
| 81.2 | MMLU-Pro |
| 68.4 | GPQA |
| 59.4 | AIME |
| 49.2 | LiveCodeBench |

> [!note]
> 表中数字只采用本目录 `src/` 保存的官方发布页、模型卡或技术报告；内部榜单和服务价格只用于理解发布语境，不外推为独立复现实验。

## 架构：这一代改了什么

模型结构仍为 V3 的 671B/37B MLA + DeepSeekMoE；官方没有声称新的预训练架构。更新集中在后训练、行为对齐与产品工作流，权重改为 MIT license。

## 数据、训练与后训练

公开材料不披露数据配比，但结果覆盖推理、前端代码可执行性/美观度、中文中长文、翻译与多轮改写、搜索报告和 function calling。API 对 temperature 做映射，使常用 API 值 1.0 对应模型温度 0.3。

## 结果应该怎样读

- MMLU-Pro：75.9 → 81.2；GPQA：59.1 → 68.4。
- AIME：39.6 → 59.4；LiveCodeBench：39.2 → 49.2。
- 这四项是同一 V3 底座上的版本差异，不能归因于参数扩大。

这里最重要的不是把不同年份的 benchmark 横向拼成排行榜，而是识别同一团队相邻 checkpoint 的变量：架构、预训练规模、post-training、推理预算、工具环境和服务接口分别改变了什么。

## 对 Agent Training 的启发

> [!insight]
> 对 agent 模型，checkpoint audit 必须把 tool-use、代码可执行性和语言一致性作为独立维度；单一 reasoning 分数无法代表能否稳定接入真实工作流。

## 局限与证据边界

缺少独立技术报告与训练消融，无法判断各项收益对应哪种数据或算法；前端与写作提升主要是官方定性评价。

## 本地一手资料

本目录已保存原始官方 HTML/Markdown、模型卡，以及可获得的论文源码或技术报告。`retrieval_manifest.json` 记录 URL、抓取日期、字节数和 SHA-256，便于日后核验网页是否变化。

- [[src/assets|assets/]]
- [[src/official_model_card.md|official_model_card.md]]
- [[src/official_release.html|official_release.html]]
- [[src/official_release.md|official_release.md]]
- [[src/retrieval_manifest.json|retrieval_manifest.json]]

## 导航

- 上一代：[[Topics/13_base_model/DeepSeek_AI/2501_deepseek_r1/DeepSeek-R1|DeepSeek-R1]]
- 下一代：[[Topics/13_base_model/DeepSeek_AI/2505_deepseek_r1_0528/DeepSeek-R1-0528|DeepSeek-R1-0528]]
- 系列总览：[[Topics/13_base_model/DeepSeek_AI/DeepSeek_AI-Series-Summary|DeepSeek AI Series Summary]]
- 中文 Poster：[[Topics/13_base_model/DeepSeek_AI/2503_deepseek_v3_0324/deepseek_v3_0324_poster_zh.html|DeepSeek-V3-0324 Poster]]
