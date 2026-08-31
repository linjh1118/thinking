---
title: "DeepSeek-V4-Flash-Base — 13B 激活的预训练基座"
type: model-note
organization: "DeepSeek-AI"
release: 2026-04-24
year: 2026
model_code: "DeepSeek-V4-Flash-Base"
url: "https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash-Base"
license: MIT
tags: [model-note, base-model, deepseek, v4, flash, pretrained, moe]
topic: "13_base_model"
status: source-limited
rating: 3
source_sufficiency: insufficient
created: 2026-09-01
updated: 2026-09-01
---

# DeepSeek-V4-Flash-Base

> [!tldr]
> **Flash-Base 是 V4-Flash 的预训练起点：284B 总参数、13B 激活、1M context、FP8 mixed 权重，不包含 Instruct checkpoint 的领域专家 SFT/GRPO、on-policy distillation 与 reasoning modes。** 它更适合继续预训练、领域适配和后训练研究，不适合作为开箱即用的 chat/agent 模型。

![DeepSeek-V4 官方规格图：包含 Flash-Base](src/assets/official_preview_release_01.png)

> [!failure] 资料充分度：不足｜未达到完整精读标准
> **本笔记明确没有达到 GLM-5.3-Flash 页面那种完整标准。原因是官方 HF 仓库没有 README/model card，`cardData` 与 `config` 元数据也为空；独立可用的一手材料只有仓库元数据，以及 V4 family model card / technical report 中的一行规格与共用 base benchmark。** 缺失独立配置、chat/encoding 说明、训练阶段说明、部署 recipe 和 checkpoint 专属图。下面只整理能被官方材料直接支持的部分。

## 目前能够确认的事实

| 维度 | 已确认信息 | 证据 |
|---|---|---|
| 参数 | 284B total / 13B activated | V4 family model card |
| Context | 1M tokens | V4 family model card |
| 权重精度 | FP8 Mixed | 官方下载表、HF tag `fp8` |
| 架构标签 | MoE / `deepseek_v4` | 官方表与 HF tags |
| HF 仓库创建 | 2026-04-22 | HF repository metadata |
| 家族发布 | 2026-04-24 | 官方 V4 Preview 发布 |
| License | MIT（家族发布） | family model card |
| 后训练 | 不包含 Instruct 完整后训练 | `Base` 身份与 family 下载表 |

## 它与 Flash Instruct 的区别

V4 family 披露的两阶段后训练——领域专家的 SFT + GRPO、再做 on-policy distillation——描述的是可交互的 Flash / Pro 模型。Base checkpoint 保留预训练能力，不能直接把 Instruct 的 reasoning modes、agent benchmark 或 prompt encoding 当成 Base 自带能力。

| 能力层 | Flash-Base | Flash |
|---|---|---|
| >32T family 预训练 | 是 | 是 |
| CSA + HCA / mHC / Muon 家族架构 | 是（family 证据） | 是 |
| 领域专家 SFT + GRPO | 未包含 / 无独立说明 | 官方明确包含 |
| on-policy distillation | 未包含 / 无独立说明 | 官方明确包含 |
| Non-think / High / Max | 不应默认支持 | 支持 |
| Chat / agent 开箱即用 | 否 | 是 |

## Base benchmark 能说明什么

| Benchmark | V3.2-Base | V4-Flash-Base | V4-Pro-Base |
|---|---:|---:|---:|
| MMLU | 87.8 | 88.7 | 90.1 |
| MMLU-Pro | 65.5 | 68.3 | 73.5 |
| C-Eval | 90.4 | 92.1 | 93.1 |
| SimpleQA-Verified | 28.3 | 30.1 | 55.2 |
| HumanEval | 62.8 | 69.5 | 76.8 |
| BigCodeBench | 63.9 | 56.8 | 59.2 |
| MATH | 60.5 | 57.4 | 64.5 |
| LongBench-V2 | 40.2 | 44.7 | 51.5 |

![DeepSeek-V4 官方 base 与综合 benchmark 图](src/assets/official_preview_release_02.png)

结果并不是每项单调提升：Flash-Base 的 HumanEval、MMLU-Pro、LongBench-V2 高于 V3.2-Base，但 BigCodeBench 与 MATH 更低。这说明 13B active 的效率路线不是在每个静态 base benchmark 上无损替代 37B active V3.2；其价值需要结合长上下文效率与后训练后的最终 Pareto 判断。

## 对研究的实际用途

> [!insight]
> Flash-Base 最适合做“低激活大容量模型如何获得 agent 能力”的起点：同一 family 同时给出 Base 与 Instruct，可以研究领域后训练到底补了什么，而不用把架构差异与后训练差异混在一起。

可做的对照包括：

1. Base → SFT → RL 各阶段的 agent 能力曲线。
2. 领域继续预训练后，13B active 是否保留足够知识容量。
3. Flash-Base 与 Pro-Base 在同样后训练 token 预算下的 scaling。
4. FP8 Base 与 FP4-expert Instruct 的部署/数值差异。

## 当前不能确认

- 独立仓库的精确层数、专家数、routing 与 tokenizer 配置。
- Base checkpoint 的训练截止日期、32T 中精确 token 数与数据配比。
- 是否提供官方最小推理代码、权重转换与推荐 serving 参数。
- Base 是否需要专用 prompt 格式；作为预训练模型，本就不应默认套 chat template。

## 一手资料

- [官方 HF 仓库（无 README/model card）](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash-Base)
- [[src/huggingface_repository_metadata/DeepSeek-V4-Flash-Base.json|本地 HF 仓库元数据]]
- [[src/huggingface_model_cards/DeepSeek-V4-Flash.md|V4 family 官方 model card]]
- [[src/paper/main.tex|V4 technical report 源码]]
- [[DeepSeek-V4-Flash|Flash Instruct 精读]]

## 补齐条件

- [ ] 官方补发 Base README / model card 后重写架构与使用部分。
- [ ] 取得独立 config 与 inference recipe 后补精确结构。
- [ ] 若发布训练细节，补数据、optimizer、阶段与消融。
