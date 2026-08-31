---
title: "DeepSeek-V2.5-1210 — DeepSeek 主线精读"
type: model-note
authors: ["DeepSeek-AI"]
year: 2024
venue: "Official release / model card"
url: "https://huggingface.co/deepseek-ai/DeepSeek-V2.5-1210"
tags: [model-note, base-model, deepseek, mainline]
status: read
rating: 5
topic: "13_base_model"
created: 2026-08-31
updated: 2026-08-31
---

# DeepSeek-V2.5-1210 — DeepSeek 主线精读

> [!tldr]
> 1210 是 V2 系列的收官 checkpoint：架构不变，但把数学、代码、写作和文件/网页场景推到 V2 能达到的上限。

## 谱系定位

- 发布时间：**2024-12**
- 团队：**DeepSeek AI**
- Atlas 口径：**主线正代 / 关键主部署 checkpoint**
- 官方入口：[一手发布页](https://huggingface.co/deepseek-ai/DeepSeek-V2.5-1210)

1210 是 V2 系列的收官 checkpoint：架构不变，但把数学、代码、写作和文件/网页场景推到 V2 能达到的上限。

## 关键规格与证据

| 指标 | 含义 |
|---|---|
| 82.8 | MATH-500 |
| 34.38 | LiveCodeBench |
| 8×80GB | BF16 推理建议 |
| Final | V2.5 收官 |

> [!note]
> 表中数字只采用本目录 `src/` 保存的官方发布页、模型卡或技术报告；内部榜单和服务价格只用于理解发布语境，不外推为独立复现实验。

## 架构：这一代改了什么

继续使用 V2.5 的 236B/21B MoE 与统一通用+代码能力，没有证据表明发生架构替换。模型卡明确更新 chat template，并保留 FIM、JSON 等开发者接口。

## 数据、训练与后训练

这是对 V2.5 的持续 post-training/checkpoint refinement。MATH-500 从 74.8 提升到 82.8，LiveCodeBench（08-01 至 12-01）从 29.2 提升到 34.38；官方还报告写作、推理、文件上传与网页总结改善。

## 结果应该怎样读

- MATH-500：+8.0 个百分点。
- LiveCodeBench：+5.18 个百分点。
- 官方明确写明 V2.5-1210 标志 V2.5 系列结束，因此应独立保留而非并入九月版本。

这里最重要的不是把不同年份的 benchmark 横向拼成排行榜，而是识别同一团队相邻 checkpoint 的变量：架构、预训练规模、post-training、推理预算、工具环境和服务接口分别改变了什么。

## 对 Agent Training 的启发

> [!insight]
> 版本化 checkpoint 值得单独追踪：同架构下的能力增长更能反映 post-training/data iteration 的收益，而不是被参数扩张混淆。

## 局限与证据边界

公开材料没有训练数据与算法细节；大量结论来自官方 benchmark 与内部体验集，适合做 release delta，不适合作为完整可复现实验。

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

- 上一代：[[Topics/13_base_model/DeepSeek_AI/2409_deepseek_v2_5/DeepSeek-V2.5|DeepSeek-V2.5]]
- 下一代：[[Topics/13_base_model/DeepSeek_AI/2412_deepseek_v3/DeepSeek-V3|DeepSeek-V3]]
- 系列总览：[[Topics/13_base_model/DeepSeek_AI/DeepSeek_AI-Series-Summary|DeepSeek AI Series Summary]]
- 中文 Poster：[[Topics/13_base_model/DeepSeek_AI/2412_deepseek_v2_5_1210/deepseek_v2_5_1210_poster_zh.html|DeepSeek-V2.5-1210 Poster]]
