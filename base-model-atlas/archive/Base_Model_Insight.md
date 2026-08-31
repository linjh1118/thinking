---
title: "Base Model Insight — 2025-2026 大模型进化全景"
type: insight
tags: [insight, base-model, llm, moe, rl, architecture, data, training, agentic]
source: "[[Topics/13_base_model/Base Model MOC]]"
created: 2026-06-11
updated: 2026-06-18
---

# Base Model Insight — 2025-2026 大模型进化全景

> [!tldr]
> 2025-2026 年的大模型进化已从「scale up」转向「scale right」：数据工程化（Rephrasing > Repeat）、架构稀疏化（48x sparsity）、训练 agentic 化（GRPO + composite reward + self-critique）。三条主线收敛：**Reasoning 进入基座**、**Agentic RL 统一 post-training**、**全模态原生融合**。国内阿里 Qwen 和 MiniMax 在特定维度已局部领先；核心差距在 post-training recipe 的系统化程度。

---

## 1. 数据进化：从 Repeat 到 Rephrase，从语料到轨迹

### 1.1 Token Efficiency 优先

过去一年的核心转变是**从「更多 token」到「更好的 token」**：

| 策略 | 做法 | 代表 |
|------|------|------|
| **Rephrasing > Multi-epoch** | 10x rephrase + 1 epoch > 1x rephrase + 10 epoch | Kimi K2 (SimpleQA 23.76% → 28.94%) |
| **Style-diverse prompting** | 多种写作风格生成同一知识的多个版本 | Kimi K2 Knowledge Data |
| **Fidelity verification** | 每个 rephrasing 输出需通过质量验证 | Kimi K2 |
| **Chunk-wise autoregressive** | 按语义 chunk 生成，避免长文本质量退化 | Kimi K2 |

**本质洞察**：高质量数据不是「重复出现」，而是「多样表达、同义不变」。这对数据稀缺领域（数学证明、代码、agent 轨迹）尤为重要。

### 1.2 Agentic 数据合成：从工具规格到轨迹

最关键的范式转变是**三层 agentic 数据合成 pipeline**：

```
Layer 1: Tool Spec Generation
  ├── 真实工具：从 GitHub 等获取 3000+ MCP 工具
  └── 合成工具：通过 hierarchical domain evolution 生成 20000+ 合成工具

Layer 2: Agent & Task Generation
  ├── 为每个 tool-set 生成多样化 agent（不同 system prompt + tool 组合）
  └── 配对 explicit rubric（成功标准、评估检查点）

Layer 3: Trajectory Generation
  ├── Multi-turn: LLM 生成 user personas + agent 多轮对话
  ├── Tool simulator: 维护状态并引入受控随机性
  └── Hybrid with Real Execution: 代码/软件工程用真实 sandbox
```

**代表模型**：Kimi K2（23K+ 工具）、Kimi K2.5（3000+ 真实 MCP + 20000+ 合成）、Qwen3-Coder-Next（21 种工具调用模板）。

### 1.3 数据组成的结构化演变

| 阶段 | 数据类型 | 占比 |
|------|---------|------|
| **2024 主流** | 爬取网页语料 + 书籍 + 代码 | 语料为主 |
| **2025 Q1-Q2** | 加入 reasoning 数据 + synthetic math | 语料 + SFT |
| **2025 Q3-Q4** | Agent 轨迹数据 + tool call 数据 | 语料 + SFT + RL |
| **2026** | 真实环境交互数据 + self-critique 数据 | 全链路 RL |

---

## 2. 架构进化：从 Dense 到 Ultra-Sparse MoE

### 2.1 MoE Sparsity Scaling Law

关键发现：**sparsity 是独立于 model size 的 scaling 维度**。

| 模型 | 总参 | 激活 | 总专家 | 激活专家 | 稀疏度 | FLOPs 节省 |
|------|------|------|--------|---------|--------|-----------|
| DeepSeek-V3 | 671B | 37B | 256 | 8 | 32x | baseline |
| Kimi K2 | 1.04T | 32.6B | 384 | 8 | **48x** | **1.69x vs sparsity 8** |
| Qwen3-Coder-Next | 80B | 3B | — | — | — | 3B active = 235B class |
| MiniMax M2 | 229.9B | 9.8B | 256 | — | — | — |
| MiniMax M3 | — | — | — | — | MSA | 1M context 可承受 |

