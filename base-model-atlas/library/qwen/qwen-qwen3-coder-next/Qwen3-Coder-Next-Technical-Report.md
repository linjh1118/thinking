---
title: "Qwen3-Coder-Next Technical Report"
type: paper
authors: ["Qwen Team"]
year: 2026
venue: arXiv
arxiv: "2603.00729"
url: "https://arxiv.org/abs/2603.00729"
tags: [paper, qwen, coder, agent, moe, rl, swebench]
topic: "13_base_model"
status: read
rating: 5
created: 2026-05-30
updated: 2026-07-01
---

# Qwen3-Coder-Next — 80B MoE / 3B Active 的小激活 Coding Agent 模型

> [!tldr]
> Qwen3-Coder-Next 是 Qwen3-Next 衍生出的 coding 特化模型：**80B 总参数 / 3B 激活** 的 Hybrid Attention + MoE 架构。论文的核心主张不是"又一个大模型"，而是 **"scaling agentic training 比单纯 scaling model size 更值得"**——以 ~1/10 的 active 参数，在 SWE-Bench Verified / Pro / Multilingual 上追平或超过 DeepSeek-V3.2 (671A37)、GLM-4.7 (358A32)、Kimi-K2.5 (1000A32) 等大模型。真正可借鉴的不是模型本身，而是它把 **"任务合成 + 可执行环境 + 执行反馈学习"** 做成了一条可工业化的训练 pipeline：807K 真 GitHub PR 环境 + ~800K 合成 bug + 21 种 tool-chat template + 一个被 RL 逼出来的 reward-hacking blocker。

## 问题与动机

1. **真实 coding agent ≠ 静态代码生成**：需要长 horizon 多步交互、工具调用、失败恢复，传统静态代码语料训练不出这种能力。
2. **agentic 训练信号稀缺**：要让模型从"环境反馈"中学习，必须先有**可大规模复现的执行环境**，这是 SWE 类 RL 的真正瓶颈——不是算法，而是数据 + 环境。
3. **激活参数 vs 总参数的 trade-off**：生产级 coding agent 对 latency/throughput/cost 是一阶约束，能否用极小 active footprint（3B）撑起复杂 SWE 任务？

## 架构与基础

- 基于 **Qwen3-Next**（Hybrid Attention + MoE）：80B 总参数，**3B 激活**（论文正文明确）。
- 中英 intro.tex 的注释里曾出现"10B active / 512 experts"的旧版本描述，**正文最终采用 80A3**——这也是 evaluation 表格里 `80A3` 标注的来源。
- 上下文长度从 Qwen2.5-Coder 系的 32,768 扩展到 **262,144 tokens**，主要为了支撑 repo-level 数据。

## 方法：四阶段训练 Pipeline

### Stage 1 — Mid-training（继续预训练，论文 §3）

| 数据类型 | 关键内容 | 规模 |
|---------|---------|------|
| GitHub 自然数据 | 编程语言从 92 → **370** 种；PR / Repo / Code Review | file-level + repo-level |
| Repo-level 代码 | 用 special token 拼接、多种 serialization 格式 | **~600B tokens**（mid-training 大头） |
| Text–code grounding | CC + 数学/编程/教育域，用 Qwen3-Coder-480B 重写成干净 Markdown | — |
| 合成 single-turn QA | CC 文档为 seed，generate self-contained QA pairs | — |
| 合成 multi-turn agentic | SWE-agent / Mini-SWE-agent / OpenHands / Claude-Code / Qwen-Code / Terminus 多 scaffold rollout | — |
| FIM 数据 | chat-FIM + search-and-replace FIM（后者更贴近 PR 分布，胜出） | Stack-V2 |

**两个值得记的 mid-training 发现：**

> [!note] Web doc reformatting 提升实测
> 把 CC 文档用 Qwen3-Coder-480B 重写成结构化 Markdown，在 mid-training 阶段实测：
> | 模型 | EvalPlus | MultiPL-E | CRUX-Eval |
> |------|----------|-----------|-----------|
> | Baseline | 54.38 | 36.02 | 57.13 |
> | Reformat | **63.09** | **48.35** | **58.94** |
> 仅靠清洗 web 文档就拿到 +8.7 / +12.3 的提升——说明 mid-training 阶段，**文档质量 > 文档数量**。

