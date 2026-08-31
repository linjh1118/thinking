---
title: "GLM-4.5: Agentic, Reasoning, and Coding (ARC) Foundation Models"
type: paper
authors: ["GLM-4.5 Team", "Aohan Zeng", "Qinkai Zheng", "Xiaotao Gu", "Jie Tang", "et al."]
year: 2025
venue: arXiv
arxiv: "2508.06471"
url: "https://arxiv.org/abs/2508.06471"
tags: [paper, glm, foundation-model, reasoning, agentic, coding]
topic: "13_base_model"
status: read
rating: 4
created: 2026-05-30
---

# TL;DR

GLM-4.5 是一个 355B 总参数/32B 激活参数的 MoE 开源模型，支持 thinking 和 direct response 双模式，在 Agentic/Reasoning/Coding (ARC) 任务上达到顶尖水平：TAU-Bench 70.1%、AIME 24 91.0%、SWE-bench Verified 64.2%，综合排名第3、Agentic 第2，且使用远少于竞品的参数。

## 问题与动机

当前旗舰 LLM（如 o3、Claude Opus 4、Gemini 2.5 Pro）在 ARC 任务上已展示强能力，但闭源和高昂推理成本限制研究社区跟进。核心挑战是：**如何在远少参数下（355B vs 671B+）实现同等的 Agentic/Reaoning/Coding 能力**，并同时支持 hybrid reasoning 模式（快慢思考切换）。

## 方法核心思路

### Architecture
- MoE with loss-free balance routing + sigmoid gates
- 与 DeepSeek-V3/Kimi K2 的关键区别：**减少 width（hidden dim / experts 数），增加 depth（layers）**，实验发现更深模型在推理 benchmark 上更好
- 96 attention heads（5120 hidden dim），比更少 heads 的同训练 loss 模型在 MMLU/BBH 上表现更好
- QK-Norm 稳定 attention logits 范围
- MTP layer 作为额外 MoE layer，支持 speculative decoding

### Pre-Training (23T tokens)
- **Web**：Nemotron-CC 风格按 quality score 分桶，过采样高质量桶，最高桶贡献 3.2 epochs；SemDedup 去除模板生成的相似网页
- **Multilingual**：Fineweb-2 + 质量分类器 up-sample 高教育价值文档
- **Code**：Fill-In-the-Middle 目标；语言特定质量模型分三层
- **Math & Science**：LLM 打分 + 小规模分类器预测

### Mid-Training（推理/Agent 能力 boost）
1. **Repo-level Code Training**：拼接同仓库代码文件，学习跨文件依赖；32K context
2. **Synthetic Reasoning Data**：数学/科学/代码竞赛的合成推理过程
3. **Long-context & Agent**：128K context + 大规模合成 agent 轨迹

### Post-Training: Expert Model Iteration

#### Stage 1: Expert Training
三个独立 Expert Model（Reasoning / Agent / General chat），各自经过 SFT cold-start + RL。

#### Stage 2: Unified Training
自蒸馏将多 expert 能力整合为单一 hybrid model（同时支持 thinking 和 direct response 模式）。

#### 关键 SFT 发现
- **Rejection Sampling 多阶段过滤**：去重复/截断 + 客观题验证 + 主观题 reward model + tool call 轨迹验证
- **Prompt 选择 + Response-level Scaling**：过滤 bottom 50% 短响应 prompt，数学/科学任务提升 2-4%；每个 hard prompt 生成 4 个 response 再提升 1-2%
- **Function Call XML 模板**：减少代码中的字符转义负担，提升 agent 能力

### Reasoning RL

**Difficulty-based Curriculum**：两阶段难度课程，第二阶段切换到极难题目（pass@8=0, pass@512>0），持续提升。

**Single-Stage RL at 64K Output Length**：与渐进增加输出长度不同，直接在 64K 训练更好，因为 SFT 已让模型习惯 64K 响应，引入短阶段会让模型"unlearn"长上下文能力。