**核心结论**：在固定激活参数下，增加 sparsity（总专家/激活专家）持续降低训练和验证 loss。sparsity 48 比 sparsity 8 减少 1.69× FLOPs，且这个优势随训练 token 数增加而扩大。

### 2.2 MuonClip：大规模 Muon 训练稳定化

Muon 优化器在相同 compute budget 下显著优于 AdamW，但 scaling 时遇到 attention logits 爆炸。Kimi K2 提出 **MuonClip**（QK-Clip）解决：

- 计算每个 head 的 max logit $S_{\max}^h$
- 当 $S_{\max}^h > \tau$ 时，对 $W_q$ 和 $W_k$ 乘以 $\sqrt{\gamma_h}$
- **per-head clipping** 最小化干预：只有少数 head 会爆炸
- 实验中 $\tau = 100$，15.5T tokens 训练全程无 loss spike

**工程价值**：为未来使用更高效优化器（Muon 替代 AdamW）提供了范式，使 1T+ 参数 MoE 的稳定训练成为可能。

### 2.3 Linear Attention：从 Hybrid 到 Production

**Kimi Linear (KDA)** 证明了 hybrid linear attention 在 production 规模下可行：

| 架构 | 128k 预填充加速 | 1M 解码吞吐 |
|------|-------------|------------|
| MLA (Full Attention) | baseline | baseline |
| Kimi Linear (KDA 3:1) | **~1.3x** | **6x** |

KDA 核心创新：**per-channel fine-grained gating**（而非 head-wise），每个 feature dimension 有独立的 forgetting rate，实现更精确的 RNN memory 调控。

### 2.4 Lightning Attention：稀疏长上下文

MiniMax-M1 验证了 **hybrid Lightning Attention** 在推理效率上的优势：

- 每 7 个 Lightning Attention blocks 后接 1 个 softmax attention block
- 100K tokens 生成：仅需 DeepSeek R1 的 **25% FLOPs**
- 原生支持 1M tokens 输入（DeepSeek R1 的 8 倍）

### 2.5 架构选型决策树

```
输入长度 < 32K, 需要 RL scaling
  → Full Attention (MLA/GQA) + AdamW
  OR Kimi Linear KDA (if KV cache 是瓶颈)

输入长度 > 128K, 需要长上下文
  → Hybrid Lightning Attention (MiniMax M1)
  OR Kimi Linear KDA
  OR MiniMax MSA (M3)

激活参数 budget < 10B, 需要 coding agent
  → Ultra-Sparse MoE + MTP (Qwen3-Coder-Next 3B active)
  OR 小模型 + 完整 agent training recipe

训练 > 1T tokens, 需要超大规模
  → MuonClip + Ultra-Sparse MoE (Kimi K2 路线)
```

---

## 3. 训练策略进化：从 SFT 到 Multi-Stage Agentic RL

### 3.1 RL 算法的收敛与分化

**主流 RL 算法对比**：

| 算法 | 提出者 | 核心创新 | 适用场景 |
|------|--------|---------|---------|
| **GRPO** | DeepSeek | group-relative advantage，简化 PPO | 规则验证任务（math/coding） |
| **CISPO** | MiniMax M1 | 裁剪 IS 权重而非 token 更新，保留低概率 tokens 梯度 | 推理链扩展，token 级优化 |
| **GRPO-RoC** | Microsoft rStar2 | Resample-on-Correct，解决 tool noise | Agentic coding |
| **DAPO** | — | 动态 clip range | 竞赛数学 |
| **PPO** | — | 通用，但实现复杂 | 通用场景 |

**关键洞察**：**CISPO vs GRPO 的本质区别**：
- GRPO/PPO 裁剪 token 更新 → 低概率 tokens（如 "Wait", "However"）被永久丢弃
- CISPO 裁剪 IS 权重 → 所有 tokens 保留梯度贡献
- 结果：CISPO 在 50% 训练步数内达到与 DAPO 相同的性能

### 3.2 Multi-Stage Training Pipeline（最完整范式）

Qwen3-Coder-Next 提供了目前最完整的 coding agent 训练范式：

