# ParseBench pipelines

Run Nemotron 3.5 Parse with single-, double-, or triple-pass inference, apply the bundled postprocessing, and evaluate with the official ParseBench scorer. Model weights, benchmark data, reference answers, and saved predictions are downloaded or generated separately.

| Pipeline | Inference stages | Reproduced ParseBench score |
| --- | --- | ---: |
| Single | Full-page parse | 72.72 |
| Double | Full-page parse → Table/Chart crops from predicted boxes | 74.88 |
| Triple | Full-page parse → separate detection pass → Table/Chart crops | 75.14 |
| Triple, region union | Same stages, with additional full-page regions after overlap filtering | 75.20 |

Scores are percentages, averaged over the five official category headlines, including Visual Grounding Element Pass Rate (EPR). These are measurements of the same checkpoint, not guarantees for every stochastic run. See [expected_results.json](expected_results.json) and [validation_metrics.json](validation_metrics.json) for exact scores, identities, and validation coverage.


The default triple-pass pipeline uses the separate detector's regions. To add Table/Chart regions found by the full-page parser, use `--triple-regions union` with `run.py`. This retains detector regions first, removes near-duplicates at IoU 0.85, suppresses added regions overlapping an original same-class box at IoU 0.5, and caps the region list at 80. It uses more crop requests. The matched full-dataset comparison improved by approximately 0.05 percentage points.

Postprocessing also removes literal repeated elements at the same coordinates, normalizes existing list bullets, removes discretionary soft hyphens between letters in textual roles, and repairs empty incomplete serialization prefixes. Code/math content is protected. Plain above-chart captions and original chart subtitles are preserved in their associated chart captions; notes below charts stay standalone. No new data values or axis/legend labels are invented.

## Download and install

Use Linux, Python 3.12, and one NVIDIA Hopper H100 with 80 GB memory for the reference serving profile. Start in this pipeline directory. Authenticate with Hugging Face if needed.

```bash
python3.12 -m venv .serve-venv
source .serve-venv/bin/activate
python -m pip install 'huggingface-hub==1.24.0'

# Fetch the evaluated model/runtime. Use the helpers in this directory.
export PIPELINE="$(pwd)"
hf download nvidia/Nemotron-3.5-Parse \
  --revision e5e0406c85ec241b164907bf41ebd648a54e4ea2 \
  --exclude 'reference/**' '*.whl' --local-dir model

export MODEL="$(realpath model)"
export BENCH_WORK="$(pwd)/parsebench-work"
mkdir -p "$BENCH_WORK"
# Install the source from that exact historical revision. No wheel download is needed.
python -m pip install "${MODEL}[vllm,client]"
python -m pip install -r "$PIPELINE/requirements.txt"
python -m pip check

hf download llamaindex/ParseBench --repo-type dataset \
  --revision 2805a1d940f95a203e0ae4b88be9934f7765b3fc \
  --local-dir "$BENCH_WORK/public-data"
```

The packaged vLLM plugin supplies one-token MTP; no legacy `sitecustomize` or training checkout is needed. `serve.py` verifies the evaluated weight SHA-256 and key runtime versions before starting. `PACKAGE_MANIFEST.json` lists the bundled helper file hashes.

## Prepare public data

Keep the scorer/data environment separate from serving:

```bash
python3.12 -m venv "$BENCH_WORK/score-venv"
source "$BENCH_WORK/score-venv/bin/activate"
python -m pip install -r "$PIPELINE/requirements-scorer-lock.txt"
python "$PIPELINE/prepare_data.py" \
  --snapshot "$BENCH_WORK/public-data" \
  --output "$BENCH_WORK/data" --workers 8
```

This prepares 2,078 unique inputs from the public PDFs and JSONL annotations. It sorts source PDF paths, assigns stable `parsebench_00000` keys, and renders the **first page of each source PDF** at 150 DPI with PyMuPDF 1.26.3, RGB, and JPEG quality 92. Sources containing additional PDF pages are recorded in `preparation.json`; those additional pages are outside this measured input contract. The resulting images and annotations were checked against all 2,078 evaluated inputs with zero differences.

The output contains five compact `train/*.tar` shards, a per-image SHA-256 manifest, and a preparation receipt. Annotation data is used for dataset preparation and scoring; the inference client reads only page images and stable keys.

## Start serving and run inference

Reactivate the serving environment from the original working directory:

```bash
source .serve-venv/bin/activate
python "$PIPELINE/prepare_inputs.py" --dataset-root "$BENCH_WORK/data" \
  --images-out "$BENCH_WORK/images" --manifest-out "$BENCH_WORK/inputs.jsonl"
python "$PIPELINE/serve.py" --model "$MODEL" --port 8000
```

In another terminal, restore the same `MODEL`, `PIPELINE`, and `BENCH_WORK` paths and activate the serving environment. Run all three pipelines:

```bash
python "$PIPELINE/run.py" \
  --images-dir "$BENCH_WORK/images" --manifest "$BENCH_WORK/inputs.jsonl" \
  --endpoint http://127.0.0.1:8000/v1 --mode all \
  --output "$BENCH_WORK/results"
```

To reproduce the **75.20** headline score, add `--triple-regions union` to the command above, or use `--mode triple --triple-regions union` to run only that profile.

