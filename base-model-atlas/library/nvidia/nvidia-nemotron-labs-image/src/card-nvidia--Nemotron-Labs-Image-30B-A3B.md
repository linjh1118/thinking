---
license: other
license_name: nvidia-license
license_link: LICENSE
pipeline_tag: text-to-image
library_name: transformers
tags:
- nvidia
- nemotron
- image-generation
- nvidia-license
---

<h1 align="center">Nemotron-Labs-VisualCreation<br /><sub>Pixel as Code for Agentic Visual Creation</sub></h1>
<p align="center">
<a href="https://huggingface.co/nvidia/Nemotron-Labs-Image-30B-A3B/resolve/main/paper.pdf"><img alt="Paper — Read Now!" src="https://img.shields.io/badge/📝Paper-Read_Now!-76B900?logoColor=white" height="24" /></a>
<a href="https://fuxiaoliu-nemotron-labs-visualcreation-gallery.static.hf.space/index.html"><img alt="Gallery — Explore Visual Creations" src="https://img.shields.io/badge/🖼Gallery-Explore_Visual_Creations-76B900?logoColor=white" height="24" /></a>
<a href="https://fuxiaoliu-nemotron-labs-visualcreation-gallery.static.hf.space/image-generation/index.html"><img alt="Image Generation Gallery" src="https://img.shields.io/badge/🖼Image_Generation_Gallery-76B900?logoColor=white" height="24" /></a>
<a href="https://developer.download.nvidia.com/licenses/NVIDIA-OneWay-Noncommercial-License-22Mar2022.pdf?t=eyJscyI6ImdzZW8iLCJsc2QiOiJodHRwczovL3d3dy5nb29nbGUuY29tLyJ"><img alt="License — NVIDIA License" src="https://img.shields.io/badge/License-NVIDIA_License-f5de53" height="24" /></a>
<br /><sub><a href="#model-overview">Overview</a> · <a href="#visual-showcase">Showcase</a> · <a href="#harness-architecture">Harness</a> · <a href="#results">Results</a> · <a href="#release-plan">Release Plan</a> · <a href="#image-model">Image Model</a> · <a href="#authors">Authors</a></sub>
</p>
<div align="center">
<a href="https://huggingface.co/nvidia/Nemotron-Labs-Image-30B-A3B/resolve/main/assets/nemotron-labs-visualcreation-showcase.gif"><img src="https://huggingface.co/nvidia/Nemotron-Labs-Image-30B-A3B/resolve/main/assets/nemotron-labs-visualcreation-showcase.gif" alt="Nemotron-Labs-VisualCreation animated showcase" width="100%" /></a><br />
</div>


## Model Overview

**Nemotron-Labs-VisualCreation** is an agentic framework for creating expressive
raster images and editable visual artifacts, including webpages, presentations,
documents, charts, and scientific figures. Its **Pixel as Code** interface
connects learned visual tokens and explicit programs through generation,
rendering, and visual inspection.

The framework combines a Nemotron-native harness with specialized components for
visual tokenization, autoregressive image generation, and structured visual
coding. **Nemotron-Labs-Image-30B-A3B is its raster image-generation component.**
The initial model release covers the image generator and its bundled
visual tokenizer.

<div align="center">
  <a href="https://huggingface.co/nvidia/Nemotron-Labs-Image-30B-A3B/resolve/main/assets/pixel-as-code-overview.png"><img src="https://huggingface.co/nvidia/Nemotron-Labs-Image-30B-A3B/resolve/main/assets/pixel-as-code-overview.png" alt="Pixel as Code unifies learned visual tokens and explicit programs through generation, rendering, and inspection" width="100%" /></a>
  <p><sub>Figure 1 from the paper. Raster appearance and editable structure share a generation-and-rendering interface.</sub></p>
</div>

### Key Design

- **Represent appearance and structure.** Discrete visual tokens capture raster
  content. SVG, HTML/CSS, plotting programs, and document markup expose editable
  text, geometry, and layout. Hybrid artifacts combine generated images with
  explicit structure.
- **Plan for the deliverable.** Routing selects the artifact family,
  representation, rendering backend, and asset policy. Structured and hybrid
  requests additionally establish a layout contract.
- **Use rendered evidence.** Visual selection chooses among raster candidates.
  Browser-based creation uses renderer checks and visual audits to diagnose
  issues, assign targeted repairs, and retain artifact checkpoints.

