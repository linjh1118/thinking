# 官方原表转录

来源：https://arxiv.org/html/2611.32203v1

原始多层表头和跨列布局以同目录HTML为准；此处保留全部单元格，不把空值补为零。

## Table 1: Serving comparison of four multimodal retrieval designs.

|  | Single vector | Single vector + reranker | Full multi-vector | OmniEVIE |
| --- | --- | --- | --- | --- |
| Score | One inner product | Coarse score, then cross-attention | Full-token MaxSim | Fixed multi-vector, K ≤ 128 K\leq 128 , d = 64 d=64 |
| Local hit | None | No coordinates | Per-token hit | Page rectangle and video seconds; span hit 94.3 % 94.3\% |
| Million-scale index | A few GiB of vectors | Must read raw media for reranking | Hundreds of GiB | 7.87 7.87 – 8.82 8.82 GiB |
| Online forwards | Encode the query once | One query encode plus k k media forwards | Encode the query once | Encode the query once |
| Bottleneck | Dimension of one vector | Rerank tail latency | Index size and full scan | Integer and bit operations |
| Width | One trained width, or a separate MRL head | Reranker maintained apart from the retriever | Fixed high dimension | One Prefix-MRL head, six widths, ST-HAC at training time |

## Table 2: Scene instructions and query layout.

| Scene | Query | Instruction | Candidate |
| --- | --- | --- | --- |
| Image to image | Instruction + image, empty text | Find an image of the same object or entity | Image |
| Composed image-text | Instruction + image + question | Find an image that answers the question about the given image | Image |
| Text to image or page | Instruction + query text | Retrieve the image or page the request names | Image or page |
| Text to video | Instruction + query text | Retrieve the video the request names; the instruction is prepended | Native video |
| Other zero-shot tasks | Task instruction + query | One shared task prefix | Text, image, or video |

## Table 3: Three-grade evidence check on the visual-document pool. Counts are candidate negatives before the grade is applied.

| Grade | Meaning | Treatment |
| --- | --- | --- |
| Full evidence | The candidate answers the query | Promoted to a positive. Of 775,635 775{,}635 queries, 175,137 175{,}137 gain an extra positive. |
| Partial evidence | A useful clue, not a full answer | Masked in the denominator. Together with full evidence, 223,877 / 1,551,270 223{,}877/1{,}551{,}270 ( 14.4 % 14.4\% ) of candidate negatives are masked. |
| No evidence | Irrelevant or contradictory | Kept. 1,327,393 1{,}327{,}393 hard negatives remain. |

## Table 4: Five-way sample policy. “First” means the positive is ranked first. Distillation is on only when the teacher is correct.

| Class | Baseline | Teacher | Keep rule | Hard negatives |
| --- | --- | --- | --- | --- |
| 1, easy agreement | First, large margin | Correct | Fixed downsample; class tasks keep a per-class floor | Baseline picks plus the original set |
| 1b, borderline | First, small margin | Correct | Keep all | Same as class 1 |
| 2, teacher fills a gap | Not first | Correct | Upweight | Same as class 1 |
| 3, baseline ahead | First | Wrong | Keep all, gold label only | Original set only |
| 4, hard | Not first | Wrong | Keep all, gold label only | Original set only |

## Table 5: The four training stages and what each stage replays.

| Stage | Input | Supervision | Replay |
| --- | --- | --- | --- |
| 1, documents | Bidirectional document vectors and the six Prefix-MRL widths | Listwise distillation from EVIE-8B, the three-grade check, joint training of the six widths | Document pool for later stages |
| 2, image and video | Image-to-image, composed image-text, text-to-image, native video | Scene instructions, temporal hard negatives, a one-way ranking constraint, ST-HAC on the candidates in the batch | Document and earlier data at a fixed rate; one batch is one task |
| 3, all tasks | Classification, question answering, grounding, long text, tools, interfaces, memory | The five-way sampler, three teachers by task, a projection bridge to the high-width teacher | Replay quotas kept; batches stay single-task |
| 4, merge and query score | Specialists added back; the query-side score is trained | Block-wise merge and the gate with the noise floor | Deltas added on the blocks they were trained on |

