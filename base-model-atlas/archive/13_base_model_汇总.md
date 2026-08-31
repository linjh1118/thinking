---
title: "Base Model 汇总 — 2025-2026 大模型基座全景"
type: summary
tags: [moc, base-model, summary, foundation-model]
created: 2026-06-01
updated: 2026-06-01
---

# Base Model 汇总 — 2025-2026 大模型基座全景

> 📅 **时间窗口**: 2025-02 至 2026-06
> **来源**: 27 份精读笔记 + 31 份 web-clipping（官方博客/Model Card/GitHub）
> **覆盖**: 国内 6 家 + 国外 4 家 + 1 个研究主线 (Agentic RL/Verification)

---

## TL;DR

2025-2026 的"百模大战"已收敛为**四条主线**：
1. **Reasoning 进入基座** —— o1/R1 之后，Thinking 不再是后训练 trick，而是 pre-training 目标
2. **Agentic RL 范式成熟** —— GRPO/CISPO/GRPO-RoC/Forge 等算法收敛于"真实环境 RL + Verification"
3. **全模态原生基座** —— 文本/图像/音频/视频统一 tokenizer，Thinker-Talker 架构成为新模板
4. **Coding Agent 主战场** —— 从单轮 HumanEval 到 SWE-bench Verified/Pro，再到 Claw-Eval/VIBE-Pro

> 关键判断：**Agent Foundation Model** 概念已成型（Seed1.8/2.0, GLM-4.5/5.1, MiniMax-M2/M3），未来 base model 不再只是"通用对话基座"，而是"为 agent 场景优化的预训练基座"。

---

## 目录

