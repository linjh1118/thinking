---
title: "MiMo Series: From 7B Reasoning Model to Omnimodal Agent Foundation Models"
type: insight
source: "[[Topics/13_base_model/Base Model MOC]]"
authors: ["Xiaomi MiMo"]
year: 2026
venue: arXiv / Official Blog / Hugging Face
arxiv:
doi:
url: "https://mimo.xiaomi.com/"
tags: [insight, mimo, xiaomi, reasoning, multimodal, embodied, agentic, long-context, moe]
topic: "13_base_model"
status: read
rating: 5
related: ["[[Topics/13_base_model/Xiaomi_MiMo/2603_MiMo_V2_Omni/MiMo-V2-Omni]]", "[[Topics/13_base_model/Xiaomi_MiMo/2603_MiMo_V2_Pro/MiMo-V2-Pro]]", "[[Topics/13_base_model/Xiaomi_MiMo/2604_MiMo_V2_5/MiMo-V2.5]]", "[[Topics/13_base_model/Xiaomi_MiMo/2604_MiMo_V2_5_Pro/MiMo-V2.5-Pro]]", "[[Topics/13_base_model/Xiaomi_MiMo/2505_MiMo_7B/MiMo]]", "[[Topics/13_base_model/Xiaomi_MiMo/2506_MiMo_VL_7B/MiMo-VL]]", "[[Topics/13_base_model/Xiaomi_MiMo/2511_MiMo_Embodied/MiMo-Embodied]]", "[[Topics/13_base_model/Xiaomi_MiMo/2512_MiMo_VL_Miloco_7B/MiMo-VL-Miloco]]", "[[Topics/13_base_model/Xiaomi_MiMo/2601_MiMo_V2_Flash/MiMo-V2-Flash]]"]
created: 2026-06-11
updated: 2026-06-11
---

# MiMo Series: From 7B Reasoning Model to Omnimodal Agent Foundation Models

> [!tldr]
> MiMo 系列最核心的主线不是"从 7B 做大到 1T"，而是把 **reasoning base model** 作为底座，沿四条路线扩张：① Dense 推理基座（MiMo-7B）→ ② 多模态 GUI grounding（MiMo-VL）→ ③ 具身/驾驶跨域统一（MiMo-Embodied/Miloco）→ ④ MoE agent 可扩展架构（V2-Flash/Pro/Omni/V2.5）。MiMo 区别于 Qwen/Kimi/MiniMax 的核心差异是：**MTP 的训练+推理双用复用** 和 **MOPD multi-teacher on-policy distillation**，这两项技术把训练效率与 serving 效率串成了一条路线，目标是 long-horizon agent 而不是单轮 benchmark 刷分。

> [!note]
> 本笔记基于已收集到本地的 arXiv HTML/源码与小米官方网页剪藏。MiMo-Embodied 在 arXiv 没有 HTML 正文，改用 arXiv e-print LaTeX 源码作为主材料。

---

## 总体判断

MiMo 系列可以拆成四条发展路线，每条有不同的押注价值：

**路线 A — Reasoning Base Model 路线（MiMo-7B）**
从"普通 7B 做 RL"到"预训练阶段就注入 reasoning potential"。核心判断：小模型的 RL 上限取决于 base model 的推理潜力，而不是 RL recipe 本身。MTP 在预训练阶段作为 auxiliary loss，同时为推理阶段 speculative decoding 埋下接口。这条路线的价值在于它证明了 MTP 的 dual-use 复用路径，对所有想做"训练-推理一体化"的团队都有参考价值。

**路线 B — GUI/多模态 Grounding 路线（MiMo-VL-7B / Miloco）**
MiMo-VL 的真正价值不是"视觉语言模型"，而是 **GUI grounding 的系统化训练方案**：element grounding + instruction grounding + before/after screenshot transition prediction + 跨平台统一 action space。这让它在 OSWorld-G（56.1）和 ScreenSpot 系列上可以和专门 GUI model 竞争。Miloco 进一步揭示了 domain specialization 的代价：SFT 快速增强专用能力，但伤泛化；GRPO 能把通用能力拉回来。这个 pattern 对所有垂直领域 agent 都有参考价值。

