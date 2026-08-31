---
title: "Base Model Coverage Gaps — 还缺什么"
type: insight
tags: [insight, base-model, coverage, research-map]
source: "[[Topics/13_base_model/Base Model MOC]]"
related:
  - "[[Topics/13_base_model/Base_Model_Insight]]"
  - "[[Topics/13_base_model/13_base_model_汇总]]"
created: 2026-06-12
updated: 2026-06-18
---

# Base Model Coverage Gaps — 还缺什么

> [!tldr]
> BaseModel topic 现在不是“资料少”，而是“资料层级还没分开”：国内开源 technical report 细，闭源模型多是 system card / blog；模型列表多，横向设计判断少；能力指标多，证据可信度和真实产品成本少。最应该补的是四类缺口：闭源模型逐卡拆解、DeepSeek 等关键基线、training/serving infra、safety/alignment 和 benchmark 可信度。

## 一句话诊断

当前 BaseModel topic 已经能回答“2025-2026 有哪些模型和主线”，但还不能稳定回答下面三个更有研究价值的问题：

1. 如果我要训练一个 agent base model，哪些设计是必须前置到 pretrain/midtrain 的？
2. 如果我要做 Coding Agent / Research Agent / RL Infra，应该选哪类基座，为什么？
3. 不同模型的分数到底是模型能力、scaffold、verifier、context budget、还是产品工程带来的？

也就是说，缺口不是更多模型名，而是“决策级比较”。

## 目前的强项和弱项

| 模块 | 当前强度 | 关键价值 | 主要短板 |
|---|---|---|---|
| 国内开源 technical reports | 强 | Qwen、GLM、Kimi、MiniMax、MiMo、StepFun 给了训练/架构/RL 细节 | 容易形成“国内路线过采样”的视角偏差 |
| Agentic RL / verification | 强 | GRPO-RoC、CISPO、RLCS、MOPD、Forge、PARL、Verification Agent 已经成谱系 | 还缺把算法映射到 failure mode 的系统比较 |
| 闭源 frontier models | 中弱 | OpenAI、Anthropic、Gemini、Llama 有剪藏和 model/system card | 缺逐模型拆解，训练和架构证据不足 |
| Inference / serving | 弱 | Step-3、MiniMax、MiMo 提供一些 cost/throughput 信号 | 还没有统一成本模型：active params、KV、通信、tool latency |
| Safety / alignment | 弱 | System card 材料已经在 vault 里 | 缺 agentic safety、computer use、cyber、sandbox 的横向分析 |
| Benchmark 可信度 | 弱 | MOC 收集了很多 benchmark | 缺证据等级、scaffold 依赖、leakage、cost per solved task |

相关来源：
- [[Topics/13_base_model/Base Model MOC]]
- [[Topics/13_base_model/Base_Model_Insight]]
- [[Topics/13_base_model/13_base_model_汇总]]

## P0 缺口：必须补，否则判断会偏

### 1. DeepSeek 系列缺位

很多现有笔记都把 DeepSeek-V3/R1 当 baseline：Kimi K2 对比 DeepSeek-V3，MiniMax-M1 对比 DeepSeek R1，GLM-4.5 对比 671B 级模型，Step 3.5 Flash 也拿 DeepSeek V3.2 Exp 做 base 对照。可是 BaseModel topic 内没有独立 DeepSeek 系统笔记。

这会导致一个问题：我们不断引用 baseline，却没有真正理解 baseline 的训练、MoE、MLA、RL、serving 和局限。

建议补：

| 优先级 | 文档 | 要回答的问题 |
|---|---|---|
| P0 | DeepSeek-V3 / V3.2 Base 对比笔记 | MLA、MoE、数据、训练稳定性到底是什么 baseline |
| P0 | DeepSeek-R1 / GRPO 路线笔记 | 后续 CISPO、GRPO-RoC、MIS-PO 都是在回应它什么问题 |
| P1 | DeepSeek attention / sparse attention 相关笔记 | 和 Kimi Linear、MiniMax MSA、MiMo Hybrid SWA 做 architecture 对照 |

### 2. Anthropic / OpenAI 不能只停在 clipping

OpenAI 和 Anthropic 对 BaseModel 研究很关键，但目前多是官方剪藏。剪藏能记录产品叙事，不能支撑训练 recipe 结论。

最该补的不是“GPT-5.5 又发了什么”，而是：

| 公司 | 应补文档 | 真正要拆的问题 |
|---|---|---|
| OpenAI | GPT-5 unified system / Codex 系列 system card 拆解 | router、thinking/fast split、long-running task、sandbox、tool safety |
| Anthropic | Claude 4.5-4.7 system cards 逐卡拆解 | agentic safety、computer use、coding autonomy、1M context beta |
| Google | Gemini Computer Use / Gemini 3.x model card 拆解 | multimodal reasoning、computer use environment、model card eval methodology |
| Meta | Llama 4 Herd 独立笔记 | open-weight native multimodal、MoE、early fusion、Llama Guard |

