---
title: "LongCat-Flash Technical Report"
type: paper
authors: ["Meituan LongCat Team"]
year: 2025
venue: arXiv
arxiv: "2509.01322"
doi:
url: "https://arxiv.org/abs/2509.01322"
tags: [paper, base-model, moe, agentic, meituan, longcat, efficiency]
status: read
rating: 4
topic: "13_base_model/Meituan_LongCat"
related: []
created: 2026-07-01
---

> [!tldr]
> 美团 LongCat 系列的起点：560B MoE / 平均激活 27B 的 **non-thinking foundation model**，靠两个核心架构创新——**Zero-Computation Experts**（动态计算预算）和 **Shortcut-Connected MoE (ScMoE)**（跨层 shortcut 拉长 communication-computation overlap）——在 30 天内训完 20T tokens，H800 推理达 100 TPS、$0.7/M tokens。它的真正价值不是绝对精度第一（和 DeepSeek-V3.1、Kimi-K2 同档），而是 **同等性能下显著更低的推理成本**，这是 agent / 高并发场景的关键卖点。

## 1. 问题与动机

开源 MoE 大模型已经很多（DeepSeek-V3、Kimi-K2、Qwen3、Llama 4），但美团团队认为还有两条没被充分挖掘的杠杆：

1. **计算效率**：MoE 的瓶颈不是算力，是 **all-to-all 通信开销**。shared-expert 的 overlap 窗口太小，comm 时间占比能到 25%。
2. **token 计算异构性**：not all tokens are equal——简单 token 不需要同样的算力，但传统 top-k MoE 给每个 token 都激活固定的 K 个专家。

他们想同时解决这两件事，并且要 **agent-friendly**（mid-training 就把 reasoning/code 数据占比拉到 70%，为后续 agent post-training 做准备）。

## 2. 核心架构创新

### 2.1 Zero-Computation Experts（动态计算预算）

在 N 个正常 FFN 专家之外，再加 Z 个 **identity 专家**——输入直接当输出返回，零计算成本。

- 路由器对所有 N+Z 个专家做 TopK（K=12），实际激活的 FFN 专家数随 token 上下文重要性变化：**18.6B – 31.3B（平均 27B）**
- 用一个 **PID controller** 调整的 expert bias 来控制平均激活比例（公式 2），保证全局计算预算收敛到目标值
- 关键经验：训练 ~20B tokens 后，平均激活专家数稳定在目标值，**fluctuation < 1%**，但 std 持续在 3 左右——说明模型确实在"看 token 给算力"
- Appendix case study 显示浅层把 function words / 数字 / 标点分给 zero experts，深层按预测难度分配——这跟"token difficulty"的直觉一致

> [!insight] 真正的价值
> Zero-computation expert 不是简单"省算力"——它是把 **routing 的离散决策变成了"是否给一个 token 投入计算"的语义**。这跟 spec decoding 里"小模型预测简单 token"的现象是同一个观察的两个侧面。它打开了 dynamic compute allocation 这条路线。

### 2.2 Shortcut-Connected MoE (ScMoE)

借鉴自家 ICCV'24 工作（Cai 2024）。核心改法：从 **前一层的 dense FFN 输出**直接拉一条 shortcut 到当前 MoE 层，让 dense FFN 的计算和当前层的 all-to-all dispatch/combine **完全 overlap**。

- 跟 shared-expert 比：shared expert 只能用一个专家的小计算窗口做 overlap，ScMoE 用整个 dense FFN 的计算窗口，overlap 范围大得多
- 关键证据：2.4B/3B/15B 三个尺寸的 loss curve 显示 **加 ScMoE 和不加 loss 几乎完全重合**（quality-neutral），但 comm 时间占比从 25.3% 降到 8.4%
- 推理端配合 **SBO (Single Batch Overlap)** 4 阶段流水：在单个 batch 内把 MLA / Dense FFN / MoE GEMM / all-to-all 四件事 overlap 起来，TPOT 比 DeepSeek-V3 的 TBO 降低 ~50%

### 2.3 Variance Alignment（让 MoE 可 scale）

两个细节但关键的设计，解决"小尺寸验证的设计到大尺寸失效"问题：

1. **MLA Scale-Correction**：在 $c_t^Q$、$c_t^{KV}$ 前加 $\alpha_q = \sqrt{d_{model}/d_q}$、$\alpha_{kv} = \sqrt{d_{model}/d_{kv}}$，抵消低秩分解引入的 variance mismatch
2. **Fine-grained expert variance compensation**：fine-grained segmentation 把方差缩 $m$ 倍（gating dilution）+ $m$ 倍（hidden dim 减小），所以给 expert 输出乘 $\gamma = m$

## 3. 预训练与稳定性

| 阶段 | 数据量 | 关键策略 |
|------|--------|---------|
| Stage 1 general | ~20T tokens, 8192 seq | SampleMix 实例级数据混合，STEM/code 上采样 |
| Stage 2 reasoning+code | 万亿级 | STEM+code 占 70%，渐进加 code 防止通用能力坍塌 |
| Long context | 8k→32k→128k | RoPE base 1M→5M→10M，repo 级代码做长上下文 |

