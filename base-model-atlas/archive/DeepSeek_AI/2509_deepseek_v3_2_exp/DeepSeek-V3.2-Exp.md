---
title: "DeepSeek-V3.2-Exp — DeepSeek 主线精读"
type: model-note
authors: ["DeepSeek-AI"]
year: 2025
venue: "Official release / model card"
url: "https://huggingface.co/deepseek-ai/DeepSeek-V3.2-Exp"
tags: [model-note, base-model, deepseek, mainline]
status: read
rating: 5
topic: "13_base_model"
created: 2026-08-31
updated: 2026-08-31
---

# DeepSeek-V3.2-Exp — DeepSeek 主线精读

> [!tldr]
> V3.2-Exp 的任务很单纯：在尽量不损能力的前提下，用 DeepSeek Sparse Attention 把长上下文 attention 从 dense 路线迁到可部署的稀疏路线。

## 谱系定位

- 发布时间：**2025-09**
- 团队：**DeepSeek AI**
- Atlas 口径：**主线正代 / 关键主部署 checkpoint**
- 官方入口：[一手发布页](https://huggingface.co/deepseek-ai/DeepSeek-V3.2-Exp)

V3.2-Exp 的任务很单纯：在尽量不损能力的前提下，用 DeepSeek Sparse Attention 把长上下文 attention 从 dense 路线迁到可部署的稀疏路线。

## 关键规格与证据

| 指标 | 含义 |
|---|---|
| DSA | 核心新架构 |
| 128K | 上下文 |
| ≈Parity | 对 Terminus |
| >50% | API 降价 |

> [!note]
> 表中数字只采用本目录 `src/` 保存的官方发布页、模型卡或技术报告；内部榜单和服务价格只用于理解发布语境，不外推为独立复现实验。

## 架构：这一代改了什么

在 V3.1-Terminus 上引入 DeepSeek Sparse Attention（DSA）：Lightning Indexer 为每个 query 选择少量高相关 token，再只对这些 token 做 fine-grained sparse attention。官方同时开放 TileLang 与 CUDA kernel，强调算法必须有对应实现。

## 数据、训练与后训练

采用持续训练把 dense attention checkpoint 迁移到 sparse attention，再做对齐。发布目标不是显著抬高 benchmark，而是保持 Terminus 水平同时降低长上下文训练/推理成本。

## 结果应该怎样读

- 官方报告整体 benchmark 与 V3.1-Terminus 大致持平。
- API 价格同步下调 50% 以上，是架构效率转化成服务成本的外部信号。
- 技术报告与模型权重同时开放，便于验证 DSA 与 kernel。

这里最重要的不是把不同年份的 benchmark 横向拼成排行榜，而是识别同一团队相邻 checkpoint 的变量：架构、预训练规模、post-training、推理预算、工具环境和服务接口分别改变了什么。

## 对 Agent Training 的启发

> [!insight]
> 对长轨迹 agent，稀疏 attention 的评价应同时看选择器召回、最终任务成功率和真实系统吞吐。只测 perplexity 很容易掩盖被 indexer 漏掉的关键 observation。

## 局限与证据边界

Exp 名称意味着过渡 checkpoint；官方主要强调 parity，没有提供对所有长程 agent 任务的独立验证。稀疏选择带来的尾部错误需要任务级分析。

## 本地一手资料

本目录已保存原始官方 HTML/Markdown、模型卡，以及可获得的论文源码或技术报告。`retrieval_manifest.json` 记录 URL、抓取日期、字节数和 SHA-256，便于日后核验网页是否变化。

- [[src/assets|assets/]]
- [[src/hf_collection_manifest.json|hf_collection_manifest.json]]
- [[src/hf_model_card.md|hf_model_card.md]]
- [[src/huggingface_model_cards|huggingface_model_cards/]]
- [[src/official_readme.md|official_readme.md]]
- [[src/official_release.html|official_release.html]]
- [[src/official_release.md|official_release.md]]
- [[src/retrieval_manifest.json|retrieval_manifest.json]]
- [[src/technical_report.pdf|technical_report.pdf]]

## 导航

- 上一代：[[Topics/13_base_model/DeepSeek_AI/2509_deepseek_v3_1_terminus/DeepSeek-V3.1-Terminus|DeepSeek-V3.1-Terminus]]
- 下一代：[[Topics/13_base_model/DeepSeek_AI/2512_deepseek_v3_2/DeepSeek-V3.2|DeepSeek-V3.2]]
- 系列总览：[[Topics/13_base_model/DeepSeek_AI/DeepSeek_AI-Series-Summary|DeepSeek AI Series Summary]]
- 中文 Poster：[[Topics/13_base_model/DeepSeek_AI/2509_deepseek_v3_2_exp/deepseek_v3_2_exp_poster_zh.html|DeepSeek-V3.2-Exp Poster]]
