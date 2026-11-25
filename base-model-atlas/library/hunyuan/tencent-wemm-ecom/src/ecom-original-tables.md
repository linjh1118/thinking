# 官方报告原表转录

完整比较行与缺失标记原样保留；这是第一手原表，不是独立实测。


## 原表 1

| Domain | Scope |
| --- | --- |
| E-commerce |  |
| Product Perception & Understanding | Category–property–value (CPV) prediction, including category prediction
with reasoning, attribute extraction, and SKU specification understanding,
together with localization and detection of target products in listing
images, multi-image listings, and livestream frames. |
| Product Information Audit | Rule-conditioned review of product listings: consistency across images,
titles, categories, and attributes; category mismatch; product-image
quality; inappropriate content; and quality checks of short titles. |
| Product Retrieval | Same-product matching and retrieval at SPU or SKU granularity, including
image-to-image and image-to-product search, text-based SKU matching, and
similarity judgments between visual entities or product regions. |
| General E-Commerce Knowledge & QA | Question answering over product images and listing text, OCR of product and
storefront images, shopping and price reasoning, and product, brand, and
entity knowledge, including entity recognition and product-word prediction. |
| E-Commerce Content Generation | Product-centric text generation: per-view and overall descriptions of
product images, multi-image listings, and livestream frames; short product
titles; and product copy and product-sharing posts. |
| General |  |
| Multimodal Understanding | Foundational understanding of single images, multiple images, and videos:
dense image captions, per-image and overall multi-image descriptions, video
event understanding and QA, and video temporal grounding. |
| OCR, Documents, and Charts | Text-rich inputs: text transcription, including multilingual OCR; document
and table parsing; document QA; chart reading; and structured extraction of
visible text. |
| Grounding and Detection | Image-space localization with coordinate targets: object detection,
referring-expression grounding, GUI element grounding, and rejection of
queries whose target is absent. |
| Visual Instruction & Reasoning | Visual tasks beyond description: VQA and cross-image comparison, counting
and relational questions without coordinate targets, image-quality
assessment, inferring edit instructions from source–edited image pairs, and
rule-conditioned moderation of general (non-listing) content. |
| Multimodal STEM | Mathematics, science, and technical problems that require visual context
(diagrams, charts, documents, educational material, or video), with worked
solutions; includes chart-to-code tasks. |
| Multimodal World Knowledge | Linking visual entities and scenes to external facts: encyclopedia- and
entity-grounded image descriptions, knowledge-intensive VQA, and
specialized-domain tasks such as medical imaging. |
| Pure Text | General text-only records: mathematical and scientific reasoning,
instruction-following and multilingual dialogue, encyclopedic and
reading-comprehension text, and curated web text. |

## 原表 2

|  | ℒ CPT ​ ( θ , ℬ ) = − ∑ i ∈ ℬ N i − 1 / 2 ∑ t ∈ ℳ i log π θ ( z i , t ∣ v i , z i , < t ) ∑ i ∈ ℬ N i . \mathcal{L}_{\mathrm{CPT}}(\theta;\mathcal{B})=-\frac{\sum_{i\in\mathcal{B}}N_{i}^{-1/2}\sum_{t\in\mathcal{M}_{i}}\log\pi_{\theta}(z_{i,t}\mid v_{i},z_{i,<t})}{\sum_{i\in\mathcal{B}}\sqrt{N_{i}}}. |  | (1) |
| --- | --- | --- | --- |

## 原表 3

|  | a i , t KD = log ⁡ π T ​ ( y i , t ∣ h i , t ) − log ⁡ π θ old ​ ( y i , t ∣ h i , t ) , a_{i,t}^{\mathrm{KD}}=\log\pi_{T}(y_{i,t}\mid h_{i,t})-\log\pi_{\theta_{\mathrm{old}}}(y_{i,t}\mid h_{i,t}), |  | (2) |
| --- | --- | --- | --- |

## 原表 4

|  | ℒ OPD ( θ ) = − 1 \| ℬ \| ∑ i ∈ ℬ 1 \| ℛ i \| ∑ t ∈ ℛ i min ( ρ i , t a i , t KD , clip ( ρ i , t , 0.8 , 1.2 ) a i , t KD ) . \mathcal{L}_{\mathrm{OPD}}(\theta)=-\frac{1}{\|\mathcal{B}\|}\sum_{i\in\mathcal{B}}\frac{1}{\|\mathcal{R}_{i}\|}\sum_{t\in\mathcal{R}_{i}}\min\!\bigl(\rho_{i,t}a_{i,t}^{\mathrm{KD}},\operatorname{clip}(\rho_{i,t},0.8,1.2)a_{i,t}^{\mathrm{KD}}\bigr). |  | (3) |
| --- | --- | --- | --- |

## 原表 5

|  | A ^ i = r i − r ¯ std ⁡ ( r 1 , … , r G ) + ϵ A , r ¯ = 1 G ​ ∑ i r i . \widehat{A}_{i}=\frac{r_{i}-\bar{r}}{\operatorname{std}(r_{1},\ldots,r_{G})+\epsilon_{A}},\qquad\bar{r}=\frac{1}{G}\sum_{i}r_{i}. |  | (4) |
| --- | --- | --- | --- |

## 原表 6

|  | ℒ RL ​ ( θ ) = 1 \| ℬ \| ​ ∑ i ∈ ℬ 1 \| ℛ i \| ​ ∑ t ∈ ℛ i [ − A ^ i ​ exp ⁡ ( ℓ i , t − sg ⁡ ( ℓ i , t ) ) + 0.01 ​ K i , t ] , \mathcal{L}_{\mathrm{RL}}(\theta)=\frac{1}{\|\mathcal{B}\|}\sum_{i\in\mathcal{B}}\frac{1}{\|\mathcal{R}_{i}\|}\sum_{t\in\mathcal{R}_{i}}\left[-\widehat{A}_{i}\exp\!\big(\ell_{i,t}-\operatorname{sg}(\ell_{i,t})\big)+0.01K_{i,t}\right], |  | (5) |
| --- | --- | --- | --- |

## 原表 7