```
Base Model
    ↓
SFT（3 数据源: in-house + verified trajectories + doc-grounded QA）
    ↓
┌─────────────────┬─────────────────┬─────────────────┐
↓                 ↓                 ↓                 ↓
WebDev Expert   UX/CLI Expert   SWE Expert    Single-turn RL Expert
(VLM 截图验证)  (Rule-based     (Kubernetes      (单元测试
                format validation) sandbox)         grounded)
    ↓                 ↓                 ↓
    └─────────────────┴─────────────────┘
                    ↓
          Expert Distillation → Unified Model
```

**关键 trick**：
- **21 种 Tool Chat Template Scaling**：不同 scaffold 的工具调用格式都训练一遍 → format-invariant behavior
- **Reward Hacking Blocker**：检测并阻止 agent 用 `git log` 获取 ground-truth（之前未报道的自发行为！）
- **Pairwise Preference Modeling**：每条请求采样 n 个候选，pairwise judge 对比多维 checklist

### 3.3 Composite Reward：过程监督的量化

长轨迹（192K tokens, 数千步 action）的信用分配问题是 agentic RL 的核心挑战：

$$r_t = \alpha \cdot r_t^{\text{process}} + \beta \cdot r_t^{\text{speed}} + r_t^{\text{perf}}$$

| Reward 分量 | 定义 | 作用 |
|------------|------|------|
| **process** | 语言混合惩罚、工具格式错误惩罚、结构化推理奖励 | 引导中间行为质量 |
| **speed** | turn-level 惩罚（防止过长 rollouts） | 提高 agent 效率 |
| **perf** | 最终结果（代码通过率、任务完成度） | 保证最终效果 |

### 3.4 Self-Critique RL：Verifiable → Open Domain

Kimi K2 的 **Self-Critique Rubric Reward** 将 RL 扩展到开放域：

1. K2 作为 critic，通过 pairwise comparisons 判断自己的输出
2. Core rubrics（Kimi 核心价值观）+ prescriptive rubrics（消除 reward hacking）+ human-annotated rubrics
3. 训练过程中 critic 通过 verifiable signals 持续更新（closed-loop critic refinement）

**本质**：把「可验证任务」的能力迁移到「主观评判任务」，而不需要人工标注。

### 3.5 训练策略进化时间线

| 时间 | 主流范式 | 关键特征 |
|------|---------|---------|
| 2024 | SFT + DPO | 模仿学习为主 |
| 2025 Q1 | SFT + GRPO (math) | RL 进入推理 |
| 2025 Q2 | Multi-stage SFT + GRPO (coding) | RL 进入 coding |
| 2025 Q3 | Expert Distillation + Multi-RL | 多域能力合并 |
| 2025 Q4 | CISPO + Composite Reward | 过程监督 |
| 2026 | Self-Critique + Interleaved Thinking | 开放域 RL + agentic thinking |

---

## 4. 关键 Insight

### Insight 1: Rephrasing > Multi-epoch（数据工程核心原则）

10x rephrase + 1 epoch 在 token efficiency 上全面优于 1x rephrase + 10 epoch。
**原因**：多样化的表达方式让模型学习到知识的多个视角，而非过拟合特定表述方式。
**适用场景**：所有数据稀缺领域，尤其是 reasoning、coding、agent 轨迹数据。
**反例**：简单重复数据会造成隐式「curriculum cheat」，模型在重复数据上过拟合。

### Insight 2: Sparsity 是独立的 Scaling 维度

在固定激活参数下，增加 sparsity（总专家/激活专家）持续降低 loss，且 FLOPs 节省随 sparsity 增加而扩大。
**工程启示**：1T+ 参数的 ultra-sparse MoE（如 Kimi K2）是可行的，关键是 MuonClip 解决稳定性。

### Insight 3: 训练范式 > 模型规模

Qwen3-Coder-Next 用 3B 激活参数匹配/超越更大 dense 模型。
rStar2-Agent 仅用 14B + 510 RL steps 超越 DeepSeek-R1 (671B)。
**本质**：完整的 agent training recipe（multi-stage RL + expert distillation + template scaling）是核心杠杆。

### Insight 4: Agentic 数据的三层架构不可绕过

从 Tool Spec → Agent/Task → Trajectory 的三层合成 pipeline 是 agentic 数据工程的标准范式。
**关键创新**：
- 真实工具 + 合成工具的双轨 diversity
- 真实 execution sandbox 保证 fidelity
- Rubric-based 质量过滤

