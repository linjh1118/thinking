---
license: mit
base_model: BAAI/bge-m3
library_name: sentence-transformers
pipeline_tag: sentence-similarity
datasets:
- amazon/poiss
widget:
- example_title: POI retrieval (Rome)
  source_sentence: "User Query: pizzeria near the colosseum; Coordinate: 41.8902N 12.4922E;"
  sentences:
  - "Location Name: Pizzeria Da Enzo; Address: Via dei Fori Imperiali 1; Position: Rome, Lazio, IT, 00184; Coordinate: 41.8925N 12.4853E; Categories: pizza restaurant;"
  - "Location Name: Trattoria Luzzi; Address: Via di San Giovanni in Laterano 88; Position: Rome, Lazio, IT, 00184; Coordinate: 41.8886N 12.4949E; Categories: italian restaurant;"
  - "Location Name: Oslo Dental Clinic; Address: Storgata 10; Position: Oslo, Oslo, NO, 0155; Coordinate: 59.9139N 10.7522E; Categories: dentist;"
- example_title: Same query, far from the user
  source_sentence: "User Query: hotel caribe; Coordinate: 21.0062N 89.5510W;"
  sentences:
  - "Location Name: Hotel Caribe; Address: Calle 59 195; Position: Mérida, Yucatán, MX, 97000; Coordinate: 20.9674N 89.6237W; Categories: hotel;"
  - "Location Name: Caribe Insurance Agency; Address: 1200 Ponce de Leon; Position: San Juan, PR, 00907; Coordinate: 18.4550N 66.0772W; Categories: insurance agency;"
language:
- en
- es
- fr
- pt
- de
- it
- nl
tags:
- sentence-transformers
- sentence-similarity
- feature-extraction
- dense-retrieval
- bi-encoder
- point-of-interest
- poi-search
- geospatial
- multilingual
---

# POISS BGE-M3 retriever

