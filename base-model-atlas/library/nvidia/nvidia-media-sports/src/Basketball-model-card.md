---
base_model: nvidia/Nemotron-3-Nano-Omni-30B-A3B-Reasoning-BF16
base_model_relation: finetune
library_name: transformers
license: other
license_name: openmdw-1.1
license_link: >-
  https://openmdw.ai/license/1-1/
pipeline_tag: any-to-any
tags:
- nvidia
- pytorch
- multimodal
track_downloads: true
---

# Model Overview

## NVIDIA-NemotronLabs-AI-for-Media-Sports-Basketball

## At a Glance

| | |
|---|---|
| **Total parameters** | 31B (Mamba2-Transformer hybrid Mixture of Experts (MoE)) |
| **Active parameters** | ~3B per token |
| **Max context** | 256k tokens |
| **Modalities (in)** | Video, Audio, Image, Text |
| **Modality (out)** | Text |
| **Best for** | Play-level basketball Q&A, player action and shot understanding, play-structure reasoning, player identification (jersey numbers and team colours), and structured play captioning |
| **Fine-tuning data** | 127k Q&A pairs over 11.2k play clips (51 Basketball games) |
| **Minimum GPU (BF16)** | 1× A100 80GB or 1× H100 80GB (single-GPU); 1× B200 / 1× H200 recommended |
| **Precisions** | bfloat16 (BF16) (`NVIDIA-NemotronLabs-AI-for-Media-Sports-Basketball`, ~62 GB) — TBD |

<video src="https://huggingface.co/nvidia/NVIDIA-NemotronLabs-AI-for-Media-Sports-Basketball/resolve/main/media/basketball_demo.mp4" controls width="100%"></video>

### Description:
NVIDIA-NemotronLabs-AI-for-Media-Sports-Basketball is a fine-tuned multimodal large language model derived from Nemotron 3 Nano Omni. It was further trained on Q&A pairs generated from BARD, a public dataset of play-level basketball broadcast video clips with human-validated annotations, to specialize in basketball play understanding. The model supports structured multiple-choice and open-ended Q&A over play clips, covering player actions, shot mechanics and outcomes, rebounding, play structure, player identification (jersey numbers and team colours), and structured play captioning. It works best when a full basketball play clip is passed as input. <br>


