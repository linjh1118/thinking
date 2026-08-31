---
title: "DeepSeek-V2 — DeepSeek 主线精读"
type: model-note
authors: ["DeepSeek-AI"]
year: 2024
venue: "arXiv + official release"
arxiv: "2405.04434"
url: "https://huggingface.co/deepseek-ai/DeepSeek-V2"
tags: [model-note, base-model, deepseek, mainline]
status: read
rating: 5
topic: "13_base_model"
created: 2026-08-31
updated: 2026-08-31
---

# DeepSeek-V2 — DeepSeek 主线精读

> [!tldr]
> V2 确立了 DeepSeek 的技术身份：MLA 解决 KV cache，DeepSeekMoE 解决激活计算，能力增长第一次与成本下降同时发生。

## 谱系定位

- 发布时间：**2024-05**
- 团队：**DeepSeek AI**
- Atlas 口径：**主线正代 / 关键主部署 checkpoint**
- 官方入口：[一手发布页](https://huggingface.co/deepseek-ai/DeepSeek-V2)

V2 确立了 DeepSeek 的技术身份：MLA 解决 KV cache，DeepSeekMoE 解决激活计算，能力增长第一次与成本下降同时发生。

## 关键规格与证据

| 指标 | 含义 |
|---|---|
| 236B | 总参数 |
| 21B | 每 token 激活 |
| 8.1T | 预训练 tokens |
| 128K | 上下文 |

> [!note]
> 表中数字只采用本目录 `src/` 保存的官方发布页、模型卡或技术报告；内部榜单和服务价格只用于理解发布语境，不外推为独立复现实验。

## 架构：这一代改了什么

Multi-head Latent Attention（MLA）把 K/V 压缩进低维 latent，显著减少推理时 KV cache；DeepSeekMoE 用细粒度专家分割、共享专家隔离通用知识，并对路由做负载约束。两者共同把“模型大”与“每 token 贵”拆开。

## 数据、训练与后训练

在 8.1T 高质量 tokens 上预训练，随后进行 SFT 与 RL。官方报告相对 DeepSeek 67B 节省 42.5% 训练成本、减少 93.3% KV cache，并把最大生成吞吐提高到 5.76 倍。

## 结果应该怎样读

- Base：MMLU 78.5、C-Eval 81.7、CMMLU 84.0、MATH 43.6。
- NIAH 显示模型覆盖到 128K context。
- V2 的关键证据不是单项 SOTA，而是同一架构同时改善训练、显存与吞吐。

这里最重要的不是把不同年份的 benchmark 横向拼成排行榜，而是识别同一团队相邻 checkpoint 的变量：架构、预训练规模、post-training、推理预算、工具环境和服务接口分别改变了什么。

## 对 Agent Training 的启发

> [!insight]
> MLA 的意义是把推理成本提前纳入基模架构设计。对 agent rollout 来说，KV cache 和长轨迹吞吐常比参数量更先成为瓶颈，V2 是这条路线的起点。

## 局限与证据边界

MoE 的专家并行与路由使部署复杂度上升；官方开源实现也提醒 Hugging Face 路径慢于内部实现。效率数字依赖特定系统配置，不能脱离硬件直接复用。

## 本地一手资料

本目录已保存原始官方 HTML/Markdown、模型卡，以及可获得的论文源码或技术报告。`retrieval_manifest.json` 记录 URL、抓取日期、字节数和 SHA-256，便于日后核验网页是否变化。

- [[src/hf_collection_manifest.json|hf_collection_manifest.json]]
- [[src/hf_model_card.md|hf_model_card.md]]
- [[src/huggingface_model_cards|huggingface_model_cards/]]
- [[src/official_readme.md|official_readme.md]]
- [[src/paper|paper/]]
- [[src/retrieval_manifest.json|retrieval_manifest.json]]

## 导航

- 上一代：[[Topics/13_base_model/DeepSeek_AI/2401_deepseek_llm/DeepSeek-LLM|DeepSeek LLM]]
- 下一代：[[Topics/13_base_model/DeepSeek_AI/2409_deepseek_v2_5/DeepSeek-V2.5|DeepSeek-V2.5]]
- 系列总览：[[Topics/13_base_model/DeepSeek_AI/DeepSeek_AI-Series-Summary|DeepSeek AI Series Summary]]
- 中文 Poster：[[Topics/13_base_model/DeepSeek_AI/2405_deepseek_v2/deepseek_v2_poster_zh.html|DeepSeek-V2 Poster]]
