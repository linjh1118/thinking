---
title: "Step-DeepResearch Technical Report"
type: paper
authors: ["Chen Hu", "Haikuo Du", "Heng Wang", "Lin Lin", "Mingrui Chen", "et al."]
year: 2025
venue: arXiv
arxiv: "2512.20491"
doi:
url: "https://arxiv.org/abs/2512.20491"
tags: [paper, deep-research, agent, 32b, stepfun]
status: read
rating: 5
topic: "13_base_model"
related: []
created: 2026-06-12
---

# Step-DeepResearch Technical Report

> [!tldr]
> Step-DeepResearch 是一个 32B 参数的 Deep Research Agent，通过"原子能力数据合成策略"（规划、信息检索、反思验证、报告生成）+ 三阶段渐进训练（Mid-training → SFT → RL）+ Checklist-style Judger 奖励设计，在 Scale AI ResearchRubrics 上取得 61.42 分，成本低于 0.50 RMB，超越 Kimi-k2-thinking（56.17）等开源模型，并可媲美 OpenAI/Gemini DeepResearch 等闭源商业系统。

## 问题与动机

### 核心痛点：Search ≠ Research

现有评测基准（如 BrowseComp）主要关注学术多跳搜索任务，与真实用户的开放域研究需求存在显著差距：
- **Search** 有明确答案，优化检索精度
- **Research** 是迭代过程，需要意图分解、规划、工具使用、跨源验证、结构化报告生成

多跳 QA 作为优化目标导致 Agent 过度偏向检索行为，像"高效的网络爬虫"而非"研究者"。

### 本文视角

将 Deep Research 重构为基于**原子能力**的长周期决策问题：
- 规划与任务分解
- 信息收集与跨源验证
- 反思与纠错
- 创意写作

核心观点：提升可用性不在于组装外部组件，而在于训练模型内化专家级认知循环，使其能在任务展开过程中自我检查和修正。

## 方法核心思路

### 1. 原子能力数据合成策略

将 Deep Research 分解为四个可迁移的高层动作抽象（原子能力），为每个原子能力构建定向数据：

| 原子能力 | 数据合成方法 |
|---------|------------|
| **规划与任务分解** | Reverse Engineering：从高质量报告/论文逆向推导"项目任务"，利用摘要作为" hindsight"约束 |
| **深度信息检索** | Graph-based：从 Wikidata5m、CN-DBpedia 采样子图，生成多跳问题；Multi-document：Wiki-doc 拓扑游走 |
| **反思验证** | Error-Reflection Loop：专家模型生成 → 结果验证 → 多轮反思（最多3次）；Deep Verification Workflow：Extract/Plan/Verify/Replan/Report 多智能体协作 |
| **报告生成** | Mid-training 学领域风格，SFT 学指令遵循和格式规范 |

关键设计：**原子动作子空间** $\mathcal{A}_{\text{atomic}} \subset \mathcal{A}_{\text{token}}$，将"预测下一个 token"重塑为"决定下一个原子动作"。

### 2. 三阶段渐进训练 pipeline

基于 Qwen2.5-32B-Base 构建：

```
Stage 1: Agentic Mid-training (32K → 128K context)
├── 32K: 规划/信息检索/反思/报告的原子能力注入（无工具调用）
└── 128K: 检索/规划/工具增强推理（引入工具调用）

Stage 2: Post-training SFT
└── 全链路轨迹对齐：Deep Search + Deep Research 端到端轨迹
    ├── "正确且最短"轨迹效率优化
    ├── 受控噪声注入（工具调用错误后接反思-纠正）
    └── 严格引文格式对齐

Stage 3: Reinforcement Learning (RL)
├── Two-Step Reverse Synthesis：生成任务 + 对应评分标准
├── Rubrics Judge 训练：从强模型学习评分逻辑和解释风格
├── Strict Reward Mapping：正 rubric 全满足=1，否则=0；负 rubric 反之
└── PPO + GAE（γ=1, λ=1）：actor-critic 结构支持 token 级学习信号
```

### 3. ADR-Bench 中文评测基准

为填补中文 Deep Research 评测空白，构建了 Application-driven Deep Research Benchmark：
- 70 条通用测试集：人类 Side-by-side 对比评估
- 40 条金融/法律专业测试集：LLM 按预设标准评分

采用 Elo 风格 rating 协议 + 多维质量标准。

## 实验结果

### ResearchRubrics 评测（Scale AI）

| 模型 | 分数 | 类别 |
|------|------|------|
| Gemini DeepResearch | 63.69 | 商业系统 |
| **Step-DeepResearch** | **61.42** | **单 Agent SOTA** |
| OpenAI DeepResearch | ~61 | 商业系统 |
| Kimi-Researcher | ~58 | 商业系统 |
| Kimi-k2-thinking | 56.17 | 开源模型 |
| DeepSeek-V3.2 | ~54 | 开源模型 |

**成本效率**：Step-DeepResearch 单次调用成本 < 0.50 RMB，是 Gemini DeepResearch（~6.65 RMB）的 1/13。

### ADR-Bench 人类评估（N=70）

- Step-DeepResearch vs Gemini：累计 Wins+Ties 达 67.1%
- Step-DeepResearch vs 非 Mid-training 版本：30 wins / 21 losses
- Mid-training 显著提升报告质量，更符合人类偏好

### 分维度分析

**ResearchRubrics 六维评估**：
- Implicit Criteria：54.5（超越 OpenAI DeepResearch 52.4）
- Explicit Criteria：72.0（领先）
- Citation Quality：57.0（与 Gemini 并列第一）
- Communication Quality：58.2（超越所有对手）

**ADR-Bench 金融/法律子集**：
| Tier | 系统 |
|------|------|
| Tier 1 (25-35) | Gemini DeepResearch |
| Tier 2 (15-25) | Step-DeepResearch, Kimi-Researcher, Kimi-k2-thinking, OpenAI DeepResearch |
| Tier 3 (0-15) | Qwen DeepResearch, MiniMax-M2, MiniMax Agent Pro, GLM-4.6 |

> [!insight]
> **核心启发**：32B 中等规模模型通过精细化训练可以达到专家级 Deep Research 能力，且成本效益极高。关键在于：
> 1. **原子能力分解**比端到端学习更有效——将"预测下一个 token"重塑为"决定下一个原子动作"
> 2. **Mid-training 是必要条件**——非 Mid-training 版本在 ADR-Bench 人类评估中输多赢少
> 3. **Rubrics Judge + Binary Reward Mapping** 解决了 RL 阶段部分满足状态的不一致问题，加速收敛
> 4. **单 Agent 架构**可以超越复杂多智能体协作——内化的原子能力比外部工作流编排更有价值
> 5. **中文评测基准的必要性**——金融/法律领域，负向评分标准对知识差距敏感，Agent 框架的流程优化无法弥补基础模型知识缺陷

## 相关工作链接

- [[Topics/11_harness/11_harness_综述_v2]] — Agent Harness 设计
- [[Topics/10_world_model/WorldModel MOC]] — World Model 相关
- [[Topics/12_skill/12_skill_综述_v2]] — Skill-Augmented RL
