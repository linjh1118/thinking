---
title: "Base Model Agent Memory and Long-Horizon State Comparison"
type: insight
tags: [insight, base-model, agentic, long-horizon, memory, context-management, agent-state]
source: "[[Topics/13_base_model/Base Model MOC]]"
related:
  - "[[Topics/13_base_model/Base_Model_Inference_Productization_Comparison]]"
  - "[[Topics/13_base_model/Base_Model_Architecture_Comparison]]"
  - "[[Topics/13_base_model/Base_Model_Agentic_Data_Synthesis_Comparison]]"
created: 2026-06-14
updated: 2026-06-18
---

# Base Model Agent Memory and Long-Horizon State Comparison

> [!tldr]
> Long-horizon agent 的核心瓶颈不是"看得多"，而是"记得对"。当前主流有 **六类状态管理范式**：① 完整保留+interleaved thinking（MiniMax M2），② 主动上下文分片（Kimi K2.5 Agent Swarm），③ reactive 简单截断（Discard-all baseline），④ 块稀疏选择（MiniMax M3 MSA），⑤ 结构化外部记忆（Agentic Reasoning Mind-Map），⑥ Hybrid/Linear attention 物理降本（Kimi Linear / MiMo SWA）。它们解决的不是同一问题：MiniMax M2 解决"推理状态漂移"，Kimi K2.5 解决"latency 线性增长"，M3 解决"KV cache 物理上限"。判断：未来 long-horizon agent 的标准架构是"完整轨迹 + 多层稀疏选择 + 主动分片"，三缺一会爆炸。

---

## 0. 为什么"long-horizon state"是 agentic 独立维度

LLM 的"context window"对 chatbot 是"输入多长"，对 agent 是"记忆多久"。Long-horizon agent 的瓶颈不是"能不能读 1M token"，而是：

1. **State drift（状态漂移）**：长轨迹中，模型每一步都在重新建立 context（constraints、partial conclusions、plan），如果中途把这些剥离掉，模型会重新推导——这导致累积漂移和 self-correction 失效。
2. **Latency 线性增长**：sequential agent 执行下，task complexity 与 latency 线性相关，限制了可处理任务复杂度上限。
3. **Cost 线性增长**：长 KV cache、长 decoding、tool latency、retry 把所有隐藏成本放大。
4. **Memory policy 复杂**：什么时候保留、什么时候截断、什么时候摘要——这是 chatbot 不存在的问题。

Inference 文档已经覆盖了 ③（cost）。本文档深入 ①、②、④，这是 chatbot 没有但 agent 必须解决的。

---

## 1. 高关键对比：六类状态管理范式

| 范式 | 代表模型 | 核心机制 | 解决什么 | 代价 |
|---|---|---|---|---|
| **完整保留 + interleaved thinking** | MiniMax M2 | 保留 r_t（reasoning）+ a_t（action）+ o_t（observation）完整历史，每轮以完整历史为条件 | state drift、self-correction | KV cache 物理上限、长 decoding 成本 |
| **主动上下文分片（Proactive Sharding）** | Kimi K2.5 Agent Swarm | 多 agent 架构，每个子 agent 有 bounded local context，只有任务相关输出 route 回 orchestrator | latency 线性增长、context overflow | orchestrator 学习复杂、sub-agent finish rate |
| **Reactive 简单截断** | Discard-all baseline | context overflow 后压缩或丢弃 thinking blocks | 应急补救 | 累积 state drift |
| **块稀疏选择** | MiniMax M3 MSA | 先筛相关 KV blocks，再精确 attention | KV cache 物理上限、1M context 可承受 | block selection recall |
| **结构化外部记忆** | Agentic Reasoning Mind-Map | 知识图谱实体抽取 + 社区聚类 + 摘要检索 | long reasoning chain 复杂逻辑 | graph 维护成本 |
| **物理降本（架构层）** | Kimi Linear / MiMo Hybrid SWA | per-channel gating / sliding window attention | KV cache 物理降本 | retrieval recall 风险 |

