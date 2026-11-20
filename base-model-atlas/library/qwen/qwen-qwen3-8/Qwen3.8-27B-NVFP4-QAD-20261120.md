---
title: "Qwen3.8-27B NVFP4-QAD — 量化材料补记"
type: model-note
html_tabs: true
created: 2026-11-20
updated: 2026-11-20
---

> [!tldr]
> NVIDIA NVFP4-QAD是已有Qwen3.8-27B的量化分发，不新增正代或发布事件；模型卡标11/4，不能把本轮观察日或repo修改日写为新模型日。

## 材料与归属

> [!tldr]
> 官方当前卡归档在同family的新updates目录；不覆盖已有家族笔记和未提交资料。

底座Qwen3.8-27B，ModelOpt v0.48.0，NVFP4 QAD1.0，文本/图/视频输入与文本输出，标称共享上下文262144。卡有Blackwell/Linux/vLLM集成声明，未运行权重、验证实际精度/速度或校准集。上游Apache与NVIDIA下载条款分别保留，不能自动认为量化包只受Apache约束。

## 证据与限制

> [!tldr]
> 量化方法说明不是该包完整实际训练账本，通用加速宣传没有本轮硬件测量。

[官方模型卡](https://huggingface.co/nvidia/Qwen3.8-27B-NVFP4-QAD)及原文见src/updates/2026-11-20/NVIDIA_27B_NVFP4_QAD.md。该材料用于部署规格核对；不报告未完成的任务质量、长上下文或吞吐对比。[[Qwen3.8-Family]]