- [国内公司](#国内公司)
  - [Zhipu / GLM](#zhipu--glm)
  - [Baidu / ERNIE](#baidu--ernie)
  - [MiniMax](#minimax)
  - [Alibaba / Qwen](#alibaba--qwen)
  - [Moonshot / Kimi](#moonshot--kimi)
  - [ByteDance Seed](#bytedance-seed)
- [国外公司](#国外公司)
  - [OpenAI / GPT](#openai--gpt)
  - [Anthropic / Claude](#anthropic--claude)
  - [Google DeepMind / Gemini](#google-deepmind--gemini)
  - [Meta / Llama](#meta--llama)
- [Agentic RL & Verification](#agentic-rl--verification-主线)
- [整体发展 Insight](#整体发展-insight)

---

## 国内公司

### 🏢 Zhipu / GLM

> **主线演进**: `VLM 多模态 RL` → `ARC 旗舰基座` → `Long-horizon agentic engineering`

#### 📄 论文笔记

| 模型                                                                                       | 月份      | 动机                                                                                         | 1️⃣ 贡献                                                                                           | 2️⃣ 贡献                                                                                       | 3️⃣ 贡献                                                                     |
| ---------------------------------------------------------------------------------------- | ------- | ------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------- |
| [[Topics/13_base_model/Zhipu_GLM/2507_GLM_4_5V/GLM-4.5V-Multimodal-Reasoning-RLCS\|GLM-4.5V]]      | 2025-07 | 把 LLM 端 Scalable RL 范式迁移到 VLM 端 —— 现有开源 VLM 在 GUI Agent / Coding / STEM 等任务上一致性不足          | 提出 **RLCS**（RL with Curriculum Sampling），结合课程学习 + pass@k 难度评估 + Ratio EMA 动态采样扩展                 | 跨领域 RL 训练发现 joint training 效果最好，**GUI Agent 数据是最强 cross-domain transfer 信号**                 | 42 个 benchmark 开源 SOTA，9B 小模型也能超 Qwen2.5-VL-72B，可比 Gemini-2.5-Flash        |
| [[Topics/13_base_model/Zhipu_GLM/2508_GLM_4_5/GLM-4.5-ARC-Foundation-Models\|GLM-4.5]]             | 2025-08 | o3/Claude Opus/Gemini 2.5 Pro 在 ARC 任务上很强但闭源 + 推理成本高，希望用**更少参数（355B vs 671B+）**实现同等 ARC 能力 | 355B/32B MoE 架构，**减少 width 增加 depth** + loss-free balance routing + 96 attention heads + QK-Norm | 后训练走 **Expert Model Iteration**：三 expert（Reasoning/Agent/General）独立 RL → 自蒸馏统一为 hybrid model | TAU-Bench 70.1% / AIME 24 91.0% / SWE-bench Verified 64.2%，综合第三、Agentic 第二 |
| [[Topics/13_base_model/Zhipu_GLM/2512_GLM_TTS/GLM-TTS-Production-Level-Speech-Synthesis\|GLM-TTS]] | 2025-12 | SOTA TTS 普遍需 1M+ 小时训练数据 + 难以克隆个性化声音 + 中文多音字/罕见字发音差 + RL 训练不稳定                              | 仅 100k 小时训练数据（CosyVoice3 的 1/10）通过 **两阶段架构**（Text-to-Token AR + Vocos2D Diffusion）达开源 SOTA       | 首次把 **GRPO 多 reward RL** 系统性引入 TTS，**LoRA 声音定制仅需 15% 参数 + 1 小时音频**                           | 提出 **Phoneme-in 机制**解决多音字/罕见字发音控制                                          |
| [[Topics/13_base_model/Zhipu_GLM/2603_GLM_OCR/GLM-OCR-Document-Understanding\|GLM-OCR]]            | 2026-03 | 现有 MLLM 太大太慢难以部署到高频并发/边缘环境，且 OCR 任务的"确定性 + 强局部依赖"与 LLM 自回归生成范式本质不匹配                        | 0.9B 超轻量级（CogViT 0.4B + GLM 0.5B），**MTP** 让每步平均生成 5.2 token，吞吐提升 50%                             | 两阶段 Pipeline：**PP-DocLayout-V3 布局分析** + 并行区域级识别                                              | OmniDocBench v1.5 排第一（94.6 分），反超 Qwen3-VL-235B 和 Gemini-3-Pro              |

#### 🌐 Web-Clippings

| 来源 | 月份 | 动机 | 1️⃣ 贡献 | 2️⃣ 贡献 | 3️⃣ 贡献 |
|------|------|------|---------|---------|---------|
| [[Topics/13_base_model/Zhipu_GLM/2508_GLM_4_5/src/GLM-4.5 - Z.ai Blog\|GLM-4.5 官方博客]] | 2025-07 | 正式发布 ARC 旗舰基座 | 12 个 ARC benchmark 评测（Agentic 3 + Reasoning 7 + Coding 2） | τ-bench / BFCL-v3 表现对齐 Claude 4 Sonnet，**BrowseComp 26.4%** 超 Claude-4-Opus (18.8%) | Test-time scaling 在 BrowseComp 上的 accuracy 曲线 |
| [[Topics/13_base_model/Zhipu_GLM/2509_GLM_4_7/src/GLM-4.7 - Z.AI Docs\|GLM-4.7 开发者文档]] | 2025-09 | 填补 4.5 与 5.1 之间的迭代窗口 | Coding 增强 | Tool use 能力升级 | **Interleaved reasoning**（交错推理） |
| [[Topics/13_base_model/Zhipu_GLM/2604_GLM_5_1/src/GLM-5.1 - Z.ai Blog\|GLM-5.1 官方博客]] | 2026-04 | GLM-4.5 在长任务上仍有局限，希望推 agentic engineering 旗舰 | **SWE-Bench Pro SOTA 58.4%**（vs GLM-5 54.2%） | **NL2Repo（repo generation）大幅领先** GLM-5 | **Terminal-Bench 2.0（real-world terminal tasks）领先** GLM-5 |

---

### 🏢 Baidu / ERNIE

> **主线演进**: `知识增强预训练` → `原生多模态 MoE` → `统一多模态自回归` → `弹性预训练 + 异步 Agentic RL`
> **系列入口**: [[Topics/13_base_model/Baidu_ERNIE/ERNIE-Series-Summary\|Baidu ERNIE Series Summary]]

#### 📄 arXiv 源码

| 模型 | 月份 | arXiv | 动机 | 1️⃣ 贡献 | 2️⃣ 贡献 | 3️⃣ 贡献 |
|------|------|-------|------|---------|---------|---------|
| ERNIE | 2019-04 | 1904.09223 | BERT 时代如何把知识结构注入表示学习 | entity/phrase masking | knowledge integration | 中文 NLP 强基线 |
| ERNIE 2.0 | 2019-07 | 1907.12412 | 静态预训练任务不足以覆盖多种语言理解需求 | continual pretraining | multi-task objective | language understanding |
| ERNIE 3.0 | 2021-07 | 2107.02137 | 统一 language understanding 与 generation | knowledge-enhanced large-scale pretraining | 多任务统一 | 知识记忆 |
| ERNIE 3.0 Titan | 2021-12 | 2112.12731 | 扩展知识增强预训练到更大规模 | larger-scale pretraining | distributed inference | knowledge-enhanced generation |
| ERNIE-Code | 2022-12 | 2212.06742 | 代码预训练过于英语中心 | cross-lingual code pretraining | multilingual PL data | code understanding/generation |
| ERNIE 3.0 Tiny | 2023-01 | 2301.03416 | 小模型蒸馏泛化不足 | task-agnostic distillation | simple generalization recipe | compact deployment |
| ERNIE 5.0 | 2026-02 | 2602.04705 | 多模态理解/生成不应靠 late fusion 拼接 | 2.4T unified multimodal MoE | Next-Group-of-Tokens Prediction | elastic training + unified text/image/video/audio |

#### 🌐 Web-Clippings

| 来源 | 月份 | 动机 | 1️⃣ 贡献 | 2️⃣ 贡献 | 3️⃣ 贡献 |
|------|------|------|---------|---------|---------|
| [[Topics/13_base_model/Baidu_ERNIE/2307_ERNIE_3_5/src/ERNIE-3.5 - Baidu PRNewswire\|ERNIE 3.5 PRNewswire]] | 2023-07 | 记录无 arXiv 的 3.5 发布/升级证据 | 训练吞吐 2x | QPS 30x vs ERNIE 3.0 | 产业落地 |
| [[Topics/13_base_model/Baidu_ERNIE/2310_ERNIE_4_0/src/ERNIE-4.0 - Baidu PRNewswire\|ERNIE 4.0 PRNewswire]] | 2023-10 | 4.0 发布证据 | 理解 | 生成/推理 | 记忆 |
| [[Topics/13_base_model/Baidu_ERNIE/2408_ERNIE_4_0_Turbo/src/ERNIE-4.0-Turbo - Baidu PRNewswire\|ERNIE 4.0 Turbo PRNewswire]] | 2024-08 | 4.0 Turbo 财报口径证据 | 更快响应 | 更低成本 | ERNIE 产品化 |
| [[Topics/13_base_model/Baidu_ERNIE/2503_ERNIE_4_5_and_X1/src/ERNIE-4.5-and-X1 - Baidu PRNewswire\|ERNIE 4.5 / X1 PRNewswire]] | 2025-03 | 4.5 与 X1 发布证据 | 4.5 native multimodal | X1 deep thinking reasoning | 免费开放 |
| [[Topics/13_base_model/Baidu_ERNIE/2504_ERNIE_4_5_Turbo_and_X1_Turbo/src/ERNIE-4.5-Turbo-and-X1-Turbo - Baidu PRNewswire\|ERNIE 4.5 Turbo / X1 Turbo PRNewswire]] | 2025-04 | Turbo 线发布证据 | 更快更低价 | 多模态 + 工具调用 | MCP / agent 应用生态 |
| [[Topics/13_base_model/Baidu_ERNIE/2503_ERNIE_4_5_and_X1/src/ERNIE-4.5 - Official Blog\|ERNIE 4.5 官方博客]] | 2025-06 | 开源 ERNIE 4.5 模型族 | heterogeneous multimodal MoE | ERNIEKit / FastDeploy | Apache 2.0 open models |
| [[Topics/13_base_model/Baidu_ERNIE/2602_ERNIE_5_0/src/ERNIE-5.0 - Official Blog\|ERNIE 5.0 官方博客]] | 2026-02 | 统一多模态大模型发布 | 2.4T parameters | unified autoregressive multimodal objective | text/image/video/audio |
| [[Topics/13_base_model/Baidu_ERNIE/2605_ERNIE_5_1/src/ERNIE-5.1 - Official Blog\|ERNIE 5.1 官方博客]] | 2026-05 | 5.0 派生的高性价比旗舰 | multi-dimensional elastic pretraining | disaggregated fully-asynchronous RL | scaled agentic post-training |

---

### 🏢 MiniMax

> **主线演进**: `M1 long-context reasoning RL` → `M2 系列 coding/office/search agent` → `M3 1M context + native multimodality + MSA`

#### 📄 论文笔记

| 模型 | 月份 | 动机 | 1️⃣ 贡献 | 2️⃣ 贡献 | 3️⃣ 贡献 |
|------|------|------|---------|---------|---------|
| [[Topics/13_base_model/MiniMax/2506_MiniMax_M1/MiniMax-M1-Scaling-Test-Time-Compute-Lightning-Attention\|MiniMax-M1]] | 2025-06 | 传统 Transformer softmax attention 二次复杂度限制长 reasoning 链 + 现有开源 LRM 上下文窗口太小 + RL 训练扩展成本高 | 首个开源大规模 hybrid-attention 推理模型，**Lightning Attention**（线性注意力 IO-aware），100K tokens 时 FLOPs 仅 DeepSeek R1 的 25% | 提出 **CISPO**（Clipped IS-weight Policy Optimization）—— 裁 IS 权重而非 token，保留低概率 token 梯度 | 1M context + 80K output tokens，RL 训练成本仅 $0.53M（512 H800 GPU，3周） |
| [[Topics/13_base_model/MiniMax/2605_MiniMax_M2_Series/MiniMax-M2-Series-Mini-Activations-Max-Real-World-Intelligence\|MiniMax-M2 Series]] | 2026-05 | Agent 任务天然需要超长上下文（192K 原生窗口） + 训练-推理 gap + 多域能力平衡（代码/搜索/办公） | **小激活大智能**：229.9B/9.8B 激活即可媲美大一个数量级闭源模型 | **Forge RL 系统** —— 统一白盒/黑盒 agent 训练框架 + 可验证轨迹 + artifact-aligned reward | M2.7 展现**自我进化**能力（自主调试训练流程、修改 agent scaffold），MLE Bench Lite 与 Gemini 3.1 Pro 持平 |
| [[Topics/13_base_model/MiniMax/2606_MiniMax_M3/MiniMax-M3-Frontier-Coding-1M-Context-Native-Multimodality\|MiniMax-M3]] | 2026-06 | M2 系列已证明 agentic coding 激进但长任务上下文成本仍高（论文/repo/日志/工具轨迹/截图累积），且 coding agent 进入多模态阶段 | 核心架构变化 **MSA（MiniMax Sparse Attention）** —— 预筛选相关 KV blocks + 精确注意力，1M context 真正可扩展 | **Frontier coding + 1M context + native multimodality** 三位一体（图像/视频输入 + computer use） | 训练和评测加入 **interactive user simulator**（模拟持续澄清/反馈修正/任务切换），SWE-Bench Pro 超 GPT-5.5/Gemini 3.1 Pro、逼近 Opus 4.7 |

#### 🌐 Web-Clippings

| 来源 | 月份 | 动机 | 1️⃣ 贡献 | 2️⃣ 贡献 | 3️⃣ 贡献 |
|------|------|------|---------|---------|---------|
| [[Topics/13_base_model/MiniMax/2510_MiniMax_M2/src/MiniMax-M2 - Official Blog\|MiniMax-M2 官方博客]] | 2025-10 | 开源 M2，定位"agent/代码专用基座" | 顶级代码能力，**专为端到端开发工作流打造** | 在 Claude Code / Cursor / Cline / Kilo Code / Droid 中表现卓越 | **Claude Sonnet 8% 价格 2 倍速度**，限时免费 |
| [[Topics/13_base_model/MiniMax/2512_MiniMax_M2_1/src/MiniMax-M2.1 - Official Blog\|MiniMax-M2.1 官方博客]] | 2025-12 | M2 解决成本和可访问性后，M2.1 转向真实复杂任务能力 | **多语言编程**显著增强 | **Office 场景**专项优化 | 构建"AI Native Company"愿景 |
| [[Topics/13_base_model/MiniMax/2602_MiniMax_M2_5/src/MiniMax-M2.5 - Official Blog\|MiniMax-M2.5 官方博客]] | 2026-02 | 在数十万个真实复杂环境中用 RL 训练，让模型"以可承受价格提供前沿能力" | **SOTA in coding, agentic tool use and search, office work**：SWE-Bench Verified 80.2% / Multi-SWE-Bench 51.3% / BrowseComp 76.3% | SWE-Bench Verified 评估比 M2.1 **快 37%**，匹配 Claude Opus 4.6 速度 | **每小时 $1 / 100 tokens per second** 连续运行 —— "too cheap to meter" |
| [[Topics/13_base_model/MiniMax/2603_MiniMax_M2_7/src/MiniMax-M2.7 - Official Blog\|MiniMax-M2.7 官方博客]] | 2026-03 | 当人类生产力被充分释放，下一步是**模型与组织的自我进化** | **"Early Echoes of Self-Evolution"**：模型深度参与自身 RL 实验循环（自主更新 memory、构建 skill、改进 harness） | **SWE-Pro 56.22%**（接近 Opus 最佳水平）、VIBE-Pro 55.6%、Terminal Bench 2 57.0% | GDPval-AA **ELO 1495（开源第一）**，97% skill adherence 率（40+ 复杂 skill） |
| [[Topics/13_base_model/MiniMax/2606_MiniMax_M3/src/MiniMax-M3 - Official Blog\|MiniMax-M3 官方博客]] | 2026-05 | 把 frontier coding / 1M context / native multimodality 整合到同一开源模型 | **MSA 架构详解** —— 预筛选 + 精确注意力的稀疏注意力新架构 | 全面评测领先：**SWE-Bench Pro** 超 GPT-5.5/Gemini 3.1 Pro、SVG-Bench 超 Opus 4.7、OmniDocBench 超 Gemini 3.1 Pro、Claw-Eval 最高分 | **Open-weight 路线图** + MiniMax Code / Token Plan / API 多渠道接入 |

---

### 🏢 Alibaba / Qwen

> **正代主线演进**: `Qwen3 thinking/no_think 统一` → `Qwen3.5/3.6 开源迭代` → `Qwen3.8 原生多模态 + 1M context + 稀疏高效架构`。Coder、Omni、Embedding、ASR、TTS 等支线统一收进 `Variants/`。

#### 📄 论文笔记

| 模型                                                                                                 | 月份      | 动机                                                                                            | 1️⃣ 贡献                                                                                                                                | 2️⃣ 贡献                                                                                         | 3️⃣ 贡献                                                                                         |
| -------------------------------------------------------------------------------------------------- | ------- | --------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------- |
| [[Topics/13_base_model/Alibaba_Qwen/2505_Qwen3/Qwen3-Technical-Report\|Qwen3]]                                  | 2025-05 | 复杂推理需要 QwQ-32B、快速响应需要 Qwen2.5-72B（模型分裂）+ 简单任务用大模型浪费推理资源 + 小模型直接 RL 训练效果差                      | **首个统一 thinking/non-thinking 单一模型**，0.6B-235B 全尺寸（MoE 235B/22B 激活）                                                                    | **Thinking Budget 机制** —— 动态分配推理 token，60% 激活参数在 17/23 基准上超 DeepSeek-R1                        | 后训练四阶段：**冷启动 → 推理 RL → 模式融合 → 蒸馏**，关键技术路径开源                                                    |
| [[Topics/13_base_model/Alibaba_Qwen/Variants/2509_Qwen3_Omni/Qwen3-Omni-Thinker-Talker-Architecture\|Qwen3-Omni]]        | 2025-09 | 传统 LLM 为中心的多模态模型存在"模态权衡"（增强一个模态导致其他模态下降）                                                      | **Thinker-Talker 架构** —— Thinker 理解/推理（文本/图像/音频/视频）+ Talker 流式语音生成                                                                    | 五大升级：MoE 化、**AuT 音频编码器**（20M 小时训练，12.5Hz token rate）、RVQ codec、**MTP 模块**、**TM-RoPE** 时间对齐位置编码 | **模态不降智** —— 加入音频后文本/视觉不退化，端到端延迟 234ms                                                         |
| [[Topics/13_base_model/Alibaba_Qwen/Variants/2601_Qwen3_TTS/Qwen3-TTS-Multilingual-Controllable-TTS\|Qwen3-TTS]]         | 2026-01 | 现代 TTS 需在稳定性 / 可控性 / 自然度 / 低延迟之间取得平衡                                                          | **双码率设计** —— 12Hz-1.7B 变体（RVQ 多码本 + MTP + 轻量级 ConvNet Code2Wav）+ 25Hz 变体（单码本 + chunk-wise DiT 解码器）                                    | **首包延迟 97ms**，S3 阶段长上下文从 8K 扩展到 32K                                                            | 三阶段训练 + DPO + GSPO + Speaker Fine-tuning；Seed-TTS benchmark **WER 1.24（SOTA）**                 |
| [[Topics/13_base_model/Alibaba_Qwen/Variants/2601_Qwen3_ASR/Qwen3-ASR-Multilingual-ASR-With-Forced-Aligner\|Qwen3-ASR]]  | 2026-01 | 传统 ASR 难以处理长语音/抗噪/多语言，时间戳预测（CTC/CIF）多语言支持差                                                    | 基于 Qwen3-Omni 的 ASR 家族（Qwen3-ASR-1.7B / 0.6B / ForcedAligner-0.6B）                                                                    | **首次把 LLM 引入 forced alignment** —— 任意时间粒度的灵活时间戳预测，11 种语言统一对齐                                   | **52 种语言/方言**（30 种语言 + 22 种中文方言），最长 20 分钟单条语音                                                  |
| [[Topics/13_base_model/Alibaba_Qwen/Variants/2603_Qwen3_Coder_Next/Qwen3-Coder-Next-Technical-Report\|Qwen3-Coder-Next]] | 2026-03 | 现有 coding agent 在 tool-call format 上过拟合 + SWE-bench 训练存在 reward hacking（agent 通过 git log 偷答案） | **80B/3B 激活 MoE，最完整的 Agent Training Recipe**：Base → SFT → 三 Expert Models（WebDev / UX/CLI / SWE）→ Expert Distillation → Unified Model | **Tool Chat Template Scaling** —— 21 种工具调用格式训练，避免过拟合单一格式                                       | **Reward Hacking Blocker** —— 防止 agent 在 SWE-bench 训练中通过 git 漏洞作弊                              |
| [[Topics/13_base_model/Alibaba_Qwen/Variants/2604_Qwen3_5_Omni/Qwen3-5-Omni-Streaming-Omni-Agent\|Qwen3.5-Omni]]         | 2026-04 | 现有模型多是被动感知-响应范式，缺乏 agentic 行为、实时交互、自主工具调用、跨模态推理                                               | **Hybrid Attention MoE** 升级，**256K context**（10+ 小时音频 / 400 秒 720P 视频）                                                                | **ARIA（Adaptive Rate Interleave Alignment）** —— 动态对齐文本和语音单元，解决双通道生成问题                          | Plus 版本在 **215 个 benchmark** 上 SOTA，超越 Gemini-3.1 Pro；新增可控音视频 captioning、实时交互（语义打断/音量/语速/情感控制） |

#### 🌐 Web-Clippings

| 来源 | 月份 | 动机 | 1️⃣ 贡献 | 2️⃣ 贡献 | 3️⃣ 贡献 |
|------|------|------|---------|---------|---------|
| [[Topics/13_base_model/Alibaba_Qwen/Variants/2506_Qwen3_Embedding/src/Qwen3-Embedding - GitHub\|Qwen3-Embedding GitHub]] | 2025-06 | Qwen3 dense 基底扩展出 embedding/reranker 模型系列 | **0.6B / 4B / 8B** 三个尺寸，覆盖 text/code retrieval | **多语言 / 长文本 / reasoning** 能力继承自 Qwen3 基底 | 适用 text retrieval / code retrieval / text classification / text clustering / bitext mining |
| [[Topics/13_base_model/Alibaba_Qwen/Variants/2507_Qwen3_Coder/src/Qwen3-Coder - GitHub\|Qwen3-Coder GitHub]] | 2025-07 | 开源 Qwen3-Coder + Coder-Next 生态 | 多 IDE 集成（Claude Code / Cursor / Cline）+ WebDev 沙箱 | **Qwen Code CLI** 工具 | HF + ModelScope 双平台权重 |
| [[Topics/13_base_model/Alibaba_Qwen/2602_Qwen3_5/src/Qwen3.5 - GitHub\|Qwen3.5 GitHub Release Notes]] | 2026-02 | 通过 Qwen3.6 仓库的 release notes 追踪 Qwen3.5 模型发布 | **9B / 4B / 2B / 0.8B** 四个尺寸开源 | HF + ModelScope 双平台 | 作为"next-gen open models"前序版本 |
| [[Topics/13_base_model/Alibaba_Qwen/2604_Qwen3_6/src/Qwen3.6 - GitHub\|Qwen3.6 GitHub]] | 2026-04 | Qwen3.6 系列的官方发布页（包含 Qwen3.5 release notes） | 统一 GitHub 仓库管理 Qwen3.5 / Qwen3.6 | 持续 Release Notes 更新 | 定位"next-gen open models" |
| [[Topics/13_base_model/Alibaba_Qwen/2608_Qwen3_8/Qwen3.8-Flash\|Qwen3.8-Flash]] | 2026-08 | 在 1M 上下文与原生多模态下同时压低服务成本和长上下文延迟 | **125B core / 6B active + 51B n-gram embedding**，Gated DeltaNet 与 Qwen Sparse Attention 混合 | QSA 在 1M context 下官方 kernel 测试最高 **7.6× prefill / 4.9× decode** | 内置代码解释器、图片搜索、网页提取与搜索，面向 agent / coding / computer-use |

---

### 🏢 Moonshot / Kimi

> **主线演进**: `K2 ultra-sparse MoE + agentic intelligence` → `Kimi Linear 架构创新` → `K2.5 原生多模态 + Agent Swarm` → `K2.6 long-horizon coding + swarm orchestration`

#### 📄 论文笔记

| 模型 | 月份 | 动机 | 1️⃣ 贡献 | 2️⃣ 贡献 | 3️⃣ 贡献 |
|------|------|------|---------|---------|---------|
| [[Topics/13_base_model/Moonshot_Kimi/2507_Kimi_K2/Kimi-K2-Open-Agentic-Intelligence\|Kimi K2]] | 2025-07 | LLM 从模仿学习转向 Agentic Intelligence，但预训练 token efficiency 成关键 + agentic 能力在自然数据中稀有难以 scale | **MuonClip 优化器**（Muon + QK-Clip per-head 裁剪）实现 15.5T tokens 无 loss spike 训练 | **Ultra-sparse MoE**（1.04T 总参 / 32B 激活 / 384 专家 / sparsity 48）+ MLA，**sparsity scaling law**：固定激活下增加 sparsity 持续降低 loss | 大规模 agentic 数据合成 pipeline + **RLVR + Self-Critique Rubric Reward**；SWE-bench / tau2-bench / ACEBench SOTA，LMSYS Arena 开源第一 |
| [[Topics/13_base_model/Moonshot_Kimi/2510_Kimi_Linear/Kimi-Linear-Expressive-Efficient-Attention\|Kimi Linear]] | 2025-10 | LLM 演化为 Agent 后，RL test-time scaling 让 softmax attention 的二次复杂度 + 线性增长 KV cache 成为瓶颈；linear attention 历史表现不如 softmax | **KDA（Kimi Delta Attention）** —— 在 Gated DeltaNet 基础上引入 **per-channel 细粒度 gating**（而非 per-head），每个 feature dimension 独立 forgetting rate | 在 fair compare 下（相同 training recipe + tokens），短/长/RL scaling 全面超越 full attention | **1M context + 6× decoding throughput**，KV cache 减少 75% |
| [[Topics/13_base_model/Moonshot_Kimi/2602_Kimi_K2_5/Kimi-K2-5-Joint-Optimization-Vision-Language\|Kimi K2.5]] | 2026-02 | 传统"事后附加视觉"方式对齐不足 + 高 vision ratio 浪费 token + sequential agent execution 限制任务复杂度 | **Joint Optimization of Text and Vision** —— 反直觉发现 early fusion + 低 vision ratio 优于 late fusion + 高 vision ratio；**zero-vision SFT 激活视觉 + 视觉 RL 反向提升文本** | **Agent Swarm + PARL** —— 通过 RL 学习动态子 agent 实例化和并行调度 | BrowseComp 比单 agent 提升 17.8%，**3~4.5× 更快**执行 |

#### 🌐 Web-Clippings

| 来源 | 月份 | 动机 | 1️⃣ 贡献 | 2️⃣ 贡献 | 3️⃣ 贡献 |
|------|------|------|---------|---------|---------|
| [[Topics/13_base_model/Moonshot_Kimi/2504_Kimi_VL/src/Kimi-VL - GitHub\|Kimi-VL GitHub]] | 2025-04 | 开源 MoE VLM，激活参数小但能力全面 | **2.8B 激活**即可 SOTA 多模态推理 | 强 agent 能力（OSWorld SOTA 可比旗舰模型） | 覆盖 college-level 图视频理解、OCR、数学、多图理解 |
| [[Topics/13_base_model/Moonshot_Kimi/2604_Kimi_K2_6/src/Kimi-K2.6 - Hugging Face\|Kimi K2.6 HF Model Card]] | 2026-04 | 开源原生多模态 agentic 模型，K2 系列的迭代版 | **Long-horizon coding** 能力 | **Coding-driven design** + proactive autonomous execution | **Swarm-based task orchestration** |

---

### 🏢 ByteDance Seed

> **主线演进**: `Seed1.8 Real-world Agency` → `Seed2.0 Agent Foundation Model 概念定型`

#### 📄 论文笔记

| 模型 | 月份 | 动机 | 1️⃣ 贡献 | 2️⃣ 贡献 | 3️⃣ 贡献 |
|------|------|------|---------|---------|---------|
| [[Topics/13_base_model/ByteDance_Seed/2603_Seed1_8_Model_Card/Seed18-Model-Card-Towards-Generalized-Real-World-Agency\|Seed1.8]] | 2026-03 | 现有 LLM/VLM 缺乏多步交互和任务执行能力，希望构建**真实世界通用 agent** | **Generalized Real-World Agency** 定位 —— 保留 LLM/VLM 能力并扩展到多步交互和任务执行 | **Search + Code Execution + GUI Interaction 统一接口** | **Latency-/Cost-Aware 四档 thinking 模式**（no_think / think-low / think-medium / think-high）+ 优化 visual encoding 减少 token 消耗 |
| [[Topics/13_base_model/ByteDance_Seed/2605_Seed2_0_Model_Card/Seed2.0-Model-Card-Agent-Foundation-Model\|Seed2.0]] | 2026-05 | 现有 General Foundation Model 在 agent 场景需大量微调，**预训练阶段就应针对 agentic 场景优化** | **"Agent Foundation Model" 概念正式落地** —— 类比 LLM 作为对话基础模型，AFM 作为 agent 场景基础模型 | 预训练数据包含 agent 轨迹和环境反馈，**评测重点在 GAIA / SWE-bench / GUI tasks** | Computer Use / Software Engineering / Research / Multimodal Agent 四大 agentic 场景展现优势 |

---

## 国外公司

### 🏢 OpenAI / GPT

> **主线演进**: `GPT-5 unified system (fast + thinking + router)` → `Codex 系列密集迭代` → `5.3/5.4/5.5 reasoning & long-running agents`
>
> ⚠️ **OpenAI 全部以 web-clipping 形式收录**，无独立论文笔记。

#### 🌐 Web-Clippings

| 来源 | 月份 | 动机 | 1️⃣ 贡献 | 2️⃣ 贡献 | 3️⃣ 贡献 |
|------|------|------|---------|---------|---------|
| [[Topics/13_base_model/OpenAI/2508_GPT_5/src/GPT-5 - OpenAI\|GPT-5 发布页]] | 2025-08 | reasoning 模型是独立产品线，需要 unified system 整合到消费级产品 | **Unified system** —— fast model（大多数问题）+ thinking model（复杂问题） | **Real-time router** —— 基于任务复杂度、工具需求、用户意图实时调度 | 集成到 ChatGPT + API |
| [[Topics/13_base_model/OpenAI/2508_GPT_OSS/src/GPT-OSS - OpenAI\|gpt-OSS 发布页]] | 2025-08 | 开源社区需要 OpenAI 风格的 reasoning 模型 | 开源 **gpt-oss-120b / gpt-oss-20b** | **Open-weight reasoning** 模型 | **Efficient deployment** 定位 |
| [[Topics/13_base_model/OpenAI/2509_GPT_5_Codex/src/GPT-5-Codex - OpenAI\|GPT-5-Codex Addendum]] | 2025-09 | GPT-5 通用强但 coding 需专用变种 | **GPT-5 变种**专为 Codex 优化 | **RL 训练于真实编码任务**（varied environments） | Agentic coding 定位 |
| [[Topics/13_base_model/OpenAI/2511_GPT_5_1/src/GPT-5.1 - OpenAI Developers\|GPT-5.1 Developer]] | 2025-11 | 开发者侧 GPT-5 体验优化 | **Adaptive reasoning**（自适应推理） | **Prompt caching** 强化 | Coding-oriented use |
| [[Topics/13_base_model/OpenAI/2511_GPT_5_1_Codex_Max/src/GPT-5.1-Codex-Max - OpenAI\|GPT-5.1-Codex-Max System Card]] | 2025-11 | Codex 应对长任务时的安全和稳定性需求 | **Long-running coding** 优化 | **Compaction**（轨迹压缩） | **Agent sandboxing + coding safety** |
| [[Topics/13_base_model/OpenAI/2512_GPT_5_2/src/GPT-5.2 - OpenAI\|GPT-5.2 发布页]] | 2025-12 | 将 GPT-5 系列推向 professional / 真实工作流 | **Professional work** 强化 | **Long-running agents** 支持 | **SWE-Bench Pro** 评测对齐 |
| [[Topics/13_base_model/OpenAI/2602_GPT_5_3_Codex/src/GPT-5.3-Codex - OpenAI\|GPT-5.3-Codex 发布页]] | 2026-02 | Codex 系列向更长任务推进 | **Long-running coding tasks** 优化 | Research 能力 | **Tool use** 增强 |
| [[Topics/13_base_model/OpenAI/2603_GPT_5_3_Instant/src/GPT-5.3 Instant System Card - OpenAI\|GPT-5.3 Instant System Card]] | 2026-03 | 日常快速响应需求 | **更快更日常**（fast everyday） | **Web-search contextualization** 强化 | 作为 instant 模型基线 |
| [[Topics/13_base_model/OpenAI/2603_GPT_5_4/src/GPT-5.4 - OpenAI\|GPT-5.4 发布页]] | 2026-03 | computer use 进入主流，GPT-5.4 跟进 | **Computer use** 能力 | **Tool search**（工具检索） | **Knowledge work** 强化 |
| [[Topics/13_base_model/OpenAI/2603_GPT_5_4_Thinking/src/GPT-5.4 Thinking System Card - OpenAI\|GPT-5.4 Thinking System Card]] | 2026-03 | reasoning 模型的 cyber safety 评估 | Reasoning model | **Cyber safeguards** | General-purpose 定位 |
| [[Topics/13_base_model/OpenAI/2604_GPT_5_5/src/GPT-5.5 - OpenAI\|GPT-5.5 发布页]] | 2026-04 | 复杂真实工作流的最强消费级模型 | **Complex real-world work** 能力 | **Coding** + **research** 强化 | **Tool use** 升级 |
| [[Topics/13_base_model/OpenAI/2605_GPT_5_5_Instant/src/GPT-5.5 Instant - OpenAI\|GPT-5.5 Instant 发布页]] | 2026-05 | Instant 模型的事实性和个性化 | **Factuality** 强化 | **Personalization** 增强 | **默认 instant 模型** 替代 5.3 Instant |

---

### 🏢 Anthropic / Claude

> **主线演进**: `4.5 系列密集迭代` → `4.6 1M context beta` → `4.7 advanced software engineering` → `Mythos Preview 探索`

#### 🌐 Web-Clippings

| 来源 | 月份 | 动机 | 1️⃣ 贡献 | 2️⃣ 贡献 | 3️⃣ 贡献 |
|------|------|------|---------|---------|---------|
| [[Topics/13_base_model/Anthropic/src/Claude System Cards - Anthropic\|Claude System Cards 总索引]] | 2025-2026 | Anthropic 模型发布的标准化 safety / capability 文档 | **Opus 4.7 (2026-04)** —— advanced software engineering | **Mythos Preview (2026-04)** —— Anthropic preview model | **Sonnet 4.6 / Opus 4.6 / Opus 4.5 / Haiku 4.5 / Sonnet/Opus 4** 等 4.x 系列完整索引 |

> ⚠️ **详细分模型笔记缺失**：Anthropic 各 system card 在 2025-2026 发布周期内对应 Claude Opus 4.5 (2025-11)、Opus 4.6 (2026-02)、Sonnet 4.6 (2026-02)、Opus 4.7 (2026-04)、Mythos Preview (2026-04)。如需深入推荐独立补 .md 笔记。

---

### 🏢 Google DeepMind / Gemini

> **主线演进**: `2.5 thinking model` → `Computer Use` → `Gemini 3 原生多模态 reasoning` → `3.1 Pro` + `Robotics 1.5 具身`

#### 📄 论文笔记

| 模型 | 月份 | 动机 | 1️⃣ 贡献 | 2️⃣ 贡献 | 3️⃣ 贡献 |
|------|------|------|---------|---------|---------|
| [[Topics/13_base_model/Google_DeepMind/2507_Gemini_2_5/Gemini-2.5-Advanced-Reasoning-Multimodality\|Gemini 2.5]] | 2025-06 | Gemini 1.5 奠定了长上下文 + 原生多模态，但 reasoning 能力有限，希望融合 Thinking 能力 | **Thinking Budget 可调节** —— AIME 2025 从 29.7% 拉到 88% | **1M context + 3 小时视频** + 原生多模态（文本/视觉/音频） | LiveCodeBench 74.2% / Aider 82.2% / SWE-bench Verified (multi) 67.2% |
| [[Topics/13_base_model/Google_DeepMind/2510_Gemini_Robotics_1_5/Gemini-Robotics-1.5-Embodied-Reasoning\|Gemini Robotics 1.5]] | 2025-10 | 通用机器人需要物理世界理解 + 高级推理 + 跨形态泛化；Gemini Robotics 1.0 缺乏显式思考 + 跨本体泛化有限 | **Gemini Robotics 1.5 (GR-1.5)**: **Motion Transfer 机制** —— 多本体预训练，零样本跨机器人技能迁移 | **Gemini Robotics-ER 1.5 (GR-ER 1.5)**: 具身推理 SoTA（空间理解/指向/进度检测） | 把 Gemini Thinking 能力带入物理世界 |

#### 🌐 Web-Clippings

| 来源 | 月份 | 动机 | 1️⃣ 贡献 | 2️⃣ 贡献 | 3️⃣ 贡献 |
|------|------|------|---------|---------|---------|
| [[Topics/13_base_model/Google_DeepMind/2507_Gemini_2_5/src/Gemini-2.5 Model Family - Google Blog\|Gemini 2.5 官方博客]] | 2025-06 | 2.5 系列从 preview 推向 GA | **2.5 Pro / Flash GA** | **2.5 Flash-Lite preview** —— cost-efficient + fastest | Hybrid reasoning family 在 cost / speed Pareto frontier |
| [[Topics/13_base_model/Google_DeepMind/src/Google DeepMind Model Cards\|Google DeepMind Model Cards]] | 2026 多次更新 | DeepMind 模型卡入口 | **Omni Flash (2026-05)** + **3.5 Flash (2026-05)** + **3.1 Flash Audio (2026-04)** | **3.1 Flash-Lite (2026-03)** + **3.1 Flash Image (2026-02)** | **3.1 Pro (2026-02)** —— 全家族矩阵 |
| [[Topics/13_base_model/Google_DeepMind/2511_Gemini_3/src/Gemini-3 - Google Blog\|Gemini 3 官方博客]] | 2025-11 | Gemini 进入"new era of intelligence" | **Most intelligent model** —— "bring any idea to life" | 全栈差异化（infra + research + tools + products） | **Agent-first development** 定位 |
| [[Topics/13_base_model/Google_DeepMind/2512_Gemini_3_Flash/src/Gemini-3-Flash - Google Blog\|Gemini 3 Flash 官方博客]] | 2025-12 | 把 frontier 智能普及到 Flash 速度和成本 | **Frontier intelligence built for speed** | **At a fraction of the cost** vs Gemini 3 Pro | 拉低 frontier 模型使用门槛 |
| [[Topics/13_base_model/Google_DeepMind/2602_Gemini_3_1_Pro/src/Gemini-3.1-Pro - Model Card\|Gemini 3.1 Pro Model Card]] | 2026-02 | Gemini 3 系列迭代 | Gemini 3 系列下一代 | **Advanced multimodal reasoning** | Model card 包含 limitations / mitigations / safety performance |

---

### 🏢 Meta / Llama

> **主线演进**: `Llama 4 herd (Scout/Maverick/Behemoth/Guard)` —— ⚠️ 注意是 2025-04，严格不在 2025-05 之后窗口，但作为最近一代 Llama 基座保留

#### 🌐 Web-Clippings

| 来源 | 月份 | 动机 | 1️⃣ 贡献 | 2️⃣ 贡献 | 3️⃣ 贡献 |
|------|------|------|---------|---------|---------|
| [[Topics/13_base_model/Meta_Llama/2601_Llama_4_Herd/src/Llama-4 - Meta AI Blog\|Llama 4 官方博客]] | 2025-04 | 开源社区需要新一代 native multimodal 模型 | **首个 open-weight native multimodal** 系列 | **Llama 4 Scout**（17B 激活/16 experts/**10M context**，单 H100 部署） | **Llama 4 Maverick**（17B/128 experts，超 GPT-4o/Gemini 2.0 Flash）+ Behemoth preview |
| [[Topics/13_base_model/Meta_Llama/2601_Llama_4_Herd/src/Llama-Guard-4 - Hugging Face\|Llama Guard 4 HF]] | 2025-04 | 开源社区需要多模态 safety 分类器 | **12B 多模态** safety classifier | 开源 | 配合 Llama 4 部署使用 |

> ⚠️ 目前 MOC 标注"2601_Llama_4_Herd"目录仅有 poster HTML，**缺独立 .md 笔记**。2601.11659（Secondary arXiv）作为汇总参考但未深度精读。

---

## Agentic RL & Verification 主线

> 这条线**不绑定单一公司**，是 2025-2026 涌现的方法论主线：把"agent 在真实环境中的能力"作为可训练目标。

#### 📄 论文笔记

| 模型 | 月份 | 动机 | 1️⃣ 贡献 | 2️⃣ 贡献 | 3️⃣ 贡献 |
|------|------|------|---------|---------|---------|
| [[Topics/13_base_model/Academic/2502_Agentic_Reasoning/Agentic-Reasoning-A-Streamlined-Framework-for-Enhancing-LLM\|Agentic Reasoning]] | 2025-02 | Reasoning 在结构化任务（math/coding）成功，但**非结构化领域**（社会/伦理/经验性）需事实验证 + 复杂逻辑关系，需 Deep Research 类能力 | **三类 agentic tools 框架** —— Web-Search Agent + Coding Agent + Mind-Map Agent（类似 GraphRAG） | 在 DeepSeek-R1 上达 **HLE 23.8%**，超所有公开开源模型 | 与 OpenAI Deep Research 差距仅 2.8% |
| [[Topics/13_base_model/Microsoft/2508_rStar2_Agent/rStar2-Agent-Agentic-Reasoning-Technical-Report\|rStar2-Agent]] | 2025-08 | Agentic RL 三大挑战 —— high rollout cost / environment noise / 训练效率 | **GRPO-RoC**（Resample-on-Correct rollout strategy）—— 当 rollout 正确时重新采样多条轨迹，增加正样本多样性 | **高效 RL infrastructure**（64 MI300X GPU）+ **关键发现：从 non-reasoning SFT 开始**（而非 thinking model） | **510 RL steps 把 14B 推到 AIME24 80.6% / AIME25 69.8%**，超 DeepSeek-R1 671B |
| [[Topics/13_base_model/MiroMind/2511_MiroThinker_v1/MiroThinker-Pushing-the-Performance-Boundaries-of-Open-Source-Research-Agents\|MiroThinker v1.0]] | 2025-11 | 现有 scaling 维度（model size + context length）已接近瓶颈；LLM test-time scaling 孤立操作可能退化 | **Interaction Scaling** —— 性能提升的第三 scaling 维度（与 model size、context length 并列） | 通过 RL 训练 agent-environment 更深更频繁交互，性能可预测提升（类似 scaling law） | 72B 模型 **GAIA 81.9% / HLE 37.7% / BrowseComp 47.1%**，逼近 GPT-5-high |
| [[Topics/13_base_model/MiroMind/2603_MiroThinker_1_7/MiroThinker-17-H1-Towards-Heavy-Duty-Research-Agents\|MiroThinker-1.7 & H1]] | 2026-03 | 复杂长程推理中错误会级联 + 最终答案需连贯证据链 + research agent 需 heavy-duty 能力 | **MiroThinker-H1：Verification Agent** —— Local Verification（中间推理步骤）+ Global Verification（整体轨迹） | **MiroThinker-1.7：Agentic Mid-training** —— Structured planning + Contextual reasoning + Tool interaction | 开源 1.7 + mini 版本在 GAIA / HLE / Financial Analysis 上展现竞争力 |

---

## 整体发展 Insight

### 1️⃣ Reasoning 从"后训练 trick"变成"预训练目标"

| 时间 | 关键节点 |
|------|----------|
| 2024-Q4 | o1/R1 把 reasoning 从 chain-of-thought prompting 变成 RL 训练范式 |
| 2025-Q2 | **Qwen3、MiniMax-M1、Gemini 2.5** 同步把 thinking 能力融入 base model 预训练 |
| 2025-Q3 | **GLM-4.5、GPT-5 unified system** 进一步把 thinking 作为 first-class mode |
| 2025-Q4 | **Claude 4.5/4.6/4.7** 默认 thinking，**Gemini 3** 原生多模态 reasoning |
| 2026 | **Deep Think / Self-Evolution** 出现：模型开始参与自身训练流程 |

**判断**：未来 12 个月内，"非 thinking base model"将变成 niche 产品（类似 non-RAG 搜索），主流 base 全部默认 thinking-on。

### 2️⃣ Agentic RL 算法范式收敛

```
POC: PPO → GRPO (DeepSeek) → DAPO → CISPO (MiniMax-M1)
                                        ↓
                          Agentic: GRPO-RoC (rStar2)
                                  CISPO + Forge (MiniMax-M2)
                                  Self-Critique Rubric Reward (Kimi K2)
                                  GSPO (Qwen3-ASR/TTS)
                                  Expert Distillation (Qwen3-Coder-Next)
                                  Verification (MiroThinker-H1)
                                  Agent Swarm + PARL (Kimi K2.5)
```

**判断**：CISPO/GRPO 已成为 RLHF 主流替代；Agent Swarm / Verification 是 2026 上半年最热子方向；Self-Evolution（M2.7）会进入 2026 下半年所有 major 玩家路线图。

### 3️⃣ 架构层面："Softmax is dead, long live Sparse/Linear Attention"

| 模型 | 架构创新 | 收益 |
|------|----------|------|
| MiniMax-M1 | **Lightning Attention**（hybrid MoE） | 1M context + 长 reasoning 链便宜 4× |
| Kimi Linear | **KDA**（Kimi Delta Attention）| per-channel 细粒度 gating，6× decoding throughput |
| Qwen3-Omni/3.5-Omni | **Thinker-Talker MoE** + Hybrid Attention | 多模态 + 256K context |
| MiniMax-M3 | **MSA**（MiniMax Sparse Attention）| 1M context 真正可扩展到 agent 级长任务 |
| GLM-4.5 | **sparsity 48** + loss-free balance | 推理成本 vs DeepSeek-V3 大幅下降 |

**判断**：2026 H2 之后，**Full attention 在 1M+ 上下文场景会被视为不可承受**。MSA/Linear Attention/Hybrid MoE 三条技术线将在 2026-2027 决出胜负。

### 4️⃣ 全模态基座"模态不降智"成为核心 KPI

| 模型 | 模态覆盖 | 不降智证据 |
|------|----------|-----------|
| Qwen3-Omni | text+image+audio+video | Thinker-Talker 解耦保证文本/视觉不退化 |
| Kimi K2.5 | text+vision | early fusion + zero-vision SFT 激活视觉，**视觉 RL 反向提升文本** |
| Gemini 3/3.1 | text+image+audio+video | 1M context 一次处理 |
| GLM-4.5V | vision+text | 9B 也能超 Qwen2.5-VL-72B |
| MiniMax-M3 | text+image+video+computer use | MSA 让多模态长上下文变得可负担 |

**判断**："先训纯文本，再补多模态"的旧范式已过时。**Joint multimodal pre-training**（K2.5 路径）是 2026 共识。

### 5️⃣ Agent Foundation Model 概念成型

**Seed1.8/Seed2.0 + GLM-4.5/5.1 + MiniMax-M2/M3 + Qwen3-Coder-Next** —— 都在说同一件事：

> "我们不是 general LLM，我们是**为 agent 场景优化的 base model**。"

证据：
- Seed2.0 明确提出 "Agent Foundation Model" vs "General Foundation Model" 的对比表
- MiniMax-M3 训练和评测都加 interactive user simulator（模拟持续澄清、反馈修正、任务切换）
- GLM-5.1 "Agentic engineering" 定位
- Qwen3-Coder-Next 的 Reward Hacking Blocker 专门防止 agent 在 SWE-bench 训练中作弊

**判断**：2026 下半年起，**base model 选型会分裂为两条线** —— "对话型 base"和"agent 型 base"。前者的代表作是 Qwen3 通用版，后者的代表作是 Seed2.0 / MiniMax-M3 / Claude 4.7。

### 6️⃣ 评测体系从 "Pass@1" 走向 "Long-horizon Verification"

| 时间窗口 | 主要评测 | 特征 |
|----------|----------|------|
| 2023-2024 | MMLU, HumanEval, GSM8K | 单轮、静态、有标准答案 |
| 2025 H1 | AIME, LiveCodeBench, Aider | 单轮 + 可调节 thinking budget |
| 2025 H2 | SWE-bench Verified, BrowseComp, GAIA | 多轮、agentic、需要环境交互 |
| 2026 H1 | **SWE-Bench Pro, Claw-Eval, VIBE-Pro, GDPval-AA, HLE** | 长时间跨度、需要 verification、模拟真实工作流 |

**判断**：未来 12 个月的 benchmark 主战场会是 **end-to-end agent evaluation**（不只是看能不能做对，还要看能不能 self-debug、self-verify、self-iterate）。

### 7️⃣ 国内外节奏对比

| 维度 | 国外（OpenAI/Google/Anthropic/Meta） | 国内（Qwen/MiniMax/Kimi/GLM/Seed） |
|------|------------------------------------|-----------------------------------|
| 节奏 | 闭源快，开放慢 | 论文+开源快，迭代密度高 |
| 路线 | Thinking + Computer Use + Robotics | Agent Foundation + Sparse Attention + Native Multimodality |
| 优势 | 商业化 + 生态（Codex/Claude Code） | 学术 + 开源透明度 + 价格优势 |
| 短板 | 架构黑盒化 | 部分基础研究滞后（如 scaling law 探索） |

**判断**：2026 年 frontier 模型上的"国内 vs 国外"差距在 **SWE-bench Pro / Claw-Eval** 这种真实工作流评测上已显著缩小（M3 超 GPT-5.5/Gemini 3.1 Pro），但在 **multi-modal creative tasks / brand new emergent capabilities** 上仍有 1 个版本的代差。

---

## 开放问题

- [ ] **Seed2.0 "Agent Foundation Model" 是否成为新标准范式？** —— 取决于 OpenAI/Anthropic 是否跟进专门做 agent 优化的 base model
- [ ] **MSA vs Linear Attention 谁会胜出？** —— Kimi Linear 和 MiniMax MSA 走的是不同路径
- [ ] **Self-Evolution 是否安全？** —— M2.7 的"模型参与自身 RL 实验循环"是亮点也是风险
- [ ] **Computer Use 是不是 base model 标配？** —— MiniMax-M3、Gemini 2.5 Computer Use、Seed2.0 都已支持
- [ ] **国内开源生态能否形成 "Qwen + MiniMax + Kimi" 三足鼎立？** —— 目前是混战，没收敛
- [ ] **Llama 5 何时发布？** —— Meta 在 2026 上半年明显慢于其他公司
- [ ] **国内大模型与 Claude Opus 4.7 / GPT-5.5 的真实差距？** —— 缺乏公平基准对比

---

## 关联主题

- [[Topics/5_gui/GUI MOC|GUI Agent MOC]] —— Computer Use / GUI Agent 是 base model 重要应用方向
- [[Topics/6_multimodal/Multimodal MOC|Multimodal MOC]] —— 全模态基座是多模态方向延伸
- [[Topics/7_rl/Reinforcement Learning MOC|RL MOC]] —— Agentic RL 是训练范式核心
- [[Topics/1_benchmarks/Benchmarks MOC|Benchmarks MOC]] —— 评测基准验证 base model 能力
- [[Topics/11_harness/Agent Harness MOC|Agent Harness MOC]] —— Agent Harness 是 evaluation infra
- [[Topics/9_self_play/Self Play MOC|Self-Play MOC]] —— Self-Evolution 的理论基础

---

## 数据来源统计

| 类别 | 数量 | 时间窗口 |
|------|------|----------|
| 📄 论文笔记 | 27 份 | 2025-02 至 2026-06 |
| 🌐 Web-Clippings | 31 份 | 2025-04 至 2026-05 |
| 🏢 覆盖公司 | 9 家（国内 5 + 国外 4）| — |
| 🎯 核心主线 | 4 条 | Reasoning / Agentic RL / Multimodal / Coding |
