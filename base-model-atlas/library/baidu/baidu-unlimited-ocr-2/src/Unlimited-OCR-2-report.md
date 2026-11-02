# Unlimited OCR Works 2 — 2610.39308v2

原始HTML：https://arxiv.org/html/2610.39308v2

Unlimited OCR Works 2Pioneering the OCR-3.0 Era: From Long- to Unlimited-Horizon Parsing
Skip to main content
Report GitHub Issue
×
Title:
Content selection saved. Describe the issue below:
Description:
Submit without GitHub
Submit in GitHub
Why HTML?
Report Issue
Back to Abstract
Download PDF
Contents
Reading mode
Colour theme
Abstract
1
Introduction
2
Related Works
2.1
VLM-based Document Parsing
2.2
Efficient Long-Context Modeling
3
Methodology
3.1
Problem Setup
3.1.1
Unlimited-horizon Parsing
3.1.2
MarathonDocBench
3.2
Architecture
3.3
Sparse Reference Sliding Window Attention
3.3.1
Page Gate
3.3.2
Token Sieve
3.4
Unlimited-Horizon Decoding Paradigm
4
Experimental Settings
4.1
Data Engine
4.2
Implementation Details
5
Evaluation
5.1
Benchmarks and Metrics
5.2
Main Results
5.3
Scaling with Document Length
5.3.1
Feasibility of Unlimited-horizon Parsing
5.3.2
Length-Invariant Accuracy
5.3.3
Constant Per-Step Decoding Latency
6
Limitation and Future Work
7
Conclusion
8
Author List
References
License: CC BY 4.0
arXiv:2610.39308v2 [cs.CL] 30 Oct 2026
\reportnumber
001
Unlimited OCR Works 2
Pioneering the OCR-3.0 Era: From Long- to Unlimited-Horizon Parsing
Baidu ERNIE Team
Abstract
Unlimited OCR ushers the era of long-horizon parsing, substantially mitigating the growth of working memory as document lengthens. However, as document length scales to hundreds of pages, the visual context grows substantially, sharply increasing the computational cost of each decoding step and limiting the scalability of ultra-long document parsing. Inspired by human book transcription via localized focus without re-scanning preceding pages, we introduce Unlimited OCR 2, a document parsing model that looks only at what it transcribes. Building on Unlimited OCR, we upgrade all the decoder attention modules to Sparse Reference Sliding Window Attention (SR-SWA), bounding active reference tokens to a fixed capacity and thus sustaining constant computational costs across arbitrarily long documents. By combining SR-SWA with Unlimited-Horizon Decoding Paradigm, Unlimited OCR 2 enables document parsing over virtually unlimited lengths without prohibitive memory overhead. At the hundred-page scale, Unlimited OCR 2 achieves 7.0
×
\times
and 5.6
×
\times
per-step speedups over Full Attention and R-SWA, respectively. Furthermore, it delivers state-of-the-art end-to-end performance on both MPDocBench and MarathonDocBench, our newly proposed benchmark targeting hundred-page document parsing. Ultimately, the capacity for uninterrupted, one-shot document parsing signifies a fundamental paradigm shift into the OCR 3.0 era.
Figure 1
:
R-SWA vs SR-SWA. R-SWA computes attention over all visual tokens across pages, inducing extreme visual redundancy; SR-SWA sparsely attends to relevant visual regions, aligning machine decoding with human reading intuition.
Contents
1
Introduction
2
Related Works
2.1
VLM-based Document Parsing
2.2
Efficient Long-Context Modeling
3
Methodology
3.1
Problem Setup
3.1.1
Unlimited-horizon Parsing
3.1.2
MarathonDocBench
3.2
Architecture
3.3
Sparse Reference Sliding Window Attention
3.3.1
Page Gate
3.3.2
Token Sieve
3.4
Unlimited-Horizon Decoding Paradigm
4
Experimental Settings
4.1
Data Engine
4.2
Implementation Details
5
Evaluation
5.1
Benchmarks and Metrics
5.2
Main Results
5.3
Scaling with Document Length
5.3.1
Feasibility of Unlimited-horizon Parsing
5.3.2
Length-Invariant Accuracy
5.3.3
Constant Per-Step Decoding Latency
6
Limitation and Future Work
7
Conclusion
8
Author List
References
1
Introduction
“Pixels are my body, and tokens are my blood. I have parsed over a thousand pages. Unknown to KV cache. Nor known to context limits. So, as I pray: Unlimited OCR Works.”
Snarcy on huggingface ( Adapted from
UBW
)
Document parsing has undergone a major paradigm shift, transitioning from traditional multi-stage pipelines (OCR-1.0)
[
5
,
40
,
6
,
22
,
26
,
20
,
8
]
with handcrafted detection and recognition modules to end-to-end Vision-Language Models (OCR-2.0)
[
19
,
7
,
21
,
31
,
18
]
. By formulating document understanding as a unified sequence-to-sequence transcription task, OCR-2.0 frameworks effectively eliminate cumulative pipeline errors. Our previous work, Unlimited OCR
[
37
]
, pushed OCR-2.0 boundaries to tens of pages by using Reference Sliding Window Attention (R-SWA) to maintain a constant KV cache. Nevertheless, it still computes attention over all visual tokens across pages during decoding. As document length scales, this persistent attention to non-informative visual tokens severely escalates visual redundancy, compounding the difficulty of end-to-end inference. This visual attention bottleneck naturally prompts a fundamental question: how can we transition from length-limited parsing to an unlimited one-shot paradigm and genuinely inaugurate the OCR-3.0 era?
To answer this question, human transcription of lengthy books provides a clear physical intuition for parsing scaling: as we copy text page by page, we maintain localized visual focus, casting only momentary glances back when cross-page references are needed, rather than keeping the entire volume active in mind. This cognitive mechanism reveals that visual dependencies in multi-page documents are inherently page-sparse yet intra-page concentrated. However, standard dense global attention completely overlooks this sparse dynamic, incurring redundant attention interactions across all pages. This not only incurs prohibitive computational overhead, but also leads to severe memory bottlenecks as document length scales. To break through these efficiency and memory bottlenecks, we align machine perception with human reading patterns and present Unlimited OCR 2, pioneering an unlimited-horizon parsing framework for the OCR-3.0 era. Our main contributions are as follows:
•
We introduce Sparse Reference Sliding Window Attention (SR-SWA), a hierarchical sparse attention mechanism designed for unlimited visual context. Specifically, Page Gate first narrows each query’s visual reference scope from the entire document to relevant pages while robustly modeling multi-page positional relationships. Token Sieve selectively incorporates top-
k
k
remote token buckets to capture long-range visual dependencies, thereby drastically reducing attention overhead while preserving comprehensive context.
•
We introduce MarathonDocBench, a benchmark for hundred-page document parsing. It substantially extends existing evaluations in document length and cross-page structural complexity, enabling a comprehensive assessment of long-document parsing performance in the hundred-page regime.
•
Comprehensive evaluations in long-horizon settings demonstrate that our approach maintains constant per-step decoding latency regardless of document length while achieving state-of-the-art end-to-end performance on multi-page benchmarks. Building on these advances, we establish an efficient unlimited-horizon parsing paradigm by integrating SR-SWA with the Unlimited-Horizon Decoding Paradigm, enabling document parsing over virtually unlimited lengths.
In summary, SR-SWA fundamentally breaks the computational and memory bottlenecks of ultra-long visual context. Operating at constant per-step decoding latency with length-invariant accuracy across hundreds of pages, Unlimited OCR 2 unlocks scalable long-document parsing and paves the way for the OCR-3.0 era of unlimited-horizon understanding.
2
Related Works
2.1
VLM-based Document Parsing
Document parsing has increasingly been reshaped by advances in vision-language models, evolving from pipeline-based OCR-1.0 systems
[
5
,
40
,
6
,
22
,
26
,
20
,
8
]
, which combine specialized page analysis modules with VLM-based decoding, to unified VLM-based OCR-2.0 systems that directly generate structured representations from document images. OCR-2.0 encompasses both single-page parsers
[
19
,
7
,
30
,
21
,
31
,
18
]
and Unlimited OCR
[
37
]
, which extends end-to-end parsing to multi-page documents by jointly modeling their visual content within a shared context. However, although Unlimited OCR improves long-document efficiency with R-SWA, it still densely attends to all remote visual tokens, causing the visual context accessible to each decoding query to expand with document length and creating a fundamental scalability bottleneck at the hundred-page scale. Unlimited OCR 2 overcomes this limitation by explicitly bounding remote visual access, enabling attention-efficient end-to-end parsing of hundred-page documents and advancing document parsing into the OCR-3.0 era.
2.2
Efficient Long-Context Modeling
Efficient long-context modeling has been explored through both attention replacement and sparse attention. Linear or recurrent alternatives
[
11
,
35
,
15
,
36
,
17
]
reduce long-context cost by summarizing historical information into compact states. Document parsing, however, requires long-range memory to preserve fine-grained visual evidence for accurate recognition and cross-page retrieval, which may not be fully retained within such compact representations.
Sparse attention retains direct access to selected historical tokens or KV blocks while avoiding dense all-to-all computation. Early methods use predefined patterns such as local windows and global tokens
[
2
,
39
]
, whereas recent approaches adopt query-dependent retrieval. Hard-selection methods, such as Compressed Sparse Attention(CSA)
[
33
]
and MiniMax Sparse Attention(MSA)
[
16
]
, rely on discrete top-
k
k
routing and typically require auxiliary supervision or warmup. In contrast, DashAttention
[
13
]
and HiLS
[
12
]
incorporate differentiable or forward-integrated routing scores, enabling more direct end-to-end optimization.
3
Methodology
3.1
Problem Setup
3.1.1
Unlimited-horizon Parsing
Unlimited-horizon parsing aims to enable end-to-end processing of documents of arbitrary lengths, from single-page forms to massive multi-page documents, with bounded computational and memory complexities.
Formally, multi-page document parsing generates a transcription
𝒴
=
(
y
1
,
…
,
y
L
)
\mathcal{Y}=(y_{1},\ldots,y_{L})
from an ordered document
𝒟
=
(
P
1
,
…
,
P
N
)
\mathcal{D}=(P_{1},\ldots,P_{N})
with visual tokens
𝒱
1
:
N
\mathcal{V}_{1:N}
. At decoding step
t
t
, the model operates on:
𝒳
t
=
Concat
⁡
(
𝒱
1
,
…
,
𝒱
N
,
y
<
t
)
.
\mathcal{X}_{t}=\operatorname{Concat}\left(\mathcal{V}_{1},\ldots,\mathcal{V}_{N},y_{<t}\right).
(1)
While Unlimited OCR constrained text history to a fixed sliding window via R-SWA, it still requires attending over all preceding visual tokens
𝒱
1
:
N
\mathcal{V}_{1:N}
. In the hundred-page regime, this page-dependent visual expansion becomes the primary bottleneck. Decoupling visual context from page count
N
N
to maintain a bounded computational and memory footprint directly motivates our proposed Sparse Reference Sliding Window Attention (SR-SWA).
Figure 2
:
MarathonDocBench versus MPDocBench. MarathonDocBench extends document length from tens to hundreds of pages (a), with substantially richer cross-page structures as shown in (b) and (c).
3.1.2
MarathonDocBench
Existing multi-page document parsing benchmarks neither extend to the hundred-page scale nor sufficiently capture the rich cross-page structures that emerge in long documents. To address this gap, we introduce MarathonDocBench, the first benchmark specifically designed for hundred-page document parsing. It contains 100 documents spanning 103–300 pages with 205k annotated layout elements, extending the document-length range by roughly an order of magnitude beyond MPDocBench
[
41
]
.
Beyond document length, MarathonDocBench contains substantially richer cross-page structures than MPDocBench, with cross-page text and tables appearing much more frequently and densely across documents, as summarized in Figure
2
. This makes MarathonDocBench a substantially more challenging testbed for evaluating whether end-to-end parsers can preserve document-level structure while scaling from tens to hundreds of pages. To ensure reliable evaluation, structural annotations, including bounding boxes, block type, hierarchy, reading order, and cross-page continuations of text and tables, are initialized from a strong page-by-page parser and carefully refined by human annotators. Content transcriptions are initialized from the same parser outputs and verified through an iterative VLM-based refinement pipeline, with flagged disagreements adjudicated by human annotators.
3.2
Architecture
Figure 3
:
Inspired by the process of humans copying books, we propose Unlimited OCR 2. SR-SWA combines Page Gate and Token Sieve to construct a fixed-length set of working reference visual tokens, substantially reducing computational and memory overhead while keeping both independent of document length throughout generation.
Unlimited OCR 2 inherits the fundamental backbone from Unlimited OCR, leveraging DeepSeek OCR
[
28
]
as its foundation. Specifically, it employs the DeepEncoder paired with a Mixture-of-Experts (MoE) decoder architecture featuring 3B total parameters and 500M activated parameters per token. Building upon this base, we replace the baseline R-SWA with our proposed SR-SWA as shown in Figure
3
. While R-SWA bounds local interactions, its visual context scope still expands with growing document length, leading to noticeable latency accumulation over ultra-long horizons. By introducing a selective remote visual routing mechanism, SR-SWA strictly bounds the active context scope, enabling Unlimited OCR 2 to maintain a constant KV cache footprint across both text and visual modalities during unlimited-horizon decoding. We detail the inner mechanics of SR-SWA in the following subsections.
3.3
Sparse Reference Sliding Window Attention
Following standard block-sparse attention
[
16
,
13
,
33
,
32
]
,
we partition
𝒳
t
\mathcal{X}_{t}
into fixed-size blocks
{
ℬ
b
}
b
=
1
B
\{\mathcal{B}_{b}\}_{b=1}^{B}
and preserve a fixed local window
ℒ
⁡
(
q
)
\mathcal{L}(q)
for each query
q
q
.
SR-SWA constructs
𝒮
⁡
(
q
)
\mathcal{S}(q)
hierarchically,
using Page Gate for page-level organization and Token Sieve for fixed-budget selection.
3.3.1
Page Gate
To eliminate irrelevant visual tokens and concentrate focus on the current page, Page Gate restricts the visual attention scope for a query
q
q
associated with page
g
⁡
(
q
)
g(q)
by retaining only blocks from designated target pages:
𝒞
page
​
(
q
)
=
{
b
|
ℬ
b
∩
𝒱
g
⁡
(
q
)
≠
∅
}
.
\mathcal{C}_{\mathrm{page}}(q)=\left\{b\;\middle|\;\mathcal{B}_{b}\cap\mathcal{V}_{g(q)}\neq\emptyset\right\}.
(2)
Since block boundaries are independent of page boundaries, a candidate block may straddle adjacent pages. Meanwhile, to prevent positional explosion as page count scales, Page Gate factorizes each token position into a bounded page-level coordinate (following an alternating
0
0
–
1
1
pattern) and a monotonic intra-page coordinate:
𝐩
i
,
j
=
[
𝐩
i
page
,
𝐩
i
,
j
intra
]
,
\mathbf{p}_{i,j}=\left[\mathbf{p}^{\mathrm{page}}_{i},\;\mathbf{p}^{\mathrm{intra}}_{i,j}\right],
(3)
ensuring both stable length extrapolation and efficient cross-page visual routing.
3.3.2
Token Sieve
While Page Gate restricts the routing space across pages, efficient fixed-budget routing requires a principled block selection strategy. Conventional sparse routers typically rely on dense-attention distillation, which lacks direct alignment with the language modeling objective. Inspired by recent end-to-end routing designs
[
13
,
12
]
, Token Sieve directly optimizes fixed-budget block selection under the language modeling objective.
Given the candidate set
𝒞
page
​
(
q
)
\mathcal{C}_{\mathrm{page}}(q)
from Page Gate, Token Sieve summarizes each candidate block
b
b
into a compact key representation
𝐤
¯
b
\bar{\mathbf{k}}_{b}
and computes its relevance to query
q
q
. The router then forms a sparse routing distribution and retains only the top-
k
k
blocks:
s
b
​
(
q
)
\displaystyle s_{b}(q)
=
𝐪
~
⊤
​
𝐤
¯
b
d
,
𝝅
(
q
)
=
α
-entmax
(
{
s
b
(
q
)
}
b
∈
𝒞
page
​
(
q
)
)
,
\displaystyle=\frac{\tilde{\mathbf{q}}^{\top}\bar{\mathbf{k}}_{b}}{\sqrt{d}},\qquad\boldsymbol{\pi}(q)=\alpha\text{-entmax}\left(\{s_{b}(q)\}_{b\in\mathcal{C}_{\mathrm{page}}(q)}\right),
(4)
𝒮
⁡
(
q
)
\displaystyle\mathcal{S}(q)
=
TopK
⁡
(
𝝅
⁡
(
q
)
,
k
)
.
\displaystyle=\operatorname{TopK}\big(\boldsymbol{\pi}(q),k\big).
Here,
d
d
denotes the hidden dimension. By selectively attending to a fixed number of top-
k
k
remote buckets, Token Sieve captures long-range visual dependencies with minimal computational overhead. To preserve relative preferences among selected blocks, the routing probabilities are converted into a mean-centered log-prior:
β
b
​
(
q
)
=
log
⁡
π
b
​
(
q
)
−
1
|
𝒮
⁡
(
q
)
|
​
∑
b
′
∈
𝒮
⁡
(
q
)
log
⁡
π
b
′
​
(
q
)
,
b
∈
𝒮
⁡
(
q
)
.
\beta_{b}(q)=\log\pi_{b}(q)-\frac{1}{|\mathcal{S}(q)|}\sum_{b^{\prime}\in\mathcal{S}(q)}\log\pi_{b^{\prime}}(q),\qquad b\in\mathcal{S}(q).
(5)
With the selected remote blocks
𝒮
⁡
(
q
)
\mathcal{S}(q)
and the fixed local window
ℒ
⁡
(
q
)
\mathcal{L}(q)
, each query attends to a length-agnostic retained token set defined as:
ℛ
⁡
(
q
)
=
ℒ
⁡
(
q
)
∪
⋃
b
∈
𝒮
⁡
(
q
)
ℬ
b
.
\mathcal{R}(q)=\mathcal{L}(q)\cup\bigcup_{b\in\mathcal{S}(q)}\mathcal{B}_{b}.\vskip-5.69046pt
(6)
The attention weights over
ℛ
⁡
(
q
)
\mathcal{R}(q)
are computed as:
α
j
(
q
)
=
Softmax
(
q
⊤
​
k
j
d
+
𝕀
[
b
(
j
)
∈
𝒮
(
q
)
]
β
b
⁡
(
j
)
(
q
)
)
,
\alpha_{j}(q)=\operatorname{Softmax}\left(\frac{q^{\top}k_{j}}{\sqrt{d}}+\mathbb{I}\!\left[b(j)\in\mathcal{S}(q)\right]\beta_{b(j)}(q)\right),
(7)
where the softmax is normalized over all tokens in
ℛ
⁡
(
q
)
\mathcal{R}(q)
,
b
⁡
(
j
)
b(j)
denotes the block containing token
j
j
, and
k
j
k_{j}
denotes its key projection. Tokens within the local window use standard attention logits, while tokens from selected remote blocks additionally incorporate the corresponding routing bias. Since the routing bias directly participates in these logits, gradients from the parsing objective can propagate to the routing module, enabling end-to-end optimization without an auxiliary KL-divergence distillation loss.
Algorithm 1
Cross-Chunk KV Reuse for Unlimited-Horizon Decoding
1:
Pages
P
1
,
…
,
P
N
P_{1},\dots,P_{N}
; instruction
q
q
; chunk size
W
W
; tail length
T
T
2:
Transcription
Y
Y
3:
Notation:
𝒞
\mathcal{C}
is a KV cache;
⊕
\oplus
concatenates KV in order;
4:
Enc
​
(
X
∣
𝒞
)
\textsc{Enc}(X\mid\mathcal{C})
returns the KV of input
X
X
computed with
𝒞
\mathcal{C}
as context.
5:
Partition
N
N
pages into
K
K
overlapping chunks
C
1
,
…
,
C
K
C_{1},\dots,C_{K}
with a 1-page boundary overlap
⊳
\triangleright
K
=
1
K{=}1
indicates unsegmented
6:
𝒞
←
Enc
​
(
C
1
⊕
q
)
\mathcal{C}\leftarrow\textsc{Enc}(C_{1}\oplus q)
⊳
\triangleright
only the first chunk carries
q
q
7:
y
1
←
Decode
​
(
𝒞
)
y_{1}\leftarrow\textsc{Decode}(\mathcal{C})
;
Y
←
y
1
Y\leftarrow y_{1}
8:
for
k
=
2
k=2
to
K
K
do
9:
𝒞
←
𝒞
overlap
img
⊕
Enc
​
(
C
k
∣
𝒞
overlap
img
)
⊕
𝒞
tail
txt
\mathcal{C}\leftarrow\mathcal{C}^{\mathrm{img}}_{\text{overlap}}\oplus\textsc{Enc}(C_{k}\mid\mathcal{C}^{\mathrm{img}}_{\text{overlap}})\oplus\mathcal{C}^{\mathrm{txt}}_{\text{tail}}
10:
y
k
←
Decode
​
(
𝒞
)
y_{k}\leftarrow\textsc{Decode}(\mathcal{C})
;
Y
←
Y
⊕
y
k
Y\leftarrow Y\oplus y_{k}
11:
end
for
12:
return
Y
Y
Figure 4
:
Comparison of (a) standard decoding and (b) our Unlimited-Horizon Decoding paradigm. Standard decoding retains visual KV caches for all pages, causing GPU memory usage to grow linearly with document length and eventually overflow. Our paradigm divides long documents into manageable chunks and processes them sequentially, reusing the KV cache of shared boundary pages and releasing inactive caches to keep GPU memory usage bounded while preserving cross-chunk continuity.
3.4
Unlimited-Horizon Decoding Paradigm
While SR-SWA bounds the number of reference tokens accessed by each query, processing extremely long multi-page documents remains constrained by the GPU memory required to prefill and retain their visual KV caches. As illustrated in Figure
4
, conventional all-at-once prefill keeps all page-level visual KV caches in memory, causing the memory footprint to grow linearly with document length. To overcome this limitation, we introduce the Unlimited-Horizon Decoding Paradigm, which partitions the document into overlapping page-level chunks and processes them sequentially. Adjacent chunks share their boundary page, whose KV cache is directly reused to preserve cross-chunk continuity, while visual KV caches outside the active chunk are released. Consequently, only a fixed-size chunk remains resident in GPU memory, bounding the memory footprint independently of the total document length. The complete procedure is formally described in Algorithm
1
.
4
Experimental Settings
4.1
Data Engine
To train Unlimited OCR 2 for versatile document parsing, we construct a large-scale multimodal corpus comprising
2
​
M
2\text{M}
multi-page and
10
​
M
10\text{M}
single-page documents. Pseudo-labels across both single- and multi-page subsets are extracted from MinerU2.5-Pro
[
26
]
and PaddleOCR-VL-v1.6
[
40
]
, tailored to their respective domain strengths. To enrich visual and layout diversity, we additionally incorporate versatile synthetic document generation pipelines. Across both real and synthetic data, we leverage VLM-based multi-dimensional feature analysis to conduct balance filtering, ensuring uniform coverage over complex layout distributions. Finally, to explicitly fortify structural hierarchy and cross-page continuity in multi-page scenarios, we apply MinerU-Popo
[
34
]
refinement alongside dedicated heuristic post-processing rules to reconcile layout inconsistencies across adjacent page boundaries.
4.2
Implementation Details
We initialize Unlimited OCR 2 from the Unlimited OCR checkpoint and perform post-training for 1 epoch on the curated dataset. Training is conducted on a cluster of
25
×
8
25\times 8
GPU NVIDIA H800 nodes with a global batch size of 1,600 and a maximum sequence length of 64K tokens. During training, we freeze both the DeepEncoder and the aligner, optimizing only the LLM parameters. Optimization is carried out using the AdamW optimizer with a cosine learning rate decay schedule, starting at an initial learning rate of
2.5
×
10
−
4
2.5\times 10^{-4}
. The entire training workflow is implemented using the MS-Swift framework. For deployment, the Unlimited-Horizon Decoding Paradigm is integrated into SGLang to facilitate efficient long-document inference.
5
Evaluation
5.1
Benchmarks and Metrics
Figure 5
:
Performance comparison on multi-page benchmarks. Unlimited OCR 2 (Ours) consistently achieves state-of-the-art performance across all evaluation categories.
Table 1
:
Performance comparison on MPDocBench. All models in the table are end-to-end
VLM-based architectures.
Method
Overall
↑
\uparrow
Text
Edit
↓
{}^{\mathrm{Edit}}\downarrow
T-Text
Edit
↓
{}^{\mathrm{Edit}}\downarrow
Formula
CDM
↑
{}^{\mathrm{CDM}}\uparrow
Table
TEDS
↑
{}^{\mathrm{TEDS}}\uparrow
T-Table
TEDS
↑
{}^{\mathrm{TEDS}}\uparrow
Figure
F1
↑
{}^{\mathrm{F1}}\uparrow
ReadOrder
Edit
↓
{}^{\mathrm{Edit}}\downarrow
Heading
TEDS
↑
{}^{\mathrm{TEDS}}\uparrow
General VLMs
Gemini-3.1-Pro Preview
[
9
]
71.79
0.070
0.232
88.37
81.68
61.26
59.08
0.127
26.94
Qwen3.8-Max
[
25
]
78.30
0.057
0.196
89.24
85.89
67.18
70.19
0.097
48.80
Kimi-K3
[
24
]
60.77
0.162
0.551
41.16
75.45
81.57
40.47
0.206
39.30
Qwen3.6-plus
[
25
]
72.14
0.096
0.245
88.77
82.99
60.50
64.80
0.179
32.06
Qwen3-VL-235B
[
1
]
73.98
0.087
0.187
84.71
81.35
61.25
63.25
0.136
42.34
InternVL-3.5-38B
[
27
]
57.01
0.133
0.515
84.30
69.86
51.69
7.97
0.199
27.01
Minimax-M3
[
16
]
62.65
0.167
0.422
81.30
77.91
76.51
7.18
0.231
40.39
Gemini-3.8-Flash
[
10
]
76.25
0.081
0.122
83.27
83.15
87.41
62.86
0.294
43.05
Qwen-3.8-Flash-Next
[
25
]
77.36
0.078
0.163
86.70
86.24
88.36
64.31
0.277
45.09
DeepSeek-4.1-Flash
[
32
]
66.25
0.114
0.451
82.12
80.14
87.72
35.55
0.312
32.10
GLM-5.3-Flash
[
38
]
68.02
0.111
0.344
81.86
83.70
70.71
43.09
0.288
39.09
Specialized VLMs (OCR-2.0)
Unlimited-OCR
[
37
]
61.89
0.167
0.605
73.71
73.51
60.76
53.19
0.204
31.58
Specialized VLMs (OCR-3.0)
Unlimited-OCR 2 (Ours)
84.59
0.052
0.100
89.39
87.78
89.54
72.91
0.077
60.10
Table 2
:
Performance comparison on MarathonDocBench. Unlimited OCR is not reported on MarathonDocBench due to its 40-page input limitation.
Method
Overall
↑
\uparrow
Text
Edit
↓
{}^{\mathrm{Edit}}\downarrow
T-Text
Edit
↓
{}^{\mathrm{Edit}}\downarrow
Formula
CDM
↑
{}^{\mathrm{CDM}}\uparrow
Table
TEDS
↑
{}^{\mathrm{TEDS}}\uparrow
T-Table
TEDS
↑
{}^{\mathrm{TEDS}}\uparrow
Figure
F1
↑
{}^{\mathrm{F1}}\uparrow
ReadOrder
Edit
↓
{}^{\mathrm{Edit}}\downarrow
Heading
TEDS
↑
{}^{\mathrm{TEDS}}\uparrow
General VLMs
Gemini-3.1-Pro Preview
[
9
]
26.97
0.516
0.764
30.44
28.48
21.71
18.94
0.654
9.68
Qwen3.8-Max
[
25
]
22.93
0.600
0.804
18.82
15.20
13.71
33.39
0.733
16.09
Kimi-K3
[
24
]
33.74
0.475
0.664
40.50
27.80
26.30
21.38
0.611
28.90
Minimax-M3
[
16
]
17.97
0.659
0.818
14.20
17.79
14.84
3.67
0.763
17.16
Gemini-3.8-Flash
[
10
]
28.61
0.519
0.658
26.35
23.40
19.56
18.62
0.687
27.34
Qwen-3.8-Flash-Next
[
25
]
27.83
0.544
0.753
28.31
25.38
21.04
24.07
0.679
21.50
DeepSeek-4.1-Flash
[
32
]
12.34
0.740
0.933
10.45
12.74
12.59
6.95
0.843
7.62
GLM-5.3-Flash
[
38
]
7.51
0.860
0.936
4.50
7.12
6.65
7.10
0.923
6.55
Specialized VLMs (OCR-3.0)
Unlimited-OCR 2 (Ours)
77.06
0.104
0.123
87.93
74.81
71.11
71.79
0.147
48.20
To comprehensively evaluate Unlimited OCR 2 on document parsing across varying lengths, we conduct experiments on two challenging multi-page benchmarks: MPDocBench
[
41
]
(up to 30 pages) and our proposed MarathonDocBench (ranging from 100 to 300 pages). Following the official evaluation protocol of MPDocBench, we report Edit Distance for textual content and reading order recognition, TEDS for table structure recognition, CDM for mathematical formula recognition, and F1 score for figure region detection. To further evaluate cross-page consistency, we include T-TextEdit and T-TEDS to assess text and table parsing across page boundaries, respectively. An overall score aggregated across these fine-grained structural categories is also computed to summarize overall parsing performance.
Table 3
:
Comparison on OmniDocBench v1.6. All models in the table are end-to-end VLM-based architectures.
Model
Size
Overall
↑
\uparrow
Text
Edit
{}^{\text{Edit}}
↓
\downarrow
Formula
CDM
{}^{\text{CDM}}
↑
\uparrow
Table
TEDs
{}^{\text{TEDs}}
↑
\uparrow
Table
TEDS-S
{}^{\text{TEDS-S}}
↑
\uparrow
ReadOrder
Edit
{}^{\text{Edit}}
↓
\downarrow
HunyuanOCR
[
23
]
1B
89.95
0.088
87.68
91.01
92.23
0.171
DeepSeek-OCR 2
[
29
]
3B-A0.5B
90.25
0.050
91.84
83.89
87.75
0.144
dots.ocr
[
19
]
3B
90.77
0.048
89.95
87.18
90.58
0.138
FireRed-OCR
[
31
]
2B
93.26
0.037
95.44
88.04
91.06
0.131
ABot-OCR
[
14
]
2B
93.30
0.037
94.86
88.69
91.87
0.137
Logics-Parsing-v2
[
4
]
4B
93.33
0.041
95.65
88.42
91.98
0.137
Qianfan-OCR
[
7
]
4B
93.90
0.040
95.08
90.53
93.31
0.130
OvisOCR2
[
21
]
0.8B
96.47
0.027
97.49
94.58
96.98
0.112
TeleOCR
[
3
]
1.2B
96.91
0.027
96.60
96.82
98.18
0.118
Unlimited-OCR
[
37
]
3B-A0.5B
93.92
0.042
95.79
90.16
93.32
0.129
Unlimited-OCR 2
3B-A0.5B
94.02
0.038
96.29
89.60
92.70
0.128
5.2
Main Results
As visually summarized in Figure
6
and further detailed in Table
1
and Table
2
, Unlimited OCR 2 takes a significant step toward the OCR 3.0 era, advancing document parsing along three key dimensions. First, it establishes the practical feasibility of hundred-page end-to-end parsing, achieving a score of 77.06 on MarathonDocBench and demonstrating its ability to handle documents at a scale beyond conventional multi-page settings. Second, it maintains robust parsing performance as document length increases. Through end-to-end modeling with SR-SWA, Unlimited OCR 2 filters redundant visual tokens while preserving relevant cross-page information, achieving the highest Overall scores and state-of-the-art performance on both cross-page text and table metrics, T-Text and T-Table, respectively, from dozens of pages on MPDocBench to hundreds of pages on MarathonDocBench. Third, it establishes a new state-of-the-art in long-document parsing, outperforming leading closed-source models and top-tier open-source MLLMs across these benchmarks. Furthermore, Unlimited OCR 2 retains strong single-page recognition capabilities, achieving an Overall score of 94.02% on OmniDocBench in Table
3
, confirming that its sparse attention design preserves fine-grained local recognition.
Table 4
:
Feasibility evaluation of the Unlimited-Horizon Decoding Paradigm. Sequential chunk processing reduces peak KV cache memory at
B
=
1
B=1
and improves end-to-end throughput at
B
=
16
B=16
, enabling hundred-page parsing under constrained GPU memory.
Method
Peak KV Memory (
B
=
1
B=1
)
TPS (
B
=
16
B=16
)
Standard Decoding
47.00 GB
360
Unlimited-Horizon Decoding
1.77 GB
1315
5.3
Scaling with Document Length
5.3.1
Feasibility of Unlimited-horizon Parsing
Benefiting from SR-SWA and the Unlimited-Horizon Decoding Paradigm, Unlimited OCR 2 enables efficient parsing of extremely long documents under constrained GPU memory. We evaluate its feasibility on the hundred-page MarathonDocBench benchmark by measuring peak KV cache memory and end-to-end throughput, as reported in Table
4
. Compared with standard decoding, page-level chunking with boundary-page KV cache reuse reduces peak KV cache memory from 47.00 GB to 1.77 GB under single-sequence inference (
B
=
1
B=1
). Meanwhile, end-to-end throughput increases from 360 to 1,315 TPS under concurrent inference with
B
=
16
B=16
. These results demonstrate that sequential chunk processing with KV cache reuse substantially reduces memory requirements while improving throughput, making hundred-page document parsing more practical under limited GPU memory.
Figure 6
:
Performance and efficiency comparison across varying document lengths. Unlimited-OCR 2 demonstrates (a) robust parsing accuracy and (b) near-constant decoding latency (ms/step) as document length scaling.
5.3.2
Length-Invariant Accuracy
To verify whether extending the document horizon compromises parsing fidelity, we evaluate the performance trajectories of Unlimited OCR 2 across continuously increasing document lengths. As illustrated in Figure
6
(a), frontier Vision-Language Models (VLMs) typically experience a noticeable performance degradation as the sequence length grows, primarily caused by attention diffusion and context dilution over ultra-long horizons. In contrast, Unlimited OCR 2 exhibits remarkable length-invariant accuracy. By leveraging SR-SWA to dynamically isolate and retrieve only the most relevant visual tokens, our model maintains consistently high parsing precision from short sequences up to extreme horizons of 300 pages.
5.3.3
Constant Per-Step Decoding Latency
Figure
6
(b) examines how decoding efficiency scales with document length. All measurements are conducted in Gundam mode with a batch size of 3 and a fixed generation length of 1,024 tokens per page. As the document length grows, Full Attention incurs rapidly growing per-step decoding latency because each query must attend to a linearly expanding visual context. While R-SWA mitigates this overhead by bounding local window, its remote visual scope still scales with sequence length, leading to noticeable latency accumulation over ultra-long horizons. In contrast, SR-SWA strictly bounds the effective per-query attention scope, achieving near-constant per-step decoding latency from short contexts up to hundred-page documents. Consequently, its latency and throughput advantage over Full Attention and naive windowed baselines becomes increasingly pronounced as document length scales, confirming the computational viability of our paradigm for real-world long-document parsing.
6
Limitation and Future Work
Although Unlimited OCR 2 enables efficient parsing of hundred-page documents, its training data remains limited in diversity, and further data refinement will improve its robustness and generalization. More importantly, the current sparse-attention mechanism does not preserve global document information, limiting its understanding of document-level structures such as heading hierarchies. Future work may introduce architectures such as linear attention to retain global information with constant per-token computational cost, further improving document-level structure understanding.
7
Conclusion
In this technical report, we presented Unlimited OCR 2, a next-generation architecture tailored for unlimited-horizon document parsing. Specifically, Unlimited OCR 2 introduces Sparse Reference Sliding Window Attention (SR-SWA) to break the long-context visual computation bottleneck, guaranteeing constant per-token computational complexity throughout decoding. Additionally, integrated with an optimized page-split decoding paradigm, the model significantly mitigates GPU memory consumption, enabling robust unlimited-horizon inference on resource-constrained hardware. Extensive evaluations and analysis confirm that Unlimited OCR 2 maintains superior parsing accuracy alongside exceptional efficiency across all scales, thereby pioneering the OCR-3.0 era of unlimited-horizon document understanding.
8
Author List
Core Contributors:
Shu Wei, Jingjing Wu, Qunyi Xie
Contributors:
Lingshu Zhang, Xiangcheng Du, Yannian Fu, Mengjie Wang, Zuyi Wang, Zhichao Liu, Yangliu Xu, Youyang Yin, Huanhuan Liu, YY, Yi Yang
References
[1]
S. Bai, Y. Cai, R. Chen, K. Chen, X. Chen, Z. Cheng, L. Deng, W. Ding, C. Gao, C. Ge,
et al.
(2025)
Qwen3-vl technical report
.
arXiv preprint arXiv:2511.21631
.
Cited by:
Table 1
.
[2]
I. Beltagy, M. E. Peters, and A. Cohan
(2020)
Longformer: the long-document transformer
.
arXiv preprint arXiv:2004.05150
.
Cited by:
§2.2
.
[3]
P. Cai, Z. Zou, S. Liu, Y. Wang, J. Tang, K. Yang, M. Tong, M. Jiang, Z. He, and H. Sun
(2026)
TeleOCR: navigating document parsing across digital and camera-captured documents
.
arXiv preprint arXiv:2608.12898
.
External Links:
2608.12898
,
Link
Cited by:
Table 3
.
[4]
X. Chen, S. Li, X. Zhu, Y. Chen, F. Yang, C. Fang, L. Qu, X. Xu, H. Wei, and M. Wu
(2025)
Logics-parsing technical report
.
arXiv preprint arXiv:2509.19760
.
Cited by:
Table 3
.
[5]
C. Cui, T. Sun, S. Liang, T. Gao, Z. Zhang, J. Liu, X. Wang, C. Zhou, H. Liu, M. Lin,
et al.
(2025)
Paddleocr-vl: boosting multilingual document parsing via a 0.9 b ultra-compact vision-language model
.
arXiv preprint arXiv:2510.14528
.
Cited by:
§1
,
§2.1
.
[6]
C. Cui, T. Sun, S. Liang, T. Gao, Z. Zhang, J. Liu, X. Wang, C. Zhou, H. Liu, M. Lin,
et al.
(2026)
PaddleOCR-vl-1.5: towards a multi-task 0.9 b vlm for robust in-the-wild document parsing
.
arXiv preprint arXiv:2601.21957
.
Cited by:
§1
,
§2.1
.
[7]
D. Dong, M. Zheng, D. Xu, C. Luo, B. Zhuang, Y. Li, R. He, H. Wang, W. Zhang, W. Wang,
et al.
(2026)
Qianfan-ocr: a unified end-to-end model for document intelligence
.
arXiv preprint arXiv:2603.13398
.
Cited by:
§1
,
§2.1
,
Table 3
.
[8]
S. Duan, Y. Xue, W. Wang, Z. Su, H. Liu, S. Yang, G. Gan, G. Wang, Z. Wang, S. Yan,
et al.
(2026)
Glm-ocr technical report
.
arXiv preprint arXiv:2603.10910
.
Cited by:
§1
,
§2.1
.
[9]
Google DeepMind
(2026)
Gemini 3.1
.
Note:
https://deepmind.google/models/gemini/pro/
Cited by:
Table 1
,
Table 2
.
[10]
Google DeepMind
(2026)
Gemini 3.8
.
Note:
https://deepmind.google/models/gemini/flash/
Cited by:
Table 1
,
Table 2
.
[11]
A. Gu and T. Dao
(2023)
Mamba: linear-time sequence modeling with selective state spaces
.
arXiv preprint arXiv:2312.00752
.
Cited by:
§2.2
.
[12]
X. Hu, X. Wei, H. Gu, M. Zhang, T. Liang, H. Li, L. Zhu, Y. Wang, S. Han, Y. Bai,
et al.
(2026)
Hierarchical sparse attention done right: toward infinite context modeling
.
arXiv preprint arXiv:2607.02980
.
Cited by:
§2.2
,
§3.3.2
.
[13]
Y. Huang, N. M. Gonçalves, F. Alvetreti, L. Li, X. Han, E. M. Ponti, A. F. Martins, and M. V. Treviso
(2026)
DashAttention: differentiable and adaptive sparse hierarchical attention
.
arXiv preprint arXiv:2605.18753
.
Cited by:
§2.2
,
§3.3.2
,
§3.3
.
[14]
K. Jiang, R. Gong, X. Cheng, K. Niu, T. Li, and M. Xu
(2026)
ABot-ocr technical report
.
arXiv preprint arXiv:2605.27978
.
Cited by:
Table 3
.
[15]
A. Katharopoulos, A. Vyas, N. Pappas, and F. Fleuret
(2020)
Transformers are rnns: fast autoregressive transformers with linear attention
.
In
International conference on machine learning
,
pp. 5156–5165
.
Cited by:
§2.2
.
[16]
X. Lai, W. Xu, Y. Yang, Q. Chen, Y. Xu, L. Zeng, X. Li, H. Sun, H. Zhu, V. Zhang,
et al.
(2026)
Minimax sparse attention
.
arXiv preprint arXiv:2606.13392
.
Cited by:
§2.2
,
§3.3
,
Table 1
,
Table 2
.
[17]
A. Li, B. Gong, B. Yang, B. Shan, C. Liu, C. Zhu, C. Zhang, C. Guo, D. Chen, D. Li,
et al.
(2025)
Minimax-01: scaling foundation models with lightning attention
.
arXiv preprint arXiv:2501.08313
.
Cited by:
§2.2
.
[18]
G. Li, X. Wan, S. Peng, W. Wang, H. Feng, Y. Du, B. Wu, Z. Ruan, Z. Lu, L. Wu,
et al.
(2026)
HunyuanOCR-1.5: making lightweight ocr vlms faster and better
.
arXiv preprint arXiv:2607.04884
.
Cited by:
§1
,
§2.1
.
[19]
Y. Li, G. Yang, H. Liu, B. Wang, and C. Zhang
(2025)
Dots. ocr: multilingual document layout parsing in a single vision-language model
.
arXiv preprint arXiv:2512.02498
.
Cited by:
§1
,
§2.1
,
Table 3
.
[20]
Z. Li, Y. Liu, Q. Liu, Z. Ma, Z. Zhang, S. Zhang, Z. Guo, J. Zhang, X. Wang, and X. Bai
(2025)
MonkeyOCR: document parsing with a structure-recognition-relation triplet paradigm
.
arXiv preprint arXiv:2506.05218
.
Cited by:
§1
,
§2.1
.
[21]
S. Lu, Y. Li, Y. Xia, Y. Chen, A. Ji, J. Jiang, Q. Chen, J. Zhao, E. Lin, H. Li,
et al.
(2026)
OvisOCR2 technical report
.
arXiv preprint arXiv:2607.13639
.
Cited by:
§1
,
§2.1
,
Table 3
.
[22]
J. Niu, Z. Liu, Z. Gu, B. Wang, L. Ouyang, Z. Zhao, T. Chu, T. He, F. Wu, Q. Zhang,
et al.
(2025)
MinerU2.5: a decoupled vision-language model for efficient high-resolution document parsing
.
In
Proceedings of the 64th Annual Meeting of the Association for Computational Linguistics–Industry Track
,
Cited by:
§1
,
§2.1
.
[23]
H. V. Team, P. Lyu, X. Wan, G. Li, S. Peng, W. Wang, L. Wu, H. Shen, Y. Zhou, C. Tang,
et al.
(2025)
Hunyuanocr technical report
.
arXiv preprint arXiv:2511.19575
.
Cited by:
Table 3
.
[24]
K. Team, T. Bai, Y. Bai, Y. Bao, S. Cai, Y. Cao, Y. Charles, H. Che, C. Chen, G. Chen,
et al.
(2026)
Kimi k2. 5: visual agentic intelligence
.
arXiv preprint arXiv:2602.02276
.
Cited by:
Table 1
,
Table 2
.
[25]
TongYi
(2025)
TongYi
.
Note:
https://www.aliyun.com/product/tongyi
Cited by:
Table 1
,
Table 1
,
Table 1
,
Table 2
,
Table 2
.
[26]
B. Wang, T. He, L. Ouyang, F. Wu, Z. Zhao, T. Chu, Y. Qu, Z. Jin, W. Zeng, Z. Miao,
et al.
(2026)
MinerU2. 5-pro: pushing the limits of data-centric document parsing at scale
.
arXiv preprint arXiv:2604.04771
.
Cited by:
§1
,
§2.1
,
§4.1
.
[27]
W. Wang, Z. Gao, L. Gu, H. Pu, L. Cui, X. Wei, Z. Liu, L. Jing, S. Ye, J. Shao,
et al.
(2025)
Internvl3. 5: advancing open-source multimodal models in versatility, reasoning, and efficiency
.
arXiv preprint arXiv:2508.18265
.
Cited by:
Table 1
.
[28]
H. Wei, Y. Sun, and Y. Li
(2025)
Deepseek-ocr: contexts optical compression
.
arXiv preprint arXiv:2510.18234
.
Cited by:
§3.2
.
[29]
H. Wei, Y. Sun, and Y. Li
(2026)
DeepSeek-ocr 2: visual causal flow
.
arXiv preprint arXiv:2601.20552
.
Cited by:
Table 3
.
[30]
S. Wei, J. Wu, L. Zhang, Q. Xie, H. Zou, L. Xiang, X. Fan, Y. Xu, M. Lin, X. Ma,
et al.
(2026)
HPD-parsing: hierarchical parallel document parsing
.
arXiv preprint arXiv:2607.18839
.
Cited by:
§2.1
.
[31]
H. Wu, H. Lou, X. Li, Z. Zhong, Z. Sun, P. Chen, X. Zhou, K. Zuo, Y. Chen, X. Tang,
et al.
(2026)
Firered-ocr technical report
.
arXiv preprint arXiv:2603.01840
.
Cited by:
§1
,
§2.1
,
Table 3
.
[32]
A. Xu, B. Li, B. Lin, B. Xue, B. Xian, B. Xu, B. Wu, B. Zhang, B. Deng, C. Yu,
et al.
(2026)
DeepSeek-v4. 1-flash: pushing the limits of kv cache compression
.
arXiv preprint arXiv:2609.19969
.
Cited by:
§3.3
,
Table 1
,
Table 2
.
[33]
A. Xu, B. Lin, B. Xue, B. Wang, B. Xu, B. Wu, B. Zhang, C. Lin, C. Dong, C. Ling,
et al.
(2026)
Deepseek-v4: towards highly efficient million-token context intelligence
.
arXiv preprint arXiv:2606.19348
.
Cited by:
§2.2
,
§3.3
.
[34]
B. Xu, Z. Miao, X. Zhou, Y. Lin, Z. Tang, X. Zhao, F. Wu, C. Tan, B. Wang, and C. He
(2026)
MinerU-popo: universal post-processing model for structured document parsing
.
arXiv preprint arXiv:2605.24973
.
Cited by:
§4.1
.
[35]
S. Yang, B. Wang, Y. Shen, R. Panda, and Y. Kim
(2023)
Gated linear attention transformers with hardware-efficient training
.
arXiv preprint arXiv:2312.06635
.
Cited by:
§2.2
.
[36]
S. Yang, B. Wang, Y. Zhang, Y. Shen, and Y. Kim
(2024)
Parallelizing linear transformers with the delta rule over sequence length
.
Advances in neural information processing systems
37
,
pp. 115491–115522
.
Cited by:
§2.2
.
[37]
Y. Yin, H. Liu, Q. Xie, C. Liu, S. Yang, S. Wang, Z. Liu, H. Zou, J. Chen, S. Wei,
et al.
(2026)
Unlimited ocr works
.
arXiv preprint arXiv:2606.23050
.
Cited by:
§1
,
§2.1
,
Table 1
,
Table 3
.
[38]
Z.AI
GLM-5.3-Flash
.
Note:
https://huggingface.co/zai-org/GLM-5.3-Flash
Model card, accessed 2026-09-25
Cited by:
Table 1
,
Table 2
.
[39]
M. Zaheer, G. Guruganesh, K. A. Dubey, J. Ainslie, C. Alberti, S. Ontanon, P. Pham, A. Ravula, Q. Wang, L. Yang,
et al.
(2020)
Big bird: transformers for longer sequences
.
Advances in neural information processing systems
33
,
pp. 17283–17297
.
Cited by:
§2.2
.
[40]
Z. Zhang, H. Liu, S. Liang, Y. Zhang, Y. Xiang, J. Liu, T. Sun, M. Lin, Y. Zhang, C. Zhou,
et al.
(2026)
PaddleOCR-vl-1.6: expanding the frontier of document parsing with under-optimized region refinement and progressive post-training
.
arXiv preprint arXiv:2606.03264
.
Cited by:
§1
,
§2.1
,
§4.1
.
[41]
B. Zhou, H. Xing, Y. Chen, J. Xu, Q. Zheng, F. Gao, Z. Yang, S. Bai, M. Yan, J. Ye,
et al.
(2026)
MPDocBench-parse: benchmarking practical multi-page document parsing
.
arXiv preprint arXiv:2605.22100
.
Cited by:
§3.1.2
,
§5.1
.
Experimental support, please
view the build logs
for errors. Generated by
L
A
T
E
xml
.
Instructions for reporting errors
We are continuing to improve HTML versions of papers, and your feedback helps enhance accessibility and mobile
      support. To report errors in the HTML that will help us improve conversion and rendering, choose any of the
      methods listed below:
Click the "Report Issue"
(
)
button, located in the page header.
Tip:
You can select the relevant text first, to include it in your report.
Our team has already identified
the following issues
. We appreciate your time reviewing and reporting rendering errors we
      may not have found yet. Your efforts will help us improve the HTML versions for all readers, because disability
      should not be a barrier to accessing research. Thank you for your continued support in championing open access for
      all.
Have a free development cycle? Help support accessibility at arXiv! Our collaborators at LaTeXML maintain a
list of packages that need conversion
, and welcome
developer contributions
.
We gratefully acknowledge support from our
major funders
,
member institutions
,
,
        and all contributors.
About
·
Help
·
Contact
·
Subscribe
·
Copyright
·
Privacy
·
Accessibility
·
Operational Status
(opens in new tab)