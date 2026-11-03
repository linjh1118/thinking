GenFirst — Generation Before Reconstruction for Stable End-to-End Latent Generative Modeling
E2E
Gen
First
Abstract
Analysis
Method
Results
Text-to-Image
Shared Latents
Unified MMDiT
Samples
BibTeX
Gen
First
Generation Before Reconstruction for
Stable End-to-End Latent Generative Modeling
The general framework for stable direct end-to-end training of VAEs and generative models: mapping the data distribution to the distribution modeled by the generative model.
Guangting Zheng
1,2
,
Yiyuan Zhang
2
,
Tao Yang
2
,
Yunpeng Chen
2
,
Rui Zhu
2,†
,
Jiajun Deng
1
,
Yanyong Zhang
1,‡
1
University of Science and Technology of China
2
ByteDance Seed
†
Project lead ·
‡
Corresponding author
ByteDance Seed Project
Paper
arXiv
Code
Contact
BibTeX
0.97
gFID, ImageNet 256
with guidance
1.45
gFID, ImageNet 256
without guidance
0.90
GenEval overall
text-to-image, 1.3B
≥70×
fewer training steps
than SiT at equal FID
Abstract
Can a VAE and its generative prior be trained together, directly?
Latent generative models typically follow a two-stage pipeline, training a variational autoencoder
        for reconstruction and then a generative model on the frozen latent space. Since
        reconstruction-optimized latents are not necessarily generation-friendly, jointly training both
        models is an appealing alternative. However, direct end-to-end training remains challenging, as it is
        prone to
latent collapse
and faces a
generation–reconstruction
        conflict
.
In this work, we revisit this problem by analyzing how different objectives shape the latent space and
        identify two key insights. First, the
entropy term in the KL objective is essential for
        preventing collapse
: reconstruction and prior fitting both tend to shrink the posterior,
        while entropy preserves non-degenerate latent uncertainty. Second, reconstruction and generation
        exhibit
asymmetric learning dynamics
: reconstruction is fast and strongly supervised,
        whereas generation is slower and harder to optimize.
Motivated by these insights, we achieve the first direct end-to-end training without latent collapse
        and further propose
GenFirst
, a simple generation-before-reconstruction strategy. The
        generative objective first shapes the latent space under weak reconstruction pressure, after which
        reconstruction is progressively strengthened to recover visual details. We validate this strategy with
        both continuous autoregressive priors with exact likelihoods and SiT priors with implicit likelihoods.
        With our end-to-end objective and GenFirst, SiT achieves a gFID of
0.97
with CFG
        and
1.45
without CFG on ImageNet 256×256, while MMDiT reaches a GenEval score of
0.90
on text-to-image generation.
Beyond image generation, we further extend the framework to
shared visual latents
for
        generation and representation learning, and to
continuous unified text–image
        generation
. These results demonstrate the generality of stable end-to-end latent learning
        across generative priors and modalities.
Figure 1. Comparison of latent generative modeling paradigms.
(a) Conventional two-stage methods train the generative model on a fixed, reconstruction-optimized
        latent space that may be suboptimal for generation. (b) Naive end-to-end training lets the generative
        loss update the encoder, but causes latent collapse. (c) REPA-E avoids collapse by stopping the
        generative gradient and reshaping the latent space with an external representation-alignment loss, so
        the generative objective never directly shapes the latents. (d) Our method enables direct end-to-end
        training: the prior loss shapes a generation-friendly latent space while the entropy term prevents
        collapse.
Analysis
Two insights behind stable end-to-end training
We revisit end-to-end training from the VAE objective rather than from the architecture, and find that
        both failure modes reported in prior work have a concrete, correctable cause.
