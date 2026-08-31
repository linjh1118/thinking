---
title: "Step-GUI Technical Report"
type: paper
authors: ["Haolong Yan", "Jia Wang", "Xin Huang", "et al."]
year: 2025
venue: arXiv
arxiv: "2512.15431"
doi:
url: "https://arxiv.org/abs/2512.15431"
tags: [paper, gui-agent, gui-automation, stepfun]
status: read
rating: 5
topic: "13_base_model"
related: []
created: 2026-06-12
---

# Step-GUI Technical Report

> [!tldr]
> Step-GUI 是字节跳动 StepFun 团队开源的 GUI Agent 模型族（4B/8B），基于 Qwen3-VL 主干，通过**自进化训练 pipeline + CSRS 校准步奖励系统**实现高效数据标注（>90% 准确率，10-100x 成本降低），在 AndroidWorld 达到 **80.2%**、OSWorld 达到 **48.5%**、ScreenSpot-Pro 达到 **62.6%** 的 SOTA 表现。同时提出 GUI-MCP 协议和 AndroidDaily 真实日常场景 benchmark。

---

## 问题与动机

GUI Agent 发展的核心瓶颈：**如何在保持标注可靠性的同时高效获取高质量训练数据？**

- 传统人工标注成本高、主观性强，难以扩展
- 模型生成的轨迹存在幻觉和事实错误，无法直接作为监督信号
- 多轮交互任务中，单步级别的标注偏差会累积放大

---

## 方法核心思路

### 1. Calibrated Step Reward System (CSRS)

CSRS 是整个 pipeline 的核心创新，通过**轨迹级校准**将模型生成的轨迹转化为可靠的训练信号：

- **校准层**：使用验证脚本或人工进行二元成功/失败判断（轨迹级），提供高置信度 reward
- **数据抽取层**：由思维模型（thinking model）从轨迹中抽取 7 类结构化训练数据
  1. Progress Tracking（进度追踪）
  2. State Summary（状态摘要）
  3. Effect Prediction（效果预测）
  4. Self-Reflection（自我反思）
  5. State Verification（状态验证）
  6. Intent Execution（意图执行）
  7. Action Prediction（动作预测）

**选择性学习策略**：成功轨迹抽取全部 7 类数据；失败轨迹只抽取知识类数据（1-6），不学习错误动作（"从失败中学知识，不学错误动作"）。

**关键效果**：>90% 标注准确率，10-100x 成本降低。

### 2. 三阶段渐进训练范式

| 阶段 | 数据规模 | 核心目标 |
|------|---------|---------|
| Mid-Train | ~11.2M | 通用能力保留 + 基础 agent 能力（visual grounding、action alignment、trajectory） |
| Cold-Start | ~1.67M | 知识注入 + 执行精调（错误驱动 VQA 知识注入） |
| RLVR（GRPO） | 迭代生成 | 精细化 RL 训练，三类 reward：空间几何 reward、动作语义 reward、LLM-as-Judge 软 reward |

### 3. 迭代 grounding 清洗 pipeline

GUI grounding 数据存在噪声（标注错误）和错位（语义不对应）。通过：
1. 初始训练 → 多轮 rollout 打分 → pass-rate 标注 + LLM 复杂度评分
2. 课程学习 Curriculum SFT + RL，按难度逐步引入
3. 零 pass-rate 样本排除后再回收精调

### 4. GUI-MCP 协议

首个专为 GUI 自动化设计的 MCP 实现，双层架构：

- **Low-level MCP**：原子操作（click, swipe, input_text, hotkey 等）
- **High-level MCP**：将任务委托给本地部署的 GUI 专家模型（如 Step-GUI-4B）

**隐私保护模式**：截图中只提取语义摘要发给云端 LLM，原始图片留在本地。

### 5. AndroidDaily Benchmark

填补"高频日常场景"的评估空白：
- **Static Benchmark**：3146 actions，8 类动作（CLICK/TYPE/SLIDE/AWAKE/INFO/COMPLETE/WAIT/LONG_PRESS）
- **End-to-End Benchmark**：235 任务，覆盖交通/购物/社交/娱乐/本地服务五大场景

---

## 实验结果

### GUI Grounding Benchmarks

| Model | ScreenSpot-Pro | ScreenSpot-v2 | OSWorld-G | MMBench-GUI-L2 | VisualWebBench |
|-------|---------------|---------------|----------|----------------|----------------|
| UI-TARS-1.5 | 61.6 | 94.2 | - | - | - |
| GUI-Owl-32B | 58.0 | 93.2 | 58.0 | 83.0 | - |
| Qwen3-30B-A3B | 60.5 | 94.7 | 61.0 | 79.7 | 79.7 |
| **Step-GUI-4B** | 60.0 | 93.6 | **66.9** | 84.0 | **90.7** |
| **Step-GUI-8B** | **62.6** | 95.1 | **70.0** | **85.6** | 89.7 |

### End-to-End Benchmarks（Pass@3）

| Model | OSWorld-Verified | AndroidWorld |
|-------|----------------|--------------|
| Claude-4.5-sonnet | 61.4 | - |
| UI-TARS-2 | 47.5 | 73.3 |
| MobileRL-9B | - | 80.2 |
| **Step-GUI-4B** | 40.4 | 75.8 |
| **Step-GUI-8B** | **48.5** | **80.2** |

### AndroidDaily

| 模型 | Static AVG | E2E Total |
|------|-----------|-----------|
| UI-TARS-1.5 | 67.69% | 56.64% |
| **Step-GUI-4B** | 87.02% | 49.06% |
| **Step-GUI-8B** | **89.91%** | 52.50% |

### 自进化训练动态

经过 6 轮迭代：
- AndroidWorld 从 Round 2 的 44.83% 跃升至 Round 3 的 73.40%（CSRS 生成数据流催化）
- OSWorld 稳步提升 29.63% → 46.26%（Refinement 数据流持续挖掘弱点）

---

## 对研究的启发

> [!insight] 核心启发

1. **轨迹级校准 > 单步级标注**：CSRS 的核心洞察是，用客观可验证的轨迹级成功/失败信号锚定LLM生成的密集步级推理，比单纯依赖模型自省或事后过滤更可靠。>90% 标注准确率证明了这一点。

2. **自进化飞轮是 Scalable 的关键**：Rollout → CSRS → Training →更强模型→更好 Rollout 的闭环，让模型自己探索并从成功轨迹中学习知识，形成自我强化的能力提升。

3. **紧凑模型可通过专项训练超越大模型**：Step-GUI-4B/8B 在多个 benchmark 上超越 30B-72B 模型，说明训练数据和训练范式比参数规模更重要。

4. **GUI-MCP 的隐私分层设计具有普适性**：将语义摘要 vs 原始截图分离的思想，可以推广到任何需要云端推理 + 本地隐私的场景。

5. **高频日常场景 benchmark 的价值**：AndroidDaily 填补了"接地气的中文移动操作"评估空白，89.91% vs 52.50% 的 static/e2e gap 说明单步 accuracy 不能替代端到端任务完成率。

---

## 相关工作链接

- [[GUI MOC]]
- [[OSWorld 相关笔记]]
- [[AndroidWorld 相关笔记]]
