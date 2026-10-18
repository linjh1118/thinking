# Document postprocessing and multipass parsing

The public helpers operate on model predictions and ordinary page images. They do
not load benchmark labels, scorer code, category IDs, reference answers, or
page-specific rules. They are adapted from the general conversion and crop-merge
components of the bundled ParseBench pipeline. The pinned reproduction bundle
remains unchanged so its recorded hashes and results stay reproducible.

## Installation

For vLLM, use the model card's repository-source installation:

```bash
hf download nvidia/Nemotron-3.5-Parse --local-dir nemotron-parse
cd nemotron-parse
python -m pip install '.[vllm,client]'
```

This installs the plugin, public `nemotron_parse` Python package, compatibility
modules, and `nemotron-parse` command. No prebuilt wheel is required.
The repository source installs the vLLM plugin, parsing helpers and CLI together.
Archived release artifacts and their digests are listed in the
[build evidence](../reference/package/README.md).
Use version 3.5.0.post5 or later for the restored merge default and post7 or later
for the corrected third-party notices.

For Transformers, keep the model card's inference dependencies. To download the
helpers without installing the package:

```bash
python -m pip install 'beautifulsoup4==4.13.3' 'Pillow==12.2.0' 'numpy==2.2.6' 'httpx==0.28.1'
hf download nvidia/Nemotron-3.5-Parse \
  --include 'postprocessing.py' 'latex2html.py' 'nemotron_parse/**' --local-dir .
```

Run Python in that directory, or put it on your Python import path. Basic text/table
postprocessing only needs Beautiful Soup; the image wrappers also need Pillow and
NumPy. The HTTP backend needs httpx. Downloaded source and installed packages
provide the same public API.

## Render an existing prediction

```python
from nemotron_parse import postprocess_document, PostprocessOptions

options = PostprocessOptions(
    infer_headers=True,
    render_charts=True,
    split_chart_value_percent=True,
    relocate_chart_captions=True,
)
document = postprocess_document(raw_model_output, image_size=(width, height), options=options)
print(document['markdown'])
print(document['blocks'])
```

`raw_out` contains the cleaned model serialization. Each block has its original
class, normalized `bbox`, literal `text`, and rendered `content`. Supplying
`image_size` adds clipped, ordered `bbox_pixels`. `markdown` renders the complete
page in model order, with section headings and HTML tables for span preservation.
Raw per-block text remains available independently of presentation changes.
Malformed table markup that cannot be converted is preserved rather than passed
through a lossy row splitter; document `warnings` identify these blocks.

Default cleanup preserves empty cells, spans, line breaks, nested inline styles,
and escaped literals. It removes exact repeated blocks at identical coordinates,
repairs empty incomplete serialization prefixes, removes internal continuation
markers, and normalizes existing bullets and soft hyphens in textual roles.
Code/math roles and marked code/math text are protected from soft-hyphen cleanup.
Table conversion is applied to Table/Chart blocks; literal LaTeX in prose, code,
formulas, or Picture blocks retains its source representation.
Header inference uses predicted span topology and existing bold styling, never an
English vocabulary list. It can still make mistakes; disable `infer_headers` to
use only explicit predicted headers. Unknown classes and page numbers are retained.

Chart titles, subtitles, and explicit panel labels can be rendered with their
associated tables. Two guarded presentation choices are enabled by default and can be disabled:

- `split_chart_value_percent=True` splits consistently predicted numeric pairs
  such as `32 (16.6%)` into Value and Percent subcolumns. It requires at least two
  matching nonempty cells, adds those column labels, and does not calculate values.
- `relocate_chart_captions=True` associates a plain caption immediately above a
  chart when geometry and text-preservation checks pass. Notes below remain
  standalone. Set `relocate_chart_captions=False` to retain the standalone caption in its source order.

`normalize_text=False`, `deduplicate=False`, and `render_charts=False` disable the
corresponding cleanup/rendering choices. The existing root imports continue to
work:

```python
from postprocessing import extract_classes_bboxes, postprocess_text
from latex2html import convert_html_table_to_json_hierarchical
```

