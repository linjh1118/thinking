---
title: "ERNIE 5.0 Technical Report"
type: paper
authors: ["ERNIE Team, Baidu"]
year: 2026
venue: COLM 2024
arxiv: "2602.04705"
doi:
url: "https://arxiv.org/abs/2602.04705"
tags: [paper, multimodal, unified-model, moe, elastic-training, autoregressive]
topic: "13_base_model"
status: read
rating: 5
related:
  - "[[Topics/13_base_model/Base Model MOC]]"
  - "[[Topics/13_base_model/Baidu_ERNIE/ERNIE-Series-Summary]]"
created: 2026-06-18
---

# ERNIE 5.0 Technical Report

> [!tldr]
> ERNIE 5.0 是百度提出的**原生多模态统一自回归基座模型**，首次在万亿参数规模实现了 text/image/video/audio 的统一建模。核心创新包括：**ultra-sparse MoE** + **modality-agnostic expert routing** + **elastic training**（一次训练产出多尺寸子模型）+ **分离式全异步 RL post-training**。在知识、推理、代码、多模态理解与生成等任务上达到 SOTA 水平。

## 问题与动机

现有系统存在两大问题：
1. **能力跷跷板**：晚期融合方法（LLM + 模态解码器）往往在提升某模态能力时牺牲其他模态性能
2. **架构碎片化**：理解用一套架构，生成用另一套架构，无法深层跨模态融合

ERNIE 5.0 的目标是：**从零开始训练**一个真正统一的模型，所有模态在同一个 Next-Group-of-Tokens Prediction 目标下共同优化。

## 方法核心

### 1. 统一自回归架构（Ultra-Sparse MoE）

```
文本: Next-Token Prediction (NTP) + Multi-Token Prediction (MTP)
图像: Next-Frame-and-Scale Prediction (NFSP) — 视为单帧视频
视频: Next-Frame-and-Scale Prediction (NFSP)
音频: Next-Codec Prediction (NCP) — 层级预测
```

关键设计：**Modality-Agnostic Expert Routing**
- 所有模态共享同一个 expert pool，路由决策基于统一 token 表示而非显式模态 ID
- ultra-sparse 设计：激活率 < 3%，参数量万亿级但计算开销可控
- 无需启发式模态特定 expert 分配

### 2. 视觉建模双路径混合表示

对于视觉理解，采用 **CNN + ViT 双路径融合**：
- CNN 提取局部感知特征，ViT 提取全局语义特征
- **Attention-Based Patch Merger** 替代简单 MLP fusion：通过多头自注意力融合 CNN 和 ViT patches

对于视觉生成，**NFSP 范式**：
- 图像生成为 Next-Scale Prediction（从低分辨率到高分辨率）
- 视频生成扩展为 Next-Frame Prediction（沿时间维度）

### 3. 音频建模层级预测

- **RVQ (Residual Vector Quantization)** 编码音频为多层级离散 tokens
- **Depth-wise Autoregressive**：将残差码预测分配到不同 transformer 层
- **Next-Codec Prediction (NCP)**：从粗到细逐层生成

### 4. 弹性训练（Elastic Training）

核心思想：**一次预训练，产出多个尺寸的子模型**，无需后压缩。

| 维度 | 方法 | 训练配置 |
|------|------|---------|
| **Elastic Depth** | 随机激活不同层数 | 75% 全深度，25% 浅层子网 |
| **Elastic Width** | 随机使用不同 expert 数量 | 80% 全部 expert，20% 子集 |
| **Elastic Sparsity** | 随机使用不同 top-k | 80% 默认 k，20% 更小 k |

实验结果：
- ERNIE 5.0-Exp-EA$_{35.8\%}$ 仅用 53.7% 激活参数 + 35.8% 总参数，仍保持接近全模型性能
- 推理 top-k 降至 25% 可获得 >15% 解码加速

### 5. Post-Training: U-RL 统一多模态强化学习

