<div align="center">

<p align="center">
  <img src="assets/hero_banner.png" width="100%" alt="OmniEVIE-4B — Evidence-Vector-Informed Embedding for Multi-modal Retrieval" />
</p>

<p align="center">
  <a href="https://huggingface.co/tencent/OmniEVIE-4B"><img src="https://img.shields.io/badge/Hugging_Face-tencent%2FOmniEVIE--4B-F59E0B?style=flat-square&logo=huggingface&logoColor=white" alt="Hugging Face"></a>
  <a href="https://github.com/Tencent/OmniEVIE"><img src="https://img.shields.io/badge/GitHub-Tencent%2FOmniEVIE-1F2937?style=flat-square&logo=github&logoColor=white" alt="GitHub"></a>
  <a href="OmniEVIE_Technical_Report.pdf"><img src="https://img.shields.io/badge/Technical_Report-PDF-E11D48?style=flat-square&logo=adobeacrobatreader&logoColor=white" alt="Technical Report"></a>
  <a href="https://huggingface.co/spaces/TIGER-Lab/MMEB-Leaderboard"><img src="https://img.shields.io/badge/MMEB--Leaderboard-Top_1_(Non--Audio)-10B981?style=flat-square" alt="MMEB-Leaderboard Top 1 (Non-Audio)"></a>
</p>

<p align="center">
  <i>Evidence lives in the details — a single cell in a dense table, a fleeting gesture in a two-minute clip, a buried clause across pages.</i><br/>
  <i>One model. Every modality. Milliseconds at million scale.</i>
</p>

</div>

---

**OmniEVIE-4B** is a 4.5B-parameter unified multi-modal, multi-vector retrieval model by **Tencent IMA Product Center** and **Tencent Youtu Lab**, ranking **#1 on the [MMEB-Leaderboard](https://huggingface.co/spaces/TIGER-Lab/MMEB-Leaderboard) (excluding audio)**—with `OmniEVIE-4B (Full)` at **60.68** and `OmniEVIE-4B (Compressed)` at **60.06** across 190 tasks (also **#1** in both Text `52.97` and Agent `54.14`). Instead of flattening an entire page or video into one vector—or re-reading every recalled item with a heavy cross-encoder—it distills each document into at most **128 int8 vectors of dimension 64** (`≤ 9,472 bytes/record`, **8.82 GiB per 1M records**), retrieving at million scale in **54.2 ms** on a single CPU thread while tracing every hit straight back to the page region or video second where the answer lives.

For complete methodology and analysis, read the [**Technical Report (PDF)**](OmniEVIE_Technical_Report.pdf).

### MMEB-Leaderboard Top 1 (Excluding Audio)

<p align="center">
  <a href="https://huggingface.co/spaces/TIGER-Lab/MMEB-Leaderboard">
    <img src="assets/mmeb_leaderboard.png" width="96%" alt="MMEB-Leaderboard Top 1 (Excluding Audio) — OmniEVIE-4B"/>
  </a><br/>
  <sub><i>Official <a href="https://huggingface.co/spaces/TIGER-Lab/MMEB-Leaderboard">TIGER-Lab/MMEB-Leaderboard</a> snapshot (2026-11-24, sorted by <code>Audio-Overall = 0</code>). <b>OmniEVIE-4B (Full, 4.54B)</b> and <b>OmniEVIE-4B (Compressed, 4.54B)</b> rank <b>#1 and #2 among all non-audio models</b> (#2 and #4 overall across all 190 tasks), surpassing 9.4B baselines while leading both Text (52.97) and Agent (54.14) tracks.</i></sub>
</p>

---

## Seeing Where the Answer Lives

### Fine-Grained Page & Long-Video Localization

Every retrieval hit carries its own spatial or temporal coordinates. From the same compressed index, `argmax` over query tokens highlights the exact table row, cross-lingual answer sentence, chart bar, or timestamp span—without external OCR or video-captioning models.

