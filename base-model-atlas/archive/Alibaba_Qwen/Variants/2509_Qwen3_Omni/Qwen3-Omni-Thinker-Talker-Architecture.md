---
title: "Qwen3-Omni Technical Report"
type: paper
authors: ["Qwen Team"]
year: 2026
venue: arXiv
arxiv: "2509.17765"
url: "https://arxiv.org/abs/2509.17765"
tags: [paper, qwen, omni, multimodal, speech]
topic: "13_base_model"
status: read
rating: 5
created: 2026-05-30
---

# TL;DR

Qwen3-Omni 是一个统一的多模态模型，能够同时理解和生成文本与语音。核心架构是 Thinker-Talker：Thinker 负责理解和推理（文本/图像/音频/视频），Talker 负责流式语音生成。关键创新是实现了"模态不降智"——在加入音频模态后，文本和视觉能力不下降，同时新增跨模态推理能力。

## 问题与动机

传统 LLM 为中心的多模态模型往往存在模态权衡：增强一个模态会导致其他模态性能下降。Qwen3-Omni 探索在 LLM 范式下实现联合多模态训练，证明可以达到所有模态都不降智，同时显著增强跨模态能力（如视频理解）。

## 方法核心思路

### Thinker-Talker 架构
- **Thinker**: 理解和推理，输出文本 token 和高层表示
- **Talker**: 接收多模态特征，生成流式语音 token

### 五大升级（相比 Qwen2.5-Omni）
1. **MoE 设计**: Thinker 和 Talker 都采用 MoE 架构
2. **AuT 音频编码器**: 从头训练的 Audio Transformer，20M 小时监督数据，12.5Hz token rate
3. **多码本表示**: RVQ codec 支持 12.5 Hz 输出，单帧即时语音合成
4. **MTP 模块**: Multi-Token Prediction 生成残差码本
5. **低延迟**: 端到端延迟最低 234ms（音频输入）

### 关键技术
- **TM-RoPE**: 时间对齐的多模态旋转位置编码，支持任意时长流式输入
- **Chunked Prefilling**: 异步预填充，Thinker 和 Talker 并行工作
- **Thinker-Talker 解耦**: Talker 不再消耗 Thinker 的高层文本表示，支持外部模块干预

### 训练数据
- 预训练: 文本+视觉+音频+音视频联合训练
- 早期阶段混合单模态和跨模态数据是关键

## 关键结果

**模态不降智验证**（30B-A3B 模型对比）:

| 任务类型 | Qwen3-30B-A3B-Base | Qwen3-VL-30B-A3B-Base | Qwen3-Omni-30B-A3B-Base |
|---------|---------------------|------------------------|-------------------------|
| MMLU | 81.24 | - | **81.69** |
| GSM8K | 90.83 | - | **91.36** |
| MMMU_val | - | 57.22 | **59.33** |
| Video-MME | - | 69.22 | **69.25** |

**36 个音频/音视频 benchmark，32 个取得开源 SOTA，22 个取得总 SOTA**

## 对研究的启发

> [!insight]
> 1. **模态不降智**的验证对 GUI Agent 很重要：添加语音/音频能力不应该损害视觉理解能力
> 2. **Thinker-Talker 分离架构**对实时交互系统有参考价值，可用于需要边想边说的 Agent
> 3. **流式语音生成 + 低延迟**对语音交互 Agent 是关键能力

## 相关链接
- 论文: [arXiv Link](https://arxiv.org/abs/2509.17765)