**路线 C — 具身/驾驶跨域统一路线（MiMo-Embodied）**
第一个把 embodied AI（室内机器人）和 autonomous driving（户外驾驶）统一到单一开源 VLM 的工作。四阶段渐进训练（而非直接混合）解决了跨域干扰：在 embodied tasks 上比混合训练高 4%，在 AD tasks 上高 8.1%。核心结论：**课程学习是 cross-domain generalization 的有效手段**，而不是简单的数据混合。这对 GUI Agent / code generation 的跨域迁移有方法论启示。

**路线 D — MoE Agent 可扩展架构路线（V2-Flash / Pro / Omni / V2.5）**
这是 MiMo 系列最值得押注的方向。309B total / 15B active 的 MoE + Hybrid SWA（5:1，128-token window）+ 3 层 MTP speculative decoding（2.6× 加速）+ MOPD multi-teacher distillation，把训练效率与推理效率用同一套技术栈解决。MOPD 的核心价值：**解决 agent model 后训练的真实痛点——不同域的 RL teacher 互相干扰**。先分域练 teacher，再用 reverse KL + importance sampling 合并 student，student 有可能超越 teacher（V2-Flash 在 AIME 2025 上 student 94.1 > teacher 93.9）。

**我的押注判断**：路线 D 是 MiMo 对整个 agent foundation model 领域最重要的贡献。GUI Agent、robotics、coding agent 都会面临类似的"多域 teacher 合并"问题，MOPD 提供了一个可复用的解决方案。路线 B（GUI grounding）的数据工程细节（尤其是 before/after screenshot transition prediction）是最值得移植到其他领域的具体技术。

---

## 关键 Insight

### 1. Reasoning 进入 base model，而不是只靠 post-training

MiMo-7B 的最反直觉结论是：小模型的 RL 上限由 base model 的 reasoning potential 决定，而不是 RL recipe。[[Topics/13_base_model/Xiaomi_MiMo/2505_MiMo_7B/MiMo]] 不是拿普通 7B 去做 RL，而是在预训练阶段就强化数学、代码、STEM、合成推理数据和高质量抽取。

关键设计：
- 改进 HTML/PDF 解析，保留数学公式、代码块和 STEM 结构
- 三阶段 data mixture，reasoning pattern density 随训练阶段调整
- MTP 作为 auxiliary loss，同时为 speculative decoding 留接口
- 130K 可验证数学/代码题，尽量用 rule-based reward，降低 reward hacking

这和 Qwen3 的"thinking/non-thinking 统一"互补：Qwen 更强调模式统一和蒸馏，MiMo 更强调 base 数据与 RL 数据围绕可验证推理重做。

### 2. GUI grounding 不是多模态的附带能力，而是独立系统工程

[[Topics/13_base_model/Xiaomi_MiMo/2506_MiMo_VL_7B/MiMo-VL]] 的训练数据显式包含 GUI 数据：mobile、web、desktop 三端统一 action space；element grounding、instruction grounding；before-and-after screenshots 的 intermediate action prediction。这让它在 OSWorld-G（56.1）和 ScreenSpot 系列上可以和专门 GUI model 竞争。

核心启示：
- GUI grounding 需要三层能力：静态元素定位 + 指令目标定位 + 动态状态转移理解
- before/after screenshot 预测中间动作，是把 GUI 从纯感知变成 transition modeling 的关键一步
- 跨平台统一 action space 后，移动端、Web、桌面数据可以合流，减轻平台割裂

### 3. Domain specialization 后必须用 RL 恢复泛化，而非放任能力衰减

[[Topics/13_base_model/Xiaomi_MiMo/2512_MiMo_VL_Miloco_7B/MiMo-VL-Miloco]] 揭示了 domain specialization 的完整 lifecycle：SFT 能快速增强 home-scenario understanding，但会伤到 video、GUI、multimodal reasoning 等通用能力。GRPO post-training 把这些能力拉回来——这说明 specialization 和 generalization 不是非此即彼，而是可以循环迭代。

这个 pattern 可直接移植到其他领域：
- GUI domain：SFT 快速上手 → GRPO 拉回泛化
- 代码 domain：SFT 快速上手 → GRPO 拉回推理
- 医疗 domain：同理

### 4. Cross-domain curriculum learning 比直接混合训练更有效

[[Topics/13_base_model/Xiaomi_MiMo/2511_MiMo_Embodied/MiMo-Embodied]] 把 embodied AI 和 autonomous driving 放进一个统一 VLM，四阶段渐进训练（Embodied SFT → Driving SFT → CoT SFT → GRPO RL）：