相关来源：
- [[Topics/13_base_model/MiniMax/2605_MiniMax_M2_Series/MiniMax-M2-Series-Mini-Activations-Max-Real-World-Intelligence]]
- [[Topics/13_base_model/Moonshot_Kimi/2602_Kimi_K2_5/Kimi-K2-5-Joint-Optimization-Vision-Language]]
- [[Topics/13_base_model/MiniMax/2606_MiniMax_M3/MiniMax-M3-Frontier-Coding-1M-Context-Native-Multimodality]]
- [[Topics/13_base_model/Moonshot_Kimi/2510_Kimi_Linear/Kimi-Linear-Expressive-Efficient-Attention]]
- [[Topics/13_base_model/Xiaomi_MiMo/MiMo-Summary-Dense]]
- [[Topics/13_base_model/Academic/2502_Agentic_Reasoning/Agentic-Reasoning-A-Streamlined-Framework-for-Enhancing-LLM]]

---

## 2. 范式逐条深剖

### 2.1 MiniMax M2：完整保留 + Interleaved Thinking

M2 把 agent 轨迹形式化为：

$$\tau = (r_1, a_1, o_1, r_2, a_2, o_2, \ldots, r_T, a_T, o_T)$$

- $r_t$ = reasoning tokens
- $a_t$ = action tokens
- $o_t$ = observation

每个 reasoning 片段 $r_t$ 以**完整历史**为条件：

$$r_t \sim p(\cdot \mid r_1, a_1, o_1, \ldots, r_{t-1}, a_{t-1}, o_{t-1})$$

**最关键的设计 — Reasoning State Persistence**：

$$\mathcal{H}_{t+1} = \mathcal{H}_t \oplus [\mathrm{assistant}(r_t, a_t)] \oplus [\mathrm{tool}(o_t)]$$

即每一步都把 reasoning + action + observation 全部追加到历史。

#### 论文明确批判的两种替代方案

| 替代方案 | 描述 | 论文原话 |
|---|---|---|
| **Front-loaded reasoning** | 所有 reasoning tokens 在 action 之前输出完 | "preventing adaptation to intermediate observations" |
| **Stateless per-turn reasoning** | 每轮生成 $r_t$ 前把 $r_{<t}$ 全部从 context 剥离 | "preventing the model from building on earlier analysis" |

#### 论文的消融实验

通过"在每个 turn 调用模型之前 strip 掉之前的 thinking blocks"做对照：

| 设置 | 结果 |
|---|---|
| Drop reasoning blocks（$\mathcal{H}_{t+1}^{(\text{drop})}$）| 所有 agentic benchmark 一致下降；deep search / SWE 任务下降最严重 |
| Keep reasoning blocks（$\mathcal{H}_{t+1}$）| 一致提升；M2.7 在 BrowseComp +33.8、RISE +14.1 |

**关键洞察**：

1. **state drift 是真实存在且可量化的**：M2 把它从模糊概念变成了可消融的实验变量。
2. **drift 与 sustained planning 需求正相关**：短 horizon 任务差异不大，长 horizon 任务差异巨大。这意味着 deep research / SWE 这种 task 是 state drift 的高风险区。
3. **Plan-Act-Reflect 三段循环**：M2 把 agent 行为抽象成 Plan（基于历史推理和观察结果制定/修订策略）→ Act（选择并执行工具调用）→ Reflect（评估观察结果是否符合预期、更新世界模型）。这三段共享完整 context。

### 2.2 Kimi K2.5 Agent Swarm：Proactive Context Sharding

K2.5 解决的是 sequential agent 的 **latency 线性增长**：

> "现有 agentic 模型依赖 sequential execution，每个 reasoning step 和 tool call 按序执行，随着任务复杂度增加，latency 线性增长，限制了可处理的任务复杂度上限。"

#### PARL（Parallel Agent RL）架构

