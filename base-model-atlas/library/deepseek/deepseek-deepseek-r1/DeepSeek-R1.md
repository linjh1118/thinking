---
title: "DeepSeek-R1 — DeepSeek 主线精读"
type: model-note
authors: ["DeepSeek-AI"]
year: 2025
venue: "arXiv + official release"
arxiv: "2501.12948"
url: "https://api-docs.deepseek.com/news/news250120/"
tags: [model-note, base-model, deepseek, mainline]
status: read
rating: 5
topic: "13_base_model"
created: 2026-08-31
updated: 2026-08-31
---

# DeepSeek-R1 — DeepSeek 主线精读

> [!tldr]
> R1 的贡献是把 reasoning 从“模仿长 CoT”改写为“在可靠 verifier 上用大规模 RL 诱导搜索、反思与自校验，再用冷启动和通用对齐修正可读性”。

## 谱系定位

- 发布时间：**2025-01**
- 团队：**DeepSeek AI**
- Atlas 口径：**主线正代 / 关键主部署 checkpoint**
- 官方入口：[一手发布页](https://api-docs.deepseek.com/news/news250120/)

R1 的贡献是把 reasoning 从“模仿长 CoT”改写为“在可靠 verifier 上用大规模 RL 诱导搜索、反思与自校验，再用冷启动和通用对齐修正可读性”。

## 关键规格与证据

| 指标 | 含义 |
|---|---|
| 671B | 总参数 |
| 37B | 激活参数 |
| 79.8 | AIME 2024 |
| 2029 | Codeforces rating |

> [!note]
> 表中数字只采用本目录 `src/` 保存的官方发布页、模型卡或技术报告；内部榜单和服务价格只用于理解发布语境，不外推为独立复现实验。

## 架构：这一代改了什么

沿用 V3 MoE 底座。R1-Zero 直接在 base model 上做 outcome-based RL；正式 R1 加入数千条冷启动数据、第一阶段 reasoning RL、rejection sampling + SFT，以及兼顾 helpfulness/harmlessness 的第二阶段 RL。

## 数据、训练与后训练

可验证数学/代码任务使用规则奖励，通用任务使用 reward model。第一阶段每题采 16 个最长 32,768-token rollout；论文还明确讨论语言一致性奖励、reward hacking，以及后 400 steps 才引入通用偏好信号的权衡。

## 结果应该怎样读

- AIME 2024 79.8、MATH-500 97.3、GPQA-Diamond 71.5。
- LiveCodeBench 65.9、Codeforces 2029；SWE Verified 49.2，显示推理与真实软件工程仍有差距。
- 六个 Distill 模型证明 reasoning trajectory 能迁移到 Qwen/Llama 小模型。

这里最重要的不是把不同年份的 benchmark 横向拼成排行榜，而是识别同一团队相邻 checkpoint 的变量：架构、预训练规模、post-training、推理预算、工具环境和服务接口分别改变了什么。

## 对 Agent Training 的启发

> [!insight]
> R1 给 agent training 的最强启发是：当终态可验证时，稀少人工示范并非上限，环境与 verifier 才是扩展瓶颈；当 reward 只能由模型近似时，reward hacking 又会迅速成为主问题。

## 局限与证据边界

R1 当时不能原生使用搜索/计算器等工具；纯 RL 输出存在语言混杂与可读性问题。对不可可靠验证的写作、开放 agent 任务，论文没有给出同等可扩展的答案。

## 本地一手资料

本目录已保存原始官方 HTML/Markdown、模型卡，以及可获得的论文源码或技术报告。`retrieval_manifest.json` 记录 URL、抓取日期、字节数和 SHA-256，便于日后核验网页是否变化。

- [[src/assets|assets/]]
- [[src/official_readme.md|official_readme.md]]
- [[src/official_release.html|official_release.html]]
- [[src/official_release.md|official_release.md]]
- [[src/paper|paper/]]
- [[src/retrieval_manifest.json|retrieval_manifest.json]]

## 导航

- 上一代：[[Topics/13_base_model/DeepSeek_AI/2412_deepseek_v3/DeepSeek-V3|DeepSeek-V3]]
- 下一代：[[Topics/13_base_model/DeepSeek_AI/2503_deepseek_v3_0324/DeepSeek-V3-0324|DeepSeek-V3-0324]]
- 系列总览：[[Topics/13_base_model/DeepSeek_AI/DeepSeek_AI-Series-Summary|DeepSeek AI Series Summary]]
- 中文 Poster：[[Topics/13_base_model/DeepSeek_AI/2501_deepseek_r1/deepseek_r1_poster_zh.html|DeepSeek-R1 Poster]]
