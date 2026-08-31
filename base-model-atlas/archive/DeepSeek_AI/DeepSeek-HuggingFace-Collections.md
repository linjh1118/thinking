---
title: "DeepSeek Hugging Face Collections Audit"
type: source-index
publisher: "DeepSeek AI on Hugging Face"
retrieved: 2026-09-01
---

# DeepSeek Hugging Face Collections 全量对账

> [!tldr]
> 本地归档以 DeepSeek 官方 Hugging Face organization 的 collections 为完整性边界。API 只用于列清单；正文资料一律保存各模型仓库原始 `README.md` model card。

- 官方入口：[deepseek-ai/collections](https://huggingface.co/deepseek-ai/collections)
- Collection 数：**19**
- 官方模型仓库数：**70**
- 已归档原始 model card：**64**
- 官方仓库无 model card：**6**（清单中显式标注，不以 API 文档冒充）
- 归档规则：同一正代的 Base / Chat / Lite / 参数尺寸共享 family 目录；不会伪装成新的正代。

## DeepSeek-V4

- Collection: [deepseek-ai/deepseek-v4-69ea2d6001aafa84d4d6f6f9](https://huggingface.co/collections/deepseek-ai/deepseek-v4-69ea2d6001aafa84d4d6f6f9)
- 官方模型仓库：**9**

  - [deepseek-ai/DeepSeek-V4-Flash-Base](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash-Base) → **官方仓库没有 README/model card**
  - [deepseek-ai/DeepSeek-V4-Flash](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/raw/main/README.md) → `DeepSeek_AI/2604_deepseek_v4/src/huggingface_model_cards/DeepSeek-V4-Flash.md`
  - [deepseek-ai/DeepSeek-V4-Pro-Base](https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro-Base) → **官方仓库没有 README/model card**
  - [deepseek-ai/DeepSeek-V4-Pro](https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro/raw/main/README.md) → `DeepSeek_AI/2604_deepseek_v4/src/huggingface_model_cards/DeepSeek-V4-Pro.md`
  - [deepseek-ai/DeepSeek-V4-Flash-DSpark](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash-DSpark/raw/main/README.md) → `DeepSeek_AI/2604_deepseek_v4/src/huggingface_model_cards/DeepSeek-V4-Flash-DSpark.md`
  - [deepseek-ai/DeepSeek-V4-Pro-DSpark](https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro-DSpark/raw/main/README.md) → `DeepSeek_AI/2604_deepseek_v4/src/huggingface_model_cards/DeepSeek-V4-Pro-DSpark.md`
  - [deepseek-ai/DeepSeek-V4-Flash-0731](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash-0731/raw/main/README.md) → `DeepSeek_AI/2604_deepseek_v4/src/huggingface_model_cards/DeepSeek-V4-Flash-0731.md`
  - [deepseek-ai/DeepSeek-V4-Pro-0813](https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro-0813/raw/main/README.md) → `DeepSeek_AI/2604_deepseek_v4/src/huggingface_model_cards/DeepSeek-V4-Pro-0813.md`
  - [deepseek-ai/DeepSeek-V4-Flash-Vision-Exp](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash-Vision-Exp/raw/main/README.md) → `DeepSeek_AI/2604_deepseek_v4/src/huggingface_model_cards/DeepSeek-V4-Flash-Vision-Exp.md`

## DeepSpec

- Collection: [deepseek-ai/deepspec-6a410e3f1831ca8ca801b88b](https://huggingface.co/collections/deepseek-ai/deepspec-6a410e3f1831ca8ca801b88b)
- 官方模型仓库：**4**

  - [deepseek-ai/dspark_qwen3_4b_block7](https://huggingface.co/deepseek-ai/dspark_qwen3_4b_block7) → **官方仓库没有 README/model card**
  - [deepseek-ai/dspark_qwen3_8b_block7](https://huggingface.co/deepseek-ai/dspark_qwen3_8b_block7) → **官方仓库没有 README/model card**
  - [deepseek-ai/dspark_qwen3_14b_block7](https://huggingface.co/deepseek-ai/dspark_qwen3_14b_block7) → **官方仓库没有 README/model card**
  - [deepseek-ai/dspark_gemma4_12b_block7](https://huggingface.co/deepseek-ai/dspark_gemma4_12b_block7) → **官方仓库没有 README/model card**

## DeepSeek-V3.1

- Collection: [deepseek-ai/deepseek-v31-68a491bed32bd77e7fca048f](https://huggingface.co/collections/deepseek-ai/deepseek-v31-68a491bed32bd77e7fca048f)
- 官方模型仓库：**3**

  - [deepseek-ai/DeepSeek-V3.1-Base](https://huggingface.co/deepseek-ai/DeepSeek-V3.1-Base/raw/main/README.md) → `DeepSeek_AI/2508_deepseek_v3_1/src/huggingface_model_cards/DeepSeek-V3.1-Base.md`
  - [deepseek-ai/DeepSeek-V3.1](https://huggingface.co/deepseek-ai/DeepSeek-V3.1/raw/main/README.md) → `DeepSeek_AI/2508_deepseek_v3_1/src/huggingface_model_cards/DeepSeek-V3.1.md`
  - [deepseek-ai/DeepSeek-V3.1-Terminus](https://huggingface.co/deepseek-ai/DeepSeek-V3.1-Terminus/raw/main/README.md) → `DeepSeek_AI/2509_deepseek_v3_1_terminus/src/huggingface_model_cards/DeepSeek-V3.1-Terminus.md`

## DeepSeek-LLM

- Collection: [deepseek-ai/deepseek-llm-65f2964ad8a0a29fe39b71d8](https://huggingface.co/collections/deepseek-ai/deepseek-llm-65f2964ad8a0a29fe39b71d8)
- 官方模型仓库：**4**

  - [deepseek-ai/deepseek-llm-67b-chat](https://huggingface.co/deepseek-ai/deepseek-llm-67b-chat/raw/main/README.md) → `DeepSeek_AI/2401_deepseek_llm/src/huggingface_model_cards/deepseek-llm-67b-chat.md`
  - [deepseek-ai/deepseek-llm-7b-chat](https://huggingface.co/deepseek-ai/deepseek-llm-7b-chat/raw/main/README.md) → `DeepSeek_AI/2401_deepseek_llm/src/huggingface_model_cards/deepseek-llm-7b-chat.md`
  - [deepseek-ai/deepseek-llm-67b-base](https://huggingface.co/deepseek-ai/deepseek-llm-67b-base/raw/main/README.md) → `DeepSeek_AI/2401_deepseek_llm/src/huggingface_model_cards/deepseek-llm-67b-base.md`
  - [deepseek-ai/deepseek-llm-7b-base](https://huggingface.co/deepseek-ai/deepseek-llm-7b-base/raw/main/README.md) → `DeepSeek_AI/2401_deepseek_llm/src/huggingface_model_cards/deepseek-llm-7b-base.md`

## DeepSeek-Coder

- Collection: [deepseek-ai/deepseek-coder-65f295d7d8a0a29fe39b4ec4](https://huggingface.co/collections/deepseek-ai/deepseek-coder-65f295d7d8a0a29fe39b4ec4)
- 官方模型仓库：**4**

  - [deepseek-ai/deepseek-coder-33b-instruct](https://huggingface.co/deepseek-ai/deepseek-coder-33b-instruct/raw/main/README.md) → `DeepSeek_AI/Variants/2311_deepseek_coder/src/huggingface_model_cards/deepseek-coder-33b-instruct.md`
  - [deepseek-ai/deepseek-coder-6.7b-instruct](https://huggingface.co/deepseek-ai/deepseek-coder-6.7b-instruct/raw/main/README.md) → `DeepSeek_AI/Variants/2311_deepseek_coder/src/huggingface_model_cards/deepseek-coder-6.7b-instruct.md`
  - [deepseek-ai/deepseek-coder-7b-instruct-v1.5](https://huggingface.co/deepseek-ai/deepseek-coder-7b-instruct-v1.5/raw/main/README.md) → `DeepSeek_AI/Variants/2311_deepseek_coder/src/huggingface_model_cards/deepseek-coder-7b-instruct-v1.5.md`
  - [deepseek-ai/deepseek-coder-1.3b-instruct](https://huggingface.co/deepseek-ai/deepseek-coder-1.3b-instruct/raw/main/README.md) → `DeepSeek_AI/Variants/2311_deepseek_coder/src/huggingface_model_cards/deepseek-coder-1.3b-instruct.md`

## DeepSeek-OCR

- Collection: [deepseek-ai/deepseek-ocr-69809076528a753251417fbd](https://huggingface.co/collections/deepseek-ai/deepseek-ocr-69809076528a753251417fbd)
- 官方模型仓库：**2**

  - [deepseek-ai/DeepSeek-OCR](https://huggingface.co/deepseek-ai/DeepSeek-OCR/raw/main/README.md) → `DeepSeek_AI/Variants/2510_deepseek_ocr/src/huggingface_model_cards/DeepSeek-OCR.md`
  - [deepseek-ai/DeepSeek-OCR-2](https://huggingface.co/deepseek-ai/DeepSeek-OCR-2/raw/main/README.md) → `DeepSeek_AI/Variants/2601_deepseek_ocr2/src/huggingface_model_cards/DeepSeek-OCR-2.md`

## DeepSeek-V3.2

- Collection: [deepseek-ai/deepseek-v32-68da2f317324c70047c28f66](https://huggingface.co/collections/deepseek-ai/deepseek-v32-68da2f317324c70047c28f66)
- 官方模型仓库：**4**

  - [deepseek-ai/DeepSeek-V3.2-Exp](https://huggingface.co/deepseek-ai/DeepSeek-V3.2-Exp/raw/main/README.md) → `DeepSeek_AI/2509_deepseek_v3_2_exp/src/huggingface_model_cards/DeepSeek-V3.2-Exp.md`
  - [deepseek-ai/DeepSeek-V3.2-Exp-Base](https://huggingface.co/deepseek-ai/DeepSeek-V3.2-Exp-Base/raw/main/README.md) → `DeepSeek_AI/2509_deepseek_v3_2_exp/src/huggingface_model_cards/DeepSeek-V3.2-Exp-Base.md`
  - [deepseek-ai/DeepSeek-V3.2](https://huggingface.co/deepseek-ai/DeepSeek-V3.2/raw/main/README.md) → `DeepSeek_AI/2512_deepseek_v3_2/src/huggingface_model_cards/DeepSeek-V3.2.md`
  - [deepseek-ai/DeepSeek-V3.2-Speciale](https://huggingface.co/deepseek-ai/DeepSeek-V3.2-Speciale/raw/main/README.md) → `DeepSeek_AI/2512_deepseek_v3_2/src/huggingface_model_cards/DeepSeek-V3.2-Speciale.md`

## DeepSeek-V3

- Collection: [deepseek-ai/deepseek-v3-676bc4546fb4876383c4208b](https://huggingface.co/collections/deepseek-ai/deepseek-v3-676bc4546fb4876383c4208b)
- 官方模型仓库：**3**

  - [deepseek-ai/DeepSeek-V3-Base](https://huggingface.co/deepseek-ai/DeepSeek-V3-Base/raw/main/README.md) → `DeepSeek_AI/2412_deepseek_v3/src/huggingface_model_cards/DeepSeek-V3-Base.md`
  - [deepseek-ai/DeepSeek-V3](https://huggingface.co/deepseek-ai/DeepSeek-V3/raw/main/README.md) → `DeepSeek_AI/2412_deepseek_v3/src/huggingface_model_cards/DeepSeek-V3.md`
  - [deepseek-ai/DeepSeek-V3-0324](https://huggingface.co/deepseek-ai/DeepSeek-V3-0324/raw/main/README.md) → `DeepSeek_AI/2503_deepseek_v3_0324/src/huggingface_model_cards/DeepSeek-V3-0324.md`

## DeepSeek-VL2

- Collection: [deepseek-ai/deepseek-vl2-675c22accc456d3beb4613ab](https://huggingface.co/collections/deepseek-ai/deepseek-vl2-675c22accc456d3beb4613ab)
- 官方模型仓库：**3**

  - [deepseek-ai/deepseek-vl2-tiny](https://huggingface.co/deepseek-ai/deepseek-vl2-tiny/raw/main/README.md) → `DeepSeek_AI/Variants/2412_deepseek_vl2/src/huggingface_model_cards/deepseek-vl2-tiny.md`
  - [deepseek-ai/deepseek-vl2-small](https://huggingface.co/deepseek-ai/deepseek-vl2-small/raw/main/README.md) → `DeepSeek_AI/Variants/2412_deepseek_vl2/src/huggingface_model_cards/deepseek-vl2-small.md`
  - [deepseek-ai/deepseek-vl2](https://huggingface.co/deepseek-ai/deepseek-vl2/raw/main/README.md) → `DeepSeek_AI/Variants/2412_deepseek_vl2/src/huggingface_model_cards/deepseek-vl2.md`

## Janus

- Collection: [deepseek-ai/janus-6711d145e2b73d369adfd3cc](https://huggingface.co/collections/deepseek-ai/janus-6711d145e2b73d369adfd3cc)
- 官方模型仓库：**3**

  - [deepseek-ai/Janus-Pro-7B](https://huggingface.co/deepseek-ai/Janus-Pro-7B/raw/main/README.md) → `DeepSeek_AI/Variants/2501_janus_pro/src/huggingface_model_cards/Janus-Pro-7B.md`
  - [deepseek-ai/Janus-Pro-1B](https://huggingface.co/deepseek-ai/Janus-Pro-1B/raw/main/README.md) → `DeepSeek_AI/Variants/2501_janus_pro/src/huggingface_model_cards/Janus-Pro-1B.md`
  - [deepseek-ai/Janus-1.3B](https://huggingface.co/deepseek-ai/Janus-1.3B/raw/main/README.md) → `DeepSeek_AI/Variants/2410_janus/src/huggingface_model_cards/Janus-1.3B.md`

## DeepSeek-V2.5

- Collection: [deepseek-ai/deepseek-v25-66d97550c81167fc5e5e32e6](https://huggingface.co/collections/deepseek-ai/deepseek-v25-66d97550c81167fc5e5e32e6)
- 官方模型仓库：**2**

  - [deepseek-ai/DeepSeek-V2.5](https://huggingface.co/deepseek-ai/DeepSeek-V2.5/raw/main/README.md) → `DeepSeek_AI/2409_deepseek_v2_5/src/huggingface_model_cards/DeepSeek-V2.5.md`
  - [deepseek-ai/DeepSeek-V2.5-1210](https://huggingface.co/deepseek-ai/DeepSeek-V2.5-1210/raw/main/README.md) → `DeepSeek_AI/2412_deepseek_v2_5_1210/src/huggingface_model_cards/DeepSeek-V2.5-1210.md`

## DeepSeek-Prover

- Collection: [deepseek-ai/deepseek-prover-66beb212ae70890c90f24176](https://huggingface.co/collections/deepseek-ai/deepseek-prover-66beb212ae70890c90f24176)
- 官方模型仓库：**3**

  - [deepseek-ai/DeepSeek-Prover-V2-671B](https://huggingface.co/deepseek-ai/DeepSeek-Prover-V2-671B/raw/main/README.md) → `DeepSeek_AI/Variants/2504_deepseek_prover_v2/src/huggingface_model_cards/DeepSeek-Prover-V2-671B.md`
  - [deepseek-ai/DeepSeek-Prover-V2-7B](https://huggingface.co/deepseek-ai/DeepSeek-Prover-V2-7B/raw/main/README.md) → `DeepSeek_AI/Variants/2504_deepseek_prover_v2/src/huggingface_model_cards/DeepSeek-Prover-V2-7B.md`
  - [deepseek-ai/DeepSeek-Prover-V1.5-Base](https://huggingface.co/deepseek-ai/DeepSeek-Prover-V1.5-Base/raw/main/README.md) → `DeepSeek_AI/Variants/2408_deepseek_prover_v1_5/src/huggingface_model_cards/DeepSeek-Prover-V1.5-Base.md`

## ESFT

- Collection: [deepseek-ai/esft-669a1e800bc10b3460569c70](https://huggingface.co/collections/deepseek-ai/esft-669a1e800bc10b3460569c70)
- 官方模型仓库：**4**

  - [deepseek-ai/ESFT-vanilla-lite](https://huggingface.co/deepseek-ai/ESFT-vanilla-lite/raw/main/README.md) → `DeepSeek_AI/Variants/2407_esft/src/huggingface_model_cards/ESFT-vanilla-lite.md`
  - [deepseek-ai/ESFT-token-law-lite](https://huggingface.co/deepseek-ai/ESFT-token-law-lite/raw/main/README.md) → `DeepSeek_AI/Variants/2407_esft/src/huggingface_model_cards/ESFT-token-law-lite.md`
  - [deepseek-ai/ESFT-token-summary-lite](https://huggingface.co/deepseek-ai/ESFT-token-summary-lite/raw/main/README.md) → `DeepSeek_AI/Variants/2407_esft/src/huggingface_model_cards/ESFT-token-summary-lite.md`
  - [deepseek-ai/ESFT-token-code-lite](https://huggingface.co/deepseek-ai/ESFT-token-code-lite/raw/main/README.md) → `DeepSeek_AI/Variants/2407_esft/src/huggingface_model_cards/ESFT-token-code-lite.md`

## DeepSeek-V2

- Collection: [deepseek-ai/deepseek-v2-669a1c8b8f2dbc203fbd7746](https://huggingface.co/collections/deepseek-ai/deepseek-v2-669a1c8b8f2dbc203fbd7746)
- 官方模型仓库：**4**

  - [deepseek-ai/DeepSeek-V2-Chat-0628](https://huggingface.co/deepseek-ai/DeepSeek-V2-Chat-0628/raw/main/README.md) → `DeepSeek_AI/2405_deepseek_v2/src/huggingface_model_cards/DeepSeek-V2-Chat-0628.md`
  - [deepseek-ai/DeepSeek-V2-Chat](https://huggingface.co/deepseek-ai/DeepSeek-V2-Chat/raw/main/README.md) → `DeepSeek_AI/2405_deepseek_v2/src/huggingface_model_cards/DeepSeek-V2-Chat.md`
  - [deepseek-ai/DeepSeek-V2](https://huggingface.co/deepseek-ai/DeepSeek-V2/raw/main/README.md) → `DeepSeek_AI/2405_deepseek_v2/src/huggingface_model_cards/DeepSeek-V2.md`
  - [deepseek-ai/DeepSeek-V2-Lite](https://huggingface.co/deepseek-ai/DeepSeek-V2-Lite/raw/main/README.md) → `DeepSeek_AI/2405_deepseek_v2/src/huggingface_model_cards/DeepSeek-V2-Lite.md`

## DeepSeekCoder-V2

- Collection: [deepseek-ai/deepseekcoder-v2-666bf4b274a5f556827ceeca](https://huggingface.co/collections/deepseek-ai/deepseekcoder-v2-666bf4b274a5f556827ceeca)
- 官方模型仓库：**4**

  - [deepseek-ai/DeepSeek-Coder-V2-Instruct](https://huggingface.co/deepseek-ai/DeepSeek-Coder-V2-Instruct/raw/main/README.md) → `DeepSeek_AI/Variants/2406_deepseek_coder_v2/src/huggingface_model_cards/DeepSeek-Coder-V2-Instruct.md`
  - [deepseek-ai/DeepSeek-Coder-V2-Base](https://huggingface.co/deepseek-ai/DeepSeek-Coder-V2-Base/raw/main/README.md) → `DeepSeek_AI/Variants/2406_deepseek_coder_v2/src/huggingface_model_cards/DeepSeek-Coder-V2-Base.md`
  - [deepseek-ai/DeepSeek-Coder-V2-Lite-Base](https://huggingface.co/deepseek-ai/DeepSeek-Coder-V2-Lite-Base/raw/main/README.md) → `DeepSeek_AI/Variants/2406_deepseek_coder_v2/src/huggingface_model_cards/DeepSeek-Coder-V2-Lite-Base.md`
  - [deepseek-ai/DeepSeek-Coder-V2-Lite-Instruct](https://huggingface.co/deepseek-ai/DeepSeek-Coder-V2-Lite-Instruct/raw/main/README.md) → `DeepSeek_AI/Variants/2406_deepseek_coder_v2/src/huggingface_model_cards/DeepSeek-Coder-V2-Lite-Instruct.md`

## DeepSeek-MoE

- Collection: [deepseek-ai/deepseek-moe-65f29679f5cf26fe063686bf](https://huggingface.co/collections/deepseek-ai/deepseek-moe-65f29679f5cf26fe063686bf)
- 官方模型仓库：**2**

  - [deepseek-ai/deepseek-moe-16b-base](https://huggingface.co/deepseek-ai/deepseek-moe-16b-base/raw/main/README.md) → `DeepSeek_AI/Variants/2401_DeepSeekMoE/src/huggingface_model_cards/deepseek-moe-16b-base.md`
  - [deepseek-ai/deepseek-moe-16b-chat](https://huggingface.co/deepseek-ai/deepseek-moe-16b-chat/raw/main/README.md) → `DeepSeek_AI/Variants/2401_DeepSeekMoE/src/huggingface_model_cards/deepseek-moe-16b-chat.md`

## DeepSeek-Math

- Collection: [deepseek-ai/deepseek-math-65f2962739da11599e441681](https://huggingface.co/collections/deepseek-ai/deepseek-math-65f2962739da11599e441681)
- 官方模型仓库：**4**

  - [deepseek-ai/DeepSeek-Math-V2](https://huggingface.co/deepseek-ai/DeepSeek-Math-V2/raw/main/README.md) → `DeepSeek_AI/Variants/2511_deepseek_math_v2/src/huggingface_model_cards/DeepSeek-Math-V2.md`
  - [deepseek-ai/deepseek-math-7b-instruct](https://huggingface.co/deepseek-ai/deepseek-math-7b-instruct/raw/main/README.md) → `DeepSeek_AI/Variants/2402_DeepSeekMath/src/huggingface_model_cards/deepseek-math-7b-instruct.md`
  - [deepseek-ai/deepseek-math-7b-rl](https://huggingface.co/deepseek-ai/deepseek-math-7b-rl/raw/main/README.md) → `DeepSeek_AI/Variants/2402_DeepSeekMath/src/huggingface_model_cards/deepseek-math-7b-rl.md`
  - [deepseek-ai/deepseek-math-7b-base](https://huggingface.co/deepseek-ai/deepseek-math-7b-base/raw/main/README.md) → `DeepSeek_AI/Variants/2402_DeepSeekMath/src/huggingface_model_cards/deepseek-math-7b-base.md`

## DeepSeek-VL

- Collection: [deepseek-ai/deepseek-vl-65f295948133d9cf92b706d3](https://huggingface.co/collections/deepseek-ai/deepseek-vl-65f295948133d9cf92b706d3)
- 官方模型仓库：**4**

  - [deepseek-ai/deepseek-vl-7b-chat](https://huggingface.co/deepseek-ai/deepseek-vl-7b-chat/raw/main/README.md) → `DeepSeek_AI/Variants/2403_deepseek_vl/src/huggingface_model_cards/deepseek-vl-7b-chat.md`
  - [deepseek-ai/deepseek-vl-1.3b-base](https://huggingface.co/deepseek-ai/deepseek-vl-1.3b-base/raw/main/README.md) → `DeepSeek_AI/Variants/2403_deepseek_vl/src/huggingface_model_cards/deepseek-vl-1.3b-base.md`
  - [deepseek-ai/deepseek-vl-7b-base](https://huggingface.co/deepseek-ai/deepseek-vl-7b-base/raw/main/README.md) → `DeepSeek_AI/Variants/2403_deepseek_vl/src/huggingface_model_cards/deepseek-vl-7b-base.md`
  - [deepseek-ai/deepseek-vl-1.3b-chat](https://huggingface.co/deepseek-ai/deepseek-vl-1.3b-chat/raw/main/README.md) → `DeepSeek_AI/Variants/2403_deepseek_vl/src/huggingface_model_cards/deepseek-vl-1.3b-chat.md`

## DeepSeek-R1

- Collection: [deepseek-ai/deepseek-r1-678e1e131c0169c0bc89728d](https://huggingface.co/collections/deepseek-ai/deepseek-r1-678e1e131c0169c0bc89728d)
- 官方模型仓库：**4**

  - [deepseek-ai/DeepSeek-R1](https://huggingface.co/deepseek-ai/DeepSeek-R1/raw/main/README.md) → `DeepSeek_AI/2501_deepseek_r1/src/huggingface_model_cards/DeepSeek-R1.md`
  - [deepseek-ai/DeepSeek-R1-Zero](https://huggingface.co/deepseek-ai/DeepSeek-R1-Zero/raw/main/README.md) → `DeepSeek_AI/2501_deepseek_r1/src/huggingface_model_cards/DeepSeek-R1-Zero.md`
  - [deepseek-ai/DeepSeek-R1-Distill-Llama-70B](https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Llama-70B/raw/main/README.md) → `DeepSeek_AI/2501_deepseek_r1/src/huggingface_model_cards/DeepSeek-R1-Distill-Llama-70B.md`
  - [deepseek-ai/DeepSeek-R1-Distill-Qwen-32B](https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Qwen-32B/raw/main/README.md) → `DeepSeek_AI/2501_deepseek_r1/src/huggingface_model_cards/DeepSeek-R1-Distill-Qwen-32B.md`