Insight 1 · why it collapses
A prior–entropy imbalance, not a broken gradient
For a standard Gaussian reference prior, the KL regularizer splits into a
prior-fitting
term and a
negative posterior-entropy
term:
\[ D_{\mathrm{KL}}(q_\phi(z|x)\|p_0(z)) = \underbrace{\mathbb{E}_{q_\phi}[-\log p_0(z)]}_{\text{prior fitting}} \;-\; \underbrace{\mathcal{H}(q_\phi(z|x))}_{\text{entropy}} \]
Naive end-to-end training inherits the LDM recipe of a tiny KL weight
          (\(\lambda_{\mathrm{KL}}\!\approx\!10^{-6}\)) and then adds a learned prior loss on top. The added
          objective is a strong extra prior-fitting force while entropy stays suppressed:
          \(\lambda_{\mathrm{prior}}+\lambda_{\mathrm{KL}} \gg \lambda_{\mathrm{KL}}\). Posterior variance is
          driven to zero, the means concentrate on nearly one code, and the latent space collapses.
The entropy term is
not a minor regularizer
: it is the counteracting force to learned prior
          fitting. Making it explicit turns latent collapse from a failure mode into a diagnosable imbalance.
Insight 2 · why weighting is not enough
Reconstruction is fast, generation is slow
Reconstruction is a strongly supervised mapping problem: given latents, the decoder gets direct pixel
          supervision and recovers detail within few steps. Generation is a distribution-modeling problem: the
          prior must learn the global latent distribution before it can sample anything recognizable.
Strong reconstruction pressure early therefore anchors the encoder to a reconstruction-oriented
          latent space that the prior can never catch up with, while permanent generative pressure prevents
          detail recovery. What matters is not only
how
the two objectives are weighted, but
when
each of them shapes the latent space.
Figure 2.
Reconstruction reaches good fidelity within far fewer steps, while generation
            needs a much longer optimization process to become sampleable.
Figure 3. What each objective does to the posterior.
Reconstruction spreads the posterior means (\(\mathrm{Std}(\mu)\!\uparrow\)) but shrinks the
        uncertainty (\(\mathbb{E}[\sigma^2]\!\downarrow\)), leaving gaps between codes that are hard to sample.
        Prior fitting without entropy shrinks both and collapses the posterior toward a constant code. Adding
        entropy restores \(\mathbb{E}[\sigma^2]\), increases posterior overlap and makes the latent space
        sampleable.
Three natural fixes for the generation–reconstruction conflict — none of them works
Figure 4.
(a) A larger latent dimension tolerates a stronger prior weight, but even
              \(d\!=\!128\) only supports \(\lambda_{\mathrm{prior}}\!\approx\!0.1\), and makes the AR prior
              harder to model. (b) Scaling the VAE (deeper encoder/decoder, or decoder only) does not
              alleviate the conflict and can even hurt reconstruction. (c) Scaling the prior improves
              generation but pushes reconstruction further down — more shaping pressure, same conflict.
The trade-off of generation and reconstruction
Figure 5.
(a) Raising \(\lambda_{\mathrm{prior}}\) from 0 to 1.0 improves gFID from
              120.60 to 8.06 while rFID degrades from 0.53 to 4.20 — no fixed weight is favourable for
              both. (b) In the reconstruction-refinement stage, a moderate prior weight of 0.25 is best.
              (c) gFID improves with a longer generation-first stage and saturates around 500 epochs.
Table 2. Loss balancing is not enough.
Same architecture and budget; only the
                way the generative objective is controlled differs.
Collapsed
= NaN training loss.
Strategy
gFID (w. CFG) ↓
IS (w. CFG) ↑
rFID ↓
PSNR ↑
SSIM ↑
GenFirst (ours)
2.10
246.70
1.26
21.93
0.58
Constant weighting
3.04
251.2
3.27
19.52
0.48
Cosine decay
5.45
136.11
0.66
23.87
0.67
PI adaptive
Collapsed
Frozen VAE (two-stage)
6.97
147.04
0.53
26.18
0.72
Constant weighting buys generation at the cost of reconstruction, cosine decay does the opposite,
            and PI-style adaptive control is numerically unstable in our setting. The optimization
