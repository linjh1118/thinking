---
title: "GLM-OCR Technical Report"
type: paper
authors: ["Shuaiqi Duan", "Yadong Xue", "Weihan Wang", "Zhe Su", "Huan Liu", "Sheng Yang", "Guobing Gan", "Guo Wang", "Zihan Wang", "Shengdong Yan", "Dexin Jin", "Yuxuan Zhang", "Guohong Wen", "Yanfeng Wang", "Yutao Zhang", "Xiaohan Zhang", "Wenyi Hong", "Yukuo Cen", "Da Yin", "Bin Chen", "Wenmeng Yu", "Xiaotao Gu", "Jie Tang"]
year: 2026
venue: arXiv
arxiv: "2603.10910"
url: "https://arxiv.org/abs/2603.10910"
tags: [paper, glm, ocr, document-understanding, multimodal]
topic: "13_base_model"
status: read
rating: 4
created: 2026-05-30
---

# TL;DR

GLM-OCR 是一个 **0.9B 参数**的轻量级多模态 OCR 模型（CogViT 0.4B 视觉编码器 + GLM 0.5B 语言解码器），通过 **Multi-Token Prediction (MTP)** 实现 50% 吞吐量提升；在 OmniDocBench v1.5 上达到 **94.6 分（第一）**，在表格、公式、印章等复杂文档任务上超越 Qwen3-VL-235B 和 Gemini-3-Pro。

## 问题与动机

现有 MLLM（如 Qwen3-VL）在文档理解上已很强，但大模型尺寸 + autoregressive 解码导致高计算成本、慢推理、大内存消耗，难以在高频并发或边缘环境部署。核心挑战是：**在保持 SOTA 性能的同时，将模型压缩到可部署的规模，并解决 OCR 任务与 LLM 生成范式的本质不匹配**。

OCR 任务是确定性的，有强局部依赖和显式结构监督，token-by-token autoregressive 解码是不必要且低效的。

## 方法核心思路

### 架构：CogViT + GLM + MTP
- **Vision Encoder**: CogViT (0.4B)，大规模图文数据预训练
- **LLM Decoder**: GLM (0.5B)
- **Multi-Token Prediction (MTP)**：训练时每步预测 10 token，推理时平均每步生成 5.2 token，≈50% 吞吐量提升；通过参数共享控制额外 GPU 内存开销

### 两阶段 Pipeline
1. **PP-DocLayout-V3**：布局分析，将文档分为段落/表格/公式等语义区域
2. **并行区域级识别**：各区域独立送入 GLM-OCR Core 并行处理

### 统一生成框架
Document Parsing 和 Key Information Extraction (KIE) 被统一为条件结构化生成：
- Parsing：输出 Markdown / JSON
- KIE：基于 prompt 提取特定字段 JSON

### 训练阶段

| Stage | Phase | Data |
|-------|-------|------|
| 1 | Vision Encoder Training | 图文对 + grounding/retrieval，MIM+CLIP 目标，ViT 蒸馏 |
| 2.1 | Pretrain (无 MTP) | 图文对 + 文档解析 + grounding + VQA |
| 2.2 | Pretrain with MTP | 文档解析 + grounding + VQA |
| 3 | SFT with MTP | 文本/公式/表格识别 + KIE |
| 4 | RL (GRPO) | 文本/公式/表格识别 + KIE |

### RL Reward 设计（Stage 4）

| Task | Primary Reward | Additional |
|------|---------------|------------|
| Text Recognition | Normalized Edit Distance | Repetition penalty |
| Formula Recognition | CDM score | Structural validity check |
| Table Recognition | TEDS score | Tag closure, structural parsing |
| KIE | Field-level F1 | JSON parse validation, missing/duplicate penalty |
| Global | - | Repetition ratio penalty, malformed structure penalty |

## 关键结果

### OmniDocBench v1.5

| Model | Params | Overall |
|-------|--------|---------|
| **GLM-OCR** | 0.9B | **94.62** |
| PaddleOCR-VL-1.5 | - | 94.50 |
| Qwen3-VL-235B | 235B | 89.15 |
| Gemini-3 Pro | - | 90.33 |
| MinerU 2.5 | - | 90.67 |

GLM-OCR **0.9B 超越 235B 和 Gemini-3 Pro**，尤其在表格任务上最强（Table_TEDS: 93.96, Table_TEDS-S: 96.39）。

### 其他公开 Benchmark

| Benchmark | GLM-OCR Score |
|-----------|--------------|
| OCRBench (Text) | 94.0 |
| UniMERNet | 96.5 |
| PubTabNet | 85.2 |
| TEDS_TEST | 86.0 |
| Nanonets-KIE | 93.7 |
| Handwritten-KIE | 86.1 |

### 工业场景

| Task | Score |
|------|-------|
| Real-world Table | 91.5 |
| Seal Recognition | 90.5 |
| Receipt KIE | 94.5 |
| Code Document | 84.7 |
| Multilingual Text | 69.3 |

## 对研究的启发

> [!insight]
> 1. **MTP 对结构化输出的价值**：不仅提升 throughput（50%），更重要的是改善局部结构连贯性（减少"broken tags"），对需要生成结构化输出的任务（JSON/HTML/代码）都有借鉴意义
> 2. **两阶段 pipeline 范式**：Layout Analysis → Parallel Recognition 分解了复杂布局问题，对小模型尤其重要。这对 GUI Agent 也有参考：先做 UI 结构解析再分别处理各区域
> 3. **0.9B 超越 235B 的启示**：专用轻量模型 + MTP + 两阶段设计可以在文档理解这种结构化任务上击败通用大模型。类似思路可用于 GUI Agent 的边缘部署
> 4. **RL reward 设计**：TEDS/normalized edit distance 等已有 metric 作为 reward signal 是可行的，值得在结构化输出任务中迁移

## 相关链接
- 论文: [arXiv 2603.10910](https://arxiv.org/abs/2603.10910)
- 源码: [github.com/zai-org/GLM-OCR](https://github.com/zai-org/GLM-OCR)
- Demo: [ocr.z.ai](https://ocr.z.ai/)
