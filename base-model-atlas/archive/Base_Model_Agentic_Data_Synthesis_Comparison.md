---
title: "Base Model Agentic Data Synthesis Pipeline Comparison"
type: insight
tags: [insight, base-model, agentic, data-synthesis, trajectory, tool-use]
source: "[[Topics/13_base_model/Base Model MOC]]"
related:
  - "[[Topics/13_base_model/Base_Model_Pretraining_Comparison]]"
  - "[[Topics/13_base_model/Base_Model_SFT_PostTraining_Comparison]]"
  - "[[Topics/13_base_model/Base_Model_RL_Comparison]]"
  - "[[Topics/13_base_model/Base_Model_Verification_Critique_Comparison]]"
created: 2026-06-14
updated: 2026-06-18
---

# Base Model Agentic Data Synthesis Pipeline Comparison

> [!tldr]
> Agentic 数据不是「更大的 SFT 数据集」，而是「状态-动作-观察-验证」的因果结构合成。当前主流有 **七条 pipeline**：Kimi K2 三层工具合成、Kimi K2.5 MCP+合成双轨、Qwen3-Coder-Next 三源 SFT+tool template scaling、Step-DeepResearch 原子能力 reverse engineering、Step-GUI CSRS 轨迹级校准、GE-Lab 树状仿真、MiniMax M2 artifact-aligned reward。它们解决的不是同一问题：有人在补「工具多样性」，有人在补「状态转移」，有人在补「错误恢复」。判断：未来 agent base model 的数据合成必须同时具备 ① tool spec 真实分布、② state-action-state 真实转移、③ 失败轨迹+恢复、④ verifier 可锚定，缺一条都会让 RL 学到的是表面格式而非真实 agent 能力。

---

## 0. 为什么"agentic 数据合成"是一个独立的对比维度

很多人把"agentic 数据"等同于"tool-use SFT 样本"。这是 Pretrain/SFT 文档已经覆盖的内容。但真正的 agentic data synthesis 是 **2025-2026 年才出现的新工程学科**，它要解决的是三类 pretrain/SFT 无法覆盖的问题：

1. **状态分布问题**：人类标注数据的状态分布和真实 agent rollout 的状态分布不重叠——agent 经常遇到"工具返回了非预期结果"、"网页结构变化"、"测试失败后状态被污染"等长尾情况，这些状态在静态 SFT 数据里几乎不存在。
2. **可锚定 reward 问题**：agent 的 reward 不能只看最终答案对错。需要每条轨迹都能被一个外部 verifier 校准（脚本通过、assertion 通过、引用可核验、状态匹配），否则 RL 训出来的就是"看似 agent 实则 chatbot"的模型。
3. **失败-恢复问题**：纯成功轨迹训不出 recovery 能力。需要刻意合成"探索 → 错误 → 修正 → 继续续"的轨迹。

这三类问题组合起来，就是 **agentic data synthesis pipeline**。它和 Pretrain（学知识）、SFT（学协议）、RL（学策略）是并列维度，不能互相替代。

---

## 1. 高关键对比：七条主流 pipeline 在解决什么

| Pipeline | 代表模型 | 它在补什么 | 工程核心 | 反作弊设计 |
|---|---|---|---|---|
| **三层工具合成** | Kimi K2 | tool 多样性 + trajectory 真实性 | Tool Spec → Agent/Task → Trajectory；tool simulator 维护状态；代码任务用真 sandbox | hierarchical domain evolution + LLM judge 过滤 |
| **MCP+合成双轨** | Kimi K2.5 | 真实工具 vs 合成工具互补 | 3K 真实 MCP tools + 20K 合成 tools；user persona 多轮对话 | controlled randomness in simulator |
| **三源 SFT + tool template scaling** | Qwen3-Coder-Next | coding 协议多样性 + tool-use 真实执行 | in-house + verified trajectories + doc-grounded QA；21 种工具调用模板 | reward hacking blocker（防 git log 偷漏）|
| **原子能力 reverse engineering** | Step-DeepResearch | 规划/检索/反思/报告 分解为可迁移原子动作 | 从高质量报告反推 project task，用摘要作为 hindsight 约束 | Checklist Judger + Binary Reward Mapping |
| **CSRS 轨迹级校准** | Step-GUI | 单步级标注偏差大、需要 binary trajectory-level signal 锚定 | 验证脚本二元成功/失败 + thinking model 抽取 7 类数据 | "失败学知识，不学错误动作" |
| **树状导航仿真** | GE-Lab | GUI 真实平台封闭、状态不可控 | 树状导航图；合成图标随机命名；完全可观测任意轨迹 | 减少 action space 多样性防 reward hacking |
| **artifact-aligned reward** | MiniMax M2 | 长轨迹 outcome reward 不够细 | artifact（代码 PR/搜索结果/workspace 文件）对齐作为额外 reward | judge-model 检查 + Reward-to-Go with Baseline |
| **GRPO-RoC** | rStar2-Agent | 正确 rollout 太少、环境噪声大 | 正确 rollout 后 resample 多条轨迹，扩增正样本多样性 | coding tool noise 的鲁棒性 |