order
— not the weight schedule — is what resolves the conflict.
Method
An entropy-preserving objective, and generation before reconstruction
One objective makes direct joint training stable; one schedule decides which objective gets to shape
        the latent space first.
\[ \mathcal{L}_{\mathrm{E2E}} = \lambda_{\mathrm{rec}}\mathcal{L}_{\mathrm{rec}} + \lambda_{\mathrm{LPIPS}}\mathcal{L}_{\mathrm{LPIPS}} + \lambda_{\mathrm{GAN}}\mathcal{L}_{\mathrm{GAN}} + \lambda_{\mathrm{prior}}\mathcal{L}_{\mathrm{prior}} - \lambda_{\mathrm{ent}}\mathcal{H}(q_\phi(z|x)) \]
Prior fitting and posterior entropy are
separated and separately weighted
. The prior term is
        whatever generative objective is being trained — an exact latent NLL for the continuous
        autoregressive prior, or the flow-matching velocity loss for SiT. For SiT we additionally keep the
        classic \(10^{-6}\) KL term purely to bound the latent scale, since an unbounded \(z\) would make the
        injected Gaussian noise relatively too small and open another shortcut.
Stage 1
Generation first
A large prior weight (with \(\lambda_{\mathrm{ent}}=\lambda_{\mathrm{prior}}\)) lets the generative
          objective form a generation-friendly latent geometry, while reconstruction preserves image
          information and entropy prevents collapse. This stage is the long one: 500 epochs for EAR,
          80 epochs for EiT.
Stage 2
Reconstruction refinement
The prior and entropy weights drop together — \(1\!\to\!0.25\) for EAR and
          \(0.1\!\to\!0.01\) for EiT — giving reconstruction more relative influence so that visual
          detail returns without dismantling the latent space formed in stage 1. This stage is short: 140
          and 40 epochs respectively.
Then
Freeze and train the prior
For diffusion priors the end-to-end phase is followed by a prior-only phase: freeze the learned VAE
          and train a fresh SiT / MMDiT on its latents. The same frozen VAE also transfers to
          512×512 and to text-to-image without retraining the tokenizer.
Instantiation A
EAR — exact-likelihood autoregressive prior
Latents are flattened into \(N=hw\) continuous tokens and modelled by a causal Transformer with a
          \(K\)-component Gaussian-mixture head, following FARMER:
          \(p_\theta(z|c)=\prod_i p_\theta(z_i|z_{<i},c)\). The exact likelihood makes the prior–entropy
          balance directly measurable, and the same loss both fits and reshapes the latent distribution.
Instantiation B
EiT — flow-matching / diffusion prior
SiT for class-conditional ImageNet and MMDiT for text-to-image, trained with the linear-interpolant
          velocity loss \(\|v_\theta(z_t,t)-(z-\epsilon_t)\|^2_2\). No explicit likelihood over latents is
          available here, which is exactly why the entropy term (rather than a likelihood diagnosis) is what
          keeps training stable.
Results
End-to-end latents are easier to generate from
The clearest evidence is not the joint model itself, but what happens when a
new
prior is
        trained from scratch on the frozen end-to-end latent space.
Table 1a. EAR.
Trained until gFID converges.
Collapsed
= NaN loss.
Setting
gFID ↓
IS ↑
rFID ↓
PSNR ↑
SSIM ↑
Frozen VAE
36.33
46.55
0.53
26.18
0.72
Naive E2E
294.90
1.48
0.70
25.11
0.68
Stable E2E (ours)
5.10
145.22
1.26
21.93
0.58
Frozen E2E-trained VAE
5.67
137.39
1.26
21.93
0.58
Table 1b. SiT
(80 epochs). Naive end-to-end training diverges outright.
Setting
gFID ↓
IS ↑
rFID ↓
PSNR ↑
SSIM ↑
Frozen VAE
7.90
122.60
0.74
25.67
0.72
Naive E2E
Collapsed
Stable E2E (ours)
92.38
13.94
0.57
25.13
0.71
Frozen E2E-trained VAE
3.57
166.49
0.57
25.13
0.71
Replacing a reconstruction-trained VAE with the frozen end-to-end-trained VAE takes a freshly trained
      prior from