| 训练策略 | Embodied Avg | AD Avg |
|---------|-------------|--------|
| 仅 Embodied | 高 | 低 |
| 仅 AD | 低 | 高 |
| 直接混合 | 中等 | 中等 |
| **多阶段渐进** | **62.4%** | **63.3%** |

结论：课程学习有效缓解跨域干扰，实现协同提升而不牺牲单任务性能。GUI / robotics / driving 可能都需要类似的课程顺序设计。

### 5. MTP 是训练-推理一体化的最佳载体

[[Topics/13_base_model/Xiaomi_MiMo/2601_MiMo_V2_Flash/MiMo-V2-Flash]] 展示了 MTP 的 dual-use 路径：
- **训练阶段**：MTP head 作为 auxiliary loss，提升 base model 的预训练效果
- **推理阶段**：MTP head 作为 draft model 做 speculative decoding，3 层 MTP → 2.6× decoding speedup

更重要的是 acceptance length 与 next-token cross-entropy 强负相关（R²=0.995），说明 MTP 的预测质量可以作为推理时自适应的信号。Low-entropy context（WebDev）下 acceptance length 最高 3.6，高熵 context 下自然降低。这是自适应 speculative decoding 的工程基础。

### 6. MOPD 是解决 multi-domain RL interference 的正确工程路径

MOPD 的三阶段流程：
1. **SFT**：在 diverse samples 上建立基础 instruction following
2. **Domain-specialized RL**：separate teachers 分别优化 Agentic（Code/Terminal/Web Dev）、Math、General、Safety
3. **MOPD**：student 在自己的 on-policy rollout 上，同时接收所有 teachers 的 token-level guidance

关键公式：`A^MOPD,t = sg[log π_domain(y_t|x,y<t) / π_θ(y_t|x,y<t)] + α × A^ORM`

使用 reverse KL divergence + importance sampling 过滤高差异 token，只学习 teacher 确信的部分，避免被低质量信号带偏。结果：student 超越 teacher（AIME 2025: 94.1 > teacher 93.9）。

### 7. Hybrid SWA 是 long-context 与 KV-cache 效率的务实平衡

5 个 SWA block + 1 个 GA block，5:1 ratio，128-token sliding window。关键创新是 **learnable attention sink bias**：softmax 分母上每 head 可学习的偏置，允许模型在需要时给某些 token 分配接近零的注意力。~7× KV-cache reduction at 128K context。

GA ratio 从 V2-Flash 的 5:1 逐步提到 V2.5-Pro 的 6:1，说明团队在逐步探索 global attention 的最小必要比例。

### 8. 1M context 是 long-horizon agent 的必要条件，不是奢侈

V2.5 系列全面升级到 1M token context，且使用"token plan"计费（而非 multiplier），降低了长上下文的成本感知门槛。V2-Flash 在 256K 检索近乎完美（NIAH-Multi 96.7%），V2.5 扩展到 1M。LongBench V2 上 V2-Flash post-trained 达到 60.6%（超越所有对比），说明长上下文不仅是"能读长文档"，而是 agent 在 long-horizon planning、multi-step tool use、context-dependent error recovery 时必须有足够的状态空间。

---

## 方法谱系

| 技术方向 | 代表论文/模型 | 核心机制 | 验证方式 | 主要价值 | 主要风险 |
|---|---|---|---|---|---|
| Reasoning 进入预训练 | MiMo-7B | 三阶段 data mixture + MTP auxiliary loss | 可验证数学/代码 rule-based reward | 提升 base model reasoning potential | 数据工程成本高 |
| GUI grounding 数据工程 | MiMo-VL | element/instruction grounding + before/after transition prediction + 统一 action space | OSWorld-G 56.1, ScreenSpot | 系统化 GUI agent 数据方案 | 三平台数据采集成本 |
| Domain specialization + RL recovery | MiMo-VL-Miloco | SFT 快速专业化 + GRPO 恢复泛化 | Smart-home F1 + 通用 benchmark | 垂直领域快速适配模板 | 需要 domain verifier |
| Cross-domain curriculum | MiMo-Embodied | 四阶段渐进训练（embodied → driving → CoT → RL） | 17 embodied + 12 driving benchmarks | 协同提升 + 跨域正迁移 | 课程顺序需要 domain knowledge |
| MoE 效率架构 | V2-Flash / V2.5 | 309B total / 15B active, 256 experts, top-8 | SWE-Bench Verified 73.4% | 用 1/2-1/3 参数达到 30B+ Dense 能力 | MoE load balancing 训练不稳定 |
| Hybrid SWA | V2-Flash / V2.5 | 5 SWA + 1 GA block，128-token window，learnable sink bias | 32K-256K NIAH 检索 | ~7× KV-cache reduction | SWA 局部信息可能不足 |
| MTP dual-use | V2-Flash / V2.5 | auxiliary loss → speculative decoding draft | 2.6× decoding speedup | 训练+推理一体化 | draft quality 随任务变化 |
| MOPD multi-teacher | V2-Flash / V2.5 | reverse KL + importance sampling + on-policy distillation | AIME 2025 94.1 > teacher 93.9 | 解决 multi-domain RL interference | 需要多个高质量 RL teachers |
| Omnimodal perception-action | V2-Omni / V2.5 | 统一 image/video/audio/text backbone + 原生 tool calling | 多模态 benchmark | perception + action 一体化 | 多模态对齐仍难 |

