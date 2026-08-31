---
title: "Base Model RL Comparison"
type: insight
tags: [insight, base-model, rl, agentic-rl, reward, verification]
source: "[[Topics/13_base_model/Base Model MOC]]"
related:
  - "[[Topics/7_rl/RL MOC]]"
  - "[[Topics/13_base_model/Base_Model_SFT_PostTraining_Comparison]]"
created: 2026-06-12
updated: 2026-06-18
---

# Base Model RL Comparison

> [!tldr]
> 当前 Base Model 的 RL 不是一个统一问题，而是五类 failure mode 的集合：可验证任务的 sample efficiency、长轨迹 agent 的 credit assignment、多模态任务的难度采样、开放域任务的 reward construction、多域能力的 teacher interference。GRPO 是底座；CISPO/MIS-PO 改 token 更新稳定性；GRPO-RoC 改 rollout 分布；RLCS 改课程采样；Forge/Slime 改训练系统；MOPD/Expert Distillation 改多域合并；Self-Critique/PARL 则把 RL 推向开放域和并行 agent。

## 高关键对比：按 failure mode 看 RL，而不是按算法名看 RL

| Failure mode | 代表方法 | 代表模型 | 核心解决什么 | 我的判断 |
|---|---|---|---|---|
| outcome 可验证，但 RL 效率低 | GRPO / RLVR | Qwen3, Step-GUI, STEP3-VL | 不用 value model，group-relative advantage 降低复杂度 | 已是默认基线，但不是长轨迹 agent 的充分解 |
| 长推理低概率 token 被裁掉 | CISPO | MiniMax-M1/M2 | 裁 IS weight 而非 token update，保留 Wait/However/Aha 等探索 token | 对长 CoT 和 interleaved thinking 更合理 |
| 环境噪声大，正确轨迹太少 | GRPO-RoC | rStar2-Agent | 正确 rollout 后 resample，扩增正样本多样性 | 很适合代码、搜索等 flaky environment |
| 多模态任务难度分布不稳 | RLCS | GLM-4.5V | pass@k 难度分桶 + Ratio EMA，避免 all-correct/all-wrong batch | 复杂感知任务需要类似机制 |
| 长轨迹 reward 太稀疏 | Composite reward | MiniMax M2 | process + speed + performance 分解信用 | Agent RL 必备，不然只会学最终投机 |
| 开放域没有标准答案 | Self-Critique / rubric reward | Kimi K2, Step-DeepResearch | 用 rubric、critic、checklist 近似 reward | 解决开放域入口，但最容易 reward hacking |
| 多域 teacher 互相干扰 | MOPD / expert distillation | MiMo V2, GLM-4.5, Qwen3-Coder-Next | 分域训练，再合并成统一模型 | 对多能力 agent 合并最关键 |
| Agent rollout 系统瓶颈 | Forge / Slime | MiniMax M2, GLM-4.5 | 白盒/黑盒 agent、异步 rollout、FP8、数据池、sandbox | 真正的 scaling bottleneck 在 infra |
| 顺序 agent latency 太高 | PARL / Agent Swarm | Kimi K2.5 | 训练 orchestrator 动态并行子 agent | 从结构上解决 long-horizon latency |

相关来源：
- [[Topics/13_base_model/MiniMax/2506_MiniMax_M1/MiniMax-M1-Scaling-Test-Time-Compute-Lightning-Attention]]
- [[Topics/13_base_model/MiniMax/2605_MiniMax_M2_Series/MiniMax-M2-Series-Mini-Activations-Max-Real-World-Intelligence]]
- [[Topics/13_base_model/Microsoft/2508_rStar2_Agent/rStar2-Agent-Agentic-Reasoning-Technical-Report]]
- [[Topics/13_base_model/Zhipu_GLM/2507_GLM_4_5V/GLM-4.5V-Multimodal-Reasoning-RLCS]]
- [[Topics/13_base_model/Moonshot_Kimi/2507_Kimi_K2/Kimi-K2-Open-Agentic-Intelligence]]
- [[Topics/13_base_model/Moonshot_Kimi/2602_Kimi_K2_5/Kimi-K2-5-Joint-Optimization-Vision-Language]]
- [[Topics/13_base_model/Xiaomi_MiMo/MiMo-Summary-Dense]]

