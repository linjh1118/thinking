---
title: "Base Model MOC — 大模型基座全景图"
type: moc
tags: [moc, base-model, llm, foundation-model]
created: 2026-05-30
updated: 2026-08-27
---

# Base Model MOC — 大模型基座全景图

> 📚 **时间窗口**: 2025-05 至 2026-06
> **来源**: 官方技术报告 / System Card / Model Card / 官方博客 / GitHub
> **深度洞察**: [[Topics/13_base_model/Base_Model_Insight]] — 数据/架构/训练策略全景分析

---

## TL;DR

2025-2026 年的大模型军备竞赛已从「参数规模」转向四大技术主线：**Reasoning 进入基座**、**Agentic RL 训练**、**全模态基座**、**Coding Agent 主战场**。国内 Qwen、MiniMax、Kimi、GLM、ERNIE 分别代表不同工业路线；国外 OpenAI、Anthropic、Google 形成 trifecta。

---

## 核心概念

| 概念 | 定义 |
|------|------|
| **Base Model / Foundation Model** | 在大规模无监督数据上预训练的通用模型，可微调适配多种任务 |
| **Thinking Model** | 内置推理链的模型，支持 test-time compute 扩展 |
| **MoE (Mixture of Experts)** | 稀疏激活架构，总参数量大但每次推理只激活小部分 |
| **Agentic RL** | 在真实任务环境中用强化学习训练 agent 能力 |
| **Computer Use** | 模型直接操作计算机/浏览器的能力 |

---

## 国内公司

### 🏢 Zhipu / GLM

| 月份 | 模型 | 原文类型 | arXiv ID | 架构 / 参数 | 核心关键词 |
|------|------|----------|----------|-------------|-----------|
| 2025-07 | GLM-4.1V-Thinking | Technical Report | 2507.01006 | VLM | multimodal reasoning, RLCS, VLM agent |
| 2025-07 | GLM-4.5V | Technical Report | 2507.01006 | VLM | multimodal reasoning, coding, VLM agents |
| 2025-07/08 | GLM-4.5 | Official blog + TR | 2508.06471 | MoE, 355B/32B | agentic, reasoning, coding, thinking/direct modes |
| 2025-07/08 | GLM-4.5-Air | Technical Report | 2508.06471 | MoE, 106B compact | efficient ARC model, reasoning |
| 2025-12 | GLM-TTS | Technical Report | 2512.14291 | TTS system | speech generation, GRPO reward |
| 2026-03 | GLM-OCR | Technical Report | 2603.10910 | 0.9B multimodal OCR | document parsing, table recovery |
| 2026-04 | GLM-5.1 | Official blog | — | 未公开 | long-horizon, agentic engineering, coding |
| 2026-06 | GLM-5.2 | Official blog + HF | — | 未公开 | solid 1M context, IndexShare, MTP, long-horizon coding, anti-hack RL |
| 2026-08 | GLM-5.3-Flash | Official docs + blog + HF | — | MoE, 320B/18B, 45 layers | native multimodal, 1M context, IndexPool, mHC, agentic coding |
| 未明确 | GLM-4.7 | Official dev docs | — | 未公开 | coding, tool use, BrowseComp, interleaved reasoning |

> **主线**: `GLM-4.5 = Agentic / Reasoning / Coding 基座` → `GLM-5.1/4.7 = Long-horizon agent + coding agent` → `GLM-5.2 = 1M context long-horizon coding agent` → `GLM-5.3-Flash = 原生多模态 + 成本/速度 Pareto 优化`
> **GLM-5.2 笔记**: [[Topics/13_base_model/Zhipu_GLM/2606_GLM_5_2/GLM-5.2-Long-Horizon-Coding-Agent]]
> **GLM-5.3-Flash 笔记**: [[Topics/13_base_model/Zhipu_GLM/2608_GLM_5_3_Flash/GLM-5.3-Flash]]

---

### 🏢 Baidu / ERNIE

| 月份 | 模型 | 原文类型 | arXiv ID | 架构 / 参数 | 核心关键词 |
|------|------|----------|----------|-------------|-----------|
| 2019-04 | ERNIE | arXiv source | 1904.09223 | BERT-era encoder | knowledge integration, entity/phrase masking |
| 2019-07 | ERNIE 2.0 | arXiv source | 1907.12412 | continual pretraining framework | multi-task continual pretraining, language understanding |
| 2021-07 | ERNIE 3.0 | arXiv source | 2107.02137 | knowledge-enhanced PLM | understanding + generation, knowledge memory |
| 2021-12 | ERNIE 3.0 Titan | arXiv source | 2112.12731 | larger-scale knowledge-enhanced PLM | large-scale pretraining, distributed inference |
| 2022-12 | ERNIE-Code | arXiv source | 2212.06742 | code LM | multilingual programming languages, code pretraining |
| 2023-01 | ERNIE 3.0 Tiny | arXiv source | 2301.03416 | distilled small model | task-agnostic distillation, generalization |
| 2023-05/07 | ERNIE 3.5 | Baidu PRNewswire | — | 未公开 | industrial foundation model, throughput/QPS |
| 2023-10 | ERNIE 4.0 | Baidu PRNewswire | — | 未公开 | understanding, generation, reasoning, memory |
| 2024-06 | ERNIE 4.0 Turbo | Baidu PRNewswire | — | 未公开 | lower cost, faster response |
| 2025-03/06 | ERNIE 4.5 | Official blog + TR | — | heterogeneous multimodal MoE, up to 424B/47B active | native multimodal, MoE, ERNIEKit, FastDeploy |
| 2025-03/04 | ERNIE X1 / X1 Turbo | Baidu PRNewswire | — | reasoning model | deep thinking, multimodal, tool invocation, low cost |
| 2026-02 | ERNIE 5.0 | Technical Report + official blog | 2602.04705 | ultra-sparse MoE, 2.4T | unified multimodal, next-group-of-tokens prediction, elastic training |
| 2026-05 | ERNIE 5.1 | Official blog | — | ERNIE 5.0-derived compact model | elastic pretraining, disaggregated async RL, scaled agentic post-training |

