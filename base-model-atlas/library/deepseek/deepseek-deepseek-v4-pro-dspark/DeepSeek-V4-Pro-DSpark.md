---
title: "DeepSeek-V4-Pro-DSpark — DeepSeek V4 家族笔记"
type: model-note
authors: ["DeepSeek-AI"]
year: 2026
url: "https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro-DSpark"
tags: [model-note, base-model, deepseek, v4-family]
status: read
created: 2026-09-01
updated: 2026-09-01
---

# DeepSeek-V4-Pro-DSpark

> [!tldr]
> **Pro 推测解码部署包。** 官方明确说明它不是新模型；它在 V4-Pro checkpoint 上附加 DSpark speculative decoding module。

## 家族定位

| 维度 | 信息 |
|---|---|
| 首次公开 | **2026-06-27** |
| V4 内身份 | Pro 推测解码部署包 |
| 参数 / 规模 | 同 Pro checkpoint |
| 精度 / 部署 | target + DSpark module |
| Context | 1M |
| 官方入口 | [HF 原始 model card](https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro-DSpark) |

## 为什么需要独立记录

官方明确说明它不是新模型；它在 V4-Pro checkpoint 上附加 DSpark speculative decoding module。

这一页的“独立”表示它是官方 collection 中可单独寻址的发行物，不表示所有发行物都是重新训练的新模型。Base、Preview、正式更新、DSpark 部署包与 Vision-Exp 会在 Atlas 中保留各自身份。

## 对 Agent Training 的判断

> [!insight]
> 它改变 serving latency 路径，不改变基础能力来源；评测归因应回到 Pro checkpoint。

## 证据边界

发布时间按官方发布页、仓库首次公开时间或名称中的官方日期记录；能力描述只采用官方 Hugging Face model card。官方 benchmark 依赖其内部 harness，不等价于第三方复现。

## 一手资料

- [HF 原始 model card](https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro-DSpark)
- [[src/huggingface_model_cards/DeepSeek-V4-Pro-DSpark.md|本地原始 HF model card]]
- [[DeepSeek-V4|V4 family 总览]]
