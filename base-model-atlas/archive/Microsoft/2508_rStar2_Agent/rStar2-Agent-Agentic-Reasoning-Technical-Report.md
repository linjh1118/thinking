---
title: "rStar2-Agent: Agentic Reasoning with GRPO-RoC"
type: paper
authors: ["Microsoft Research"]
year: 2025
venue: arXiv
arxiv: "2508.20722"
url: "https://arxiv.org/abs/2508.20722"
tags: [paper, microsoft, agentic-rl, grpo, coding]
topic: "13_base_model"
status: read
rating: 5
created: 2026-05-30
---

# TL;DR

rStar2-Agent 是 **Agent RL 代表工作**，核心创新是 **GRPO-RoC**（Agentic RL algorithm with Resample-on-Correct rollout strategy），在 64 MI300X GPUs 上仅用 510 RL steps 就能将 14B 模型提升到 SOTA 数学推理（AIME24: 80.6%, AIME25: 69.8%），超越 DeepSeek-R1 (671B)。

## 问题与动机

### Agentic RL 的挑战

1. **High rollout costs**：Agent 任务需要多次环境交互，GPU 消耗大
2. **Environment noises**：Coding tool 的固有噪声影响训练稳定性
3. **训练效率**：如何在有限资源下实现高效 RL

## 方法核心思路

### 1. 高效 RL Infrastructure

- 支持高吞吐量的 Python code execution
- 缓解高 rollout costs
- 仅需 **64 MI300X GPUs**

### 2. GRPO-RoC Algorithm

**核心创新：Resample-on-Correct rollout strategy**

- 解决 coding tool 环境固有噪声问题
- 当 rollout 产生正确结果时，重新采样多个轨迹
- 增加正样本的多样性，提高训练稳定性

### 3. 高效 Agent Training Recipe

关键发现：**从 non-reasoning SFT 开始**

1. Non-reasoning SFT（不用 thinking model）
2. Multi-RL stages（多阶段强化学习）
3. → 用最少计算成本获得 advanced cognitive abilities

### 4. Cognitive Behaviors 涌现

模型展现出 advanced cognitive behaviors：
- **Think carefully before using Python coding tools**
- **Reflect on code execution feedback**
- **Autonomously explore, verify, and refine intermediate steps**

## 关键结果

| Model | AIME24 | AIME25 | HMMT25 |
|--------|--------|--------|--------|
| OpenAI o3-mini (medium) | 79.6 | 77.0 | 53.0 |
| DeepSeek-R1 (671B) | 79.8 | 70.0 | 44.4 |
| Claude-Opus-4.0 (Think) | 76.0 | 69.2 | - |
| QWQ-32B | 79.5 | 65.8 | 47.5 |
| **rStar2-14B** | **80.6** | **69.8** | **52.7** |

**仅 510 RL steps，仅 14B 参数，超越 671B 的 DeepSeek-R1**

## 对研究的启发

> [!insight]
> 1. **GRPO-RoC** 的 Resample-on-Correct 策略对 GUI Agent RL 训练有直接参考价值
> 2. **Non-reasoning SFT → Multi-RL** 的训练范式可能是高效训练的关键
> 3. 14B 模型能达到 SOTA 说明模型规模不是唯一因素，训练 recipe 同样重要
> 4. 对齐、科学推理、Agentic tool-use 都有泛化，说明底层能力可迁移

## 相关链接

- 论文: [arXiv Link](https://arxiv.org/abs/2508.20722)
- GitHub: [microsoft/rStar](https://github.com/microsoft/rStar)
