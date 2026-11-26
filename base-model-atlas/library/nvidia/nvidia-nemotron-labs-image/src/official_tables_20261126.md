# 官方原表转录

来源：https://arxiv.org/html/2611.31358v1

原始多层表头和跨列布局以同目录HTML为准；此处保留全部单元格，不把空值补为零。

## Table 1 : Nemotron-Labs-Image-Tokenizer architecture. The encoder produces discrete visual codes and the decoder renders them into raster images.

| Hyperparameter | Value |
| --- | --- |
| Transformer architecture |  |
| Implementation class | VITVQModel |
| Parameters | Approximately 642M |
| Encoder / decoder layers | 24 / 24 |
| Hidden width / attention heads | 1,024 / 16 |
| MLP ratio | 4 |
| Decoder output FFN | Enabled; output FFN dimension 3,072 |
| RoPE θ \theta / dropout | 10,000 / 0 |
| Discrete representation |  |
| Patch size | 16 × 16 16\times 16 |
| Quantized embedding dimension | 24 |
| Codebook | Normalized Leech lattice; 196,560 entries |
| Codebook weights / L2 normalization | Frozen / enabled |
| Image interface |  |
| Encode / decode resize | None / none |
| Zero-mean input | Enabled |
| Output clamp | [ − 1 , 1 ] [-1,1] |

## Table 2: Image tokenizer training configuration through 670K steps. AdamW optimizes both the tokenizer autoencoder and the discriminator; Table 3 gives the effective learning rates.

| Hyperparameter | Value |
| --- | --- |
| Reconstruction and distillation |  |
| Pixel reconstruction / weight | Mean absolute RGB error in [ − 1 , 1 ] [-1,1] / 1.0 |
| Perceptual loss / weight | LPIPS / 0.1 |
| Distillation teacher / weight | DINOv2 ViT-L / 0.1 |
| Distillation objective | Negative mean cosine similarity |
| Distillation attachment | Decoder block 3, followed by an MLP |
| Feature alignment | 2D adaptive average pooling to the teacher grid |
| Feature normalization | Tokenwise L2 normalization on both sides |
| Arbitrary-resolution distillation | Enabled |
| Commitment loss | Not used |
| Quantization gradients / codebook | Straight-through estimator / fixed |
| Adversarial training |  |
| Discriminator | Unconditional PatchGAN; 3 input channels |
| Layers / base width / kernel size | 3 / 64 / 4 × 4 4\times 4 |
| Normalization | Batch normalization; ActNorm disabled |
| Blur downsampling | Disabled |
| Arbitrary-resolution mode | pad_max |
| GAN objective / start step | Softplus / 0 |
| Discriminator weight / adaptive weighting | 0.5 / disabled |
| R1 γ \gamma / frequency | 10 / every 16 steps (lazy regularization) |
| R1 multiplier | 80 when evaluated; time-averaged coefficient 5 |
| Data and token packing |  |
| Training corpus | NVCLIP (Section 4.1 ) |
| Curated image pool | Approximately 200M images |
| Images used in training | Approximately 153M |
| Clustering, deduplication, and filtering | SigLIP 2, DINOv2, and SSCD |
| Batch construction | Variable-resolution token packing |
| min_pixels / max_pixels | 256 / 1,638,400 |
| Size divisor / padding mode | 16 / replicate |
| Pixel budget per rank per batch | 2,621,440 |
| Optimization |  |
| Autoencoder / discriminator optimizer | AdamW / AdamW |
| Base learning rate | 4 × 10 − 7 4\times 10^{-7} |
| World size / nominal batch size | 32 / 8 |
| Scaled base learning rate | 1.024 × 10 − 4 1.024\times 10^{-4} |
| Weight decay | 10 − 4 10^{-4} |
| AdamW β 1 , β 2 \beta_{1},\beta_{2} / ϵ \epsilon | ( 0.9 , 0.99 ) (0.9,0.99) / 10 − 8 10^{-8} |
| Precision / automatic mixed precision | BF16 / enabled |
| Gradient checkpointing | Enabled |
| Encoder freezing | After 480K steps |
| Training duration | 670K steps |

