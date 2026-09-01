---
title: "Seed1.6 — 230B/23B-active 原生多模态与 AdaCoT"
type: model-note
year: 2025
url: "https://seed.bytedance.com/en/blog/introduction-to-techniques-used-in-seed1-6"
tags: [model-note, base-model, seed, moe, multimodal, adaptive-thinking]
status: read
created: 2026-08-31
updated: 2026-09-01
---

# Seed1.6 — 230B/23B-active 原生多模态与 AdaCoT

> [!tldr]
> Seed1.6 把 Seed1.5 的稀疏 MoE 主干升级为 **230B total / 23B active、256K context** 的多模态 family，并引入 AdaCoT：根据问题难度决定是否进入深度思考。它的关键不是多一个“thinking”开关，而是把推理质量、延迟和多模态任务统一到一个自适应策略中。

## 预训练三阶段

| 阶段 | 数据与目标 | 作用 |
|---|---|---|
| Text-only pre-training | 网页、书籍、论文、代码；规则+模型清洗 | 建立知识、代码和语言底座 |
| MMCT | 增加学科、代码、推理与高质量视觉数据 | 在连续训练中融合文本和图像 |
| LongCT | 多长度长上下文数据，32K 逐步扩到 256K | 避免一次性拉长导致训练不稳 |

官方明确披露 230B 总参数与 23B 激活参数，这比 Seed1.5 的“高稀疏 MoE”口径更可审计。

这三阶段并不是简单地“多喂一些图和长文”。Text-only 阶段先建立语言、代码与学科知识；MMCT 在已有文本底座上提高视觉数据和推理数据权重，减少从零联合训练的优化冲突；LongCT 再把长度从 32K 逐步扩到 256K，避免模型突然面对长序列时位置外推和数据分布同时变化。

值得注意的是，官方披露了数据类型和清洗流程——规则与模型联合清洗、过滤、去重、重采样——但没有披露每类数据占比。因而可以判断 curriculum 的方向，不能由此推算训练 token 或视觉 token 配方。

![Seed1.6 Base 官方评测](src/assets/base-benchmark.png)

## AdaCoT：把推理预算变成策略

AdaCoT 根据问题难度自适应启动思考，目标是在准确率与 reasoning latency 之间找到更好的 Pareto。它不同于用户手工指定固定 token budget：决策本身也是模型行为，需要训练数据覆盖“该想”和“不该想”的边界。

![Seed1.6 AdaCoT 效果](src/assets/adacot.png)

风险也随之出现：如果训练 reward 只奖励答案正确，模型可能学会对简单题过度思考；如果过度惩罚 latency，又可能在难题上过早停止。可靠评测应同时报告准确率、思考触发率、thinking tokens 和校准误差。

### AdaCoT 应怎样做消融

只比较“开启/关闭思考”的平均分不够。至少需要四组审计：

1. **难度校准**：按题目难度分桶，看触发概率是否单调上升；
2. **反事实预算**：对同一道题强制 no-think 与 think，测真实收益，而非模型自选后的选择偏差；
3. **成本曲线**：同时报告正确率、P50/P95 latency 与 reasoning tokens；
4. **跨模态稳定性**：文本难题与视觉难题是否使用同一套可靠的触发机制。

对于 Agent，AdaCoT 还存在一个更难的 credit assignment：一次失败可能是“想得不够”，也可能是 observation 不完整、工具选错或执行失败。若训练数据只给最终成功标签，自适应思考策略很容易学到错误归因。

## 多模态与长上下文

Seed1.6 在持续预训练中混合视觉数据，并覆盖 GUI interaction、视觉理解和深推理。官方多模态图表显示相对 Seed1.5-VL 的提升，但具体任务的 prompt、裁剪工具和输入分辨率会影响结论。

![Seed1.6 多模态评测](src/assets/multimodal-benchmark.jpeg)

256K context 解决的是“可以输入”，不是“可以可靠使用”。真正需要验收的是长文定位、跨段证据整合、针孔检索之外的多跳推理，以及在长 Agent 轨迹中对旧 observation 的正确引用。对于 GUI interaction，还要区分视觉 grounding、动作规划和执行器质量，避免把 harness 增益记到模型上。

## 从 Seed1.5 到 Seed1.6 的连续性

| 问题 | Seed1.5 | Seed1.6 的推进 |
|---|---|---|
| 稀疏效率 | 强调训练—推理共设计 | 给出 230B total / 23B active 的可核对规模 |
| 多模态 | 数据合成与偏好训练 | 将视觉数据纳入连续预训练主流程 |
| 推理成本 | serving 四象限优化 | AdaCoT 在模型行为层面分配计算 |
| 上下文 | 未形成主叙事 | 通过 LongCT 从 32K 扩到 256K |

这里的关键变化是：Seed1.5 主要在系统层节省每个 token 的成本，Seed1.6 开始在策略层决定“哪些问题值得生成更多 token”。两者共同构成后来 Agent 模型的成本控制基础。

## 如何验收这一代

- 固定相同题集，对比自动 AdaCoT、强制 no-think、强制 think；
- 对 32K、64K、128K、256K 分桶测试，而不是只报最大窗口；
- 把总参数与激活参数分开记录，同时测真实 latency；
- 多模态结果注明输入分辨率、帧采样、裁剪/grounding 工具；
- 对简单任务检查“过度思考”，对困难任务检查“过早停止”。

> [!insight]
> 对 Agent Training，AdaCoT 可以扩展成“自适应计算 + 自适应交互”：模型不仅决定想多久，还决定是否调用工具、是否请求更多 observation、何时停止 rollout。reward 应把 token 与环境 step 都计入成本。

## 资料充分度与边界

- 官方技术博客足以支撑架构、三阶段预训练和 AdaCoT 的机制判断，但未公开完整数据配比、专家路由细节、SFT/RL 数据规模和 reward 形式，因此不能还原训练 recipe。
- 256K 是最大 context 能力，不等于长轨迹信息会被有效利用。
- Embedding 等衍生模型属于支线。

## 一手资料

- [Seed1.6 官方技术博客](https://seed.bytedance.com/en/blog/introduction-to-techniques-used-in-seed1-6)
- [Seed 官方模型索引](https://seed.bytedance.com/en/models?view_from=homepage_tab)
- [[src/Official Source|本地来源索引]]
