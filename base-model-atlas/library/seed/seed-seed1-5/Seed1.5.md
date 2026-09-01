---
title: "Seed1.5（Doubao-1.5-pro）— 稀疏 MoE 的生产化起点"
type: model-note
year: 2025
url: "https://seed.bytedance.com/en/special/doubao_1_5_pro"
tags: [model-note, base-model, seed, moe, multimodal, serving]
status: read
created: 2026-08-31
updated: 2026-09-01
---

# Seed1.5（Doubao-1.5-pro）— 稀疏 MoE 的生产化起点

> [!tldr]
> Seed1.5 的核心不是堆出一个更大稠密模型，而是把 **稀疏 MoE、训练—推理一体化设计、低精度 serving 与多模态数据合成** 同时做成生产系统。官方将 2025-01-22 发布的 Doubao-1.5-pro 纳入 Seed1.5 主线；Atlas 保留 family 节点，但不能把 Seed1.5-VL 的全部论文结论倒灌给通用版。

![Doubao-1.5-pro 官方主视觉](src/assets/hero.jpeg)

## 一页判断

| 维度 | 官方做法 | 主线意义 |
|---|---|---|
| 架构 | 高稀疏 MoE，小激活参数 | 以更低推理计算承载更大容量 |
| Scaling | 在相同 9T tokens 阶段实验中研究 MoE 稀疏度 | 用可观测训练曲线选择效率点 |
| Serving | Prefill/Decode、Attention/FFN 四象限分别优化 | 模型结构从一开始考虑线上吞吐 |
| 多模态 | 图文、语音与纯文本混合训练；RL 阶段投入较多 | 多模态不是简单外挂 encoder |

## MoE：性能杠杆而非免费午餐

官方专题页称，在相同 9T tokens 的阶段性对比中，优化后的 MoE 以约为对应稠密模型 **1/7 的激活参数**达到或超过其性能。这个“7 倍杠杆”是特定内部对照，不等于所有 workload 都能获得 7 倍端到端加速；专家权重驻留、路由与通信仍有成本。

![Seed1.5 MoE 与 Dense 效率对比](src/assets/moe-efficiency.png)

## 训练—推理一体化

Seed1.5 把 serving 约束前置到模型设计：Prefill 更偏计算瓶颈，Decode 更容易受访存与通信影响；官方分别采用低精度 attention、W4A8 FFN、跨 query batching 与分块流水等策略。这意味着“模型能力”与“能否低延迟、高吞吐上线”不是两个串行阶段。

![Doubao-1.5-pro 官方综合评测](src/assets/benchmark.jpeg)

多模态后训练则使用人工与模型合成偏好数据，并在 RL 阶段针对不同 prompt 设计偏好标准、削弱长度偏好。对 Agent Training，这比单纯“多模态榜单更高”更重要：reward model 如果把冗长误当质量，会直接抬高长轨迹成本。

> [!insight]
> Seed1.5 提供了一个很实用的研究命题：Agent 模型的 scaling law 应同时包含任务成功率、激活参数、TTFT/TPOT 与轨迹长度。只优化模型分数，会把成本问题推迟到无法修补的 serving 阶段。

## 资料充分度与证据边界

> [!warning]
> 通用 Seed1.5 缺少独立的完整 Tech Report；本页主要依据官方专题页。Seed1.5-VL 有 arXiv 报告，但它是多模态支线，只能用来理解同代视觉训练方法，不能代替通用模型的参数和评测证据。

## 一手资料

- [Doubao-1.5-pro 官方专题](https://seed.bytedance.com/en/special/doubao_1_5_pro)
- [Seed 官方模型索引](https://seed.bytedance.com/en/models?view_from=homepage_tab)
- [Seed1.5-VL Tech Blog（同代支线背景）](https://seed.bytedance.com/en/blog/first-release-of-seed-vlm-tech-report-comprehensive-solutions-for-image-video-gui-and-game)
- [[src/Official Source|本地来源索引]]