## Table 3 : Tokenizer learning-rate stages. The multiplier scales the base rate after world-size and nominal-batch-size scaling. The codebook is frozen throughout training.

| Training steps | Multiplier m ⁡ ( t ) m(t) | Learning rate η ⁡ ( t ) \eta(t) | Encoder |
| --- | --- | --- | --- |
| 0–300K | 1.0 | 1.024 × 10 − 4 1.024\times 10^{-4} | Trainable |
| 300K–480K | 0.6 | 6.144 × 10 − 5 6.144\times 10^{-5} | Trainable |
| 480K–670K | 0.36 | 3.6864 × 10 − 5 3.6864\times 10^{-5} | Frozen |

## Table 4 : Raster image generator training configurations. For Nemotron-Labs-Image-30B-A3B, we report three arbitrary-resolution mid-training
stages with increasing maximum image pixel counts and the mixed-resolution
reinforcement-learning stage. Aspect ratios vary within each mid-training stage.
T2I denotes text-to-image generation; TI2I denotes generation conditioned on both
text and source or reference images.
The optimizer configuration uses Muon ( Jordan, 2024 ) with
Polar Express ( Amsel et al., 2026 ) and Adam ( Kingma and Ba, 2015 ) .

| Configuration | Mid-Training Stage 1 | Mid-Training Stage 2 | Mid-Training Stage 3 | Reinforcement Learning |
| --- | --- | --- | --- | --- |
| Maximum image pixels | 256 2 256^{2} | 512 2 512^{2} | 1024 2 1024^{2} | – |
| Optimization |  |  |  |  |
| LR scheduler | Constant | Constant | Constant | Constant |
| Learning rate (Muon) | 1 × 10 − 3 1\times 10^{-3} | 1 × 10 − 3 1\times 10^{-3} | 1 × 10 − 3 1\times 10^{-3} | – |
| Learning rate (Adam) | 1 × 10 − 4 1\times 10^{-4} | 1 × 10 − 4 1\times 10^{-4} | 1 × 10 − 4 1\times 10^{-4} | 2 × 10 − 6 2\times 10^{-6} |
| Optimizer (Muon) | μ = 0.95 \mu=0.95 , Polar Express, spectral-norm LR adjustment | – |  |  |
| Optimizer (Adam) | β 1 = 0.9 , β 2 = 0.95 , ϵ = 10 − 8 \beta_{1}=0.9,\ \beta_{2}=0.95,\ \epsilon=10^{-8} | β 1 = 0.9 , β 2 = 0.98 , ϵ = 10 − 8 \beta_{1}=0.9,\ \beta_{2}=0.98,\ \epsilon=10^{-8} |  |  |
| Weight decay | 0.01 | 0.01 | 0.01 | 0.0 |
| Gradient norm clip | 1.0 | 1.0 | 1.0 | 1.0 |
| EMA ratio | 0.9999 | 0.9999 | 0.9999 | – |
| Training steps | 35K | 90K | 70K | 200 rollout iterations |
| Warmup steps | 500 | 500 | 500 | 0 |
| Sequence length | 81920 | 81920 | 81920 | 8192 |
| Prompts per rollout | – | – | – | 48 |
| Candidates per prompt | – | – | – | 32 |
| Trajectories per update | – | – | – | 768 |
| Training data mixture |  |  |  |  |
| T2I data | 0.9 | 0.9 | 0.9 | 1.0 |
| TI2I data | 0.1 | 0.1 | 0.1 | 0.0 |

## Table 5 : Overall tokenizer reconstruction quality on approximately 178K images across six visual domains. MUSIQ and CLIP-IQA score reconstructed images without a reference. The Laplacian-variance ratio has a target value of 1. Bold marks the better value for each metric.

