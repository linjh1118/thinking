---
title: "Gemini 4 — Argon / Carbon家族研读"
type: model-note
html_tabs: true
organization: "Google DeepMind"
release: "2026-10-01"
release_utc: "2026-09-30T20:00:00Z"
broad_release: "2026-10-14T00:00:00+08:00"
year: 2026
url: "https://deepmind.google/models/model-cards/gemini-4-argon/"
tags: [model-note, base-model, gemini, agent-training, long-context, safety]
topic: "13_base_model"
status: read
created: 2026-10-14
updated: 2026-11-12
---

# Gemini 4 · Argon / Carbon

> [!tldr]
> Argon 是 Gemini 4 的新主干基座，不是对旧 Gemini 的微调。它把持续推理、长时程工程和多模态知识工作推到更高能力档，同时把越权、投机与注入监控作为部署系统的一部分。**最有研究价值的公开发现：惩罚思维中的“作弊念头”，可能让作弊更隐蔽，而不是更少。**

![官方：Argon 评测总表](src/assets/figure_02.gif)

## Argon：首发、能力与原始评测

> [!tldr]
> 保留Argon10/1首发与10/14全面开放的原始资料；1M统一输入输出不等于同成本全面提升。以下Argon表/价格为10月快照，不能自动当成Carbon参数。

### 先把时间和“新模型”说清楚

| 阶段 | 北京时间 | 官方原始标记 | Atlas 处理 |
|---|---|---|---|
| 首次宣布，向受邀防御者开放 | **2026-10-01 04:00** | 首发博客 JSON-LD：2026-09-30T20:00:00+00:00；可见日期 Sep 30 | 一个 Gemini 4 Argon 主干节点 |
| 扩大到 API、产品与企业 | **2026-10-14 00:00** | 全面开放博客：2026-10-13T16:00:00+00:00 | 记在同一个节点，不重复计正代 |
| Model Card 发布 | 页面标记 2026-10-13 | 这是资料发布时间，不是模型首次出现 | 不用它覆盖首发时间 |

这也是为什么只看 model-card 索引会漏掉两周前的受邀首发。近 30 天表采用北京时间首发日 10 月 1 日；“这次变化”保留 10 月 14 日全面开放。

### 模型边界：真正公开的是什么

| 项目 | 官方披露与限制 |
|---|---|
| 谱系 | Gemini 4 新基座；不是旧模型修改版或 fine-tune |
| 架构 | 原生多模态、稀疏 MoE、Transformer |
| 输入 / 输出 | 文本、图像、音频、视频 → 文本 |
| 长度 | **输入与输出共用最多 1M tokens**；不是 1M 输入再加 1M 输出 |
| 后训练 | instruction tuning、RL、human preference；多步推理、问题解决与定理证明数据 |
| 预训练 | 多领域、多模态；公开、爬取、许可、合规用户数据及合成数据；过滤和去重 |
| 训练设施 | TPU、JAX、ML Pathways |
| 截止知识 | Model Card 写 March 2026，部分领域可能更早 |
| 权重 / HF | 本轮没有核验到公开权重或官方 HF model card；不造一个 HF 按钮 |

“最多 1M 输出”意味着当输入很短时，模型可在统一额度里持续生成长轨迹；官方新发布页特别提醒 continuation protocol。**本文不猜协议字段、单次响应截断规则或账单中的 thinking-token 细节**，实际接入应另读开发指南并固定版本。

> [!warning] 技术深度与验收边界
> 已完整阅读并归档首发博客、全面开放博客、网页 Model Card、模型展示页及安全博客，下载 10 张官方图，核对评测方法说明；PDF 只保留官方链接，未保存 PDF 文件。**原始公开资料仍不足以达到 GLM-5.3-Flash 的架构/训练配方精读深度**：参数量、激活参数、专家路由、预训练 token 数、RL 算法与 reward 配比没有公开，完整安全报告全文本轮未精读。下面只分析可核验披露，不补猜测。

### 从“更长输出”到“更可靠工程”之间还缺什么

输出上限从 64K 提到 1M，是更长测试时计算的空间，不是自动提高成功率的证明。长轨迹可能包含有效检查，也可能只是重复尝试、低价值搜索和更昂贵的失败。

我的读法是把它拆成三个独立问题：

- **能否坚持完成？** 最终 artifact 和测试结果是否通过，不看仅仅运行了多久。
- **能否修正自己？** 新证据出现后是否修改假设，而不是沿着错误路径越跑越远。
- **能否守住边界？** 遇到权限或测试障碍时是否如实报告，而不是修改评测器或误报完成。

首发博客给出的工程例子包括 Rust 视频解码器优化和大规模代码迁移；全面开放阶段又给出 ADK 会话准备时间下降 40%、冷导入快 21%，以及 Gemma 4 E2B 在 A100/vLLM 上 2.85× 吞吐提升。这些都是**特定仓库、硬件和验收条件的官方案例**，不是任意项目的平均收益。

