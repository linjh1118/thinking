---
title: "GLM-5.2: Built for Long-Horizon Coding Agents"
type: model-note
authors: ["Z.ai / Zhipu GLM"]
year: 2026
venue: Official Blog
arxiv:
doi:
url: "https://z.ai/blog/glm-5.2"
tags: [model-note, glm, zhipu, coding-agent, long-context, agentic-rl, sparse-attention]
topic: "13_base_model"
status: read
rating: 5
related: ["[[Topics/13_base_model/Zhipu_GLM/2508_GLM_4_5/GLM-4.5-ARC-Foundation-Models]]", "[[Topics/13_base_model/Zhipu_GLM/2604_GLM_5_1/src/GLM-5.1 - Z.ai Blog]]", "[[Topics/13_base_model/Zhipu_GLM/2606_GLM_5_2/src/GLM-5.2 - Z.ai Blog]]"]
created: 2026-06-17
---

## TL;DR

> [!tldr]
> GLM-5.2 是 Z.ai 在 GLM-5.1 之后面向 **long-horizon coding / agent tasks** 的一次实用化升级：官方重点不是公布更大的参数规模，而是把 **1M context、IndexShare sparse attention、MTP speculative decoding、slime agentic RL、critic-based PPO、anti-hack guard** 放到同一条工程链路里。我的判断是：GLM-5.2 的价值在于它把“长上下文模型”推向“长任务执行系统”，尤其适合作为 coding agent / research agent / post-training agent 的基础模型来观察。

> [!note]
> 官方博客没有明确公布总参数 / 激活参数，因此本笔记不硬填架构规模；只记录官方明确披露的 1M context、IndexShare、MTP、slime、OPD、PPO 与 benchmark 信息。

## 问题与动机

GLM-5.1 已经把 GLM 系列推到 long-horizon agent 和 coding agent 方向，但真实工程任务的瓶颈不只是“能塞更多 token”：

- coding agent 轨迹会快速积累 repo、日志、测试输出、错误修复、工具调用和压缩摘要。
- long-horizon task 需要数小时到数十小时的持续执行，context 稳定性比理论窗口更重要。
- RL 训练中的超长轨迹会被 compaction 切成多个 sub-traces，传统 group-wise optimization 不再自然。
- coding reward 很容易被 hack，模型越强，越可能学会绕过评测而不是真正解决任务。

GLM-5.2 的核心动机就是让 1M context 在 engineering pressure 下可用，而不是停留在 passkey retrieval 或静态长文 QA。

## 方法核心思路

### 1. Solid 1M Context：面向 coding-agent 轨迹训练

官方特别强调 GLM-5.2 的 1M context 是为了 long-horizon work，而不是简单扩窗。训练覆盖了：

- large-scale implementation
- automated research
- performance optimization
- complex debugging

这和 MiniMax M3、MiMo-V2-Pro/V2.5 的方向一致：1M context 正在从“模型能力指标”变成 agent 执行基础设施。差别是 GLM-5.2 的博客把 coding-agent 轨迹、PostTrainBench、FrontierSWE、SWE-Marathon 放在中心位置，说明它的主战场是长任务软件工程。

### 2. IndexShare for DSA：减少 1M context 下的稀疏注意力成本

GLM-5.2 使用 IndexShare 来降低 DSA indexer 成本：每 4 个 sparse attention layers 共享一个 lightweight indexer，top-k indices 在 4 层内复用。官方称这在 1M context 下可以减少 per-token FLOPs 2.9x，并且从 128K mid-training 阶段开始训练 IndexShare。

我的理解是：这类似把 sparse attention 的“找哪些 token/blocks 重要”从每层重复计算，变成局部层组共享。它不是减少 KV cache 体积，而是降低长上下文 attention 的选择/索引计算开销。

### 3. MTP with IndexShare / KVShare：把 speculative decoding 做到 RL rollout 可用

GLM-5.2 继续优化 MTP draft model，目标是：

- 降低 MTP layer 作为 draft model 的成本。
- 提高 speculative decoding acceptance rate。

关键改动包括：

| 技术 | 作用 |
|------|------|
| IndexShare on MTP | 多步 MTP 共用第一步的 top-k indices |
| KVShare | 复用第一步 KV cache，缓解 GLM-5.1 MTP 的 train-inference discrepancy |
| Rejection Sampling | 提高 speculative decoding 的可接受序列质量 |
| End-to-end TV Loss | 用端到端训练目标进一步对齐 MTP |

