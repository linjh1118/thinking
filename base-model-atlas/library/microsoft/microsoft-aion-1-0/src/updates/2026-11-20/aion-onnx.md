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
license_link: LICENSE
base_model: microsoft/Aion-1.0-Instruct-2.3B
base_model_relation: quantized
library_name: onnxruntime-genai
pipeline_tag: text-generation
tags:
- quantized
- onnx
- onnxruntime
- onnxruntime-genai
- webgpu
- int4
- summarization
- rewriting
- chat
---

# Aion 1.0 Instruct — ONNX WebGPU

<img src="images/ASG%20Logo.svg" alt="ASG Logo" class="block dark:hidden" width="25%">
<img src="images/ASG_Logo_white.svg" alt="ASG Logo" class="hidden dark:block" width="25%">
Microsoft Windows Applied Sciences Group

> This repository contains the **ONNX WebGPU** quantized version of [**Aion Instruct v1**](https://huggingface.co/microsoft/Aion-1.0-Instruct-2.3B).
> For the full model description, intended uses, limitations, safety information and evaluation results, see the original model card: [microsoft/Aion-1.0-Instruct-2.3B](https://huggingface.co/microsoft/Aion-1.0-Instruct-2.3B).

## Model Details

| | |
|---|---|
| **Base model** | [microsoft/Aion-1.0-Instruct-2.3B](https://huggingface.co/microsoft/Aion-1.0-Instruct-2.3B) |
| **Format** | ONNX (opset 21, `com.microsoft` contrib ops) |
| **Target hardware** | GPU via WebGPU (browser and native) |
| **Runtime** | [ONNX Runtime GenAI](https://github.com/microsoft/onnxruntime-genai) / ONNX Runtime (Web) with the WebGPU execution provider |
| **Quantization** | INT4 weights (block-wise, QAT), FP16 activations and KV cache |
| **Model size** | ~1.3 GB |
| **Parameters** | ~2.29B (base model) |
| **Context length** | 32,768 tokens |
| **Languages** | English, German, Spanish, Portuguese, Italian, French, Chinese, Japanese |
| **License** | MIT |

## Quantization Details

| Component | Scheme |
|---|---|
| Linear layers (attention q/k/v/o, MLP gate/up/down) | 4-bit symmetric block-wise weights (`MatMulNBits`, block size 32), exported from a quantization-aware-trained (QAT) checkpoint |
| Token embedding / tied LM head | 4-bit block-wise weights (`GatherBlockQuantized` / `MatMulNBits`, block size 64) |
| Activations, norms, logits | FP16 |
| KV cache | FP16 |
| Attention | `GroupQueryAttention` with fused RoPE; 21 sliding-window layers (window 2048) + 7 full-attention layers |

The model is a single ONNX decoder graph (opset 21 + `com.microsoft` contrib ops) with an FP16 KV cache, so it runs on any ONNX Runtime build that provides the WebGPU execution provider, including ONNX Runtime Web in the browser.

## Usage

Run with [ONNX Runtime GenAI](https://github.com/microsoft/onnxruntime-genai) using the WebGPU execution provider. `onnxruntime-genai` is installed with `--no-deps` so that it uses the WebGPU build of ONNX Runtime instead of the default CPU build:

```bash
hf download microsoft/Aion-1.0-Instruct-2.3B-ONNX-WebGPU --local-dir Aion-Instruct-v1-ONNX-WebGPU
pip install numpy onnxruntime-webgpu==1.27.0
pip install --no-deps onnxruntime-genai==0.14.1
```

```python
import onnxruntime_genai as og

model_dir = "Aion-Instruct-v1-ONNX-WebGPU"
config = og.Config(model_dir)
config.clear_providers()
config.append_provider("webgpu")
model = og.Model(config)
tokenizer = og.Tokenizer(model)

chat_template = open(f"{model_dir}/chat_template.jinja", encoding="utf-8").read()
messages = '[{"role": "user", "content": "Give me a short introduction to large language models."}]'
prompt = tokenizer.apply_chat_template(messages, template_str=chat_template, add_generation_prompt=True)

params = og.GeneratorParams(model)
params.set_search_options(max_length=4096)
generator = og.Generator(model, params)
generator.append_tokens(tokenizer.encode(prompt))

stream = tokenizer.create_stream()
while not generator.is_done():
    generator.generate_next_token()
    print(stream.decode(generator.get_next_tokens()[0]), end="", flush=True)
```

`max_length` (prompt + generated tokens) defaults to 4,096 in `genai_config.json`; it can be raised up to the model's 32,768-token context, at the cost of a larger pre-allocated KV cache. To run on CPU instead, omit the `clear_providers` / `append_provider` calls.

## Files

| File | Description |
|---|---|
| `model.onnx` | ONNX decoder graph |
| `model.onnx.data` | Quantized weights (external data, ~1.3 GB) |
| `genai_config.json` | ONNX Runtime GenAI configuration |
| `config.json`, `generation_config.json` | Model and generation configuration |
| `tokenizer.json`, `tokenizer_config.json` | Tokenizer |
| `chat_template.jinja` | Chat template |
| `LICENSE` | MIT License |

### Inputs and outputs

| Name | Type | Shape |
|---|---|---|
| `input_ids` | int64 | `[batch, sequence_length]` |
| `attention_mask` | int64 | `[batch, total_sequence_length]` |
| `past_key_values.{0..27}.key` / `.value` | float16 | `[batch, 8, past_sequence_length, 128]` |
| `logits` (output) | float16 | `[batch, 1, 200029]` (last position only) |
| `present.{0..27}.key` / `.value` (outputs) | float16 | `[batch, 8, total_sequence_length, 128]` |

## Chat Format

This quantized model uses the same [chat template](./chat_template.jinja) as the base model. See the [Chat Format section](https://huggingface.co/microsoft/Aion-1.0-Instruct-2.3B#chat-format) of the original model card.

## Evaluation

Quantization can affect output quality. Quality relative to the bfloat16 base model will be reported here. For the reference results of the unquantized model, see the [Evaluation section](https://huggingface.co/microsoft/Aion-1.0-Instruct-2.3B#evaluation) of the original model card.

## Bias, Risks, and Limitations

This model inherits all limitations of the base model, and quantization may introduce additional quality degradation. Please read the [Bias, Risks, and Limitations section](https://huggingface.co/microsoft/Aion-1.0-Instruct-2.3B#bias-risks-and-limitations) and the [Out-of-Scope Use section](https://huggingface.co/microsoft/Aion-1.0-Instruct-2.3B#out-of-scope-use) of the original model card before using this model.

## Other Versions

| Version | Link |
|---|---|
| Original (bfloat16, Transformers) | [microsoft/Aion-1.0-Instruct-2.3B](https://huggingface.co/microsoft/Aion-1.0-Instruct-2.3B) |
| GGUF (llama.cpp) | [asgmodels/Aion-Instruct-v1-GGUF](https://huggingface.co/asgmodels/Aion-Instruct-v1-GGUF) |
| ONNX (WebGPU) | [microsoft/Aion-1.0-Instruct-2.3B-ONNX-WebGPU](https://huggingface.co/microsoft/Aion-1.0-Instruct-2.3B-ONNX-WebGPU) |
| ONNX (NPU) | [asgmodels/Aion-Instruct-v1-ONNX-NPU](https://huggingface.co/asgmodels/Aion-Instruct-v1-ONNX-NPU) |

## License

This model is released under the [MIT License](./LICENSE), the same as the [base model](https://huggingface.co/microsoft/Aion-1.0-Instruct-2.3B).

## Model Card Contact

[aioninstruct@microsoft.com](mailto:aioninstruct@microsoft.com)