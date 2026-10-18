## Explainability

Field | Response
:---- | :----
Intended Task/Domain: | Document understanding, OCR, layout parsing, table extraction, and text extraction with spatial grounding.
Model Type: | Transformer-based vision-encoder-decoder model.
Intended Users: | Developers and teams building document intelligence, retrieval-augmented generation (RAG), data-curation, extraction, and multimodal agent workflows.
Output: | Structured text containing document element classes, bounding boxes, reading-order information, chart/table annotations, and extracted text.
Describe how the model works: | Nemotron 3.5 Parse encodes a dynamically sized document image with C-RADIOv4-SO400M, compresses the visual features with a neck, and places them before the OCR prompt as a causal prefix to a 10-layer mBART decoder. The decoder uses grouped-query self-attention and produces structured document annotations with content-normalized boxes. The 72,505-token tokenizer includes multilingual, task-control, and chart-aware tokens such as `<class_Chart>`.
Name the adversely impacted groups this has been tested to deliver comparable outcomes regardless of: | Not Applicable
Technical Limitations & Mitigation: | Performance can vary for low-resolution scans, motion blur, handwriting, decorative fonts, dense tables, unusual layouts, unsupported languages or scripts, and documents with heavy compression artifacts. Users should evaluate outputs on representative documents and use human review for high-impact workflows.
Verified to have met prescribed NVIDIA quality standards: | Yes
Performance Metrics: | OCR accuracy, layout/class accuracy, table extraction quality, chart extraction quality, reading-order quality, grounding quality, latency, throughput, and qualitative visual inspection.
Potential Known Risks: | The model may miss text, hallucinate structure, assign incorrect classes, produce inaccurate bounding boxes, or incorrectly order elements. Downstream systems should treat output as model-generated extraction results and apply validation, confidence checks, and human review where appropriate.
Licensing: | Governing Terms: Your use of this model is governed by the [OpenMDW License Agreement, version 1.1](https://openmdw.ai/license/1-1/). Use of the tokenizer included in this model is governed by the [MIT license and tokenizer attribution](https://huggingface.co/nvidia/Nemotron-3.5-Parse/blob/main/TOKENIZER_ATTRIBUTION.md). See [third-party notices](https://huggingface.co/nvidia/Nemotron-3.5-Parse/blob/main/THIRD_PARTY_NOTICES.md) for separately installed dependencies.
