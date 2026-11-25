---
library_name: transformers
base_model: Qwen/Qwen3.5-4B
tags:
- decision-model
- typed-decisions
- multimodal
- safetensors
---

# LemonDecider 4B

LemonDecider 4B is a multimodal decision model built on Qwen3.5-4B. It answers named questions over text or JSON and up to four images. A request is encoded as one joint prompt: the shared state, then every question with its options, each followed by a decision marker. The model returns a probability distribution at every marker. A request that exceeds the 8,192-token serving limit is split by recursively bisecting the question list, never truncated.

- **Choice** selects an option and returns a probability for each candidate.
- **Noul** returns the probability that a yes/no proposition is true.
- **Score** rates the input against 2–10 ordered levels. It returns the probability of each level and the expected level, computed as the sum of each zero-based level index times its probability.

## Public Decision Index 0.3

LemonDecider 4B scored **64.25** on Text (140,178 requests) and **72.349** on Vision (12,210 requests) across the Decision Index 0.3 public suites.

| Panel | LemonDecider 4B | Requests |
| :---: | ---: | ---: |
| Text | **64.25** | 140,178 |
| Vision | **72.349** | 12,210 |

The evaluation used `joint-question-inline-readout-v1` with rereading disabled, temperature 0.835655, BF16/SDPA, a 262,144-token checkpoint context with an 8,192-token serving limit, and a 1,638,400-pixel cap per image.

### Per-dataset results

<details>
<summary>Show the Vision and Text breakdown</summary>

#### Public Vision (11 datasets)

| Dataset | Accuracy | Skill |
| --- | ---: | ---: |
| CV-Bench | 86.85 | 78.31 |
| BLINK | 73.57 | 59.08 |
| RealWorldQA | 80.65 | 68.37 |
| CharXiv | 81.95 | 75.94 |
| InfographicVQA | 96.31 | 95.08 |
| Mind2Web | 84.58 | 79.45 |
| Winoground | 91.75 | 83.50 |
| KIE (CORD+FUNSD) | 96.06 | 93.52 |
| Moderation (Hateful Memes) | 71.56 | 43.12 |
| R-Bench-M | 49.62 | 39.54 |
| MMMU-Pro vision | 45.14 | 37.08 |
| **Public Vision Index** | — | **72.349** |

#### Public Text (43 datasets)

| Dataset | Original metric | Non-Skill | Skill |
| --- | --- | ---: | ---: |
| BFCL | case exact accuracy | 96.40 | 95.14 |
| ToolRet | nDCG@10 | 61.23 | 55.23 |
| API-Bank | accuracy | 82.09 | 81.74 |
| BANKING77 | macro-F1 | 93.21 | 93.12 |
| CLINC150+OOS | macro-F1 | 95.02 | 94.99 |
| RouterBench † | selected quality (quality objective) | 79.93 | 52.94 |
| Home appliance simulator | case exact accuracy | 77.27 | 77.27 |
| SGD/SGD-X † | macro-F1 | 51.52 | 19.33 |
| ContractNLI | macro-F1 | 86.95 | 81.13 |
| ANLI | macro-F1 | 73.46 | 60.25 |
| BPoMP | accuracy | 98.47 | 96.94 |
| Humicroedit | accuracy | 63.96 | 27.93 |
| POP909-CL | accuracy | 79.82 | 79.66 |
| cfcolor | accuracy | 72.36 | 44.72 |
| MMLU † | accuracy | 81.20 | 74.93 |
| GPQA Diamond | accuracy | 52.04 | 36.05 |
| ARC-Easy † | accuracy | 99.20 | 98.93 |
| ARC-Challenge † | accuracy | 95.99 | 94.65 |
| WinoGrande | accuracy | 89.50 | 79.00 |
| HellaSwag | accuracy | 95.51 | 94.01 |
| GSM8K | accuracy | 64.94 | 58.01 |
| ChessBench | accuracy | 19.78 | 12.63 |
| MuSR | accuracy | 61.97 | 39.54 |
| SATA-Bench | case exact accuracy | 36.48 | 35.64 |
| SimpleBench † | accuracy | 20.00 | 4.00 |
| BRIGHT | nDCG@10 | 42.67 | 35.14 |
| Amazon ESCI | macro-F1 | 60.49 | 50.45 |
| ACOS | per-review F1 | 27.89 | 25.58 |
| FinEntity | macro-F1 | 93.44 | 90.35 |
| iSarcasmEval | Sarcasm F1 · track A, English | 64.14 | 53.87 |
| VAST | macro-F1 | 78.25 | 67.37 |
| NLI4CT | macro-F1 | 81.55 | 64.11 |
| CRUXEval | accuracy | 65.26 | 44.89 |
| CLadder | accuracy | 81.00 | 62.00 |
| HLE | accuracy | 12.57 | 0.00 |
| Habermas Machine | accuracy | 61.81 | 44.58 |
| PhishNChips phishing decisions | accuracy | 93.05 | 86.10 |
| MMLU-Pro | accuracy | 64.16 | 59.69 |
| BBH fixed-option tasks | accuracy | 76.70 | 66.23 |
| RAGTruth response-level hallucination | F1 on hallucinated class | 84.19 | 67.22 |
| HoVer claim verification | accuracy | 88.82 | 77.64 |
| When2Call MCQ | accuracy | 90.91 | 87.88 |
| New Yorker caption matching | accuracy | 65.91 | 57.39 |
| **Public Text Index** | **Weighted aggregate** | **72.64** | **64.25** |