This model is fine-tuned from Nemotron 3 Nano Omni on Q&A pairs generated from the public [BARD dataset](https://huggingface.co/datasets/GabrieleGiudici/BARD) (Basketball Action Recognition Dataset, CC BY 4.0) of basketball play video clips using the [NVIDIA Sports Intelligence playbooks](https://github.com/NVIDIA/sports-intelligence-playbooks). For base model details, see the [base model card](https://huggingface.co/nvidia/Nemotron-3-Nano-Omni-30B-A3B-Reasoning-BF16). <br>

This model is ready for commercial or non-commercial use. <br>

### License/Terms of Use

Governing Terms: Use of this model is governed by the [OpenMDW License Agreement v1.1 (OpenMDW-1.1)](https://openmdw.ai/license/1-1/)<br>

### Deployment Geography:
Global <br>

### Use Case: <br>
This model is designed for basketball-specific multimodal understanding over play-level video. Expected users include:
- Basketball broadcast and media workflows — play-level Q&A, player action and shot-outcome understanding over broadcast footage
- Coaching and performance analysis — structured and open-ended questions about actions, shots, rebounds, and play structure on play clips
- Sports analytics and production — player identification (jersey number and team colour) and play-structure reasoning aligned with play-level annotations
- Enterprise basketball applications — searchable play-level understanding and basketball-domain assistants over archived game video


### Release Date: <br>
Hugging Face 10/15/2026 via [Hugging Face](https://huggingface.co/nvidia/NVIDIA-NemotronLabs-AI-for-Media-Sports-Basketball) <br>

## Model Architecture:
**Architecture Type:** Other (Mamba2-Transformer hybrid Mixture of Experts backbone with multimodal encoders) <br>

**Network Architecture:**
- [Nemotron 3 Nano LLM (30B A3B)](https://huggingface.co/nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B-BF16) — 31B-parameter Mamba2-Transformer hybrid MoE backbone with ~3B active parameters per token.
- [CRADIO v4-H](https://huggingface.co/nvidia/C-RADIOv4-H) — vision encoder for image and video frames.
- [Parakeet](https://huggingface.co/nvidia/parakeet-tdt-0.6b-v2) — speech encoder for audio inputs.

**Number of model parameters:** 3.1 x 10^10 (31B A3B) <br>

**How the model was developed:** Weights are initialized from the pretrained Nemotron 3 Nano Omni BF16 checkpoint. Fine-tuning trains the language-model parameters and the vision encoder (with its projector); the audio encoder remains frozen. Video inputs are sampled at 2 FPS up to 32 frames, with each sampled frame encoded as its own temporal patch at 4096 visual patches per frame. Optimization uses AdamW (learning rate 5×10⁻⁵, β=(0.9, 0.999)) with warmup and cosine decay, regularized by weight decay 0.05 and gradient clipping at max-norm 1.0, with no additional damping. Training is BF16 packed supervised fine-tuning over play-level basketball clips. Hyperparameters follow the published NeMo AutoModel recipe rather than a dedicated search. <br>


## Input(s): <br>
**Input Type(s):** Video, Audio, Image, Text <br>

**Input Format(s):** <br> 
- Video: mp4, short play-level clips (fine-tuning clips were 3–38 seconds of 720p broadcast footage at 60 FPS (frames per second)). For basketball tasks, pass a full basketball play clip as input for best results, sampled at 2 FPS / up to 32 frames to match the fine-tuning configuration.
- Audio: wav, mp3 files (up to 1 hour), 8kHz and higher sampling rates
- Image: Red, Green, Blue (RGB) (jpeg, png)
- Text: String <br>

**Input Parameters:** <br>
- Video: Three-Dimensional (3D)
- Audio: One-Dimensional (1D)
- Image: Two-Dimensional (2D)
- Text: One-Dimensional (1D) <br>

**Other Properties Related to Input:** <br>
- Recommended input: a full basketball play (video clip, with broadcast audio when available), matching the play-level clips used during fine-tuning
- Maximum context length up to 256k tokens 
- Language support: English only  <br>


## Output(s)

**Output Type(s):** Text <br>

**Output Format(s):** <br>
- Text: String <br>

**Output Parameters:** <br>
- Text: One-Dimensional (1D) <br>

**Other Properties Related to Output:** <br>
- Maximum context length up to 256k tokens. <br>

Our AI models are designed and/or optimized to run on NVIDIA GPU-accelerated systems. By leveraging NVIDIA's hardware (e.g. GPU cores) and software frameworks (e.g., CUDA libraries), the model achieves faster training and inference times compared to central processing unit (CPU)-only solutions. <br>

## Software Integration:
**Runtime Engine(s):**
* NeMo <br>
* Megatron <br>

**Supported Hardware Microarchitecture Compatibility:** <br>
* NVIDIA Ampere (A100 80GB SXM/NVLink) <br>
* NVIDIA Blackwell (B200 SXM/NVLink, RTX Pro 6000 SE, DGX Spark, Jetson Thor, RTX 5090) <br>
* NVIDIA Hopper (H100 SXM/NVLink, H200 SXM/NVLink) <br>
* NVIDIA Lovelace (L40S) <br>

**Preferred/Supported Operating System(s):**
* Linux <br>

The integration of foundation and fine-tuned models into AI systems requires additional testing using use-case-specific data to ensure safe and effective deployment. Following the V-model methodology, iterative testing and validation at both unit and system levels are essential to mitigate risks, meet technical and functional requirements, and ensure compliance with safety and ethical standards before deployment. <br>

---

## Quick Start

### Video inference

Provide a full basketball play as an MP4, with broadcast audio when available. Frames are sampled with [`video_io.py`](video_io.py), included with this model.

#### Convenience script

For a ready-to-run CLI (download, load, sample frames, and generate), use [`video_inference.py`](video_inference.py) in this repo. Set up the environment with either option, then run the script.

**Option 1**, pip (Python 3.12, NVIDIA driver 570 or newer). **Linux x86_64:** [`requirements.txt`](requirements.txt) (prerequisites at the top of that file). **Linux aarch64:** [`requirements-linux-aarch64.txt`](requirements-linux-aarch64.txt) instead of `requirements.txt` (prerequisites and install steps at the top of that file). On **GB10 / DGX Spark**, after that install, run `pip install triton==3.9.0 --no-deps` (torch pins an older Triton; required for Mamba on Blackwell).

```bash
python3 -c 'import sys; assert sys.version_info[:2] == (3, 12), f"Python 3.12 required, found {sys.version.split()[0]}"'
pip install -r requirements.txt  # Linux aarch64: requirements-linux-aarch64.txt; then triton==3.9.0 --no-deps on GB10
# Verify the GPU driver and the CUDA kernels before downloading the model
python -c 'import torch; assert torch.cuda.is_available(), "No usable CUDA GPU: NVIDIA driver 570 or newer is required"; import flash_attn, causal_conv1d, mamba_ssm; print("GPU and kernels OK")'
```

**Option 2**, Docker (NeMo AutoModel 26.06 container; requires Docker with the NVIDIA Container Toolkit):

```bash
docker run --gpus all -it --rm \
  -v "$HOME/.cache/huggingface:/root/.cache/huggingface" \
  -v "$PWD":/workspace -w /workspace \
  nvcr.io/nvidia/nemo-automodel:26.06.00 bash
pip install decord librosa imageio-ffmpeg
```

On **Linux aarch64**, install **`decord2`** instead of **`decord`**.

Run from the directory holding `video_inference.py` and your MP4:

```bash
python video_inference.py \
  --video basketball_play.mp4 \
  --question "Analyze the basketball video and extract all player actions. For each action, identify the player's jersey number, jersey colour, and action type, using the format: \"A player with jersey number <n> and jersey_color <colour> made a <action> which result was made/miss and was assisted by other player with jersey number <n>\"."
```

Add `--local-files-only` after weights are cached. If librosa cannot decode MP4 audio, `video_inference.py` extracts a WAV with ffmpeg (`imageio-ffmpeg` or a system `ffmpeg`); pass `--extract-audio-wav` to force that path, or `--no-audio` to skip audio.

The first `AutoModel.from_pretrained(..., trust_remote_code=True)` also downloads RADIO vision code from [`nvidia/C-RADIOv4-H`](https://huggingface.co/nvidia/C-RADIOv4-H).

Default inference policy (same as [`video_inference.py`](video_inference.py)): **2 frames per second (FPS)**, up to **32 frames**, **512** new tokens, **video + audio** from the MP4, greedy decode, `video_pruning_rate=0.0`.

#### Python snippet

The core inference steps (functionally equivalent to `video_inference.py`):

```python
import importlib.util
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

import torch
from huggingface_hub import snapshot_download
from transformers import AutoConfig, AutoModel, AutoProcessor
from transformers.video_utils import VideoMetadata

repo_id = "nvidia/NVIDIA-NemotronLabs-AI-for-Media-Sports-Basketball"
video_path = "/path/to/basketball_play.mp4"
question = (
    "Analyze the basketball video and extract all player actions. For each action, "
    "identify the player's jersey number, jersey colour, and action type, using the "
    'format: "A player with jersey number <n> and jersey_color <colour> made a <action> '
    'which result was made/miss and was assisted by other player with jersey number <n>".'
)
video_fps, max_video_frames, max_new_tokens = 2, 32, 512
revision, local_files_only = None, False  # optional: pin Hub commit; cache-only load

cache_dir = os.environ.get("HF_HOME") or os.environ.get("HF_HUB_CACHE")
hub = {"trust_remote_code": True, "local_files_only": local_files_only}
if cache_dir:
    hub["cache_dir"] = cache_dir
if revision:
    hub["revision"] = revision
snapshot_dir = snapshot_download(
    repo_id=repo_id, repo_type="model", **{k: v for k, v in hub.items() if k != "trust_remote_code"}
)

spec = importlib.util.spec_from_file_location("checkpoint_video_io", Path(snapshot_dir) / "video_io.py")
video_io = importlib.util.module_from_spec(spec)
spec.loader.exec_module(video_io)
frame_urls, metadata = video_io.sample_video_frames_to_data_urls(
    video_path, fps=max(0, int(video_fps)), nframe_max=max_video_frames,
)
frames = [video_io.pil_image_from_base64(url) for url in frame_urls]
video_metadata = VideoMetadata(
    total_num_frames=metadata.total_num_frames, fps=metadata.fps, frames_indices=metadata.frames_indices,
)

ffmpeg = shutil.which("ffmpeg")
if ffmpeg is None:
    import imageio_ffmpeg
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
audio_wav = tempfile.NamedTemporaryFile(suffix=".wav", delete=False).name
subprocess.run(
    [ffmpeg, "-nostdin", "-y", "-i", video_path, "-vn", "-acodec", "pcm_s16le",
     "-ar", "16000", "-ac", "1", audio_wav],
    check=True, capture_output=True,
)

processor = AutoProcessor.from_pretrained(repo_id, **hub)
config = AutoConfig.from_pretrained(repo_id, **hub)
config.video_pruning_rate = 0.0
model = AutoModel.from_pretrained(
    repo_id, config=config, torch_dtype=torch.bfloat16,
    device_map={"": 0} if torch.cuda.is_available() else None, low_cpu_mem_usage=True, **hub,
)
if hasattr(model, "vision_model") and hasattr(model.vision_model, "radio_model"):
    model.vision_model.radio_model.summary_idxs = None
model.eval()

prompt = processor.tokenizer.apply_chat_template(
    [{"role": "user", "content": f"{processor.video_token}\n{processor.audio_token}\n{question}"}],
    tokenize=False, add_generation_prompt=True, enable_thinking=False,
)
inputs = processor(
    text=[prompt], videos=frames, audio=[audio_wav], return_tensors="pt", do_sample_frames=False,
    videos_kwargs={"video_metadata": video_metadata}, audio_kwargs={"sampling_rate": 16000},
)
for key in ("num_patches", "num_tokens", "imgs_sizes"):
    inputs.pop(key, None)
device = next(model.parameters()).device
inputs = {k: v.to(device) if isinstance(v, torch.Tensor) else v for k, v in inputs.items()}

def trim_generated_ids(input_ids, generated_ids):
    if hasattr(generated_ids, "sequences"):
        generated_ids = generated_ids.sequences
    if generated_ids.dim() == 1:
        return [generated_ids[input_ids.shape[-1]:]]
    if input_ids.dim() == 1:
        input_ids = input_ids.unsqueeze(0)
    return [out_ids[len(in_ids):] for in_ids, out_ids in zip(input_ids, generated_ids)]

with torch.no_grad():
    generated_ids = model.generate(**inputs, max_new_tokens=max_new_tokens, do_sample=False, output_hidden_states=False)
print(processor.batch_decode(
    trim_generated_ids(inputs["input_ids"], generated_ids), skip_special_tokens=True, clean_up_tokenization_spaces=False,
)[0].strip())
```

Requires one GPU with ~80 GB memory (BF16). Authenticate with `hf auth login` before downloading a private repo. Frame sampling uses `decord` (Linux aarch64: install `decord2`). MP4 audio is decoded by extracting a 16 kHz WAV with ffmpeg (`imageio-ffmpeg` or a system `ffmpeg`); librosa/soundfile cannot open many MP4s directly. `summary_idxs | MISSING` on load is expected.


---

## Training, Testing, and Evaluation Datasets:

### Base Model
This model is a fine-tuned variant of [Nemotron 3 Nano Omni 30B-A3B-Reasoning](https://huggingface.co/nvidia/Nemotron-3-Nano-Omni-30B-A3B-Reasoning-BF16), retaining the same Mamba2-Transformer hybrid MoE architecture and multimodal encoders (CRADIO v4-H vision encoder and Parakeet speech encoder). <br>

### Training Dataset

**Dataset Name:** BARD categorical Q&A dataset (template-generated from the public [BARD dataset](https://huggingface.co/datasets/GabrieleGiudici/BARD) — Basketball Action Recognition Dataset, CC BY 4.0) <br>
**Data Modality:** Video, Text <br>
**Video Training Data Size:** Less than 100 Hours (11,218 play-level video clips) <br>
**Text Training Data Size:** Less than 1 Billion Tokens (127,211 training Q&A examples) <br>
**Dataset Size:** 127,211 training examples <br>
**Data Collection Method:** Automated (play-level clips from the public BARD dataset) <br>
**Labeling Method:** Hybrid: Automated, Human-Validated (BARD annotations are human-validated by the dataset authors; Q&A pairs are template-generated from those annotations with programmatic quality gates) <br>
**Time period for training data collection:** 2024-2025 <br>
**Properties (Quantity, Dataset Descriptions, Sensor(s)):** 127,211 basketball play video Q&A examples (101,773 multiple-choice and 25,438 open-ended) from 11,218 play-level clips across 51 basketball games and 16 question templates (14 multiple-choice and 2 open-ended) in 4 capability areas (Fine-Grained Visual Recognition, Match Structure & Reasoning, Player Identification, Commentary & Reporting). Content is 720p/60 FPS basketball broadcast footage with live commentary audio from the public BARD dataset (2024–25 season), with English questions and answers template-generated from BARD's human-validated annotations (player actions, shot types and results, jersey numbers, team colours). No sensor-derived metadata beyond standard video/audio capture. **Linguistic characteristics:** English-only basketball-domain questions and answers in multiple-choice and open-ended formats covering player actions, shot mechanics and outcomes, rebounding, play structure, possession outcomes, player identification (jersey number and team colour), and structured play captioning. <br>

### Testing Dataset

**Dataset Name:** BARD categorical Q&A dataset — Test (unseen games) partition (derived from the public BARD dataset) <br>
**Dataset Size:** 26,201 test examples from 9 fully held-out games (2,208 play-level clips; no training game overlap) <br>
**Data Collection Method:** Automated (play-level clips from the public BARD dataset) <br>
**Labeling Method:** Hybrid: Automated, Human-Validated <br>
**Properties (Quantity, Dataset Descriptions, Sensor(s)):** Q&A pairs from **9 fully held-out games** (no training game overlap) — 2,208 play-level clips, 26,201 examples. English basketball-domain labels aligned with the training taxonomy. The corpus also includes a validation split (6,695 examples sharing clips with training) and a separate Test (seen games) partition (15,086 examples of held-out clips from the 51 games represented in training, with game-level overlap only); **only Test (unseen games) was used for reported model testing.** <br>

### Evaluation Dataset

**Dataset Name:** BARD categorical Test (unseen games) balanced evaluation subset (derived from the public BARD dataset) <br>
**Dataset Size:** 2,500 evaluation examples — a fixed, category-balanced subset of the Test (unseen games) partition (250 examples per fine-grained category, seeded sampling; 2,125 multiple-choice and 375 open-ended) used for MCQ accuracy and open-ended judge scoring <br>
**Data Collection Method:** Automated (play-level clips from the public BARD dataset) <br>
**Labeling Method:** Hybrid: Automated, Human-Validated <br>
**Properties (Quantity, Dataset Descriptions, Sensor(s)):** **Test (unseen games)** — 9 fully held-out games with no training game overlap (2,208 play-level clips, 26,201 Q&A examples), from which a fixed category-balanced subset of 2,500 examples (250 per fine-grained category, seeded sampling) was used for reported metrics. Evaluated with automated MCQ scoring and LLM-as-judge pass@9 metrics on open-ended responses. English basketball-domain questions across 16 question templates in 4 capability areas. Test (seen games) was not used for reported metrics. <br>

Fine-tuning was performed on top of the base Nemotron 3 Nano Omni weights using the BARD-derived basketball Q&A dataset. Pre-training dataset details for the base model are documented in the [base Nemotron 3 Nano Omni model card](https://huggingface.co/nvidia/Nemotron-3-Nano-Omni-30B-A3B-Reasoning-BF16). <br>


# Inference:
**Acceleration Engine:** PyTorch, Hugging Face Transformers, NeMo AutoModel <br>
**Test Hardware:** <br>
* NVIDIA Hopper H100 SXM <br>
* NVIDIA Hopper H200 SXM <br>
* NVIDIA Blackwell B200 SXM <br>
* NVIDIA Ampere A100 80GB SXM <br>
* NVIDIA Blackwell GB200 NVL72 <br>
* NVIDIA Blackwell RTX PRO 6000 SE <br>
* NVIDIA Lovelace L40S PCIe 48GB <br>
* NVIDIA Blackwell DGX Spark <br>
* NVIDIA Blackwell Jetson Thor <br>
* NVIDIA Blackwell RTX 5090

## Ethical Considerations:
NVIDIA believes Trustworthy AI is a shared responsibility and we have established policies and practices to enable development for a wide array of AI applications. When downloaded or used in accordance with our terms of service, developers should work with their internal model team to ensure this model meets requirements for the relevant industry and use case and addresses unforeseen product misuse. <br>

Please make sure you have proper rights and permissions for all input image and video content; if image or video includes people, personal health information, or intellectual property, the image or video generated will not blur or maintain proportions of image subjects included. <br>

For more detailed information on ethical considerations for this model, please see the Model Card++ [Bias](bias.md), [Explainability](explainability.md), [Safety & Security](safety.md), and [Privacy](privacy.md) Subcards. <br>

Please report model quality, risk, security vulnerabilities or NVIDIA AI Concerns [here](https://www.nvidia.com/en-us/support/submit-security-vulnerability/). <br>
