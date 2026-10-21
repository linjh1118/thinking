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
  - vllm
  - vllm-omni
  - sglang
  - sglang-diffusion
  - diffusers
  - text, image, video, audio, and action generation
  - omnimodel
---

# **Cosmos 3: Omnimodal World Models for Physical AI**
**[Model Collection](https://huggingface.co/collections/nvidia/cosmos3)** | **[Code](https://github.com/nvidia/cosmos)** | **[White Paper](https://research.nvidia.com/labs/cosmos-lab/cosmos3/technical-report.pdf)** | **[Website](https://research.nvidia.com/labs/cosmos-lab/cosmos3/)**

[NVIDIA Cosmos™](https://github.com/nvidia/cosmos) is a world foundation model platform designed to accelerate the development of Physical AI by enabling machines to understand, simulate, and interact with the physical world across robotics, autonomous driving, and smart space environments, including industrial and factory-scale applications.

# Model Overview: Cosmos3-Super

## Description

Cosmos3 is a collection of Omnimodal world models capable of generating dynamic, high-quality video, image, audio, and action commands from combinations of text, image, video, and action trajectory inputs. It serves as a foundational building block for a broad range of Physical AI applications and research spanning world understanding, world generation, simulation, and embodied policy learning.

This model is ready for commercial and non-commercial use.

**Model Developer:** NVIDIA

### Model Versions
- Cosmos3-Super:
  - Given multimodal inputs including text, images, video, audio, and action trajectories, generate coherent text, images, video, audio, and action outputs for multimodal understanding, world simulation, future prediction, action reasoning, and Physical AI applications.

### License

This model is released under the [OpenMDW1.1](https://openmdw.ai/license/1-1/)

### Deployment Geography

Global

### Use Case

Physical AI: Encompassing robotics, autonomous vehicles (AV), and smart space environments, including industrial and factory-scale applications.

### Release Date

Hugging Face 05/31/2026 via [https://huggingface.co/collections/nvidia/cosmos3](https://huggingface.co/collections/nvidia/cosmos3)
GitHub 05/31/2026 via [https://github.com/nvidia/cosmos](https://github.com/nvidia/cosmos)

## Model Architecture

**Architecture Type:** Transformer

**Network Architecture:** Mixture-of-Transformers (MoT)

Cosmos3 is an Omni-modal foundation model built on a Mixture-of-Transformers (MoT) architecture consisting of two complementary transformer towers: an autoregressive transformer for discrete token generation and a diffusion transformer for continuous multimodal generation. During inference, text is generated through standard next-token autoregressive decoding, while non-text modalities, such as images, video, audio, and actions, are synthesized through iterative denoising. This unified architecture enables Cosmos3 to model heterogeneous modalities within a single framework while preserving generation mechanisms best suited to each modality.

**This model was developed based on:**  [Cosmos Framework](https://github.com/nvidia/cosmos-framework)

**Number of trainable model parameters:**

- Cosmos3-Super: 64B

## Input/Output Specifications

- **Generator Input**
  - **Input Type(s)**: Text, Image, Video (with audio or without audio), Action Trajectory
  - **Input Format(s)**:
    - Text: String
    - Image: jpg, png, jpeg, webp
    - Video (with or without audio): mp4
    - Action: json (1D list)
  - **Input Parameters**:
    - Text: One-dimensional (1D)
    - Image: Two-dimensional (2D)
    - Video: Three-dimensional (3D)
    - Audio: One-dimensional (1D)
    - Action trajectory: One-dimensional (1D)
  - **Other Properties Related to Input**:
    - For video inputs, we accept various resolutions, including 720p, 480p, and 256p.
    - When using input video with audio muxed into the video MP4 file, the audio should have 2 channels (stereo) and a 48 kHz sample rate.
    - Image and video inputs are RGB color (8 bits per channel, sRGB color space); grayscale inputs are not supported.
    - Action input is a per-frame sequence of robot/agent state or control values (e.g., joint positions, gripper state, camera pose). The full input is a 2D array shaped (T, D), where T is the number of frames and D is the embodiment-specific dimensionality listed below.
    - Input action is only supported for compatible embodiments, including general camera motion (9D), autonomous vehicle (9D), egocentric motion (57D), single Franka Panda arm with RobotiQ gripper (10D), dual Franka Panda arm with RobotiQ gripper (20D), Agibot (29D), UR (10D), Google robot (10D), WidowX 250 (10D), UMI (9D).
  - **Input Size and Length limits:**
    - **Text:** 4096 tokens
    - **Image:** 256p, 480p, and 720p resolution at one of these aspect ratios (16:9, 4:3, 1:1, 3:4, 9:16)
    - **Video:** 256p, 480p, and 720p resolution at one of these aspect ratios (16:9, 4:3, 1:1, 3:4, 9:16). Max number of frames = 5.
    - **Audio:** Max 0.5 second
    - **Action:** 16 – 400 video frames
- **Generator Output**
  - **Output Type(s)**: Image, video, audio, action, text
  - **Output Format(s)**:
    - Image: JPG
    - Video: MP4
    - Audio: Advanced Audio Coding (AAC) stream (muxed within the MP4)
    - Action: 1D list (.json)
    - Text: string
  - **Output Parameters**:
    - Image: Two-dimensional (2D)
    - Video: Three-dimensional (3D)
    - Audio: One-dimensional (1D)
    - Action: One-dimensional (1D)
    - Text: One-dimensional (1D)
  - **Other Properties Related to Output**:
    - The generated video is an MP4 file, with the resolution, frame rate, and duration specified in the input. The generated audio is encoded in AAC format, muxed into the video MP4 file with 2 channels (stereo) and a 48 kHz sample rate.
    - Video generation supports durations from 5 to 400 frames, with 189 frames as the default generation duration.
    - The generated action is only supported for compatible embodiments, including general camera motion (9D), autonomous vehicle (9D), egocentric motion (57D), single Franka Panda arm with RobotiQ gripper (10D), dual Franka Panda arm with RobotiQ gripper (20D), Agibot (29D), UR (10D), Google robot (10D), WidowX 250 (10D), UMI (9D).
    - Audio: 48 kHz stereo AAC stream muxed into video mp4
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
    - Long-context inputs supported up to 256K tokens.
  - **Input Size and Length limits:**
    - **Text:** Up to 256K tokens (context window).
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

- [PyTorch](https://github.com/nvidia/cosmos3)
- [vLLM-Omni](https://github.com/vllm-project/vllm-omni)
- [Hugging Face Diffusers](https://huggingface.co/docs/diffusers/en/index)
- [SGLang](https://github.com/sgl-project/sglang)

**Supported Hardware Microarchitecture Compatibility:**

- NVIDIA Ampere
- NVIDIA Blackwell
- NVIDIA Hopper

**Operating System(s):**

- Linux (We have not tested on other operating systems.)

**Note:** Only BF16 precision is tested. Other precisions like FP4, FP8, and FP16 are not officially supported.

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

- For more information about the datasets used to train this model, please see the [Public Summary of Training Content](https://docs.nvidia.com/cosmos/latest/_downloads/e482b7114ce8dbfbb07d2d4b42cafe4e/training-content-Cosmos-3.pdf).

**Data Modality and Training Data Size**

| Modality | Reasoning Data Sample Count | Generation Data Sample Count |
| -------- | ------------------- | -------------------- |
| Text     | 22M                 | Not Applicable       |
| Image    | 19M                 | 767M                 |
| Video    | 1M                  | 348M                 |
| Audio    | Not Applicable      | 139M                 |
| Action   | Not Applicable      | 8M                   |

**Data Collection Method by dataset**

- Hybrid: Automatic/Sensors, Synthetic, Automated

**Labeling Method by dataset**

- Hybrid: Human, Automated

**Properties:** The training, testing, and evaluation datasets consist of diverse multimodal video, image, audio, action, synthetic, and sensor-conditioned data sourced from NVIDIA-owned data and publicly available, commercially permissive datasets. These datasets are curated to exclude known restricted content and to support building an Omni model that learns to generate and reason about dynamic physical environments across world reasoning and generation tasks.

### Public Datasets

| Dataset&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; | Samples&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; |
|---|---|
| OpenImage | 1.2M |
| Coyo700M | 100M |
| YouTube Video | 340M |
| UMI | 4.5M |

### Private Datasets

| Dataset&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; | Samples&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; |
|---|---|
| Egocentric | 7M |
| Nexar | 0.6M |
| AgiBot | 0.2M |
| HOI | 0.3M |

### Synthetic Datasets

| Dataset | Samples |
|---|---|
| synthetic images generated using HiDream-I1 | 15M |
| synthetic images generated using Qwen-Image-2512 | 14M |
| synthetic captions generated using Qwen3-VL | 1115M |

## Evaluation Datasets

**Data Collection Method by dataset**

- Hybrid: Automatic/Sensors, Synthetic, Automated

**Labeling Method by dataset**

- Hybrid: Human, Automated

**Properties:** The training, testing, and evaluation datasets consist of diverse multimodal video, image, audio, action, synthetic, and sensor-conditioned data sourced from NVIDIA-owned data and publicly available, commercially permissive datasets. These datasets are curated to exclude known restricted content and to support building an Omni model that learns to generate and reason about dynamic physical environments across world reasoning and generation tasks.

## Benchmarks

Please see our [technical paper](https://research.nvidia.com/labs/cosmos-lab/cosmos3/technical-report.pdf) for detailed evaluations of the base model.

### Overall

![Overall benchmark results](images/benchmark-overall.png)

### Reasoning Benchmarks

![Reasoning benchmarks](images/benchmark-reasoning.png)

### Generation Benchmarks

#### Visual-Audio Generation

![Visual & audio generation benchmarks](images/benchmark-visual-audio.png)

#### Action

![Action benchmarks — forward and inverse dynamics](images/benchmark-action-1.png)

## Usage

- See [Cosmos](https://github.com/nvidia/cosmos) for details.

### Prompt upsampling

For optimal quality, text prompts should be upsampled into a specific JSON structure. Description and code can be found [here](https://github.com/nvidia/cosmos-framework/blob/main/docs/prompt_upsampling.md).

For example, for text-to-video upsampling using Opus-4.6:

```bash
git clone https://github.com/NVIDIA/cosmos-framework.git packages/cosmos-framework
pip install -e packages/cosmos-framework

export PROMPT_UPSAMPLER_ENDPOINT_URL="https://api.anthropic.com/v1/"
export PROMPT_UPSAMPLER_MODEL_NAME="claude-opus-4-6"
export PROMPT_UPSAMPLER_API_TOKEN="<you_token>"

python -m cosmos_framework.inference.prompt_upsampling \
    --input assets/example_t2v_prompt_short.txt \
    --output /tmp/upsampled_t2v_opus/ \
    --mode text2video \
    --endpoint-url "${PROMPT_UPSAMPLER_ENDPOINT_URL}" \
    --model "${PROMPT_UPSAMPLER_MODEL_NAME}" \
    --api-token "${PROMPT_UPSAMPLER_API_TOKEN}" \
    --resolution 720 \
    --aspect-ratio "16,9"
```

The JSON-upsampled version of `assets/example_t2v_prompt_short.txt` is saved in `assets/example_t2v_prompt.json` for convenience, and is used for the video generation examples below.

### vLLM-Omni

#### Container

```
docker pull vllm/vllm-omni:cosmos3
```

#### General Invocation

You can use the release-tested `vllm-omni` package for deploying an OpenAI-compatible API inference endpoint.
The recommended vLLM-Omni serving configuration for nvidia/Cosmos3-Super on 8xH200, 8xH100, or 8xA100 is:

```bash
vllm serve nvidia/Cosmos3-Super \
  --omni \
  --host 0.0.0.0 \
  --port 8000 \
  --cfg-parallel-size 2 \
  --ulysses-degree 4 \
  --use-hsdp \
  --hsdp-shard-size 8 \
  --init-timeout 1800
```

With this configuration, video generation with 50 steps should take approximately 55 seconds on H200 GPUs. For 2xH200, one can simply use `--cfg-parallel-size 2 --use-hsdp --hsdp-shard-size 2`, and a video should take approximately 3 minutes to generate. Tensor parallelism is also supported by setting `--tensor-parallel-size`. Setting `--enable-layerwise-offload` can help reduce memory usage on GPUs with less available memory.

#### Examples

##### Download example prompts

The example inputs (`assets/`) live in this model repo. Download just this folder with the Hugging Face CLI:

```bash
pip install -U "huggingface_hub[cli]"
hf download nvidia/Cosmos3-Super assets/ --local-dir Cosmos3-Super
cd Cosmos3-Super
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
    "size": "1280x720",
    "num_frames": "189",
    "fps": "24",
    "num_inference_steps": "35",
    "guidance_scale": "6.0",
    "max_sequence_length": "4096",
    "flow_shift": "10.0",
    "extra_params": json.dumps(
        {
          "use_resolution_template": False,
          "use_duration_template": False,
          "guardrails": True,
        }
    ),
    "seed": "17",
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
output_path = Path("/tmp/cosmos3_super_i2v.mp4")
output_path.write_bytes(response.content)
print(f"Saved video to {output_path}")
```

Example output:

<video controls width="1280" height="720" src="https://huggingface.co/nvidia/Cosmos3-Super/resolve/main/assets/example_i2v_output.mp4"></video>

---

##### Text to video generation

```python
import json
from pathlib import Path

import requests

# 1. Read JSON-upsampled prompt and negative prompt
json_prompt = json.load(open("assets/example_t2v_prompt.json"))
negative_prompt = json.load(open("assets/negative_prompt.json"))

# 2. Build your API payload
data = {
    "prompt": json.dumps(json_prompt),
    "negative_prompt": json.dumps(negative_prompt),
    "size": "1280x720",
    "num_frames": "189",
    "fps": "24",
    "num_inference_steps": "35",
    "guidance_scale": "6.0",
    "max_sequence_length": "4096",
    "flow_shift": "10.0",
    "extra_params": json.dumps(
        {
          "use_resolution_template": False,
          "use_duration_template": False,
          "guardrails": True,
        }
    ),
    "seed": "17",
}

# 3. Send the POST request
url = "http://localhost:8000/v1/videos/sync"
print("Sending request to server...")
response = requests.post(
    url,
    data=data,
    headers={"Accept": "video/mp4"},
)
response.raise_for_status()

# 4. Save the generated video
output_path = Path("/tmp/cosmos3_super_t2v.mp4")
output_path.write_bytes(response.content)
print(f"Saved video to {output_path}")
```

Example output:

<video controls width="1280" height="720" src="https://huggingface.co/nvidia/Cosmos3-Super/resolve/main/assets/example_t2v_output.mp4"></video>

---

##### Image to Video + Audio generation

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
    "size": "1280x720",
    "num_frames": "189",
    "fps": "24",
    "num_inference_steps": "35",
    "guidance_scale": "6.0",
    "max_sequence_length": "4096",
    "generate_sound": "true",
    "sound_duration": "7.875",
    "flow_shift": "10.0",
    "extra_params": json.dumps(
        {
          "use_resolution_template": False,
          "use_duration_template": False,
          "guardrails": True,
        }
    ),
    "seed": "17",
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
output_path = Path("/tmp/cosmos3_super_i2vs.mp4")
output_path.write_bytes(response.content)
print(f"Saved video to {output_path}")
```

Example output:

<video controls width="1280" height="720" src="https://huggingface.co/nvidia/Cosmos3-Super/resolve/main/assets/example_i2vs_output.mp4"></video>

---

##### Text to Video + Audio generation

```python
import json
from pathlib import Path

import requests

# 1. Read JSON-upsampled prompt and negative prompt
json_prompt = json.load(open("assets/example_t2vs_prompt.json"))
negative_prompt = json.load(open("assets/negative_prompt.json"))

# 2. Build your API payload
data = {
    "prompt": json.dumps(json_prompt),
    "negative_prompt": json.dumps(negative_prompt),
    "size": "1280x720",
    "num_frames": "189",
    "fps": "24",
    "num_inference_steps": "35",
    "guidance_scale": "6.0",
    "max_sequence_length": "4096",
    "generate_sound": "true",
    "sound_duration": "7.875",
    "flow_shift": "10.0",
    "extra_params": json.dumps(
        {
          "use_resolution_template": False,
          "use_duration_template": False,
          "guardrails": True,
        }
    ),
    "seed": "17",
}

# 3. Send the POST request
url = "http://localhost:8000/v1/videos/sync"
print("Sending request to server...")
response = requests.post(
    url,
    data=data,
    headers={"Accept": "video/mp4"},
)
response.raise_for_status()

# 4. Save the generated video
output_path = Path("/tmp/cosmos3_super_t2vs.mp4")
output_path.write_bytes(response.content)
print(f"Saved video to {output_path}")
```

Example output:

<video controls width="1280" height="720" src="https://huggingface.co/nvidia/Cosmos3-Super/resolve/main/assets/example_t2vs_output.mp4"></video>

---

##### Action generation

The forward-dynamics example uses AgiBotWorld-Beta robotics action trajectories, and the inverse-dynamics examples use autonomous-vehicle (AV) action trajectories. Source files:

- Forward dynamics first frame: `assets/example_action_fd_agibotworld_first_frame.png`
- Forward dynamics action chunks: `assets/example_action_fd_agibotworld_action_chunks.json`
- Forward dynamics output video: `assets/example_action_fd_agibotworld_4chunk_output.mp4`
- Inverse dynamics source videos: `assets/example_action_id_av_0_input.mp4`, `assets/example_action_id_av_1_input.mp4`
- Inverse dynamics predicted actions: `assets/example_action_id_av_0_output.json`, `assets/example_action_id_av_1_output.json`

###### Action forward dynamics

The example below performs a 4-chunk AgiBotWorld-Beta robotics rollout with the vLLM-Omni `/v1/videos/sync` inference endpoint. Each request sends one conditioning frame through `input_reference` and one 16-step normalized 29-D action chunk through `extra_params["action"]`. The request also sets the top-level `size` field to the input image resolution, so vLLM-Omni returns each chunk at the same resolution as the conditioning image without reflection padding. The stitched output drops each chunk's conditioning frame, producing 64 generated frames. The script extracts the last generated frame from each chunk and uses it as the next chunk's conditioning frame.

```python
import json
import mimetypes
from pathlib import Path

import imageio.v3 as iio
import numpy as np
import requests
from PIL import Image

url = "http://localhost:8000/v1/videos/sync"
first_frame_path = Path("assets/example_action_fd_agibotworld_first_frame.png")
action_spec = json.loads(Path("assets/example_action_fd_agibotworld_action_chunks.json").read_text())
action_chunks = action_spec["action_chunks"]

prompt = action_spec.get("prompt", "Pickup items in the supermarket")
fps = int(action_spec.get("fps", 10))
action_chunk_size = int(action_spec.get("action_chunk_size", 16))
current_frame_path = first_frame_path
input_width, input_height = Image.open(first_frame_path).size
chunk_video_paths = []
stitch_frames = []

for chunk_idx, action_chunk in enumerate(action_chunks):
    mime_type = mimetypes.guess_type(current_frame_path)[0] or "image/png"
    extra_params = {
        "action_mode": "forward_dynamics",
        "domain_name": action_spec.get("domain_name", "agibotworld"),
        "action_chunk_size": action_chunk_size,
        "image_size": action_spec.get("image_size", 480),
        "view_point": action_spec.get("view_point", "concat_view"),
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
        "seed": "0",
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

    chunk_video_path = Path(f"/tmp/cosmos3_super_action_fd_chunk_{chunk_idx:02d}.mp4")
    chunk_video_path.write_bytes(response.content)
    chunk_video_paths.append(chunk_video_path)

    # The returned chunk contains the conditioning frame followed by generated frames.
    # Drop the conditioning frame when stitching the generated-only rollout.
    frames = iio.imread(chunk_video_path)
    stitch_frames.extend(frames[1:])

    # Autoregressive conditioning: use the final generated frame from this chunk
    # as the input image for the next vLLM-Omni request.
    if chunk_idx + 1 < len(action_chunks):
        current_frame_path = Path(f"/tmp/cosmos3_super_action_fd_ar_frame_{chunk_idx + 1:02d}.png")
        iio.imwrite(current_frame_path, frames[-1])

stitched_path = Path("/tmp/cosmos3_super_action_fd_agibotworld_4chunk.mp4")
iio.imwrite(stitched_path, np.asarray(stitch_frames), fps=fps)
print("Generated chunk videos:", chunk_video_paths)
print("Saved stitched rollout:", stitched_path)
print("stitched resolution:", f"{input_width}x{input_height}")
```


Example output:

<video width="640" controls src="https://huggingface.co/nvidia/Cosmos3-Super/resolve/main/assets/example_action_fd_agibotworld_4chunk_output.mp4"></video>

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

    output_path = Path(f"/tmp/cosmos3_super_action_id_{name}.json")
    output_path.write_text(json.dumps(action, indent=2))
    print(f"Saved predicted action to {output_path}")
    print("action shape:", action.get("shape"), "dtype:", action.get("dtype"))
```

Example outputs:

- [av_inverse_0 predicted action JSON](https://huggingface.co/nvidia/Cosmos3-Super/blob/main/assets/example_action_id_av_0_output.json)
- [av_inverse_1 predicted action JSON](https://huggingface.co/nvidia/Cosmos3-Super/blob/main/assets/example_action_id_av_1_output.json)

<img width="1280" src="https://huggingface.co/nvidia/Cosmos3-Super/resolve/main/assets/example_action_id_av_0_output.png">

<img width="1280" src="https://huggingface.co/nvidia/Cosmos3-Super/resolve/main/assets/example_action_id_av_1_output.png">

### vLLM

#### General Invocation

You can use the release-tested `vllm` package for deploying an OpenAI-compatible API endpoint:

```shell
uv venv --python 3.13 --seed --managed-python
source .venv/bin/activate
uv pip install --torch-backend=cu130 "vllm==0.21.0" \
  "vllm-cosmos3 @ git+https://github.com/NVIDIA/cosmos-framework.git#subdirectory=packages/vllm-cosmos3" \
  openai
```

Use `--torch-backend=cu130 "vllm==0.21.0"` for CUDA 13 drivers. For CUDA 12.8 drivers, use `--torch-backend=cu128 "vllm==0.19.1"`.

Start the Reasoner server:

```shell
CUDA_VISIBLE_DEVICES=0,1,2,3 \
vllm serve nvidia/Cosmos3-Super \
  --hf-overrides '{"architectures": ["Cosmos3ReasonerForConditionalGeneration"]}' \
  --tensor-parallel-size 4 \
  --mm-encoder-tp-mode data \
  --async-scheduling \
  --allowed-local-media-path / \
  --media-io-kwargs '{"video": {"num_frames": -1}}' \
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

<img src="assets/example_reasoning_input.png" width="640">

Prompt:

```text
The task is to put flower into the red bottle. Generate a plan consisting of subtasks for accomplish the task.
```

Example output from the command above:

```text
1. Move the arm to the left side of the table.
2. Pick up the flower.
3. Move the arm to the right side of the table.
4. Place the flower into the red bottle.
```

### Diffusers

#### Container

To install diffusers with Cosmos3OmniPipeline:

```
uv venv --python 3.13 --seed --managed-python
source .venv/bin/activate
uv pip install \
  "diffusers @ git+https://github.com/huggingface/diffusers.git" \
  accelerate \
  av \
  cosmos_guardrail \
  huggingface_hub \
  imageio \
  imageio-ffmpeg \
  torch \
  torchvision \
  transformers

```

#### Examples

##### Text to video generation

Run this example from the model repository root. It reads the JSON-upsampled prompt from `assets/example_t2v_prompt.json` and the negative prompt from `assets/negative_prompt.json`. It then loads the pipeline and generate the video, then save it to an MP4 file.

```python
import json
import torch
from diffusers import Cosmos3OmniPipeline
from diffusers.schedulers.scheduling_unipc_multistep import UniPCMultistepScheduler
from diffusers.utils import export_to_video

# Read JSON-upsampled prompt and negative prompt
json_prompt = json.load(open("assets/example_t2v_prompt.json"))
negative_prompt = json.load(open("assets/negative_prompt.json"))

pipe = Cosmos3OmniPipeline.from_pretrained(
    "nvidia/Cosmos3-Super",
    torch_dtype=torch.bfloat16,
    device_map="cuda",
    enable_safety_checker=True,
)
pipe.scheduler = UniPCMultistepScheduler.from_config(pipe.scheduler.config, flow_shift=10.0)

result = pipe(
    prompt=json.dumps(json_prompt),
    negative_prompt=json.dumps(negative_prompt),
    num_frames=189,
    height=720,
    width=1280,
    num_inference_steps=35,
    guidance_scale=6.0,
    generator=torch.Generator(device="cuda").manual_seed(123),
)

export_to_video(result.video, "/tmp/cosmos3_super_t2v_diffusers.mp4", fps=24)
print("Saved video to /tmp/cosmos3_super_t2v_diffusers.mp4")
```

Example output:

<video controls width="1280" height="720" src="https://huggingface.co/nvidia/Cosmos3-Super/resolve/main/assets/example_t2v_diffusers_output.mp4"></video>

### SGLang

[SGLang Diffusion](https://docs.sglang.io/docs/sglang-diffusion/index) can serve `nvidia/Cosmos3-Super` through OpenAI-compatible image and video generation endpoints. Install SGLang from the main branch with diffusion dependencies, then start the server:

```bash
git clone --branch main https://github.com/sgl-project/sglang.git
cd sglang
pip install -e "python[diffusion]"
pip install "cosmos-guardrail==0.3.1"

sglang serve \
  --model-path nvidia/Cosmos3-Super \
  --num-gpus 4
```

Cosmos 3 support in SGLang Diffusion currently requires the SGLang main branch. Switch to a stable SGLang release once Cosmos 3 support is included there.

For the video-specialized checkpoint:

```bash
sglang serve \
  --model-path nvidia/Cosmos3-Super-Image2Video \
  --num-gpus 4
```

Supported SGLang endpoints:

| Mode | Endpoint | Notes |
| --- | --- | --- |
| Text to image | `POST /v1/images/generations` | Returns base64 image data by default |
| Text to video | `POST /v1/videos` | Creates an async job; poll `GET /v1/videos/{id}` and download `/content` |
| Image to video | `POST /v1/videos` | Upload the conditioning image with `input_reference` |

Example text-to-video request:

```bash
job_id=$(curl -sS -X POST http://localhost:30000/v1/videos \
  --form-string "prompt=A small warehouse robot moves a blue box across a clean floor." \
  --form-string "negative_prompt=blurry, distorted, low quality" \
  --form-string "size=1280x720" \
  --form-string "num_frames=81" \
  --form-string "fps=24" \
  --form-string "num_inference_steps=35" \
  --form-string "guidance_scale=4.0" \
  --form-string "flow_shift=10.0" \
  --form-string "seed=42" \
  --form-string 'extra_params={"guardrails":true,"use_resolution_template":false,"use_duration_template":false}' \
  | python -c 'import json, sys; print(json.load(sys.stdin)["id"])')

while true; do
  status=$(curl -sS "http://localhost:30000/v1/videos/${job_id}" \
    | python -c 'import json, sys; print(json.load(sys.stdin)["status"])')
  [ "$status" = "completed" ] && break
  [ "$status" = "failed" ] && exit 1
  sleep 1
done

curl -sS -L "http://localhost:30000/v1/videos/${job_id}/content" \
  -o cosmos3_super_t2v_output.mp4
```

Video-to-video, video-with-sound, and action generation are not supported by SGLang yet.

For complete serving instructions and request examples, see the [Cosmos3 SGLang cookbook](https://docs.sglang.io/cookbook/diffusion/Cosmos/Cosmos3).

## Limitations

Cosmos3 may produce imperfect outputs in challenging scenarios. Generation artifacts include temporal inconsistency, unstable camera or object motion, imprecise physical interactions, inaccurate audio-video synchronization, and action-state drift — especially in long-horizon or high-resolution outputs. Reasoning may also be incorrect: object states, causal relationships, spatial geometry, temporal ordering, agent intent, and future outcomes can be misinferred, and complex or long-context inputs may yield hallucinated entities, inconsistent interpretations, or implausible predictions. Because the model lacks an explicit physics simulator, 3D geometry, 4D space-time evolution, object permanence, contact dynamics, and physical laws are only approximated — producing artifacts such as disappearing or morphing objects, unrealistic collisions, and physically implausible motions. Quality further degrades in out-of-distribution environments, safety-critical edge cases, and domains underrepresented in training.

Cosmos3 outputs should not be treated as physically accurate simulation, reliable ground-truth reasoning, or safety-certified decision making. Applications involving robotics control, autonomous systems, scientific simulation, or safety-critical planning require additional validation, external constraints, system-level safety analysis, and domain-specific guardrails before deployment.

## Inference

**Acceleration Engine:** [PyTorch](https://pytorch.org/), [vLLM](https://github.com/vllm-project/vllm), [vLLM-Omni](https://github.com/vllm-project/vllm-omni), [Hugging Face Diffusers](https://github.com/huggingface/diffusers), [SGLang](https://github.com/sgl-project/sglang), [SGLang Diffusion](https://docs.sglang.io/docs/sglang-diffusion/index)

**Test Hardware:** GB200 and H100

## Ethical Considerations

NVIDIA believes Trustworthy AI is a shared responsibility and we have established policies and practices to enable development for a wide array of AI applications.  Developers should work with their internal model team to ensure this model meets requirements for the relevant industry and use case and addresses unforeseen product misuse.

Please make sure you have proper rights and permissions for all input image and video content; if image or video includes people, personal health information, or intellectual property, the image or video generated will not blur or maintain proportions of image subjects included.

Users are responsible for model inputs and outputs. Users are responsible for ensuring safe integration of this model, including implementing guardrails as well as other safety mechanisms, prior to deployment.

For more detailed information on ethical considerations for this model, please see the Model Card++ [Explainability](EXPLAINABILITY.md), [Bias](BIAS.md), [Safety & Security](SAFETY.md), and [Privacy](PRIVACY.md) subcards. Please report model quality, risk, security vulnerabilities or NVIDIA AI Concerns [here](https://www.nvidia.com/en-us/support/submit-security-vulnerability/).
