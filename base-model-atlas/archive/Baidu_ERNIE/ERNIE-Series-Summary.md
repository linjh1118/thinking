---
title: "Baidu ERNIE Series Summary"
type: insight
source: "[[Topics/13_base_model/Base Model MOC]]"
authors: ["Baidu ERNIE Team"]
year: 2026
venue: "arXiv / ERNIE Blog / Baidu PRNewswire"
arxiv:
doi:
url: "https://ernie.baidu.com/blog/"
tags: [insight, baidu, ernie, base-model, multimodal, moe, agentic-rl]
topic: "13_base_model"
status: read
rating: 4
related:
  - "[[Topics/13_base_model/Base Model MOC]]"
  - "[[Topics/13_base_model/Baidu_ERNIE/2503_ERNIE_4_5_and_X1/src/ERNIE-4.5 - Official Blog]]"
  - "[[Topics/13_base_model/Baidu_ERNIE/2602_ERNIE_5_0/src/ERNIE-5.0 - Official Blog]]"
  - "[[Topics/13_base_model/Baidu_ERNIE/2605_ERNIE_5_1/src/ERNIE-5.1 - Official Blog]]"
created: 2026-06-18
updated: 2026-06-18
---

# Baidu ERNIE Series Summary

> [!tldr]
> ERNIE 系列的主线不是单纯从 encoder 到大模型放大，而是从 **knowledge-enhanced pretraining** 起步，逐步转向 **多模态 MoE、统一自回归多模态、弹性子网继承、分离式异步 RL 和 agentic post-training**。它对 Base Model 主题的价值在于补齐一条中国特色的工业路线：知识增强和应用生态很早，2025 之后才把技术叙事集中到 open-weight multimodal foundation model 与 agent/reasoning 能力。

> [!note]
> 本次只完成材料入库与系列索引：arXiv 条目已抓取 LaTeX 源码和 `meta.json`；无 arXiv 的型号以官方博客 / Baidu PRNewswire / 发布页剪藏形式保存。尚未写逐篇精读 paper notes。

## 系列演化判断

ERNIE 的早期路线和 Qwen/Kimi/MiniMax/GLM 不太一样。2019-2021 的 ERNIE 更像是 BERT/T5 时代的 **知识增强预训练谱系**：entity masking、phrase masking、continual multi-task pretraining、知识记忆与语言理解生成统一。它的重点不是 agent，也不是 long-context，而是把结构化知识和海量语料里的语义关系注入表示学习。

2025 之后的 ERNIE 叙事发生明显切换：ERNIE 4.5 把重点放到 **native multimodal + heterogeneous MoE + PaddlePaddle training/serving stack**；ERNIE 5.0 进一步强调统一多模态自回归，把 text/image/video/audio 放进同一 Next-Group-of-Tokens Prediction 框架；ERNIE 5.1 则把关键增量讲成 **多维弹性预训练 + 分离式全异步 RL + scaled agentic post-training**。

我的判断：ERNIE 的研究价值不在于“某个 benchmark 是否第一”，而在于它展示了一个工业模型从知识增强到多模态、再到 agentic RL 的转型过程。对 agent training 研究来说，最值得后续精读的是 ERNIE 5.0/5.1：它们把 MoE 子网弹性、统一多模态、RL 训练基础设施和 agent evaluation 连在了一起。

## 本地材料索引

### arXiv 源码

| 月份 | 模型/论文 | arXiv | 本地源码 | 核心关键词 |
|---|---|---|---|---|
| 2019-04 | ERNIE: Enhanced Representation through Knowledge Integration | 1904.09223 | `Topics/13_base_model/Baidu_ERNIE/1904_ERNIE/src/` | knowledge masking, entity-level masking, phrase-level masking |
| 2019-07 | ERNIE 2.0 | 1907.12412 | `Topics/13_base_model/Baidu_ERNIE/1907_ERNIE_2_0/src/` | continual pretraining, multi-task learning, language understanding |
| 2021-07 | ERNIE 3.0 | 2107.02137 | `Topics/13_base_model/Baidu_ERNIE/2107_ERNIE_3_0/src/` | knowledge enhanced pretraining, understanding and generation |
| 2021-12 | ERNIE 3.0 Titan | 2112.12731 | `Topics/13_base_model/Baidu_ERNIE/2112_ERNIE_3_0_Titan/src/` | large-scale knowledge enhanced pretraining, distributed inference |
| 2022-12 | ERNIE-Code | 2212.06742 | `Topics/13_base_model/Baidu_ERNIE/2212_ERNIE_Code/src/` | cross-lingual code pretraining, programming languages |
| 2023-01 | ERNIE 3.0 Tiny | 2301.03416 | `Topics/13_base_model/Baidu_ERNIE/2301_ERNIE_3_0_Tiny/src/` | task-agnostic distillation, small model generalization |
| 2026-02 | ERNIE 5.0 Technical Report | 2602.04705 | `Topics/13_base_model/Baidu_ERNIE/2602_ERNIE_5_0/src/` | unified multimodal, ultra-sparse MoE, elastic training, multimodal generation |

### 官方网页 / 发布页剪藏