```
Trainable Orchestrator（主 agent）
  ├── 动态任务分解
  ├── 子 agent 实例化
  └── 并行调度
        ↓
Frozen Subagents（子 agent）
  ├── 从固定中间 checkpoint 实例化
  └── 执行轨迹不参与优化（避免 credit assignment ambiguity + training instability）
```

#### PARL Reward 设计

$$r_{\text{PARL}}(x, y) = \lambda_1 \cdot r_{\text{parallel}} + \lambda_2 \cdot r_{\text{finish}} + r_{\text{perf}}(x, y)$$

| Reward 分量 | 作用 |
|---|---|
| $r_{\text{parallel}}$（instantiation reward） | 防 serial collapse——鼓励探索并发调度空间 |
| $r_{\text{finish}}$（sub-agent finish rate） | 防 spurious parallelism——防通过大量创建无意义 sub-agent 刷指标 |
| $r_{\text{perf}}$（task-level outcome） | 最终任务质量 |

训练过程中 $\lambda_1$ 和 $\lambda_2$ anneal 至 0，最终策略优化主目标。

#### Critical Steps as Resource Constraint

K2.5 把 parallel agent 执行的时间成本类比为计算图的 critical path：

$$\text{CriticalSteps} = \sum_{t=1}^{T} \left( S_{\mathrm{main}}^{(t)} + \max_i S_{\mathrm{sub},i}^{(t)} \right)$$

通过约束 critical steps（而非总 steps）显式激励**有效并行化**——这比单纯"激励并行数"更精准（避免模型作弊创建无意义并行）。

#### Proactive Context Sharding vs Reactive Truncation

K2.5 论文把 context 管理范式分为：

| 范式 | 描述 | 代表 | 风险 |
|---|---|---|---|
| Reactive Hide-Tool-Result | overflow 后隐藏工具结果 | 通用做法 | 信息丢失 |
| Reactive Summary | overflow 后 LLM 摘要 | 通用做法 | 摘要丢细节 |
| Reactive Discard-all | overflow 后丢弃历史 | Kimi K2.5 baseline | state drift |
| **Proactive Sharding**（Agent Swarm） | 长任务分解为并行、语义隔离的子任务，每个 sub-agent 有独立 bounded context；只有任务相关输出 route 回 orchestrator | Kimi K2.5 | orchestrator 学习复杂 |

**核心区别**：reactive 是"满了再压缩"，proactive 是"先分解，每个子任务 scope 内 bounded"。

#### 实验结果

| Benchmark | K2.5 Single | K2.5 Agent Swarm | Claude Opus 4.5 | GPT-5.2 Pro |
|---|---|---|---|---|
| BrowseComp | 60.6% | **78.4%** | 37.0% | 77.9% |
| WideSearch Item-F1 | 72.7% | **79.0%** | 76.2% | - |
| In-house Swarm Bench | 41.6% | **58.3%** | 45.8% | - |

WideSearch 上实现 **3×~4.5× 执行时间减少**（随目标 Item-F1 从 30% 增至 70%）。

### 2.3 Discard-all baseline：Reactive 简单截断

Kimi K2.5 论文报告了 BrowseComp 上 74.9% 的成绩是用 Discard-all 配置（reactive 截断）实现的。Agent Swarm 在同一 benchmark 上 78.4%。

**为什么 Discard-all 仍是有效的 baseline**：

1. 实现简单，不需训练 orchestrator。
2. 在 search 类任务上，早期 search 失败的信息"丢掉"反而帮助（因为 search 是 noisy 的，overflow 后丢旧 search 让模型重新搜）。
3. 在 BrowseComp 这种"目标信息存在于单一网页"的任务上，state drift 影响小。

**何时 Discard-all 不够**：

- 任务需要跨多源信息整合（GAIA, deep research）。
- 任务需要长程 plan-revise（SWE, software engineering）。
- 任务需要 self-correction（M2 论文消融实验显示 deep search 下降最严重）。

