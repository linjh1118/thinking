---
title: "Base Model Pretraining Comparison"
type: insight
tags: [insight, base-model, pretraining, data, reasoning, multimodal]
source: "[[Topics/13_base_model/Base Model MOC]]"
related:
  - "[[Topics/13_base_model/Base_Model_Insight]]"
  - "[[Topics/13_base_model/Xiaomi_MiMo/MiMo-Summary-Dense]]"
  - "[[Topics/13_base_model/Base_Model_SFT_PostTraining_Comparison]]"
  - "[[Topics/13_base_model/Base_Model_Agentic_Data_Synthesis_Comparison]]"
created: 2026-06-12
updated: 2026-06-18
---

# Base Model Pretraining Comparison

> [!tldr]
> Pretraining 的关键变化，不是简单从“更多 tokens”变成“更多高质量 tokens”，而是训练阶段的功能边界正在重画：哪些能力必须在 base/mid-training 阶段形成表征锚点，哪些能力可以留给 SFT/RL 释放。我的判断：agent base model 的 pretrain 目标正在从 language modeling 扩展到 **state-action-observation modeling**，但不同论文的证据强度差别很大，不能把技术报告、model card、官方 blog 混成同一级结论。

## 1. 核心问题：能力应该锚定在哪个训练阶段

这个部分更适合问：

> **一种能力如果只靠 post-training 学到，它是不是会停留在行为模板；如果进入 pretrain/mid-training，它是否会变成更稳定的表征与归纳偏置？**

| 能力锚点 | 代表模型 | 进入阶段 | 关键证据 | 我的判断 |
|---|---|---|---|---|
| 通用知识与模式切换 | [[Topics/13_base_model/Alibaba_Qwen/2505_Qwen3/Qwen3-Technical-Report\|Qwen3]] | Pretrain 打广谱基础，post-training 统一 thinking/non-thinking | 36T tokens；三阶段预训练；四阶段后训练 | Qwen3 的强项是产品化统一与模型家族化；agent 轨迹不是 pretrain 主角 |
| ARC 表征前置 | [[Topics/13_base_model/Zhipu_GLM/2508_GLM_4_5/GLM-4.5-ARC-Foundation-Models\|GLM-4.5]] | Pretrain 后的 mid-training | 23T tokens 后加入 repo-level code、synthetic reasoning、128K long-context agent trajectories | 这是“通用 base + ARC mid-train”的清晰路线，比纯 post-training 更接近 agent base |
| Token utility 与训练稳定性 | [[Topics/13_base_model/Moonshot_Kimi/2507_Kimi_K2/Kimi-K2-Open-Agentic-Intelligence\|Kimi K2]] | Pretrain recipe 本身 | rephrasing > repeat；fidelity verification；MuonClip 稳定 15.5T | K2 没把 agent 轨迹主要放进 pretrain，但把每个 token 的学习效率做成 scaling 变量 |
| Reasoning potential 前置 | [[Topics/13_base_model/Xiaomi_MiMo/2505_MiMo_7B/MiMo\|MiMo-7B]] / [[Topics/13_base_model/Xiaomi_MiMo/MiMo-Summary-Dense\|MiMo series]] | Pretrain 起步 | 25T tokens；math/code/STEM/synthetic reasoning 比例递进；MTP | 小模型能被 RL 拉多高，首先取决于 base 里是否已有足够 reasoning density |
| 多模态 grounding 前置 | [[Topics/13_base_model/Xiaomi_MiMo/2506_MiMo_VL_7B/MiMo-VL\|MiMo-VL]] / [[Topics/13_base_model/stepfun/2601_STEP3_VL_10B/STEP3-VL-10B\|STEP3-VL]] | Multimodal pretrain | MiMo-VL 的 GUI transition；STEP3-VL 的 1.2T unified pretraining 与 GUI/OCR/grounding 数据 | grounding 不是“看图补丁”，而是状态建模；后续 RL 主要压缩搜索空间和校准动作 |
| Native multimodality | [[Topics/13_base_model/Moonshot_Kimi/2602_Kimi_K2_5/Kimi-K2-5-Joint-Optimization-Vision-Language\|Kimi K2.5]] / [[Topics/13_base_model/Alibaba_Qwen/Variants/2509_Qwen3_Omni/Qwen3-Omni-Thinker-Talker-Architecture\|Qwen3-Omni]] / [[Topics/13_base_model/Alibaba_Qwen/Variants/2604_Qwen3_5_Omni/Qwen3-5-Omni-Streaming-Omni-Agent\|Qwen3.5-Omni]] | Early/ongoing modality fusion + architecture | low-ratio early fusion；single/cross-modal mixed data；Thinker/Talker；ARIA | 多模态能力从“输入接口”变成“混合状态空间”，后训练不再负责从零对齐模态 |
| 长上下文与能力密度 | [[Topics/13_base_model/stepfun/2602_Step_3_5_Flash/Step-3.5-Flash\|Step 3.5 Flash]] / [[Topics/13_base_model/MiniMax/2606_MiniMax_M3/MiniMax-M3-Frontier-Coding-1M-Context-Native-Multimodality\|MiniMax M3]] | Architecture + pretrain + serving co-design | 196B/11B MoE、S3F1、MTP-3；M3 的 MSA/1M context/native multimodality | agent 能力的瓶颈不只在智力，也在能否便宜地保留长轨迹状态 |
| Agent Foundation Model 宣言 | [[Topics/13_base_model/ByteDance_Seed/2605_Seed2_0_Model_Card/Seed2.0-Model-Card-Agent-Foundation-Model\|Seed2.0]] | 宣称 pretrain 阶段面向 agent | model card 区分 General Foundation Model 与 Agent Foundation Model，提出 agent trajectories/environment feedback | 概念最直接，但当前证据最弱；需要 technical report 验证训练 recipe |

