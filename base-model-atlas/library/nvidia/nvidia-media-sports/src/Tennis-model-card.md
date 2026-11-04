---
library_name: transformers
license: other
license_name: openmdw-1.1
license_link: >-
  https://openmdw.ai/license/1-1/
base_model: nvidia/Nemotron-3-Nano-Omni-30B-A3B-Reasoning-BF16
base_model_relation: finetune
pipeline_tag: any-to-any
tags:
- nvidia
- pytorch
- multimodal
track_downloads: true
---

# Model Overview

## NVIDIA-NemotronLabs-AI-for-Media-Sports-Tennis

## At a Glance

| | |
|---|---|
| **Total parameters** | 31B (Mamba2-Transformer hybrid Mixture of Experts (MoE)) |
| **Active parameters** | ~3B per token |
| **Max context** | 256k tokens |
| **Modalities (in)** | Video, Audio, Image, Text |
| **Modality (out)** | Text |
| **Best for** | Point-level tennis Q&A, shot and court understanding, match-state reasoning, rules knowledge, and audio-aware point analysis |
| **Fine-tuning data** | 1.31M Q&A pairs over 43k point clips (239 matches) |
| **Minimum GPU (BF16)** | 1× A100 80GB or 1× H100 80GB (single-GPU); 1× B200 / 1× H200 recommended |
| **Precisions** | bfloat16 (BF16) (`NVIDIA-NemotronLabs-AI-for-Media-Sports-Tennis`, ~62 GB) — TBD |

<video src="https://huggingface.co/nvidia/NVIDIA-NemotronLabs-AI-for-Media-Sports-Tennis/resolve/main/media/tennis_demo.mp4" controls width="100%"></video>

### Description:
NVIDIA-NemotronLabs-AI-for-Media-Sports-Tennis is a fine-tuned multimodal large language model derived from Nemotron 3 Nano Omni. It was further trained on an in-house NVIDIA tennis dataset of manually labeled point-level video clips to specialize in tennis match understanding. The model supports structured multiple-choice and open-ended Q&A over point clips, covering shot mechanics, court positioning, player movement, match facts, rules knowledge, and audio cues. It works best when a full tennis point clip is passed as input. <br>


