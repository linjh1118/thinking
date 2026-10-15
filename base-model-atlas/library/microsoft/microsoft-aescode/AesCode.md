---
title: "AesCode"
type: model-note
release: "2026-09"
year: 2026
url: "https://huggingface.co/microsoft/AesCode-32B"
tags: [model-note, base-model, microsoft]
topic: "13_base_model"
status: read
created: 2026-10-13
updated: 2026-10-15
---

# AesCode

> [!tldr]
> Qwen3-VL 8B/32B上的视觉HTML生成模型，以设计图和七通道reward做GDPO。 把设计要求转成图，可解析属性由确定性verifier检查，视觉不可解析属性由VLM rubric评估；分通道group normalization减少某个容易优化信号吞掉设计质量。

![研读路径：整理示意，不代表未公开架构](src/assets/reading-map.svg)

## 一页速览

| 维度 | 当前证据 |
|---|---|
| 发布时间 | 2026-09（确切日期待核实，未计入精确30日表） |
| 类型 | 专项支线 / family · Visual Code |
| 关键事实 1 | 3K SFT；7408 RL prompts |
| 关键事实 2 | 32B：520 RL steps |
| 关键事实 3 | Overall85.89；Style55.99 |
| 检查日期 | 2026-10-13；官方原始资料在同级src/ |

## 视觉产物需要多维 Verifier，而非只奖励截图审美

基于Qwen3VL8B/32B微调，输出可执行视觉代码。SFT约3K样本、学习率1e-5；RL有7408prompts，32B520steps、8B400steps，GDPO128×8rollout、5e-6，KL与entropy系数.001，prompt/response预算8192。

## 奖励设计里最有价值的分工

设计图中的可解析结构使用确定性检查，无法轻易程序化的风格由VLM判断；七类评测通道帮助避免单一审美分数掩盖表格/边界错误。Playwright评测禁网络，使页面不依赖临时在线资源，但需要固定浏览器与渲染环境。

| 32B官方自报 | 得分 |
|---|---:|
| Overall | 85.89 |
| Rule | 94.33 |
| Table/Chart | 90.37 |
| Boundary | 97.27 |
| Style | 55.99 |

结构分高但Style不足60，说明不能从Overall推导全面设计质量。确定性奖励也可能被绕过：应检测隐藏元素、虚构图表数据、用图片替代需要可编辑代码等reward hacking。

> [!warning] 阅读与日期边界
> 已读HF model card；报告的完整源码尚未精读，不依据under-review声明推断正式会议接收。仓库9月29日创建，正式首发日尚未独立核实，暂按9月待核实。

### 2026-10-15：官方模型卡新增技术报告链接

最新HF卡已明确链接 [Tech Report：AesCode](https://arxiv.org/pdf/2610.18860) 与 [官方项目页](https://microsoft.github.io/AesCode/)。arXiv v1提交记录为2026-10-13 17:59:31 UTC，即北京时间10月14日01:59:31。这是**报告公开时间**，不证明模型权重在同一时间首次发布，故本模型仍不进入精确日期的30天表。

> [!warning] 技术深度尚未达标
> 当前新增的报告全文与源码尚未完成精读，原有笔记仍主要依赖HF卡，达不到完整报告的图表、训练消融和失败分析深度。本次先保存更新后的原始卡与报告摘要页并加入明确的Tech Report链接；不把“链接已发现”写成“全文已读”，也不下载PDF。

## 对 Agent Training 的启发

> [!insight]
> 使用禁外网的浏览器验收执行、文本、边界、表图、布局、留白、设计。参考图条件化带来收益但Style仍低于60，不能把Overall写成无需人工修订。

以上是基于已读官方资料的研究判断，不是官方保证，也没有在本机运行模型推理或复现论文成绩。下一步优先补独立验证器、固定任务/版本和完整失败轨迹，避免只保存最好样例。

## 一手资料与导航

- [S1] [HF Model Card](https://huggingface.co/microsoft/AesCode-32B)
- [S2] [Tech Report（PDF，仅链接）](https://arxiv.org/pdf/2610.18860)
- [S3] [官方项目页](https://microsoft.github.io/AesCode/)

原始下载文件与SHA-256见 [[src/retrieval_manifest.json|抓取记录]]。报告保留链接，不抓PDF；动态网页响应若只有壳文件，不将其标成完整离线正文。

- [[Topics/13_base_model/Base Model MOC|基模主题索引]]
- [[aescode_poster_zh.html|中文Poster]]

> 📊 相关可视化: [[aescode_poster_zh.html|AesCode 中文Poster]]
