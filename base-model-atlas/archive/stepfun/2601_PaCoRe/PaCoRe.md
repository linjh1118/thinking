---
title: "PaCoRe: Learning to Scale Test-Time Compute with Parallel Coordinated Reasoning"
type: paper
authors: ["Jingcheng Hu", "Yinmin Zhang", "Shijie Shang", "Xiaobo Yang", "Yue Peng", "Zhewei Huang", "Hebin Zhou", "Xin Wu", "Jie Cheng", "Fanqi Wan", "Xiangwen Kong", "Chengyuan Yao", "Kaiwen Yan", "Ailin Huang", "Hongyu Zhou", "Qi Han", "Zheng Ge", "Daxin Jiang", "Xiangyu Zhang", "Heung-Yeung Shum"]
year: 2026
venue: arXiv
arxiv: "2601.05593"
doi:
url: "https://arxiv.org/abs/2601.05593"
tags: [paper, llm, test-time-compute, reasoning, parallel-reasoning]
status: read
rating: 5
topic: "13_base_model"
related: []
created: 2026-06-12
---

> [!tldr]
> PaCoRe 通过多轮并行协调推理（Parallel Coordinated Reasoning）将测试时计算（TTC）扩展到数百万 token 级别——在固定上下文窗口约束下，通过消息传递架构协调大量并行推理轨迹，并将每轮的完整轨迹压缩为结论消息，从而实现 TTC 与上下文窗口的解耦。8B 模型在 HMMT 2025 上达到 94.5%，超越 GPT-5 的 93.2%。

## 问题与动机

当代语言模型在长上下文推理时面临一个根本矛盾：标准序贯推理（chain-of-thought）将所有中间状态压缩在单条不断扩展的推理链中，推理量严格受限于上下文窗口容量。一旦窗口填满，推理必须停止，无法继续 scaling test-time compute（TTC）。

核心瓶颈：
- **上下文窗口硬上限**：固定上下文窗口对 TTC 构成了硬性天花板
- **推理孤立主义（Reasoning Solipsism）**：并行分支产生的丰富信息被忽略，模型各自独立从头解题
- **简单聚合策略失效**：多数投票等简单策略在复杂解结构（代码生成、定理证明）上效果有限

## 方法核心思路：PaCoRe 框架

### 推理流程：多轮协调推理（Coordinated Reasoning）

PaCoRe 推理管道执行 $R$ 轮协调推理，每轮包含两个阶段：

1. **综合与并行探索（Synthesis and Parallel Exploration）**
   - 给定问题 $x$ 和上一轮压缩消息 $M_{r-1}$，用提示函数 $P(x, M_{r-1})$ 序列化输入
   - 核心推理模型 $\pi_r$ 并行生成 $K_r$ 条独立推理轨迹：$\omega_r^{(i)} \sim \pi_r(\cdot | P(x, M_{r-1}))$
   - 有效 TTC = 所有轨迹的 token 总和 $\sum_r \sum_i |\omega_r^{(i)}|$，但每轮输入只消耗 $|x| + |M_{r-1}|$（几乎恒定上下文成本）

2. **消息压缩（Message Compaction）**
   - 将完整轨迹 $\Omega_r$ 压缩为下一轮消息集 $M_r = \mathcal{C}(\Omega_r)$
   - 压缩函数 $\mathcal{C}$ 只保留每条轨迹的最终结论段（final conclusion），丢弃中间推导步骤
   - 关键效果：有效 TTC 可扩展到数百万 token，同时输入长度始终被约束在上下文窗口内

**迭代协调**：重复 $R$ 轮，最后一轮 $K_R = 1$，输出最终结论 $y = m_R^{(1)}$。

### 训练流程：大规模 RL 诱导游荡综合能力

PaCoRe 的核心依赖模型具备**综合能力（Synthesis）**——批判性评估输入消息中的多样化视角、协调冲突信息、生成超越任意单一轨迹质量的策略。

**RL 环境设置**：
- 将单轮综合阶段建模为 episode RL 环境
- 训练 episode 中，从训练分布 $D$ 采样问题 $x$ 和消息集 $M$（在线生成或从缓存池采样）
- 策略 $\pi_\theta$ 基于格式化输入 $P(x, M)$ 生成推理轨迹 $\omega$，获得稀疏终端奖励 $R(\omega) \in [0,1]$

**两阶段课程设计**：
- **Stage 1**（250 iterations）：筛选低消息集准确率样本（mean(message_acc) < 9/24 for math; < 15/24 for code），迫使模型学习综合而非简单聚合
- **Stage 2**（450 additional iterations）：使用 Stage 1 中间 checkpoint 评估综合准确率，筛选 0 < synthesis_acc < 1 的实例
- 总计 700 iterations 得到 PaCoRe-8B

**SFT 数据**：61.1B tokens（10.2M samples after filtering），包括数学、代码、科学、软件工程、工具调用、逻辑推理、创意写作等领域。

## 实验结果

### 主实验结果

