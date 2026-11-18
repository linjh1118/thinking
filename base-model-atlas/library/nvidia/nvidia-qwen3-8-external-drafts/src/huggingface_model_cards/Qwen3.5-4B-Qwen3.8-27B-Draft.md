---
pipeline_tag: text-generation
base_model:
- Qwen/Qwen3.5-4B
- Qwen/Qwen3.8-27B
license: other
license_name: nvidia-open-model-agreement
library_name: Model Optimizer
tags:
- nvidia
- ModelOpt
- Qwen3.5
- Qwen3.8
- Draft
---

# Model Overview

## Description:
The NVIDIA Qwen3.5-4B-Qwen3.8-27B-Draft model is an external draft model for Qwen’s [Qwen3.8-27B](https://huggingface.co/Qwen/Qwen3.8-27B) – a complete language model rather than a draft head, sharing the target's tokenizer and vocabulary. It proposes blocks of candidate tokens
which Qwen3.8-27B verifies by rejection sampling, reducing decode latency without changing the target's output distribution.

Trained with NVIDIA Model Optimizer in external speculative decoding mode.

This model is ready for commercial or non-commercial use.  <br>

### License/Terms of Use:
**GOVERNING DOWNLOAD TERMS:** Use of this model is governed by the [NVIDIA Open Model Agreement](https://www.nvidia.com/en-us/agreements/enterprise-software/nvidia-open-model-agreement/).

**ADDITIONAL INFORMATION** : The Qwen3.5-4B draft base is governed by the [Apache 2.0 License](https://huggingface.co/Qwen/Qwen3.5-4B/blob/main/LICENSE). **Qwen3.5-4B**. The Qwen3.8-27B target model is governed by the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). **Qwen3.8-27B**.

### Deployment Geography:
Global <br>

### Use Case: <br>
Developers and inference providers serving Qwen3.8-27B who want lower decode latency through speculative decoding. Recommended for this target. <br>

### Release Date:  <br>
Huggingface 11/17/2026 via https://huggingface.co/nvidia/Qwen3.5-4B-Qwen3.8-27B-Draft <br>

## References
NVIDIA Model Optimizer: https://github.com/NVIDIA/Model-Optimizer

## Model Architecture:
**Architecture Type:** Transformer  <br>
**Network Architecture:** Qwen3_5ForCausalLM <br>
This model was developed based on [Qwen/Qwen3.5-4B](https://huggingface.co/Qwen/Qwen3.5-4B).
**Number of Model Parameters:** 4.21B <br>
**This model was developed based on [Qwen3.5-4B](https://huggingface.co/Qwen/Qwen3.5-4B) and [Qwen3.8-27B](https://huggingface.co/Qwen/Qwen3.8-27B)** <br>

## Input:
**Input Type(s):** Text <br>
**Input Format(s):** String <br>
**Input Parameters:** One-Dimensional (1D) <br>
**Other Properties Related to Input:** Input must be tokenized with the Qwen3.8-27B tokenizer. Trained at a sequence length of 12,288 tokens. <br>

## Output:
**Output Type(s):** Text <br>
**Output Format:** String <br>
**Output Parameters:** One-Dimensional (1D): Sequences <br>
**Other Properties Related to Output:** The model emits proposed token blocks for the target to verify. Final output text is produced by Qwen3.8-27B <br>

Our AI models are designed and/or optimized to run on NVIDIA Hardware accelerated systems. By leveraging NVIDIA's hardware (e.g. GPU cores) and software frameworks (e.g., CUDA libraries), the model achieves faster training and inference times compared to CPU-only solutions. <br>

## Software Integration:
**Supported Runtime Engine(s):** <br>
* **vLLM** <br>

**Supported Hardware Microarchitecture Compatibility:** <br>
* NVIDIA Blackwell <br>

**Preferred Operating System(s):** <br>
* Linux <br>

The integration of foundation and fine-tuned models into AI systems requires additional testing using use-case-specific data to ensure safe and effective deployment. Following the V-model methodology, iterative testing and validation at both unit and system levels are essential to mitigate risks, meet technical and functional requirements, and ensure compliance with safety and ethical standards before deployment.

## Model Version(s):
Qwen3.5-4B-Qwen3.8-27B-Draft model checkpoint is 1.0 version and is trained with nvidia-modelopt **v0.48.0rc0** <br>

## Training and Evaluation Datasets:

## Training Dataset:
**Link:** [Nemotron-Post-Training-Dataset-v2](https://huggingface.co/datasets/nvidia/Nemotron-Post-Training-Dataset-v2). Only the prompts were taken from this dataset. Responses were synthesized by Qwen3.8-27B. 
**Data Modality:** Text 
**Text Training Data Size:** 1 Billion to 10 Trillion Tokens 
**Data Collection Method by dataset:** Hybrid: Automated, Synthetic <br> 
**Labeling Method by dataset:** Synthetic 
**Properties:** 199,998 single-turn conversations. Prompts were sampled with a fixed seed in equal shares across nine categories of Nemotron-Post-Training-Dataset-v2: STEM, code, math, chat, and multilingual German, Spanish, French, Italian and Japanese. Prompts longer than 3,072 tokens were dropped. For every response position the target’s top-20 output distribution under its serving policy was recorded, and that distribution is the training signal.

## Evaluation Dataset:
**Link:** SPEED-Bench (qualitative and throughput-32k subsets) 
**Data Collection Method by dataset:** Hybrid: Manually-Collected, Synthetic
**Labeling Method by dataset:** Synthetic 
**Properties:** SPEED-Bench is a unified benchmark for speculative decoding spanning coding, humanities, math, multilingual, QA, RAG, reasoning, roleplay, STEM, summarization and writing. Its qualitative subset has 1,138 conversation turns; its throughput-32k subset has 1,536 single-turn prompts of 33k to 46k tokens, split evenly across the low_entropy, mixed and high_entropy categories.

## Inference:
**Acceleration Engine:** **vLLM** <br>
**Test Hardware:** **NVIDIA Groq 3 LPU (Language Processing Unit)** <br>

The intended deployment of these drafts is on NVIDIA Groq 3 LPU hardware, where they are
compiled for the LPU and run under its runtime. The published checkpoints are standard
HuggingFace models and also load in vLLM, SGLang and TRT-LLM.

**Speculative Decoding with an External Draft**
Responses to the prompts above were synthesized by Qwen3.8-27B, and the draft was trained to match the target’s output distribution at every response position. At serving time the draft samples a block of candidate tokens autoregressively under the target’s serving policy (temperature 1.0, top-k 20, top-p 0.95), and the target verifies the block by rejection sampling against the same policy, resampling a rejected token from the residual distribution. Drafting is therefore probabilistic rather than greedy, and the accepted sequence has exactly the distribution the target would have produced on its own. The number of tokens returned per target step is the acceptance rate.


## Evaluation
Acceptance rate on SPEED-Bench (qualitative subset) with a draft block size of 16:

| Category | This draft | Qwen3.8-27B MTP head |
|---|---|---|
| coding | 5.22 | 3.78 |
| humanities | 5.39 | 3.61 |
| math | 5.61 | 3.63 |
| multilingual | 6.55 | 4.38 |
| qa | 5.39 | 3.75 |
| rag | 6.58 | 4.68 |
| reasoning | 5.98 | 3.93 |
| roleplay | 4.41 | 3.16 |
| stem | 5.44 | 3.61 |
| summarization | 6.19 | 4.13 |
| writing | 4.59 | 3.29 |
| Overall Average | 5.58 | 3.81 |

Acceptance rate on SPEED-Bench (throughput-32k subset, long-context) with a draft block
size of 16:

| Category | This draft | Qwen3.8-27B MTP head |
|---|---|---|
| low_entropy | 5.80 | 4.73 |
| mixed | 5.53 | 3.85 |
| high_entropy | 4.01 | 3.00 |
| Overall Average | 5.11 | 3.86 |


### Comparison with the other drafts in this family

All three drafts were trained on the same corpus against the same target and evaluated with the same harness, at a draft block size of 16 averaged over categories. 

| Draft | Embedding | Non-embedding | Total | qualitative | throughput-32k |
|---|---|---|---|---|---|
| **Qwen3.5-4B** (this model) | 0.64B | 3.57B | 4.21B | **5.58** | **5.11** |
| [Qwen3.5-0.8B](https://huggingface.co/nvidia/Qwen3.5-0.8B-Qwen3.8-27B-Draft) | 0.25B | 0.50B | 0.75B | 3.92 | 3.60 |
| [Llama-3.2-1B](https://huggingface.co/nvidia/Llama-3.2-1B-Qwen3.8-27B-Draft) | 0.51B | 0.97B | 1.48B | 3.42 | 3.07 |
| Qwen3.8-27B built-in MTP head | 0 (shared) | 0.42B | 0.42B | 3.81 | 3.86 |

Parameter counts are for the checkpoints published here. All three drafts tie their input embedding to their output head, so the embedding column counts that one matrix, which is large because the target's vocabulary is 248,320 tokens. The Llama-3.2-1B draft is bigger than the stock model for the same reason: its embedding and output layers were rebuilt on that vocabulary. The MTP head carries no embedding or output head of its own and reads the target's, which are a further 2.54B parameters it does not have to store but cannot run without.

## Model Limitations:
The base model was trained on data that contains toxic language and societal biases originally crawled from the internet. Therefore, the model may amplify those biases and return toxic responses especially when prompted with toxic prompts. The model may generate answers that may be inaccurate, omit key information, or include irrelevant or redundant text producing socially unacceptable or undesirable text, even if the prompt itself does not include anything explicitly offensive.

## Citation

Please cite the base model:

```bibtex
@misc{qwen3.5,
    title  = {{Qwen3.5}: Towards Native Multimodal Agents},
    author = {{Qwen Team}},
    month  = {February},
    year   = {2026},
    url    = {https://qwen.ai/blog?id=qwen3.5}
}
```
Please also cite this draft and the target it was trained against:

```bibtex
@misc{nvidia_qwen35_4b_qwen38_27b_draft,
    title  = {{Qwen3.5-4B-Qwen3.8-27B-Draft}},
    author = {{NVIDIA}},
    year   = {2026},
    url    = {https://huggingface.co/nvidia/Qwen3.5-4B-Qwen3.8-27B-Draft}
}

@misc{qwen3.8_27b,
    title  = {{Qwen3.8-27B}},
    author = {{Qwen Team}},
    year   = {2026},
    url    = {https://huggingface.co/Qwen/Qwen3.8-27B}
}
```

## Ethical Considerations

NVIDIA believes Trustworthy AI is a shared responsibility and we have established policies and practices to enable development for a wide array of AI applications. Developers should work with their internal model team to ensure this model meets requirements for the relevant industry and use case and addresses unforeseen product misuse.

For more detailed information on ethical considerations for this model, please see the Model Card++ Explainability, Bias, Safety & Security, and Privacy Subcards below.

Please report model quality, risk, security vulnerabilities or NVIDIA AI Concerns [here](https://www.nvidia.com/en-us/support/submit-security-vulnerability/).

SUBCARDS:
## Explainability


| Field                                    | Response                                                                                                                                                                                                                                                                                                                                                                                                                                                |
|:----------------------------------------:|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------:|
| **Intended Task/Domain:**                | Text generation, reasoning, summarization, and question answering.                                                                                                                                                                                                                                                                                                                                                                                       |
| **Model Type:**                          | Text-to-text transformer                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| **Intended Users:**                      | This model is intended for developers, researchers, and customers building/utilizing LLMs, while balancing accuracy and efficiency.                                                                                                                                                                                                                                                                                                                     |
| **Output:**                              | Text String(s)                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| **Describe how the model works:**        | A Qwen3.5-4B draft proposes candidate tokens for Qwen3.8-27B. The target model verifies the candidates, and the longest accepted sequence is returned.                                                                                                                                                                                                                                                                                                   |
| **Name the adversely impacted groups this has been tested to deliver comparable outcomes regardless of:**        | Not Applicable    |
| **Technical Limitations & Mitigation:**  | The model was trained on data that contains toxic language and societal biases originally crawled from the internet. Therefore, the model may amplify those biases and return toxic responses especially when prompted with toxic prompts. Therefore, before deploying any applications of this model, developers should perform safety testing and tuning tailored to their specific applications of the model.                                       |
| **Verified to have met prescribed NVIDIA quality standards:** | Yes                                                                                                                                                                                                                                                                                                                                                                                                                                |
| **Performance Metrics:**                 | Accuracy, Throughput, and user-side throughput                                                                                                                                                                                                                                                                                                                                                                                                           |
| **Potential Known Risk**                 | The model may generate answers that may be inaccurate, omit key information, or include irrelevant or redundant text producing socially unacceptable or undesirable text, even if the prompt itself does not include anything explicitly offensive.                                                                                                                                                                                                       |
| **Licensing:**                           | **GOVERNING DOWNLOAD TERMS:** Use of this model is governed by the [NVIDIA Open Model Agreement](https://www.nvidia.com/en-us/agreements/enterprise-software/nvidia-open-model-agreement/).

**ADDITIONAL INFORMATION** : The Qwen3.5-4B draft base is governed by the [Apache 2.0 License](https://huggingface.co/Qwen/Qwen3.5-4B/blob/main/LICENSE). **Qwen3.5-4B**. The Qwen3.8-27B target model is governed by the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). **Qwen3.8-27B**.. |


## Bias

| Field                                                                                                           | Response |
|:---------------------------------------------------------------------------------------------------------------:|:--------:|
| Participation considerations from adversely impacted groups [protected classes](https://www.senate.ca.gov/protected-classes) in model design and testing:       | None     |
| Measures taken to mitigate against unwanted bias                                                                | None     |
| Bias Metric (If Measured):                                                                | None     |


## Safety & Security

| Field                              | Response                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
|:-----------------------------------:|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------:|
| Model Application Field(s):         | Chat, Instruction Following, Chatbot Development, Code Generation, Reasoning                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| Describe the life critical impact (if present) | Not Applicable                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| Use Case Restrictions:              | Abide by the **GOVERNING DOWNLOAD TERMS:** Use of this model is governed by the [NVIDIA Open Model Agreement](https://www.nvidia.com/en-us/agreements/enterprise-software/nvidia-open-model-agreement/).

**ADDITIONAL INFORMATION** : The Qwen3.5-4B draft base is governed by the [Apache 2.0 License](https://huggingface.co/Qwen/Qwen3.5-4B/blob/main/LICENSE). **Qwen3.5-4B**. The Qwen3.8-27B target model is governed by the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). **Qwen3.8-27B**. |
| Model and Dataset Restrictions:     | The Principle of least privilege (PoLP) is applied limiting access for dataset generation. Restrictions enforce dataset access during training, and dataset license constraints adhered to. Model checkpoints are made available on Hugging Face, and may become available on cloud providers' model catalog.                                                                                                                                                                                            

## Privacy

| Field | Response |
| :---- | :---- |
| Privacy Statement | The datasets used to train this model were reviewed before release. Please review NVIDIA’s Privacy Policy (https://www.nvidia.com/en-us/about-nvidia/privacy-policy/) for more information. | 
