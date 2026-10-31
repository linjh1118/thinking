---
pipeline_tag: image-text-to-text
base_model:
- "meta-models/Muse-Spark-Open-816B-A42B"
license: other
license_name: nvidia-open-model-agreement-license
library_name: Model Optimizer
tags:
- nvidia
- ModelOpt
- Muse-Spark-Open-816B-A42B
- DFlash
- DFlash2
---

# Model Overview

## Description:
The NVIDIA Muse-Spark-Open-816B-A42B-DFlash2 model is the DFlash 2 draft checkpoint for Muse-Spark-Open-816B-A42B, a multimodal mixture-of-experts causal language model that produces text and supports long-context, tool-enabled workflows. The NVIDIA Muse-Spark-Open-816B-A42B-DFlash2 model incorporates DFlash 2 speculative decoding with [Model Optimizer](https://github.com/NVIDIA/Model-Optimizer). DFlash 2 adds a two-tap in-block convolution around every sublayer and a pairwise path selector that walks one coherent path through each position’s top-k candidates.

This model is ready for commercial or non-commercial use.  <br>

## Third-Party Community Consideration:
The target model, Muse-Spark-Open-816B-A42B, is not owned or developed by NVIDIA. It has been developed and built to a third-party's requirements; see link to Non-NVIDIA [Muse-Spark-Open-816B-A42B Model Card](https://huggingface.co/meta-models/Muse-Spark-Open-816B-A42B). This DFlash 2 draft model was trained by NVIDIA for use with that target model.

### License/Terms of Use:
**GOVERNING TERMS:** Use of the model/checkpoints is governed by the [NVIDIA Open Model Agreement](https://www.nvidia.com/en-us/agreements/enterprise-software/nvidia-open-model-agreement/). <br>
**Additional Information:** Meta’s Muse Model [License](https://huggingface.co/meta-models/Muse-Spark-Open-816B-A42B/blob/main/LICENSE.md). **Built with Muse Spark Open**. 


### Deployment Geography:
Global <br>

### Use Case:
Muse-Spark-Open-816B-A42B is intended for evaluation and development of long-context multimodal and agentic text-generation workflows, including tool-assisted coding. This DFlash2 release is intended for DFlash 2–assisted serving of Muse-Spark-Open-816B-A42B rather than as a standalone target model checkpoint. <br>

### Release Date:
**Huggingface:** 10/16/2026 via https://huggingface.co/nvidia/Muse-Spark-Open-816B-A42B-DFlash2 <br>

## References
NVIDIA Model Optimizer: https://github.com/NVIDIA/Model-Optimizer
[DFlash: Block Diffusion for Flash Speculative Decoding](https://huggingface.co/papers/2602.06036)

## Model Architecture:
**Architecture Type:** Transformer <br>
**Network Architecture:** 5 dense decoder layers with non-causal sliding-window attention (window 2048) <br>
**Total Parameters:** 4.38B; the token embedding and output head are shared with the target and not included <br>
**Active Parameters:** 4.38B (dense, no expert routing) <br>
**Vocabulary Size:** 202,048 <br>

## Input:
**Input Type(s):** Text, Image, Other (Video), Audio <br>
**Input Format(s):** String, Red, Green, Blue (RGB), Other (Video), Other (Waveform) <br>
**Input Parameters:** One-Dimensional (1D), Two-Dimensional (2D), Three-Dimensional (3D), One-Dimensional (1D) <br>
**Other Properties Related to Input:** Requests support `temperature`, `top_p`, and `top_k` parameters. Combined input and output context length is up to 1,000,000 tokens. <br>

## Output:
**Output Type(s):** Text <br>
**Output Format:** String <br>
**Output Parameters:** One-Dimensional (1D) <br>
**Other Properties Related to Output:** The combined input and output context length is up to 1,000,000 tokens. <br>

Our AI models are designed and/or optimized to run on NVIDIA GPU-accelerated systems. By leveraging NVIDIA's hardware (e.g. GPU cores) and software frameworks (e.g., CUDA libraries), the model achieves faster training and inference times compared to CPU-only solutions. <br>

## Software Integration:
**Supported Runtime Engine(s):** <br>
* TRT-LLM <br>
* vLLM <br>
* SGLang <br>


**Supported Hardware Microarchitecture Compatibility:** <br>
* NVIDIA Blackwell <br>

**Preferred Operating System(s):** <br>
* Linux <br>

The integration of foundation and fine-tuned models into AI systems requires additional testing using use-case-specific data to ensure safe and effective deployment. Following the V-model methodology, iterative testing and validation at both unit and system levels are essential to mitigate risks, meet technical and functional requirements, and ensure compliance with safety and ethical standards before deployment.

## Model Version(s):
v1.0: Muse-Spark-Open-816B-A42B-DFlash2 is the DFlash 2 draft model for Muse-Spark-Open-816B-A42B, trained with a pre-release build of **NVIDIA Model Optimizer 0.47** and released in BF16 (bfloat16) <br>

## Training and Evaluation Datasets:

## Training Dataset:
**Link:** [Nemotron-Post-Training-Dataset-v2](https://huggingface.co/datasets/nvidia/Nemotron-Post-Training-Dataset-v2), only prompts from the datasets were used for data synthesis (the original responses from GPT were not used), which is then used to train the DFlash modules.  
**Data Modality:** Text  
**Text Training Data Size:** 1 Billion to 10 Trillion Tokens  
**Data Collection Method by dataset:** Hybrid: Automated, Synthetic  
**Labeling Method by dataset:** Hybrid: Automated, Synthetic  
**Properties:** About 3.48 million multilingual text samples featuring prompts spanning math, code, STEM, and conversational topics. Each sample includes a synthetic response generated by the target model; the corpus mixes responses generated at five reasoning-effort levels, each including its reasoning trace.

## Testing Dataset:
**Link:** [SPEED-Bench](https://huggingface.co/datasets/nvidia/SPEED-Bench), [MT-Bench](https://huggingface.co/spaces/lmsys/mt-bench)  
**Data Collection Method by dataset:** Hybrid: Automated, Manually-Collected, Synthetic  
**Labeling Method by dataset:** Hybrid: Automated, Manually-Labeled, Synthetic  
**Properties:** The SPEED-Bench qualitative split (880 text prompts in 11 task categories, mostly English), the 32k-token bucket of the SPEED-Bench throughput split (first 100 prompts of each of its three categories), and MT-Bench (80 English two-turn text questions in 8 categories) were used during development to measure acceptance length and select checkpoints.

## Evaluation Dataset:
The model is evaluated on the [SPEED-Bench](https://huggingface.co/datasets/nvidia/SPEED-Bench) and [MT-Bench](https://huggingface.co/spaces/lmsys/mt-bench) datasets for speculative decoding benchmarking.

**Data Collection Method by dataset:** Hybrid: Automated, Manually-Collected, Synthetic  
**Labeling Method by dataset:** Hybrid: Automated, Manually-Labeled, Synthetic  
**Properties:** All prompts are text and mostly in English. The SPEED-Bench qualitative split has 880 prompts in 11 task categories (such as coding, math, reasoning, and writing, plus a multilingual category covering 23 languages); MT-Bench has 80 two-turn questions in 8 categories. Acceptance length over the target model's responses measures the quality of the draft model.


## Inference:
**Acceleration Engine:** **vLLM, SGLang** <br>
**Test Hardware:** **NVIDIA Blackwell GB300** <br>

## DFlash 2 Speculative Decoding
This model is ready for inference in DFlash 2 speculative decoding mode. DFlash 2 drafts a block of candidate tokens in a single non-causal forward pass, then uses a pairwise path selector over each position’s top-k candidates. The target model verifies the proposed path so that more than one token can be accepted per generation step. The mean number of tokens emitted per step is the acceptance length.

## Usage

### vLLM
```sh
vllm serve meta-models/Muse-Spark-Open-816B-A42B \
    --speculative-config '{"method": "dflash", "model": "nvidia/Muse-Spark-Open-816B-A42B-DFlash2", "num_speculative_tokens": 7, "draft_sample_method": "probabilistic"}' \
    --trust-remote-code
```

### SGLang
Run inside the Muse Spark Open image, `lmsysorg/sglang:dev-muse-spark-open`. On 4 Blackwell GPUs, serve the NVFP4 target with this draft model:

```sh
python -m sglang.launch_server \
    --model-path meta-models/Muse-Spark-Open-816B-A42B-NVFP4 \
    --quantization modelopt_fp4 \
    --moe-runner-backend flashinfer_trtllm \
    --tp-size 4 \
    --ep-size 4 \
    --attention-backend trtllm_mha \
    --page-size 128 \
    --kv-cache-dtype fp8_e4m3 \
    --mem-fraction-static 0.8 \
    --reasoning-parser muse \
    --tool-call-parser muse \
    --enable-layernorm-sp \
    --enable-megamoe-for-layernorm-sp \
    --speculative-algorithm DFLASH \
    --speculative-draft-model-path nvidia/Muse-Spark-Open-816B-A42B-DFlash2 \
    --speculative-draft-attention-backend fa4 \
    --speculative-num-draft-tokens 8 \
    --host 0.0.0.0 \
    --port 30000
```

## Evaluation

All acceptance lengths below were measured with reasoning effort xhigh, 4,096 output tokens, and concurrency 32 on one NVIDIA GB300 node (TP4 + EP4). The t=0 numbers use greedy decoding; the t=1 numbers use temperature 1.0 with no top-p or top-k truncation and `draft_sample_method: probabilistic`.

Acceptance length on [MT-Bench](https://huggingface.co/spaces/lmsys/mt-bench) with draft length 7, measured with vLLM and Muse-Spark-Open-816B-A42B (NVFP4):

| Category            | AL, greedy (t=0) | AL, sampling (t=1) |
| ------------------- | ----------------: | -----------------: |
| writing             | 3.87 | 3.59 |
| roleplay            | 3.38 | 3.20 |
| reasoning           | 3.80 | 3.44 |
| math                | 4.78 | 4.45 |
| coding              | 4.68 | 4.12 |
| extraction          | 4.84 | 4.30 |
| stem                | 3.48 | 3.26 |
| humanities          | 3.21 | 2.96 |
| **Overall Average** | **4.01** | **3.66** |

Acceptance length on [SPEED-Bench](https://huggingface.co/datasets/nvidia/SPEED-Bench) (qualitative split) with draft length 7, measured with vLLM and Muse-Spark-Open-816B-A42B (NVFP4):

| Category            | AL, greedy (t=0) | AL, sampling (t=1) |
| ------------------- | ----------------: | -----------------: |
| coding              | 4.53 | 4.15 |
| humanities          | 3.50 | 3.13 |
| math                | 4.19 | 3.81 |
| multilingual        | 4.81 | 4.34 |
| qa                  | 3.79 | 3.40 |
| rag                 | 4.52 | 4.10 |
| reasoning           | 4.22 | 3.78 |
| roleplay            | 3.70 | 3.31 |
| stem                | 3.73 | 3.37 |
| summarization       | 4.51 | 4.03 |
| writing             | 3.34 | 3.08 |
| **Overall Average** | **4.08** | **3.68** |

Acceptance length on [SPEED-Bench](https://huggingface.co/datasets/nvidia/SPEED-Bench) (throughput split, 32k-token inputs, first 100 prompts of each category) with draft length 7, measured with vLLM and Muse-Spark-Open-816B-A42B (NVFP4):

| Category            | AL, greedy (t=0) | AL, sampling (t=1) |
| ------------------- | ----------------: | -----------------: |
| mixed               | 4.00 | 3.65 |
| low_entropy         | 3.99 | 3.62 |
| high_entropy        | 2.78 | 2.52 |
| **Overall Average** | **3.59** | **3.26** |

## Model Limitations:
The base model was trained on data that contains toxic language and societal biases originally crawled from the internet. Therefore, the model may amplify those biases and return toxic responses especially when prompted with toxic prompts. The model may generate answers that may be inaccurate, omit key information, or include irrelevant or redundant text producing socially unacceptable or undesirable text, even if the prompt itself does not include anything explicitly offensive.

## Ethical Considerations
NVIDIA believes Trustworthy AI is a shared responsibility and we have established policies and practices to enable development for a wide array of AI applications. Developers should work with their internal model team to ensure this model meets requirements for the relevant industry and use case and addresses unforeseen product misuse.

For more detailed information on ethical considerations for this model, please see the Model Card++ Explainability, Bias, Safety & Security, and Privacy Subcards below.

Please report model quality, risk, security vulnerabilities or NVIDIA AI Concerns [here](https://www.nvidia.com/en-us/support/submit-security-vulnerability/).

SUBCARDS:

# **Explainability**

|Field:|Response:|  
|:---:|:---:|  
|**Intended Task/Domain:**| Text generation, reasoning, summarization, and question answering. |  
|**Model Type:** |Text and Image-to-text transformer |  
|**Intended Users:**|This model is intended for developers, researchers, and customers building/utilizing LLMs, while balancing accuracy and efficiency.|  
|**Output:**|Text String(s)|  
|**Describe how the model works:**|Generates text by predicting the next word or token based on the context provided in the input sequence using multiple self-attention layers|  
|**Name the adversely impacted groups this has been tested to deliver comparable outcomes regardless of:**  |  Not Applicable|
|**Technical Limitations & Mitigation:**| The model was trained on data that contains toxic language and societal biases originally crawled from the internet. Therefore, the model may amplify those biases and return toxic responses especially when prompted with toxic prompts. Therefore, before deploying any applications of this model, developers should perform safety testing and tuning tailored to their specific applications of the model.|  
|**Verified to have met prescribed quality standards?**|Yes|  
|**Performance Metrics:**|Accuracy, Throughput, and user-side throughput|  
|**Potential Known Risk:**| The model may generate answers that may be inaccurate, omit key information, or include irrelevant or redundant text producing socially unacceptable or undesirable text, even if the prompt itself does not include anything explicitly offensive. |
|**Licensing:**| **GOVERNING TERMS:** Use of the model/checkpoints is governed by the [NVIDIA Open Model Agreement](https://www.nvidia.com/en-us/agreements/enterprise-software/nvidia-open-model-agreement/). <br> **Additional Information:** Meta’s Muse Model [License](https://huggingface.co/meta-models/Muse-Spark-Open-816B-A42B/blob/main/LICENSE.md). **Built with Muse Spark Open**.  |                                                                        


# **Bias**


| Field                                                                                       | Response |
| ------------------------------------------------------------------------------------------- | -------- |
| **Participation considerations from adversely impacted groups in model design and testing** | None     |
| **Measures taken to mitigate against unwanted bias**                                        | None     |
| **Bias Metric**                                                                             | None     |


# **Safety & Security**

|Field:|Response:|  
|:---:|:---:|  
|**Model Application(s):**|Chat, Instruction Following, Chatbot Development, Code Generation, Reasoning|  
|**Describe life critical application (if present):**|Not Applicable |  
|**Use Case Restrictions:**|Abide by the **GOVERNING TERMS:** Use of the model/checkpoints is governed by the [NVIDIA Open Model Agreement](https://www.nvidia.com/en-us/agreements/enterprise-software/nvidia-open-model-agreement/). <br> **Additional Information:** Meta’s Muse Model [License](https://huggingface.co/meta-models/Muse-Spark-Open-816B-A42B/blob/main/LICENSE.md). **Built with Muse Spark Open**. |  
|**Model and Dataset Restrictions:**|The Principle of least privilege (PoLP) is applied limiting access for dataset generation.  Restrictions enforce dataset access during training, and dataset license constraints adhered to. Model checkpoints are made available on Hugging Face, and may become available on cloud providers' model catalog.|



# **Privacy**


| Field                                                                          | Response                                                                           |
| ------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------- |
| **Generatable or reverse-engineerable personal data**                          | No                                                                                 |
| **Was consent obtained for any personal data used**                            | Not Applicable                                                                     |
| **Personal data used to create this model**                                    | None Known                                                                         |
| **How often is the dataset reviewed**                                          | Before Release                                                                     |
| **Was data from user interactions with the AI model used to train the model**  | No                                                                                 |
| **Is there provenance for all datasets used in training**                      | Yes                                                                                |
| **Does data labeling comply with privacy laws**                                | Yes                                                                                |
| **Is the data compliant with data-subject requests for correction or removal** | No, not possible with externally-sourced data.                                     |
| **Applicable NVIDIA Privacy Policy**                                           | [NVIDIA Privacy Policy](https://www.nvidia.com/en-us/about-nvidia/privacy-policy/) |

