---
title: "FrogNano"
type: model-note
year: 2026
release: "2026-09-22"
url: "https://huggingface.co/microsoft/FrogNano-4B-2609"
tags: [model-note, base-model, microsoft]
status: reading
topic: "13_base_model"
created: 2026-10-13
updated: 2026-10-13
---

# FrogNano

> [!tldr]
> 4B级仓库Agent，以TaskPilot合成并校准任务做纯RL；不使用强模型解题轨迹作行为蒸馏。 TaskPilot共同生成问题、参考patch和测试，先验证原仓库测试失败而参考patch通过，再用当前策略筛出既有成功也有失败的任务。五轮RL让任务难度跟随策略，Leaf五工具负责完整多轮环境交互。

![研读链路整理示意](src/assets/reading-map.svg)

## 一页速览

| 项目 | 当前证据 |
|---|---|
| 日期 | 2026-09-22  |
| 归属 | microsoft · 专项支线 |
| 关键事实1 | 约4.66B；32层混合架构 |
| 关键事实2 | 约1500合成SWE任务 |
| 关键事实3 | SWE-bench Verified Avg@3 61.5% |

## TaskPilot：环境生成与行为蒸馏不是同一件事

任务作者会生成问题、参考patch和隐藏测试，但FrogNano的RL不以强模型动作、推理或patch作为行为目标。约1500个任务经过可执行验证和当前policy校准：fail-to-pass必须原始仓库失败、参考修复通过，pass-to-pass保持原有行为，最终保留mixed-success任务供RL学习。

## 五轮迭代必须与预算变化一起读

| 模型阶段 | SWE-bench Verified Avg@3 |
|---|---:|
| Qwen3.5-4B基础checkpoint | 39.4% |
| RL轮1 / 2 / 3 | 49.1% / 53.1% / 56.7% |
| RL轮4 / 5 | 59.1% / 61.5% |

前四轮65,536context、75turns，第五轮约131K、150turns，因此不能把全部增益归给任务校准算法。Verified500题作为validation，不应称为独立held-out测试。真正held-out为Pro731题、TB2.0的89题、PatchEval230个CVE案例，Avg@3分别37.6%、31.1%、47.3%。

Avg@3是三个seed平均单次成功率；Pass@3是三次至少一次成功，Verified71.0%、Pro47.6%，两者不能互换。

## 紧凑模型也有系统前提

约4.66B、32层GatedDeltaNet/gated-attention，继承视觉组件但没有进行多模态专项训练和评测，不能宣称可支持图片/视频。Leaf五工具在隔离仓库中读写、编辑、搜索和运行测试；输出无tool call才结束。模型产出候选patch，不直接部署生产。

授权存在需要核对的矛盾：README frontmatter写MIT，正文许可栏写Apache2.0。本文不替官方消除矛盾，实际使用前需核验LICENSE与upstream通知。正文“1B–1T训练token”也是宽泛披露区间，不将其改成具体精确训练量。

> [!warning] 阅读范围
> 已读model card全部方法、评测与限制，保存报告入口但未完成technical report全文源码精读。测试通过不意味着安全，也没有独立泛化、多语言和完整内容安全验证。

## 对 Agent Training 的判断

> [!insight]
> 关键不是不使用教师，而是不蒸馏教师的解题轨迹：任务作者仍可生成环境。验证集选模与held-out测试必须分开，记录训练任务校准通过率、测试完备性和越权补丁。

以上是基于已读材料的研究判断，未在本机复现模型推理或训练结果。

## 官方来源与导航

- [S1] [HF Model Card](https://huggingface.co/microsoft/FrogNano-4B-2609)
- [S2] [Tech Report](https://aka.ms/frognano-tech-report)

- [[src/retrieval_manifest.json|原始抓取记录]]
- [[frognano_poster_zh.html|中文Poster]]
- [[Topics/13_base_model/Base Model MOC|基模主题索引]]

> 📊 相关可视化: [[frognano_poster_zh.html|中文研究Poster]]
