---
title: "GLM-4.5-Air — 高效率 ARC 同代模型"
type: model-note
year: 2025
url: "https://huggingface.co/zai-org/GLM-4.5-Air"
tags: [model-note, base-model, glm, air, reasoning, coding, agent]
status: read
created: 2026-09-01
updated: 2026-09-01
---

# GLM-4.5-Air

> [!tldr]
> **GLM-4.5-Air 是 GLM-4.5 ARC family 的独立高效率 checkpoint：106B 总参数、12B 激活参数，保留 thinking / non-thinking 双模式以及 reasoning、coding、agent 能力，而不是 GLM-4.5 的 FP8 副本。**

## 一页速览

| 维度 | GLM-4.5-Air |
|---|---|
| Family | GLM-4.5 ARC |
| 参数 | 106B total / 12B activated |
| 架构 | MoE，面向更低部署成本 |
| 推理模式 | Thinking / non-thinking hybrid reasoning |
| 能力定位 | Reasoning、coding、tool use、agent |
| License | MIT |

## 与 GLM-4.5 的关系

GLM-4.5 与 Air 共用 ARC foundation model 的训练目标和 hybrid reasoning 设计，但采用不同的参数/激活规模。官方同时发布二者的 Base、混合推理和 FP8 权重：`Air` 是模型成员，`Air-FP8` 才是精度副本。因此 Atlas 单列 Air，但不再为 FP8 重复拆叶子。

## 能力—成本取舍

Air 的目标不是在所有榜单上替代 355B/32B 的 GLM-4.5，而是在保留 agent workflow、tool calling 与长输出能力的同时降低每 token 激活和部署资源。阅读 benchmark 时应把它与同等激活规模模型比较，而不是只看 family 内绝对最高分。

> [!insight]
> 对训练系统而言，Air 说明同一套 expert training、curriculum RL 与 agentic RL 可以产出多个成本工作点；选择哪一个应由任务长度、并发量和 verifier 成本共同决定。

## 一手资料

- [GLM-4.5-Air · Hugging Face](https://huggingface.co/zai-org/GLM-4.5-Air)
- [[GLM-4.5-ARC-Foundation-Models|GLM-4.5 family 技术报告笔记]]