### 3. 证据等级必须显式化

当前同一个 MOC 里混用了 technical report、system card、official blog、GitHub、HF card、poster。它们不是同一类证据。

| 等级 | 来源 | 能支持的结论 | 不能支持的结论 |
|---|---|---|---|
| A | Technical report / full model card | 训练、架构、消融、benchmark 细节 | 仍需警惕自报告偏差 |
| B | System card / safety report | safety、deployment、风险缓解、能力边界 | 训练 recipe、架构细节 |
| C | Official blog / GitHub / HF card | 产品定位、开源状态、接口、生态 | 严格横向性能比较 |
| D | Poster / secondary summary | 快速索引 | 作为唯一证据 |

以后每个横向对比文档都应该在表外标注“证据等级”。这比继续堆模型名更有价值。

## P1 缺口：决定研究判断质量

### 4. Training infra 缺独立层

真正决定 agentic RL 能否 scale 的往往不是算法名，而是训练系统：

- GLM-4.5 的 Slime：同步/异步混合训练、FP8 rollout、Docker agent 环境。
- MiniMax M2 的 Forge：白盒/黑盒 agent 统一接入、Windowed FIFO、artifact reward。
- Qwen3-Coder-Next 的 reward hacking blocker：防止 agent 用环境漏洞偷答案。
- MiMo 的 MOPD：多 teacher 合并，解决 multi-domain RL interference。
- Step 3.5 Flash 的可扩展 RL loop：expert trajectory -> rejection sampling -> self-distillation。

建议单独补 `Base_Model_RL_Infra_Comparison.md`。

关键 insight：Agentic RL 的护城河不只是 policy optimizer，而是 rollout 系统、verifier 系统、环境隔离、数据池和反作弊。

### 5. Serving / productization 缺成本模型

Agent base model 不是聊天模型。它真正的产品指标是 cost per solved task，而不是 token 单价或 MMLU。

需要统一比较：

| 成本项 | 为什么关键 |
|---|---|
| active params | 决定每 token compute，但不决定权重显存 |
| total params | 决定 MoE 权重加载、专家并行、部署复杂度 |
| KV cache | 决定 128K/1M context 是否可用 |
| attention pattern | full / sparse / linear / SWA 直接影响长轨迹成本 |
| MTP acceptance | 决定 rollout 和 decoding 吞吐 |
| tool latency | coding / search agent 的真实瓶颈 |
| retry / self-debug | 高分可能来自更多尝试，不一定来自更强单步能力 |

本轮已经写了 [[Topics/13_base_model/Base_Model_Inference_Productization_Comparison]]，但后续还可以补一张定量 cost matrix。

### 6. Safety / alignment 应该成为独立主题

BaseModel topic 现在太偏 capability。Agent Foundation Model 的 safety 问题不是普通 chatbot safety，而是：

- computer use 权限边界
- agent 自主长期运行
- tool misuse / data exfiltration
- benchmark leakage 和 reward hacking
- cyber / code execution / sandbox escape
- model self-evolution 的 governance

建议补 `Base_Model_Safety_Alignment_Comparison.md`，优先拆 OpenAI / Anthropic / Google system cards。

## P2 缺口：扩展全球模型生态

| 方向 | 为什么值得补 | 优先级 |
|---|---|---|
| Mistral / Magistral / Codestral | 欧洲开源和商业 coding/reasoning 路线 | P1 |
| xAI Grok | 长上下文、实时工具、产品化路线 | P1 |
| Cohere Command | enterprise / RAG / tool use / retrieval 场景 | P2 |
| NVIDIA Nemotron | synthetic data、reward model、enterprise AI | P2 |
| Microsoft Phi / small models | 小模型效率和端侧部署 | P2 |

## 最关键的 meta insight

BaseModel topic 应该从“模型百科”升级成“agent base model 设计空间”。最好的组织方式不是公司列表，而是四层结构：

1. 公司/模型时间线：MOC 负责。
2. 横向设计维度：pretrain、SFT、RL、architecture、evaluation、serving、安全。
3. 可迁移 recipe：tool template scaling、MOPD、Forge、RLCS、CSRS、reward hacking blocker。
4. 研究假设：哪些 recipe 可以迁移到 BrainHao 关注的 agentic RL / RL Infra / Harness。

如果只停在“谁发布了什么模型”，这个 topic 会很快过期；如果整理成设计空间，它会变成后续做 agent training 和 agentic RL 的方法库。
