---
title: "LongCat-Flash-Thinking-2601 Technical Report"
type: paper
authors: ["Meituan LongCat Team"]
year: 2026
venue: arXiv
arxiv: "2601.16725"
doi:
url: "https://arxiv.org/abs/2601.16725"
tags: [paper, base-model, moe, agentic, meituan, longcat, rl, tool-use, agentic-search, test-time-scaling]
status: read
rating: 4
topic: "13_base_model/Meituan_LongCat"
related:
  - "[[2509_LongCat_Flash|LongCat-Flash]]"
  - "[[2509_LongCat_Flash_Thinking|LongCat-Flash-Thinking]]"
  - "[[2603_LongCat_Next|LongCat-Next]]"
created: 2026-07-01
---

> [!tldr]
> 美团 LongCat 系列的 **2026 年 1 月 thinking 升级版**——仍是 560B MoE / 平均激活 27B，但重心从 2509 版本的"基础 reasoning + tool-augmented 数学"明确转向 **agentic reasoning**：agentic search / agentic tool use / tool-integrated reasoning 三条线全面拉到开源 SOTA。真正的新东西不是模型本身，而是 **三件配套基础设施**：(1) **Environment Scaling**——把"工具图"做成自动化 pipeline，扩张到 20+ domain、1万+ 环境、3.2万并发；(2) **Robust RL**——把真实世界的 noise（instruction noise + tool noise）显式拆解并 curriculum-injected 进训练；(3) **Heavy Thinking Mode**——同时扩 depth × width 的 test-time scaling，AIME-25 heavy mode 直接打满 100。在 BrowseComp 73.1、BrowseComp-ZH 77.7、τ²-Bench 88.2、VitaBench 29.3 这些 agentic 指标上把开源拉开了一个身位，但 GPQA / HLE / SWE-bench 这些"传统硬骨头"仍输给 Gemini-3-Pro / GPT-5.2 一个段位。

## 1. 问题与动机：vs 2509 版本到底缺了什么

[[2509_LongCat_Flash_Thinking|LongCat-Flash-Thinking]]（2509.18883）解决的是"让 base model 学会 thinking"，主要战场是数学（AIME / HMMT）和 tool-augmented reasoning——靠 code execution 把数学难题解出来。但跑下来发现三个真实世界的 gap：

1. **agentic 任务没有现成环境**：传统 reasoning 是 environment-free 的（纯语言内部推演），但 agentic search / tool use 需要 model 主动决定 **何时、如何与环境交互**，并把环境反馈接回 reasoning loop。这种长 horizon、多轮、异构环境的 trajectory 在真实语料里基本不存在。
2. **训练出来的 agent 不鲁棒**：在干净 benchmark 上 88 分的模型，部署到真实用户场景（用户表达模糊、工具偶发失败、返回部分结果）就掉到 60 分以下。根因是训练环境太理想化。
3. **single-pass thinking 撞天花板**：当 intrinsic reasoning 接近极限，单条 CoT 再加长收益递减，必须在 test time 同时扩 depth（self-reflection）和 width（多路并行探索）。

2601 版本就是冲这三个 gap 去的。论文 Introduction 把 agentic reasoning 定义为「通过 **与外部环境的自适应交互** 来解决复杂问题」，并明确把它和"intrinsic reasoning 能力接近极限"挂钩——这是这一代的核心 framing。

## 2. 方法核心：四层 co-design

整篇报告的 backbone 是一个 **端到端 co-design**，从 pre-training 一路延伸到 post-training，强调 data construction / environment / algorithm / infrastructure 四件套必须一起设计。