† Shown but not counted in the index.
</details>

## Usage

Use Python 3.12 with the versions in `requirements.txt`.

```bash
python -m pip install -r requirements.txt
```

### Python

```python
from PIL import Image
from model import DecisionModel

model = DecisionModel(".", device="cuda:0")

text = model.predict(
    state="The order arrived damaged. The customer wants a refund.",
    questions={
        "intent": {
            "type": "choice",
            "instructions": "What does the customer want?",
            "criteria": {"refund": "A refund", "delivery": "Delivery status"},
        },
        "damaged": {"type": "noul", "instructions": "Does the customer mention damage?"},
        "urgency": {
            "type": "score",
            "instructions": "How urgent is the request?",
            "criteria": ["Low", "Medium", "High"],
        },
    },
)
print(text["answers"])

questions = {
    "which": {
        "type": "choice",
        "instructions": "Which image is red?",
        "criteria": {"first": "The first image", "second": "The second image"},
    }
}
with Image.open("blue.png") as blue, Image.open("red.png") as red:
    vision = model.predict(state={}, questions=questions, images=[blue, red])
print(vision["answers"])
```

Images are attached in list order before the state text. A request accepts up to four images; each image is resized within the processor's 65,536–1,638,400 pixel budget. A dictionary `{"state": ..., "questions": ..., "images": [...]}` is also accepted, where image entries are Base64 data URLs, raw Base64 strings or paths under the configured image root.

### HTTP API

`model.py --serve` exposes the same decision request on both `POST /v1/systemone` and `POST /v1/decisions`. `/v1/systemone` is the Decision Index text-engine route; `/v1/decisions` is the official `decide` engine's image-capable JSON protocol. Both take `model`, `state`, `questions` and optional `images`.

```bash
python model.py --serve --port 8173 --image-root ./images
```

Send a text request with an inline JSON body.

```bash
curl -fsS http://127.0.0.1:8173/v1/systemone \
  -H 'Content-Type: application/json' -d '{
  "state": "The order arrived damaged. The customer wants a refund.",
  "questions": {
    "intent": {
      "type": "choice",
      "instructions": "What does the customer want?",
      "criteria": {"refund": "A refund", "delivery": "Delivery status"}
    },
    "damaged": {"type": "noul", "instructions": "Does the customer mention damage?"},
    "urgency": {
      "type": "score",
      "instructions": "How urgent is the request?",
      "criteria": ["Low", "Medium", "High"]
    }
  }
}'
```

For a vision request, add an ordered `images` array. Entries can be Base64 data URLs (`data:image/...;base64,...`), raw Base64 strings, or server-side file paths relative to `--image-root`.

```bash
curl -fsS http://127.0.0.1:8173/v1/decisions \
  -H 'Content-Type: application/json' -d '{
  "state": {},
  "images": ["blue.png", "red.png"],
  "questions": {
    "which": {
      "type": "choice",
      "instructions": "Which image is red?",
      "criteria": {"first": "The first image", "second": "The second image"}
    }
  }
}'
```

The response puts results under `answers` using the supplied question IDs.

## Decision Index compatibility and submission

The two public runs use the joint/no-reread protocol reproduced by `model.py`. The checkpoint config also sets the legacy single-question `inference_protocol.read_twice` field to `false`; the joint readout above is the only decision path. The evaluated checkpoint is the weight set in this repository; the 255 × 2,560 readout head has sha256 `20295371f7bdea1e91e583d4d881934931b71f271907c7bebeacd31aa2387731`, and the index contains 724 tensors and 4,539,918,336 parameters. This repository also contains the matching image-capable inference code and model card.

```bash
python -m pip install "huggingface_hub>=0.34,<2"
hf download inclusionAI/LemonDecider --local-dir ./lemondecider-4b
python -m pip install -r ./lemondecider-4b/requirements.txt
python ./lemondecider-4b/model.py --serve --host 127.0.0.1 --port 8173
```

With that server running on loopback, the official kit uses `http` for text and `decide --option protocol=decisions` for Vision:

```bash
python -m decision_index run --engine http \
  --option base_url=http://127.0.0.1:8173 \
  --option model=LemonDecider-4B-v3.2 --out runs/lemondecider-text
python -m decision_index vision pipeline --dir work/vision --engine decide \
  --option base_url=http://127.0.0.1:8173 --option protocol=decisions \
  --out runs/lemondecider-vision
```

The public results are in `inclusionAI/lemondecider-decision-index-results` under `runs/lemondecider-4b-v32-text` and `runs/lemondecider-4b-v32-vision`, and contain every request's prediction, probabilities, wall time and official scores. Private Text/Vision evaluation and official single-RTX-PRO-6000 latency qualification remain maintainer-run.
