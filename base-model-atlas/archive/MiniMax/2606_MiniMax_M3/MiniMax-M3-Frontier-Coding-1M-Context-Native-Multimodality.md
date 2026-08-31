---
title: "MiniMax M3: Frontier Coding, 1M Context, Native Multimodality"
type: model-note
authors: ["MiniMax"]
year: 2026
venue: Official Blog
arxiv:
doi:
url: "https://www.minimax.io/blog/minimax-m3"
tags: [model-note, minimax, coding-agent, multimodal, long-context, sparse-attention]
topic: "13_base_model"
status: read
rating: 5
related: ["[[Topics/13_base_model/MiniMax/2605_MiniMax_M2_Series/MiniMax-M2-Series-Mini-Activations-Max-Real-World-Intelligence]]", "[[Topics/13_base_model/MiniMax/2606_MiniMax_M3/src/MiniMax-M3 - Official Blog]]"]
created: 2026-06-01
---

# TL;DR

MiniMax M3 是 M2 系列之后的一次架构级换代：它把 **frontier coding / agentic tasks、1M context、native multimodality** 放到同一个模型里，核心机制是 MiniMax Sparse Attention (MSA)。我对它的判断是：M3 的关键不只是“更会写代码”，而是把长上下文压到可承受成本后，让 agent 可以把论文、repo、日志、工具轨迹和截图/视频都放进一个持续工作线程里。

> [!note]
> 技术报告和权重还没同步放出。官方博客写明“未来 10 天内发布 technical report 并开源对应权重”。所以这篇先基于官方发布博客、API 文档、工具文档与第三方路由页整理，等 technical report 出来后应再更新一次。

## 问题与动机

M2 系列已经证明 MiniMax 在 agentic coding、office work、search/tool use 和 self-evolution 上很激进，但 M2 的瓶颈也很明显：长任务的上下文成本仍然高，尤其是真实 agent 工作流会快速积累代码、日志、工具结果、截图、文档、历史计划和错误轨迹。

M3 要解决的是这个更底层的问题：

- **Agent 长任务需要 1M 级上下文**：paper reproduction、repo-level coding、GUI/desktop 操作都不是 200K 内稳定解决的问题。
- **Full attention 在 1M 上不可经济地扩展**：复杂度随长度二次增长，导致长上下文 agent 即使能跑也很贵。
- **Coding agent 进入多模态阶段**：真实工作流里代码问题经常来自截图、GUI 状态、论文图表、视频或跨应用操作，而不是纯文本。
- **单轮 benchmark 不够代表真实使用**：官方特别强调 M3 训练和评测里加入 interactive user simulator，模拟持续澄清、反馈修正、任务切换和项目迭代。

## 方法核心思路

### 1. MSA：把长上下文变成可扩展维度

M3 的核心架构变化是 **MiniMax Sparse Attention (MSA)**。官方给出的直觉是：先用预筛选阶段找出相关 KV blocks，再对被选中的 blocks 做精确注意力计算。

相对 full attention，MSA 的目标不是“粗暴截断上下文”，而是让模型在 1M context 下仍能覆盖有效信息：

| 维度 | M3 / MSA 设计 |
|------|---------------|
| 上下文窗口 | 1M tokens |
| 稀疏机制 | 对 KV 分 block，先筛选再计算 |
| 对比对象 | DSA、MoBA、full attention |
| 算子优化 | KV outer gather Q，KV block 作为外层循环 |
| 1M context 成本 | per-token compute 约为上一代的 1/20 |
| 官方速度宣称 | prefill >9x，decode >15x |

我觉得这里最值得关注的是“硬件友好”这点：博客说 MSA 的 block 读取是连续内存访问，且每个 block 只读一次，在 M3 的 head configuration 下 arithmetic intensity 更好。这说明 MiniMax 不是只在算法图上做稀疏，而是在算子和 serving 侧一起做了工程闭环。

### 2. Native Multimodality：从 Step 0 混合模态训练

M3 不是后挂一个视觉 encoder 的“能看图模型”，而是从训练早期就做 mixed-modality training。官方强调 interleaved data 比他们预期更关键，也就是文本、图像等信息自然交错在同一序列中。

这对 agent 很重要：GUI/desktop 任务不是“先看一张图再回答”，而是在多轮操作中不断混合文本计划、截图状态、工具结果和文件内容。M3 支持 image/video input，并且 MiniMax Code 宣称支持 computer use。

### 3. Interactive User Simulator：训练真实协作而不是单轮解题

M3 在 coding/agent 方向的一个关键变化是引入 interactive user simulator。它模拟真实开发者在协作中的行为：

- 需求补充和澄清
- 方案讨论
- 基于反馈的修正
- 连续任务切换
- 复杂项目迭代

这和 M2 的 Forge / agentic RL 一脉相承，但重心更贴近“人和 agent 长期共事”。如果 M2 是让模型会跑复杂任务，M3 试图让模型更像一个能持续协作的开发伙伴。

### 4. Tool Use & Interleaved Thinking：保留完整推理状态

MiniMax API 文档明确说，M3 natively supports Interleaved Thinking：每轮 tool use 前，模型会基于当前环境和工具输出继续反思再决定下一步。

对开发者最关键的实现细节是：**多轮工具调用时必须把 assistant 的完整 response 追加回历史**，包括 thinking / reasoning_details / tool_calls。否则会打断 M3 的 reasoning chain。

这和 M2 笔记里的 interleaved thinking 很一致，只是 M3 文档把它变成了 API 使用原则：

