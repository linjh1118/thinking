---
title: "Qwen3.7 — 托管正代检查点（公开资料有限）"
type: model-note
year: 2026
url: "https://github.com/QwenLM/Qwen3.8"
tags: [model-note, base-model, qwen, hosted-model, evidence-limited]
status: read
created: 2026-08-31
updated: 2026-09-01
---

# Qwen3.7 — 托管正代检查点（公开资料有限）

> [!warning]
> **本页达不到 Qwen3.6 或 GLM-5.3-Flash 的技术笔记深度，原因是官方没有发布 Qwen3.7 的独立技术报告、开放权重模型卡或完整发布博客。** 目前能一手确认的是 Qwen3.7-Plus / Max 作为托管模型存在，并在 Qwen3.8 官方材料中被用作前代对照；参数规模、训练 tokens、数据配比和后训练流水线均不能可靠补写。

> [!tldr]
> Qwen3.7 更适合被理解为 3.5/3.6 到 3.8 之间的**产品化正代检查点**：延续 hybrid attention 家族，继续提升托管 Agent 与专业任务能力，但没有对应开放 checkpoint 让外部进行架构和训练复核。

## 可以确认的事实

| 事实 | 证据 | 可信度 |
|---|---|---|
| 存在 Qwen3.7-Plus 与 Qwen3.7-Max | 后续 Qwen3.8 官方模型卡/评测直接列名 | 高 |
| 属于 Qwen3.5–3.8 hybrid 架构连续谱 | Qwen3.8-Flash-Next 官方博客明确回溯 | 高 |
| 是托管产品模型 | 无公开权重或独立 HF model card | 高 |
| 具体参数、激活量、训练规模 | 官方未公开 | 不可写 |

![家族架构背景：此图来自 Qwen3-Next，并非 Qwen3.7 独立架构图](src/assets/family-architecture-context.png)

## 为什么仍保留为正代叶子

Atlas 的“正代”按官方产品族与时间线判断，不以是否开源为唯一条件。Qwen3.7 被官方后续材料作为明确命名的前代基线，而且 Plus/Max 承担了公开服务角色，因此应保留；但页面必须把“存在一个产品版本”与“技术细节可审计”分开。

## 对 Agent Training 的可用信息

Qwen3.8-Flash-Next 官方材料表明 3.5、3.6、3.7、3.8 都延续 Gated DeltaNet + Gated Attention hybrid。由此可以把 3.7 当作观察产品能力演进的节点，却不能将后代的 QSA、N-gram embedding、Muon 或具体 RL 方法倒灌到 3.7。

> [!insight]
> 对闭源 Agent 模型，最重要的不是写一篇“看似完整”的架构猜测，而是建立证据分级：可重复的 API 行为、官方 benchmark、后代回溯描述分别记录；未知参数保持未知。否则谱系页面会把产品营销误写成训练事实。

## 资料充分度：尚缺的一手材料

- 独立 Tech Blog / Tech Report；
- Hugging Face model card 或开放权重；
- 参数规模、context 默认值与训练数据；
- Agent RL 环境、reward、rollout 和消融。

## 一手资料

- [Qwen3.8 官方仓库（含 3.7 前代对照）](https://github.com/QwenLM/Qwen3.8)
- [Qwen3.8-Flash-Next 官方博客（回溯 3.5–3.8 架构）](https://qwen.ai/blog?id=qwen3.8-flash-next)
- [[src/Official Source|本地证据边界说明]]