#### U-RB: Unbiased Replay Buffer
解决长尾响应分布导致 GPU 空闲问题。通过数据排序约束保持无偏分布。

#### MISC: Multi-granularity Importance Sampling Clipping
避免熵崩溃。对 GSPO 的 sequence-level truncated IS 进行 token-level 改造。

#### WPSM: Well-learned Positive Sample Mask
对已掌握的 query 屏蔽梯度，将预算转向困难样本。

#### AHRL: Adaptive Hint-based RL
对于极难任务（base model pass@k ≈ 0），通过渐进揭示 think skeleton 提供 scaffold。

## 实验结果

### 预训练模型对比

| Benchmark | DS V3.2-Exp-Base | Kimi K2-Base | ERNIE 5.0-Base |
|-----------|------------------|--------------|----------------|
| MMLU-Pro | 68.27 | 67.19 | **75.58** |
| MATH (CoT) | 65.70 | 65.90 | **73.89** |
| LiveCodeBench v6 | 24.90 | 26.30 | **31.94** |
| ChineseSimpleQA | 74.19 | 78.29 | **90.09** |

### Post-trained 模型对比

| Benchmark | Gemini 3-Pro | ERNIE 5.0 |
|-----------|--------------|-----------|
| SimpleQA | 69.33 | **74.01** |
| Multi-IF | 81.15 | **85.56** |
| ACEBench-en | 80.90 | **87.70** |
| VLMAreBlind | 80.83 | **91.38** |
| AISHELL-1 (WER↓) | 3.04 | **0.31** |

### 视觉理解对比

ERNIE 5.0 在 DocVQA (95.45)、CountBench (96.54) 等任务上达到第一。

### 图像/视频生成

- GenEval: 90.1（与 Qwen-Image 91.0 相当）
- VBench-Semantic: **83.40**（超越 Veo3 等商业模型）

## 关键洞察

> [!insight]
> 1. **Modality-Agnostic Routing 的自组织特性**：尽管路由机制不区分模态，但专家仍展现出明显的模态特定激活模式。这表明路由器能自主捕捉模态结构并分配专家容量，无需显式设计。
>
> 2. **Elastic Training 的正则化效应**：弹性深度训练不仅不损害全深度性能，反而略有提升（验证 loss 1.941 vs 1.945）。这说明 layer dropping 起到类似 DropPath 的正则化作用。
>
> 3. **理解与生成的互强化**：统一框架中，语义级信号引导生成建模趋向全局一致性，而生成训练反过来增强细粒度感知和细节敏感推理。两者相互强化，而非相互制约。
>
> 4. **多模态 RL 的工程挑战**：超稀疏 MoE + 多模态输入使 RL 训练极易遭遇采样偏差、稀疏奖励信号和熵崩溃。解法需要系统（U-RB）和算法（MISC/WPSM/AHRL）的协同优化。

## 论文矩阵

| 维度 | ERNIE 5.0 |
|------|-----------|
| **核心贡献 1** | 首个万亿参数统一自回归多模态模型（text/image/video/audio 端到端） |
| **核心贡献 2** | Modality-Agnostic Ultra-Sparse MoE（激活率 <3%） |
| **核心贡献 3** | Elastic Training（一次训练产出多尺寸子模型） |
| **核心贡献 4** | 分离式全异步 RL 训练系统（U-RB + MISC + WPSM + AHRL） |
| **训练目标** | Next-Group-of-Tokens Prediction（统一） |
| **模型规模** | ~2.4T 参数 |
| **多模态支持** | text + image + video + audio |
| **创新点类型** | 架构创新 + 训练范式创新 + RL 优化创新 |
| **工程价值** | PaddlePaddle 完整训练/推理栈，弹性部署支持 |

## 相关论文

- [[Topics/10_world_model/2509_GeneralAgenticIntel/AgentScaler]] — AgentScaler 类似地探索子网弹性
- [[Topics/12_skill/think_with_image/think_with_image_insight]] — 多模态统一建模思路相关
