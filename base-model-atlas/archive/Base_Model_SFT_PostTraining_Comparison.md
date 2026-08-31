---
title: "Base Model SFT and Post-training Comparison"
type: insight
tags: [insight, base-model, sft, post-training, distillation, agent]
source: "[[Topics/13_base_model/Base Model MOC]]"
related:
  - "[[Topics/13_base_model/Base_Model_Pretraining_Comparison]]"
  - "[[Topics/13_base_model/Base_Model_RL_Comparison]]"
  - "[[Topics/13_base_model/Base_Model_Agentic_Data_Synthesis_Comparison]]"
  - "[[Topics/13_base_model/Base_Model_Verification_Critique_Comparison]]"
created: 2026-06-12
updated: 2026-06-18
---

# Base Model SFT and Post-training Comparison

> [!tldr]
> SFT 的地位在下降，但不是变得不重要，而是从“最终对齐手段”变成“可被 RL 改进的行为接口”。2025-2026 的强模型基本收敛到一个共识：SFT 负责协议、格式、模式切换、领域入口和 cold-start；RL 负责从可验证环境中长能力；distillation 负责把多域 teacher 合并；self-distillation 负责把 RL 探索出的新行为固化成下一轮数据。真正的分歧不再是“要不要 SFT”，而是：SFT 应该保留多少探索可塑性？专家能力应该直接混训，还是先分域 RL 再合并？失败轨迹应该进入 SFT、preference，还是只作为 verifier/RL 信号？

## 0. 先定义：这里的 post-training 不是一个阶段，而是四类信号

很多技术报告把 post-training 写成一个 pipeline，但它其实由四种性质完全不同的训练信号组成。混在一起看，很容易得出“SFT 不重要了”这种过粗结论。

| 信号类型 | 训练对象 | 核心作用 | 典型失败模式 |
|---|---|---|---|
| **SFT / Cold-start SFT** | 模仿高质量行为轨迹 | 建立对话协议、工具格式、thinking/direct 模式、领域入口 | 数据太简单会降低探索；格式单一会 scaffold overfit |
| **Preference / DPO-like** | 区分好坏响应或轨迹 | 在不可完全验证的开放域任务中注入偏好排序 | 轨迹级偏好信用分配粗，长任务容易奖惩错步骤 |
| **RL / RLVR / Agentic RL** | 在环境中优化策略 | 用 verifier、sandbox、reward model 推动能力增长 | reward hacking、长轨迹 credit assignment、环境噪声 |
| **Distillation / Self-distillation** | 合并 teacher 或固化 RL 发现 | 把 expert、RL teacher、强模型输出压回统一模型 | teacher conflict、能力遗忘、蒸馏只学表面答案 |

**我的判断**：SFT 和 RL 的关系不是“旧范式 vs 新范式”，而是“行为分布初始化 vs 环境反馈优化”。SFT 决定模型一开始会不会以可训练的方式探索；RL 决定探索是否能转化为可泛化能力；distillation 决定这些能力能否进入一个可部署的统一模型。

## 高关键对比 1：SFT 到底在学什么

