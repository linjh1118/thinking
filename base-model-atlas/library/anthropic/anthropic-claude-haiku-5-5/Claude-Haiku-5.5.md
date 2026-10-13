---
title: "Claude Haiku 5.5"
type: model-note
release: "2026-10-07"
year: 2026
url: "https://www.anthropic.com/claude-haiku-5-5"
tags: [model-note, base-model, anthropic]
topic: "13_base_model"
status: read
created: 2026-10-13
updated: 2026-10-13
---

# Claude Haiku 5.5

> [!tldr]
> 高频低成本模型，首次在 Haiku 档提供可调 effort，适合辅助 Agent 与检索摘要。 便宜模型应承接可明确验收的短任务，而不是把大模型全部工作直接迁过去。可调 effort 使同一个小模型兼顾速度与推理预算，但任务从属关系和失败升级策略仍需要 harness 管理。

![研读路径：整理示意，不代表未公开架构](src/assets/reading-map.svg)

## 一页速览

| 维度 | 当前证据 |
|---|---|
| 发布时间 | 2026-10-07 |
| 类型 | 专项支线 / family · Haiku |
| 关键事实 1 | Terminal-Bench 4.0：39.2% |
| 关键事实 2 | HLE：45.9%（无工具） |
| 关键事实 3 | ≤100K 输入：$0.10/M；输出：$0.50/M |
| 检查日期 | 2026-10-13；官方原始资料在同级src/ |

## 小模型的使用边界

5.5首度在Haiku档提供可调effort，适合高频检索、文档抽取、上下文压缩和辅助任务。若最终任务需要开放式规划，可以先做明确子任务，再按验收结果升级至Sonnet/Opus，而不是把所有工作无条件迁入便宜模型。

| 官方指标 | Haiku5.5 | Haiku4.5 |
|---|---:|---:|
| GDPval-AA2.1 | 1620 | 735 |
| AA-Briefcase1.1 | 1578 | 614 |
| OSWorld2.1 offline subset | 72.4% | 15.7% |
| HLE无工具 | 45.9% | 10.2% |
| HLE工具 | 57.4% | 18.7% |
| Terminal-Bench4.0 | 39.2% | 0.0% |

OSWorld这里是offline subset，不能与另篇博客的partial值直接放同一列。Haiku仍不是复杂coding任务的最佳选择。

## 100K 阈值是重要部署条件

| 每百万token | ≤100K提示 | >100K提示 |
|---|---:|---:|
| 输入 | $0.10 | $0.50 |
| 输出 | $0.50 | $2.50 |
| cache read | $0.01 | $0.05 |
| cache write | $0.125 | $0.625 |

升级tokenizer会略微增加同任务token数，故“单价便宜90%”不能直接解释为任务必便宜90%。压缩任务应查关键数字、权限约束、未完成动作是否丢失；抽取任务应查来源定位和拒绝伪造。此类短任务才能形成稳定委派和重试边界。

> [!warning] 公开证据限制
> 发布博客未披露参数与训练recipe。本文已整理能力、费用和评测边界，但无法提供开源模型级别的架构精读；System Card另列官方入口，不声称已完成全文审核。

## 对 Agent Training 的启发

> [!insight]
> 把搜索抽取、数据库查询、上下文压缩分开测；压缩任务检验关键信息遗漏而非字数。100K 上下文价格分段必须进入预算，并测委派后总任务成本。

以上是基于已读官方资料的研究判断，不是官方保证，也没有在本机运行模型推理或复现论文成绩。下一步优先补独立验证器、固定任务/版本和完整失败轨迹，避免只保存最好样例。

## 一手资料与导航

- [S1] [Tech Blog](https://www.anthropic.com/claude-haiku-5-5)

原始下载文件与SHA-256见 [[src/retrieval_manifest.json|抓取记录]]。报告保留链接，不抓PDF；动态网页响应若只有壳文件，不将其标成完整离线正文。

- [[Topics/13_base_model/Base Model MOC|基模主题索引]]
- [[claude-haiku-5_5_poster_zh.html|中文Poster]]

> 📊 相关可视化: [[claude-haiku-5_5_poster_zh.html|Claude Haiku 5.5 中文Poster]]
