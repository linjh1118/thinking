---
title: "GPT-Image 2.6 · Flare / Sunburst"
type: model-note
year: 2026
url: "https://openai.com/index/introducing-images-2-6/"
tags: [model-note, base-model, openai, image-generation, multimodal]
status: read
created: 2026-11-05
updated: 2026-11-05
---

# GPT-Image 2.6 · 从一次生成到可控的编辑迭代

> [!tldr]
> OpenAI 官方发布页与系统卡标注 **2026-11-04**。Flare 与 Sunburst 是同一图像专项代际的速度与精细度配置。新增的复杂度控制、标注编辑、GIF 和 SVG 让工作流可拆开验收；系统卡显示 Flare 的审核前与审核后结果不能混读。

## 家族和接口

| 维度 | Flare | Sunburst |
|---|---|---|
| 模型 ID | `gpt-image-2.6-flare` | `gpt-image-2.6-sunburst` |
| 官方定位 | 较小、优先短响应与迭代 | 复杂布局、细节保真与精确编辑 |
| 输入与输出 | 文本与图像 → 图像 | 同左 |
| API 卡所列直接端点 | `/v1/images/generations`、`/v1/images/edits` | 同左 |
| 文本输入／缓存 | $5／$1.25 每百万 token | 同左 |
| 图像输入／缓存／输出 | $8／$2／$30 每百万 token | 同左 |

发布页给出的最低约 6 秒限定为 Flare、低 quality 的条件。相同标价不意味着单图成本相同，实际费用取决于输入、输出 token、格式和迭代次数。接口支持以当前模型卡为准，不能从 ChatGPT 或 Codex 可用推断每个 API 端点均已开放。

## Quality 和 Complexity 各自控制什么

Quality 侧重细节与保真，Complexity 控制为复杂约束投入的规划程度。局部改字可以固定图像质量，从低复杂度测试；多对象海报可提高复杂度并逐条验收版面约束。下列官方样例使用同一提示、Sunburst、1024×1536、medium quality、PNG 生成，改变 complexity。网页展示的是 WebP 副本。三图可观察构图、奖杯和标题位置变化，不构成独立质量或延迟评估。

![低复杂度官方示例](src/assets/complexity-low.webp)
![中复杂度官方示例](src/assets/complexity-medium.webp)
![高复杂度官方示例](src/assets/complexity-high.webp)

## 编辑、动画与矢量输出

- **标注编辑**。圈点标记是定位线索。验收时分别检查目标区域的变化和非目标区域的身份、排版与文字保留，至少加入一次回退和多轮改写。
- **GIF**。官方指南给出了帧数和帧时长等控制。逐帧看似正确仍可能出现对象闪烁、动作断裂或跨帧风险。样例 9 帧 × 200 ms 对应约 1.8 秒，不能把这个样例当生成延迟。
- **SVG**。按官方 API 指南检查输出是否真正可编辑，检查 viewBox、文字轮廓、依赖与浏览器显示。矢量格式适合图标与品牌资产，格式可用性和视觉正确性应分开验收。

## 系统卡与证据边界

系统卡使用同一组 3,077 条刻意设计的对抗请求，和对应的 2.5 版本比较。Flare 经选定审核后呈现的违规图像从 46/3,077（1.49%）到 66/3,077（2.14%），总体差异不显著。审核前 Flare 的非违规比例从 78.36% 降到 75.04%，官方报告为显著下降。这些指标分别刻画所评模型配置与选定审核组件，无法估计生产流量中的违规率。

GIF 风险还包含跨帧语义，系统卡单列 GIF 审核测试。发布材料说明图像来源标记结合 C2PA 元数据与不可见 SynthID 水印，不能保证转码后元数据完整。两款均未跨越系统卡所定义的 Bio High 或 Cyber High 门槛；这是给定评估条件下的结论。

> [!warning]
> 资料达到系统卡、模型接口与官方样例级别。官方未披露参数量、网络结构、训练计算与数据配比，缺少对等画质基准和速度分位数。产品发布页已核读但归档请求返回 403，本地保留系统卡与 API 原文并保留官方发布链接。

## 对评测和上线的启发

先固定输入资产、输出尺寸、质量和 harness，再做 Flare/Sunburst × complexity 比较。分开计目标正确率、区域外稳定性、连续修改保留率、总轮数、费用与到可接受成品的时间。保留每轮输出与模型 ID，GIF 另加跨帧一致性和审核，SVG 另加可编辑性与渲染验证。

## 一手来源

- [发布博客](https://openai.com/index/introducing-images-2-6/)
- [系统卡](https://deploymentsafety.openai.com/chatgpt-images-2-6)
- [Flare API 模型卡](https://developers.openai.com/api/docs/models/gpt-image-2.6-flare)
- [Sunburst API 模型卡](https://developers.openai.com/api/docs/models/gpt-image-2.6-sunburst)
- [提示与官方示例](https://developers.openai.com/api/docs/guides/image-prompting)
- [中文 Poster](gpt_image_2_6_poster_zh.html)
