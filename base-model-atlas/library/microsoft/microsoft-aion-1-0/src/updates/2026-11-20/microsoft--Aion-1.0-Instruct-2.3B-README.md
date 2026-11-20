---
language:
- en
- de
- es
- pt
- it
- fr
- zh
- ja
license: mit
license_link: https://huggingface.co/microsoft/Aion-1.0-Instruct-2.3B/blob/main/LICENSE
library_name: transformers
pipeline_tag: text-generation
tags:
- custom_code
- summarization
- rewriting
- chat


---

# Aion 1.0 Instruct 

Microsoft Windows Applied Sciences Group

## Model Description

Aion Instruct serves as the foundational Small Language Model (SLM) in the Windows ecosystem, specifically optimized for on-device AI, text and operating system use cases. This 2.3B parameters base model delivers enterprise-grade language understanding and generation capabilities directly at the edge, enabling responsive, private, and cost-effective AI-powered scenarios without requiring constant cloud connectivity.

A further optimized version of Aion Instruct, coupled with Microsoft’s content moderation model, will become the Windows OS SLM by the end of January 2027. This Hugging Face version is meant to be an introduction to what’s coming and a way to maximize transparency with our users, as well as welcome their feedback. 
We are publishing the unquantized model first, to be followed by quantized versions. 

## Model Details

