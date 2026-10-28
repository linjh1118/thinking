---
title: "EgoHand v1 — 单帧手部裁切到可变形三维手，而非直接动作策略"
type: model-note
tags: [model-note, nvidia, agent-training]
created: 2026-10-22
updated: 2026-10-28
---

# EgoHand v1：单帧手部裁切到可变形三维手，而非直接动作策略

> [!tldr] 我的判断
> 883.5M单图手部重建：DINOv3+TransformerDecoder预测SOMA/MHR pose、27维shape/scale及相机平移。官方代码News现已核实10/21首发；卡仍无公开benchmark分数。

> [!warning] 原始资料覆盖不足，尚未达到完整技术报告精读深度
> 官方代码News已给10/21，推理/微调入口与pipeline原图已补；报告2610.30293仅保留链接与摘要页，未精读源码，仍未达到完整技术报告深度。模型卡与代码概览的数据/速度口径不同，缺统一协议；研读示意与官方图分开标注。

## 收录身份与日期

10/22首次归档时原卡没有首发日；10/28沿当前新增代码链接读到IsaacCapture的官方News明确“2026-10-21 EgoHand v1 is released”。本轮据此将目录/Atlas日期改为2026-10-21，并计入精确日期30天表；不是把仓库createdAt或报告提交日用作首发。它是视觉几何专项，不是通用聊天正代，也不是机器人动作策略。

![官方IsaacCapture推理pipeline：检测、单帧估计、时序平滑与世界坐标转换](src/assets/egohand_pipeline.svg)

## 输入里已包含哪些外部工作

输入是一张RGB图像里由2D hand bounding box裁出的手部，平方化加padding后缩放到256×256，另外输入3×3相机内参（焦距和主点）。2D检测、正确裁切、左右手/镜像约定与crop坐标到原图坐标变换并未凭空消失；把它包装成“直接理解整场景”会隐藏依赖。

## 结构：身份、姿态、相机不能混为一个mesh

DINOv3视觉骨干从SAM3DBody初始化，接TransformerDecoder的SOMAHandTransformerDecoderHeadV2；learnable init pose/shape/camera queries产生SOMA手pose、27维MHR shape/scale和full-perspective相机translation。形状/尺度定义rest-pose hand identity，SOMA rig再通过前向运动学按姿态变形，最终可得到3D关节与mesh。

相机输出不能简单等同于完整6DoF全局camera pose。卡明确描述的是以内参为条件的perspective translation；尺度、camera/crop坐标和深度歧义仍须核验。本笔记公式仅是机制示意，不冒充未披露loss。

## 训练与评估证据到底够到哪里

训练组合真实第一人称手运动、RigPlay/DigitalHuman合成渲染与采购动捕，监督包括crop-frame 2D/3D关键点及MHR/SOMA参数。合成渲染有精确ground truth，但真实数据权利、分布覆盖与标签噪声不能因此忽略。卡称约16小时动捕，分1360×1360/30FPS与2464×2064/60FPS两种格式；这不是全部图像去重训练量。

| 材料 | 官方内容 | 本文边界 |
|---|---|---|
| 定性测试字段 | 100K images，真实视频/XR片段 | 不等于100K带3D标签定量验证 |
| EgoDex | 829h、338K演示、约90M帧 | 卡明确只用RGB做定性，不声称全量训练 |
| HOT3D | 9人、1.5K clips、227K帧 | 遮挡与不同相机的定量成绩未披露 |
| H2O | 4人、184clips、114K帧 | 与HOT3D标签/采集方法不同 |
| Evaluation字段 | 231K images | 与227K+114K不能直接相加对上，子集/去重口径待核 |
| Benchmark score | Undisclosed | 不补造MPJPE、PA-MPJPE或排名 |

![研读示意：重建到机器人数据还需要的验收](src/assets/protocol.svg)

## 10/28来源补充：推理管线与微调入口

新增的[IsaacCapture EgoHand README](https://github.com/NVIDIA/IsaacCapture/tree/main/src/python/isaaccapture_egopost)明确给出10/21 release，描述25关节、14M图像训练、约9ms推理，并链接[报告2610.30293](https://arxiv.org/abs/2610.30293)。其中9ms缺少此处统一的计时硬件、batch、检测/平滑/坐标转换覆盖范围，不能当完整视频系统延迟；14M也不能与模型卡的动捕小时和评测帧数直接对齐。模型卡仍写benchmark undisclosed，因此暂不补造排行榜或MPJPE。

[GEM-X](https://github.com/NVlabs/GEM-X)将Body Pose、Hand Pose、Body Motion放在共享推理/训练/评估框架中。`pose-video --task hand`是逐帧运行图像手模型，跟踪与平滑是可选处理；学得的temporal模型属于Body Motion。默认exo逐帧检测，ego配置增加跟踪、crop稳定与参数平滑。不能把这些处理混写成EgoHand单帧网络已经学会时序动力学。

IsaacCapture还要求视频、相机标定、2D框、EgoHand权重及SOMA-X手部assets；它提供可选检测、时序处理和依相机轨迹转换世界坐标。公开训练/微调入口不等于完整原始数据ETL与原训练recipe已可复现。两份README和官方SVG已保存；本轮未安装、执行代码或下载权重。

## 从单帧结果到机器人训练，缺的桥是什么

即使mesh视觉上自然，逐帧跳动、接触穿透、相机抖动和形状漂移仍会污染动作轨迹。原卡说可为机器人基础模型和操控策略提供信号，这是应用动机，不是已公开的闭环策略收益。应保存RGB、手框、内参、crop变换、pose/shape/camera及置信/失败标记，再做时间一致、物体接触和retarget约束。

卡给PyTorch/Linux与Ampere兼容，L40/L40s测试硬件，但无统一吞吐、延迟或显存表；883.5M参数不能换算成已验证实时FPS。本轮没有运行模型或下载权重。

> [!insight] 几何标签不自动成为可靠动作监督
> 对Agent/具身训练，应先分开检验2D重投影、3D误差、时序抖动、接触一致性，再问策略最终状态是否成功。用同一重建器产生标签又做唯一verifier会形成自证回路；少量独立动捕/专家审查比仅看渲染图更关键。

## 一手来源与限制

[🤗 HF Model Card](https://huggingface.co/nvidia/EgoHand-v1)，本地保存原MD与仓库元数据。权重OpenMDW1.1；原卡列出的隐私/安全subcards作为来源链接保留；新增报告与代码入口已在上节分别标明，未将摘要页当全文精读。涉及人物的图像与手部轨迹应具有授权，模型输出不会自动匿名化。


> 📊 相关可视化：[[egohand_v1_poster_zh.html|中文Poster]]