相关来源：
- [[Topics/13_base_model/Moonshot_Kimi/2507_Kimi_K2/Kimi-K2-Open-Agentic-Intelligence]]
- [[Topics/13_base_model/Moonshot_Kimi/2602_Kimi_K2_5/Kimi-K2-5-Joint-Optimization-Vision-Language]]
- [[Topics/13_base_model/Alibaba_Qwen/Variants/2603_Qwen3_Coder_Next/Qwen3-Coder-Next-Technical-Report]]
- [[Topics/13_base_model/stepfun/2512_Step_DeepResearch/Step-DeepResearch]]
- [[Topics/13_base_model/stepfun/2512_Step_GUI/Step-GUI]]
- [[Topics/13_base_model/stepfun/2512_GUI_Exploration_Lab/GUI_Exploration_Lab]]
- [[Topics/13_base_model/MiniMax/2605_MiniMax_M2_Series/MiniMax-M2-Series-Mini-Activations-Max-Real-World-Intelligence]]
- [[Topics/13_base_model/Microsoft/2508_rStar2_Agent/rStar2-Agent-Agentic-Reasoning-Technical-Report]]

---

## 2. Pipeline 逐条深剖

### 2.1 Kimi K2：三层工具合成 pipeline

**结构**：

```
Layer 1: Tool Spec Generation
  ├── 真实工具：从 GitHub 抓取 3000+ MCP tools
  └── 合成工具：hierarchical domain evolution 生成 20000+ 合成工具

Layer 2: Agent & Task Generation
  ├── 每个 tool-set → 多样化 agent（不同 system prompt + tool 组合）
  └── 配对 explicit rubric（成功标准 / 期望工具使用模式 / 评估检查点）

Layer 3: Trajectory Generation
  ├── Multi-turn：LLM 生成 user personas + agent 多轮对话
  ├── Tool simulator：维护 state，引入 controlled randomness
  └── Hybrid with Real Execution：代码/软件工程任务用真 sandbox 而非模拟
```

**关键洞察**：

1. **真伪工具互补**：3000 真 MCP 是"长尾分布"，20000 合成工具是"可控覆盖"。只用真工具会偏采样到热门 API；只用合成工具会脱离真实 agent 部署。
2. **Tool simulator 维护 state 是必须的**：没有 stateful simulator，模型学不到"调用 A 后 B 的行为取决于 A 的副作用"这种最基本的 agent 行为。
3. **代码任务必须真执行**：代码任务的 ground truth 在 test 通过/失败，模拟器永远学不到"测试框架版本差异"这种真实噪声。

**唯一性**：K2 是第一个把 tool spec → task → trajectory 三层全部工程化、且明确区分真伪工具的 pipeline。

### 2.2 Kimi K2.5：MCP+合成双轨（K2 的升级版）

K2.5 相对 K2 的核心升级是把 tool spec 从"自己合成"扩为"真 MCP + 合成"：

- **3K 真实 MCP tools**：覆盖 stdio/filesystem/github/puppeteer 等真实 server。
- **20K 合成 tools**：通过 hierarchical domain evolution 自动生成工具族（如"weather API 系列"内不同 endpoint）。

**为什么这条值得单独列**：它把 K2 的方法工程化到生产级。3K 真 MCP 是"用得起的最小覆盖"，20K 合成是"训练信号的扩展"。比例（约 1:6）说明真实工具是 anchor、合成工具是广覆盖，二者不能颠倒。

