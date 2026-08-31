---
title: "DeepSeek-V4-Flash-Vision-Exp — DeepSeek V4 家族笔记"
type: model-note
authors: ["DeepSeek-AI"]
year: 2026
url: "https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash-Vision-Exp"
tags: [model-note, base-model, deepseek, v4-family]
status: read
created: 2026-09-01
updated: 2026-09-01
---

# DeepSeek-V4-Flash-Vision-Exp

> [!tldr]
> **V4 首个实验多模态模型。** 在 Flash 架构上加入视觉模块并继续训练，提升多模态 agent 能力，同时维持相近的纯文本 agent 表现。

## 家族定位

| 维度 | 信息 |
|---|---|
| 首次公开 | **2026-08-31** |
| V4 内身份 | V4 首个实验多模态模型 |
| 参数 / 规模 | 约 305B（HF collection） |
| 精度 / 部署 | Flash + visual modules |
| Context | V4 Flash backbone |
| 官方入口 | [HF 原始 model card](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash-Vision-Exp) |

## 为什么需要独立记录

在 Flash 架构上加入视觉模块并继续训练，提升多模态 agent 能力，同时维持相近的纯文本 agent 表现。

这一页的“独立”表示它是官方 collection 中可单独寻址的发行物，不表示所有发行物都是重新训练的新模型。Base、Preview、正式更新、DSpark 部署包与 Vision-Exp 会在 Atlas 中保留各自身份。

## 对 Agent Training 的判断

> [!insight]
> 它是 V4 family 内明确的新能力 checkpoint；虽标 Exp，也不能从 V4 家族清单中消失。

## 证据边界

发布时间按官方发布页、仓库首次公开时间或名称中的官方日期记录；能力描述只采用官方 Hugging Face model card。官方 benchmark 依赖其内部 harness，不等价于第三方复现。

## 一手资料

- [HF 原始 model card](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash-Vision-Exp)
- [[src/huggingface_model_cards/DeepSeek-V4-Flash-Vision-Exp.md|本地原始 HF model card]]
- [[DeepSeek-V4|V4 family 总览]]