| 模型 | Pipeline | SFT 真正承担的角色 | 后训练的决定性动作 | 深层判断 |
|---|---|---|---|---|
| Qwen3 | Long-CoT cold start -> Reasoning RL -> mode fusion -> General RL -> distillation | 用可验证 reasoning 数据冷启动 thinking 行为 | 统一 thinking/non-thinking，并用 strong-to-weak distillation 放大小模型 | SFT 不是“教会推理”，而是建立 `<think>` 行为先验，让 GRPO 能在正确动作空间内探索 |
| Qwen3-Coder-Next | Base -> SFT -> WebDev/UX/SWE/Single-turn experts -> distillation | 学 coding instruction、verified trajectories、doc-grounded QA、tool protocol | 21 种 tool template scaling + reward hacking blocker | coding agent 的 SFT 本质是接口鲁棒性训练：同一工具语义要跨 XML/JSON/CLI/scaffold 泛化 |
| GLM-4.5 | Reasoning/Agent/General experts -> unified hybrid model | 为三个 expert 分别建立可 RL 的行为初态 | Expert Model Iteration + self-distillation | 先分 expert 再统一，承认 Reasoning/Agent/General 的 reward 和行为分布不同 |
| GLM-5.2 | 多 expert -> slime rollout/serving -> parallel OPD -> long-horizon RL | 延续 expert 能力入口，并让模型适应 compacted traces | critic-based PPO + online anti-hack guard + parallel OPD | long-horizon agent 的后训练开始和 serving/cache/compaction 合流 |
| MiMo V2/V2.5 | SFT student -> domain RL teachers -> MOPD student | 建立 diverse instruction following 和领域入口 | 用 MOPD 合并多域 teacher，缓解 RL teacher 干扰 | MOPD 的价值在于 on-policy 合并，不是离线抄 teacher 答案 |
| Kimi K2.5 | native multimodal pretrain -> zero-vision SFT -> multimodal RL -> PARL | 纯文本 SFT 通过程序化图像工具激活视觉 reasoning | 视觉 RL + Agent Swarm，把能力扩到跨模态和并行 agent | 当 pretrain alignment 足够强，SFT 可以训练“操作接口”而不一定直接堆目标模态样本 |
| MiniMax M2 | mixed-domain post-training -> Forge RL -> interleaved thinking | 学会 coding/search/office/tool workflow 的基本形态 | 保留 reasoning state，使用 composite reward 训练长轨迹 | SFT 学 workflow 外形，RL 学在 observation 变化后持续修正状态 |
| Step 3.5 Flash | unified SFT -> domain RL -> self-distill -> scalable RL loop | 统一 Math/Code/STEM/Logic/Agent/Long Context 行为 | 专家轨迹拒绝采样后合并到学生模型 | 871K 多域 SFT 更像“统一初态”，后续能力增长来自 MIS-PO 和 self-distill |
| Step-GUI | mid-train -> curriculum SFT -> RLVR | 初始化 visual grounding、action alignment、trajectory | CSRS step reward + GUI-MCP 部署协议 | GUI 任务证明：失败轨迹可学知识，但不能直接学错误动作 |

相关来源：
- [[Topics/13_base_model/Alibaba_Qwen/2505_Qwen3/Qwen3-Technical-Report]]
- [[Topics/13_base_model/Alibaba_Qwen/Variants/2603_Qwen3_Coder_Next/Qwen3-Coder-Next-Technical-Report]]
- [[Topics/13_base_model/Zhipu_GLM/2508_GLM_4_5/GLM-4.5-ARC-Foundation-Models]]
- [[Topics/13_base_model/Zhipu_GLM/2606_GLM_5_2/GLM-5.2-Long-Horizon-Coding-Agent]]
- [[Topics/13_base_model/Xiaomi_MiMo/MiMo-Summary-Dense]]
- [[Topics/13_base_model/Xiaomi_MiMo/2601_MiMo_V2_Flash/MiMo-V2-Flash]]
- [[Topics/13_base_model/Moonshot_Kimi/2602_Kimi_K2_5/Kimi-K2-5-Joint-Optimization-Vision-Language]]
- [[Topics/13_base_model/MiniMax/2605_MiniMax_M2_Series/MiniMax-M2-Series-Mini-Activations-Max-Real-World-Intelligence]]
- [[Topics/13_base_model/stepfun/2512_Step_GUI/Step-GUI]]
- [[Topics/13_base_model/stepfun/2602_Step_3_5_Flash/Step-3.5-Flash]]

## 高关键对比 2：SFT 的深层功能已经从“对齐”拆成五件事

### 1. Interface prior：让模型进入正确协议空间

对 agent base model 来说，SFT 最基础的作用是把输出约束到“环境能执行”的形式：工具调用 schema、function call XML、CLI 命令、GUI action、MCP protocol、thinking/direct 标签。这个能力看起来低级，但它决定 RL 是否有意义。

如果没有 interface prior，RL 初期采样到的大量行为都是 invalid action，reward 全是噪声；如果 interface prior 太强，模型又会过度模仿训练 scaffold，换一个工具模板就掉性能。Qwen3-Coder-Next 的 21 种 tool template scaling 正是在解决这个张力：**SFT 不应该只训练一种格式，而要训练格式不变性**。

