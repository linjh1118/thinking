---
title: "Muse Ember｜低成本Agent执行与测量边界"
type: model-note
release: "2026-11-09"
year: 2026
url: "https://research.meta.ai/blog/muse-ember"
tags: [model-note, base-model, ember, agent-training]
topic: "13_base_model"
status: reading
html_tabs: true
created: 2026-11-10
updated: 2026-11-10
---

# Muse Ember：为大量Agent子任务设计的低成本模型

> [!tldr]
> 2026年11月9日Meta发布Muse Ember，面向工具调用、代码子任务、路由、提取和长文档处理。它是使用Muse Wonder Full训练的专项效率模型，单列支线；1M上下文与低标价不能替代真实任务成本，长提示有更高费率，FrontierCode仍落后Haiku。

> [!warning] 当前是发布材料研读
> 已读官方发布页、完整表格、成本曲线与脚注，并归档原始HTML/文本和原生SVG。Evaluation Report入口返回PDF，按现行约定仅保留链接，未保存、未阅读。参数、架构与蒸馏/训练方法未披露到可复现程度，无法达到GLM-5.3-Flash / Kimi-K3完整报告精读标准；没有实际调用服务或独立复测。

## 产品定位、价格与来源

> [!tldr]
> 不是Muse Wonder的新代号，也不是一个尺寸SKU。官网将它定位独立效率模型，API名muse-ember-1.0；按专项支线展示，海外默认筛选保持不变。

