---
title: "MiMo-V2-Omni: Unified Omnimodal Foundation Model for Perception and Agency"
authors: ["Xiaomi MiMo Team"]
year: 2026
venue: Official Blog
arxiv: ""
doi: ""
url: "https://mimo.xiaomi.com/mimo-v2-omni"
tags: [paper, omnimodal, agentic, perception, video, audio, xiaomi]
topic: "13_base_model"
status: read
rating: 4
related: ["[[Topics/13_base_model/Xiaomi_MiMo/2601_MiMo_V2_Flash/MiMo-V2-Flash]]", "[[Topics/13_base_model/Xiaomi_MiMo/2604_MiMo_V2_5/MiMo-V2.5]]", "[[Topics/13_base_model/Base Model MOC]]"]
created: 2026-06-11
---

# MiMo-V2-Omni

> [!tldr]
> MiMo-V2-Omni 是小米发布的全模态（Omnimodal）基座模型，**统一融合图像/视频/音频/文本四大模态**到单一共享 backbone，perception 与 agency 一体化训练。核心卖点：在 Audio（76.8 MMAU-Pro）、Video（94.0 Video-MME）、Agentic（52.0 Multi-Modal Agent）上达到或接近顶级闭源模型水平，且原生支持 structured tool calling、function execution 和 UI grounding。

---

## 1. 问题与动机

现有 VLM 多为"感知型"——能看图说话但不能行动。真正需要的是 **agentic multimodal model**：不仅理解图像/视频/音频，还要能基于感知做决策、调用工具、操作界面。

**核心挑战**：
1. 多模态融合：图像、视频、音频、文本四种模态如何统一建模？
2. Perception-Action 一体化：感知与行动能否在训练阶段就融合，而不是分阶段？
3. 长时序理解：10小时连续音频理解、分钟级自动驾驶视频分析

---

## 2. 核心方法

### 2.1 统一 Omnimodal 架构

MiMo-V2-Omni 将**专用图像、视频、音频 encoder** 通过轻量 projector 连接到统一语言 backbone：
- **不是** separate capabilities bolted together
- **而是** unified perceptual stream，模型同时看、听、读

### 2.2 Perception-Action 一体化训练

核心思路：**训练模型预测未来，而非只描述现在**。

> "What is in the scene, what will happen next, what should be done now" — 模型从第一步就学习这三个能力。

Perception 和 Action **永不分离**：它们作为连续推理过程同时涌现，而非分阶段训练。

### 2.3 原生 Agentic 能力

输出端原生支持：
- Structured tool calling
- Function execution
- UI grounding

可直连 OpenClaw 等 agent scaffold，无需额外 adaptation layer。

---

## 3. 实验结果

### 3.1 感知能力

| Benchmark | Task | MiMo-V2-Omni | 对比最强 |
|-----------|------|-------------|---------|
| **MMAU-Pro** | Audio Understanding | **76.8** | GPT-5.2: 79.5, Gemini 3 Pro: 81.0 |
| **BigBench-Audio** | Speech Reasoning | **80.1** | GPT-5.2: 82.1, Claude Opus 4.6: 77.4 |
| **MMMU-Pro** | Multimodal Reasoning | 85.3 | Gemini 3 Pro: 88.4 |
| **Video-MME** | Video QA | **94.0** | Gemini 3 Flash: 99.2 |
| **CharXiv RQ** | Chart Understanding | **66.7** | Gemini 3 Flash: 62.9 |

**亮点**：
- Audio 超越 Gemini 3 Pro（76.8 vs 81.0 MMAU-Pro，差距最小）
- 10小时连续音频理解（播客摘要任务）
- 自动驾驶 dashcam 实时风险评估演示

### 3.2 Agentic 能力

| Benchmark | Task | MiMo-V2-Omni | 对比最强 |
|-----------|------|-------------|---------|
| **Multi-Modal Agent** | Agent | **52.0** | Claude Opus 4.6: 59.3 |
| **MM-BrowserComp** | Web Browsing | 49.8 | Gemini 3 Pro: 62.5 |
| **OmniGAIA** | Multimodal Agent | 54.8 | Claude Opus 4.6: 66.3 |
| **SWE-Bench Verified** | Code Agent | 1410 | Claude Opus 4.6: 1606 |
| **GDPVal** | Professional Tasks | **81.2** | Claude Opus 4.6: 81.5 |

**亮点**：
- 超越 Gemini 3 Pro/Flash、GPT-5.2 在 agentic benchmarks
- 端到端浏览器自动化演示：小红书调研 → 京东下单 → 客服砍价
- TikTok 视频生成+上传全流程演示

---

## 4. 关键演示

### 4.1 自动驾驶实时风险评估

输入：沿海小镇 dashcam 视频（~7分钟）
指令：作为自动驾驶视觉大脑，实时识别安全隐患

输出：时间戳分段风险分析：
- 环岛让行风险、骑行者弱势道路使用者
- 建筑遮挡"隧道视野"、行人路边行走
- 街道清洁车慢速障碍物、违规过马路检测

### 4.2 长音频理解

输入：7小时播客访谈（谢赛宁 × Yann LeCun）
输出：结构化摘要，捕获跨小时的话题逻辑串联

### 4.3 全链路 Agent 演示

**任务**：帮用户选购小米17手机
1. 小红书调研（10+帖子）
2. 京东比价
3. 客服聊天砍价
4. 加购下单

**任务**：生成并发布 TikTok 视频
1. 设计4个场景分镜
2. 编程合成音频（bass、electronic tones、whoosh effects）
3. 渲染15秒 1080p 视频
4. 上传到 TikTok（处理非标准 DOM 结构）
5. 填写描述、发布、评论

---

## 5. 对研究的启发

> [!insight]
> **感知与行动必须一体化训练，而非分阶段拼接**。MiMo-V2-Omni 的核心设计是让模型从第一阶段就同时学习"场景有什么"、"下一步发生什么"、"现在该做什么"。这与传统的感知→决策→行动分离范式完全不同。

> [!insight]
> **Audio understanding 是多模态模型的盲区**，大多数 VLM 聚焦图像，音频仅作为 transcription。MiMo-V2-Omni 在 10 小时连续音频上验证了真实世界理解能力，这是未来具身 AI 的关键能力。

---

## 6. 技术定位

MiMo-V2-Omni 是 MiMo V2 系列的**全模态旗舰**：

```
MiMo-7B (Dense, reasoning base)
    ↓
MiMo-VL-7B (加入视觉理解)
    ↓
MiMo-V2-Flash (MoE, MTP, Hybrid SWA)
    ↓
MiMo-V2-Pro (更强的 agentic 能力)
    ↓
MiMo-V2-Omni (统一四大模态 + 原生 agentic)
    ↓
MiMo-V2.5 (多模态 + 更强 agentic，开源)
```

---

## 7. 开放问题

1. **Omnimodal tool calling 是否需要 modality-specific action heads？** 当前 unified text output + structured parsing 是否最优？
2. **10小时音频理解的可扩展性**：推理成本如何？是否对所有长音频任务都需要全量输入？
3. **与 V2.5 的关系**：V2.5 是否是 Omni 的能力子集还是独立演进路线？

---

## 相关资料

- 博客原文：[[2603_MiMo_V2_Omni/src/MiMo-V2-Omni - Xiaomi Blog]]
- MiMo-V2-Flash：[[Topics/13_base_model/Xiaomi_MiMo/2601_MiMo_V2_Flash/MiMo-V2-Flash]]
- MiMo-V2.5：[[Topics/13_base_model/Xiaomi_MiMo/2604_MiMo_V2_5/MiMo-V2.5]]
