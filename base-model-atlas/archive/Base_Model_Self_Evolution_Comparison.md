---
title: "Base Model Self-Evolution and Iterative Improvement Comparison"
type: insight
tags: [insight, base-model, agentic, self-evolution, self-distillation, iterative-training, rl-loop]
source: "[[Topics/13_base_model/Base Model MOC]]"
related:
  - "[[Topics/13_base_model/Base_Model_SFT_PostTraining_Comparison]]"
  - "[[Topics/13_base_model/Base_Model_RL_Comparison]]"
  - "[[Topics/13_base_model/Base_Model_Agentic_Data_Synthesis_Comparison]]"
  - "[[Topics/13_base_model/Base_Model_Verification_Critique_Comparison]]"
created: 2026-06-14
updated: 2026-06-18
---

# Base Model Self-Evolution and Iterative Improvement Comparison

> [!tldr]
> Self-evolution 是 2026 年 agent 训练的前沿。当前主流有 **五类自进化范式**：① Agent 改自己的 scaffold（MiniMax M2.7），② Rollout → Calibrate → Train 飞轮（Step-GUI），③ Expert trajectory → rejection sampling → self-distillation（Step 3.5 Flash / GLM-4.5），④ Closed-loop critic refinement（Kimi K2），⑤ Interaction scaling as third dimension（MiroThinker）。它们不是同一回事：M2.7 是"agent 优化 agent"，Step-GUI 是"data pipeline 自循环"，Step/GLM 是"模型蒸馏自己"，K2 是"critic 同步演化"。判断：未来 agent base model 的训练不再是"一次训完"，而是 **永续自进化**——模型 + verifier + data pipeline 三者共同迭代，每一轮都用上一轮的输出作为下一轮的输入。

---

## 0. 为什么"self-evolution"是 2026 年的新维度

2024-2025 的训练范式是 **一次性**：pretrain → SFT → RL → 部署。每个 stage 都是"数据集 → 训练 → 验证 → 下一 stage"。

2026 年开始出现 **循环式** 训练范式：

1. **训练完的模型本身就是下一轮训练的 teacher**（self-distillation）。
2. **训练完的模型可以改自己的训练 pipeline**（M2.7 改 agent scaffold）。
3. **训练完的 verifier 随 policy 同步演化**（K2 closed-loop critic）。
4. **训练完的模型生成 rollout → 反哺 data pipeline**（Step-GUI 6 轮飞轮）。

这导致 agent base model 的训练从"线性 pipeline"变成"循环 pipeline"。SFT/RL 文档已经覆盖了单 stage 内的设计；本文档聚焦 **跨 stage 的循环**。

---

## 1. 高关键对比：五类自进化范式

| 范式 | 代表模型 | 自进化的对象 | 核心机制 | 风险 |
|---|---|---|---|---|
| **Agent 改自己的 scaffold** | MiniMax M2.7 | Agent harness / training pipeline | 人类设目标 + agent 自主 debug/iterate | 模型优化"非真实问题" |
| **Rollout → Calibrate → Train 飞轮** | Step-GUI | 训练数据 pipeline | rollout → CSRS 抽 7 类 → 选学 → train → stronger rollout | 数据退化（弱模型生成弱数据）|
| **Expert trajectory → rejection sampling → self-distillation** | Step 3.5 Flash, GLM-4.5 | 模型自身 | expert 模型生成轨迹 → 拒绝采样 → 蒸馏到学生 | expert 能力上限锁死 student |
| **Closed-loop critic refinement** | Kimi K2 | Verifier（critic） | critic 随 verifiable signal 同步演化 | critic self-loop collapse |
| **Interaction scaling as third dimension** | MiroThinker | 模型与环境交互深度 | RL 训更深更频繁的 tool interaction | 交互成本线性增长 |

