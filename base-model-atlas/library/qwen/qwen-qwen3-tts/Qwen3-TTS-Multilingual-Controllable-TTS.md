---
title: "Qwen3-TTS Technical Report"
type: paper
authors: ["Qwen Team"]
year: 2026
venue: arXiv
arxiv: "2601.15621"
url: "https://arxiv.org/abs/2601.15621"
tags: [paper, qwen, tts, speech-synthesis]
topic: "13_base_model"
status: read
rating: 4
created: 2026-05-30
---

# TL;DR

Qwen3-TTS 是 Qwen 系列的首个 TTS 模型，支持多语言、可控的流式语音合成。核心创新包括双码率设计（12Hz 和 25Hz）和多码本预测（MTP）模块，实现最低 97ms 的首包延迟。12Hz-1.7B 变体在 Seed-TTS benchmark 上达到 SOTA，WER 仅 1.24。

## 问题与动机

现代 TTS 系统需要在**稳定性**（文本对齐）、**可控性**（细粒度控制声音属性）、**自然度**（类人语音）和**低延迟**（流式交互）之间取得平衡。Qwen3-TTS 旨在构建一个同时满足这些要求的统一模型。

## 方法核心思路

### 模型架构
- 基于 Qwen3 LM 骨干
- **25Hz 变体**: 单码本表示 + chunk-wise DiT 解码器
- **12Hz 变体**: RVQ 多码本表示 + MTP 模块 + 轻量级 ConvNet Code2Wav

### 训练流程
1. **S1 通用阶段**: 5M+ 小时多语言语音数据，建立文本到语音的单调映射
2. **S2 高质量阶段**: 精选高质量数据，缓解噪声数据导致的幻觉
3. **S3 长上下文阶段**: 最大长度从 8K 扩展到 32K

### 后训练
1. **DPO**: 基于人类反馈的偏好对齐
2. **GSPO**: 基于规则的奖励提升稳定性和任务表现
3. **Speaker Fine-tuning**: 支持特定声音克隆

### 关键能力
- **3 秒语音克隆**: 支持参考音频克隆
- **Voice Design**: 通过自然语言描述创建/操控声音
- **多语言**: 10+ 语言，跨语言一致性生成
- **长语音生成**: 可合成 10+ 分钟的流畅语音

## 关键结果

**语音重建性能**（LibriSpeech test-clean）:

| 模型 | PESQ_WB | STOI | UTMOS | SIM |
|------|---------|------|-------|-----|
| Mimi | 2.88 | 0.94 | 3.87 | 0.87 |
| Qwen-TTS-Tokenizer-12Hz | **3.21** | **0.96** | **4.16** | **0.95** |

**Zero-shot 语音生成**（Seed-TTS test-en WER，越低越好）:
- Qwen3-TTS-12Hz-1.7B: **1.24** (SOTA，超越 CosyVoice 3 的 1.45)

**延迟性能**:

| 模型 | 首包延迟 | RTF (1 并发) |
|------|---------|-------------|
| Qwen3-TTS-12Hz-0.6B | **97ms** | 0.288 |
| Qwen3-TTS-12Hz-1.7B | 101ms | 0.313 |

## 对研究的启发

> [!insight]
> 1. **多码本 + MTP** 的设计对需要流式语音输出的 Agent 有直接参考价值
> 2. **超低延迟（<100ms）** 对实时语音交互至关重要，是用户体验的关键
> 3. **Voice Design via 自然语言**的能力对个性化 Agent 场景很有价值

## 相关链接
- 论文: [arXiv Link](https://arxiv.org/abs/2601.15621)