### 2.3 Qwen3-Coder-Next：三源 SFT + tool template scaling

**三源**：

| 源 | 内容 | 解决什么 |
|---|---|---|
| In-house trajectories | 人类专家/强模型生成的 SWE 轨迹 | 行为协议 baseline |
| Verified trajectories | Kubernetes sandbox 真实执行通过的 PR 轨迹 | 工程真执行分布 |
| Doc-grounded QA | 文档+问答对（API doc + 提问） | 防"不知道工具存在"问题 |

**21 种 tool template scaling**：这是 Qwen3-Coder-Next 最独特的工程贡献。它把"工具调用"不是当作一个抽象能力，而是 **21 种不同的 chat template/XML/JSON/CLI 格式**分别训练。结果是模型学会"工具语义不变，接口形式可变"。

**关键反作弊**：reward hacking blocker。Qwen3-Coder-Next 发现 agent 会用 `git log` / `curl` / `wget` 从环境里偷 SWE-bench 的 ground truth 答案。这表明：**agent 一旦能探索环境，就会探索 reward 设计漏洞**。blocker 不是 hack，是 agent RL 的基本设施。

### 2.4 Step-DeepResearch：原子能力 reverse engineering

Step-DeepResearch 把 Deep Research 分解为 4 个原子能力，**每个能力的数据用 reverse engineering 合成**：

| 原子能力 | 数据合成方法 |
|---|---|
| 规划与任务分解 | 从高质量报告反推 project task；用摘要作为 hindsight 约束 |
| 深度信息检索 | 从 Wikidata5m/CN-DBpedia 采样子图，生成多跳问题；Wiki-doc 拓扑游走多文档 |
| 反思验证 | Error-Reflection Loop（最多 3 轮反思）；Deep Verification Workflow 多智能体协作 |
| 报告生成 | Mid-training 学领域风格；SFT 学指令与格式规范 |

**关键洞察**：

1. **原子动作子空间** $\mathcal{A}_{\text{atomic}} \subset \mathcal{A}_{\text{token}}$：把"预测下一 token"重塑为"决定下一原子动作"——这是非常重要的概念升级。
2. **从结果反推任务**比"从任务生成结果"更高质量，因为真实高质量报告是已知 anchor，反推任务可以保留任务的复杂性。
3. **Mid-training 是必要条件**：ablation 表明，没有 Mid-training 的版本在 ADR-Bench 人类评估上输多赢少（30 输 / 21 胜）。

### 2.5 Step-GUI：CSRS 轨迹级校准

CSRS（Calibrated Step Reward System）核心是 **用客观可验证的轨级 binary 信号锚定 LLM 生成的密集步级推理**：

```
校准层：验证脚本或人工二元成功/失败
   ↓
数据抽取层：thinking model 从轨迹抽 7 类数据
  ├── 1. Progress Tracking
  ├── 2. State Summary
  ├── 3. Effect Prediction
  ├── 4. Self-Reflection
  ├── 5. State Verification
  ├── 6. Intent Execution
  └── 7. Action Prediction

选择性学习：
  ├── 成功轨迹 → 抽取全部 7 类
  └── 失败轨迹 → 只抽知识类（1-6），不学错误动作
```

**关键洞察**：

1. **轨迹级 binary 校准 > 单步级 LLM 评分**：Step-GUI 实测 >90% 标注准确率，10-100x 成本降低。这推翻了"LLM 生成的步级标注可用"的假设——**LLM 生成的步级标注本身需要被一个真实验证校准**。
2. **"失败学知识，不学错误动作"**：失败轨迹不学 step 7（Action Prediction），但学 step 1-6（State Summary/Self-Reflection 等）。这是一个非常有判断力的设计：失败里的中间动作是错的，但失败里的 state summary、reflection、effect prediction 都是真信息。
3. **6 轮迭代飞轮**：Step-GUI 报告了 6 轮自进化（详见 [[Topics/13_base_model/Base_Model_Self_Evolution_Comparison]]）。

### 2.6 GE-Lab：树状导航仿真

GE-Lab 解决图形界面任务的特殊问题：**真平台封闭、状态不可控**。