相关来源：
- [[Topics/13_base_model/MiniMax/2605_MiniMax_M2_Series/MiniMax-M2-Series-Mini-Activations-Max-Real-World-Intelligence]]
- [[Topics/13_base_model/stepfun/2512_Step_GUI/Step-GUI]]
- [[Topics/13_base_model/stepfun/2602_Step_3_5_Flash/Step-3.5-Flash]]
- [[Topics/13_base_model/Zhipu_GLM/2508_GLM_4_5/GLM-4.5-ARC-Foundation-Models]]
- [[Topics/13_base_model/Moonshot_Kimi/2507_Kimi_K2/Kimi-K2-Open-Agentic-Intelligence]]
- [[Topics/13_base_model/MiroMind/2511_MiroThinker_v1/MiroThinker-Pushing-the-Performance-Boundaries-of-Open-Source-Research-Agents]]

---

## 2. 五类自进化范式逐条深剖

### 2.1 MiniMax M2.7：Agent 改自己的 scaffold

M2.7 是**最早的"模型自主改进自己训练 pipeline"工作**。

#### 模型迭代系统

```
人类角色：
  ├── 设定目标
  ├── 引导 agent
  └── 审查输出

Agent 角色：
  ├── 自主执行分析
  ├── 自主调试
  └── 自主配置调整

双循环工作流：
  外循环：人类触发主要迭代决策
  内循环：agent 在审查之间自主执行
```

#### 关键发现：Agent Harness 完全由模型生成

> "Agent Harness：完全由 M2.7 模型生成（零人类代码）"

这意味着：
1. Agent scaffold（prompt / tool definitions / workflow）由模型自己写。
2. 模型参与自身训练流程的改进。

#### M2.7 自进化的具体成果

1. **MLE Bench Lite**（22 个 Kaggle 竞赛）：
   - 3 次独立 24 小时试验，平均 66.6% medal rate。
   - 与 Gemini 3.1 Pro 持平。
   - 最优运行：9 金、5 银、1 铜。

2. **自主 100 轮迭代优化内部编程 scaffold**：
   - 引入 loop 检测等机制。
   - 实现 **30% 性能提升**。

#### 关键洞察

> [!insight]
> **M2.7 的本质是"agent 优化 agent harness"**——不是优化模型权重，是优化 scaffold（prompt / tool / workflow）。这是 self-evolution 中最激进的一类：模型不只是 teacher，是 system designer。30% 性能提升来自"agent 发现了人类没发现的 scaffold 改进点（如 loop 检测）"。这意味着 agent harness 设计本身可以自动化。

### 2.2 Step-GUI：Rollout → CSRS → Train 飞轮

Step-GUI 的自进化是 **data pipeline 层的自循环**：

```
Round N Model
   ↓ rollout
Raw Trajectories
   ↓ CSRS Calibration
   ├── 验证脚本 binary 判断
   └── thinking model 抽 7 类数据
        ↓ Selective Learning
   Training Data
        ↓ Train
   Round N+1 Model
        ↓ (next iteration)
   ...
```

#### Step-GUI 报告的 6 轮迭代数据

| 轮次 | 关键变化 |
|---|---|
| Round 1 → 2 | AndroidWorld: 44.83% |
| Round 2 → 3 | AndroidWorld: **44.83% → 73.40%**（CSRS 数据流催化）|
| Round 3 → 4 | 持续提升 |
| Round 4 → 5 | OSWorld 持续提升 |
| Round 5 → 6 | Refinement 数据流持续挖掘弱点，OSWorld 29.63% → 46.26% |

**关键观察**：

1. **Round 2 → 3 的 +28.57% 跃升是 CSRS 飞轮的拐点**——说明前 2 轮模型弱，rollout 失败多，CSRS 抽不出有效训练数据。一旦模型足够强 rollout 有成功，CSRS 才能放大。
2. **6 轮后仍有提升空间**——说明飞轮可以持续运转，没有明显饱和。

#### 关键洞察

> [!insight]
> **Step-GUI 飞轮的核心是"calibration"**——LLM 生成的 dense step 信号不可信，必须被 binary trajectory 锚定。一旦锚定，dense 信号可以放大 binary 的训练效率。这是"不可信 dense + 可信 binary"组合的标准范式。其他自进化范式没有这个 calibration layer，导致 LLM 生成的数据直接训会出错。