## Table 6: Candidate representation, operator, and bytes of the three stages. K ′ K^{\prime} is the number of stored centroids, at most 128 128 .

| Stage | Representation | Operator | Window | Bytes |
| --- | --- | --- | --- | --- |
| S1 | μ avg = L2 ⁡ ( 1 K ′ ​ ∑ k μ k ) \mu_{\mathrm{avg}}=\operatorname{L2}(\frac{1}{K^{\prime}}\sum_{k}\mu_{k}) | Exact inner product or ANN | N db → N 1 N_{\mathrm{db}}\to N_{1} | 256 256 |
| S2 | sign ⁡ ( μ k ) \operatorname{sign}(\mu_{k}) | Hamming MaxSim, XOR and popcount | N 1 → N 2 N_{1}\to N_{2} | 1,024 1{,}024 |
| S3 | Fixed-scale int8 μ ^ k \hat{\mu}_{k} | Int8 MaxSim, plus equation 9 | N 2 → top ​ - ​ k N_{2}\to\mathrm{top}\text{-}k | 8,192 8{,}192 |

## Table 7: Deployment properties of three multi-vector retrieval designs.

|  | PLAID | MUVERA | OmniEVIE |
| --- | --- | --- | --- |
| Index | Global codebook and residual postings | One high-dimensional FDE vector | Mean, 1 1 -bit signs, and int8 centroids on the record |
| Updates | Codebook is rebuilt when the corpus shifts | Fixed random hyperplanes | Append an independently encoded record |
| Filters | Scalar filters inside the postings | Filters of a single-vector engine | Restrict the S1 candidate set |
| Local hit | Centroid map, residuals must be decoded | Dropped by the projection | Kept, from the S3 argmax |
| Engine | Inverted index and residual decode | High-dimensional MIPS | Inner product, popcount, int8 dot product |

## Table 8: MMEB-V3 over 190 tasks. All is the unweighted mean in Appendix B . Text reports nDCG@5; other groups report Hit@1. The 8-frame row changes only the video frame cap. Bold marks the best value in the column.

| Model | All | Text | T-RR | T-IF | T-LC | T-MC | T-GR | Agent | Tool | GUI | Mem. | MCMR |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Tasks | 190 | 53 | 20 | 9 | 6 | 5 | 13 | 47 | 35 | 8 | 4 | 1 |
| Qwen3-VL-Emb-2B | 50.9 | 39.2 | 16.6 | 40.6 | 53.1 | 61.2 | 58.0 | 39.3 | 42.6 | 30.4 | 28.4 | 42.0 |
| Qwen3-VL-Emb-8B | 53.5 | 42.5 | 18.2 | 44.8 | 58.0 | 61.2 | 61.2 | 38.4 | 41.3 | 33.5 | 22.8 | 38.0 |
| WeMM-Emb-2B | 55.77 | 45.34 | 26.29 | 49.30 | 61.90 | 59.72 | 58.74 | 44.05 | 46.23 | 38.87 | 35.38 | 42.51 |
| WeMM-Emb-4B | 57.97 | 47.88 | 30.01 | 52.02 | 62.43 | 60.14 | 61.09 | 48.06 | 50.58 | 41.44 | 39.19 | 41.91 |
| WeMM-Emb-9B | 59.33 | 48.76 | 31.82 | 52.78 | 64.48 | 58.28 | 61.12 | 50.10 | 52.95 | 43.33 | 38.65 | 49.34 |
| OmniEVIE-4B | 60.06 | 51.77 | 26.36 | 69.65 | 70.71 | 67.75 | 63.58 | 54.03 | 58.84 | 41.34 | 37.35 | 47.39 |
| OmniEVIE-4B, 8 frames | 59.76 | 51.77 | 26.36 | 69.65 | 70.71 | 67.75 | 63.58 | 54.03 | 58.84 | 41.34 | 37.35 | 47.39 |
| OmniEVIE-4B, full sequence d = 2048 d=2048 | 60.68 | 52.97 | 27.46 | 70.81 | 73.04 | 68.55 | 64.60 | 54.14 | 58.81 | 42.00 | 37.60 | 49.74 |