36.33 → 5.67
gFID for EAR and
7.90 → 3.57
for SiT. EAR, whose exact
      likelihood directly models the VAE density, is slightly better
during
joint training; SiT, which
      has no explicit likelihood over latents, prefers the freeze-and-retrain protocol.
Figure 8. GenFirst latents converge much faster.
(a) FID-50K without guidance on ImageNet: GenFirst reaches FID 6.91 at 100K steps and 4.97 at 150K
        steps, beating the
final
results of SiT and REPA with at least
70×
and
26×
fewer steps, and matching REPA-E at roughly
2×
lower cost.
        (b–c) On text-to-image, both EiT variants pass the 200K-step SiT+REPA baseline by 80K steps on
        GenEval and DPG-Bench.
Class-conditional ImageNet 256×256 — full comparison
Table 6.
*
results obtained with a low-temperature sampling strategy.
Method
Epochs
#Params
Without guidance
With guidance
gFID ↓
IS ↑
Prec. ↑
Rec. ↑
gFID ↓
IS ↑
Prec. ↑
Rec. ↑
Pixel space
ADM
400
554M
10.94
101.0
0.69
0.63
3.94
215.8
0.83
0.53
RIN
480
410M
3.42
182.0
–
–
–
–
–
–
PixelFlow
320
677M
–
–
–
–
1.98
282.1
0.81
0.60
PixNerd
160
700M
–
–
–
–
2.15
297.0
0.79
0.59
SiD2
1280
–
–
–
–
–
1.38
–
–
–
TARFlow
320
1.4B
–
–
–
–
4.69
–
–
–
JetFormer
500
2.8B
–
–
–
–
6.64
–
0.69
0.56
FARMER
320
1.9B
–
–
–
–
3.60
269.2
0.81
0.51
JiT
600
2B
–
–
–
–
1.82
292.6
0.79
0.62
PixelDiT
320
797M
–
–
–
–
1.61
292.7
0.78
0.64
DeCo
600
682M
–
–
–
–
1.69
304.0
0.79
0.63
Latent autoregressive
GIVT
500
1.67B
–
–
–
–
2.59
–
0.81
0.57
VAR
350
2.0B
1.92
323.1
0.82
0.59
1.73
350.2
0.82
0.60
MAR
800
943M
2.35
227.8
0.79
0.62
1.55
303.7
0.81
0.62
xAR
800
1.1B
–
–
–
–
1.24
301.6
0.83
0.64
Latent diffusion
DiT
1400
675M
9.62
121.5
0.67
0.67
2.27
278.2
0.83
0.57
MaskDiT
1600
675M
5.69
177.9
0.74
0.60
2.28
276.6
0.80
0.61
SiT
1400
675M
8.61
131.7
0.68
0.67
2.06
270.3
0.82
0.59
MDTv2
1080
675M
–
–
–
–
1.58
314.7
0.79
0.65
REPA
800
675M
5.78
158.3
0.70
0.68
1.29
306.3
0.79
0.64
VA-VAE
800
675M
2.17
205.6
0.77
0.65
1.35
295.3
0.79
0.65
DDT
400
675M
6.27
154.7
0.68
0.69
1.26
310.6
0.79
0.65
RAE
800
839M
1.51
242.9
0.79
0.63
1.13
262.6
0.78
0.67
End-to-end generative models
SimFlow
160
1.4B
13.72
105.2
0.67
0.62
2.15
276.8
0.83
0.57
REPA-E
800
675M
1.69
219.3
0.77
0.67
1.12
302.9
0.79
0.66
EAR (ours, w/o GenFirst)
500
312M
5.17
147.5
0.70
0.59
3.04
251.2
0.73
0.55
EAR (ours)
500+140
312M
6.10 / 3.83
*
138.4 / 164.0
*
0.65
0.64
2.10
246.7
0.72
0.59
EiT (ours)
80
675M
2.79
175.4
0.78
0.63
1.38
271.3
0.79
0.63
EiT (ours)
480
675M
1.60
216.8
0.78
0.65
0.988
270.7
0.79
0.67
EiT (ours)
800
675M
1.45
226.7
0.79
0.65
0.969
283.4
0.79
0.67
EAR reaches a guided gFID of 2.10 with only
312M
parameters, outperforming much larger
            continuous-AR baselines such as GIVT (2.59), FARMER (3.60) and JetFormer (6.64). EiT reaches
