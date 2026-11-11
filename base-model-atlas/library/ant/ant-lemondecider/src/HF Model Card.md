---
license: apache-2.0
base_model: Qwen/Qwen3.5-4B
library_name: transformers
tags:
- decision-engine
- typed-decision
- choice
- classification
- merge
- qwen3.5
---

# LemonDecider 4B

**Model ID:** `lemondecider-4b-20261104-v3`  
**Base model:** `Qwen/Qwen3.5-4B`

This v3 release makes typed decisions from a shared text state and named questions. It returns choice probabilities, yes/no probabilities (noul), or ordinal scores without generating an answer token stream. Requests that fit use one joint forward; overlength question lists are recursively bisected, preserving the complete state and every option in each chunk. Inputs are never truncated.

## Model description

| Property | Value |
|---|---|
| Architecture | Qwen3.5-4B hybrid backbone with a 255-option decision readout |
| Loader | `modeling_lemondecider.LemonDeciderForDecisionClassification`, `trust_remote_code=True` |
| Model type / protocol | `lemondecider_decision` / `lemondecider-v1` |
| Attention | Noncausal periodic full-attention layers; hybrid recurrent layers; SDPA |
| Readout | Native inline joint-question readout (`joint_readout.predict_joint`) |
| Temperature | 1.0026751894886363, inherited from the parent checkpoint; not refit |
| Capacity | 8192 tokens per chunk including template; at most 255 options per question |
| Serving strategy | `recursive-question-bisection-v1`; short requests are not split |
| Precision | BF16 loading; model-specific readout precision preserved by packaged implementation |
| Serialized tensors | 724 |
| Modalities | Published HTTP service is text-only |
| Runtime | Python 3.12; evaluated runtime recorded Torch 2.9.0, Transformers 5.17.0, FLA 0.5.2 |


## Training

LemonDecider 4B v3 was fine-tuned (SFT) from a common Qwen3.5-4B initialization on 1,199,692 decision/QA rows (about 1.20M training rows, with separate development, calibration and test splits). The released weights are a uniform FP32 average of four checkpoints from the same SFT run, followed by scalar temperature calibration—not a combination of two independent training runs.

Question formats: choice (up to 255 options; 84.4%), noul (no/yes; 15.2%) and score (ordinal ratings; 0.4%). This training run is text-only, with the vision tower frozen. The original training corpus retains joint-question grouping where applicable; the single-record export preserves the question-level content but removes grouping metadata and is not an exact reproduction of the original joint-training layout.

**Data categories**:

- Service and action decisions — user-intent routing, case classification, agent-action safety and policy judgments;
- Language judgment — sentiment, sarcasm, natural language inference, factuality and paraphrase-style checks;
- Knowledge and reasoning QA — multiple-choice knowledge, commonsense and logical reasoning, arithmetic and math word problems;
- Retrieval and selection — relevance judgments, information retrieval and product selection;
- Preference and quality judgments — helpfulness, correctness, safety and response-quality comparisons;
- Probability and ordinal judgments — yes/no probabilities and ordered ratings.

**Training parameters** (from the recorded configuration and training log):

- Distributed FSDP with full sharding on 16 accelerators;
- One epoch, 4,690 optimization steps, effective batch size 256, learning rate 2e-6;
- Maximum sequence length and token budget 8,192; native joint-question inline readout;
- Objective recorded as option_cross_entropy; choice permutation global-reference; text-only inputs and frozen vision tower;
- Warmup ratio 0.15, weight decay 0.01, gradient clipping 1.0, gradient checkpointing enabled;
- Precision policy fp32-master-bf16, BF16 serving load, SDPA with noncausal full attention;
- Four-checkpoint weight averaging; final temperature 1.0026751894886363, fitted on 1,448 held-out calibration rows.

The corpus manifest records fingerprint-based filtering against protected JevBench and Decision Index evaluation inputs, while some source collections include benchmark training splits. This is not a blanket guarantee of zero overlap, nor a claim that every upstream source has permissive redistribution terms; source-specific terms still require review.