## 2. 阶段边界：pretrain、mid-training、post-training 各自负责什么

| 阶段 | 更适合学什么 | 不适合承担什么 | 代表证据 |
|---|---|---|---|
| Pretrain | world knowledge、reasoning potential、token utility、基础多模态对齐、长上下文表征 | 复杂工具协议、具体产品格式、价值偏好细节 | Qwen3 36T；Kimi K2 rephrasing；MiMo-7B reasoning density；Kimi K2.5 early fusion |
| Mid-training / CPT | repo-level code、long-context agent traces、GUI transition、domain grounding、任务形态迁移 | 高成本开放域 RL、细粒度偏好对齐 | GLM-4.5 ARC mid-training；Step-GUI mid-train；Qwen3-Coder-Next coding CPT/SFT 数据 |
| SFT | instruction protocol、tool-call format、cold-start behavior、expert domain entrance | 能力上限本身；环境理解本身 | Qwen3-Coder-Next tool template scaling；Kimi K2.5 zero-vision SFT |
| RL / self-distillation | verifier 对齐、搜索策略、长轨迹 credit assignment、反作弊、多域 teacher 合并 | 从零学习世界状态；补救所有 pretrain 缺失 | GLM-4.5 expert iteration；MiMo MOPD；Step 3.5 Flash scalable RL；Kimi K2.5 PARL |

这个分工能解释一个常见现象：很多模型在 SFT 后“会调用工具”，但一旦 observation 出现异常就崩。原因是它学到了接口格式，却没有在 base/mid-training 中学到 state transition 和 recovery 的表征。

## 3. 数据量、数据密度、数据形态不是同一件事

| 维度 | 低价值做法 | 高价值做法 | 代表 |
|---|---|---|---|
| 数据量 | 简单重复语料、多 epoch 混训 | 增加去重、可验证、难度可控、高质量样本 | GLM-4.5 quality bucket；Qwen3 数据去污染 |
| 数据密度 | 普通网页语料占主导 | math/code/STEM/reasoning/agent trace 比例递进 | MiMo-7B；GLM-4.5 |
| 表达多样性 | 同一知识反复出现 | rephrasing、多风格、多路径、fidelity verification | Kimi K2 |
| 任务形态 | 单轮 QA 或单文件代码 | repo-level code、issue/PR、multi-file dependency、long-context trajectories | GLM-4.5；Qwen3-Coder-Next |
| 状态结构 | 静态输入到静态答案 | state-action-observation-transition-recovery | MiMo-VL；Step-GUI；Seed2.0 宣言 |
| 模态结构 | 文本训完后接 adapter | early low-ratio fusion、interleaved data、Thinker/Talker 解耦 | Kimi K2.5；Qwen3-Omni；MiniMax M3 |
| 成本结构 | 只看参数规模 | active params、attention pattern、MTP、KV/cache 成本共同优化 | Step 3.5 Flash；MiniMax M3；MiMo V2 |

最关键的 insight：Agent 数据的价值不在“这条轨迹成功了”，而在它提供了状态、动作、观察、错误、恢复、验证之间的因果结构。普通 language modeling 可以吸收知识，但很难天然学到“动作改变环境、环境反馈改变计划”的闭环。

## 4. Reasoning pretrain 和 Agent pretrain 的目标不同

Reasoning pretrain 学的是“从问题到答案的可验证推导”。Agent pretrain/mid-training 还必须覆盖：

1. state：当前环境是什么。
2. affordance：可执行动作有哪些。
3. transition：执行动作后状态怎么变。
4. observation update：新观察如何改变计划。
5. verifier：什么算完成，什么算失败。
6. recovery：失败后怎么回退或改策略。
7. memory policy：哪些历史状态应该保留、压缩或路由给子 agent。

这解释了为什么 MiMo-VL 的 before/after screenshot transition prediction、GLM-4.5 的 long-context agent mid-training、MiniMax M3 的 1M context + interleaved multimodal data、Seed2.0 的 environment feedback 叙事，比普通 tool-call SFT 更接近 Agent Foundation Model 的本质。

