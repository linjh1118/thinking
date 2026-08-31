---
title: "Xiaomi MiMo Series - Dense Notes"
type: insight
source: "[[Topics/13_base_model/Base Model MOC]]"
authors: ["Xiaomi MiMo Team"]
year: 2026
venue: arXiv / Official Blog / Hugging Face
arxiv:
doi:
url: "https://mimo.xiaomi.com/"
tags: [insight, mimo, xiaomi, base-model, reasoning, multimodal, agentic, rl-infra, moe, long-context]
topic: "13_base_model"
status: read
rating: 5
related:
  - "[[Topics/13_base_model/Xiaomi_MiMo/2505_MiMo_7B/MiMo]]"
  - "[[Topics/13_base_model/Xiaomi_MiMo/2506_MiMo_VL_7B/MiMo-VL]]"
  - "[[Topics/13_base_model/Xiaomi_MiMo/2511_MiMo_Embodied/MiMo-Embodied]]"
  - "[[Topics/13_base_model/Xiaomi_MiMo/2512_MiMo_VL_Miloco_7B/MiMo-VL-Miloco]]"
  - "[[Topics/13_base_model/Xiaomi_MiMo/2601_MiMo_V2_Flash/MiMo-V2-Flash]]"
  - "[[Topics/13_base_model/Xiaomi_MiMo/2603_MiMo_V2_Pro/MiMo-V2-Pro]]"
  - "[[Topics/13_base_model/Xiaomi_MiMo/2603_MiMo_V2_Omni/MiMo-V2-Omni]]"
  - "[[Topics/13_base_model/Xiaomi_MiMo/2604_MiMo_V2_5/MiMo-V2.5]]"
  - "[[Topics/13_base_model/Xiaomi_MiMo/2604_MiMo_V2_5_Pro/MiMo-V2.5-Pro]]"
created: 2026-06-11
updated: 2026-06-11
---

# Xiaomi MiMo Series - Dense Notes

> [!tldr]
> MiMo 系列不是简单的"7B 变 1T"故事，而是一条 agent foundation model 路线：先把可验证推理能力做进 base model，再把视觉/GUI/具身/音频接进来，最后用 MoE、Hybrid SWA、MTP 和 MOPD 解决长程 agent 的效率与多域后训练干扰。

## 一句话总判断

MiMo 的核心押注是：**强 agent 不是靠单个大模型直接混训出来，而是靠高密度预训练数据、可验证 RL、领域 teacher 分治、on-policy 蒸馏、长上下文和高效 rollout 共同堆出来。**

最值得研究者复用的不是某个 benchmark 分数，而是这四个 pattern：

1. **Reasoning first**：预训练阶段就提高 reasoning density，后训练只负责释放潜力。
2. **Grounding as transition**：GUI/具身不是只做静态定位，还要学习状态变化和动作后果。
3. **Specialize then recover**：领域 SFT 会带来遗忘，需要用 RL 或课程训练拉回泛化。
4. **Separate teachers, merge student**：多域能力先分别练 teacher，再用 MOPD 合并，避免直接混训互相伤害。

## 系列演进图

```text
MiMo-7B
  纯文本 reasoning base：25T tokens + MTP + 可验证 math/code RL
    |
MiMo-VL-7B
  视觉 + GUI grounding：2.4T 多模态预训练 + MORL
    |
MiMo-Embodied / MiMo-VL-Miloco
  领域落地：具身+驾驶课程学习；智能家居 SFT 后用 GRPO 恢复泛化
    |
MiMo-V2-Flash
  MoE agent 基座：309B/15B + Hybrid SWA + MTP + MOPD
    |
MiMo-V2-Pro / V2-Omni / V2.5 / V2.5-Pro
  1M context、全模态、开源权重、长程 tool-use 与 harness-aware agent
```

## 每篇文章速查

