---
title: "Base Model Architecture Comparison"
type: insight
tags: [insight, base-model, architecture, moe, attention, multimodal, inference]
source: "[[Topics/13_base_model/Base Model MOC]]"
related:
  - "[[Topics/13_base_model/QA/0611_MoE_vs_Dense_Resource_Comparison]]"
  - "[[Topics/13_base_model/Base_Model_Inference_Productization_Comparison]]"
created: 2026-06-12
updated: 2026-06-18
---

# Base Model Architecture Comparison

> [!tldr]
> 架构竞争已经不是 Dense vs MoE 这么简单，而是四个瓶颈的联合优化：每 token compute、KV/cache/context 成本、rollout/decode 吞吐、多模态/工具接口。Kimi K2 证明 sparsity 是独立 scaling 维度；MiniMax/Kimi Linear/MiMo/StepFun 证明长上下文必须改 attention；MiMo/GLM/StepFun 证明 MTP 正在变成训练和推理的共同接口；Qwen-Omni/Kimi K2.5/MiniMax M3 说明 agent 架构必须原生支持多模态状态。

## 高关键对比：架构创新到底解决哪个瓶颈

| 瓶颈 | 架构路线 | 代表模型 | 解决方式 | 代价 |
|---|---|---|---|---|
| 每 token compute 太高 | small-active / ultra-sparse MoE | Kimi K2, MiniMax M2, MiMo V2, Step 3.5 | 总参数大，激活参数小 | 权重显存、专家并行、通信复杂 |
| 1M context 太贵 | hybrid / sparse / linear attention | MiniMax M1/M3, Kimi Linear, MiMo Hybrid SWA | 降低 attention/KV 成本 | retrieval recall 和全局信息整合风险 |
| rollout / decoding 太慢 | MTP / speculative decoding | GLM-4.5, MiMo V2, Step 3.5, MiniMax M2 | 多 token 预测，提升 decode 和 RL rollout 吞吐 | acceptance rate 依赖任务熵 |
| 多模态互相拖累 | native multimodal / Thinker-Talker / early fusion | Qwen3.5-Omni, Kimi K2.5, MiniMax M3 | 模态从训练早期或架构层面融合 | 训练数据和对齐复杂度高 |
| agent 状态太长 | interleaved thinking + long context | MiniMax M2/M3, Kimi K2.5 | 保留 reasoning/action/observation 历史 | 成本和 memory policy 复杂 |

## 模型结构速览

| 模型 | 参数/激活 | Attention/context | 关键结构 | 架构判断 |
|---|---|---|---|---|
| Qwen3 | Dense 0.6B-32B；MoE 235B/22B | GQA | no QKV bias, QK-Norm | 稳健的通用家族，架构不是最激进，recipe 是核心 |
| Qwen3-Coder-Next | 80B/3B active | 细节未充分展开 | coding/tool 专项 MoE | 证明小激活 + 强后训练可放大 agent 能力 |
| Qwen3.5-Omni | Hybrid Attention MoE | 256K context | Thinker/Talker, ARIA | 适合实时 omni agent，关键是理解/生成解耦 |
| GLM-4.5 | 355B/32B active | 96 heads, QK-Norm | loss-free routing, MTP, deeper-not-wider | 固定预算下更深结构利于 reasoning |
| Kimi K2 | 1.04T/32.6B active | MLA, 128K | MuonClip, 384 experts, sparsity 48 | sparsity 是独立 scaling 维度 |
| Kimi Linear | 48B/3B active | KDA 3:1 hybrid, 1M | per-channel gating, NoPE | linear attention 进入可生产候选 |
| MiniMax-M1 | 456B/45.9B active | 7 Lightning + 1 softmax, 1M/80K | CISPO | 长 reasoning 成本下降是主贡献 |
| MiniMax M2 | 229.9B/9.8B active | Full MHA with GQA, 192K | fine-grained MoE, Forge | 架构服务于 agentic RL 和真实任务 |
| MiniMax M3 | 未完整公开 | MSA, 1M | native multimodality | 从“长上下文可用”转向“长任务可持续” |
| MiMo-V2-Flash | 309B/15B active | Hybrid SWA 5:1 | MTP, MOPD | agent efficiency stack 完整 |
| MiMo-V2.5-Pro | 1.02T/42B active | Hybrid SWA 6:1, 1M | omnimodal, MTP | 长程 agent + token efficiency |
| Step-3 | 321B/38B active | MFA | AFD | model-system co-design 直接优化解码成本 |
| Step 3.5 Flash | 196B/11B active | 3:1 SWA/full | MTP-3, head-wise gating | 能力密度路线很强 |

