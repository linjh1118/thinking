---
title: "Global Base Model Coverage — 2026-08"
type: insight
tags: [insight, base-model, coverage, timeline]
source: "[[Topics/13_base_model/Base Model MOC]]"
created: 2026-08-31
updated: 2026-08-31
---

# Global Base Model Coverage — 2026-08

> [!tldr]
> 本轮将 Base Model topic 从 15 个已有团队扩为 **22 个厂商团队 + 1 个 research-agent 团队**。这里的“完整”指**团队级主干正代覆盖**，不等于收录每个 API snapshot、参数尺寸、Turbo/Max/Flash SKU 或所有专项模型。

## 编辑口径

- 主树：通用基模正代、团队公认旗舰、改变训练/架构范式的关键节点。
- 支线：Coder、Embedding、ASR/TTS、Robotics、Guard、Image/Video 等进入 Variants 或对应专题。
- 证据：优先 technical report / model card，其次 system card / official docs / official blog。
- 页面：每个叶子都有 overview；已有精读笔记与 Poster 则继续深链，没有则明确标注资料状态。

## 团队覆盖

| 区域 | 团队 | 主干节点 | 当前节点 | 一句话判断 |
|---|---|---:|---|---|
| 海外 | OpenAI · GPT | 12 | GPT-5.6 Sol | 从通用 next-token scaling 走向统一 reasoning、工具调用与专业工作基座。 |
| 海外 | Anthropic · Claude | 12 | Claude Opus 5 | 以 Constitutional AI、安全评估和长时程 agentic coding 为主轴。 |
| 海外 | Google DeepMind · Gemini | 7 | Gemini 3.5 Flash | 原生多模态、超长上下文与推理/工具生态合流。 |
| 海外 | Meta · Llama | 6 | Llama 4 | 开放权重生态从 dense LLM 演进到原生多模态 MoE。 |
| 海外 | xAI · Grok | 10 | Grok-4.6 | 以超大规模训练、实时搜索和 agentic RL 推动闭源旗舰快速迭代。 |
| 海外 | Mistral AI | 8 | Mistral Small 4 | 欧洲开放模型路线：稀疏 MoE、轻量部署、multimodal 与 agentic coding。 |
| 海外 | Microsoft · Phi | 6 | Phi-4 Reasoning Vision | 用高质量合成数据把复杂 reasoning 压进小模型。 |
| 海外 | Amazon · Nova | 3 | Nova 2 | 面向 Bedrock 的多尺寸、多模态、企业可部署模型家族。 |
| 海外 | NVIDIA · Nemotron | 6 | Nemotron 3.5 Lightning | 开放模型 + 数据 + recipe + 推理栈共同服务 enterprise agents。 |
| 海外 | Cohere · Command | 4 | Command A | 围绕 enterprise RAG、tool use、多语言与私有部署优化。 |
| 海外 | IBM · Granite | 7 | Granite 4.0 | 以透明数据、企业安全、RAG/tool use 和混合 SSM 效率为核心。 |
| 国内 | Alibaba · Qwen | 8 | Qwen3.8 | 统一 thinking/non-thinking，继而走向原生多模态、稀疏高效和 1M context。 |
| 国内 | DeepSeek AI | 9 | DeepSeek-V4 Pro | MLA/MoE 训练效率、开放 reasoning RL 与 agentic tool-use 是三条主轴。 |
| 国内 | Baidu · ERNIE | 7 | ERNIE 5.1 | 知识增强预训练演进到统一多模态 MoE 与异步 agentic RL。 |
| 国内 | Tencent · Hunyuan | 5 | Hunyuan-A13B | 腾讯云产品化、MoE 效率、hybrid reasoning 与开放权重并行推进。 |
| 国内 | ByteDance · Seed | 4 | Seed2.0 | 从多模态理解走向真实环境 agency 与 computer use。 |
| 国内 | Zhipu · GLM | 9 | GLM-5.3 Flash | General Language Model 演进为 agentic reasoning/coding 原生基座。 |
| 国内 | Moonshot · Kimi | 7 | Kimi K2.6 | 超长上下文底座逐步转向开放 MoE、视觉 agent 与 agent swarm。 |
| 国内 | MiniMax | 6 | MiniMax-M3 | 长上下文 attention 效率与真实环境 agent RL 双线合流。 |
| 国内 | Xiaomi · MiMo | 6 | MiMo-V2.5-Pro | 小型 reasoning base 演进为低激活、长上下文、全模态 agent family。 |
| 国内 | Meituan · LongCat | 6 | LongCat-Next | 稳定 560B MoE 基座上扩展 thinking、agent、omni 与 formal reasoning。 |
| 国内 | StepFun · Step | 4 | Step-3.5-Flash | 大规模 MoE、推理效率与专项 agent/reasoning family。 |
| 国内 | MiroMind · MiroThinker | 2 | MiroThinker 1.7 | 以 interaction scaling 和 verification agent 构建 research-agent 基模。 |

## 本轮新增的 P0/P1 团队

DeepSeek、xAI、Mistral、Tencent Hunyuan、Amazon Nova、NVIDIA Nemotron、Cohere Command、IBM Granite、Microsoft Phi；并补齐 Anthropic Claude Opus 5 与 OpenAI GPT-5.6 当前节点。

## 仍不应声称“全收录”的边界

- 未把每个尺寸、服务层、dated API snapshot 拆成独立叶子。
- 华为盘古、商汤日日新等公开一手技术材料不足或产品口径难以稳定映射到独立主干正代，暂列候补，不混入已核验主树。
- 专项生成模型与 physical/world models 不属于本轮通用基模主树。