## Table 9: MMEB-V2 over 78 tasks. All is the unweighted mean. Image and video report Hit@1; visual documents report nDCG@5. WeMM-Emb-4B uses the same 4.5 4.5 B backbone as OmniEVIE. Bold marks the best value in the column.

| Model | All | Image | Video | VisDoc |
| --- | --- | --- | --- | --- |
| Tasks | 78 | 36 | 18 | 24 |
| Qwen3-VL-Emb-2B | 73.25 | 74.96 | 61.87 | 79.22 |
| Qwen3-VL-Emb-8B | 77.82 | 80.12 | 67.15 | 82.36 |
| WeMM-Emb-2B | 77.94 | 79.63 | 70.82 | 80.75 |
| WeMM-Emb-4B | 79.19 | 80.84 | 72.11 | 82.04 |
| WeMM-Emb-9B | 80.58 | 81.87 | 74.31 | 83.34 |
| OmniEVIE-4B | 77.96 | 78.09 | 69.62 | 84.02 |
| OmniEVIE-4B, 8 frames | 77.24 | 78.09 | 66.49 | 84.02 |
| OmniEVIE-4B, full sequence d = 2048 d=2048 | 78.56 | 78.70 | 70.08 | 84.70 |

## Table 10: ViDoRe V3 graded nDCG@10, macro-averaged over eight domains and six languages. Storage is GiB per million pages for the compressed rows. Bold marks the best value in the column.

| Model | Index | Avg | Comp. | Energy | Fin-EN | Fin-FR | HR | Ind. | Med. | Phys. |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Nemotron-ColEmbed-V2-8B | Full multi-vector | 63.76 | 79.35 | 70.05 | 67.72 | 51.50 | 66.92 | 56.81 | 67.39 | 50.31 |
| Qwen3-VL-Emb-8B | Single vector | 59.00 | 75.86 | 64.47 | 60.88 | 44.70 | 58.88 | 47.78 | 66.05 | 48.31 |
| OmniEVIE-4B, d = 2048 d=2048 | Prefix-MRL, full sequence | 64.34 | 79.89 | 71.25 | 67.76 | 53.45 | 66.33 | 57.03 | 68.11 | 50.87 |
| OmniEVIE-4B, K ​ 128 × d ​ 64 K128\times d64 | 7.87 7.87 GiB/M | 62.96 | 78.73 | 69.94 | 66.01 | 52.52 | 64.68 | 55.08 | 66.47 | 50.28 |
| OmniEVIE-4B, K ​ 32 × d ​ 64 K32\times d64 | 2.15 2.15 GiB/M | 61.16 | 78.13 | 68.61 | 64.52 | 49.43 | 60.90 | 51.73 | 65.73 | 50.22 |

## Table 11: Fine-grained image Top-1, video nDCG@10, and forward-versus-reversed accuracy. The four-set mean is MSR-VTT, MSVD, DiDeMo, and VATEX. Bold marks the best value in the column.

| Model | FORB | S2S | MFashion | MSR | MSVD | DiDeMo | VATEX | Vid-4 | Order |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Qwen3-VL-Emb-8B | 92.80 | 62.90 | 65.10 | 71.95 | 77.84 | 74.54 | 76.60 | 75.23 | 51.63 |
| Frame-independent | – | – | – | 63.76 | 73.11 | 78.30 | 69.37 | 71.13 | 51.17 |
| OmniEVIE-4B | 89.94 | 72.16 | 75.98 | 72.38 | 78.89 | 87.54 | 76.14 | 78.74 | 75.63 |

## Table 12: Stage, query-side, and merge ablations on MMEB-V3. M cells are written as before → \to after. T1 video uses 8 frames.