相关来源：
- [[Topics/13_base_model/Moonshot_Kimi/2507_Kimi_K2/Kimi-K2-Open-Agentic-Intelligence]]
- [[Topics/13_base_model/Moonshot_Kimi/2510_Kimi_Linear/Kimi-Linear-Expressive-Efficient-Attention]]
- [[Topics/13_base_model/MiniMax/2506_MiniMax_M1/MiniMax-M1-Scaling-Test-Time-Compute-Lightning-Attention]]
- [[Topics/13_base_model/MiniMax/2606_MiniMax_M3/MiniMax-M3-Frontier-Coding-1M-Context-Native-Multimodality]]
- [[Topics/13_base_model/Xiaomi_MiMo/MiMo-Summary-Dense]]
- [[Topics/13_base_model/stepfun/2507_Step_3_Large_Affordable/Step_3_Large_Affordable]]

## 关键 insight 1：Total params 是能力容量，active params 是计算成本，二者都不是部署成本

很多模型现在会写成 “309B/15B active” 或 “1T/32B active”。这不能简单理解为 15B 或 32B 模型。

| 指标 | 决定什么 | 容易误读 |
|---|---|---|
| total params | 权重容量、专家总知识量、显存需求 | 以为总参越大每 token 越慢 |
| active params | 每 token FFN compute | 以为 active 小就能单卡部署 |
| expert count / top-k | 稀疏度、通信模式、专家利用率 | 忽略 all-to-all 通信 |
| KV cache | 长上下文显存 | 和 active params 没有直接关系 |
| attention pattern | 长上下文 FLOPs / recall | 只看 context length 不看成本 |

参考：[[Topics/13_base_model/QA/0611_MoE_vs_Dense_Resource_Comparison]]

## 关键 insight 2：长上下文架构路线分成三派

### A. Hybrid local/global attention

代表：MiMo Hybrid SWA、Step 3.5 Flash。

适合 agent，因为局部 action-observation 很密集，但周期性需要全局回看。风险是全局 block 太少会漏远处关键状态。

### B. Linear attention

代表：Kimi Linear。

优势是 KV cache 和 1M decode throughput。风险是有限状态容量，需要 hybrid global attention 弥补 long-context retrieval。

### C. Block sparse attention

代表：MiniMax M3 的 MSA。

最贴近 agent memory：先筛相关 KV blocks，再做精确 attention。风险是 block selection recall，一旦筛掉关键失败步骤，后续无法恢复。

## 关键 insight 3：MTP 是 agent RL 的基础设施，不只是推理加速

MTP 的价值有三层：

1. Pretraining auxiliary loss：提升 next-token 表征质量。
2. Speculative decoding：减少推理延迟。
3. RL rollout acceleration：降低 on-policy generation 成本。

对普通聊天，MTP 是加速器；对 agentic RL，MTP 可能是能不能规模化的瓶颈开关。因为 agent RL 最贵的是采样轨迹，而不是训练 backward。

## 关键 insight 4：多模态 agent 不能只靠 adapter

多模态架构有三种层级：

| 层级 | 做法 | 代表 | 局限 |
|---|---|---|---|
| Adapter VLM | 训好 LLM 后接 vision encoder/projector | 早期 VLM、部分小模型 | 容易视觉变外挂 |
| Early/native fusion | 训练早期混合 text/image/video | Kimi K2.5, MiniMax M3 | 数据工程难，但能力融合好 |
| Modality-specialized architecture | Thinker/Talker、ARIA、omni agent | Qwen3.5-Omni | 系统复杂，但适合实时交互 |

多模态 agent 需要的是 perception-action 统一，而不是只会看图说话。MiMo-V2-Omni、Seed2.0、MiniMax M3 的叙事都在往这个方向走。

## 架构选型建议

| 目标 | 更合理的架构优先级 |
|---|---|
| 高并发 coding agent | small-active MoE + MTP + robust tool-use post-training |
| 1M context research/coding | sparse/hybrid/linear attention + long-context verifier |
| RL infra 训练 | MTP/spec decoding + async rollout + strong blocker |

## 最短结论

未来 agent base model 的架构不是“越大越好”，而是“哪个瓶颈最先爆”。如果瓶颈是 reasoning capacity，用 MoE；如果瓶颈是 1M context，用 sparse/linear/hybrid attention；如果瓶颈是 rollout，优先 MTP/spec decoding；如果瓶颈是多模态状态建模，优先 native multimodal + trajectory data。
