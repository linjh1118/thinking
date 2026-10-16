---
title: "Nemotron 3.5 Super VL / Bolt — 从多模态父模型到 24GB 部署预算"
type: model-note
tags: [base-model, nvidia, nemotron, compression, agent-training]
created: 2026-10-16
updated: 2026-10-16
release_date: 2026-10-15
url: "https://huggingface.co/nvidia/NVIDIA-Nemotron-3.5-Super-VL-120B-A12B-BF16"
---

# Nemotron 3.5 Super VL / Bolt

> [!tldr] 核心判断
> 本次发布同时给出大容量父模型与围绕本地显存预算压缩的派生模型。Super VL 的语言—视觉联合后训练、Bolt 的结构压缩—能力恢复—混合量化，是一条链，不是 BF16、NVFP4、GGUF、Base、drafter 各自成为新正代。Atlas 以一个 3.5 family 发布阶段展示；不把既有 Lightning 历史节点擅自删除或重命名。

> [!warning] 证据边界
> 已读取并归档 Super BF16 / NVFP4 / Base、Bolt BF16 / 24GB / GGUF / LiLiCorr 模型卡，以及 Bolt 官方博客和官方图。两份 Tech Report 已找到并列出链接，按当前约定不下载 PDF；报告全文与消融尚未完成精读，因此还达不到 GLM / Kimi 完整报告级细节。以下是卡与博客级深入研读，不冒充报告全文结论。本次没有运行权重。

## 同一发布阶段中的两种任务

官方模型卡写明 **2026-10-15** 发布，Bolt 博客也标为 10 月 15 日；博客有时区时间，模型卡只给日期。训练时期、仓库创建时间、lastModified 均不替代这个发布日期。

| 项目 | Super VL | Bolt |
|---|---|---|
| 总参数 / active | 120B / 12B | 74B / 9B |
| 上下文窗口 | 1M，输入输出共享 | 256K |
| 角色 | 多模态父模型 | 从父模型结构压缩的本地 Agent 模型 |
| 权重选择 | BF16、NVFP4、Base 等 | BF16 定制基准、24GB 混合量化、GGUF |
| 推测解码 | 原生 MTP | 配套 LiLiCorr drafter |
| 许可 | OpenMDW 1.1 | 原卡列 OpenMDW 1.1 |

“24GB”是部署版本设计目标，不是 BF16 的体积，更不是任意 256K 上下文、并发、视觉输入都能在 24GB 总系统内运行。激活参数减少计算，但全部权重、KV、运行时和视觉组件仍需内存。

![官方 Super VL 能力总览](src/assets/super-accuracy.png)

*图：官方 Super 模型卡结果。指标绑定其 harness，不代表本次本地实测。*

## Super：能力来自训练链，而不只是接一个视觉编码器

Super 使用混合 Mamba-2、MoE、Attention 主干，视觉侧是 C-RADIO encoder 与 connector。模型卡列出 512 个 routed experts；不要把路由专家总数与每 token 活跃参数混为一谈。

公开训练路径可以按依赖关系理解：

1. 冻结主干训练 MTP，随后通过来自 Nemotron 3 Ultra Base 的 1T token 蒸馏更新能力。
2. 加入 100B Indic 持续预训练、35B 的 1M 长上下文扩展、67B 的 SWE 中间训练，再做 9B 长上下文恢复。SWE 数据包含仓库、issue/PR、diff、CI 日志和 Agent 轨迹。
3. 训练视觉 encoder / connector，进行语言与视觉联合的两阶段 SFT，序列打包至 524,288。
4. 结合可验证奖励 RL、RLHF、专项教师与多教师 on-policy 蒸馏；最后对冻结的后训练主干重新训练 MTP。
5. NVFP4 通过 QAD 恢复量化质量；不是把所有模块无差别四比特化。

卡中语言基础训练规模超过 20T tokens；这与 Bolt 的 80B 压缩训练量是不同口径，不能相加成一个新的训练总量。公开流程仍缺完整可复现配比和逐项因果消融；知道阶段名不等于知道每一步的独立贡献。

## Bolt：先改变结构，再恢复能力，再按模块量化

Star Elastic 用预算条件路由器选择各层专家数量与 MoE 中间宽度，在结构搜索中考虑后续量化占用，将 120B/A12B 压到 74B/A9B。博客给出专家 top-k 从 22 改为 9。它不是简单删掉固定比例层，也不是在同一权重上换文件格式。

压缩后先恢复视觉能力，再做模拟环境端到端 RL；最后进一步优化推理路径与工具执行的 token 效率。这里最值得研究的是：压缩损失能否被任务反馈补回，而不是只看压缩前后知识问答均分。

| 模块 | 24GB 版本的处理 |
|---|---|
| routed 与 shared experts 的 FC1 / FC2 | IQ2_XXS，2.0625 bits/element |
| Mamba 线性层 | NVFP4 |
| lm_head、embedding、attention、Latent MoE | Q8_0 |
| 恢复方法 | Quantization-aware distillation |

因此，“整个模型只有 2bit”是不准确的。Super NVFP4 也保留视觉 encoder / connector、Mamba convolution、embedding 的 BF16 与 router 的 FP32；Blackwell W4A4 与其他硬件 W4A16 路径不能混报。

![官方 Bolt 同内存级比较](src/assets/bolt-accuracy.png)

*图：官方按约 24GB 内存级筛选的对照；这是特定筛选条件，不是所有开放模型总榜。*