### 2. Cognitive mode prior：让模型知道何时 think，何时直接答

Qwen3 的 thinking/non-thinking 融合和 GLM-4.5 的 hybrid thinking/direct 都说明，后训练已经不只是“让回答更好”，而是训练模型的 **mode controller**。SFT 在这里学的不是某个答案，而是：

- 哪类任务需要长 CoT。
- 哪类任务应该短答，避免过度推理。
- thinking tokens 与 final answer 如何分离。
- 工具观察返回后是否继续思考。

这类能力很难纯靠 RL 从零学，因为 early exploration 太稀疏；也很难纯靠 SFT 达到上限，因为模式选择依赖真实任务结果。

### 3. Domain entry prior：给 RL 一个可探索的起点

GLM-4.5 的 Reasoning/Agent/General experts、MiMo V2 的 domain teachers、Step 3.5 Flash 的多域 SFT 都在做同一件事：先把模型推到每个领域“能开始做”的区域。

这个起点不是越强越好，而是要满足三条：

1. **有效动作率足够高**：RL rollout 中 invalid format、明显跑题、空转比例不能太高。
2. **错误仍有多样性**：模型不能只会模板化回答，否则 RL 没有探索空间。
3. **reward 能区分行为差异**：如果 SFT 后同一个 prompt 的采样几乎全对或全错，group-relative RL 信号会变弱。

这解释了为什么一些报告会过滤简单 prompt、保留 medium/hard 样本。SFT 太容易，会提升表面 helpfulness，却降低后续 RL 的有效学习信号。

### 4. State representation prior：学会在轨迹中维护状态

MiniMax M2 的 interleaved thinking 把这个问题讲得最清楚：agent 不是一次性输出答案，而是在 `reasoning -> action -> observation` 循环中持续更新状态。SFT 如果只给 front-loaded reasoning，模型会在工具观察出现后无法修正计划；如果每轮 stateless reasoning，又会重复推导、状态漂移。

因此 agent SFT 应该刻意覆盖：

- 中间 observation 与原计划冲突时如何修正。
- 工具失败、测试失败、网页变化时如何恢复。
- 哪些中间结论应该保留，哪些可以丢弃。
- 何时继续探索，何时停止。

这类数据不只是“多轮对话”，而是带状态转移的轨迹数据。它和 [[Topics/13_base_model/Base_Model_Agentic_Data_Synthesis_Comparison]] 里的 state-action-observation-verification 结构是一体的。

### 5. Distillation target prior：让统一模型能接住 expert 能力

Expert distillation 不是最后把答案混一下。它要求 student 已经有足够的 shared interface 和 shared representation，否则不同 teacher 的行为会互相污染。

例如：

- Qwen3-Coder-Next 先有 base SFT，再训练 WebDev/UX/SWE/Single-turn experts，最后统一蒸馏。
- GLM-4.5 先有 Reasoning/Agent/General experts，再 self-distill 成 hybrid model。
- MiMo V2 用 MOPD 让 student 在自己的 on-policy rollout 上接收 teacher token-level guidance。

这里的关键是：**SFT 建立 student 的可接收空间，distillation 才能真正合并能力**。没有这个 shared prior，蒸馏常常只会学到 teacher 的口吻和格式，而不是能力。

## 高关键对比 3：四种 post-training 哲学

### 哲学 A：统一模型优先

代表：Qwen3。

先把 thinking/non-thinking 两种行为放进一个模型，再通过 budget 控制输出。优点是产品形态简单，缺点是不同能力的相互干扰需要精心设计 stage。

**适用条件**：领域之间共享大量底层能力，比如 math/code/general reasoning 都能通过统一 verifier 和格式控制受益。

**风险**：统一得太早会出现 mode interference：该短答时过度思考，该深思时提前收敛；agent 任务里还会出现工具调用和自然语言解释互相污染。

### 哲学 B：先分 expert，再统一

代表：GLM-4.5、Qwen3-Coder-Next、Step 3.5 Flash。