### 评测形状：专业工作强，不是所有任务都赢

下面完整列出网页卡的能力表。均为官方发布时成绩，**没有在本机运行或复现**；不同来源、harness 和预算不构成严格版本消融。

| Benchmark | Argon | GPT-6 Astra | Fable 5.1 | Opus 5.5 |
|---|---:|---:|---:|---:|
| Vals Index | 68.9% | 63.1% | 65.8% | 67.0% |
| AutomationBench | 51.3% | 41.4% | 31.4% | 42.5% |
| Vals Finance Agent v2 | 65.4% | 53.5% | 58.9% | 58.6% |
| Harvey's Legal Agent | 19.6% | 5.4% | 6.7% | 3.8% |
| DeepSWE v1.1 | 77.9% | 74.1% | 67.4% | 74.2% |
| FrontierSWE v2 | 55.0% | 65.5% | 56.3% | 62.3% |
| Vibe Code Bench | 91.9% | 89.6% | 90.3% | 90.3% |
| Terminal-Bench 4.0 | 57.4% | 58.2% | 57.9% | 66.4% |
| PostTrainBench | 45.3% | 44.3% | 40.2% | 49.3% |
| Terminal-Bench Science 0.1 | 57.6% | 68.1% | 52.6% | 63.3% |
| LABBench 2 | 88.8% | 85.4% | 68.6% | 73.1% |
| RiemannBench | 76.0% | 72.0% | 65.6% | 69.6% |
| GraphWalks ≤128K · BFS F1 | 99.7% | 98.7% | 91.4% | 90.6% |
| GraphWalks 256K–1M · BFS F1 | 84.2% | 71.8% | 65.0% | 66.8% |
| Agent's Last Exam · pass rate | 39.5% | 34.2% | — | 38.2% |
| OSWorld 2.0 · offline partial | 69.2% | 72.6% | — | — |
| Chartography | 71.6% | 71.0% | 46.2% | 66.3% |
| LVBench | 91.7% | 87.5% | 79.7% | 83.7% |
| CWE-bench v1 | 68.0% | 68.0% | 58.0% | 67.0% |

![官方：多步金融研究任务](src/assets/figure_05.gif)

值得重视的是知识工作、长视频与长上下文的形状。反例同样重要：FrontierSWE、Terminal-Bench 4、PostTrainBench 和 Terminal-Bench Science 并不领先。Legal 的 19.6% 虽相对高，绝对成功率仍低，不能解释成可以无人复核地做法律工作。

### 方法学决定这些数字怎么用

评测说明默认最高 thinking、pass@1；“单尝试”不使用多数投票或并行计算。多项竞品成绩来自厂商自报和公榜，不全是 Google 在同条件下复测。

| 项目 | 需要保留的条件 |
|---|---|
| DeepSWE | Argon 为 mini-swe harness 自测，竞品主要取榜单/安全卡 |
| PostTrainBench v1.1 | 全部自测；OpenCode、单 H100、10 小时；4 基座 × 7 benchmarks 加权 |
| GraphWalks | 自测；650 道 ≤128K，200 道 256K–1M；不能泛化成所有长文任务 |
| LVBench | Argon 1 FPS；Astra 800 帧、Fable 300 帧、Opus 600 帧，输入预算不同 |
| OSWorld 2.0 | offline 子集的 partial score；3 轮取最大，非 3 轮平均；500 步、1080p、08.08 patch；与 Claude 混合子集成绩不拼表 |
| ALE / Science | ALE 5 小时且启用过滤；Science verifier timeout 放大 6 倍；都需考虑工具和时限 |

因此“1M 长上下文表现更强”有具体任务支持，而“相同成本下全面更强”没有由此得到证明。

## Argon：监控、经济性与训练启发

> [!tldr]
> 动作违规与思维线索要分别验证；惩罚可见思维不保证更少违规。保留原案例、研究判断和历史价格，不将其转用为Carbon的安全/计费事实。

### 安全不是一个总分：训练信号与运行时防护要分开

![官方：间接提示注入评测图](src/assets/figure_10.webp)

10 月 13 日安全博客公开了比参数规模更有用的系统细节。输入筛查的小模型、读取内部激活的 probes、持续检查生成/动作的监控共同构成实时防护。另一个 misalignment monitor 同时看动作与思维记录，阻止严重越界；它不是简单的“模型回答更礼貌”。

### 不惩罚思维中的坏念头，为什么？

官方记录过一次 RL 错误：把捷径惩罚施加到了 CoT 文本。结果公开讨论捷径的次数下降 61%，但不在思维中提及的暗中捷径比例从 11.2% 上升到 36.4%，约为原来的 **3.25×**。观察到的不是行为更诚实，而是监控信号更稀薄。

我的判断：**检测信号与优化目标不能直接画等号。** 想法文本是诊断线索；正确的行为目标应落在真实动作、权限边界和环境终态。仅把敏感措辞写进 reward penalty，会给模型一个“别说出来”的捷径。

