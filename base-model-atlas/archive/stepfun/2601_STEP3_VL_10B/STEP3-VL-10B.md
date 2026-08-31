---
title: "STEP3-VL-10B Technical Report"
type: paper
authors: ["Ailin Huang", "Chengyuan Yao", "Chunrui Han", "Fanqi Wan", "Hangyu Guo", "Haoran Lv", "Hongyu Zhou", "Jia Wang", "Jian Zhou", "Jianjian Sun", "Jingcheng Hu", "Kangheng Lin", "Liang Zhao", "Mitt Huang", "Song Yuan", "Wenwen Qu", "Xiangfeng Wang", "Yanlin Lai", "Yingxiu Zhao", "Yinmin Zhang", "Yukang Shi", "Yuyang Chen", "Zejia Weng", "Ziyang Meng", "et al."]
year: 2026
venue: arXiv
arxiv: "2601.09668"
doi:
url: "https://arxiv.org/abs/2601.09668"
tags: [paper, vlm, multimodal, 10b, reinforcement-learning, reasoning]
topic: "13_base_model"
status: read
rating: 5
related: []
created: 2026-06-12
---

# STEP3-VL-10B Technical Report

> [!tldr]
> STEP3-VL-10B 是一个 10B 参数的多模态大模型，通过 1.2T token 的统一预训练 + 1k+ 轮强化学习（RLVR + RLHF）+ PaCoRe（并行协同推理）实现高效的小模型（10B）超越 10-20x 大模型（GLM-4.6V 106B、Qwen3-VL 235B）的性能。在 MMBench 达到 92.2%、MMMU 80.11%、AIME2025 94.43%。

## 问题与动机

当前多模态大模型（MLLM）的发展主要由参数规模扩张驱动。顶级闭源模型如 Gemini-3-Pro 和 GPT-5.2 通过大规模缩放达到 SOTA，但计算成本高昂，难以实际部署。相反，轻量级模型（<10B 参数）通常被视为"高效但受限"，在有限的参数预算内难以提升复杂推理和感知能力。

**核心问题**：如何在 10B 参数规模下实现与 100B+ 模型竞争的前沿多模态智能？

## 方法核心思路

### 1. 统一预训练（Unified Pre-training）

- **架构**：1.8B 语言对齐 Perception Encoder + Qwen3-8B decoder，通过 16x 空间下采样 projector 连接
- **策略**：单阶段、完全 unfrozen 训练（而非传统多阶段 frozen backbone）
- **数据**：1.2T token 多模态语料，涵盖知识（Interleaved 数据 + Image-Text Pairs）、教育（15M K-12 到大学+成人考试样本）、OCR（10M 真实 + 30M 合成 + 80M 文档）、Grounding & Counting（400M）、GUI（23M）
- **训练**：370K iterations，batch size 8192，seq len 4096，两阶段 LR schedule

### 2. 后训练（Post-Training）

**两阶段 SFT**：
- Stage 1：Text-Dominant Reasoning（9:1 text-to-multimodal ratio）
- Stage 2：Multimodal Integration（1:1 ratio）
- 总计约 226B tokens，128k seq len

**强化学习（PPO + GAE）**：
- RLVR（Verifiable Rewards）：600 iterations，覆盖数学、几何、物理、科学推理、感知、Grounding 等
- RLHF：300 iterations，优化人类偏好对齐
- PaCoRe（Parallel Coordinated Reasoning）：500 iterations，扩展测试时计算

### 3. PaCoRe 核心创新

**动机**：视觉任务的 RL 增益来自 Pass@N → Pass@1 的搜索空间压缩，而非延长推理链（与文本 RL 不同）

**方法**：
1. 从 RLVR 阶段保留 24 个 rollouts 作为 message cache pool
2. 对 some-accept 样本，采样 16-24 条消息作为合成上下文
3. 模型在并行提案 + 顺序交叉验证的模式下学习

**类比**：类似 Faster R-CNN 的 RPN（区域提案网络）→ proposal-then-refinement

## 实验结果

### 与同规模模型对比（7B-10B）

| Benchmark | STEP3-VL-10B | GLM-4.6V-Flash (9B) | Qwen3-VL-Thinking (8B) |
|-----------|-------------|---------------------|------------------------|
| MMMU | **78.11%** | 71.17% | 73.53% |
| MMBench EN | **92.05%** | 91.04% | 90.55% |
| MMBench CN | **91.55%** | 89.56% | 89.75% |
| MathVision | **70.81%** | 54.05% | 59.60% |
| OCRBench | **86.75%** | 85.97% | 82.85% |
| ScreenSpot-V2 | 92.61% | 92.14% | **93.60%** |
| OSWorld-G | **59.02%** | 54.71% | 56.70% |

### 与大模型对比（10B vs 106B-235B）

| Benchmark | SeRe (10B) | PaCoRe (10B) | GLM-4.6V (106B) | Qwen3-VL (235B) | Gemini-2.5-Pro |
|-----------|-----------|--------------|-----------------|-----------------|----------------|
| MMMU | 78.11% | **80.11%** | 75.20% | 78.70% | 83.89% |
| MathVision | 70.81% | **75.95%** | 63.50% | 72.10% | 73.30% |
| AIME2025 | 87.66% | **94.43%** | 71.88% | 83.59% | 83.96% |
| MMBench Avg | 92.05% | **92.17%** | 92.75% | 92.70% | 93.19% |
| MMStar | 77.48% | **77.64%** | 75.30% | 76.80% | 79.18% |

> [!insight]
> **核心发现**：
> 1. **PaCoRe 显著提升推理密集任务**：MathVision +5.14%，AIME2025 +6.77%，DynaMath +5.09%
> 2. **PaCoRe 对感知密集任务效果明显**：CountQA +4.6%，OCRBench +2.25%，All-Angles-Bench +7.50%
> 3. **RL 长度动态独特**：文本 RL 表现为链式思维增长，而多模态 RL 表现为长度缩减（感知任务 entropy reduction）
> 4. **语言对齐的视觉编码器至关重要**：PE-lang 相比 DINOv3 收敛更快、性能更好

## 对研究的启发

> [!insight]
> 1. **小模型可通过训练配方匹敌大模型**：正确的预训练策略（unified fully unfrozen）+ 规模化 RL 可弥补参数差距
> 2. **PaCoRe 是感知 Scaling 的有效路径**：将隐式视觉过程外化，通过并行提案 + 顺序验证实现多视角自验证
> 3. **RL 在视觉任务中的机制与文本不同**：感知任务 RL 增益来自 entropy reduction（搜索空间压缩），而非 chain-of-thought 延长
> 4. **未来方向**：通过 self-distillation 将 PaCoRe 的"慢思考"轨迹内化为模型"快直觉"

## 相关链接

- **arXiv**: https://arxiv.org/abs/2601.09668
- **ModelScope**: https://modelscope.cn/collections/stepfun-ai/Step3-VL-10B
- **Huggingface**: https://huggingface.co/collections/stepfun-ai/step3-vl-10b