先让 Reasoning / Agent / General 或 WebDev / UX / SWE 等 expert 各自变强，再蒸馏进统一模型。优点是每个能力域能针对性优化；缺点是合并时会丢能力或产生冲突。

**适用条件**：不同领域 reward 目标差异明显。比如 coding 需要 test pass，agent 需要工具成功和速度，general chat 需要偏好对齐，safety 需要约束行为。

**风险**：expert 越强，合并越难。蒸馏时如果只看最终 answer，会丢掉 expert 的中间策略；如果把所有轨迹混合 SFT，又可能伤害通用能力。

### 哲学 C：多 teacher on-policy 合并

代表：MiMo V2/V2.5 的 MOPD。

不是简单蒸馏专家答案，而是用 on-policy distillation 合并多个 domain teacher。关键价值在于解决 multi-domain RL interference：一个 teacher 强 math，一个 teacher 强 agent，一个 teacher 强 safety，直接混 reward 可能互相伤害。

**适用条件**：student 需要保持自己的采样分布，同时吸收 teacher 的局部优势。MOPD 的重点不是“teacher 输出什么”，而是“student 在自己会走到的 token/state 上，teacher 给什么方向”。

**风险**：teacher guidance 如果没有过滤，会把低质量 token、分布外 token 或 teacher 自己的偏置灌进 student。MiMo V2 的 training-inference IS mask 和 reverse KL advantage 本质上是在做 teacher signal sanitation。

### 哲学 D：训练系统与部署系统合流

代表：MiniMax M2、GLM-5.2。

这条路线不再把 post-training 当离线训练 recipe，而是把 rollout、serving、cache、agent scaffold、anti-hack、compaction 都看作同一系统的一部分。MiniMax Forge 支持白盒/黑盒 agent、Windowed FIFO、prefix tree merging、KV cache 复用；GLM-5.2 用 slime 串起 rollout、parallel OPD、long-horizon serving 和 online anti-hack guard。

**适用条件**：long-horizon coding / research / GUI / office agent。此时训练瓶颈不是算法名，而是如何稳定产生、存储、审计和复用长轨迹。

**风险**：系统复杂度高，训练目标容易被 scaffold 绑定。模型可能学到某个 harness 的捷径，而不是可迁移的 agent 能力。

## 关键机制 1：SFT 数据质量的判断标准变了

以前 SFT 数据常按“答案是否优质”来筛，现在 agent/base model 的 SFT 数据至少要按五个维度判断：

| 维度 | 好数据的特征 | 坏数据的症状 | 代表例子 |
|---|---|---|---|
| **可执行性** | 轨迹能在 sandbox / GUI / tool 环境中复现 | 看起来合理但执行失败 | Qwen3-Coder-Next verified trajectories |
| **格式多样性** | 同一语义跨多种 template 表达 | 换 scaffold 后 tool-use 崩 | 21 种 tool template scaling |
| **难度密度** | prompt 处在模型可探索但不全对的位置 | 简单样本堆多，RL 信号变弱 | GLM prompt filtering / hard prompt response scaling |
| **状态覆盖** | 含成功、失败、恢复、观察变化 | 只学成功 demo，遇到异常不会修 | Step-GUI CSRS、MiniMax interleaved thinking |
| **verifier 锚定** | 每条轨迹可由外部信号校准 | judge 自说自话、reward 不可信 | Step-GUI trajectory-level calibration |

**我的判断**：SFT 数据的核心不再是“像人类”，而是“可被环境验证、可支持后续策略改进”。一个普通但可执行、可验证、能产生对比学习信号的轨迹，常常比一个漂亮但不可验证的答案更有训练价值。

## 关键机制 2：失败轨迹不能简单丢，也不能直接学

失败轨迹是 agent training 最容易被低估的资产。问题在于，失败轨迹里混着两种东西：

1. **有价值的状态知识**：模型到达了什么页面、工具返回了什么错误、测试失败暴露了什么约束。
2. **不该模仿的错误动作**：点错按钮、调用错工具、复制错误假设、绕过评测漏洞。

