---
title: "DeepSeek-V3.2 — DeepSeek 主线精读"
type: model-note
authors: ["DeepSeek-AI"]
year: 2025
venue: "Official release / model card"
url: "https://huggingface.co/deepseek-ai/DeepSeek-V3.2"
tags: [model-note, base-model, deepseek, mainline]
status: read
rating: 5
topic: "13_base_model"
created: 2026-08-31
updated: 2026-08-31
---

# DeepSeek-V3.2 — DeepSeek 主线精读

> [!tldr]
> V3.2 把 DSA 从效率实验推进到 reasoning-first agent 模型：首次把 thinking 直接嵌入工具调用，并用大规模合成环境扩展 agent post-training。

## 谱系定位

- 发布时间：**2025-12**
- 团队：**DeepSeek AI**
- Atlas 口径：**主线正代 / 关键主部署 checkpoint**
- 官方入口：[一手发布页](https://huggingface.co/deepseek-ai/DeepSeek-V3.2)

V3.2 把 DSA 从效率实验推进到 reasoning-first agent 模型：首次把 thinking 直接嵌入工具调用，并用大规模合成环境扩展 agent post-training。

## 关键规格与证据

| 指标 | 含义 |
|---|---|
| 1,800+ | 合成环境 |
| 85K+ | 复杂指令 |
| DSA | 长上下文稀疏注意力 |
| 2 modes | Thinking + Non-Thinking |

> [!note]
> 表中数字只采用本目录 `src/` 保存的官方发布页、模型卡或技术报告；内部榜单和服务价格只用于理解发布语境，不外推为独立复现实验。

## 架构：这一代改了什么

继承 V3.2-Exp 的 DSA 与 685B 级 MoE 结构。新 chat template 支持 thinking-with-tools，并为搜索场景加入专用 developer role；正式版还发布高算力 V3.2-Speciale，但二者共享结构。

## 数据、训练与后训练

三条主线同时扩展：DSA 提升效率；scalable RL protocol 增加 post-training compute；agent task synthesis pipeline 覆盖 1,800+ 环境和 85K+ 复杂指令，把 reasoning、tool-use 与多轮交互联合训练。

## 结果应该怎样读

- 官方将 V3.2 定位为 V3.2-Exp 的正式 successor。
- V3.2 同时支持 thinking/non-thinking 工具调用；Speciale 取得 IMO、CMO、ICPC WF、IOI 2025 金牌级结果。
- Speciale 不支持工具调用，说明最大化纯推理与稳定 agent 接口仍是不同优化目标。

这里最重要的不是把不同年份的 benchmark 横向拼成排行榜，而是识别同一团队相邻 checkpoint 的变量：架构、预训练规模、post-training、推理预算、工具环境和服务接口分别改变了什么。

## 对 Agent Training 的启发

> [!insight]
> V3.2 最值得 Agent Training 借鉴的是环境规模：复杂轨迹能力来自可生成、可执行、可验证的环境集合，而不仅是更多问答 CoT。下一步应关注环境覆盖与 verifier 质量的 scaling law。

## 局限与证据边界

官方没有公开完整 85K 指令、环境实现与 verifier；Speciale 的高推理分数不能代表工具任务能力。模型卡也提醒 parser 只处理格式良好输出，生产环境仍需恢复逻辑。

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
- [[src/technical_report.pdf|technical_report.pdf]]

## 导航

- 上一代：[[Topics/13_base_model/DeepSeek_AI/2509_deepseek_v3_2_exp/DeepSeek-V3.2-Exp|DeepSeek-V3.2-Exp]]
- 下一代：[[Topics/13_base_model/DeepSeek_AI/2604_deepseek_v4/DeepSeek-V4|DeepSeek-V4]]
- 系列总览：[[Topics/13_base_model/DeepSeek_AI/DeepSeek_AI-Series-Summary|DeepSeek AI Series Summary]]
- 中文 Poster：[[Topics/13_base_model/DeepSeek_AI/2512_deepseek_v3_2/deepseek_v3_2_poster_zh.html|DeepSeek-V3.2 Poster]]
