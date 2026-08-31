---
title: "MiroThinker-1.7 & H1: Towards Heavy-Duty Research Agents via Verification"
type: paper
authors: ["MiroMind Team", "S. Bai", "L. Bing", "L. Lei"]
year: 2026
venue: arXiv
arxiv: "2603.15726"
url: "https://arxiv.org/abs/2603.15726"
tags: [paper, miromind, research-agent, verification, reasoning]
topic: "13_base_model"
status: read
rating: 5
created: 2026-05-30
---

# TL;DR

MiroThinker-H1 是 **Verification Agent 最强代表**，核心创新是将验证直接嵌入推理过程：Local Verification 评估中间推理步骤，Global Verification 审计整体推理轨迹。开源版本 MiroThinker-1.7 和 MiroThinker-1.7-mini 也在 GAIA、HLE、Financial Analysis 等 benchmark 上展现了竞争力。

## 问题与动机

### 复杂长程推理的挑战

1. **交互步骤可靠性**：每个交互步骤的错误会级联传播
2. **整体推理一致性**：最终答案需要连贯的证据链支撑
3. **Research Agent 的 heavy-duty 要求**：需要处理 open-web research、scientific reasoning、financial analysis

## 方法核心思路

### MiroThinker-1.7: Agentic Mid-training

强调三大能力：
- Structured planning（结构化规划）
- Contextual reasoning（上下文推理）
- Tool interaction（工具交互）

→ 更有效的多步交互和复杂任务上的持续推理

### MiroThinker-H1: Verification-Enhanced Reasoning

**核心创新：将 Verification 嵌入推理过程**

#### Local Verification（局部验证）

- 中间推理决策可以被评估和 refine
- 每个 reasoning step 都有 self-checking 机制
- 不正确的中间结论被即时修正

#### Global Verification（全局验证）

- 审计整体推理轨迹
- 确保最终答案被连贯的证据链支撑
- 反向检查：从结论倒推到前提

### 技术架构

```
┌─────────────────────────────────────────────────────┐
│                  MiroThinker System                 │
├─────────────────────────────────────────────────────┤
│  ┌─────────────┐    ┌─────────────┐               │
│  │  Planner    │───→│  Reasoner   │               │
│  └─────────────┘    └─────────────┘               │
│         ↓                  ↓                       │
│  ┌─────────────────────────────────────────────┐   │
│  │           Verification Module               │   │
│  │  ┌─────────────┐  ┌─────────────┐          │   │
│  │  │Local Verify │  │Global Verify│          │   │
│  │  └─────────────┘  └─────────────┘          │   │
│  └─────────────────────────────────────────────┘   │
│         ↓                  ↓                       │
│  ┌─────────────┐    ┌─────────────┐               │
│  │   Tool      │    │  Memory     │               │
│  │  Executor   │    │  Manager    │               │
│  └─────────────┘    └─────────────┘               │
└─────────────────────────────────────────────────────┘
```

## 关键结果

| Benchmark | MiroThinker-H1 | MiroThinker-1.7 |
|-----------|----------------|-----------------|
| Open-web Research | SOTA | Strong |
| Scientific Reasoning | SOTA | Strong |
| Financial Analysis | SOTA | Strong |

## 对研究的启发

> [!insight]
> 1. **Verification Agent** 的设计思路对 GUI Agent 很有价值——GUI 任务的中间步骤（点击、输入）也需要验证是否正确执行
> 2. Local/Global Verification 的分层设计值得借鉴
> 3. **MiroThinker-1.7 开源**，可以直接使用或微调

## 相关链接

- 论文: [arXiv Link](https://arxiv.org/abs/2603.15726)
- Demo: [https://dr.miromind.ai](https://dr.miromind.ai)
- GitHub: [MiroMindAI/MiroThinker](https://github.com/MiroMindAI/MiroThinker)
- Model: [MiroThinker-1.7 on HuggingFace](https://huggingface.co/miromind-ai/MiroThinker-1.7)
