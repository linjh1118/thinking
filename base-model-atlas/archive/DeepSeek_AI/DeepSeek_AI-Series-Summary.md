---
title: "DeepSeek AI Series Summary"
type: moc
tags: [moc, base-model, deepseek, mainline]
created: 2026-08-31
updated: 2026-08-31
---

# DeepSeek AI Series Summary

> [!tldr]
> DeepSeek 主线不是单一“低成本模型”故事，而是四次连续迁移：Dense scaling science → MLA/DeepSeekMoE 效率架构 → R1 verifier-driven reasoning → V3.1/V3.2/V4 的 agent + long-context 系统。

## 主线判断

1. **DeepSeek LLM** 建立数据与 scaling 实验方法。
2. **V2** 用 MLA + DeepSeekMoE 把 KV cache 和每-token 激活成本压下来。
3. **V3** 通过 FP8、MTP、无辅助损失均衡和通信重叠把 MoE 扩到 671B。
4. **R1** 证明 verifier + large-scale RL 可以诱导可迁移的 reasoning behavior。
5. **V3.1—V3.2** 把 reasoning 融入多轮工具调用与合成 agent 环境。
6. **V4** 用压缩+稀疏混合注意力把 1M context、agent 和可变推理预算统一成产品形态。

## 完整主线