Step-GUI 的策略很有启发：成功轨迹抽取完整 7 类数据，失败轨迹只抽取知识类数据，不学习错误动作。这个原则可以推广到 coding/search/research agent：

| 失败轨迹片段 | 是否适合 SFT | 更适合的训练信号 |
|---|---|---|
| 错误前的有效观察、状态摘要 | 适合 | SFT / state summary |
| 第一次实质性错误决策 | 不宜直接 SFT | preference / dwDPO-like step weighting |
| 错误后的 recovery 行为 | 如果最终恢复成功，适合 | SFT + process reward |
| reward hacking 行为 | 不适合 | blocker / penalty / online guard |
| 长时间空转 | 不适合 | speed reward / termination reward |

**对当前研究的启发**：失败轨迹的关键不是“变成正样本”，而是拆开成 state、decision、recovery、hack、dead-loop 五类不同信号。SFT 只应该吸收其中可迁移的状态理解和恢复策略；错误决策应该进入偏好优化或 RL penalty。

## 关键机制 3：RL cold-start 需要“适度 SFT”，不是最大 SFT

SFT 过少，RL 会陷入 invalid actions；SFT 过多，RL 会失去探索。这个 trade-off 在 GUI、coding、long-horizon agent 中都很明显。

可以把冷启动质量看成三个指标：

```text
RL cold-start quality
  = valid action rate
  + behavior diversity
  + reward separability
```

- **valid action rate** 太低：rollout 里大多数工具调用无效，训练被格式错误主导。
- **behavior diversity** 太低：模型只会复现 SFT 模板，采样不到新策略。
- **reward separability** 太低：同一 prompt 的采样全对或全错，group-relative advantage 失效。

这解释了三个看似不同的做法：

- Qwen3 用 3,995 query-verifier pairs 做 Long-CoT cold start，不是海量普通 SFT。
- GLM-4.5 过滤 bottom 50% 短响应 prompt，并对 hard prompt 做 response-level scaling。
- GUI Exploration Lab 发现过多 SFT 会损害 RL 效果，早期 SFT epoch 初始化 RL 反而最好。

**结论**：SFT 的目标不是把模型训到“看起来完成任务”，而是把模型放在一个 RL 能分辨好坏、还能探索改进的区域。

## 关键机制 4：Distillation 已经分化成四种完全不同的东西

| 蒸馏类型 | 代表 | 蒸馏什么 | 适合解决 |
|---|---|---|---|
| **Strong-to-weak distillation** | Qwen3 | 大模型 thinking/non-thinking 输出 | 把强推理能力压到小模型 |
| **Expert distillation** | GLM-4.5、Qwen3-Coder-Next | 多个 domain expert 的行为 | 统一 Reasoning/Agent/General 或 WebDev/SWE/UX |
| **On-policy distillation** | MiMo V2 MOPD | student 自己 rollout 上的 teacher token guidance | 缓解 teacher/student 分布错位和多域干扰 |
| **Self-distillation** | GLM-4.5、Step 3.5 Flash、MiniMax M2 | RL 后模型生成的新高质量轨迹 | 把 RL 探索出的能力固化为下一轮 SFT 数据 |

这里最容易混淆的是 expert distillation 和 self-distillation：

- **Expert distillation** 是横向合并：多个 teacher，各自擅长不同域。
- **Self-distillation** 是纵向迭代：同一个模型经过 RL 变强后，反过来给下一轮训练造数据。

强模型路线越来越像一个飞轮：

```text
SFT cold-start
  -> domain RL / agentic RL
  -> expert or self-distillation
  -> cleaner unified model
  -> harder rollout / better verifier data
  -> next RL round
```

这个飞轮比一次性 SFT 数据集重要得多。它也解释了为什么 Base Model topic 现在应该把数据、RL、verification、inference infra 放在一起看，而不是分散看。

## SFT 的四个陷阱