## 关键 insight 1：GRPO 是底座，但不是答案

GRPO 成为主流，是因为它把 PPO/RLHF 的复杂度降下来，适合 math/code 这种 outcome-verifiable 任务。但 agent 任务比 math/code 多三个问题：

1. outcome 延迟很长：几百步之后才知道失败。
2. environment 有噪声：同一个 action 可能因为网络、UI、sandbox 状态产生不同结果。
3. reward 可被钻空子：agent 会主动探索环境漏洞。

所以后续方法都在补 GRPO 的不同短板：

- CISPO 补 token-level exploration。
- GRPO-RoC 补 rollout distribution。
- RLCS 补 difficulty sampling。
- Composite reward 补 credit assignment。
- Reward hacking blocker 补环境漏洞。
- MOPD 补多域干扰。

## 关键 insight 2：多模态 RL 不是“文本 RL 加图片”

GLM-4.5V 和 STEP3-VL 都指向一个共同现象：视觉任务的 RL 增益不一定来自更长 CoT，而常常来自感知校准和搜索空间压缩。

| 文本 reasoning RL | VLM / multimodal RL |
|---|---|
| 鼓励更长、更系统的推理链 | 不一定鼓励更长，可能要更短、更准 |
| reward 多为最终答案正确 | reward 应包含空间、动作语义、状态变化 |
| KL loss 常用于稳定 | GLM-4.5V 发现 KL 可能限制 VLM 能力 |
| 难度主要是题目难 | 难度还包括视觉噪声、目标尺寸、遮挡、观测状态 |
| 错误多是推理错 | 错误可能是看错、点错、动作错、状态理解错 |

## 关键 insight 3：Agent RL 的第一性问题是 credit assignment

MiniMax M2 明确指出长轨迹可达 192K tokens、数千步 action。这个时候 outcome-only reward 几乎不可用，因为模型不知道是哪个中间决策导致成功或失败。

更合理的 reward 分解：

```text
trajectory reward
  = task success
  + process quality
  + action validity
  + verifier confidence
  + speed / token efficiency
  + safety / leakage penalty
```

这解释了为什么：

- MiniMax M2 要 composite reward。
- MiroThinker-H1 要 local/global verification。
- Qwen3-Coder-Next 要 reward hacking blocker。
- Step-DeepResearch 要 checklist-style judger。
- Kimi K2 要 self-critique rubric。

它们本质上都在把“最后对不对”拆成更可训练的中间信号。

## 关键 insight 4：多域 RL 不能直接混

MiMo 的 MOPD 很重要，因为它正面回答了一个真实工程问题：Math teacher、Agent teacher、Safety teacher、General teacher 的目标不一致，直接混 reward 会互相破坏。

这个问题在多域 agent 训练中也会出现：coding、research、tool-use、safety、general helpfulness 的 reward 目标不一致。因此更稳的路线是先分 expert teacher，再做 MOPD/Distillation 合并，而不是一开始就混一个大 reward。

## 选择 RL 方法的决策表

| 你的任务 | 首选路线 | 不建议只用 |
|---|---|---|
| math/code 单步可验证 | GRPO / RLVR | 复杂 composite reward |
| coding agent with flaky tests | GRPO-RoC + blocker | outcome-only GRPO |
| 多域 agent model | expert RL + MOPD / distillation | 所有 domain reward 直接混 |
| deep research / open-domain | rubric reward + human/judge audit | 自评 reward 单独使用 |
| parallel long tasks | PARL / Agent Swarm | 顺序 tool call 堆上下文 |

## 最短结论

RL 的关键不是“哪个 optimizer 最强”，而是“你的 failure mode 是什么”。对 agent base model 来说，最关键的不是 GRPO vs PPO 的名字，而是 reward 是否可分解、环境是否防泄漏、rollout infra 是否能规模化、多域能力是否能合并。