## Package artifacts

### Weight files

| File | Bytes | SHA-256 |
|---|---:|---|
| `model-00001-of-00002.safetensors` | 4,973,336,472 | `49d5d5302c6457507ec3d0bc424248352344d44fab47a216a4a8e73e4975d490` |
| `model-00002-of-00002.safetensors` | 4,106,591,800 | `f1b25448bae5837b10bdf1d7854fd75414d2c7439b1f288331e740d7fbdf43a9` |
| `tokenizer.json` | 19,989,492 | `6f32ce20dc35f57a7f9ad1eac03525bd7d30f9df8cea6507e958279cc3657706` |
| `model.safetensors.index.json` | 68,426 | `f78614fd6c201725fe3f749e71474375eabe2c2f3029c5eb7d1880da42143320` |

The repository keeps the HF model/processor/tokenizer layout. `joint_readout.py`
is required for the reproducing joint bridge; `code/` provides the joint CLI
and local HTTP service; `tests/` contains chunking regression tests. The root
`model.py` remains only for the old independent-question path and is not the
recommended reproducing CLI.

## Evaluation results

### 1) Decision Index, edition 0.4 — full public suite

On **2026-11-04**, this model was evaluated over the complete public
0.4 suite using **16 PPU-ZW810E workers**. The run was joint inference plus
iterative question bisection. The official scorer reported `complete: true`.
The underlying selected file contains **140,620 rows**: **140,178 scoreable**
requests and **442 officially excluded** requests. The benchmark-native summary
counts **140,148 answered / 30 unsupported** requests; unsupported requests
remain in index coverage.

| Headline | Value |
|---|---:|
| **Decision Index (public 0.4)** | **61.67** |
| Raw index | 70.84 |
| Breadth skill | 60.28 |
| Median / mean / p95 request latency | 49.9 ms / 121.2 ms / 286.9 ms |

This is a self-evaluated complete public-suite run, not a private Full score or
submission-accepted leaderboard result. Latency is HTTP request wall time on a
16-worker PPU run, not official single-GPU latency admission.

#### Per-area scores

| Area | Raw | Skill | Coverage | Benchmarks |
|---|---:|---:|---:|---:|
| Knowledge & Reasoning | 0.5320 | 0.4063 | 0.9998 | 11 |
| Language Understanding | 0.7616 | 0.6674 | 1.0000 | 9 |
| Retrieval & Classification | 0.7680 | 0.6909 | 1.0000 | 6 |
| Tools & Automation | 0.8029 | 0.7817 | 0.9986 | 5 |
| Arts & Human Taste | 0.7345 | 0.5790 | 0.9979 | 6 |

#### Per-benchmark native scores (★ = included in the public index)

The **Score** column uses each benchmark's native headline metric. Skill and
coverage come from the official index report; area weighting and chance
correction can therefore make Skill differ from Score. iSarcasmEval uses its
English track-A headline, matching the suite's selected summary. All values
are generated from this model run, not from the earlier v3 card.