| API 格式 | 关键做法 |
|----------|----------|
| Anthropic-compatible | append 完整 `response.content`，包括 thinking/text/tool_use blocks |
| OpenAI-compatible | 推荐 `reasoning_split=True`，并把 `reasoning_details` 原样放回历史 |
| Native OpenAI format | thinking 会注入 content，需要完整保留，不要手动裁剪 |

## 关键结果

### 官方主张

官方博客称 M3 在 SWE-Bench Pro 上超过 GPT-5.5 和 Gemini 3.1 Pro、接近 Opus 4.7；在 SVG-Bench 上超过 Opus 4.7；在 OmniDocBench 上超过 Gemini 3.1 Pro；在 Claw-Eval 上取得最高分。

明确列出的 coding/agent 指标：

| Benchmark | M3 |
|-----------|----|
| SWE-Bench Pro | 59.0% |
| Terminal-Bench 2.1 | 66.0% |
| SWE-fficiency | 34.8% |
| KernelBench Hard | 28.8% |
| MCP Atlas | 74.2% |

### Real-world task demos

| 任务 | M3 表现 | 我怎么看 |
|------|---------|----------|
| 论文复现 | 近 12 小时自主运行，18 commits，23 experimental figures，复现核心实验趋势 | 这是 long-context + coding + multimodal 的组合验证，比单纯 SWE 分数更能说明 agent 能力 |
| FP8 GEMM kernel 优化 | 24 小时、147 benchmark submissions、1,959 tool calls；Hopper FP8 peak utilization 从 7.6% 到 71.3%，9.4x speedup | 关键不是一次写对，而是能熬过 plateau，持续试错到第 145 次才找到最好方案 |
| PostTrainBench | 12 小时内自主完成 data synthesis → training → evaluation → iteration；得分 0.37，略低于 Opus 4.7 和 GPT-5.5 | 这是 M2.7 self-evolution 路线的延续，但任务更接近“训练模型”本身 |

### 多模态 / GUI 相关

官方评测方法里提到：

- OSWorld-Verified：361 samples，M3 使用 0-1000 相对坐标、1920x1080 image resolution、Max Steps = 200；Max Steps 从 100 到 200 时完成率从 68.70% 到 70.06%。
- Video-MME：M3 在 512 frames 设置下得分 84.6。
- VideoMMMU、MMMU Pro、OmniDocBench 均列入评测方法。

这些信息对 GUI Agent 方向非常重要：M3 是 MiniMax 第一次把 multimodal + computer use + long-context agent 放在同一个旗舰叙事里。

## 对研究的启发

> [!insight]
> M3 对 GUI Agent / RL Infra 最有价值的启发是：**长上下文不是附加能力，而是 agent 训练与执行的基础设施能力**。如果上下文成本降到上一代的 1/20，agent 就可以保留更多截图、DOM/AX tree、工具日志、失败轨迹和 self-reflection，而不是依赖激进压缩。对 GUI RL 来说，这可能改变 verifier、trajectory replay、失败样本再训练的设计空间。

具体可转化为几个研究问题：

- GUI agent 的 state history 是否应该从“摘要记忆”回到“完整轨迹 + 稀疏检索式注意力”？
- MSA 类 sparse attention 是否能显著降低 GUI long-horizon rollout 的 serving 成本？
- Interleaved Thinking 的完整保留是否比“只保留最终 action”更利于 RL credit assignment？
- OSWorld 这类 benchmark 中，Max Steps 提升带来的收益是否说明 M3 更擅长长链恢复，而不是单步 grounding？

## 与 M2 系列的关系

M2 系列的核心是“mini activations + agentic RL + self-evolution”；M3 的核心是“让这些 agent 能力在 1M context 和多模态输入下继续扩展”。

| 维度 | M2 系列 | M3 |
|------|---------|----|
| 主线 | 小激活 MoE + agentic RL + Forge | MSA + 1M context + native multimodality |
| 代表能力 | coding / office / search / self-evolution | frontier coding / computer use / multimodal agent |
| 上下文 | 约 192K/204.8K | 1M |
| 训练强调 | real-world environments, composite reward | interactive user simulator, interleaved multimodal data |
| 开源状态 | M2 系列已开源/技术报告已出 | 官方称 technical report 和 weights 10 天内发布 |

## 相关资料

- 官方博客剪藏：[[Topics/13_base_model/MiniMax/2606_MiniMax_M3/src/MiniMax-M3 - Official Blog]]
- AI Coding Tools 文档：待补剪藏
- Tool Use & Interleaved Thinking 文档：待补剪藏
- M2 系列笔记：[[Topics/13_base_model/MiniMax/2605_MiniMax_M2_Series/MiniMax-M2-Series-Mini-Activations-Max-Real-World-Intelligence]]
- Vercel AI Gateway：[MiniMax M3 on AI Gateway](https://vercel.com/changelog/minimax-m3-on-ai-gateway)
- OpenRouter：[MiniMax M3 model page](https://openrouter.ai/minimax/minimax-m3)

## 待更新

- [ ] 技术报告发布后补充完整架构、训练数据、RL 配方、ablation。
- [ ] 权重开源后补充 Hugging Face / GitHub 链接和本地部署条件。
- [ ] 等第三方 coding harness 实测出来后，校准官方 benchmark 与真实使用差距。
- [ ] 单独整理 MSA 与 DeepSeek DSA / NSA / MoBA / Kimi Linear 的架构对比。
