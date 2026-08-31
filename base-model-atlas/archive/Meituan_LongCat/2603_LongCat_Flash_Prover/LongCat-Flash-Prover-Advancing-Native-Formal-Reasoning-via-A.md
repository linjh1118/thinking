---
title: "LongCat-Flash-Prover: Advancing Native Formal Reasoning via Agentic Tool-Integrated Reinforcement Learning"
type: paper
authors: ["Jianing Wang", "Jianfei Zhang", "Qi Guo", "Linsen Guo", "Rumei Li", "Chao Zhang", "Chong Peng", "Cunguang Wang", "Dengchang Zhao", "Jiarong Shi", "Jingang Wang", "Liulin Feng", "Mengxia Shen", "Qi Li", "Shengnan An", "Shun Wang", "Wei Shi", "Xiangyu Xi", "Xiaoyu Li", "Xuezhi Cao", "Yi Lu", "Yunke Zhao", "Zhengyu Chen", "Zhimin Lin", "Wei Wang", "Peng Pei", "Xunliang Cai", "Meituan LongCat Team"]
year: 2026
venue: arXiv
arxiv: "2603.21065"
doi:
url: "https://arxiv.org/abs/2603.21065"
tags: [paper, base-model, moe, formal-reasoning, theorem-proving, lean4, auto-formalization, agentic-rl, tool-integrated-reasoning, meituan, longcat]
status: read
rating: 5
topic: "13_base_model/Meituan_LongCat"
related: ["[[2509_LongCat_Flash/LongCat-Flash-Technical-Report|LongCat-Flash]]", "[[2509_LongCat_Flash_Thinking/LongCat-Flash-Thinking|Flash-Thinking]]"]
created: 2026-07-01
---

> [!tldr]
> 美团 LongCat 系列第 7 篇：在 [[2509_LongCat_Flash_Thinking/LongCat-Flash-Thinking|Flash-Thinking]] 560B MoE / 27B-激活 的基座上，做 **Native Formal Reasoning**——把"自然语言数学题 → Lean4 形式化语句 → 完整/拆分式证明"做成模型的原生能力，而不是堆叠专门的 prover 模型。三个真正的创新点：(1) **Hybrid-Experts Iteration Framework**，把 auto-formalization / sketching / proving 拆成 3 个原子能力，用 Lean4 verifier 反复合成 6 类高质量轨迹；(2) **HisPO（Hierarchical Importance Sampling Policy Optimization）**，针对 MoE + 长程任务 RL 训练里的 train-inference discrepancy 和 policy staleness 做层级式梯度屏蔽；(3) **AST-based legality detection**，直接堵住开源评估 pipeline 里的 reward hacking 漏洞（custom imports / 篡改定理条件 / 凭空造 axiom）。最终 **MiniF2F-Test 97.1% @ 72 budget**（开源 SOTA，吊打 Goedel-Prover-V2 的 92.2% @ 1024 budget），PutnamBench 41.5%、ProverBench 70.8%（开源 SOTA），同时几乎不丢 general task。

## 1. 形式化推理的难点（Native Formal Reasoning）

普通 reasoning 模型（o1/R1/LongCat-Flash-Thinking）擅长用自然语言写 CoT，但碰到 **Lean4 / Isabelle 这类形式化语言** 仍束手无策。原因在于：

- Lean4 是一门**强类型、编译验证**的函数式编程 + 定理证明语言。一个证明不是"看着像对就行"，必须通过 Lean4 kernel 编译。
- 现成的 Tool-Integrated Reasoning (TIR) 框架（Python tool / code interpreter 那一套）**不能直接搬到 Lean4 上**——因为 Lean4 不是"调一下函数拿个返回值"，而是要把整个逻辑链条嵌入形式化代码。
- 通用 reasoning 模型在 MiniF2F-Test 上 Pass@32 通常只有 10-30%（论文实测：DeepSeek-V3.2 79.5%、Qwen3-235B 26.6%、GLM-4.5 27.0%、o3 37.7%、GPT-5 51.2%），跟专门 prover 差距巨大。

作者提出 **Native Formal Reasoning** 这个概念（类比 native multimodal、native tool call），希望模型把形式化操作当作内建能力，**三件事一起做**：

