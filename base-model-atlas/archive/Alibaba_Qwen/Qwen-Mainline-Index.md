---
title: "Qwen 主线与支线模型索引"
type: moc
tags: [moc, base-model, qwen, model-family]
created: 2026-08-27
updated: 2026-08-27
---

# Qwen 主线与支线模型索引

> [!tldr]
> 厂商根目录只保留按代际演进的通用主线：Qwen3 → Qwen3.5 → Qwen3.6 → Qwen3.8。Coder、VL、Omni、Image、Embedding、ASR/TTS、Guard 等任务或模态支线统一进入 [[Topics/13_base_model/Alibaba_Qwen/Variants/Variants-Index|Variants]]。

## 正代主线

| 代际 | 目录 | 判断 |
|---|---|---|
| Qwen3 | [[Topics/13_base_model/Alibaba_Qwen/2505_Qwen3/Qwen3-Technical-Report]] | Qwen3 通用基座起点 |
| Qwen3.5 | [[Topics/13_base_model/Alibaba_Qwen/2602_Qwen3_5/src/Qwen3.5 - GitHub]] | 原生多模态主线开始成形 |
| Qwen3.6 | [[Topics/13_base_model/Alibaba_Qwen/2604_Qwen3_6/src/Qwen3.6 - GitHub]] | Qwen3.5 架构的后续主线迭代 |
| Qwen3.8 | [[Topics/13_base_model/Alibaba_Qwen/2608_Qwen3_8/Qwen3.8-Family]] | Max、Flash、2.4T-A95B、27B 共同组成当前主线家族 |

## 支线模型

支线目录：[[Topics/13_base_model/Alibaba_Qwen/Variants/Variants-Index|Variants]]

- Coding：Qwen3-Coder、Qwen3-Coder-Next
- Multimodal：Qwen3-VL、Qwen3-Omni、Qwen3.5-Omni、Qwen-VLA、VL-Seg
- Generation：Qwen-Image、Image 2、Image-VAE 2
- Representation：Qwen3-Embedding、VL Embedding / Reranker
- Speech / Safety：Qwen3-ASR、Qwen3-TTS、Qwen3Guard

> [!note]
> “是否多模态”不是唯一分类条件。Qwen3.8-27B 虽然是原生 VLM，但官方把它作为 Qwen3.8 正代家族成员，因此仍留在主线目录；只有独立命名、独立任务路线的 VL / Omni / Image 等进入 `Variants/`。
