---
title: "Step-3 is Large yet Affordable: Model-system Co-design for Cost-effective Decoding"
type: paper
authors: ["StepFun Team"]
year: 2025
venue: arXiv
arxiv: "2507.19427"
tags: [paper, infra, moe, attention, inference]
topic: "13_base_model"
status: read
rating: 5
created: 2026-06-12
related: []
---

> [!tldr]
> Step-3 通过 Multi-Matrix Factorization Attention (MFA) 和 Attention-FFN Disaggregation (AFD) 实现极低解码成本。321B 总参/38B 激活模型，在 Hopper GPU 上达到 4,039 tok/s/GPU，比 DeepSeek-V3 高 74%。核心洞察：解码成本由 attention arithmetic intensity 决定，而非参数总量。

## 问题与动机

大语言模型在 decoding 阶段硬件效率极低，尤其长上下文推理场景。现有方法存在两大问题：

1. **Attention 设计**：过度压缩 KV cache 以牺牲计算效率为代价，在弱硬件上运行成本反而更高
2. **MoE FFN**：过度追求稀疏性而忽略硬件适配，导致实际效率不升反降

Step-3 探索 model-system co-design，目标是在多百亿参数规模下实现最低解码成本。

## 方法核心

### MFA (Multi-Matrix Factorization Attention)

核心思想：对 Query-Key 电路做低秩矩阵分解，在减少 KV cache 的同时保持足够计算密度。

配置：64 Q-heads + 1 shared KV-head，Q 投影：7168→2048（低秩）→64×256

### AFD (Attention-FFN Disaggregation)

将 attention 层和 FFN 层部署到不同 GPU 集合，各自使用最优并行策略。Attention 和 FFN 通过高速网络通信形成 3-stage 流水线（A / F / comm 各 16.6ms）。

### MoE 配置

- 61 层 Transformer（除前 4 层和最后一层外全 MoE）
- 1 shared expert
- 总参 316B，激活 38B/token

## 关键实验数据

| 指标 | Step-3 | DeepSeek-V3 | Qwen3 MoE 235B |
|------|--------|-------------|----------------|
| 总参 | 321B | ~236B | ~235B |
| 激活参 | 38B | 动态 | 动态 |
| tok/s/GPU | **4,039** | 2,324 | - |
| 成本节省 | 基准 | +73% | +8% |

> [!insight]
> Qwen3 MoE 总参比 Step-3 少 65%，但解码成本反而高 8%——印证了"参数量 ≠ 解码成本"的论断。MoE 稀疏度必须与硬件的算力/带宽/网络带宽联合考虑。

## AFD vs DeepSeek EP 对比

| 维度 | AFD | DeepSeek EP |
|------|-----|------------|
| 部署规模 | 32 GPU | 320 GPU |
| 上下文效率 | 独立扩展 attention | FFN 利用率低 |
| 负载均衡 | 天然支持混合 TP-EP | 需要 duplicated experts |
| 异构硬件 | 支持 | 不支持 |

## 研究启发

1. **解码成本优化是 test-time scaling 的关键**：更低的解码成本 → 相同的预算下更高的 intelligence
2. **Model-system co-design 才是正道**：单独优化模型或系统都不够，需要联合设计
3. **AFD 释放了 divide-and-conquer 的设计空间**：attention 和 FFN 可以独立演进
4. **线性注意力、量化、MTP 都是好方向，但细节决定成败**：某些设计点看似细微却会移除大部分收益