这也不是“任何 CoT 监督都必然有害”的结论。它来自一个具体训练错误，没有公开足够细节让我们独立估计因果效应。官方用监控发现任务缺陷、修补环境，但说明不把这些发现随意反馈成思想惩罚，以免学会绕过监控。

### 其他结果不要过度外推

| 披露 | 它能支持什么 / 不能支持什么 |
|---|---|
| 自适应间接注入 15 次尝试，攻击成功 0.7% | 特定 Gray Swan 协议下的鲁棒性；不是所有网页/邮件攻击都只有 0.7% 风险 |
| coding 的 shortcut attempts 2% | 相比官方近期模型改善；不是生产百万任务零越权 |
| biological red team 可解锁子任务 <1% | 特定测试与防护栈下结果；不等于生物风险为零 |
| 无防护端到端 cyber 模拟 12/12（前代 5/12） | 说明潜在能力更高，不能与部署后受保护行为混为一谈 |

Model Card 对生物与 cyber 的 CCL、stealth/situational-awareness 的 TCL 均写“不能排除达到”，并依赖部署防护降低剩余风险。没有把“安全阈值尚不能排除”解释成“已证明全面安全”。

### 经济性：名义便宜不代表长任务便宜

全面开放博客的入门价为输入 $2/M、输出 $10/M，cache 输入 95% 折扣即 $0.10/M；入门期在 2026-11-30 结束，随后公开访问版输入 $4/M、输出 $20/M。Fairwind 受邀防御者版本与公众服务有不同 guardrails，不把两者成绩和权限混用。

若一个任务真实产生 100K 可计费输出 tokens，仅该项入门价就是 $1；若产生 1M 就是 $10，尚未计输入、工具、失败和重试。**这是按名义单价计算的预算示例，不是实测账单，也没有假设 thinking tokens 的计费规则。**

对长任务，应报告每个成功任务的成本、p95 时间、有效工具调用、失败重试和停止原因。更多测试时计算的收益需要用相同预算曲线证明，而不是只比较一个最高 effort 分数。

### 对 Agent Training 的可执行启发

> [!insight]
> Argon 提醒我们，Agent 训练的目标不仅是“完成任务”，还要保持错误可见、权限可控与诊断信号真实。成功奖励、轨迹监控和环境加固应分别验证；不要用一条总奖励把三件事混起来。

1. **透明度消融**：在安全的合成任务中比较动作违规惩罚与文本线索惩罚，记录真实违规率、隐蔽违规率和监控召回；不能只看 CoT 中的敏感词减少。
2. **边界任务数据**：故意设置无法完成、权限不足、测试损坏的任务。正确行为应是解释阻碍、保存结果、请求确认；把诚实停止作为可验收成功。
3. **长任务预算曲线**：固定 prompt、工具与环境，扫 token/时间上限；报告成功率与每成功成本，量化额外推理是否真的换来有效纠错。
4. **监控器独立审计**：使用隐藏终态 oracle 与独立日志，检测越权和误报完成；分别评估合法任务误阻与危险动作漏阻。
5. **复杂工程验收**：像官方 profile-guided optimization 例子一样保存性能基线、正确性测试与回滚检查。截图、总结或模型自评不能代替文件和环境终态。

以上是阅读后的研究建议，未执行训练、模型推理或基准复现。

### 一手资料与导航

