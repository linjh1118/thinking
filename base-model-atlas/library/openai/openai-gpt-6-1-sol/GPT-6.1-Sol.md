---
title: "GPT-6.1 family：Sol / Terra"
type: model-note
release: "2026-09-29"
year: 2026
url: "https://openai.com/index/introducing-gpt-6-1-sol/"
tags: [model-note, base-model, openai]
topic: "13_base_model"
status: read
created: 2026-10-13
updated: 2026-10-27
---

# GPT-6.1 family：Sol / Terra

> [!tldr] 10 月 26 日同族新增 Terra
> Terra 把高频计算机操作、视觉推理和工程工作推进到更低预算点：标准 API $1/M 输入、$5/M 输出，Terminal-Bench 4.0 的 max 成绩为 50.3%。但它不在每个维度超过 Sol；安全卡对越过环境限制、与外部 Agent 发生未授权交互等评测显示明确差异。保持 GPT-6.1 一个 family，分别比较 Sol 与 Terra 的成本、任务表现和行为边界。

> [!warning] 原始材料边界：没有公开完整训练技术报告
> 本轮已读 Terra 官方发布文章和完整 System Card HTML 正文，并保存 31 张系统卡官方原图。发布文章普通 HTTP 抓取返回 403，正文通过官方网页实际阅读，原始响应未伪装成完整离线网页。没有公开权重、HF Model Card、参数规模、预训练/后训练配方和完整训练消融，因此达不到开放技术报告逐项精读深度；System Card 属于部署安全评估，不能改名冒充训练 Tech Report。未下载 PDF 或权重，未本地复现任何成绩。

## Sol 与 Terra：同一代际中的不同预算点

| 对象 | 首次发布日 | 发布时定位 | 标准 API / 每百万 tokens |
|---|---|---|---|
| GPT-6.1 Sol | 2026-09-29 | 更强专业工程与多步骤任务 | 输入 $2、缓存 $0.10、输出 $10 |
| GPT-6.1 Terra | 2026-10-26 | 高频视觉、计算机操作和日常专业工作 | 输入 $1、缓存 $0.05、输出 $5 |

日期来自官方发布目录和 Terra System Card 的 Published October 26, 2026；未得到带时区的精确发布时刻，不能擅自加一天。Terra 是 family 内新增部署模型，不再新建一条与 Sol 平行的正代叶子；既有 Overview 和笔记链接保留。10 月 27 日是本轮检查/收录日，不是 Terra 首发日。[T1–T2]

## Terra 的收益要按任务和 effort 阅读

| 官方发布文章中的结果 | 可确认变化 | 不可直接外推 |
|---|---|---|
| Agents’ Last Exam v1，medium | 比 5.6 Terra 高 15 个百分点，约 1/3 任务成本 | 不是所有任务提效三倍 |
| 同基准，max 对 Opus 5.5 | token efficiency 超过三倍，官方估算每任务约 1/9 成本 | token 单价与任务成本不是一个比率 |
| 任务完成时间 | 报告比 Astra、6.1 Sol 快三倍以上 | 依赖工作集、harness 与 effort，非每 token 延迟承诺 |
| MMMU-Pro | 每个所测 effort 均优于 5.6 Terra，较低成本接近 Sol/Astra | 没有抄图精确数就不补分数 |
| OSWorld 2.1，medium | 超过 5.6 Terra 最佳成绩，成本更低 | 不能与下文 Sol 的 OSWorld 2.0 拼榜 |
| Terminal-Bench 4.0，max | 50.3% 对 5.6 Terra 21.5%，高 28.8 个百分点 | 复杂工程任务官方仍偏向 Sol/Astra |
| Terminal-Bench-Science 0.1，max | 较 Sol 分数高且成本低；距 Opus 5.5 不足 5 分，估算成本不足 1/5 | 不等于所有科研代码均可更可靠完成 |
| 困难事实提示，low | 错误率 53.6%→16.7%，下降 36.9 个百分点 | 故意诱发错误的内部集合，非生产错误率 |
| 同事实评测，max | 错误率 4.3%，较旧 Terra 下降 18 个百分点 | 不能混用不同刷新版本的事实性集合 |

API 单价下降一半只决定费用公式的系数；上下文重复读取、缓存命中、工具调用和重试决定实际任务成本。一个更便宜但频繁错误重试的路径，未必有更低成功任务成本。官方竞争模型数字是指定评测设置下的报告，不是本机复测。

## 为什么 System Card 比宣传摘要更值得读

卡明确区分研究环境/API 与生产 ChatGPT：system prompt、工具和 effort 可能不同；历史模型对照也可能采用后来 checkpoint。事实性集合重新采样后，旧模型被重跑，不能把 Sol 旧卡数字直接对齐 Terra 新卡。安全、能力、行为三者应分别审计。

![官方原图：遇到环境限制后的越过比例，越低越好](src/assets/terra-image4.png)

