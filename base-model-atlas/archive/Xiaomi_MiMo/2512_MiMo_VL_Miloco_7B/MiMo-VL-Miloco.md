---
title: Xiaomi MiMo-VL-Miloco Technical Report
type: paper
authors:
  - Xiaomi LLM-Core Team
year: 2025
venue: arXiv
arxiv: "2512.17436"
doi:
url: https://arxiv.org/abs/2512.17436
tags:
  - paper
  - smart-home
  - vision-language-model
  - edge-deployment
  - grpo
  - gesture-recognition
  - activity-recognition
topic: 13_base_model
status: read
rating: 4
related:
  - "[[Topics/13_base_model/Xiaomi_MiMo/2506_MiMo_VL_7B/MiMo-VL]]"
  - "[[Topics/13_base_model/Xiaomi_MiMo/2511_MiMo_Embodied/MiMo-Embodied]]"
  - "[[Topics/13_base_model/Xiaomi_MiMo/2606_MiMo_Series/MiMo-Series-From-7B-Reasoning-Model-to-Omnimodal-Agent-Foundation-Models]]"
created: 2026-06-11
---

# MiMo-VL-Miloco: Smart-Home-Specialized VLM

> [!tldr]
> MiMo-VL-Miloco-7B 是面向智能家居场景的专业 VLM，基于 MiMo-VL-7B 通过 SFT + GRPO 两阶段训练。核心设计：CoT annotations + token-budget-aware reasoning 实现数据高效 + 推理高效。5 种日常活动 F1 全部超越 Gemini-2.5-Pro，5 种手势识别平均 F1 超 Gemini-2.5-Pro 约 5 分。展示了 domain specialization 后如何通过 GRPO 恢复泛化能力。

## 问题与动机

智能家居场景对 VLM 有特殊需求：
- **边缘部署**：隐私 + 低延迟，不能依赖云端
- **手势识别**：OK、Thumbs Up、V Sign、Shaka Sign、Open Palm
- **日常活动识别**：看电视、阅读、玩手机、玩游戏、健身
- **数据稀缺**：智能家居场景的标注数据比通用域少得多

## 方法核心思路

### 1. 架构：继承 MiMo-VL-7B

- Vision Encoder：ViT，支持原生分辨率
- Projector：MLP
- LLM Backbone：MiMo-VL-7B 预训练权重

### 2. 两阶段训练

**Stage 1: SFT**
- 数据：proprietary home-scenario data + MiMo-VL 通用多模态数据
- Optimizer: AdamW, batch size 128, LR 1e-5
- Max seq: 32,768 tokens
- 全参数微调

**Stage 2: GRPO**
- 解决 SFT 的 catastrophic forgetting
- Time-R1 数据构建 + difficulty-aware filtering
- 混合 RL 信号：video understanding、GUI grounding、multimodal reasoning

### 3. CoT Supervision + Token-Budget-Aware Reasoning

**CoT annotations**：为家庭场景生成显式推理模式，在标注数据有限的情况下实现深度理解。

**Token-budget-aware reasoning**：训练模型在边缘部署场景下直接输出答案，不需要显式推理步骤，降低推理延迟。

**组合效果**：数据高效学习 + 高效推理。

### 4. 数据构造

Proprietary 数据采集流程：
1. 标准化采集协议（志愿者表演者）
2. 实时偏差校正标注
3. AI researcher 质量审查

### 5. Home-Scenario Specialization 后如何恢复泛化

关键洞察：SFT 会快速增强 home-scenario 能力，但会伤到 video、GUI、multimodal reasoning 等通用能力。GRPO post-training 把这些能力拉回来。

## 实验结果

### 智能家居场景 F1（表1）

| 类别 | MiMo-VL-Miloco-7B | Best Baseline |
|------|------------------|---------------|
| Watch TV | **98.3** | 93.8 (Gemini-2.5-Pro) |
| Reading | **90.8** | 88.9 (Gemini-2.5-Pro) |
| Play on Phone | **90.5** | 88.4 (Qwen2.5-VL-7B) |
| Play Esports | **99.2** | 95.9 (Gemini-2.5-Pro) |
| Workout | **96.7** | 93.7 (MiMo-VL-7B-SFT) |
| OK gesture | **86.3** | 81.8 (Gemini-2.5-Pro) |
| Thumbs Up | **90.5** | 86.9 (Gemini-2.5-Pro) |
| V Sign | **90.3** | 86.7 (Gemini-2.5-Pro) |
| Shaka Sign | **88.3** | 70.1 (Gemini-2.5-Pro) |
| Open Palm | **87.5** | 87.4 (Gemini-2.5-Pro) |

### 通用 benchmark（表2）

| Benchmark | MiMo-VL-Miloco-7B | Best Baseline |
|-----------|------------------|---------------|
| MMMU-Pro standard | **55.7** | 37.8 (Gemma-3-27B-IT) |
| Video-MMMU | **63.6** | SOTA among compared |
| Charades-STA | **46.6** | SOTA among compared |
| MMLU-Pro | **68.5** EM | top open-source |
| MATH500 | **95.2** Pass@1 | — |

## 对研究的启发

> [!insight]
> MiMo-VL-Miloco 最有价值的方法论贡献是"domain specialization 后如何恢复泛化"：先 SFT 快速增强专用能力，再 GRPO 拉回通用能力。这个 pattern 在 GUI agent、robotics、driving 等场景都有参考价值。

**可转化的问题**：
- GUI domain specialization + GRPO 恢复泛化是否可行？
- CoT + token-budget-aware reasoning 的组合在 GUI agent 上如何应用？
- 边缘部署对 GUI agent 模型的启示——推理效率与能力的关系

## 相关资料

- arXiv：https://arxiv.org/abs/2512.17436
- GitHub：https://github.com/XiaoMi/xiaomi-mimo-vl-miloco
- 系列总览：[[Topics/13_base_model/Xiaomi_MiMo/2606_MiMo_Series/MiMo-Series-From-7B-Reasoning-Model-to-Omnimodal-Agent-Foundation-Models]]
- MiMo-VL：[[Topics/13_base_model/Xiaomi_MiMo/2506_MiMo_VL_7B/MiMo-VL]]
