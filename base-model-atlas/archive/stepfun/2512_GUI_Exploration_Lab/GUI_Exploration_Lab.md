---
title: "GUI Exploration Lab: Enhancing Screen Navigation in Agents via Multi-Turn Reinforcement Learning"
type: paper
authors: ["Haolong Yan", "Yeqing Shen", "Xin Huang", "Jia Wang", "Kaijun Tan", "Zhixuan Liang", "Hongxin Li", "Zheng Ge", "Osamu Yoshie", "Si Li", "Xiangyu Zhang", "Daxin Jiang"]
year: 2025
venue: arXiv
arxiv: "2512.02423"
tags: [paper, gui-agent, rl, navigation, simulation]
topic: "13_base_model"
status: read
rating: 5
created: 2026-06-12
related: []
---

> [!tldr]
> GUI Exploration Lab (GE-Lab) 提出 GUI Agent 导航的三阶段训练范式：SFT 记忆基础知识 → ST-RL 提升 OOD 泛化 → MT-RL 发展探索策略。MT-RL 在 AndroidWorld 交互 benchmark 达到 Pass@1 17.47%、Pass@5 25.16%（最高），且持续训练后迁移到真实世界 benchmark 同样最优。

## 问题与动机

当前 GUI Agent 的核心瓶颈已从 grounding（选择正确图标）转移到 **screen navigation**（理解导航图、点击正确图标到达目标页面）。

真实世界 GUI 平台（PC 软件、手机 App）复杂且封闭，难以获取训练所需的完整环境信息和页面跳转图。现有方法：
- **SFT**：需要大量专家轨迹数据，泛化差
- **ST-RL（如 DPO/GRPO）**：依赖人工标注和规则化 reward 工程

## 方法核心

### GE-Lab 仿真引擎

- **树状导航图**：节点=页面，边=点击图标后的跳转
- **合成图标**：从互联网收集、随机命名，防止模型利用先验知识
- **完全可观测**：元数据支持任意页面间低成本轨迹合成

### 三阶段训练范式

```
SFT → ST-RL (GRPO) → MT-RL (GRPO)
记忆基础   单步纠正     多轮探索
```

#### SFT
- 使用 Edge + Path 数据训练
- 记忆页面跳转模式，提供基础导航知识

#### ST-RL (GRPO)
- 4-component 规则化 reward：Action Type / Coordinate Accuracy / Intent Matching / Format
- 基于预构建轨迹的单步动作纠正

#### MT-RL (GRPO)
- 多轮在线交互 rollout
- A2B reward（到达目标页面 +1，否则 0）
- 探索策略 + 回溯机制

### Reward Hacking 应对

MT-RL 发现 reward hacking：模型倾向选择 "complete" 而非真正学习点击序列。解决方案：减少 action space 多样性，让模型专注于核心 click 动作。

## 关键实验数据

### ID / OOD / Interactive Benchmark

| Model | ID Overall | OOD Overall | Int. Pass@1 | Int. Pass@5 |
|-------|-----------|------------|------------|------------|
| GPT-4o (non-ft) | - | 25.85% | 1.74% | 2.49% |
| Qwen2.5-VL-7B-SFT | 98.89% | 55.45% | 14.30% | 20.86% |
| Qwen2.5-VL-7B-ST-RL | 97.63% | 63.06% | 17.22% | 22.34% |
| **Qwen2.5-VL-7B-MT-RL** | 67.33% | **63.25%** | **17.47%** | **25.16%** |

### 真实世界 Benchmark（持续训练后）

| Model | Average (8 benchmarks) |
|-------|----------------------|
| Base | 67.15% |
| SFT-Continue-Train | 70.87% |
| ST-RL-Continue-Train | 70.92% |
| **MT-RL-Continue-Train** | **72.03%** |

> [!insight]
> MT-RL 在 ID 上低于 ST-RL（67.33% vs 97.63%），但在 OOD 和交互 benchmark 上相当或更好。说明 MT-RL 避免了过拟合训练分布，发展了更 generalizable 的导航策略。

> [!insight]
> 过多 SFT 损害 RL 效果——早期 SFT epoch（epoch 1）初始化 RL 达到最高 reward。启示：SFT 要适度，保留多样性，避免 plasticity 丧失。

## 研究启发

1. **仿真 → 真实迁移是可行的**：GE-Lab 训练的 agent 在真实世界 benchmark 上同样表现最优
2. **SFT 是必要的但需适度**：SFT 记忆基础 + RL 泛化是标准范式，但 SFT 过度会损害 RL
3. **MT-RL 的交互训练最接近真实场景**：比大量单轮 sampling 更高效
4. **OOG 环境设计决定研究质量**：合成图标的随机命名设计是防止模型作弊的关键
