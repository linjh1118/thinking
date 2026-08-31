---
title: "Base Model Top 8 Branch Audit — 2026-08"
type: insight
tags: [insight, base-model, coverage, variants, top8]
source: "[[Topics/13_base_model/Base Model MOC]]"
created: 2026-08-31
updated: 2026-08-31
---

# Base Model Top 8 Branch Audit — 2026-08

> [!tldr]
> 本审计把国内 Top 5（DeepSeek、GLM、Kimi、Qwen、Seed）和海外 Top 3（GPT、Claude、Gemini）拆成“通用主干正代 + 专项/模态支线”。主干只放跨代旗舰，Coder、Vision、Speech、Robotics、Medical 等单列，避免把 SKU、尺寸和 API snapshot 混成代际。

## 审计总表

| 团队 | 当前主干节点 | 已核对支线 |
|---|---|---|
| DeepSeek AI | DeepSeek-V4 Pro | **Reasoning**：R1-Zero · R1 · R1-Distill · V3.2-Speciale；**Code**：DeepSeek-Coder · Coder-V2；**Math / Prover**：DeepSeekMath · Prover V1/V1.5/V2；**Vision / Omni**：DeepSeek-VL/VL2 · Janus/Janus-Pro；**Document**：DeepSeek-OCR · OCR2 |
| Zhipu · GLM | GLM-5.3 Flash | **Vision**：GLM-4V · 4.5V · 4.6V · 5V · CogVLM；**Code**：CodeGeeX · CodeGeeX4；**Speech**：GLM-4-Voice · GLM-TTS；**Document**：GLM-OCR；**Image / Video**：CogView · CogVideoX；**Agent**：AutoGLM · Phone / Computer Use |
| Moonshot · Kimi | Kimi K2.6 | **Vision**：Kimi-VL · K1.5 · K2.5；**Audio**：Kimi-Audio；**Code**：Kimi-Dev；**Formal Reasoning**：Kimina-Prover；**Efficient Attention**：MoBA · Kimi Linear |
| Alibaba · Qwen | Qwen3.8 | **Code**：Qwen-Coder · Qwen3-Coder · Coder-Next；**Vision**：Qwen-VL · Qwen3-VL · VL-Seg · VLA；**Omni / Speech**：Qwen3-Omni · ASR · TTS；**Image**：Qwen-Image · Image 2 · VAE 2；**Retrieval**：Embedding · Reranker · VL-Embedding；**Safety / Agent**：Qwen3Guard · Qwen-Scope |
| ByteDance · Seed | Seed2.0 | **Vision / Omni**：Seed1.5-VL · Seed1.5-Thinking · Seed2.0；**Medical**：MedXIAOHE；**Code / Open**：Seed-Coder · Seed-OSS · Seed-Prover；**Any-to-any**：BAGEL；**Speech**：Seed-TTS；**Image / Video**：Seedream · SeedEdit · Seedance；**World / Embodied**：Seed3D · GR family |
| OpenAI · GPT | GPT-5.6 Sol | **Reasoning**：o1 · o3 · o4-mini；**Coding**：GPT-5-Codex · 5.1-Codex-Max · 5.2/5.3-Codex；**Open weights**：gpt-oss-20b · gpt-oss-120b；**Realtime / Audio**：GPT-Realtime · Transcribe · TTS；**Image / Cyber**：GPT-Image · GPT-5.6 Cyber / Daybreak |
| Anthropic · Claude | Claude Opus 5 | **Capability tiers**：Haiku · Sonnet · Opus；**Hybrid Reasoning**：Claude 3.7+ extended thinking；**Computer Use**：Claude Computer Use；**Special access**：Fable 5 · regulated capability programs |
| Google DeepMind · Gemini | Gemini 3.5 Flash | **Serving tiers**：Pro · Flash · Flash-Lite · Nano；**Deep Think / Computer**：Deep Think · Computer Use；**Image / Omni**：Flash Image · Gemini Omni；**Audio / Live**：Flash Audio · Live · Translate · Transcribe；**Robotics**：Robotics · Robotics-ER · On-Device；**Open sibling**：Gemma · CodeGemma · PaliGemma · ShieldGemma |

## 关键补漏判断

- **DeepSeek**：本地此前几乎只有 V4-Pro；谱系不能因此漏掉 R1、Coder、Math/Prover、VL/Janus 与 OCR 支线。
- **GLM**：已有 4.5V、TTS、OCR，但应把 CogVLM/CodeGeeX/CogView/CogVideoX/AutoGLM 作为历史支系写入地图。
- **Kimi**：已有 VL、K2、Linear、K2.5；缺口主要是 Kimi-Audio、Kimi-Dev 与 Kimina-Prover。
- **Qwen**：本地 Variants 覆盖最完整；需要保持 Coder、VL/VLA、Omni/ASR/TTS、Image、Retrieval 与 Guard 的分支关系。
- **Seed**：除 Seed1.8/2.0 外，必须补 Seed1.5-VL、Seed-OSS/Code、BAGEL、Seed-TTS、Seedream/Seedance、Seed3D，以及 **MedXIAOHE 医疗支线**。
- **GPT**：除 GPT 正代，还要单列 o-series、Codex、gpt-oss、Realtime/Audio、Image/Cyber；这些不应伪装成 GPT 主干新代。
- **Claude**：Haiku/Sonnet/Opus 是能力—成本层；extended thinking、computer use 是能力支线，Claude Code 是产品/agent，不是独立基模。
- **Gemini**：Pro/Flash/Flash-Lite/Nano 是服务层；Deep Think、Computer Use、Audio/Live、Image/Omni、Robotics 是支线；Gemma 是同团队开放 sibling family。

## 一手证据入口

- [OpenAI model catalog](https://developers.openai.com/api/docs/models)
- [Anthropic system cards](https://www.anthropic.com/system-cards)
- [Google DeepMind model cards](https://deepmind.google/models/model-cards/)
- [DeepSeek changelog](https://api-docs.deepseek.com/updates/)
- [Z.ai model overview](https://docs.z.ai/guides/overview/overview)
- [Moonshot AI official repositories](https://github.com/MoonshotAI)
- [Qwen official blog](https://qwenlm.github.io/blog/)
- [ByteDance Seed official repositories](https://github.com/ByteDance-Seed)
- [MedXIAOHE technical report](https://arxiv.org/abs/2602.12705)