| 层 | 2509 Thinking 做了什么 | 2601 新增 / 改了什么 |
|----|----------------------|---------------------|
| Pre-training | 继承 Flash-Chat 配方 | **完全继承** Flash-Chat 数据分布，只在中训阶段改 |
| Mid-training | 长 context + 基础 agentic 数据 | **三路 hybrid synthesis**（text-driven / environment-grounded / planning-oriented），32K→128K→256K 分级，500B + 40B tokens |
| Post-training RL | GSPO + curriculum + dynamic budget | 上面这些保留，**新增 multi-domain environment training + robust RL with noise** |
| Inference | 单条 thinking trace | **新增 Heavy Thinking Mode**（parallel reasoning + summary model）|
| Infrastructure | DORA（异步 rollout） | DORA **扩展到 32K 环境 / 400 台机器**，加 PD disaggregation + CPU KV swap |

## 3. Agentic Search & Tool Use 的具体机制

这是这篇报告的真正技术干货，分成四个互相耦合的子系统讲。

### 3.1 Environment Scaling Pipeline（最核心的创新）

目标：**自动**把一个高层 domain spec 变成可执行、可验证的环境集合。流程是：

1. **Domain → tool graph**：给定一个 domain（如 airline / retail / telecom），用 LLM 合成 60+ 个 tool，自动生成对应的 database schema 和 tool 实现，跑 unit test + 一个 debugging agent 验证，**成功率 >95%**。
2. **构造 tool dependency graph**：tool 之间有参数依赖，建成有向图。
3. **从 graph 里采 executable tool chain $s_1$**：BFS-style 扩张，每加一个 tool 必须它的依赖都已被实例化（防止"加 tool 引发级联未满足依赖"导致 database 失一致 → 错误负 reward）。
4. **决定是否再加第二个 seed chain $s_2$**：用概率 $p = f(c(\mathcal{E}_n), g(\mathcal{D}_n), |\mathcal{D}_n|)$，其中 $c$ 是当前复杂度，$g$ 是强 solver 找新 chain 的难度，$|\mathcal{D}_n|$ 是剩余 tool 数。**fallback**：环境 tool 数 < 20 时随机补一个 chain，保证每个环境至少 20 个 tool。

最终产出：**20+ domain、tens of thousands 个环境**，每个环境至少 20 tools。

> [!insight] 真正的工程突破在"verifiability-preserving expansion"
> "加新 tool 就行"听起来简单，但 uncontrolled 加 tool 会让 cross-tool database 失一致——一旦失一致，正确 trajectory 也会被判失败，inject 出来的负 reward 是 **biased** 的，比没有 reward 还糟。作者把这个失败模式诊断得很清楚：必须 BFS + 依赖检查 + 至少 20 tool 的 fallback。这是这套 pipeline 能 scale 到 32K 环境的关键。Kimi-K2 的工具图是静态构造，LongCat-2601 把它做成了 **自动化扩张 + 可验证** 的闭环。

### 3.2 Mid-training 三路 hybrid 数据合成

- **Text-driven synthesis**：从大规模文本里挖 multi-step workflow（教程、说明文档），转成 explicit tool schema + 多轮 user-agent 交互。再两种 augmentation：(a) **Tool Decomposition** 把部分 tool 参数藏进环境，逼模型去 extract；(b) **Reasoning Decomposition** 在每个 action step 生成多个候选并让模型选。
- **Environment-grounded synthesis**：直接在 Python 环境里跑，反向合成 user simulator 的 system prompt，最后用代码执行 + environment database 最终状态验证 trajectory 正确性。
- **Planning-Oriented Augmentation**：专门强化 planning——(a) 把 problem decomposition + 正确的初始 action 选择配对；(b) 在每个 decision step生成多个候选让模型挑。这是单独给 planning 这一能力做的。

效果用 pass@k 在 τ²-Bench 上验证（论文 Figure 2），"Enhanced" recipe 在大 k 下显著高于"Baseline"——说明探索能力被 mid-training 拉起来了，给后续 RL 一个好起点。

### 3.3 Cold Start：四类能力各自的 data 策略

