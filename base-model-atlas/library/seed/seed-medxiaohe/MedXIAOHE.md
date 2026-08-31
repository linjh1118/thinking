---
title: "MedXIAOHE — Medical MLLM Overview"
type: model-note
authors: ["ByteDance XiaoHe Medical AI", "et al."]
year: 2026
arxiv: "2602.12705"
url: "https://arxiv.org/abs/2602.12705"
tags: [model-note, base-model, seed, medical, multimodal]
status: read
created: 2026-08-31
updated: 2026-08-31
---

# MedXIAOHE — Medical MLLM Overview

> [!tldr]
> MedXIAOHE 不是 Seed 通用主干的新正代，而是字节小荷医疗团队构建医疗多模态大模型的完整 recipe；在谱系中应归入 **ByteDance · Seed → Medical** 支线。

## 定位

MedXIAOHE 面向医疗多模态理解和长报告生成，重点不是单一 benchmark 冲分，而是把数据构建、偏好准则、证据约束推理与低幻觉长文本生成串成可复现流程。

## 方法与研究价值

- 通过医疗图文数据治理与多阶段训练建立领域能力。
- 引入用户偏好 rubric 与 evidence-grounded reasoning，强调真实医疗指令的可用性。
- 将低幻觉长报告生成视为核心交付，而不是只评短答案准确率。

> [!insight]
> 对 agent training 的启发是：高风险垂直领域不能只靠通用 RL reward；需要把证据引用、偏好 rubric、长报告结构和幻觉惩罚共同写进 verifier 与训练数据闭环。

## 证据边界

- 技术报告：[https://arxiv.org/abs/2602.12705](https://arxiv.org/abs/2602.12705)
- 归属口径：团队为 ByteDance XiaoHe Medical AI；Atlas 按字节 Seed 研究生态收录为医疗支线，不把它误写成 Seed2.x 通用基模。

## 导航

- [[Topics/13_base_model/Base_Model_Top8_Branch_Audit_2026|Top 8 支线审计]]
- [[MedXIAOHE_poster_zh|中文 Poster]]