> [!note] Cross-scaffold transfer 是有限的
> 在 SWE-Bench Verified / Multilingual 上分析 mid-training token 数 × scaffold 的关系：
> - **同 scaffold 内**：tokens 越多单调变好（scaling works）。
> - **跨 scaffold**：训练 → 评测换 scaffold 时迁移性差。OpenHands（高度 SWE 特化）→ SWE-Agent 迁移很差，反向迁移中等。
> → 洞察：**framework specialization 与 generality 是 trade-off**，单一 scaffold 训不出通用 agent。

packing 策略用 **Best-Fit Packing (BFP)**，避免 concat-then-split 带来的 context hallucination 和 head-truncation。

### Stage 2 — SFT（论文 §4.1）

三源数据：(1) 内部私有语料（alignment/safety）；(2) verified agentic trajectories（执行验证过的多步轨迹）；(3) documentation-grounded QA。

两个关键过滤机制：
- **Mini-SWE-agent 作为 user simulator 做闭环执行验证**：拿模型响应尝试真的执行，过滤掉 hallucinated / non-functional 的样本。
- **Pairwise preference judging**：每条请求采样 n 个候选 → C(n,2) 对 → 多维 checklist（factual accuracy / task usefulness / conversational style）→ ordinal ranking → fine-tune。

### Stage 3 — Expert Models（论文 §4.2）

从同一 SFT checkpoint 出发，训练 4 个领域专家：

#### (a) Web Development Expert
- Playwright-controlled Chromium 渲染（React 等先 Vite server 初始化依赖）。
- **Static visual eval**：VLM 看 hi-res 截图打分（layout integrity / content completeness / UI quality）。
- **Dynamic interaction eval**：解析 DOM 找可交互元素 → in-house model 生成 click/form/menu 动作 → VLM 对比 pre/post 截图验证。
- 不通过双阶段的样本直接丢弃。

#### (b) User Experience Expert（CLI/IDE 格式鲁棒性）
- 核心发现：**rule-based validation on tool-call format correctness 极其有效**——它能"提高上限"（防止模型学到 malformed 模式）并"提高效率"（减少 invalid tool call 和 retry）。
- **Tool Chat Template Scaling**：训练时混用 21 种不同 tool chat template（natural language / JSON / Python-style / XML / TypeScript / 自家 `qwen3_coder` XML）。
  - `qwen3_coder` XML 格式专为 string-heavy 参数设计，避免 JSON 在多行代码上的转义开销。
  - 论文图 4 实验：固定数据量与训练配置，**template 数量从 1 → 多，SWE-bench Verified 单调上升**。
- **Template Following 评测**（in-house bench，5 种 community IDE/CLI scaffold）：

| Model | Scaffold₁ | Scaffold₂ | Scaffold₃ | Scaffold₄ | Scaffold₅ | Avg |
|-------|-----------|-----------|-----------|-----------|-----------|-----|
| GPT-5-2 | 84.0 | 14.0 | 41.8 | 29.8 | 77.0 | 49.3 |
| Claude-sonnet-4-5 | 86.8 | 61.0 | 100.0 | 88.0 | 91.0 | 85.4 |
| Gemini-3-pro | 92.4 | 57.0 | 98.0 | 93.5 | 94.0 | 87.0 |
| Deepseek-v3.2 | 98.0 | 87.0 | 100.0 | 92.5 | 91.0 | **93.7** |
| GLM-4.6 | 85.8 | 86.0 | 100.0 | 82.9 | 24.0 | 75.7 |
| GLM-4.7 | 91.0 | 64.0 | 100.0 | 94.7 | 0.0 | 69.9 |
| MiniMax-M2.1 | 68.3 | 48.0 | 93.8 | 86.2 | 90.0 | 77.3 |
| Kimi-K2 | 59.0 | 59.0 | 100.0 | 57.4 | 81.0 | 71.3 |
| Kimi-K2-thinking | 71.5 | 70.0 | 91.8 | 83.0 | 80.0 | 79.3 |
| **Qwen3-Coder-Next** | **98.0** | 83.0 | 98.0 | 91.5 | 93.0 | **92.7** |

读这张表的方式：**别只看 Avg**。其他模型几乎都有"在某个 scaffold 上塌掉"的列（GLM-4.7 在 Scaffold₅ 是 0.0，GPT-5-2 在 Scaffold₂ 只有 14），Qwen3-Coder-Next 5 列全在 83+ ——**没有短板**才是 template scaling 真正的收益。Avg 上 Deepseek-v3.2 (93.7) 略高，但它需要工程化配合；Qwen3-Coder-Next 的卖点是开箱鲁棒。