| 月份 | 模型/页面 | 本地剪藏 | 证据类型 | 关键点 |
|---|---|---|---|---|
| 2023-07 | ERNIE 3.5 | [[Topics/13_base_model/Baidu_ERNIE/2307_ERNIE_3_5/src/ERNIE-3.5 - Baidu PRNewswire]] | Baidu PRNewswire | 3.5 相比 3.0 提升训练吞吐和 QPS，强调产业落地 |
| 2023-10 | ERNIE 4.0 | [[Topics/13_base_model/Baidu_ERNIE/2310_ERNIE_4_0/src/ERNIE-4.0 - Baidu PRNewswire]] | Baidu PRNewswire | 理解、生成、推理、记忆四项能力升级 |
| 2024-06 | ERNIE 4.0 Turbo | [[Topics/13_base_model/Baidu_ERNIE/2408_ERNIE_4_0_Turbo/src/ERNIE-4.0-Turbo - Baidu PRNewswire]] | Baidu PRNewswire / 财报发布 | 更快、更低成本的 4.0 变体 |
| 2025-03 | ERNIE 4.5 / X1 | [[Topics/13_base_model/Baidu_ERNIE/2503_ERNIE_4_5_and_X1/src/ERNIE-4.5-and-X1 - Baidu PRNewswire]] | Baidu PRNewswire | 4.5 原生多模态，X1 深度思考 reasoning model |
| 2025-04 | ERNIE 4.5 Turbo / X1 Turbo | [[Topics/13_base_model/Baidu_ERNIE/2504_ERNIE_4_5_Turbo_and_X1_Turbo/src/ERNIE-4.5-Turbo-and-X1-Turbo - Baidu PRNewswire]] | Baidu PRNewswire | Turbo 线强调低价、高速、多模态和工具调用 |
| 2025-06 | ERNIE 4.5 Official Blog | [[Topics/13_base_model/Baidu_ERNIE/2503_ERNIE_4_5_and_X1/src/ERNIE-4.5 - Official Blog]] | ERNIE official blog | 10 个开源模型、heterogeneous multimodal MoE、PaddlePaddle/ERNIEKit/FastDeploy |
| 2026-02 | ERNIE 5.0 Official Blog | [[Topics/13_base_model/Baidu_ERNIE/2602_ERNIE_5_0/src/ERNIE-5.0 - Official Blog]] | ERNIE official blog | 2.4T unified multimodal model，text/image/video/audio 统一自回归 |
| 2026-05 | ERNIE 5.1 Official Blog | [[Topics/13_base_model/Baidu_ERNIE/2605_ERNIE_5_1/src/ERNIE-5.1 - Official Blog]] | ERNIE official blog | 多维弹性预训练、分离式全异步 RL、scaled agentic post-training |
| 2026-06 | ERNIE Publications | [[Topics/13_base_model/Baidu_ERNIE/src/ERNIE Publications - Official Page]] | ERNIE official publication page | 官方论文入口，列出 ERNIE 4.5 Technical Report 与 ERNIE 5.0 arXiv |

## 对 Base Model 主题的补位价值

1. **知识增强路线的历史纵深**：ERNIE 早期论文可以作为“pretraining 目标设计”的历史对照。它提醒我们，base model 能力并不只来自数据量和参数量，也来自 masked task / knowledge integration 的 inductive bias。

2. **工业多模态 MoE 的另一种实现**：ERNIE 4.5 的 heterogeneous modality structure 与 Qwen3-Omni 的 Thinker-Talker、Kimi K2.5 的 text-vision joint optimization、MiMo-V2-Omni 的 omnimodal agent 路线都可对比。

3. **Agentic RL infra 值得单独拆**：ERNIE 5.1 官方页把“分离式全异步强化学习训练”作为关键技术点，这和 GLM Slime、MiniMax Forge、Qwen3-Coder-Next reward hacking blocker、MiMo MOPD 属于同一层问题：不是只调 GRPO，而是构建能支撑长程环境训练的系统。

## 后续精读优先级

| 优先级 | 材料 | 为什么 |
|---|---|---|
| P0 | ERNIE 5.0 Technical Report | 统一多模态 + ultra-sparse MoE + elastic training，直接对齐 2026 base model 主线 |
| P0 | ERNIE 5.1 Official Blog | 虽不是论文，但明确给出 agentic RL infra 叙事，适合放入 RL infra 横向对比 |
| P1 | ERNIE 4.5 Technical Report / Official Blog | heterogeneous multimodal MoE 与开源生态，适合对比 Qwen/MiMo/GLM |
| P2 | ERNIE 2.0 / 3.0 / Titan | 作为知识增强预训练历史路线，用于写 pretraining objective 对照 |

## 关联主题

- [[Topics/13_base_model/Base_Model_Pretraining_Comparison]] — 可加入 ERNIE 早期 knowledge-enhanced objectives 与 5.0 unified multimodal objective。
- [[Topics/13_base_model/Base_Model_Architecture_Comparison]] — 可加入 ERNIE 4.5 heterogeneous MoE 与 ERNIE 5.0 ultra-sparse MoE。
- [[Topics/13_base_model/Base_Model_RL_Comparison]] — 可加入 ERNIE 5.1 的 disaggregated fully-asynchronous RL。
- [[Topics/13_base_model/Base_Model_Inference_Productization_Comparison]] — 可加入 PaddlePaddle / FastDeploy / ERNIEKit / PD disaggregation。

> 📊 相关可视化: [[00.work/260618_ernie_series/discussion_ernie_series]]

---

## 精读笔记与 Poster

| 论文 | 笔记 | Poster |
|------|------|--------|
| ERNIE 5.0 | [[Topics/13_base_model/Baidu_ERNIE/2602_ERNIE_5_0/ERNIE-5-0-Technical-Report]] | [[Topics/13_base_model/Baidu_ERNIE/2602_ERNIE_5_0/ERNIE_5_0_poster_zh]] |
| ERNIE 3.0 | 待写 | 待写 |
| ERNIE-Code | 待写 | 待写 |
| ERNIE 3.0 Tiny | 待写 | 待写 |
| ERNIE 1.0/2.0 | 待写 | 待写 |