> **主线**: `ERNIE 1/2/3 = knowledge-enhanced pretraining` → `ERNIE 4.5 = open multimodal heterogeneous MoE` → `ERNIE 5.0 = unified multimodal autoregressive model` → `ERNIE 5.1 = elastic sub-model inheritance + fully-asynchronous agentic RL`
> **系列笔记**: [[Topics/13_base_model/Baidu_ERNIE/ERNIE-Series-Summary|Baidu ERNIE Series Summary]]

---

### 🏢 MiniMax

| 月份 | 模型 | 原文类型 | arXiv ID | 架构 / 参数 | 核心关键词 |
|------|------|----------|----------|-------------|-----------|
| 2025-06 | MiniMax-M1 | Technical Report | 2506.13585 | hybrid MoE, 456B/45.9B | 1M context, Lightning Attention, CISPO RL |
| 2025-10 | MiniMax-M2 | Official blog + GitHub | — | MoE, ~230B/10B | coding agent, agentic workflows, open-source |
| 2026-01 | MiniMax-M2.1 | Official blog + GitHub | — | MoE, ~230B/10B | agent post-training, SWE scaling, AppDev |
| 2026-02 | MiniMax-M2.5 | Official blog + GitHub | — | 未完整公开 | real-world RL, coding, tool use, office tasks |
| 2026-03 | MiniMax-M2.7 | Official blog | — | 未完整公开 | self-evolution, autonomous debugging |
| 2026-05 | MiniMax-M2 Series | Technical Report | 2605.26494 | MoE, 229.9B/9.8B | Forge RL, agentic coding, cowork, self-evolution |
| 2026-06 | MiniMax-M3 | Official blog + API docs | — | MSA sparse attention, 1M context | frontier coding, native multimodality, computer use |

> **主线**: M1 解决 **long-context + reasoning RL**，M2 系列转向 **coding / office / search / cowork agent**，M3 则把 agent 能力推到 **1M context + native multimodality + sparse attention**。

---

### 🏢 Xiaomi / MiMo

| 月份 | 模型 | 原文类型 | arXiv ID | 架构 / 参数 | 核心关键词 |
|------|------|----------|----------|-------------|-----------|
| 2025-05 | MiMo-7B | Technical Report | 2505.07608 | Dense 7B | 25T tokens, reasoning pretraining, MTP, 130K RL data |
| 2025-06 | MiMo-VL-7B | Technical Report | 2506.03569 | 7B VLM | 2.4T multimodal tokens, MORL, visual grounding |
| 2025-11 | MiMo-Embodied | Technical Report | 2511.16518 | VLM | embodied AI + autonomous driving, CoT/RL finetuning |
| 2025-12 | MiMo-VL-Miloco | Technical Report | 2512.17436 | 7B home-centric VLM | smart-home, SFT + GRPO, token-budget-aware reasoning |
| 2026-01 | MiMo-V2-Flash | Technical Report | 2601.02780 | MoE, 309B/15B | Hybrid SWA, 256K, MTP, MOPD |
| 2026-03 | MiMo-V2-Pro | Official blog | — | MoE, >1T/42B | 1M context, OpenClaw, agentic workloads |
| 2026-03 | MiMo-V2-Omni | Official blog | — | Omnimodal | image/video/audio/text, tool calling, UI grounding |
| 2026-04 | MiMo-V2.5 | Official blog + HF | — | MoE, 310B/15B | 1M context, omnimodal agent, RL + MOPD |
| 2026-04 | MiMo-V2.5-Pro | Official blog + HF | — | MoE, 1.02T/42B | long-horizon agent, coding, 27T tokens, FP8 |

> **主线**: `MiMo-7B = reasoning base` → `MiMo-VL = multimodal grounding` → `MiMo-Embodied = physical-world reasoning` → `MiMo-V2 = MoE + long-context agent` → `MiMo-V2.5 = open omnimodal agent`。
> **系列笔记**: [[Topics/13_base_model/Xiaomi_MiMo/MiMo-Summary|MiMo Series Summary]]

---

### 🏢 Alibaba / Qwen

| 月份 | 模型 | 原文类型 | arXiv ID | 架构 / 参数 | 核心关键词 |
|------|------|----------|----------|-------------|-----------|
| 2025-05* | Qwen3 | Technical Report | 2505.09388 | Dense + MoE, 0.6B–235B | thinking/non-thinking unified, multilingual |
| 2025-06 | Qwen3 Embedding/Reranker | Official GitHub | — | 0.6B/4B/8B | embedding, reranking, multilingual |
| 2025-07 | Qwen3-Coder | Official GitHub | — | 多尺寸, 含 480B-A35B | agentic coding, software workflows |
| 2025-09 | Qwen3-Omni | Technical Report | 2509.17765 | Thinker-Talker MoE | text-image-audio-video, real-time speech |
| 2026-01 | Qwen3-TTS | Technical Report | 2601.15621 | dual-track LM TTS | controllable TTS, voice cloning |
| 2026-01 | Qwen3-ASR | Technical Report | 2601.21337 | ASR family | 52 languages, forced aligner |
| 2026-02 | Qwen3.5 | Official GitHub | — | 含 397B-A17B MoE 等 | next-generation open models |
| 2026-03 | Qwen3-Coder-Next | Technical Report | 2603.00729 | MoE, 80B/3B | coding agents, RL from feedback |
| 2026-04 | Qwen3.5-Omni | Technical Report | 2604.15804 | Hybrid Attention MoE, 256K | omni-modality, AV vibe coding |
| 2026-04 | Qwen3.6 | Official GitHub | — | 27B/35B-A3B 等 | open models |
| 2026-08 | Qwen3.8 family | Official model pages + blog + model card | — | Max 2.4T MoE；Flash 125B/6B active + 51B n-gram | 1M context, native multimodality, sparse attention, built-in tools |

