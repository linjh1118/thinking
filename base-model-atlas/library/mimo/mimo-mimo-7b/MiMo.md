---
title: "MiMo: Unlocking the Reasoning Potential of Language Model"
type: paper
authors:
  - Xiaomi LLM-Core Team
year: 2025
venue: arXiv
arxiv: "2505.07608"
doi:
url: https://arxiv.org/abs/2505.07608
tags:
  - paper
  - reasoning
  - base-model
  - rl
  - mtp
  - grpo
  - code-generation
  - math-reasoning
topic: 13_base_model
status: read
rating: 5
related:
  - "[[Topics/13_base_model/Xiaomi_MiMo/2506_MiMo_VL_7B/MiMo-VL]]"
  - "[[Topics/13_base_model/Xiaomi_MiMo/2601_MiMo_V2_Flash/MiMo-V2-Flash]]"
  - "[[Topics/13_base_model/Xiaomi_MiMo/2606_MiMo_Series/MiMo-Series-From-7B-Reasoning-Model-to-Omnimodal-Agent-Foundation-Models]]"
created: 2026-06-11
---

# MiMo: Unlocking the Reasoning Potential of Language Model

> [!tldr]
> 小模型也可以有强推理能力。MiMo-7B（7B 参数）在 25T tokens 预训练 + 三阶段 data mixture + MTP 的基础上，通过 130K 可验证 math/code RL 数据 + test-difficulty-driven reward + Seamless Rollout Engine（2.29× 训练加速），在 AIME 2025 上达到 55.4，超越 o1-mini 的 50.7。核心洞察：推理能力的瓶颈不在模型规模，而在预训练数据的 reasoning density 和后训练的 reward 设计。

## 问题与动机

现有 LLM Scaling 的两条路：Scale up（更大的模型）和 Scale compute（更多的 RL 训练）。小米选择的是第三条路：**不靠参数规模，靠预训练数据质量和后训练 recipe**。

核心问题：
- 7B 模型能否通过高质量预训练数据 + 精细 RL recipe 达到 30B+ 模型的推理水平？
- RL 后训练的瓶颈是什么？如何解决 sparse reward 问题？

## 方法核心思路

### 1. 预训练：从数据工程开始强化 reasoning potential

**三阶段 Data Mixture：**

| 阶段 | Context | 数据配比 | 关键动作 |
|------|---------|---------|---------|
| Stage 1 | 8K | 均衡 diverse corpus | 降采样过度代表的内容（广告、新闻、招聘信息） |
| Stage 2 | 8K | Math/Code 提升到 ~70% | 提高推理密度 |
| Stage 3 | 32K | ~10% synthetic reasoning responses | 扩展上下文 + 合成推理数据 |

**MTP（Multi-Token Prediction）：**
- 单个 MTP layer 在预训练阶段使用
- 推理时用多个 MTP layers 做 speculative decoding
- 既提升训练效果，也为 decoding 加速留了接口

**改进 HTML/PDF 解析**：保留数学公式、代码块和 STEM 结构，而不是把复杂内容 flatten 成纯文本。

### 2. 后训练：Test-Difficulty-Driven Code Reward

**RL 数据构造**：
- 100K 数学问题 + 30K 代码问题 = 130K 可验证问题
- Rule-based reward 为主，降低 reward hacking 风险

**IOI-inspired scoring**（test-difficulty-driven reward）：
- 传统 binary pass/fail reward 太粗糙
- 新方案：对于每个测试用例，按难度（pass 人数比例）赋权重
- 鼓励模型通过所有测试用例，特别是困难测试用例

**Easy Data Re-sampling**：
- 10% 概率从 easy pool 重新采样，防止模型在简单数据上过拟合
- 动态采样策略提升训练稳定性

**GRPO 算法**：去除 KL loss，动态采样，clip-higher

### 3. 基础设施：Seamless Rollout Engine

GPU idle time 的主要来源：
- Rollout 和 reward computation 的串行依赖
- Validation 的额外计算开销

**优化方案**：
- Continuous rollout：rollout 连续进行，不等待 reward
- Async reward computation：reward 计算异步执行
- Early termination：简单样本提前终止

**结果**：Training speedup 2.29×，Validation speedup 1.96×

## 实验结果

### MiMo-7B-Base（表1）

| Benchmark | Score |
|-----------|-------|
| BBH | 75.2 |
| LiveCodeBench v5 | 32.9 |
| AIME 2024 | 32.9 |
| AIME 2025 | 24.3 |
| MATH | 37.4 |
| SuperGPQA | 25.1 |

**关键发现**：Base model 在 BBH 75.2 已经超过很多 32B 模型，说明 reasoning potential 来自数据质量而非参数规模。

### MiMo-7B-RL vs o1-mini（表4）

| Benchmark | o1-mini | MiMo-7B-RL |
|-----------|---------|------------|
| AIME 2025 | 50.7 | **55.4** ✅ |
| LiveCodeBench v5 | 53.8 | **57.8** ✅ |
| LiveCodeBench v6 | 46.8 | **49.3** ✅ |
| MATH500 | 90.0 | **95.8** ✅ |

7B 模型在所有评测上超越 o1-mini。

### MiMo-7B-RL-0530（扩展训练后）

| Benchmark | Score |
|-----------|-------|
| AIME 24 | **80.1** |
| AIME 25 | **70.2** |
| MATH500 | **97.2** |

48K generation budget + extended training 带来进一步提升。

## 对研究的启发

> [!insight]
> MiMo-7B 证明了推理能力的瓶颈不在参数规模，而在：(1) 预训练数据的 reasoning density，(2) RL reward 的精细程度。Test-difficulty-driven reward 是 code generation RL 的一个重要改进方向，比 binary reward 信息量更大，比 learned reward model 更稳定。

**可转化的问题**：
- GUI grounding 任务的 test-difficulty 如何定义？能否用 GUI 测试用例的 pass rate 作为 difficulty signal？
- 多模态推理的 reward 如何设计？visual reasoning 的"正确答案"可能不止一个
- Seamless Rollout Engine 的 continuous rollout 设计是否能迁移到 GUI agent RL 训练？

## 相关资料

- arXiv：https://arxiv.org/abs/2505.07608
- 系列总览：[[Topics/13_base_model/Xiaomi_MiMo/2606_MiMo_Series/MiMo-Series-From-7B-Reasoning-Model-to-Omnimodal-Agent-Foundation-Models]]
- MiMo-VL：[[Topics/13_base_model/Xiaomi_MiMo/2506_MiMo_VL_7B/MiMo-VL]]