`postprocess_text(..., cls='Table', table_format=...)` supports LaTeX, HTML,
Markdown, record JSON, hierarchical JSON, and CSV. HTML retains merged-cell
structure. Flat exports expand spans and use neutral column names for headerless
tables without consuming the first data row as a header. Duplicate column names
are disambiguated without overwriting values. Hierarchical JSON retains the
existing `headers`, `columns`, and flat `data` fields and additionally exposes
`body_cells` with explicit text, span, and header-role metadata.

## Parse a page with a running vLLM server

Start the server using the model card. Then:

```python
from nemotron_parse.inference import DocumentParser

with DocumentParser(base_url='http://localhost:8000/v1', model='nemotron-parse') as parser:
    single = parser.parse('page.png')
    double = parser.parse_double('page.png')
    triple = parser.parse_triple('page.png', triple_regions='union')
    documents = parser.parse_many(['one.png', 'two.png'], mode='double', concurrency=128)
```

| Mode | Work performed |
| --- | --- |
| Single | Full-page parse and document rendering |
| Double | Full-page parse, then Table/Chart crops from its predicted regions |
| Triple | Full-page parse, separate detection, then Table/Chart crop parsing |

A pass denotes a stage, not one request: each retained crop needs its own model
call. `triple_regions='union'` retains detector regions first and adds parser
regions after overlap filtering; `'detector'` uses only the separate detector.
The region budget defaults to 80 per page and can be changed with `max_regions`.
Crops use 4% plus 12-pixel margins and JPEG quality 95, configurable margins, and
content-normalized coordinates mapped back to the original image. Tiny crops are
skipped. Crops are made in memory and no temporary image files remain.

The default `merge_policy="alternatives"` preserves differing overlapping
Table/Chart predictions from the full-page and crop passes. Near-identical blocks
are deduplicated using geometry and text. Guarded table refinement checks native
grid validity and compatible column counts; the original block order is preserved
and crop alternatives are inserted by their predicted geometry. This policy
matches the reference approach using only model predictions, without labels,
benchmark categories or scorer feedback.

A returned document can contain overlapping or conflicting Table/Chart hypotheses.
Use `DocumentParser(merge_policy="guarded")` (CLI: `--merge-policy guarded`) when
one selected prediction per overlapping same-class region is preferable. This
option applies conservative structural replacement and rejects overlapping
same-class additions. It can discard a correct alternative, reducing recall.
Raw stage responses remain available with either policy.

Returned results include `stages` with original raw responses and usage, and
`inference` with request counts, regions, sampling, and crop/rendering settings.
Empty, failed, filtered, or token-limited generations raise `GenerationError`;
its `stage` and `response` expose the failed response. Successful stage responses
from the same page are only returned when parsing completes. No automatic retry
policy changes the request settings.

Sampling is configurable per stage:

```python
from nemotron_parse.inference import DocumentParser, GenerationSettings

with DocumentParser(
    fullpage=GenerationSettings(temperature=0, top_k=1, repetition_penalty=1.1),
    detection=GenerationSettings(temperature=0, top_k=1, max_tokens=4096),
    crop=GenerationSettings(temperature=0, top_k=1, repetition_penalty=1.0),
) as parser:
    document = parser.parse_double('page.png')
```

Defaults are temperature 0.2 / repetition penalty 1.05 for full-page and detection,
and 0.1 / 1.0 for crops, top-k 50, top-p 1.0, seed 0. Token caps are 8,744 for
parsing and 4,096 for detection. These are practical starting settings rather than
a claim of optimal sampling for every document type.

## Use an already loaded Transformers model

Continue from the model card's Transformers setup:

```python
from nemotron_parse.inference import DocumentParser, TransformersBackend

backend = TransformersBackend(model, processor, generation_config=generation_config)
with DocumentParser(backend=backend) as parser:
    document = parser.parse_triple(image)
```

This uses the same image/crop orchestration without a server or plugin. The adapter
serializes calls to the shared model, uses inference mode, applies stage settings,
and restores the CPU/current-GPU RNG after generation. Model weights and processor
remain caller-owned. Reaching the token cap is conservatively reported as
truncation, including when generation forces an EOS at the cap.

Other inference implementations can supply a callable
`backend(image, *, prompt, stage, settings)` returning
`{'raw_out': text, 'finish_reason': 'stop', 'usage': {...}}`. A string return is also
accepted, but then the custom backend must detect truncation itself. Custom
backends used with `parse_many` should support concurrent calls or use concurrency 1.

