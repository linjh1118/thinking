---
title: "Base Model 训练 Token 量级全览"
type: insight
tags: [insight, base-model, pretraining, post-training, token-scale, sft, rl]
source: "[[Topics/13_base_model/Base Model MOC]]"
related:
  - "[[Topics/13_base_model/Base_Model_Pretraining_Comparison]]"
  - "[[Topics/13_base_model/Base_Model_Architecture_Comparison]]"
  - "[[Topics/13_base_model/Base_Model_RL_Comparison]]"
created: 2026-07-03
updated: 2026-07-03
---

# Base Model 训练 Token 量级全览

> [!tldr]
> 预训练 token 量决定模型能力上限（15T-100T 量级），Post-training 只是精细调优（通常 < 1% 预训练量）。120B math token 是 DeepSeekMath 从 Common Crawl 几十T 网页中精选出的高质量数学子集，约等于 MiMo-7B 全部 25T 的 0.5%。Post-training 分 SFT（5B-60B tokens）和 RL（1B-10B tokens），核心在于数据质量而非数量。

---

## 一、预训练 Token 量级对比

### 各模型预训练 Token 总览

| 模型 | 预训练 Token 总数 | 架构 | 备注 |
|------|-------------------|------|------|
| **DeepSeekMath** | **120B** math tokens | Dense 7B | ⚠️ 纯数学精选子集，非全语料 |
| **LongCat Flash** | ~20T | Dense | 美团 Dense 模型 |
| **Step 3.5 Flash** | 17.2T | MoE | 阶跃函数，全程无 loss spike |
| **Kimi K2** | ~15.5T | MoE 1.04T/32B active | Rephrasing 增强 token utility |
| **GLM-4.5** | 15T + 7T = **~22T** | MoE | 通用 + 代码/推理分段 |
| **MiMo-7B (Dense)** | 25T | Dense 7B | 三阶段递进 reasoning density |
| **MiMo-V2-Flash** | 27T | MoE 309B/15B active | 三阶段（通用→代码→长上下文） |
| **Qwen3** | 36T | Dense/MoE | 三阶段预训练 |
| **MiMo-V2.5 / V2.5-Pro** | 27T (Base) / 48T (Total) | MoE 310B/15B active | 五阶段含多模态 |
| **MiniMax M3** | **~100T**（估） | MoE | 官方强调"比预期更多 interleaved data" |

---

## 二、预训练分阶段 Token 分配

### MiMo-7B (Dense, 25T Total)

| 阶段 | Context | Token 范围 | 关键动作 |
|------|---------|-----------|---------|
| **Stage 1** | 8K | 初始 | 均衡 diverse corpus，降采样广告/新闻/招聘 |
| **Stage 2** | 8K | 逐步到 ~25T | Math/Code 提升到 ~70%，提高推理密度 |
| **Stage 3** | 32K | 末期 ~10% | ~10% synthetic reasoning responses，扩展上下文 |

> 三阶段核心：**reasoning density 随训练推进逐步提升**，而非从头就全上高推理数据。

### MiMo-V2-Flash (MoE, 27T Base)

| 阶段 | Context | Token 范围 | 关键动作 |
|------|---------|-----------|---------|
| **Stage 1** | 32K | 0-22T (81%) | 通用语料打底 |
| **Stage 2** | 32K | 22-26T (15%) | 代码上采样 + 5% 合成推理数据 |
| **Stage 3** | 256K | 26-27T (4%) | 上下文扩展到 256K，长依赖数据上采样 |

**MTP loss weight**：Stage 1 用 0.3（强辅助），Stage 2/3 用 0.1（弱化）。

### MiMo-V2.5 (MoE, 48T Total)

| 阶段 | Token 范围 | 关键动作 |
|------|-----------|---------|
| **Stage 1: Text Pretraining** | 前期大部分 | Diverse corpora → LLM backbone |
| **Stage 2: Projector Warmup** | 中期 | Align audio/visual projectors with LLM |
| **Stage 3: Multimodal Pretraining** | 大规模 | High-quality cross-modal data at scale |
| **Stage 4: SFT + Agentic Post-Training** | 渐进扩展 | Progressively extend context: 32K → 256K → 1M |
| **Stage 5: RL + MOPD** | 末期 | Further strengthen perception, reasoning, agentic |