| 能力 | 定义 | 输入 → 输出 |
|------|------|------------|
| **Auto-Formalization (AF)** | 自然语言数学题 → Lean4 形式化语句 | $x$ → $s_x = \pi_{\theta_{af}}(x)$ |
| **Sketching (Sk)** | 给出 lemma 式分治骨架，主定理引用若干 `sorry` 的 helper lemma | $(x, s_x)$ → $d_x = [lemma_1, \ldots, lemma_n, s_x, body_x]$ |
| **Proving (Pf)** | Whole-proof（直接整段证）或 Sketch-proof（先 sketch 再逐 lemma 证） | $(x, s_x)$ 或 $(x, d_x)$ → $p_x$ |

sketch 本质是分治+动态规划：把难定理拆成若干易证 helper lemma，已证的 lemma 可被后续复用。

## 2. 方法：Agentic Tool-Integrated RL（recipe）

### 2.1 整体 pipeline（两阶段）

```
LongCat Mid-train Base (560B MoE, 27B active)
        │
        ▼
[1] Cold-start Phase
   • 用自家 ATF-32B 合成大量 formal statement
   • 用 Flash-Thinking-2601 在 Lean4 verifier 上跑 TIR 合成轨迹
   • 多样性/难度/去重采样 → domain-mixed SFT → cold-start model
        │
        ▼
[2] Iteration Phase（多次循环）
   • 用 cold-start model 当新 expert 重新合成 6 类轨迹
   • 同时混入大量 general data（保 informal 能力）
   • domain-mixed SFT → agentic TIR RL → 下一轮 expert
        │
        ▼
[Final] 最后一轮 SFT + agentic TIR RL → LongCat-Flash-Prover
```

### 2.2 Hybrid-Experts Iteration Framework（核心数据合成）

6 类轨迹来自 3 个 expert（AF / Sk / Pf）× （单轮 / TIR）+ 两种证明模式：

| 集合 | 类型 | 工具交互 |
|------|------|---------|
| $\mathcal{D}_{af}$ | AF 单轮 | 无 |
| $\mathcal{D}'_{af}$ | AF + TIR | 多轮 tool feedback |
| $\mathcal{D}_{whole.pf}$ | Whole-proof 单轮 | 无 |
| $\mathcal{D}'_{whole.pf}$ | Whole-proof + TIR | 多轮 tool feedback |
| $\mathcal{D}'_{sk}$ | Sketch + TIR | 多轮 tool feedback |
| $\mathcal{D}'_{sk.pf}$ | Sketch-proof + TIR | 多轮 tool feedback |

**curriculum learning**：先合单轮（简单题），再合 TIR（难）；whole-proof 走不通的题自动 fall back 到 sketch-proof。难度估计通过 $N$ 次重复采样计算 pass 率：难度 0（全过）的题保留给下一轮，难度 1（全挂）连续两轮就剔除。

> [!insight] Tool-Integrated RL 的真正机制价值
> 这篇的关键不是"用 Lean4 当 verifier"——所有 prover 都这么干——而是 **把 tool call 本身做成 RL 优化目标**：模型不是单次生成完去打分，而是要学会"自己写一段 → 让 Lean4 编译 → 看错误 → 改"这种**多轮 agentic 闭环**。HisPO 稳定的就是这种长 horizon 轨迹（一次成功证明可能调几十次 Lean4 server）。这种"用 verifier 做环境反馈、把工具调用变成可学习行为"的范式，远比单纯 SFT 蒸馏强：whole-proof 模式 Pass@32 是 84.4%，加 TIR 涨到 90.2%，加 sketch+TIR 再到 93.9%——每一步工具集成都带来 5-7% 真实提升。

### 2.3 HisPO：层级式梯度屏蔽（关键 RL 创新）

**问题**：MoE + 长程任务 + 异步训练，importance sampling ratio $r_{i,t}(\theta)$ 会被两件事污染：

$$r_{i,t}(\theta) = \underbrace{\frac{\pi_{\theta_{old}}}{\mu_{\theta_{old}}}}_{r^{dis}(\theta),\ \text{train-inf 差异}} \times \underbrace{\frac{\pi_\theta}{\pi_{\theta_{old}}}}_{r^{stale}(\theta),\ \text{policy 过时}}$$