| 能力 | 数据来源 | 关键 trick |
|------|---------|-----------|
| General Thinking | 大规模语料里筛 210K | **Sliding-window PPL + KCG**：取所有 512-token window 的 max avg PPL，避免全局平均稀释掉局部 hard token；KCG 保 coverage，PPL 强调模型当前 gap |
| Agentic Coding | 真实开发平台 trajectory | 全可执行 + 可验证；action-level 过滤掉错误/冗余/投机操作；长调试 trajectory 用 step 压缩保住 horizon 而不被 length 限制 |
| Agentic Search | 合成（真实 search log 太少） | **强制 verify all conditions**，防 shortcut（基于部分证据的侥幸猜测）；长探索 trajectory 压缩保留 |
| Agentic Tool-Use | 基于 Environment Scaling pipeline，覆盖 33 个 domain | turn-level loss masking：失败 tool call 和格式错误的 turn 排除出 loss，但保留在 context 里 |

### 3.4 RL Task Set 的两类难度建模（agentic search）

- **Graph-based QA Synthesis**（multi-hop reasoning 难度）：从 Wikipedia 低频实体出发建 relational graph，采 connected subgraph 生成 QA，**deliberately obfuscate** 数字 / 实体名 / 地理 / 时间标记。LLM-as-judge + agent-based 验证唯一答案。
- **Agent-based QA Synthesis**（ambiguity 难度）：Finite State Machine 编排 Entity Extraction Agent → Question Synthesis Agent → Verification Agent → Answer Generation Agent → Judgment Agent。遇到 multi-answer conflict 自动加 attribute 重合成 question 保证唯一性。同时产出基于 Answer Generation Agent accuracy 的 **自动难度分级**。

### 3.5 Heavy Thinking Mode（test-time scaling 的具体实现）

两阶段：
1. **Parallel Reasoning**：thinking model 并行生成 N 条 candidate trajectory（扩 width）。
2. **Heavy Thinking**：summary model 反思并 aggregate 这 N 条 trajectory 的中间推理和答案（扩 depth）。

关键工程细节：
- 配一个 **context memory module** 存 message history；summary model 每轮接收 parallel reasoning 阶段的 history。
- prompt template 把 N 条 trajectory 的 answer（只 answer）做 permutation 后喂给 summary model，输出格式严格对齐 parallel 阶段，方便直接拼回 message history。
- thinking model 和 summary model 可以共享参数。
- **额外一个 RL stage 专门训 summary 阶段**。

## 4. 实验结果（关键 benchmark，全部从 leaderboard.tex 抽取）

对比对象：DeepSeek-V3.2-Thinking / Kimi-K2-Thinking / Qwen3-235B-A22B-Thinking-2507 / GLM-4.7-Thinking（开源）vs Claude-Opus-4.5-Thinking / Gemini-3-Pro / GPT-5.2-Thinking-xhigh（闭源）。

### 4.1 Mathematical Reasoning w/ Tools（Avg@16 / Avg@4）

| Benchmark | DS-V3.2 | Kimi-K2 | Qwen3-2507 | GLM-4.7 | **LongCat-2601** | **LongCat-2601 (heavy)** |
|-----------|---:|---:|---:|---:|---:|---:|
| AIME-25 (Avg@16) | 93.5* | 99.1† | 92.6* | 95.3* | 99.6 (开源第一) | **100.0** (并列第一) |
| HMMT-25 (Avg@16) | 93.5* | 95.1† | 83.9* | 98.1* | 93.4 | 97.5 |
| IMO-AnswerBench (Avg@4) | 77.7* | 78.7* | 73.0* | 84.0* | 78.6 | **86.8** |
| AMO-Bench EN (Avg@16) | 51.9* | 56.0* | 47.8* | 62.4* | 61.6 | **66.0** (开源第一) |
| AMO-Bench CH (Avg@16) | 52.0* | 51.8* | 28.8* | 35.1* | 56.8 | **67.5** (开源第一) |

*`*` = 外部报告的 w/o tools 数字；`†` = 外部报告*