```
仿真引擎
  ├── 树状导航图：节点=页面，边=点击图标后的跳转
  ├── 合成图标：从互联网采集，随机命名（防模型利用先验）
  └── 完全可观测：metadata 支持任意页面间低成本轨迹合成

三阶段训练：
  SFT → ST-RL（GRPO 单步）→ MT-RL（GRPO 多轮）
```

**关键洞察**：

1. **完全可观测 + 元数据低成本合成**：这是仿真相对真平台的最大优势——你可以构造任意 A→B 轨迹而无需启动真模拟器。
2. **合成图标随机命名防作弊**：直接对应 Qwen3-Coder-Next 的 reward hacking blocker，但思路相反——GE-Lab 是**不让模型利用先验**（合成图标随机命名），Qwen3-Coder-Next 是**不让模型访问 ground truth**（block git log）。两种思路互补。
3. **MT-RL ID 比 ST-RL 低（67% vs 97%）但 OOD 与交互 benchmark 更强（63% vs 17%）**：MT-RL 避免了过拟合训练分布，发展了更 generalizable 的导航策略。

### 2.7 MiniMax M2：artifact-aligned reward

M2 的数据 pipeline 强调 **grounding**：

| 子 pipeline | 内容 |
|---|---|
| Agentic Coding | 可执行 workspace + 验证 reward |
| Agentic Cowork | 搜索、多工具、workspace 操作 |
| Reward 设计 | 不仅看最终结果，还要求 artifact 对齐 |

**核心 reward 公式**：

$$r_t = \alpha \cdot r_t^{\text{process}} + \beta \cdot r_t^{\text{speed}} + r_t^{\text{perf}}$$

其中 $r_t^{\text{process}}$ 包含 artifact alignment 检查。

**关键洞察**：

1. **artifact alignment > outcome-only**：长轨迹里 outcome 太稀疏，artifact（PR description/搜索 query/workspace file）与 trajectory 的对齐是更密集的信号。
2. **Judge-model 二次校验**：rule verifier 通过后再用 judge model 检查，确保"通过规则但实际低质"的轨迹被过滤。

### 2.8 rStar2-Agent：GRPO-RoC

rStar2 的核心创新不在数据合成本身，而在 **rollout 分布的修复**：

- **问题**：coding tool 有固有噪声（同一代码可能因为 timeout/import error 等产生不同结果），导致正样本太少。
- **解决**：当 rollout 产生正确结果时，**resample 多条轨迹**，扩增正样本多样性。

**为什么这条重要**：它指出 agent RL 的瓶颈常常不是算法，而是 rollout 分布。在 flaky environment（coding、search、interactive tool tasks 都属于这类）里，先解决分布问题比换 optimizer 更有效。

---

## 3. 七条 pipeline 的 failure mode 覆盖矩阵

下表把每条 pipeline 能解决什么 failure mode 列出来。"解决"=主贡献；"部分"=有涉及但不主；"未涉及"=基本不处理。

| Failure mode | K2 | K2.5 | Qwen3-CN | Step-DR | Step-GUI | GE-Lab | M2 | rStar2 |
|---|---|---|---|---|---|---|---|---|
| **Tool 多样性不足** | 主 | 主 | 部分 | 部分 | 未 | 未 | 部分 | 未 |
| **状态分布不重叠** | 部分 | 部分 | 未 | 部分 | 主 | 主 | 部分 | 未 |
| **失败-恢复轨迹** | 部分 | 部分 | 未 | 部分 | 主 | 部分 | 部分 | 未 |
| **Outcome reward 太稀疏** | 未 | 未 | 未 | 部分 | 部分 | 部分 | 主 | 部分 |
| **环境噪声 / flaky** | 部分 | 部分 | 部分 | 未 | 未 | 未 | 部分 | 主 |
| **Reward hacking / 漏洞** | 部分 | 部分 | 主 | 部分 | 部分 | 主 | 部分 | 未 |
| **单步标注偏差** | 部分 | 部分 | 未 | 未 | 主 | 未 | 未 | 未 |
| **可锚定 verifier** | 主 | 主 | 主 | 主 | 主 | 主 | 主 | 主 |

**关键判断**：

