---
title: "StepFun-Prover Preview: Let's Think and Verify Step by Step"
type: paper
authors: ["Shijie Shang", "Ruosi Wan", "Yue Peng", "Yutong Wu", "Xiong-hui Chen", "Jie Yan", "Xiangyu Zhang"]
year: 2025
venue: arXiv
arxiv: "2507.20199"
tags: [paper, rl, theorem-proving, lean4, tool-use]
topic: "13_base_model"
status: read
rating: 5
created: 2026-06-12
related: []
---

> [!tldr]
> StepFun-Prover 通过 RL 训练让模型自主决定何时停止使用 Lean 4 REPL 工具，实现"像人类一样边想边验证"。32B 模型在 miniF2F-test 达到 70.0% Pass@1，超越所有 671B/72B 模型。核心创新：cold-start SFT → 动态数据过滤 RL → GRPO。

## 问题与动机

现有形式定理证明方法的 sample 效率极低：scaling from 32→64 次 sampling 仅提升 3-4% accuracy。这说明存在系统性错误模式——传统方法无法利用 Lean 4 反馈，因为采用人类预定义的固定推理模式。

核心问题：**形式定理证明器能否自我进化出适合的模式来思考、与形式验证器交互、高效推导证明？**

## 方法核心

### 工具集成推理框架

模型在生成最终答案前，交织使用：
- 自然语言推理（think）
- Lean 4 代码片段（interact）
- Lean 4 REPL 实时反馈（verify）

### 训练流水线

1. **Cold-start SFT**：建立基础环境交互模式，包括 REPL 格式和交互规范
2. **动态数据过滤**：在 RL 训练循环内过滤数据——用 RL 中期模型筛选成功率为 (0,1) 的题目（去除 trivial 和当前不可解的）
3. **GRPO RL**：multi-turn tool interaction，使用 Lean 4 REPL 验证作为 reward

### Lean4-REPL Remote Server 优化

实现 10x 加速，使多轮 RL 可行：
- 修改 Lean4-REPL 内存回收，减少重启频率
- 全面的 REPL 返回类型处理
- LLM 输出流式输入 + 异步提交
- Redis Producer-Broker-Consumer 模式，1000+ 并发进程

## 关键实验数据

| Model | Size | Pass@1 (miniF2F) |
|-------|------|-----------------|
| DeepSeek-Prover-V2 | 7B | 58.6% |
| DeepSeek-Prover-V2 | 671B | 61.9% |
| Kimina-Prover | 8B | 61.1% |
| Kimina-Prover | 72B | 63.9% |
| **StepFun-Prover-Preview** | **7B** | **66.0%** |
| **StepFun-Prover-Preview** | **32B** | **70.0%** |

### Generation Length Scaling (32B)

| Max Length | Pass@1 |
|------------|--------|
| 4,096 | 58.3% |
| 8,192 | 66.5% |
| 12,288 | 68.9% |
| 16,384 | 69.9% |
| 20,480 | 70.0% |

> [!insight]
> 7B 模型已超越 DeepSeek-Prover-V2-671B（66.0% vs 61.9%）——这不是参数量的胜利，而是工具集成推理范式的胜利。模型自主决定停止工具使用的时机，减少了无效 sampling。

## 研究启发

1. **多轮交互比大量单轮 sampling 更高效**：Prover 的 REPL 交互分布显示很多正确证明是通过多轮反馈后得到的
2. **动态数据过滤比静态过滤更有效**：in-RL filtering 能找到"对当前模型偏难但可提升"的题目
3. **冷启动 SFT 为 RL 提供基础交互模式**：没有 SFT，RL 难以学到正确的 REPL 使用规范
4. **基础设施优化直接决定算法可行性**：Lean4-RS 10x 加速使 multi-turn RL 从不可行变为可行
