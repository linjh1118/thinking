---
title: "GLM-4.5V and GLM-4.1V-Thinking: Towards Versatile Multimodal Reasoning with Scalable Reinforcement Learning"
type: paper
authors: ["GLM-V Team", "Wenyi Hong", "Xiaotao Gu", "Jie Tang", "et al."]
year: 2025
venue: arXiv
arxiv: "2507.01006"
url: "https://arxiv.org/abs/2507.01006"
tags: [paper, glm, multimodal, vlm, reinforcement-learning]
topic: "13_base_model"
status: read
rating: 4
created: 2026-05-30
---

# TL;DR

GLM-4.5V 是一个开源多模态 VLM 家族（9B/106B-A12B），通过 **RLCS（Reinforcement Learning with Curriculum Sampling）** 训练框架在 42 个 benchmark 上达到开源同尺寸 SOTA，尤其在 GUI Agent 和 Coding 任务上可比 Gemini-2.5-Flash；小模型 GLM-4.1V-9B 在 29 个 benchmark 上超越 Qwen2.5-VL-72B。

## 问题与动机

多模态任务（STEM、视频、GUI Agent、OCR 等）对 VLM 的推理能力要求已远超简单视觉感知，现有开源社区缺乏能在广泛场景一致超越同尺寸非-thinking 模型的多模态推理模型。核心挑战是：**如何将 LLM 端 Scalable RL 的成功范式迁移到 VLM 端**，实现跨领域推理能力的系统性提升。

## 方法核心思路

### 1. 视觉基础模型预训练
构建大规模图文预训练 corpus，包含：
- 精准事实知识的大规模图文对
- 自整理的交错图像-文本学术语料
- 标注的文档图表、教学视频、自然/合成图像的 grounding 数据

### 2. SFT Cold-Start
构造跨领域 domain-specific SFT 数据集，教会模型标准化格式的推理过程。

### 3. RLCS（核心创新）
**Reinforcement Learning with Curriculum Sampling** 结合了课程学习和难度感知采样：
- 离线评估：用多个 VLM 或 RL checkpoint 做 pass@k 打分，结合人工标注，将样本分为多个难度等级
- 在线评估：每次 rollout 记录 pass@k 结果，合并到离线难度标签
- 自适应采样：根据模型当前能力动态调整各难度等级的采样比例，优先选中间难度样本
- **动态采样扩展 via Ratio EMA**：解决 GRPO 中 all-correct/incorrect batch 造成的有效 batch size 波动问题，通过 expansion_ratio_ema 维持训练稳定性

### 4. 训练 tricks
- **Force Answering**：当 thinking 过长被截断时，插入 `</think>` token 强制输出答案并给予公平 reward，支持动态控制推理预算
- **Discard KL Loss**：VLM 在 RL 过程中 KL 散度上升更快，加 KL loss 会明显限制能力
- **Clip-Higher**：提高 importance sampling ratio 的上界，防止 entropy collapse
- **top-p=1**：比降低 top-p 更稳定，避免 rare token under-learning 导致的乱码
- **Per-sample loss computation**：比 per-token 方式训练更稳定

### 5. Cross-Domain Generalization
跨领域 RL 训练发现：**在一个领域训练会 boost 其他领域性能**，且 joint training 效果最好。GUI Agent 数据因其综合了文本识别、视觉 grounding 和逻辑推理需求，是最强 cross-domain transfer 信号。

## 关键结果

| Benchmark | GLM-4.5V-Thinking | Qwen2.5-VL-72B |
|-----------|-------------------|----------------|
| MMBench v1.1 | 88.2 | - |
| MMStar | 75.3 | 70.8 |
| MMMU Pro | SOTA | - |
| MathVista | SOTA | 74.8 |
| ChartQAPro | SOTA | - |
| MMLongBench-Doc | SOTA | - |
| OSWorld (GUI Agent) | 显著超越开源 | - |
| Design2Code | 显著超越开源 | - |
| GLM-4.1V-9B vs Qwen2.5-VL-72B | 29/42 benchmark 胜出 | - |

GLM-4.5V 在 42 个 public benchmark 上全面超越同尺寸开源模型，在 22 个 benchmark 上可比/超越 Gemini-2.5-Flash。

## 基础设施

- **Sequence Packing + Gradient Accumulation**：将多个 sample 打包到固定 32K context，减少 padding
- **Load Balancing across DP Ranks**：rollout 后按序列长度 balance 到各 rank，最大化 throughput
- **intra-rank 优化**：结合 packing 和梯度累积，半减 forward-backward 时间

## 对研究的启发

> [!insight]
> 1. **RLCS 课程采样是关键**：不是简单混合多领域数据，而是根据模型当前能力动态筛选"最 informative"样本，这是 RL 在 VLM 端成功的核心工程 trick
> 2. **Cross-domain Transfer 比预期强**：视觉理解/文本识别/推理能力在不同领域间共享底层能力，一个领域的 RL 信号能广泛迁移。这对 GUI Agent 的 RL 训练是重要参考——用 OCR/STEM 数据辅助 GUI Agent 训练是可行的
> 3. **Force Answering trick**：支持动态控制推理预算，对 GUI Agent 这种需要平衡深度推理和效率的场景很有价值
> 4. **VLM 的 RL 不需要 KL loss**：与 LLM RL 不同，VLM 的 KL 散度上升更快，加 KL loss 会限制能力

## 相关链接
- 论文: [arXiv 2507.01006](https://arxiv.org/abs/2507.01006)
- 源码: [github.com/zai-org/GLM-V](https://github.com/zai-org/GLM-V)
