---
title: "GPT-6.1 Sol"
type: model-note
release: "2026-09-29"
year: 2026
url: "https://openai.com/index/introducing-gpt-6-1-sol/"
tags: [model-note, base-model, openai]
topic: "13_base_model"
status: read
created: 2026-10-13
updated: 2026-10-13
---

# GPT-6.1 Sol

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
