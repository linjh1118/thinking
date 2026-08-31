---
title: "DeepSeek-V4-Pro-DSpark — Pro 推测解码发行物"
type: model-note
organization: "DeepSeek-AI"
release: 2026-06-27
year: 2026
model_code: "DeepSeek-V4-Pro-DSpark"
url: "https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro-DSpark"
license: MIT
tags: [model-note, base-model, deepseek, v4, dspark, speculative-decoding, serving]
topic: "13_base_model"
status: read
rating: 4
source_sufficiency: release-complete
created: 2026-09-01
updated: 2026-09-01
---

# DeepSeek-V4-Pro-DSpark

> [!tldr]
> **Pro-DSpark 是 V4-Pro 原 checkpoint 加推测解码模块的部署包，不是一个新的 1.6T 模型。** 对 49B activated 的 Pro，减少串行 target decode step 的潜在价值尤其大；但官方没有发布独立吞吐数据，因此不能把“有 DSpark”直接写成某个确定加速倍数。

![DeepSeek-V4 官方长上下文效率图](src/assets/official_preview_release_04.png)

> [!note] 资料充分度：发行物完整，不适用“独立基模精读”
> 官方明确说明它与 V4-Pro 是 same checkpoint。它没有独立预训练、后训练或能力变化，无法也不应该伪装成一篇新基模全链路笔记。本页完整覆盖其发行身份、部署方法、验证指标与公开缺口。

## 身份与主线关系

| 维度 | Pro | Pro-DSpark |
|---|---|---|
| Target checkpoint | DeepSeek-V4-Pro Preview | 完全相同 |
| 主体规模 | 1.6T total / 49B activated | 完全相同 |
| Context | 1M | 完全相同 |
| 新增 | 无 | DSpark speculative decoding module |
| 能力代际 | 四月 Preview | 仍是四月 Preview，不是新代 |
| Atlas 位置 | 主线 | 推测解码支线 |

正式 [[DeepSeek-V4-Pro-0813]] 已将 DSpark module 随 checkpoint 一起提供，所以独立 Pro-DSpark 更像四月 Preview 到正式版之间的 serving 发行节点。

## 为什么 Pro 更需要推测解码

Pro 每个 token 激活 49B 参数，约为 Flash 13B 的 3.8 倍。混合注意力已经把 1M context 下的 attention/KV 成本大幅压低，但 MoE forward 仍是每个自回归 token 都要执行的串行工作。DSpark 试图一次提议多个 token，再由 target 批量验证，从另一个维度减少 decode wall time。

这两种优化可以叠加：

- CSA/HCA：降低长上下文 attention 与 KV cache 成本；
- MoE：降低每 token 激活参数；
- DSpark：降低每个输出序列需要的串行 target steps。

![DeepSeek-V4 官方规格图](src/assets/official_preview_release_01.png)

## 官方接入方式

vLLM 的核心参数：

```bash
vllm serve deepseek-ai/DeepSeek-V4-Pro-DSpark \
  --trust-remote-code \
  --speculative-config '{"method":"dspark","num_speculative_tokens":7,"draft_sample_method":"greedy"}'
```

SGLang 使用：

```bash
sglang serve \
  --model-path deepseek-ai/DeepSeek-V4-Pro-DSpark \
  --speculative-algorithm DSPARK
```

因为 speculative 权重已经在 checkpoint 内，SGLang 不需要 `--speculative-draft-model-path`。若另挂一个 draft model，就不是这张 model card 描述的部署方式。

## “同 checkpoint”意味着什么

在正确实现下，DSpark 的目标是保持 Pro target distribution，而不是改变模型知识或推理策略。因此：

- 不能给 Pro-DSpark 单列一个能力代际；
- 不需要重复抄一份 Pro benchmark 假装是新评测；
- 应检查输出等价性与接受/拒绝逻辑，而非期待准确率提升；
- 若出现显著能力差异，首先怀疑 decoding 实现、采样参数或数值精度。

## 部署验收应看哪些指标

| 指标 | 为什么必要 |
|---|---|
| acceptance rate | 决定 speculative work 有多少被真正采用 |
| accepted tokens / target step | 比单看候选长度更直接 |
| p50 / p95 latency | agent 用户更关心尾部等待 |
| tokens/s at batch N | 高并发可能与单流结论相反 |
| GPU memory | 附加模块和缓存并非零成本 |
| output equivalence | 确认加速没有改变目标分布 |
| solved tasks / GPU-hour | 对 rollout 系统的最终指标 |

> [!insight]
> Pro-DSpark 对 agent training 的价值应按“每 GPU-hour 能得到多少条通过 verifier 的长轨迹”来衡量。若推测模块只提升短文本单流吞吐，却在工具交替、长 reasoning 或高并发下接受率下降，它对训练集群的实际价值可能有限。

## 官方资料没有提供什么

没有独立的 DSpark benchmark、硬件吞吐、batch scaling、接受率、额外显存、数值一致性或长输出稳定性数据；也没有说明 speculative module 如何训练。因此本页没有声称固定 speedup。

这正是“原始资料较少”需要明确写出的地方：模型身份与接入方式证据充分，性能量化证据不足。

## 一手资料

- [官方 Hugging Face model card](https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro-DSpark)
- [[src/huggingface_model_cards/DeepSeek-V4-Pro-DSpark.md|本地 HF model card]]
- [DeepSpec 官方仓库](https://github.com/deepseek-ai/DeepSpec)
- [[DeepSeek-V4-Pro|Pro checkpoint 精读]]
- [[DeepSeek-V4|V4 family 总览]]

## 待补证据

- [ ] 在 Pro 典型多节点配置上测吞吐、接受率和尾延迟。
- [ ] 验证 High / Max 长 reasoning 的收益是否稳定。
- [ ] 与 Pro-0813 内置 DSpark 做同机对照。
