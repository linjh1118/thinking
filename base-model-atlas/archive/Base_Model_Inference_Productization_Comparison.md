---
title: "Base Model Inference and Productization Comparison"
type: insight
tags: [insight, base-model, inference, productization, serving, cost, latency]
source: "[[Topics/13_base_model/Base Model MOC]]"
related:
  - "[[Topics/13_base_model/Base_Model_Architecture_Comparison]]"
  - "[[Topics/13_base_model/QA/0611_MoE_vs_Dense_Resource_Comparison]]"
created: 2026-06-12
updated: 2026-06-18
---

# Base Model Inference and Productization Comparison

> [!tldr]
> Agent 模型产品化的核心不是单 token 价格，而是 cost per solved task。长程 agent 会把所有隐藏成本放大：KV cache、tool latency、retry、sandbox、context retention、compaction、MTP acceptance、MoE 通信。MiniMax、MiMo、StepFun 的共同趋势是 model-system co-design；OpenAI/Anthropic/Google 的共同趋势是 router、thinking mode、sandbox、product scaffold。真正的产品竞争是“能力、成本、延迟、可靠性”四者的 Pareto。

## 高关键对比：推理成本不是一个数

| 成本层 | 决定因素 | 代表路线 | 对 agent 的影响 |
|---|---|---|---|
| FFN compute | active params、MoE top-k | MiniMax M2, MiMo V2, Step 3.5 | 决定每 token 基础成本 |
| Weight memory | total params、expert placement、quantization | 1T MoE、309B MoE | 决定部署卡数和并行复杂度 |
| Attention/KV | context length、KV heads、attention pattern | MiniMax M3 MSA, Kimi Linear, MiMo SWA | 决定 128K/1M 是否真可用 |
| Decode throughput | MTP、speculative decoding、batching | MiMo V2, Step 3.5, GLM-4.5 | 决定 rollout 和长回答速度 |
| Tool latency | sandbox、browser、API、interactive environment | Codex, Claude Code, MiniMax Code, OpenClaw | 常常超过模型生成时间 |
| Retry/search budget | self-debug、parallel agents、pass@k | Kimi Agent Swarm, coding agents | 分数提高但成本也提高 |
| Memory policy | full trace、summary、compaction、block sparse retrieval | MiniMax M3, GPT-Codex clipping | 决定长任务是否持续稳定 |

## Productization 路线对比

| 路线 | 代表 | 产品化赌注 | 最大风险 |
|---|---|---|---|
| 小激活大总参 | MiniMax M2, MiMo V2, Step 3.5 | 用 10B-15B active 支撑长任务低 compute | 权重显存和 MoE 通信 |
| model-system co-design | Step-3 | 用 MFA/AFD 直接优化 Hopper 解码吞吐 | 强依赖特定硬件和 serving stack |
| 长上下文成本坍缩 | MiniMax M1/M3, Kimi Linear | 让 1M context 成为 agent 基础设施 | sparse/linear recall 失败会伤可靠性 |
| MTP/spec rollout | MiMo, GLM, StepFun, MiniMax | 降低 decoding 和 on-policy RL rollout 成本 | 高熵任务 acceptance 下降 |
| Thinking router/modes | Qwen3, Seed1.8, GPT-5 clipping | 根据任务动态分配 test-time compute | router 误判会造成过度/不足思考 |
| Agent IDE/CLI ecosystem | GPT-Codex, Claude Code, MiniMax Code, Qwen Code | 用默认 scaffold 提升可用性 | 模型分数和 scaffold 强绑定 |

相关来源：
- [[Topics/13_base_model/stepfun/2507_Step_3_Large_Affordable/Step_3_Large_Affordable]]
- [[Topics/13_base_model/MiniMax/2506_MiniMax_M1/MiniMax-M1-Scaling-Test-Time-Compute-Lightning-Attention]]
- [[Topics/13_base_model/MiniMax/2606_MiniMax_M3/MiniMax-M3-Frontier-Coding-1M-Context-Native-Multimodality]]
- [[Topics/13_base_model/Xiaomi_MiMo/MiMo-Summary-Dense]]
- [[Topics/13_base_model/ByteDance_Seed/2603_Seed1_8_Model_Card/Seed18-Model-Card-Towards-Generalized-Real-World-Agency]]

## 关键 insight 1：MoE 是用显存和通信换每 token compute

参考 [[Topics/13_base_model/QA/0611_MoE_vs_Dense_Resource_Comparison]]。

MoE 的产品化判断不能只看 active params：

```text
per-token compute ~ active params
weight memory ~ total params
network cost ~ expert routing / all-to-all
KV cache ~ attention config and context length
```

所以 309B/15B active 不是“15B 部署成本”。它可能每 token 像 15B，但权重和通信像大模型。对单用户长任务，它可能很划算；对小团队本地部署，它可能很痛。

## 关键 insight 2：1M context 的价值不是读长文，而是少丢状态

Agent 长任务里，最贵的错误往往来自记忆丢失：

- 忘记早先失败过的修复。
- 忘记用户约束。
- 忘记环境状态变化。
- 忘记某个测试日志里的关键报错。
- summary 把细节压掉，导致重复犯错。

MiniMax M3、Kimi Linear、MiMo V2.5 的长上下文路线真正价值是：让系统可以从 aggressive summarization 转向 selective retrieval over full trace。

## 关键 insight 3：MTP 对 agent 比对聊天更重要

聊天模型的瓶颈通常是延迟体验；agentic RL 的瓶颈是 rollout 采样成本。

MTP/spec decoding 在 agent 中有三类收益：

1. 产品推理：长 thinking 和长报告更快。
2. Self-debug：多次尝试成本更低。
3. RL 训练：on-policy rollout 更便宜，更多环境交互成为可能。

这也是为什么 MiMo、StepFun、GLM、MiniMax 都把 MTP 或 speculative decoding 放进系统设计里。

## 关键 insight 4：产品化模型要有 compute controller

Qwen3 的 thinking budget、Seed1.8 的 thinking modes、GPT-5 clipping 中的 router，本质上都在做同一件事：给 test-time compute 加控制器。

| 控制方式 | 适合场景 | 风险 |
|---|---|---|
| 用户手动 budget | API / research user | 用户不知道该给多少 |
| 模型自动 router | consumer / ChatGPT 类产品 | router failure 不透明 |
| 多档 thinking mode | agent product / enterprise | mode 选择需要任务分类器 |
| parallel agent orchestration | long research / coding | 资源调度和结果合并复杂 |
| verifier-triggered escalation | coding / safety-critical | 需要可靠 verifier |

## 应该如何报告产品化性能

| 指标 | 解释 |
|---|---|
| cost per solved task | 最核心，比 input/output token price 更真实 |
| median / p90 wall-clock | 长任务用户体验 |
| tokens per successful trajectory | 是否靠长推理堆成功 |
| tool calls per successful trajectory | 是否靠暴力尝试 |
| failure recovery rate | 第一次失败后能否修复 |
| context retained ratio | 完整历史 vs summary |
| compaction error rate | 压缩是否丢关键约束 |
| verifier calls per task | verifier 成本 |
| sandbox overhead | 环境交互成本 |

## 最短结论

Agent base model 的产品化竞争，不是“谁模型最大”，也不是“谁 token 最便宜”。真正比较的是：

```text
solved task quality / (model compute + KV/context + tool latency + retry + verifier + memory)
```

谁能把这个分母压下来，同时不丢长任务可靠性，谁才是真正的 agent foundation model 产品化赢家。
