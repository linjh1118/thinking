---
title: "Qwen3.5-Omni Technical Report"
type: paper
authors: ["Qwen Team"]
year: 2026
venue: arXiv
arxiv: "2604.15804"
url: "https://arxiv.org/abs/2604.15804"
tags: [paper, qwen, omni, multimodal, agent]
topic: "13_base_model"
status: read
rating: 5
created: 2026-05-30
---

# TL;DR

Qwen3.5-Omni 是 Qwen3-Omni 的升级版，核心升级包括 Hybrid Attention MoE 架构（更高效的长序列推理）、256K token 上下文（支持 10+ 小时音频或 400 秒 720P 视频）、以及 **ARIA**（自适应速率交错对齐）技术解决流式语音合成中的文本-语音单元对齐问题。Plus 版本在 215 个 benchmark 上取得 SOTA，超越 Gemini-3.1 Pro。

## 问题与动机

现有模型大多是被动的感知-响应范式，缺乏可扩展的 agentic 行为、实时交互、自主工具调用和跨模态推理能力。Qwen3.5-Omni 旨在构建一个**原生 omni agent**：不仅感知和推理所有模态，还能**行动**（WebSearch、FunctionCall、语音生成、流式交互）。

## 方法核心思路

### 架构升级（相比 Qwen3-Omni）
1. **Hybrid MoE**: Thinker 和 Talker 都采用 Hybrid Attention MoE，提升 scalability 和 efficiency
2. **256K 上下文**: 支持 10+ 小时音频、400 秒 720P 视频
3. **ARIA (Adaptive Rate Interleave Alignment)**: 动态对齐文本和语音单元，解决双通道生成的稳定性问题
4. **AuT encoder 升级**: 40M 小时训练数据，6.25Hz token rate，20+ 语言

### ARIA 技术
- 替代 Qwen3-Omni 的双通道生成范式
- 单通道统一生成 formulation
- **自适应速率约束**: 任何生成序列前缀的累计 speech-to-text token 比不超过对应的 item-level 全局比
- 解决跳词、发音错误、数字渲染歧义等问题

### 关键新能力
1. **可控音视频 captioning**: 脚本级结构化描述，自动分段、时间戳标注
2. **实时交互**: 语义打断（原生 turn-taking）、端到端音量/语速/情感控制、语音克隆
3. **原生 omni agent 行为**: 自主 WebSearch、复杂 FunctionCall、**Audio-Visual Vibe Coding**（从音视频指令直接生成可执行代码）

### 流式延迟

| 配置 | 1 并发 | 4 并发 | 8 并发 |
|------|--------|--------|--------|
| Flash (音频输入) | 235ms | 298ms | 352ms |
| Plus (音频输入) | 435ms | 619ms | 955ms |
| Flash (视频输入) | 426ms | 891ms | 1625ms |

## 关键结果

**215 个 benchmark 综合评估**:
- Qwen3.5-Omni-Plus 在通用音频理解、推理、识别、翻译、对话上超越 Gemini-3.1 Pro
- 音视频理解达到 Gemini-3.1 Pro 水平

**语音生成**（Seed-TTS test-en WER，越低越好）:
- Qwen3.5-Omni-Plus: **1.26** (after RLHF optimization)

## 对研究的启发

> [!insight]
> 1. **Audio-Visual Vibe Coding** 的出现意味着多模态 Agent 可能直接从音视频理解跳到代码生成，这对 GUI Agent 有重要启示
> 2. **ARIA 技术**对需要同时生成文本和语音的 Agent 系统有直接参考价值
> 3. **原生 omni agent**（感知+行动）可能是未来 GUI Agent 的最终形态
> 4. **256K 上下文 + Hybrid MoE** 的组合使处理超长 GUI 任务成为可能

## 相关链接
- 论文: [arXiv Link](https://arxiv.org/abs/2604.15804)
