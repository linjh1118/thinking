# ParseBench comparison sources

The [main card](../../../README.md#parsebench) shows 10 selected comparison models and single-, double- and triple-pass Nemotron 3.5 Parse profiles. It uses published overall scores, without replacing them with reproduced scores. The [CSV](results.csv) contains the same 13 rows; [results.json](results.json) adds provenance and retains the earlier reproduction sweep for reference.

## Scores

The selected comparison scores were checked against the current upstream leaderboard on October 17, 2026. Its revision remains `9af4102e26b51f234ab5f037e19fec05c0696ec6`; the published scores are unchanged. Displayed speeds use the completed matched prepared-page runs below.

Comparison-model scores come from the [pinned ParseBench leaderboard](https://github.com/run-llama/ParseBench/blob/9af4102e26b51f234ab5f037e19fec05c0696ec6/leaderboard.csv) or, for [Nemotron Parse 2.0](https://huggingface.co/nvidia/NVIDIA-Nemotron-Parse-2.0/blob/b6742064f4a8cf22a10383ece5e7fbead355ac04/README.md), its released model card. Published protocols and scorer versions can differ from our reproduction runs. Category-level differences and reproduced results remain in the JSON; they do not replace the published headline scores.

The Nemotron 3.5 rows use scored outputs from the same measured runs as their speed receipts:

* **Single-pass: 72.74**, from `baseline/single` in [scheduler benchmark receipt](../../validation/batch_benchmarks.json).
* **Double-pass: 74.92** and **triple-pass: 75.20**, from `fresh_full_runs` in [accuracy restoration receipt](../../validation/accuracy_restoration.json).

All three cover 2,078 inputs and use the released weights with SHA-256 `81dd7609c589f3694ce75520c25af5010953231358de6aec4d03e8c6aac787e9`. The scored prediction digests match the measured-run artifacts. These results use the scorer identified in their receipts. The existing reference-pipeline triple-pass headline and its category metrics remain unchanged; its 75.20 rounds to the same value as the newer general helper's triple-pass result.

## Throughput

Every displayed speed uses **pages/s** on the same **2,078 prepared ParseBench page images**, with **one H100 per model**. The ten comparison models were rerun with their native model stages enabled, including detection, recognition, and dependent region or chart rereads where applicable.

The timer spans the first model call through the final response, including server queueing, response transfer, and gaps for dependent crop preparation and dispatch. Concurrent call durations are not added. Initial page preparation, server startup, untimed warmup, final document rendering and file writes are excluded. Paddle includes its local learned layout detector and VLM calls; MinerU is timed before final Markdown rendering.

[Matched inference timing](matched_inference_timing.json) records all ten comparison models, receipt/prediction digests, exact input-image identity, coverage, and current weight checks. [Nemotron inference timing](../../validation/inference_benchmarks.json) records the single/double/triple profiles at **15.42 / 11.65 / 10.62 pages/s**. Every comparison run has 2,078 unique outputs; successful empty responses are preserved as empty predictions rather than omitted or regenerated.

Rates count processed pages, including token-limited responses. The Nemotron receipt also reports untruncated-page counts and rates. Some native SDKs do not expose per-page finish reasons. Published accuracy scores remain separate from these speed measurements; the Nemotron rows' scored prediction digests are checked against their timing runs.

Historical full-document timings remain explicitly named in the JSON's `models` records. The displayed card, CSV and `published_comparison` array use the matched prepared-page timings. These are measured serving profiles, not a claim of maximum hardware throughput.
