---
license: apache-2.0
base_model:
- ibm-granite/granite-speech-5.0-2b
library_name: transformers.js
pipeline_tag: automatic-speech-recognition
language:
- multilingual
- en
- fr
- de
- es
- pt
- ja
tags:
- onnx
- webgpu
---

# Granite-Speech-5.0-2B ONNX

ONNX weights of [ibm-granite/granite-speech-5.0-2b](https://huggingface.co/ibm-granite/granite-speech-5.0-2b) for in-browser inference with [Transformers.js](https://huggingface.co/docs/transformers.js) on WebGPU. These are the weights used by the [granite-speech-webgpu](https://huggingface.co/spaces/ibm-granite/granite-speech-webgpu) demo.

| file | precision | size |
| --- | --- | --- |
| `onnx/audio_encoder_q4.onnx` | 4-bit weights, fp32 activations | 658 MB |
| `onnx/embed_tokens_q4f16.onnx` | 4-bit weights, fp16 | 119 MB |
| `onnx/decoder_model_merged_q4f16.onnx` | 4-bit weights, fp16, KV cache | 948 MB |

Weights are 4-bit, block size 32, asymmetric (`MatMulNBits` / `GatherBlockQuantized`).

## Usage (Transformers.js >= 4.3)

```js
import { AutoProcessor, GraniteSpeechForConditionalGeneration } from '@huggingface/transformers';

const model_id = 'ibm-granite/granite-speech-5.0-2b-ONNX';
const processor = await AutoProcessor.from_pretrained(model_id);
const model = await GraniteSpeechForConditionalGeneration.from_pretrained(model_id, {
  dtype: { audio_encoder: 'q4', embed_tokens: 'q4f16', decoder_model_merged: 'q4f16' },
  device: 'webgpu',
});

const messages = [{ role: 'user', content: '<|audio|>transcribe the speech with proper punctuation and capitalization.' }];
const text = processor.tokenizer.apply_chat_template(messages, { add_generation_prompt: true, tokenize: false });
const inputs = await processor(text, audio /* Float32Array, 16 kHz mono */);
const ids = await model.generate({ ...inputs, max_new_tokens: 256 });
const output = processor.batch_decode(ids.slice(null, [inputs.input_ids.dims.at(-1), null]), { skip_special_tokens: true });
```

Transformers.js 4.3 or newer is required for WebGPU in Safari 26.

See the [base model card](https://huggingface.co/ibm-granite/granite-speech-5.0-2b) for the supported tasks, prompts and languages.

## How it was made

granite-speech-5.0-2b has the same architecture as granite-speech-4.1-2b, except that the language model's rotary position embeddings use YaRN scaling (factor 4, up to 16384 positions). These files reuse the graphs of [onnx-community/granite-speech-4.1-2b-ONNX](https://huggingface.co/onnx-community/granite-speech-4.1-2b-ONNX) with every weight re-derived from the 5.0 checkpoint:

- direct weight copies, BatchNorm folded into the encoder depthwise convolutions, and the constant-folded Q-Former query self-attention, all recomputed from the 5.0 weights;
- the decoder's rotary cos/sin caches regenerated from the model's own YaRN rotary embedding (16384 positions, attention scaling included);
- 4-bit quantization with the same recipe as the 4.1 files (it reproduces them byte for byte when applied to the 4.1 weights).

Checks:

- **fp32 conversion:** greedy transcripts identical to `transformers` on the bundled `multilingual_sample.wav` and LibriSpeech clips.
- **4-bit files:** 2.43% WER (2.31% normalized) on the 73-utterance `hf-internal-testing/librispeech_asr_dummy` set on the onnxruntime CPU EP, vs 2.70% for the 4.1 ONNX files under the same pipeline.

The decoder's logits are 1/8 of `transformers`' logits, the same as the 4.1 ONNX files; this does not change greedy decoding.
