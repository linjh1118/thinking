---
title: "Seed1.8 Model Card: Towards Generalized Real-World Agency"
type: paper
authors: ["Bytedance Seed Team"]
year: 2026
venue: arXiv
arxiv: "2603.20633"
url: "https://arxiv.org/abs/2603.20633"
tags: [paper, bytedance, seed, agent, gui, multimodal]
topic: "13_base_model"
status: read
rating: 5
created: 2026-05-30
---

# TL;DR

Seed1.8 是 **Real-world Agency 代表模型**，核心设计目标是 **Generalized Real-World Agency**——不仅保留 LLM/VLM 能力，还扩展到多步交互和任务执行。Seed1.8 的四大设计考量：强基础能力、统一 Agentic 交互、延迟/成本感知推理、与实践对齐的评测。

## 设计理念

### 四大设计考量

1. **Strong Base Capabilities**：保持 LLM 和 VLM 的竞争性性能（reasoning、instruction following、knowledge、multimodal understanding）

2. **Unified Agentic Interface**：Search + Code Execution + GUI Interaction 在统一接口内

3. **Latency- and Cost-Aware Inference**：
   - 可配置的 **thinking modes**（no_think, think-low, think-medium, think-high）
   - 优化的 visual encoding 减少图像/视频 token 消耗

4. **Evaluation Aligned with Practical Use**：
   - 公共 benchmark + 内部高价值应用领域评测
   - 覆盖 foundation、multimodal、agentic workflows

## 核心能力

### 1. Fundamental LLM Capabilities

| 领域 | 表现 |
|------|------|
| Coding | 与 leading SOTA 竞争 |
| Mathematics | 与 leading SOTA 竞争 |
| BeyondAIME, AMO-Bench | 第二名 |
| KOR-Bench, ARC-AGI-1 | 第二名 |
| Instruction Following | Inverse IFEval 第二名 |
| Knowledge (MMLU, MMLU-pro) | 与 leading LLMs 持平 |

### 2. Vision Capabilities

**GUI Grounding 亮点**：
- ScreenSpot-Pro: **64.3** (vs Seed1.5-VL: 60.9)
- With crop-box tool: **73.1** (new SOTA)

**多模态推理**：
- ZeroBench (main): **11.0** SOTA (vs Gemini 3 Pro: 10.0)
- MMMU, MathVista, MathVision: 第二名，紧追 Gemini 3 Pro

**视频理解**：
- Motion & Perception: 5/6 tasks 达到 SOTA
- Streaming: OVBench, LiveSports-3K, OVOBench 达到 SOTA
- **Proactive response capability**：无需显式触发即可识别最优干预时机

### 3. Agentic Capabilities

**Agentic Search**：
- GAIA: **93.2** (超越 GPT-5-high: 76.7!)
- BrowseComp-en: 67.6
- BrowseComp-zh: 78.5

**GUI Agent（亮点）**：
- OSWorld: **SOTA**
- Realbench: **SOTA**
- Online-Mind2web: **SOTA**
- AndroidWorld: **SOTA**

**经济价值场景**：
- FinSearchComp (Finance): 56.2
- XpertBench Finance: 62.0
- XpertBench Law: 55.2
- WorldTravel: **Best** (multimodal setting)

### 4. Thinking Modes Efficiency

Seed1.8 支持四种 thinking modes：

| Mode | 用途 |
|------|------|
| no_think | 快速简单任务 |
| think-low | 低延迟要求 |
| think-medium | 平衡 |
| think-high | 复杂任务 |

**Token Efficiency 优势**：
- BeyondAIME, KORBench: 同等 token 使用下持续提升
- MathVision: Peak 81.3 vs Seed1.6 71.8 (+9.5%)
- Pareto frontier dominance：no_think 模式已超越 Seed1.6 的 high 模式

**多模态 Token Efficiency**：
- 32K token budget 超越 Seed1.5-VL 的 80K token budget

### 5. Agent Execution Efficiency

在 BrowseComp 上：
- Low reasoning: 45.0 @ <50 steps
- Medium reasoning: 55.0 @ <50 steps
- Unlimited: 67.6 @ 150 steps（展现 scaling behavior）

## 对研究的启发

> [!insight]
> 1. **Seed1.8 的 GAIA 93.2** 远超 GPT-5-high 的 76.7，说明国内模型在 agentic search 上已有优势
> 2. **GUI Agent 四项 SOTA** 对 GUI 研究有直接参考价值
> 3. **Proactive response capability** 值得关注——模型可以无需显式触发就判断何时干预
> 4. **Thinking modes** 的设计对 GUI Agent 的 latency/cost tradeoff 有参考
> 5. **Agent execution efficiency** 展现 scaling behavior，与 MiroThinker 的 interaction scaling 呼应

## 相关链接

- 论文: [arXiv Link](https://arxiv.org/abs/2603.20633)
