---
title: "Seed2.0 — Pro/Lite/Mini 组成的 Agent Foundation Family"
type: model-note
year: 2026
url: "https://seed.bytedance.com/en/seed2"
tags: [model-note, base-model, seed, agent-foundation, multimodal, long-horizon]
status: read
created: 2026-08-31
updated: 2026-09-01
---

# Seed2.0 — Pro/Lite/Mini 组成的 Agent Foundation Family

> [!tldr]
> Seed2.0 将“Agent Foundation Model”做成三个生产档位：Pro 负责长链推理与复杂工作流，Lite 平衡质量和速度，Mini 优化吞吐与部署密度。主线能力同时覆盖多模态、搜索、编码、GUI 和真实长程任务；4 月升级后的 Lite 进一步统一视频、图像、音频和文本理解。

![Seed2.0 官方主视觉](src/assets/hero.jpg)

## 家族不是简单尺寸缩放

| 成员 | 官方定位 | 适合工作负载 |
|---|---|---|
| Seed2.0 Pro | 长链 reasoning、复杂流程鲁棒性 | 高价值研究、专业任务、长程 Agent |
| Seed2.0 Lite | 质量—速度平衡；后续升级 omni-modal | 通用生产服务、编码和多模态应用 |
| Seed2.0 Mini | 推理吞吐与部署密度 | 高并发、批生成、成本敏感 executor |

官方没有在网页上完整公开三者参数，因此不能根据 Pro/Lite/Mini 名称猜总参数或激活参数。

## 从 benchmark 到真实工作流

Seed2.0 的评测覆盖知识、推理、指令、SearchAgent、SkillsBench、GDPval、金融、SWE-bench、Terminal-Bench、多模态与 GUI。比单项冠军更重要的是，它尝试把研究级任务、CAD 操作、生物技术支持和代码修复纳入同一 Agent family。

![Seed2.0 官方综合评测](src/assets/benchmark.jpg)

![Seed2.0 Agent 评测](src/assets/agent-evaluation.jpeg)

4 月版 Seed2.0 Lite 被官方称为 Seed 主线首个 omni-modal understanding 模型，可联合处理视频、图像、音频和文本。这种统一 observation 对长程 Agent 有价值：环境状态不必先由多个独立模型压成文本，但训练也更容易出现模态偏置和 reward 不一致。

## Agent Training 判断

> [!insight]
> Pro/Lite/Mini 最适合做“同 family 分层策略”：Pro 负责规划、困难验证与失败恢复，Lite 承担大多数交互，Mini 承担高频结构化动作。训练数据应记录何时升级模型，而不只是给每个角色固定分工。

Seed2.0 强调长程稳定性，但官网结果仍是特定 harness 下的终态指标。真正的训练审计还需要观察失败轨迹：错误来自 perception、planning、tool schema、执行器还是恢复策略。

## 资料充分度与证据边界

> [!warning]
> Seed2.0 有官方模型页、Tech Blog 和 Model Card 链接，能力与评测材料丰富；但参数、预训练 tokens、Agent RL 环境分布和 reward 细节仍未达到可复现技术报告的深度。本笔记可以做产品/训练判断，不能还原完整训练 recipe。

## 一手资料

- [Seed2.0 官方模型页](https://seed.bytedance.com/en/seed2)
- [Seed2.0 Tech Blog](https://seed.bytedance.com/en/blog/seed-2-0-official-launch)
- [Seed2.0 官方 Model Card（PDF）](https://lf3-static.bytednsdoc.com/obj/eden-cn/lapzild-tss/ljhwZthlaukjlkulzlp/seed2/seed2_model_card.pdf)
- [[../2605_Seed2_0_Model_Card/Seed2.0-Model-Card-Agent-Foundation-Model|本地 Model Card 笔记]]
- [[src/Official Source|本地来源索引]]
