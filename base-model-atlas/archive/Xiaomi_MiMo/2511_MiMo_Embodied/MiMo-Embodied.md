---
title: "MiMo-Embodied: Advancing Cross-Domain Generalization for Embodied Intelligence and Autonomous Driving"
type: paper
authors:
  - Xiaomi LLM-Core Team
year: 2025
venue: arXiv
arxiv: "2511.16518"
doi:
url: https://arxiv.org/abs/2511.16518
tags:
  - paper
  - embodied-ai
  - autonomous-driving
  - vlm
  - spatial-reasoning
  - affordance
  - cross-domain
topic: 13_base_model
status: read
rating: 5
related:
  - "[[Topics/13_base_model/Xiaomi_MiMo/2506_MiMo_VL_7B/MiMo-VL]]"
  - "[[Topics/13_base_model/Xiaomi_MiMo/2512_MiMo_VL_Miloco_7B/MiMo-VL-Miloco]]"
  - "[[Topics/13_base_model/Xiaomi_MiMo/2606_MiMo_Series/MiMo-Series-From-7B-Reasoning-Model-to-Omnimodal-Agent-Foundation-Models]]"
created: 2026-06-11
---

# MiMo-Embodied: Cross-Domain Embodied Intelligence & Autonomous Driving

> [!tldr]
> MiMo-Embodied（XFM）是第一个把 embodied AI 和 autonomous driving 统一到单一开源 VLM 的工作。基于 MiMo-VL，四阶段渐进训练（Embodied SFT → Driving SFT → CoT SFT → GRPO RL）解决了跨域干扰问题：在 embodied tasks 上比直接混合训练高 4%，在 AD tasks 上高 8.1%。覆盖 17 个 embodied AI benchmark + 12 个 driving benchmark。

## 问题与动机

**核心问题**：Embodied AI（室内机器人）和 Autonomous Driving（户外驾驶）是两个独立发展的研究领域，但都需要"视觉感知 → 状态理解 → 行动规划"的能力。能否用一个统一的 VLM 覆盖两者？

**挑战**：
- 两个领域的视觉分布差异大（室内 vs 户外）
- 任务目标不同（affordance prediction vs 轨迹规划）
- 直接混合训练会导致负迁移

## 方法核心思路

### 1. 架构：三组件 VLM（继承自 MiMo-VL）

1. **ViT**：处理单图、多图、视频
2. **Projector（MLP）**：视觉 token → LLM latent space
3. **LLM Backbone**：从 MiMo-VL 初始化，继承 VLM 对齐和推理能力

### 2. 四阶段渐进训练

| 阶段 | 数据 | 关键目标 | Batch Size | LR |
|------|------|---------|-----------|-----|
| Stage 1 | General + Embodied AI | affordance理解、任务规划、空间推理 | 512 | 2e-6 |
| Stage 2 | + Autonomous Driving | 跨域对齐（混合监督） | 512 | 2e-6 |
| Stage 3 | + CoT Data | 带推理链的复杂推理 | 512 | 2e-6 |
| Stage 4 | RL Data | GRPO 强化学习微调 | 32 | 1e-6 |

**关键洞察**：渐进训练比直接混合训练效果好：
- Embodied tasks：62.4% avg（vs 混合 58.4%，+4%）
- AD tasks：63.3% avg（vs 混合 55.2%，+8.1%）

### 3. 能力评估体系

**17 个 Embodied AI Benchmarks**：
- Affordance Prediction（5）：Roborefit、Where2Place、VABench-Point、Part-Afford、RoboAfford-Eval
- Task Planning（3）：EgoPlan2、RoboVQA、Cosmos-Reason1
- Spatial Understanding（9）：EmbSpatial、RoboSpatial、SAT、VSI-Bench、CRPE-relation、RefSpatial-Bench、ERQA、MetaVQA、CV-Bench

**12 个 Autonomous Driving Benchmarks**：
- Perception（10）：CODA-LM、DriveAction、DRAMA、MME-RealWorld、IDKB、DriveLM、MAPLM、nuScenes-QA、LingoQA、OmniDrive
- Prediction：MME-RealWorld、DriveLM
- Planning：DriveLM、BDD-X、NAVSIM

## 实验结果

### Embodied AI（表2）

| Benchmark | MiMo-Embodied | Best Baseline | Delta |
|-----------|--------------|--------------|-------|
| VABench-Point | **SOTA** | — | large margin |
| Part-Afford | **SOTA** | — | large margin |
| RoboAfford-Eval | **SOTA** | — | large margin |
| CV-Bench | **SOTA** | — | — |
| RoboSpatial | **SOTA** | — | — |
| RefSpatial-Bench | **SOTA** | — | — |
| CRPE-relation | **SOTA** | — | — |

### Autonomous Driving（NAVSIM 表）

| Metric | Score | 对比 |
|--------|-------|------|
| NC | 97.9 | 超越 InternVL3-8B、ReCogDrive |
| DAC | 94.3 | — |
| TTC | 93.8 | — |
| EP | 81.7 | — |
| PDMS | 86.5 | — |

### Ablation Study（关键）

| 训练策略 | Embodied Avg | AD Avg |
|---------|-------------|-------|
| 单域（仅 Embodied） | 高 | 低 |
| 单域（仅 AD） | 低 | 高 |
| 直接混合 | 中等 | 中等 |
| **多阶段渐进（XFM）** | **62.4%** | **63.3%** |

**结论**：课程学习有效缓解跨域干扰，实现协同提升而不牺牲单任务性能。

## 对研究的启发

> [!insight]
> MiMo-Embodied 的核心价值不是某个单一任务 SOTA，而是证明了 **cross-domain generalization 是可行的**。这对 GUI / robotics / autonomous driving 的意义：这三个领域可能需要"视觉状态 → 行动约束 → 可验证反馈"的同构训练接口，只是 verifier 和 action space 不同。

**可转化的问题**：
- GUI Agent 和 code generation 是否有类似的跨域迁移可能？
- 多域课程学习的课程顺序如何设计？embodied → driving → code 是否可行？
- CoT 在 embodied 和 driving 任务上的作用有何不同？

## 相关资料

- arXiv：https://arxiv.org/abs/2511.16518
- 系列总览：[[Topics/13_base_model/Xiaomi_MiMo/2606_MiMo_Series/MiMo-Series-From-7B-Reasoning-Model-to-Omnimodal-Agent-Foundation-Models]]
- MiMo-VL：[[Topics/13_base_model/Xiaomi_MiMo/2506_MiMo_VL_7B/MiMo-VL]]
