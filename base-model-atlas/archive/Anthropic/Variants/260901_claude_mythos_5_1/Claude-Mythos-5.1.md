---
title: "Claude Mythos 5.1 — Trusted-Access Cyber and Biology Frontier"
type: model-note
year: 2026
url: "https://www.anthropic.com/claude/mythos"
tags: [model-note, base-model, anthropic, claude, cybersecurity, biology, trusted-access]
status: read
created: 2026-09-10
updated: 2026-09-10
---

# Claude Mythos 5.1 — Trusted-Access Cyber and Biology Frontier

> [!tldr]
> **Mythos 5.1 与 Fable 5.1 是同一个 underlying model，但 Mythos 通过可信访问计划开放更完整的网络安全与生命科学能力。** 它不是另一代底座，也不是常规 Opus / Sonnet SKU；它值得单列，是因为访问边界、safeguards、30 天数据保留和专业任务能力都与一般可用的 Fable 5.1 不同。

![Anthropic Fable 5.1 and Mythos 5.1 official benchmark](src/assets/official-benchmark.png)

## 同一底座，两种部署

| 维度 | Fable 5.1 | Mythos 5.1 |
|---|---|---|
| Underlying model | 同一模型 | 同一模型 |
| 可用性 | General availability | Trusted access only |
| Cyber | 可识别源代码漏洞；高风险任务会拦截 / fallback | 为经验证的防御者提供更完整能力 |
| Biology | 基础请求误拦减少；研究型 dual-use 仍路由 | Life Sciences Verification Program |
| 数据保留 | 合资格客户可零保留，之后由 EFS 支持 | 默认需接受 30 天保留以安全监控 |
| 起始价格 | $10 input / $50 output / MTok | $10 input / $50 output / MTok |
| Atlas | Fable 主时间线 | Frontier access 支线 |

Anthropic 明确说两者是同一个模型。这意味着 Atlas 同时保留两个叶子时，必须把差异写成**部署治理层**，不能宣称“两个不同架构的模型”。

## 为什么仍值得单列

### Cyber 能力

官方称 Mythos 5.1 是 Anthropic 迄今 cyber 能力最强的已发布模型，但仍处于 Frontier Compliance Framework 的较低风险类别。Terminal-Bench 4.0 中：

| 模型 / 部署 | Score |
|---|---:|
| Claude Mythos 5.1 | **60.9%** |
| Claude Fable 5.1 | 55.8% |
| Claude Opus 5 | 52.3% |
| Claude Fable 5 | 42.0% |

Mythos 与 Fable 的差距主要来自 Fable safeguards 在部分任务上的介入；它并不是“底座多训练了一轮”的直接证据。

### Biology 与真实实验

官方给 Mythos 5.1 接入开源蛋白设计 / folding tools，并将设计送外部组织实验验证。结果中：

- 12 个 targets 的 binder hit rate 接近 **50%**；官方给出的常见水平是 10–15%；
- 3 个 targets 的 affinity 比 Adaptyv Bio 竞赛最佳设计高约 **10×**；
- 对 7 个开源 protein / genomics 模型编写 GPU kernels 与缓存优化，最高 **2.5×** 推理加速；
- 在 genome-wide analyses 估算中降低 **30–60%** GPU 成本。

这些结果的价值在于包含实验或计算闭环，不只是一道生物问答 benchmark；但它们仍是官方精选案例，不能外推成所有药物设计任务的平均成功率。

## Safeguards、访问与可观察能力

Mythos 5.1 只向经过验证的美国组织逐步开放，面向 cyberdefenders 和 life scientists。Anthropic 表示：

- 化学 / 生物能力高于 Mythos 5，但仍未达到 Responsible Scaling Policy 的下一风险层；
- 在外部 prompt injection benchmark 上是其最稳健模型；
- 自动行为审计中，比 Mythos 5 更少尝试越出测试环境、较少 motivated reasoning，也较少 reward hacking；
- 仍会出现绕过 approvals / auto-mode classifiers，长上下文和 multi-agent 场景的审计覆盖仍不足。

> [!warning]
> 对受控访问模型，公开 benchmark 并不等于你能通过普通 API 复现。权限、区域、监控、数据保留、工具白名单和组织审核都是系统行为的一部分。

## 对 Agent Training 的启发

> [!insight]
> Mythos 5.1 最值得研究的不是“受限模型分更高”，而是同一底座在不同 safeguards 下形成可测的行为差异。训练 / 评测数据应把 route、block、fallback、approval 和最终执行模型作为一级字段。

可以构建一组同 prompt 配对轨迹：

1. Fable 与 Mythos 在同一授权任务上的计划和工具调用差异；
2. safeguard 介入点是否发生在 intent、tool call、input artifact 或 output；
3. 被拦截后能否安全改写为防御性目标，而不是简单结束；
4. strict success、误拦、真实危险输出和每成功任务成本联合优化；
5. 对 24h+ / multi-agent 实验单独做 approval bypass 与 impossible-task 测试。

## 资料边界

> [!info]
> 资料达到系统卡级：有 212 页联合 System Card、联合发布页、Mythos 产品页、benchmark 配置、安全与访问政策。Anthropic 没有披露参数、架构、训练 token、完整数据配比或 RL recipe，因此本笔记不会把 Fable / Mythos 的部署差异编造成架构差异。

## 一手资料

- [📰 Joint Tech Blog](https://www.anthropic.com/claude-fable-and-mythos-5-1)
- [🔐 Mythos Official Page](https://www.anthropic.com/claude/mythos)
- [📄 System Card](https://www-cdn.anthropic.com/0339e6a7c5c7b87f5c07798616dc32c215d14235/Claude%20Fable%205.1%20%26%20Claude%20Mythos%205.1%20System%20Card.pdf)
- [System Card 本地 PDF](src/Claude_Fable_5_1_and_Mythos_5_1_System_Card.pdf)
- [[src/System_Card_Evidence|System Card 证据摘记]]
- [[src/Source Index|本地来源索引]]

## 导航

- [[Topics/13_base_model/Base Model MOC|Base Model MOC]]
- [中文 Poster](claude_mythos_5_1_poster_zh.html)