| Metric | Emu3.5 IBQ | Nemotron-Labs-Image-Tokenizer (ours) |
| --- | --- | --- |
| Reconstruction fidelity |  |  |
| PSNR (dB) ↑ \uparrow | 26.08 | 29.57 |
| SSIM ↑ \uparrow | 0.781 | 0.834 |
| LPIPS ↓ \downarrow | 0.0855 | 0.0713 |
| GMSD ↓ \downarrow | 0.0994 | 0.0675 |
| Feature-distribution distance |  |  |
| FID ↓ \downarrow | 36.36 | 35.06 |
| FD-DINOv2 ↓ \downarrow | 7.49 | 5.25 |
| Image quality and sharpness |  |  |
| MUSIQ ↑ \uparrow | 65.84 | 65.78 |
| CLIP-IQA ↑ \uparrow | 0.593 | 0.583 |
| Lap-var ratio → 1 \to 1 | 0.892 | 0.982 |

## Table 6 : Compositional generation and prompt following. GenEval2 reports Soft-TIFA GM; UniGenBench++ reports English short- and long-prompt scores. Both agentic configurations use the same image generator as the standalone model.

| Model / configuration | Params | GenEval ↑ \uparrow | GenEval2 GM ↑ \uparrow | UniGen++ EN ↑ \uparrow | UniGen++ EN-Long ↑ \uparrow |
| --- | --- | --- | --- | --- | --- |
| Closed-source models |  |  |  |  |  |
| GPT Image 2 | Undisc. | 89.00 | 81.00 | – | – |
| Nano Banana 2.0 | Undisc. | 83.00 | – | – | – |
| Nano Banana Pro † \dagger | Undisc. | – | 59.00 | 92.72 | 94.20 |
| Qwen-Image 3.0 | Undisc. | – | 76.00 | – | – |
| Qwen-Image 2.0 | Undisc. | – | 48.00 | – | – |
| Seedream 5.0 Pro | Undisc. | – | 68.00 | – | – |
| Seedream 4.5 | Undisc. | – | – | 89.70 | 91.38 |
| Seedream 4.0 | Undisc. | 84.00 | – | 87.35 | 89.77 |
| HiDream-O1-Image-Pro | 200B+ | 92.00 | – | – | – |
| Open-weight models |  |  |  |  |  |
| SenseNova-U1.5 | 8B | 92.00 | 55.00 | – | – |
| SenseNova-U1 | 8B | 91.00 | 43.00 | – | – |
| FLUX.2 Dev | 24B + 32B | 87.00 | – | 84.76 | 90.31 |
| Qwen-Image | 7B + 20B | 86.83 | 33.80 | 78.36 | 83.94 |
| GLM-Image | 9B + 7B | – | – | 67.23 | 75.48 |
| Z-Image | 4B + 6B | 84.00 | 31.00 | 78.10 | 86.77 |
| Z-Image-Turbo | 4B + 6B | 82.00 | – | 71.40 | 80.72 |
| ERNIE-Image (w/ PE) | 8B + 3B PE | 87.28 | – | – | – |
| ERNIE-Image (w/o PE) | 8B | 88.56 | – | – | – |
| LLaDA-Image | 6B | 85.00 | – | – | – |
| Boogu-Image 0.1 Base | 10B | 85.00 | – | – | – |
| HiDream-O1-Image | 8B | 90.00 | – | – | – |
| Our configurations |  |  |  |  |  |
| Nemotron-Labs-Image-30B-A3B (standalone) | 30B-A3B | 80.97 | 31.71 | 77.64 | 85.02 |
| Nemotron-Labs-VisualCreation (+ Nemotron agentic model) | - | 86.40 | 52.56 | 88.78 | 89.84 |
| Nemotron-Labs-VisualCreation (+ GPT-6 agentic model) | - | 92.86 | 65.43 | 93.20 | 94.25 |

## Table 7 : Visual text rendering on LongTextBench and CVTG-2K, using their English settings. Both agentic configurations use the same image generator as the standalone model.

