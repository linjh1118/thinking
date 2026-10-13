---
title: "StepAudio 3"
type: model-note
release: "2026-09-15"
year: 2026
url: "https://static.stepfun.com/blog/stepaudio3/realtime/"
tags: [model-note, base-model, stepfun]
topic: "13_base_model"
status: read
created: 2026-10-13
updated: 2026-10-13
---

# StepAudio 3

> [!tldr]
> Realtime、ASR、TTS、Gen、Music 共用一个 family 节点；全双工对话与统一音频生成。 语音家族需要分别评测识别、对话时序和生成，不把五个接口理解为五个通用正代。Realtime 将听、说、推理和工具执行放进连续交互；Gen 统一语音、音乐和环境声，Music 强调乐曲结构规划。

![研读路径：整理示意，不代表未公开架构](src/assets/reading-map.svg)

## 一页速览

| 维度 | 当前证据 |
|---|---|
| 发布时间 | 2026-09-15 |
| 类型 | 专项支线 / family · Speech / Audio |
| 关键事实 1 | Realtime：AA Full-Duplex 98.9 |
| 关键事实 2 | τ-Voice：56.0 |
| 关键事实 3 | ASR Max：LibriSpeech clean WER 1.18% |
| 检查日期 | 2026-10-13；官方原始资料在同级src/ |

## 五种专项能力，共用一个发布阶段

9月15日官方新闻宣布Realtime、ASR、TTS、Gen、Music，全部收录同一family。语音识别、全双工对话和生成的指标不同，不用某个第一名宣传覆盖全部路线。

| 路线 | 任务 | 当前可核对证据 |
|---|---|---|
| Realtime | 连续听说、边思考边发声、工具执行 | 官方详情与语音实验室 |
| ASR | 实时/批量转写 | ASR Max评测，不冒充全部ASR配置 |
| TTS | 可控声音合成 | 官方模型页 |
| Gen | 语音、环境声、音乐混合生成 | arXiv2609.12945 |
| Music | 长音乐与结构规划 | arXiv2609.16034 |

## 实时对话不能只测语音识别

官方Realtime页列AA Full-Duplex98.9、τ-Voice56.0；其余音频理解AudioMultiChallenge49.3、MMSU90.6、MMAR86.5。前者检查交互，τ-Voice检查语音Agent，后三者关注理解，各有不同题目和单位。

ASR Max的LibriSpeech clean WER1.18%、WenetSpeech meeting4.35%、AISHELL1 0.49%。不能把干净英语集合错误率推广到多语种会议。实验室排行榜页面会变化，应保留抓取日期，而非宣称永久第一。

## 统一生成和任务工具仍要分别验收

Gen可组合说话、音效与音乐，Music强调显式段落与编排规划；文本提示正确不保证音频时间线、发音和音乐结构都正确。Voice Agent还需验收打断恢复、错误意图确认和执行状态，不以“更像真人”代替任务成功率。

> [!warning] 资料阅读范围
> 已读官方Realtime与模型页、报告摘要，保存报告链接；Gen/Music全文尚未完成源码精读，TTS/ASR的完整训练配方尚未获得。当前笔记因此不达到全部子模型的GLM式架构精读深度。

## 对 Agent Training 的启发

> [!insight]
> 对 Voice Agent，工具成功率与打断处理应同时验收；ASR 的 WER、说话人分离和任务完成率是不同指标。保留实时模式和离线模式，不用一个总分盖过全部子能力。

以上是基于已读官方资料的研究判断，不是官方保证，也没有在本机运行模型推理或复现论文成绩。下一步优先补独立验证器、固定任务/版本和完整失败轨迹，避免只保存最好样例。

## 一手资料与导航

- [S1] [Tech Blog](https://static.stepfun.com/blog/stepaudio3/realtime/)
- [S2] [官方模型页](https://audio.stepfun.ai/)
- [S3] [Tech Report · Gen](https://arxiv.org/abs/2609.12945)
- [S4] [Tech Report · Music](https://arxiv.org/abs/2609.16034)
- [S5] [官方发布记录](https://www.stepfun.com/news)

原始下载文件与SHA-256见 [[src/retrieval_manifest.json|抓取记录]]。报告保留链接，不抓PDF；动态网页响应若只有壳文件，不将其标成完整离线正文。

- [[Topics/13_base_model/Base Model MOC|基模主题索引]]
- [[stepaudio-3_poster_zh.html|中文Poster]]

> 📊 相关可视化: [[stepaudio-3_poster_zh.html|StepAudio 3 中文Poster]]
