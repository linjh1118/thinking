---
title: "HyFF：五尺寸保守原子势与可核验的分子动力学协议"
type: model-note
tags: [model-note, base-model, hunyuan, molecular-dynamics, atomistic-model]
created: 2026-11-02
updated: 2026-11-03
release_date: 2026-11-02
url: "https://github.com/Tencent-Hunyuan/hyra-results/tree/main/AI4Science/hyff"
html_tabs: true
---

# HyFF：从模型披露补齐为权重、代码与数值协议

> [!tldr] 我的判断
> HyFF是能量—力一致的原子势family，五种尺寸按同一节点管理。新发布README补全OMol25验证、不同容量的误差/速度、数值精度、长程项和MD约束；证明工具研发产物已公开，却不等于所有化学空间和长时模拟可靠。

## 发布与资料边界

> [!tldr]
> 官方11/2博客介绍模型，GitHub Release于11/2 14:30:56 UTC（北京时间22:30:56）发布。保留同一天的原节点，不另拆五尺寸或重复发布行。

之前只有博客的资料快照保存在src/history，现已补官方News、README、performance/largo/md/inputs/batch文档与发布页。权重挂在`hyff-v0.2.0`Release，9.3MB至4.81GB，包在首次使用时自动下载并验SHA；**本轮只核对公开入口，不触发下载或运行**。代码Apache-2.0，公开状态不继承给其他Hyra模型。

> [!warning] 原始训练资料仍不足，达不到完整报告精读标准
> 独立Tech Report现有明确PDF链接，遵照不下载PDF，尚未取得可读报告正文。公开代码/文档足以说明机制、完整性能条件和已知限制，但训练数据清洗、全阶段recipe、消融、验证集重叠与独立复现仍不能完整审核，达不到GLM-5.3-Flash/Kimi-K3完整报告级归因标准。旧“没有权重/报告入口”的限制已撤销，不再沿用。

![手绘研读：原子级模型与两个蛋白模型的输入输出分开](src/assets/handdrawn-scientific-models.png)

## 机制、输入与五尺寸

> [!tldr]
> 所有模型是平滑、保守的消息传递原子势，力为能量负梯度；Largo额外长程电荷项目前贡献很小，不应因“有电荷模块”便夸大其作用。

模型覆盖H到Bi共83元素，输入原子坐标、元素、total charge与spin multiplicity，在OMol25训练。原子特征含标量、向量和rank-2 Cartesian tensor（l≤2），平滑截断消息，每元素专家网络更新特征。Presto/Vivace/Moderato为增宽增深的基本模型，2–4 interactions、4.5–8Å截断；Andante/Largo增加edge-frame mixing，Largo另有总电荷/自旋attention embedding和latent-charge静电项。

| 型号 | 总参数 | 每原子激活 | 权重大小 | MD ms/step | MD ns/day | Force MAE meV/Å | Energy MAE meV/atom |
|---|---:|---:|---:|---:|---:|---:|---:|
| Presto | 2.31M | 0.05M | 9.3MB | 0.71 | 121 | 47.7 | 5.78 |
| Vivace | 6.66M | 0.16M | 26.7MB | 1.27 | 68 | 33.5 | 4.36 |
| Moderato | 34.8M | 0.83M | 139MB | 4.04 | 21 | 16.5 | 1.36 |
| Andante | 175M | 5.0M | 700MB | 29.5 | 2.9 | 7.65 | 0.620 |
| Largo | 1.20B | 34M | 4.81GB | 125 | 0.69 | 5.79 | 0.364 |

以上是完整官方README表。误差在全OMol25 validation 2,762,021结构上测，速度在另一套2586原子溶剂体系上测，不是每个验证结构的速度。单位要保留，不能把meV/atom与总体系eV混用。

输入`positions_A[N,3]`、`atomic_numbers[N]`，`box_A[3,3]`行是晶格向量；charge/multiplicity默认0/1。输出能量eV、力eV/Å；单结构CPU可用，GPU引擎与MD需Linux/CUDA。83元素覆盖不保证任意电荷、自旋或反应状态都准确。

## 评测条件与原图

> [!tldr]
> 29倍、9.7倍都是固定H20、固定体系与MD协议的对照，不能移植为任意原子数和任意GPU的加速保证。