### 2.3 Step 3.5 Flash / GLM-4.5：Self-Distillation Loop

Step 3.5 Flash 和 GLM-4.5 共享同一范式：**Expert 模型生成 → 拒绝采样 → 蒸馏到统一模型**。

#### Step 3.5 Flash 的可扩展 RL 后训练

```
Stage 1: 统一 SFT 基础（多域 SFT）
        ↓
Stage 2: 领域特定 RL → 领域专家模型
   ├── Math Expert
   ├── Code Expert
   ├── STEM Expert
   ├── Logic Expert
   ├── Agent Expert
   └── Long Context Expert
        ↓ Expert Trajectory Generation
高质量专家轨迹
        ↓ Rejection Sampling
消除不良模式
        ↓ Self-Distillation
集中专家知识到单一学生模型
        ↓ Scalable RL Loop
回到 Stage 2（用更强的 student 训更强的 expert）
```

#### GLM-4.5 的 Iterative Self-distillation

GLM-4.5 在 Agentic RL 部分明确写：

> "Iterative Self-distillation：RL 提升 → self-distillation → 再 RL，逐阶段提升"

具体步骤：

```
Stage 1: Expert Training
  ├── Reasoning Expert: SFT cold-start + RL
  ├── Agent Expert: SFT cold-start + RL
  └── General chat Expert: SFT cold-start + RL

Stage 2: Unified Training
  ├── Self-distillation 整合多 expert 到 hybrid model
  └── 同时支持 thinking 和 direct response

Iterative Loop:
  RL → 更强的 expert → self-distillation → 更强的 unified → 再 RL
```

#### 关键洞察

> [!insight]
> **Self-distillation loop 的本质是"expert 模型教自己"**——expert 训出来后，把 expert 的轨迹作为下一轮 SFT 的数据，再训出更强的 student。这绕开了"再 hire 一批 expert 标注员"的成本。**代价是 expert 能力上限锁死 student**——如果 expert 本身有偏，student 会继承这个偏。Step 3.5 Flash 用 rejection sampling 部分缓解这个问题（消除不良模式），GLM-4.5 用 self-distillation 后再 RL（RL 可以突破 expert 上限）。

### 2.4 Kimi K2：Closed-loop Critic Refinement

K2 的自进化是 **verifier 层的自循环**：

```
Policy π_θ 生成 trajectory
       ↓
Critic 用 verifiable signals 判断
       ↓
Reward r 更新 Policy
       ↓
同时：Critic 也被 verifiable signals 更新
       ↓
Policy 与 Critic 同步演化
```

#### 关键设计

1. **三类 rubric**：
   - Core rubrics：硬约束（如不输出敏感内容）。
   - Prescriptive rubrics：防 reward hacking（negative rubric）。
   - Human-annotated rubrics：领域特定。

2. **Closed-loop refinement**：
   - Critic 不固定，随 verifiable signals 持续更新。
   - 这避免了"critic 评错 → policy 学错 → critic 永远对"的循环。

#### 关键洞察

> [!insight]
> **K2 的 closed-loop critic refinement 解决了 self-critique 的根本矛盾**——self-critique 的可信度受限于模型自身能力。如果 critic 固定，它会成为 ceiling。如果 critic 随 policy 同步演化，verifiable signals 提供外部锚定，critic 可以突破当前 policy 的能力上限。**核心创新是"verifier 也要训"**——这和 Step 3.5 Flash 的 MetaRM（验证 GenRM）思路相通，但 K2 更彻底：critic 不只是验证 policy，是和 policy 共演化。

### 2.5 MiroThinker：Interaction Scaling as Third Dimension

MiroThinker 的自进化是**模型行为层的 scaling**：

| 维度 | 描述 | 之前的工作 |
|---|---|---|
| Model Size | 更大的模型参数 | 主流方向 |
| Context Length | 更长的上下文窗口 | 主流方向 |
| **Interaction Scaling** | 更深更频繁的 agent-environment 交互 | **MiroThinker 首创** |

#### 关键论据