0.988
guided gFID after 480 epochs — to our knowledge the first diffusion model below
            FID 1.0 without a Fréchet-Distance loss — and 1.45 unguided at 800 epochs.
Class-conditional ImageNet 512×512
Table 7.
The VAE is trained end-to-end at 256×256, then frozen; only the
                prior is trained at 512×512.
Method
Epochs
#Params
gFID ↓
IS ↑
Prec. ↑
Rec. ↑
BigGAN-deep
–
158M
8.43
177.9
0.88
0.29
StyleGAN-XL
–
–
2.41
267.8
0.77
0.52
VAR
350
2.3B
2.63
303.2
–
–
MAGVIT-v2
1080
307M
1.91
324.3
–
–
MAR
800
481M
1.73
279.9
–
–
xAR
800
608M
1.70
281.5
–
–
ADM
871+210
731M
3.85
221.7
0.84
0.53
SiD2
–
–
1.50
–
–
–
PixNerd
340
700M
2.84
245.6
0.80
0.59
JiT
600
2B
1.78
306.8
–
–
PixelDiT
850
797M
1.81
278.6
0.78
0.67
DeCo
340
682M
2.22
290.0
0.80
0.60
DiT
600
674M
3.04
240.8
0.84
0.54
SiT
600
674M
2.62
252.2
0.84
0.57
REPA
200
675M
2.08
274.6
0.83
0.58
Unified Latents
–
–
1.31
–
–
–
DDT
356
675M
1.28
305.1
0.80
0.63
EDM2
–
1.5B
1.25
–
–
–
RAE
400
839M
1.13
259.6
0.80
0.63
STARFlow
–
1.4B
3.00
–
–
–
SimFlow + REPA-E
160
1.4B
2.74
304.9
0.81
0.57
EAR (ours)
320
940M
1.87
280.0
0.82
0.58
EiT (ours)
80
675M
1.63
278.9
0.81
0.61
EiT (ours)
400
675M
1.23
286.1
0.80
0.63
Comparison with REPA / REPA-E, and how end-to-end training interacts with REPA
Table 4.
All models evaluated after 80 epochs.
Method
gFID ↓
IS ↑
Prec. ↑
Rec. ↑
REPA
7.90
122.60
0.70
0.65
REPA-E (scratch)
4.34
154.30
0.75
0.63
REPA-E (SD-VAE init.)
4.07
161.80
0.76
0.62
REPA-E (VA-VAE init.)
3.46
159.80
0.77
0.63
EiT (scratch)
3.78
161.42
0.78
0.61
EiT (SD-VAE init.)
3.57
166.49
0.77
0.62
EiT (VA-VAE init.)
2.79
175.40
0.78
0.63
Scaling the prior, GMM capacity, the optional normalizing flow, and SiT prior weights
Table 3a. EAR model scale
on a frozen GenFirst VAE.
Model
#Params
gFID ↓
IS ↑
EAR-B
174M
13.85
79.00
EAR-L
477M
5.67
137.39
EAR-XL
775M
3.91
163.71
EAR-XXL
1.4B
3.19
181.99
Table 3b. GMM components
with EAR-L fixed.
GMM \(K\)
gFID ↓
IS ↑
32
6.08
132.70
64
5.67
137.39
128
5.64
137.24
1024
5.01
144.63
4096
5.00
144.99
Table 5.
Is a normalizing flow still needed for continuous AR modeling?
Setting
gFID ↓
IS ↑
Frozen VAE + AR
110.10
14.79
Frozen VAE + NF + AR
36.33
46.55
Stable E2E VAE + AR
5.27
149.28
Stable E2E VAE + NF + AR
5.12
151.17
Table 13.
GenFirst prior weights for the SiT instantiation.
\(\lambda^{(1)}_{\mathrm{prior}}\)
\(\lambda^{(2)}_{\mathrm{prior}}\)
rFID ↓
PSNR ↑
FID ↓
IS ↑
1.00
0.10
0.61
24.57
4.44
154.25
0.10
0.01
0.57
25.13
3.57
166.49
0.01
0.01
0.48
25.17
3.84
161.40
After end-to-end training the extra normalizing flow becomes largely optional
            (5.27 → 5.12), whereas on a frozen reconstruction-optimized VAE it is worth 74 FID points.
            The latent space produced by GenFirst is already well suited to continuous AR modeling.