| Model / configuration | Params | LongTextBench-EN ↑ \uparrow | CVTG-2K-EN ↑ \uparrow |
| --- | --- | --- | --- |
| Closed-source models |  |  |  |
| GPT Image 2 | Undisc. | 96.00 | 90.03 |
| Nano Banana 2.0 | Undisc. | 98.00 | 78.75 |
| Nano Banana Pro | Undisc. | 97.60 | 77.90 |
| Qwen-Image 3.0 | Undisc. | 98.20 | – |
| Seedream 5.0 Pro | Undisc. | 94.10 | – |
| Seedream 4.5 | Undisc. | 98.90 | 89.90 |
| Seedream 4.0 | Undisc. | 92.14 | 90.03 |
| HiDream-O1-Image-Pro | 200B+ | 98.20 | 92.22 |
| Open-weight models |  |  |  |
| SenseNova-U1.5 | 8B | 98.80 | 94.80 |
| SenseNova-U1 | 8B | 97.90 | 94.00 |
| FLUX.2 Dev | 24B + 32B | 96.30 | 89.26 |
| Qwen-Image | 7B + 20B | 94.30 | 82.88 |
| GLM-Image | 9B + 7B | 95.24 | 91.16 |
| Z-Image | 4B + 6B | 93.50 | 86.71 |
| Z-Image-Turbo | 4B + 6B | 91.70 | 85.85 |
| ERNIE-Image (w/ PE) | 8B + 3B PE | 98.04 | – |
| ERNIE-Image (w/o PE) | 8B | 96.79 | – |
| Emu3.5 | 32B | 97.60 | 91.20 |
| LLaDA-Image | 6B | 92.30 | 87.50 |
| Boogu-Image 0.1 Base | 10B | 95.20 | 86.30 |
| HiDream-O1-Image | 8B | 97.90 | 91.28 |
| Our configurations |  |  |  |
| Nemotron-Labs-Image-30B-A3B (standalone) | 30B-A3B | 94.30 | 84.11 |
| Nemotron-Labs-VisualCreation (+ Nemotron agentic model) | - | 97.00 | 89.63 |
| Nemotron-Labs-VisualCreation (+ GPT-6 agentic model) | - | 97.98 | 92.53 |

## Table 8 : Broad visual-generation evaluation on OneIG and Qwen-Image-Bench, using their English settings. Both agentic configurations use the same image generator as the standalone model.

| Model / configuration | Params | OneIG-EN ↑ \uparrow | Qwen-Image-Bench EN ↑ \uparrow |
| --- | --- | --- | --- |
| Closed-source models |  |  |  |
| GPT Image 2 | Undisc. | 51.60 | 65.23 |
| Nano Banana 2.0 | Undisc. | 57.80 | 59.59 |
| Nano Banana Pro | Undisc. | 58.30 | 59.33 |
| Qwen-Image 3.0 | Undisc. | 56.30 | – |
| Qwen-Image 2.0 | Undisc. | 54.10 | 57.90 |
| Seedream 5.0 Pro | Undisc. | 55.30 | 57.80 |
| Seedream 4.5 | Undisc. | 57.60 | 56.95 |
| Seedream 4.0 | Undisc. | 57.30 | 56.48 |
| Open-weight models |  |  |  |
| SenseNova-U1.5 | 8B | 55.20 | 52.82 |
| SenseNova-U1 | 8B | 54.90 | 48.28 |
| Qwen-Image | 7B + 20B | 53.90 | 48.48 |
| GLM-Image | 9B + 7B | 52.80 | 47.86 |
| Z-Image | 4B + 6B | 54.60 | – |
| Z-Image-Turbo | 4B + 6B | 52.80 | – |
| ERNIE-Image (w/ PE) | 8B + 3B PE | 57.50 | – |
| ERNIE-Image (w/o PE) | 8B | 55.37 | – |
| Emu3.5 | 32B | 56.40 | – |
| LLaDA-Image | 6B | – | 53.53 |
| Boogu-Image 0.1 Base | 10B | – | 51.00 |
| Our configurations |  |  |  |
| Nemotron-Labs-Image-30B-A3B (standalone) | 30B-A3B | 52.77 | 46.36 |
| Nemotron-Labs-VisualCreation (+ Nemotron agentic model) | - | 54.14 | 51.33 |
| Nemotron-Labs-VisualCreation (+ GPT-6 agentic model) | - | 54.63 | 52.46 |