| Setting | CPT Stage 1 | CPT Stage 2 | OPD | RL/GRPO |
| --- | --- | --- | --- | --- |
| Training budget (tokens) | 370.3B | 76.7B | 0.6B | 0.2B |
| Optimization signal | Likelihood | Likelihood | Teacher scores | Task rewards |
| Optimizer | AdamW + Muon | AdamW + Muon | AdamW | AdamW |
| LR warmup steps | 1,000 | 1,500 | 0 | 0 |
| Peak learning rate | 1.5 × 10 − 6 1.5\times 10^{-6} | 10 − 6 10^{-6} | 10 − 6 10^{-6} | 10 − 6 10^{-6} |
| Minimum learning rate | 1.5 × 10 − 7 1.5\times 10^{-7} | 10 − 7 10^{-7} | 10 − 6 10^{-6} | 10 − 6 10^{-6} |
| Tokens per step | 5.7M | 5.7M | – | – |
| Global batch size | – | – | 2,048 | 2,048 |
| Sequence length | 16,384 | 32,768 | 32,768 | 65,536 |

## 原表 8

| Benchmark | WeMM-Ecom | Qwen3.8 Flash-Next | HY4 | DeepSeek V4.1-Flash-1017 | GLM-5.3 Flash | MiMo-V2.6 Flash-RL |
| --- | --- | --- | --- | --- | --- | --- |
| Size | 35B-A3B | 180B-A6B | 770B-A49B | 763B-A16B | 320B-A18B | 310B-A15B |
|  |  |  |  |  |  |  |
| Product Knowledge |  |  |  |  |  |  |
| E-commerce Knowledge | 67.1 | 78.9 | 85.2 | 82.4 | 82.9 | 79.2 |
| Entity Recognition | 80.4 | 84.2 | 86.7 | 81.6 | 84.9 | 76.2 |
|  |  |  |  |  |  |  |
| Product Attributes |  |  |  |  |  |  |
| Attribute Selection | 77.1 | 75.7 | 76.5 | 74.0 | 71.9 | 68.3 |
| Attribute Extraction | 81.8 | 78.8 | 77.9 | 79.0 | 76.4 | 76.9 |
| Brand Attribution | 83.1 | 86.3 | 84.3 | 82.5 | 80.5 | 80.8 |
| Brand Extraction | 83.6 | 81.2 | 80.5 | 82.7 | 83.1 | 81.5 |
|  |  |  |  |  |  |  |
| Product Moderation |  |  |  |  |  |  |
| Illegal Goods | 93.0 | 93.7 | 89.0 | 93.7 | 93.1 | 93.0 |
| Sales Restrictions | 91.1 | 89.7 | 90.6 | 86.6 | 88.4 | 90.2 |
| Image-Title Mismatch | 87.4 | 91.7 | 89.7 | 87.7 | 89.5 | 84.0 |
|  |  |  |  |  |  |  |
| Product OCR | 97.8 | 97.7 | 97.1 | 95.9 | 97.0 | 93.8 |
|  |  |  |  |  |  |  |
| Product Retrieval |  |  |  |  |  |  |
| Region-level Retrieval | 85.1 | 78.6 | 76.0 | 83.9 | 76.7 | 76.1 |
| Product-level Retrieval | 87.5 | 66.5 | 63.9 | 78.3 | 61.9 | 66.1 |
| SKU-level Retrieval | 62.2 | 43.6 | 43.0 | 49.3 | 49.3 | 38.7 |
|  |  |  |  |  |  |  |
| Product Grounding |  |  |  |  |  |  |
| Chart Detection | 77.0 | 79.4 | 72.7 | 66.5 | 65.4 | 27.6 |
| Product Detection | 79.9 | 71.7 | 73.3 | 67.1 | 67.6 | 44.3 |
| Logo Detection | 58.9 | 59.3 | 49.2 | 42.2 | 36.0 | 6.1 |
| Qualification Detection | 61.8 | 54.4 | 37.2 | 23.6 | 18.1 | 2.0 |
| Dimension Detection | 74.3 | 74.3 | 68.1 | 55.7 | 55.4 | 26.8 |
| Livestream Detection | 64.7 | 47.7 | 55.6 | 53.0 | 50.1 | 27.1 |
|  |  |  |  |  |  |  |
| E-commerce Reasoning |  |  |  |  |  |  |
| Chart Reasoning | 99.4 | 99.5 | 99.1 | 93.5 | 98.5 | 96.8 |
| Category Reasoning | 81.2 | 85.6 | 85.8 | 85.2 | 85.6 | 80.2 |
| Product Counting | 82.2 | 79.6 | 81.2 | 69.0 | 83.8 | 72.8 |
| Spatial Reasoning | 31.2 | 35.6 | 32.6 | 19.4 | 35.4 | 17.4 |
|  |  |  |  |  |  |  |
| E-commerce (Open) |  |  |  |  |  |  |
| ShoppingMMLU [ 32 ] | 74.9 | 78.0 | 76.9 | 76.0 | 78.3 | 76.3 |
| RAIR [ 48 ] | 43.7 | 48.0 | 45.0 | 44.9 | 45.9 | 45.9 |
| ChineseEcomQA [ 4 ] | 64.2 | 71.6 | 74.7 | 68.2 | 70.5 | 69.3 |
| EcomMMMU (GTS) [ 41 ] | 48.0 | 50.3 | 54.9 | 49.3 | 53.3 | 48.9 |
| IndustryBench-MIPU [ 63 ] | 63.5 | 66.8 | 72.8 | 63.2 | 69.7 | 65.3 |
| Overall mean (28) | 74.4 | 73.2 | 72.1 | 69.1 | 69.6 | 61.1 |

## 原表 9

