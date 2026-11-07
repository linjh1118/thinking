# DFlash2 single-, double-, and triple-pass throughput

One H200, BF16, all 2,078 ParseBench pages, three independent full-set trials per configuration. Each mode uses its best tested serving profile, selected by median fully completed-page throughput. The model card reports processed-page throughput; both measures and completion counts appear below.

| Mode | Pages/s | Observed range | Fully completed pages/s | Complete pages / 2078 |
| --- | ---: | --- | ---: | --- |
| single | 18.57 | 17.97–18.61 | 18.29 | [2051, 2049, 2047] |
| double | 14.60 | 14.35–14.67 | 14.33 | [2041, 2040, 2039] |
| triple | 13.49 | 13.39–13.74 | 13.24 | [2043, 2038, 2039] |

The inference clock runs from the first model request to the final response. It includes HTTP, server queueing and dependent crop preparation; it excludes initial page preparation, startup, warmup, output writing and final rendering after the last response. Each workload starts with a fresh server and separate synthetic warmup pages. This is prepared-page inference throughput, not PDF-ingestion throughput.

All modes use the published overlapping pipeline, alternatives merging, original image resolution and generation budgets. Triple pass refines the detector/parser union. Token-limited responses remain marked incomplete and do not count toward fully completed-page throughput. Timing does not establish new accuracy scores; the model card retains the separate reference-protocol scores.

## Serving settings

| Mode | Draft tokens | Concurrency | Capacity | Batched tokens | Prefix cache | Processor cache GiB | GPU memory fraction |
| --- | ---: | ---: | ---: | ---: | --- | ---: | ---: |
| single | 16 | 512 | 512 | 32768 | False | 4 | 0.8 |
| double | 16 | 128 | 192 | 32768 | False | 4 | 0.8 |
| triple | 16 | 256 | 256 | 65536 | True | 8 | 0.9 |

Native vLLM, TP1, maximum context 16,384, FA3, async scheduling and chunked prefill on, model compilation off with full-decode CUDA graphs. Eight preparation/render workers. The commands below preserve the measured graph shapes.

Full-page/detection defaults: temperature 0.2, repetition penalty 1.05; crops: temperature 0.1, repetition penalty 1.0. Top-k 50, top-p 1, seed 0; parsing cap 8,744 and detection cap 4,096. These settings are unchanged across the tuning study.

## Concurrency range

The table shows the best confirmed HTTP single-pass profile at each tested concurrency. The main card’s base/MTP/DFlash2 figure uses a separate native greedy protocol; these rates must not be combined with it.

| Concurrency | Draft | Batch tokens | Prefix cache | Processor cache GiB | Pages/s | Completed pages/s |
| ---: | ---: | ---: | --- | ---: | ---: | ---: |
| 1 | 32 | 32768 | False | 4 | 3.23 | 3.18 |
| 2 | 32 | 32768 | False | 4 | 5.65 | 5.57 |
| 4 | 32 | 32768 | False | 4 | 9.02 | 8.89 |
| 8 | 32 | 32768 | False | 4 | 12.76 | 12.60 |
| 16 | 32 | 32768 | False | 4 | 15.14 | 14.93 |
| 32 | 16 | 32768 | False | 4 | 17.33 | 17.08 |
| 64 | 8 | 32768 | False | 4 | 17.82 | 17.54 |
| 128 | 16 | 32768 | True | 4 | 18.22 | 17.92 |
| 256 | 16 | 32768 | False | 4 | 18.46 | 18.20 |
| 512 | 16 | 32768 | False | 4 | 18.57 | 18.29 |

For concurrency 512, the confirmed profile uses fresh HTTP connections. Other profiles use a 1-second idle connection lifetime.

[Download confirmed metrics and settings](optimization.json). Ranges are observed min/max, not confidence intervals. Best tested settings are workload-specific; output lengths and crop counts can change with nonzero sampling.

## Use the measured profiles

Start the server for your chosen mode with one of these native vLLM commands:

- [Single pass](serve-single.sh)
- [Double pass](serve-double.sh)
- [Triple pass](serve-triple.sh)

Download the complete model repository as `./parse35` first. These scripts use its bundled DFlash2 weights and do not install a serving plugin. Each mode has its own measured concurrency, draft length and server settings.

Run from the directory containing `./parse35`, for example `bash ./parse35/reference/dflash2-passes/serve-triple.sh`. The client below uses the matching request window and HTTP connection settings. Images must already be RGB pages; PDF rendering is excluded from these timings.

```python
import sys
from pathlib import Path
import httpx
sys.path.insert(0, "./parse35")
from nemotron_parse.inference import DocumentParser

PROFILES = {'single': {'concurrency': 512, 'keepalive': 0}, 'double': {'concurrency': 128, 'keepalive': 'pooled'}, 'triple': {'concurrency': 256, 'keepalive': 'pooled'}}

def main():
    mode = sys.argv[1]
    profile = PROFILES[mode]
    concurrency = profile["concurrency"]
    keepalive = 0 if profile["keepalive"] == 0 else max(64, concurrency)
    pages = sys.argv[2:]
    with httpx.Client(
        timeout=1800, limits=httpx.Limits(
            max_connections=max(64, concurrency),
            max_keepalive_connections=keepalive, keepalive_expiry=1.0,
        ),
    ) as client:
        with DocumentParser(
            base_url="http://localhost:8000/v1", model="nemotron-parse", client=client,
        ) as parser:
            prepared = parser.prepare(pages, workers=8)
            result = parser.parse_prepared(
                prepared, mode=mode, concurrency=concurrency, postprocess_workers=8,
                triple_regions="union", schedule="pipelined", allow_partial=True,
            )
    print(result.metrics)

if __name__ == "__main__":
    main()
```

Call `python ./parse35/reference/dflash2-passes/run_profile.py triple pages/*.png` after starting the corresponding server. Preparation, warmup and output writing must be handled consistently when reproducing timings. `allow_partial=True` retains and marks capped pages; inspect the complete-page count as well as speed.

Generation defaults and scoring reproduction are preserved in the [reference pipeline](../parsebench/pipeline/README.md).
