---
title: "Seed1.8 — 面向真实世界工作流的通用 Agent 模型"
type: model-note
year: 2025
url: "https://seed.bytedance.com/en/blog/official-release-of-seed1-8-a-generalized-agentic-model"
tags: [model-note, base-model, seed, multimodal, agentic, tool-use]
status: read
created: 2026-08-31
updated: 2026-09-01
---

# Seed1.8 — 面向真实世界工作流的通用 Agent 模型

> [!tldr]
> Seed1.8 把主线目标从“强多模态模型”改成 **Generalized Real-World Agency**：统一 Search、Code Execution 与 GUI interaction，并用 no/low/medium/high 四档 thinking mode 控制延迟和成本。它的价值在于同时评估基础能力、工具执行、视觉 observation 与真实专业工作流。

## 四个设计目标

1. **Strong base**：保留语言、代码、数学、知识和视觉能力；
2. **Unified agent interface**：搜索、代码、GUI 使用统一交互协议；
3. **Cost-aware inference**：四档 thinking mode 与视觉 token 优化；
4. **Practice-aligned evaluation**：公共 benchmark 加金融、法律、旅行等高价值任务。

## Agent 能力不是单一分数

官方发布资料覆盖 GAIA、BrowseComp、GUI 与真实专业任务。BrowseComp-en 报告 67.6；更重要的是，模型在低、中、无限步数设置下呈现明显的 interaction scaling：增加环境步数能提高成功率，但同时提高 token、搜索与工具成本。

![Seed1.8 Agent 综合评测](src/assets/agent-benchmark.png)

![Seed1.8 搜索 Agent 评测](src/assets/search-benchmark.png)

GUI 任务需要视觉 grounding、动作选择、执行反馈和错误恢复。Seed1.8 把这些能力放在同一正代主线，而不是把截图先交给独立 VLM 再转写。

![Seed1.8 GUI Agent 评测](src/assets/gui-benchmark.png)

## Thinking modes 与执行效率

四档 thinking mode 让同一模型在低延迟和深推理之间切换。它比“永远多想”更适合生产系统，但评测必须同时控制工具步数与 thinking tokens：否则模型可能通过更多搜索、更多代码执行换取分数，看不出真实效率。

> [!insight]
> Seed1.8 最适合作为 interaction scaling 研究对象：固定模型，逐步放宽 reasoning tokens、搜索次数、代码执行次数和 GUI steps，绘制成功率—总成本曲线，而不是只报告无限预算下的最高分。

## 资料充分度与证据边界

- 2025-12 发布博客提供产品与 benchmark；更完整的 Seed1.8 Model Card 于 2026-03 发布，因此本页将两者合并阅读，但不新增一个重复正代节点。
- 部分结果依赖 crop-box、浏览器/GUI harness 和内部专业任务；跨模型比较必须核对工具条件。
- 参数规模、训练 tokens 和完整 RL recipe 未充分公开。

## 一手资料

- [Seed1.8 官方发布博客](https://seed.bytedance.com/en/blog/official-release-of-seed1-8-a-generalized-agentic-model)
- [Seed1.8 Model Card](https://arxiv.org/abs/2603.20633)
- [[../2603_Seed1_8_Model_Card/Seed18-Model-Card-Towards-Generalized-Real-World-Agency|本地 Model Card 精读]]
- [[src/Official Source|本地来源索引]]