This model is fine-tuned from Nemotron 3 Nano Omni on an in-house NVIDIA tennis dataset of tennis point video clips using the [NVIDIA Sports Intelligence playbooks](https://github.com/NVIDIA/sports-intelligence-playbooks). For base model details, see the [base model card](https://huggingface.co/nvidia/Nemotron-3-Nano-Omni-30B-A3B-Reasoning-BF16). <br>

This model is ready for commercial or non-commercial use. <br>

### License/Terms of Use

Governing Terms: Use of this model is governed by the [OpenMDW License Agreement v1.1 (OpenMDW-1.1)](https://openmdw.ai/license/1-1/)<br>

### Deployment Geography:
Global <br>

### Use Case: <br>
This model is designed for tennis-specific multimodal understanding over point-level video. Expected users include:
- Tennis broadcast and media workflows — point-level Q&A, shot and outcome understanding, and audio cue interpretation over match footage
- Coaching and performance analysis — structured and open-ended questions about shots, positioning, movement, and rally structure on point clips
- Sports analytics and production — match-fact and score-state reasoning aligned with point-level annotations
- Enterprise tennis applications — searchable point-level understanding and tennis-domain assistants over archived match video


### Release Date: <br>
Hugging Face 09/10/2026 via [Hugging Face](https://huggingface.co/nvidia/NVIDIA-NemotronLabs-AI-for-Media-Sports-Tennis) <br>

## Model Architecture:
**Architecture Type:** Other (Mamba2-Transformer hybrid Mixture of Experts backbone with multimodal encoders) <br>

**Network Architecture:**
- [Nemotron 3 Nano LLM (30B A3B)](https://huggingface.co/nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B-BF16) — 31B-parameter Mamba2-Transformer hybrid MoE backbone with ~3B active parameters per token.
- [CRADIO v4-H](https://huggingface.co/nvidia/C-RADIOv4-H) — vision encoder for image and video frames.
- [Parakeet](https://huggingface.co/nvidia/parakeet-tdt-0.6b-v2) — speech encoder for audio inputs.

**Number of model parameters:** 3.1 x 10^10 (31B A3B) <br>

**How the model was developed:** Weights are initialized from the pretrained Nemotron 3 Nano Omni BF16 checkpoint. Fine-tuning trains only the language-model parameters; the vision and audio encoders remain frozen. Optimization uses AdamW (learning rate 5×10⁻⁵, β=(0.9, 0.999)) with warmup and cosine decay, regularized by weight decay 0.05 and gradient clipping at max-norm 1.0, with no additional damping. Training is BF16 packed supervised fine-tuning over point-level tennis clips. Hyperparameters follow the published NeMo AutoModel recipe rather than a dedicated search. <br>


## Input(s): <br>
**Input Type(s):** Video, Audio, Image, Text <br>

**Input Format(s):** <br> 
- Video: mp4, up to 2 minutes. For tennis tasks, pass a full tennis point clip as input for best results. For 1080p videos, sample up to 1 FPS (frames per second) / 128 frames. For lower-resolution videos such as 720p, higher temporal sampling such as 2 FPS / 256 frames may be used.
- Audio: wav, mp3 files (up to 1 hour), 8kHz and higher sampling rates
- Image: Red, Green, Blue (RGB) (jpeg, png)
- Text: String <br>

**Input Parameters:** <br>
- Video: Three-Dimensional (3D)
- Audio: One-Dimensional (1D)
- Image: Two-Dimensional (2D)
- Text: One-Dimensional (1D) <br>

**Other Properties Related to Input:** <br>
- Recommended input: a full tennis point (video clip, with audio when available), matching the point-level clips used during fine-tuning
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

This repo includes a sample full point at [`media/full_tennis_point.mp4`](media/full_tennis_point.mp4) for inference. You can also pass your own MP4 (serve through end of point, with audio when available). Frames are sampled with [`video_io.py`](video_io.py), included with this model.

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

Run from the directory holding `video_inference.py` (or use the bundled clip after download):

```bash
python video_inference.py
```

`video_inference.py` uses the bundled clip [`media/full_tennis_point.mp4`](media/full_tennis_point.mp4) and the default caption prompt when `--video` / `--question` are omitted. Override with `--video /path/to/point.mp4` and/or `--question '...'`. Add `--local-files-only` after weights are cached. The bundled demo clip is video-only; the script detects missing audio and runs video-only inference. When your MP4 has an audio track, it uses video + audio (extracting a 16 kHz WAV with ffmpeg if librosa cannot decode the container). Pass `--extract-audio-wav` to force WAV extraction, or `--no-audio` to skip audio.

The first `AutoModel.from_pretrained(..., trust_remote_code=True)` also downloads RADIO vision code from [`nvidia/C-RADIOv4-H`](https://huggingface.co/nvidia/C-RADIOv4-H).

Default inference policy (same as [`video_inference.py`](video_inference.py)): **2 frames per second (FPS)**, up to **128 frames**, **256** new tokens, greedy decode, `video_pruning_rate=0.0`. In the Python snippet below, set `audio_present=True` to include audio from your MP4 (leave `False` for the bundled video-only demo).

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

repo_id = "nvidia/NVIDIA-NemotronLabs-AI-for-Media-Sports-Tennis"
question = (
    "What happened in this point? Provide a detailed caption. "
    '(Major - "Major" is the player in the white sleeveless tennis dress with a pleated skirt. '
    "She is wearing white shoes and has dark hair tied back in a ponytail.; "
    'Mustermann - "Mustermann" is the player in the black sleeveless top and black pleated skirt '
    "with white piping along the sides and hem. She is wearing white shoes and has blonde hair "
    "tied back in a ponytail. She is holding a green and black tennis racket with a red grip.)"
)
video_fps, max_video_frames, max_new_tokens = 2, 128, 256
revision, local_files_only = None, False  # optional: pin Hub commit; cache-only load
audio_present = False  # bundled demo is video-only; set True when your MP4 has audio

cache_dir = os.environ.get("HF_HOME") or os.environ.get("HF_HUB_CACHE")
hub = {"trust_remote_code": True, "local_files_only": local_files_only}
if cache_dir:
    hub["cache_dir"] = cache_dir
if revision:
    hub["revision"] = revision
snapshot_dir = snapshot_download(
    repo_id=repo_id, repo_type="model", **{k: v for k, v in hub.items() if k != "trust_remote_code"}
)
video_path = str(Path(snapshot_dir) / "media/full_tennis_point.mp4")

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

audio_wav = None
if audio_present:
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

media = processor.video_token
if audio_present:
    media = f"{media}\n{processor.audio_token}\n"
prompt = processor.tokenizer.apply_chat_template(
    [{"role": "user", "content": f"{media}{question}"}],
    tokenize=False, add_generation_prompt=True, enable_thinking=False,
)
processor_kwargs = {
    "text": [prompt], "videos": frames, "return_tensors": "pt", "do_sample_frames": False,
    "videos_kwargs": {"video_metadata": video_metadata},
}
if audio_present:
    processor_kwargs["audio"] = [audio_wav]
    processor_kwargs["audio_kwargs"] = {"sampling_rate": 16000}
inputs = processor(**processor_kwargs)
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

Requires one GPU with ~80 GB memory (BF16). Authenticate with `hf auth login` before downloading a private repo. Frame sampling uses `decord` (Linux aarch64: install `decord2`). When `audio_present=True`, a 16 kHz WAV is extracted with ffmpeg (`imageio-ffmpeg` or a system `ffmpeg`). `summary_idxs | MISSING` on load is expected.


---

## Training, Testing, and Evaluation Datasets:

### Base Model
This model is a fine-tuned variant of [Nemotron 3 Nano Omni 30B-A3B-Reasoning](https://huggingface.co/nvidia/Nemotron-3-Nano-Omni-30B-A3B-Reasoning-BF16), retaining the same Mamba2-Transformer hybrid MoE architecture and multimodal encoders (CRADIO v4-H vision encoder and Parakeet speech encoder). <br>

### Training Dataset

**Dataset Name:** NVIDIA In-House Tennis Dataset (proprietary) <br>
**Data Modality:** Video, Text <br>
**Video Training Data Size:** Less than 10,000 Hours (43,084 point-level video clips) <br>
**Text Training Data Size:** Less than 1 Billion Tokens (1,312,129 training Q&A examples) <br>
**Dataset Size:** 1,312,129 training examples <br>
**Data Collection Method:** Manually-Collected <br>
**Labeling Method:** Manually-Labeled <br>
**Time period for training data collection:** 2025 <br>
**Properties (Quantity, Dataset Descriptions, Sensor(s)):** 1,312,129 tennis point video Q&A examples (1,226,081 multiple-choice and 86,048 open-ended) from 43,084 point-level clips across 239 matches and 38 annotation categories. Content is proprietary broadcast and court-capture tennis footage with manually authored English questions and answers. No sensor-derived metadata beyond standard video/audio capture. **Linguistic characteristics:** English-only tennis-domain questions and answers in multiple-choice and open-ended formats covering shot mechanics, court positioning, player movement, rally structure, score state, rules knowledge, audio cues, and cross-field reasoning. <br>

### Testing Dataset

**Dataset Name:** NVIDIA In-House Tennis Dataset — Test (unseen matches) partition (proprietary) <br>
**Dataset Size:** 80,872 test examples from 12 fully held-out matches (2,689 point-level clips; no training match overlap) <br>
**Data Collection Method:** Manually-Collected <br>
**Labeling Method:** Manually-Labeled <br>
**Properties (Quantity, Dataset Descriptions, Sensor(s)):** Q&A pairs from **12 fully held-out matches** (no training match overlap) — 2,689 point-level clips, 80,872 examples. English tennis-domain labels aligned with the training taxonomy. The corpus also includes a validation split (68,931 examples) and a separate Test (seen matches) partition (69,091 examples from 238 matches represented in training, with match-level overlap only); **only Test (unseen matches) was used for reported model testing.** <br>

### Evaluation Dataset

**Dataset Name:** NVIDIA In-House Tennis Test (unseen matches) evaluation benchmark (proprietary) <br>
**Dataset Size:** 80,872 test examples from the Test (unseen matches) partition (12 fully held-out matches) used for MCQ accuracy and open-ended judge scoring <br>
**Data Collection Method:** Manually-Collected <br>
**Labeling Method:** Manually-Labeled <br>
**Properties (Quantity, Dataset Descriptions, Sensor(s)):** **Test (unseen matches)** — 12 fully held-out matches with no training match overlap (2,689 point-level clips, 80,872 Q&A examples). Evaluated with automated MCQ scoring and LLM-as-judge pass@9 metrics on open-ended responses. English tennis-domain questions across 38 fine-grained categories. Test (seen matches) was not used for reported metrics. <br>

Fine-tuning was performed on top of the base Nemotron 3 Nano Omni weights using the in-house tennis dataset. Pre-training dataset details for the base model are documented in the [base Nemotron 3 Nano Omni model card](https://huggingface.co/nvidia/Nemotron-3-Nano-Omni-30B-A3B-Reasoning-BF16). <br>


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