### Insight 5: Cross-Domain Transfer 在 VLM RL 中强于预期

GLM-4.5V 发现：**在一个领域训练会 boost 其他所有领域性能**，且 joint training 效果最好。

### Insight 6: Verification 嵌入推理过程

MiroThinker-H1 证明 Local Verification（评估中间步骤）+ Global Verification（审计整体轨迹）是长程推理的关键。

### Insight 7: Interleaved Thinking = Agentic Thinking

MiniMax M2 的 Plan-Act-Reflect Loop 证明：**thinking 和 tool execution 的交替 + 完整推理状态保留**是长 horizon agent 的关键。
**与纯 CoT 的区别**：不是生成更长的 thinking chain，而是在 thinking 和 action 之间交替，利用环境反馈更新推理。

### Insight 8: Interaction Scaling 是第三 Scaling 维度

MiroThinker 提出 model size、context length、interaction depth 是并列的三个 scaling 维度。
**证据**：随着 agent-environment 交互深度增加，research performance 呈现可预测的提升（类似 scaling law）。

### Insight 9: Agentic 数据合成是独立工程学科（2026-06-14 新增）

七条主流 pipeline 在补不同 failure mode：K2/K2.5 补 tool 多样性、Qwen3-Coder-Next 补协议多样性 + reward hacking、Step-DeepResearch 补原子能力、Step-GUI 补单步标注偏差、GE-Lab 补仿真可控性、M2 补 outcome reward 稀疏、rStar2 补 rollout 分布。**未来 agent base model 的数据合成必须同时具备 tool spec 真实分布 + state-action-state 真实转移 + 失败轨迹+恢复 + verifier 可锚定，缺一条都会让 RL 学到的是表面格式而非真实 agent 能力**。详见 [[Base_Model_Agentic_Data_Synthesis_Comparison]]。

### Insight 10: Long-Horizon Agent 的核心是"记得对"（2026-06-14 新增）

六类状态管理范式不是同一回事：MiniMax M2 Interleaved Thinking 解决 state drift、Kimi K2.5 Agent Swarm 解决 latency 线性增长、M3 MSA 解决 KV cache 物理上限、Agentic Reasoning Mind-Map 解决长链复杂逻辑、KDA/SWA 物理降本让 long context 可承受。**未来 long-horizon agent 标准架构是"完整轨迹 + 多层稀疏选择 + 主动分片"，三缺一会爆炸**。详见 [[Base_Model_Agent_Memory_State_Comparison]]。

### Insight 11: Verifier 是 agent 区别于 chatbot 的核心组件（2026-06-14 新增）

七类 verifier 不是同类东西：过程 verifier（Local+Global / Self-Critique Rubric / CSRS / Synthesis）判断中间步骤质量、规则 verifier（Checklist Judger / Hacking Blocker）判断合规性、模型 verifier（Message Compaction / GenRM+MetaRM）用 reward model 判断。**完整 verifier 系统需要三层全栈：前置 anti-cheat + 过程 process + 终端 outcome**。当前没有一家同时具备三层。详见 [[Base_Model_Verification_Critique_Comparison]]。

### Insight 12: Self-evolution 需要外部 anchor（2026-06-14 新增）

五类自进化范式不是同一回事：M2.7 改 scaffold、Step-GUI 飞轮、Step/GLM self-distillation、K2 closed-loop critic、MiroThinker interaction scaling。**所有 self-evolution 范式都需要一个外部 anchor——benchmark / verifiable signals / binary verifier。没有外部 anchor 的 self-evolution 是 reward hacking loop**。未来 agent base model 的训练从"一次训完"转为"永续自进化"。详见 [[Base_Model_Self_Evolution_Comparison]]。

---

## 5. 方法谱系表

