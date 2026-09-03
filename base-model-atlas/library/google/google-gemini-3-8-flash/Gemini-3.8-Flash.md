---
title: "Gemini 3.8 Flash — Software Engineering and Agentic Knowledge Work"
type: model-note
year: 2026
url: "https://deepmind.google/models/model-cards/gemini-3-8-flash/"
tags: [model-note, base-model, google-deepmind, gemini, agentic-workflow]
status: read
created: 2026-09-03
updated: 2026-09-03
---

# Gemini 3.8 Flash — Software Engineering and Agentic Knowledge Work

> [!tldr]
> Gemini 3.8 Flash 是以 3.7 Flash 为底座的快速迭代：不换 1M 输入 / 64K 输出的服务边界，重点抬升软件工程、终端 agent、知识工作与研究流程。**我的判断：这是 Gemini 主时间线的新节点，而不是一个应被折叠的 Flash SKU。**

![Gemini 3.8 Flash 官方评测矩阵](src/assets/official-evals.jpg)

## 谱系位置

| 字段 | 结论 |
|---|---|
| 团队 | Google DeepMind · Gemini |
| 发布时间 | 2026-09-02 |
| 前代依赖 | Gemini 3.7 Flash |
| Atlas 归类 | 主干正代，当前 Gemini 最新叶子 |
| 主要证据 | Google DeepMind Model Card |

官方没有宣称一套全新架构，反而反复说明 3.8 Flash **based on Gemini 3.7 Flash**。因此，最合理的读法不是“新架构革命”，而是：保持 Flash 的产品边界，集中更新后训练、行为稳定性和真实 agent 工作负载。

## 模型与接口边界

| 维度 | 官方披露 |
|---|---|
| 输入 | 文本、图像、音频、视频 |
| 上下文 | 最高 1M tokens |
| 输出 | 文本 |
| 最大输出 | 64K tokens |
| 推理预算 | 支持可调 effort levels，在质量、成本与延迟之间取舍 |
| 分发渠道 | Gemini app、Enterprise Agent Platform、AI Studio、Gemini API、AI Mode、Antigravity |

这里最值得记住的是：**3.8 的价值不是窗口变大，而是在相同窗口和 Flash 经济性下，让 agent 轨迹更有用。**

## 评测：增益落在真实工作流

| 评测 | Gemini 3.8 Flash | Gemini 3.7 Flash | 变化 |
|---|---:|---:|---:|
| DeepSWE v1.1 · 长时程软件工程 | 73.7% | 65.3% | +8.4pp |
| Terminal-bench 2.1 · agentic terminal coding | 89.4% | 85.8% | +3.6pp |
| Terminal-bench 4.0 · 通用 agent 能力 | 19.1% | 11.2% | +7.9pp |
| OSWorld-2.0 · computer use partial score | 59.0% | 50.6% | +8.4pp |
| Vals Finance Agent v2 | 61.4% | 59.0% | +2.4pp |
| BioMysteryBench · human-difficult | 56.5% | 43.5% | +13.0pp |
| LABBench2 · 生物研究任务 | 86.2% | 82.1% | +4.1pp |
| HLE-Verified | 54.9% | 53.6% | +1.3pp |

官方图表显示了一个比“平均分更高”更重要的模式：增益集中在 **长时程 coding、终端操作、computer use、金融/法务/生物研究工作流**。这与 Model Card 对“software engineering and agentic knowledge workflows”的定位相互印证。

## 经济性怎么看

官方评测图给出的限时入门价为：

- Input: **$0.75 / 1M tokens**
- Output: **$3.75 / 1M tokens**
- 图中注明该入门价到 2026-12-31 结束；之后常规价为 $1.50 / $7.50。

价格不应单独与 benchmark 排名绑定。对 agent workload，真正该测的是 **cost per successful task**：包括推理 tokens、工具往返、失败重试和超时。

## 安全与局限

Model Card 没有回避退步：

- 相对 3.7 Flash，多语言安全自动评测 **+5.4pp（越低越好）**，官方明确称为小幅回归。
- Text-to-text safety 为 -0.4pp，image-to-text safety 为 0.0pp。
- Unjustified refusals 为 +1.1pp（越低越好），不应误读成改善。
- 人工红队未发现 egregious concerns，儿童安全达到发布阈值。
- Google 判断 3.8 Flash 相对 3.7 没有 Frontier Safety Framework 中有意义的新能力或重大增幅，因此仍不太可能触及 T/CCLs。

此外，官方提醒模型仍可能幻觉，高 effort 可能消耗更多 tokens，并偶发慢响应或超时。知识截止时间为 2026-03，但部分领域可能仍只到 2025-01。

## 对 Agent Training 的启发

> [!insight]
> 3.8 Flash 最有价值的信号是：在没有换一套显性架构或上下文规格的情况下，多个真实工作流评测同时上升。这更像是后训练、工具环境与轨迹质量的改进问题。

对自己的 agent training 工作，可以直接拆出三个实验方向：

1. 同一任务分别用不同 effort 运行，测量成功率—成本—延迟 Pareto frontier。
2. 把 Terminal / OSWorld 类任务的失败拆成计划、调用、观测、验证和恢复，避免只记最终分数。
3. 对多语言 agent 另建 safety regression set，不要用英文安全结论代替中文与其他语言。

## 资料边界

> [!warning]
> 这是一份 Model Card，不是完整 Tech Report。官方明确说明了依赖、接口、主要评测和安全结果，但没有公开参数规模、训练数据配比、详细 post-training recipe 与消融实验。本笔记不对这些空白作推测。

## 一手资料

- [Google DeepMind Model Card](https://deepmind.google/models/model-cards/gemini-3-8-flash/)
- [Official PDF](https://storage.googleapis.com/deepmind-media/Model-Cards/Gemini-3-8-Flash-Model-Card.pdf)
- [[src/Official Model Card|Model Card 原页快照]]
- [[src/Gemini 3.8 Flash Model Card|Model Card 本地阅读版]]

## 导航

- [[Topics/13_base_model/Base Model MOC|Base Model MOC]]
- [[gemini_3_8_flash_poster_zh|中文 Poster]]
