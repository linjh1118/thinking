---
title: "DeepSeek-V3-0324 — Model Overview"
type: model-note
year: 2025
url: "https://api-docs.deepseek.com/news/news250325/"
tags: [model-note, base-model, deepseek]
status: read
created: 2026-08-31
updated: 2026-08-31
---

# DeepSeek-V3-0324 — Model Overview

> [!tldr]
> 替换线上 deepseek-chat 的 V3 主 checkpoint，显著增强推理、前端、工具调用、中文写作与搜索。

## 谱系定位

- 团队：**DeepSeek AI**
- 时间：**2025-03**
- Atlas 归类：**主干正代**
- 一手证据：[Official docs](https://api-docs.deepseek.com/news/news250325/)

## 核心变化

替换线上 deepseek-chat 的 V3 主 checkpoint，显著增强推理、前端、工具调用、中文写作与搜索。

这个节点单独收录，是因为官方把它作为可独立识别的模型 / family 发布；同一 family 内的参数尺寸、服务档位和 dated API snapshot 不再重复拆叶子。

## 阅读判断

- 与前代比较时，优先看架构、数据、post-training 与工具环境四类变化。
- 官方未披露的参数、训练数据和消融不作推断。
- 若该节点是专项模型，应沿团队主干理解其能力迁移，而不是把它误写成新的通用正代。

## 一手资料

- [https://api-docs.deepseek.com/news/news250325/](https://api-docs.deepseek.com/news/news250325/)
- [[src/Official Source|本地官方来源摘录]]

## 导航

- [[Topics/13_base_model/Base_Model_Top8_Branch_Audit_2026|Top 8 支线审计]]
