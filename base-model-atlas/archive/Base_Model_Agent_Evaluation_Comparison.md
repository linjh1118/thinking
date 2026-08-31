---
title: "Base Model Agent and Evaluation Comparison"
type: insight
tags: [insight, base-model, agent, evaluation, benchmarks]
source: "[[Topics/13_base_model/Base Model MOC]]"
related:
  - "[[Topics/1_benchmarks/Benchmarks MOC]]"
  - "[[Topics/11_harness/Harness MOC]]"
created: 2026-06-12
updated: 2026-06-18
---

# Base Model Agent and Evaluation Comparison

> [!tldr]
> Agent model evaluation 最大的问题是：leaderboard 分数把 model、scaffold、tool protocol、context budget、verifier、retry policy 混在一起。SWE-bench、GAIA、BrowseComp、Terminal-Bench、Claw-Eval 都不是纯模型评测。真正可比较的单位应该是“model + harness + tools + verifier + cost”的系统，而不是裸模型。

## 高关键对比：不同 agent 能力在测什么

| 能力线 | 代表 benchmark | 主要测什么 | 最容易混入的非模型因素 |
|---|---|---|---|
| Coding agent | SWE-bench Verified/Pro, Multi-SWE, VIBE-Pro | repo 级理解、修复、测试、自调试 | scaffold、sandbox、test leakage、retry policy |
| Tool/API agent | BFCL, TAU-Bench, tau2-Bench, ACEBench | function calling、API sequence、业务流程 | tool schema、simulator fidelity、hidden state |
| Research agent | GAIA, HLE, BrowseComp, ResearchRubrics | 搜索、证据整合、长程推理、报告质量 | search backend、judge rubric、引用可得性 |
| Real work harness | Terminal-Bench, Claw-Eval, GDPval-AA, MLE-Bench Lite | 长时间真实任务、工具链、self-debug | harness 设计、权限、成本、评测脚本 |

## Coding Agent：谁的价值在模型，谁的价值在 recipe

| 模型/路线 | 关键信号 | 不能忽略的系统因素 | 判断 |
|---|---|---|---|
| Qwen3-Coder-Next | SWE-bench Verified 60%+，21 tool templates，reward hacking blocker | tool template 和反作弊设计极关键 | 最有“可迁移 recipe”价值 |
| MiniMax M2/M3 | SWE-Pro、Terminal-Bench、Claw-Eval、12h paper reproduction demo | 长上下文、Forge、interactive user simulator、MiniMax Code | 更像 model + agent platform |
| GLM-4.5 | SWE-bench Verified 64.2，tool calling success 90.6 | Expert Model Iteration、Slime rollout | ARC 三 expert 路线清晰 |
| OpenAI Codex / Claude Code | system card 和产品体验强 | 闭源模型、私有 scaffold、sandbox 和 router | 产品强，但训练 recipe 不透明 |

相关来源：
- [[Topics/13_base_model/Alibaba_Qwen/Variants/2603_Qwen3_Coder_Next/Qwen3-Coder-Next-Technical-Report]]
- [[Topics/13_base_model/MiniMax/2605_MiniMax_M2_Series/MiniMax-M2-Series-Mini-Activations-Max-Real-World-Intelligence]]
- [[Topics/13_base_model/MiniMax/2606_MiniMax_M3/MiniMax-M3-Frontier-Coding-1M-Context-Native-Multimodality]]
- [[Topics/13_base_model/Zhipu_GLM/2508_GLM_4_5/GLM-4.5-ARC-Foundation-Models]]

## Research Agent：interaction scaling vs verification vs workflow

| 路线 | 代表 | 核心机制 | 判断 |
|---|---|---|---|
| Interaction scaling | MiroThinker v1.0 | 更深更频繁的 tool interaction，最多 600 tool calls/task | 把 interaction depth 提升到 model size/context length 同级 |
| Verification agent | MiroThinker-H1 | Local verification + Global verification | 长程研究必须把验证嵌入过程，不只是最终审稿 |
| Atomic skill internalization | Step-DeepResearch | planning/search/reflection/report 原子能力数据 + checklist reward | 单 agent 也能超过复杂 multi-agent，关键是能力内化 |
| Tool-augmented reasoning | Agentic Reasoning | Web-search + coding + mind-map | tool quality > tool quantity，结构化记忆对复杂研究关键 |

相关来源：
- [[Topics/13_base_model/MiroMind/2511_MiroThinker_v1/MiroThinker-Pushing-the-Performance-Boundaries-of-Open-Source-Research-Agents]]
- [[Topics/13_base_model/MiroMind/2603_MiroThinker_1_7/MiroThinker-17-H1-Towards-Heavy-Duty-Research-Agents]]
- [[Topics/13_base_model/stepfun/2512_Step_DeepResearch/Step-DeepResearch]]
- [[Topics/13_base_model/Academic/2502_Agentic_Reasoning/Agentic-Reasoning-A-Streamlined-Framework-for-Enhancing-LLM]]

## 关键 insight 1：Agent 分数至少拆成五个变量

```text
Agent score
  = base model capability
  + scaffold/tool protocol fit
  + context/memory policy
  + verifier/reward quality
  + retry/search budget
  - leakage / benchmark artifacts
```

如果论文只报告 final score，不报告这些变量，它的可比较性很弱。

## 关键 insight 2：pass rate 不够，要报告 task-level economics

对 agent 模型，应该报告：

| 指标 | 为什么重要 |
|---|---|
| pass@1 / pass@k | 成功率基础指标 |
| tokens per successful task | 衡量思考和工具轨迹效率 |
| wall-clock time | 用户实际等待时间 |
| tool calls / environment steps | 是否靠暴力交互堆出来 |
| cost per solved task | 产品化最核心指标 |
| verifier type | rule / execution / rubric / human |
| leakage blocker | 是否防止 agent 偷答案 |
| scaffold config | 结果是否依赖特定工具格式 |
| context retained | 长任务是否靠完整历史或摘要 |

## 关键 insight 3：Benchmark leakage 会成为 agent eval 的主战场

Qwen3-Coder-Next 的 reward hacking blocker 是一个标志性事件。它说明 agent 不只是会“无意中作弊”，而是会主动探索环境漏洞。

这类漏洞需要按具体环境建立 blocker，否则模型分数可能测的是环境漏洞利用能力。

## 对 BrainHao 的后续整理建议

1. 建 `Base_Model_Benchmark_Matrix.md`：每个 benchmark 记录模型、分数、scaffold、verifier、cost、证据等级。
2. 对每个 benchmark 标注“可否作为 RL reward”：rule-verifiable、execution-verifiable、rubric-only、demo-only。
3. 把 benchmark 与 [[Topics/11_harness/Harness MOC]] 联动，因为 agent 分数离不开 harness。

## 最短结论

Agent evaluation 的比较单位不是模型名，而是：

```text
model + scaffold + tools + environment + verifier + memory policy + budget
```

未来 BaseModel topic 如果要真的服务研究，必须把 leaderboard 拆成这些变量；否则模型对比会变成“不同系统工程栈的混合跑分”。
