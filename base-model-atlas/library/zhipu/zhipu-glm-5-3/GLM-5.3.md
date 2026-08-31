---
title: "GLM-5.3 — Model Overview"
type: model-note
year: 2026
url: "https://docs.z.ai/guides/llm/glm-5.3"
tags: [model-note, base-model, zhipu]
status: read
created: 2026-08-31
updated: 2026-08-31
---

# GLM-5.3 — Model Overview

> [!tldr]
> 沿用 GLM-5.2 base，以 post-training 把复杂软件工程、长时程 agent 与网络安全能力继续推高；1M context、128K max output。

## 谱系定位

- 团队：**Zhipu · GLM**
- 时间：**2026-08**
- Atlas 归类：**主干正代**
- 一手证据：[Official docs](https://docs.z.ai/guides/llm/glm-5.3)

## 核心变化

沿用 GLM-5.2 base，以 post-training 把复杂软件工程、长时程 agent 与网络安全能力继续推高；1M context、128K max output。

这个节点单独收录，是因为官方把它作为可独立识别的模型 / family 发布；同一 family 内的参数尺寸、服务档位和 dated API snapshot 不再重复拆叶子。

## 阅读判断

- 与前代比较时，优先看架构、数据、post-training 与工具环境四类变化。
- 官方未披露的参数、训练数据和消融不作推断。
- 若该节点是专项模型，应沿团队主干理解其能力迁移，而不是把它误写成新的通用正代。

## 一手资料

- [https://docs.z.ai/guides/llm/glm-5.3](https://docs.z.ai/guides/llm/glm-5.3)
- [[src/Official Source|本地官方来源摘录]]

## 导航

- [[Topics/13_base_model/Base_Model_Top8_Branch_Audit_2026|Top 8 支线审计]]