> **正代主线**: `Qwen3 = thinking/no-thinking 统一` → `Qwen3.5/3.6 = next-gen open models` → `Qwen3.8 = 原生多模态 + 1M context + 稀疏高效架构`。Coder、Omni、Embedding、ASR、TTS 等任务/模态支线统一收进 `Variants/`。
>
> **导航**: [[Topics/13_base_model/Alibaba_Qwen/Qwen-Mainline-Index|Qwen 正代与支线索引]] · [[Topics/13_base_model/Alibaba_Qwen/2608_Qwen3_8/Qwen3.8-Family|Qwen3.8 Family]] · [[Topics/13_base_model/Alibaba_Qwen/2608_Qwen3_8/Qwen3.8-Flash|Qwen3.8-Flash 精读]]

---

### 🏢 Moonshot / Kimi

| 月份 | 模型 | 原文类型 | arXiv ID | 架构 / 参数 | 核心关键词 |
|------|------|----------|----------|-------------|-----------|
| 2025-07 | Kimi K2 | Technical Report | 2507.20534 | MoE, 1T/32B | MuonClip, agentic intelligence, coding |
| 2025-10 | Kimi Linear | Technical Report | 2510.26692 | hybrid linear attention, 48B/3B | Kimi Delta Attention, 1M context, 6× throughput |
| 2026-02 | Kimi K2.5 | Technical Report | 2602.02276 | open multimodal agentic | visual agentic, joint text-vision RL, Agent Swarm |
| 2026-04 | Kimi K2.6 | Model card | — | 1T MoE/32B, 256K | open-source coding, scaling agentic |
| 未明确 | Kimi-VL | Official GitHub | — | MoE VLM, 2.8B active | multimodal reasoning, agent capabilities |

> **主线**: K2 开始就是 **open agentic intelligence**，K2.5 合入视觉+多模态+Agent Swarm，Linear 是底层架构线让超长上下文更便宜

---

### 🏢 Meituan / LongCat

| 月份 | 模型 | 原文类型 | arXiv ID | 架构 / 参数 | 核心关键词 |
|------|------|----------|----------|-------------|-----------|
| 2025-09 | **LongCat-Flash** | Technical Report | 2509.01322 | MoE, 560B/27B avg | Zero-Comp Experts, ScMoE, variance alignment, agentic foundation |
| 2025-09 | LongCat-Flash-Thinking | Technical Report | 2509.18883 | MoE, 560B/27B | long CoT cold-start, Domain-Parallel RL, DORA (>3× speedup) |
| 2025-11 | LongCat-Flash-Omni | Technical Report | 2511.00279 | MoE, 560B + ~1.8B 模态模块 | omni-modal, real-time audio-visual (<100ms) |
| 2026-01 | LongCat-Flash-Thinking-2601 | Technical Report | 2601.16725 | MoE, 560B/27B | agentic search, tool use, robust RL with noise, 1M context |
| 2026-01 | LongCat-Flash-Lite | Technical Report | 2601.21204 | MoE, 68.5B/3B avg | scaling embeddings > scaling experts, N-gram embedding scaling |
| 2026-03 | LongCat-Flash-Prover | Technical Report | 2603.21065 | MoE, 560B/27B | Lean4 formal reasoning (MiniF2F 97.1%), HisPO, tool-integrated RL |
| 2026-03 | LongCat-Next | Technical Report | 2603.27538 | DiNA decoder-only MoE | lexicalizing modalities as discrete tokens, dNaViT, native unified omni |

> **主线**: 一个 560B MoE 基座（Flash）+ 六方向扩展（thinking / agent / small / omni / formal / next-gen）。三个核心判断：
> (1) **架构稳定** — 全系列继承 Zero-Comp Experts + ScMoE，扩展都在训练 recipe / 模态模块 / tokenizer 层，没推倒过基座；
> (2) **RL 三段进化** — Flash-Thinking (Domain-Parallel) → Thinking-2601 (Robust+Noise) → Prover (Tool-Integrated + HisPO)，是工业级 RL 训 base model 的教科书案例；
> (3) **Omni 范式分歧** — Flash-Omni 走 encoder-decoder 拼接，LongCat-Next 押注原生离散 token 统一，后者是美团下一代主线。
> **系列 MOC**: [[Topics/13_base_model/Meituan_LongCat/Meituan LongCat Series MOC|Meituan LongCat Series MOC]]

---

## Agent 训练方法（新增）

### 🏢 Research Agent / Agentic RL

