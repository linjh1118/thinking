---
title: "DeepSeek-V3 — DeepSeek 主线精读"
type: model-note
authors: ["DeepSeek-AI"]
year: 2024
venue: "arXiv + official release"
arxiv: "2412.19437"
url: "https://api-docs.deepseek.com/news/news1226/"
tags: [model-note, base-model, deepseek, mainline]
status: read
rating: 5
topic: "13_base_model"
created: 2026-08-31
updated: 2026-08-31
---

# DeepSeek-V3 — DeepSeek 主线精读

> [!tldr]
> V3 把 V2 的稀疏架构扩到 671B，并用 FP8、无辅助损失负载均衡、MTP 与通信重叠证明“大 MoE 也能稳定且经济地训完”。

## 谱系定位

- 发布时间：**2024-12**
- 团队：**DeepSeek AI**
- Atlas 口径：**主线正代 / 关键主部署 checkpoint**
- 官方入口：[一手发布页](https://api-docs.deepseek.com/news/news1226/)

V3 把 V2 的稀疏架构扩到 671B，并用 FP8、无辅助损失负载均衡、MTP 与通信重叠证明“大 MoE 也能稳定且经济地训完”。

## 关键规格与证据

| 指标 | 含义 |
|---|---|
| 671B | 总参数 |
| 37B | 每 token 激活 |
| 14.8T | 预训练 tokens |
| 2.788M | H800 GPU hours |

> [!note]
> 表中数字只采用本目录 `src/` 保存的官方发布页、模型卡或技术报告；内部榜单和服务价格只用于理解发布语境，不外推为独立复现实验。

## 架构：这一代改了什么

继承 MLA + DeepSeekMoE；新增 auxiliary-loss-free load balancing，避免为了均衡专家而损伤主目标；Multi-Token Prediction（MTP）既增强训练信号，也可用于 speculative decoding。权重包含 671B 主模型与 14B MTP 模块。

## 数据、训练与后训练

大规模 FP8 mixed-precision、DualPipe 式计算/通信重叠与硬件协同设计，使 14.8T-token 预训练约需 2.664M H800 GPU hours，全部训练约 2.788M。随后 SFT、RL，并把 R1 的 verification/reflection 模式蒸馏回标准 LLM。

## 结果应该怎样读

- Base：BBH 87.5、MMLU 87.1、HumanEval 65.2、MATH 61.6。
- Chat：MMLU 88.5、DROP 91.6；官方报告 128K NIAH 表现稳定。
- 全程没有不可恢复 loss spike 或 rollback，是训练系统成熟度的重要证据。

这里最重要的不是把不同年份的 benchmark 横向拼成排行榜，而是识别同一团队相邻 checkpoint 的变量：架构、预训练规模、post-training、推理预算、工具环境和服务接口分别改变了什么。

## 对 Agent Training 的启发

> [!insight]
> V3 的核心不是“低价复现 frontier”，而是算法—系统—硬件协同。对大规模 rollout/训练同样成立：如果通信、精度和路由不共同设计，算法收益会被系统成本吞掉。

## 局限与证据边界

训练成本只覆盖官方配置，不能简单等同于复现成本；部分后训练数据、R1 蒸馏 recipe 与内部基础设施未公开。

## 本地一手资料

本目录已保存原始官方 HTML/Markdown、模型卡，以及可获得的论文源码或技术报告。`retrieval_manifest.json` 记录 URL、抓取日期、字节数和 SHA-256，便于日后核验网页是否变化。

- [[src/assets|assets/]]
- [[src/official_readme.md|official_readme.md]]
- [[src/official_release.html|official_release.html]]
- [[src/official_release.md|official_release.md]]
- [[src/official_weights_readme.md|official_weights_readme.md]]
- [[src/paper|paper/]]
- [[src/retrieval_manifest.json|retrieval_manifest.json]]

## 导航

- 上一代：[[Topics/13_base_model/DeepSeek_AI/2412_deepseek_v2_5_1210/DeepSeek-V2.5-1210|DeepSeek-V2.5-1210]]
- 下一代：[[Topics/13_base_model/DeepSeek_AI/2501_deepseek_r1/DeepSeek-R1|DeepSeek-R1]]
- 系列总览：[[Topics/13_base_model/DeepSeek_AI/DeepSeek_AI-Series-Summary|DeepSeek AI Series Summary]]
- 中文 Poster：[[Topics/13_base_model/DeepSeek_AI/2412_deepseek_v3/deepseek_v3_poster_zh.html|DeepSeek-V3 Poster]]