![官方结构压缩与量化阶段对照](src/assets/bolt-deployment.png)

*图：博客展示压缩到部署阶段的精度变化。与训练数据、后训练同时改变时，不把全部收益只归因于比特数。*

## 检查弱项：量化不会在每个任务上等比例退化

下面第一张表来自官方控制其他参数不变的 Super BF16 / NVFP4 比较。保留 offline 标记，不与在线网页环境混用。

| 基准 | Super BF16 | Super NVFP4 |
|---|---:|---:|
| GPQA Diamond | 89.52 | 89.90 |
| SWE-bench Verified | 71.10 | 71.07 |
| SWE-bench Pro | 51.78 | 51.30 |
| Terminal-Bench 2.1 | 60.67 | 62.78 |
| BrowseComp | 78.00 | 77.50 |
| WebVoyager offline | 77.72 | 66.31 |
| OSWorld-Verified | 51.14 | 52.30 |
| DeepSWE offline | 24.65 | 18.20 |

SWE Verified 几乎持平，WebVoyager 却下降 11.41 个百分点；Terminal / OSWorld 反而略高。正确结论是逐任务验收 checkpoint，不是宣称“量化完全无损”或“所有任务都变差”。同一官方对照中 Qwen3.8 Flash Next 的 Terminal-Bench 2.1 为 85.8，也不能被只选优势项目的叙述省略。

| 基准 | Bolt 24GB | Bolt BF16 |
|---|---:|---:|
| Terminal-Bench 2.1 | 50.98 | 53.93 |
| GPQA Diamond | 86.43 | 88.83 |
| PinchBench | 87.82 | 90.35 |
| MCP Atlas | 52.20 | 55.60 |
| BrowseComp | 66.75 | 70.00 |
| WebArena Vision | 50.86 | 50.25 |
| AA-Omniscience non-hallucination | 61.27 | 56.14 |

这张表不是 Super 的量化实验，也不能把不同榜单上 MCP Atlas 的 reported 全量值与 reproduced 500 题子集混成同一设置。NeMo Gym 提供部分重现实验配方；一些视觉基准仍使用待开源内部 scaffold，复现能力不是全面完备。

## 84 tokens/s 必须连同慢项一起读

博客在 Windows 11 ARM x64、同一 RTX Spark（Surface Laptop Ultra，128GB）上用 llama.cpp 测试：

| 模型配置 | SPEED-Bench-Coding TPS ↑ | AA AgentPerf Local replay 秒 ↓ |
|---|---:|---:|
| Bolt IQ2_XXS + LiLiCorr | 83.99 | 600.80 |
| Qwen3.6 35B-A3B Q4 + MTP | 96.63 | 453.97 |
| Gemma4 26B-A4B Q4 + MTP | 100.56 | 480.68 |
| Qwen3.8 27B Q4 + DFlash | 28.26 | 1043.28 |

Bolt 不是这张表中最快的模型。速度与质量 Pareto 的主张依赖质量维度，不能删去 Qwen3.6 / Gemma4 更快的事实。LiLiCorr 是 1.13B 参数的并行 drafter（不含共享 embedding / head），与目标模型是两个组件。博客另列 7-token draft、vLLM 并发 64 的接受长度，不能与上述 llama.cpp 端到端结果拼成一个实验。

## 研读后的验收方案

固定任务集、harness、parser、thinking effort、输入长度与输出预算，比较 Super BF16、Super NVFP4、Bolt BF16、Bolt 24GB。每项记录终态成功、工具格式错误、无效重复、每成功任务 tokens、延迟、峰值内存；推测解码开关另做同硬件对照。卡里的示例允许本地媒体目录过宽，实际服务应收窄文件权限，不原样照搬到多人服务。

> [!insight] 对 Agent Training 的启发
> 面向内存预算做结构压缩后，奖励应直接覆盖工具正确性和推理效率，而不能只通过教师 token 相似度恢复。量化在长链任务上的退化可能远大于短问答均分变化；优先分析第一个工具错误及其后续放大，而不是把所有失败都叫知识不足。

## 来源与导航

- [HF Model Card · Super BF16](https://huggingface.co/nvidia/NVIDIA-Nemotron-3.5-Super-VL-120B-A12B-BF16)；[[src/NVIDIA-Nemotron-3.5-Super-VL-120B-A12B-BF16-model-card|本地原卡]]
- [HF Model Card · Bolt 24GB](https://huggingface.co/nvidia/NVIDIA-Nemotron-3.5-Bolt-74B-A9B-24GB)
- [Tech Blog · Bolt](https://research.nvidia.com/labs/nemotron/Nemotron-3.5-Bolt-24GB/)
- [Tech Report · Super / Lightning PDF](https://research.nvidia.com/labs/nemotron/files/NVIDIA-Nemotron-3.5-Super-and-Lightning-Technical-Report.pdf)
- [Tech Report · Bolt PDF](https://research.nvidia.com/labs/nemotron/files/NVIDIA-Nemotron-3.5-Bolt-74B-A9B-24GB-Technical-Report.pdf)
- [[Topics/13_base_model/NVIDIA_Nemotron/Variants/261015_Kimodo_SOMA_RP_v1_2/Kimodo-SOMA-RP-v1.2|同团队动作生成支线]]

> 📊 相关可视化：[[nemotron35_super_bolt_poster_zh.html|中文 Poster]]