| # | Benchmark | Metric | Requests | Score | Skill | Cov. |
|---:|---|---|---:|---:|---:|---:|
| 1 | BFCL ★ | case exact accuracy | 1,694 | 0.9528 | 0.9362 | 1.0000 |
| 2 | ToolRet ★ | nDCG@10 | 685 | 0.6354 | 0.5768 | 0.9971 |
| 3 | API-Bank ★ | accuracy | 508 | 0.8478 | 0.8415 | 0.9961 |
| 4 | BANKING77 ★ | macro-F1 | 3,080 | 0.9317 | 0.9308 | 1.0000 |
| 5 | CLINC150+OOS ★ | macro-F1 | 5,500 | 0.9423 | 0.9420 | 1.0000 |
| 6 | RouterBench | selected quality (quality objective) | 10,000 | 0.7936 | 0.5161 | 1.0000 |
| 9 | Home appliance simulator ★ | case exact accuracy | 88 | 0.6477 | 0.6477 | 1.0000 |
| 10 | SGD/SGD-X | macro-F1 | 2,500 | 0.4253 | 0.0438 | 1.0000 |
| 11 | ContractNLI ★ | macro-F1 | 123 | 0.8684 | 0.8097 | 1.0000 |
| 12 | ANLI ★ | macro-F1 | 3,200 | 0.7203 | 0.5810 | 1.0000 |
| 20 | BPoMP ★ | accuracy | 5,000 | 0.9858 | 0.9715 | 1.0000 |
| 21 | Humicroedit ★ | accuracy | 2,628 | 0.6320 | 0.2641 | 1.0000 |
| 22 | POP909-CL ★ | accuracy | 2,000 | 0.8339 | 0.8197 | 0.9875 |
| 23 | cfcolor ★ | accuracy | 5,000 | 0.7446 | 0.4336 | 1.0000 |
| 24 | MMLU | accuracy | 14,033 | 0.7940 | 0.7253 | 1.0000 |
| 25 | GPQA Diamond ★ | accuracy | 196 | 0.4643 | 0.2857 | 1.0000 |
| 26 | ARC-Easy | accuracy | 2,376 | 0.9882 | 0.9843 | 1.0000 |
| 27 | ARC-Challenge | accuracy | 1,172 | 0.9548 | 0.9397 | 1.0000 |
| 28 | WinoGrande ★ | accuracy | 1,267 | 0.8942 | 0.7884 | 1.0000 |
| 29 | HellaSwag ★ | accuracy | 10,042 | 0.9511 | 0.9348 | 1.0000 |
| 30 | GSM8K ★ | accuracy | 2,638 | 0.6391 | 0.5680 | 1.0000 |
| 31 | ChessBench ★ | accuracy | 5,000 | 0.1220 | 0.0437 | 1.0000 |
| 32 | MuSR ★ | accuracy | 752 | 0.6037 | 0.3700 | 1.0000 |
| 33 | SATA-Bench ★ | case exact accuracy | 1,650 | 0.2636 | 0.2538 | 1.0000 |
| 34 | SimpleBench | accuracy | 10 | 0.1000 | 0.0000 | 1.0000 |
| 36 | BRIGHT ★ | nDCG@10 | 220 | 0.4485 | 0.3762 | 1.0000 |
| 37 | Amazon ESCI ★ | macro-F1 | 5,000 | 0.6007 | 0.4991 | 1.0000 |
| 38 | ACOS ★ | per-review F1 | 1,565 | 0.3341 | 0.3128 | 1.0000 |
| 39 | FinEntity ★ | macro-F1 | 979 | 0.9331 | 0.9016 | 1.0000 |
| 40 | iSarcasmEval ★ | see separate subtask tracks | 4,600 | 0.6076 | 0.4952 | 1.0000 |
| 41 | VAST ★ | macro-F1 | 3,006 | 0.7683 | 0.6524 | 1.0000 |
| 42 | NLI4CT ★ | macro-F1 | 5,500 | 0.8051 | 0.6208 | 1.0000 |
| 43 | CRUXEval ★ | accuracy | 570 | 0.6333 | 0.4182 | 1.0000 |
| 44 | CLadder ★ | accuracy | 5,000 | 0.7960 | 0.5920 | 1.0000 |
| 45 | HLE ★ | accuracy | 501 | 0.1140 | 0.0000 | 0.9980 |
| 50 | Habermas Machine ★ | accuracy | 1,676 | 0.6092 | 0.4328 | 1.0000 |
| 56 | PhishNChips phishing decisions ★ | accuracy | 2,000 | 0.7890 | 0.5780 | 1.0000 |
| 57 | MMLU-Pro ★ | accuracy | 12,032 | 0.5910 | 0.5400 | 1.0000 |
| 58 | BBH fixed-option tasks ★ | accuracy | 5,507 | 0.7086 | 0.5776 | 1.0000 |
| 59 | RAGTruth response-level hallucination ★ | F1 on hallucinated class | 2,700 | 0.8371 | 0.6622 | 1.0000 |
| 61 | HoVer claim verification ★ | accuracy | 4,000 | 0.8922 | 0.7844 | 1.0000 |
| 62 | When2Call MCQ ★ | accuracy | 3,652 | 0.8976 | 0.8635 | 1.0000 |
| 64 | New Yorker caption matching ★ | accuracy | 528 | 0.6420 | 0.5525 | 1.0000 |