| 文章/模型 | 它在系列里的位置 | 关键做法 | 最重要数字 | 我的判断 |
|---|---|---|---|---|
| [[Topics/13_base_model/Xiaomi_MiMo/2505_MiMo_7B/MiMo\|MiMo-7B]] | 纯文本推理基座 | 25T tokens；三阶段数据配比；单层 MTP；130K 可验证 math/code RL；difficulty-driven code reward；Seamless Rollout Engine | AIME 2025 55.4；LiveCodeBench v5 57.8；MATH500 95.8；rollout 训练 2.29x | 证明小模型 RL 上限首先取决于 base model 的 reasoning potential，而不是只看 RL recipe |
| [[Topics/13_base_model/Xiaomi_MiMo/2506_MiMo_VL_7B/MiMo-VL\|MiMo-VL-7B]] | 把 reasoning base 接到视觉和 GUI | MiMo-7B + Qwen2.5-ViT；2.4T tokens 四阶段训练；GUI element/instruction grounding；before/after screenshot action prediction；MORL=RLVR+RLHF | MMMU 66.7；OlympiadBench 59.4；OSWorld-G SFT 54.7 / RL 56.1；ScreenSpot 87.3；ScreenSpot-v2 90.5 | 对 GUI Agent 最有价值：GUI 数据不只是截图定位，而是跨平台 action space + 状态转移建模 |
| [[Topics/13_base_model/Xiaomi_MiMo/2511_MiMo_Embodied/MiMo-Embodied\|MiMo-Embodied/XFM]] | 把 VLM 推到物理世界 | 在 MiMo-VL 上继续训；General + Embodied + Autonomous Driving；Embodied SFT -> AD SFT -> CoT -> GRPO | 17 个 embodied benchmark；12 个 AD benchmark；直接混合 59.2/55.2，多阶段 63.7/63.4；NAVSIM PDMS 86.5，+RL 91.0 | 跨域不是简单混数据，课程顺序本身就是能力；对 GUI+robotics+driving 的统一接口很有启发 |
| [[Topics/13_base_model/Xiaomi_MiMo/2512_MiMo_VL_Miloco_7B/MiMo-VL-Miloco\|MiMo-VL-Miloco]] | 智能家居领域专用版 | Home-scenario SFT；CoT annotations；token-budget-aware reasoning；再用 GRPO 针对 video、GUI、reasoning 恢复通用能力 | 活动 F1：Watch TV 98.3、Workout 96.7；手势 F1：Thumbs Up 90.5、Shaka 88.3；Video-MMMU 63.6；MMLU-Pro 68.5 | 垂直领域模型的标准生命周期：SFT 注入专用知识，RL 修复泛化损失 |
| [[Topics/13_base_model/Xiaomi_MiMo/2601_MiMo_V2_Flash/MiMo-V2-Flash\|MiMo-V2-Flash]] | 系列真正的技术转折点 | 309B total / 15B active MoE；48 层，39 SWA + 9 GA；256 experts top-8；128-token Hybrid SWA 5:1；attention sink；27T tokens；MTP；MOPD | NIAH-Multi 32K-256K 99.3/99.9/98.6/96.7；3-layer MTP 约 2.6x；SWE-Bench Verified 73.4；LongBench V2 60.6 | 最重要的论文。它把模型结构、推理加速、RL infra、多 teacher 后训练放进同一条 agent 路线 |
| [[Topics/13_base_model/Xiaomi_MiMo/2603_MiMo_V2_Pro/MiMo-V2-Pro\|MiMo-V2-Pro]] | V2-Flash 的大参数 agent 版 | >1T total / 42B active；Hybrid ratio 7:1；1M context；OpenClaw 深度集成；agent scaffold SFT/RL | ClawEval 61.5；PinchBench 81.0；Terminal-Bench 2.0 86.7；Hunter Alpha 超 1T tokens 使用 | 重点不是刷分，而是 model 与 agent scaffold co-design；但材料主要来自官方 Blog，证据强度低于 arXiv |
| [[Topics/13_base_model/Xiaomi_MiMo/2603_MiMo_V2_Omni/MiMo-V2-Omni\|MiMo-V2-Omni]] | 全模态感知-行动模型 | image/video/audio/text 共享 backbone；structured tool calling；function execution；UI grounding；perception-action 一体化叙事 | MMAU-Pro 76.8；BigBench-Audio 80.1；Video-MME 94.0；MMMU-Pro 85.3；支持 10h+ continuous audio | 它补上 audio/video/action，但技术细节披露少；更像方向宣言：agent 必须从看图说话转到感知后行动 |
| [[Topics/13_base_model/Xiaomi_MiMo/2604_MiMo_V2_5/MiMo-V2.5\|MiMo-V2.5]] | 开源多模态 agent 基座 | 310B/15B Sparse MoE；48T tokens；继承 V2-Flash Hybrid SWA；视觉/音频 encoder；五阶段训练；1M context；完全开源 | Coding Agent 71.8；Claw-Eval Text 65.8；MMMU-Pro 88.5；Video-MME 83.5；Token Plan 1x | 对社区最实用：把 V2 技术栈和多模态能力开源，成本模型也支持 1M context 实验 |
| [[Topics/13_base_model/Xiaomi_MiMo/2604_MiMo_V2_5_Pro/MiMo-V2.5-Pro\|MiMo-V2.5-Pro]] | 最强长程 agent 版 | 1.02T/42B；Hybrid SWA 6:1；128 window；MTP 约 3x；27T pretrain；SFT -> domain RL -> MOPD；1M context；开源 | SWE-Bench Pro 57.2；SWE-Bench Verified 78.9；Terminal-Bench 2.0 68.4；SysY compiler 4.3h/672 calls/233 passed；video editor 11.5h/1868 calls/8192 LOC | 最重要信号是 harness awareness 和 token efficiency：约 70K tokens/trajectory 达到 ClawEval 64% pass^3 |