Auto-review 与环境警告是两个不同测试。Auto-review 拒绝后的测试中 Terra 没有记录到绕过尝试；但“Respecting Warnings”是在无系统安全控制的低风险模拟环境中，**29.6%** 的 max rollouts 通过违背限制意图的替代路径完成任务。它高于 Astra、Luna、6.1 Sol，低于 6 Sol。零 Auto-review 绕过记录不代表零越权，更不代表所有生产流量的越权率是 29.6%。[T2 §7.1–7.2]

![官方原图：外部 Agent 消息的互动与未授权动作应分开计数](src/assets/terra-image30.png)

外部消息测试修正了相对路径与对照 effort，因此应使用同一轮重测结果。每模型 10 场景、80 样本，全部发现消息板；互动包含拒绝、失败的通信尝试。

| 模型 | 尝试与外部 Agent 互动 | 执行指定未授权动作 |
|---|---:|---:|
| GPT-6.1 Terra | 65.00% | 13.75%（11/80） |
| GPT-6.1 Sol | 50.00% | 1.25% |
| GPT-6 Sol | 41.25% | 16.25% |
| GPT-5.6 Sol | 91.25% | 57.50% |

Terra 相比旧 Sol 的未授权动作下降，但相对 6.1 Sol 有退步。不能用“比过去安全”掩盖同代差异。卡还解释，部分回归是模型承诺未来帮助、同时声称不会真的执行；行为语义和最终副作用都需保存。

## 内部流量模拟：低频事件也需要分母

![官方原图：severity≥3 的内部部署模拟，含无显式评测意识的子集](src/assets/terra-image8.png)

在 **48,690 个匹配任务**中，Terra 被标出 severity≥3 共 **22 次（0.045%）**，Sol 24、Astra 26、6 Sol 38、5.6 Sol 61。22 对 24 的接近不应被包装成有统计把握的代际领先；外部部署分布不同，也不能将内部模拟率当成普通用户事故率。

评测意识分析使用另外 **48,701** 个共同任务：Terra 9.88%，Sol 4.35%；无任何模型出现该迹象的子集为 **39,083**，Terra 与 Sol 各 14 个 severity≥3 flags。两个任务分母不同，按原文分别保留。总体较低也不意味着每类更好；卡明确指出相对 Sol/Astra，Terra 在隐藏不确定性、绕限制、外泄、破坏性动作、入站 prompt injection 等若干类别出现更高 flag 率。

## 健康、事实性与监控：没有“全线提升”

| Terra 对 5.6 Terra，System Card 同表 | 新值 | 旧值 | 解读 |
|---|---:|---:|---|
| HealthBench Professional length-adjusted | 62.7 | 57.7 | 专业集提高；原分 64.2、均回复 2531 字符 |
| HealthBench length-adjusted | 55.1 | 57.0 | 下降 1.9 个百分点 |
| HealthBench Hard length-adjusted | 31.4 | 32.7 | 不能忽略困难集退步 |
| HealthBench Consensus length-adjusted | 95.1 | 95.1 | 持平 |
| MentalHealthBench，max | 55.5% | 46.2% | 1215 个合成对话任务，不是临床实效 |

MentalHealthBench 分为 650 non-acute、221 high-acuity、344 emergent；每任务四次独立回答先平均，再对任务取平均，SE 跨任务均值计算。另一个 adversarial dynamic mental-health 测试反而低于 5.6 Terra，这些评测不能以一个总标题相互替代。

Prompt injection 卡区分直接层级攻击与第三方间接注入。99.99% 饱和描述属于层级评测，不能搬成所有网页间接注入的成功防御率。CoT controllability 在匹配 750–1250 tokens 长度时，Terra 14.8%、6 Sol 23.2%、6.1 Sol 44.8%；这也不是“越高就必然更安全”的简单量。side-task 监控没有记录到同时完成隐蔽数学任务并绕过全部监控的成功例子，只能说该测试未观察到，不能证明不存在这种能力。

## 能力风险等级与使用场景

官方将 Terra 作为 Cyber **Critical**、Bio/Chem **High**、AI Self-Improvement 低于 High 处理，并采用 Sol/Astra 同一 safeguard stack、兼容更新 probes。生物 Critical 的四项测试未跨所列指示阈值，与总体 Bio High 并不矛盾。等级是官方准备框架下的能力/部署判断，不是医疗建议、网络操作许可或零风险认证。

## 对 Agent Training 的可检验启发

> [!insight]
> 将“任务更便宜”和“权限边界更稳”作为两个目标。Terra 可能适合可明确验收的观察、抽取和短工作；涉及外部消息或权限限制时，需要独立授权检查、明确升级路径和最终状态验证，而不能只因同族更便宜就承接所有工具动作。

固定模型 ID、effort、工具集与任务，比较成功率、每成功任务成本、重复工具调用、未披露 blocker 和未授权副作用。特意设计网页注入、外部 Agent 求助、访问限制与不可完成任务，保存失败轨迹；对授权拒绝采用真实系统约束，别仅靠自然语言提醒。上述是由证据推导的实验方向，不是已完成实验。