| 月份 | 模型 | 原文类型 | arXiv ID | 核心关键词 |
|------|------|----------|----------|-----------|
| 2026-03 | Qwen3-Coder-Next | Technical Report | 2603.00729 | RL from feedback, tool chat template scaling, reward hacking blocker |
| 2026-03 | MiroThinker-1.7 & H1 | Technical Report | 2603.15726 | Verification agent (local + global), research agent |
| 2026-03 | MiroThinker v1.0 | Technical Report | 2511.11793 | Interaction scaling, 600 tool calls/task |
| 2025-08 | rStar2-Agent | Technical Report | 2508.20722 | GRPO-RoC, 14B SOTA math, 510 RL steps |
| 2025-02 | Agentic Reasoning | Technical Report | 2502.04644 | Mind-Map agent, web search, deep research |

> **主线**: Agentic RL 训练范式收敛：GRPO/CISPO + Verification + Interaction Scaling

### 🏢 Agent Foundation Models（字节跳动）

| 月份 | 模型 | 原文类型 | 核心关键词 |
|------|------|----------|-----------|
| 2026-03 | Seed1.8 | Model Card | Real-world agency, GAIA 93.2, thinking modes |
| 2026-05 | Seed2.0 | Model Card | Agent foundation model, Computer Use |

> **主线**: **Agent Foundation Model** 概念——为 agent 场景专门优化的 base model

---

## 国外公司

### 🏢 OpenAI / GPT

| 月份 | 模型 | 原文类型 | arXiv ID | 架构 / 参数 | 核心关键词 |
|------|------|----------|----------|-------------|-----------|
| 2025-08 | GPT-5 | System Card + arXiv | 2601.03267 | 未公开 | unified reasoning, router, coding, health |
| 2025-08 | gpt-oss-120B/20B | Model Card | — | open-weight reasoning | efficient deployment |
| 2025-09 | GPT-5-Codex | System card | — | GPT-5 variant | agentic coding, tests-until-pass |
| 2025-11 | GPT-5.1 | Official release | — | 未公开 | adaptive reasoning, prompt caching |
| 2025-11 | GPT-5.1-Codex-Max | System Card | — | Codex-specialized | agent sandboxing, coding safety |
| 2025-12 | GPT-5.2 | Official release | — | GPT-5 series | professional work, SWE-Bench Pro |
| 2026-02 | GPT-5.3-Codex | Official release | — | Codex-specialized | long-running tasks, research, tool use |
| 2026-03 | GPT-5.3 Instant | System Card | — | Instant model | faster everyday, web-search |
| 2026-03 | GPT-5.4 Thinking | System Card | — | reasoning model | cybersecurity, general-purpose |
| 2026-03 | GPT-5.4 | Official release | — | 未公开 | coding, computer use, knowledge work |
| 2026-04 | GPT-5.5 | Official release | — | 未公开 | complex real-world work, coding, research |
| 2026-05 | GPT-5.5 Instant | Official release | — | Instant model | factuality, personalization |

> **主线**: `GPT-5 unified system` → `Codex agentic coding` → `5.2 professional work` → `5.3/5.4 reasoning & coding` → `5.5 complex real-world work`

---

### 🏢 Anthropic / Claude

| 月份 | 模型 | 原文类型 | arXiv ID | 架构 / 参数 | 核心关键词 |
|------|------|----------|----------|-------------|-----------|
| 2025-05 | Claude Sonnet 4 / Opus 4 | System Card | — | 未公开 | hybrid reasoning, coding, agent tasks |
| 2025-08 | Claude Opus 4.1 | System Card | — | 未公开 | stronger Opus 4 line |
| 2025-09 | Claude Sonnet 4.5 | System Card | — | 未公开 | agentic safety, autonomous work |
| 2025-10 | Claude Haiku 4.5 | System Card | — | 未公开 | Sonnet-level coding at lower cost |
| 2025-11 | Claude Opus 4.5 | System Card | — | 未公开 | coding, agents, computer use |
| 2026-02 | Claude Sonnet 4.6 / Opus 4.6 | System Card | — | 未公开 | agents, 1M context beta, large output |
| 2026-04 | Claude Opus 4.7 | System Card | — | 未公开 | advanced software engineering |
| 2026-04 | Mythos Preview | System Card | — | 未公开 | Anthropic preview model |

> **主线**: 密集迭代 4.5→4.6→4.7，主打 **coding agent / computer use / long-horizon autonomous work / safety eval**

---

### 🏢 Google DeepMind / Gemini

| 月份 | 模型 | 原文类型 | arXiv ID | 架构 / 参数 | 核心关键词 |
|------|------|----------|----------|-------------|-----------|
| 2025-06 | Gemini 2.5 Pro / Flash / Flash-Lite | Technical Report | 2507.06261 | 未公开 | thinking model, multimodal, 3h video |
| 2025-08 | Gemini 2.5 Deep Think | Model Card | — | 未公开 | enhanced reasoning mode |
| 2025-10 | Gemini 2.5 Computer Use | Model Card | — | 未公开 | computer use, agentic browser |
| 2025-10 | Gemini Robotics 1.5 | Technical Report | 2510.03342 | VLA | embodied agent, motion transfer |
| 2025-11 | Gemini 3 Pro | Model Card | — | 未公开 | natively multimodal reasoning |
| 2025-12 | Gemini 3 Flash | Official release | — | 未公开 | Pro-grade reasoning at Flash speed |
| 2026-02 | Gemini 3.1 Pro | Model Card | — | 未公开 | advanced multimodal reasoning |

> **主线**: `Gemini 2.5 thinking` → `Computer Use` → `Gemini 3/3.1 multimodal reasoning` → `Robotics embodied reasoning`

---

