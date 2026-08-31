---
title: "Gemini Robotics 1.5: Pushing the Frontier of Generalist Robots with Advanced Embodied Reasoning, Thinking, and Motion Transfer"
type: paper
authors: ["Gemini Robotics Team, Google DeepMind"]
year: 2025
venue: arXiv
arxiv: "2510.03342"
url: "https://arxiv.org/abs/2510.03342"
tags: [paper, gemini, robotics, embodied-reasoning, vla]
topic: "13_base_model"
status: read
rating: 5
created: 2026-05-30
---

# TL;DR

Gemini Robotics 1.5 是 Google 面向机器人领域的 VLA（Vision-Language-Action）模型家族，包含两个核心创新：(1) **Gemini Robotics 1.5 (GR-1.5)**：多本体 Motion Transfer 机制 + Thinking VLA，实现零样本跨机器人技能迁移；(2) **Gemini Robotics-ER 1.5 (GR-ER 1.5)**：具身推理模型，在空间理解、指向、进度检测等任务上达到 SoTA。两者结合构成完整的机器人 agentic 系统。

## 问题与动机

真正的通用机器人需要：
1. **深度理解物理世界**：空间推理、时间推理、直觉物理、因果关系、 affordances
2. **高级推理能力**：分解复杂多步任务、在执行中调整计划
3. **泛化能力**：跨不同机器人形态（本体）工作，无需针对每个机器人单独微调

Gemini Robotics 1.0 已经奠定了基础，但存在局限：缺乏显式的思考能力、跨本体泛化有限。1.5 版本的核心动机是：**将 Gemini 的 Thinking 能力带入物理世界**。

## 方法核心思路

### 1. Gemini Robotics 1.5 (GR-1.5) — Thinking VLA

#### Motion Transfer (MT) 机制

核心创新：让模型从异构、多本体的机器人数据中学习，形成统一的运动和物理理解。

- **多本体预训练**：在 ALOHA、Bi-arm Franka、Apollo 人形机器人等多种形态上联合训练
- **零样本技能迁移**：在一个机器人上训练，可以零样本迁移到另一个机器人
- **MT 放大正迁移**：对齐不同本体间的共性，提升跨本体学习效果

#### Thinking VLA

将思考与动作交织，自然语言形式的多层内部推理过程：

```
观察 → 思考（语言） → 动作 → 观察 → 思考 → 动作 ...
```

关键能力：
- **分解复杂任务**：将高层指令转化为具体短视距步骤
- **自我纠正**：检测失败后自动提出恢复行为
- **可解释性**：可视化机器人的思考轨迹，增强人机信任
- **情境感知**：隐式感知子任务成功（如抓住球后自动切换目标）

### 2. Gemini Robotics-ER 1.5 (GR-ER 1.5) — Embodied Reasoning Model

专用于具身推理的 VLM，基于 Gemini 的 Thinking 和多模态能力：

- **Complex Pointing**：预测点集而非单个点，可生成运动轨迹和路径
- **Progress Understanding**：预测任务完成百分比、检测成功/失败
- **多视角理解**：综合多个相机视角进行判断

### 3. Agentic Framework

将 GR-1.5 和 GR-ER 1.5 组合成完整系统：

1. **用户对话**：自然语言交互
2. **高层推理与规划**：GR-ER 1.5 提供具身推理
3. **工具使用**：Gemini 原生的网页搜索等能力
4. **低层动作控制**：GR-1.5 的 VLA 输出

## 关键结果

### GR-1.5 多本体泛化

在 230 个任务的 benchmark 上，GR-1.5 在四种泛化维度上显著优于 baselines：

| 泛化类型 | 描述 | 提升效果 |
|----------|------|----------|
| Visual Generalization | 抗背景、光照、纹理变化 | +显著 |
| Instruction Generalization | 理解同义改写、多语言、模糊指令 | +显著 |
| Action Generalization | 适应新初始条件或物体实例 | +显著 |
| Task Generalization | 新环境新任务（最综合） | +显著 |

### 跨本体零样本迁移

- ALOHA → Bi-arm Franka：**成功执行仅在 Franka 数据上训练的任务**
- Bi-arm Franka → ALOHA：**成功执行仅在 ALOHA 数据上训练的任务**
- 其他机器人 → Apollo 人形：**尽管形态差异巨大，仍有迁移效果**

MT 机制的有效性取决于：
- 数据充足的平台（ALOHA）：MT 主要起对齐和提取共性作用
- 数据中等的平台（Bi-arm Franka）：MT 显著放大跨本体数据的正迁移
- 数据稀缺的平台（人形机器人）：跨本体数据带来最大提升，但 MT 效果相对有限

### Thinking VLA 的效果

在多步任务（如"按颜色分类衣物"）上：
- **启用 Thinking**：显著更高的 progress score
- **两阶段分解**：
  1. 生成语言思考轨迹（将复杂任务转化为短视距步骤）
  2. 将语言命令直接映射到机器人动作

### GR-ER 1.5 的具身推理性能

#### Complex Pointing (SoTA)

在 5 个学术 benchmark 上，GR-ER 1.5 显著优于 GR-ER 1.0、Gemini 2.5、GPT-5：

- **Average Pointing**: 新 SoTA
- **Spatial Pointing**: 空间推理指向（如"指向杯子左侧的空间"）
- **Steerable Pointing**: 根据指令修改点的位置
- **Point-to-Count**: 用点作为中间步骤进行计数

#### Success Detection (进度理解)

| 设置 | GR-ER 1.5 性能 |
|------|----------------|
| Real-time (5Hz) + Multi-view | 强 |
| Real-time (5Hz) + Single-view | 强 |
| Offline + Multi-view | 强 |
| Offline + Single-view | 强 |

#### Thinking Scaling

GR-ER 1.5 展示出 Thinking 在具身推理任务上的 scaling 能力：

- **图像/视频 QA 任务**：受益于更长的思考轨迹（峰值 3072 tokens）
- **指向任务**：所需推理较少（峰值 2048 tokens）
- **自动调节**：给定相同思考预算，模型自动为不同任务分配合适的思考量

## 对研究的启发

> [!insight]
> 1. **Thinking VLA 是未来方向**：将 Thinking 与动作交织是处理复杂多步机器人任务的有效方法。GUI Agent 可以借鉴这种"思考后行动"的范式。
>
> 2. **多本体学习的价值**：跨本体数据 + Motion Transfer 机制可以显著提升泛化能力。对于 GUI Agent，这意味着跨不同环境/应用的学习可能带来类似的正迁移。
>
> 3. **具身推理是通用 agent 的关键**：GR-ER 1.5 展示了视觉-空间-时间理解对于物理世界任务的重要性。类似地，GUI Agent 需要对屏幕空间、UI 元素空间关系的深度理解。
>
> 4. **工具使用 + 具身推理的结合**：Gemini 的工具使用能力与具身推理结合，为构建能在物理世界和信息世界自由操作的通用 agent 奠定了基础。

## 相关链接

- 论文: [arXiv 2510.03342](https://arxiv.org/abs/2510.03342)
- 源码: LaTeX 源码位于 `2510_Gemini_Robotics_1_5/src/`