<p align="center">
  <img src="assets/fig8_localization.png" width="96%" alt="Page Region and Long-Video Timestamp Localization Cases"/><br/>
  <sub><i>Real retrieval hits on ViDoRe V3 pages and a 150-second QVHighlights clip. Across 1,083 QVHighlights validation queries, the heat peak falls inside the labeled interval for <b>78.0%</b> of queries and the returned span intersects it for <b>94.3%</b> (vs. 44.9% random), covering 18% of video duration on average.</i></sub>
</p>

### Native Video Moment Localization

Video frames are encoded directly by the spatio-temporal backbone. Queries land straight on the target action across 150-second clips without converting video into text.

<p align="center">
  <img src="assets/fig9_video_cases.png" width="96%" alt="Direct Video Moment Localization Cases"/><br/>
  <sub><i>Returned intervals and peak timestamps on three 150-second QVHighlights videos directly from the compressed multi-vector index.</i></sub>
</p>

### Token-Level Alignment & Query Saliency Gate

Compressing a 966-patch document page into 128 `int8` clusters preserves crisp word-to-patch correspondence. The learned `QueryGate` up-weights discriminative terms while spherical noise-floor suppression (`θ = 0.38`) cleanly separates relevant pages from distractors.

<p align="center">
  <img src="assets/fig7_alignment.png" width="96%" alt="Token-Level Alignment and Query Saliency Gate"/><br/>
  <sub><i>Per-token cluster matches, learned saliency gate weights (τ = 0.6), and noise-floor margin on a 966-patch document compressed to 128 int8 clusters.</i></sub>
</p>

---

## A Compact Memory for Every Modality

| Feature | Specification |
|---|---|
| **Checkpoint** | `OmniEVIE-4B` (4.54B params, Qwen3.5 backbone with bidirectional full-attention layers) |
| **Modalities** | Text · Natural Image · Visual Document · Native Video · Agent / Tool / GUI / Memory |
| **Elastic Dimensions** | Single Prefix-MRL head supporting `{64, 128, 256, 512, 1024, 2048}` dimensions at runtime |
| **Index Footprint** | `≤ 128 × 64D int8` via ST-HAC — **8.82 GiB / 1M records** (down to 2.15 GiB at `K=32`) |
| **Search Latency** | **54.2 ms** (1M) / **120.2 ms** (5M) on a single CPU thread via three-stage search |
| **Evidence Localization** | Direct page bounding box & video timestamp interval from retrieval `argmax` |
| **License** | Apache-2.0 (`LICENSE.txt`) |

### Unified ST-HAC Compression & Three-Stage Funnel

Text windows, document pages, and video segments share one spatio-temporal guided Ward clustering pipeline (**ST-HAC**). Position codes guide grouping only; stored centroids retain pure semantics quantized at a single global scale (`1/127`). Each record exports three nested views—a `d=64` mean vector (256 B), `1-bit` signs (1,024 B), and `int8` multi-vectors (≤ 8,192 B)—for coarse, middle, and fine scoring.

<p align="center">
  <img src="assets/fig4_sthac.png" width="96%" alt="Unified ST-HAC Compression Pipeline"/><br/>
  <sub><i>Unified ST-HAC clustering, sphere-renormalized centroids, fixed-scale int8 quantization, and exact per-record byte layout.</i></sub>
</p>

<p align="center">
  <img src="assets/fig5_three_stage.png" width="96%" alt="Three-Stage Retrieval Funnel and Latency"/><br/>
  <sub><i>Three-stage retrieval funnel on 1M records (14.6 ms coarse + 19.7 ms Hamming + 19.9 ms int8 = 54.2 ms single-thread CPU).</i></sub>
</p>

| Input | Encoding & ST-HAC Pooling |
|---|---|
| **Text document** | 128-token sentence chunks, windows of 8 chunks, 1-D monotonic time-guided Ward pooling to `≤ 128` |
| **Image / Visual document** | Up to 4,096 visual tokens, 2-D spatial-guided Ward pooling to `≤ 128` |
| **Video (`deploy`)** | 16 frames/min (keyframes first), 60-second segments, spatio-temporal Ward pooling to `≤ 128` |
| **Video (`protocol="mmeb"`)** | 32 evenly spaced frames from 64 saved frames, single clip, up to 14,400 tokens |
| **Query** | All tokens kept; default scene instruction overridable via `instruction=` |