### 🏢 Meta / Llama

| 月份 | 模型 | 原文类型 | arXiv ID | 架构 / 参数 | 核心关键词 |
|------|------|----------|----------|-------------|-----------|
| 2025-04* | Llama 4 Scout | Official blog | — | MoE, 17B active/16 experts | open-weight, native multimodal, long context |
| 2025-04* | Llama 4 Maverick | Official blog | — | MoE, 17B active/128 experts | open-weight, native multimodal, MoE |
| 2025-04* | Llama 4 Behemoth | Official preview | — | 未完整公开 | teacher model, frontier MoE preview |
| 2025-04* | Llama Guard 4 | HF model card | — | 12B multimodal | multimodal safety |
| 2026-01 | Llama 4 Herd compilation | Secondary arXiv | 2601.11659 | 汇总信息 | architecture/training/evaluation notes |

> **注意**: Llama 4 是 2025-04，严格不在 2025-05 之后。但作为"最近一代 Llama 基座"保留。
> **主线**: 从 Llama 3 dense 转向 **MoE + native multimodal + long context**

---

## 技术主线总结

| 主线 | 代表模型 | 核心洞察 |
|------|---------|---------|
| **Reasoning 进入 Base Model** | GPT-5, Gemini 2.5, Qwen3, GLM-4.5, MiniMax-M1 | 推理能力从 post-training 上移到预训练基座 |
| **Agentic RL** | Kimi K2/K2.5, MiniMax M2系列, Qwen3-Coder-Next, GLM-5.2, rStar2, Agentic Reasoning | 在真实任务环境中用 RL 训练 agent 能力 |
| **全模态基座** | Gemini 3/3.1, Qwen3-Omni/3.5-Omni, GLM-4.5V, Kimi K2.5, Llama 4 | 统一处理 text/image/audio/video 的原生多模态 |
| **Coding Agent 主战场** | Claude 4.5/4.6/4.7/4.8, GPT-5-Codex/5.3-Codex, Qwen3-Coder-Next, GLM-5.2, MiniMax M2/M3, Kimi K2.6 | coding 是 frontier model 必争之地 |
| **1M Long-Horizon Agent** | MiniMax M3, MiMo-V2.5-Pro, GLM-5.2 | 长上下文从静态读取转向持续工程执行，瓶颈迁移到 KV cache、compaction、rollout 和 anti-hack |
| **Verification Agent** | MiroThinker-H1, Agentic Reasoning | 中间推理步骤验证 + 整体轨迹审计 |
| **Interaction Scaling** | MiroThinker v1.0 | 交互深度作为第三 scaling 维度（model size, context, interaction） |
| **Agent Foundation Model** | Seed1.8, Seed2.0 | 为 agent 场景专门优化的 base model |

---

## 横向对比文档

### 基础维度（Pretrain / SFT / RL / 架构 / 评测 / 推理）

- [[Topics/13_base_model/Base_Model_Pretraining_Comparison|Base Model Pretraining Comparison]] — Reasoning、multimodal、agent trajectory 是在哪个训练阶段进入模型的？
- [[Topics/13_base_model/Base_Model_SFT_PostTraining_Comparison|Base Model SFT and Post-training Comparison]] — SFT、expert distillation、domain specialization、self-distillation 如何分工？
- [[Topics/13_base_model/Base_Model_RL_Comparison|Base Model RL Comparison]] — GRPO、CISPO、GRPO-RoC、RLCS、MOPD、Forge、Self-Critique 分别解决什么问题？
- [[Topics/13_base_model/Base_Model_Architecture_Comparison|Base Model Architecture Comparison]] — MoE、hybrid/linear/sparse attention、MTP、omni architecture 如何影响 agent 能力？
- [[Topics/13_base_model/Base_Model_Agent_Evaluation_Comparison|Base Model Agent and Evaluation Comparison]] — Coding、research、tool-use、real work harness 应该如何公平比较？
- [[Topics/13_base_model/Base_Model_Inference_Productization_Comparison|Base Model Inference and Productization Comparison]] — 模型如何以承受成本跑完长程真实任务？

### ⭐ Agentic 专题维度（2026-06-14 新增）

- [[Topics/13_base_model/Base_Model_Agentic_Data_Synthesis_Comparison|Base Model Agentic Data Synthesis Pipeline Comparison]] — 七条主流 pipeline（K2 三层 / Qwen3-CN 三源 / Step-DR 原子能力 / Step-GUI CSRS / GE-Lab 仿真 / M2 artifact / rStar2 GRPO-RoC）对比
- [[Topics/13_base_model/Base_Model_Agent_Memory_State_Comparison|Base Model Agent Memory and Long-Horizon State Comparison]] — 六类状态管理范式（Interleaved Thinking / Agent Swarm / Discard-all / Block Sparse / Mind-Map / 物理降本）对比
- [[Topics/13_base_model/Base_Model_Verification_Critique_Comparison|Base Model Verification and Self-Critique Architecture Comparison]] — 七类 verifier 设计（Local+Global / Self-Critique Rubric / CSRS / Checklist Judger / Hacking Blocker / Synthesis / GenRM+MetaRM）对比
- [[Topics/13_base_model/Base_Model_Self_Evolution_Comparison|Base Model Self-Evolution and Iterative Improvement Comparison]] — 五类自进化范式（改 scaffold / Rollout 飞轮 / Self-distillation / Closed-loop Critic / Interaction Scaling）对比

### 元维度

- [[Topics/13_base_model/Base_Model_Coverage_Gaps|Base Model Coverage Gaps]] — BaseModel topic 还缺哪些公司、证据类型和分析维度？