---

## 论文矩阵

| 论文 | 动机 | 核心贡献（1️⃣2️⃣3️⃣） | 对其他领域的可借鉴之处 |
|---|---|---|---|
| [[Topics/13_base_model/Xiaomi_MiMo/2505_MiMo_7B/MiMo\|MiMo-7B]] | 小模型做 RL 效果差，根源在于 base model reasoning potential 不足 | 1️⃣ 三阶段 data mixture 让 reasoning pattern density 随训练阶段调整<br>2️⃣ MTP auxiliary loss 提升训练效果，同时为 speculative decoding 留接口<br>3️⃣ 130K 可验证数学/代码题 + IOI 风格 test-difficulty-driven code reward | 数据工程重于 RL recipe；MTP dual-use 对所有想做推理加速的模型都有价值 |
| [[Topics/13_base_model/Xiaomi_MiMo/2506_MiMo_VL_7B/MiMo-VL\|MiMo-VL-7B]] | 视觉语言模型的 GUI grounding 能力弱，缺少系统化训练方案 | 1️⃣ 四阶段课程（2.4T tokens），长 CoT reasoning 进入预训练<br>2️⃣ MORL（RLVR + RLHF）统一训练<br>3️⃣ OSWorld-G 56.1 超越专门 GUI model UI-TARS（52.4） | 统一 action space + transition prediction 是 GUI 数据工程的核心；长 CoT 进入预训练而非只做 post-training |
| [[Topics/13_base_model/Xiaomi_MiMo/2512_MiMo_VL_Miloco_7B/MiMo-VL-Miloco\|MiMo-VL-Miloco]] | 智能家居场景数据稀缺，domain specialization 代价不清晰 | 1️⃣ CoT annotations + token-budget-aware reasoning 实现数据高效<br>2️⃣ SFT 快速专业化，GRPO 恢复泛化<br>3️⃣ Shaka Sign 手势识别 F1 88.3，大幅超越 Gemini-2.5-Pro（70.1） | specialization 后用 RL 恢复泛化是通用 pattern；CoT + 直接输出可降低边缘部署延迟 |
| [[Topics/13_base_model/Xiaomi_MiMo/2511_MiMo_Embodied/MiMo-Embodied\|MiMo-Embodied]] | Embodied AI 和 Autonomous Driving 独立发展，能否统一？直接混合训练会负迁移 | 1️⃣ 第一个把 embodied AI + autonomous driving 统一到单一开源 VLM<br>2️⃣ 四阶段渐进训练，比混合训练 embodied 高 4%，AD 高 8.1%<br>3️⃣ 17 个 embodied + 12 个 driving benchmarks | 课程学习解决跨域干扰；spatial grounding + affordance + planning 的同构抽象可迁移到 GUI |
| [[Topics/13_base_model/Xiaomi_MiMo/2601_MiMo_V2_Flash/MiMo-V2-Flash\|MiMo-V2-Flash]] | 如何在 15B active 参数限制下达到 30B+ Dense 能力？如何高效合并多域 RL teachers？ | 1️⃣ MoE 309B/15B + Hybrid SWA 5:1 + MTP speculative decoding 2.6×<br>2️⃣ MOPD 三阶段 multi-teacher on-policy distillation<br>3️⃣ SWE-Bench Verified 73.4% 开源最强 | MOPD 是解决 multi-domain agent RL interference 的最佳方案；MTP dual-use 是训练-推理一体化的工程模板 |
| [[Topics/13_base_model/Xiaomi_MiMo/2603_MiMo_V2_Pro/MiMo-V2-Pro\|MiMo-V2-Pro]] | Base model 能力如何转化为真实 agent scaffold 能力？ | 1️⃣ >1T total / 42B active，1M context<br>2️⃣ Hybrid ratio 从 5:1 提到 7:1，减少 GA 比例<br>3️⃣ OpenClaw / PinchBench / ClawEval agentic benchmarks | 1M context + agent scaffold co-design 是 long-horizon agent 的标配 |
| [[Topics/13_base_model/Xiaomi_MiMo/2603_MiMo_V2_Omni/MiMo-V2-Omni\|MiMo-V2-Omni]] | perception 和 action 能否真正一体化，而非分开的模块？ | 1️⃣ 统一 image/video/audio/text 共享 backbone<br>2️⃣ 原生支持 structured tool calling + function execution + UI grounding<br>3️⃣ perception-action 一体化叙事 | 端侧输出 tool calling/action 而不只是文本，是 agent foundation model 的形态定义 |
| [[Topics/13_base_model/Xiaomi_MiMo/2604_MiMo_V2_5_Pro/MiMo-V2.5-Pro\|MiMo-V2.5-Pro]] | 如何让最强模型在真实 hard tasks 上可验证？ | 1️⃣ 1.02T/42B，3-stage post-training（MOPD）<br>2️⃣ SysY 编译器 4.3h/672 calls/233 passes<br>3️⃣ 开源 Base + post-trained 权重 | 硬任务演示（编译/视频编辑/EDA）比 benchmark 更真实地验证 agent 能力 |
| [[Topics/13_base_model/Xiaomi_MiMo/2604_MiMo_V2_5/MiMo-V2.5\|MiMo-V2.5]] | 如何在开源生态下提供可用成本的全模态 agent model？ | 1️⃣ 310B/15B，48T tokens，五阶段训练<br>2️⃣ 1M context，token plan 计费（无 multiplier）<br>3️⃣ 完整开源 Hugging Face Base + post-trained | 开源全模态 agent model 的训练 pipeline 是社区复用的关键基础设施 |