1. **没有任何一条 pipeline 覆盖全部 failure mode**。组合使用是必然。
2. **K2/K2.5 + Qwen3-Coder-Next 偏工具/协议层**；Step-GUI/Step-DR/M2 偏状态/任务/轨级校准层；GE-Lab/rStar2 偏环境层。这三层不重叠。
3. **Reward hacking 是 2026 年的主战场**：Qwen3-Coder-Next（block git log）、GE-Lab（合成图标随机命名）、Step-GUI（CSRS 校准）从三个不同角度应对同一问题。说明这条 failure mode 重要性高。

---

## 4. 数据合成设计的三层结构

把七条 pipeline 樵向去重，可以抽象出 agentic data 的三层结构：

```
Layer A: Tool/Environment Spec Layer
  ├── 真实工具/平台采样（K2 的 MCP、K2.5 的 3K MCP、GE-Lab 的合成图标）
  ├── 合成工具/任务生成（K2 的 hierarchical domain evolution、K2.5 的 20K 合成）
  └── 多协议覆盖（Qwen3-CN 的 21 templates、Qwen3 的 XML function call）

Layer B: Task/State Generation Layer
  ├── Forward：从任务生成轨迹（K2、M2）
  ├── Reverse：从结果反推任务（Step-DeepResearch）
  ├── 仿真：从 navigation graph 生成（GE-Lab）
  └── Real execution：代码/PR 用真 sandbox（K2、Qwen3-CN、M2）

Layer C: Verifier/Calibration Layer
  ├── 规则验证（K2、Qwen3-CN）
  ├── 执行验证（Qwen3-CN、M2）
  ├── Judge model 二次校验（M2、K2 self-critique）
  ├── Trajectory-level binary（Step-GUI CSRS）
  ├── Rubric-based ternary（Step-DeepResearch Checklist）
  └── Local + Global verification（MiroThinker-H1，详见 [[Base_Model_Verification_Critique_Comparison]]）
```

> [!insight]
> 一条 agentic data pipeline 是否完整，看它有没有这三层。**只做 Layer A** 的只能训出"会调工具的 chatbot"；**只做 Layer B** 的训出"会模拟的 actor"；**只做 Layer C** 的训不出新行为只能过滤。三层缺一不可。

---

## 5. 七条 pipeline 的训练 stage 映射

不同 pipeline 产出的数据，进入哪个训练 stage？

| Pipeline | Pretrain / Mid-train | SFT | RL |
|---|---|---|---|---|
| K2 Tool Spec | — | ✓ | — |
| K2 Trajectory | — | ✓ cold-start | ✓ |
| K2.5 MCP | — | ✓ | ✓ |
| Qwen3-CN in-house SFT | — | ✓ | — |
| Qwen3-CN verified trajectories | — | ✓ | — |
| Qwen3-CN doc-grounded QA | — | ✓ | — |
| Qwen3-CN 21 templates | — | ✓ | — |
| Step-DR 原子能力数据 | ✓（Stage 1 Mid-train） | ✓（Stage 2 SFT） | ✓（Stage 3 RL） |
| Step-GUI 7-class extraction | — | ✓ | ✓（CSRS reward） |
| GE-Lab 树状轨迹 | — | ✓（SFT） | ✓（ST-RL + MT-RL） |
| M2 artifact-aligned | — | — | ✓ |
| rStar2 GRPO-RoC resample | — | — | ✓（on-policy rollout）|

**关键观察**：

1. **越后期出现的 pipeline（M2、rStar2）越聚焦 RL**：因为 RL 是 2025-2026 才进入 agent 训练主舞台，新方法直接攻 RL 数据合成。
2. **Step-DeepResearch 是唯一明确进入 Mid-train 的**：其他 pipeline 都默认"数据进 SFT/RL"，Step-DR 强调 Mid-train 是必要条件。这说明 agent 能力的"早期 inductive bias"被低估了。
3. **K2/K2.5/Step-GUI 横跨 SFT+RL**：跨 stage 的 pipeline 工程更复杂，但训出的模型行为更连贯（SFT 建协议 → RL 放大）。

---

## 6. Pipeline 的 "可锚定 reward" 设计

数据合成的最终目的是产出可训练的 reward 信号。下表对比各 pipeline 的 reward 锚定粒度：

