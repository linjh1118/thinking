---
title: "DeepSeek-V4-Flash — 13B 激活的百万上下文主力"
type: model-note
organization: "DeepSeek-AI"
release: 2026-04-24
year: 2026
model_code: "DeepSeek-V4-Flash"
arxiv: "2606.19348"
url: "https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash"
license: MIT
tags: [model-note, base-model, deepseek, v4, moe, long-context, agentic, hybrid-attention]
topic: "13_base_model"
status: read
rating: 5
source_sufficiency: sufficient
created: 2026-09-01
updated: 2026-09-01
---

# DeepSeek-V4-Flash

> [!tldr]
> **V4-Flash 的关键不是“小”，而是用 284B 总容量、13B 单 token 激活量和 CSA + HCA 混合注意力，把 1M context、推理能力与部署成本压到同一个设计里。** 它在知识上明显弱于 Pro，却能用更大的 reasoning budget 接近 Pro 的数学、代码与部分 agent 表现；这使它更像面向大规模 rollout 的研究主力，而不是 Pro 的廉价量化版。

![DeepSeek-V4 官方规格图](src/assets/official_preview_release_01.png)

> [!success] 资料充分度：完整
> 本笔记基于官方 HF model card、DeepSeek-V4 technical report LaTeX 源码、官方发布页与本地化图片整理，达到完整精读标准。仍未公开的训练配方会在文中单独列出，不以推测补齐。

## 先看它在家族中的位置

| 维度 | DeepSeek-V4-Flash |
|---|---|
| 发布 | 2026-04-24，Preview checkpoint |
| 参数 | 284B total / 13B activated，MoE |
| Context | 1M tokens；Think Max 建议至少 384K |
| 权重精度 | MoE experts FP4，其余多数参数 FP8 |
| 注意力 | CSA（Compressed Sparse Attention）+ HCA（Heavily Compressed Attention） |
| 训练 | >32T tokens；SFT + GRPO 培养领域专家，再做 on-policy distillation |
| 推理模式 | Non-think / Think High / Think Max |
| 适合 | 成本敏感的长上下文、coding、工具调用与批量 agent rollout |
| 后继 | [[DeepSeek-V4-Flash-0731]]，正式替代 Preview |

## 我的核心判断

### Flash 的优势来自“每 token 激活计算”，不是总参数小

13B activated 只有 V3.2-Base 37B 的约三分之一，也远低于 V4-Pro 的 49B；但 284B 总参数仍给了它足够大的专家容量。因而它的 Pareto 逻辑是：知识广度不可能完全追上 1.6T Pro，但在可通过 test-time compute 改善的任务上，增加思考预算能换回大量能力。

官方对照很能说明问题：Flash 从 Non-Think 切到 Max，LiveCodeBench 从 55.2 升到 91.6，GPQA Diamond 从 71.2 升到 88.1；但 SimpleQA-Verified 仍只有 34.1，远低于 Pro-Max 的 57.9。**推理预算能补 reasoning，补不了未存进参数的知识。**

### 1M context 的真正贡献是系统成本，而不是只把窗口数字写大

V4 的 CSA 负责从长历史中选择相关 token，HCA 则压缩需要长期保存的注意力状态。官方报告称，在 1M context 下，V4-Pro 单 token 推理 FLOPs 仅为 V3.2 的 27%，KV cache 为 10%。这个数字针对 Pro，但解释了整个 V4 家族为什么能把百万上下文用于实际 agent，而非只做一次性 needle test。

![DeepSeek-V4 官方长上下文效率图](src/assets/official_preview_release_04.png)

对 agent training 更重要的是：长轨迹成本由 prefill、KV 常驻、decode 与并发共同决定。V4 的设计把优化对象从 attention FLOPs 扩到 KV cache，直接影响一台机器能同时承载多少环境 rollout。

### 后训练不是把所有数据混在一起，而是“专家先分化、能力再合并”

官方披露的两阶段流程是：先对不同领域分别做 SFT 与 GRPO，训练领域专家；再通过 on-policy distillation，把不同专家的能力汇总到一个统一模型。这里最值得记住的不是“用了 GRPO”，而是能力整合发生在 on-policy 分布上——学生在自己的轨迹上学习专家，能减少离线蒸馏里常见的状态分布偏移。

对于 tool-use / coding agent，这给出一个清晰实验方向：分别训练 browser、shell、coding、research 专家，再比较离线混合 SFT、off-policy 蒸馏与 on-policy consolidation 的稳定性和能力干扰。

## 架构：三项升级分别解决什么

| 组件 | 官方作用 | 我的理解 |
|---|---|---|
| CSA | 稀疏选择长上下文相关 token | 把全量历史变成可检索的注意力工作集 |
| HCA | 高压缩注意力状态 | 重点降低 1M context 下的 KV 常驻成本 |
| mHC | 约束 hyper-connection 的信号传播 | 在更复杂连接下保持训练稳定与表达能力 |
| Muon | 加快收敛、提升训练稳定性 | 说明规模扩展不只依赖架构，也改了 optimizer |
| MoE 13B active | 大总容量、低单步计算 | 适合大量生成 token 的 agent rollout |