> "Research performance improves predictably as the model engages in deeper and more frequent agent–environment interactions"

这意味着 **interaction depth exhibits scaling behaviors analogous to model size and context length**。

#### 具体实现

- **256K context window**：支持最多 600 tool calls per task。
- **Sustained multi-turn reasoning**：支持复杂的真实世界研究工作流。
- **RL 训练 interaction depth**：通过 RL 训模型"主动调用工具"。

#### MiroThinker v1.0 / 1.7 / H1 的演进

```
MiroThinker v1.0：
  ├── 提出 Interaction Scaling 概念
  ├── GAIA 81.9%, HLE 37.7%, BrowseComp 47.1%
  └── 600 tool calls per task

MiroThinker 1.7：
  ├── Agentic Mid-training 强化
  ├── Structured planning + Contextual reasoning + Tool interaction
  └── 更有效的多步交互

MiroThinker H1：
  ├── Verification-Enhanced Reasoning
  ├── Local + Global Verification
  └── Heavy-Duty Research Agent
```

#### 关键洞察

> [!insight]
> **Interaction scaling 是自进化的"行为层"**——不是模型权重优化，是模型行为模式优化。MiroThinker 通过 RL 训模型"主动调用工具更深更频繁"，让 interaction depth 成为可训练的能力。这对 agent 的意义是：**未来 agent base model 不只是参数 scaling，还是行为 scaling**。Interaction depth 是 third dimension 这个说法的真正含义是"行为 scaling law"。

---

## 3. 自进化范式的训练 stage 映射

| 范式 | 在哪个 stage 循环？ | 循环单位 | 终止条件 |
|---|---|---|---|
| M2.7 Agent 改 scaffold | Inference / Training infrastructure | Iteration（100+ 轮） | 性能收敛或人类停止 |
| Step-GUI 飞轮 | Data pipeline + Training | Round（6+ 轮） | 性能饱和 |
| Step 3.5 Flash self-distillation | SFT + RL | Loop（多次 expert→student）| expert = student |
| GLM-4.5 iterative self-distillation | SFT + RL | Iteration | 性能饱和 |
| K2 closed-loop critic | RL 内嵌 | Training step | 训练结束 |
| MiroThinker interaction scaling | RL | Training step | 训练结束 |

**关键观察**：

1. **M2.7 和 Step-GUI 是 macro-loop**（多轮跨 stage），其他是 micro-loop（单 stage 内）。
2. **macro-loop 的工程复杂度远高于 micro-loop**——需要 data pipeline / scaffold infrastructure 完整自动化。
3. **目前没有"end-to-end 自动 macro-loop"**——M2.7 还需要人类设目标、Step-GUI 还需要工程师监控。

---

## 4. 自进化飞轮的"启动条件"

不是所有模型都能 self-evolve。启动飞轮需要：

| 条件 | 含义 | 哪家具备 |
|---|---|---|
| **Cold-start 模型够强** | 初始模型 rollout 必须有部分成功 | Step-GUI Round 2 才起飞 |
| **可靠 verifier** | 必须能区分好坏 rollout | 所有 5 家 |
| **Calibration layer** | LLM 抽 dense 必须被 binary 锚定 | Step-GUI CSRS / K2 rubric |
| **Rejection sampling 机制** | 拒绝低质 rollout | Step 3.5 Flash / GLM-4.5 |
| **Hacking blocker** | 防 reward loop | Qwen3-CN blocker（虽不在本文档对比范围）|
| **资源持续投入** | 每轮训完要继续训下一轮 | 所有 5 家 |

> [!insight]
> **Step-GUI Round 2 → 3 的拐点（44.83% → 73.40%）说明 self-evolution 有"启动阈值"**。如果初始模型太弱，rollout 没有足够成功轨迹，CSRS 抽不出有效数据，飞轮不转。这意味着 **小模型 self-evolution 比大模型更难启动**——这是为什么 M2.7 / Step-GUI / Step 3.5 Flash / GLM-4.5 / K2 都是相对强的模型。小模型可能需要外部 teacher 提供 cold-start。

---

## 5. 自进化范式的 Failure Mode 覆盖