| ID | Variant | V3 | Image | Video | VisDoc | Text | Agent |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T1 | End of stage 2 | 44.38 | 39.33 | 45.17 | 83.59 | 45.74 | 36.73 |
| T2 | End of stage 3 | 58.14 | 75.67 | 67.25 | 82.71 | 50.77 | 50.85 |
| T3 | Final model | 60.06 | 78.09 | 69.62 | 84.02 | 51.77 | 54.03 |
| Q1 | Gate only | 59.85 | 78.02 | 69.65 | 83.87 | 51.71 | 53.35 |
| Q2 | Uniform MaxSim | 59.71 | 78.04 | 69.37 | 83.80 | 51.64 | 52.99 |
| M1 | One variant → \to linear average | 58.37 → \to 58.80 | 76.34 → \to 76.97 | 67.90 → \to 67.81 | 82.93 → \to 83.25 | 50.96 → \to 51.27 | 50.65 → \to 51.41 |
| M2 | One round → \to cross-round | 59.16 → \to 59.29 | 77.15 → \to 77.59 | 68.74 → \to 68.76 | 83.69 → \to 83.83 | 51.24 → \to 51.30 | 52.25 → \to 52.31 |
| M3 | Trunk → \to four specialists | 59.44 → \to 59.67 | 77.84 → \to 78.11 | 68.95 → \to 69.31 | 83.98 → \to 83.66 | 51.48 → \to 51.67 | 52.34 → \to 52.83 |
| M4 | Shared coefficient → \to per block | 59.60 → \to 59.66 | 77.95 → \to 77.98 | 69.24 → \to 69.36 | 83.84 → \to 83.62 | 51.56 → \to 51.65 | 52.72 → \to 52.94 |

## Table 13: Compression at K = 128 K=128 , d = 64 d=64 , scored by ViDoRe V3 nDCG@10. Indexing time is single-thread milliseconds per page.

| Method | Training | nDCG@10 | ms / rec. |
| --- | --- | --- | --- |
| Full sequence | – | 63.09 | – |
| Uniform grid pool | At indexing | 56.50 | 2.3 |
| Keep K K random tokens | At indexing | 60.41 | 0.1 |
| ST-HAC | With training | 62.96 | 20.0 |
| ST-HAC, w s = 0 w_{s}=0 | With training | 62.90 | 20.1 |
| ST-HAC, raw mean | With training | 63.00 | 20.0 |

## Table 14: Business-scenario retrieval, Top-1, averaged within each scenario. Scenario names are generalized. Bold marks the best value in the row.

| Scenario | Qwen3-VL-Emb-8B | WeMM-Emb-9B | OmniEVIE-4B |
| --- | --- | --- | --- |
| Text to image (mean) | 54.6 | 61.2 | 64.2 |
| Image to image (mean) | 93.4 | 94.1 | 96.5 |
| Image-text (mean) | 81.2 | 84.1 | 90.4 |
| Finance, text to image | 76.3 | 66.4 | 76.3 |
| Industry, text to image | 61.8 | 70.9 | 81.8 |
| Museums, text to image | 53.2 | 67.5 | 79.2 |
| Landmarks, image to image | 78.6 | 81.4 | 92.9 |
| Automotive, image-text | 86.4 | 90.9 | 100.0 |

## Table 15: Prefix-MRL width and ST-HAC budget on ViDoRe V3. Bytes include the mean vector where ST-HAC stores one. Storage is per million records.

| Setting | ( K , d ) (K,d) | Bytes / rec. | GiB / M | ViDoRe V3 |
| --- | --- | --- | --- | --- |
| Prefix-MRL, full | seq. × 2048 \times 2048 | 4,106,184 4{,}106{,}184 | 3,824 3{,}824 | 64.34 |
| Prefix-MRL, full | seq. × 512 \times 512 | 1,026,546 1{,}026{,}546 | 956 956 | 64.12 |
| Prefix-MRL, full | seq. × 128 \times 128 | 256,636 256{,}636 | 239 239 | 63.55 |
| Prefix-MRL, full | seq. × 64 \times 64 | 128,318 128{,}318 | 120 120 | 63.09 |
| ST-HAC | ≤ 128 × 64 \leq 128\times 64 | 8,448 8{,}448 | 7.87 7.87 | 62.96 |
| ST-HAC | ≤ 64 × 64 \leq 64\times 64 | 4,352 4{,}352 | 4.05 4.05 | 62.47 |
| ST-HAC | ≤ 32 × 128 \leq 32\times 128 | 4,608 4{,}608 | 4.29 4.29 | 61.82 |
| ST-HAC | ≤ 32 × 64 \leq 32\times 64 | 2,304 2{,}304 | 2.15 2.15 | 61.16 |