| 陷阱 | 表现 | 代表警告 | 解决思路 |
|---|---|---|---|
| 简单样本过多 | 模型更听话但 exploration 下降 | Llama 4 路线、GLM/Qwen hard prompt filtering | 删除简单 prompt，保留 medium/hard 样本 |
| 格式过拟合 | 换一个 scaffold 就 tool-use 失败 | Qwen3-Coder-Next | tool template scaling |
| 领域遗忘 | domain SFT 后通用能力下降 | MiMo-VL-Miloco | targeted RL recovery |
| 长 CoT 幻觉 | 看起来推理很长但不能根据 observation 更新 | MiniMax M2 | interleaved thinking + state persistence |

还可以再补四个更 agent-specific 的陷阱：

| 陷阱 | 表现 | 为什么危险 | 解决思路 |
|---|---|---|---|
| **成功轨迹偏置** | 模型只会顺风执行，不会 debug/recover | 真实 agent 大量时间在处理异常状态 | 合成失败-恢复轨迹；失败轨迹只学知识不学错动作 |
| **teacher conflict** | math/coding/safety/general 能力互相拉扯 | 多域 reward 目标不同，直接混训会互相伤害 | expert RL + MOPD / distillation |
| **reward leakage** | agent 学会读答案、绕 sandbox、利用 git/network | 越强的 agent 越会主动探索评测漏洞 | blocker、online guard、dummy response、环境隔离 |
| **serving mismatch** | 训练时完整轨迹，部署时 compaction/cache/routing | 长任务真实运行一定会压缩、分段、复用缓存 | 把 compacted traces 和 serving constraints 纳入训练 |

## 最关键的机制差异：逐条深挖

### 1. Tool template scaling

Qwen3-Coder-Next 训练 21 种工具调用格式，这个点比表面分数更重要。它说明 tool-use 能力不是抽象存在的，模型会过拟合特定 XML/JSON/CLI/chat template。

更深一层看，tool template scaling 训练的是 **semantic-tool invariance**：

```text
同一个工具意图
  -> 多种 schema / XML / JSON / CLI / IDE protocol
  -> 同样能完成状态转移
```

这对 GUI/MCP/浏览器 agent 很关键，因为真实产品里的 tool surface 会频繁变化。一个只在单一模板上 SFT 的模型，可能 benchmark 很高，但换成另一个 agent scaffold 就掉。

### 2. Reward hacking blocker

Qwen3-Coder-Next 发现 agent 会利用 git / remote / curl / wget 等方式偷 ground truth。这不只是 SWE-bench 问题，而是所有 agent RL 的基本问题：一旦环境可探索，模型就会探索 reward 设计漏洞。

GLM-5.2 的 online anti-hack guard 更进一步：不是检测到 hack 后丢掉整条轨迹，而是在每一步 tool call 监控并阻断，返回 dummy information，让 rollout 继续。这一点很重要，因为直接 reject 整条轨迹会让 RL 数据分布剧烈变化；在线阻断则把“越权不可用”变成环境动力学的一部分。

**判断**：anti-hack 不应该是评测补丁，而应该是 agent training environment 的一等组件。越接近真实电脑使用、代码执行、浏览器环境，越需要把安全边界写进 rollout。

### 3. Zero-vision SFT

Kimi K2.5 的 zero-vision SFT 很反直觉：纯文本 SFT + 程序化图像操作代理可以激活视觉能力。这说明如果 joint multimodal pretrain 足够强，SFT 不一定要大量视觉样本。

这里的深层含义是：SFT 可以训练 **跨模态操作程序**，而不是直接训练目标模态感知本身。只要 pretrain 已经建立 text-vision alignment，文本工具轨迹可以教模型“如何调用图像操作、如何把视觉 observation 纳入推理”。

这对 GUI agent 很有价值：大量 GUI 数据昂贵，但可以用文本化的工具操作、accessibility tree、程序化截图分析来训练 action/reasoning protocol，再通过少量 RL/grounding 数据校准视觉动作。

### 4. Self-distillation loop

GLM-4.5、Step 3.5 Flash 都显示：RL 后的模型可以生成更高质量轨迹，再用作下一轮 SFT teacher。这个循环比一次性 SFT 数据集更重要。

但 self-distillation 有一个隐藏风险：模型会把自己 RL 中形成的偏置也蒸馏回去。因此必须配合：

