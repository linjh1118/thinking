# Quick20 and full500 release regression

These fixed OmniDocBench v1.5 subsets contain 20 and 500 pages. Full500 has 250 table pages and 250 picture/figure pages. This is the portable `layout_lite` regression harness, not official OmniDocBench TEDS or ParseBench.

The references were refreshed on October 18, 2026 using the released model at revision `dca5b2df89d00a671509204501d8f1f379d5e94f`, weights SHA-256 `81dd7609c589f3694ce75520c25af5010953231358de6aec4d03e8c6aac787e9`, and package `3.5.0.post7`. Both splits completed without request failures. See [validation.json](validation.json) for the exact run and verification scope, and [reference_manifest.json](reference_manifest.json) for artifact hashes.

## Scores

| Full500 metric | Historical raw parsing | Released table parsing |
| --- | ---: | ---: |
| Overall | 70.17% | 74.49% |
| Table quality | 70.41% | 83.38% |
| Layout class F1 at IoU 0.50 | 66.10% | 66.10% |
| Table recall at IoU 0.50 | 93.36% | 93.36% |
| Picture recall at IoU 0.50 | 74.01% | 74.01% |

Both columns use the same raw model predictions. Version 3 converts only predicted Table bodies through the released HTML postprocessor before applying the existing metric formulas. Boxes, classes, ground truth and other block text stay unchanged. This corrects parsing compatibility; it is not an inference improvement. Full500 table quality averages character-bag F1, cell-bag F1 and grid-shape similarity on table pages. Overall averages class F1, table quality and picture recall.

Full500 request-phase throughput was 9.03197 pages/s on one H100 80GB, BF16, with one-token MTP, concurrency 128, 16 warmups and preloaded images. The timed 500-page request phase took 55.35890 seconds; startup, preload, warmup, conversion and scoring are excluded. All 19 token-capped pages and 2 malformed Table bodies remain in scoring. Quick20 contains 1 capped page. This is one measured profile, not a serving ceiling.

## Reference files

Each split includes:

- `predictions.jsonl`: new raw model outputs. Only `image_path` is made portable; `raw_out`, usage, termination reason and latency are preserved.
- `tables_html_predictions.jsonl`: derived Table-body HTML conversion for inspection.
- `validation_metrics.json` and `.csv`: version 3 released-table scores.
- `legacy_validation_metrics.json` and `.csv`: historical raw-parser scores for the same outputs.
- `coverage.json`, `benchmark_metrics.json`, `speculative_metrics.json` and `table_conversion_audit.json`: coverage, timing, MTP counters and conversion audit.

Use raw `predictions.jsonl` as scorer input. The scorer applies conversion internally; do not preconvert it a second time.

## Reproduce

Install the source package from the same immutable model snapshot used for inference and retain the evaluation inputs locally. The bundle does not distribute dataset images or labels. [evaluation_input_manifest.json](evaluation_input_manifest.json) records exact input hashes; its ParseBench section retains historical input provenance.

```bash
export MODEL_REPO=/absolute/path/to/model-snapshot
export EVAL_ROOT=/absolute/path/to/evaluation-data
export SPLIT=full500  # quick20 is also supported.
python -m pip install "$MODEL_REPO[client]"
```

Start the release's documented vLLM server with one H100, BF16, one-token MTP, FA3, a 16,384-token context, 192 maximum sequences and 16,384 batched tokens; disable prefix caching. Then run:

```bash
python "$MODEL_REPO/vllm_example.py" \
  --base-url http://127.0.0.1:8000/v1 --model nemotron-parse \
  --image-dir "$EVAL_ROOT/$SPLIT/images" --out-dir "$SPLIT-result" \
  --concurrency 128 --warmup-count 16 --preload-images --max-tokens 8744 \
  --temperature 0 \
  --prompt '</s><s><predict_bbox><predict_classes><output_markdown><predict_text_in_pic>' \
  --no-annotate --no-write-text-files \
  --predictions-jsonl "$SPLIT-result/predictions.jsonl" \
  --metrics-out "$SPLIT-result/benchmark_metrics.json"

python "$MODEL_REPO/reference/parse_3_5/scorer/score_layout_candidate_predictions.py" \
  --labels "$EVAL_ROOT/$SPLIT/labels.jsonl" \
  --predictions "$SPLIT-result/predictions.jsonl" \
  --out "$SPLIT-result/validation_metrics.json" \
  --csv-out "$SPLIT-result/validation_metrics.csv" \
  --coord-mode normalized --table-mode released
```

Compare the seven metrics in [expected_results.json](expected_results.json) against the matching split, using absolute tolerance 0.02. Different GPU batch schedules can change outputs; exact byte equality is not required. For historical version 2 raw scoring, add `--table-mode legacy` and compare with `legacy_validation_metrics.json`. Legacy mode only requires Python's standard library. Released mode requires the installed `nemotron_parse` package.

The measured container used Pillow 12.3.0 rather than the source package's 12.2.0 pin. This is recorded as a dependency deviation, not a clean dependency-lock reproduction. Existing `inference.constraints.txt` and `transformers.constraints.txt` retain the older rc3 environment for historical provenance; they are not locks for this refreshed run.

Older reference predictions and scores remain accessible in repository history at revision `dca5b2df89d00a671509204501d8f1f379d5e94f`. ParseBench pipelines and their references are separate from this refresh.