## Table 16: Full-sequence ceiling and the released index on MMEB. V3 and V2 use the means in Appendix B .

| Representation | V3 | V2 | Image | Video | VisDoc | Text | Agent |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Full sequence, d = 2048 d=2048 | 60.68 | 78.56 | 78.70 | 70.08 | 84.70 | 52.97 | 54.14 |
| Full sequence, d = 64 d=64 | 59.02 | 77.89 | 78.06 | 69.52 | 83.90 | 52.50 | 49.17 |
| K ​ 128 × d ​ 64 K128\times d64 int8 | 59.71 | 77.81 | 78.04 | 69.37 | 83.80 | 51.64 | 52.99 |
| Released index | 60.06 | 77.96 | 78.09 | 69.62 | 84.02 | 51.77 | 54.03 |

## Table 17: Int8 quantization on ViDoRe V3, graded nDCG@10.

| Scheme | Extra / vec. | Compare | Append | nDCG@10 |
| --- | --- | --- | --- | --- |
| fp16 centroids | + 64 +64 B | Float | Direct | 62.99 |
| int8 + fp16 scale | + 2 +2 B | Float | Direct | 62.96 |
| int8, scale dropped | 0 0 | Integer | Direct | 57.82 |
| Corpus max / 127 /127 | 0 0 | Integer | Rescan | 62.97 |
| Fixed scale 1 / 127 1/127 | 0 0 | Integer | Direct | 62.96 |

## Table 18: Single-thread retrieval latency in milliseconds. Cells are totals. Δ \Delta is the nDCG@10 change on the document pool and the video pool.

| Pipeline | N 1 N_{1} | N 2 N_{2} | 100k | 1M | 5M | Δ \Delta doc / vid |
| --- | --- | --- | --- | --- | --- | --- |
| Full int8 MaxSim | all | – | 1,657 1{,}657 | 12,781 12{,}781 | 63,892 63{,}892 | 0 0 / 0 0 |
| Single vector d = 2048 d=2048 | all | – | 34.6 | 331.0 | 1,666 1{,}666 | – |
| Single vector d = 4096 d=4096 | all | – | 60.9 | 604.0 | 3,039 3{,}039 | – |
| S1 + S3 | 2,000 2{,}000 | – | 41.8 | 55.2 | 128.5 | − 0.60 -0.60 / − 0.66 -0.66 |
| S1 + S3 | 5,000 5{,}000 | – | 103.9 | 115.1 | 186.5 | − 0.13 -0.13 / − 0.10 -0.10 |
| Three-stage | 5,000 5{,}000 | 200 200 | 24.6 | 38.4 | 110.2 | − 0.20 -0.20 / − 3.09 -3.09 |
| Three-stage | 5,000 5{,}000 | 500 500 | 30.6 | 44.2 | 116.6 | − 0.13 -0.13 / − 0.84 -0.84 |
| Three-stage | 5,000 5{,}000 | 1,000 1{,}000 | 41.9 | 54.2 | 120.2 | − 0.13 -0.13 / − 0.26 -0.26 |
| Three-stage | 10,000 10{,}000 | 1,000 1{,}000 | 62.3 | 75.7 | 127.7 | 0.00 0.00 / − 0.35 -0.35 |
| Float × \times 1 1 -bit | 5,000 5{,}000 | 100 100 | 72.7 | 85.8 | 156.7 | − 0.21 -0.21 / − 1.05 -1.05 |

## Table 19: Latency in milliseconds by query length on 1 1 million records, at N 1 = 5,000 N_{1}=5{,}000 and N 2 = 1,000 N_{2}=1{,}000 . Speedup is against full int8 MaxSim.

| Query | L q L_{q} | S1 | S2 | S3 | Total |
| --- | --- | --- | --- | --- | --- |
| Short text | 20 20 – 40 40 | 14.8 | 14.6 | 17.3 | 46.7 ( 274 × 274\times ) |
| Image or image-text | 90 90 – 270 270 | 14.8 | 91.6 | 49.8 | 156.2 ( 82 × 82\times ) |
| Long context or a full page | 150 150 – 500 + 500+ | 14.8 | 321.8 | 103.3 | 439.9 ( 29 × 29\times ) |