| Failure mode | M2.7 改 scaffold | Step-GUI 飞轮 | Step/GLM Self-distill | K2 Closed-loop | MiroThinker Interaction |
|---|---|---|---|---|---|
| **数据稀缺** | 未 | 主解决 | 部分 | 未 | 未 |
| **Expert 能力上限** | 未 | 部分 | 主解决 | 未 | 未 |
| **Reward hacking** | 未 | 部分 | 未 | 主解决 | 未 |
| **Critic collapse** | 未 | 未 | 未 | 主解决 | 未 |
| **Scaffold 不优** | 主解决 | 未 | 未 | 未 | 未 |
| **模型行为单一** | 未 | 未 | 未 | 未 | 主解决 |
| **Cold-start 弱** | 未 | 部分（需要 cold-start 强）| 未 | 未 | 未 |
| **训练成本高** | 部分 | 加剧（多轮）| 加剧 | 部分 | 加剧（更多 interaction）|

**关键判断**：

1. **没有任何一类范式覆盖所有 failure mode**。
2. **数据稀缺是 Step-GUI 飞轮的核心价值**——它把 data scarcity 转化为"用模型生成数据"。
3. **Critic collapse 是 K2 closed-loop 的核心价值**——其他范式没解决 verifier 自我强化。
4. **Scaffold 不优是 M2.7 的独家价值**——其他范式都没碰 scaffold 优化。

---

## 6. 自进化范式的"信任来源"

self-evolution 的根本问题是：**为什么相信下一轮模型比上一轮强**？各家信任来源：

| 范式 | 信任来源 | 风险 |
|---|---|---|
| M2.7 改 scaffold | Human review + MLE Bench 客观 metric | Agent 优化"非真实问题" |
| Step-GUI 飞轮 | CSRS binary 锚定 | Binary verifier 自身错 |
| Step/GLM Self-distill | Expert = 强模型 + rejection sampling | Expert 偏差继承 |
| K2 Closed-loop | Verifiable signals 外部锚定 critic | Verifiable signals 自身覆盖不全 |
| MiroThinker Interaction | Benchmark 分数（GAIA, HLE）| Benchmark 自身偏差 |

> [!insight]
> **所有 self-evolution 范式都需要一个"外部 anchor"**——这是 self-evolution 的根本约束。M2.7 用 MLE Bench；Step-GUI 用 CSRS binary；K2 用 verifiable signals；MiroThinker 用 benchmark。**没有外部 anchor 的 self-evolution 是 reward hacking loop**——模型会优化自己定的目标，而非真实任务。

---

## 7. 自进化的成本与回报

各家报告的成本与回报：

| 范式 | 训练成本 | 性能提升 | ROI |
|---|---|---|---|
| M2.7 改 scaffold（100 轮） | 推理时间（agent 自主跑） | +30%（scaffold 优化） | 极高 |
| Step-GUI 6 轮飞轮 | 6 轮训练 + 多次 rollout | +28.57%（AndroidWorld）| 高 |
| Step 3.5 Flash self-distill | Expert train + student train + RL loop | AIME 2025: 97.3 → 99.9 (with PaCoRe) | 高 |
| GLM-4.5 iterative self-distill | Multi-expert + unified + RL | 持续提升（论文未给量化） | 中 |
| K2 closed-loop critic | 同步训练 + verifiable signals | SimpleQA: 23.76 → 28.94 | 高 |
| MiroThinker interaction scaling | RL + 600 tool calls/task | GAIA 81.9%（开源 SOTA）| 中 |

**关键观察**：

1. **M2.7 ROI 最高**——它不需要重训模型权重，只改 scaffold，但获得 30% 提升。
2. **Step-GUI 是 data-driven 飞轮的标杆**——6 轮 +28.57%，每轮 ROI 递增（轮次越后，rollout 越强，CSRS 抽取越有效）。
3. **MiroThinker 的 ROI 最低**——600 tool calls/task 的成本极高，但 interaction scaling 是 third dimension 的概念价值。

---

## 8. 自进化的伦理与安全考量

