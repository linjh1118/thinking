---
license: other
license_name: openmdw1.1-license
license_link: >-
  https://openmdw.ai/license/1-1/
library_name: cosmos
tags:
  - nvidia
  - cosmos
  - cosmos3
---

# **Cosmos 3: Omnimodal World Models for Physical AI**
**[Cosmos3](https://huggingface.co/collections/nvidia/cosmos3)** | **[Cosmos3 Examples](https://huggingface.co/collections/nvidia/cosmos3-examples)** | **[Code](https://github.com/nvidia/cosmos)** | **[White Paper](https://research.nvidia.com/labs/cosmos-lab/cosmos3/technical-report.pdf)** | **[Website](https://research.nvidia.com/labs/cosmos-lab/cosmos3/)**

[NVIDIA Cosmos™](https://github.com/nvidia/cosmos) is a world foundation model platform designed to accelerate the development of Physical AI by enabling machines to understand, simulate, and interact with the physical world across robotics, autonomous driving, and smart space environments, including industrial and factory-scale applications.

# Model Overview: Cosmos3-Edge-FP8

![Cosmos3-Edge base model and its FP8-quantized variant](images/cosmos3_edge_fp8.png)

The highlighted checkpoint, Cosmos3-Edge-FP8, is an FP8-quantized version of the Cosmos3-Edge base model.

## Description

Cosmos3-Edge-FP8 is an FP8-quantized variant of Cosmos3-Edge. It retains the base model architecture and intended applications, with FP8 quantization applied to selected model components.

Cosmos3 is a collection of Omnimodal world models capable of generating dynamic, high-quality video, image, audio, and action commands from combinations of text, image, video, and action trajectory inputs. It serves as a foundational building block for a broad range of Physical AI applications and research spanning world understanding, world generation, simulation, and embodied policy learning.

This model is ready for commercial and non-commercial use.

**Model Developer:** NVIDIA

### Model Versions

- Cosmos3-Edge-FP8:
  - Given multimodal inputs including text, images, video, and action trajectories, generate coherent text, images, video, and action outputs for multimodal understanding, world simulation, future prediction, action reasoning, and Physical AI applications.

### License

This model is released under the [OpenMDW1.1](https://openmdw.ai/license/1-1/)

### Deployment Geography

Global

### Use Case

Physical AI: Encompassing robotics, autonomous vehicles (AV), and smart space environments, including industrial and factory-scale applications.

### Release Date

Hugging Face 11/09/2026 via [https://huggingface.co/collections/nvidia/cosmos3](https://huggingface.co/collections/nvidia/cosmos3)
GitHub 11/09/2026 via [https://github.com/nvidia/cosmos](https://github.com/nvidia/cosmos)

## Model Architecture

**Architecture Type:** Transformer

**Network Architecture:** Mixture-of-Transformers (MoT)

Cosmos3 is an Omni-modal foundation model built on a Mixture-of-Transformers (MoT) architecture consisting of two complementary transformer towers: an autoregressive transformer for discrete token generation and a diffusion transformer for continuous multimodal generation. During inference, text is generated through standard next-token autoregressive decoding, while non-text modalities, such as images, video, audio, and actions, are synthesized through iterative denoising. This unified architecture enables Cosmos3 to model heterogeneous modalities within a single framework while preserving generation mechanisms best suited to each modality.

**This model was developed based on:**  [Cosmos Framework](https://github.com/nvidia/cosmos-framework)

**Number of trainable model parameters:**

- Cosmos3-Edge-FP8: 4B


## Input/Output Specifications

- **Generator Input**
  - **Input Type(s)**: Text, Image, Action Trajectory
  - **Input Format(s)**:
    - Text: String
    - Image: jpg, png, jpeg, webp
    - Action: JSON — 2D array shaped (T, D), where T is the number of frames and D is the embodiment-specific dimensionality
  - **Input Parameters**:
    - Text: One-dimensional (1D)
    - Image: Two-dimensional (2D)
    - Action trajectory: Two-dimensional (2D)
  - **Other Properties Related to Input**:
    - Image input is RGB color (8 bits per channel, sRGB color space); grayscale inputs are not supported.
    - Action input is a per-frame sequence of robot/agent state or control values (e.g., joint positions, gripper state, camera pose). The full input is a 2D array shaped (T, D), where T is the number of frames and D is the embodiment-specific dimensionality listed below.
    - Input action is only supported for compatible embodiments, including general camera motion (9D), autonomous vehicle (9D), egocentric motion (57D), single Franka Panda arm with RobotiQ gripper (10D), dual Franka Panda arm with RobotiQ gripper (20D), Agibot (29D), UR (10D), Google robot (10D), WidowX 250 (10D), UMI (10D).
  - **Input Size and Length limits:**
    - **Text:** 4096 tokens
    - **Image:** 256p and 480p resolution at one of these aspect ratios (16:9, 4:3, 1:1, 3:4, 9:16)
    - **Action:** 16 – 400 sequence length
- **Generator Output**
  - **Output Type(s)**: Image, video, action, text
  - **Output Format(s)**:
    - Image: JPG
    - Video: MP4
    - Action: JSON
    - Text: string
  - **Output Parameters**:
    - Image: Two-dimensional (2D)
    - Video: Three-dimensional (3D)
    - Action: Two-dimensional (2D)
    - Text: One-dimensional (1D)
  - **Other Properties Related to Output**:
    - The generated video is an MP4 file, with the resolution, frame rate, and duration specified in the input.
    - Video generation supports 256p and 480p resolution, 12–30 fps, and 50–150 frames. These are set per request via the `size`, `fps`, and `num_frames` fields.
    - The generated action is only supported for compatible embodiments, including general camera motion (9D), autonomous vehicle (9D), egocentric motion (57D), single Franka Panda arm with RobotiQ gripper (10D), dual Franka Panda arm with RobotiQ gripper (20D), Agibot (29D), UR (10D), Google robot (10D), WidowX 250 (10D), UMI (10D).
    - Video: mp4 at the FPS specified in input
    - Image: JPEG
- **Reasoner Input**
  - **Input Type(s)**: Text, Text+Image, Text+Video
  - **Input Format(s)**:
    - Text: String
    - Image: jpg, png, jpeg, webp
    - Video: mp4
  - **Input Parameters**:
    - Text: One-dimensional (1D)
    - Image: Two-dimensional (2D)
    - Video: Three-dimensional (3D)
  - **Other Properties Related to Input**:
    - Video inputs are recommended at a frame rate of 4 fps.
    - Long-context inputs supported up to 131,072 tokens.
  - **Input Size and Length limits:**
    - **Text:** Up to 131,072 tokens (context window).
    - **Image:** Standard input image formats; passed as file or URL.
    - **Video:** mp4 at the recommended 4 fps.
- **Reasoner Output**
  - **Output Type(s)**: Text
  - **Output Format(s)**:
    - Text: string
  - **Output Parameters**:
    - Text: One-dimensional (1D)
  - **Other Properties Related to Output**:
    - Default `max_tokens=4096+` is recommended for reasoning outputs; longer outputs may be requested.
    - Reasoning outputs may include structured chain-of-thought, 2D/3D point localization, and bounding-box coordinates for vision-based tasks.

The video content visualizes the input text description as a short animated scene, capturing key elements within the specified time constraints.

Our AI models are designed and/or optimized to run on NVIDIA GPU-accelerated systems. By leveraging NVIDIA's hardware (e.g., GPU cores) and software frameworks (e.g., CUDA libraries), the model achieves faster training and inference times compared to CPU-only solutions.

## Software Integration

**Runtime Engine(s):**

- [vLLM-Omni](https://github.com/vllm-project/vllm-omni)
- [vLLM](https://github.com/vllm-project/vllm)
- [PyTorch](https://github.com/nvidia/cosmos3)
- [Hugging Face Diffusers](https://github.com/huggingface/diffusers)

**Supported Hardware Microarchitecture Compatibility:**

- NVIDIA Ampere
- NVIDIA Blackwell
- NVIDIA Hopper

**Operating System(s):**

- Linux (We have not tested on other operating systems.)

**Precision:** This repository provides the FP8-quantized Cosmos3-Edge checkpoint. Components excluded from quantization retain their original precision. See [Performance Benchmark](#performance-benchmark) for backend- and hardware-specific precision details.

The integration of foundation and fine-tuned models into AI systems requires additional testing using use-case-specific data to ensure safe and effective deployment. Following the V-model methodology, iterative testing and validation at both unit and system levels are essential to mitigate risks, meet technical and functional requirements, and ensure compliance with safety and ethical standards before deployment.

## Training, Testing, and Evaluation Datasets

### Dataset Overview

- **Total Size:** 1.3B data points
- **Total Number of Datasets:** 393 dataset entries
- **Dataset partition:** Training [100%], Testing [N/A — evaluation benchmarks used separately], Validation [N/A — evaluation benchmarks used separately]
- **Time period for training data collection:** 2024–2026
- **Time period for testing data collection:** N/A (standard public benchmarks)
- **Time period for validation data collection:** N/A (standard public benchmarks)

Raw data from internal and external sources is transformed into training-ready data through multiple stages of curation, filtering, and quality review. Data acquisition spans diverse multimodal sources — robotics, autonomous driving, industrial environments, indoor and outdoor scenes, varied lighting and weather conditions, camera viewpoints, object categories, and human activities — to broaden coverage across Physical AI operating environments. Automated filtering pipelines remove corrupted, duplicate, low-quality, and restricted content. Metadata analysis, heuristic rules, and model-assisted classifiers are applied during preprocessing to flag anomalous distributions and low-diversity subsets. Human review supplements automated filtering for selected datasets, benchmark construction, and targeted quality analysis. Datasets are balanced across modalities and task categories — visual reasoning, text-to-image, text-to-video, image-to-video, audio generation, video transfer, action-conditioned generation, and action command generation — to reduce overrepresentation of narrow domains. Synthetic and simulation-based augmentation supplements coverage of rare physical interactions and edge-case scenarios. Deduplication and provenance tracking are applied across the corpus. The resulting processed data is converted into model-ready tokenized or encoded representations through modality-specific preprocessors before training begins.

Training datasets passed through multiple layers of automated and manual safeguards designed to reduce the presence of harmful or policy-violating content across categories including weapons and weapons-related instructional content, criminal planning, child sexual abuse material (CSAM), non-consensual intimate imagery (NCII), sexual content involving minors, harassment, hate speech, profanity, threats and incitement to violence, self-harm or suicide-related content, and graphic violence. Data sources are reviewed for licensing compatibility, provenance, and alignment with internal data governance and safety policies before admission into training corpora. Automated filtering pipelines combine multiple detection strategies: hash-matching against known CSAM and NCII reference databases; classifier-based moderation models trained for explicit sexual content, hate speech, violence, weapons imagery, and other restricted categories; keyword and regex-based screening for criminal-planning, threats, and self-harm phrases in text data; metadata and provenance heuristics for source-level risk signals; and embedding-based anomaly detection to surface samples that fall outside expected distributions. Human review and targeted audits supplement automated filtering for selected datasets, benchmark construction, and safety-sensitive evaluation. For multimodal Physical AI data (robotics, autonomous driving, industrial scenes), additional filtering targets invalid action trajectories, physically implausible interactions, and unsafe control sequences. Synthetic and simulation-generated data are evaluated through internal validation before inclusion. Benchmark evaluations and red-team testing are applied post-training to surface remaining safety gaps across world generation, reasoning, audio, and action tasks. No large-scale data-filtering process can guarantee complete removal of all harmful content; residual risks may remain, particularly in rare edge cases or open-world deployment settings. Ongoing monitoring and dataset review continue post-release.

For more information about the datasets used to train this model, please see the [Public Summary of Training Content](https://docs.nvidia.com/cosmos/latest/cosmos3/index.html).

**Data Modality and Training Data Size**

| Modality | Reasoning Data Sample Count | Generation Data Sample Count |
| -------- | ------------------- | -------------------- |
| Text     | 22M                 | Not Applicable       |
| Image    | 19M                 | 767M                 |
| Video    | 1M                  | 348M                 |
| Audio    | Not Applicable      | 139M                 |
| Action   | Not Applicable      | 7M                   |

**Data Collection Method by dataset**

- Hybrid: Automatic/Sensors, Synthetic, Automated

**Labeling Method by dataset**

- Hybrid: Manually-Labelled, Automated

**Properties:** The training, testing, and evaluation datasets consist of diverse multimodal video, image, audio, action, synthetic, and sensor-conditioned data sourced from NVIDIA-owned data and publicly available, commercially permissive datasets. These datasets are curated to exclude known restricted content and to support building an Omni model that learns to generate and reason about dynamic physical environments across world reasoning and generation tasks.

### Public Datasets

| Dataset                   | Samples     |
|---------------------------|-------------|
| OpenImage                 | 1.2M        |
| Coyo700M                  | 100M        |
| YouTube Video             | 340M        |
| UMI                       | 4.5M        |

### Private Datasets

| Dataset                   | Samples     |
|---------------------------|-------------|
| Egocentric                | 7M          |
| Nexar                     | 0.6M        |
| AgiBot                    | 0.2M        |
| HOI                       | 0.3M        |

### Synthetic Datasets

| Dataset                                 | Samples     |
|-----------------------------------------|-------------|
| synthetic images generated using HiDream-I1       | 15M         |
| synthetic images generated using Qwen-Image-2512  | 14M         |
| synthetic captions generated using Qwen3-VL       | 1115M       |

## Evaluation Datasets

**Data Collection Method by dataset**

- Hybrid: Automatic/Sensors, Synthetic, Automated

**Labeling Method by dataset**

- Hybrid: Manually-Labelled, Automated

**Properties:** The training, testing, and evaluation datasets consist of diverse multimodal video, image, audio, action, synthetic, and sensor-conditioned data sourced from NVIDIA-owned data and publicly available, commercially permissive datasets. These datasets are curated to exclude known restricted content and to support building an Omni model that learns to generate and reason about dynamic physical environments across world reasoning and generation tasks.

## Quality Benchmark

### Reasoner Benchmarks

We compare **Cosmos3-Edge-FP8** with its BF16 counterpart across general reasoning, robotics, smart infrastructure, and driving benchmarks. Each domain score is the unweighted mean of the benchmark scores listed below, using the same benchmark set for BF16 and FP8.

| Domain | BF16 | FP8 |
| --- | --- | --- |
| General ↑ | 56.56 | 58.10 |
| Robotics ↑ | 49.17 | 48.68 |
| Smart Infrastructure ↑ | 52.00 | 51.95 |
| Driving ↑ | 62.50 | 62.38 |

- **General** (18 benchmarks): MMBench_DEV_EN_V11, RealWorldQA, CVBench, VideoPhy2, CausalVQA_4fps, MVPBench, CountBenchQA, AI2D_TEST, DocVQA_VAL, InfoVQA_VAL, OCRBench_v2, LogicVista, MMMU_Pro_10c, MVBench_2fps64f, BlinkSpatial, BlinkDepth, HallusionBench, IFBench
- **Robotics** (10 benchmarks): CosmosReason, RefSpatial, VSI-Bench_32frame, SparBench, MMSIBench_wo_circular, MMSIVideoBench_32frame, HealthSurgiBench, CosmosERQA, RoboSpatialHome, Where2Place
- **Smart Infrastructure** (8 benchmarks): VANTAGE_2DGrounding, VANTAGE_Astro2D, VANTAGE_2DPointing, VANTAGE_DVC, VANTAGE_EventVerification, VANTAGE_SOT, VANTAGE_Temporal, VANTAGE_VQA
- **Driving** (3 benchmarks): LingoQA, AVSpecialCollisionBench, AVSpecialStopBehaviorBench

### Generator Benchmarks

We compare **Cosmos3-Edge-FP8** with its BF16 counterpart. PAIBench-G evaluates text-to-video and image-to-video generation. RBench assesses task correctness, physical plausibility, and visual fidelity in robotics videos. PhysicsIQ evaluates image-to-video generation by comparing predicted video continuations with recorded physical outcomes.

| Benchmark | BF16 | FP8 |
| --- | --- | --- |
| PAIBench-G I2V ↑ | 81.10 | 80.75 |
| PAIBench-G T2V ↑ | 76.90 | 76.58 |
| RBench ↑ | 0.55 | 0.57 |
| PhysicsIQ I2V ↑ | 31.28 | 31.37 |

*For quality benchmarks, BF16 results were obtained using PyTorch, and FP8 results were obtained using vLLM-Omni.*

## Performance Benchmark

The table reports single-GPU inference performance for Cosmos3-Edge-FP8 using FLASH_ATTN unless otherwise noted.

| Hardware | Generator — 480p (frames/s) | Reasoner — time to first token (ms) | Reasoner — output token throughput (tokens/s) | Action Policy — 480p (actions/s, 32-action chunks) |
| --- | ---: | ---: | ---: | ---: |
| H100 | 13.04 | 108.1 | 312.64 | 20.50 |
| H200 | 12.96 | 103.0 | 341.18 | 21.11 |
| H20 | 3.30 | 163.6 | 262.42 | 6.81 |
| DGX Station | 30.63 | 65.4 | 425.65 | 30.48 |
| DGX Spark | 1.65 | 213.2 | 69.46 | 4.03 |
| RTX PRO 6000 | 7.52 | 121.0 | 245.38 | 10.77 |
| RTX PRO 5000 | 4.51 | 99.7 | 243.16 | 9.58 |
| Jetson Thor T5000 | 1.92 | 205.7 | 76.69 | 3.79 |
| Jetson T3000 | 0.88 | 384.3 | 62.16 | 1.81 |
| Jetson AGX Orin | - | 817.8 | 41.46 | - |

A dash (-) indicates unavailable benchmark results for the specified configuration.

- **Generator:** FP8 image-to-video (`i2v`) with vLLM-Omni, 832 × 480 resolution, 121 generated frames, 35 denoising steps, concurrency 1, and one warmup request. Each GPU uses its fastest measured backend for this image-to-video workload: FLASH_ATTN for H100 and H200; CUDNN_ATTN for H20, RTX PRO 6000, DGX Station, DGX Spark, RTX PRO 5000, Thor T5000, and emulated T3000. Throughput is 121 divided by end-to-end server inference time in seconds and measures inference throughput.
- **Reasoner:** FP8 vLLM with concurrency 1, 50 input text tokens plus a 30-second, 374 × 374 video sampled at FPS 1 (30 frames), and 100 output tokens. H100, H200, H20, RTX PRO 6000, and embedded hardware use this workload and FLASH_ATTN; output throughput copies the reported output-token throughput.
- **DGX Station, DGX Spark, and RTX PRO 5000 reasoner:** OSL (output sequence length) 100, FPS 1, and concurrency 1. The attention backend, input text length, video duration, and resolution are unspecified for these results.
- **Action Policy:** FP8 vLLM-Omni, Policy Robot (DROID), 480p, one GPU, 32-action chunks, 30 denoising steps, concurrency 1, and one warmup request. Throughput is 32 divided by end-to-end server inference time in seconds, reported in actions per second. Each GPU uses its fastest measured backend for this workload: FLASH_ATTN for H100 and H200; CUDNN_ATTN for H20, RTX PRO 6000, DGX Station, DGX Spark, RTX PRO 5000, Thor T5000, and emulated T3000.
- **Hardware:** Generator measurements use one H100 SXM 80 GB, H200 SXM 141 GB, or H20 SXM 96 GB GPU. The RTX PRO 6000 generator measurement uses one RTX PRO 6000 Blackwell Server Edition GPU. The RTX PRO 5000 generator measurement uses the 72 GB variant.
- **Embedded generator and action policy:** Thor T5000 and emulated T3000 use FP8 with CUDNN_ATTN and one warmup request. Policy requests use 736 × 544 output in the 480p model tier, with 32 actions plus one conditioning frame. Orin generator and policy measurements use a separate BF16 checkpoint and are omitted from this FP8 table.
- **Embedded hardware:** Reasoner measurements use one integrated GPU: Jetson AGX Thor T5000 (128 GB), a T5000 devkit configured to emulate T3000 (12 SMs, 8 CPUs, 32 GB), and Jetson AGX Orin (64 GB), all in MAXN mode with clocks locked. Orin runs the FP8 checkpoint with weight-only W8A16 compute; Thor uses FP8 compute. T3000 results are emulated measurements. Hardware variants for other rows require matching benchmark results.
- Throughputs are calculated before rounding to two decimal places; time to first token is displayed to one decimal place. No estimates are included.

## Usage

- See [Cosmos](https://github.com/nvidia/cosmos) for details.

### Prompt upsampling

For optimal quality, prompts should be upsampled into a specific JSON structure. Description and code can be found [here](https://github.com/nvidia/cosmos-framework/blob/main/docs/prompt_upsampling.md).

For example, for image-to-video upsampling using Opus-4.6:

```bash
git clone https://github.com/NVIDIA/cosmos-framework.git packages/cosmos-framework
pip install -e packages/cosmos-framework

export PROMPT_UPSAMPLER_ENDPOINT_URL="https://api.anthropic.com/v1/"
export PROMPT_UPSAMPLER_MODEL_NAME="claude-opus-4-6"
export PROMPT_UPSAMPLER_API_TOKEN="<your_token>"

python -m cosmos_framework.inference.prompt_upsampling \
    --input inputs/prompt_upsampler/prompts_i2v.txt \
    --image-list inputs/prompt_upsampler/images.txt \
    --output outputs/prompt_upsampler/upsampled_i2v_prompts_opus \
    --mode image2video \
    --endpoint-url "${PROMPT_UPSAMPLER_ENDPOINT_URL}" \
    --model "${PROMPT_UPSAMPLER_MODEL_NAME}" \
    --api-token "${PROMPT_UPSAMPLER_API_TOKEN}" \
    --resolution 480 \
    --aspect-ratio "16,9" \
    --duration "5s" \
    --fps 24
```

For image-to-video, provide either one shared image via `--image-url` or one image per prompt via `--image-list` (the image-list file must have the same number of non-empty lines as the prompt file). Accepted image formats: local paths, HTTP(S) URLs, and `data:` URLs.

### vLLM-Omni

#### Container

```
docker pull vllm/vllm-omni:cosmos3
```

#### General Invocation

You can use the release-tested `vllm-omni` package for deploying an OpenAI-compatible API inference endpoint.
The recommended vLLM-Omni serving configuration for nvidia/Cosmos3-Edge-FP8 on a single GPU is:

```bash
VLLM_OMNI_USE_QUACK_FP8=0 \
vllm serve nvidia/Cosmos3-Edge-FP8 \
  --omni \
  --host 0.0.0.0 \
  --port 8000 \
  --init-timeout 1800
```

To speed up inference with additional GPUs, enable context parallelism with `--ulysses-degree` or switch to tensor parallelism with `--tensor-parallel-size`. Setting `--enable-layerwise-offload` can help reduce memory usage on GPUs with less available memory.

#### Examples

##### Download example prompts

The example inputs (`assets/`) live in this model repo. Download just this folder with the Hugging Face CLI:

```bash
pip install -U "huggingface_hub<2"
hf download nvidia/Cosmos3-Edge-FP8 assets/ --local-dir Cosmos3-Edge-FP8
cd Cosmos3-Edge-FP8
```

Run all commands below from the downloaded repo root.

---

##### Image to video generation

```python
import json
import mimetypes
from pathlib import Path

import requests

# 1. Read JSON-upsampled prompt and negative prompt
json_prompt = json.load(open("assets/example_i2v_prompt.json"))
negative_prompt = json.load(open("assets/negative_prompt.json"))

# 2. Build and send the multipart API request
url = "http://localhost:8000/v1/videos/sync"
image_path = Path("assets/example_i2v_input.jpg")
mime_type = mimetypes.guess_type(image_path)[0] or "image/png"
data = {
    "prompt": json.dumps(json_prompt),
    "negative_prompt": json.dumps(negative_prompt),
    "size": "832x480",
    "num_frames": "121",
    "fps": "24",
    "num_inference_steps": "20",
    "guidance_scale": "6.0",
    "max_sequence_length": "4096",
    "flow_shift": "12.0",
    "extra_params": json.dumps(
        {
          "use_resolution_template": False,
          "use_duration_template": False,
          "guardrails": True,
        }
    ),
    "seed": "0",
}

with image_path.open("rb") as image_file:
    files = {
        "input_reference": (image_path.name, image_file, mime_type),
    }
    print("Sending request to server...")
    response = requests.post(
        url,
        data=data,
        files=files,
        headers={"Accept": "video/mp4"},
    )
    response.raise_for_status()

# 3. Save the generated video
output_path = Path("/tmp/cosmos3_edge_i2v.mp4")
output_path.write_bytes(response.content)
print(f"Saved video to {output_path}")
```

Example output:

<video controls width="832" height="480" src="https://huggingface.co/nvidia/Cosmos3-Edge-FP8/resolve/main/assets/edge_i2v_output.mp4"></video>

---

##### Action generation

The forward-dynamics example uses UMI robotics action trajectories, and the inverse-dynamics examples use autonomous-vehicle (AV) action trajectories. Source files:

- Forward dynamics first frame: `assets/example_action_fd_umi_first_frame.png`
- Forward dynamics action chunks: `assets/example_action_fd_umi_action_chunks.json`
- Forward dynamics output video: `assets/edge_action_fd_umi_2chunk_output.mp4`
- Inverse dynamics source videos: `assets/example_action_id_av_0_input.mp4`, `assets/example_action_id_av_1_input.mp4`
- Inverse dynamics predicted actions: `assets/edge_action_id_av_0_output.json`, `assets/edge_action_id_av_1_output.json`

###### Action forward dynamics

The example below performs a 2-chunk UMI robotics rollout with the vLLM-Omni `/v1/videos/sync` inference endpoint. Each request sends one conditioning frame through `input_reference` and one 16-step normalized 10-D action chunk through `extra_params["action"]`. The request also sets the top-level `size` field to the input image resolution, so vLLM-Omni returns each chunk at the same resolution as the conditioning image without reflection padding. The stitched output drops each chunk's conditioning frame, producing 32 generated frames. The script extracts the last generated frame from each chunk and uses it as the next chunk's conditioning frame.

```python
import json
import mimetypes
from pathlib import Path

import imageio.v3 as iio
import numpy as np
import requests
from PIL import Image

url = "http://localhost:8000/v1/videos/sync"
first_frame_path = Path("assets/example_action_fd_umi_first_frame.png")
action_spec = json.loads(Path("assets/example_action_fd_umi_action_chunks.json").read_text())
action_chunks = action_spec["action_chunks"]

prompt = action_spec.get("prompt", "mouse arrangement")
fps = int(action_spec.get("fps", 20))
action_chunk_size = int(action_spec.get("action_chunk_size", 16))
current_frame_path = first_frame_path
input_width, input_height = Image.open(first_frame_path).size
chunk_video_paths = []
stitch_frames = []

for chunk_idx, action_chunk in enumerate(action_chunks):
    mime_type = mimetypes.guess_type(current_frame_path)[0] or "image/png"
    extra_params = {
        "action_mode": "forward_dynamics",
        "domain_name": action_spec.get("domain_name", "umi"),
        "action_chunk_size": action_chunk_size,
        "image_size": action_spec.get("image_size", 256),
        "view_point": action_spec.get("view_point", "ego_view"),
        "action": action_chunk,
        "guardrails": True,
    }
    data = {
        "prompt": prompt,
        "num_frames": str(action_chunk_size + 1),  # conditioning frame + generated frames
        "fps": str(fps),
        "size": f"{input_width}x{input_height}",  # return chunks at input resolution
        "num_inference_steps": "30",
        "guidance_scale": "1.0",
        "flow_shift": "10.0",
        "seed": str(chunk_idx),
        "extra_params": json.dumps(extra_params),
    }

    with current_frame_path.open("rb") as image_file:
        files = {"input_reference": (current_frame_path.name, image_file, mime_type)}
        print(f"Sending action FD chunk {chunk_idx} to vLLM-Omni...")
        response = requests.post(
            url,
            data=data,
            files=files,
            headers={"Accept": "video/mp4"},
            timeout=600,
        )
        response.raise_for_status()

    chunk_video_path = Path(f"/tmp/cosmos3_edge_action_fd_chunk_{chunk_idx:02d}.mp4")
    chunk_video_path.write_bytes(response.content)
    chunk_video_paths.append(chunk_video_path)

    # The returned chunk contains the conditioning frame followed by generated frames.
    # Drop the conditioning frame when stitching the generated-only rollout.
    frames = iio.imread(chunk_video_path)
    stitch_frames.extend(frames[1:])

    # Autoregressive conditioning: use the final generated frame from this chunk
    # as the input image for the next vLLM-Omni request.
    if chunk_idx + 1 < len(action_chunks):
        current_frame_path = Path(f"/tmp/cosmos3_edge_action_fd_ar_frame_{chunk_idx + 1:02d}.png")
        iio.imwrite(current_frame_path, frames[-1])

stitched_path = Path("/tmp/cosmos3_edge_action_fd_umi_2chunk.mp4")
iio.imwrite(stitched_path, np.asarray(stitch_frames), fps=fps)
print("Generated chunk videos:", chunk_video_paths)
print("Saved stitched rollout:", stitched_path)
print("stitched resolution:", f"{input_width}x{input_height}")
```


Example output:

<video width="512" controls src="https://huggingface.co/nvidia/Cosmos3-Edge-FP8/resolve/main/assets/edge_action_fd_umi_2chunk_output.mp4"></video>

###### Action inverse dynamics

```python
import json
import time
from pathlib import Path

import requests

base_url = "http://localhost:8000"
input_videos = {
    "av_inverse_0": Path("assets/example_action_id_av_0_input.mp4"),
    "av_inverse_1": Path("assets/example_action_id_av_1_input.mp4"),
}

for name, video_path in input_videos.items():
    extra_params = {
        "action_mode": "inverse_dynamics",
        "domain_name": "av",
        "action_chunk_size": 60,
        "image_size": 480,
        "view_point": "ego_view",
        "raw_action_dim": 9,
        "guardrails": True,
    }
    data = {
        "prompt": "You are an autonomous vehicle planning system.",
        "num_frames": "61",
        "fps": "10",
        "num_inference_steps": "30",
        "guidance_scale": "1.0",
        "flow_shift": "10.0",
        "seed": "0",
        "extra_params": json.dumps(extra_params),
    }

    with video_path.open("rb") as video_file:
        files = {
            "input_reference": (video_path.name, video_file, "video/mp4"),
        }
        print(f"Submitting {name} request to server...")
        response = requests.post(f"{base_url}/v1/videos", data=data, files=files)
        response.raise_for_status()
    initial = response.json()

    while True:
        response = requests.get(f"{base_url}/v1/videos/{initial['id']}", timeout=30)
        response.raise_for_status()
        final = response.json()
        print(initial["id"], final.get("status"), f"{final.get('progress', 0)}%")
        if final.get("status") == "completed":
            break
        if final.get("status") in {"failed", "cancelled"}:
            raise RuntimeError(json.dumps(final, indent=2))
        time.sleep(2)

    action = final.get("action")
    if not action or "data" not in action:
        raise RuntimeError(f"Response did not include action data: {json.dumps(final, indent=2)}")

    output_path = Path(f"/tmp/cosmos3_edge_action_id_{name}.json")
    output_path.write_text(json.dumps(action, indent=2))
    print(f"Saved predicted action to {output_path}")
    print("action shape:", action.get("shape"), "dtype:", action.get("dtype"))
```

Example outputs:

- [av_inverse_0 predicted action JSON](https://huggingface.co/nvidia/Cosmos3-Edge-FP8/blob/main/assets/edge_action_id_av_0_output.json)
- [av_inverse_1 predicted action JSON](https://huggingface.co/nvidia/Cosmos3-Edge-FP8/blob/main/assets/edge_action_id_av_1_output.json)

<img width="1280" src="https://huggingface.co/nvidia/Cosmos3-Edge-FP8/resolve/main/assets/edge_action_id_av_0_output.png">

<img width="1280" src="https://huggingface.co/nvidia/Cosmos3-Edge-FP8/resolve/main/assets/edge_action_id_av_1_output.png">

### Diffusers

Cosmos3-Edge-FP8 is supported in the Hugging Face Diffusers library through [`Cosmos3OmniPipeline`](https://huggingface.co/docs/diffusers/main/en/api/pipelines/cosmos3). The pipeline supports image-to-video generation and action-conditioned forward and inverse dynamics.

#### Container

To install Diffusers with `Cosmos3OmniPipeline`:

```bash
uv venv --python 3.12 --seed --managed-python
source .venv/bin/activate
uv pip install \
  "diffusers @ git+https://github.com/huggingface/diffusers.git" \
  accelerate \
  av \
  cosmos_guardrail \
  huggingface_hub \
  imageio \
  imageio-ffmpeg \
  nvidia-modelopt==0.44.0 \
  torch \
  torchvision \
  transformers
```

#### Examples

The examples use the inputs in this repository's `assets/` directory. Run them from the model repository root.

Enable ModelOpt checkpoint restoration before loading each pipeline. The explicit `hf_hub_download` ensures `transformer/modelopt_state.pth` is present even though it is not included in Diffusers' default Hub download allowlist.

##### Image to video generation

```python
import json
from pathlib import Path

import modelopt.torch.quantization.backends.fp8_per_tensor_gemm  # noqa: F401
import torch
from diffusers import Cosmos3OmniPipeline
from diffusers.schedulers.scheduling_unipc_multistep import UniPCMultistepScheduler
from diffusers.utils import export_to_video, load_image
from huggingface_hub import hf_hub_download
from modelopt.torch.opt import enable_huggingface_checkpointing

# Read the JSON-upsampled positive and negative prompts.
json_prompt = json.loads(Path("assets/example_i2v_prompt.json").read_text())
negative_prompt = json.loads(Path("assets/negative_prompt.json").read_text())

model_id = "nvidia/Cosmos3-Edge-FP8"
enable_huggingface_checkpointing()
hf_hub_download(repo_id=model_id, filename="transformer/modelopt_state.pth")

pipe = Cosmos3OmniPipeline.from_pretrained(
    model_id,
    torch_dtype=torch.bfloat16,
    enable_safety_checker=True,
)
pipe.to("cuda")
pipe.scheduler = UniPCMultistepScheduler.from_config(
    pipe.scheduler.config, flow_shift=12.0, use_karras_sigmas=False
)

result = pipe(
    prompt=json.dumps(json_prompt),
    negative_prompt=json.dumps(negative_prompt),
    image=load_image("assets/example_i2v_input.jpg"),
    num_frames=121,
    height=480,
    width=832,
    fps=24.0,
    num_inference_steps=20,
    guidance_scale=6.0,
    generator=torch.Generator(device="cuda").manual_seed(0),
    add_resolution_template=False,
    add_duration_template=False,
)

output_path = Path("assets/diffusers_outputs/edge_i2v_diffusers.mp4")
output_path.parent.mkdir(parents=True, exist_ok=True)
# macro_block_size=1 preserves the requested 832x480 resolution.
export_to_video(result.video, str(output_path), fps=24, macro_block_size=1)
print(f"Saved video to {output_path}")
```

Example output:

<video controls width="832" height="480" src="https://huggingface.co/nvidia/Cosmos3-Edge-FP8/resolve/main/assets/diffusers_outputs/edge_i2v_diffusers.mp4"></video>

---

##### Action generation

The forward-dynamics example uses UMI robotics action trajectories, and the inverse-dynamics examples use autonomous-vehicle (AV) action trajectories. The pipeline's `CosmosActionCondition` groups the action task, embodiment, action chunk, and conditioning image or video. Unlike the image-to-video example, action prompts are plain task descriptions and should not be prompt-upsampled.

###### Action forward dynamics

This two-chunk UMI rollout conditions the first chunk on `assets/example_action_fd_umi_first_frame.png`, then conditions each subsequent chunk on the final generated frame of the previous chunk. Dropping each chunk's conditioning frame produces a stitched 32-frame rollout.

```python
import json
from pathlib import Path

import modelopt.torch.quantization.backends.fp8_per_tensor_gemm  # noqa: F401
import torch
from diffusers import Cosmos3OmniPipeline, CosmosActionCondition
from diffusers.schedulers.scheduling_unipc_multistep import UniPCMultistepScheduler
from diffusers.utils import export_to_video, load_image
from huggingface_hub import hf_hub_download
from modelopt.torch.opt import enable_huggingface_checkpointing

action_spec = json.loads(Path("assets/example_action_fd_umi_action_chunks.json").read_text())
output_dir = Path("assets/diffusers_outputs")
output_dir.mkdir(parents=True, exist_ok=True)

model_id = "nvidia/Cosmos3-Edge-FP8"
enable_huggingface_checkpointing()
hf_hub_download(repo_id=model_id, filename="transformer/modelopt_state.pth")

pipe = Cosmos3OmniPipeline.from_pretrained(
    model_id,
    torch_dtype=torch.bfloat16,
    enable_safety_checker=True,
)
pipe.to("cuda")
pipe.scheduler = UniPCMultistepScheduler.from_config(
    pipe.scheduler.config, flow_shift=10.0, use_karras_sigmas=False
)

prompt = action_spec.get("prompt", "mouse arrangement")
fps = int(action_spec.get("fps", 20))
chunk_size = int(action_spec.get("action_chunk_size", 16))
current_frame = load_image("assets/example_action_fd_umi_first_frame.png")
stitched_frames = []
chunk_paths = []

for chunk_idx, action_chunk in enumerate(action_spec["action_chunks"]):
    result = pipe(
        prompt=prompt,
        action=CosmosActionCondition(
            mode="forward_dynamics",
            chunk_size=chunk_size,
            domain_name=action_spec.get("domain_name", "umi"),
            resolution_tier=int(action_spec.get("image_size", 256)),
            raw_actions=torch.tensor(action_chunk, dtype=torch.float32),
            image=current_frame,
            view_point=action_spec.get("view_point", "ego_view"),
        ),
        fps=fps,
        num_inference_steps=30,
        guidance_scale=1.0,
        generator=torch.Generator(device="cuda").manual_seed(chunk_idx),
        use_system_prompt=False,
    )

    chunk_path = output_dir / f"edge_action_fd_diffusers_chunk_{chunk_idx:02d}.mp4"
    export_to_video(result.video, str(chunk_path), fps=fps, macro_block_size=1)
    chunk_paths.append(chunk_path)
    stitched_frames.extend(result.video[1:])
    current_frame = result.video[-1]

stitched_path = output_dir / "edge_action_fd_umi_2chunk_diffusers.mp4"
export_to_video(stitched_frames, str(stitched_path), fps=fps, macro_block_size=1)
print("Generated chunk videos:", chunk_paths)
print("Saved stitched rollout:", stitched_path)
```

Example output:

<video controls width="256" height="256" src="https://huggingface.co/nvidia/Cosmos3-Edge-FP8/resolve/main/assets/diffusers_outputs/edge_action_fd_umi_2chunk_diffusers.mp4"></video>

###### Action inverse dynamics

This example predicts the 60-step, 9-D AV action sequence that connects each 61-frame conditioning video. It writes one JSON output per input video.

```python
import json
from pathlib import Path

import modelopt.torch.quantization.backends.fp8_per_tensor_gemm  # noqa: F401
import torch
from diffusers import Cosmos3OmniPipeline, CosmosActionCondition
from diffusers.schedulers.scheduling_unipc_multistep import UniPCMultistepScheduler
from diffusers.utils import load_video
from huggingface_hub import hf_hub_download
from modelopt.torch.opt import enable_huggingface_checkpointing

input_videos = {
    "av_inverse_0": Path("assets/example_action_id_av_0_input.mp4"),
    "av_inverse_1": Path("assets/example_action_id_av_1_input.mp4"),
}
output_dir = Path("assets/diffusers_outputs")
output_dir.mkdir(parents=True, exist_ok=True)

model_id = "nvidia/Cosmos3-Edge-FP8"
enable_huggingface_checkpointing()
hf_hub_download(repo_id=model_id, filename="transformer/modelopt_state.pth")

pipe = Cosmos3OmniPipeline.from_pretrained(
    model_id,
    torch_dtype=torch.bfloat16,
    enable_safety_checker=True,
)
pipe.to("cuda")
pipe.scheduler = UniPCMultistepScheduler.from_config(
    pipe.scheduler.config, flow_shift=10.0, use_karras_sigmas=False
)

for name, video_path in input_videos.items():
    result = pipe(
        prompt="You are an autonomous vehicle planning system.",
        action=CosmosActionCondition(
            mode="inverse_dynamics",
            chunk_size=60,
            domain_name="av",
            resolution_tier=480,
            video=load_video(str(video_path)),
            view_point="ego_view",
        ),
        fps=10,
        num_inference_steps=30,
        guidance_scale=1.0,
        generator=torch.Generator(device="cuda").manual_seed(0),
        use_system_prompt=False,
    )
    if result.action is None:
        raise RuntimeError(f"{name} did not return an action tensor")

    action = result.action[0].cpu()
    output_path = output_dir / f"edge_action_id_{name}_diffusers.json"
    output_path.write_text(
        json.dumps(
            {
                "data": action.tolist(),
                "shape": list(action.shape),
                "dtype": str(action.dtype),
                "raw_action_dim": 9,
                "action_mode": "inverse_dynamics",
                "domain_id": 1,
            },
            indent=2,
        )
        + "\n"
    )
    print(f"Saved predicted action to {output_path}; shape={tuple(action.shape)}")
```

Example outputs:

- [av_inverse_0 predicted action JSON](https://huggingface.co/nvidia/Cosmos3-Edge-FP8/blob/main/assets/diffusers_outputs/edge_action_id_av_inverse_0_diffusers.json)
- [av_inverse_1 predicted action JSON](https://huggingface.co/nvidia/Cosmos3-Edge-FP8/blob/main/assets/diffusers_outputs/edge_action_id_av_inverse_1_diffusers.json)

### vLLM

#### Container

```bash
docker pull vllm/vllm-openai:v0.33.0
```

#### General Invocation

Use the vllm `v0.33.0` version for deploying an OpenAI-compatible API endpoint:

```shell
uv venv --python 3.13 --seed --managed-python
source .venv/bin/activate
uv pip install -U "huggingface_hub<2" "openai==3.42.1"
uv pip install --torch-backend=cu130 vllm==0.33.0
```

Start the Reasoner server:

```shell
vllm serve nvidia/Cosmos3-Edge-FP8 \
    --served-model-name nvidia/Cosmos3-Edge-FP8 \
    --tensor-parallel-size 1 \
    --mm-encoder-tp-mode data \
    --async-scheduling \
    --max-model-len 131072 \
    --allowed-local-media-path / \
    --port 8000
```

#### Examples

##### Reasoning

Run this example from the model repository root. It reads the robot planning prompt from `assets/example_reasoning_prompt.json` and sends `assets/example_reasoning_input.png` to the local vLLM server.

```python
import json
from pathlib import Path

import openai

# 1. Read the image reasoning prompt
example = json.load(open("assets/example_reasoning_prompt.json"))
image_path = Path("assets/example_reasoning_input.png").resolve()
image_url = image_path.as_uri()

# 2. Query the OpenAI-compatible vLLM server
client = openai.OpenAI(
    api_key="EMPTY",
    base_url="http://localhost:8000/v1",
)

response = client.chat.completions.create(
    model=client.models.list().data[0].id,
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "image_url", "image_url": {"url": image_url}},
                {"type": "text", "text": example["prompt"]},
            ],
        },
    ],
    max_tokens=example["max_tokens"],
    seed=0,
)

# 3. Print the generated reasoning output
print(response.choices[0].message.content)
```

Example input:

<img src="https://huggingface.co/nvidia/Cosmos3-Edge-FP8/resolve/main/assets/example_reasoning_input.png" width="640">

Prompt:

```text
The task is to put flower into the red bottle. Generate a plan consisting of subtasks for accomplish the task.
```

Example output from the command above:

```text
Got it, let's see. The task is to put the flower into the red bottle. First, I need to figure out the steps. The flower is currently next to the blue and yellow bottles, and the red bottle is nearby. So first, the robot arm needs to pick up the flower. Then, it has to move the flower over to the red bottle. Then, lower the flower into the red bottle. Wait, but maybe I need to check the positions. Let me visualize the setup: the flower is on the left, red bottle is center-right, blue and yellow are next to it. So steps would be: 1. Move the robot arm to the flower. 2. Grasp the flower with the gripper. 3. Lift the flower from the table. 4. Move the robot arm (with the flower) over to the red bottle. 5. Position the flower above the red bottle's opening. 6. Lower the flower into the red bottle. 7. Release the flower, ensuring it's inside the red bottle. Wait, but maybe some steps are more precise, like aligning the flower with the bottle's opening, then lowering carefully to avoid spilling or dropping. So the subtasks should be broken down into moving to the flower, picking it up, moving to the bottle, positioning, and releasing.</think>
1. Move the robot arm to the flower.
2. Grasp the flower with the gripper.
3. Lift the flower from the table.
4. Move the robot arm (with the flower) to the red bottle.
5. Position the flower above the red bottle's opening.
6. Lower the flower into the red bottle.
7. Release the flower into the red bottle.
So the answer is move to the flower, pick it up, move it to the red bottle, lower it into the red bottle, and release.
```

Thinking is enabled by default. To disable it, add the following argument to the `client.chat.completions.create(...)` call:

```python
extra_body={"chat_template_kwargs": {"enable_thinking": False}}
```

## Limitations

Cosmos3 may produce imperfect outputs in challenging scenarios. Generation artifacts include temporal inconsistency, unstable camera or object motion, imprecise physical interactions, and action-state drift — especially in long-horizon or high-resolution outputs. Reasoning may also be incorrect: object states, causal relationships, spatial geometry, temporal ordering, agent intent, and future outcomes can be misinferred, and complex or long-context inputs may yield hallucinated entities, inconsistent interpretations, or implausible predictions. Because the model lacks an explicit physics simulator, 3D geometry, 4D space-time evolution, object permanence, contact dynamics, and physical laws are only approximated — producing artifacts such as disappearing or morphing objects, unrealistic collisions, and physically implausible motions. Quality further degrades in out-of-distribution environments, safety-critical edge cases, and domains underrepresented in training.

Cosmos3 outputs should not be treated as physically accurate simulation, reliable ground-truth reasoning, or safety-certified decision making. Applications involving robotics control, autonomous systems, scientific simulation, or safety-critical planning require additional validation, external constraints, system-level safety analysis, and domain-specific guardrails before deployment.

## Inference

**Acceleration Engine:** [vLLM-Omni](https://github.com/vllm-project/vllm-omni), [vLLM](https://github.com/vllm-project/vllm), [PyTorch](https://pytorch.org/), [Hugging Face Diffusers](https://github.com/huggingface/diffusers)

**Test Hardware:** See [Performance Benchmark](#performance-benchmark) for the evaluated GPU configurations, including emulated T3000 results and Orin weight-only W8A16 compute.

## Ethical Considerations

NVIDIA believes Trustworthy AI is a shared responsibility and we have established policies and practices to enable development for a wide array of AI applications.  Developers should work with their internal model team to ensure this model meets requirements for the relevant industry and use case and addresses unforeseen product misuse.

Please make sure you have proper rights and permissions for all input image and video content; if image or video includes people, personal health information, or intellectual property, the image or video generated will not blur or maintain proportions of image subjects included.

Users are responsible for model inputs and outputs. Users are responsible for ensuring safe integration of this model, including implementing guardrails as well as other safety mechanisms, prior to deployment.

For more detailed information on ethical considerations for this model, please see the Model Card++ [Explainability](EXPLAINABILITY.md), [Bias](BIAS.md), [Safety & Security](SAFETY.md), and [Privacy](PRIVACY.md) subcards. Please report model quality, risk, security vulnerabilities or NVIDIA AI Concerns [here](https://www.nvidia.com/en-us/support/submit-security-vulnerability/).
