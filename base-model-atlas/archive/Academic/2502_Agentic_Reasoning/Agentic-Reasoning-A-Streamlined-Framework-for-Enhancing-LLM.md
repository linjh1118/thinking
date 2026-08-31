---
title: "Agentic Reasoning: Enhancing LLM Reasoning with Agentic Tools"
type: paper
authors: ["Junde Wu", "Jiayuan Zhu", "Yuyuan Liu", "Min Xu", "Yueming Jin"]
year: 2025
venue: arXiv
arxiv: "2502.04644"
url: "https://arxiv.org/abs/2502.04644"
tags: [paper, agentic-reasoning, web-search, mind-map, deep-research]
topic: "13_base_model"
status: read
rating: 5
created: 2026-05-30
---

# TL;DR

**Agentic Reasoning 是 Deep Research 的开源最强代表**，核心创新是集成三类 agentic tools：Web-Search Agent（信息检索）、Coding Agent（计算分析）、Mind-Map Agent（知识图谱记忆）。在 DeepSeek-R1 上实现 23.8% on Humanity's Last Exam，超越所有公开模型，与 OpenAI Deep Research 差距仅 2.8%。

## 问题与动机

### Reasoning 的局限

- **Structured domains**（math/coding）：outcome 可验证，RL 效果好
- **Unstructured domains**（social science, ethics, experiential）：形式化推理不适用，需要事实验证、复杂逻辑关系

### Deep Research 的核心需求

- Extensive research（广泛研究）
- Repeated verification（重复验证）
- Information retrieval（信息检索）
- Computational analysis（计算分析）
- Organizing complex logical relationships（组织复杂逻辑关系）

## 方法核心思路

### Agentic Reasoning Pipeline

```
User Query
    ↓
┌─────────────────────────────────────────────────────┐
│           Reasoning LLM (DeepSeek-R1)                │
│  ┌─────────────────────────────────────────────┐   │
│  │ <thinking> ...                              │   │
│  │ <web-search> [query] → Web-Search Agent    │   │
│  │ <coding> [task] → Coding Agent             │   │
│  │ <mind-map> [context] → Mind-Map Agent      │   │
│  └─────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────┘
    ↓
Final Answer (with evidence chain)
```

### Mind-Map Agent（关键创新）

**知识图谱构建**：
- LLM 从推理链中提取实体
- 识别实体间的语义关系（类似 GraphRAG）
- 社区聚类（Louvain algorithm）
- 每个聚类生成摘要

**两大功能**：
1. **Context Provision**：为外部工具提供结构化推理上下文
2. **Memory Retrieval**：长推理链中不确定时，查询 Mind-Map 获取相关信息

### Web-Search Agent

四组件 pipeline：
1. **Query Breakdown**：将原始 query + Mind-Map context 重写为搜索优化 query
2. **Search Service**：Bing 搜索，返回 top 20 相关页面
3. **Re-ranking Service**：Cohere Rerank 3.5，按相关性排序
4. **RAG**：提取有意义 insights，合成最终 snippet

### Coding Agent

设计决策：**不用 reasoning model 直接生成代码**，而是委托给 specialized coding LLM（Claude-3.5-sonnet）

好处：
- Reasoning model 保持专注于核心推理
- 更长的连贯推理链
- Claude 更擅长 coding tasks

## 关键结果

### Humanity's Last Exam

| Model | Accuracy |
|-------|----------|
| GPT-4o | 3.3% |
| OpenAI o1 | 9.1% |
| **DeepSeek-R1** | **9.4%** |
| OpenAI o3-mini (high) | 13.0% |
| **Agentic Reasoning w/ R1** | **23.8%** (+14.4%) |
| Perplexity deep research | 21.1% |
| OpenAI deep research | 26.6% |

**差距仅 2.8%！**

### GAIA Benchmark

| Level | Agentic Reasoning | OpenAI Deep Research |
|-------|------------------|---------------------|
| Level 1 | 74.36 | 74.29 |
| Level 2 | 69.21 | 69.06 |
| Level 3 | 45.46 | 47.60 |
| **Avg** | **66.13** | **67.36** |

### Deep Research (Human Evaluation)

| Method | Interest | Organization | Relevance | Coverage |
|--------|----------|--------------|-----------|----------|
| Gemini-DR | 2.7 | 2.5 | 2.3 | 3.0 |
| STORM | 2.9 | 3.2 | 2.9 | 3.7 |
| **Ours** | **3.7** | **4.6** | **4.2** | **4.1** |

## Ablation 关键发现

### 1. Tool Quality > Tool Quantity

| Toolbox | GPQA Performance |
|---------|-----------------|
| HuggingFace (7 tools) | ↓ |
| LangChain (109 tools) | ↓↓ |
| Web search + Mind-Map + Coding | **Best** |

### 2. 工具组合的协同效应

- Web search + Mind-Map > Web search + Coding > Mind-Map + Coding
- 三个工具组合 > 任意两个组合（synergy effect）

### 3. Mind-Map 特别有效于

- **Long reasoning chains with many tool calls**
- **Logic-heavy questions**（如 modified riddle: "The surgeon is the boy's father"）
- **Strategic reasoning**（Werewolf game: 72% win rate vs 36% without Mind-Map）

## 对研究的启发

> [!insight]
> 1. **Mind-Map Agent** 的设计对 GUI Agent 有重要参考——GUI 任务需要维护复杂的状态历史，结构化记忆是关键
> 2. **Tool synergy** 的发现很重要，不是工具越多越好，而是需要互补的工具组合
> 3. Agentic tool call 比 direct API call 更 robust，因为可以 self-monitor confidence
> 4. **Deep Research 的 gap 缩小到 2.8%** 说明开源模型通过 agentic 增强可以接近闭源水平

## 相关链接

- 论文: [arXiv Link](https://arxiv.org/abs/2502.04644)
- GitHub: [theworldofagents/Agentic-Reasoning](https://github.com/theworldofagents/Agentic-Reasoning)