## Table 9 : Knowledge and reasoning in visual creation. WISE uses the Verified protocol. Both agentic configurations use the same image generator as the standalone model.

| Model / configuration | Params | WISE Verified ↑ \uparrow |
| --- | --- | --- |
| Closed-source models |  |  |
| Nano Banana Pro | Undisc. | 87.60 |
| Qwen-Image 2.0 | Undisc. | 79.54 |
| Open-weight models |  |  |
| FLUX.2 Dev | 24B + 32B | 56.50 |
| Qwen-Image | 7B + 20B | 51.00 |
| Z-Image | 4B + 6B | 45.30 |
| Our configurations |  |  |
| Nemotron-Labs-Image-30B-A3B (standalone) | 30B-A3B | 46.30 |
| Nemotron-Labs-VisualCreation (+ Nemotron agentic model) | - | 88.60 |
| Nemotron-Labs-VisualCreation (+ GPT-6 agentic model) | - | 91.50 |

## Table 10 : Commercial visual design on BizGenEval. The standalone raster image generator result is unreported. Both agentic configurations use the same image generator as the standalone model.

| Model / configuration | Params | BizGenEval ↑ \uparrow |
| --- | --- | --- |
| Closed-source models |  |  |
| GPT Image 2 | Undisc. | 83.2 |
| Nano Banana 2.0 | Undisc. | 68.5 |
| Nano Banana Pro | Undisc. | 76.7 |
| Qwen-Image 2.0 | Undisc. | 45.5 |
| Seedream 5.0 Pro | Undisc. | 48.8 |
| Seedream 4.5 | Undisc. | 30.1 |
| Seedream 4.0 | Undisc. | 14.3 |
| Open-weight models |  |  |
| FLUX.2 Dev | 24B + 32B | 4.9 |
| Qwen-Image | 7B + 20B | 6.3 |
| Z-Image | 4B + 6B | 8.2 |
| Emu3.5 | 32B | 13.2 |
| Our configurations |  |  |
| Nemotron-Labs-Image-30B-A3B (standalone) | 30B-A3B | – |
| Nemotron-Labs-VisualCreation (+ Nemotron agentic model) | - | 64.7 |
| Nemotron-Labs-VisualCreation (+ GPT-6 agentic model) | - | 86.0 |

## Table 13: Principal machine-readable records used by the creation harness.

| Record | Principal fields |
| --- | --- |
| Artifact route | route , target_surface , subtype , aspect_ratio , canvas_count , primary_format , visual_asset_policy , renderer , and needs_web_search . |
| Resolved layout | Layout mode ; canvas dimensions, safe margins, and overflow policy;
ordered regions with stable section identifiers, normalized bounds or flow
order, component and text budgets; and feasibility checks performed before
code generation. |
| Acceptance checklist | Stable checklist identifier, observable criterion, associated requirement
identifiers, verification mode, source, frozen status, and content hash. The
checklist is fixed before candidate generation and remains unchanged during
repair. |
| Audit issue | Repair target, stable artifact selector, affected requirement and checklist
identifiers, evaluated viewport, evidence image, optional asset identifier,
visible evidence, and an executable repair instruction. |
| Root-cause hypothesis | Diagnosis code, lowest responsible owner selector, causal evidence, and
confidence. Diagnosis codes cover component rendering, collision, containment,
spatial density, typography, color contrast, layout structure, content
fidelity, visual-asset quality, and interaction behavior. |
| Repair plan | Repair action, active and deferred issues, root-cause tree, repair scope,
selected assets, frozen unaffected regions, and the accepted-repair and
total-cycle limits. |
| Pairwise decision | Blind artifact assignment, winner or tie, confidence, concise rationale,
visible regressions, and differences with respect to the frozen checklist. |

