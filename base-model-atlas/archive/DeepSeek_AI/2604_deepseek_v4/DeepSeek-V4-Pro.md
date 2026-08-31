---
title: "DeepSeek-V4-Pro — DeepSeek V4 家族笔记"
type: model-note
authors: ["DeepSeek-AI"]
year: 2026
url: "https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro"
tags: [model-note, base-model, deepseek, v4-family]
status: read
created: 2026-09-01
updated: 2026-09-01
---

# DeepSeek-V4-Pro

> [!tldr]
> **Pro Preview 正式权重入口。** V4 family 的高容量 Preview：CSA/HCA 混合注意力、1M context，以及 non-think / high / max reasoning。

## 家族定位

| 维度 | 信息 |
|---|---|
| 首次公开 | **2026-04-24** |
| V4 内身份 | Pro Preview 正式权重入口 |
| 参数 / 规模 | 1.6T / 49B activated |
| 精度 / 部署 | FP4 + FP8 Mixed |
| Context | 1M |
| 官方入口 | [HF 原始 model card](https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro) |

## 为什么需要独立记录

V4 family 的高容量 Preview：CSA/HCA 混合注意力、1M context，以及 non-think / high / max reasoning。

这一页的“独立”表示它是官方 collection 中可单独寻址的发行物，不表示所有发行物都是重新训练的新模型。Base、Preview、正式更新、DSpark 部署包与 Vision-Exp 会在 Atlas 中保留各自身份。

## 对 Agent Training 的判断

> [!insight]
> Pro 的核心不是单纯扩大总参，而是用更高激活容量承接知识、复杂 reasoning 与生产 agent 任务。

## 证据边界

发布时间按官方发布页、仓库首次公开时间或名称中的官方日期记录；能力描述只采用官方 Hugging Face model card。官方 benchmark 依赖其内部 harness，不等价于第三方复现。

## 一手资料

- [HF 原始 model card](https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro)
- [[src/huggingface_model_cards/DeepSeek-V4-Pro.md|本地原始 HF model card]]
- [[DeepSeek-V4|V4 family 总览]]