| Benchmark | WeMM-Ecom | Qwen3.5 | Valley3 |  |  |  |
| --- | --- | --- | --- | --- | --- | --- |
| Size | 0.8B | 2B | 4B | 9B | 9B | 32B |
|  |  |  |  |  |  |  |
| Product Knowledge |  |  |  |  |  |  |
| E-commerce Knowledge | 26.7 / 30.8 | 36.4 / 38.6 | 50.9 / 51.4 | 58.7 / 59.4 | 57.5 / 55.8 | 63.4 / 62.8 |
| Entity Recognition | 53.1 / 66.9 | 74.4 / 76.6 | 78.4 / 78.4 | 80.2 / 77.3 | 79.8 / 75.6 | 79.3 / 80.6 |
|  |  |  |  |  |  |  |
| Product Attributes |  |  |  |  |  |  |
| Attribute Selection | 66.2 / 62.6 | 71.1 / 71.3 | 73.3 / 74.1 | 73.6 / 74.5 | 71.0 / 70.1 | 69.2 / 71.9 |
| Attribute Extraction | 71.8 / 75.2 | 77.6 / 79.2 | 79.9 / 80.4 | 80.8 / 81.1 | 77.0 / 73.6 | 74.1 / 78.6 |
| Brand Attribution | 79.1 / 79.2 | 82.6 / 83.3 | 81.8 / 80.8 | 83.5 / 81.0 | 79.8 / 73.6 | 77.0 / 80.3 |
| Brand Extraction | 80.1 / 80.8 | 81.0 / 82.5 | 80.8 / 83.2 | 81.2 / 85.1 | 81.8 / 81.8 | 83.1 / 83.8 |
|  |  |  |  |  |  |  |
| Product Moderation |  |  |  |  |  |  |
| Illegal Goods | 83.8 / 84.2 | 88.4 / 87.4 | 91.5 / 91.5 | 91.9 / 91.7 | 91.0 / 88.4 | 91.8 / 90.3 |
| Sales Restrictions | 82.6 / 77.5 | 84.3 / 83.1 | 89.3 / 90.0 | 89.9 / 90.8 | 89.7 / 83.3 | 90.4 / 88.2 |
| Image-Title Mismatch | 77.2 / 38.5 | 82.7 / 62.3 | 88.3 / 82.2 | 85.7 / 85.6 | 80.2 / 70.1 | 89.1 / 86.7 |
|  |  |  |  |  |  |  |
| Product OCR | 93.3 / 93.8 | 96.3 / 96.2 | 97.1 / 97.5 | 97.6 / 97.3 | 97.2 / 96.4 | 95.1 / 96.1 |
|  |  |  |  |  |  |  |
| Product Retrieval |  |  |  |  |  |  |
| Region-level Retrieval | 74.2 / 83.5 | 78.8 / 84.4 | 80.2 / 84.3 | 80.7 / 85.6 | 76.9 / 80.7 | 73.4 / 81.6 |
| Product-level Retrieval | 64.3 / 85.3 | 60.9 / 88.5 | 64.7 / 85.3 | 61.1 / 85.8 | 61.6 / 79.9 | 67.9 / 83.6 |
| SKU-level Retrieval | 53.7 / 63.1 | 62.4 / 64.8 | 58.3 / 64.0 | 61.9 / 61.4 | 52.1 / 32.0 | 33.0 / 43.2 |
|  |  |  |  |  |  |  |
| Product Grounding |  |  |  |  |  |  |
| Chart Detection | 52.4 / 50.6 | 64.4 / 55.7 | 61.4 / 66.9 | 73.4 / 73.3 | 60.8 / 63.6 | 69.4 / 65.4 |
| Product Detection | 74.8 / 75.1 | 68.6 / 72.3 | 76.4 / 78.5 | 79.2 / 80.4 | 70.0 / 72.3 | 66.0 / 71.8 |
| Logo Detection | 45.5 / 41.8 | 44.2 / 43.1 | 54.1 / 51.1 | 59.1 / 54.0 | 44.5 / 43.4 | 41.5 / 42.0 |
| Qualification Detection | 16.6 / 19.7 | 24.7 / 25.1 | 27.9 / 35.5 | 49.0 / 51.4 | 22.6 / 37.2 | 34.3 / 40.2 |
| Dimension Detection | 30.5 / 42.2 | 44.4 / 38.7 | 40.5 / 36.8 | 77.2 / 85.9 | 55.9 / 75.2 | 41.1 / 73.2 |
| Livestream Detection | 55.9 / 58.5 | 59.9 / 60.9 | 59.2 / 61.8 | 58.6 / 60.2 | 48.5 / 52.0 | 40.9 / 47.1 |
|  |  |  |  |  |  |  |
| E-commerce Reasoning |  |  |  |  |  |  |
| Chart Reasoning | 77.6 / 65.9 | 96.3 / 94.4 | 99.2 / 98.3 | 99.4 / 95.9 | 98.7 / 98.4 | 73.6 / 89.5 |
| Category Reasoning | 77.6 / 76.6 | 80.2 / 80.4 | 83.4 / 82.2 | 84.2 / 82.4 | 83.0 / 80.6 | 81.6 / 81.6 |
| Product Counting | 38.0 / 34.4 | 63.2 / 56.0 | 79.8 / 70.8 | 80.4 / 68.6 | 77.4 / 70.2 | 60.6 / 74.2 |
| Spatial Reasoning | 3.8 / 1.2 | 13.4 / 10.6 | 32.4 / 24.4 | 38.2 / 21.6 | 29.2 / 20.6 | 16.4 / 17.4 |
|  |  |  |  |  |  |  |
| E-commerce (Open) |  |  |  |  |  |  |
| ShoppingMMLU [ 32 ] | 61.1 / 50.2 | 70.5 / 60.6 | 74.9 / 69.7 | 76.6 / 72.5 | 76.0 / 69.4 | 73.3 / 73.8 |
| RAIR [ 48 ] | 37.0 / 23.8 | 36.1 / 36.6 | 40.5 / 36.1 | 44.3 / 42.7 | 44.6 / 41.5 | 48.7 / 44.5 |
| ChineseEcomQA [ 4 ] | 50.6 / 45.4 | 57.6 / 46.9 | 61.1 / 61.1 | 64.3 / 60.0 | 61.4 / 54.8 | 59.8 / 66.9 |
| EcomMMMU (GTS) [ 41 ] | 40.5 / 41.5 | 41.1 / 41.7 | 50.6 / 50.4 | 51.5 / 52.0 | 48.6 / 42.0 | 46.8 / 48.5 |
| IndustryBench-MIPU [ 63 ] | 44.9 / 39.7 | 57.6 / 51.9 | 67.1 / 57.0 | 66.5 / 61.4 | 66.6 / 56.1 | 67.1 / 57.4 |
| Overall mean (28) | 57.6 / 56.7 | 64.2 / 63.3 | 68.7 / 68.7 | 72.5 / 72.1 | 67.3 / 65.7 | 64.6 / 68.6 |

## 原表 10

