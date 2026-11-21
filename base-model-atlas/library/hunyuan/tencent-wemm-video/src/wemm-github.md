<h1 align="center">WeMM-Video: Pushing the Frontiers of Open-Source Omni-Modal Video Understanding</h1>

<p align="center">
  <b>English</b> · <a href="README_zh.md">简体中文</a>
</p>

<p align="center">
  <a href="https://github.com/Tencent/WeMM-Video"><img src="https://img.shields.io/badge/GitHub-WeMM--Video-24292F?logo=github&amp;logoColor=white" alt="GitHub repository"></a>
  <a href="https://arxiv.org/abs/2611.26409"><img src="https://img.shields.io/badge/arXiv-Paper-B31B1B?logo=arxiv&amp;logoColor=white" alt="arXiv paper"></a>
  <a href="https://huggingface.co/collections/tencent/wemm-video"><img src="https://img.shields.io/badge/Hugging%20Face-Model%20Collection-FFD21E?logo=huggingface&amp;logoColor=FFD21E" alt="Hugging Face model collection"></a>
  <a href="LICENSE#L12"><img src="https://img.shields.io/badge/License-Apache%202.0-0969DA?logo=apache&amp;logoColor=white" alt="Apache 2.0 license"></a>
</p>

<p align="center">
  <a href="#architecture--evaluation">Architecture &amp; Evaluation</a> ·
  <a href="#model-zoo">Model Zoo</a> ·
  <a href="#quick-start">Quick Start</a> ·
  <a href="#serving-and-examples">Serving and Examples</a> ·
  <a href="#citation">Citation</a>
</p>

## Overview

WeMM-Video is a family of Chinese–English bilingual omni-modal foundation
models for joint audio-visual understanding and reasoning. It accepts text,
images, audio, and video and generates text responses. For video inputs, it can
use the original soundtrack alongside the frames. The family includes 2B, 4B,
and 9B dense models and a 35B-A3B mixture-of-experts model.

- **Inference modes.** Instruct mode gives fast, direct responses. Thinking mode
  supports explicit multi-step reasoning.
- **Training.** Trained on approximately 1.2 trillion multimodal tokens through progressive pre-training and multi-stage post-training.

<p align="center">
  <a href="assets/wemm-video-capabilities-compact.png">
    <img src="assets/wemm-video-capabilities-compact.png" width="90%" alt="WeMM-Video examples of audio-visual understanding and reasoning, audio and music understanding, and image and text understanding.">
  </a>
</p>

## Architecture & Evaluation

Here is the architecture of the WeMM-Video family.
<p align="center">
  <a href="assets/wemm-video-architecture.pdf">
    <img src="assets/wemm-video-architecture.png" width="75%" alt="WeMM-Video architecture. A vision encoder and an audio encoder feed image, timestamped video frame, and audio tokens into a language model alongside text tokens.">
  </a>
</p>

**WeMM-Video-35B-A3B** establishes a new open-source state of the art on omni-modal video understanding, outperforming proprietary models such as Qwen3.5-Omni-Flash and Seed2.0-Mini-0428 and narrowing the gap with Gemini-3.0-Flash.

<p align="center">
  <a href="assets/wemm-video-benchmarks.png">
    <img src="assets/wemm-video-benchmarks.png" width="90%" alt="WeMM-Video omni-modal video benchmark results">
  </a>
</p>

**WeMM-Video-35B-A3B** and **WeMM-Video-9B** achieve leading performance on general audio understanding.

<p align="center">
  <a href="assets/wemm_index_audio.png">
    <img src="assets/wemm_index_audio.png" width="90%" alt="WeMM-Video audio benchmark results">
  </a>
</p>

## Model Zoo

