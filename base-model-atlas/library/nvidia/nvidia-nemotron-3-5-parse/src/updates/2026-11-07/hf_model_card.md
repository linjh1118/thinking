---
license: openmdw-1.1
pipeline_tag: image-text-to-text
tags:
- VLM
- OCR
- Parse
library_name: transformers
---
# Nemotron 3.5 Parse

**Turn document pages into structured information.** Nemotron 3.5 Parse extracts
text, tables, chart data, reading order, semantic classes, and bounding boxes from
page images. Use it on scans, rendered PDFs, slides, forms, reports, and mixed
document layouts; export the results as Markdown, HTML, or structured JSON.

![Synthetic documents and charts become structured predictions](assets/parse-demo.gif)

*Full-page predictions on synthetic documents. [Static preview](assets/parse-demo.png) · [All examples](assets/hero-examples.md).*

<a id="benchmark-highlights"></a>

- **Leading ParseBench accuracy:** **75.20** with triple-pass parsing, the highest
  overall score among the systems in our [reported comparison](#parsebench).
- **Broad multilingual OCR:** evaluated across **163 language/script entries in
  26 script groups**, plus 10 Indic languages. See [language results](#multilingual-ocr).
- **Small and fast:** **0.631B parameters**, with an optional **89.3M-parameter
  DFlash2 drafter**. See [throughput measurements](#new-dflash2-speculative-decoding)
  for the hardware, concurrency, and parsing mode behind each result.

<a id="new-dflash2-speculative-decoding"></a>

**New — November 4, 2026:** Native DFlash2 speculative decoding is available in
[`dflash2/`](dflash2/README.md), in the same repository as the target model.

![DFlash2, MTP, and base inference across concurrency](dflash2/performance/concurrency.png)

One H200, BF16, 2,078 pages, median of three runs, using the best tested native
draft length at each concurrency. See the [benchmark protocol and data](dflash2/performance/README.md).
This direct-engine, greedy benchmark is separate from the HTTP pass-mode timings.

<a id="hosted-inference"></a>

[Try the NVIDIA Build API](https://build.nvidia.com/nvidia/nemotron-3.5-parse) ·
[Deploy on Baseten](https://www.baseten.co/library/nemotron-35-parse/)

[Run it](#run-parse) · [Choose a parsing mode](#single-double-or-triple-pass) ·
[Prompts](#task-prompts) · [Tables and postprocessing](#tables-and-postprocessing) ·
[Benchmarks](#evaluation-results) · [Model details and terms](#model-details-and-terms)

<a id="quick-start"></a>

## Run Parse

<a id="transformers-installation"></a>

### Transformers

Use a fresh Python environment:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install transformers torchvision timm
```

<a id="usage-example"></a>

```python
import torch
from PIL import Image
from transformers import AutoModel, AutoProcessor, GenerationConfig

MODEL = "nvidia/Nemotron-3.5-Parse"
TASK_PROMPT = "</s><s><predict_bbox><predict_classes><output_markdown><predict_text_in_pic>"

model = AutoModel.from_pretrained(
    MODEL, trust_remote_code=True, dtype=torch.bfloat16,
).to("cuda").eval()
processor = AutoProcessor.from_pretrained(MODEL, trust_remote_code=True)
image = Image.open("page.png").convert("RGB")
inputs = processor(
    images=[image], text=TASK_PROMPT,
    return_tensors="pt", add_special_tokens=False,
).to("cuda")
generation = GenerationConfig.from_pretrained(MODEL)
generation.max_new_tokens = 8744

with torch.inference_mode():
    output_ids = model.generate(**inputs, generation_config=generation)
raw_output = processor.batch_decode(output_ids, skip_special_tokens=False)[0]
print(raw_output)
```

Keep the control tokens in `raw_output` for postprocessing. Transformers uses
the normal decoder; the speculative-decoding options below are for vLLM.

<a id="inference-with-vllm"></a>
<a id="vllm-inference-example"></a>

### vLLM

Use vLLM with native Parse and DFlash2 support. The included speculator speeds up token generation:

Download the target and drafter together and start a server:

```bash
hf download nvidia/Nemotron-3.5-Parse --local-dir ./parse35

vllm serve ./parse35 \
  --served-model-name nemotron-parse \
  --trust-remote-code \
  --speculative-config '{"method":"dflash","model":"./parse35/dflash2","num_speculative_tokens":32}'
```

Send one RGB page through the OpenAI-compatible API (`pip install openai`):

```python
import base64
from openai import OpenAI

TASK_PROMPT = "</s><s><predict_bbox><predict_classes><output_markdown><predict_text_in_pic>"
with open("page.png", "rb") as f:
    image_b64 = base64.b64encode(f.read()).decode()
client = OpenAI(base_url="http://localhost:8000/v1", api_key="EMPTY")
response = client.chat.completions.create(
    model="nemotron-parse",
    messages=[{"role": "user", "content": [
        {"type": "text", "text": TASK_PROMPT},
        {"type": "image_url", "image_url": {"url": "data:image/png;base64," + image_b64}},
    ]}],
    temperature=0, max_tokens=8744,
    extra_body={"top_k": 1, "repetition_penalty": 1.1, "skip_special_tokens": False},
)
raw_output = response.choices[0].message.content
print(raw_output)
```

The text content is the task prompt only. vLLM handles the image placeholder;
do not manually prepend `<pad>` or a newline to this HTTP request.

<details>
<summary>Offline vLLM: use the same task tokens without an extra newline</summary>

For offline `LLM.generate`, put one image placeholder directly before the task
prompt, without an intervening newline:

```python
request = {
    "prompt": "<pad>" + TASK_PROMPT,
    "multi_modal_data": {"image": image},
}
outputs = llm.generate(
    [request], sampling_params,
    tokenization_kwargs={"add_special_tokens": False},
)
```

Here `llm` is an initialized `vllm.LLM`, `image` is a PIL RGB image, and
`sampling_params` is your `SamplingParams`. Transformers and HTTP requests use
the task prompt without a manually inserted image placeholder.

</details>

### PDF input

The model consumes page images. Render each PDF page first; for example, with
`pip install pymupdf`:

```python
import pymupdf
from pathlib import Path

pages = Path("pages")
pages.mkdir(exist_ok=True)
page_paths = []
with pymupdf.open("document.pdf") as pdf:
    for number, page in enumerate(pdf):
        pix = page.get_pixmap(dpi=150, colorspace=pymupdf.csRGB, alpha=False)
        path = pages / f"page-{number:04d}.png"
        pix.save(str(path))
        page_paths.append(str(path))
```

Pass `page_paths` to `parse_many` below. Each result corresponds to one
page; combine their Markdown if desired. The helper does not infer cross-page
table continuations or a document-wide reading order.

<a id="parsing-helpers"></a>

## Single, double, or triple pass

Pass count controls how much image analysis is performed. A speculator accelerates
token generation within those requests; it does not select the pass count.

| Mode | What it does | Reported ParseBench overall | DFlash2 pages/s |
| --- | --- | ---: | ---: |
| Single | Parse the full page once | 72.74 | 18.57 |
| Double | Parse the page, then refine predicted Table/Chart crops | 74.92 | 14.60 |
| Triple | Also detect regions separately; refine the detector/parser union | 75.20 | 13.49 |

**Single pass** sends the whole page once and extracts its text, layout, tables
and chart data. Start here when throughput is the priority.

**Double pass** uses the full-page prediction to locate tables and charts, parses
those cropped regions at higher detail, and merges the refinements back into the
page. Crops start as each page's first result becomes available.

**Triple pass** starts full-page parsing and independent layout detection
together. It refines the union of their table/chart regions, including regions
that either request missed. Ready crops run while other pages and stages are
still in flight. Each retained crop is a separate request; a pass is a stage,
rather than a fixed count of three requests.

Timing uses one H200 and all 2,078 ParseBench pages; median of three fresh runs
per mode at its best tested serving configuration. See [profiles, completion
coverage and timing details](reference/dflash2-passes/README.md). Scores are the
existing reference-protocol results, separate from these DFlash2 timing runs.
See the [accuracy reproduction instructions](reference/parsebench/pipeline/README.md).

The downloaded repository includes the parser helpers. Install their dependencies
and make the downloaded source importable, without installing the serving plugin:

```bash
python -m pip install beautifulsoup4 Pillow numpy httpx
```

With the server above running:

```python
import sys
sys.path.insert(0, "./parse35")
from nemotron_parse.inference import DocumentParser

def main():
    with DocumentParser(
        base_url="http://localhost:8000/v1", model="nemotron-parse",
    ) as parser:
        documents = parser.parse_many(
            ["page.png"], mode="single", concurrency=128,
            triple_regions="union",  # used when mode="triple"
        )
    print(documents[0]["markdown"])
    print(documents[0]["blocks"])

if __name__ == "__main__":
    main()
```

`parse_many` uses the overlapping HTTP pipeline. In triple pass, parsing and
detection run together, and crops are dispatched as their regions become ready.

By default, crop merging preserves differing full-page/crop alternatives. Returned
documents can therefore contain overlapping table/chart hypotheses. Use
`DocumentParser(merge_policy="guarded")` when you prefer conservative replacement
and a single selected hypothesis, accepting the documented accuracy tradeoff.
See [batch parsing, crop settings, completion handling, and Transformers backends](docs/postprocessing.md).

## Task prompts

Parse uses control-token task prompts rather than a general-purpose chat
instruction. The default is:

```python
TASK_PROMPT = "</s><s><predict_bbox><predict_classes><output_markdown><predict_text_in_pic>"
```

Keep token order and spelling unchanged. Disable automatic special-token
insertion when tokenizing this complete prefix.

| Control | On | Off |
| --- | --- | --- |
| Bounding boxes | `<predict_bbox>` | `<no_bbox>` |
| Semantic classes | `<predict_classes>` | `<no_classes>` |
| Text formatting | `<output_markdown>` | `<output_plain>` |

These controls request an output style and can be combined. Some combinations
can still emit extra structure. For a fixed export schema, run a full parse
and select fields from the postprocessed blocks. Each comparison below holds the other controls fixed on the same synthetic page:

![Boxes on and off](assets/prompt-boxes.png)

### Semantic classes

With boxes disabled in both variants, toggle `<predict_classes>` / `<no_classes>`:

![Classes on and off](assets/prompt-classes.png)

### Text formatting

With boxes and classes disabled in both variants, toggle `<output_markdown>` / `<output_plain>`:

![Markdown and plain text](assets/prompt-format.png)

For layout-only detection, use
`</s><s><predict_bbox><predict_classes><output_no_text><predict_no_text_in_pic>`.
For text only, use
`</s><s><no_bbox><no_classes><output_plain><predict_text_in_pic>`.
Full-structure benchmark scores do not apply to a changed task.

CSV, HTML, and JSON are export choices: keep the full parsing prompt and choose
the desired table format during postprocessing.

<a id="postprocessing"></a>

## Tables and postprocessing

The model returns a serialization containing class and coordinate tokens. The
helpers turn it into a complete document and preserve the original block text:

For Transformers-only use, download the helper source into the same local layout
used by the vLLM example:

```bash
python -m pip install beautifulsoup4 Pillow numpy httpx
hf download nvidia/Nemotron-3.5-Parse \
  --include 'postprocessing.py' 'latex2html.py' 'nemotron_parse/**' \
  --local-dir ./parse35
```

```python
import sys
from pathlib import Path
from PIL import Image
sys.path.insert(0, "./parse35")
from nemotron_parse import postprocess_document, PostprocessOptions

image = Image.open("page.png").convert("RGB")
document = postprocess_document(raw_output, image_size=image.size)
Path("page.md").write_text(document["markdown"], encoding="utf-8")
print(document["blocks"])  # class, bbox, bbox_pixels, text, rendered content
```

`image_size` is `(width, height)`. Boxes are normalized to the evaluated image
content; `bbox_pixels` maps them back to pixels. Preserve class and coordinate
tokens when generating and decoding. Document Markdown uses HTML tables so merged
cells survive rendering. Raw per-block `text` remains available separately.

Convert a predicted table without running inference again:

```python
from postprocessing import postprocess_text

table = next(block for block in document["blocks"] if block["class"] == "Table")
print(postprocess_text(table["text"], cls="Table", table_format="csv"))
print(postprocess_text(table["text"], cls="Table", table_format="json_hierarchical"))
```

| Format | Use it for |
| --- | --- |
| `HTML` | Rendering tables while preserving merged cells |
| `json_hierarchical` | Structure with cell spans and header-role metadata |
| `markdown`, `csv`, `json` | Flat exports; merged-cell spans are expanded |
| `latex` | The predicted table's LaTeX representation |

Cleanup retains blank cells, spans, line breaks, model order, and predicted values.
Header inference can be disabled, as can chart-caption association and numeric
value/percentage splitting:

```python
options = PostprocessOptions(
    infer_headers=False,
    relocate_chart_captions=False,
    split_chart_value_percent=False,
)
document = postprocess_document(raw_output, image_size=image.size, options=options)
```

See [postprocessing examples and controls](docs/postprocessing.md) for the full API,
including literal raw output, warnings, chart rendering, and prepared batches.
The guide also includes the [predicted-box overlay example](docs/postprocessing.md#draw-predicted-boxes).

<a id="option-1-python-inference-with-mtp"></a>
<a id="option-2-vllm-serve-with-mtp"></a>

## Speed and speculative decoding

Choose one decoder in vLLM:

| Decoder | Server option |
| --- | --- |
| Base inference | Omit `--speculative-config` |
| One-token MTP | [MTP serving setup](docs/serving.md#one-token-mtp) |
| DFlash2 | `--speculative-config '{"method":"dflash","model":"./parse35/dflash2","num_speculative_tokens":32}'` |

MTP weights are bundled with the target. DFlash2 weights are in `dflash2/`.
Choose one speculator; adjust `num_speculative_tokens` to tune DFlash2 for your
request load. See the [draft-length table](dflash2/README.md#draft-length-tuning).

## Evaluation Results

### ParseBench

The headline score is **75.20 overall**, using triple pass with the detector/parser
region union on 2,078 unique pages. It is the highest overall score among the
models in the comparison below. Pass count, crop merging, generation settings,
and scoring protocol matter when reproducing these results.

Published overall scores and measured throughput:

| Model | Published ParseBench ↑ | Measured pages/s ↑ |
| :--- | ---: | ---: |
| **Nemotron 3.5 Parse (triple-pass)** | **75.20** | **13.49** |
| LightOnOCR-3-4B | 75.10 | 2.76 |
| **Nemotron 3.5 Parse (double-pass)** | **74.92** | **14.60** |
| LightOnOCR-3-0.8B | 74.60 | 5.69 |
| Infinity-Parser2-Flash | 73.25 | 3.06 |
| MinerU2.5-Pro-2605-1.2B | 72.78 | 4.13 |
| **Nemotron 3.5 Parse (single-pass)** | **72.74** | **18.57** |
| KDL-Frontier-Parser-nano | 72.38 | 2.98 |
| LightOnOCR-3-1B | 71.40 | 2.44 |
| Chandra-ocr-2 | 70.10 | 2.01 |
| PaddleOCR-VL-1.6 | 67.43 | 3.11 |
| PaddleOCR-VL-1.5 | 65.95 | 3.40 |
| Nemotron Parse 2.0 | 63.91 | 3.95 |

<details>
<summary>Category scores and evaluation details</summary>

Triple-pass category results:

| Model | Mean ↑ | Tables ↑ | Charts ↑ | Content Faithfulness ↑ | Semantic Formatting ↑ | Visual Grounding ↑ |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: |
| **Nemotron 3.5 Parse** | **75.20** | **84.67** | **64.40** | **87.96** | **68.28** | **70.67** |

- **Single pass:** parse the full page once.
- **Double pass:** parse the page, then refine Table/Chart crops selected from its predictions.
- **Triple pass:** add a separate detection request and refine the union of detector and parser regions. Full-page parsing and detection can overlap.

The refinement merge retains differing full-page/crop alternatives; the reported scores include these alternatives.

See [score sources](reference/parsebench/comparisons/README.md), [comparison records](reference/parsebench/comparisons/results.json), [current Parse timing profiles](reference/dflash2-passes/README.md), and the [pipeline reproduction instructions](reference/parsebench/pipeline/README.md).

</details>

### Multilingual OCR

**IndicVisionBench:** 83.73 ANLS-char on 876 pages across 10 Indic languages.
**MOSCAR:** 99.51 character-bag F1 on 8,111 synthetic pages across 163
language/script entries and 26 script groups.

MOSCAR tests basic OCR on simple synthetic text renderings. Coverage of a
language/script entry does not guarantee equivalent quality on complex scans,
handwriting, or degraded documents. Character-bag F1 measures character overlap
without considering order.

<a id="indicvisionbench-ocr"></a>

<details>
<summary>IndicVisionBench: per-language accuracy and character error rate</summary>

OCR results on 876 test pages across 10 languages. ANLS-char and character error rate (CER) are shown as percentages. CER includes insertion errors and can exceed 100%.

| Language | Pages | Parse 2.0 ANLS-char ↑ | Parse 3.5 ANLS-char ↑ | Parse 2.0 CER ↓ | Parse 3.5 CER ↓ |
| :--- | ---: | ---: | ---: | ---: | ---: |
| Overall | 876 | 72.12 | 83.73 | 52.67 | 16.00 |
| Bengali | 89 | 55.47 | 90.25 | 68.92 | 7.69 |
| Gujarati | 90 | 40.70 | 66.96 | 127.53 | 34.08 |
| Hindi | 85 | 85.03 | 88.34 | 16.32 | 9.36 |
| Kannada | 89 | 87.54 | 91.37 | 19.25 | 7.33 |
| Malayalam | 88 | 48.89 | 63.15 | 75.55 | 42.47 |
| Marathi | 83 | 92.95 | 93.19 | 6.50 | 6.01 |
| Odia | 86 | 67.77 | 73.61 | 71.46 | 24.61 |
| Punjabi | 89 | 83.25 | 91.95 | 66.57 | 7.30 |
| Tamil | 88 | 81.77 | 91.24 | 42.05 | 7.41 |
| Telugu | 89 | 79.86 | 87.75 | 43.57 | 10.53 |

</details>

<a id="moscar-multilingual-ocr"></a>

<details>
<summary>MOSCAR: results by script</summary>

MOSCAR uses simple synthetic renderings of text in each language to test basic OCR capability. These results do not guarantee accuracy on complex scanned documents, handwriting, degraded images, or other real-world variations. Character bag F1 measures character overlap without considering character order.

OCR results on 8,111 held-out synthetic pages covering all 163 configured language/script entries across 26 script groups. Character bag F1 (BoC F1, higher is better) and CER (lower is better) are percentages. Overall CER is computed across all reference characters, so it is not an unweighted average of the script rows.

| Script | Pages | Parse 2.0 BoC F1 ↑ | Parse 3.5 BoC F1 ↑ | Parse 2.0 CER ↓ | Parse 3.5 CER ↓ |
| :--- | ---: | ---: | ---: | ---: | ---: |
| Overall | 8111 | 97.44 | 99.51 | 11.55 | 1.35 |
| Arabic | 824 | 91.27 | 98.87 | 20.17 | 5.80 |
| Armenian | 50 | 99.38 | 99.92 | 1.15 | 0.09 |
| Bengali | 100 | 98.82 | 99.80 | 1.78 | 0.34 |
| Cyrillic | 597 | 98.75 | 99.69 | 2.36 | 0.89 |
| Devanagari | 350 | 97.99 | 99.47 | 5.41 | 0.79 |
| Ethiopic | 100 | 98.31 | 99.89 | 5.52 | 0.14 |
| Georgian | 50 | 99.91 | 99.99 | 0.13 | 0.02 |
| Greek | 50 | 99.63 | 99.93 | 1.07 | 0.10 |
| Gujarati | 50 | 99.52 | 99.92 | 0.74 | 0.15 |
| Gurmukhi | 50 | 94.85 | 99.91 | 14.87 | 0.16 |
| Han (Simplified) | 50 | 98.33 | 99.50 | 1.99 | 1.05 |
| Han (Traditional) | 100 | 97.83 | 99.68 | 3.10 | 0.54 |
| Hangul | 50 | 98.82 | 99.62 | 0.99 | 0.43 |
| Hebrew | 100 | 97.62 | 99.79 | 5.79 | 4.16 |
| Japanese | 50 | 98.66 | 99.77 | 2.61 | 0.47 |
| Kannada | 50 | 95.73 | 99.84 | 5.60 | 0.24 |
| Khmer | 50 | 96.56 | 99.63 | 5.79 | 0.71 |
| Lao | 50 | 98.74 | 99.74 | 2.26 | 0.46 |
| Latin | 5040 | 98.20 | 99.53 | 12.82 | 0.79 |
| Malayalam | 50 | 97.65 | 99.27 | 6.46 | 1.10 |
| Myanmar | 50 | 87.83 | 99.56 | 45.41 | 1.47 |
| Odia | 50 | 97.79 | 99.74 | 7.58 | 0.41 |
| Sinhala | 50 | 96.52 | 99.91 | 15.28 | 2.48 |
| Tamil | 50 | 97.89 | 99.92 | 7.92 | 0.14 |
| Telugu | 50 | 96.69 | 99.69 | 9.33 | 0.47 |
| Thai | 50 | 99.66 | 99.95 | 0.47 | 0.06 |

Both comparisons use the [released Parse 2.0 weights](https://huggingface.co/nvidia/NVIDIA-Nemotron-Parse-2.0) and current Parse 3.5 weights, identical page sets, greedy decoding, and the same scorer for each benchmark. Each model uses its documented default task prompt. All outputs, including those reaching the token limit, are included. See the [full MOSCAR results for all 163 language/script entries](reference/multilingual/moscar_by_language.md), [downloadable results](reference/multilingual/README.md), and [evaluation settings](reference/multilingual/README.md#evaluation-settings).


</details>

## Model details and terms

<details>
<summary>Description, architecture, inputs, outputs, and runtime details</summary>

### Description:
Nemotron 3.5 Parse is a document image parser that produces structured, machine-readable text with semantic layout classes, bounding boxes, and reading order. It combines a C-RADIOv4-SO400M vision encoder with a 10-layer mBART decoder that consumes the visual sequence as a causal prefix. The release uses dynamic rectangular NaViT preprocessing, content-normalized coordinates, grouped-query self-attention (16 query heads and 8 key/value heads), a 72,505-token multilingual tokenizer, and chart-aware output through the `<class_Chart>` token. It is intended for document understanding, information retrieval, data extraction, and multimodal data-curation workflows.<br>

Nemotron 3.5 Parse was developed by NVIDIA as a part of Nemotron.

This model is ready for commercial or non-commercial use. <br>

## Model Architecture:
**Architecture Type:** Transformer<br>

**Network Architecture:** <br>
* Vision Encoder: NVIDIA C-RADIOv4-SO400M (`vit_so400m_patch16_224`) with dynamic rectangular NaViT preprocessing<br>
* Adapter Layer: 1D convolutions and normalization layers that compress the vision latent sequence before decoding<br>
* Decoder: 10-layer mBART causal visual-prefix decoder with 16 query heads and 8 key/value heads<br>
* Auxiliary Prediction Head: One trained one-step multi-token-prediction (MTP) head is included in `model.safetensors`. Transformers uses the normal decoder for generation; the vLLM plugin enables the bundled head for one-token speculative decoding.<br>
* Tokenizer: 72,505 entries with multilingual and task/control tokens including `<predict_bbox>`, `<predict_classes>`, `<predict_text_in_pic>`, and `<class_Chart>`; the decoder embedding is padded to 72,512 rows. Use of the tokenizer included in this model is governed by the [MIT license and tokenizer attribution](https://huggingface.co/nvidia/Nemotron-3.5-Parse/blob/main/TOKENIZER_ATTRIBUTION.md).<br>
* Number of Parameters: 630,800,496 unique trainable parameters (approximately 0.631B), including the MTP head; shared decoder embedding/output weights are counted once<br>

## Input(s): <br>
**Input Type(s):** Image, Text<br>

**Input Format(s):** <br>
* Image: Red, Green, Blue (RGB)<br>
* Text: Prompt string<br>

**Input Parameters:** <br>
* Image: Two-Dimensional (2D)<br>
* Text: One-Dimensional (1D)<br>

**Other Properties Related to Input:** <br>
* Recommended maximum input resolution (Width, Height): 1664, 2048<br>
* Channel Count: 3<br>
* Prompt format: one task prompt composed from the supported control tokens. The default prompt extracts bounding boxes, semantic classes, and text in markdown format: `</s><s><predict_bbox><predict_classes><output_markdown><predict_text_in_pic>`.<br>

## Output(s): <br>
**Output Type(s):** Text<br>

**Output Format(s):** String<br>

**Output Parameters:** One-Dimensional (1D)<br>

**Other Properties Related to Output:** Nemotron 3.5 Parse returns a string encoding document text, semantic element classes, and content-normalized bounding boxes. Scale x coordinates by the evaluated image width and y coordinates by its height. Postprocessing utilities can convert table or chart-associated text into LaTeX, HTML, markdown, JSON, or CSV where supported.<br>

Our AI models are designed and/or optimized to run on NVIDIA GPU-accelerated systems. By leveraging NVIDIA hardware and software frameworks, the model achieves faster training and inference times compared to CPU-only solutions. <br>

## Software Integration:
**Runtime Engine(s):**
* Transformers <br>
* vLLM <br>

**Reference Hardware:** NVIDIA H100 and H200, BF16. See each benchmark for its hardware and configuration.<br>

**Supported Operating System(s):**
* Linux <br>

## Model Version(s):
Nemotron 3.5 Parse · October 17, 2026 release <br>

This AI model can be embedded as an Application Programming Interface (API) call through the documented Transformers or vLLM serving interfaces.

## Inference:
**Acceleration Engine:** Transformers, vLLM <br>
**Test Hardware:** <br>
* NVIDIA Hopper H100 <br>
* NVIDIA Hopper H200 (new DFlash2 throughput measurements) <br>

</details>

<details>
<summary>Training, testing, and evaluation data disclosures</summary>

## Training, Testing, and Evaluation Datasets:

### Training Dataset

**Data Modality:** <br>
* Image <br>
* Text <br>

**Image Training Data Size:** <br>
* 1 Million to 1 Billion Images <br>

**Text Training Data Size:** <br>
* 1 Billion to 10 Trillion Tokens <br>

**Data Collection Method by dataset:** <br>
* Automated, Manually-Collected, Synthetic <br>

**Labeling Method by dataset:** Automated, Manually-Labeled, Synthetic <br>
**Labeling Details:** Labels are produced through a combination of automated OCR and layout annotation, manual annotation, and synthetic generation. The combination varies by constituent dataset. <br>

**Properties:** The training set contains millions of image-text items aggregated across large document, table, and layout datasets. The data consists of document-page and table images paired with OCR text, bounding boxes, and layout labels. Sources include rendered digital documents, scientific papers, PDFs, Wikipedia-style pages, and synthetic document, table, word, and character renderings. Annotations come from OCR and layout models, third-party OCR services, synthetic-generation pipelines, and human labeling. <br>

### Testing Dataset

**Data Collection Method by dataset:** Automated, Manually-Collected, Synthetic  
**Collection Details:** Sources combine automated collection, manually collected material, and synthetic generation; methods vary by constituent dataset.

**Labeling Method by dataset:** Automated, Manually-Labeled, Synthetic  
**Labeling Details:** Labels are produced through a combination of automated OCR and layout annotation, manual annotation, and synthetic generation. The combination varies by constituent dataset.

**Properties:** Tested on internal and public document-understanding benchmarks using document-page images and reference text, layout classes, bounding boxes, and structure annotations. Coverage includes OCR quality, layout structure, table parsing, reading order, and visual grounding across document types and languages.

### Evaluation Dataset

**Data Collection Method by dataset:** Automated, Manually-Collected, Synthetic  
**Collection Details:** Sources combine automated collection, manually collected material, and synthetic generation; methods vary by constituent dataset.

**Labeling Method by dataset:** Automated, Manually-Labeled, Synthetic  
**Labeling Details:** Labels are produced through a combination of automated OCR and layout annotation, manual annotation, and synthetic generation. The combination varies by constituent dataset.

**Properties:** Evaluated on internal and public document-understanding benchmarks covering OCR quality, layout structure, table parsing, reading order, and visual grounding. The ParseBench reference evaluation covers 2,078 unique document pages. Additional benchmarks cover Indic-language OCR and multilingual synthetic OCR across the scripts listed below. <br>

Benchmark coverage: <br>
* ParseBench evaluates document parsing across text fidelity, semantic formatting, tables, charts, and visual grounding with layout boxes/classes. <br>
* IndicVisionBench evaluates OCR quality for Indic-language pages, including Bengali, Gujarati, Hindi, Kannada, Malayalam, Marathi, Odia, Punjabi, Tamil, and Telugu. <br>
* MOSCAR evaluates multilingual synthetic OCR across broad script coverage, including Latin, Arabic, Cyrillic, Han, Hangul, Japanese, Indic scripts, Hebrew, Thai, Greek, and others. <br>

</details>

### Deployment Geography:
Global<br>

### Use Case: <br>
Nemotron 3.5 Parse is designed for developers and teams building document intelligence, retrieval-augmented generation (RAG), curator, extractor, and agentic AI applications. It can convert scanned or rendered PDFs, presentation slides, forms, reports, tables, and mixed-content document pages into structured outputs for downstream indexing, retrieval, analytics, model training-data creation, and human-in-the-loop review.<br>

### Release Date:  <br>
Hugging Face 10/17/2026 via https://huggingface.co/nvidia/Nemotron-3.5-Parse <br>

## References:
* [Hugging Face Transformers mBART documentation](https://huggingface.co/docs/transformers/en/model_doc/mbart) <br>
* [NVIDIA C-RADIOv4-SO400M](https://huggingface.co/nvidia/C-RADIOv4-SO400M) <br>

### License/Terms of Use:
Governing Terms: Your use of this model is governed by the [OpenMDW License Agreement, version 1.1](https://openmdw.ai/license/1-1/). Use of the tokenizer included in this model is governed by the [MIT license and tokenizer attribution](https://huggingface.co/nvidia/Nemotron-3.5-Parse/blob/main/TOKENIZER_ATTRIBUTION.md). See [third-party notices](https://huggingface.co/nvidia/Nemotron-3.5-Parse/blob/main/THIRD_PARTY_NOTICES.md) for separately installed dependencies.<br>

Tokenizer source and modifications are documented in [TOKENIZER_ATTRIBUTION.md](TOKENIZER_ATTRIBUTION.md).

The portable ParseBench pipeline has its own [license](reference/parsebench/pipeline/LICENSE)
and [third-party notices](reference/parsebench/pipeline/THIRD_PARTY_NOTICES.md),
including the separately installed benchmark environment. See the
[component inventory](reference/package/benchmark_environment_components.json)
and [package build evidence](reference/package/README.md) for exact versions and digests.

### Deployment and responsible use

The integration of foundation and fine-tuned models into AI systems requires additional testing using use-case-specific data to ensure safe and effective deployment. Following the V-model methodology, iterative testing and validation at both unit and system levels is essential to mitigate risks, meet technical and functional requirements, and ensure compliance with safety and ethical standards before deployment. <br>

## Ethical Considerations:
NVIDIA believes Trustworthy AI is a shared responsibility and we have established policies and practices to enable development for a wide array of AI applications. Developers should work with their internal model team to ensure this model meets requirements for the relevant industry and use case and addresses unforeseen product misuse. <br>

Please make sure you have proper rights and permissions for all input image and video content. If an input image contains people, personal health information, confidential business data, or intellectual property, the model may extract or reproduce visible text from that content. <br>

For more detailed information on ethical considerations for this model, please see the Model Card++ [Bias](bias.md), [Explainability](explainability.md), [Safety & Security](safety.md), and [Privacy](privacy.md) subcards. <br>
Please report model quality, risk, security vulnerabilities, or NVIDIA AI Concerns [here](https://www.nvidia.com/en-us/support/submit-security-vulnerability/). <br>