| Benchmark | WeMM-Ecom | Qwen3.5 | Qwen3.6 | MiniCPM-V-4.7 | Gemma4 |
| --- | --- | --- | --- | --- | --- |
| Size | 35B-A3B | 35B-A3B | 35B-A3B | 35B-A3B | 26B-A4B |
|  |  |  |  |  |  |
| STEM and Multimodal Reasoning |  |  |  |  |  |
| CMMMU (val) [ 105 ] | 73.7 / 69.8 | 73.6 / 69.1 | 73.8 / 67.1 | 70.6 / 70.0 | 59.3 / 60.9 |
| CMMU (val, MCQ) [ 23 ] | 93.2 / 91.9 | 93.4 / 91.4 | 92.3 / 91.1 | 92.7 / 92.8 | 71.7 / 74.8 |
| CSVQA [ 30 ] | 83.5 / 73.6 | 83.3 / 75.3 | 84.2 / 74.2 | 77.3 / 81.8 | 43.5 / 48.5 |
| DynaMath [ 111 ] | 84.6 / 83.5 | 81.8 / 79.8 | 81.5 / 77.6 | 81.6 / 81.7 | 64.6 / 72.9 |
| LogicVista [ 93 ] | 78.0 / 74.0 | 79.0 / 72.0 | 78.0 / 71.0 | 69.0 / 72.0 | 63.0 / 67.0 |
| MATH-Vision [ 84 ] | 79.6 / 72.4 | 80.9 / 72.6 | 81.7 / 73.3 | 66.0 / 72.2 | 64.2 / 65.4 |
| MathVista (mini) [ 49 ] | 87.5 / 85.7 | 85.8 / 83.7 | 86.2 / 84.3 | 85.5 / 86.5 | 75.9 / 76.6 |
| MMMU [ 101 ] | 80.1 / 79.3 | 80.8 / 78.6 | 82.9 / 79.1 | 78.3 / 79.1 | 74.4 / 73.1 |
| MMMU-Pro [ 102 ] | 74.1 / 69.2 | 74.5 / 69.5 | 74.5 / 69.0 | 62.7 / 66.1 | 47.3 / 56.1 |
| VisualPuzzles [ 75 ] | 61.8 / 54.8 | 60.3 / 53.5 | 61.6 / 53.3 | 52.7 / 56.3 | 46.0 / 53.0 |
| VisuLogic [ 94 ] | 31.7 / 32.6 | 32.3 / 31.2 | 33.3 / 28.1 | 29.5 / 32.7 | 11.2 / 27.7 |
| ZeroBench (sub) [ 71 ] | 35.0 / 31.7 | 34.7 / 30.2 | 36.8 / 29.9 | 25.5 / 26.7 | 11.7 / 21.0 |
|  |  |  |  |  |  |
| General VQA |  |  |  |  |  |
| CCBench [ 59 ] | 78.2 / 79.8 | 76.1 / 77.5 | 76.5 / 73.9 | 82.4 / 81.2 | 61.4 / 61.6 |
| ChineseSimpleVQA [ 22 ] | 58.8 / 56.1 | 56.4 / 54.2 | 55.2 / 54.7 | 52.1 / 52.0 | 53.1 / 47.4 |
| CII-Bench [ 104 ] | 70.9 / 67.0 | 67.6 / 67.1 | 69.8 / 68.6 | 66.6 / 68.8 | 67.1 / 69.6 |
| MMBench EN-DEV-v1.1 [ 45 ] | 90.5 / 89.3 | 90.6 / 88.5 | 90.6 / 88.4 | 91.3 / 92.0 | 86.1 / 86.7 |
| MMBench CN-DEV-v1.1 [ 45 ] | 90.1 / 89.5 | 90.1 / 88.6 | 89.6 / 87.2 | 91.3 / 88.9 | 85.6 / 84.9 |
| MMStar [ 6 ] | 79.1 / 78.1 | 79.0 / 77.7 | 78.9 / 78.0 | 77.1 / 77.5 | 73.0 / 72.2 |
| MM-Vet [ 100 ] | 89.4 / 86.0 | 85.9 / 82.5 | 87.1 / 82.1 | 83.4 / 84.3 | 79.1 / 76.6 |
| PerceptionBench [ 40 ] | 41.5 / 38.4 | 43.6 / 37.3 | 42.9 / 36.6 | 34.2 / 35.8 | 32.4 / 34.4 |
| RealWorldQA [ 92 ] | 83.0 / 78.7 | 84.7 / 77.3 | 83.1 / 81.7 | 76.3 / 76.6 | 65.8 / 67.2 |
| SimpleVQA [ 9 ] | 67.6 / 60.8 | 62.9 / 59.5 | 60.7 / 58.3 | 61.0 / 58.4 | 56.4 / 54.0 |
| WorldVQA [ 110 ] | 23.4 / 24.0 | 26.8 / 23.1 | 27.2 / 24.8 | 15.7 / 16.1 | 14.9 / 14.0 |
|  |  |  |  |  |  |
| Documents and Charts |  |  |  |  |  |
| AI2D (test) [ 34 ] | 89.4 / 89.3 | 90.4 / 88.9 | 91.0 / 89.4 | 90.3 / 89.6 | 83.9 / 84.7 |
| CC-OCR [ 97 ] | 85.1 / 86.3 | 85.5 / 86.2 | 85.2 / 86.1 | 77.3 / 81.6 | 65.0 / 76.0 |
| ChartQAPro [ 55 ] | 68.9 / 67.2 | 68.2 / 66.3 | 68.2 / 64.4 | 64.4 / 65.6 | 58.9 / 63.0 |
| ChartQA (test) [ 54 ] | 91.0 / 88.4 | 91.2 / 86.8 | 91.0 / 87.0 | 89.4 / 86.9 | 87.5 / 83.4 |
| CharXiv (RQ) [ 88 ] | 76.8 / 70.4 | 77.8 / 69.9 | 75.0 / 69.6 | 67.9 / 68.3 | 63.6 / 62.8 |
| DocVQA (val) [ 56 ] | 97.7 / 96.9 | 97.5 / 96.6 | 97.3 / 96.0 | 96.5 / 94.6 | 89.9 / 90.3 |
| InfographicVQA (val) [ 57 ] | 92.8 / 91.2 | 93.0 / 90.7 | 93.2 / 91.3 | 85.8 / 84.9 | 70.7 / 67.0 |
| OCRBench [ 46 ] | 90.9 / 90.6 | 88.7 / 89.5 | 88.5 / 90.1 | 87.5 / 89.1 | 82.9 / 83.6 |
| OCRBench v2 [ 19 ] | 64.6 / 63.9 | 65.5 / 64.1 | 66.8 / 66.5 | 49.5 / 61.8 | 39.1 / 44.3 |
| OmniDocBench [ 60 ] | 90.6 / 92.7 | 89.6 / 88.6 | 91.5 / 90.3 | 77.6 / 92.0 | 3.1 / 27.0 |
| WildDoc [ 82 ] | 68.6 / 70.9 | 77.0 / 74.8 | 76.8 / 74.4 | 67.3 / 70.5 | 43.3 / 48.7 |
|  |  |  |  |  |  |
| Grounding and Counting |  |  |  |  |  |
| CountBenchQA [ 3 ] | 96.5 / 91.0 | 96.7 / 92.1 | 96.1 / 92.1 | 92.9 / 90.4 | 95.1 / 85.7 |
| CountQA [ 76 ] | 70.2 / 43.9 | 69.4 / 40.1 | 67.3 / 40.1 | 35.5 / 31.7 | 39.3 / 26.6 |
| MIHBench [ 37 ] | 83.1 / 79.1 | 82.4 / 60.0 | 81.6 / 63.9 | 81.3 / 81.5 | 75.8 / 44.0 |
| ODInW13 [ 38 ] | 48.6 / 44.5 | 45.0 / 48.8 | 50.8 / 50.4 | 26.3 / 27.8 | 35.3 / 33.0 |
| PixMo-Count [ 13 ] | 89.9 / 75.4 | 90.1 / 75.8 | 89.7 / 73.5 | 71.0 / 69.3 | 81.9 / 62.4 |
| RefCOCO (avg) [ 98 , 53 ] | 88.6 / 88.9 | 88.4 / 89.2 | 88.1 / 89.3 | 88.7 / 88.9 | 79.1 / 79.0 |
| Ref-L4 (val) [ 5 ] | 90.0 / 90.5 | 89.2 / 88.1 | 88.8 / 88.3 | 77.8 / 86.5 | 76.4 / 86.0 |
| TallyQA [ 1 ] | 83.1 / 82.6 | 80.3 / 81.5 | 79.7 / 81.3 | 81.2 / 80.6 | 78.8 / 79.0 |
|  |  |  |  |  |  |
| 2D/3D Spatial Understanding |  |  |  |  |  |
| CV-Bench [ 81 ] | 88.9 / 88.4 | 88.0 / 87.8 | 87.7 / 87.9 | 86.8 / 86.5 | 84.2 / 80.0 |
| EmbSpatial-Bench [ 16 ] | 83.7 / 78.9 | 83.9 / 79.3 | 84.1 / 79.3 | 82.7 / 82.2 | 78.5 / 70.3 |
| ERQA [ 77 ] | 56.5 / 48.8 | 61.0 / 50.3 | 58.5 / 52.3 | 55.0 / 49.8 | 47.0 / 45.3 |
| MMSI-Bench [ 96 ] | 39.1 / 32.8 | 40.2 / 32.2 | 41.4 / 32.4 | 29.4 / 35.1 | 27.1 / 28.8 |
| OmniSpatial [ 29 ] | 61.0 / 55.5 | 60.6 / 53.0 | 59.8 / 54.1 | 53.5 / 53.6 | 49.3 / 44.9 |
| SpatialMQA [ 44 ] | 58.5 / 47.5 | 58.9 / 45.3 | 58.1 / 47.1 | 50.9 / 47.5 | 57.8 / 44.5 |
|  |  |  |  |  |  |
| Multi-Image Understanding |  |  |  |  |  |
| BLINK [ 20 ] | 69.7 / 68.6 | 69.7 / 66.1 | 70.4 / 65.6 | 66.4 / 67.0 | 58.3 / 63.0 |
| Mantis-Eval [ 31 ] | 88.5 / 86.6 | 87.6 / 84.8 | 90.3 / 87.6 | 87.6 / 86.6 | 83.0 / 74.7 |
| MMIU [ 58 ] | 66.2 / 66.2 | 67.6 / 63.8 | 70.1 / 64.1 | 64.4 / 63.5 | 53.4 / 50.1 |
| MuirBench [ 83 ] | 70.9 / 71.0 | 73.2 / 62.0 | 74.7 / 73.7 | 72.2 / 65.5 | 57.8 / 60.0 |
|  |  |  |  |  |  |
| Instruction Following |  |  |  |  |  |
| CFBench [ 106 ] | 86.2 / 84.4 | 85.2 / 84.9 | 87.0 / 84.1 | 86.2 / 85.6 | 78.6 / 82.8 |
| IFBench [ 62 ] | 75.7 / 51.0 | 71.3 / 43.3 | 65.3 / 35.7 | 55.3 / 42.3 | 64.7 / 43.0 |
| IFEval [ 108 ] | 94.3 / 86.7 | 93.7 / 85.4 | 91.7 / 83.2 | 91.1 / 88.4 | 87.3 / 87.8 |
| MIA-Bench [ 64 ] | 87.2 / 83.8 | 86.8 / 82.8 | 87.2 / 85.1 | 83.7 / 86.2 | 83.1 / 81.3 |
| MM-IFEval [ 15 ] | 82.5 / 74.3 | 82.8 / 65.2 | 80.9 / 66.3 | 69.9 / 70.5 | 69.8 / 69.6 |
|  |  |  |  |  |  |
| Text-Centric Tasks |  |  |  |  |  |
| C-Eval [ 26 ] | 91.4 / 89.7 | 91.1 / 90.4 | 90.8 / 90.7 | 90.1 / 89.9 | 79.4 / 74.9 |
| GPQA (Diamond) [ 70 ] | 81.8 / 77.8 | 81.3 / 86.4 | 81.8 / 84.9 | 74.8 / 76.8 | 64.7 / 63.6 |
| HMMT (Nov. 2025) [ 14 ] | 87.5 / 84.2 | 86.7 / 69.2 | 88.3 / 67.5 | 78.3 / 65.8 | 66.7 / 64.2 |
| IMO-AnswerBench (v2) [ 51 ] | 73.3 / 62.5 | 74.0 / 58.3 | 75.3 / 59.8 | 67.3 / 56.5 | 52.5 / 50.8 |
| MMLU-Pro [ 87 ] | 85.3 / 84.1 | 85.7 / 84.3 | 85.3 / 84.5 | 84.5 / 84.6 | 65.7 / 80.9 |
| MMLU-Redux [ 21 ] | 93.5 / 91.3 | 93.5 / 88.8 | 93.4 / 93.5 | 93.3 / 93.4 | 86.0 / 90.2 |
| SuperGPQA [ 18 ] | 64.3 / 61.1 | 64.8 / 62.5 | 65.9 / 63.7 | 60.5 / 61.3 | 44.0 / 52.1 |
| Overall mean (64) | 76.4 / 72.6 | 76.2 / 71.0 | 76.3 / 71.2 | 70.5 / 70.8 | 62.4 / 62.4 |

