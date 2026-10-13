---
title: "GPT-6 Sol / Luna"
type: model-note
release: "2026-09-22"
year: 2026
url: "https://openai.com/index/introducing-gpt-6-sol-and-luna/"
tags: [model-note, base-model, openai]
topic: "13_base_model"
status: read
created: 2026-10-13
updated: 2026-10-13
---

# GPT-6 Sol / Luna

> [!tldr]
> Sol / Luna 于9月22日发布；10月7日 Chat 部署更新在同一 family 中记录，不重复计为正代。 这是官方明确区分的十月部署阶段，不应覆盖九月 checkpoint。Intelligent UI 是产品体验，模型自身判断仍要由固定工具、提示和评测协议支撑；安全评估低 effort 与能力评估最高 effort 不是同一条件。

![研读路径：整理示意，不代表未公开架构](src/assets/reading-map.svg)

## 一页速览

| 维度 | 当前证据 |
|---|---|
| 发布时间 | 2026-09-22 |
| 类型 | 主干正代 / family · 主干部署阶段 |
| 关键事实 1 | 部署：ChatGPT |
| 关键事实 2 | Cyber / Bio：High |
| 关键事实 3 | 9月 Work/Codex 版本保持区分 |
| 检查日期 | 2026-10-13；官方原始资料在同级src/ |

## 时间线：首次发布与后来部署分开记录

| 日期 | 事件 | Atlas口径 |
|---|---|---|
| 2026-09-22 | Sol / Luna进入API、Work、Codex | family首次发布日期 |
| 2026-09-29 | GPT6.1Sol发布 | 独立增量代际节点 |
| 2026-10-07 | GPT6Sol / Luna进入Chat，新增部署安全卡 | 本family内更新，不伪造第三个正代 |

两档使用与Astra相似的训练方法，把成本前沿扩展到更高频工作；这不等于公开了完整recipe。Sol负责更复杂的专业与多步骤工作，Luna更适合低费用、规模化和辅助任务。

## 价格与实际计算预算

| API / 每百万token | Sol | Luna |
|---|---:|---:|
| 输入 | $2 | $0.10 |
| 输出 | $10 | $0.50 |

较上一档促销价格下调并不能替代一次端到端成本评测。更高effort的小模型可能在某些任务接近低effort的大模型，但对不明确、长程任务仍应留升级路径。

10月7日的更新涉及Chat部署；不能默认当日Codex/Work的相同名字checkpoint同步改变。安全卡说明使用低effort检查安全、高effort检查能力边界；两种设置应并列记录，而非用其中一个作为所有设置的结论。新增交互UI也是产品变化，不另算基础模型。

> [!warning] 公开证据限制
> 保存首发博客、10月安全卡与Chat发布页。闭源参数、数据与奖励明细未公开，无法写成GLM式架构精读；不同部署版本需继续按实际接口revision核对。

## 对 Agent Training 的启发

> [!insight]
> 实验记录必须包括 September/October 标识、Chat/Work/Codex、工具集和 reasoning effort。对较低风险违规回归也保留明细，不能用总体平均覆盖局部退步。

以上是基于已读官方资料的研究判断，不是官方保证，也没有在本机运行模型推理或复现论文成绩。下一步优先补独立验证器、固定任务/版本和完整失败轨迹，避免只保存最好样例。

## 一手资料与导航

- [S1] [Tech Blog · 首发](https://openai.com/index/introducing-gpt-6-sol-and-luna/)
- [S2] [System Card](https://deploymentsafety.openai.com/gpt-6-october)
- [S3] [Tech Blog](https://openai.com/index/gpt-6-for-everyone/)

原始下载文件与SHA-256见 [[src/retrieval_manifest.json|抓取记录]]。报告保留链接，不抓PDF；动态网页响应若只有壳文件，不将其标成完整离线正文。

- [[Topics/13_base_model/Base Model MOC|基模主题索引]]
- [[gpt-6-sol-luna_poster_zh.html|中文Poster]]

> 📊 相关可视化: [[gpt-6-sol-luna_poster_zh.html|GPT-6 Sol / Luna 中文Poster]]