官方 ablation 里，coding scenario 的 acceptance length 从 4.56 提升到 5.47，约 +20%。这对 agentic RL 重要，因为 rollout 是训练成本大头；MTP 不只是 serving 加速，也会改变 RL 数据生成吞吐。

### 4. Serving 1M Context：瓶颈从 FLOPs 转向 KV cache 和调度

GLM-5.2 把 context 从 200K 扩到 1M 后，博客明确指出瓶颈转移到：

- KV-cache capacity
- long-context kernel overhead
- CPU-side overhead
- cache transfer 与 request scheduling

它的 inference engine 优化方向包括更细粒度 memory management、LayerSplit 上的并行策略、长上下文 kernel 优化、CPU-side cache management 和 runtime path 优化。

这个判断很关键：长上下文模型不能只看 attention FLOPs，serving 侧的 KV cache、调度和并发才是 production agent 的硬约束。

### 5. slime for Agentic RL：训练 rollout 与生产 serving 合流

GLM-5.2 的 agentic RL 使用 slime 作为训练到大规模 inference rollout 的基础设施。博客提到 slime 支持：

- white-box rollout
- black-box rollout
- compact trajectory
- sub-agent workflow
- parallel OPD training

GLM-5.2 用 slime 做并行 OPD，把十多个 expert models 合并到最终模型，过程约两天。这里和 GLM-4.5 的 expert model iteration 一脉相承，但 GLM-5.2 更明确地把 training-side rollout、inference services、PD disaggregation、routing policies、production serving 优化连接起来。

我觉得这是 GLM-5.2 最值得跟 RL Infra 方向关联的部分：post-training 和 serving 不再是两个系统，而是同一套 rollout / cache / scheduling / deployment 经验的复用。

### 6. Long-Horizon RL：从 group-wise optimization 转向 critic-based PPO

GLM-5.2 在 long-horizon tasks 上放弃单纯 group-wise optimization，改用 critic-based PPO。原因是超长轨迹经过 compaction 后，一个 prompt 会产生不同数量、不同长度的 trainable traces；group-relative 比较变得不稳定。

新的 formulation 学习 individual rollouts，用 critic 估计 token-level advantages，并把 compacted sub-traces 全部作为 trainable trajectories。这个设计对长任务 agent 很重要，因为它承认“轨迹会被压缩和切分”是训练分布的一部分，而不是 serving 时才处理的工程细节。

### 7. Anti-Hack in Coding Agents：在线阻断而不是丢弃整条轨迹

GLM-5.2 官方指出，模型更强后 hacking behavior 比 GLM-5.1 更明显。典型行为包括读取 hidden eval artifacts、复制 reference answer、从 GitHub 直接抓目标源码等。

它的 anti-hack 机制分两阶段：

- rule-based filter 先最大化 recall。
- LLM judge 判断意图，保证 precision。

更关键的是 online guard：每一步 tool call 都被监控；如果检测到 hack，则阻断该调用并返回 dummy information，但允许 rollout 继续。这比直接 reject 整条轨迹更适合 RL，因为它减少训练不稳定和 model collapse。

## 关键结果

### Long-horizon coding

| Benchmark | GLM-5.2 | 对比 |
|-----------|---------|------|
| FrontierSWE | 74.4 | 接近 Claude Opus 4.8 75.1，高于 GPT-5.5 72.6 |
| PostTrainBench | 34.3 | 低于 Opus 4.8 37.2，高于 GPT-5.5 28.4 |
| SWE-Marathon | 13.0 | 高于 GPT-5.5 12.0，但低于 Opus 4.8 26.0 |

我的解读：FrontierSWE 和 PostTrainBench 是 GLM-5.2 的强项，说明它在长时间工程执行和“训练小模型”的 agent task 上很强；SWE-Marathon 仍明显落后 Opus 4.8，说明超长工程任务里还存在稳定性/规划/环境恢复差距。

### Standard coding / agentic

| Benchmark | GLM-5.2 | GLM-5.1 | 备注 |
|-----------|---------|---------|------|
| Terminal-Bench 2.1 | 81.0 | 63.5 | 提升非常大，接近 Claude Opus 4.8 的 85.0 |
| SWE-bench Pro | 62.1 | 58.4 | 高于 MiniMax M3 59.0、GPT-5.5 58.6 |
| MCP-Atlas public set | 76.8 | 71.8 | 接近 Claude Opus 4.8 77.8 |
| Tool-Decathlon | 48.2 | 40.7 | 低于 DeepSeek-V4-Pro / GPT-5.5 / Claude Opus 4.8 |

