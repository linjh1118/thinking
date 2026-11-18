---
license: apache-2.0
base_model: Qwen/Qwen3.5-4B
library_name: transformers
pipeline_tag: text-classification
language:
- en
- zh
tags:
- lemondecider
- decision-engine
- typed-decision
- classification
---

# LemonDecider 4B

**Model ID:** `lemondecider-4b-20261112-v3.1`  
**Base model:** `Qwen/Qwen3.5-4B`

LemonDecider makes typed decisions from a text or structured-JSON state and named
questions. It returns choice probabilities, yes/no probabilities (`noul`), or ordinal
scores without generating an answer token stream. This release processes questions
independently, retaining the complete state and options for each question. Inputs
are never truncated.

## Model description

| Property | Value |
|---|---|
| Architecture | Qwen3.5-4B hybrid backbone with a 255-option decision readout |
| Loader | `modeling_lemondecider.LemonDeciderForDecisionClassification`, `trust_remote_code=True` |
| Model type | `lemondecider_decision` |
| Attention | Noncausal periodic full-attention layers; hybrid recurrent layers; SDPA |
| Readout | Marker-position decision readout; one question per forward |
| Temperature | **0.835655**, scalar calibrated and applied by the bundled runtime |
| Capacity | **8,192 tokens per question**, including the rendered template; up to 255 options |
| Serving strategy | Independent-question processing; configured short-input rereading within the input sequence |
| Precision | BF16 weights; FP32 probability postprocessing |
| Serialized tensors | 724 |
| Modalities | Text and structured JSON only |
| Runtime | Python 3.12; tested with a PyTorch 2.9.0 accelerator build and Transformers 5.17.0 |

## Training

### Stage 1: general decision learning

The initial stage establishes broad typed-decision capabilities through supervised
fine-tuning on approximately **1.20 million decision/QA examples**, covering `choice`,
`noul`, and `score` tasks.

**Data categories:**

- Service and action decisions: intent routing, classification, and action selection;
- Language judgment: sentiment, inference, factuality, and paraphrase-style checks;
- Knowledge and reasoning: knowledge QA, commonsense, logic, and arithmetic;
- Retrieval and selection: relevance judgments and candidate selection;
- Preference and quality judgments: response quality and ordered comparisons;
- Probability and ordinal judgments: yes/no probabilities and graded ratings.

### Model-aware incremental data construction

The guiding idea is to build data around what the base model has **not yet mastered**,
rather than blindly accumulating more examples:

- **Incorrect answers become training candidates directly**, concentrating supervision
  on observed weaknesses.
- **Correct answers are followed by one more question or reasoning step**, or an added
  condition, to create more challenging variants instead of repeatedly training on easy cases.

Following this principle, **35,467 incremental decision examples** were assembled
through selection, rewriting, and difficulty enhancement. The emphasis is on the
learning value of each example, not dataset size alone.

### Stage 2: targeted decision refinement

Stage 2 continues supervised fine-tuning of the existing decision model on the
incremental corpus, focusing on difficult decisions and more demanding conditions
while retaining the same three output types. The resulting updates are consolidated
into full weights, with calibrated probability postprocessing. The released package
is self-contained and does not require a separate adapter or base-model download.

## Package artifacts

### Weight files

| File | Bytes | SHA-256 |
|---|---:|---|
| `model-00001-of-00002.safetensors` | 4,973,336,472 | `a88cb411fb417c49f2ed4444d17f93f9c7c1e8af5fcde81768c00022c8c87499` |
| `model-00002-of-00002.safetensors` | 4,106,591,800 | `dd8090bb59e0b6bcca04b4966e249a69de5f697bfd4bb9f4ad99a92b2e34aef6` |
| `tokenizer.json` | 19,989,492 | `6f32ce20dc35f57a7f9ad1eac03525bd7d30f9df8cea6507e958279cc3657706` |
| `model.safetensors.index.json` | 68,427 | `cdc57ae81f5d72a44461bdbb9949139319294b25ce35734646fb0c7b074f52f8` |

The package keeps the HF model/processor/tokenizer layout. The root `model.py` is the
recommended Python, CLI, and HTTP entry point. `decision_runtime.py` implements input
preparation and typed answers; `example.json` demonstrates all three question types.
Run `python verify.py` to check the complete `SHA256SUMS` manifest.

The distribution does not include training data, raw predictions, benchmark inputs,
or internal experiment logs. Required copyright and license notices are retained.

## Evaluation results

### Decision Index, edition 0.3 — complete public scoreable suite

The completed **2026-11-16** local development run covered **140,178 scoreable requests**
across **43 benchmarks**. The suite contains 140,620 requests in total, of which 442
are officially excluded from scoring. The recorded scorer reported `complete: true`,
with **140,099 ok**, **79 unsupported**, and **0 errors**. Unsupported requests remain
in index coverage.

| Headline | Value |
|---|---:|
| **Decision Index (balanced skill)** | **63.78** |
| Raw index | 72.09 |
| Breadth skill | 62.87 |
| Recorded request wall time: median / mean / p95 | 102.6 / 342.5 / 1121.6 ms |