---

## 自动索引

```dataview
TABLE title, year, venue, status
FROM "Topics/13_base_model"
WHERE type = "paper"
SORT title ASC
```

---

## 官方原始资料

- [[Topics/13_base_model/Zhipu_GLM/2508_GLM_4_5/src/GLM-4.5 - Z.ai Blog|GLM-4.5 官方博客剪藏]] — GLM-4.5 的 reasoning / coding / agentic 能力与训练细节
- [[Topics/13_base_model/Zhipu_GLM/2509_GLM_4_7/src/GLM-4.7 - Z.AI Docs|GLM-4.7 开发者文档剪藏]] — coding、tool use 与 interleaved reasoning
- [[Topics/13_base_model/Zhipu_GLM/2604_GLM_5_1/src/GLM-5.1 - Z.ai Blog|GLM-5.1 官方博客剪藏]] — long-horizon tasks 与 agentic engineering
- [[Topics/13_base_model/Zhipu_GLM/2606_GLM_5_2/src/GLM-5.2 - Z.ai Blog|GLM-5.2 官方博客剪藏]] — solid 1M context、IndexShare、MTP、slime、critic-based PPO 与 anti-hack RL
- [[Topics/13_base_model/Zhipu_GLM/2608_GLM_5_3_Flash/src/00_Source_Index|GLM-5.3-Flash 官方资料索引]] — 中英开发文档、技术博客、模型卡、API、价格及本地化图片
- [[Topics/13_base_model/MiniMax/2510_MiniMax_M2/src/MiniMax-M2 - Official Blog|MiniMax-M2 官方博客剪藏]] — coding agent 与 agentic workflows
- [[Topics/13_base_model/MiniMax/2512_MiniMax_M2_1/src/MiniMax-M2.1 - Official Blog|MiniMax-M2.1 官方博客剪藏]] — agent 场景后训练与 SWE scaling
- [[Topics/13_base_model/MiniMax/2602_MiniMax_M2_5/src/MiniMax-M2.5 - Official Blog|MiniMax-M2.5 官方博客剪藏]] — real-world productivity、agentic RL 与 Forge 框架
- [[Topics/13_base_model/MiniMax/2603_MiniMax_M2_7/src/MiniMax-M2.7 - Official Blog|MiniMax-M2.7 官方博客剪藏]] — self-evolution 与 autonomous debugging
- [[Topics/13_base_model/MiniMax/2606_MiniMax_M3/src/MiniMax-M3 - Official Blog|MiniMax-M3 官方博客剪藏]] — MSA、1M context、native multimodality 与 frontier coding
- MiniMax-M3 AI Coding Tools 文档剪藏 — 待补；Claude Code、OpenCode、Cursor 等工具接入方式
- MiniMax-M3 Tool Use 文档剪藏 — 待补；interleaved thinking 与多轮 tool use 历史保留
- [[Topics/13_base_model/Xiaomi_MiMo/2603_MiMo_V2_Pro/src/MiMo-V2-Pro - Xiaomi Blog|MiMo-V2-Pro 小米官方剪藏]] — 1T+ MoE、42B active、1M context 与 OpenClaw agent 场景
- [[Topics/13_base_model/Xiaomi_MiMo/2603_MiMo_V2_Omni/src/MiMo-V2-Omni - Xiaomi Blog|MiMo-V2-Omni 小米官方剪藏]] — image/video/audio/text、tool calling、function execution 与 UI grounding
- [[Topics/13_base_model/Xiaomi_MiMo/2604_MiMo_V2_5/src/MiMo-V2.5 - Xiaomi Blog|MiMo-V2.5 小米官方剪藏]] — 310B/15B omnimodal agent、48T tokens、1M context 与 RL+MOPD
- [[Topics/13_base_model/Xiaomi_MiMo/2604_MiMo_V2_5_Pro/src/MiMo-V2.5-Pro - Xiaomi Blog|MiMo-V2.5-Pro 小米官方剪藏]] — 1.02T/42B long-horizon agent、coding 与 hybrid attention
- [[Topics/13_base_model/Alibaba_Qwen/Variants/2506_Qwen3_Embedding/src/Qwen3-Embedding - GitHub|Qwen3 Embedding/Reranker GitHub 剪藏]] — multilingual embedding 与 reranking
- [[Topics/13_base_model/Alibaba_Qwen/Variants/2507_Qwen3_Coder/src/Qwen3-Coder - GitHub|Qwen3-Coder GitHub 剪藏]] — agentic coding 与 software workflows
- [[Topics/13_base_model/Alibaba_Qwen/2602_Qwen3_5/src/Qwen3.5 - GitHub|Qwen3.5 GitHub 索引剪藏]] — Qwen3.5 系列在官方 Qwen3.6 repo 中的发布记录
- [[Topics/13_base_model/Alibaba_Qwen/2604_Qwen3_6/src/Qwen3.6 - GitHub|Qwen3.6 GitHub 剪藏]] — Qwen3.6 开源模型系列
- [[Topics/13_base_model/Alibaba_Qwen/2608_Qwen3_8/src/00_Source_Index|Qwen3.8 官方来源索引]] — Flash、Max、2.4T-A95B、27B、技术博客、模型卡与平台文档
- [[Topics/13_base_model/Moonshot_Kimi/2504_Kimi_VL/src/Kimi-VL - GitHub|Kimi-VL GitHub 剪藏]] — MoE VLM、多模态推理与 agent capabilities
- [[Topics/13_base_model/Moonshot_Kimi/2604_Kimi_K2_6/src/Kimi-K2.6 - Hugging Face|Kimi K2.6 Hugging Face model card 剪藏]] — K2.6 的 long-horizon coding、multi-agent orchestration 与部署用法
- [[Topics/13_base_model/OpenAI/2508_GPT_5/src/GPT-5 - OpenAI|GPT-5 OpenAI 剪藏]] — unified reasoning system、router 与 thinking model
- [[Topics/13_base_model/OpenAI/2508_GPT_OSS/src/GPT-OSS - OpenAI|gpt-oss OpenAI 剪藏]] — open-weight reasoning models
- [[Topics/13_base_model/OpenAI/2509_GPT_5_Codex/src/GPT-5-Codex - OpenAI|GPT-5-Codex OpenAI 剪藏]] — Codex agentic coding 与 test-until-pass
- [[Topics/13_base_model/OpenAI/2511_GPT_5_1/src/GPT-5.1 - OpenAI Developers|GPT-5.1 OpenAI 剪藏]] — adaptive reasoning、prompt caching 与 coding
- [[Topics/13_base_model/OpenAI/2511_GPT_5_1_Codex_Max/src/GPT-5.1-Codex-Max - OpenAI|GPT-5.1-Codex-Max OpenAI 剪藏]] — long-running coding 与 compaction
- [[Topics/13_base_model/OpenAI/2512_GPT_5_2/src/GPT-5.2 - OpenAI|GPT-5.2 OpenAI 剪藏]] — professional work 与 long-running agents
- [[Topics/13_base_model/OpenAI/2602_GPT_5_3_Codex/src/GPT-5.3-Codex - OpenAI|GPT-5.3-Codex OpenAI 剪藏]] — complex execution 与 tool use
- [[Topics/13_base_model/OpenAI/2603_GPT_5_3_Instant/src/GPT-5.3 Instant System Card - OpenAI|GPT-5.3 Instant System Card 剪藏]] — faster everyday model 与 web-search contextualization
- [[Topics/13_base_model/OpenAI/2603_GPT_5_4/src/GPT-5.4 - OpenAI|GPT-5.4 OpenAI 剪藏]] — computer use、tool search 与 knowledge work
- [[Topics/13_base_model/OpenAI/2603_GPT_5_4_Thinking/src/GPT-5.4 Thinking System Card - OpenAI|GPT-5.4 Thinking System Card 剪藏]] — reasoning model 与 cyber safeguards
- [[Topics/13_base_model/OpenAI/2604_GPT_5_5/src/GPT-5.5 - OpenAI|GPT-5.5 OpenAI 剪藏]] — complex real-world work、coding、research 与 tool use
- [[Topics/13_base_model/OpenAI/2605_GPT_5_5_Instant/src/GPT-5.5 Instant - OpenAI|GPT-5.5 Instant OpenAI 剪藏]] — factuality、personalization 与 default instant model
- [[Topics/13_base_model/Anthropic/src/Claude System Cards - Anthropic|Claude System Cards 剪藏]] — Claude 4.x system cards 总入口
- [[Topics/13_base_model/Google_DeepMind/2507_Gemini_2_5/src/Gemini-2.5 Model Family - Google Blog|Gemini 2.5 model family 官方博客剪藏]] — Gemini 2.5 Pro / Flash / Flash-Lite
- [[Topics/13_base_model/Google_DeepMind/src/Google DeepMind Model Cards|Google DeepMind Model Cards 剪藏]] — Gemini Deep Think、Computer Use 与模型卡入口
- [[Topics/13_base_model/Google_DeepMind/2511_Gemini_3/src/Gemini-3 - Google Blog|Gemini 3 官方博客剪藏]] — Gemini 3 的 multimodal reasoning 与 agent-first development
- [[Topics/13_base_model/Google_DeepMind/2512_Gemini_3_Flash/src/Gemini-3-Flash - Google Blog|Gemini 3 Flash 官方博客剪藏]] — Flash-speed reasoning
- [[Topics/13_base_model/Google_DeepMind/2602_Gemini_3_1_Pro/src/Gemini-3.1-Pro - Model Card|Gemini 3.1 Pro model card 剪藏]] — advanced multimodal reasoning
- [[Topics/13_base_model/Meta_Llama/2601_Llama_4_Herd/src/Llama-4 - Meta AI Blog|Llama 4 官方博客剪藏]] — Llama 4 Scout / Maverick / Behemoth 的 MoE 与 native multimodal 路线
- [[Topics/13_base_model/Meta_Llama/2601_Llama_4_Herd/src/Llama-Guard-4 - Hugging Face|Llama Guard 4 Hugging Face 剪藏]] — multimodal safety classifier

