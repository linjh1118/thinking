---
title: "Meituan LongCat Series MOC — 美团 LongCat 全系列技术报告"
type: moc
tags: [moc, base-model, meituan, longcat, moe, agentic, multimodal]
created: 2026-07-01
updated: 2026-07-01
---

# Meituan LongCat Series MOC

> 📚 **时间窗口**: 2025-09 至 2026-03
> **来源**: arXiv 官方技术报告（全部 7 篇均含 LaTeX 源码）
> **基座统一**: 全系列基于 560B MoE（28 层，平均激活 27B，ScMoE + Zero-Computation Experts）
> **上级 MOC**: [[Topics/13_base_model/Base Model MOC|Base Model MOC]]

---

## TL;DR

美团 LongCat 是 2025-2026 年国产开源大模型里 **路线最清晰、技术报告粒度最细** 的系列之一：**一个 560B MoE 基座**（LongCat-Flash，2509.01322）+ 沿 six 不同方向的扩展（reasoning / small / omni / native multimodal / formal / prover / next-gen）。所有扩展都在原基座架构上做，没有推倒重来。三个值得记的研究价值锚点：

1. **架构基座（Flash）**：Zero-Computation Experts（动态计算预算）+ ScMoE（跨层 shortcut 拉 overlap 窗口）——把 comm 占比从 25.3% 压到 8.4%，TPOT 比 DeepSeek-V3 理论极限再降 50%。
2. **路线分歧点**：Flash-Omni（2511）走 encoder-decoder 拼接式 omni；LongCat-Next（2603.27538）走 DiNA 原生离散 token 统一式 omni。**后者是美团的下一代押注**。
3. **意外发现**：Flash-Lite（2601.21204）证明 **scaling embedding > scaling experts**——在小基座 regime（≤10B activated），把参数投到 N-gram Embedding 比堆专家数更划算，这是 scaling law 类的方法论贡献。

---

## 系列全景图

```
                  LongCat-Flash (560B MoE 基座, 2509.01322)
                            ↓ 继承架构
        ┌──────────┬──────────┬──────────┬──────────┬──────────┐
        ↓          ↓          ↓          ↓          ↓          ↓
   Flash-     Flash-      Lite     Flash-      Flash-     LongCat-
   Thinking   Thinking             Omni        Prover     Next
   (2509)     -2601                (2511)     (2603)      (2603)
   推理 RL    推理+agent             全模态     形式化     原生离散
              升级                  实时交互    Lean4      统一 token
```

---

## 论文清单（按时间线）

| 月份 | 模型 | arXiv ID | 类型 | 参数规模 | 核心贡献 | 笔记 |
|------|------|----------|------|----------|----------|------|
| 2025-09 | **LongCat-Flash** | 2509.01322 | LLM 基座 | 560B / 27B avg | Zero-Comp Experts + ScMoE + 稳定训练套件 | [[LongCat-Flash-Technical-Report]] |
| 2025-09 | **LongCat-Flash-Thinking** | 2509.18883 | Reasoning | 560B / 27B | 长 CoT cold-start + Domain-Parallel RL + DORA 异步系统 | [[Introducing-LongCat-Flash-Thinking-A-Technical-Report]] |
| 2025-11 | **LongCat-Flash-Omni** | 2511.00279 | 全模态 | 560B / 27B + 三个轻量模块 | 实时 audio-visual 交互，端到端 <100ms | [[LongCat-Flash-Omni-Technical-Report]] |
| 2026-01 | **LongCat-Flash-Thinking-2601** | 2601.16725 | Reasoning 升级 | 560B / 27B | Environment Scaling + Robust RL + Heavy Mode + 1M context | [[LongCat-Flash-Thinking-2601-Technical-Report]] |
| 2026-01 | **LongCat-Flash-Lite** | 2601.21204 | 小基座 | 68.5B / 3B avg | Scaling Embeddings > Scaling Experts（N-gram Embedding scaling law） | [[Scaling-Embeddings-Outperforms-Scaling-Experts-in-Language-M]] |
| 2026-03 | **LongCat-Flash-Prover** | 2603.21065 | 形式化推理 | 560B / 27B | Lean4 proving SOTA (MiniF2F 97.1%) + HisPO + Auto-formalization | [[LongCat-Flash-Prover-Advancing-Native-Formal-Reasoning-via-A]] |
| 2026-03 | **LongCat-Next** | 2603.27538 | 下一代范式 | (size varies) | DiNA + dNaViT，把 text/vision/audio 统一成离散 token 自回归 | [[LongCat-Next-Lexicalizing-Modalities-as-Discrete-Tokens]] |