---

## 可操作建议

**给 GUI Agent 研究者：**
1. 借鉴 MiMo-VL 的 GUI 数据工程方案：element grounding + instruction grounding + before/after screenshot transition prediction + 跨平台统一 action space。不要只收集"成功轨迹"，transition prediction 是更难的预训练任务。
2. 尝试 MOPD 而非单一 reward 混训：分别训练 element grounding teacher、instruction following teacher、error recovery teacher，再合并到 student。reverse KL + importance sampling 可以避免低质量 teacher 信号带偏 student。
3. 移植"specialization + RL recovery" pattern：先 SFT 快速适应目标 GUI 域，再用 GRPO 恢复 OSWorld/WebArena 等通用能力。

**给 Agent Foundation Model 训练团队：**
1. MTP dual-use 应成为标准配置：MTP head 在预训练阶段提升训练效果，在推理阶段作为 draft model 做 speculative decoding，不需要额外训练一个独立的 draft 模型。
2. Hybrid SWA 的 attention sink bias 是关键工程细节：128-token SWA + learnable bias 在 V2-Flash 上实现了 ~7× KV-cache reduction，且 32K-256K 检索近乎完美。
3. 1M context 是 long-horizon agent 的必要条件：V2.5 的 token plan 计费（而非 multiplier）降低了长上下文的成本感知门槛，值得参考。

**给 RL Infra 工程师：**
1. 多域 RL teacher 的干扰是真实问题：MOPD 的三阶段流程（SFT → 分域 RL → on-policy distillation）是可复用的工程方案。
2. 130K 可验证数学/代码题 + rule-based reward 显著优于纯 LLM judge：尽量用确定性验证器，降低 reward hacking 风险。
3. Test-difficulty-driven code reward（IOI 风格）是稀疏奖励代码任务的有效增强，值得移植到 SWE-bench 类任务。

---

## 可做实验

**实验 1：MOPD 在 GUI Agent 上的多域 teacher 合并**
- **假设**：GUI Agent 的不同能力（element grounding、instruction following、error recovery、tool orchestration）分别训练 RL teacher 再合并，比单一 reward 混训效果更好。
- **设计**：分别训练 4 个 domain-specialized RL teachers → MOPD student → 对比单一 GRPO baseline
- **指标**：OSWorld/WebArena 成功率、每种子能力的独立评测、域间干扰（某域 teacher 是否被其他域带偏）
- **预期**：MOPD student 在各域均超越或持平对应 teacher，且比单一 GRPO baseline 更稳定