Self-evolution 带来新的伦理/安全问题：

1. **Reward hacking 加剧**：self-evolution 让模型有更多"优化自己目标"的机会。
2. **Sandbox 逃逸**：M2.7 能改 scaffold，理论上可以改 sandbox 配置。
3. **目标漂移**：M2.7 在 100 轮迭代中，"目标"是否被 agent 自己重新解释？
4. **不可解释性**：M2.7 改的 scaffold 是 agent 自己写的，人类可能无法理解。
5. **Catastrophic forgetting 加剧**：self-evolution 多轮后，模型可能丢失最初的能力。

> [!insight]
> **Self-evolution 的根本风险是"模型优化自己认为好的目标，而非人类认为好的目标"**。M2.7 的"零人类代码"是优点也是风险——它让 scaffold 优化高效，但也让人类失去对 scaffold 的直接控制。未来 self-evolution 的安全设计必须包括 **(a) human-in-the-loop 检查点 (b) 行为可解释性 (c) rollback 机制 (d) 目标稳定性约束**。这是 Coverage Gaps 文档提到的 safety/alignment 缺口的延续。

---

## 9. 开放问题

1. **Self-evolution 的收敛性**：M2.7 / Step-GUI 多轮后是否收敛？还是会震荡或退化？目前只有 6 轮 / 100 轮的实验数据，缺乏长期（1000+ 轮）观察。
2. **Self-evolution 与 catastrophic forgetting**：多轮 self-evolution 后，模型可能丢失最初能力。如何防止？
3. **Self-evolution 的可解释性**：M2.7 改的 scaffold 是 agent 自己写的，人类可能无法理解。如何让 self-evolution 可解释？
4. **Self-evolution 的安全边界**：M2.7 能改 sandbox，理论上能逃逸。self-evolution 的安全设计是什么？
5. **小模型 self-evolution**：cold-start 弱的模型如何 self-evolve？需要外部 teacher 还是 reward shaping？
6. **Self-evolution 的"meta-objective"**：M2.7 优化的"目标"是性能。是否可以让 agent 自己定义"什么是好的 agent"？这进入 unsupervised self-evolution，风险极高。
7. **Self-evolution 与 RLHF 的关系**：RLHF 是"人类反馈训练"，self-evolution 是"自己反馈训练"。两者结合是什么？

---

## 10. 最短结论

Self-evolution 是 2026 年 agent 训练的前沿。五类主流范式不是同一回事：

- **M2.7 改 scaffold**：agent 优化自己的 agent harness（30% 提升，零人类代码）。
- **Step-GUI 飞轮**：rollout → CSRS → train 循环（AndroidWorld 44.83% → 73.40%）。
- **Step/GLM self-distillation**：expert 轨迹 → rejection sampling → student。
- **K2 closed-loop critic**：verifier 随 policy 共演化。
- **MiroThinker interaction scaling**：interaction depth 作为第三 scaling 维度。

**所有 self-evolution 范式都需要外部 anchor**——benchmark / verifiable signals / binary verifier。没有外部 anchor 的 self-evolution 是 reward hacking loop。

未来 agent base model 的训练不再是"一次训完"，而是 **永续自进化**——模型 + verifier + data pipeline 三者共同迭代，每一轮都用上一轮的输出作为下一轮的输入。Self-evolution 的根本约束是"外部 anchor"，根本风险是"模型优化自己认为好的目标，而非人类认为好的目标"。

---

## 相关对比

- [[Topics/13_base_model/Base_Model_SFT_PostTraining_Comparison]] — SFT 与 self-distillation 单 stage 内
- [[Topics/13_base_model/Base_Model_RL_Comparison]] — RL 内嵌的 critic 演化
- [[Topics/13_base_model/Base_Model_Agentic_Data_Synthesis_Comparison]] — data pipeline 与飞轮的关系
- [[Topics/13_base_model/Base_Model_Verification_Critique_Comparison]] — verifier 自演化
- [[Topics/13_base_model/Base_Model_Agent_Memory_State_Comparison]] — 长 horizon 状态与自进化