What end-to-end training costs in reconstruction
Table 12.
VAE reconstruction on ImageNet-256. End-to-end training reshapes the
                latent space toward generation at a moderate, predictable reconstruction cost.
VAE
rFID ↓
PSNR ↑
SSIM ↑
LPIPS ↓
FLUX.1-dev VAE
0.18
31.59
0.90
0.05
E2E-trained (Version A: SiT-XL/2 on ImageNet, FLUX.1-dev init.)
0.23
29.43
0.85
0.07
E2E-trained (Version B: MMDiT-L/2 on T2I, FLUX.1-dev init.)
0.21
29.37
0.85
0.07
SD-VAE
0.74
25.67
0.72
0.13
E2E-trained (f8d4, SD-VAE init.)
0.57
25.13
0.71
0.14
VA-VAE
0.28
26.32
0.76
0.11
E2E-trained (f16d32, VA-VAE init.)
0.36
25.82
0.74
0.12
Text-to-image
0.90 GenEval with a 1.3B MMDiT
The end-to-end phase produces a VAE — either with SiT-XL/2 on ImageNet (Version A) or with an
        MMDiT-L/2 on the text-to-image mixture (Version B). The prior-only phase then trains the same
        MMDiT-XL/2 on its latents at 256×256 for 200K steps, 512×512 for 80K steps, plus 40K steps
        of fine-tuning.
Table 8. GenEval and DPG-Bench.
†
uses prompt rewriting;
*
replaces the CLIP text encoder with Qwen3-1.7B.
Method
#Params
Single
Two obj.
Count
Color
Position
Attr.
GenEval ↑
DPG-Bench ↑
PixArt
4.3B+0.6B
0.98
0.50
0.44
0.80
0.08
0.07
0.48
71.11
DALL·E 2
–
0.94
0.66
0.49
0.77
0.10
0.19
0.52
–
Show-o
1.3B
0.95
0.52
0.49
0.82
0.11
0.28
0.53
–
Emu3-Gen
8B
0.98
0.71
0.34
0.81
0.17
0.21
0.54
80.60
SDXL
0.81B+2.6B
0.98
0.74
0.39
0.85
0.15
0.23
0.55
74.65
Janus
1.3B
0.97
0.68
0.30
0.84
0.46
0.42
0.61
79.68
JanusFlow
1.3B
0.97
0.59
0.45
0.83
0.53
0.42
0.63
80.09
FLUX.1 [dev]
4.8B+12B
0.98
0.81
0.74
0.79
0.22
0.45
0.66
–
DALL·E 3
–
0.96
0.87
0.47
0.83
0.43
0.45
0.67
83.50
SD3-Medium
5.5B+2B
0.99
0.94
0.72
0.89
0.33
0.60
0.74
84.08
Show-o2-7B
7B
1.00
0.87
0.58
0.92
0.52
0.62
0.76
†
86.14
MetaQuery-XL
7B
–
–
–
–
–
–
0.80
†
82.05
Janus-Pro-7B
7B
0.99
0.89
0.59
0.90
0.79
0.66
0.80
84.19
Z-Image-Turbo
4B+6B
1.00
0.95
0.77
0.89
0.65
0.68
0.82
84.86
BLIP3-o-8B
8B
–
–
–
–
–
–
0.84
81.60
FLUX.2 [dev]
24B+32B
1.00
0.99
0.79
0.93
0.73
0.78
0.87
87.57
Qwen-Image
7B+20B
0.99
0.92
0.89
0.88
0.76
0.77
0.87
88.32
BAGEL-7B
7B
0.98
0.95
0.84
0.95
0.78
0.77
0.88
†
–
EiT (ours)
0.1B+1.3B
1.00
0.94
0.83
0.94
0.87
0.82
0.90
82.60
EiT (ours)
*
1.7B+1.3B
0.99
0.94
0.73
0.96
0.89
0.84
0.89
84.65
With 1.3B generation parameters, EiT outperforms much larger text-to-image systems on GenEval, with the
      largest margins on