![官方博客图4：五尺寸的精度—速度前沿；表中精确值以新README为准](src/assets/official-hyff.png)

速度条件：单H20/sm90，2586原子chorismate-in-water，1fs NVE、键约束，100步warm-up后500步均值，含neighbor-list重建；Python3.12、torch2.7.1/CUDA12.x、Triton3.3.1。其他GPU未测，首次编译耗时不含在热态表内。

Andante力MAE7.65，对比UMA-S-1.2的7.55，**略差而非更优**，但同条件MD快29倍。Largo能量0.364比DPA4-Pro0.380低约4.2%，同条件快9.7倍。不同指标的优势不合并成“全任务更准确”。

博客近6万原子膜100ns、4.6万原子酶一次断成键依然是厂商案例；100ns是物理模拟时长，单轨迹不足估计反应速率或自由能。此次补全数表并未自动补全湿实验、长时间统计与域外验证。

## 数值路径、守恒与MD约束

> [!tldr]
> 力的保守定义不能自动消除积分误差。刚性/柔性体系的步长、精度、重启与恢复协议都影响结果。

默认权重不cast。Presto/Vivace/Moderato用tf32x3乘法与FP32 LayerNorm统计；Andante乘法FP32、统计FP64；Largo默认tf32x3、统计FP64。MD以FP64 velocity-Verlet+RATTLE积分，力引擎仍有自己的FP32/近似数值路径；不能写“全模型FP64”。

| Presto水体系NVE | 时长 | 漂移 meV/atom/ns | 解释 |
|---|---:|---:|---|
| 刚性，1fs | 2ps | +0.4 | 默认有约束，不当任意体系保证 |
| 柔性，1fs | 2ps | −26.8 | 反例不能删去 |
| 柔性，0.5fs | 20ps | −2.8 | 步长减小后改善 |
| 柔性，0.25fs | 20ps | −0.7 | 仍为有限时长测试 |

NVT用Bussi thermostat，NPT用Monte Carlo barostat；不支持多GPU NPT、stress/virial输出、非周期MD或Langevin/Nosé–Hoover。NVT完整性失败可回退重抽速度用更小步长继续，NVE失败则停止；训练评测必须把recovery与真实稳定轨迹分开。restart续位置/速度/盒子，但计步器、时间和thermostat随机流重置，不是随机轨迹的无缝延续。

Largo的latent-charge项遵守总电荷，但已发权重scale约−4.66e-8、σ72.9Å，文档示例能量/力贡献很小。不能把名义长程模块当作主要精度来源。周期用SPME；isolated dense/tree不支持周期recenter和NPT。多GPU路径又使用isolated dense，不等同单GPU默认SPME。

Largo2586原子eager autograd在96GB H20放不下，专用引擎约12.8GB allocated（reserved另约18.8GB）；expert共享存储省约4.7GB而非减少参数。103440原子1/4/8GPU约6347/2207/1173ms，2586原子两卡反比单卡慢，不把多卡当默认更快。

> [!insight] 对Agent训练
> Agent搜索低能构型时，需要独立高精度复核与适用域检查，不能仅用同一势函数自评。记录输入结构hash、checkpoint SHA、数值档位、integrator、约束、thermostat、恢复次数与墙钟；把恢复后的成功与从未失稳的轨迹分别统计。本文建议未执行。

## 官方来源与导航

> [!tldr]
> 公开状态已由官方News和Release核实；报告PDF仅链接，不能描述成已读完整报告。

- [官方README](https://github.com/Tencent-Hunyuan/hyra-results/tree/main/AI4Science/hyff)、[权重/代码Release页面](https://github.com/Tencent-Hunyuan/hyra-results/releases/tag/hyff-v0.2.0)。
- [📄 Tech Report PDF，仅链接](https://github.com/Tencent-Hunyuan/hyra-results/blob/main/AI4Science/hyff/paper/HyFF_Technical_Report.pdf)，[📝 Tech Blog](https://hunyuan.tencent.com/research/hyra2?langVersion=zh)。
- 本地[[src/README|README]]、[[src/docs/performance|数值与速度]]、[[src/docs/largo|Largo]]、[[src/docs/md|MD]]、[[src/docs/inputs|输入]]、[[src/docs/batch|批推理]]。

> 📊 相关可视化：[[hyff_poster_zh.html|中文Poster]]