---

## Visual Showcase

<div align="center">
<a href="https://huggingface.co/nvidia/Nemotron-Labs-Image-30B-A3B/resolve/main/assets/paper-figure2.png"><img src="https://huggingface.co/nvidia/Nemotron-Labs-Image-30B-A3B/resolve/main/assets/paper-figure2.png" alt="Figure 2 from the paper, showing infographics, visual text, portraits, typography, and product imagery" width="100%" /></a><br />
<sub>Figure 2. Raster image creation examples spanning illustrated infographics, text-rich compositions, portraits, stylized typography, and product imagery.</sub>
</div>

[**Image Generation Gallery →**](https://fuxiaoliu-nemotron-labs-visualcreation-gallery.static.hf.space/image-generation/index.html) — Browse generated images, original prompts, and resolution sets.


<table>
  <tr>
    <th width="50%">Raster images</th>
    <th width="50%">Editable structured artifacts</th>
  </tr>
  <tr>
    <td valign="top"><a href="https://huggingface.co/nvidia/Nemotron-Labs-Image-30B-A3B/resolve/main/assets/paper-image-examples.jpg"><img src="https://huggingface.co/nvidia/Nemotron-Labs-Image-30B-A3B/resolve/main/assets/paper-image-examples.jpg" alt="Framework-generated landscapes, architecture, wildlife, and portraiture from Figure 3" width="100%" /></a></td>
    <td valign="top"><a href="https://huggingface.co/nvidia/Nemotron-Labs-Image-30B-A3B/resolve/main/assets/paper-structured-examples.png"><img src="https://huggingface.co/nvidia/Nemotron-Labs-Image-30B-A3B/resolve/main/assets/paper-structured-examples.png" alt="Framework-created webpages, icons, presentations, charts, and scientific figures from Figure 4" width="100%" /></a></td>
  </tr>
</table>

*Figures 3 and 4 from the paper. Select either image to view it at full size.
The Gallery button at the top opens the interactive showcase.*

---

## Harness Architecture

<div align="center">
  <a href="https://huggingface.co/nvidia/Nemotron-Labs-Image-30B-A3B/resolve/main/assets/harness-workflow.png"><img src="https://huggingface.co/nvidia/Nemotron-Labs-Image-30B-A3B/resolve/main/assets/harness-workflow.png" alt="The Nemotron-native harness routes requests through direct raster generation, browser-based structured or hybrid creation, and native-format generation" width="100%" /></a>
  <p><sub>Figure 5 from the paper. Route-specific control flow in the Nemotron-native harness.</sub></p>
</div>

**Super-VL** denotes Nemotron-3.5-Super-VL, **Ultra** denotes Nemotron 3 Ultra,
and **Image** denotes Nemotron-Labs-Image-30B-A3B.

| Route | Generation and inspection | Deliverable |
|---|---|---|
| **Direct raster** | Image generates candidates. Super-VL performs visual selection. | Selected raster image |
| **Browser-based structured / hybrid** | Ultra resolves the layout and assets. Ultra and Super-VL act as Dual Coder. Renderer checks, visual audits, and pairwise selection guide bounded repairs. | Editable artifact and rendered preview |
| **Native presentation / document / SVG** | Format-specific generators and renderers provide inspection and judging. | Native artifact |

The browser workflow freezes the request checklist and layout contract before
generation. Audits assign issues to plan, asset, layout, code, interaction, or
content owners. Repairs may regenerate an asset, revise the plan, or update the
explicit representation. The default limits allow three accepted repairs within
eight attempted cycles, with checkpoint selection retaining the strongest
eligible artifact.

### Learned Components

| Component | Role in Pixel as Code |
|---|---|
| **Nemotron-Labs-Image-Tokenizer** | Roughly 642M-parameter encoder and decoder, 16×16 patches, and a fixed codebook of 196,560 Leech-lattice vectors |
| **Nemotron-Labs-Image-30B-A3B** | Autoregressive raster generator initialized from Nemotron 3 Nano, with 30B total and 3B active parameters |
| **Nemotron-Labs-VisionCode** | 30B-A3B and 120B-A12B models trained for the structured-code interface and evaluated in standalone coding tests |

VisionCode's 30B and 120B variants are initialized from Nemotron-3-Nano-Omni and
Nemotron-3.5-Super-VL, respectively. They use the same training data and training
procedure. Their standalone evaluation is separate from the harness Dual Coder
assignment shown above.

---

## Results

The tables below summarize selected results from the technical report. The
paper provides the complete comparison sets, evaluation protocols, and metric
definitions.

### Raster Generation and Agentic Creation

**Nemotron-Labs-VisualCreation** reports our best score for each benchmark
across the configurations evaluated in the paper. English benchmark settings
are used where applicable. GenEval2 reports Soft-TIFA GM, and WISE uses the
Verified protocol. A dash indicates an unreported value. Bold marks the highest
score in each displayed row. The comparison includes selected closed-source and open-weight baselines from the paper.

| Benchmark ↑ | **Nemotron-Labs-VisualCreation** | GPT Image 2 | Nano Banana Pro |
|---|---|---|---|
| GenEval | **92.86** | 89.00 | — |
| GenEval2 | 65.43 | **81.00** | 59.00 |
| UniGenBench++ short | **93.20** | — | 92.72 |
| UniGenBench++ long | **94.25** | — | 94.20 |
| LongTextBench | **97.98** | 96.00 | 97.60 |
| CVTG-2K | **92.53** | 90.03 | 77.90 |
| OneIG | 54.63 | 51.60 | **58.30** |
| Qwen-Image-Bench | 52.46 | **65.23** | 59.33 |
| WISE Verified | **91.50** | — | 87.60 |
| BizGenEval | **86.0** | 83.2 | 76.7 |

<details>
<summary><strong>More comparisons — SenseNova-U1.5, FLUX.2 Dev, and Qwen-Image</strong></summary>

| Benchmark ↑ | Nemotron-Labs-VisualCreation | SenseNova-U1.5 | FLUX.2 Dev | Qwen-Image |
|---|---|---|---|---|
| GenEval | **92.86** | 92.00 | 87.00 | 86.83 |
| GenEval2 | **65.43** | 55.00 | — | 33.80 |
| UniGenBench++ short | **93.20** | — | 84.76 | 78.36 |
| UniGenBench++ long | **94.25** | — | 90.31 | 83.94 |
| LongTextBench | 97.98 | **98.80** | 96.30 | 94.30 |
| CVTG-2K | 92.53 | **94.80** | 89.26 | 82.88 |
| OneIG | 54.63 | **55.20** | — | 53.90 |
| Qwen-Image-Bench | 52.46 | **52.82** | — | 48.48 |
| WISE Verified | **91.50** | — | 56.50 | 51.00 |
| BizGenEval | **86.0** | — | 4.9 | 6.3 |

</details>


Nemotron-Labs-VisualCreation reaches 92.86 on GenEval and 91.50 on WISE
Verified. On BizGenEval, it scores 86.0, compared with 83.2 for GPT Image 2 and
76.7 for Nano Banana Pro. SenseNova-U1.5 leads LongTextBench and CVTG-2K among the displayed models. Nano Banana Pro leads the displayed OneIG comparison,
while GPT Image 2 leads GenEval2 and Qwen-Image-Bench. The paper provides the
complete configuration breakdown. In the GenEval2 source, Nano Banana Pro is
reported as Gemini 3 Pro Image.

### Structured Visual Coding

The paper evaluates five tasks across Chart2Code, MMSVG image-to-SVG and
text-to-SVG, Design2Code, and Image2Struct. Both VisionCode variants use
thinking-enabled inference in these standalone tests.

| Model | Chart + SVG Overall ↑ | SVG + Web + Document Overall ↑ | Five-task aggregate ↑ |
|---|---|---|---|
| Nemotron-3-Nano-Omni-30B-A3B | 46.81 | 62.93 | 56.48 |
| **VisionCode-30B-A3B** | 91.17 | 95.25 | 93.62 |
| Nemotron-3.5-Super-VL-120B-A12B | 93.12 | 91.96 | 92.42 |
| **VisionCode-120B-A12B** | **97.47** | **98.80** | **98.27** |
| Qwen3.5-35B-A3B | 87.29 | — | — |
| Qwen3.5-122B-A10B | 90.54 | — | — |
| Kimi K3.1 Pro (2.8T-A104B) | 96.28 | 93.21 | 94.44 |

VisionCode refers to the **Nemotron-Labs-VisionCode** family. The first score
covers Chart2Code and Img2SVG. The second covers Text2SVG, Design2Code, and
Image2Struct. Each metric is divided by the best reported value for that metric
and scaled to 100. Normalized metrics are averaged within each task, then tasks
receive equal weight. The five-task aggregate weights the two table scores by
2/5 and 3/5, respectively. Scores require complete measurements for the covered
tasks. Qwen models have no reported Text2SVG results. These descriptive aggregates
depend on the included models and metrics.

VisionCode-120B-A12B leads the aggregate among models with complete coverage.
Kimi K3.1 Pro retains higher Img2SVG DINO and SSIM and higher Text2SVG aesthetic
quality. Full task metrics and trade-offs appear in Tables 11 and 12 of the paper.

### Visual Tokenizer Quality and Efficiency

Reconstruction is evaluated on approximately **178K images across six visual
domains**. Quality metrics below compare reconstructed images against Emu3.5
IBQ using the paper's protocol.

| Metric | Emu3.5 IBQ | Nemotron-Labs-Image-Tokenizer |
|---|---|---|
| PSNR (dB) ↑ | 26.08 | **29.57** |
| SSIM ↑ | 0.781 | **0.834** |
| LPIPS ↓ | 0.0855 | **0.0713** |
| GMSD ↓ | 0.0994 | **0.0675** |
| FID ↓ | 36.36 | **35.06** |
| FD-DINOv2 ↓ | 7.49 | **5.25** |
| MUSIQ ↑ | **65.84** | 65.78 |
| CLIP-IQA ↑ | **0.593** | 0.583 |
| Laplacian-variance ratio (target 1) | 0.892 | **0.982** |

At batch size one on A100, tokenizer encoding takes **41.30 ms** and decoding
**37.10 ms**, compared with 294.53 ms and 405.46 ms for Emu3.5. These measurements
correspond to 7.13× and 10.93× tokenizer latency speedups. End-to-end creation
also includes visual-token generation and the agentic workflow.

---

## Release Plan

The initial release scope is **Nemotron-Labs-Image-30B-A3B**, including its
bundled visual tokenizer, model definition, and inference code. The broader
framework and VisionCode release items are listed below.

| Component | Plan |
|---|---|
| **Nemotron-Labs-Image-30B-A3B** | Release |
| **Nemotron-Labs-VisualCreation harness** | Will be released upon legal clearance. |
| **Nemotron-Labs-VisionCode** | Will be released upon legal clearance. |

## Image Model

**Nemotron-Labs-Image-30B-A3B** provides standalone autoregressive image
generation. It uses progressive mid-training followed by GRPO for semantic
alignment and image quality. Its visual-token outputs are rendered by the
bundled Nemotron-Labs-Image-Tokenizer.

## Repository contents

| Component | Location |
|---|---|
| Nemotron image-generation weights | Repository root; 32 safetensors shards |
| Model and tokenizer code | Repository root |
| L24SQ image tokenizer/decoder | `Nemotron-Labs-Image-Tokenizer/` |

The image tokenizer keeps its internal Transformers model type,
`l24sq_vit`. The external directory name does not change its architecture or
weights.

<details>
<summary><strong>Download, installation, inference code, generation settings, and model details</strong></summary>

## Quick start

### 1. Create an environment and install the dependencies

Use Linux with Python 3.12 and an NVIDIA driver compatible with CUDA 13.0.
The inference example below uses four NVIDIA H100 80GB GPUs. Check that the
GPUs are visible with `nvidia-smi` before installing the Python packages.

Create a separate environment and install the reference package versions:

```bash
python3.12 -m venv .venv-image
source .venv-image/bin/activate
python -m pip install --upgrade pip
python -m pip install \
  "torch==2.11.0" \
  "vllm==0.21.0" \
  "transformers==5.23.0" \
  "Pillow==12.3.0" \
  "safetensors==0.8.0" \
  "einops>=0.8,<1" \
  "huggingface_hub>=1,<3"
python -m pip check
export VLLM_WORKER_MULTIPROC_METHOD=spawn
```

The previously validated environment used Python 3.12.13, PyTorch
2.11.0+cu130, vLLM 0.21.0, Transformers 5.23.0, Pillow 12.3.0, and
safetensors 0.8.0. The commands above install Python dependencies; the host
must already have a compatible NVIDIA driver. No container is required.

Check the installed environment:

```bash
python - <<'PY_CHECK'
import torch
import transformers
import vllm
from PIL import __version__ as pillow_version
import safetensors

print("PyTorch:", torch.__version__)
print("CUDA build:", torch.version.cuda)
print("vLLM:", vllm.__version__)
print("Transformers:", transformers.__version__)
print("Pillow:", pillow_version)
print("safetensors:", safetensors.__version__)
assert torch.cuda.is_available(), "CUDA is not available; check the NVIDIA driver."
assert torch.cuda.device_count() >= 4, "This example requires four visible GPUs."
print("Environment check passed.")
PY_CHECK
```

### 2. Download the repository

Keep the environment active and run the following command from the directory
where you will save `infer.py`. The model tokenizer requires a local checkpoint
path. Download the entire repository, including the image-tokenizer directory.

```bash
# Required only while the repository is private or if access requires login:
# hf auth login

hf download nvidia/Nemotron-Labs-Image-30B-A3B \
  --local-dir ./Nemotron-Labs-Image-30B-A3B
```

### 3. Generate an image from a prompt

The following example generates one 1024×1024 image. Save it as `infer.py` and
run `python infer.py`. It preserves the model's required chat template,
visual-token framing, size header, and L24SQ decoding protocol.

```python
import re
from pathlib import Path

import torch
from PIL import Image
from transformers import AutoModel, AutoTokenizer
from vllm import LLM, SamplingParams


MODEL_DIR = Path("./Nemotron-Labs-Image-30B-A3B").resolve()
DECODER_DIR = MODEL_DIR / "Nemotron-Labs-Image-Tokenizer"
OUTPUT_PATH = Path("output.png")

PROMPT = "A cinematic photograph of a red fox in a snowy pine forest at dawn."
WIDTH = 1024
HEIGHT = 1024
PATCH_SIZE = 16

SYSTEM_PROMPT = (
    "Generate an image matching the requested resolution by detailing the color, "
    "quantity, text, shape, size, texture, spatial relationships of the objects "
    "and background."
)


def extract_l24sq_codes(token_ids, tokenizer):
    """Validate one generated image block and return codebook indices."""
    image_start = tokenizer.convert_tokens_to_ids("<|img_start|>")
    image_end = tokenizer.convert_tokens_to_ids("<|img_end|>")
    visual_row = tokenizer.convert_tokens_to_ids("<|vis_row|>")
    vision = tokenizer.unitron_token_ranges["vision"]
    vision_start = int(vision["start_id"])
    vision_end = int(vision["end_id"])

    try:
        start = token_ids.index(image_start)
        end = token_ids.index(image_end, start + 1)
    except ValueError as exc:
        raise RuntimeError("Generation did not contain a complete image block") from exc

    prefix_ids = []
    rows = []
    current_row = None
    for token_id in token_ids[start + 1 : end]:
        if token_id == visual_row:
            if current_row is not None:
                rows.append(current_row)
            current_row = []
        elif vision_start <= token_id < vision_end:
            if current_row is None:
                raise RuntimeError("Visual token appeared before the first row marker")
            current_row.append(token_id - vision_start)
        elif current_row is None:
            prefix_ids.append(token_id)
        else:
            raise RuntimeError("Non-visual token appeared inside the image grid")
    if current_row is not None:
        rows.append(current_row)

    size_header = tokenizer.decode(prefix_ids, skip_special_tokens=False)
    match = re.search(r"height=(\d+)\s+width=(\d+)", size_header)
    if match is None:
        raise RuntimeError("Generation did not contain a valid size header")
    generated_height, generated_width = map(int, match.groups())
    if (generated_height, generated_width) != (HEIGHT, WIDTH):
        raise RuntimeError(
            f"Generated size {(generated_width, generated_height)} does not match "
            f"the requested size {(WIDTH, HEIGHT)}"
        )

    expected_grid = (HEIGHT // PATCH_SIZE, WIDTH // PATCH_SIZE)
    if len(rows) != expected_grid[0] or any(
        len(row) != expected_grid[1] for row in rows
    ):
        raise RuntimeError("Generated visual-token grid has the wrong shape")

    codes = [code for row in rows for code in row]
    return codes, expected_grid


def main():
    tokenizer = AutoTokenizer.from_pretrained(
        str(MODEL_DIR),
        trust_remote_code=True,
    )

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {
            "role": "user",
            "content": f"Generate a {WIDTH}x{HEIGHT} image.\n\n{PROMPT}",
        },
    ]
    prompt_token_ids = tokenizer.apply_chat_template(
        messages,
        tokenize=True,
        add_generation_prompt=True,
        enable_thinking=False,
        return_tensors=None,
    )

    image_end_id = tokenizer.convert_tokens_to_ids("<|img_end|>")
    sampling = SamplingParams(
        temperature=0.9,
        top_p=1.0,
        top_k=-1,
        max_tokens=4352,
        seed=42,
        n=1,
        skip_special_tokens=False,
        detokenize=True,
        stop=["<|img_end|>"],
        stop_token_ids=[image_end_id],
        include_stop_str_in_output=True,
    )

    generator = LLM(
        model=str(MODEL_DIR),
        tokenizer=str(MODEL_DIR),
        trust_remote_code=True,
        tensor_parallel_size=4,
        moe_backend="triton",
        dtype="bfloat16",
        max_model_len=6144,
        gpu_memory_utilization=0.70,
        enforce_eager=True,
        seed=42,
    )
    result = generator.generate(
        [{"prompt_token_ids": prompt_token_ids}],
        sampling,
        use_tqdm=False,
    )[0]
    generated_token_ids = list(result.outputs[0].token_ids)
    codes, grid_size = extract_l24sq_codes(generated_token_ids, tokenizer)

    decoder = AutoModel.from_pretrained(
        str(DECODER_DIR),
        trust_remote_code=True,
        dtype=torch.bfloat16,
    ).to("cuda:0").eval()

    indices = torch.tensor(codes, dtype=torch.long, device="cuda:0")
    with torch.inference_mode():
        decoded = decoder.pack_decode(
            indices_list=[indices],
            grid_sizes=[grid_size],
        )[0]

    pixels = (
        ((decoded.float().clamp(-1, 1) + 1) / 2 * 255)
        .round()
        .to(torch.uint8)
        .permute(1, 2, 0)
        .cpu()
        .numpy()
    )
    Image.fromarray(pixels).save(OUTPUT_PATH)
    print(f"Saved {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
```

To change the output resolution, edit `WIDTH` and `HEIGHT` near the top of the
script. For example, use the following settings for a landscape image:

```python
WIDTH = 1184
HEIGHT = 880
```

The script automatically includes the selected resolution in the generation
prompt, validates the resulting visual-token grid, and decodes it at the
requested size.

The example selects the Triton MoE backend, matching the validated inference
configuration and avoiding FlashInfer MoE extension compilation during startup.

The generator and decoder may be run in separate processes if GPU memory is
tight. Preserve the generated token IDs between the two stages.

## Image resolutions

The model supports any-resolution image generation. For the best balance of
quality, composition, and inference cost, the recommended resolutions are:

- `1024x1024`
- `1184x880`
- `1248x832`
- `880x1184`

Width and height must be positive multiples of 16. For other resolutions, the
visual-token grid (`WIDTH / 16 × HEIGHT / 16`) must fit within `max_tokens` and
the model context window. The recommended resolutions above fit the example's
4,352-token generation budget.

## Recommended generation settings

| Parameter | Value |
|---|---:|
| Temperature | 0.9 |
| Top-p | 1.0 |
| Top-k | -1 |
| Maximum generated tokens | 4,352 |
| Seed | 42 |
| Generation dtype | bfloat16 |
| Tensor parallel size | 4 |
| vLLM maximum model length | 6,144 |

## Model details

| Field | Value |
|---|---|
| Developer | NVIDIA |
| Task | Text-to-image generation |
| Architecture | `NemotronHForCausalLM` |
| Precision | bfloat16 |
| Context length | 262,144 tokens |
| Model vocabulary rows | 327,680 |
| Base text vocabulary | 131,072 |
| Visual vocabulary | 196,560 virtual tokens |
| Visual framing tokens | `<|img_start|>`, `<|img_end|>`, `<|vis_row|>` |
| Image patch size | 16 pixels |
| Pixel decoder | `Nemotron-Labs-Image-Tokenizer/` (`l24sq_vit`) |

</details>

<details>
<summary><strong>Limitations</strong></summary>


## Limitations

- This is not a Diffusers pipeline and is not compatible with
  `AutoPipelineForText2Image`.
- Loading executes repository code through `trust_remote_code=True`; pin and
  review a specific repository revision for controlled deployments.
- Image generation is stochastic. Composition, anatomy, object counts,
  spatial relationships, and rendered text may be incorrect.
- Generated images can contain biases, false details, or content resembling
  people, brands, copyrighted styles, and other training concepts.
- Users are responsible for reviewing outputs and applying appropriate policy,
  privacy, provenance, and content controls.

</details>

## License/Terms of Use

GOVERNING TERMS: This model is licensed for non-commercial research and evaluation under the [NVIDIA License](https://developer.download.nvidia.com/licenses/NVIDIA-OneWay-Noncommercial-License-22Mar2022.pdf?t=eyJscyI6ImdzZW8iLCJsc2QiOiJodHRwczovL3d3dy5nb29nbGUuY29tLyJ). A copy is included in [LICENSE](LICENSE).

---

## Authors

**Core contributors**

Guo Chen*, Fuxiao Liu*, Haoqin Tu*, Yiyang Zhou*, Andrew Tao, Bryan Catanzaro, and Guilin Liu.

<sup>*</sup>Equal contribution. Listed alphabetically by surname.  
**Project lead** — Guilin Liu.

**Contributors**

Cihang Xie, Yuyin Zhou, Huaxiu Yao, Lidong Lu, and Zongxia Li.

**Affiliations**

NVIDIA, University of North Carolina at Chapel Hill, University of California,
Santa Cruz, University of Maryland, and Nanjing University. Haoqin Tu and
Yiyang Zhou contributed during their internships at NVIDIA.

## Acknowledgments

We thank Wei Xiong, Yongsheng Yu, Max Ehrlich, Edward Liu, Mike Ranzinger, Zhiding Yu, Greg Heinrich, Weili Nie, Karan Sapra, Danial Mohseni Taheri, Amala Sanjay Deshmukh, Matthieu Le, Tuomas Rintamaki, Mingjie Liu, Atefeh Sohrabizadeh, Enze Xie, Song Han and Ming-Yu Liu for their valuable discussions and feedback.

## Related Papers

Selected foundations and related work cited in our [technical report](https://huggingface.co/nvidia/Nemotron-Labs-Image-30B-A3B/resolve/main/paper.pdf).

| Paper | Connection to this work |
|---|---|
| [Nemotron 3 Nano](https://research.nvidia.com/labs/nemotron/files/NVIDIA-Nemotron-3-Nano-Technical-Report.pdf) | Backbone initialization for Nemotron-Labs-Image-30B-A3B. |
| [Nemotron 3 Nano Omni](https://research.nvidia.com/labs/nemotron/files/NVIDIA-Nemotron-3-Omni-report.pdf) | Base model for Nemotron-Labs-VisionCode-30B-A3B. |
| [Nemotron 3.5 Super and Lightning](https://arxiv.org/abs/2610.38095) | The Super-VL model used for routing, coding, and visual assessment, and as the base for VisionCode-120B-A12B. |
| [Nemotron 3 Ultra](https://arxiv.org/abs/2606.15007) | Semantic planning and the Ultra side of the harness Dual Coder. |
| [Cosmos 3: Omnimodal World Models for Physical AI](https://arxiv.org/abs/2606.02800) | Related work on multimodal understanding and generation. |
| [Cosmos-Reason1: From Physical Common Sense to Embodied Reasoning](https://arxiv.org/abs/2503.15558) | Related work on visual understanding and reasoning. |

## Citations

If you use this model or framework in your research, please cite our paper,
[Nemotron-Labs-VisualCreation: Pixel as Code for Agentic Visual Creation](https://huggingface.co/papers/2611.31358).

```bibtex
@misc{chen2026nemotronlabsvisualcreationpixelcodeagentic,
      title={Nemotron-Labs-VisualCreation: Pixel as Code for Agentic Visual Creation}, 
      author={Guo Chen and Fuxiao Liu and Haoqin Tu and Yiyang Zhou and Andrew Tao and Bryan Catanzaro and Cihang Xie and Yuyin Zhou and Huaxiu Yao and Didong Lu and Zongxia Li and Guilin Liu},
      year={2026},
      eprint={2611.31358},
      archivePrefix={arXiv},
      primaryClass={cs.CV},
      url={https://arxiv.org/abs/2611.31358}, 
}
```