The repository intentionally omits results.jsonl, benchmark labels, raw logs and
suite inputs. If separately publishing evaluation evidence, attach immutable
model weights and an immutable results dataset rather than editing predictions.

## Usage

Install a hardware-compatible **Torch 2.9.0** build in a Python 3.12 environment,
then install the stated pure-Python dependencies. The requirements file is a
candidate recipe rather than a vendor-validated NVIDIA lockfile. Download the
entire model directory before loading; custom code executes during loading, so
inspect `configuration_lemondecider.py`, `modeling_lemondecider.py` and
`joint_readout.py` first.

```bash
python -m pip install -r requirements.txt
```

### Python: native joint decisions with capacity-aware chunking

```python
import json
import sys
from pathlib import Path

checkpoint = Path("./LemonDecider").resolve()
sys.path.insert(0, str(checkpoint / "code"))
from serve_312k import LemonDeciderHFService

service = LemonDeciderHFService(checkpoint, "cuda:0", None)
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
print(json.dumps(service.predict(request), indent=2))
```

### CLI and HTTP

From this repository root:

```bash
python code/verify_files.py
python tests/test_chunking.py
CUDA_VISIBLE_DEVICES=0 python code/infer.py --input examples/request.json
# Alternatively, start the local HTTP service:
CUDA_VISIBLE_DEVICES=0 bash code/serve.sh
# In another terminal:
python code/smoke_test.py
```

HTTP endpoints are `GET /health`, `GET /v1/models`, and `POST /v1/systemone`.
The service binds to localhost by default. Use `LEMONDECIDER_API_KEY` for
optional bearer authentication. The local smoke client assumes that variable is
unset.

A long question list is recursively bisected in original order. Each chunk
contains the complete state and every option. Planning finishes before the first
model forward, so a singleton that cannot fit rejects the entire request with
HTTP 422. Answers retain their original IDs, and input usage sums all chunks
including repeated state. No reread, option pruning or benchmark-specific
rendering is performed.

No new GPU inference was performed merely to rename the public loader. The
AutoConfig loader is checked offline in this package, the remote-code modeling
implementation is functionally equivalent to the evaluated implementation after
class and protocol naming normalization, and the two safetensors files retain the exact
evaluated model hashes above. Path-adjusted users should still run
`tests/test_chunking.py`; production users should smoke-test once on their own
hardware and accelerator build.

## Intended use & limitations

- Designed for option-based routing, classification, structured choices and
  typed decision endpoints, not open-ended text generation.
- A probability output does not imply a correctness or calibration guarantee.
- Capacity is 8192 tokens per chunk, not the backbone's 262144-position setting.
- A long shared state cannot be shortened to make a question fit.
- The HTTP bridge is text-only. Vision tensors in the checkpoint do not imply a
  supported public image API or a reported vision benchmark result.
- Iterative bisection is part of the release contract; omitting it changes
  behavior on overlength joint requests.
- Unsupported cases remain in scoring coverage. Public results do not establish
  performance on private tests, unseen domains or real-world traffic.
- The published service is not a safety system. Validate decisions for the
  domain, locale, language and affected population before deployment.

## License

`LICENSE` is Apache-2.0 and `LICENSE.code` is MIT. Both are retained from the
LemonDecider export. The Qwen3.5-4B base model remains subject to its own
upstream terms. Applicable upstream copyright, license and notice obligations
pass through to users. This packaging does not expand rights over training data
or evaluation data.

## Acknowledgements

This model family builds on the Qwen backbone and the typed-decision runtime
work used in LemonDecider. Attribution and notices remain in the packaged
license files.
