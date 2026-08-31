---
title: "Tencent · Hunyuan — Series Summary"
type: model-note
tags: [model-note, base-model, series, tencent-hunyuan]
created: 2026-08-31
updated: 2026-08-31
---

# Tencent · Hunyuan — Series Summary

> [!tldr]
> 腾讯云产品化、MoE 效率、hybrid reasoning 与开放权重并行推进。

## 主干时间线

| 时间 | 模型 | 关键变化 | 一手来源 |
|---|---|---|---|
| 2023-09 | Hunyuan | 腾讯通用基模公开发布。 | [Official release](https://www.tencent.com/en-us/articles/2201699.html) |
| 2024-05 | Hunyuan-Large | 大规模 MoE 与长上下文基座。 | [Official repo / model card](https://github.com/Tencent/Tencent-Hunyuan-Large) |
| 2025-02 | Hunyuan-TurboS | Hybrid-Mamba-Transformer 提升长文效率。 | [Official repo / model card](https://github.com/Tencent/Hunyuan-Large) |
| 2025-04 | Hunyuan-T1 | hybrid reasoning 模型。 | [Official release](https://cloud.tencent.com/product/tclm) |
| 2025-06 | Hunyuan-A13B | 80B/13B active 开放混合推理 MoE，20T tokens。 | [Official repo / model card](https://github.com/Tencent-Hunyuan/Hunyuan-A13B) |

## 编辑判断

- 这里只收主干正代与改变路线的关键节点，不把每个尺寸、API snapshot 或专项 SKU 拆成正代。
- 训练数据、参数和消融只在官方技术报告明确披露时记录；闭源发布不做架构猜测。
- 当前旗舰详见 [[2506_Hunyuan_A13B/Hunyuan-A13B|Hunyuan-A13B]]。