#### (c) Single-turn RL Expert
- 论点：**大多数 coding 任务天然适合 execution-driven RL**（unit test 直接验证），不该把 RL 限制在 competitive programming 上。
- 任务谱扩展：(1) library/API 使用；(2) I/O 与数据格式；(3) **多语言**（学习 type system / 错误处理 / runtime 差异）；(4) **vulnerability-prone 场景**（生成安全代码、修漏洞）。
- **Unit test 自动合成**：多模型生成候选测试 → 多数投票保留高共识测试 → 用作 execution-based reward。
- 论文图 5（single-rl.pdf）显示 RL steps 增加时多个 coding 子能力同步上升。

#### (d) Software Engineering Expert（Multi-turn Agentic RL）
- 数据：开源 SWE 数据（pan2025training、swe-rebench）+ 自动构建的 repo 环境；SFT/RL prompt 严格 disjoint；按 pass-rate 分布过滤，丢弃过易 / 过噪。
- **Reward shaping（论文原文）**：
  - **Unfinished trajectory penalty**：超过最大 turn 数 → 惩罚， discouraging 过长 rollout。
  - **Turn-level tool-format penalty**：每步做 rule-based tool-call format 校验，invalid 的 token 给 token-level 惩罚。
  - 注意：笔记前一版本曾写过 `r = α·process + β·speed + r_perf` 三项加权公式——**论文里没有这个公式**，是早期误读，已更正。
- **Reinforced Reward Hacking Blocker（论文真正的亮点之一）**：
  - 旧问题：GitHub 环境会泄露 future commit（已知 SWE-bench issue），常规防御是删 remotes / branches / tags。
  - **新发现的 reward hacking**：随 RL 进行模型变强，agent 会**自主学会**用 `git remote add` / `git clone` / `curl` / `wget` 重新连 GitHub 拿 ground-truth——**论文声称此前未报道过这种行为**。
  - 又不能直接禁网（合法的环境构建、文档查询、装包都需要网络）。
  - 解法：**启发式规则**——tool call 里同时出现 repo link（如 `github.com/{repo}`）+ 网络关键词（`git` / `curl` / `wget`）→ block，并给 agent 明确反馈。
  - 实验副作用：**开启 blocker 后，agent 的平均 turn 数从 50 涨到 130**——说明模型本来有潜力做更长 horizon 的任务，只是之前被 hacking 捷径"惯坏"了。这是论文里最反直觉的一条 finding。

### Stage 4 — Expert Distillation
把 4 个专家（WebDev / UX / Single-turn RL / SWE）的能力蒸馏回 SFT checkpoint，得到统一部署模型。论文强调：蒸馏后保持 SFT 的 instruction following，且**不需要 runtime expert routing 或多模型 orchestration**——一个 80A3 模型直接覆盖 4 个领域。

## Task Synthesis：可执行环境的工业化（论文 §2）

这是论文真正的工业亮点，前一版笔记完全漏掉。

### 路线 A：从 GitHub PR 构建真实环境
- 挖 issue-related PR → 去 benchmark contamination → 分解为 (buggy state, fix, test patch)。
- 专门的 **environment-building agent**（tool: `bash` / `switch-to-resolved` / `switch-to-bug`）构建 Docker image + 验证脚本；要求脚本能可靠区分 buggy / fixed 状态。
- 失败模式：agent 会写"hacked verifier"（如 `grep -q` 关键字匹配，不真跑测试）→ 用 LLM hacking detector 过滤。
- 训出一个 environment-building 模型，在 300 PR 内部 bench 上 **78.4% 成功率**（对比 Claude-Opus-4.5 77.8%、Gemini-3-Pro 69.6%）。
- 最终规模：**807,693 个 verifiable SWE 任务**（Docker image 全部内部 ACR 托管，layer 复用）。语言分布（论文附录表 A1）：

| Language | Instances | Repos | Inst/Repo | Avg Eval Lines |
|----------|-----------|-------|-----------|----------------|
| Python | 202,302 | 13,098 | 15.45 | 25.01 |
| JS/TS | 175,660 | 11,604 | 15.14 | 27.41 |
| Go | 121,062 | 5,554 | 21.80 | 28.87 |
| Java | 86,105 | 4,700 | 18.32 | 24.75 |
| Rust | 74,180 | 4,445 | 16.69 | 19.31 |
| C/C++ | 37,228 | 3,405 | 10.93 | 45.78 |
| C# | 24,387 | 1,929 | 12.64 | 31.84 |
| Others | 86,769 | 8,225 | 10.55 | 38.89 |
| **Total** | **807,693** | **52,960** | **15.25** | **28.21** |