判断：heavy mode 把 LongCat-2601 推到 AIME 满分、IMO-AnswerBench 第一（含闭源），AMO-Bench 中英双版本都是开源第一，但和 Gemini-3-Pro（72.5 / 74.9）还有 ~7 分差距。

### 4.2 Agentic Search（核心卖点）

| Benchmark | DS-V3.2 | Kimi-K2 | GLM-4.7 | GPT-5.2 | **LongCat-2601** |
|-----------|---:|---:|---:|---:|---:|
| BrowseComp (Pass@1) | 51.4† / 67.6† | - / 60.2† | 52.0† / 67.5† | **65.8†** / - | **56.6 / 73.1** |
| BrowseComp-ZH (Pass@1) | 65.0† / - | - / 62.3† | 66.6† / - | - | **69.0 / 77.7** |
| RWSearch (Pass@1) | 74.0 | 63.0 | 69.0 | **82.0** | 79.5 (开源第一) |

> [!insight] LongCat-2601 的真正护城河
> BrowseComp 73.1 / BrowseComp-ZH 77.7 / RWSearch 79.5——这三个数字是 LongCat-2601 相对其他开源模型最显著的领先区域。BrowseComp 加 context management 后从 56.6 → 73.1（+16.5），证明 **context management 是 agentic search 的必备件**，不是可选优化。论文 Appendix A 给的曲线显示 80K token 是 summarization 触发阈值的最优点（20K→63.86%，80K→66.58%，100K→65.9%）。

### 4.3 Agentic Tool Use

| Benchmark | DS-V3.2 | Kimi-K2 | Qwen3-2507 | GLM-4.7 | Gemini-3-Pro | GPT-5.2 | **LongCat-2601** |
|-----------|---:|---:|---:|---:|---:|---:|---:|
| τ²-Retail | 81.8† | - | 71.9† | - | - | 82.0† | 88.6 |
| τ²-Airline | 63.8† | - | 58.6† | - | - | - | **76.5** |
| τ²-Telecom | 96.2† | - | 47.3 | - | - | 98.7† | **99.3** |
| τ²-Avg | 80.6 | 74.3† | 59.3 | 87.4† | **90.7†** | 80.6 | 88.2 |
| **τ²-Noise** | 64.1 | 63.1 | 44.3 | 66.0 | 57.3 | 65.0 | **67.1** |
| VitaBench | 24.0 | 12.8 | 14.5 | 18.3 | **31.5** | 24.3 | 29.3 |
| **VitaBench-Noise** | 14.0 | 9.2 | 6.5 | 10.8 | **20.8** | 19.0 | 20.5 |
| Random Complex Tasks | 32.5 | 29.7 | 28.3 | 25.3 | 32.5 | 17.2 | **35.8** |

判断：τ²-Avg 开源第二（仅次于 Gemini-3-Pro），τ²-Noise / Random Complex Tasks **开源第一**。Random Complex Tasks（35.8）甚至压过所有闭源——这是 paper 强调"泛化到 OOD agentic 场景"的最硬证据。VitaBench-Noise（20.5）虽然略输 Gemini-3-Pro（20.8），但和 GPT-5.2（19.0）、Claude-Opus-4.5（20.3）几乎打平——**Robust RL with noise 这条路线被噪声 benchmark 数字证实有效**。

### 4.4 General QA & Coding（相对短板）

| Benchmark | DS-V3.2 | GLM-4.7 | Gemini-3-Pro | GPT-5.2 | **LongCat-2601** |
|-----------|---:|---:|---:|---:|---:|
| HLE text-only | 24.1 | 26.9 | **40.3** | 34.5† | 25.2 |
| GPQA-Diamond (Avg@16) | 86.9 | 84.9 | 91.9 | **92.9** | 80.5 / 85.2 (heavy) |
| LCB (24.08-25.05) | 82.4 | 84.8 | **88.1** | - | 82.8 |
| OJBench | 41.8 | 44.6 | **61.2** | - | 42.2 |
| OIBench EN | 43.3 | 30.8 | **58.2** | - | 47.7 |
| SWE-bench Verified | 73.1 | 73.8 | 76.2 | 80.0 | 70.0 |