## Command line

```bash
nemotron-parse --image page.png --mode double --output parsed-page
nemotron-parse --image-dir pages --mode triple --triple-regions union --output parsed-pages
```

The download-only equivalent is `python -m nemotron_parse.inference` with the same
arguments. The default outputs are compact `documents.jsonl.gz` and `metrics.json`, containing
blocks, raw stages, settings and timing. Add `--write-page-files` for individual
Markdown and JSON exports. Use a new/empty output directory. Files are written only
after all pages complete. The API accepts PIL images and image paths; the CLI
accepts image files. Render PDF pages to images before calling it.

## Validation and scope

Run the focused CPU regression suite from the downloaded repository:

```bash
python -m pip install pytest
python -m pytest -q tests/test_postprocessing.py tests/test_inference.py tests/test_batch.py
```

The 86 focused tests passed from both source and the installed wheel. They cover
table structure, text preservation, chart defaults and opt-outs, crop geometry,
merge guards, HTTP handling, explicit truncation reporting, batch ordering,
independent-stage overlap, early crop submission, a shared concurrency bound,
and staged/pipelined region and output equivalence with deterministic responses.
The Transformers adapter is checked with a small CPU model stub. The real-model
H100 runs and official full-page scoring are recorded below and in
[the validation receipt](../reference/validation/postprocessing.json). The pinned reproduction
bundle and its recorded headline result remain unchanged.

## Prepared batches and timing

`parser.prepare(images, workers=8)` returns a reusable in-memory batch containing
decoded RGB pixels and encoded image requests. Existing RGB JPEG/PNG/WebP payloads
are retained without another lossy encode. Other inputs are encoded as PNG.
The preparation time is reported separately, and cached images can occupy several
GB for thousands of document pages.

`parser.parse_prepared(batch, mode="double", concurrency=128, postprocess_workers=8)`
returns a `BatchResult` with `documents` and `metrics`. The default
`schedule="pipelined"` overlaps independent full-page and detection requests,
submits detector crops as soon as their regions are ready, and adds parser-only
regions in the original union order. Double-pass crops similarly start as each
page finishes its full-page request. Ready crops take the next available HTTP
slot, and new pages fill remaining slots. All stages share one bounded
`concurrency` window, including requests waiting inside vLLM. Crop preparation
uses separate CPU threads; finished pages merge and render while other pages
continue inference. Large batches use spawned rendering processes.

Run standalone scripts under a main guard, or choose `postprocess_workers=1`.
HTTP `parse_many` uses this same pipelined batch engine and returns only the
documents. Its default request window is 128; a custom backend retains the
four-worker default. Pass `concurrency=1` for a backend that requires serial calls.
Use `schedule="staged"` for stage-barrier comparisons. A custom Transformers
backend still serializes its shared model calls.

Metrics include separately reported initial preparation, pipeline elapsed time,
request counts, token-limit counts, and processed-page and fully completed-page
throughput. Pipeline time excludes
initial preparation and output-file writing; model-dependent crop preparation is
included. A benchmark should also report serialization and warmup/server-startup
exclusions explicitly. The same prepared batch can be reused for different modes;
each call generates its own responses and provides an independent pipeline timing.
Pipelined stage spans overlap and must not be added together.
`request_service_seconds` sums concurrent request latency, including server queue
wait; it is not GPU compute time. `peak_inflight_requests` records the client
window, while actual server running/waiting requests require vLLM metrics.

Strict generation handling remains the default. Set `allow_partial=True` (CLI:
`--allow-partial`) only when partial results are useful: capped raw responses are
preserved, affected pages have `complete=False` and `generation_warnings`, and
truncated crops are excluded from refinement. HTTP/transport errors and empty
responses still raise. A successful benchmark execution does not imply that every
page completed within its token limit; inspect both coverage and throughput.

The CLI supports `--no-split-chart-value-percent` and
`--no-relocate-chart-captions` to disable the default presentation rules.

## Measured prepared-batch performance

