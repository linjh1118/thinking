---
title: "StepFun-Formalizer: Unlocking the Autoformalization Potential of LLMs through Knowledge-Reasoning Fusion"
type: paper
authors: ["Yutong Wu", "Di Huang", "Ruosi Wan", "Yue Peng", "Shijie Shang", "et al."]
year: 2025
venue: arXiv
arxiv: "2508.04440"
tags: [paper, autoformalization, rlvr, math-ai, lean4]
topic: "13_base_model"
status: read
rating: 5
created: 2026-06-12
related: []
---

> [!tldr]
> StepFun-Formalizer 提出 ThinkingF 数据合成流水线，解决 autoformalization 的两大问题：形式语言领域知识不足 + 非正式到正式的对齐推理能力弱。通过知识蒸馏 + 推理轨迹合成 + SFT + RLVR，32B 模型在 FormalMATH-Lite 达到 BEq@1 40.5%（SOTA），7B 也超越所有 671B 通用模型。

## 问题与动机

Autoformalization（自然语言数学→Lean 4 形式化语言）面临两大挑战：

1. **形式语言知识缺失**：通用 LLM 在 formal corpus 稀缺，不知道 Euler totient function 在 Lean 4 中如何定义
2. **非正式→正式对齐推理能力弱**：无法理解自然语言问题的实际意图，且 informal→formal 之间存在隐式信息需显式化

现有方法（直接蒸馏通用模型 / 专用模型）都存在低准确率问题，需要大量人工修正。

## 方法核心：ThinkingF Pipeline

### 双数据集策略

| 数据集 | 来源 | 解决的问题 |
|--------|------|-----------|
| **知识数据** | KMAuto 蒸馏大量 NL→Lean pairs | 形式语言领域知识 |
| **推理数据** | 专家模板引导 Claude 合成 reasoning 轨迹 | informal-formal 对齐 |

### 两阶段 SFT

1. **Stage 1（知识融合）**：使用知识数据集，模型学习形式语言表达
2. **Stage 2（推理能力）**：使用推理轨迹数据，enclose reasoning 在 `<think>`和`</think>` 中

### RLVR (GRPO + DAPO)

- Reward：BEq 等价验证（generated ↔ ground-truth）
- 动态 sampling + token-level loss
- Rollout temperature 1.0

## 关键实验数据

### FormalMATH-Lite / ProverBench / CombiBench (BEq@1)

| Model | Size | FormalMATH-Lite | ProverBench | CombiBench |
|-------|------|----------------|-------------|------------|
| Claude4-thinking | - | 34.0% | 18.4% | 10.0% |
| DeepSeek-R1 | 671B | 29.1% | 17.1% | 8.7% |
| KMAuto | 7B | 38.2% | 17.4% | 13.1% |
| **StepFun-Formalizer** | **7B** | **39.6%** | **24.0%** | **17.6%** |
| **StepFun-Formalizer** | **32B** | **40.5%** | **26.7%** | **22.5%** |

### End-to-End 定理证明

用 Kimina-Prover-7B 对各模型生成的 formal statements 各 sampling 16 次证明：
- Formalizer-7B → 4,940 可证明 statements
- KMAuto-7B → 4,549 可证明 statements
- **提升 8.6%**

> [!insight]
> 推理数据（reasoning trajectories）比知识数据更重要——移除推理数据后 BEq@16 大幅下降，说明 informal-to-formal reasoning 是性能上限的主要驱动力。知识数据提供基础，但上限由推理能力决定。

## 研究启发

1. **专家模板 > 直接蒸馏通用推理模型**：用 Claude4-thinking 直接蒸馏推理轨迹会导致性能显著下降，因为通用推理模型在 formalization 时倾向于"解题"而非"形式化"
2. **7B 模型已足够强**：7B 超越所有 671B 通用模型，说明专用训练 > 模型 scale
3. **BEq 验证作为 reward 是可行的**：无需 LLM-as-judge，形式化等价的数学性质使精确验证成为可能
4. **数据合成质量 > 数据量**：知识数据经过 majority voting + LLM judge 筛选，推理数据由专家模板引导，质量比数量更重要