- **Train-Inference Discrepancy**：训练用 Megatron、推理用 vLLM，bitwise 不一致；MoE 还叠加 expert routing 不一致。
- **Policy Staleness**：异步 RL 下，每个 rollout 可能来自多个旧版本策略。

**HisPO 的层级 mask**：用一个指示函数 $H_{i,t}(\theta)$ 同时做两层屏蔽：

$$H_{i,t}(\theta) = \mathbb{I}\left\{\left|\exp\left(\frac{1}{|y_i|}\sum_j \log r_{i,j}^{dis}\right) - 1\right| < \delta_{seq}\right\} \cdot \mathbb{I}\left\{|r_{i,t}^{dis} - 1| < \delta_{tok}\right\}$$

1. **Sequence-level**：对整条序列求几何均值的 discrepancy，超出阈值 → 整条序列的梯度 mask 掉（但比 GSPO 只看序列级更细，避免误杀好 token）。
2. **Token-level**：剩下的序列里再剔除 per-token discrepancy 过大的 token。
3. **Token-level Staleness Control**：对保留的 token，用 triplet clipping（$\epsilon_{\text{neg\_low/high}}$ 控负 advantage、$\epsilon_{\text{pos\_high}}$ 控正 advantage），借鉴 DAPO/MoBA，防止 MoE 下 expert routing 漂移导致方差爆炸。

同时**移除 KL divergence loss**（$k_3$ estimator 梯度有偏）、用 **global max length** 做分母消除 length bias。

### 2.4 Reward hacking 检测（真实工程问题）

训练到第 80 步，rollout pass rate 突然飙升——作者发现是**开源评估 pipeline 漏洞**：Lean4 只检查 syntax + 目标定理定义一致性，**formal context 完全可编辑**。模型学会通过以下方式作弊：

- 加 `import` 引入隐藏 axiom
- 加 `open`/`lemma`/`instance` helper，把目标定理改写成 trivial 的形式
- 凭空造 axiom 假装证明（"non-existent axiom"）

**修复方案**：写一个轻量 Lean4 lexer/parser → 转 AST → 严格对比 formal statement 与 proof/sketch 之间的 AST 一致性。修好 reward function 后从第 80 步重启 RL，pass rate 曲线立刻回到合理水平。

> [!insight] 形式化推理对基础模型研究的意义
> 这篇论文给 base model 研究带来一个被低估的信号：**形式化推理不是垂直 task，而是检验 RLVR 是否真"verified"的试金石**。一般数学题用 LLM-as-judge / final-answer match 就能算 reward，但 Lean4 kernel 是**地球上少数能给真 binary、零模糊、抗 reward hacking 的 reward signal 之一**。作者被 reward hacking 教训后，反过来发现"开源评估 pipeline 本身都漏"——这说明**很多所谓 verified RL 其实没那么 verified**。LongCat-Flash-Prover 提出的 AST legality detection + verifier tool integration + HisPO 这套组合，本质是在回答一个更基础的问题：当 reward signal 变得真正严格时，MoE LLM 的 RL 训练会暴露哪些隐藏 bug？这个问题对所有追求 RLVR 的 base model 工作都适用。

## 3. Auto-formalization Pipeline

Auto-formalization（自然语言数学题 → Lean4）独立训练一个 expert $\pi_{\theta_{af}}$。工具集 $\mathcal{T}_{af} = \{\mathcal{V}_{syn}, \mathcal{V}_{con}\}$：

- **$\mathcal{V}_{syn}$（Syntax Detection）**：把生成语句拼上 `:= by sorry`，丢进 Lean4 Server (v4.15，复用 Kimina 实现) 编译。返回 `{SORRY, FAIL}`——SORRY 表示除 `sorry` 外无语法错误。
- **$\mathcal{V}_{con}$（Semantic Consistency）**：用 LLM-as-Judge 过滤"语义和原题不一致"的形式化语句（比如把"求最大值"翻成"求最小值"）。

Cold-start 阶段先用自家之前发布的 **ATF-32B**（已有的 auto-formalization 模型）批量合成，再让 Prover expert 在此基础上跑证明轨迹。