position
(0.87) and
attribute binding
(0.82). Swapping CLIP for a
      Qwen3-1.7B text encoder trades a little counting accuracy for +2.05 DPG-Bench.
Same MMDiT, same data — only the VAE differs
Hover a sample (or flip the switch) to swap between the FLUX.1-dev VAE and our end-to-end trained VAE.
      Click to open it full size; use ←/→ to browse.
Show:
Ours (E2E VAE)
FLUX.1-dev VAE
Show more prompts
Extension experiment 1 — Shared latents
Toward a shared latent space for generation and representation learning
The first of two
extension experiments
that push the same recipe past text-to-image.
        If the generative objective can shape a latent space, representation learning can share it. We swap
        the FLUX.1-dev encoder for a Qwen3-VL ViT plus a posterior projector and add representation
        supervision
inside
the same end-to-end loop, so the features being aligned are exactly the
        latents the diffusion model consumes.
Figure 9 (a–b). Two ways to add representation supervision.
(a) Latent-level SigLIP supervision, so representation learning shapes exactly the latents the
        generative model uses. (b) Caption-based VLM-NLL supervision applied to the intermediate
        ViT features: they are fed to a frozen Qwen3-VL and the caption NLL is minimized — no in-batch
        negatives needed.
Table 9. Reconstruction, generation and representation quality of different visual
          encoders.
The FLUX.1-dev encoder is replaced by the Qwen3-VL ViT plus a posterior projector;
          Top-1 is an ImageNet linear probe.
Encoder
Setting
rFID ↓
PSNR ↑
GenEval ↑
DPG-Bench ↑
Top-1 Acc. ↑
FLUX.1-dev VAE
Pretrained
0.18
31.59
–
–
3.1
Qwen3-VL ViT
Pretrained
–
–
–
–
79.64
Qwen3-VL ViT + projector
E2E
0.42
27.79
0.89
83.70
77.71
Qwen3-VL ViT + projector
E2E + SigLIP supervision
0.39
27.64
0.90
83.76
79.25
Qwen3-VL ViT + projector
E2E + VLM-NLL supervision
0.46
27.19
0.89
83.49
81.69
Representation supervision can be folded into end-to-end training almost for free: caption-based
      VLM-NLL supervision lifts linear-probe accuracy from 77.71 to
81.69
, which even
exceeds
the pretrained Qwen3-VL ViT’s 79.64, while GenEval and DPG-Bench stay at
      0.89 / 83.49.
Generation and representation learning can live in
one
latent space — no separate tokenizer
      for the diffusion model and no frozen encoder for the probe.
Extension experiment 2 — Unified MMDiT
Unified text-image modeling via an end-to-end diffusion
The second
extension experiment
shows the framework is not tied to pixels. Here we replace one
        modality outright: text is encoded into continuous latents as well, and a single block-causal MMDiT
        learns both directions between the two latent spaces.