> [!insight] 短板很明确
> HLE 25.2 / GPQA 85.2 / SWE-bench 70.0——这三个是 LongCat-2601 输 Gemini-3-Pro / GPT-5.2 一个段位的地方。**作者把 inference cost 拉出来对比 GLM-4.7**：同样性能下 LongCat 只花 ~45K tokens/problem，GLM-4.7 花 57K——这是开源模型的传统辩护词：性能接近但 cost 更低。但 HLE 落后 15 分不是 cost 能解释的，更可能是预训练数据 / 知识覆盖的系统性差距。

### 4.5 Robust RL ablation（Table 2，noise 训练是否真的有用）

| Dataset | ColdStart | Training w/o Noise | Training w/ Noise |
|---------|---:|---:|---:|
| VitaBench (Avg@4) | 10.0 | 28.6 | **29.3** |
| VitaBench-Noise (Avg@4) | 6.3 | 13.3 | **20.5** (+7.2) |
| τ²-Bench (Avg@4) | 78.8 | 87.1 | **88.2** |
| τ²-Bench-Noise (Avg@4) | 58.8 | 62.2 | **67.1** (+4.9) |

关键发现：**加 noise 训练在干净 benchmark 上几乎不掉点（甚至略升），但在 noisy benchmark 上 +5~7 分**。说明 instruction noise + tool noise 的拆解是合理的，curriculum 渐进注入（避免 reward 不可靠）是关键。论文特别强调："injected imperfections 不应该 invalidate task solvability，只增加 difficulty 和 stochasticity"——这是防止噪声注入变成有毒 reward 的设计原则。

## 5. 与 2509 Thinking 的对比（这代到底进步在哪）

| 维度 | 2509 Flash-Thinking | 2601 Flash-Thinking-2601 |
|------|---------------------|--------------------------|
| 模型规模 | 560B / 27B | **不变** |
| 主战场 | 数学 reasoning + tool-augmented（code exec 解题）| **Agentic**：search / tool use / 真实环境交互 |
| RL 框架 | DORA（异步 rollout 基础版） | **DORA 扩展到 32K 环境 + 400 台机器 + PD disaggregation + CPU KV swap** |
| 环境数量 | 数百到数千量级 | **1万+ 环境，20+ domain，3.2万并发** |
| 数据合成 | 主要数学 + 代码 reasoning trace | **三路 hybrid synthesis**（text-driven / environment-grounded / planning-oriented）|
| Noise 处理 | 没专门处理 | **Robust RL**：instruction noise + tool noise 显式拆解，curriculum 注入 |
| Test-time scaling | 单条 thinking trace | **Heavy Thinking Mode**：parallel reasoning + summary model + 专门 RL |
| 长上下文 | 标准 attention | 标准 + **ZigZag Attention 附加版**（50% 层换 SSA，1.5× 推理加速，支持 1M tokens）|

一句话总结：2509 解决"会不会 think"，2601 解决"能不能 agent"。从 paper 的 framing（"intrinsic reasoning approaches its limits, interaction with external environments emerges as a key mechanism"）也能看出，团队认为下一代突破必须来自 **环境交互**，而不是把 thinking trace 再加长。

## 6. 局限与思考