## 原表 11

| Benchmark | WeMM-Ecom | Qwen3.5 | GLM-4.6V-Flash |  |  |  |
| --- | --- | --- | --- | --- | --- | --- |
| Size | 0.8B | 2B | 4B | 9B | 9B | 9B |
|  |  |  |  |  |  |  |
| STEM and Multimodal Reasoning |  |  |  |  |  |  |
| CMMMU (val) [ 105 ] | 41.8 / 34.4 | 55.6 / 51.3 | 65.4 / 59.9 | 69.9 / 66.2 | 70.9 / 65.1 | 61.1 / 53.0 |
| CMMU (val, MCQ) [ 23 ] | 53.7 / 46.3 | 76.2 / 72.4 | 89.1 / 84.3 | 91.2 / 88.6 | 91.8 / 87.9 | 80.4 / 70.7 |
| CSVQA [ 30 ] | 25.2 / 25.8 | 51.5 / 45.9 | 71.5 / 61.4 | 79.9 / 69.7 | 77.9 / 68.8 | 52.3 / 36.6 |
| DynaMath [ 111 ] | 60.0 / 49.2 | 76.8 / 71.8 | 82.4 / 78.3 | 83.9 / 80.3 | 81.4 / 74.0 | 73.6 / 63.5 |
| LogicVista [ 93 ] | 48.0 / 39.0 | 59.0 / 57.0 | 70.0 / 67.0 | 77.0 / 71.0 | 75.0 / 68.0 | 60.0 / 52.0 |
| MATH-Vision [ 84 ] | 27.4 / 27.5 | 52.2 / 50.0 | 70.1 / 65.2 | 76.3 / 70.9 | 77.7 / 69.7 | 55.9 / 42.1 |
| MathVista (mini) [ 49 ] | 68.1 / 66.1 | 80.2 / 79.0 | 86.2 / 82.6 | 86.5 / 83.9 | 84.6 / 83.3 | 83.0 / 72.7 |
| MMMU [ 101 ] | 54.0 / 42.7 | 65.7 / 63.3 | 75.6 / 72.7 | 79.1 / 76.7 | 78.7 / 75.1 | 72.3 / 67.2 |
| MMMU-Pro [ 102 ] | 35.1 / 31.5 | 51.9 / 49.8 | 65.4 / 62.4 | 69.8 / 64.9 | 69.3 / 66.0 | 56.9 / 47.8 |
| VisualPuzzles [ 75 ] | 32.3 / 31.3 | 40.4 / 41.7 | 49.2 / 50.2 | 56.9 / 53.8 | 58.1 / 49.0 | 42.0 / 42.6 |
| VisuLogic [ 94 ] | 24.0 / 25.7 | 26.6 / 25.8 | 29.4 / 26.7 | 32.0 / 28.9 | 34.2 / 29.7 | 26.6 / 15.3 |
| ZeroBench (sub) [ 71 ] | 15.3 / 11.4 | 21.9 / 18.3 | 26.7 / 29.0 | 33.5 / 28.1 | 32.3 / 29.3 | 24.0 / 16.5 |
|  |  |  |  |  |  |  |
| General VQA |  |  |  |  |  |  |
| CCBench [ 59 ] | 40.0 / 45.3 | 60.0 / 64.7 | 66.1 / 69.4 | 74.7 / 74.5 | 69.6 / 70.2 | 67.8 / 61.4 |
| ChineseSimpleVQA [ 22 ] | 17.6 / 18.9 | 32.1 / 29.4 | 45.5 / 41.4 | 49.7 / 48.5 | 44.3 / 45.7 | 50.2 / 44.6 |
| CII-Bench [ 104 ] | 38.4 / 37.8 | 48.9 / 48.4 | 61.3 / 56.6 | 65.6 / 64.4 | 65.6 / 63.6 | 57.0 / 54.8 |
| MMBench EN-DEV-v1.1 [ 45 ] | 73.1 / 73.0 | 85.0 / 83.0 | 87.5 / 86.7 | 90.2 / 89.6 | 88.2 / 86.2 | 86.2 / 82.8 |
| MMBench CN-DEV-v1.1 [ 45 ] | 72.0 / 70.3 | 83.5 / 81.6 | 87.6 / 87.3 | 89.4 / 88.9 | 87.2 / 85.4 | 86.3 / 83.0 |
| MMStar [ 6 ] | 62.9 / 58.0 | 72.3 / 71.3 | 76.5 / 75.7 | 80.2 / 77.6 | 77.7 / 74.6 | 73.2 / 68.1 |
| MM-Vet [ 100 ] | 66.0 / 62.6 | 75.6 / 72.0 | 81.5 / 76.3 | 85.9 / 80.3 | 80.0 / 76.9 | 77.4 / 76.1 |
| PerceptionBench [ 40 ] | 25.2 / 23.6 | 31.3 / 29.0 | 36.5 / 32.8 | 41.4 / 36.5 | 39.6 / 33.9 | 31.2 / 28.3 |
| RealWorldQA [ 92 ] | 68.1 / 66.1 | 75.6 / 71.6 | 77.7 / 78.2 | 81.1 / 77.0 | 80.5 / 74.1 | 75.8 / 72.2 |
| SimpleVQA [ 9 ] | 42.7 / 37.9 | 54.8 / 48.3 | 59.1 / 53.7 | 59.9 / 57.6 | 56.4 / 53.8 | 58.4 / 53.3 |
| WorldVQA [ 110 ] | 8.2 / 6.5 | 14.1 / 13.8 | 20.6 / 16.7 | 22.1 / 20.1 | 20.7 / 19.4 | 14.9 / 12.1 |
|  |  |  |  |  |  |  |
| Documents and Charts |  |  |  |  |  |  |
| AI2D (test) [ 34 ] | 73.9 / 73.1 | 83.7 / 82.7 | 87.8 / 86.2 | 89.4 / 88.3 | 89.4 / 86.8 | 84.7 / 84.8 |
| CC-OCR [ 97 ] | 73.6 / 77.6 | 80.6 / 81.8 | 82.4 / 84.6 | 84.7 / 85.6 | 84.3 / 85.3 | 63.7 / 62.8 |
| ChartQAPro [ 55 ] | 49.0 / 33.8 | 58.4 / 56.2 | 65.6 / 64.7 | 68.2 / 66.8 | 67.0 / 64.3 | 58.1 / 43.4 |
| ChartQA (test) [ 54 ] | 87.0 / 82.6 | 89.7 / 87.1 | 90.6 / 87.2 | 90.8 / 87.8 | 89.9 / 86.6 | 89.0 / 88.2 |
| CharXiv (RQ) [ 88 ] | 50.7 / 45.3 | 60.9 / 59.5 | 70.3 / 64.4 | 73.1 / 68.6 | 74.3 / 67.9 | 60.7 / 50.3 |
| DocVQA (val) [ 56 ] | 94.1 / 93.8 | 96.2 / 96.4 | 97.1 / 96.6 | 97.5 / 97.0 | 97.3 / 96.1 | 96.5 / 96.5 |
| InfographicVQA (val) [ 57 ] | 77.8 / 72.8 | 87.7 / 84.6 | 90.8 / 87.9 | 92.2 / 90.9 | 91.8 / 88.3 | 89.0 / 86.2 |
| OCRBench [ 46 ] | 80.6 / 84.6 | 88.0 / 89.0 | 86.2 / 86.7 | 89.8 / 90.6 | 87.8 / 85.2 | 85.4 / 85.3 |
| OCRBench v2 [ 19 ] | 50.1 / 48.2 | 56.3 / 51.3 | 60.8 / 57.9 | 65.6 / 60.9 | 64.0 / 62.1 | 53.2 / 50.3 |
| OmniDocBench [ 60 ] | 80.1 / 84.3 | 85.9 / 86.9 | 86.1 / 90.7 | 90.9 / 90.5 | 86.8 / 88.6 | 53.5 / 50.6 |
| WildDoc [ 82 ] | 61.3 / 54.7 | 67.7 / 52.8 | 67.7 / 65.5 | 70.4 / 69.2 | 71.8 / 70.4 | 70.0 / 64.6 |
|  |  |  |  |  |  |  |
| Grounding and Counting |  |  |  |  |  |  |
| CountBenchQA [ 3 ] | 75.8 / 72.1 | 90.0 / 85.1 | 93.3 / 84.5 | 95.5 / 90.8 | 97.0 / 87.8 | 90.6 / 83.1 |
| CountQA [ 76 ] | 18.3 / 12.4 | 37.0 / 31.2 | 46.8 / 33.3 | 65.3 / 38.6 | 61.8 / 37.4 | 35.9 / 27.6 |
| MIHBench [ 37 ] | 78.6 / 42.6 | 83.1 / 53.5 | 83.6 / 52.4 | 82.6 / 56.9 | 82.6 / 51.9 | 81.1 / 80.6 |
| ODInW13 [ 38 ] | 33.0 / 26.4 | 40.5 / 37.9 | 41.8 / 40.6 | 44.5 / 43.2 | 41.8 / 42.8 | 26.3 / 26.2 |
| PixMo-Count [ 13 ] | 52.9 / 42.0 | 75.6 / 70.0 | 80.9 / 63.7 | 87.8 / 68.3 | 87.6 / 74.2 | 73.9 / 57.6 |
| RefCOCO (avg) [ 98 , 53 ] | 76.8 / 78.8 | 82.8 / 81.9 | 85.2 / 84.8 | 86.4 / 86.3 | 86.9 / 86.2 | 84.1 / 83.8 |
| Ref-L4 (val) [ 5 ] | 78.6 / 83.6 | 85.8 / 87.5 | 86.0 / 89.0 | 89.5 / 90.0 | 88.1 / 88.2 | 88.2 / 88.2 |
| TallyQA [ 1 ] | 75.4 / 75.0 | 80.3 / 79.9 | 81.4 / 81.5 | 82.8 / 82.1 | 79.7 / 80.2 | 81.8 / 81.1 |
|  |  |  |  |  |  |  |
| 2D/3D Spatial Understanding |  |  |  |  |  |  |
| CV-Bench [ 81 ] | 80.3 / 76.4 | 86.1 / 86.1 | 88.0 / 86.3 | 88.8 / 87.0 | 88.3 / 86.1 | 86.1 / 83.5 |
| EmbSpatial-Bench [ 16 ] | 72.1 / 63.8 | 79.5 / 75.7 | 81.3 / 76.1 | 82.2 / 76.2 | 81.7 / 72.6 | 80.8 / 78.2 |
| ERQA [ 77 ] | 40.5 / 34.3 | 44.8 / 43.8 | 51.0 / 45.3 | 53.3 / 43.5 | 55.3 / 45.5 | 43.8 / 41.3 |
| MMSI-Bench [ 96 ] | 27.8 / 29.2 | 30.2 / 28.3 | 33.8 / 33.0 | 38.1 / 32.6 | 36.3 / 31.9 | 30.3 / 31.3 |
| OmniSpatial [ 29 ] | 43.3 / 40.8 | 49.1 / 51.0 | 54.1 / 50.9 | 56.2 / 53.2 | 56.5 / 48.0 | 48.8 / 45.7 |
| SpatialMQA [ 44 ] | 40.7 / 37.6 | 45.0 / 43.6 | 51.5 / 47.3 | 57.1 / 45.0 | 57.0 / 45.1 | 46.2 / 42.3 |
|  |  |  |  |  |  |  |
| Multi-Image Understanding |  |  |  |  |  |  |
| BLINK [ 20 ] | 57.9 / 52.8 | 64.2 / 63.8 | 66.1 / 65.8 | 68.5 / 68.1 | 68.9 / 65.2 | 66.0 / 64.0 |
| Mantis-Eval [ 31 ] | 76.0 / 57.1 | 82.5 / 81.6 | 87.1 / 83.0 | 88.0 / 81.6 | 87.6 / 82.0 | 83.4 / 77.4 |
| MMIU [ 58 ] | 54.1 / 46.0 | 61.3 / 58.5 | 65.8 / 63.6 | 68.8 / 64.5 | 67.0 / 59.8 | 62.4 / 59.4 |
| MuirBench [ 83 ] | 52.1 / 35.1 | 59.6 / 59.8 | 65.5 / 66.2 | 71.4 / 63.0 | 67.3 / 52.4 | 75.6 / 63.5 |
|  |  |  |  |  |  |  |
| Instruction Following |  |  |  |  |  |  |
| CFBench [ 106 ] | 64.6 / 57.4 | 78.0 / 70.0 | 84.5 / 80.5 | 84.5 / 81.3 | 84.7 / 83.0 | 81.8 / 74.5 |
| IFBench [ 62 ] | 29.7 / 28.0 | 45.3 / 33.3 | 56.3 / 32.7 | 68.0 / 50.7 | 69.3 / 40.0 | 28.3 / 22.0 |
| IFEval [ 108 ] | 69.9 / 60.8 | 84.8 / 73.9 | 89.3 / 79.9 | 91.5 / 82.3 | 92.4 / 84.5 | 63.4 / 57.3 |
| MIA-Bench [ 64 ] | 67.5 / 68.9 | 80.6 / 76.5 | 83.5 / 81.0 | 83.3 / 83.7 | 83.1 / 82.7 | 81.1 / 77.0 |
| MM-IFEval [ 15 ] | 56.0 / 48.2 | 67.3 / 58.5 | 77.9 / 68.2 | 81.1 / 70.5 | 81.3 / 64.8 | 66.1 / 57.7 |
|  |  |  |  |  |  |  |
| Text-Centric Tasks |  |  |  |  |  |  |
| C-Eval [ 26 ] | 58.3 / 52.5 | 74.8 / 69.9 | 85.8 / 81.9 | 88.2 / 86.3 | 88.0 / 86.7 | 84.7 / 77.6 |
| GPQA (Diamond) [ 70 ] | 35.4 / 36.4 | 60.1 / 54.6 | 71.7 / 67.2 | 75.8 / 75.8 | 78.3 / 78.8 | 41.4 / 42.4 |
| HMMT (Nov. 2025) [ 14 ] | 10.0 / 3.3 | 27.5 / 33.3 | 70.8 / 68.3 | 80.0 / 75.8 | 80.8 / 61.7 | 19.2 / 9.2 |
| IMO-AnswerBench (v2) [ 51 ] | 8.5 / 6.8 | 31.5 / 32.5 | 59.3 / 55.5 | 66.3 / 63.3 | 66.8 / 48.3 | 25.8 / 20.8 |
| MMLU-Pro [ 87 ] | 49.6 / 47.6 | 69.2 / 66.2 | 80.0 / 77.6 | 82.8 / 81.1 | 82.5 / 80.4 | 73.6 / 65.4 |
| MMLU-Redux [ 21 ] | 61.5 / 53.4 | 80.5 / 76.1 | 89.4 / 85.9 | 92.0 / 89.7 | 91.5 / 90.1 | 87.0 / 69.9 |
| SuperGPQA [ 18 ] | 25.9 / 23.8 | 40.8 / 36.7 | 53.7 / 49.5 | 58.7 / 55.2 | 58.6 / 55.3 | 45.9 / 34.8 |
| Overall mean (64) | 52.3 / 48.0 | 63.5 / 60.4 | 70.5 / 66.6 | 74.2 / 69.7 | 73.4 / 67.6 | 63.3 / 57.9 |

