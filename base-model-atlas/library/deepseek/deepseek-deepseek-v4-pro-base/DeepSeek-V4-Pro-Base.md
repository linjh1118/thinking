---
title: "DeepSeek-V4-Pro-Base — DeepSeek V4 家族笔记"
type: model-note
authors: ["DeepSeek-AI"]
year: 2026
url: "https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro-Base"
tags: [model-note, base-model, deepseek, v4-family]
status: read
created: 2026-09-01
updated: 2026-09-01
---

# DeepSeek-V4-Pro-Base

> [!tldr]
> **Pro 预训练基座。** V4-Pro 的大容量预训练 checkpoint，面向继续训练与研究，不带正式版完整 post-training 行为。

## 家族定位

| 维度 | 信息 |
|---|---|
| 首次公开 | **2026-04-24** |
| V4 内身份 | Pro 预训练基座 |
| 参数 / 规模 | 1.6T / 49B activated |
| 精度 / 部署 | FP8 Mixed |
| Context | 1M |
| 官方入口 | [HF 官方仓库（无 README/model card）](https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro-Base) |

## 为什么需要独立记录

V4-Pro 的大容量预训练 checkpoint，面向继续训练与研究，不带正式版完整 post-training 行为。

这一页的“独立”表示它是官方 collection 中可单独寻址的发行物，不表示所有发行物都是重新训练的新模型。Base、Preview、正式更新、DSpark 部署包与 Vision-Exp 会在 Atlas 中保留各自身份。

## 对 Agent Training 的判断

> [!insight]
> Base 与正式版必须分开读：前者回答“预训练基座是什么”，后者回答“可直接使用的 agent 模型是什么”。

## 证据边界

发布时间按官方发布页、仓库首次公开时间或名称中的官方日期记录；能力描述只采用官方 Hugging Face model card。官方 benchmark 依赖其内部 harness，不等价于第三方复现。

## 一手资料

- [HF 官方仓库（无 README/model card）](https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro-Base)
- [[src/huggingface_repository_metadata/DeepSeek-V4-Pro-Base.json|HF 仓库元数据]]
- [[DeepSeek-V4|V4 family 总览]]