---

## 常见问题（QA）

```dataview
TABLE title, topic, created
FROM "Topics/13_base_model/QA"
SORT created DESC
```

- [[Topics/13_base_model/QA/0611_MoE_vs_Dense_Resource_Comparison|309B MoE vs 30B Dense 资源消耗对比]] — 显存/算力/通信开销全面对比

---

## 开放问题

- [ ] **Llama 5 何时发布？** Meta 在 2026 上半年公开节奏明显慢于其他公司
- [ ] **OpenAI GPT-5 架构是否公开？** 目前仍是黑盒
- [ ] **国内模型与 GPT-4.5/Claude 4.7 的真实差距？** 缺乏公平基准对比
- [ ] **Agent RL 的最佳训练范式？** GRPO vs CISPO vs PPO 各有优劣
- [ ] **Computer Use 是否成为 base model 标配？** Google Gemini 2.5 已率先支持

---

## 关联主题

- [[Topics/6_multimodal/Multimodal MOC]] — 全模态基座是多模态方向的延伸
- [[Topics/7_rl/RL MOC]] — Agentic RL 是训练范式核心
- [[Topics/1_benchmarks/Benchmarks MOC]] — 评测基准验证 base model 能力
- [[Topics/11_harness/Harness MOC]] — Agent Harness 是 evaluation infra

