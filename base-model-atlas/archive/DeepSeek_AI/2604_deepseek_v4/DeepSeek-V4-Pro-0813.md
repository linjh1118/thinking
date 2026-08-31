---
title: "DeepSeek-V4-Pro-0813 — DeepSeek V4 家族笔记"
type: model-note
authors: ["DeepSeek-AI"]
year: 2026
url: "https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro-0813"
tags: [model-note, base-model, deepseek, v4-family]
status: read
created: 2026-09-01
updated: 2026-09-01
---

# DeepSeek-V4-Pro-0813

> [!tldr]
> **Pro 正式更新 checkpoint。** 正式替代 Pro Preview，显著强化生产环境 agent 能力；支持 low / high / max reasoning_effort。

## 家族定位

| 维度 | 信息 |
|---|---|
| 首次公开 | **2026-08-13** |
| V4 内身份 | Pro 正式更新 checkpoint |
| 参数 / 规模 | Pro 级激活规模 |
| 精度 / 部署 | 内置 DSpark |
| Context | 1M / 长输出 |
| 官方入口 | [HF 原始 model card](https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro-0813) |

## 为什么需要独立记录

正式替代 Pro Preview，显著强化生产环境 agent 能力；支持 low / high / max reasoning_effort。

这一页的“独立”表示它是官方 collection 中可单独寻址的发行物，不表示所有发行物都是重新训练的新模型。Base、Preview、正式更新、DSpark 部署包与 Vision-Exp 会在 Atlas 中保留各自身份。

## 对 Agent Training 的判断

> [!insight]
> V4-Pro 的当前主检查点应以 0813 为准，四月 Pro 只保留为 Preview 历史节点。

## 证据边界

发布时间按官方发布页、仓库首次公开时间或名称中的官方日期记录；能力描述只采用官方 Hugging Face model card。官方 benchmark 依赖其内部 harness，不等价于第三方复现。

## 一手资料

- [HF 原始 model card](https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro-0813)
- [[src/huggingface_model_cards/DeepSeek-V4-Pro-0813.md|本地原始 HF model card]]
- [[DeepSeek-V4|V4 family 总览]]