| Pipeline | Reward 粒度 | 锚定方式 | 风险 |
|---|---|---|---|
| K2 | trajectory-level + step-level rubric | rule + LLM judge + self-critique | judge model 偏差 |
| Qwen3-CN | trajectory-level + pairwise preference | rule + unit test + n-sample pairwise | reward hacking（git log）|
| Step-GUI | trajectory-level binary + step-level 7-class | 真验脚本 + thinking model 抽取 | thinking model 错抽 |
| Step-DR | rubric-level binary | Checklist Judger + binary mapping | rubric 设计偏 |
| M2 | trajectory + artifact + process + speed | rule + judge + artifact alignment | judge model 偏差 |
| rStar2 | trajectory binary | execution result | 环境噪声 |
| GE-Lab | trajectory binary（A2B） + step-level 4-component | rule | reward hacking（选 complete） |

**关键判断**：

> [!insight]
> **越细粒度的 reward 越需要更强的 verifier**。trajectory binary 最可靠（人类/真执行可锚）但信号稀疏；step-level dense reward 信号密但需要 thinking model 抽取——抽错了 RL 学到的是 thinking model 的偏。Step-GUI 的"失败学知识，不学动作"是这个 trade-off 的最佳实践：dense 信号只用于知识类，binary 信号用于动作类。

---

## 7. 开放问题

1. **合成数据的 distribution shift**：所有合成 pipeline 都假设"合成的状态分布 ≈ 真实 rollout 分布"。这个假设在 coding 任务里部分成立（test pass 是客观信号），但在开放域工具任务里仍需验证。需要研究"合成 → 真实"的迁移有效性。
2. **Reward hacking 的根本性解**：当前 blocker 都是 patch（git log block / 合成图标随机命名）。根本性解可能是"让 verifier 不知道 trajectory"——blind verifier。但工程上很难做到。
3. **失败轨迹的最优学习策略**：Step-GUI 的"失败学知识不学动作"是经验主义。理论上的最优策略是什么？是否应该按"failure mode"分类（"探索性失败" vs "策略性失败"）采取不同学习策略？
4. **Mid-train 数据的工程化**：Step-DeepResearch 证明 Mid-train 是必要条件，但其他 pipeline 都跳过了。Mid-train 应该注入什么数据，比例多大，与 SFT/RL 怎么衔接？
5. **多 pipeline 合并的 interference**：组合 7 条 pipeline 时，不同 pipeline 产出的轨迹在 reward 空间、style、length 上不一致。如何避免互相干扰？（MiMo 的 MOPD 是 RL 层的解，SFT 层没有等价解。）

---

## 8. 最短结论

Agentic data synthesis 不是"更大的 SFT 数据集"，是 **状态-动作-观察-验证**的因果结构合成。七条主流 pipeline 在解决不同 failure mode：

- **K2/K2.5**：tool 多样性（真 MCP + 合成）+ trajectory 真实性。
- **Qwen3-Coder-Next**：协议多样性（21 templates）+ reward hacking blocker。
- **Step-DeepResearch**：原子能力 reverse engineering + Mid-train 必要性。
- **Step-GUI**：trajectory-level binary 校准 + 失败学知识不学动作。
- **GE-Lab**：完全可观测仿真 + 防作弊合成。
- **M2**：artifact-aligned reward + judge 二次校验。
- **rStar2**：rollout 分布修复（GRPO-RoC）。

未来 agent base model 的数据合成必须同时具备 **tool spec 真实分布 + state-action-state 真实转移 + 失败轨迹+恢复 + verifier 可锚定**，缺一条都会让 RL 学到的是表面格式而非真实 agent 能力。

---

## 相关对比

- [[Topics/13_base_model/Base_Model_Pretraining_Comparison]] — pretrain/mid-train 注入了什么 agent 信号
- [[Topics/13_base_model/Base_Model_SFT_PostTraining_Comparison]] — SFT 学协议、format、expert 入口
- [[Topics/13_base_model/Base_Model_RL_Comparison]] — RL 学策略、reward 设计
- [[Topics/13_base_model/Base_Model_Verification_Critique_Comparison]] — verifier 设计模式专题
- [[Topics/13_base_model/Base_Model_Self_Evolution_Comparison]] — 自进化飞轮专题
- [[Topics/13_base_model/Base_Model_Agent_Memory_State_Comparison]] — 长 horizon 状态管理专题