### 2.4 MiniMax M3 MSA：块稀疏选择

M3 用 MSA（MiniMax Sparse Attention）解决 1M context 的物理上限。

**核心思想**：先筛相关 KV blocks，再精确 attention。

| 操作 | 描述 |
|---|---|
| Block selection | 学习一个 query-key 相关性打分，选 top-K blocks |
| Precise attention | 仅在 selected blocks 上做精确 attention |

**为什么这适合 agent**：coding/search/research agent 轨迹里 80% 是低价值重复状态（同样的 console 输出、同样的网页片段、同样的中间日志），20% 是关键失败状态。MSA 的"先筛后精"正好匹配这个分布。

**风险**：block selection 一旦筛掉关键失败步骤，后续无法恢复。M3 论文提到这是 open problem。

### 2.5 Agentic Reasoning Mind-Map：结构化外部记忆

Agentic Reasoning 用外部 graph 作为长链记忆：

```
推理过程中
  ↓
LLM 从推理链提取实体
  ↓
识别实体间语义关系（类似 GraphRAG）
  ↓
Louvain 社区聚类
  ↓
每个聚类生成摘要
  ↓
两大功能：
  ├── Context Provision：为外部工具提供结构化推理上下文
  └── Memory Retrieval：长链中不确定时查询 Mind-Map
```

**关键消融发现**：Mind-Map 特别有效于：

- Long reasoning chains with many tool calls。
- Logic-heavy questions（如 modified riddle: "The surgeon is the boy's father"）。
- Strategic reasoning（Werewolf game: 72% win rate with Mind-Map vs 36% without）。

**关键判断**：Mind-Map 是把"agent 内部记忆"外化为"可查询 graph"。代价是 graph 维护成本（每次 reasoning step 都要更新 graph），但收益是"长链中不确定时主动检索"。

### 2.6 物理降本：Kimi Linear + MiMo Hybrid SWA

这两条不是"管理策略"，是"架构降本"，让 long context 物理可行。

#### Kimi Linear（KDA）

- KDA 3:1 hybrid：每 3 个 linear attention block + 1 个 softmax attention block。
- per-channel fine-grained gating：每个 feature dimension 有独立 forgetting rate。
- 1M context decode throughput **6× over MLA**。
- 风险：有限状态容量，需要 hybrid global attention 弥补 long-context retrieval。

#### MiMo Hybrid SWA

- 128-token sliding window + periodic global attention。
- V2-Flash 48 层：39 SWA + 9 GA（5:1）。
- V2.5-Pro 1M context：Hybrid ratio 7:1（更多 SWA 节省 KV cache）。
- 128K context 下 KV-cache 和 attention compute 接近 **6-7x reduction**。
- 关键直觉：SWA 负责局部连续性，GA 负责长程桥接。

> [!insight]
> **物理降本和状态管理是两个维度**。Kimi Linear 让 1M context "可承受"，但不解决"在 1M context 里如何选择/压缩/检索"的问题。MSA 解决后者但不降本。理想架构是 **KDA + MSA + 主动分片**，三者不冲突，是不同维度。

---

## 3. Long-Horizon State 管理的 Failure Mode 覆盖

| Failure mode | M2 Interleaved | K2.5 Swarm | Discard-all | M3 MSA | Mind-Map | KDA/SWA 物理降本 |
|---|---|---|---|---|---|---|
| **State drift** | 主解决 | 部分缓解 | 加剧 | 部分 | 部分 | 无关 |
| **Latency 线性增长** | 加剧（保留全部）| 主解决 | 加剧 | 部分 | 加剧（graph 维护）| 部分（MTP 加速）|
| **KV cache 物理上限** | 加剧 | 部分缓解 | 主解决 | 主解决 | 部分缓解 | 主解决 |
| **跨源信息整合** | 主解决 | 主解决 | 部分缓解 | 部分 | 主解决 | 无关 |
| **Self-correction** | 主解决 | 部分 | 加剧 | 部分 | 部分 | 无关 |
| **Critical state 可追溯** | 主解决 | 部分 | 主失败点 | 主失败点 | 主解决 | 无关 |
| **Decoding 吞吐** | 加剧 | 主解决 | 加剧 | 加剧 | 加剧 | 主解决 |
| **训练稳定性** | 主解决 | 主失败点 | 主解决 | 部分 | 部分 | 部分 |

