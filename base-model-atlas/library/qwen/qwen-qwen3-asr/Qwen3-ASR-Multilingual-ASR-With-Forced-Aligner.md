---
title: "Qwen3-ASR Technical Report"
type: paper
authors: ["Qwen Team"]
year: 2026
venue: arXiv
arxiv: "2601.21337"
url: "https://arxiv.org/abs/2601.21337"
tags: [paper, qwen, asr, speech-recognition]
topic: "13_base_model"
status: read
rating: 4
created: 2026-05-30
---

# TL;DR

Qwen3-ASR 是一个基于 LALM（Large Audio-Language Model）范式的自动语音识别模型家族，包括 Qwen3-ASR-1.7B、Qwen3-ASR-0.6B 和 Qwen3-ForcedAligner-0.6B。核心贡献是首次将 LLM 引入强制对齐（Forced Alignment）任务，实现任意时间粒度的灵活时间戳预测，且支持 11 种语言的统一对齐。

## 问题与动机

传统 ASR 系统难以处理长语音、抗噪声、多语言/方言覆盖等问题。LALM 范式可以利用 LLMs 的语言建模能力和世界知识，更自然地解决这些问题。同时，时间戳预测是字幕生成等下游任务的关键，现有方法（CTC、CIF）在多语言支持、长语音鲁棒性和计算开销方面存在局限。

## 方法核心思路

### 架构
- 基于 Qwen3-Omni 基础模型
- **AuT 音频编码器**: AED 架构，8 倍下采样，12.5Hz token rate，动态 attention window（1-8 秒）
- **Qwen3-ASR-1.7B**: Qwen3-1.7B + 300M AuT encoder
- **Qwen3-ASR-0.6B**: Qwen3-0.6B + 180M AuT encoder

### 训练策略
1. **AuT 预训练**: ~40M 小时伪标签 ASR 数据
2. **Omni 预训练**: 多模态（音频+视觉+文本）训练，3T tokens
3. **ASR SFT**: 风格迁移，统一 ASR 输入/输出格式
4. **ASR RL (GSPO)**: 50k  utterances，35% 中英文 + 35% 多语言 + 30% 功能数据

### 关键能力
- **52 种语言/方言**: 30 种语言 + 22 种中文方言
- **长语音**: 最长 20 分钟单条语音
- **流式/离线统一推理**
- **唱歌识别**: 支持带背景音乐的完整歌曲转录
- **Contextual Biasing**: 自由形式的上下文偏置

### Qwen3-ForcedAligner-0.6B
- **Slot-filling 范式**: 在 transcript 中插入 [time] token，预测对应的时间戳索引
- **因果训练**: 不使用 next-token prediction 的 shift，确保时间戳槽位对齐
- **NAR 解码**: 非自回归，同时预测所有时间戳
- **MFA 伪标签蒸馏**: 从 Montreal Forced Aligner 蒸馏，减少系统性偏移

## 关键结果

**英语/中文 ASR 性能**:

| 数据集 | GPT-4o-Transcribe | Whisper-Large-v3 | Qwen3-ASR-1.7B |
|--------|-------------------|------------------|-----------------|
| LibriSpeech (clean) | 1.39 | 1.51 | **1.63** |
| GigaSpeech | 9.37 | 9.76 | **8.45** |
| WenetSpeech (meeting) | 14.43 | 9.86 | **4.97** |
| AISHELL-2-test | 4.24 | 5.06 | **2.71** |

**推理效率**:

| 模型 | 并发 | TTFT avg. | RTF | 吞吐量 |
|------|------|-----------|-----|--------|
| Qwen3-ASR-0.6B | 128 | 3210ms | 0.064 | **2000** |
| Qwen3-ASR-1.7B | 128 | 3392ms | 0.105 | 1219 |

**ForcedAligner 时间戳精度**:
- 比 MFA 相对减少 67-77% 的累积平均偏移

## 对研究的启发

> [!insight]
> 1. **LALM 范式**对构建通用语音 Agent 有重要参考价值，可同时支持 ASR、TTS、语音对话
> 2. **Sub-1B 参数的 ASR 模型**达到与专有 API 相当的性能，对边缘部署极具价值
> 3. **Forced Alignment + LLM** 的组合可能用于自动生成语音-文本对齐数据，对训练语音 Agent 很有用

## 相关链接
- 论文: [arXiv Link](https://arxiv.org/abs/2601.21337)
