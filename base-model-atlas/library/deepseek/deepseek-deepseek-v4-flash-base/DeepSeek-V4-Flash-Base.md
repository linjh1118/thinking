---
title: "DeepSeek-V4-Flash-Base — DeepSeek V4 家族笔记"
type: model-note
authors: ["DeepSeek-AI"]
year: 2026
url: "https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash-Base"
tags: [model-note, base-model, deepseek, v4-family]
status: read
created: 2026-09-01
updated: 2026-09-01
---

# DeepSeek-V4-Flash-Base

> [!tldr]
> **Flash 预训练基座。** 保留预训练阶段能力，不包含面向对话、reasoning effort 与 agent 的完整后训练。

## 家族定位

| 维度 | 信息 |
|---|---|
| 首次公开 | **2026-04-24** |
| V4 内身份 | Flash 预训练基座 |
| 参数 / 规模 | 284B / 13B activated |
| 精度 / 部署 | FP8 Mixed |
| Context | 1M |
| 官方入口 | [HF 官方仓库（无 README/model card）](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash-Base) |

## 为什么需要独立记录

保留预训练阶段能力，不包含面向对话、reasoning effort 与 agent 的完整后训练。

这一页的“独立”表示它是官方 collection 中可单独寻址的发行物，不表示所有发行物都是重新训练的新模型。Base、Preview、正式更新、DSpark 部署包与 Vision-Exp 会在 Atlas 中保留各自身份。

## 对 Agent Training 的判断

> [!insight]
> 它适合研究继续预训练、领域适配与后训练，而不是直接替代 Instruct/Chat 服务。

## 证据边界

发布时间按官方发布页、仓库首次公开时间或名称中的官方日期记录；能力描述只采用官方 Hugging Face model card。官方 benchmark 依赖其内部 harness，不等价于第三方复现。

## 一手资料

- [HF 官方仓库（无 README/model card）](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash-Base)
- [[src/huggingface_repository_metadata/DeepSeek-V4-Flash-Base.json|HF 仓库元数据]]
- [[DeepSeek-V4|V4 family 总览]]