Figure 9 (c). Unified text–image modeling with a block-causal diffusion transformer.
Continuous text and image latents are jointly optimized for bidirectional text-to-image and
        image-to-text generation; entropy terms keep either latent space from collapsing while reconstruction
        losses keep both decodable.
Setup
Two latent spaces, one diffusion backbone
Text is encoded into continuous latents by a text VAE (initialized from Cola) and reconstructed with a
        CE loss; text and image latents then enter a block-causal MMDiT trained on \(p(i|t)\) and \(p(t|i)\)
        with equal probability. Both diffusion directions shape the latent representations, the entropy term
        prevents collapse, and GenFirst balances latent modeling against reconstruction. Following the
        text-to-image recipe, the end-to-end phase uses a block-causal
MMDiT-L/2
(24 blocks, width
        1024) and the prior-only phase trains a fresh block-causal
MMDiT-XL/2
(28 blocks, width 1152)
        from scratch. Because of compute limits, the end-to-end phase uses half the steps of our text-to-image
        run and the prior-only phase only 30.8% of its samples.
Table 10.
Frozen versus end-to-end trained text/image VAEs, with the same
          block-causal MMDiT and the same three-stage recipe. Image-to-text is evaluated on the COCO
          Karpathy test split with
pycocoevalcap
.
Setting
GenEval ↑
DPG-Bench ↑
CIDEr ↑
BLEU-4 ↑
METEOR ↑
ROUGE-L ↑
SPICE ↑
CLIPScore ↑
Frozen text VAE + frozen image VAE
79.88
63.96
20.03
5.36
13.72
29.01
8.03
53.21
E2E-trained text VAE + frozen image VAE
81.87
68.24
30.19
7.46
16.81
32.95
11.12
55.96
E2E-joint-trained text VAE and image VAE
86.57
72.68
33.28
7.76
17.74
34.16
11.81
57.97
Both arms use the same MMDiT and the same sampling configuration, so the gaps come entirely from how the
      latent spaces were trained.
Figure 10. The three latent-space settings, same MMDiT and sampling configuration.
Top: text-to-image on DPG-Bench — only the jointly trained latents render the cat rather than a
        third teddy bear, and place the Opera House, Eiffel Tower and a snow-capped Everest together.
        Bottom: image-to-text on the COCO Karpathy test split — captions go from incoherent to
        “children playing soccer in a field”.
Shaping the
text
latent space end-to-end is worth +1.99 GenEval and +10.2 CIDEr on its own;
      shaping
both
latent spaces jointly adds another +4.70 GenEval, +4.44 DPG-Bench and +3.1 CIDEr.
Samples
Class-conditional ImageNet generation
Uncurated samples with guidance from EiT (480 epochs) and EAR (640 epochs) at 256×256.
        Click any block to view it full size; use ←/→ to browse.
Figure 6.
Class-to-image samples from EiT (rows 1–2) and EAR (rows 3–4) with
        guidance, CFG scale 4.
Cite
BibTeX
Copy
@article{zheng2026genfirst,
  title={GenFirst: Generation Before Reconstruction for Stable End-to-End Latent Generative Modeling},
  author={Zheng, Guangting and Zhang, Yiyuan and Yang, Tao and Chen, Yunpeng and Zhu, Rui and Deng, Jiajun and Zhang, Yanyong},
  journal={arXiv preprint arXiv:2608.29335},
  year={2026}
}
@inproceedings{zheng2026farmer,
  title={Farmer: Flow autoregressive transformer over pixels},
  author={Zheng, Guangting and Zhao, Qinyu and Yang, Tao and Xiao, Fei and Lin, Zhijie and Wu, Jie and Deng, Jiajun and Zhang, Yanyong and Zhu, Rui},
  booktitle={Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition},
  pages={25730--25741},
  year={2026}
}
Questions or feedback are very welcome —
zgt@mail.ustc.edu.cn
.
© 2026 the authors. All trademarks belong to their respective owners.
Page style adapted from the
Nerfies
/
Academic Project Page Template
.
✕
‹
›
1 / 1