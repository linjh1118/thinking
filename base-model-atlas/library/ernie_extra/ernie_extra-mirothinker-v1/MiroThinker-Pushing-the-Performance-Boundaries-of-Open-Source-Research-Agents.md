---
title: "MiroThinker v1.0: Interaction Scaling as a Third Dimension"
type: paper
authors: ["MiroMind Team", "Song Bai", "Lidong Bing", "Carson Chen"]
year: 2025
venue: arXiv
arxiv: "2511.11793"
url: "https://arxiv.org/abs/2511.11793"
tags: [paper, miromind, interaction-scaling, tool-augmented, research-agent]
topic: "13_base_model"
status: read
rating: 5
created: 2026-05-30
---

# TL;DR

**MiroThinker v1.0 提出 Interaction Scaling（交互扩展）作为性能提升的第三维度**，与 model size 和 context length 并列。核心发现：随着 agent-environment 交互深度增加，research performance 呈现可预测的提升（类似 scaling law）。72B 模型在 GAIA (81.9%), HLE (37.7%), BrowseComp (47.1%) 上超越之前的开源 agent，逼近 GPT-5-high。

## 核心洞察

### 三大 Scaling 维度

| 维度 | 描述 | 之前的工作 |
|------|------|-----------|
| **Model Size** | 更大的模型参数 | 主流方向 |
| **Context Length** | 更长的上下文窗口 | 主流方向 |
| **Interaction Scaling** | 更深更频繁的 agent-environment 交互 | MiroThinker 首创 |

### 为什么 Interaction Scaling 重要？

- **LLM test-time scaling 的局限**：孤立操作，longer reasoning chains 可能退化
- **Interactive scaling 的优势**：利用环境反馈和外部信息获取来纠正错误和优化轨迹

## 方法核心思路

### Interactive Scaling via RL

通过强化学习训练模型进行更深、更频繁的 agent-environment 交互：

- **256K context window**：支持最多 600 tool calls per task
- **Sustained multi-turn reasoning**：支持复杂的真实世界研究工作流

### 关键发现

> "Research performance improves predictably as the model engages in deeper and more frequent agent–environment interactions"

这意味着 **Interaction depth exhibits scaling behaviors analogous to model size and context length**

## 关键结果

| Benchmark | MiroThinker-72B | Previous SOTA (Open) |
|-----------|-----------------|---------------------|
| GAIA | 81.9% | - |
| HLE | 37.7% | - |
| BrowseComp | 47.1% | - |
| BrowseComp-ZH | 55.6% | - |

**接近 GPT-5-high 的商业水平**

## 对研究的启发

> [!insight]
> 1. **Interaction Scaling** 为 GUI Agent 研究提供了新视角——不仅仅是更大模型或更长上下文，还包括更深的交互
> 2. Scaling law 在 interaction depth 上也成立，这对 GUI Agent 的训练有指导意义
> 3. 600 tool calls per task 的能力对复杂 GUI 任务（如超长操作序列）很有价值
> 4. **开源可用**，可以直接使用 MiroThinker-v1.0-72B

## 相关链接

- 论文: [arXiv Link](https://arxiv.org/abs/2511.11793)
- Demo: [https://dr.miromind.ai](https://dr.miromind.ai)
- GitHub: [MiroMindAI/MiroThinker](https://github.com/MiroMindAI/MiroThinker)
- Model: [MiroThinker-v1.0-72B on HuggingFace](https://huggingface.co/miromind-ai/MiroThinker-v1.0-72B)