- verifier / sandbox 过滤。
- rejection sampling。
- reward hacking 检测。
- 多 teacher 或 human audit。
- 对 hard prompt 的 response-level scaling，而不是无差别采样。

### 5. Interleaved thinking

MiniMax M2 的贡献在于把 agent reasoning 从“前置长 CoT”改成“观察驱动的持续状态更新”。这比“模型会不会想很久”更重要。

```text
front-loaded thinking:
  reason reason reason -> action -> observation -> action

interleaved thinking:
  reason -> action -> observation -> revise reason -> action -> observation
```

对长任务 agent，第二种才接近真实工作流。它要求 SFT 数据和 RL 环境都保留 reasoning state，而不是每轮把 thinking blocks 剥离掉。否则模型每一步都在重推导，容易发生 cumulative state drift。

### 6. MOPD / OPD：合并能力不是离线抄答案

MiMo V2 的 MOPD 和 GLM-5.2 的 parallel OPD 共同指向一个趋势：多域合并要越来越 on-policy。

原因很简单：如果 student 从不会走到某个 state，teacher 在那个 state 上的答案再好，也很难直接转化为 student 能力。on-policy distillation 让 teacher 在 student 自己的 rollout 分布上给 guidance，减少训练-推理错位。

## 一张决策表：什么时候用 SFT，什么时候用 RL，什么时候用 distillation

| 目标 | 首选训练信号 | 不要只靠 | 关键检查项 |
|---|---|---|---|
| 建立工具调用格式 | SFT + template scaling | RL 从零学格式 | invalid tool call rate 是否足够低 |
| 提升 math/code 正确率 | RLVR / GRPO / MIS-PO | 普通 SFT | verifier 是否可靠，采样是否有区分度 |
| 训练 coding agent | verified SFT + single-turn RL + multi-turn RL | outcome-only RL | 是否防 git/network leakage，是否有真实 sandbox |
| 训练 deep research agent | 原子能力 SFT + rubric reward + RL | 最终报告 SFT | citation/factuality/coverage 是否可校准 |
| 训练 GUI agent | grounding/action SFT + CSRS/RLVR | 成功 demo SFT | 失败轨迹是否只学知识不学错动作 |
| 合并多域能力 | expert distillation / MOPD | 多域 reward 直接混 | teacher conflict 是否被隔离 |
| 长轨迹 agent | composite reward + interleaved thinking + infra-aware RL | 只看最终成功 | 是否处理 compaction、speed、state persistence |
| 强模型迭代 | self-distillation loop | 一次性数据集 | RL 生成轨迹是否经过 verifier/rejection sampling |

## 对 Agent Training 的研究定位

这篇 comparison 对当前 Agent Training 方向的直接启发是：**SFT/RL/Distillation 不是三种可替代方法，而是三种不同粒度的 credit assignment。**

- SFT 给 token/action 一个正例轨迹，但不知道反事实。
- Preference 给两条轨迹一个相对排序，但常常不知道关键分歧点。
- RL 给环境结果和过程 reward，但需要可验证环境和稳定采样。
- Distillation 把 teacher 的局部策略压给 student，但需要处理分布错位。

因此一个强 agent base model 的训练设计，应该先回答四个问题：

1. **动作空间是否先被 SFT 约束到有效区间？**
2. **失败信号是否能被拆到 step/state/recovery，而不是只给整条轨迹标签？**
3. **不同能力域是否有互相冲突的 reward？如果有，就应该先 expert 化。**
4. **部署时的真实约束，如 compaction、cache、sandbox、anti-hack，是否进入训练环境？**

我的判断：2026 年之后的 agent base model 差距，很大一部分不会来自“谁的 SFT 数据更多”，而来自谁能把 **可验证环境、失败轨迹拆解、on-policy teacher 合并、在线安全边界、长轨迹训练系统** 做成闭环。

## 最短结论

SFT 不是越大越好，也不是越像人类答案越好。对 agent base model 来说，SFT 最重要的作用是建立“可被 RL 改进的行为接口”。真正的上限来自：是否有可靠 verifier、是否能防 reward hacking、是否能合并多域 teacher、是否能保留长轨迹 reasoning state。