**Token-weighted Mean Loss**：对 code RL 比 sequence-mean loss 收敛更快，抑制"base case"重复生成。

**Science RL**：只用 expert-verified 多选题比混合质量数据效果好很多。

### Agentic RL

- **BrowseComp 数据合成**：知识图谱多跳推理 + human-in-the-loop 网页内容抽取
- **SWE 数据**：GitHub PR/issue + 分布式沙箱测试
- **Group-wise Policy Optimization**：每个 problem 采样 K 个 agent trace，以 mean reward 为 baseline
- **Iterative Self-distillation**：RL 提升 → self-distillation → 再 RL，逐阶段提升
- **Interaction Turns Scaling**：agent 任务通过增加环境交互轮数 scaling test-time compute

### General RL
- **Holistic RL**：5000 prompts × 7 primary / 33 secondary / 139 tertiary categories
- **Instruction Following RL**：7 major + 151 minor constraint types，配规则验证 + reward model + critique model
- **Function Calling RL**：step-wise rule-based + end-to-end multi-turn RL
- **Pathology RL**：专门针对语言混合/重复/格式错误，数据构建用高度触发这些问题的 prompt

### RL Infrastructure (Slime)
- **Flexible Hybrid Training**：同步（数学/代码）和异步（Agent SWE）两种模式
- **FP8 Rollout**：BF16 训练 + FP8 在线量化 rollout，加速数据生成
- **异步 Agent 训练**：Docker 隔离环境 + 独立 rollout/training GPU 调度

## 关键结果

### ARC 任务

| Benchmark | GLM-4.5 | o3 | Claude Opus 4 | Gemini 2.5 Pro |
|-----------|----------|-----|--------------|----------------|
| TAU-Bench | **70.1** | - | - | - |
| AIME 24 | **91.0** | 90.3 | 75.7 | 88.7 |
| SWE-bench Verified | 64.2 | 69.1 | 67.8 | 49.0 |
| MMLU-Pro | 84.6 | 85.3 | 87.3 | 86.2 |
| SciCode | 41.7 | 41.0 | 39.8 | 42.8 |
| BFCL V3 | **77.8** | - | - | - |

### 翻译任务（超越专用 MT 模型）
| Model | Score (0-3) |
|-------|------------|
| GLM-4.5 | **1.71** |
| Qwen-MT-plus | 0.38 |
| Seed-X | 0.65 |

### Coding Agent (CC-Bench)
- GLM-4.5 vs Claude Sonnet 4: 40.4% win, 9.6% tie, 50.0% loss
- GLM-4.5 vs Kimi K2: 53.9% win, 17.3% tie, 28.8% loss
- Tool calling success rate: **90.6%** (最高)

## 对研究的启发

> [!insight]
> 1. **更深 MoE 比更宽更利于推理**：这对设计 GUI Agent backbone 有直接参考——在预算固定时，优先增加 depth
> 2. **Hybrid thinking 模式** 是平衡深度推理和效率的正确方向，GLM-4.5 的 unified training 自蒸馏策略值得借鉴
> 3. **难度课程两阶段设计**：第二阶段直接上极难题（pass@8=0 但 pass@512>0）比渐进增加难度更有效，说明模型需要"stretch its limits"
> 4. **Agentic RL 的 iterative self-distillation** 解决了 RL 训练耗时的痛点——用 RL 提升的模型作为更好的 SFT teacher 再 RL
> 5. **CC-Bench 90.6% tool calling 成功率** 说明 GLM-4.5 的 function calling 能力很强，对 GUI Agent 的 tool-use 能力有参考价值

## 相关链接
- 论文: [arXiv 2508.06471](https://arxiv.org/abs/2508.06471)
- 源码: [github.com/zai-org/GLM-4.5](https://github.com/zai-org/GLM-4.5)
