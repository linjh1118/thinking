---
title: "Step 3.5 Flash: Open Frontier-Level Intelligence with 11B Active Parameters"
type: paper
authors: ["Ailin Huang", "Ang Li", "Aobo Kong", "Bin Wang", "et al."]
year: 2026
venue: arXiv
arxiv: "2602.10604"
doi:
url: "https://arxiv.org/abs/2602.10604"
tags: [paper, base_model, MoE, agentic, stepfun]
status: read
rating: 5
topic: "13_base_model"
related: []
created: 2026-06-12
---

# Step 3.5 Flash: Open Frontier-Level Intelligence with 11B Active Parameters

> [!tldr]
> Step 3.5 Flash 是一个 196B MoE 模型，激活参数仅 11B，通过 3:1 滑动窗口/全注意力混合 + MTP-3 + 可扩展 RL 框架，在 AIME 2025 (97.3%)、LiveCodeBench-v6 (86.4%)、tau2-Bench (88.2%) 等基准上达到前沿水平，同时在 OpenRouter 上实现 ~170 tokens/s 的推理速度，重新定义了 agentic 智能的效率边界。

## 问题与动机

开源 LLM 在复杂推理和 agentic 任务上仍落后于闭源前沿模型，同时长上下文 agentic 部署面临严重的效率瓶颈。核心问题：**如何在 11B 激活参数的效率约束下，实现与数百 B 参数模型相当的前沿级推理和工具使用能力？**

## 方法核心思路

### 1. 高效架构设计

| 组件 | 配置 |
|------|------|
| 总参数量 | 196B |
| 激活参数量 | 11B/token |
| Transformer 层 | 45（3 dense + 42 MoE） |
| MoE 配置 | 288 experts + 1 shared expert，top-8 路由 |
| 注意力布局 | **3:1 SWA:Full（S3F1）**，SWA window=512 |
| KV Heads | GQA-8 |
| MTP | 3 个 Dense SWA 块 |
| 头门控注意力 | Head-wise gated attention，替代固定 sink token |

**关键设计**：
- **S3F1 布局**：每 4 层 = 3 层 SWA + 1 层全注意力，兼顾局部建模与全局上下文
- **Head-wise Gated Attention**：引入输入依赖的 sink token 机制，将 SWA query heads 从 64 扩展到 96，在额外计算开销极小的情况下显著提升性能
- **MTP-3**：多 token 预测，total params 198B，激活 13B/token

### 2. 预训练稳定性

- **Muon 优化器**：比 Adam 更准确稳定的梯度更新
- **轻量级异步监控**：微批量级连续日志，及时识别专家崩溃、激活爆炸等故障模式
- **激活裁剪（Activation Clipping）**：解决 SwiGLU + Muon 组合下的 logit 爆炸问题
- 在 17.2T tokens 训练中仅出现**一次短暂 loss spike**

### 3. 可扩展 RL 后训练框架

**两阶段后训练**：
1. **统一 SFT 基础**：多领域（Math/Code/STEM/Logic/Agent/Long Context）SFT，871k samples，7.23B tokens
2. **领域特定 RL → 自蒸馏 → 可扩展 RL 循环**：专家模型生成高质量轨迹，通过拒绝采样消除不良模式，集中专家知识到单一学生模型

**MIS-PO（Metropolis Independence Sampling-Filtered Policy Optimization）**：
- 核心思想：将推理策略作为提议分布，训练策略作为目标，通过二元掩码过滤离策略样本
- 在 token 级别和轨迹级别同时应用离散过滤（token-level: [0.5, 2], trajectory-level: [0.996, 1.001]）
- 相比 PPO，梯度噪声显著降低，MoE 大规模 RL 训练稳定可扩展

**奖励系统**：
- **RLVR（可验证奖励）**：STEM 用 gpt-oss-120b verifier，Code 用沙箱执行验证
- **GenRM（生成奖励模型）**：pairwise 偏好学习 + MetaRM 验证防止虚假推理
- **Agent Reward**：搜索任务用 LLM 实体匹配评分，研究报告用 rubric-based ternary judgment