| 范式 | 代表模型 | 训练信号 | 工具形态 | 核心价值 | 主要风险 |
|------|---------|---------|---------|---------|---------|
| **Dense + SFT** | Qwen3 8B | 模仿学习 | 无 | 强 base 能力 | 无法 scale reasoning |
| **MoE + Thinking** | Qwen3 235B, Kimi K2 | RL from outcomes | 无/简单 | unified thinking/non-thinking | 推理成本高 |
| **MoE + Agentic RL** | Qwen3-Coder-Next, MiniMax M2 | RL from execution | 多工具 | coding agent 能力 | reward hacking |
| **VLM + RLCS** | GLM-4.5V | RL from curriculum | 视觉感知 | multimodal reasoning | VLM RL 不稳定 |
| **Linear + MuonClip** | Kimi Linear | RL from outcomes | 无 | 超长上下文高效 | hybrid 训练复杂 |
| **Hybrid Lightning** | MiniMax M1 | CISPO RL | 无 | 1M context 可承受 | 工程实现难度 |
| **Verification Agent** | MiroThinker-H1 | local+global verify | 多工具 | 长程推理可靠性 | 验证模块开销 |
| **Agent Foundation** | Seed1.8, Seed2.0 | real-world agency | computer/tool use | 真实世界泛化 | 评测困难 |

---

## 6. 论文矩阵

| 模型 | 公司 | 架构 | 训练策略 | 核心贡献 | Agent 能力 |
|------|------|------|---------|---------|-----------|
| **Kimi K2** | Moonshot | 1T MoE / 32B active / 384 experts / 48x sparsity | MuonClip + Self-Critique RL | MuonClip 稳定化 / 23K+ 工具合成 | SWE-bench 65.8%, #1 开源 LMSYS |
| **Kimi Linear** | Moonshot | 48B / 3B active / KDA 3:1 hybrid | MuonClip + Multi-stage SFT + RL | per-channel gating / 6x 1M throughput | RL scaling 优势 |
| **Kimi K2.5** | Moonshot | open multimodal agentic | joint text-vision RL / Agent Swarm | visual agentic / cross-modal transfer | 视觉推理 SOTA |
| **Qwen3 8B** | Alibaba | Dense + MoE / 0.6B–235B | thinking/non-thinking unified SFT | "Think More, Means Less" paradigm | frontier reasoning |
| **Qwen3-Coder-Next** | Alibaba | 80B MoE / 3B active | Expert Distillation + Multi-RL + Tool Template Scaling | 完整 coding agent recipe / 21-format invariance | SWE-bench 60%+ |
| **Qwen3-Omni** | Alibaba | Thinker-Talker MoE | multi-modality SFT | 音频+视频+文本原生融合 | multimodal SOTA |
| **MiniMax M1** | MiniMax | 456B MoE / 45.9B / Lightning Attention | CISPO RL | 1M context / 80K output / CISPO 算法 | 工具使用 SOTA |
| **MiniMax M2 Series** | MiniMax | 229.9B MoE / 9.8B / 256 experts | CISPO + Composite Reward + Forge RL | Interleaved Thinking / self-evolution | coding agent 竞争 |
| **MiniMax M3** | MiniMax | MSA sparse attention | — | 1M context 可承受成本 / native multimodality | frontier coding |
| **GLM-4.5V** | Zhipu | VLM 9B/106B | RLCS + Cross-domain Transfer | VLM RL 稳定化 / 课程采样 | 多模态 benchmark 强 |
| **GLM-OCR** | Zhipu | 0.9B / 0.4B CogViT + 0.5B GLM | MTP 训练 | 5.2x tokens/step / 文档理解 SOTA | #1 OmniDocBench |
| **rStar2-Agent** | Microsoft | 14B | GRPO-RoC (Resample-on-Correct) | 510 steps 超越 671B R1 | math SOTA |
| **MiroThinker v1.0** | MiroMind | 72B | Interaction Scaling RL | Interaction 是第三 scaling 维度 | GAIA 81.9% |
| **MiroThinker H1** | MiroMind | — | Local + Global Verification RL | Verification 嵌入推理 | research agent SOTA |
| **Agentic Reasoning** | — | DeepSeek-R1 based | Web-Search + Coding + Mind-Map Agent | Deep research pipeline | HLE 23.8% |
| **Seed1.8** | ByteDance | — | real-world agency training | Agent Foundation Model 概念 | GAIA 93.2, OSWorld SOTA |
| **Llama 4** | Meta | 17B active / 128 experts / native multimodal | — | MoE + Early Fusion + iRoPE | open-weight multimodal |

---

## 7. 可操作建议