## 能力不是“全面接近 Pro”

| Benchmark | Flash Non-Think | Flash High | Flash Max | Pro Max | 怎么看 |
|---|---:|---:|---:|---:|---|
| SimpleQA-Verified | 23.1 | 28.9 | 34.1 | 57.9 | 参数容量带来的知识差距明显 |
| GPQA Diamond | 71.2 | 87.4 | 88.1 | 90.1 | 加思考预算后接近 Pro |
| LiveCodeBench | 55.2 | 88.4 | 91.6 | 93.5 | 代码推理是 Flash 强项 |
| MRCR 1M | 37.5 | 76.9 | 78.7 | 83.5 | 长上下文随推理模式显著改善 |
| SWE Verified | 73.7 | 78.6 | 79.0 | 80.6 | agent coding 差距很小 |
| BrowseComp | — | 53.5 | 73.2 | 83.4 | 开放检索仍明显落后 Pro |
| Toolathlon | 40.7 | 43.5 | 47.8 | 51.8 | 工具任务差距可控 |

![DeepSeek-V4 官方综合性能图](src/assets/official_preview_release_02.png)

这些是官方 harness 下的自报结果，不能与第三方榜单直接混用。不过模式内对照仍有价值：Flash 的能力上限高度依赖 reasoning effort，评测时如果只跑默认模式，会低估它；如果只报 Max，又会忽略真实 token 成本。

## 训练公开了什么，仍缺什么

已公开的关键事实：

- Flash 与 Pro 均使用超过 32T 的多样、高质量预训练 token。
- 领域专家通过 SFT 与 GRPO 独立培养。
- 统一模型通过 on-policy distillation 吸收专家能力。
- 后训练 checkpoint 对 routed experts 使用 FP4，并进行了相应量化适配。
- 支持 Non-think、High、Max 三档 reasoning effort。

仍未公开：

- 32T 数据中代码、数学、中文、网页与合成数据的比例及 curriculum。
- CSA 的选择器训练目标、稀疏率调度，以及 HCA 的完整压缩细节。
- 各领域专家数量、GRPO reward 构成、rollout 规模与 on-policy 蒸馏损失权重。
- FP4 routed experts 的 QAT 细节及不同硬件上的真实吞吐。

## 使用时最容易踩的坑

官方仓库没有 Jinja chat template，而是提供独立 `encoding` 代码把 OpenAI 风格 messages 编成模型字符串，再解析输出。直接套通用 tokenizer chat template 可能得到错误格式。

```python
from encoding_dsv4 import encode_messages

prompt = encode_messages(
    [{"role": "user", "content": "审查这个仓库并修复测试"}],
    thinking_mode="thinking"
)
```

- 本地部署建议 `temperature=1.0, top_p=1.0`。
- Think Max 建议 context window 至少 384K；这不是说每个请求都要填满 384K，而是避免长 reasoning 被上限提前截断。
- 该页面对应四月 Preview；线上能力谱系应优先看七月的 [[DeepSeek-V4-Flash-0731]]。

## 对 Agent Training 的启发

> [!insight]
> V4-Flash 最有价值的研究角色是 **低激活、高总容量、百万上下文的 rollout generator**。如果训练目标是大量采集长轨迹，不应只比较单请求 accuracy，而应比较单位 GPU-hour 的 solved trajectories、KV cache 占用、有效 reasoning tokens 与 verifier 通过率。

可以直接做三组实验：

1. 固定总推理成本，比较 Flash-Max 与 Pro-High 谁产生更多可训练成功轨迹。
2. 将工具专家分别训练后做 on-policy consolidation，测量能力合并时的遗忘与负迁移。
3. 在 32K、128K、384K、1M 轨迹长度上记录 solved-task / KV-GB / latency，验证混合注意力的端到端收益。

## 证据边界

模型卡和 technical report 足以支撑架构、规模、训练范式与官方评测分析，因此本页达到完整精读标准；但 benchmark 均属于官方口径，DSBench 等内部集合不可独立复现。涉及部署吞吐与成本时，还需要在具体硬件与 serving stack 上复测。

## 一手资料

- [官方 Hugging Face model card](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash)
- [DeepSeek-V4 Technical Report（arXiv:2606.19348）](https://arxiv.org/abs/2606.19348) — 同时覆盖 V4-Flash 与 V4-Pro 的 family report
- [[src/huggingface_model_cards/DeepSeek-V4-Flash.md|本地 HF model card]]
- [[src/paper/main.tex|DeepSeek-V4 technical report 源码]]
- [[src/official_preview_release.md|官方 Preview 发布页]]
- [[DeepSeek-V4|V4 family 总览]]

## 待跟踪

- [ ] 用统一 agent harness 复测 Flash High / Max 的能力—token Pareto。
- [ ] 补充 CSA / HCA 的独立实现与 1M KV cache 实测。
- [ ] 对照 [[DeepSeek-V4-Flash-0731]]，区分架构收益与后训练 checkpoint 收益。
