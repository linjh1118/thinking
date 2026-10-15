---
title: "Hy4 Preview — 稀疏注意力与百万上下文的生产力旗舰"
type: model-note
organization: "Tencent Hunyuan"
release: 2026-08-28
updated: 2026-10-15
tags: [model-note, base-model, hunyuan, sparse-attention, agent-training]
topic: "13_base_model"
status: read
url: "https://huggingface.co/tencent/Hy4-preview"
created: 2026-10-15
---

# Hy4 Preview：稀疏注意力与百万上下文的生产力旗舰

> [!tldr]
> **Hy4 Preview 将混元从 Hy3 的295B/21B与256K，推进到770B/49B与1M；更重要的是同时引入 Gated DSA、IndexCache 和 iHC，围绕长程任务重新设计信息访问与残差流。** 它仍是 Preview，官方主动承认过度思考与重复验证，不能把“更长推理”直接当成更可靠。

![Hy4 Preview 官方能力总览](src/assets/benchmark.jpg)

> [!warning] 资料深度与日期边界
> 已亲读 HF 模型卡和腾讯云ADP首发接入博客，并保存原始页面和两张官方图。**当前取得的原始资料较少，尚达不到 GLM-5.3-Flash / Kimi-K3 那种完整训练技术报告级深度**：数据规模、RL目标、架构逐项消融均未充分披露。日期以2026-08-28官方“首发接入”公告为依据，不使用 HF lastModified；尚未发现更早的官方首发证据，如以后找到应前移，而不是把权重上传日当首发。

## 一页理解代际变化

| 维度 | Hy3正式版 | Hy4 Preview |
|---|---|---|
| 主干总参 / 活跃参数 | 295B / 21B | 770B / 49B |
| 上下文 | 256K | 1M |
| 注意力 | GQA | Gated DSA + IndexCache |
| 残差路径 | 本笔记不推定额外结构 | iHC，4条 residual streams |
| 专家 | 192、top-8 | 256 routed +1 shared，激活top-8 routed |
| 主干层数 | 80 | 78：首层dense、其余77层MoE |
| 状态 | 正式版 | Preview，仍有已知问题 |

不要将770B与49B相减后称为“节省了多少推理成本”：激活参数只是计算路径的代理指标，不能替代访存、通信、注意力和具体硬件测量。FP8也并非新的Hy4正代。

## 三个架构变化分别解决什么问题

### Gated DSA：减少每层需要读取的历史

标准密集注意力在长序列下读取大量过去位置。卡中给出的 Hy4 使用带门控的 DeepSeek Sparse Attention：索引器先挑选候选位置，再做稀疏访问。模型卡列出 indexer 32 heads、head dim128、top-k2048；这能说明检索预算的结构，**不能直接推导端到端速度提升倍数**，因为还要计算索引器和其余网络。

### IndexCache：相邻层不必重复全部索引工作

卡中明确采用跨层稀疏索引复用。对长程 Agent，同一历史在连续层中反复建立候选集合可能是额外成本；复用有机会减少重复计算。但复用周期、命中率、精度损失和单独消融没有在这份卡中完整给出，不能把论文中的一般结论直接当成Hy4实测。

### iHC：拓宽跨层的信息通道

模型使用 identity Hyper-Connections，将 residual streams 扩展到4条。这里改变的是信息在网络层之间如何流动，而不是工具调用协议。官方引用结构来源并不意味着训练稳定性细节已完整公开；没有约束公式和消融前，不自行补成“官方已证明的机制”。

| 其他卡内规格 | 值 |
|---|---:|
| hidden / attention heads | 6144 / 64 |
| Q / KV compression dimension | 2048 / 512 |
| MoE / dense FFN intermediate | 2048 / 18432 |
| 词表 | 120832 |
| 额外MTP层 | 1层，10B总参 /0.7B active；不在770B/49B主干表内 |

## 结果：读懂专家盲评，不替官方扩大结论

![Hy4 Preview 官方完整基准附录](src/assets/benchmark-appendix.jpg)

卡中有163名腾讯内部专家、203个工程任务的盲评。两组对照结果应分别阅读：

| 对照 | Hy4平均分 | 对照平均分 | Hy4胜 / 平 / 负 |
|---|---:|---:|---|
| GLM-5.3 | 2.99 | 2.92 | 46.8% /12.8% /40.4% |
| Kimi-K3 | 2.99 | 2.94 | 51.2% /7.9% /40.9% |

优势存在但幅度有限，且是内部生产力任务分布，不是全球通用能力排名；缺少逐任务方差、统计检验与盲化细节，不能宣称显著或全面领先。软件、办公、游戏和科学问题案例说明产品方向，并不能证明所有任务都具有同样收益。

## 官方承认的反例：验证也会成为低效循环

已知问题包括复杂任务思考过久、过度验证。对 Agent 来说，验证不是越多越好：同样成功的任务，重复运行同一测试、反复确认已经确定的事实，会增加延迟和成本，甚至挤掉有效上下文。

这也限制“1M就能把整个项目放进去”的产品描述。1M是窗口规格，不等于输入多少都能等质量利用；仍需测远距离证据定位、矛盾处理、指令优先级、输出预算和峰值KV占用。

## 部署与可复现边界

模型卡采用Apache-2.0，另提供FP8版本。推荐temperature=0.9、top_p=1.0；默认high思考，可通过no_think切换。vLLM / SGLang均有专门recipe，意味着部署需检查模型实现与parser，而不是只替换模型ID。本次未下载权重、未执行远程代码，未对硬件速度作实测承诺。

> [!insight] 对 Agent Training 的启发
> 可将“第一次得到足够证据后还做了多少无效验证”定义为轨迹效率指标。固定终态成功条件，分别统计有价值的反例搜索、重复测试和无依据自我怀疑，再比较Hy3/Hy4及不同effort。奖励设计应鼓励必要验证，同时惩罚不能改变结论的重复动作；这是研究建议，不是已披露的Hy4训练奖励。

## 一手资料与关联

- [S1 · HF Model Card](https://huggingface.co/tencent/Hy4-preview)，原始MD：[[src/Hy4-preview-model-card]]。
- [S2 · Tech Blog：腾讯云ADP，2026-08-28](https://adp.tencent.com/zh/blog/adp-hunyuan-hy4-preview-support)，原始HTML：`src/official-blog.html`。
- 架构引用来自原卡；它们是组件论文，不伪装成Hy4完整Tech Report。
- 前代：[[Topics/13_base_model/Tencent_Hunyuan/260423_Hy3/Hy3-Family]]。

> 📊 中文 Poster：[[hy4-preview_poster_zh.html]]
