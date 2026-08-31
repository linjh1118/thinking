---
title: "Base Model Top 8 Mainline Audit — 2026-08-31"
type: insight
tags: [insight, base-model, top8, mainline, audit]
source: "[[Topics/13_base_model/Base Model MOC]]"
created: 2026-08-31
updated: 2026-08-31
---

# Base Model Top 8 Mainline Audit — 2026-08-31

> [!tldr]
> 本审计只收国内 Top 5（DeepSeek、GLM、Kimi、Qwen、Seed）和海外 Top 3（GPT、Claude、Gemini）的正式主系列与主部署 checkpoint。Coder、VL、Audio、Image、Embedding、Pro/Flash/mini 等纯能力层或成本 SKU 不单独拆叶；但官方把小数版本或命名 checkpoint 作为主模型更新时必须保留。

## 判定口径

纳入：

- 官方正式发布的整数代、小数代和主部署 checkpoint。
- 官方页面明确描述为上一主模型的 successor、upgrade 或线上默认模型替换。
- Qwen3-Next 这类被官方明确写入后续正代架构演进的过渡主节点。

不纳入：

- Coder、VL、Audio、Image、Embedding、Robotics 等专项支线。
- 同一代的参数尺寸、Mini/Nano/Air/Flash-Lite 等成本层 SKU。
- preview endpoint、临时高算力 sibling 或纯产品功能。

MedXIAOHE 按既有编辑约定作为 Seed 时间线中的普通模型保留，不赋予特殊主线标签。

## 逐团队结论

| 团队 | 核验后的正代/主 checkpoint | 本轮纠错与补漏 |
|---|---|---|
| DeepSeek | DeepSeek LLM → V2 → V2.5 → V2.5-1210 → V3 → R1 → V3-0324 → R1-0528 → V3.1 → V3.1-Terminus → V3.2-Exp → V3.2 → V4 | 补 V2.5-1210、V3-0324、R1-0528；删除重复且日期错误的 V4 Pro 叶 |
| GLM | GLM-130B → ChatGLM → ChatGLM2 → ChatGLM3 → GLM-4 → 4.5 → 4.6 → 4.7 → 5 → 5.1 → 5.2 → 5.3 | 补 ChatGLM、ChatGLM2 |
| Kimi | Moonshot v1 → Kimi k1.5 → K2 → K2-Instruct-0905 → K2 Thinking → K2.5 → K2.6 → K3 | 补 K2-Instruct-0905、K2 Thinking；Kimi-VL、Kimi Linear 移出正代 |
| Qwen | Qwen → 1.5 → 2 → 2.5 → 3 → 3-Next → 3.5 → 3.6 → 3.7 → 3.8 | 补 Qwen3-Next |
| Seed | Seed1.5 → 1.6 → 1.8 → Seed2.0 → Seed2.1；另保留 MedXIAOHE | 主系列与官网 Foundation Models 列表一致 |
| GPT | GPT-1 → 2 → 3 → 3.5 → 4 → 4 Turbo → 4o → 4.5 → 4.1 → 5 → 5.1 → 5.2 → 5.3 → 5.4 → 5.5 → 5.6 | 补 GPT-4 Turbo、GPT-5.3 |
| Claude | Claude 1 → 2 → 2.1 → 3 → 3.5 Sonnet → 3.7 Sonnet → 4 → Opus 4.1 → Sonnet 4.5 → Opus 4.5 → Sonnet 4.6 → Opus 4.6 → Opus 4.7 → Opus 4.8 → Sonnet 5 → Opus 5 | 补 Sonnet 4.5、Sonnet 4.6，避免只保留 Opus 而丢失正式主模型 |
| Gemini | Gemini 1.0 → 1.5 Pro → 2.0 → 2.5 Pro → 3 Pro → 3.1 Pro → 3.5 Flash → 3.6 Flash → 3.7 Flash | 使用官方真实型号，不再用模糊 family 标签代替 Pro/Flash 名称；修正 3.5 发布时间 |

## 关键一手证据

- [DeepSeek changelog](https://api-docs.deepseek.com/updates/)
- [Z.ai release notes](https://docs.z.ai/release-notes/new-released)
- [Kimi Research Blog](https://www.kimi.com/en/blog/)
- [Qwen3.8 official repository and release history](https://github.com/QwenLM/Qwen3.8)
- [ByteDance Seed Foundation Models](https://seed.bytedance.com/en/models)
- [OpenAI model catalog](https://developers.openai.com/api/docs/models/all)
- [Anthropic system cards](https://www.anthropic.com/system-cards)
- [Gemini API model catalog](https://ai.google.dev/gemini-api/docs/models)

## 编辑判断

这一轮的主要问题不是“少补了几个最新旗舰”，而是此前把“正代”错误理解成了每个团队只挑少数代表节点。正确做法是：主树可以不收支线，但不能吞掉官方正式的小数代、主部署 checkpoint 和同一能力主线中的正式 Sonnet/Opus 更新。