| Benchmark | AIME 2025 | HMMT 2025 | IMO AnswerBench | Apex | LiveCodeBench | HLE_text | MultiChallenge |
|-----------|-----------|-----------|-----------------|------|---------------|----------|----------------|
| GPT-5 | 93.5 (13k) | 93.2 (16k) | 72.9 (26k) | 1.0 (33k) | **83.5** (13k) | **26.0** (14k) | **71.1** (5.0k) |
| Kimi-K2-Thinking | **95.3** (25k) | 86.5 (33k) | 76.5 (44k) | 0.8 (60k) | 79.2 (25k) | 23.9 (29k) | 66.4 (1.6k) |
| RLVR-8B (baseline) | 84.1 (50k) | 75.4 (48k) | 64.6 (56k) | 0.0 (65k) | 70.6 (34k) | 9.3 (35k) | 33.3 (1.7k) |
| **PaCoRe-8B (low) K=[4]** | 89.7 (255k) | 88.1 (243k) | 76.1 (306k) | 0.7 (362k) | 75.8 (188k) | 13.0 (196k) | 41.8 (13k) |
| **PaCoRe-8B (medium) K=[16]** | 92.5 (908k) | 92.9 (869k) | 77.3 (1080k) | 1.4 (1280k) | 76.7 (659k) | 14.6 (694k) | 45.7 (45k) |
| **PaCoRe-8B (high) K=[32,4]** | 93.7 (1873k) | **94.5** (1796k) | **78.4** (2258k) | 2.3 (2679k) | 78.2 (1391k) | 16.0 (1451k) | 48.0 (95.3k) |

> 表格中数字为准确率，括号内为每题 TTC（单位：千 token）

### 与 Self-Consistency 对比

| Method | Setting | AIME 2025 | HMMT 2025 | IMO AnswerBench | Apex |
|--------|---------|-----------|-----------|-----------------|------|
| Self-Consistency | @4 | 87.0 (194k) | 82.3 (193k) | 69.7 (226k) | 0.3 (249k) |
| Self-Consistency | @64 | 89.5 (3106k) | 85.1 (3094k) | 72.8 (3615k) | 0.0 (3981k) |
| Self-Consistency | @256 | 90.0 (12422k) | 84.7 (12376k) | 73.0 (14458k) | 0.0 (15924k) |
| **PaCoRe (high)** | K=[32,4] | **93.7** (1873k) | **94.5** (1796k) | **78.4** (2258k) | **2.3** (2679k) |

> Self-Consistency 在 256 次采样时 TTC 达到 ~16M token 就已饱和，而 PaCoRe 高效利用 TTC，效果持续提升。

### 消融实验

**第二轮宽度 $K_2$（配置 $\vec{K} = [32, K_2]$）**：

| $K_2$ | HMMT 2025 | LiveCodeBench (2408-2505) |
|-------|-----------|--------------------------|
| 2 | 94.0 | 77.4 |
| **4** | **94.6** | **78.4** |
| 8 | 94.0 | 77.5 |

**消息集大小 $|M|$ 训练策略**：

| Setting | HMMT 2025 | LiveCodeBench |
|---------|-----------|--------------|
| $|M|=4$ | 83.6 | 63.3 |
| $|M|=8$ | 83.7 | 64.4 |
| $|M|=16$ | 84.2 | 64.1 |
| $|M|\sim U(1,16)$ | 84.3 | 64.3 |
| **$|M|\sim U(8,16)$** | **85.2** | **65.1** |

**SWE-Verified 泛化结果**：

| Model | SWE-Verified |
|-------|-------------|
| RLVR-8B | 29.8% |
| **PaCoRe-8B (low)** | **34.0%** |

## 对研究的启发

> [!insight]
>
> **1. TTC  Scaling 新范式**：PaCoRe 证明了 TTC 可以通过"并行协调"而非"深度序贯"来 scaling，将 TTC 从上下文窗口约束中解耦，这是一个根本性的范式转变。
>
> **2. 消息压缩是 TTC Scaling 的关键**：将完整轨迹压缩为结论消息（message compaction），使得 TTC 可扩展到 ~2M token 而不超出上下文窗口——这为后续多模态、长程 Agent 提供了新思路。
>
> **3. RL 是诱导游荡综合能力的必要条件**：没有 RL 训练，模型会陷入"推理孤立主义"（Reasoning Solipsism）——忽略并行分支输入，独立从头解题。大规模 outcome-based RL 强迫模型学会综合（Synthesis）。
>
> **4. Emergent Correctness Rate**：模型在所有输入消息都错误时，仍能生成正确答案——这说明模型学到了"从错误中重建"的元认知能力，而非简单的多数投票。
>
> **5. PaCoRe 数据本身就是高质量 RL 训练资源**：仅用 50 iterations 的 RLVR 在 PaCoRe 数据集上微调，就能显著提升 AIME 和 LiveCodeBench 表现，说明"需要真正综合而非简单聚合"的数据筛选标准是关键。
>
> **6. 局限与开放问题**：目前 PaCoRe 仅验证于 8B 模型，在更大模型上是否同样有效？消息压缩策略（仅保留结论段）是否还有其他信息损失？多模态场景（如视觉推理）能否迁移？