> 注：本 MOC 收录的是 **base model 路线 + Prover**（用户指定 7 篇）。LongCat 系列另有 Image (2512.07584) / Video (2510.22200) / Audio-Codec (2510.15227) / AudioDiT (2603.29339) / Video-Avatar 1.5 (2605.26486) 等生成模型与组件，不在本 MOC 范围。

---

## 三条主线判断

### 主线 1：架构基座稳定，能力横向扩展

LongCat 系列的 7 篇技术报告全部基于同一套 560B MoE 基座（28 层 / 512 FFN experts + 256 zero-comp experts / 12 activated / ScMoE + MLA + variance alignment）。**没有任何一篇推倒重做架构**，扩展都通过：

- **训练后 recipe 扩展**：Thinking 加 RL，Thinking-2601 加 Robust RL，Prover 加 tool-integrated RL
- **模态模块挂载**：Omni 在基座外加 ViT 637M + Audio Encoder/Decoder ~1.2B
- **token 化方案替换**：LongCat-Next 把所有模态离散化进共享 codebook（基座架构不变，只换 tokenizer）

这条路线的选择有得有失：**得**在工程效率高、复用充分；**失**在 LongCat-Next 想推原生离散多模态时，基座的 continuous embedding 假设反而成了束缚。

### 主线 2：从 thinking 到 agentic 到 formal——RL recipe 的三段进化

| 阶段 | 论文 | RL 核心 | 关键技术 |
|------|------|---------|---------|
| 思维链 | Flash-Thinking (2509) | Domain-Parallel RL + Fusion | DORA 异步系统、3× 加速 |
| Agent 工具 | Thinking-2601 (2601) | Robust RL with Noise | Environment Scaling、Heavy Mode |
| 形式化验证 | Flash-Prover (2603) | Tool-Integrated RL | HisPO、AST-based legality detection |

每一步 RL recipe 都更复杂——从单 domain 到多 domain 并行，到 noise-aware robust，到 tool-augmented hierarchical importance sampling。**这条进化路径本身就是工业级 RL 训练 base model 的教科书案例。**

### 主线 3：Omni 路线的范式分歧（**最值得追踪**）

Flash-Omni（2511）vs. LongCat-Next（2603）代表了全模态建模的两种范式：

| 维度 | Flash-Omni（拼接式） | LongCat-Next（原生统一） |
|------|---------------------|------------------------|
| 模态表示 | text 离散 + vision/audio continuous embedding | 全部离散 token（共享 codebook） |
| 架构 | 基座 LLM + 挂载 ViT/Audio enc-dec | 单一 decoder-only MoE，modality-agnostic |
| 视觉编码 | continuous ViT feature | dNaViT: SAE + 8 级 RVQ 离散化 |
| 训练目标 | LM loss + 多模态对齐 loss | 统一 NTP（next-token prediction） |
| 性能 | OmniBench 61.38，端到端 <100ms 实时 | OCRBench 858 / MMMU 58.0，discrete vs continuous gap ≤1% |
| 风险 | encoder-decoder 拼接效率天花板 | discrete 性能上限长期存疑（论文试图证伪） |

**判断**：LongCat-Next 是工业界第一次用 ~300B 训练量把 discrete vs continuous 多模态 gap 压到 1% 以内。如果结论稳固，**下一代 any-to-any 模型会大规模转向 native discrete 路线**。

---

## 系列横向对比

### 性能定位（同一基座，不同方向）