---

## Install

```bash
git clone https://github.com/Tencent/OmniEVIE.git
cd OmniEVIE
pip install -e ".[test]"   # core package and pytest
pip install -e ".[eval]"   # adds pyarrow for MMEB reproduction scripts
```

`flash-attn>=2.7.0` is required (`attn_implementation="flash_attention_2"`; verified with `torch 2.7.1`, `transformers 5.13–5.17`, `flash-attn 2.8.1`). Model weights are hosted at [**tencent/OmniEVIE-4B**](https://huggingface.co/tencent/OmniEVIE-4B).

---

## Quick Start

### Python API

`OmniEVIE.from_pretrained` and `QueryGate.from_pretrained` accept either `"tencent/OmniEVIE-4B"` or a local directory.

```python
from omnievie import OmniEVIE, QueryGate, ThreeStageIndex

model = OmniEVIE.from_pretrained("tencent/OmniEVIE-4B", device="cuda")
gate = QueryGate.from_pretrained("tencent/OmniEVIE-4B")

# 1. Encode and index documents across modalities
index = ThreeStageIndex()
for path in ["photos/fda_slide.png", "clips/news_segment.mp4", "notes/report.txt"]:
    modality, vectors = model.encode_document(path)
    index.add(path, vectors, modality)
index.save("index.pt")

# 2. Retrieve with three-stage index + learned query saliency gate
query = model.encode_query(text="Two TV show hosts sit on a red couch and discuss the news.", target="video")
weights = gate.weights(query.vectors, query.vision_mask, query.aug_mask, query.has_text)
hits = index.search(query.vectors, weights=weights, modality="video", topk=3)
print("search:", hits)

# 3. Direct evidence localization on a matched page
q_doc = model.encode_query(text="Did the FDA's 2018 Strategic Policy Roadmap eliminate clinical trials?", target="image")
w_doc = gate.weights(q_doc.vectors, q_doc.vision_mask, q_doc.aug_mask, q_doc.has_text)
page_loc = model.localize_image(q_doc, "photos/fda_slide.png", weights=w_doc)
print("top page region (x0, y0, x1, y1):", page_loc.top_box)
```

Example output:

```text
search: [('clips/news_segment.mp4', 41.827)]
top page region (x0, y0, x1, y1): (0.1429, 0.1304, 0.4524, 0.2174)
```

<p align="center">
  <img src="assets/quickstart_output.png" width="96%" alt="Quick Start Video Retrieval and Page Localization Output"/><br/>
  <sub><i>Visualized output of the Quick Start snippet: three-stage text-to-video retrieval on <code>clips/news_segment.mp4</code> (left) and normalized <code>top_box</code> evidence localization on <code>photos/fda_slide.png</code> (right).</i></sub>
</p>

### Command Line

```bash
omnievie --weights tencent/OmniEVIE-4B index index.pt photos/ clips/ notes/
omnievie --weights tencent/OmniEVIE-4B search index.pt --text "a dog catching a frisbee" --target video --top 3
```

Example output:

```text
image   128 vectors  photos/fda_slide.png
video   128 vectors  clips/news_segment.mp4
text     96 vectors  notes/report.txt
wrote 3 documents to index.pt

   41.827  clips/news_segment.mp4
```

> Every input runs in its own forward pass because padding alters the recurrent state of linear-attention layers.

---

## Evaluations & Benchmarks

<p align="center">
  <img src="assets/fig1_overview.png" width="96%" alt="OmniEVIE-4B Multi-Modal Accuracy and Retrieval Latency Overview"/><br/>
  <sub><i>(a) MMEB-V3 overall accuracy (190 tasks) across model scales; (b) single-thread CPU retrieval latency from 100K to 5M records.</i></sub>
</p>

### MMEB-V3 (190 Tasks)

| Model | All (190) | Text (53) | T-RR | T-IF | T-LC | T-MC | T-GR | Agent (47) | Tool | GUI | Memory | MCMR |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Qwen3-VL-Embedding-2B | 50.90 | 39.20 | 16.60 | 40.60 | 53.10 | 61.20 | 58.00 | 39.30 | 42.60 | 30.40 | 28.40 | 42.00 |
| Qwen3-VL-Embedding-8B | 53.50 | 42.50 | 18.20 | 44.80 | 58.00 | 61.20 | 61.20 | 38.40 | 41.30 | 33.50 | 22.80 | 38.00 |
| WeMM-Embedding-2B | 55.77 | 45.34 | 26.29 | 49.30 | 61.90 | 59.72 | 58.74 | 44.05 | 46.23 | 38.87 | 35.38 | 42.51 |
| WeMM-Embedding-4B | 57.97 | 47.88 | 30.01 | 52.02 | 62.43 | 60.14 | 61.09 | 48.06 | 50.58 | 41.44 | **39.19** | 41.91 |
| WeMM-Embedding-9B | 59.33 | 48.76 | **31.82** | 52.78 | 64.48 | 58.28 | 61.12 | 50.10 | 52.95 | **43.33** | 38.65 | 49.34 |
| **OmniEVIE-4B (`K128×d64 int8`, 8-fr)** | 59.76 | 51.77 | 26.36 | 69.65 | 70.71 | 67.75 | 63.58 | 54.03 | **58.84** | 41.34 | 37.35 | 47.39 |
| **OmniEVIE-4B (`K128×d64 int8`, 32-fr)** | 60.06 | 51.77 | 26.36 | 69.65 | 70.71 | 67.75 | 63.58 | 54.03 | **58.84** | 41.34 | 37.35 | 47.39 |
| **OmniEVIE-4B (Full Sequence `d=2048`)** | **60.68** | **52.97** | 27.46 | **70.81** | **73.04** | **68.55** | **64.60** | **54.14** | 58.81 | 42.00 | 37.60 | **49.74** |

### MMEB-V2 (78 Tasks)

| Model | All (78) | Image (36) | Video (18) | VisDoc (24) |
|---|---:|---:|---:|---:|
| Qwen3-VL-Embedding-2B | 73.25 | 74.96 | 61.87 | 79.22 |
| Qwen3-VL-Embedding-8B | 77.82 | 80.12 | 67.15 | 82.36 |
| WeMM-Embedding-2B | 77.94 | 79.63 | 70.82 | 80.75 |
| WeMM-Embedding-4B | 79.19 | 80.84 | 72.11 | 82.04 |
| WeMM-Embedding-9B | **80.58** | **81.87** | **74.31** | 83.34 |
| **OmniEVIE-4B (`K128×d64 int8`, 8-fr)** | 77.24 | 78.09 | 66.49 | 84.02 |
| **OmniEVIE-4B (`K128×d64 int8`, 32-fr)** | 77.96 | 78.09 | 69.62 | 84.02 |
| **OmniEVIE-4B (Full Sequence `d=2048`)** | 78.56 | 78.70 | 70.08 | **84.70** |

### ViDoRe V3 Visual Document Retrieval (8 Domains × 6 Languages, graded nDCG@10)

| Model | Index Representation | Mean | CS | Energy | Fin (EN) | Fin (FR) | HR | Industrial | Pharma | Physics |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Nemotron-ColEmbed-V2-8B | Full multi-vector | 63.76 | 79.35 | 70.05 | 67.72 | 51.50 | **66.92** | 56.81 | 67.39 | 50.31 |
| Qwen3-VL-Embedding-8B | Single-vector | 59.00 | 75.86 | 64.47 | 60.88 | 44.70 | 58.88 | 47.78 | 66.05 | 48.31 |
| **OmniEVIE-4B (Full Sequence `d=2048`)** | Prefix-MRL upper bound | **64.34** | **79.89** | **71.25** | **67.76** | **53.45** | 66.33 | **57.03** | **68.11** | **50.87** |
| **OmniEVIE-4B (`K128×d64 int8`)** | 7.87 GiB / 1M pages | 62.96 | 78.73 | 69.94 | 66.01 | 52.52 | 64.68 | 55.08 | 66.47 | 50.28 |
| **OmniEVIE-4B (`K32×d64 int8`)** | 2.15 GiB / 1M pages | 61.16 | 78.13 | 68.61 | 64.52 | 49.43 | 60.90 | 51.73 | 65.73 | 50.22 |

### Single-Thread CPU Retrieval Latency (ms)

| Method | 100K | 1M | 5M | Speedup vs. Full `int8` (1M) |
|---|---:|---:|---:|---:|
| Full `int8` MaxSim | 1,657 | 12,781 | 63,892 | 1.0× |
| Exact Single-Vector (`d=4096`) | 60.9 | 604.0 | 3,039 | 21.2× |
| Exact Single-Vector (`d=2048`) | 34.6 | 331.0 | 1,666 | 38.6× |
| **OmniEVIE-4B Three-Stage (`N1=5000, N2=1000`)** | **41.9** | **54.2** | **120.2** | **236×** |

---

## Reproducing MMEB

MMEB data is not included in this repository.

```bash
python scripts/reproduce_mmeb.py --weights tencent/OmniEVIE-4B \
    --parquet MMEB/image-query/CIRR/test-00000-of-00001.parquet \
    --image-root MMEB/image-tasks/MMEB --task CIRR --scoring maxsim --out results/CIRR.json

python scripts/reproduce_mmeb_video.py --weights tencent/OmniEVIE-4B \
    --manifest manifests/MSR-VTT.parquet \
    --frame-root frames/MSR-VTT --direction t2v --task MSR-VTT --scoring maxsim --out results/MSR-VTT.json
```

`--scoring maxsim` runs exact MaxSim over int8 candidate vectors; `--scoring index` (default) uses `ThreeStageIndex` with `QueryGate`. The video script also supports `--labels`, `--cache DIR`, and `--shard K/N`.

| Task | Recorded | `maxsim` | `index` |
|---|---:|---:|---:|
| CIRR | 0.751 | 0.741 | 0.745 |
| MSCOCO_t2i | 0.809 | 0.809 | 0.810 |
| VisDial | 0.900 | 0.911 | 0.901 |
| MSR-VTT | 0.579 | 0.588 | 0.583 |
| DiDeMo | 0.786 | 0.785 | 0.784 |
| MSVD | 0.785 | 0.782 | 0.781 |
| VATEX | 0.588 | 0.595 | — |
| YouCook2 | 0.454 | 0.454 | — |
| UCF101 | 0.942 | 0.942 | 0.944 |
| HMDB51 | 0.850 | 0.845 | 0.852 |
| K700 | 0.727 | 0.724 | — |
| Breakfast | 0.670 | 0.670 | 0.660 |
| SmthSmthV2 | 0.895 | 0.892 | 0.897 |

## Tests

```bash
python -m pytest tests -q
```

---

## Citation

```bibtex
@article{wang2026omnievie,
  title   = {OmniEVIE: Evidence-Vector-Informed Embedding for Multi-modal Retrieval},
  author  = {Wang, Zifei and Wen, Wei and Ji, Qiang and Zhang, Qian-Wen and Qiao, Ruizhi and Liu, He and Sun, Xing and Lin, Qiang},
  year    = {2026},
  url     = {https://github.com/Tencent/OmniEVIE}
}
```

## License

The code and models released under OmniEVIE, including OmniEVIE, OmniEVIE-2B, and OmniEVIE-4B, are licensed under the **Apache License 2.0**. See [`LICENSE.txt`](LICENSE.txt) and [`NOTICE`](NOTICE) for details and third-party notices.

## Contact

- **Zifei Wang**: zifeiwang@tencent.com
- **Wei Wen**: jawnrwen@tencent.com