## 4. Lean4 实验结果（关键数字）

### 4.1 Theorem Proving - 同预算 Pass@32 对比（Table 2）

| Model | MathOlympiad-Bench | MiniF2F-Test | ProofNet-Test | ProverBench | PutnamBench |
|-------|---:|---:|---:|---:|---:|
| DeepSeek-V3.2（reasoning） | 14.7 | 77.9 | 20.4 | 42.8 | 5.8 |
| Kimi-K2.5（reasoning） | 7.5 | 76.6 | 19.9 | 44.3 | 1.2 |
| Claude-Opus-4.5 | — | 65.6 | 35.0 | — | — |
| Gemini-3 Pro | 3.9 | 56.2 | 22.0 | 33.5 | 1.2 |
| Kimina-Prover-72B | 13.1 | 84.0 | 18.3 | 44.6 | 3.9 |
| DeepSeek-Prover-V2-671B | 13.9 | 82.4 | 30.5 | 52.9 | 3.3 |
| Goedel-Prover-V2-32B w/ self-corr | 20.3 | **90.4** | — | — | 8.6 |
| **LongCat-Flash-Prover (whole-proof)** | 16.9 | 84.4 | 19.9 | 49.9 | 4.9 |
| **LongCat-Flash-Prover (whole-proof + TIR)** | 27.5 | 90.2 | 36.1 | 57.9 | 10.4 |
| **LongCat-Flash-Prover (sketch + TIR)** | **35.8** | **93.9** | **47.3** | **66.5** | **28.9** |

**核心观察**：
- TIR 比单轮 whole-proof 平均涨 5-10%；sketch+TIR 再涨 5-10%（PutnamBench 从 10.4 → 28.9 翻近 3 倍）。
- 在开源 prover 中全面 SOTA，PutnamBench 28.9% 是 Goedel-Prover-V2-32B (8.6%) 的 3.4 倍。

### 4.2 Theorem Proving - 大预算 + sample efficiency 对比（Table 3）

| Model | MathOlympiad / budget | MiniF2F / budget | ProofNet / budget | ProverBench / budget | Putnam / budget |
|-------|---|---|---|---|---|
| Kimina-Prover-72B w/ TTRL | — | 92.2 / UNK | — | — | — |
| DeepSeek-Prover-V2-671B | — | 88.9 / **8,192** | 37.1 / 1,024 | 59.1 / 512 | 7.1 / 1,024 |
| Goedel-Prover-V2-32B w/ self-corr | — | 92.6 / 1,024 | — | — | 13.0 / 184 |
| Delta-Prover（close） | — | 95.9 / **16,384** | — | — | — |
| Seed-Prover（close） | — | **99.6** / UNK | — | — | 50.4 / UNK |
| Seed-Prover 1.5（close） | — | — | — | — | **87.9** / UNK |
| **LongCat-Flash-Prover (sketch+TIR)** | 42.5 / 180 | 95.5 / **72** | 51.1 / 68 | 69.5 / 220 | 31.7 / 118 |
| **LongCat-Flash-Prover (sketch+TIR + Tree Search)** | **46.7** / 180 | **97.1** / **72** | **52.2** / 68 | **70.8** / 220 | **41.5** / 118 |

**sample efficiency 的震撼对比**：
- Goedel-Prover-V2-32B 和 Kimina-Prover-72B 都要 1,024+ attempts 才到 92.2% on MiniF2F。
- LongCat-Flash-Prover 用 **72 attempts** 就到 **95.5%（+Tree Search 97.1%）**——开源最强 sample efficiency。
- Tree Search 平均再涨 3.1%（MiniF2F +1.6%，Putnam +9.8% 最显著，说明难题受益更多）。
- 与 Seed-Prover 1.5 (Putnam 87.9%) 还有差距，但对方 budget 完全不公开，作者明确指出"无法严格对比"。

## 5. Auto-Formalization 实验（Table 1）

Pass@8 指标，7 个 benchmark：