| 模型 | 定位 | 关键 benchmark | 数字 | 对标 |
|------|------|---------------|------|------|
| Flash | Non-thinking 基座 | MMLU-Pro / SuperGPQA | 70.3 / 52.0 | DeepSeek-V3.1 / Kimi-K2 |
| Flash-Thinking | Reasoning | AIME-25 / MiniF2F pass@1 | 90.6 / 67.6 | DeepSeek-V3.1-Thinking |
| Thinking-2601 | Reasoning + Agent | BrowseComp / τ²-Noise | 73.1 / 67.1 | GPT-5.2 |
| Flash-Lite | Small | τ²-Telecom / BBH | 72.8 / (?) | Qwen3-Next / Gemini-2.5-Flash-Lite |
| Flash-Omni | 实时全模态 | OmniBench / 首包延迟 | 61.4 / <100ms | Qwen3-Omni |
| LongCat-Next | 原生多模态 | MMMU / MathVista | 58.0 / 83.1 | Qwen3-VL-A3B（continuous） |
| Flash-Prover | 形式化 | MiniF2F-Test / ProverBench | 97.1% / 70.8% | Goedel-Prover-V2 / DeepSeek-Prover-V2 |

### 架构与训练资源

| 模型 | 总/激活参数 | 训练规模 | 关键架构创新 |
|------|------------|---------|------------|
| Flash | 560B / 27B avg | 20T tokens / 30 天 | Zero-Comp Experts + ScMoE + Variance Alignment |
| Flash-Thinking | 560B / 27B | RL 投入近 20% pre-training compute | Domain-Parallel RL + DORA |
| Thinking-2601 | 560B / 27B | (未公开) | ZigZag Attention（50% 层 SSA）+ 1M context |
| Flash-Lite | 68.5B / 3B avg | (未公开) | N-gram Embedding Scaling（参数占比 46%） |
| Flash-Omni | 560B + ~1.8B 模态模块 | Stage 0 ~16T + Stage 1-5 ~11T | MDP 训练（>90% text-only throughput）|
| LongCat-Next | (单模态各 size，跨模态 ~300B 训练量) | ~300B 训练量 | DiNA + dNaViT（SAE + 8 级 RVQ）|
| Flash-Prover | 560B / 27B | (未公开) | HisPO + AST-based legality detection |

---

## 开放问题

1. **Zero-Computation Experts 的最优比例**：Flash 用 Z=256 / N=512（比例 1:2），这个比例的 ablation 没给。是否随规模变化？
2. **LongCat-Next 的 discrete 范式在大规模（560B+）下是否仍成立**：当前证据只在 ~300B 训练量上。
3. **ScMoE + SBO 推理优化的硬件依赖**：DeepEP / NVLink Sharp / RDMA 都是 H800 假设，迁移到国产卡（如昇腾）效果未知。
4. **Flash-Lite 的 NE 路线在 >10B activated 规模是否仍 Pareto 最优**：论文显示宽度效应——1.3B 上 NE 仍优势，但更大规模未验证。
5. **DORA 系统的工程开源**：论文给数据但代码未完全开源，复现 >3× 加速的细节（graph-level compilation、staleness 配置）需要社区跟进。
6. **Omni → Next 的迁移路径**：现有 Flash-Omni 用户能否平滑迁到 LongCat-Next，还是需要从头重训？

---

## 关联主题

- [[Topics/13_base_model/Base Model MOC|Base Model MOC]] — 全 vault 大模型基座全景
- [[Topics/13_base_model/Base_Model_Insight|Base Model Insight]] — 数据/架构/训练策略深度分析
- [[Topics/13_base_model/Base_Model_Architecture_Comparison|架构对比]] — 与其他 MoE 模型对比
- [[Topics/13_base_model/Base_Model_RL_Comparison|RL 对比]] — 与其他 reasoning RL 工作对比

---

## 外部链接

- LongCat Chat: https://longcat.ai
- HuggingFace: https://huggingface.co/meituan-longcat
- GitHub: https://github.com/meituan-longcat
- LongCat-2.0（HF 模型卡，1.6T MoE / 48B activated / 1M context，arXiv ID 暂无）