## Table 14: Default control limits for candidate generation, repair, and
checkpoint selection.

| Control | Default limit |
| --- | --- |
| Raster candidates per generation job | 4 |
| Repair candidates per cycle | 2 |
| Accepted automatic repairs | 3 |
| Total attempted repair cycles | 8 |
| Layout-replan attempts | 1 |
| Search-template-replan attempts | 1 |
| Pairwise confidence threshold | 0.75 |

## Table 15 : Image sources for the six-domain tokenizer reconstruction evaluation. Counts are rounded totals for the images used here; individual dataset release sizes are not shown.

| Visual domain | Source datasets | Images |
| --- | --- | --- |
| Natural photos / general vision | MMBench ( 56 ) , MMStar ( 13 ) , BLINK ( 24 ) , OK-VQA ( 62 ) , RefCOCO ( 127 ) , POPE ( 45 ) , IllusionVQA ( 89 ) , NoCaps ( 1 ) , DetailCaps ( 19 ) , CountBenchQA ( 4 ) , HR-Bench ( 109 ) , Q-Bench ( 114 ) , RealWorldQA ( 117 ) | 55.1K |
| Documents / OCR | OCRBench v2 ( 23 ) , DocVQA ( 64 ) , TextVQA ( 94 ) , MMLongBench-Doc ( 60 ) , OmniDocBench ( 81 ) , MTVQA ( 101 ) | 24.3K |
| Charts / diagrams / science and math | AI2D ( 40 ) , ChartQA ( 63 ) , MathVista ( 59 ) , OlympiadBench ( 29 ) , ScienceQA ( 58 ) , PhyX ( 91 ) , VisuLogic ( 121 ) , MMMU ( 129 ) , CMMMU ( 132 ) , JMMMU ( 79 ) , ZeroBench ( 85 ) | 21.0K |
| UI screenshots | ScreenSpot-Pro ( 42 ) , VisualWebBench ( 54 ) | 3.6K |
| Faces | FFHQ ( 37 ) | 70.0K |
| Generated / edited | GEdit-Bench ( 55 ) , KRIS-Bench ( 116 ) | 3.7K |
| Total | 35 datasets across six visual domains | ∼ \sim 178K |

## Table 16 : Reconstruction fidelity by visual domain. Approximate domain sizes are shown in thousands of images. Bold marks the better value within each domain.

| Domain | Tokenizer | PSNR (dB) ↑ \uparrow | SSIM ↑ \uparrow | LPIPS ↓ \downarrow | GMSD ↓ \downarrow |
| --- | --- | --- | --- | --- | --- |
| Natural photos | Emu3.5 IBQ | 23.65 | 0.678 | 0.109 | 0.123 |
| (55.1K images) | Nemotron-Labs-Image-Tokenizer (ours) | 26.26 | 0.738 | 0.099 | 0.093 |
| Documents / OCR | Emu3.5 IBQ | 24.88 | 0.860 | 0.061 | 0.095 |
| (24.3K images) | Nemotron-Labs-Image-Tokenizer (ours) | 29.51 | 0.909 | 0.041 | 0.054 |
| Charts / diagrams | Emu3.5 IBQ | 25.51 | 0.917 | 0.041 | 0.080 |
| (21.0K images) | Nemotron-Labs-Image-Tokenizer (ours) | 30.86 | 0.946 | 0.023 | 0.041 |
| UI screenshots | Emu3.5 IBQ | 25.73 | 0.907 | 0.049 | 0.090 |
| (3.6K images) | Nemotron-Labs-Image-Tokenizer (ours) | 30.74 | 0.952 | 0.026 | 0.047 |
| Faces | Emu3.5 IBQ | 28.56 | 0.787 | 0.091 | 0.088 |
| (70.0K images) | Nemotron-Labs-Image-Tokenizer (ours) | 31.70 | 0.844 | 0.077 | 0.061 |
| Generated / edited | Emu3.5 IBQ | 26.86 | 0.792 | 0.079 | 0.098 |
| (3.7K images) | Nemotron-Labs-Image-Tokenizer (ours) | 30.49 | 0.843 | 0.067 | 0.068 |