## 5. 三条 pretrain 路线的真实分歧

### 路线 A：通用 base 优先，post-training 做统一行为

代表：Qwen3 主线。

优点是家族化、可控性和产品一致性强；缺点是 agent 能力更依赖后训练和 scaffold。如果 pretrain 没见过足够的状态转移与工具反馈，模型容易“会格式，不懂环境”。

### 路线 B：pretrain/mid-training 注入 reasoning、grounding、agent signals

代表：GLM-4.5、MiMo、STEP3-VL、Kimi K2.5、Seed2.0。

优点是 base 的 inductive bias 更接近 agent，后续 RL 更容易放大；缺点是数据工程贵、证据更难公开，而且多域信号可能互相干扰。MiMo 的 MOPD 和 GLM 的 expert iteration 都是在补这个问题。

### 路线 C：通过架构、优化器、注意力和数据共同提高能力密度

代表：Kimi K2、Step 3.5 Flash、MiniMax M3、MiMo V2。

优点是适合 long-horizon agent 的训练与部署：更便宜的 rollout、更长的 state history、更低的 serving 成本。缺点是复现门槛高，技术报告之外的 blog/model card 证据要降级看。

## 6. 证据强度分层

| 证据强度 | 代表 | 可以怎么用 |
|---|---|---|
| 强：完整技术报告/论文 + 训练细节 + ablation | Qwen3、GLM-4.5、Kimi K2、MiMo-7B/VL/V2、STEP3-VL、Kimi K2.5、Step 3.5 Flash | 可以作为训练 recipe 和研究假设来源 |
| 中：官方 model note/blog + benchmark + 部分方法细节 | MiniMax M3、部分 MiMo V2.x blog | 可以作为趋势信号，等待技术报告校准 |
| 弱：model card/定位宣言 | Seed2.0 | 可以引用概念，但不应当当作已验证 recipe |
| 不透明：system card 只披露行为和安全评估 | OpenAI/Anthropic/Google 近期模型 | 适合做能力边界对照，不适合推断 pretraining recipe |

## 7. 可执行的数据设计建议

| 目标能力 | 应进入 pretrain/mid-training 的数据 | 适合留给 SFT/RL 的部分 | 不应只靠什么 |
|---|---|---|---|
| Coding agent | repo-level code、issue/PR、test logs、multi-file dependency、失败修复轨迹 | tool template、sandbox reward、reward hacking blocker | 单文件代码补全 |
| Research agent | search trace、evidence graph、source conflict、citation judgment、报告反推任务 | checklist/rubric reward、self-critique、human audit | 多跳 QA |
| GUI / computer use | before/after screenshots、action transition、UI affordance、跨平台 action space | RLVR/RLHF 校准、CSRS、环境反作弊 | 静态 element grounding |
| Tool-use | tool spec、stateful simulator、API side effect、error recovery | tool-call format、template scaling、execution verifier | 静态 function signature |
| Multimodal agent | low-ratio early fusion、interleaved multimodal state、video/audio/document long context | zero-vision SFT、visual RL、omni RLHF | 后接 adapter |
| Long-horizon agent | long context trajectory、memory routing、context sharding、failure replay | PARL、Agent Swarm、composite reward | outcome-only trajectory |

## 8. 对当前研究的判断

1. **Agent base 的关键不是“有没有工具调用数据”，而是有没有状态转移数据。** Tool-call SFT 解决的是接口，state-action-observation 数据解决的是环境理解。
2. **Reasoning density 是 RL 的地基，但不是 agent 的全部。** MiMo-7B 证明小模型 reasoning potential 可以被 RL 放大；MiMo-VL/Step-GUI 说明 agent 还需要 transition、grounding、recovery。
3. **长上下文成本会改变 agent 数据设计。** 如果 MiniMax M3 / Kimi Linear / MiMo Hybrid SWA 这类路线让长轨迹保留变便宜，训练数据就可以从“摘要后再训练”转向“完整轨迹 + 稀疏选择 + replay”。
4. **Seed2.0 的 Agent Foundation Model 概念是正确方向，但证据还不够。** 目前更适合作为命名和问题定义，不适合作为技术 recipe。

## 9. 还缺什么才能做更强判断

1. DeepSeek pretraining/mid-training 作为强 baseline。
2. Seed2.0 technical report，验证 AFM pretrain 是否真的有 agent trajectories/environment feedback。
3. Llama 4 full technical note，补 early fusion / online RL / open-weight multimodal 的对照。
4. MiniMax M3 technical report，确认 interleaved multimodal pretraining、interactive user simulator 和 MSA 的细节。
5. OpenAI/Anthropic/Google system cards 的“不透明训练部分”需要单独标证据等级，避免把能力表现误读成训练 recipe。