These are previously recorded local development results, not an official leaderboard
acceptance or a fresh full evaluation of the BF16-fused publication package. Recorded
latencies are from the in-process evaluation run, not an HTTP deployment benchmark
or a single-GPU latency certification.

#### Per-area scores

Headline scores use a 0–100 scale. Area and benchmark values below use 0–1.

| Area | Raw | Skill | Coverage | Benchmarks |
|---|---:|---:|---:|---:|
| Knowledge & Reasoning | 0.5797 | 0.4639 | 0.9992 | 11 |
| Language Understanding | 0.7866 | 0.7004 | 1.0000 | 9 |
| Retrieval & Classification | 0.7883 | 0.7314 | 0.9926 | 6 |
| Tools & Automation | 0.7516 | 0.7299 | 0.9926 | 5 |
| Arts & Human Taste | 0.7253 | 0.5701 | 0.9967 | 6 |

#### Per-benchmark native scores (★ = included in the public index)

The Score column uses each benchmark's native headline metric on supported cases;
Skill and Coverage come from the index report. Chance correction, track aggregation,
and coverage adjustment can make these columns differ. For iSarcasmEval, Score is
the English track-A headline, not a combined score across subtasks.

| # | Benchmark | Metric | Requests | Score | Skill | Cov. |
|---:|---|---|---:|---:|---:|---:|
| 1 | BFCL ★ | case exact accuracy | 1,694 | 0.9728 | 0.9633 | 1.0000 |
| 2 | ToolRet ★ | nDCG@10 | 685 | 0.6678 | 0.5894 | 0.9650 |
| 3 | API-Bank ★ | accuracy | 508 | 0.5158 | 0.5044 | 0.9961 |
| 4 | BANKING77 ★ | macro-F1 | 3,080 | 0.9313 | 0.9304 | 1.0000 |
| 5 | CLINC150+OOS ★ | macro-F1 | 5,500 | 0.9543 | 0.9540 | 1.0000 |
| 6 | RouterBench | selected quality (quality objective) | 10,000 | 0.7995 | 0.5299 | 1.0000 |
| 9 | Home appliance simulator ★ | case exact accuracy | 88 | 0.7500 | 0.7500 | 1.0000 |
| 10 | SGD/SGD-X | macro-F1 | 2,500 | 0.5553 | 0.2601 | 1.0000 |
| 11 | ContractNLI ★ | macro-F1 | 123 | 0.8618 | 0.8002 | 1.0000 |
| 12 | ANLI ★ | macro-F1 | 3,200 | 0.7586 | 0.6384 | 1.0000 |
| 20 | BPoMP ★ | accuracy | 5,000 | 0.9802 | 0.9600 | 1.0000 |
| 21 | Humicroedit ★ | accuracy | 2,628 | 0.6130 | 0.2260 | 1.0000 |
| 22 | POP909-CL ★ | accuracy | 2,000 | 0.7434 | 0.7181 | 0.9800 |
| 23 | cfcolor ★ | accuracy | 5,000 | 0.7230 | 0.4535 | 1.0000 |
| 24 | MMLU | accuracy | 14,033 | 0.8164 | 0.7552 | 1.0000 |
| 25 | GPQA Diamond ★ | accuracy | 196 | 0.5153 | 0.3537 | 1.0000 |
| 26 | ARC-Easy | accuracy | 2,376 | 0.9895 | 0.9860 | 1.0000 |
| 27 | ARC-Challenge | accuracy | 1,172 | 0.9556 | 0.9408 | 1.0000 |
| 28 | WinoGrande ★ | accuracy | 1,267 | 0.9092 | 0.8184 | 1.0000 |
| 29 | HellaSwag ★ | accuracy | 10,042 | 0.9556 | 0.9408 | 1.0000 |
| 30 | GSM8K ★ | accuracy | 2,638 | 0.6630 | 0.5963 | 1.0000 |
| 31 | ChessBench ★ | accuracy | 5,000 | 0.2048 | 0.1339 | 1.0000 |
| 32 | MuSR ★ | accuracy | 752 | 0.6436 | 0.4334 | 1.0000 |
| 33 | SATA-Bench ★ | case exact accuracy | 1,650 | 0.3327 | 0.3238 | 1.0000 |
| 34 | SimpleBench | accuracy | 10 | 0.2000 | 0.0400 | 1.0000 |
| 36 | BRIGHT ★ | nDCG@10 | 220 | 0.4447 | 0.3512 | 0.9591 |
| 37 | Amazon ESCI ★ | macro-F1 | 5,000 | 0.6131 | 0.5147 | 1.0000 |
| 38 | ACOS ★ | per-review F1 | 1,565 | 0.4130 | 0.3942 | 1.0000 |
| 39 | FinEntity ★ | macro-F1 | 979 | 0.9323 | 0.9004 | 1.0000 |
| 40 | iSarcasmEval ★ | Sarcasm F1 (track A, English) | 4,600 | 0.6684 | 0.5734 | 1.0000 |
| 41 | VAST ★ | macro-F1 | 3,006 | 0.8025 | 0.7038 | 1.0000 |
| 42 | NLI4CT ★ | macro-F1 | 5,500 | 0.8221 | 0.6539 | 1.0000 |
| 43 | CRUXEval ★ | accuracy | 570 | 0.6825 | 0.4962 | 1.0000 |
| 44 | CLadder ★ | accuracy | 5,000 | 0.8076 | 0.6152 | 1.0000 |
| 45 | HLE ★ | accuracy | 501 | 0.1549 | 0.0000 | 0.9920 |
| 50 | Habermas Machine ★ | accuracy | 1,676 | 0.6187 | 0.4467 | 1.0000 |
| 56 | PhishNChips phishing decisions ★ | accuracy | 2,000 | 0.9275 | 0.8550 | 1.0000 |
| 57 | MMLU-Pro ★ | accuracy | 12,032 | 0.6541 | 0.6110 | 1.0000 |
| 58 | BBH fixed-option tasks ★ | accuracy | 5,507 | 0.7863 | 0.6902 | 1.0000 |
| 59 | RAGTruth response-level hallucination ★ | F1 on hallucinated class | 2,700 | 0.8373 | 0.6627 | 1.0000 |
| 61 | HoVer claim verification ★ | accuracy | 4,000 | 0.8875 | 0.7750 | 1.0000 |
| 62 | When2Call MCQ ★ | accuracy | 3,652 | 0.8806 | 0.8408 | 1.0000 |
| 64 | New Yorker caption matching ★ | accuracy | 528 | 0.6932 | 0.6165 | 1.0000 |