## Table 17 : Feature-distribution distances, no-reference quality, and sharpness by domain. MUSIQ and CLIP-IQA evaluate the reconstructions. For the Laplacian-variance ratio, proximity to 1 determines the highlighted value; values above 1 are not inherently better.

| Domain | Tokenizer | FID ↓ \downarrow | FD-DINOv2 ↓ \downarrow | MUSIQ ↑ \uparrow | CLIP-IQA ↑ \uparrow | Lap-var ratio → 1 \to 1 |
| --- | --- | --- | --- | --- | --- | --- |
| Natural photos | Emu3.5 IBQ | 26.35 | 15.83 | 65.57 | 0.555 | 0.854 |
| (55.1K images) | Nemotron-Labs-Image-Tokenizer (ours) | 26.48 | 12.29 | 65.28 | 0.545 | 0.920 |
| Documents / OCR | Emu3.5 IBQ | 48.09 | 14.94 | 58.40 | 0.538 | 0.922 |
| (24.3K images) | Nemotron-Labs-Image-Tokenizer (ours) | 47.66 | 5.94 | 58.44 | 0.550 | 1.032 |
| Charts / diagrams | Emu3.5 IBQ | 62.16 | 29.93 | 61.95 | 0.709 | 0.902 |
| (21.0K images) | Nemotron-Labs-Image-Tokenizer (ours) | 61.50 | 7.85 | 62.24 | 0.709 | 1.042 |
| UI screenshots | Emu3.5 IBQ | 178.37 | 75.10 | 65.83 | 0.532 | 1.059 |
| (3.6K images) | Nemotron-Labs-Image-Tokenizer (ours) | 182.68 | 18.95 | 65.14 | 0.497 | 1.030 |
| Faces | Emu3.5 IBQ | 164.74 | 6.34 | 69.64 | 0.610 | 0.950 |
| (70.0K images) | Nemotron-Labs-Image-Tokenizer (ours) | 160.53 | 7.73 | 69.66 | 0.591 | 0.957 |
| Generated / edited | Emu3.5 IBQ | 48.60 | 29.81 | 68.79 | 0.582 | 0.915 |
| (3.7K images) | Nemotron-Labs-Image-Tokenizer (ours) | 49.03 | 22.01 | 68.76 | 0.583 | 0.940 |

## Table 18 : ImageNet-1K validation under arbitrary-resolution evaluation. Bold marks the better value between Emu3.5 and native-scale Nemotron-Labs-Image-Tokenizer. The separate 2 × 2\times Nemotron-Labs-Image-Tokenizer setting doubles each spatial dimension before encoding and resizes the reconstruction back, using approximately four times the native token count.

| Tokenizer / encoding | PSNR (dB) ↑ \uparrow | SSIM ↑ \uparrow | MS-SSIM ↑ \uparrow | LPIPS ↓ \downarrow | rFID ↓ \downarrow |
| --- | --- | --- | --- | --- | --- |
| Emu3.5 IBQ | 22.13 | 0.5909 | 0.8387 | 0.1254 | 0.5482 |
| Nemotron-Labs-Image-Tokenizer (native) | 24.16 | 0.6529 | 0.8858 | 0.1209 | 0.8595 |
| Nemotron-Labs-Image-Tokenizer ( 2 × 2\times scale) | 28.27 | 0.8076 | 0.9559 | 0.0610 | 0.4235 |