## 原表 12

|  | R det = 2 N ​ ∑ ( p , g ) ∈ 𝒫 IoU ⁡ ( p , g ) ​ w ​ ( p , g ) , R_{\mathrm{det}}=\frac{2}{N}\sum_{(p,g)\in\mathcal{P}}\operatorname{IoU}(p,g)\,w(p,g), |  | (6) |
| --- | --- | --- | --- |

## 原表 13

| Benchmark | Instances | Input and target | Primary metric |
| --- | --- | --- | --- |
| Product Knowledge |  |  |  |
| E-commerce Knowledge | 4,048 | Text questions about products, brands, and industry knowledge | Judged accuracy |
| Entity Recognition | 550 | Product image to product name, brand, and model | Acceptability |
| Product Attributes |  |  |  |
| Attribute Selection | 3,020 | Product image and candidate values to one attribute value | Accuracy |
| Attribute Extraction | 14,534 | Listing images, product fields, and options to attribute values | Reference-attribute accuracy |
| Brand Attribution | 6,122 | Listing images and fields, with optional brand candidates, to product brand | Accuracy |
| Brand Extraction | 3,000 | Listing images and product context to an extracted brand name | Accuracy |
| Product Moderation |  |  |  |
| Illegal Goods | 3,496 | Listing evidence and rules to an illegal-goods decision | Accuracy |
| Sales Restrictions | 1,050 | Listing evidence and rules to a restricted-sales decision | Accuracy |
| Image-Title Mismatch | 1,897 | Product title and images to the set of unrelated image indices | Exact-set accuracy |
| Product OCR |  |  |  |
| Product OCR | 19,962 | Single, multiple, or long product images to an answer about visible text | Mean judged accuracy |
| Product Retrieval |  |  |  |
| Region-level Retrieval | 15,335 | Two product crops to an ordinal similarity judgment | Normalized Spearman |
| Product-level Retrieval | 2,981 | Two product images and listing fields to a same-product judgment | Average precision |
| SKU-level Retrieval | 3,268 | Two textual SKU descriptions to a variant-equivalence decision | Match F1 |
| Product Grounding |  |  |  |
| Chart Detection | 1,456 | Listing image to chart and table boxes | Mean class F1 |
| Product Detection | 5,000 | Product image to boxes for the target product | Box F1 |
| Logo Detection | 1,500 | Product image to brand-logo boxes | Box F1 |
| Qualification Detection | 997 | Product image to typed certification-mark boxes | Mean class F1 |
| Dimension Detection | 994 | Product image to dimension-annotation boxes | Box F1 |
| Livestream Detection | 1,992 | Livestream frame to boxes for the advertised product | Box F1 |
| E-commerce Reasoning |  |  |  |
| Chart Reasoning | 2,000 | Rendered SKU, price, attribute, or constraint table to a derived answer | Mean accuracy |
| Category Reasoning | 500 | Product image and options to the requested category | Accuracy |
| Product Counting | 500 | Product arrangement and selection constraints to an item count | Accuracy |
| Spatial Reasoning | 500 | Product arrangement and relative-position constraints to a target item | Accuracy |
| E-commerce (Open) |  |  |  |
| ShoppingMMLU | 20,570 | Text tasks spanning shopping knowledge and e-commerce operations | Mean task score |
| RAIR | 48,835 | Query, item fields, and available images to a relevance grade | Macro F1 |
| ChineseEcomQA | 1,800 | Chinese e-commerce questions and task instructions to answers or labels | Mean task score |
| EcomMMMU (GTS) | 36,736 | Main product image and text to outputs for eight GTS tasks | GTS mean score |
| IndustryBench-MIPU | 4,474 | Multiple industrial-product images and a request to attribute values | Micro F1 |
| Each instance may contain several images, targets, or products. |  |  |  |