- **Languages:** English, German, Spanish, Portuguese, Italian, French, Chinese, Japanese
- **License:** MIT
- **Library names:** PyTorch, ONNX, GGUF 
- **Task:** Text generation
- **Tags:** Summarization, rewriting, chat
- **Authors:** Applied Sciences Group @ Microsoft Windows & Devices
- **Related GitHub repository:** [microsoft/Aion-Instruct-Preview-Sample](https://github.com/microsoft/Aion-Instruct-Preview-Sample/)


## Uses

The model was primarily trained for general-purpose text scenarios including document comprehension, content analysis, question answering, and natural language understanding. 
With context window extending to 32K tokens, it can process multi-page documents, lengthy email threads, and complex technical specifications entirely on-device, ensuring user data remains private.

### Out-of-Scope Use

The model is not specifically designed or evaluated for every possible downstream purpose. Anyone accessing the model should bear in mind the guidance below.

1. Developers should consider common limitations of language models as they select use cases, and evaluate and mitigate for accuracy, safety, and fairness before using within a specific downstream use case, particularly for high-risk scenarios.
2. Developers should be aware of and adhere to applicable laws or regulations (including privacy, trade compliance laws, etc.) that are relevant to their use case.
3. This model should not be used for:
   - Generating harmful, violent, explicit, or offensive content.
   - Creating misleading content, such as fake news or misinformation.
   - Automated decision-making in critical contexts like medical diagnoses or legal judgments.
4. Nothing contained in this Model Card should be interpreted as or deemed a restriction or modification to the license the model is released under.

## Bias, Risks, and Limitations

With 2.3 billion parameters, Aion Instruct is a rather small language model. While this means the model is taking up less disk space and can be quite fast, it also comes with trade-offs.

In comparison to large language models, whose size enables storing vast amounts of factual knowledge and grasping subtle context, logic, and nuance, small language models such as Aion Instruct can miss fine details, provide misstatements, or show inability to follow complex multi-step reasoning. Larger models also have larger context and the memory needed to remember facts accurately, as well as the reasoning to see through trick questions. Smaller models lack the storage and reasoning depth to consistently do both.

While Microsoft’s best practices were followed while training and safety alignment was conducted, anyone using the model should bear in mind that Aion Instruct does not have the complex reasoning needed to understand all the nuances of safety, including attempts to induce unsafe behavior. Aion Instruct may be susceptible to adversarial attacks.

XPIA, DIC, and ECI are amongst the key metrics to improve in future releases:

![Aion Instruct safety benchmarks bar chart](images/aion_safety_bchart.png)

*Scores are direction-normalized so higher is better (0–100).*

While we continue to work towards closing performance gaps across languages and supporting more languages, output quality may differ depending on the language.

We also remain committed to improving the groundedness and safety of Aion Instruct. One way of limiting harmful output generation are content moderation models – a local model from that group will be used alongside Aion Instruct when the model becomes available in Windows (General Availability coming by end of Jan 2027).

### Recommendations

The model was not trained to excel at world knowledge. Users should take note of recommended uses (see section: Uses), use their best judgement, and follow laws and regulations when interacting with the model.

Your feedback is important for helping us improve Aion Instruct. If you encounter harmful, inaccurate, or otherwise unexpected outputs from the model, please provide feedback.


### Training Data

Our training data is an extension of the data used for training Phi Silica (the previous generation Windows OS SLM) and includes a wide variety of sources from:

- Publicly available documents filtered rigorously for quality; 
- Newly created synthetic data for the purpose of teaching math, coding, common sense reasoning, general knowledge of the world (science, daily activities, theory of mind, etc.).

Multilingual data constitutes about 6% of our overall data. We are focusing on the quality of data that could potentially improve the reasoning ability for the model, and we filter the publicly available documents to contain the correct level of knowledge.

## Evaluation

All benchmarks were run with [EleutherAI’s lm-evaluation-harness](https://github.com/EleutherAI/lm-evaluation-harness) where a task implementation was available. Otherwise, the official implementation from each benchmark’s own repository was used. For benchmarks that need an LLM judge (marked †), GPT-4o was the judge model. Scores are percentages unless stated otherwise.

| Category | Benchmark | Score | Notes |
|---|---|---:|---|
| Knowledge | MMLU | 55.15 | |
| Knowledge | MMLU-Pro | 33.35 | |
| Knowledge | MMMLU | 45.51 | Multilingual MMLU |
| Knowledge | GPQA | 28.18 | |
| Math | GSM8K | 74.91 | Loose matching |
| Math | GSMPlus | 49.56 | |
| Math | MATH-500 | 48.00 | |
| Instruction following | IFEval | 83.90 | Mean of prompt-level strict and instruction-level strict |
| Instruction following | IFBench | 32.00 | Prompt-level loose |
| Instruction following | Multi-IF | 64.70 | |
| Translation | chrF++ | 43.18 | |



## Model Overview

| | |
|---|---|
| **Type** | Causal language model (instruction-tuned) |
| **Parameters** | ~2.29B (tied input/output embeddings) |
| **Layers** | 28 |
| **Hidden size** | 2048 |
| **MLP intermediate size** | 8192 (SiLU) |
| **Attention** | GQA: 24 query heads, 8 key/value heads, head dim 128 |
| **Attention pattern** | Hybrid: 21 sliding-window layers (window 2048) + 7 full-attention layers |
| **Positional encoding** | RoPE (θ = 32000); YaRN scaling (factor 16) on full-attention layers |
| **Context length** | 32,768 tokens |
| **Vocabulary size** | 200,029 |
| **Precision** | bfloat16 |
| **Knowledge cutoff** | 2025-12 |

## Quickstart

The model uses custom modeling code, so `trust_remote_code=True` is required. It was exported with `transformers` 5.x.

```python
from transformers import AutoModelForCausalLM, AutoTokenizer

model_id = "microsoft/Aion-1.0-Instruct-2.3B"

tokenizer = AutoTokenizer.from_pretrained(model_id, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    dtype="auto",
    device_map="auto",
    trust_remote_code=True,
)

messages = [
    {"role": "user", "content": "Give me a short introduction to large language models."},
]
inputs = tokenizer.apply_chat_template(
    messages,
    add_generation_prompt=True,
    return_dict=True,
    return_tensors="pt",
).to(model.device)

outputs = model.generate(**inputs, max_new_tokens=512)
print(tokenizer.decode(outputs[0][inputs["input_ids"].shape[-1]:], skip_special_tokens=True))
```

## Chat Format

Conversations are formatted with the included [chat template](./chat_template.jinja):

```
<|system|>You are Aion Instruct, a large language model trained by Microsoft.
Knowledge cutoff: 2025-12
Current date: YYYY-MM-DD<|end|><|user|>Hello!<|end|><|assistant|>Hi! How can I help?<|end|>
```

- Every turn ends with `<|end|>`, which is also the EOS token.
- A leading `system` message is appended to the default system preamble.
- Optional template variables: `model_identity`, `knowledge_cutoff`, and `current_date`.

### Tool Calling

Pass tools via `apply_chat_template(..., tools=tools)`. The tool schemas are injected into the system prompt between `<|tool|>` and `<|/tool|>`, and the model emits calls as:

```
<|tool_call|>{"name": "<function-name>", "arguments": {...}}<|/tool_call|>
```

Tool results (`role: "tool"` messages) are returned to the model inside a user turn prefixed with `<|tool_response|>`.

## Files

| File | Description |
|---|---|
| `model.safetensors` | Model weights (bfloat16) |
| `config.json` | Model configuration |
| `generation_config.json` | Default generation settings |
| `configuration_aion_instruct.py` | Custom configuration class (`AionInstructConfig`) |
| `modeling_aion_instruct.py` | Custom model implementation (`AionInstructForCausalLM`) |
| `tokenizer.json`, `tokenizer_config.json` | Tokenizer |
| `chat_template.jinja` | Chat template |

## License

This model is released under the [MIT License](./LICENSE).

## Model Card Contact

[aioninstruct@microsoft.com](mailto:aioninstruct@microsoft.com)