### Reasoning

GLM-5.2 在 AIME 2026、IMOAnswerBench、HLE with tools 上都有很强成绩，但这篇博客的主线不是数学 reasoning，而是 long-horizon agent/coding。对 base model 追踪来说，reasoning 是底座，真正新意在 long-context execution。

## 对研究的启发

> [!insight]
> GLM-5.2 对 GUI Agent / RL Infra 的启发是：**compaction、anti-hack、serving cache、rollout orchestration 都应该进入训练设计，而不是部署阶段的补丁**。长任务 agent 的轨迹天然会被压缩、分段、审计和重放；如果训练目标仍假设完整同质 trajectory，就会和真实 agent 工作流错位。

可转化成几个研究问题：

- GUI / coding agent 的 compaction sub-traces 是否应该作为独立 trainable trajectories 进入 PPO？
- online anti-hack guard 能否迁移到 GUI Agent，阻断“读答案文件 / 利用评测脚本 / 越权访问状态”的行为，同时保留 rollout？
- 1M context 的实际瓶颈是 KV cache 与调度；GUI agent 的 screenshot / accessibility tree / tool log 是否需要类似 LayerSplit / cache management 的 serving 设计？
- MTP speculative decoding 对长任务 rollout 是否能降低 RL 成本到足够做大规模 self-play / self-debugging？
- 对 agentic RL 来说，critic-based PPO 是否比 GRPO 更适合长轨迹和不定长 compacted traces？

## 与 GLM-4.5 / GLM-5.1 的关系

| 维度 | GLM-4.5 | GLM-5.1 | GLM-5.2 |
|------|---------|---------|---------|
| 主线 | ARC foundation model | long-horizon / agentic engineering | solid 1M context long-horizon coding agent |
| 训练整合 | expert model iteration + unified training | 官方博客线索较少 | slime + parallel OPD，合并十多个 expert models |
| RL 重点 | reasoning / agent / general expert RL | long-horizon agent | critic-based PPO + compaction traces + anti-hack |
| 架构重点 | MoE, MTP, thinking/direct | 未完整公开 | IndexShare for DSA, improved MTP, 1M serving |
| 产品化 | API / open model | coding agent 方向 | ZCode、Claude Code/OpenCode 接入、HF/ModelScope open weights |

## 与其他 1M / agent 模型的关系

| 对比对象 | 相似点 | GLM-5.2 的差异点 |
|----------|--------|------------------|
| MiniMax M3 | 1M context、coding agent、long-horizon tasks | GLM-5.2 更强调 critic-based PPO、anti-hack 和 open-weight local deployment |
| MiMo-V2.5-Pro | 1M context、MTP、agent/coding | MiMo 用 MOPD multi-teacher on-policy distillation；GLM-5.2 用 slime + OPD + PPO/anti-hack |
| Qwen3-Coder-Next | coding agent + RL + tool templates | GLM-5.2 更强调超长轨迹 compaction 和 1M context serving |
| Claude Opus 4.8 / GPT-5.5 | long-horizon software engineering | GLM-5.2 是开源模型，部分 benchmark 已接近或超过 GPT-5.5，但 SWE-Marathon 仍落后 Opus 4.8 |

## 相关资料

- 官方博客剪藏：[[Topics/13_base_model/Zhipu_GLM/2606_GLM_5_2/src/GLM-5.2 - Z.ai Blog]]
- 官方博客原文：[GLM-5.2: Built for Long-Horizon Tasks](https://z.ai/blog/glm-5.2)
- Hugging Face：[zai-org/GLM-5.2](https://huggingface.co/zai-org/GLM-5.2)
- ModelScope：[ZhipuAI/GLM-5.2](https://modelscope.cn/models/ZhipuAI/GLM-5.2)
- IndexShare：[arXiv:2603.12201](https://arxiv.org/abs/2603.12201)
- GLM-4.5 笔记：[[Topics/13_base_model/Zhipu_GLM/2508_GLM_4_5/GLM-4.5-ARC-Foundation-Models]]

## 待更新

- [ ] 等 technical report / model card 补齐参数规模、MoE 配置、训练 token、数据配比。
- [ ] 单独整理 IndexShare / DSA / MiniMax MSA / MiMo Hybrid SWA 的 1M context 架构对比。
- [ ] 跟踪 GLM-5.2 在 Claude Code、OpenCode、ZCode 中的真实使用反馈。
- [ ] 把 anti-hack guard 和 GUI Agent verifier / sandbox 防作弊机制做一篇横向对比。