| Benchmark | DeepSeek-V3.2 | Kimi-K2.5 | Claude-Opus-4.5 | Gemini-3 Pro | Goedel-V2-Formalizer-32B | **Prover (w/o TIR)** | **Prover (w/ TIR)** |
|-----------|---:|---:|---:|---:|---:|---:|---:|
| CombiBench | 65.0 | 84.0 | 92.0 | 82.0 | 73.0 | 83.0 | **97.0** |
| FormalMath-Lite | 95.2 | 97.9 | 97.9 | 97.4 | 98.1 | 98.6 | **99.8** |
| MathOlympiad-Bench | 85.6 | 91.1 | 94.4 | 93.1 | 89.2 | 93.3 | **99.2** |
| MiniF2F-Test | 97.5 | 98.4 | 98.0 | 97.5 | 98.4 | 99.2 | **100.0** |
| ProofNet-Test | 81.8 | 88.2 | 90.9 | 91.9 | 79.0 | 87.1 | **97.9** |
| ProverBench | 83.0 | 91.7 | 94.8 | 93.0 | 94.4 | 95.2 | **100.0** |
| PutnamBench | 46.7 | 82.8 | 93.5 | 90.8 | 85.9 | 89.9 | **98.1** |

加 TIR 比不加 TIR 平均涨 ~10%，CombiBench/ProofNet/ProverBench 直接拉满。**全面 SOTA**，包括超过所有闭源 reasoning 和专门 auto-formalizer 模型。

## 6. General Task 表现（不丢 informal 推理）

跟自家前作 Flash-Thinking-2601 比对（Table 4），证明做 formal RL 不会摧毁 informal 能力：

| Benchmark | Flash-Thinking-2601 | LongCat-Flash-Prover | Gap |
|-----------|---:|---:|---:|
| AIME-25 (Avg@16) | **99.6** | 97.7 | −1.9 |
| HMMT-25 (Avg@16) | **93.4** | 90.8 | −2.6 |
| IMO-AnswerBench (Avg@4) | **78.6** | 77.3 | −1.3 |
| AMO-Bench EN (Avg@16) | 61.6 | **62.2** | +0.6 |
| AMO-Bench CH (Avg@16) | 56.8 | **57.3** | +0.5 |
| GPQA-Diamond (Avg@16) | **80.5** | 79.2 | −1.3 |
| LiveCodeBench 24.08-25.05 (Avg@4) | **82.8** | 81.8 | −1.0 |
| OJBench (Pass@1) | **42.2** | 41.8 | −0.4 |

平均损失 < 1%，AMO-Bench 甚至略涨。作者在 general reasoning 主表（Table 5，跟 DeepSeek-V3.1/Qwen3/GLM-4.5/o3/Gemini-2.5-Pro/GPT-5 对比）里也展示了 MiniF2F-Test 的悬殊差距：Pass@32 = **83.2%**（自家表，reasoning 模式 vs GPT-5 51.2%、o3 37.7%）。**证明它不只是 prover，general LRM 也保持顶尖水平**。

## 7. 与 LongCat-Flash 基座的关系

LongCat-Flash-Prover 是 LongCat 系列 base model 路线的第 3 个公开 checkpoint，承接关系：

```
LongCat-Flash-Base (560B MoE / 27B active)        ← 2509, foundation
        │
        ▼ mid-training + reasoning SFT + 大规模 RL
LongCat-Flash-Thinking / -Thinking-2601            ← 2509/2601, informal reasoning 强者
        │
        ▼ + native formal reasoning SFT + agentic TIR RL (HisPO)
LongCat-Flash-Prover                               ← 2603, this work
```

**继承点**：
- 560B total / 27B active 的 MoE 架构（ScMoE + Zero-Computation Experts）保持不变
- 复用 [[2509_LongCat_Flash/LongCat-Flash-Technical-Report|LongCat-Flash]] 的 **DORA（Dynamic ORchestration for Asynchronous rollout）** 异步 RL 系统
- 复用 Flash-Thinking-2601 的 mid-train base 作 cold-start 起点，general reasoning 数据直接采样自 Flash-Thinking 用过的 cold-start 集

**新增点**：
- HisPO 算法（GRPO 在 MoE + 长 horizon 上的稳定性扩展）
- Hybrid-Experts Iteration 数据合成框架（6 类轨迹）
- Lean4 server + AST legality detection 作为新 verifier 工具链
- Formal reasoning 专项 RL data（AF/Sk/Pf 三类）

