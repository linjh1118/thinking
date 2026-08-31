---
title: "DeepSeek-V3.1-Terminus — DeepSeek 主线精读"
type: model-note
authors: ["DeepSeek-AI"]
year: 2025
venue: "Official release / model card"
url: "https://api-docs.deepseek.com/news/news250922/"
tags: [model-note, base-model, deepseek, mainline]
status: read
rating: 5
topic: "13_base_model"
created: 2026-08-31
updated: 2026-08-31
---

# DeepSeek-V3.1-Terminus — DeepSeek 主线精读

> [!tldr]
> Terminus 是一次面向真实用户反馈的稳定性收口：重点不是新能力宣传，而是语言一致性、异常字符和 Code/Search Agent 回归。

## 谱系定位

- 发布时间：**2025-09**
- 团队：**DeepSeek AI**
- Atlas 口径：**主线正代 / 关键主部署 checkpoint**
- 官方入口：[一手发布页](https://api-docs.deepseek.com/news/news250922/)

Terminus 是一次面向真实用户反馈的稳定性收口：重点不是新能力宣传，而是语言一致性、异常字符和 Code/Search Agent 回归。

## 关键规格与证据

| 指标 | 含义 |
|---|---|
| 38.5 | BrowseComp |
| 68.4 | SWE Verified |
| 36.7 | Terminal-bench |
| 21.7 | HLE |

> [!note]
> 表中数字只采用本目录 `src/` 保存的官方发布页、模型卡或技术报告；内部榜单和服务价格只用于理解发布语境，不外推为独立复现实验。

## 架构：这一代改了什么

结构、参数与普通 chat template 继续沿用 V3.1/V3；主要修改 search agent template、工具集合和 checkpoint。官方还记录一个 self_attn.o_proj 的 UE8M0 FP8 scale 格式已知问题。

## 数据、训练与后训练

围绕线上反馈做针对性 post-training：减少中英混杂与随机字符，强化 Code Agent 和 Search Agent。它是一份很有价值的“模型回归修复”样本，而不是架构论文。

## 结果应该怎样读

- BrowseComp：30.0 → 38.5；SimpleQA：93.4 → 96.8。
- SWE Verified：66.0 → 68.4；Terminal-bench：31.3 → 36.7。
- 并非所有指标单调上升：BrowseComp-zh 49.2 → 45.0、Codeforces 2091 → 2046。

这里最重要的不是把不同年份的 benchmark 横向拼成排行榜，而是识别同一团队相邻 checkpoint 的变量：架构、预训练规模、post-training、推理预算、工具环境和服务接口分别改变了什么。

## 对 Agent Training 的启发

> [!insight]
> Agent checkpoint 应采用多目标发布门槛。Terminus 说明修复可靠性会伴随能力 trade-off；回归矩阵必须覆盖语言、工具、搜索、代码与格式，而不是只比较总平均。

## 局限与证据边界

没有完整训练 recipe；部分搜索指标同时受模板和 tool-set 变化影响，无法隔离纯模型增益。已知权重格式问题也提醒部署端必须读模型卡而不是只拉权重。

## 本地一手资料

本目录已保存原始官方 HTML/Markdown、模型卡，以及可获得的论文源码或技术报告。`retrieval_manifest.json` 记录 URL、抓取日期、字节数和 SHA-256，便于日后核验网页是否变化。

- [[src/assets|assets/]]
- [[src/official_model_card.md|official_model_card.md]]
- [[src/official_release.html|official_release.html]]
- [[src/official_release.md|official_release.md]]
- [[src/retrieval_manifest.json|retrieval_manifest.json]]

## 导航

- 上一代：[[Topics/13_base_model/DeepSeek_AI/2508_deepseek_v3_1/DeepSeek-V3.1|DeepSeek-V3.1]]
- 下一代：[[Topics/13_base_model/DeepSeek_AI/2509_deepseek_v3_2_exp/DeepSeek-V3.2-Exp|DeepSeek-V3.2-Exp]]
- 系列总览：[[Topics/13_base_model/DeepSeek_AI/DeepSeek_AI-Series-Summary|DeepSeek AI Series Summary]]
- 中文 Poster：[[Topics/13_base_model/DeepSeek_AI/2509_deepseek_v3_1_terminus/deepseek_v3_1_terminus_poster_zh.html|DeepSeek-V3.1-Terminus Poster]]