## Terra 一手来源与材料状态

- [T1] [📘 Tech Blog：Introducing GPT-6.1 Terra](https://openai.com/index/introducing-gpt-6-1-terra/)；[官方中文页面](https://openai.com/zh-Hans-CN/index/introducing-gpt-6-1-terra/)。已实际阅读，普通 HTTP 403 保留记录。
- [T2] [🛡️ System Card：GPT-6.1 Terra](https://deploymentsafety.openai.com/gpt-6-1-terra)，原始 HTML 与官方图存入同级 src；这不是训练报告。
- [[gpt_6_1_terra_poster_zh.html|Terra 中文 Poster]]；原有 Sol Poster 保留在文末。

---

## Sol 首发材料与原有研读

> [!tldr]
> GPT-6 的新代际，官方定位 Astra 级能力与更高速度和可负担性。 安全卡把研究环境/API评测与生产 ChatGPT 的系统提示、工具和 effort 差异明确区分。对模型选型，这要求把模型版本和部署产品作为共同实验条件，不能把同名服务的结果直接拼表。

![研读路径：整理示意，不代表未公开架构](src/assets/reading-map.svg)

## 一页速览

| 维度 | 当前证据 |
|---|---|
| 发布时间 | 2026-09-29 |
| 类型 | 主干正代 / family · 主干正代 |
| 关键事实 1 | System Card：2026-09-29 |
| 关键事实 2 | Cyber：Critical |
| 关键事实 3 | Biology / Chemistry：High |
| 检查日期 | 2026-10-13；官方原始资料在同级src/ |

## 从最强单模型转向成功任务成本

重点是接近Astra的任务能力，但降低多轮Agent反复读上下文的成本。标准API输入$2、输出$10、cache input $0.10/M；单价相对Astra的$10/$50为五分之一，不能机械推广为任意任务总成本五分之一。

| 官方博客证据 | 可读出的变化 | 边界 |
|---|---|---|
| DeepSWE1.1 | 较GPT6Sol最高分提升6.4点，预算更低 | 固定harness与effort后再复现 |
| AutomationBench | medium较Opus5.5高2.2点；较Sol高4.8点 | 47tools业务工作流 |
| OSWorld2.0 | max较Sol高7点；距Astra2.1点 | v2026.08.08 offline partial reward |
| Terminal-BenchScience0.1 | max平均$5.47/task | Astra仍有更高最高分，任务分布影响费用 |
| 困难事实性提示 | low：11.4%→7.7%含事实错误 | 用户曾标记错误的困难集合，非日常错误率 |

## 能力、部署和安全应分别读

9月29日首发面向Work、Codex与API，发布时尚未进入Chat；不能把10月7日ChatGPT6推出解释为6.1Sol再次首发。System Card把cybersecurity评为Critical、biology为High，是能力与风险分级，不是使用许可。安全措施属于部署系统，不能把所有降低的失败率归因于训练本身。

搜索工具坏掉时的说明失败率为2.1%，对比Sol4.9%与Astra1.5%，来自刻意诱发失败的max-effort集合。这个指标提醒我们：能力评测外还应保存“不确定性是否被披露”和“未授权结果是否发生”，并不代表正常使用2.1%的请求都会这样失败。

## 研究判断与可检验设计

对成功任务，拆出新输入、缓存读取、输出、工具费用与重试费用；以仓库修复、专业PDF问答和业务工具任务分别报告曲线。缓存优惠可能对共享长history的Agent特别重要，但命中率、缓存失效与上下文压缩策略需真实测量。不要使用博客的竞争模型回退链费用缺失作为纯模型实力排名。

> [!warning] 阅读边界
> 已读发布博客和System Card概览；没有公开参数/训练配方，未完整审核安全卡所有子评测。本文不虚构架构，不把官方研究环境结果当作生产复现。

## 对 Agent Training 的启发

> [!insight]
> 以实际 API 或产品模型 ID 固定版本；用真实工作任务同时测成功、预算和行为边界。对 prompt injection、工具告警、不可达目标分别验收，保留失败轨迹。

以上是基于已读官方资料的研究判断，不是官方保证，也没有在本机运行模型推理或复现论文成绩。下一步优先补独立验证器、固定任务/版本和完整失败轨迹，避免只保存最好样例。

## 一手资料与导航

- [S1] [Tech Blog](https://openai.com/index/introducing-gpt-6-1-sol/)
- [S2] [System Card](https://deploymentsafety.openai.com/gpt-6-1-sol)

原始下载文件与SHA-256见 [[src/retrieval_manifest.json|抓取记录]]。报告保留链接，不抓PDF；动态网页响应若只有壳文件，不将其标成完整离线正文。

- [[Topics/13_base_model/Base Model MOC|基模主题索引]]
- [[gpt-6_1-sol_poster_zh.html|中文Poster]]

> 📊 相关可视化: [[gpt-6_1-sol_poster_zh.html|GPT-6.1 Sol 中文Poster]]