Choose `--mode single`, `--mode double`, or `--mode triple` to run one pipeline. `all` shares the full-page pass across modes. Use a new output directory for each run. For a small smoke test, append:

```bash
--keys parsebench_00000,parsebench_00010,parsebench_00568,parsebench_01087,parsebench_01405,parsebench_01571,parsebench_02077
```

Default concurrency is 128. Full-page parsing and detection use temperature 0.2 and repetition penalty 1.05; crop parsing uses temperature 0.1 and repetition penalty 1.0. All requests use top-k 50, top-p 1.0, and seed 20261012. Output limits are 8,744 tokens for parsing and 4,096 for detection. Table/Chart crops use predicted boxes, a 4% plus 12-pixel margin, and JPEG quality 95. These settings are recorded in `contract.json`.

Crops are merged into the full-page output using ordered structural additions and guarded table replacement. All three modes automatically apply the same postprocessing:

- Convert predicted tables, charts, and semantic formatting into Markdown/HTML.
- Infer table headers from predicted spans and existing bold markup. No English header vocabulary or forced header bolding is applied.
- Preserve predicted panel and chart-caption context.
- For chart columns consistently containing numeric pairs such as `32 (16.6%)`, separate the existing values into **Value** and **Percent** subcolumns. This requires at least two matching nonempty cells and does not calculate or invent values.

These rules operate on predictions without benchmark categories, annotations, page-specific routing, or reference answers. They remain heuristics and can make errors on other document distributions.

Permanent outputs are compact JSONL/gzip files and receipts:

```text
results/
  contract.json
  inputs.jsonl
  direct.jsonl.gz
  single/predictions.jsonl.gz
  double/predictions.jsonl.gz
  double/crop_predictions.jsonl
  triple/predictions.jsonl.gz
  triple/crop_predictions.jsonl
  triple/detection_predictions.jsonl.gz
  complete.json
```

Each final prediction includes `key`, `raw_out`, `markdown`, and `coordinate_frame`. Temporary crop images are deleted after each mode. Put `--scratch` on local storage when available. Timing receipts from `all` share an initial pass and should not be treated as independent throughput measurements.

## Score with official ParseBench

The latest official scorer validated for this bundle is pinned to commit `9af4102e26b51f234ab5f037e19fec05c0696ec6` (October 16, 2026). Upstream source is downloaded separately and is not modified.

```bash
source "$BENCH_WORK/score-venv/bin/activate"
git clone https://github.com/run-llama/ParseBench.git "$BENCH_WORK/ParseBench"
git -C "$BENCH_WORK/ParseBench" checkout 9af4102e26b51f234ab5f037e19fec05c0696ec6

for mode in single double triple; do
  python "$PIPELINE/score.py" \
    --source "$BENCH_WORK/ParseBench/src" --dataset-root "$BENCH_WORK/data" \
    --predictions "$BENCH_WORK/results/$mode/predictions.jsonl.gz" \
    --output "$BENCH_WORK/results/$mode/score" --workers 16
done
```

The adapter passes the final Markdown and predicted geometry to the official evaluators. `score.py` verifies all 241 upstream Python source hashes, scores every page freshly with the default rule timeouts, and writes per-page results and independently checked aggregate means. Add `--allow-partial` only for smoke-test scoring. Full runs require 2,078 unique keys. Later upstream revisions require a separate validation and updated source hashes.

Expected finite metric counts are Tables 503, Charts 568, Content Faithfulness 506, Semantic Formatting 456, and Visual Grounding EPR 500. Formatting has 476 cases, of which 456 have applicable finite metrics. Errors are recorded and cause scoring to fail.

## Replay postprocessing and validation

Reapply conversion to saved inference without a GPU or benchmark annotations:

```bash
source .serve-venv/bin/activate
python "$PIPELINE/postprocess.py" \
  --direct "$BENCH_WORK/results/direct.jsonl.gz" \
  --crops "$BENCH_WORK/results/triple/crop_predictions.jsonl" \
  --output "$BENCH_WORK/replay.jsonl.gz" --workers 8
```

Omit `--crops` for single-pass rendering; use the double-pass crops for double-pass replay.

The portable client generated all stages on all 2,078 public inputs using one H100 and the pinned release weights. Detector-only and union triple outputs share the same fresh full-page, detection and original-region crop responses. Every mode was scored freshly with the pinned official scorer. Public-data preparation reproduces the reference inputs byte-for-byte.

The corrected renderer was replayed on all 8,312 saved outputs without new inference. A conservative header rule changes four pages per mode while preserving raw predictions, geometry, cell text, order, and spans. Empty-title guards cover both chart-rendering paths. All four modes were then freshly scored with the pinned official scorer. `validation_metrics.json` preserves the original HTTP hashes separately from the final renderer and corrected prediction hashes.

Original licenses and notices are preserved in the accompanying files. `SOURCE_MANIFEST.json` records the extracted NVIDIA implementation sources and subsequent simplifications; `PACKAGE_MANIFEST.json` identifies this bundle.


## License and environment notices

See this directory's [license](LICENSE) and [third-party notices](THIRD_PARTY_NOTICES.md).
The separately installed scoring environment is inventoried in
[benchmark_environment_components.json](../../package/benchmark_environment_components.json).
The source, model runtime, scoring dependencies and benchmark data keep their
respective licenses. The notice update does not change inference or scorer code.
