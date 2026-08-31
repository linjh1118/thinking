---
title: "DeepSeek-V4-Flash — 高效率 V4 同代模型"
type: model-note
year: 2026
url: "https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash"
tags: [model-note, base-model, deepseek, flash, long-context, agent]
status: read
created: 2026-09-01
updated: 2026-09-01
---

# DeepSeek-V4-Flash

> [!tldr]
> **V4-Flash 不是 V4-Pro 的量化副本，而是 V4 family 中独立训练、面向低激活与长上下文效率的 284B/13B MoE：原生 1M context，在同一套混合压缩注意力下把每 token 计算和 KV 占用继续压低。**

## 一页速览

| 维度 | DeepSeek-V4-Flash |
|---|---|
| 首次公开 | **2026-04-24**（Preview） |
| Family | DeepSeek-V4 |
| 参数 | 284B total / 13B activated |
| 预训练 | 约 32T tokens |
| Context | 原生 1M |
| 架构 | DeepSeekMoE + CSA/HCA hybrid attention + mHC |
| 精度与优化 | routed experts FP4；Muon；post-training QAT |
| 官方模型卡 | [Hugging Face](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash) |

## 为什么应当单独成为叶子

V4-Pro 与 V4-Flash 属于同一正代，但不是“同一个 checkpoint 换服务档位”。二者总参、激活参数、预训练规模和成本目标均不同。Flash 用更低的每 token 激活计算服务长上下文与 agent workload，因此需要一个独立 Overview；BF16、FP8 等纯精度镜像则不另拆叶子。

## 架构与效率

V4 family 将 Compressed Sparse Attention 与 Highly Compressed Attention 组合：历史 KV 先压缩，再由稀疏检索选择相关块，并保留近期未压缩窗口。Flash 进一步通过较小激活规模服务 1M context。官方报告给出的 1M 场景中，Flash 的单 token FLOPs 与累计 KV cache 分别约为 V3.2 的 **10%** 与 **7%**。

## 训练与 Agent 定位

- 预训练规模约 32T tokens，并保留 DeepSeekMoE 与 multi-token prediction 路线。
- post-training 先培养数学、代码、agent 与通用指令专家，再通过 on-policy distillation 合并。
- MoE experts 与 indexer QK path 使用 FP4 quantization-aware training，效率不是部署后的附加压缩，而是训练目标的一部分。

> [!insight]
> 对 agent training，更值得追踪的指标是“完成一次长任务的总激活计算 + KV 驻留 + test-time reasoning 成本”。V4-Flash 的价值正是在同一正代内提供了不同的成本—能力工作点。

## 证据边界

参数、训练规模与效率数字来自官方 model card / 技术报告；官方 benchmark 仍依赖其内部 harness，不能等价为第三方复现结果。

## 一手资料

- [DeepSeek-V4-Flash · Hugging Face](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash)
- [[src/huggingface_model_cards/DeepSeek-V4-Flash|本地原始 HF model card]]
- [[DeepSeek-V4|V4 family 总览]]