## Table 20: Training and index settings used for the released model.

| Group | Setting |
| --- | --- |
| Backbone | Qwen3.5-VL with bidirectional full attention; d hid = 2560 d_{\mathrm{hid}}=2560 ; W ∈ ℝ 2048 × 2560 W\in\mathbb{R}^{2048\times 2560} ; widths { 64,128,256,512 , 1024 , 2048 } \{64,128,256,512,1024,2048\} . |
| Video | Δ ​ t patch = 2 \Delta t_{\mathrm{patch}}=2 . Training pads clips shorter than 12 12 frames up to 12 12 , with a cap of 3,600 3{,}600 tokens. Evaluation uses 32 32 frames and 14,400 14{,}400 tokens, and the official comparison uses 8 8 frames and 3,600 3{,}600 tokens. |
| Optimization | AdamW, weight decay 0.02 0.02 . LoRA rank 64 64 or 128 128 , α = 4 ​ r \alpha=4r , dropout 0.05 0.05 . Learning rate 2 × 10 − 5 2\times 10^{-5} on LoRA and 4 × 10 − 6 4\times 10^{-6} on the merger and the head, cosine decay to 0.1 × 0.1\times the peak, warmup 5 % 5\% of steps. Global batch 512 512 . One epoch per stage. |
| Loss | τ = 0.02 \tau=0.02 , γ = 1 \gamma=1 , β = 0.5 \beta=0.5 , λ ord = 0.10 \lambda_{\mathrm{ord}}=0.10 . λ kd \lambda_{\mathrm{kd}} is frozen after it is set from the early gradient-norm ratio. w e = 0.80 w_{e}=0.80 . |
| Train-time K K | { 64,128 } \{64,128\} with probabilities 0.3 0.3 and 0.7 0.7 . |
| Query side | τ gate = 0.6 \tau_{\mathrm{gate}}=0.6 , θ nf = 0.38 \theta_{\mathrm{nf}}=0.38 , β nf = 2.5 \beta_{\mathrm{nf}}=2.5 . |
| Merge | c k , b ∈ [ 0 , 1 ] c_{k,b}\in[0,1] per block. Language-layer trim keeps ρ = 0.75 \rho=0.75 ; other blocks use ρ = 1 \rho=1 . |
| ST-HAC | Video ( w s , w t ) = ( 0.07 , 0.03 ) (w_{s},w_{t})=(0.07,0.03) ; images and pages ( 0.10 , 0 ) (0.10,0) ; text ( 0 , 0.10 ) (0,0.10) . K ≤ 128 K\leq 128 , d = 64 d=64 . Time frequencies in [ π / 4 , π ] [\pi/4,\pi] . |
| Quantization | Scale 1 / 127 1/127 , integers in [ − 127,127 ] [-127,127] . Record caps 8,448 8{,}448 bytes (two-level) and 9,472 9{,}472 bytes (three-stage). |
| Retrieval | N 1 = 5,000 N_{1}=5{,}000 , N 2 = 1,000 N_{2}=1{,}000 , k = 10 k=10 . |

## Table 21: Suites reported in Section 8. MMEB-V3 scores 11 audio tasks as zero and includes them in the denominator. Agent is Tool + GUI + Memory, with MCMR reported separately in Table 8 .

| Suite | Coverage | Tasks | Metric |
| --- | --- | --- | --- |
| MMEB-V3 | Image, video, visual documents, text, tool, GUI, memory, multi-hop | 190 | Hit@1; nDCG@5 on text and visual documents |
| MMEB-V2 | Image (36), video (18), visual documents (24) | 78 | Hit@1 on image and video; nDCG@5 on visual documents |
| ViDoRe V3 | 8 domains, 6 languages | 48 | Graded nDCG@10 |
| Fine-grained | FORB, Street2Shop, MovingFashion; MSR-VTT, MSVD, DiDeMo, VATEX; ActivityNet order | 8 | Top-1 / nDCG@10 / win rate |