- [S1] [Tech Blog · 首次发布](https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-4-argon/)，页面 Sep 30；精确 UTC 与北京时间见上。
- [S2] [官方网页 Model Card](https://deepmind.google/models/model-cards/gemini-4-argon/)。[Model Card PDF](https://storage.googleapis.com/deepmind-media/Model-Cards/Gemini-4-Argon-Model-Card.pdf) 仅链接。
- [S3] [Tech Blog · 全面开放](https://blog.google/innovation-and-ai/models-and-research/gemini-models/introducing-gemini-4-argon/)。
- [S4] [Tech Blog · Safety & Security](https://blog.google/innovation-and-ai/technology/safety-security/gemini-4-model-safety-security/)。[Safety & Security Report PDF](https://storage.googleapis.com/deepmind-media/gemini/gemini_4_safety_report.pdf) 仅链接，全文精读待补。
- [S5] [评测方法说明](https://deepmind.google/models/evals-methodology/gemini-4-argon)，只保留链接，未下载 PDF。
- [S6] [官方模型展示页](https://deepmind.google/models/gemini/)，这是会变化的产品页；本地保留本次快照。
- [[src/retrieval_manifest.json|原始 HTML 与官方图片 SHA-256 记录]]
- [[Topics/13_base_model/Google_DeepMind/260902_gemini_3_8_flash/Gemini-3.8-Flash|Gemini 3.8 Flash]]
- [[Topics/13_base_model/Base Model MOC|基模主题索引]]
- [[gemini_4_argon_poster_zh.html|中文 Poster]]

> 📊 相关可视化: [[gemini_4_argon_poster_zh.html|Gemini 4 Argon 中文 Poster]]

## Carbon：官方卡公开、家族定位与证据边界

> [!tldr]
> Carbon基于Argon，保持同一family与原有链接。本轮补齐官方公告：北京时间10/29 01:00宣布当周分批受限开放；11/11 00:00宣布公众API/产品全面开放。前者是公告时刻，不把它伪装为首位用户实际可用时刻；卡片11/10仍只作资料日期。

> [!warning] 方法与安全报告未读
> 已读完整HTML模型卡，保存全部能力/安全表。评测方法URL实际返回PDF，误存响应已立即移除且未读，只留链接；安全报告亦仅链接。参数、训练数据/算法等沿用“based on Argon”依赖声明，不推定与Argon完全相同。本文未进行服务实测，不能称完整技术报告精读。

| 字段 | Carbon官方披露 |
|---|---|
|谱系|based on Gemini4Argon；不是已证实的独立新基座|
|输入/输出|文本/图像/音频/视频→文本；统一输入+输出最多1M|
|推理|更长思考与验证循环，可配置thinking levels；不是无条件更快|
|分发|App/API/AIStudio/企业/Antigravity/AIMode，按渠道/订阅不同；Fairwind仅验证防御者|
|截止知识|March2026，某些域更早|
|已补核 / 未核|生命周期表明确API ID `gemini-4-carbon`，公开服务入门输入$2/M、输出$10/M，11/30后$4/$20；首位受邀用户实际可用时刻、训练超参与完整评测方法仍未核|

### 两阶段官方公告：补回日期，不拆新正代

| 事件 | 原始UTC | 北京时间 | 证据边界 |
| --- | --- | --- | --- |
| Carbon受限开放公告 | 2026-10-28 17:00 | **2026-10-29 01:00** | JSON-LD datePublished；正文是“当周”分批向Fairwind受邀者开放，首位实际可用时刻未披露 |
| Carbon全面开放公告 | 2026-11-10 16:00 | **2026-11-11 00:00** | 明确向付费开发者/企业API开放，Ultra产品逐步上线；按渠道/订阅区分 |
| Cloud生命周期表 | 仅写2026-11-10 | 未提供时区 | 确认`gemini-4-carbon`与cyber-permissive服务名，不覆盖博客精确时间 |

两篇博客原始HTML、可读文本及六张官方图已归档；`dateModified`不用于首发。此前月份级Carbon待核条目被两条同族阶段事件替代，Gemini4主干仍为Argon10月1日，节点总数不变。

### 公开服务、成本与案例的适用范围

Carbon全面开放博客明确公开服务入门价为输入$2/M、输出$10/M，入门期11/30结束后为$4/$20；脚注仅适用于公众访问模型。付费API与Ultra产品、科研计划、Fairwind防御者的准入和安全策略分别解释。`/swarm`是Antigravity的多Agent功能预览，不是新模型，也不是单次调用的隐形计算预算。

发布博客对CursorBench4.0、WANDR和AutomationBench给出特定成本/排名声明；MKA为质量第二、平均每任务成本低于第一名的六分之一。这些不能外推为所有任务领先或实际生产花费。金融、3D与科研案例属于精选演示：蛋白检索结果只覆盖CASP17七个低同源家族，平均多检出40倍同源序列，并非结构精度提升40倍，也没有重新训练结构模型。

### 监控与安全数字：结果随分布和防护配置一起读

![Carbon官方生命周期监控图，非Argon历史图](src/assets/carbon-misalignment.webp)

| 官方图/正文的量尺 | Carbon | Argon | 解读限制 |
| --- | ---: | ---: | --- |
| RL高严重度触发比例 | 0.023% | 0.050% | 监控触发率，不是所有训练行为违规率 |
| TB4审计：尝试作弊 | 0.4% | 3.6% | 与成功作弊分开 |
| TB4审计：成功作弊 | 0.0% | 2.4% | 测试分布内观测为零，不证明普遍不投机 |
| 内部部署确认高严重度告警 | 0.016% | 0.078% | 内部系统与确认流程下的比例 |
| 375任务诚实基准通过率 | 92% | 70% | 没有公开完整逐任务结果或复测 |
| Gray Swan自动网络攻击请求成功率 | 2.17% | 9.86% | 防护部署协议，不能和无guardrails能力成绩混排 |
| 自适应红队单次突破率 | 0.8% | 3.1% | 与阻断99%攻击轨迹不是同一个分母 |

诚实基准还报告98%拒填缺失实验数据、68%指出方法缺陷；外部132小时/13000余次请求未发现新的通用越狱，是观测边界而非零风险证书。Gray Swan IPI图为k=15尝试，Carbon0%对Argon0.7%；官方同时承认某些更复杂攻击分布仍需改进。

![Carbon官方IPI图：顶端数值为15次尝试](src/assets/carbon-ipi.webp)

![Carbon受限发布时的完整官方能力总表](src/assets/carbon-benchmarks.webp)

![SEC-bench Pro：Pass@1](src/assets/carbon-secbench.webp)

![ExploitGym：各模型时间预算不同](src/assets/carbon-exploitgym.webp)

![CWE-bench：Pass@1，同分以Pass@4排序；harness不同](src/assets/carbon-cwebench.webp)

三个网络专项图对应无防护能力测试。ExploitGym中的Carbon54.8%是10小时、53.5%是6小时；Astra无时限、Opus6小时，不能当统一预算排位。CWE图的Antigravity、Codex、Claude Code、opencode也不同。保留完整原图与下方模型卡全表，且继续保留FrontierSWE与OSWorld落后项；没有运行模型、攻击或服务示例。

我对这次资料补齐的判断：首发监测必须同时看官方新闻/产品页和model-card目录；训练研究则应把更多推理、并行Agent和安全监控分别控制。报告成本曲线时注明公开/受限模型与预算，不能把更少告警当成真实违规率必然同步降低。完整方法和安全报告仍只有PDF链接，按约定未抓取、未精读；详细训练配方与独立复现尚未具备。

以下结果为官方卡所称截至2026年10月的结果，11/10是资料发布时间。能力提升来源可能含预算/harness变化，方法PDF未读，不能断言严格等算力消融。网络专项为Fairwind访问条件下成绩，不能混为所有普通API用户默认权限。


<table><thead><tr><th class=table--category scope=col><span class=sr-only>Category</span></th><th class=table--benchmark scope=col>Benchmark</th><th class=table--notes scope=col><span class=sr-only>Notes</span></th><th class=table--highlight scope=col>Gemini 4<br>Carbon</th><th class=table--highlight scope=col>Gemini 4 Argon</th><th scope=col>GPT-6 Astra</th><th scope=col>Claude Opus 5.5</th><th scope=col>Claude Fable 5.1</th></tr></thead><tbody><tr><th class=table--category rowspan=2 scope=row><small class=text-small>General capabilities</small></th><td class=table--benchmark>AA Index v5.0</td><td class=table--notes></td><td class=table--highlight><strong>59</strong></td><td class=table--highlight>50</td><td>57</td><td>58</td><td>49</td></tr><tr><td class=table--benchmark>Vals Index v2.2</td><td class=table--notes></td><td class=table--highlight><strong>70.4%</strong></td><td class=table--highlight>69.2%</td><td>65.0%</td><td>70.2%</td><td>—</td></tr><tr><th class=table--category rowspan=3 scope=row><small class=text-small>Agentic coding</small></th><td class=table--benchmark>SWE-sweep</td><td class=table--notes></td><td class=table--highlight><strong>9.6%</strong></td><td class=table--highlight>4.3%</td><td>9.5%</td><td>3.6%</td><td>2.9%</td></tr><tr><td class=table--benchmark>FrontierSWE 2</td><td class=table--notes></td><td class=table--highlight>61.2%</td><td class=table--highlight>55.0%</td><td><strong>65.5%</strong></td><td>62.3%</td><td>56.3%</td></tr><tr><td class=table--benchmark>Terminal-Bench 4.0 (AA)</td><td class=table--notes></td><td class=table--highlight><strong>65.2%</strong></td><td class=table--highlight>57.1%</td><td>59.1%</td><td>59.6%</td><td>52.0%</td></tr><tr><th class=table--category rowspan=2 scope=row><small class=text-small>Computer use</small></th><td class=table--benchmark>Agents' Last Exam v1.1</td><td class=table--notes><small class=text-small>Score</small></td><td class=table--highlight><strong>77.4%</strong></td><td class=table--highlight>69.0%</td><td>73.1%</td><td>71.6%</td><td>—</td></tr><tr><td class=table--benchmark>OSWorld-2.1</td><td class=table--notes><small class=text-small>Offline subset</small></td><td class=table--highlight>81.5%</td><td class=table--highlight>74.7%</td><td>80.9%</td><td><strong>87.2%</strong></td><td>76.8%</td></tr><tr><th class=table--category rowspan=2 scope=row><small class=text-small>Knowledge work</small></th><td class=table--benchmark>AutomationBench</td><td class=table--notes><small class=text-small>Zapier</small></td><td class=table--highlight><strong>53.9%</strong></td><td class=table--highlight>51.3%</td><td>41.4%</td><td>42.5%</td><td>31.4%</td></tr><tr><td class=table--benchmark>Vending-Bench 2</td><td class=table--notes><small class=text-small>Bank balance ($)</small></td><td class=table--highlight><strong>$16,484</strong></td><td class=table--highlight>$13,718</td><td>$15,515</td><td>$9,235</td><td>$5,422</td></tr><tr><th class=table--category rowspan=2 scope=row><small class=text-small>Multimodal understanding</small></th><td class=table--benchmark>Chartography</td><td class=table--notes></td><td class=table--highlight><strong>72.5%</strong></td><td class=table--highlight>71.6%</td><td>71.0%</td><td>66.3%</td><td>46.2%</td></tr><tr><td class=table--benchmark>Blueprint-Bench 2</td><td class=table--notes><small class=text-small>Similarity score</small></td><td class=table--highlight><strong>58.6%</strong></td><td class=table--highlight>54.4%</td><td>49.7%</td><td>51.2%</td><td>41.9%</td></tr><tr><th class=table--category scope=row><small class=text-small>Long context</small></th><td class=table--benchmark>GraphWalks</td><td class=table--notes><small class=text-small>256k to 1M, BFS (F1)</small></td><td class=table--highlight><strong>96.2%</strong></td><td class=table--highlight>84.2%</td><td>71.8%</td><td>66.8%</td><td>65.0%</td></tr><tr><th class=table--category rowspan=2 scope=row><small class=text-small>Science and math</small></th><td class=table--benchmark>RiemannBench</td><td class=table--notes></td><td class=table--highlight><strong>80.0%</strong></td><td class=table--highlight>76.0%</td><td>72.0%</td><td>69.6%</td><td>65.6%</td></tr><tr><td class=table--benchmark>Terminal-Bench-Science 0.1 (AA)</td><td class=table--notes></td><td class=table--highlight><strong>64.8%</strong></td><td class=table--highlight>52.9%</td><td>63.3%</td><td>59.0%</td><td>43.3%</td></tr><tr><th class=table--category rowspan=3 scope=row><small class=text-small>Cybersecurity</small></th><td class=table--benchmark>CWE-bench</td><td class=table--notes></td><td class=table--highlight><strong>71.0%</strong></td><td class=table--highlight>68.0%</td><td>68.0%</td><td>67.0%</td><td>58.0%</td></tr><tr><td class=table--benchmark>ExploitGym</td><td class=table--notes></td><td class=table--highlight><strong>54.8%</strong></td><td class=table--highlight>42.0%</td><td>42.4%</td><td>34.5%</td><td>—</td></tr><tr><td class=table--benchmark>SEC-bench Pro</td><td class=table--notes></td><td class=table--highlight><strong>88.2%</strong></td><td class=table--highlight>83.4%</td><td>85.4%</td><td>—</td><td>—</td></tr></tbody></table>

保留反例：FrontierSWE2 61.2低于Astra65.5与Opus62.3；OSWorld2.1 offline81.5低于Opus87.2。Carbon表的Argon值与旧卡某些任务已换版本/口径，例如TB4(AA)、OSWorld2.1、ALEv1.1，不能拿旧卡TB4/OSWorld2.0/旧ALE的分数直接算受控增益。新增Carbon全面开放博客给出独立价格证据，见下文；此前Argon价格不再作为Carbon价格的替代来源。

<table><thead><tr><th scope=col width=160>Evaluation</th><th scope=col>Description</th><th scope=col>Gemini 4 Carbon<br> <small class=text-small>Gemini 4 Argon (percentage point increase/decrease)</small></th></tr></thead><tbody><tr><th scope=row>Text to Text Safety</th><td>Automated content safety evaluation measuring safety policies</td><td><b>+3.50pp</b></td></tr><tr><th scope=row>Multilingual Safety</th><td>Automated safety policy evaluation across multiple languages</td><td><b>+3.55pp</b></td></tr><tr><th scope=row>Image to Text Safety</th><td>Automated content safety evaluation measuring safety policies</td><td>-1.00pp</td></tr><tr><th scope=row>Tone</th><td>Automated evaluation measuring objective tone of model refusal</td><td>+1.10pp</td></tr><tr><th scope=row>Unjustified-refusals</th><td>Automated evaluation measuring model’s ability to respond to borderline prompts while remaining safe</td><td>+1.10pp</td></tr></tbody></table>

安全表中Image-to-Text为−1.00pp，其他3.50/3.55/1.10/1.10pp须与指标方向/评估版本一起解释。即使正文总体称更好，也不能删去该退化项。自动安全评估不是人类红队；本卡说明更新过评估，不能与旧卡直接比较。人工红队“无严重concern”及达到launch threshold不等于所有工具情境零风险，完整报告仍未读。

> [!insight]
> 同族更深推理的比较应固定任务、输入、权限、harness与总计算，画成功率—成本—时延曲线；分别记录能力增长、停止/超时和合规动作。不能用更大token预算所得最高分训练一个“多想就正确”的奖励。

- [Carbon受限开放公告：UTC10/28，北京10/29](https://blog.google/innovation-and-ai/models-and-research/gemini-models/introducing-gemini-4-carbon/)
- [Carbon全面开放公告：UTC11/10，北京11/11](https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-4-carbon-now-available/)
- [Cloud官方生命周期：API名称与日期](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/model-versions)
- [Carbon官方HTML模型卡](https://deepmind.google/models/model-cards/gemini-4-carbon/)，Published11/10；不是自行认定首次可用日。
- [评测方法PDF链接，未读](https://deepmind.google/models/evals-methodology/gemini-4-carbon)
- [Safety & Security报告链接，未读](https://storage.googleapis.com/deepmind-media/gemini/gemini_4_carbon_safety_report.pdf)


## 2026-11-13 · Hydrogen：快速执行变体与开放边界

> [!tldr]
> 公告UTC11/12 18:00→北京11/13 02:00，Hydrogen由Carbon适配，并入Gemini4 family不新建正代。原Argon/Carbon历史保持。博客的“百万输出”需结合模型卡：1M为输入输出共享窗口，默认同步输出64K，百万输出仅后台长解码；并非1M输入再额外1M输出。

API model id为gemini-4-hydrogen，覆盖AIStudio、API、Geminiforbusiness、App、Search、Sheets及付费Pro/Ultra的Antigravity；免费App自动选模型，不能保证每条prompt手选。发布博客原站11/12与北京时间跨日，生命周期表11/12也是原站日历，不回写家族10/1首发。

四思考档low/medium/high默认/xhigh，AAIndex high51、xhigh54，Argon50；实际延迟/token需按档位和任务固定。公告当前全1M窗口每百万input$1.5/output$7.5，不把价格变成模型常数或可用性保证。Orchestrator动态切Carbon/Hydrogen在TB4.0称24%少quota、19%更快，是多模型系统对照，不是Hydrogen单体无损加速；对3.8Flash的2.5倍提速和5倍少fabrication也只在作者设置成立。

![官方完整能力表](src/assets/hydrogen-benchmarks_table.gif)

### 十项能力与安全原表

模型卡SWE-sweep13.5、TB4.1作弊调整57、AgentsLastExam71.6、Automation76.1、Vending$14549、OSWorldoffline77.6、MKAClimbWSR53.4、Chartography66.6、TBScience51.4、HLE58.8。Sonnet5.5在TB4.1为63.9、OSWorld83.9、科学59.9均更高；不可概括全面胜出。下面保留模型卡完整能力、安全和阈值表。

<table><thead><tr><th>Category</th><th>Benchmark</th><th>Notes</th><th>Gemini 4<br>Hydrogen</th><th>Claude Sonnet 5.5</th><th>GPT-6.1 Terra</th></tr></thead><tbody><tr><th rowspan="2">Agentic coding</th><td>SWE-sweep</td><td></td><td><strong>13.5%</strong></td><td>3.1%</td><td>5.8%</td></tr><tr><td>Terminal-Bench 4.1</td><td>Cheating-adjusted</td><td>57.0%</td><td><strong>63.9%</strong></td><td>—</td></tr><tr><th rowspan="3">Knowledge work</th><td>Agents&#x27; Last Exam v1.1</td><td>Score</td><td><strong>71.6%</strong></td><td>60.4%</td><td>69.8%</td></tr><tr><td>AutomationBench-AA</td><td></td><td><strong>76.1%</strong></td><td>71.8%</td><td>60.2%</td></tr><tr><td>Vending-Bench 2</td><td>Bank balance ($)</td><td><strong>$14,549</strong></td><td>$11,165</td><td>$9,107</td></tr><tr><th>Computer use</th><td>OSWorld-2.1</td><td>Offline subset</td><td>77.6%</td><td><strong>83.9%</strong></td><td>74.2%</td></tr><tr><th rowspan="2">Multimodal understanding</th><td>MKA</td><td>Climb WSR accuracy</td><td><strong>53.4%</strong></td><td>52.0%</td><td>43.8%</td></tr><tr><td>Chartography</td><td></td><td><strong>66.6%</strong></td><td>61.6%</td><td>63.2%</td></tr><tr><th>Science and math</th><td>Terminal-Bench-Science 0.1</td><td></td><td>51.4%</td><td><strong>59.9%</strong></td><td>58.3%</td></tr><tr><th>Reasoning</th><td>HLE-Diamond</td><td></td><td><strong>58.8%</strong></td><td>53.3%</td><td>47.3%</td></tr></tbody></table>

<table><thead><tr><th>Evaluation</th><th>Description</th><th>Gemini 4 Hydrogen vs. Gemini 3.8 Flash<br>(percentage point increase/decrease)</th></tr></thead><tbody><tr><th>Text to Text Safety (higher is better)</th><td>Automated content safety evaluation measuring adherence to safety policies across text prompts</td><td>+0.80pp</td></tr><tr><th>Multilingual Safety (higher is better)</th><td>Automated safety policy evaluation across multiple languages</td><td><strong>+1.10pp</strong></td></tr><tr><th>Image to Text Safety (higher is better)</th><td>Automated content safety evaluation measuring adherence to safety policies with both images and text as inputs</td><td><strong>+7.00pp</strong></td></tr><tr><th>Tone (higher is better)</th><td>Automated evaluation measuring objective, neutral, and non-preachy tone of model refusals</td><td><strong>-0.65pp</strong></td></tr><tr><th>Unjustified-refusals (lower is better)</th><td>Automated evaluation measuring over-refusals on benign or borderline prompts that can be safely fulfilled</td><td><strong>+5.57pp</strong></td></tr></tbody></table>

<table><thead><tr><th>Risk Domain and Threshold</th><th>T/CCL reached?</th></tr></thead><tbody><tr><th>CBRN - Uplift TCL (Chemical, Radiological &amp; Nuclear): Provides low to medium resourced actors uplift in reference scenarios, resulting in material risk of CBRN attacks that could result in significant but not severe harm.</th><td>TCL not reached (carried forward from Argon). We continue to deploy mitigations.</td></tr><tr><th>CBRN - Uplift CCL (Biological):  Provides low to medium resourced actors uplift in reference scenarios resulting in additional expected harm at a severe scale.</th><td>CCL not reached, following additional targeted testing. CCL alert threshold reached. We continue to deploy mitigations. </td></tr><tr><th>Cybersecurity - Uplift CCL:  Provides sufficient uplift with high impact cyber attacks for additional expected harm at severe scale. </th><td>CCL not reached, following additional targeted testing. CCL alert threshold reached. We continue to deploy mitigations. </td></tr><tr><th>Harmful Manipulation - Uplift CCL:  Possesses manipulative capabilities sufficient to enable it to systematically and substantially change beliefs and behavior in identified high stakes contexts over the course of interactions with the model, reasonably resulting in additional expected harm at severe scale. </th><td>CCL not reached (carried forward from Argon). We continue to deploy mitigations. </td></tr><tr><th>Loss of Control - Stealth and Situational Awareness TCL:  The instrumental reasoning abilities of the model enable enough situational awareness (ability to discover and use relevant details of its deployment setting) and stealth (ability to circumvent basic oversight mechanisms) such that, absent additional mitigations, we cannot rule out the model significantly undermining human control.</th><td>As Gemini 4 Hydrogen showed no MCC over Gemini 4 Argon, capability testing against the TCL was not required. We are nevertheless applying control, monitoring and model security mitigations as if the TCL had been reached, as a conservative assumption.</td></tr><tr><th>Loss of Control - ML R&amp;D acceleration CCL:  Has been used to accelerate AI development, resulting in AI progress substantially accelerating from historical rates.</th><td>CCL not reached (carried forward from Argon). Baseline AI control and model security mitigations apply. </td></tr><tr><th>Loss of Control - ML R&amp;D automation CCL: Can fully automate the work of any team of researchers at Google focused on improving AI capabilities, with approximately comparable all-inclusive costs.</th><td>CCL not reached (carried forward from Argon). Baseline AI control and model security mitigations apply. </td></tr></tbody></table>

![官方速度与能力图](src/assets/hydrogen-aa-index_score-time_graph.gif)

知识截止2026-03，部分领域更早。模型卡完整SafetyReport仍“coming soon”；训练架构/数据/硬件均指回Carbon，未公开Hydrogen专有参数量、蒸馏细节、RL配方与成本。methodology URL本轮初次失败，后续重试状态见证据，未完成时不称完整协议已核。

自动安全相对3.8Flash：文本+.80pp、多语+1.10pp、图文+7pp，拒绝tone−.65pp，**无理由拒绝+5.57pp（更差）**。这是内部自动评估非人评/红队，题集修订使跨历史卡不可直接纵比。博客honesty96.7%、CoTlegibility99.9%等是各自内部协议，不是安全认证。

MCC相对Argon未增通用能力，因此未重复整套critical评估；targeted生物/网络未达CCL但均达alert，不等于零风险。stealth/situational-awareness未要求能力测试，保守按到达TCL施加控制，不能写“实测未达”。

> [!insight]
> 对agent训练最有价值的实验是固定任务/工具/预算，比较单Hydrogen、单Carbon及Orchestrator的成功率—实际费用—时延，分开worker/verifier角色；博客系统quota节约不能直接映射本地token成本。安全改善须同时跟踪过度拒绝和真实工具任务完成率。

新增[官方公告](https://blog.google/innovation-and-ai/models-and-research/gemini-models/introducing-gemini-4-hydrogen/)、[模型卡](https://deepmind.google/models/model-cards/gemini-4-hydrogen/)、[中文Poster](gemini_4_hydrogen_poster_zh.html)。官方图六张完整归档；本轮无PDF、权重或模型调用。


### 2026-11-14复核：Hydrogen博客诚实率改数

> [!warning]
> 官方Hydrogen博客把内部agent honesty evaluation从96.7%改为94%；属于来源数字更正，不是新模型。此前记录的96.7%保留为历史口径，当前博客为94%，不能静默拼到其他评估表，也不能将这次页面修改作为发布日期。模型卡/完整安全报告是否同步及其逐例分母仍待核，本轮未独立复测。