**关键判断**：

1. **没有任何一条范式覆盖全部 failure mode**。组合使用是必然。
2. **M2 Interleaved + K2.5 Swarm 是互补的**：前者解决 state drift，后者解决 latency。组合使用是 long-horizon agent 的未来。
3. **Discard-all 是 baseline，不是终态**：M2 消融实验明确显示它在 deep search / SWE 上失败。但作为应急 fallback 仍有效。
4. **物理降本（KDA/SWA/MSA）是基础设施**：它不替代任何管理策略，只让策略可行。

---

## 4. State 管理范式的训练 stage 映射

| 范式 | 进 pretrain？ | 进 SFT？ | 进 RL？ | 进 inference policy？ |
|---|---|---|---|---|
| M2 Interleaved Thinking | — | ✓ trajectory SFT | ✓ composite reward | ✓ 默认开启 |
| K2.5 Agent Swarm / PARL | — | — | ✓ PARL reward | ✓ orchestrator 决定 |
| Discard-all | — | — | — | ✓ 系统层 fallback |
| M3 MSA | ✓ 架构层 | — | — | ✓ attention 默认 |
| Mind-Map | — | — | — | ✓ 工具调用层 |
| KDA/SWA | ✓ 架构层 | — | — | ✓ attention 默认 |

**关键观察**：

1. **架构层范式（MSA/KDA/SWA）进 pretrain**：因为它们是 attention pattern，进不了 RL。
2. **行为层范式（Interleaved/Swarm/Discard-all）进 SFT+RL+inference**：它们是行为，需要训练和部署一致。
3. **Mind-Map 是 inference-time 工具**：不在训练 stage，是 agent scaffold 的一部分。

---

## 5. Reward 设计中的 State 约束

state 管理不只是 inference 决策，也嵌入到 RL reward。各家做法：

### 5.1 M2 Composite Reward

$$r_t = \alpha \cdot r_t^{\text{process}} + \beta \cdot r_t^{\text{speed}} + r_t^{\text{perf}}$$

- **process**：语言混合惩罚、工具格式错误惩罚、结构化推理奖励。
- **speed**：turn-level 惩罚（防过长 rollouts）。
- **perf**：最终结果。

speed reward 直接影响 state 长度——不奖励"绕远路"。

### 5.2 K2.5 PARL Critical Steps Constraint

$$\text{CriticalSteps} = \sum_{t=1}^{T} \left( S_{\mathrm{main}}^{(t)} + \max_i S_{\mathrm{sub},i}^{(t)} \right)$$

这是把"agent wall-clock"建模成计算图 critical path 的 reward。

### 5.3 Kimi K2 Budget Control + PTX Loss

- **Budget Control**：per-sample maximum token budget + 截断惩罚。
- **PTX Loss**：防止在 RL 训练中遗忘高能力数据——本质是"state 偏离 cold-start 太远就惩罚"。

### 5.4 Qwen3-Coder-Next Pairwise Preference

每条请求采样 n 个候选，pairwise judge 对比多维 checklist。checklist 内含 "context 是否保留" 维度。

> [!insight]
> **state 管理不只是 inference policy，也是 RL reward 的一部分**。如果不在 reward 里设 speed/critical-steps/budget，模型 RL 训出来就会无限延长 trajectory。这是为什么单纯"训更大模型"无法解决 long-horizon agent——必须把 state 约束写进 reward。

---

## 6. 长 horizon 评估指标

报告 long-horizon agent 时，pass@1 远远不够。应报告：