**实验 2：MTP speculative decoding 对 GUI RL 训练吞吐的影响**
- **假设**：MTP speculative decoding 能显著提升 on-policy rollout 吞吐，降低 RL 训练的时间成本。
- **设计**：对比 3-layer MTP speculative decoding vs 无 speculative decoding 的同budget RL 训练
- **指标**：有效 generation throughput（tokens/s）、端到端训练时间、最终 model quality
- **预期**：2-3× throughput 提升，model quality 持平或略有提升（speculative draft 本身带来的 regularization 效果）

**实验 3：Cross-domain curriculum learning 在 GUI + Code 任务上的迁移**
- **假设**：GUI Agent 和 Code Agent 有正向迁移，课程顺序（先 GUI grounding 后 code reasoning）比直接混合更优。
- **设计**：四阶段训练（GUI SFT → Code SFT → Cross CoT → Cross RL）vs 直接混合 vs 仅 GUI vs 仅 Code
- **指标**：GUI benchmark（OSWorld）+ Code benchmark（SWE-bench）+ 二者联合 benchmark
- **预期**：课程训练在两个 domain 上均高于直接混合，接近各自单域最优

**实验 4：Hybrid SWA 的 attention sink bias 对长 GUI 任务的影响**
- **假设**：learnable attention sink bias 允许模型自适应调整 local vs global attention，对跨页面/跨应用 GUI 任务特别重要。
- **设计**：对比 learnable sink bias vs 固定 sink vs 纯 local attention vs 纯 global attention
- **指标**：长 GUI trajectory 成功率（>20 steps）、KV-cache 内存占用、推理 latency
- **预期**：learnable sink bias 在长轨迹上接近纯 global attention，但 KV-cache 效率接近 local attention

**实验 5：Domain specialization 后 RL recovery 的最优 schedule**
- **假设**：SFT 和 RL 的比例、RL 的时机（早停/晚停）影响 recovery 质量和专业化深度。
- **设计**：Grid search over SFT duration × RL start timing × RL duration for smart-home domain
- **指标**：Domain F1（home task）+ 通用 benchmark（MMLU-Pro、Video-MMMU）+ 两者的帕累托前沿
- **预期**：存在最优 SFT/RL schedule，且该 schedule 对不同 domain 有迁移性

---

## 开放问题

1. **MTP 的最优层数和位置是什么？** V2-Flash 用 3 层 MTP，是否存在 scaling law？MTP head 的位置（第一层 vs 最后层 vs 均匀分布）对训练效果有何影响？

2. **MOPD 的 teacher 数量上限在哪里？** 当有 10+ 个 domain-specialized teachers 时，reverse KL + importance sampling 是否仍能有效合并？会不会出现"平均化"效应导致所有域都略有退化？

3. **Hybrid SWA 的 GA ratio 最优值是否随任务类型变化？** V2-Flash 用 5:1，V2.5-Pro 用 6:1，是否存在对 GUI tasks 更优的 ratio（比如 4:1）？

4. **GUI grounding 数据是否可以用 MOPD 合并多源 teacher？** OSWorld 轨迹 teacher + ScreenSpot grounding teacher + 真实用户交互 teacher 能否通过 MOPD 合并到一个更通用的 GUI 模型？

5. **Cross-domain curriculum 的课程顺序是否可以自动学习？** MiMo-Embodied 需要人工设计课程顺序（embodied → driving），能否用 AutoCurriculum 方式自动发现最优顺序？

6. **1M context 的实际 agent 任务有哪些？** 目前 benchmark（LongBench V2）偏向检索类任务，真实的 1M-context agent 任务（如分析大型代码库、跨文档任务）如何设计可靠的 evaluation protocol？

7. **V2-Omni 的 omnimodal tool calling 是否需要 modality-specific action heads？** 当前设计是 unified text output + structured parsing，是否存在更高效的 modality-grounded action space？

8. **MiMo 路线和其他模型路线（MiniMax Lightning/MiniMax-M3、Kimi K2.5-MSA）的技术差异，哪个更重要？** Hybrid SWA vs Lightning/MSA sparse attention、MOPD vs single RL teacher，哪个对 long-horizon agent 能力的贡献更大？