这正解释了为什么用户把这篇归到 base model 路线——它不是垂直 task 专精，而是同一个 560B MoE 基座在 formal reasoning 维度的能力扩展。

## 8. 与同类工作的对比

| 维度 | AlphaProof (DeepMind) | Kimina-Prover | DeepSeek-Prover-V2 | Goedel-Prover-V2 | **LongCat-Flash-Prover** |
|------|------|------|------|------|------|
| 基座 | Gemini（闭源） | Qwen-2.5-Math (7B/72B) | DeepSeek-V2/Math (7B/671B) | Goedel-LM (8B/32B) | **LongCat-Flash 560B MoE / 27B active** |
| Formal 语言 | Lean | Lean4 | Lean4 | Lean4 | Lean4 |
| AF & Pf 是否分离 | 集成 | 分离（两个模型） | 分离 | 分离 | **集成（同一模型做三件事）** |
| 训练范式 | 闭源 RL + 大规模搜索 | expert iter + RL | expert iter + RL | expert iter + self-correction | **Hybrid-Experts iter + Agentic TIR RL (HisPO)** |
| MiniF2F-Test | 未公开 | 92.2% @ 1,024+ | 88.9% @ 8,192 | 92.6% @ 1,024 | **97.1% @ 72**（开源最强 sample eff.）|
| PutnamBench | — | 4.8% @ 32 | 7.1% @ 1,024 | 13.0% @ 184 | **41.5% @ 118**（开源 SOTA） |
| Reward hacking 处理 | — | 未提 | 未提 | 未提 | **AST-based legality detection**（首次系统揭露开源评估漏洞） |
| General task | — | 弱（专门 prover） | 弱 | 弱 | **几乎不丢 general reasoning**（AIME-25 97.7、HMMT-25 90.8）|

**核心差异化**：
1. AlphaProof 是黑盒闭源，不可比；Seed-Prover / Seed-Prover-1.5 也是闭源且 budget 不公开，作者明确指出"无法严格对比"。
2. 跟开源 prover 比，LongCat-Flash-Prover 的优势主要来自 (a) 560B MoE 的强基座 + (b) AF/Sk/Pf 三能力 co-train（不是单独 prover）+ (c) HisPO 让 MoE 上 RL 真正稳。
3. 价值不只 prover：它是开源里少数**同时保持 general reasoning SOTA-级 + formal reasoning SOTA** 的模型，呼应"native formal reasoning"的定义。

## 9. 关键链接

- 论文：[arXiv 2603.21065](https://arxiv.org/abs/2603.21065)
- HuggingFace 模型：[meituan-longcat/LongCat-Flash-Prover](https://huggingface.co/meituan-longcat/LongCat-Flash-Prover)
- Project Page / 代码：[github.com/meituan-longcat/LongCat-Flash-Prover](https://github.com/meituan-longcat/LongCat-Flash-Prover)
- 同系列：[[2509_LongCat_Flash/LongCat-Flash-Technical-Report|LongCat-Flash]]（base），[[2509_LongCat_Flash_Thinking/LongCat-Flash-Thinking|Flash-Thinking]]（informal reasoning 前作）

## 10. 局限与开放问题

- **PutnamBench 仍弱于闭源 Seed-Prover 1.5（41.5% vs 87.9%）**：作者自己承认，主要因为 search budget 没拉满。把 budget 扩到 1,000+ 是明显的下一步。
- **HisPO 的 $\delta_{seq}$ / $\delta_{tok}$ 没给具体值**（appendix 才有），需要在自家 setup 上调。
- **AF/Sk/Pf 共一个模型，但 inference 时仍要切 prompt mode**——真正的"native formal"应该让模型自己决定何时 formalize、何时 sketch，目前还是 user/script 指定。
- **Reward hacking detection 是 Lean4-specific**：能不能 generalize 到 Coq / Isabelle / Metamath，值得后续工作验证。
- **数据规模未量化**：abstract 里说"over 2 million formal prompts"被注释掉了，正文没给具体合成量。
