---
license: mit
---
<p align="center">
    <img src="https://mdn.alipayobjects.com/huamei_qa8qxu/afts/img/A*4QxcQrBlTiAAAAAAQXAAAAgAemJ7AQ/original" width="100"/>
</p>
<p align="center">🤗 <a href="https://huggingface.co/inclusionAI">Hugging Face</a>&nbsp;&nbsp; | &nbsp;&nbsp;🤖 <a href="https://www.modelscope.cn/models/inclusionAI/Ling-3.2-air">ModelScope</a></p>

## Introduction

We introduce **Ling-3.2-air**, an open-weight model that shares the same native multimodal architecture as [**Ling-3.0-flash-VL**](https://huggingface.co/inclusionAI/Ling-3.0-flash-VL). Compared with its predecessor, Ling-3.2-air shows stronger performance in workflow automation and reasoning over professional documents. Its **AutomationBench-AA** score rises from 15.7% to **61%**, while its **GDP.pdf** all-pass rate increases from 8.4% to **16%**. On **AA-Briefcase v1.1**, its Elo rating rises from 987 to **1340**, a gain of **353 points**. On **Terminal-Bench 4.0**, its pass rate on terminal-based tasks rises from 0% to **27%**. Overall, **Ling-3.2-air** scores **23** on the **Artificial Analysis Intelligence Index v5.0.1**.

Specialized evaluations highlight **Ling-3.2-air**’s performance in quantitative data analysis and legal work. On **Harvey LAB-AA v1.1**, it earns an **87.7%** criterion pass rate. Its all-pass rate is **8.3%** before the material hallucination check and **0.8%** after it.

<img src="https://intranetproxy.alipay.com/skylark/lark/0/2026/png/143556413/1795446647339-971e8d9b-8476-4adb-abf6-511f353bace3.png" alt="Ling-3.2-air evaluation results" width="4723" style="max-width: 100%; height: auto;" />

## Model Overview

The model summary information and architecture diagram are as follows:

<div align="center">
<table align="center" style="display: table; width: auto; margin: 0 auto;">
  <thead>
    <tr><th>Architecture</th><th>Hybrid-linear MoE</th></tr>
  </thead>
  <tbody>
    <tr><td>Parameter Scale</td><td>Total 124B, Activated 5.5B</td></tr>
    <tr><td>Transformer Layers</td><td>35 KDA + 7 Gated MLA (5:1)</td></tr>
    <tr><td>Number of Dense Layers</td><td>2</td></tr>
    <tr><td>Number of Routed Experts</td><td>512</td></tr>
    <tr><td>Number of Shared Experts</td><td>1</td></tr>
    <tr><td>Number of Activated Experts</td><td>8</td></tr>
    <tr><td>Attention Heads</td><td>32</td></tr>
    <tr><td>Hidden Size</td><td>2560</td></tr>
    <tr><td>Expert Intermediate Size</td><td>768</td></tr>
    <tr><td>Dense Intermediate Size</td><td>6144</td></tr>
    <tr><td>Vocabulary Size</td><td>157184</td></tr>
  </tbody>
</table>
</div>

<img src="https://intranetproxy.alipay.com/skylark/lark/0/2026/png/308395/1795445566709-9cfe00e0-8743-4e69-a07c-23d1a01d4a1d.png" alt="Ling-3.2-air architecture" width="1126" style="max-width: 100%; height: auto;" />

## Quickstart

### SGLang (Recommended)

The day-0 SGLang image includes Ling-3.2-air support, MTP (NEXTN) speculative decoding, and Hopper decode optimizations:

```bash
docker pull lmsysorg/sglang:dev-Ling-3.0-flash-VL
```

#### Run Inference

Recommended recipe with 256K context, on 4× 141GB-class GPUs (H20-3e / H200) or 4-GPU Blackwell nodes (B300 / GB300):

```bash
docker run --rm --gpus all --ipc=host --shm-size 32g \
  -p 30000:30000 \
  lmsysorg/sglang:dev-Ling-3.0-flash-VL \
  python3 -m sglang.launch_server \
    --model-path inclusionAI/Ling-3.2-air \
    --tp 4 \
    --context-length 262144 \
    --speculative-algorithm NEXTN \
    --trust-remote-code \
    --reasoning-parser auto \
    --tool-call-parser auto \
    --host 0.0.0.0 \
    --port 30000
```

On 80GB cards (H100 / H800), scale out to `--tp 8`. The reasoning and tool-call parsers resolve automatically to `ling3` from the chat template; you can also set them explicitly with `--reasoning-parser ling3 --tool-call-parser ling3`.

**Client**

It is recommended to use the sampling parameters (`temperature=1.0`, `top_p=0.95`, `top_k=20`) and set `enable_thinking` to `true` for better performance.

```bash
curl -s http://localhost:30000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "inclusionAI/Ling-3.2-air",
    "messages": [{
      "role": "user",
      "content": [
        {"type": "image_url", "image_url": {"url": "https://example.com/image.png"}},
        {"type": "text", "text": "Describe this image in one sentence."}
      ]
    }],
    "chat_template_kwargs": {"enable_thinking": true},
    "stream": true,
    "temperature": 1.0,
    "top_k": 20,
    "top_p": 0.95
  }'
```

Video input uses `{"type": "video_url", "video_url": {"url": "..."}}` in the same message shape.

### vLLM

#### Environment Preparation

```bash
pip install uv

uv venv ~/my_ling_env

source ~/my_ling_env/bin/activate

git clone https://github.com/inclusionAI/vllm-ling-v3.git

cd vllm-ling-v3

VLLM_USE_PRECOMPILED=1 uv pip install --editable . --torch-backend=auto
```

#### Run Inference

**Server**

```bash
vllm serve "$MODEL_PATH" \
    --port "$PORT" \
    --trust-remote-code \
    --served-model-name auto \
    --tensor-parallel-size 4 \
    --gpu-memory-utilization 0.85 \
    --enable-prefix-caching \
    --mamba-cache-mode align \
    --enable-auto-tool-choice \
    --tool-call-parser ling3 \
    --reasoning-parser ling3 \
    --speculative-config '{"method":"mtp","num_speculative_tokens":3}'
```

**Client**

It is recommended to use the sampling parameters (`temperature=1.0`, `top_p=0.95`, `top_k=20`) and set `enable_thinking` to `true` for better performance.

```bash
curl -s http://${MASTER_IP}:${PORT}/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "auto",
    "messages": [{
      "role": "user",
      "content": [
        {"type": "image_url", "image_url": {"url": "https://example.com/image.png"}},
        {"type": "text", "text": "Describe this image in one sentence."}
      ]
    }],
    "chat_template_kwargs": {"enable_thinking": true},
    "stream": true,
    "temperature": 1.0,
    "top_k": 20,
    "top_p": 0.95
  }'
```