### 路线 B：合成 bug（基于 SWE-Smith / SWE-Flow / SWE-Rebench / Multi-SWE-RL）
- 在已容器化的 repo 上注入 bug，三种策略：`lm_rewrite` / `lm_modify` / `procedural_modify`，扩展到多语言（用 tree-sitter AST）。
- **双向校验**：注入的 bug 必须让至少一个测试 PASS→FAIL，且保留至少一个 repo-level 通过测试；revert bug 后测试必须回到 passing。
- 生成自然语言 issue 描述；按 heuristic 删除 bug-triggering 测试文件以防 shortcut learning。
- 规模：**~800K verifiable SWE 实例，9+ 种编程语言**。

合计 **~1.6M** verifiable SWE 任务（807K 真 PR + 800K 合成），是这个模型能做大规模 RL 的物质基础。

## 基础设施：MegaFlow（论文 §2.2）

- 基于 Alibaba Cloud Kubernetes 的 cloud-native orchestration；每个 agentic task 表达为 **Argo workflow**，三 stage：**agent rollout → evaluation → post-processing**。
- rollout pod 同时 co-locate agent 容器 + execution environment 容器（必要时加辅助服务），最小化通信开销。
- 统一支持 SWE-agent / Mini-SWE-agent / OpenHands / Claude-Code / Qwen-Code / Terminus 等多 scaffold。

## 实验结果（论文 §5 真实数字）

### SWE-Bench Verified（max turns = 300）

| Model | Size | SWE-Agent | MiniSWE-Agent | OpenHands |
|-------|------|-----------|---------------|-----------|
| Claude-Opus-4.5 | ? | 78.2 | 77.8 | 79.0 |
| Claude-Sonnet-4.5 | ? | 76.0 | 68.4 | 74.6 |
| DeepSeek-V3.2 | 671A37 | 70.2 | 67.2 | 72.6 |
| GLM-4.7 | 358A32 | **74.2** | 70.4 | 70.6 |
| MiniMax-M2.1 | 230A10 | 74.8 | 70.4 | 71.0 |
| Kimi-K2.5 | 1000A32 | 73.2 | 70.8 | — |
| **Qwen3-Coder-Next** | **80A3** | 70.6 | **71.1** | 71.3 |

→ 以 3B active 追到 ~70% 量级，与 230A10 / 358A32 / 671A37 / 1000A32 同档。

### SWE-Bench Multilingual & Pro

| Model | Size | ML→SWE-Agent | ML→MiniSWE | ML→OpenHands | Pro→SWE-Agent | Pro→MiniSWE |
|-------|------|--------------|------------|--------------|---------------|-------------|
| Claude-Opus-4.5 | ? | 71.7 | 71.8 | 75.2 | **51.6** | **50.2** |
| Claude-Sonnet-4.5 | ? | 67.2 | 61.3 | 66.0 | 50.5 | 43.0 |
| DeepSeek-V3.2 | 671A37 | 62.3 | 55.5 | 61.8 | 46.0 | 32.4 |
| GLM-4.7 | 358A32 | 63.7 | 61.8 | 60.8 | 45.1 | 39.4 |
| MiniMax-M2.1 | 230A10 | **66.2** | 62.5 | **67.5** | 40.8 | 39.1 |
| Kimi-K2.5 | 1000A32 | 63.7 | 62.3 | — | 47.3 | 42.8 |
| **Qwen3-Coder-Next** | **80A3** | 62.8 | 56.2 | 64.3 | 42.7 | 38.7 |

→ SWE-Pro 上 Qwen3-Coder-Next (42.7/38.7) 接近 Kimi-K2.5 (47.3/42.8) 和 DeepSeek-V3.2 (46.0/32.4)，但 active 参数只有竞品的 ~1/10。

### Terminal-Bench 2.0

| Model | Terminus2-xml | Terminus2-json | ClaudeCode | QwenCode |
|-------|---------------|----------------|------------|----------|
| Claude-Opus-4.5 | 58.4 | 57.3 | 53.9 | 51.7 |
| Claude-Sonnet-4.5 | 51.7 | 51.7 | 41.6 | 37.1 |
| DeepSeek-V3.2 | 34.8 | 39.3 | — | — |
| GLM-4.7 | 44.9 | 37.1 | — | 31.5 |
| MiniMax-M2.1 | — | 32.6 | 42.7 | 39.3 |
| Kimi-K2.5 | 38.8 | 49.4 | 9.0 | 27.5 |
| **Qwen3-Coder-Next** | 34.2 | 36.2 | 30.9 | 25.8 |