| 指标 | 解释 | 解决什么 failure mode |
|---|---|---|
| pass@1 / pass@k | 成功率基础指标 | task capability |
| tokens per successful trajectory | 是否靠长推理堆成功 | state efficiency |
| wall-clock time | 用户实际等待 | latency |
| tool calls / environment steps | 是否靠暴力交互 | interaction efficiency |
| cost per solved task | 产品化核心 | total cost |
| verifier type | rule / execution / rubric / human | reward 锚定度 |
| context retained ratio | 完整历史 vs summary | state management policy |
| compaction error rate | 压缩是否丢关键约束 | reactive truncation 风险 |
| failure recovery rate | 第一次失败后能否修复 | self-correction |
| critical state recall | 关键失败状态能否追溯 | MSA recall 风险 |

> [!insight]
> 当前所有论文都只报 pass@1 / pass@k。**这导致不同 state 管理范式不可比较**。K2.5 报告了 4.5× latency reduction（WideSearch）是少数例外。未来 long-horizon agent 的标准评测必须包含 context retained ratio / failure recovery rate / critical state recall，否则 MSA vs Interleaved vs Swarm 的对比无从谈起。

---

## 7. 开放问题

1. **State drift 的根本性解**：M2 把它从模糊变可测量，但根本性解仍开放。是否需要专门的"state consistency reward"？
2. **Critical state 的定义**：什么算"critical"？是失败状态、是 plan revision 点、还是 verifier 触发？不同定义导致不同 block selection policy。
3. **Reactive vs Proactive 的边界**：什么时候 proactive 不必要（成本高），什么时候 reactive 不够（state drift）。M2 消融显示 deep search 需要 proactive，但短 task 不需要——这个分界点在哪里？
4. **Sub-agent 的 state 隔离 vs 共享**：K2.5 Agent Swarm 让每个 sub-agent 有 bounded local context，但什么时候 sub-agent 需要 share state？比如多 tab 操作同一账号时。
5. **Long-horizon 的 cost 上限**：1M context / 192K agent trajectory 的实际成本是多少？目前只有 MiniMax / Kimi Linear 给出部分数据，缺少统一 cost 模型。

---

## 8. 最短结论

Long-horizon agent 的核心瓶颈不是"看得多"，而是"记得对"。当前主流有六类状态管理范式：

- **M2 Interleaved Thinking**：完整保留 reasoning state，解决 state drift、self-correction。代价是 KV cache 物理上限。
- **K2.5 Agent Swarm / PARL**：主动分片，解决 latency 线性增长、context overflow。代价是 orchestrator 学习复杂。
- **Discard-all baseline**：reactive 截断，简单但加剧 state drift。
- **M3 MSA**：块稀疏选择，解决 KV cache 物理上限。代价是 critical state recall 风险。
- **Agentic Reasoning Mind-Map**：结构化外部记忆，解决 long chain 复杂逻辑。
- **KDA/SWA 物理降本**：架构层让 long context 可承受，但不解决策略问题。

未来 long-horizon agent 的标准架构是 **"完整轨迹 + 多层稀疏选择 + 主动分片"**，三缺一会爆炸：缺完整轨迹→state drift；缺稀疏选择→KV cache 爆；缺主动分片→latency 线性涨。

---

## 相关对比

- [[Topics/13_base_model/Base_Model_Inference_Productization_Comparison]] — cost per solved task 总览
- [[Topics/13_base_model/Base_Model_Architecture_Comparison]] — MSA/KDA/SWA 架构层细节
- [[Topics/13_base_model/Base_Model_Agentic_Data_Synthesis_Comparison]] — 训练数据如何包含 state transition
- [[Topics/13_base_model/Base_Model_Verification_Critique_Comparison]] — verifier 触发升档思考
- [[Topics/13_base_model/Base_Model_Self_Evolution_Comparison]] — 自进化如何持续改进 long-horizon 能力