### 对模型训练
1. **数据：优先 Rephrase > Repeat** — 对稀缺领域数据，用 10x style-diverse rephrasing 代替 multi-epoch 简单重复
2. **架构：考虑 Ultra-Sparse MoE + MTP** — sparsity 48x + multi-token prediction 在激活参数受限场景下是最优选择
3. **优化器：Muon + MuonClip** — 在 1T+ 参数规模下，AdamW 已非最优，MuonClip 使 Muon 可用
4. **注意力：KDA 3:1 hybrid** — 当 KV cache 是瓶颈时（>128K），KDA 提供 6x throughput 提升

### 对 Agentic RL
5. **RL 算法：优先 CISPO** — 对推理链扩展，CISPO 比 GRPO 在 50% 步数内达到相同性能
6. **Reward 设计：Composite Reward** — 长轨迹必须用 process + speed + perf 三分量，否则信用分配不足
7. **Self-Critique** — 在 verifiable tasks 上训练 critic，再泛化到开放域主观评判
8. **GRPO-RoC** — tool-use 场景用 Resample-on-Correct 解决环境噪声

---

## 8. 开放问题

1. **Agentic RL 的 scaling law 还未建立** — Interaction depth 的 scaling 在 MiroThinker 中被观察到，但尚未系统化
2. **Muon/MuonClip 的边界** — Kimi K2 证明了 15.5T tokens 可行，更大规模（如 10T+）是否稳定？
3. **VLM RL 的 KL loss 问题** — GLM-4.5V 发现 VLM RL 不需要 KL loss，理论解释还不完整
4. **Self-Critique 的可靠性** — 用模型自己的判断作为 reward 是否会形成 reward hacking 循环？
5. **Agent Foundation Model 的边界** — Seed1.8 的「为 agent 专门优化」与「通用基座」的边界在哪里？
6. **Tool Template Scaling 的极限** — 21 formats 对 Qwen3-Coder-Next 有效，100 种会怎样？

---

## 9. 结论

2025-2026 年的大模型进化已清晰呈现三条收敛主线：

**主线 1：推理能力内化**
从 o1 的「外部思考」到 Qwen3/MiniMax M1 的「基座内化 Thinking」，推理不再是 post-hoc 的 prompting trick，而是模型架构和预训练的内在能力。MTP（Multi-Token Prediction）进一步将推理效率化，GLM-OCR 用 0.9B 实现 5.2x throughput 提升。

**主线 2：Agentic 训练范式收敛**
从 GRPO 到 CISPO 到 GRPO-RoC 到 Self-Critique，agentic RL 的算法创新在加速收敛。Composite Reward + Verification 嵌入解决了长轨迹信用分配问题。Expert Distillation + Multi-Stage RL 提供了完整的多域能力合并方案。

**主线 3：效率驱动的架构革新**
MuonClip + Ultra-Sparse MoE 使 1T+ 参数稳定训练；KDA hybrid 使 1M context 解码 6x 提速；Lightning Attention 将长推理链成本降到可承受范围。效率不是妥协，而是目标。

---

## 相关可视化

> 📊 相关可视化: [[Topics/13_base_model/Zhipu_GLM/2603_GLM_OCR/GLM_OCR_poster]] | [[Topics/13_base_model/Moonshot_Kimi/2507_Kimi_K2/Kimi_K2_poster]] | [[Topics/13_base_model/Alibaba_Qwen/Variants/2603_Qwen3_Coder_Next/Qwen3_Coder_Next_poster]] | [[Topics/13_base_model/MiniMax/2506_MiniMax_M1/MiniMax_M1_poster]] | [[Topics/13_base_model/Moonshot_Kimi/2510_Kimi_Linear/Kimi_Linear_poster]]

## ⭐ 相关对比文档（Agentic 专题）

- [[Topics/13_base_model/Base_Model_Agentic_Data_Synthesis_Comparison|Base Model Agentic Data Synthesis Pipeline Comparison]] — 七条主流 pipeline 对比
- [[Topics/13_base_model/Base_Model_Agent_Memory_State_Comparison|Base Model Agent Memory and Long-Horizon State Comparison]] — 六类状态管理范式对比
- [[Topics/13_base_model/Base_Model_Verification_Critique_Comparison|Base Model Verification and Self-Critique Architecture Comparison]] — 七类 verifier 设计对比
- [[Topics/13_base_model/Base_Model_Self_Evolution_Comparison|Base Model Self-Evolution and Iterative Improvement Comparison]] — 五类自进化范式对比