> V2.5 比 V2-Flash 多两个多模态专属阶段 + 独立 RL 阶段。

### GLM-4.5 (MoE, ~23T)

| 阶段 | Token 范围 | 关键动作 |
|------|-----------|---------|
| **Pre-training** | 15T | General pre-training corpus |
| **Mid-training** | +7T | Code & reasoning corpus 专项加强 |
| **Post-training** | - | Repo-level code、synthetic reasoning、128K agent trajectories |

> GLM-4.5 特色：**Mid-training 概念**——不是全部 pretrain 完再做专项，而是在 pretrain 途中插入 code/reasoning 专项阶段。

### LongCat Flash Omni (多模态)

| 阶段 | Token 范围 | 关键动作 |
|------|-----------|---------|
| **Stage 0** | ~16T | 文本基座，逐步加 STEM/code 比例 |
| **Stage 1** | 5.1T (text:audio = 2:1) | 语音-文本对齐，4 个 audio prediction heads |
| **Stage 3** | 0.33T | Video、OCR、grounding、GUI；**PPL-gap signal** 自动调采样权重 |
| **Stage 4** | 120B (8K→32K) + 20B (32K→128K) | RoPE base 1M→5M→10M，逐步扩展上下文 |

### Kimi K2 (MoE)

| 阶段 | 特点 | 关键动作 |
|------|------|---------|
| **Knowledge Data Rephrasing** | 10× rephrasing + 1 epoch | 将知识数据重复暴露多次而不导致过拟合（SimpleQA 23.76%→28.94%） |
| **Mathematics Rephrasing** | 翻译 + 改写 | 将数学文档改写为"学习笔记"风格 |

> Kimi K2 特色：**Rephrasing 增强 token utility**——不是增加数据量，而是让同一批数据被模型"看"得更有效。

### Step 3.5 Flash (MoE, 17.2T)

| 阶段 | Token 范围 | 关键动作 |
|------|-----------|---------|
| **Pretraining** | 17.2T | MTP-3, head-wise gating，全程无 loss spike |
| **SFT** | 7.23B tokens (871k samples) | 多领域统一 SFT（Math/Code/STEM/Logic/Agent/Long Context） |

---

## 三、阶段划分的普遍规律

| 规律 | 代表模型 |
|------|---------|
| **2-3 阶段最常见** | MiMo-7B、V2-Flash、LongCat Flash、Qwen3 |
| **4-5 阶段 = 加多模态** | MiMo-V2.5（+Projector +Multimodal +RL）、LongCat Flash Omni（+Audio +Video +Context） |
| **Mid-training 插入专项** | GLM-4.5（通用中途插 code/reasoning）、LongCat Flash Thinking（通用中途插 agentic） |
| **Post-training = RL 阶段** | MiMo-V2.5（Stage 5: RL + MOPD）、Qwen3（推理RL → 模式融合 → 蒸馏） |
| **SFT 独立阶段** | Step 3.5 Flash（pretrain 后独立 SFT）、MiMo-V2.5（Stage 4 含 SFT） |

---

## 四、Post-Training Token 量级

> **核心结论**：Post-training token 量远小于预训练，通常是 **5B-60B tokens**（SFT）和 **1B-10B tokens**（RL），仅占预训练的 **0.01%-0.5%**。

### 各模型 Post-Training 数据量

| 模型 | SFT | RL | 特点 |
|------|-----|-----|------|
| **MiMo-7B** | - | 130K 可验证问题（~1-5B tokens） | 100K 数学 + 30K 代码；Rule-based reward |
| **Step 3.5 Flash** | 871K samples, **7.23B tokens** | 700 iterations | 两阶段课程（250 + 450） |
| **PaCoRe (8B)** | 10.2M samples, **61.1B tokens** | 700 iterations | 数学/代码/科学/工具调用/逻辑/创意 |
| **Kimi K2** | 大规模（未公开量） | 大规模 agentic 数据合成 | 强调"大规模"但未披露具体数字 |
| **Kimi Linear** | Multi-stage SFT（未公开量） | RL with PTX loss | 具体量未公开 |
| **MiMo-V2.5-Pro** | 基础 instruction following（未公开量） | 分域 RL + MOPD | 三阶段：SFT → Domain RL → MOPD |

