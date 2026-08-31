---
title: "Qwen3.8 Family"
type: model-family
organization: "Alibaba / Qwen"
release: 2026-08
year: 2026
url: "https://www.qianwenai.com/models/qwen3.8-flash"
tags: [model-family, base-model, qwen, qwen3.8, multimodal, agentic]
topic: "13_base_model"
status: read
created: 2026-08-27
---

# Qwen3.8 Family

> [!tldr]
> Qwen3.8 不是一条“旗舰大模型 + 若干阉割版”的简单产品线，而是同时覆盖 **2.4T 极稀疏旗舰、低激活 Flash、新一代 27B Dense VLM** 的正代家族。Max 追求能力上限，Flash 追求 agent 场景的成本—吞吐 Pareto，两个开放权重版本则分别给出超大 MoE 与本地 Dense 路线。

![Qwen3.8-Flash-Next 官方主视觉](src/assets/qwen3.8-flash-banner-zh.jpg)

## 家族成员

| 模型 | 参数 / 架构 | 模态 | API context | 当前定位 |
|---|---|---|---:|---|
| Qwen3.8-Max | 2.4T MoE | text / image / video → text | 1M | 闭源旗舰，复杂编程、办公和专业任务 |
| [[Qwen3.8-Flash]] | Flash-Next 公开架构为 125B core / 6B active + 51B N-gram + 4B MTP | text / image / video → text | 1M | 高并发、工具工作流与 coding 默认款 |
| Qwen3.8-2.4T-A95B | 2.4T / 95B active MoE | 当前 API 页面列 text → text | 1M | Max 同尺度的开放权重旗舰 |
| Qwen3.8-27B | 27B Dense | text / image / video → text | 1M | 可本地部署的原生视觉语言主线模型 |

## API 价格快照

价格来自 2026-08-27 模型市场页面，单位为人民币 / MTok。

| 模型 | 输入 | 输出 | 缓存命中 |
|---|---:|---:|---:|
| Qwen3.8-Max | ¥12 | ¥36 | ¥1.5 |
| Qwen3.8-Flash | ¥0.8 | ¥2.7 | ¥0.1 |
| Qwen3.8-2.4T-A95B | ¥12 | ¥36 | ¥1.5 |
| Qwen3.8-27B | ¥3 | ¥12 | ¥0.6 |

> [!warning]
> 官方博客发布时写的是 Flash 输入 ¥1、输出 ¥3；模型市场当前显示 ¥0.8 / ¥2.7。价格是动态产品信息，后续引用应以模型市场实时值为准，并保留抓取日期。

## 我对产品线的判断

Qwen3.8 把同一代模型拆成三类工程约束：

1. **能力上限**：Max / 2.4T-A95B 用 2.4T 总容量承接长程专业任务。
2. **服务 Pareto**：Flash 通过 6B active、QSA、N-gram embedding 和 1M serving 面向高并发 agent。
3. **私有部署**：27B Dense 保留多模态与工具能力，让单机或小集群部署不必承担超大 MoE 的通信复杂度。

这比按“文本模型 / 多模态模型”分目录更有解释力：同一正代家族内部已经原生多模态，真正的支线边界应看它是否形成独立任务路线和独立命名体系。

## 官方资料

- [[src/00_Source_Index|Qwen3.8 官方资料索引]]
- [[src/01_Qwen3.8-Flash - Qianwen AI|Qwen3.8-Flash 模型市场页]]
- [[src/02_Qwen3.8-Max - Qianwen AI|Qwen3.8-Max 模型市场页]]
- [[src/03_Qwen3.8-2.4T-A95B - Qianwen AI|Qwen3.8-2.4T-A95B 模型市场页]]
- [[src/04_Qwen3.8-27B - Qianwen AI|Qwen3.8-27B 模型市场页]]
- [[src/05_Qwen3.8-Flash-Next - Official Blog|Qwen3.8-Flash-Next 官方技术博客]]
- [[src/06_Qwen3.8-Flash-Next - Hugging Face|官方开放权重模型卡]]