- **Heavy Thinking Mode 的 N（并行数）和 RL 训练细节没给全**：summary 阶段用的是什么 reward？parallel reasoning 的 N 在不同 benchmark 上是否一致？heavy mode 在 AIME 满分但 GPQA 只 +4.7（80.5→85.2），说明 width 在不同任务上收益差很大，论文没分析原因。
- **General QA / Coding 的差距**：HLE 25.2 落后 Gemini-3-Pro 15 分，SWE-bench 70.0 落后 GPT-5.2 / Claude-Opus-4.5 约 10 分。这部分被 framing 成"retains competitiveness"，但其实是预训练 / 数据的根本短板，agentic 再强也补不回来。
- **Environment Scaling 的 domain 覆盖**：报告说 20+ domain，每个环境 ≥20 tools——但哪些 domain、tool 复杂度分布、和真实生产环境（如企业 IT 系统、复杂电商后台）的 gap 没量化。
- **Random Complex Tasks 是自建 benchmark**：35.8 这个开源第一的数字需要谨慎——这是作者自己设计的环境合成 pipeline 生成的，和他们的训练 distribution 有 leakage 风险。论文说"three independent runs"取平均，但没说训练时是否见过类似环境。
- **ZigZag Attention 是"One More Thing"**——只是 mid-training 阶段 50% 层换成 SSA，1.5× 加速，性能保持——但被放在论文末尾"as a side release"，说明它还不是主线，真正想吃下长上下文市场要等 [[2603_LongCat_Next|LongCat-Next]]（2603.27538）。

## 7. 对研究的启发

> [!insight] 这一代的方法论价值远大于模型本身
> 560B / 27B 的 model card 和 2509 没变，benchmark 提升的来源是 **环境工程 + RL recipe + 推理调度** 三件基础设施。这印证了一个判断：当 base model scale 到一定体量后，agent 能力的边际收益主要来自 **environment diversity × RL stability × inference parallelism**，而不是参数或数据量。这套 co-design 的工程方法（特别是 BFS 依赖检查的 verifiable environment expansion、PD disaggregation + CPU KV swap 在 60GB 显存上的实现）可以被其他团队直接复用。

> [!insight] Heavy Thinking 揭示了 thinking model 的"聚合"能力是独立可训的
> 把 parallel reasoning 和 summary 拆开，并专门为 summary 阶段做 RL——这个设计暗示 **"生成多个候选" 和 "在多个候选间反思选择" 是两个可分离的能力**。这跟 self-consistency 的简单 majority vote 不一样，summary model 是在 message 层做反思，可以做 refine 而不只是 vote。值得在 agentic 长任务（ BrowseComp 这种 ）上系统对比 heavy mode vs self-consistency。

## 8. 关键链接

- LongCat Chat: https://longcat.ai
- HuggingFace: https://huggingface.co/meituan-longcat/LongCat-Flash-Thinking-2601
- GitHub: https://github.com/meituan-longcat/LongCat-Flash-Thinking-2601
- AMO-Bench（本文发布）: https://github.com/meituan-longcat/AMO-Bench
- RWSearch（本文发布）: https://github.com/AGI-Eval-Official/RW-Search
- τ²-Bench revised: https://github.com/AGI-Eval-Official/tau2-bench-revised
- VitaBench（升级版）: https://github.com/meituan-longcat/vitabench
- ZigZag 附加版: https://huggingface.co/meituan-longcat/LongCat-Flash-Thinking-ZigZag

## 9. 系列定位

> [!insight] LongCat 系列的 agentic 转折点
> 这一篇是 LongCat 从 **base model 阶段**（Flash 架构基座）走向 **agentic-native model** 的转折点。2509 系列还在解决"模型有多大、多便宜、会不会 think"，2601 Thinking 已经把重心明确转到"能不能 agent"。后续 [[2603_LongCat_Next|LongCat-Next]]（2603.27538）的 DiNA（统一离散 token）会把多模态 agent 也并入这条主线。理解这一篇 = 理解 LongCat 团队 2026 年的技术押注方向。

相关笔记：
- 架构基座：[[2509_LongCat_Flash|LongCat-Flash]]（2509.01322）
- 上一代 thinking：[[2509_LongCat_Flash_Thinking|LongCat-Flash-Thinking]]（2509.18883）
- 下一代主线：[[2603_LongCat_Next|LongCat-Next]]（2603.27538）
