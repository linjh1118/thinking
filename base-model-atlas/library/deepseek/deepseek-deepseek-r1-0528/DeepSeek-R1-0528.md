---
title: "DeepSeek-R1-0528 — DeepSeek 主线精读"
type: model-note
authors: ["DeepSeek-AI"]
year: 2025
venue: "Official release / model card"
url: "https://api-docs.deepseek.com/news/news250528/"
tags: [model-note, base-model, deepseek, mainline]
status: read
rating: 5
topic: "13_base_model"
created: 2026-08-31
updated: 2026-08-31
---

# DeepSeek-R1-0528 — DeepSeek 主线精读

> [!tldr]
> 0528 的主要变化是把更多 post-training compute 转成更深的测试时推理，并补上 function calling、JSON 与 vibe coding，令 R1 从研究模型靠近工具模型。

## 谱系定位

- 发布时间：**2025-05**
- 团队：**DeepSeek AI**
- Atlas 口径：**主线正代 / 关键主部署 checkpoint**
- 官方入口：[一手发布页](https://api-docs.deepseek.com/news/news250528/)

0528 的主要变化是把更多 post-training compute 转成更深的测试时推理，并补上 function calling、JSON 与 vibe coding，令 R1 从研究模型靠近工具模型。

## 关键规格与证据

| 指标 | 含义 |
|---|---|
| 87.5 | AIME 2025 |
| 23K | AIME 平均思考 tokens |
| 73.3 | LiveCodeBench |
| 57.6 | SWE Verified |

> [!note]
> 表中数字只采用本目录 `src/` 保存的官方发布页、模型卡或技术报告；内部榜单和服务价格只用于理解发布语境，不外推为独立复现实验。

## 架构：这一代改了什么

沿用 R1/V3 的 671B/37B MoE。官方将提升归因于更多计算资源与 post-training algorithm optimization，而非基础架构变化；最大评测输出长度提升到 64K。

## 数据、训练与后训练

AIME 平均推理长度从约 12K 增到 23K tokens，体现 inference-time compute 的直接扩展。同时改善幻觉、前端和函数调用，并把 CoT 蒸馏到 Qwen3-8B，形成 R1-0528-Qwen3-8B。

## 结果应该怎样读

- AIME 2024：79.8 → 91.4；AIME 2025：70.0 → 87.5。
- LiveCodeBench：63.5 → 73.3；SWE Verified：49.2 → 57.6。
- 蒸馏 8B 在 AIME 2024 达 86.0，说明新 CoT 仍有很强的 teacher value。

这里最重要的不是把不同年份的 benchmark 横向拼成排行榜，而是识别同一团队相邻 checkpoint 的变量：架构、预训练规模、post-training、推理预算、工具环境和服务接口分别改变了什么。

## 对 Agent Training 的启发

> [!insight]
> 更多 thinking tokens 能明显抬高可验证推理，但 agent 训练不能只放大轨迹长度：工具成功率、环境反馈和成本必须同时纳入 reward，否则会把“更长”误当成“更好”。

## 局限与证据边界

官方未公开算法优化细节；长思考提高延迟与成本。函数调用虽已支持，但尚未形成后续 V3.1 那种完整 thinking/non-thinking + agent 模板。

## 本地一手资料

本目录已保存原始官方 HTML/Markdown、模型卡，以及可获得的论文源码或技术报告。`retrieval_manifest.json` 记录 URL、抓取日期、字节数和 SHA-256，便于日后核验网页是否变化。

- [[src/assets|assets/]]
- [[src/official_model_card.md|official_model_card.md]]
- [[src/official_release.html|official_release.html]]
- [[src/official_release.md|official_release.md]]
- [[src/retrieval_manifest.json|retrieval_manifest.json]]

## 导航

- 上一代：[[Topics/13_base_model/DeepSeek_AI/2503_deepseek_v3_0324/DeepSeek-V3-0324|DeepSeek-V3-0324]]
- 下一代：[[Topics/13_base_model/DeepSeek_AI/2508_deepseek_v3_1/DeepSeek-V3.1|DeepSeek-V3.1]]
- 系列总览：[[Topics/13_base_model/DeepSeek_AI/DeepSeek_AI-Series-Summary|DeepSeek AI Series Summary]]
- 中文 Poster：[[Topics/13_base_model/DeepSeek_AI/2505_deepseek_r1_0528/deepseek_r1_0528_poster_zh.html|DeepSeek-R1-0528 Poster]]
