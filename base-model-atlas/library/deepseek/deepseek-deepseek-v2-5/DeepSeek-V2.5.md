---
title: "DeepSeek-V2.5 — DeepSeek 主线精读"
type: model-note
authors: ["DeepSeek-AI"]
year: 2024
venue: "Official release / model card"
url: "https://huggingface.co/deepseek-ai/DeepSeek-V2.5"
tags: [model-note, base-model, deepseek, mainline]
status: read
rating: 5
topic: "13_base_model"
created: 2026-08-31
updated: 2026-08-31
---

# DeepSeek-V2.5 — DeepSeek 主线精读

> [!tldr]
> V2.5 不是新架构，而是把通用 Chat 与 Coder 两条权重线合并成一个可服务的统一 checkpoint。

## 谱系定位

- 发布时间：**2024-09**
- 团队：**DeepSeek AI**
- Atlas 口径：**主线正代 / 关键主部署 checkpoint**
- 官方入口：[一手发布页](https://huggingface.co/deepseek-ai/DeepSeek-V2.5)

V2.5 不是新架构，而是把通用 Chat 与 Coder 两条权重线合并成一个可服务的统一 checkpoint。

## 关键规格与证据

| 指标 | 含义 |
|---|---|
| 236B | 沿用 V2 总参数 |
| 21B | 激活参数 |
| 82.6 | 官方安全分 |
| 4.6% | 安全 spillover |

> [!note]
> 表中数字只采用本目录 `src/` 保存的官方发布页、模型卡或技术报告；内部榜单和服务价格只用于理解发布语境，不外推为独立复现实验。

## 架构：这一代改了什么

底座仍是 V2 的 MLA + DeepSeekMoE。更新核心是合并 DeepSeek-V2-Chat-0628 与 DeepSeek-Coder-V2-0724，并通过 alignment 同时保留通用对话、代码、FIM、JSON 与 function calling。

## 数据、训练与后训练

官方把它描述为 general/coder 权重融合与偏好对齐版本，而非从零预训练。更严格的安全边界使安全分从 74.4 提升到 82.6，同时把对正常请求的安全误伤率从 11.3% 降到 4.6%。

## 结果应该怎样读

- 大多数通用基准超过 V2-0628 与 Coder-V2-0724。
- DS-FIM-Eval 内部集提升 5.1%。
- 官方仍承认 SWE-verified 较弱，说明代码补全强不等于软件工程 agent 强。

这里最重要的不是把不同年份的 benchmark 横向拼成排行榜，而是识别同一团队相邻 checkpoint 的变量：架构、预训练规模、post-training、推理预算、工具环境和服务接口分别改变了什么。

## 对 Agent Training 的启发

> [!insight]
> 这是一次很典型的 capability merge：统一 checkpoint 降低产品路由复杂度，但训练目标之间是否互相干扰，必须用分领域回归集与安全 spillover 一起看。

## 局限与证据边界

没有独立技术报告，合并算法与训练配比未公开；若只看官方聚合分数，很难判断收益来自数据、训练还是 checkpoint merge。

## 本地一手资料

本目录已保存原始官方 HTML/Markdown、模型卡，以及可获得的论文源码或技术报告。`retrieval_manifest.json` 记录 URL、抓取日期、字节数和 SHA-256，便于日后核验网页是否变化。

- [[src/assets|assets/]]
- [[src/hf_collection_manifest.json|hf_collection_manifest.json]]
- [[src/hf_model_card.md|hf_model_card.md]]
- [[src/huggingface_model_cards|huggingface_model_cards/]]
- [[src/official_model_card.md|official_model_card.md]]
- [[src/official_release.html|official_release.html]]
- [[src/official_release.md|official_release.md]]
- [[src/retrieval_manifest.json|retrieval_manifest.json]]

## 导航

- 上一代：[[Topics/13_base_model/DeepSeek_AI/2405_deepseek_v2/DeepSeek-V2|DeepSeek-V2]]
- 下一代：[[Topics/13_base_model/DeepSeek_AI/2412_deepseek_v2_5_1210/DeepSeek-V2.5-1210|DeepSeek-V2.5-1210]]
- 系列总览：[[Topics/13_base_model/DeepSeek_AI/DeepSeek_AI-Series-Summary|DeepSeek AI Series Summary]]
- 中文 Poster：[[Topics/13_base_model/DeepSeek_AI/2409_deepseek_v2_5/deepseek_v2_5_poster_zh.html|DeepSeek-V2.5 Poster]]