### 经验规律

| 阶段 | 典型 Token 量 | 占预训练比例 |
|------|--------------|-------------|
| **预训练** | 15T - 48T | 100% |
| **SFT** | 5B - 60B | **~0.1% - 0.4%** |
| **RL (rollout)** | 1B - 10B | **~0.01% - 0.07%** |

---

## 五、120B Math Token 的直观理解

### 与书籍对比

| 参考物 | 估算 Token 数 | 120B token ≈ |
|--------|-------------|--------------|
| 一本 200 页的数学/CS 英文教材 | ~150,000 tokens | **约 80 万本** |
| 一本 100 页的短教材 | ~75,000 tokens | **约 160 万本** |
| 《Concrete Mathematics》全书 | ~200,000 tokens | **约 60 万本** |

> 相当于 6-16 个普通高校数学图书馆（每馆约 10 万册）。

### 与 QA 对比

| 参考物 | 估算 Token 数 | 120B token ≈ |
|--------|-------------|--------------|
| 一道中等难度数学题（含详细推理步骤） | ~500 tokens | **约 2.4 亿道题** |
| 一道竞赛数学题（含多步证明） | ~1,000 tokens | **约 1.2 亿道题** |
| 一个 math conversation（多轮对话） | ~2,000 tokens | **约 6000 万轮对话** |

### 与其他模型对比

| 对比维度 | 120B math tokens 相当于 |
|---------|----------------------|
| vs Kimi K2 全部 15.5T | 约 **0.8%** |
| vs MiMo-7B 全部 25T | 约 **0.5%** |
| vs GLM-4.5 代码段 7T | 约 **1.7%** |
| vs 全部人类数字数学资料（估 ~500B-1T） | 约 **12-24%** |

> **关键洞察**：120B 不是"很大"，而是**极其精纯**。DeepSeekMath 做了两阶段过滤（fastText 粗筛 30% 保留 + OpenAI embedding 精选），最终 120B 是从 Common Crawl 几十T 网页中筛出来的质量最高的数学子集。

---

## 六、换算速查表

```
120B tokens
├── ≈ 240 万本教材（每本 ~500K tokens）
├── ≈ 1.2 亿道数学竞赛题（每题 ~1000 tokens）
├── ≈ MiMo-7B 全部 25T 的 ~0.5%
└── ≈ 人类数学知识总库的 ~12-24%
```

---

## 七、直观类比

```
预训练 = 学"说话"（需要听几十万人说话）
Post-training = 学"演讲"（只需要几百个小时的专业演讲练习）

预训练 = 建语法库（几亿条语法规则）
Post-training = 写演讲稿（几万字就够）

预训练 = 吃遍天下美食（几十TB）
Post-training = 专攻米其林（几十GB）
```

---

## 八、方法谱系

| 技术方向 | 代表模型 | 核心机制 | 典型 Token 量 |
|---|---|---|---|
| 预训练全谱系 | MiMo-V2.5 | 五阶段（通用→多模态→SFT→上下文→RL） | 48T total |
| Mid-training 专项 | GLM-4.5 | 通用中途插 code/reasoning | ~22T |
| Rephrasing 增强 | Kimi K2 | 同一批数据多次 rephrasing | ~15.5T |
| SFT 精选 | Step 3.5 Flash | 871K 高质量多领域 SFT | 7.23B |
| 大规模 SFT | PaCoRe | 10.2M samples 多领域 | 61.1B |
| 精选数学子集 | DeepSeekMath | 两阶段过滤（fastText + embedding） | 120B math |

---

## 相关资料

- Base Model MOC：[[Topics/13_base_model/Base Model MOC]]
- 预训练对比：[[Topics/13_base_model/Base_Model_Pretraining_Comparison]]
- 架构对比：[[Topics/13_base_model/Base_Model_Architecture_Comparison]]
- RL 方法对比：[[Topics/13_base_model/Base_Model_RL_Comparison]]
