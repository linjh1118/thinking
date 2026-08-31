---
title: "DeepSeek-V4 — DeepSeek 主线精读"
type: model-note
authors: ["DeepSeek-AI"]
year: 2026
venue: "arXiv + official release"
arxiv: "2606.19348"
url: "https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro"
tags: [model-note, base-model, deepseek, mainline]
status: read
rating: 5
topic: "13_base_model"
created: 2026-08-31
updated: 2026-08-31
source_sufficiency: sufficient
---

# DeepSeek-V4 — DeepSeek 主线精读

> [!tldr]
> **V4 把 DeepSeek 的效率路线推进到 1M context：Pro/Flash 共用 CSA + HCA 混合注意力，并把 agent、长上下文、可变 reasoning effort 与低比特部署作为一个系统问题。** 四月 Preview、七月 Flash-0731、八月 Pro-0813 是同一正代内不同 checkpoint，不能把它们的发布时间和分数混在一起。

![DeepSeek-V4 官方规格总览](src/assets/official_preview_release_01.png)

> [!success] 资料充分度：完整
> Family 层有官方 technical report 源码、HF model cards、Preview/正式发布页、完整 benchmark 与本地化图片，本页达到完整综述标准。各发行物的材料边界在对应独立笔记中说明。

## 谱系定位

- 发布时间：**2026-04-24**（Preview family 首次公开）
- 团队：**DeepSeek AI**
- Atlas 口径：**主线正代 / 关键主部署 checkpoint**
- 官方入口：[一手发布页](https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro)

V4 把 DeepSeek 的效率路线推进到 1M context：Pro/Flash 共用压缩+稀疏混合注意力，并把 agent、长上下文和可变 reasoning effort 作为默认服务形态。

## 关键规格与证据

| 指标 | 含义 |
|---|---|
| 1.6T / 49B | Pro 总参/激活 |
| 284B / 13B | Flash 总参/激活 |
| 32T+ | 预训练 tokens |
| 1M | 原生 context |

![DeepSeek-V4 官方综合性能图](src/assets/official_preview_release_02.png)

> [!note]
> 表中数字只采用本目录 `src/` 保存的官方发布页、模型卡或技术报告；内部榜单和服务价格只用于理解发布语境，不外推为独立复现实验。

## 架构：这一代改了什么

Hybrid Attention 组合 Compressed Sparse Attention（CSA）与更高压缩率的 Highly Compressed Attention（HCA）：先沿序列压缩 KV，再用 DSA 选择压缩块，并保留近期未压缩窗口。另引入 mHC 稳定残差连接、Muon optimizer 与 FP4 路由专家。

## 数据、训练与后训练

Flash 预训练约 32T tokens，Pro 约 33T。post-training 先分别培养数学、代码、agent、指令跟随专家，再通过 on-policy distillation 合并；后训练对 MoE expert 与 indexer QK path 做 FP4 quantization-aware training。GA 版本增加 low/high/max reasoning effort 与原生 Responses API。

## 结果应该怎样读

- 在 1M context，Pro 单 token FLOPs/累计 KV cache 约为 V3.2 的 27%/10%；Flash 为 10%/7%。
- 官方报告 Pro 1.6T/49B、Flash 284B/13B，二者都原生支持 1M。
- V4-Pro 八月 GA 继续强化生产 agent，并保持模型名不变；因此 GA 归入同一 V4 family，而不是另造一代。

这里最重要的不是把不同年份的 benchmark 横向拼成排行榜，而是识别同一团队相邻 checkpoint 的变量：架构、预训练规模、post-training、推理预算、工具环境和服务接口分别改变了什么。

![DeepSeek-V4 正式 checkpoint 官方 benchmark](src/assets/official_ga_release_01.png)

## 官方 collection 的九个发行物怎样归类

| 类型 | 发行物 | Atlas 位置 | 是否独立能力 checkpoint |
|---|---|---|---|
| Base | [[DeepSeek-V4-Flash-Base]] / [[DeepSeek-V4-Pro-Base]] | 主线 family 的训练起点 | 是，但不是 Chat/Agent 模型 |
| Preview | [[DeepSeek-V4-Flash]] / [[DeepSeek-V4-Pro]] | 四月主线 | 是 |
| 正式更新 | [[DeepSeek-V4-Flash-0731]] / [[DeepSeek-V4-Pro-0813]] | 七月、八月主线 | 是，分别替代 Preview |
| 推测解码 | [[DeepSeek-V4-Flash-DSpark]] / [[DeepSeek-V4-Pro-DSpark]] | 默认折叠的 serving 支线 | 否，同 checkpoint + module |
| 多模态实验 | [[DeepSeek-V4-Flash-Vision-Exp]] | 默认折叠的视觉支线 | 是，experimental |

这个分类同时满足两件事：官方 collection 不漏项；主干时间线也不会被同一 checkpoint 的 DSpark 打乱。

## 对 Agent Training 的启发

> [!insight]
> V4 把 agent scaling 的三类成本放到同一设计里：模型激活、长轨迹 KV、test-time reasoning。真正的 agent 基模优化目标应是任务成功率/端到端成本，而不是孤立的每 token 价格。

## 局限与证据边界

公开报告仍无法复现内部数据与完整 agent 环境；1M benchmark 不等于真实长程记忆。Pro/Flash 的效果—成本选择也要求按任务难度动态路由。

## 本地一手资料

本目录已保存原始官方 HTML/Markdown、模型卡，以及可获得的论文源码或技术报告。`retrieval_manifest.json` 记录 URL、抓取日期、字节数和 SHA-256，便于日后核验网页是否变化。

- [[src/assets|assets/]]
- [[src/hf_collection_manifest.json|hf_collection_manifest.json]]
- [[src/hf_model_card.md|hf_model_card.md]]
- [[src/huggingface_model_cards|huggingface_model_cards/]]
- [[src/hf_collection_raw.json|DeepSeek-V4 官方 collection 原始 JSON]]
- [[src/huggingface_repository_metadata|Base 仓库原始元数据/]]
- [[src/official_flash_model_card.md|official_flash_model_card.md]]
- [[src/official_ga_release.html|official_ga_release.html]]
- [[src/official_ga_release.md|official_ga_release.md]]
- [[src/official_preview_release.html|official_preview_release.html]]
- [[src/official_preview_release.md|official_preview_release.md]]
- [[src/official_pro_model_card.md|official_pro_model_card.md]]
- [[src/paper|paper/]]
- [[src/retrieval_manifest.json|retrieval_manifest.json]]

## 导航

- 上一代：[[Topics/13_base_model/DeepSeek_AI/2512_deepseek_v3_2/DeepSeek-V3.2|DeepSeek-V3.2]]
- 系列总览：[[Topics/13_base_model/DeepSeek_AI/DeepSeek_AI-Series-Summary|DeepSeek AI Series Summary]]
- 中文 Poster：[[Topics/13_base_model/DeepSeek_AI/2604_deepseek_v4/deepseek_v4_poster_zh.html|DeepSeek-V4 Poster]]