The following matched scheduler comparison used the earlier **guarded** merge
policy in package 3.5.0.post4. The restored default and its fresh results are in
[accuracy restoration](#accuracy-restoration-with-the-faster-scheduler).

Measured on all 2,078 unique ParseBench pages with one H100 80GB, vLLM 0.26.0,
`--distributed-executor-backend uni`, tensor parallelism 1, one-token MTP, FA3,
`max_num_seqs=192`, `max_num_batched_tokens=16384`, and `max_model_len=16384`.
Both chart presentation rules were enabled. Each run generated all of its own
responses. The same-server comparison used the same prepared images and
per-mode concurrency limit for both schedulers.

| Mode | Concurrency | Staged pages/s | Pipelined pages/s | Pipelined elapsed | Fully completed pages |
| --- | ---: | ---: | ---: | ---: | ---: |
| Single | 128 | 14.56 | 14.91 | 139.4 s | 2047/2078 |
| Double | 256 | 11.16 | 11.87 | 175.0 s | 2038/2078 |
| Triple | 128 | 7.31 | 10.90 | 190.6 s | 2039/2078 |

Initial decoding/encoding of the full batch took 9.7 seconds and was excluded
from these rates. Timed work includes all model calls, predicted-region crop
preparation, merge and rendering; startup, warmup and output serialization are
excluded. The receipt separately reports serialization-inclusive rates.

These diagnostic runs explicitly enabled `allow_partial=True`. Token-limited
responses remain visible and affected pages count as incomplete. The table reports
processed-page throughput; fully completed-page throughput and cap counts are in
[the benchmark receipt](../reference/validation/batch_benchmarks.json). Strict failure handling remains
the API default. A successful scoring run does not make truncated generations complete.

Concurrency 128 and 256 were compared on a 256-page pilot; the selected settings
above were then checked on the full batch. The earlier full single-pass sweep reached
15.09 pages/s at 256. These are measured serving profiles, not a throughput ceiling.
Sampling is nonzero: changed batching can change output lengths and crop counts.
The receipt includes request and completion-token totals for each run.
Stages share one bounded client request window. In the pipelined runner, crops
receive available slots while independent full-page/detection requests continue.
Stage spans overlap; adding them does not produce elapsed time. Queue averages
include pipeline ramp-up and final drain, so mean running-request counts need not
equal the configured limit.

### Quality and the reference output contract

| Previous guarded merge, pipelined | Official overall (%) |
| --- | ---: |
| Single | 72.79 |
| Double | 73.28 |
| Triple | 73.48 |

Each full-run output shown here was freshly scored on all 2,078 pages with the
pinned official scorer
`9af4102e26b51f234ab5f037e19fec05c0696ec6`, with all 241 Python source hashes
verified and zero official scoring errors. Capped generations are included in scoring.

The pinned reference merge can retain an original Table/Chart block and an
overlapping crop alternative when their text differs. The chart evaluator searches
rendered tables for the best matching data. The previous guarded policy uses
replacement and rejects overlapping same-class crop additions; raw alternatives
remain in `stages.crops` for inspection.

A controlled replay of identical baseline triple responses scored 73.44
with the previous guarded merge and 75.19 with reference-style merging of
the same completed crops. The latter inserted 1,660 overlapping alternative blocks.
This identified the output contract as the cause of the score gap. Package
3.5.0.post5 restores alternatives as the default, keeping the faster scheduler.
Use the separately pinned reproduction pipeline for the exact headline 75.20
contract. The receipt includes category metrics and the merge-only replay checks.

## Accuracy restoration with the faster scheduler

Package 3.5.0.post5 defaults to `merge_policy="alternatives"`. The scheduler,
model settings, region selection and chart presentation defaults are unchanged.
The merge retains differing full-page/crop hypotheses as the reference does;
it adds no model calls. `merge_policy="guarded"` remains available explicitly.

Fresh model inference on all 2,078 pages with one H100, the same uni/FA3/MTP server
profile, and prepared inputs produced:

| Pipeline | Concurrency | Pages/s | Elapsed | Official overall (%) | Fully completed pages |
| --- | ---: | ---: | ---: | ---: | ---: |
| Double | 256 | 11.64 | 178.5 s | 74.92 | 2043/2078 |
| Triple | 128 | 10.61 | 195.8 s | 75.20 | 2038/2078 |

Timing includes crop preparation and merge/rendering. Preparation, startup, warmup
and serialization are excluded; the receipt also reports serialization-inclusive
and fully completed-page rates. These diagnostic runs explicitly used
`allow_partial=True`; token-limit cases remain marked incomplete.

The same saved responses from the earlier staged and pipelined runs were also
rescored with the restored merge. This isolates the merge from generation:

| Saved responses | Guarded overall (%) | Alternatives overall (%) |
| --- | ---: | ---: |
| Double Staged | 73.25 | 74.88 |
| Double Pipelined | 73.28 | 74.96 |
| Triple Staged | 73.51 | 75.23 |
| Triple Pipelined | 73.48 | 75.23 |

All six outputs were freshly scored on 2,078 unique pages with the pinned official
scorer and all 241 source hashes verified, with zero official scoring errors.
Batching at nonzero temperature can change individual responses; this does not
establish bit-identical generations or a guarantee for every document.

The reference-compatible score includes alternative tables/charts. The evaluator
can match the best alternative, so score recovery does not prove that a single
chosen transcription is equally accurate. The alternatives are present in the
actual returned document and its raw stages. Use the guarded policy for a more
compact document when that tradeoff fits the application.

See [the restoration receipt](../reference/validation/accuracy_restoration.json) for category
scores, generation coverage, exact settings, request/token counts, hashes and
controlled replay results.


## Inference throughput with prepared pages

For prediction throughput, use `result.metrics["inference_pages_per_second"]`
(package 3.5.0.post6 or later). Its wall clock runs from the first model request
start to the last model response across all passes. It includes server queueing,
image encoding inside the server, generation, HTTP transfer and any gaps waiting
for predicted-region selection, crop encoding or dispatch. It excludes initial
page preparation, startup/warmup, final merge/rendering after inference, and writes.
`pipeline_seconds` and `processed_pages_per_second` retain their earlier meanings,
including merge/rendering, for applications that need complete documents.
Concurrent rendering can still compete for CPU during inference; that observed
contention remains in the wall time. We do not subtract overlapping CPU time or
sum concurrent request latencies to claim a higher rate.

The fastest observed profiles compatible with the restored output quality are:

| Pipeline | Concurrency | Schedule | Prediction pages/s | Inference wall time | Fully completed pages |
| --- | ---: | --- | ---: | ---: | ---: |
| Single | 256 | Staged | **15.42** | 134.78 s | 2045/2078 |
| Double | 256 | Pipelined | **11.65** | 178.35 s | 2043/2078 |
| Triple | 128 | Pipelined | **10.62** | 195.70 s | 2038/2078 |

These use 2,078 unique prepared ParseBench page images on one H100 80GB and the
same uni/FA3/MTP serving profile. The single-pass measurement predates the merge
restoration; it has no crops and is unaffected by that merge change. Its saved
stage clock includes executor setup/teardown and is slightly conservative.
Double/triple times are reconstructed exactly from saved stage start/end spans,
including gaps between calls. These are existing measured runs, not a new GPU
run of the timing-only post6 release. See the [timing receipt](../reference/validation/inference_benchmarks.json).

The earlier guarded-merge runs reached 11.88/10.91 prediction pages/s for
double/triple, respectively, but had the lower scores documented above. Use the
restored profiles when comparing speed while preserving the reference output
contract. The restored double/triple scores are 74.92/75.20.

This is realistic batch prediction throughput when pages are prepared ahead of
time and enough work is queued. It is not PDF ingestion throughput or single-page
latency, and is not a measured hardware ceiling. Document complexity, generation
length, crop count, CPU capacity, network placement and batching affect speed.
The numerator includes token-limited pages; these diagnostic runs explicitly
allow partial output. Use `complete_inference_pages_per_second` for the number
of fully completed pages divided by the same wall time. Strict errors remain the
default outside these diagnostic runs.

```python
prepared = parser.prepare(page_images, workers=8)  # outside inference clock
result = parser.parse_prepared(
    prepared, mode="triple", concurrency=128, postprocess_workers=8,
)
print(result.metrics["inference_seconds"])
print(result.metrics["inference_pages_per_second"])
```

For double pass, use `mode="double", concurrency=256`. The measured fastest
single-pass profile uses `mode="single", concurrency=256, schedule="staged"`;
a single-pass pipelined run at concurrency 128 measured 14.92 prediction pages/s.
A pipelined single-pass run at concurrency 256 has not been measured here.