---

## 结论

MiMo 系列的发展轨迹揭示了 agent foundation model 的三条核心规律：

**第一条：reasoning 必须进入预训练，而不是只靠 post-training**。MiMo-7B 的三阶段 data mixture 证明，小模型的 RL 上限由 base model 的 reasoning potential 决定。这对所有想做强 agent 的团队都是基础共识。

**第二条：MTP 是训练-推理一体化的最佳载体**。V2-Flash 的 MTP dual-use（auxiliary loss + speculative decoding draft）让训练阶段的投资在推理阶段直接复用，2.6× decoding speedup 是纯工程收益，不需要额外的模型权重。

**第三条：MOPD 是 multi-domain agent RL 的正确工程路径**。分域练 teacher + on-policy distillation 合并的方案，解决了不同能力域的 RL teacher 互相干扰这一真实痛点，且 student 有可能超越 teacher。这个 pattern 可迁移到 GUI Agent、coding agent、robotics agent 等所有需要多域合并的场景。

MiMo 系列最值得押注的方向是 V2.5 系列的 omnimodal agent 开源生态：48T tokens 五阶段训练、1M context、MTP + MOPD + Hybrid SWA 的完整技术栈，以及完整开源的 Base 和 post-trained 权重，将成为社区复现和研究的基础设施。

---

## 与其他模型路线的关系

| 对比对象 | 相似点 | MiMo 的差异点 |
|----------|--------|---------------|
| Qwen3 / Qwen3-Omni | reasoning 进入基座，多模态/全模态扩展 | MiMo 更突出 MTP dual-use、GUI grounding 数据工程和 MOPD multi-teacher post-training |
| MiniMax M1/M2/M3 | long-context、agentic RL、coding agent | MiniMax 更强调 Lightning/MSA sparse attention 与真实 agent harness；MiMo 更强调 hybrid SWA + MTP + MOPD 技术栈完整性 |
| Kimi K2/K2.5 | MoE agentic intelligence、coding/vision-agent 能力 | Kimi 更强调大规模 agentic tool/data 与 MuonClip 等训练稳定性；MiMo 更强调小激活 MoE（15B active）和 teacher-student 合并的系统工程 |
| Gemini Robotics / Seed Agent Foundation Model | physical-world / computer-use agent | MiMo-Embodied 把 embodied AI 与 autonomous driving 统一到一个 open-source VLM 技术报告里，是同类工作中最透明的 |

---

## 相关资料

- MiMo-7B：[[Topics/13_base_model/Xiaomi_MiMo/2505_MiMo_7B/MiMo]]
- MiMo-VL-7B：[[Topics/13_base_model/Xiaomi_MiMo/2506_MiMo_VL_7B/MiMo-VL]]
- MiMo-VL-Miloco-7B：[[Topics/13_base_model/Xiaomi_MiMo/2512_MiMo_VL_Miloco_7B/MiMo-VL-Miloco]]
- MiMo-Embodied：[[Topics/13_base_model/Xiaomi_MiMo/2511_MiMo_Embodied/MiMo-Embodied]]
- MiMo-V2-Flash：[[Topics/13_base_model/Xiaomi_MiMo/2601_MiMo_V2_Flash/MiMo-V2-Flash]]
- MiMo-V2-Pro：[[Topics/13_base_model/Xiaomi_MiMo/2603_MiMo_V2_Pro/MiMo-V2-Pro]]
- MiMo-V2-Omni：[[Topics/13_base_model/Xiaomi_MiMo/2603_MiMo_V2_Omni/MiMo-V2-Omni]]
- MiMo-V2.5-Pro：[[Topics/13_base_model/Xiaomi_MiMo/2604_MiMo_V2_5_Pro/MiMo-V2.5-Pro]]
- MiMo-V2.5：[[Topics/13_base_model/Xiaomi_MiMo/2604_MiMo_V2_5/MiMo-V2.5]]

---

## 待更新

- [ ] MiMo-V2-Pro / V2-Omni 若后续发布 technical report，需要补充架构与训练 recipe 的可验证细节
- [ ] V2.5-Pro Hugging Face model card 可再单独剪藏一次，补全 deployment 与 evaluation 表
- [ ] 和 MiniMax M3、Qwen3.5-Omni、Kimi K2.5 做一张"全模态 agent 基座"对比表
- [ ] 单独整理 MOPD 与 DPO / GRPO / CISPO / Forge RL 的关系
