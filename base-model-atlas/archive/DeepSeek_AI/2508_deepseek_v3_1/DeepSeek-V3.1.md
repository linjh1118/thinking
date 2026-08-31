---
title: "DeepSeek-V3.1 — DeepSeek 主线精读"
type: model-note
authors: ["DeepSeek-AI"]
year: 2025
venue: "Official release / model card"
url: "https://api-docs.deepseek.com/news/news250821/"
tags: [model-note, base-model, deepseek, mainline]
status: read
rating: 5
topic: "13_base_model"
created: 2026-08-31
updated: 2026-08-31
---

# DeepSeek-V3.1 — DeepSeek 主线精读

> [!tldr]
> V3.1 把 V3 与 R1 两条线重新合并：单模型支持 Think/Non-Think，并第一次把 code/search agent 的多轮工具调用放到主模型定位中心。

## 谱系定位

- 发布时间：**2025-08**
- 团队：**DeepSeek AI**
- Atlas 口径：**主线正代 / 关键主部署 checkpoint**
- 官方入口：[一手发布页](https://api-docs.deepseek.com/news/news250821/)

V3.1 把 V3 与 R1 两条线重新合并：单模型支持 Think/Non-Think，并第一次把 code/search agent 的多轮工具调用放到主模型定位中心。

## 关键规格与证据

| 指标 | 含义 |
|---|---|
| 671B | 总参数 |
| 37B | 激活参数 |
| 128K | 双模式 context |
| 839B | 长上下文续训 tokens |

> [!note]
> 表中数字只采用本目录 `src/` 保存的官方发布页、模型卡或技术报告；内部榜单和服务价格只用于理解发布语境，不外推为独立复现实验。

## 架构：这一代改了什么

底层仍是 V3 架构；V3.1-Base 在 V3 上做两阶段长上下文扩展：32K 阶段 630B tokens、128K 阶段 209B tokens。新 tokenizer/chat template 在同一权重中编码 thinking、non-thinking 与 tool-call。

## 数据、训练与后训练

post-training 同时优化混合推理与多步 agent。deepseek-chat 映射非思考模式，deepseek-reasoner 映射思考模式；代码 agent 和搜索 agent 使用显式工具描述、结构化调用以及多轮 observation。

## 结果应该怎样读

- SWE Verified（agent mode）66.0，对 V3-0324 的 45.4。
- SWE-bench Multilingual 54.5，对 29.3；Terminal-bench 31.3，对 13.3。
- 官方称 V3.1-Think 以更少时间达到接近 R1-0528 的答案质量。

这里最重要的不是把不同年份的 benchmark 横向拼成排行榜，而是识别同一团队相邻 checkpoint 的变量：架构、预训练规模、post-training、推理预算、工具环境和服务接口分别改变了什么。

## 对 Agent Training 的启发

> [!insight]
> 这是 DeepSeek 从“会推理”到“在环境里推理”的转折点。关键资产不再只是 CoT，而是 chat template、工具 schema、多轮轨迹与 agent-specific post-training 数据。

## 局限与证据边界

搜索结果依赖内部商业搜索 API、网页过滤和 128K context，不能只归因于模型；严格 function calling 当时仍位于 Beta。

## 本地一手资料

本目录已保存原始官方 HTML/Markdown、模型卡，以及可获得的论文源码或技术报告。`retrieval_manifest.json` 记录 URL、抓取日期、字节数和 SHA-256，便于日后核验网页是否变化。

- [[src/assets|assets/]]
- [[src/official_model_card.md|official_model_card.md]]
- [[src/official_release.html|official_release.html]]
- [[src/official_release.md|official_release.md]]
- [[src/retrieval_manifest.json|retrieval_manifest.json]]

## 导航

- 上一代：[[Topics/13_base_model/DeepSeek_AI/2505_deepseek_r1_0528/DeepSeek-R1-0528|DeepSeek-R1-0528]]
- 下一代：[[Topics/13_base_model/DeepSeek_AI/2509_deepseek_v3_1_terminus/DeepSeek-V3.1-Terminus|DeepSeek-V3.1-Terminus]]
- 系列总览：[[Topics/13_base_model/DeepSeek_AI/DeepSeek_AI-Series-Summary|DeepSeek AI Series Summary]]
- 中文 Poster：[[Topics/13_base_model/DeepSeek_AI/2508_deepseek_v3_1/deepseek_v3_1_poster_zh.html|DeepSeek-V3.1 Poster]]