---

## 参考文献

| ID | 公司 | 链接 |
|----|------|------|
| [1] | GLM-4.1V/4.5V | https://arxiv.org/abs/2507.01006 |
| [2] | GLM-4.5 | https://z.ai/blog/glm-4.5 |
| [3] | GLM-4.5 Air | https://arxiv.org/abs/2508.06471 |
| [4] | GLM-TTS | https://arxiv.org/abs/2512.14291 |
| [5] | GLM-OCR | https://arxiv.org/abs/2603.10910 |
| [6] | GLM-5.1 | https://z.ai/blog/glm-5.1 |
| [7] | GLM-4.7 | https://docs.z.ai/guides/llm/glm-4.7 |
| [8] | MiniMax-M1 | https://arxiv.org/abs/2506.13585 |
| [9] | MiniMax-M2 | https://www.minimaxi.com/news/minimax-m2 |
| [10] | MiniMax-M2.1 | https://www.minimax.io/news/minimax-m21 |
| [11] | MiniMax-M2.5 | https://www.minimax.io/news/minimax-m25 |
| [12] | MiniMax-M2.7 | https://www.minimax.io/news/minimax-m27-en |
| [13] | MiniMax-M2 Series | https://arxiv.org/abs/2605.26494 |
| [14] | Qwen3 | https://arxiv.org/abs/2505.09388 |
| [15] | Qwen3-Embedding | https://github.com/QwenLM/Qwen3-Embedding |
| [16] | Qwen3-Coder | https://github.com/QwenLM/Qwen3-Coder |
| [17] | Qwen3-Omni | https://arxiv.org/abs/2509.17765 |
| [18] | Qwen3-TTS | https://arxiv.org/html/2601.15621v1 |
| [19] | Qwen3-ASR | https://arxiv.org/html/2601.21337v1 |
| [20] | Qwen3.5/3.6 | https://github.com/QwenLM/Qwen3.6 |
| [21] | Qwen3-Coder-Next | https://arxiv.org/abs/2603.00729 |
| [22] | Qwen3.5-Omni | https://arxiv.org/abs/2604.15804 |
| [23] | Kimi K2 | https://arxiv.org/abs/2507.20534 |
| [24] | Kimi Linear | https://arxiv.org/abs/2510.26692 |
| [25] | Kimi K2.5 | https://arxiv.org/abs/2602.02276 |
| [26] | Kimi K2.6 | https://huggingface.co/moonshotai/Kimi-K2.6 |
| [27] | Kimi-VL | https://github.com/MoonshotAI/Kimi-VL |
| [28] | GPT-5 | https://openai.com/index/introducing-gpt-5/ |
| [29] | GPT-5.5 System Card | https://openai.com/index/gpt-5-5-system-card/ |
| [30] | GPT-5-Codex | https://openai.com/index/gpt-5-system-card-addendum-gpt-5-codex/ |
| [31] | GPT-5.1 | https://openai.com/index/gpt-5-1-for-developers/ |
| [32] | GPT-5.1-Codex-Max | https://openai.com/index/gpt-5-1-codex-max-system-card/ |
| [33] | GPT-5.2 | https://openai.com/index/introducing-gpt-5-2/ |
| [34] | GPT-5.3-Codex | https://openai.com/index/introducing-gpt-5-3-codex/ |
| [35] | GPT-5.3 Instant | https://openai.com/index/gpt-5-3-instant-system-card/ |
| [36] | GPT-5.4 Thinking | https://openai.com/index/gpt-5-4-thinking-system-card/ |
| [37] | GPT-5.4 | https://openai.com/index/introducing-gpt-5-4/ |
| [38] | GPT-5.5 | https://openai.com/index/introducing-gpt-5-5/ |
| [39] | GPT-5.5 Instant | https://openai.com/index/gpt-5-5-instant/ |
| [40] | Claude System Cards | https://www.anthropic.com/system-cards |
| [41] | Claude Opus 4.5 | https://www.anthropic.com/claude-opus-4-5-system-card |
| [42] | Gemini 2.5 | https://arxiv.org/abs/2507.06261 |
| [43] | Gemini 2.5 Flash-Lite | https://blog.google/products-and-platforms/products/gemini/gemini-2-5-model-family-expands/ |
| [44] | Gemini Model Cards | https://deepmind.google/models/model-cards/ |
| [45] | Gemini Robotics 1.5 | https://arxiv.org/abs/2510.03342 |
| [46] | Gemini 3 | https://blog.google/products-and-platforms/products/gemini/gemini-3/ |
| [47] | Gemini 3 Flash | https://blog.google/products-and-platforms/products/gemini/gemini-3-flash/ |
| [48] | Gemini 3.1 Pro | https://deepmind.google/models/model-cards/gemini-3-1-pro/ |
| [49] | Llama 4 | https://ai.meta.com/blog/llama-4-multimodal-intelligence/ |
| [50] | Llama Guard 4 | https://huggingface.co/meta-llama/Llama-Guard-4-12B |
| [51] | Llama 4 Herd | https://arxiv.org/abs/2601.11659 |
