---
title: "Gemini 2.5: Pushing the Frontier with Advanced Reasoning, Multimodality, Long Context, and Next Generation Agentic Capabilities"
type: paper
authors: ["Gemini Team, Google"]
year: 2025
venue: arXiv
arxiv: "2507.06261"
url: "https://arxiv.org/abs/2507.06261"
tags: [paper, gemini, multimodal, reasoning]
topic: "13_base_model"
status: read
rating: 5
created: 2026-05-30
---

# TL;DR

Gemini 2.5 是 Google 迄今为止最强大的 Thinking 模型系列，在编码、推理、长上下文和多模态理解方面达到 SoTA 性能。核心创新在于将 RL训练的 Thinking 能力与原生多模态、长上下文（1M tokens）深度融合，使得模型能够在推理时通过增加计算成本来提升答案质量。

## 问题与动机

Gemini 1.5 系列奠定了长上下文（1M tokens）和原生多模态的基础，但推理能力有限。Gemini 2.5 的核心动机是：**将 Thinking（思考）能力与 Gemini 的多模态、长上下文优势结合**，从而支撑更复杂的 agentic 工作流。

核心问题：
1. 如何在推理时通过额外的计算成本换取更高的准确率？
2. 如何将 Thinking 能力与多模态理解、长上下文融合？
3. 如何覆盖从日常任务到复杂编码的全谱系需求？

## 方法核心思路

### 1. Thinking 机制

Gemini 2.5 的 Thinking 模型使用强化学习训练，在推理时花费数万步 forward pass 来"思考"后再回答。关键特性：

- **可调节的 Thinking Budget**：用户可以设置模型用于内部思考的 token 数量
- **Scaling 特性**：增加 Thinking Budget 可持续提升准确率（AIME 2025 从 29.7% 提升到 88.0%）
- **原生融合**：与多模态输入（图像、文本、视频、音频）和长上下文（1M+ tokens）深度集成

### 2. 模型架构

- **Sparse Mixture-of-Experts (MoE)** Transformer
- 原生多模态支持（文本、视觉、音频输入）
- 蒸馏技术用于小模型（Flash 及以下），使用 k-sparse 近似教师分布

### 3. 能力融合

Gemini 2.5 的关键突破是多种能力的融合：
- **长上下文 + 推理**：可处理 3 小时视频内容
- **多模态 + 工具使用**：支持 Google Search 等工具调用
- **代码 + 推理**：在代码库级别理解任务上展现出 emergent 能力

## 关键结果

### 核心 benchmark 性能（Gemini 2.5 Pro）

| 能力 | Benchmark | Gemini 2.5 Pro | Gemini 1.5 Pro |
|------|-----------|----------------|----------------|
| **Code** | LiveCodeBench | **74.2%** | 29.7% |
| **Code** | Aider Polyglot | **82.2%** | 16.9% |
| **Code** | SWE-bench Verified (multi) | **67.2%** | 34.2% |
| **Math** | AIME 2025 | **88.0%** | 17.5% |
| **Reasoning** | GPQA (diamond) | **86.4%** | 58.1% |
| **Factuality** | SimpleQA | **54.0%** | 24.9% |
| **Long-context** | LOFT 1M | **69.8%** | 47.1% |
| **Image Understanding** | MMMU | **82.0%** | 67.7% |

### 与其他 LLM 对比（Gemini 2.5 Pro vs 主要竞品）

Gemini 2.5 Pro 在多个维度领先：
- **Coding**: Aider Polyglot 最高 (82.2%)
- **Reasoning**: GPQA diamond 最高 (86.4%)
- **Factuality**: SimpleQA 和 FACTS Grounding 均为最高
- **Long-context**: 唯一支持 1M+ tokens 的模型，LOFT 1M 得分 69.8%
- **Video Understanding**: VideoMME (audio+visual+subtitles) 达到 **86.9%**

### 模型家族

| 模型 | 特点 | Thinking | 输入长度 | 输出长度 |
|------|------|----------|----------|----------|
| Gemini 2.5 Pro | 最强推理、代码能力 | Dynamic | 1M | 64K |
| Gemini 2.5 Flash | 高性价比思考模型 | Dynamic | 1M | 64K |
| Gemini 2.0 Flash | 快速日常任务 | Yes* | 1M | 8K |
| Gemini 2.0 Flash-Lite | 最低成本 | No | 1M | 8K |

## 对研究的启发

> [!insight]
> 1. **Thinking + 多模态的融合是趋势**：Gemini 2.5 展示了将 Thinking 能力与原生多模态结合的可能性，这对 GUI Agent 的多模态理解有直接启示。
>
> 2. **推理时计算 Scaling 的实际价值**：通过增加 Thinking Budget 可以持续提升准确率，这意味着在复杂任务上可以通过分配更多推理资源来解决问题。
>
> 3. **长上下文 + Agentic Workflow**：1M token 上下文窗口使得处理整个代码仓库成为可能，为 codebase-level 的 GUI Agent 研究提供了基础。
>
> 4. **工具使用与 Thinking 的结合**：Gemini 2.5 可以将 Thinking 与 Google Search 等工具调用交织，这是构建复杂 agentic 系统的核心能力。

## 相关链接

- 论文: [arXiv 2507.06261](https://arxiv.org/abs/2507.06261)
- 源码: LaTeX 源码位于 `2507_Gemini_2_5/src/`
