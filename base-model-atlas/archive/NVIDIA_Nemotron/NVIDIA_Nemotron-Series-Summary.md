---
title: "NVIDIA · Nemotron — Series Summary"
type: model-note
tags: [model-note, base-model, series, nvidia-nemotron]
created: 2026-08-31
updated: 2026-08-31
---

# NVIDIA · Nemotron — Series Summary

> [!tldr]
> 开放模型 + 数据 + recipe + 推理栈共同服务 enterprise agents。

## 主干时间线

| 时间 | 模型 | 关键变化 | 一手来源 |
|---|---|---|---|
| 2024-10 | Llama 3.1 Nemotron | 在 Llama 基座上强化 reasoning 与 agent 能力。 | [Official release](https://build.nvidia.com/nvidia/llama-3_1-nemotron-70b-instruct) |
| 2025-01 | Llama Nemotron | Nano / Super / Ultra agentic family。 | [Official release](https://blogs.nvidia.com/blog/nemotron-model-families/) |
| 2025-12 | Nemotron 3 | 从派生 Llama 转向 NVIDIA 自有开放 family。 | [Official release](https://blogs.nvidia.com/blog/nemotron-open-source-ai/) |
| 2026-03 | Nemotron 3 Super | 120B/12B active hybrid MoE，面向 agent 吞吐。 | [Official release](https://blogs.nvidia.com/blog/nemotron-3-super-agentic-ai/) |
| 2026-04 | Nemotron 3 Nano Omni | 30B-A3B omni perception agent。 | [Official release](https://blogs.nvidia.com/blog/nemotron-3-nano-omni-multimodal-ai-agents/) |
| 2026-08 | Nemotron 3.5 Lightning | 30B MoE 服务长时程、多 agent 专项任务。 | [Official release](https://blogs.nvidia.com/blog/nemotron-lightning-switchyard-rtx-dgx/) |

## 编辑判断

- 这里只收主干正代与改变路线的关键节点，不把每个尺寸、API snapshot 或专项 SKU 拆成正代。
- 训练数据、参数和消融只在官方技术报告明确披露时记录；闭源发布不做架构猜测。
- 当前旗舰详见 [[2608_Nemotron_3_5_Lightning/Nemotron-3.5-Lightning|Nemotron 3.5 Lightning]]。