| 时间 | 模型 | 一句话判断 | Poster |
|---|---|---|---|
| 2024-01 | [[Topics/13_base_model/DeepSeek_AI/2401_deepseek_llm/DeepSeek-LLM|DeepSeek LLM]] | DeepSeek 的真正起点不是某个榜单分数，而是把 scaling law、数据质量与训练系统一起当作可重复的工程问题。 | [[Topics/13_base_model/DeepSeek_AI/2401_deepseek_llm/deepseek_llm_poster_zh.html|Poster]] |
| 2024-05 | [[Topics/13_base_model/DeepSeek_AI/2405_deepseek_v2/DeepSeek-V2|DeepSeek-V2]] | V2 确立了 DeepSeek 的技术身份：MLA 解决 KV cache，DeepSeekMoE 解决激活计算，能力增长第一次与成本下降同时发生。 | [[Topics/13_base_model/DeepSeek_AI/2405_deepseek_v2/deepseek_v2_poster_zh.html|Poster]] |
| 2024-09 | [[Topics/13_base_model/DeepSeek_AI/2409_deepseek_v2_5/DeepSeek-V2.5|DeepSeek-V2.5]] | V2.5 不是新架构，而是把通用 Chat 与 Coder 两条权重线合并成一个可服务的统一 checkpoint。 | [[Topics/13_base_model/DeepSeek_AI/2409_deepseek_v2_5/deepseek_v2_5_poster_zh.html|Poster]] |
| 2024-12 | [[Topics/13_base_model/DeepSeek_AI/2412_deepseek_v2_5_1210/DeepSeek-V2.5-1210|DeepSeek-V2.5-1210]] | 1210 是 V2 系列的收官 checkpoint：架构不变，但把数学、代码、写作和文件/网页场景推到 V2 能达到的上限。 | [[Topics/13_base_model/DeepSeek_AI/2412_deepseek_v2_5_1210/deepseek_v2_5_1210_poster_zh.html|Poster]] |
| 2024-12 | [[Topics/13_base_model/DeepSeek_AI/2412_deepseek_v3/DeepSeek-V3|DeepSeek-V3]] | V3 把 V2 的稀疏架构扩到 671B，并用 FP8、无辅助损失负载均衡、MTP 与通信重叠证明“大 MoE 也能稳定且经济地训完”。 | [[Topics/13_base_model/DeepSeek_AI/2412_deepseek_v3/deepseek_v3_poster_zh.html|Poster]] |
| 2025-01 | [[Topics/13_base_model/DeepSeek_AI/2501_deepseek_r1/DeepSeek-R1|DeepSeek-R1]] | R1 的贡献是把 reasoning 从“模仿长 CoT”改写为“在可靠 verifier 上用大规模 RL 诱导搜索、反思与自校验，再用冷启动和通用对齐修正可读性”。 | [[Topics/13_base_model/DeepSeek_AI/2501_deepseek_r1/deepseek_r1_poster_zh.html|Poster]] |
| 2025-03 | [[Topics/13_base_model/DeepSeek_AI/2503_deepseek_v3_0324/DeepSeek-V3-0324|DeepSeek-V3-0324]] | 0324 是 V3 的关键 post-training checkpoint：没有换架构，却大幅抬高推理、前端、中文写作与函数调用，是“同底座能力迁移”的清晰样本。 | [[Topics/13_base_model/DeepSeek_AI/2503_deepseek_v3_0324/deepseek_v3_0324_poster_zh.html|Poster]] |
| 2025-05 | [[Topics/13_base_model/DeepSeek_AI/2505_deepseek_r1_0528/DeepSeek-R1-0528|DeepSeek-R1-0528]] | 0528 的主要变化是把更多 post-training compute 转成更深的测试时推理，并补上 function calling、JSON 与 vibe coding，令 R1 从研究模型靠近工具模型。 | [[Topics/13_base_model/DeepSeek_AI/2505_deepseek_r1_0528/deepseek_r1_0528_poster_zh.html|Poster]] |
| 2025-08 | [[Topics/13_base_model/DeepSeek_AI/2508_deepseek_v3_1/DeepSeek-V3.1|DeepSeek-V3.1]] | V3.1 把 V3 与 R1 两条线重新合并：单模型支持 Think/Non-Think，并第一次把 code/search agent 的多轮工具调用放到主模型定位中心。 | [[Topics/13_base_model/DeepSeek_AI/2508_deepseek_v3_1/deepseek_v3_1_poster_zh.html|Poster]] |
| 2025-09 | [[Topics/13_base_model/DeepSeek_AI/2509_deepseek_v3_1_terminus/DeepSeek-V3.1-Terminus|DeepSeek-V3.1-Terminus]] | Terminus 是一次面向真实用户反馈的稳定性收口：重点不是新能力宣传，而是语言一致性、异常字符和 Code/Search Agent 回归。 | [[Topics/13_base_model/DeepSeek_AI/2509_deepseek_v3_1_terminus/deepseek_v3_1_terminus_poster_zh.html|Poster]] |
| 2025-09 | [[Topics/13_base_model/DeepSeek_AI/2509_deepseek_v3_2_exp/DeepSeek-V3.2-Exp|DeepSeek-V3.2-Exp]] | V3.2-Exp 的任务很单纯：在尽量不损能力的前提下，用 DeepSeek Sparse Attention 把长上下文 attention 从 dense 路线迁到可部署的稀疏路线。 | [[Topics/13_base_model/DeepSeek_AI/2509_deepseek_v3_2_exp/deepseek_v3_2_exp_poster_zh.html|Poster]] |
| 2025-12 | [[Topics/13_base_model/DeepSeek_AI/2512_deepseek_v3_2/DeepSeek-V3.2|DeepSeek-V3.2]] | V3.2 把 DSA 从效率实验推进到 reasoning-first agent 模型：首次把 thinking 直接嵌入工具调用，并用大规模合成环境扩展 agent post-training。 | [[Topics/13_base_model/DeepSeek_AI/2512_deepseek_v3_2/deepseek_v3_2_poster_zh.html|Poster]] |
| 2026-04 | [[Topics/13_base_model/DeepSeek_AI/2604_deepseek_v4/DeepSeek-V4|DeepSeek-V4]] | V4 把 DeepSeek 的效率路线推进到 1M context：Pro/Flash 共用压缩+稀疏混合注意力，并把 agent、长上下文和可变 reasoning effort 作为默认服务形态。 | [[Topics/13_base_model/DeepSeek_AI/2604_deepseek_v4/deepseek_v4_poster_zh.html|Poster]] |

## 原始材料状态

- 13/13 模型目录均有 `src/retrieval_manifest.json`。
- 官方发布页同时保存原始 HTML 和可读 Markdown。
- GitHub/Hugging Face README 与模型卡以原始 Markdown 保存。
- 有 arXiv 源码的 LLM、V2、V3、R1、V4 已解包到各自 `src/paper/`；仅提供 PDF 的 V3.2-Exp/V3.2 保留官方技术报告 PDF。

## 研究判断

> [!insight]
> DeepSeek 最连贯的研究变量是“单位有效能力的系统成本”：V2 降低 KV/激活成本，V3 降低训练成本，R1 用 verifier 扩大 test-time search，V3.2 扩展 environment/tool trajectory，V4 再压缩超长上下文。阅读各代时应沿这条变量看，而不是把每个 checkpoint 当作孤立榜单。