[S1官方博客](https://research.meta.ai/blog/muse-ember)显示November9,2026并称today introducing，作为首发日；HF当前未见对应权重卡，不伪造HF按钮。服务入口为Meta Model API / Muse Code；Google Cloud和Oracle可用是博客声明，未逐账号验收。

| 字段 | <=200K提示 | >200K提示 |
| --- | --- | --- |
| 输入 / 百万tokens | $0.10 | $0.30 |
| 缓存输入 / 百万tokens | $0.004 | $0.012 |
| 输出 / 百万tokens | $0.50 | $1.50 |
| context / 最大输出 | 1M / 512K | 同一模型上限，不等于常规任务每次需要用满 |

模型原生理解文本、图片、音频、视频，支持Responses API。它被官方定位为大量重复的Agent执行工作；Wonder负责最难规划，Ember负责高频子任务是**建议工作流**，不是已公开的自动路由算法或固定部署图。

![官方原生SVG：成本与AA Intelligence Index，不改变几何和数据](src/assets/cost-frontier.svg)

图中Ember xhigh为33.9/$0.116，max为35.8/$0.136；Haiku medium24.6/$0.092、high29.6/$0.159、xhigh34.3/$0.248、max36.2/$0.411；Luna high21.4/$0.073、xhigh23.3/$0.104、max27.8/$0.152。博客概括“约三分之一成本匹配Haiku最好分”，但精确点35.8低于36.2；它是接近的成本曲线判断，不是逐分完全相等。页面图注仍称proposed pricing estimates，正文给出当日API价格；保留这项口径差异。

## 全部量化结果与协议

> [!tldr]
> 同effort不代表同harness。最大effort下Ember在多数所列Agent指标较强，但FrontierCode低于Haiku，GDP.pdf与Luna打平，AA Index也和Haiku同为四舍五入36。

| 指标 | Ember max | Haiku5.5 max | GPT6 Luna max | 解释 |
| --- | --- | --- | --- | --- |
| AutomationBench-AA | 37.8 | 13.9 | 20.2 | AA；strict pass@1 |
| Agents’ Last Exam | 61.6 | 57.0 | 57.1 | Meta内部，Linux子集 |
| Personal Superintelligence Index | 46.8 | 36.1 | 37.0 | 内部8评估复合指标 |
| Terminal-Bench4 | 40.9 | 39.2 | 16.4 | 各用最好公开harness；非统一harness |
| Coding Agent Index-AA | 46 | 37 | 31 | AA，不能与单项百分比混为一谈 |
| FrontierCode2-AA | 27.2 | 34.9 | 25.2 | **落后Haiku7.7个百分点** |
| GDP.pdf-AA | 22.8 | 20.8 | 22.8 | 与Luna同分 |
| OSWorld2.1 partial | 69.5 | 68.9 | 50.5 | 内部部分给分 |
| OSWorld2.1 binary | 33.8 | 27.8 | 17.0 | 不同打分口径，另列 |
| PerceptionBench w/tools | 80.6 | 78.6 | 62.8 | 内部、使用工具 |
| AA Intelligence Index | 36 | 36 | 28 | 图精确Ember35.8、Haiku36.2 |

AA结果为Intelligence Index v5、11月9日公布值，成本按标价估计；本次没有独立读取AA原站或重新计算。TB4分别是 mini-swe-agent（Ember）、Claude Code（Haiku）、Codex（Luna）；成绩同时反映harness差异，不能直接当纯模型能力消融。PSI包含ALE、AutomationBench、FocusBench、JobBench、OfficeQA Pro、GDP.pdf、GDP.xlsx、VBT，复合量尺不能解释成46.8%真实办公全流程成功率。

| 与Spark1.3的官方表 | Ember max | Muse Spark1.3 max |
| --- | --- | --- |
| AA Intelligence Index | 36 | 37 |
| 每AA任务成本 | $0.14 | $2.39 |
| 每百万输入/输出 | $0.10 / $0.50 | $1.25 / $4.25 |

2.39/0.14约17.1倍是按四舍五入表值的计算，不是任何任务17倍降本。图中的0.136与概括0.14不应当作矛盾，但$0.14也不是每一次真实业务请求固定价格。

## 训练线索、安全与Agent研究判断

> [!tldr]
> “使用Wonder Full训练”没有交代完整蒸馏方法。公开资料主要证明定位和测量口径，后续实验应该验证任务路由、失败恢复及每个正确产物成本。

官方只说明Ember是首个使用Muse Wonder Full训练的模型；未披露参数、dense/MoE、训练token、teacher/student loss、RL配方、数据混合与推理显存。不能自己补成某一种on-policy distillation，也不推测它是Spark的量化版。

合作方引述分别涉及合同条款、子Agent代码检查、跨仓库调查和低延迟coding quests。Cloudflare“tail最高快30%”与You.com p95 2.2秒、相对部分开放模型4–13倍、输出token少36–48%来自各自早期测试，缺任务全集、硬件、并发和预算，不混成官方统一benchmark或普遍SLA。

安全方面，Meta称按其Superintelligence Scaling Framework评估化学生物、网络与失控风险，所评类别低于高风险阈值；另测用户意图、敏感信息、网页/文档/工具提示注入与高影响操作前请求人类意见。没有报告细节就不能推出无提示注入风险，也不等于所有低成本模型都可自由执行外部写操作。

> [!insight]
> 训练与部署都应把“路由正确”列为独立任务：简单提取交给Ember，复杂规划保留强模型，失败后明确升级，并按最终正确产物而非每token价格比较成本。路由标签不能泄露测试答案；相同文件、工具协议和harness下记录被升级的比例、恢复成本和误写次数，才能确认小模型减少的账单没有被返工吃掉。

### 可执行的验证设计

| 变量 | 必须固定 | 验收 |
| --- | --- | --- |
| 大小模型路由 | 同任务集与总预算，先冻结路由规则 | 正确产物成本、升级率、失败修复时间 |
| 长提示价格阶梯 | 输入长度与缓存命中分别记录 | <=200K / >200K真实账单与时延 |
| 子任务执行 | 同工具schema、仓库revision与最大重试 | 测试通过、越权/误写、重复调用 |
| 多模态理解 | 原始图片/音视频，未预做答案提示 | 细节提取、跨证据一致性、来源定位 |

### 一手材料与关联

- [S1 Tech Blog](https://research.meta.ai/blog/muse-ember)：本地src保存完整HTML/可读文本/原始表格；SVG保留官方几何与样式，未重画数据。
- [S2 Evaluation Report（PDF，链接保留，未读）](https://research.meta.ai/static/muse-ember-evaluation-report)。
- 相关：[[Topics/13_base_model/Anthropic/261109_Claude_Fable_Mythos_5_2/Claude-Fable-Mythos-5.2]]（更强能力与成本曲线）；中文Poster：[[muse_ember_poster_zh.html]]。
