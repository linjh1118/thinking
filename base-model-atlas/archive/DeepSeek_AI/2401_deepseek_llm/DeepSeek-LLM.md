---
title: "DeepSeek LLM — DeepSeek 主线精读"
type: model-note
authors: ["DeepSeek-AI"]
year: 2024
venue: "arXiv + official release"
arxiv: "2401.02954"
url: "https://huggingface.co/deepseek-ai/deepseek-llm-67b-base"
tags: [model-note, base-model, deepseek, mainline]
status: read
rating: 5
topic: "13_base_model"
created: 2026-08-31
updated: 2026-08-31
---

# DeepSeek LLM — DeepSeek 主线精读

> [!tldr]
> DeepSeek 的真正起点不是某个榜单分数，而是把 scaling law、数据质量与训练系统一起当作可重复的工程问题。

## 谱系定位

- 发布时间：**2024-01**
- 团队：**DeepSeek AI**
- Atlas 口径：**主线正代 / 关键主部署 checkpoint**
- 官方入口：[一手发布页](https://huggingface.co/deepseek-ai/deepseek-llm-67b-base)

DeepSeek 的真正起点不是某个榜单分数，而是把 scaling law、数据质量与训练系统一起当作可重复的工程问题。

## 关键规格与证据

| 指标 | 含义 |
|---|---|
| 67B | 旗舰 Dense 参数 |
| 2T | 中英预训练 tokens |
| 1M+ | SFT 样本 |
| 4K | 上下文 |

> [!note]
> 表中数字只采用本目录 `src/` 保存的官方发布页、模型卡或技术报告；内部榜单和服务价格只用于理解发布语境，不外推为独立复现实验。

## 架构：这一代改了什么

沿用 LLaMA 式 decoder-only 主干：Pre-Norm、RMSNorm、SwiGLU、RoPE；67B 用 GQA，并以 95 层的“加深而非加宽”设计控制参数与流水线切分。多阶段学习率调度替代 cosine，服务后续持续训练。

## 数据、训练与后训练

论文不只给出 7B/67B 成品，还重新拟合 batch size、learning rate、模型/数据分配的 scaling law。数据管线采用跨 91 个 Common Crawl dump 的全局去重、质量过滤与 remix；Chat 版经历 SFT 与 DPO。HAI-LLM 组合 DP/TP/SP/PP、FlashAttention 与 ZeRO-1。

## 结果应该怎样读

- 67B Base：MMLU 71.3、GSM8K 63.4、HumanEval 42.7。
- 67B Chat：GSM8K 84.1、HumanEval 73.8；官方开放式评测称中英文表现超过 GPT-3.5。
- 论文明确指出：数据质量变化会改变最优模型/数据 scaling 配比，scaling law 不能脱离语料直接外推。

这里最重要的不是把不同年份的 benchmark 横向拼成排行榜，而是识别同一团队相邻 checkpoint 的变量：架构、预训练规模、post-training、推理预算、工具环境和服务接口分别改变了什么。

## 对 Agent Training 的启发

> [!insight]
> 对今天的训练工作最有价值的不是旧榜单，而是它把“数据版本”纳入 scaling 实验：换语料后，最优 compute allocation 也会变。训练预算规划必须绑定数据质量，而不是照搬 Chinchilla 常数。

## 局限与证据边界

Dense 67B、4K context 已明显过时；部分开放式和中文评测依赖内部框架。它应被当作方法论基线，而不是当前部署候选。

## 本地一手资料

本目录已保存原始官方 HTML/Markdown、模型卡，以及可获得的论文源码或技术报告。`retrieval_manifest.json` 记录 URL、抓取日期、字节数和 SHA-256，便于日后核验网页是否变化。

- [[src/hf_collection_manifest.json|hf_collection_manifest.json]]
- [[src/hf_model_card.md|hf_model_card.md]]
- [[src/huggingface_model_cards|huggingface_model_cards/]]
- [[src/official_readme.md|official_readme.md]]
- [[src/paper|paper/]]
- [[src/retrieval_manifest.json|retrieval_manifest.json]]

## 导航

- 下一代：[[Topics/13_base_model/DeepSeek_AI/2405_deepseek_v2/DeepSeek-V2|DeepSeek-V2]]
- 系列总览：[[Topics/13_base_model/DeepSeek_AI/DeepSeek_AI-Series-Summary|DeepSeek AI Series Summary]]
- 中文 Poster：[[Topics/13_base_model/DeepSeek_AI/2401_deepseek_llm/deepseek_llm_poster_zh.html|DeepSeek LLM Poster]]