| Size | BF16 | FP8 Block128 | AWQ W4A16 | GGUF Q4_K_M | NVFP4 W4A16 |
| --- | --- | --- | --- | --- | --- |
| 2B | [WeMM-Video-2B](https://huggingface.co/tencent/WeMM-Video-2B) | [WeMM-Video-2B-FP8](https://huggingface.co/tencent/WeMM-Video-2B-FP8) | [WeMM-Video-2B-AWQ](https://huggingface.co/tencent/WeMM-Video-2B-AWQ) | [WeMM-Video-2B-GGUF](https://huggingface.co/tencent/WeMM-Video-2B-GGUF) | [WeMM-Video-2B-NVFP4](https://huggingface.co/tencent/WeMM-Video-2B-NVFP4) |
| 4B | [WeMM-Video-4B](https://huggingface.co/tencent/WeMM-Video-4B) | [WeMM-Video-4B-FP8](https://huggingface.co/tencent/WeMM-Video-4B-FP8) | [WeMM-Video-4B-AWQ](https://huggingface.co/tencent/WeMM-Video-4B-AWQ) | [WeMM-Video-4B-GGUF](https://huggingface.co/tencent/WeMM-Video-4B-GGUF) | [WeMM-Video-4B-NVFP4](https://huggingface.co/tencent/WeMM-Video-4B-NVFP4) |
| 9B | [WeMM-Video-9B](https://huggingface.co/tencent/WeMM-Video-9B) | [WeMM-Video-9B-FP8](https://huggingface.co/tencent/WeMM-Video-9B-FP8) | [WeMM-Video-9B-AWQ](https://huggingface.co/tencent/WeMM-Video-9B-AWQ) | [WeMM-Video-9B-GGUF](https://huggingface.co/tencent/WeMM-Video-9B-GGUF) | [WeMM-Video-9B-NVFP4](https://huggingface.co/tencent/WeMM-Video-9B-NVFP4) |
| 35B-A3B | [WeMM-Video-35BA3B](https://huggingface.co/tencent/WeMM-Video-35BA3B) | [WeMM-Video-35BA3B-FP8](https://huggingface.co/tencent/WeMM-Video-35BA3B-FP8) | [WeMM-Video-35BA3B-AWQ](https://huggingface.co/tencent/WeMM-Video-35BA3B-AWQ) | [WeMM-Video-35BA3B-GGUF](https://huggingface.co/tencent/WeMM-Video-35BA3B-GGUF) | [WeMM-Video-35BA3B-NVFP4](https://huggingface.co/tencent/WeMM-Video-35BA3B-NVFP4) |

## Quick Start

### Install dependencies

Use a Python 3.12 environment with an NVIDIA GPU, a driver compatible with
CUDA 12.9, and FFmpeg. See the [host prerequisites](patch/README.md#install) for
TorchCodec's shared-library requirements. Run from the project root.

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install --index-url https://download.pytorch.org/whl/cu129 \
  torch==2.10.0 torchvision==0.25.0 torchcodec==0.10.0
python -m pip install transformers==5.2.0 accelerate pillow librosa soundfile scipy requests
```

### Load from Hugging Face with Transformers

Run this Python example from the project root. It downloads the 2B BF16
checkpoint and processor from the Hub and reuses them for all five requests.
Review the model repository's custom code before enabling `trust_remote_code`.
Set `revision` to a commit SHA to pin the weights and custom code.

```python
import torch
from transformers import AutoModelForImageTextToText, AutoProcessor

model_id = "tencent/WeMM-Video-2B"
revision = "main"
processor = AutoProcessor.from_pretrained(
    model_id, revision=revision, trust_remote_code=True
)
model = AutoModelForImageTextToText.from_pretrained(
    model_id, revision=revision, trust_remote_code=True,
    dtype=torch.bfloat16, device_map="auto",
)


def ask(prompt, *media):
    messages = [{
        "role": "user",
        "content": [*media, {"type": "text", "text": prompt}],
    }]
    inputs = processor.apply_chat_template(
        messages, tokenize=True, return_dict=True, return_tensors="pt",
        add_generation_prompt=True, enable_thinking=False,
    ).to(device=model.device, dtype=model.dtype)
    with torch.inference_mode():
        output = model.generate(**inputs, max_new_tokens=128, do_sample=False)
    answer_ids = output[0, inputs.input_ids.shape[1]:]
    return processor.tokenizer.decode(answer_ids, skip_special_tokens=True)


# Text. The expected answer is 10:05.
print(ask("A meeting starts at 09:30 and lasts 35 minutes. What time does it end?"))

# Image and audio from the Apollo 11 archives.
print(ask("Which planet is shown? Describe what you see.", {
    "type": "image", "image": "examples/media/apollo-11-earth.jpg",
}))
print(ask("Transcribe the English speech in this recording.", {
    "type": "audio", "audio": "examples/media/apollo-11-small-step.wav",
}))

# Use the same MP4 for frames alone or for frames with the original soundtrack.
clip = {
    "video": "examples/media/apollo-11-first-steps.mp4",
    "fps": 1.0, "min_frames": 4, "max_frames": 16, "total_pixels": 262144,
}
print(ask("Describe what happens on screen.", {"type": "video", **clip}))
print(ask("Describe the scene and summarize the speech.", {"type": "video_audio", **clip}))
```

The example uses instruct mode. Set `enable_thinking=True` in
`apply_chat_template` to enable thinking mode.

To run just the video-with-audio example from the command line, use
`python examples/transformers_video.py`. It accepts `--video`, `--model`, and
`--revision`.

## Serving and Examples

### Choose a runtime

| Runtime | Checkpoint formats | Guide |
| --- | --- | --- |
| Transformers | BF16 | [Load a model from Hugging Face](#load-from-hugging-face-with-transformers) |
| Patched vLLM | BF16, FP8 Block128, AWQ W4A16, NVFP4 W4A16 | [Version and GPU requirements](docs/serving.md#runtime-profiles) |
| Patched SGLang | BF16 | [Serving recipes](docs/serving.md) |
| Native runtime | GGUF Q4_K_M | [Run on CPU or CUDA](native/README.md) |

To set up vLLM or SGLang outside Docker, follow the [manual installation and patch guide](patch/README.md#manual-install-and-patch).

### Docker

The images contain the serving environment and open Bash by default. With
[Docker and the NVIDIA Container Toolkit](docs/serving.md#docker-environments)
configured, choose one backend below. Both examples use local port `8000`.
Export `HF_TOKEN` in the host shell when the checkpoint requires authentication.

Each request can contain up to four images, two videos, and two audio items
within the configured context length.

#### vLLM

```bash
docker compose build vllm-018

MODEL=tencent/WeMM-Video-2B
docker run --rm --gpus all --shm-size=8g \
  --publish 127.0.0.1:8000:8000 \
  --mount type=volume,source=wemm-video-hub,target=/root/.cache/huggingface \
  --env HF_TOKEN \
  wemm-video:vllm-0.18.0-cu129 \
  vllm serve "$MODEL" --served-model-name "$MODEL" --trust-remote-code --dtype bfloat16 \
  --host 0.0.0.0 --port 8000 --max-model-len 8192 \
  --no-enable-prefix-caching --mamba-ssm-cache-dtype float32 \
  --limit-mm-per-prompt '{"image":4,"video":2,"audio":2}' \
  --media-io-kwargs '{"video":{"fps":2,"min_frames":4,"max_frames":16,"total_pixels":262144}}'
```

#### SGLang

```bash
docker compose build sglang-0516

MODEL=tencent/WeMM-Video-2B
docker run --rm --gpus all --shm-size=8g \
  --publish 127.0.0.1:8000:8000 \
  --mount type=volume,source=wemm-video-hub,target=/root/.cache/huggingface \
  --env HF_TOKEN \
  wemm-video:sglang-0.5.16-cu129 \
  python -m sglang.launch_server --model-path "$MODEL" --served-model-name "$MODEL" --trust-remote-code \
  --host 0.0.0.0 --port 8000 --dtype bfloat16 --context-length 8192 \
  --attention-backend triton --linear-attn-backend triton \
  --limit-mm-data-per-request '{"image":4,"video":2,"audio":2}'
```

#### Send a request

For both patched backends, send a `video_url` content item to
`POST /v1/chat/completions`. Set `video_url.use_audio` to `true` to include the
original soundtrack or `false` for frames only. Place `fps` and `max_frames`
inside `video_url` to control frame sampling. See the [full HTTP request
example](docs/serving.md#send-a-video-request) for the Thinking-mode option.

The named volume keeps downloaded weights across container runs. When the
server is ready, send the bundled clip from a second terminal in the project root.

```bash
curl --fail --silent --show-error http://127.0.0.1:8000/health
python examples/chat.py video-audio --model tencent/WeMM-Video-2B
```

The [examples](examples/README.md) cover text, images, audio, video, and video with audio.

## Licensing

The WeMM-Video project source code is licensed under the [Apache License 2.0](LICENSE#L12).
The [model license](LICENSE) covers the WeMM-Video collection as of November 20, 2026.
See the [third-party notices](THIRD_PARTY_NOTICES.md) and
[example media credits](examples/README.md#media-credits) for applicable terms
and attribution. Check the Hugging Face model card for each checkpoint's license.
 
## Citation

If you use WeMM-Video in your research, please cite the project.

```bibtex
@misc{WeMM-Video,
      title={WeMM-Video: Pushing the Frontiers of Open-Source Omni-Modal Video Understanding}, 
      author={Changli Tang and Jie Yang and Tianyi Wang and Lei Li and Daoze Zhang and Zijie Xin and Zhan Liu and Li Li and Jinchang Xu and Fengyun Rao and Chao Zhang and Jing Lyu},
      year={2026},
      eprint={2611.26409},
      archivePrefix={arXiv},
      primaryClass={cs.CV},
      url={https://arxiv.org/abs/2611.26409}, 
}
```
