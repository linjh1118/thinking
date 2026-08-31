---
title: "Qwen3-Next — Model Overview"
type: model-note
year: 2025
url: "https://qwen.ai/blog?id=qwen3-next"
tags: [model-note, base-model, qwen]
status: read
created: 2026-08-31
updated: 2026-08-31
---

# Qwen3-Next — Model Overview

> [!tldr]
> 80B/3B-active 超稀疏 MoE，以 Gated DeltaNet + Gated Attention 的 hybrid 架构预演 Qwen3.5。

## 谱系定位

- 团队：**Alibaba · Qwen**
- 时间：**2025-09**
- Atlas 归类：**主干正代**
- 一手证据：[Official release](https://qwen.ai/blog?id=qwen3-next)

## 核心变化

80B/3B-active 超稀疏 MoE，以 Gated DeltaNet + Gated Attention 的 hybrid 架构预演 Qwen3.5。

这个节点单独收录，是因为官方把它作为可独立识别的模型 / family 发布；同一 family 内的参数尺寸、服务档位和 dated API snapshot 不再重复拆叶子。

## 阅读判断

- 与前代比较时，优先看架构、数据、post-training 与工具环境四类变化。
- 官方未披露的参数、训练数据和消融不作推断。
- 若该节点是专项模型，应沿团队主干理解其能力迁移，而不是把它误写成新的通用正代。

## 一手资料

- [https://qwen.ai/blog?id=qwen3-next](https://qwen.ai/blog?id=qwen3-next)
- [[src/Official Source|本地官方来源摘录]]

## 导航

- [[Topics/13_base_model/Base_Model_Top8_Branch_Audit_2026|Top 8 支线审计]]