`BAAI/bge-m3` fine-tuned on [POISS](https://huggingface.co/datasets/amazon/poiss) for
point-of-interest retrieval over the full Overture Maps Places corpus (72M+ POIs). It is a
bi-encoder: queries and POIs are encoded independently, so POI embeddings can be built offline
and searched with an ANN index.

The distinguishing feature of this task is that a query carries **the coordinate it was issued
from**, and relevance depends jointly on semantics and geography. The coordinate is given to
the model as text, at four-decimal precision, in both the query and the POI representation.

Companion cross-encoder: [`amazon/poiss-bge-m3-reranker`](https://huggingface.co/amazon/poiss-bge-m3-reranker).

## Results

Full-corpus retrieval on the POISS test split (42,018 queries, percentages):

| System | R@10 | R@100 | R@1k | N@5 | N@20 |
|---|---|---|---|---|---|
| BM25 | 17.8 | 29.9 | 42.8 | 16.0 | 18.0 |
| BGE-M3 zero-shot | 15.2 | 26.4 | 40.0 | 13.7 | 15.3 |
| **this model** | **45.2** | **83.2** | **95.6** | **58.3** | **60.3** |

Per-language R@100: EN 82.4, ES 83.9, FR 85.1, PT 80.5, DE 86.1, IT 84.7, NL 79.8.
Fine-tuning shrinks the cross-language spread from 2.2× to 1.08×.

Per-intent R@100: `Search` 89.1, `Detail` 88.0, `Recommend` 77.3, `Things-to-do` 74.0.
Open-ended intents remain the harder half of the benchmark.

Used as a reranker over its own top-1000 (the setting the cross-encoder is compared against):
P@5 57.6, P@20 35.5, MRR 85.5, nDCG@5 61.5, nDCG@20 62.6.

## Usage

Embeddings are the **CLS token of the last layer**, L2-normalized; score with a dot product.
Both sides must follow the templates below, including the coordinate formatting, or accuracy
drops sharply.

With `sentence-transformers`, pooling and normalization are already configured:

```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("amazon/poiss-bge-m3-retriever")
query = "User Query: pizzeria near the colosseum; Coordinate: 41.8902N 12.4922E;"
pois = [
    "Location Name: Pizzeria Da Enzo; Address: Via dei Fori Imperiali 1; Position: Rome, "
    "Lazio, IT, 00184; Coordinate: 41.8925N 12.4853E; Categories: pizza restaurant, restaurant;",
    "Location Name: Oslo Dental Clinic; Address: Storgata 10; "
    "Position: Oslo, Oslo, NO, 0155; Coordinate: 59.9139N 10.7522E; Categories: dentist;",
]
print(model.similarity(model.encode([query]), model.encode(pois)))
```

Or with `transformers` directly, which is what the formatting helpers below are for:

```python
import torch
from transformers import AutoModel, AutoTokenizer

model_id = "amazon/poiss-bge-m3-retriever"
tokenizer = AutoTokenizer.from_pretrained(model_id)
# add_pooling_layer=False: the checkpoint has no pooler, and pooled output is unused
model = AutoModel.from_pretrained(model_id, add_pooling_layer=False).eval()


def encode(texts, max_length):
    batch = tokenizer(texts, padding=True, truncation=True,
                      max_length=max_length, return_tensors="pt")
    with torch.no_grad():
        hidden = model(**batch).last_hidden_state[:, 0, :]
    return torch.nn.functional.normalize(hidden, dim=1)


def format_query(text, lat, lng):
    lat_dir, lng_dir = "N" if lat >= 0 else "S", "E" if lng >= 0 else "W"
    return (f"User Query: {text}; "
            f"Coordinate: {abs(lat):.4f}{lat_dir} {abs(lng):.4f}{lng_dir};").strip()


def format_poi(name, street, city, state, country, postcode, lat, lng, categories):
    parts = ["Location "]
    if name:
        parts.append(f"Name: {name}; ")
    if street:
        parts.append(f"Address: {street}; ")
    position = [v for v in (city, state, country, postcode) if v]
    parts.append("Position: " + ", ".join(position) + "; ")
    lat_dir, lng_dir = "N" if lat >= 0 else "S", "E" if lng >= 0 else "W"
    parts.append(f"Coordinate: {abs(lat):.4f}{lat_dir} {abs(lng):.4f}{lng_dir}; ")
    if categories:
        parts.append(f"Categories: {categories}; ")
    return "".join(parts).strip()


query = format_query("pizzeria near the colosseum", 41.8902, 12.4922)
pois = [
    format_poi("Pizzeria Da Enzo", "Via dei Fori Imperiali 1", "Rome", "Lazio", "IT",
               "00184", 41.8925, 12.4853, "pizza restaurant, restaurant"),
    format_poi("Oslo Dental Clinic", "Storgata 10", "Oslo", "Oslo", "NO",
               "0155", 59.9139, 10.7522, "dentist"),
]

query_vec = encode([query], max_length=128)
poi_vecs = encode(pois, max_length=160)
print((query_vec @ poi_vecs.T).squeeze(0))
```

Notes on the templates:

- `Categories` is the Overture primary category followed by the alternates, comma-separated,
  with underscores and slashes replaced by spaces.
- Truncation lengths at training and evaluation time were 128 tokens for queries and 160 for
  POIs.
- Strip the final string. Training inputs were stripped, so a trailing space after the last
  `;` adds a token and shifts the embedding. `sentence-transformers` strips for you; with plain
  `transformers` do it yourself, as the helpers above do.
- No rating, review-count or quality signal appears in either input: this model is purely
  semantic + geographic. The cross-encoder is the component that consumes the quality score.

For corpus-scale use, embed POIs offline and index them (the paper used FAISS).

## Training

Fine-tuned from `BAAI/bge-m3` on the POISS train split: 254,089 training records and 13,374
validation records, with POI content resolved from Overture Places release `2026-03-18`.

| | |
|---|---|
| Objective | InfoNCE with in-batch negatives, learnable temperature initialized at 0.01 |
| Hard negatives | 100 mined per query, 4 sampled per step |
| Optimizer | AdamW, lr 2e-5, linear schedule, gradient clipping 1.0 |
| Batch size | 16 per GPU × 8 GPUs |
| Precision / hardware | bf16 mixed precision, 8× NVIDIA A100 40GB |
| Schedule | up to 20 epochs, early stopping on validation MRR |
| Selected checkpoint | epoch 19, validation MRR 0.8828 |

Negatives are mined by taking the candidates the LLM judge marked non-relevant and padding
from the cross-encoder's reranked top-300 starting at rank 30 — semantically related POIs that
are nonetheless wrong, typically differing in quality score, distance or prominence.

Training supervision is derived from POISS labels: positives are the graded `relevant` POIs.

## Reproducibility note

The published weights are numerically identical to the ones used for the paper: they were
converted from the training checkpoint by re-expressing a fused-QKV flash-attention layout in
the standard `XLMRobertaModel` layout, and the conversion round-trips bit-exactly through the
original remapping function.

Metrics reproduce to about 1e-3 rather than exactly, because the reported numbers were computed
in bf16 with flash attention. Near-tied candidates around rank 20 can swap order across
precisions, which moves nDCG@20 slightly while leaving the top of the ranking unchanged.

## Intended use and limitations

Intended for research on POI search and geospatial retrieval. Coverage is limited to 7 languages
concentrated in the Americas and Europe, so behaviour outside those locales is untested.

## Citation

```bibtex
@inproceedings{maritan-etal-2026-poiss,
    title = "{POISS}: A Large-Scale Multilingual Dataset for Point-of-Interest Search",
    author = "Maritan, Nicola  and
      Moschitti, Alessandro  and
      Borazio, Federico  and
      Zhou, Xiaokun  and
      Bai, Zhengwei",
    booktitle = "Proceedings of the 2026 Conference on Empirical Methods in Natural Language Processing",
    month = oct,
    year = "2026",
    address = "Budapest, Hungary",
    publisher = "Association for Computational Linguistics",
    note = "To appear",
}
```

## License

These weights are a derivative work of [BAAI/bge-m3](https://huggingface.co/BAAI/bge-m3),
distributed by BAAI under the **MIT License**, and are released under the same license; see
`LICENSE`. The base model derives from XLM-RoBERTa, also MIT.

Modification with respect to the base model: all weights were modified by supervised
fine-tuning on the POISS train split with an InfoNCE objective. Architecture, configuration,
vocabulary and tokenizer are unchanged.

The training data, [POISS](https://huggingface.co/datasets/amazon/poiss), is Apache-2.0 and
places no additional restriction on these weights.