**Scaling 套件**（让 560B 训练稳定）：
- **Hyperparameter Transfer**：从 width=768 的 proxy model 按 Adam LR Full Align 规则迁移到目标（width × 8）
- **Model Growth**：先训一个 14 层 half-scale 模型，再 stack 成 28 层。loss 曲线呈现"先升后加速收敛超过随机初始化"——作者猜测是 small model 的快收敛提供了高质量初始化 + growth 隐式正则化
- **Hidden z-loss**：抑制 massive activation；公式 6，对最后一层 hidden state 的 log-sum-exp 加一个小系数 loss
- **Adam epsilon = 1e-16**：传统 1e-5 在大模型 + 小初始化 + 大 batch 下会 dominate gradient 二阶矩，导致性能崩溃

> [!insight] 对研究的启发
> 这套 stability suite 不是"调参玄学"——每一项都有明确的失败模式诊断（router weight similarity、gradient RMS norm、massive activation）。值得作为训练大 MoE 的 baseline checklist。

## 4. Agentic Post-Training（关键卖点）

作者把 agent 任务难度归因到 **三个维度**：
1. **Information processing complexity**（信息整合复杂度）
2. **Tool set complexity**（用工具图建模，节点数 + 边密度量化）
3. **User interaction complexity**（多轮主动提问，少而准）

设计了 6 个 agent 流水线：`UserProfileAgent`、`ToolSetAgent`（40 domains × 1600 apps × 80k tools 构工具图，random walk 采子图）、`InstructionAgent`、`EnvironmentAgent`、`RubricAgent`（滑动窗口评估长 trajectory）、`ValidatorAgent` + `DeduplicatorAgent`。

这块和 Kimi-K2 的工具图思路类似，但 LongCat 强调的是 **三个 complexity 轴可控**。

## 5. 实验结果

### 5.1 Base Model 主要 benchmark

| Benchmark | DeepSeek-V3.1 Base | Llama-4-Maverick | Kimi-K2 Base | **LongCat-Flash Base** |
|-----------|---:|---:|---:|---:|
| Total / Activated | 671B / 37B | 402B / 17B | 1043B / 32B | **560B / 27B** |
| MMLU | 87.46 | 84.41 | 87.47 | 87.05 |
| MMLU-Pro | 59.29 | 63.90 | 68.36 | **70.32** |
| GPQA | 47.16 | 48.08 | 45.89 | **51.09** |
| SuperGPQA | - | 40.58 | 44.70 | **52.03** |
| BBH | 89.46 | 87.56 | 89.19 | **90.54** |
| MATH | 65.38 | 63.34 | 66.74 | **69.28** |
| HumanEval+ | 67.07 | 60.37 | 69.84 | 65.85 |
| MultiPL-E | 62.00 | 58.35 | 59.22 | **69.25** |
| CRUXEval-O | 71.25 | 64.25 | 68.75 | **75.88** |

**判断**：在 27B activated（比 DeepSeek-V3.1 少 10B、比 Kimi-K2 少 5B）的情况下，reasoning / math / code 大部分项 **持平或更好**；MMLU-Pro / SuperGPQA / CRUXEval 这种"难" benchmark 优势明显。

### 5.2 推理性能（H800）

| 配置 | TGS (throughput) | TPS/user |
|------|---:|---:|
| DeepSeek-V3 bf16 (144 GPU) | 1850 | 20-22 |
| **LongCat-Flash bf16 (高吞吐模式)** | 2205 | 68.9 |
| **LongCat-Flash bf16 (低延迟模式)** | 804 | **100.5** |

理论极限 TPOT = 16ms，实测 26ms（61.5%），与 DeepSeek-V3 的 64% 实现度相当。**$0.7 / 1M output tokens** 是作者反复强调的成本卖点。

## 6. 局限与思考

- **Chat 模型的 agentic 数字（ArenaHard-V2 86.5 / TerminalBench 39.5 / τ²-Bench 67.7）**：作者自建了 Meeseeks 和 VitaBench 来防污染，但和 SOTA thinking model 比还有差距（thinking 的工作交给 [[2509_LongCat_Flash_Thinking|LongCat-Flash-Thinking]]）
- **base model 上中文（CEval/CMMLU）略低于 Kimi-K2 / DeepSeek-V3**：可能训练数据中文占比偏少，或 tokenizer 调整影响
- **fine-grained expert + zero-computation expert 的 ablation 没给得很细**：例如 zero expert 比例 Z=256 是怎么定的，没说
- **agentic post-training 的具体 SFT 数据规模未公开**

## 7. 对 LongCat 系列的定位

> [!insight] 系列定位
> 这篇是 LongCat 全系列的 **架构基座**——560B MoE + ScMoE + zero-computation experts 这套设计被后续所有技术报告（Thinking、Omni、Prover、Lite）继承。理解这篇是理解整个 LongCat 系列的前提。

后续路线：
- 推理能力 → [[2509_LongCat_Flash_Thinking|LongCat-Flash-Thinking]]（2509.18883）和 [[2601_LongCat_Flash_Thinking_2601|Thinking-2601]]（2601.16725）
- 小基座 → [[2601_LongCat_Flash_Lite|LongCat-Flash-Lite]]（2601.21204，"Scaling Embeddings > Scaling Experts"）
- 全模态 → [[2511_LongCat_Flash_Omni|Flash-Omni]]（2511.00279）和 [[2603_LongCat_Next|LongCat-Next]]（2603.27538，DiNA 统一离散 token）
- 形式化推理 → [[2603_LongCat_Flash_Prover|Flash-Prover]]（2603.21065）

## 8. 关键链接

- LongCat Chat: https://longcat.ai
- HuggingFace: https://huggingface.co/meituan-longcat
- GitHub: https://github.com/meituan-longcat