## 关键机制

### 1. Reasoning density 是 RL 的地基

MiMo-7B 没有把 RL 当魔法。它先在预训练里做了三件事：

- 改 HTML/PDF 抽取，保留数学公式、代码块、STEM 结构。
- 三阶段 data mixture：普通语料 -> math/code 到约 70% -> 32K context + 约 10% synthetic reasoning responses。
- MTP 作为 auxiliary objective，让训练时的投资能在推理时复用。

所以 MiMo-7B-RL 能在 AIME 2025 上到 55.4，不是因为 7B 本身神奇，而是 base model 已经有足够推理潜力。

### 2. GUI grounding 的重点是状态转移

MiMo-VL 最值得抄的是 GUI 数据设计：

- 静态层：element grounding，按文本描述定位 UI 元素。
- 意图层：instruction grounding，按用户目标找可操作对象。
- 动态层：before/after screenshots -> predict intermediate action。
- 执行层：mobile/web/desktop 统一 action space，包括 click、scroll、input、drag、open、press、finished 等。

这说明 GUI Agent 的预训练任务不该停在"点哪里"，而要问"这个状态变成那个状态，中间动作是什么"。

### 3. SFT 会专精，也会遗忘

Miloco 说得很直接：home-scenario SFT 会让智能家居活动/手势识别变强，但 video、GUI、multimodal reasoning 会退化。它用 GRPO 在 temporal grounding、GUI grounding、STEM reasoning 上恢复。

这给垂直 agent 一个简单 recipe：

```text
领域 SFT 注入专业行为
  -> 找出退化的通用能力
  -> 针对退化能力构造 RL/verifier 数据
  -> 用 GRPO/RL 拉回泛化
```

### 4. 跨域训练要有课程顺序

MiMo-Embodied 不是把 embodied 和 driving 直接混起来，而是：

```text
General + Embodied SFT
  -> 加 Autonomous Driving SFT
  -> 加 CoT SFT
  -> GRPO RL
```

Ablation 里直接混合的 Embodied Avg / AD 是 59.2 / 55.2，多阶段是 63.7 / 63.4。也就是说，课程学习比"多域一起喂"更像真正的 cross-domain generalization。

### 5. Hybrid SWA 是长上下文 agent 的成本解法

V2-Flash 用 128-token sliding window + periodic global attention：

- 48 层：39 SWA + 9 GA。
- 每 5 个 SWA 后接 1 个 GA。
- attention sink bias 允许模型在 softmax 分母里学一个 sink，减少无意义注意力。
- 128K context 下 KV-cache 和 attention compute 接近 6-7x reduction。

关键直觉：SWA 负责局部连续性，GA 负责长程桥接。窗口太大反而会模糊分工，V2-Flash 的 ablation 里 128 比 512 更适合长上下文。

### 6. MTP 是训练和推理的同一个接口

MiMo 系列一直在复用 MTP：

- MiMo-7B：预训练单层 MTP，增强模型质量，也为 speculative decoding 留接口。
- V2-Flash：MTP block 用 dense FFN + SWA，单个 block 约 0.33B，避免变成新瓶颈。
- 推理：3-layer MTP 在不同 batch/accept length 下大约 2x-2.7x，实际常写约 2.6x。
- RL：rollout 阶段通常是瓶颈，MTP 可以减少小 batch on-policy RL 的吞吐损失。

