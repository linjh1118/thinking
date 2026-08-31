---
title: "GLM-4.7-Flash — 30B-A3B 轻量 Agent 模型"
type: model-note
year: 2026
url: "https://huggingface.co/zai-org/GLM-4.7-Flash"
tags: [model-note, base-model, glm, flash, coding, agent]
status: read
created: 2026-09-01
updated: 2026-09-01
---

# GLM-4.7-Flash

> [!tldr]
> **GLM-4.7-Flash 是 GLM-4.7 family 的 30B-A3B MoE 独立开放权重模型，专门在本地部署成本、coding 和多轮 agent execution 之间取平衡；它不是 GLM-4.7-FP8。**

## 一页速览

| 维度 | GLM-4.7-Flash |
|---|---|
| 发布时间 | 2026-01 |
| 参数 | 30B total / 3B activated |
| 架构 | Lightweight MoE |
| 输出 | 最长 131K tokens（官方推荐配置） |
| 强项 | Coding、SWE、tool use、preserved thinking |
| License | MIT |

## 为什么是独立模型叶子

官方 GLM-4.7 collection 同时列出 GLM-4.7、GLM-4.7-FP8 与 GLM-4.7-Flash。Flash 有独立架构规模、模型卡和权重；FP8 只是数值精度版本。Atlas 因此单列 Flash，但不把 FP8 再冒充新模型。

## Agent 使用要点

官方模型卡把 preserved thinking 明确用于 Terminal-Bench、τ²-Bench 等多轮 agent task。这里的重点不是延长一次性 CoT，而是在跨轮工具调用时保留任务状态与推理连续性。轻量激活让它更适合作为高并发 coding agent 或本地执行模型。

> [!insight]
> 30B-A3B 的意义是让 agent rollout 数量变得可扩展：同样算力下可以采更多轨迹、运行更长环境交互，再用 verifier 选择或训练，而不是只追求单次调用最强。

## 一手资料

- [GLM-4.7-Flash · Hugging Face](https://huggingface.co/zai-org/GLM-4.7-Flash)
- [[GLM-4.7|GLM-4.7 family 总览]]
- [[src/Official Source|本地官方来源摘录]]

