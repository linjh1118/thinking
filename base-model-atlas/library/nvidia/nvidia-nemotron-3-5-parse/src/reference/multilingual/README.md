# Multilingual OCR evaluation

MOSCAR uses simple synthetic renderings of text in each language to test basic OCR capability. These results do not guarantee accuracy on complex scanned documents, handwriting, degraded images, or other real-world variations. Character bag F1 measures character overlap without considering character order.

These results compare the published [Nemotron Parse 2.0](https://huggingface.co/nvidia/NVIDIA-Nemotron-Parse-2.0) and [Nemotron 3.5 Parse](https://huggingface.co/nvidia/Nemotron-3.5-Parse) weights on identical evaluation pages.

* [MOSCAR: all 163 language/script entries](moscar_by_language.md)
* [MOSCAR per-language CSV](moscar_by_language.csv)
* [MOSCAR per-script CSV](moscar_by_script.csv)
* [IndicVisionBench per-language CSV](indicvision_by_language.csv)
* [Full-precision metrics and provenance](results.json)

## Evaluation settings

MOSCAR uses 8,111 held-out synthetic document pages, with 45–50 pages per language/script entry. The 163 entries represent 162 distinct language codes; Simplified and Traditional Chinese are separate entries. IndicVisionBench OCR uses 876 test pages across 10 languages.

Both models use one pass with temperature 0, top-k 1, repetition penalty 1.1, and an output limit of 8,744 tokens. Each model uses its documented default task prompt: Parse 2.0 uses `</s><s><predict_bbox><predict_classes><output_markdown><predict_no_text_in_pic>`, and Parse 3.5 uses `</s><s><predict_bbox><predict_classes><output_markdown><predict_text_in_pic>`. A full shared-prompt control, using `predict_text_in_pic` for both models, is also recorded in the results JSON. Model-specific image preprocessing is preserved. Parse 2.0 boxes are mapped back using its published `transform_bbox_to_original` helper; Parse 3.5 boxes are scaled from content-normalized coordinates. The same frozen benchmark scorer is used for both models. No ParseBench multi-pass merging or postprocessing is applied to these OCR evaluations. All pages, including outputs reaching the token limit, remain in the results.

MOSCAR CER divides the total character edit distance by the total reference character count after Unicode NFKC normalization, whitespace normalization, and case folding. Script and overall CER are recomputed from those totals. Character bag F1 ignores character order and averages the per-page F1 scores. The CSV localization recall uses a bounding-box IoU threshold of 0.5; matched class accuracy is computed only on localized blocks. IndicVisionBench uses the benchmark adapter's character/word ANLS and corpus CER/WER with whitespace and parsing/semantic-markup normalization. ANLS averages pages; CER and WER aggregate edit and reference counts. Metrics are percentages in the tables and CSV files. CER and WER include insertion errors and are not clipped at 100%. CER and WER are lower-is-better; ANLS and character bag F1 are higher-is-better.

The [results JSON](results.json) records evaluated model revisions, model-weight digests, input/label manifest hashes, prediction digests, coverage, token-limit counts, and the scoring snapshot digest. These identify the evaluated artifacts without requiring internal filesystem paths.
