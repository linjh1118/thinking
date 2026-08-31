---
title: "Kimi K3 — Model Overview"
type: model-note
year: 2026
url: "https://github.com/MoonshotAI/Kimi-K3"
tags: [model-note, base-model, kimi]
status: read
created: 2026-08-31
updated: 2026-08-31
---

# Kimi K3 — Model Overview

> [!tldr]
> 2.8T 总参数、104B 激活，KDA + Attention Residuals、原生视觉与 1M context，面向长时程 coding 和知识工作。

## 谱系定位

- 团队：**Moonshot · Kimi**
- 时间：**2026-07**
- Atlas 归类：**主干正代**
- 一手证据：[Official repo / model card](https://github.com/MoonshotAI/Kimi-K3)

## 核心变化

2.8T 总参数、104B 激活，KDA + Attention Residuals、原生视觉与 1M context，面向长时程 coding 和知识工作。

这个节点单独收录，是因为官方把它作为可独立识别的模型 / family 发布；同一 family 内的参数尺寸、服务档位和 dated API snapshot 不再重复拆叶子。

## 阅读判断

- 与前代比较时，优先看架构、数据、post-training 与工具环境四类变化。
- 官方未披露的参数、训练数据和消融不作推断。
- 若该节点是专项模型，应沿团队主干理解其能力迁移，而不是把它误写成新的通用正代。

## 一手资料

- [https://github.com/MoonshotAI/Kimi-K3](https://github.com/MoonshotAI/Kimi-K3)
- [[src/Official Source|本地官方来源摘录]]

## 导航

- [[Topics/13_base_model/Base_Model_Top8_Branch_Audit_2026|Top 8 支线审计]]