**PaCoRe（Parallel Coordinated Reasoning）**：多轮并行推理轨迹合成，将推理能力从上下文限制中解耦

## 实验结果

### 预训练结果（Base 模型 vs 更大模型）

| Benchmark | Step 3.5 Flash Base | DeepSeek V3.2 Exp Base (671B) | Kimi K2 Base (1043B) |
|-----------|---------------------|-------------------------------|----------------------|
| MMLU | 85.8 | 87.8 | 87.8 |
| SimpleQA | **31.6** | 27.0 | 35.3 |
| HumanEval | **81.1** | 67.7 | 84.8 |
| MATH | 66.8 | 62.5 | 70.2 |
| C-EVAL | 89.6 | 91.0 | **92.5** |

> [!insight]
> 仅用 1/3 参数（196B vs 671B）即在 SimpleQA 上超越 DeepSeek V3.2 Exp，展示了极高的能力密度。

### 后训练结果（与前沿模型对比）

#### Reasoning

| Benchmark | Step 3.5 Flash | PaCoRe | Gemini 3.0 Pro | Claude Opus 4.5 | GPT-5.2 xHigh |
|-----------|---------------|--------|----------------|-----------------|---------------|
| AIME 2025 | 97.3 | 99.9 | 95.0 | 92.8 | 100.0 |
| IMO-AnswerBench | 85.4 | 88.8 | 83.3 | 84.0 | 86.3 |
| LiveCodeBench-v6 | 86.4 | 88.9 | 90.7 | 84.8 | 87.7 |
| HMMT 2025 Feb. | **98.4** | **100.0** | 97.5 | 92.9 | 99.4 |
| GPQA-Diamond | 83.5 | 85.0 | 91.9 | 87.0 | 92.4 |

#### Code Agent

| Benchmark | Step 3.5 Flash | Kimi K2.5 | Claude Opus 4.5 | GPT-5.2 xHigh |
|-----------|---------------|-----------|-----------------|---------------|
| SWE-Bench Verified | 74.4 | 76.8 | **80.9** | 80.0 |
| SWE-Bench Multilingual | 67.4 | **73.0** | 77.5 | 72.0 |
| Terminal-Bench 2.0 | 51.0 | 50.8 | **59.3** | 54.0 |

#### General Agent

| Benchmark | Step 3.5 Flash | Kimi K2.5 | Gemini 3.0 Pro |
|-----------|---------------|-----------|---------------|
| BrowseComp (w. Ctx) | 69.0 | **74.9** | 59.2 |
| GAIA | **84.5** | 75.9 | 76.6 |
| tau2-Bench | 88.2 | 85.4 | **90.7** |
| ResearchRubrics | **65.3** | 59.5 | 50.1 |

## 对研究的启发

> [!insight]
> **MIS-PO 的离散过滤思想**：连续重要性加权在长 horizon 推理中天然不稳定，离散的二元掩码（接受/拒绝）比连续 ratio clipping 更有效。这对其他长上下文 RL 训练（如agentic coding、deep research）有直接参考价值。

> [!insight]
> **S3F1 + Head-wise Gating 的效率组合**：将 SWA query heads 从 64 扩展到 96，在几乎不增加延迟的情况下（IO-bound 区域）大幅弥合了 hybrid attention 与全注意力的性能差距。这种"小改动大收益"的架构优化思路值得借鉴。

> [!insight]
> **效率边界的重新定义**：196B/11B 的 Step 3.5 Flash 在多个基准上与 671B~1T 参数模型相当，证明了**稀疏 MoE + 混合注意力 + 短序列注意力**的组合是未来高效 frontier-level agent 模型的可行路径，而非单纯追求参数量。

## 相关工作

[[Step 3.5 Flash Poster|Step-3.5-Flash_poster_zh.html]]
