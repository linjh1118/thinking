---
title: "Claude Opus 5.5"
type: model-note
release: "2026-09-22"
year: 2026
url: "https://www.anthropic.com/claude-opus-5-5"
tags: [model-note, base-model, anthropic]
topic: "13_base_model"
status: read
created: 2026-10-13
updated: 2026-10-13
---

# Claude Opus 5.5

> [!tldr]
> 复杂 Agent 工作的 5.5 旗舰；官方报告成本下降与更可靠的长期执行。 Opus 5.5 的价值集中在开放式任务中的持续判断、行为边界与每个完整任务的成本。官方展示的长迁移与性能优化案例需要结合任务定义阅读，单个成功案例不等于普遍工程保证。

![研读路径：整理示意，不代表未公开架构](src/assets/reading-map.svg)

## 一页速览

| 维度 | 当前证据 |
|---|---|
| 发布时间 | 2026-09-22 |
| 类型 | 主干正代 / family · 主干正代 |
| 关键事实 1 | Terminal-Bench 4.0：66.4% |
| 关键事实 2 | FrontierCode：54.4% |
| 关键事实 3 | 输入 $4 / 输出 $20 每百万 tokens |
| 检查日期 | 2026-10-13；官方原始资料在同级src/ |

## 变化在哪里

这一发布把前沿工作能力与执行效率放在一起：面向跨仓库迁移、审计与专业分析，既关注最终产物，也关注长任务中的越权动作、无效重复和误报完成。官方客户案例能说明任务形态，却不能作为稳定成功率或普遍速度保证。

## 发布时的评测口径

| 评测 | Opus5.5 | Opus5 | 解释 |
|---|---:|---:|---|
| Terminal-Bench4.0 | 66.4% | 52.3% | Opus5.5使用xhigh，标准误±2.6点 |
| FrontierCode1.1 Main | 54.4% | 48.0% | 代码合并质量，不是刷算法题 |
| CursorBench4.0 | 57.8% | 46.6% | 含模糊、多文件需求 |
| GDPval-AA2.1 | 1846 | 1708 | Elo，不是准确率 |
| AutomationBench | 40.0% | 26.9% | Zapier评测；安全拦截按失败 |
| HLE（工具） | 67.7% | 63.6% | 不与无工具结果混比 |
| OSWorld2.1 | 81.8% partial | 74.0% partial | 部分奖励口径 |

大多数评测用adaptive thinking/max；最高TB分数用xhigh。生产安全措施会让部分cyber任务回退Opus4.8、biology与模型研发回退Opus5；结果包含回退链，不能视为一个纯checkpoint的能力。WANDR使用离线web工具、代码执行与980K预算，亦不同于公开榜配置。

## 任务成本不能从 token 单价直接得出

发布价格为输入$4、输出$20、cache read $0.20、cache write $5，单位均为每百万token。官方所称典型工作成本降低40%，同时依赖降价与实际使用token减少；Fast Mode为$8/$40，不适合把普通模式报价用于全部任务。将早期客户单个迁移案例推广为“所有仓库都一天完成”是不成立的。

## 对 Agent 安全的阅读

长任务、不可完成任务和真实事故场景进入alignment测试，是比礼貌拒答更贴近自主工作的一步。应检验模型能否在搜索坏掉时主动说明、在权限边界前停下、在做不完时不伪报成功；不能把官方“最强alignment”解释为不存在prompt injection。

> [!warning] 公开证据限制
> 已读发布博客；参数、训练语料和奖励配方没有在博客公开，无法达到开源模型的架构精读深度。System Card需继续单独审核，本文不把未读安全报告内容写成结论。

## 对 Agent Training 的启发

> [!insight]
> 用真实仓库任务检验性能优化后行为是否保持一致；加入不可完成任务和工具权限边界，单列越权动作及误报完成，复核缓存读费用与实际 token 减少。

以上是基于已读官方资料的研究判断，不是官方保证，也没有在本机运行模型推理或复现论文成绩。下一步优先补独立验证器、固定任务/版本和完整失败轨迹，避免只保存最好样例。

## 一手资料与导航

- [S1] [Tech Blog](https://www.anthropic.com/claude-opus-5-5)

原始下载文件与SHA-256见 [[src/retrieval_manifest.json|抓取记录]]。报告保留链接，不抓PDF；动态网页响应若只有壳文件，不将其标成完整离线正文。

- [[Topics/13_base_model/Base Model MOC|基模主题索引]]
- [[claude-opus-5_5_poster_zh.html|中文Poster]]

> 📊 相关可视化: [[claude-opus-5_5_poster_zh.html|Claude Opus 5.5 中文Poster]]