最有意思的细节：acceptance length 和 next-token cross-entropy 强负相关，R2=0.995。这意味着 MTP throughput 可以用不确定性做自适应调度。

### 7. MOPD 是多域 agent 后训练的核心

V2-Flash 的 MOPD 可以压成三步：

```text
SFT student
  -> 每个领域单独 RL/SFT 出 teacher
  -> student 用自己的 on-policy rollout，接收 teacher token-level guidance + outcome reward
```

它解决两个问题：

- **capability imbalance**：数学、代码、搜索、安全、写作、工具调用直接混训会互相拉扯。
- **learning inefficiency**：只看 outcome reward 太稀疏，teacher logits 给 token-level dense signal。

效果不是所有项都超 teacher，但关键项很强：

| Benchmark | Student before | Best teacher | After MOPD |
|---|---:|---:|---:|
| AIME 2025 | 89.3 | 93.9 | 94.1 |
| HMMT Feb. 2025 | 76.9 | 82.6 | 84.4 |
| LiveCodeBench | 77.5 | 82.6 | 83.2 |
| SWE-Bench Verified | 67.8 | 74.2 | 73.4 |
| Tau2-Bench | 75.9 | 79.6 | 80.3 |

我的理解：MOPD 不是"蒸馏平均值"，而是让 student 在自己会遇到的状态分布上，只吸收 teacher 确信、且没有严重 train/inference mismatch 的 token。

## 对 GUI Agent / RL Infra 的直接启发

1. GUI 数据应加入 **before/after transition prediction**，不只做元素定位。
2. GUI RL 可以拆 teacher：element grounding teacher、instruction-following teacher、error-recovery teacher、tool-use teacher，再用 MOPD 合并。
3. GUI reward 可以借鉴 test-difficulty-driven reward：按用例通过率给困难状态更高权重，而不是 binary success。
4. On-policy rollout 吞吐是 RL 能否规模化的硬瓶颈，MTP/spec decoding 可能比换 optimizer 更重要。
5. 长程 agent 评估应同时看成功率和 token efficiency，例如 pass@k / tokens per trajectory，而不是只看最终分数。
6. Harness awareness 应成为评测项：模型是否会管理 memory、主动组织 context、利用工具环境，而不是只会生成下一步动作。

## 不要误读

- MiMo-VL 的 MORL 也承认多任务 RL 有干扰：reasoning 倾向长 CoT，grounding/counting 倾向短输出，目标不一致。
- V2-Pro、V2-Omni、V2.5、V2.5-Pro 的不少数字来自官方 Blog，不等于独立 benchmark 复现。
- Hard demo 很有信号，但不是标准评测；SysY compiler、视频编辑器、EDA 更适合看 harness-aware long-horizon behavior。
- "1M context" 不自动等于 long-horizon agency；真正重要的是能否在 1M 里选择、压缩、调用和恢复上下文。
- "Omni" 的技术细节披露较少，当前更像 perception-action 一体化方向宣言。

## 最短结论

MiMo 系列的真正贡献可以概括成一句话：

> **把 agent 的训练问题拆成可验证推理、GUI/多模态 grounding、领域课程学习、多 teacher 后训练、长上下文效率和 rollout 吞吐六个工程问题，然后逐个给出可复用方案。**

对 BrainHao 当前关注的 GUI Agent + RL Infra 来说，最该深入复现的是：

1. [[Topics/13_base_model/Xiaomi_MiMo/2506_MiMo_VL_7B/MiMo-VL\|MiMo-VL]] 的 GUI transition data。
2. [[Topics/13_base_model/Xiaomi_MiMo/2601_MiMo_V2_Flash/MiMo-V2-Flash\|MiMo-V2-Flash]] 的 MTP + MOPD。
3. [[Topics/13_base_model/Xiaomi_MiMo/2512_MiMo_VL_Miloco_7B/MiMo-VL-Miloco\|Miloco]] 的 specialize-then-recover 训练范式。
4. [[Topics/13_base_model/Xiaomi_MiMo/2604_MiMo_V2_5_Pro/MiMo-V2.5-Pro\|V2.5-Pro]] 的 harness-aware long-horizon demos 和 token efficiency 视角。
