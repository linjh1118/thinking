---
title: "Claude Sonnet 5.5"
type: model-note
release: "2026-09-28"
year: 2026
url: "https://www.anthropic.com/claude-sonnet-5-5"
tags: [model-note, base-model, anthropic]
topic: "13_base_model"
status: read
created: 2026-10-13
updated: 2026-10-13
---

# Claude Sonnet 5.5

> [!tldr]
> 面向日常工程与专业产物的 5.5 模型，官方称生成速度提升 30%+。 Sonnet 的任务定位是边界清晰、适合快速迭代的工作。单项 terminal 分数高于 Opus 不代表复杂开放式判断更强；同一工作流应比较 effort、任务总成本和验收结果。

![研读路径：整理示意，不代表未公开架构](src/assets/reading-map.svg)

## 一页速览

| 维度 | 当前证据 |
|---|---|
| 发布时间 | 2026-09-28 |
| 类型 | 主干正代 / family · 主干正代 |
| 关键事实 1 | Terminal-Bench 4.0：70.6% |
| 关键事实 2 | GDPval-AA：1844（发布时） |
| 关键事实 3 | 输入 $2 / 输出 $10 每百万 tokens |
| 检查日期 | 2026-10-13；官方原始资料在同级src/ |

## Sonnet 的定位不是所有任务都替换 Opus

更适合需求边界清晰、需要快速迭代的代码和专业产物。TB4.0的最高分不代表开放式复杂判断全面超过Opus；比较应固定effort和harness，并把代码通过验收、知识工作事实正确与任务费用作为不同维度。

| 发布博客指标 | Sonnet5.5 |
|---|---:|
| Terminal-Bench4.0 | 70.6% |
| FrontierCode1.1 Main | max 46.2%；xhigh 52.1% |
| GDPval-AA2.1 | 1844 Elo |
| HLE（工具） | 64.5% |
| OSWorld2.1 | 80.1% partial |

## 速度与预算

官方报告生成速度提升超过30%，典型任务需要更少token。价格输入$2、输出$10/M；发布时cache read $0.20/M，10月7日改为$0.10/M。后一变化是费用更新，不新建一个模型节点。价格更低不等于所有任务费用等比例下降，重试、工具用量、长上下文与最终返工仍会影响成本。

## 怎样把发布结果变成可复现实验

同一个任务分别运行低、中、高effort，保存全部工具轨迹，记录隐藏测试、修改范围、完成时间和成功任务成本。前端/Office产物须检查真实交互和事实，不仅看截图。报告Elo时保留评测版本与发布日期，不能把不同时间的榜单分数拼成一张不注明时间的统一排名。

> [!warning] 公开证据限制
> 当前依据发布博客；参数、训练数据比例、RL配方未公开，因此本文不能达到GLM开源模型那样的训练与架构精读深度。安全报告仍需独立阅读，不将宣传措辞当作安全证明。

## 对 Agent Training 的启发

> [!insight]
> 分别用低、中、高 effort 做成本曲线。专业文档和前端任务须验收事实、版式和可执行性，而非仅凭截图审美；缓存读价格在 Haiku 发布时再次变化，保留日期。

以上是基于已读官方资料的研究判断，不是官方保证，也没有在本机运行模型推理或复现论文成绩。下一步优先补独立验证器、固定任务/版本和完整失败轨迹，避免只保存最好样例。

## 一手资料与导航

- [S1] [Tech Blog](https://www.anthropic.com/claude-sonnet-5-5)

原始下载文件与SHA-256见 [[src/retrieval_manifest.json|抓取记录]]。报告保留链接，不抓PDF；动态网页响应若只有壳文件，不将其标成完整离线正文。

- [[Topics/13_base_model/Base Model MOC|基模主题索引]]
- [[claude-sonnet-5_5_poster_zh.html|中文Poster]]

> 📊 相关可视化: [[claude-sonnet-5_5_poster_zh.html|Claude Sonnet 5.5 中文Poster]]