The publication runtime was separately checked on **91 requests / 444 questions**
covering all 43 benchmark categories and all three output types. Outputs matched
a reference implementation using the **same fused weights**. This validates runtime
integration on that sample; it is not a substitute for a new complete benchmark run.

## Usage

Install a hardware-compatible PyTorch/torchvision build in a Python 3.12 environment,
then install the remaining dependencies. Do not overwrite an accelerator vendor's
PyTorch build with a generic CUDA wheel. The tested runtime used PyTorch 2.9.0 and
Transformers 5.17.0; other hardware/software combinations should be smoke-tested locally.
Download the entire model directory before loading. Custom code executes during
loading, so review the packaged Python files first.

```bash
python -m pip install -r requirements.txt
python verify.py
```

### Python: typed decisions

```python
import json
import sys
from pathlib import Path

checkpoint = Path("./LemonDecider").resolve()
sys.path.insert(0, str(checkpoint))
from model import DecisionModel

model = DecisionModel(checkpoint, device="cuda:0")
request = {
    "state": "The customer wants to return a damaged package.",
    "questions": {
        "action": {
            "type": "choice",
            "instructions": "Choose the next action.",
            "criteria": {
                "refund": "Offer a refund",
                "tracking": "Check tracking"
            }
        },
        "damaged": {
            "type": "noul",
            "instructions": "Is the package damaged?"
        }
    }
}
print(json.dumps(model.predict(request), indent=2))
```

### CLI and HTTP

From the model directory:

```bash
python model.py --device cuda:0 --input example.json
# Alternatively, start the local HTTP service:
python model.py --serve --device cuda:0 --port 8000
# In another terminal, when API-key authentication is unset:
curl -s http://127.0.0.1:8000/health
curl -s http://127.0.0.1:8000/v1/systemone \
  -H 'Content-Type: application/json' --data-binary @example.json
```

HTTP endpoints are `GET /health`, `GET /v1/models`, and `POST /v1/systemone`.
The service binds to localhost by default. Set `LEMONDECIDER_API_KEY` to require
bearer authentication on all endpoints; binding to a non-loopback address requires
that key to be set. Use HTTPS and appropriate access controls in production.
Health responses do not expose local checkpoint paths.

Requests may contain multiple named questions. Each is processed independently;
short inputs use the package's configured second reading within the input sequence.
Oversized structured states may fall back to plain JSON without optional index
annotations, but original content and options are not truncated. If a question still
exceeds capacity, the request fails with HTTP 422. Do not apply another chat template
or temperature transformation outside the supplied runtime.

For installation details, input schemas and additional examples, see
[QUICKSTART.md](QUICKSTART.md).

## Intended use & limitations

- Designed for routing, classification, structured choices and ordinal judgments,
  not open-ended text generation.
- A probability output is not a correctness or calibration guarantee.
- `noul` is the probability of the affirmative answer. `score` is the expected
  zero-based ordinal level and need not be an integer.
- Capacity is 8,192 tokens per rendered question, not the backbone's positional limit.
- The serving API is text-only; serialized vision tensors do not imply image support.
- The bundled renderer and postprocessing are part of the inference contract.
- Local development results do not establish independent generalization, performance
  on private tests, or reliability on real deployment traffic.
- The model is not a safety system. Validate it for the intended domain and population
  before deployment.

## License

`LICENSE` contains the Apache-2.0 license and `LICENSE.code` contains the MIT license.
Applicable upstream copyright, license and notice obligations remain in effect;
see `NOTICE`. This release does not expand rights over training or evaluation data.

## Acknowledgements

LemonDecider builds on the Qwen backbone and the open-source model/runtime ecosystem.
Required attribution is preserved in the packaged license and notice files.