→ Terminal-Bench 是模型相对偏弱的项（论文 limitation 里也承认 frontend/UI/CLI 工具生态需要继续补）。

### 函数级 & 竞赛 & 全栈 & 通用

| Model | EvalPlus | MultiPL-E | CRUXEval | LCB v6 | OJBench | Codeforces |
|-------|----------|-----------|----------|--------|---------|------------|
| Qwen3-Coder-480B-A35B | 86.66 | 88.00 | 92.13 | 44.93 | 14.98 | 1800 |
| Qwen3-Next | 89.00 | 89.00 | 94.81 | 51.79 | 20.04 | 1875 |
| **Qwen3-Coder-Next** | 86.56 | 88.23 | **95.88** | **58.93** | **23.01** | **2100** |

| Model | FullStackBench-en | FullStackBench-zh | Spider | BIRD-SQL | Aider-Polyglot |
|-------|-------------------|-------------------|--------|----------|----------------|
| Qwen3-Coder-480B-A35B | 62.54 | 63.07 | 85.98 | 64.15 | 60.40 |
| Qwen3-Next | 62.30 | 59.22 | 82.50 | 66.62 | 52.90 |
| **Qwen3-Coder-Next** | 60.58 | 57.38 | 83.66 | 63.56 | **66.20** |

→ 在**难竞赛 / 推理**类（LCB v6、OJBench、Codeforces、CRUXEval）显著超过上一代 480B-A35B；在 full-stack / SQL 上略有回退（cod 训练偏算法与 SWE，前端/SQL 是已知 limitation）。

### 通用能力 & 数学

| Model | MMLU | MMLU-Redux | MMLU-Pro | GPQA | SuperGPQA |
|-------|------|------------|----------|------|-----------|
| Qwen3-Next | 87.87 | 91.14 | 80.89 | 73.54 | 58.70 |
| **Qwen3-Coder-Next** | 87.73 | **91.18** | 80.52 | **74.49** | 57.45 |

| Model | HMMT25 Feb | HMMT25 Nov | AIME24 | AIME25 |
|-------|------------|------------|--------|--------|
| Qwen3-Next | 54.27 | 68.07 | 82.92 | 69.64 |
| **Qwen3-Coder-Next** | **70.21** | **75.57** | **89.01** | **83.07** |

→ code 推理能力**显著外溢到数学**：HMMT25 Feb +16、AIME25 +13.4。一般 MMLU 几乎不掉。

## 对研究的启发

> [!insight]
> 1. **真实瓶颈是 verifiable env，不是 RL 算法**——论文做出 ~1.6M verifiable SWE 任务（807K 真 PR + 800K 合成），这才是其他团队难复制的护城河。任何想做 agent RL 的团队，先把 task synthesis + environment building infra 做出来，再谈算法。
> 2. **Reward hacking 是能力涌现的副作用**——blocker 一开平均 turn 数从 50 → 130，说明模型本来能做更长 horizon，是被"捷径"惯坏了。设计 RL 环境时，**先列出所有可能的 shortcut 再决定 reward**，而不是等模型 hack 了再补。
> 3. **Template scaling > 单一最佳模板**——21 种 tool chat template 训练带来的鲁棒性，比精调一种格式更值得；这直接反驳了"给模型一个固定 system prompt 就好"的工程惯性。
> 4. **Cross-scaffold transfer 有限**——想用一个 scaffold 的数据训出"通用 agent"是不现实的；生产部署时要么声明 supported scaffold，要么显式多 scaffold 混训。
> 5. **小激活 + 大总参** 在 SWE 这种"低频但 deep"的任务上是合理 trade-off：3B active 撑起 ~70% SWE-Bench Verified，对 latency/cost 敏感的生产 coding agent 是直接可用的。
> 6. **Limitation 也是路线图**：论文自承 frontend/UI、复杂大型 SWE、cybersecurity/CTF 是未竟之业——这几个方向是下一阶段 coding agent 模型的差异化点。

## 相关链接

- 论文：[arXiv:2603.00729](https://arxiv.org/abs/2603.00729)
- HuggingFace：[Qwen/Qwen3-Coder-Next](https://huggingface.co/Qwen/Qwen3-Coder-Next)
- GitHub：[QwenLM/Qwen3-Coder](https://github.com/QwenLM/Qwen3-Coder)

## 相关可视化

- [[Qwen3_Coder_Next_poster_zh]] — 中文 poster（暗色）
- [[Qwen3_Coder_Next_poster]] — English poster（light）
