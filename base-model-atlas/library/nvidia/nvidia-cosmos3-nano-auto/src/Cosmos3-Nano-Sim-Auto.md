---
license: other
license_name: openmdw1.1-license
license_link: >-
  https://openmdw.ai/license/1-1/
library_name: cosmos
tags:
  - nvidia
  - cosmos
  - cosmos3
  - omnimodel
---

# **Interactive World Simulation with Cosmos for Physical AI**

**[Cosmos3 Examples Collection](https://huggingface.co/collections/nvidia/cosmos3-examples)** | **[Code](https://github.com/nvidia/cosmos)** | **[Technical Report](https://research.nvidia.com/labs/cosmos-lab/cosmos-simulation/technical-report.pdf)** (coming soon) | **[Website](https://research.nvidia.com/labs/cosmos-lab/cosmos-simulation/)**

# Model Overview: Cosmos3-Nano-Sim-Auto

![Cosmos3 product and examples lineage highlighting Cosmos3-Nano-Sim-Auto](images/cosmos3-nano-sim-auto-graph.png)

The highlighted checkpoint, Cosmos3-Nano-Sim-Auto, is a causal-distilled variant of Cosmos3-Nano-Transfer-Auto.

## Description

<p align="center">
  <video src="https://huggingface.co/nvidia/Cosmos3-Nano-Sim-Auto/resolve/main/images/cosmos3-nano-sim-auto-golden-hour.mp4" controls autoplay loop muted playsinline width="100%" aria-label="Cosmos3-Nano-Sim-Auto: Golden hour, 11 synchronized camera views and LiDAR"></video>
</p>

Cosmos3-Nano-Sim-Auto is designed for real-time, closed-loop driving simulation by generating synchronized multi-view camera videos and LiDAR observations conditioned on a text prompt and World Scenario Map (WSM) controls, including aligned LiDAR controls when LiDAR output is requested. A WSM renderer converts driving inputs from an autonomous vehicle (AV) policy or a human-operated steering-wheel interface into scene controls. The model generates video in small latent-frame chunks conditioned on cached history and incoming WSM controls, enabling subsequent observations to reflect updated driving inputs. It supports up to 11 standard and fisheye camera views, with spatially and temporally aligned LiDAR output converted to 3D point clouds. The joint sensor outputs support evaluation of multi-sensor perception stacks and driving policies within the same rollout. Inference throughput depends on the hardware and generation configuration.

Cosmos3-Nano-Sim-Auto was developed by NVIDIA as part of the Cosmos example model family.

For a quick start, see the [Cosmos3-Nano-Sim-Auto skill](https://github.com/NVIDIA/cosmos-framework/tree/main/.agents/skills/cosmos3-nano-sim-auto).

This model is ready for commercial or non-commercial use.

## License

This model is released under [OpenMDW1.1](https://openmdw.ai/license/1-1/).

## Deployment Geography

Global

## Use Case

Physical AI for autonomous vehicles: closed-loop driving policy evaluation and verification, and synchronized multi-sensor synthetic data generation.

## Release Date

- Hugging Face 10/20/2026 via [https://huggingface.co/collections/nvidia/cosmos3-examples](https://huggingface.co/collections/nvidia/cosmos3-examples)
- GitHub 10/20/2026 via [https://github.com/nvidia/cosmos](https://github.com/nvidia/cosmos)

## Model Architecture

**Architecture Type:** Transformer

**Network Architecture:** Mixture-of-Transformers (MoT)

Cosmos3-Nano-Sim-Auto is derived from [Cosmos3-Nano](https://huggingface.co/nvidia/Cosmos3-Nano) in two stages: first, post-training on multi-sensor driving data, including LiDAR, to produce [Cosmos3-Nano-Transfer-Auto](https://huggingface.co/nvidia/Cosmos3-Nano-Transfer-Auto); then, causal distillation to produce a few-step model that generates video in small latent-frame chunks conditioned on cached history and the incoming WSM controls. Cached history provides temporal context across generation chunks. Camera views and LiDAR are generated jointly to support spatial and temporal consistency.

This model was developed using the [Cosmos Framework](https://github.com/NVIDIA/cosmos-framework).

**Number of trainable model parameters:** 16B

## Inputs

- **Input Type(s):** Text; Video (World Scenario Map (WSM) camera controls); Image (optional initial RGB conditioning); Other: numerical LiDAR controls and optional measured LiDAR conditioning.
- **Input Format(s):**
  - **Text:** String (scene description: weather, lighting, time of day; also carries the camera configuration)
  - **World Scenario Map (WSM) camera controls:** Synchronized MP4 videos of rendered scene structure, including lane markings and object cuboids, one per selected camera view.
  - **LiDAR controls:** Prepared HD-map range-map sequences aligned with the camera controls, supplied in the supported range-map archive or tensor format. Required when generating LiDAR.
  - **Optional RGB conditioning:** Synchronized initial camera images, supplied directly or extracted from the first frame of each camera video.
  - **Optional LiDAR conditioning:** An initial measured LiDAR sweep in the supported range/intensity representation, aligned with the start of the camera and control sequences.
- **Input Parameters:**
  - **Text:** One-dimensional (1D)
  - **WSM camera controls:** Three-dimensional (3D), per view
  - **Optional RGB conditioning:** Two-dimensional (2D), per image
  - **HD-map/LiDAR controls:** Three-dimensional (3D) sequences of projected range maps: time × height × width.
  - **Optional LiDAR conditioning:** Two-dimensional (2D) range-view map per initial sweep: height × width, with range, intensity, and validity channels.
- **Other Properties Related to Input:**
  - For measured LiDAR conditioning, the current causal inference path supports one initial sweep only; longer measured prefixes are not supported.
  - Supported camera rigs contain 1–11 views (Hyperion 8.1 camera set: front-wide 120°, front-tele 30°, cross-left/right 120°, rear-left/right 70°, rear-tele 30°, and front/left/right/rear fisheye 200°) and 128-beam rotating LiDAR.
  - Users can select up to 11 supported camera views through the input configuration. To adapt to a custom rig, first post-train Transfer-Auto using the [Transfer-Auto skill](https://github.com/NVIDIA/cosmos-framework/tree/main/.agents/skills/cosmos3-nano-transfer-auto), then perform causal distillation using the [Sim-Auto skill](https://github.com/NVIDIA/cosmos-framework/tree/main/.agents/skills/cosmos3-nano-sim-auto).
  - WSM controls are produced by a WSM renderer from an AV policy's planned trajectory or a human-operated steering-wheel interface. See the [Cosmos3-Nano-Sim-Auto skill](https://github.com/NVIDIA/cosmos-framework/tree/main/.agents/skills/cosmos3-nano-sim-auto) for details.

## Outputs

- **Output Type(s):** Video (multi-view, synchronized), LiDAR
- **Output Format(s):**
  - **Video:** MP4 or streamed video frames, one stream per camera view (standard and fisheye)
  - **LiDAR:** Range and intensity maps, converted to 3D point clouds with per-point intensity
- **Output Parameters:**
  - **Video:** Three-dimensional (3D), per view
  - **LiDAR:** Three-dimensional (3D)
- **Other Properties Related to Output:**
  - Camera videos and LiDAR observations are spatially and temporally synchronized.
  - Generates video at 480p or 720p with output video frame rates of 10–30 frames per second (fps) across all selected views.
  - Supported inference hardware includes, but is not limited to, H series (H100/H20/H200) and B/GB series (B200/300, GB200/300) GPUs.
  - Output video frame rates describe playback timing; inference throughput is reported separately.

Our AI models are designed and/or optimized to run on NVIDIA GPU-accelerated systems. By leveraging NVIDIA's hardware (e.g., GPU cores) and software frameworks (e.g., CUDA libraries), the model achieves faster training and inference times compared to CPU-only solutions.

## Software Integration

**Runtime Engine(s):**

- [PyTorch](https://pytorch.org/)
- [vLLM-Omni](https://github.com/vllm-project/vllm-omni)
- [SGLang](https://github.com/sgl-project/sglang)

**Supported Hardware Microarchitecture Compatibility:**

- NVIDIA Blackwell
- NVIDIA Hopper

**Operating System(s):**

- Linux (other operating systems have not been tested).

The integration of foundation and fine-tuned models into AI systems requires additional testing using use-case-specific data to ensure safe and effective deployment. Following the V-model methodology, iterative testing and validation at both unit and system levels are essential to mitigate risks, meet technical and functional requirements, and ensure compliance with safety and ethical standards before deployment.

## Model Version(s)

**Cosmos3-Nano-Sim-Auto — V1.0 (10/20/2026)**

Cosmos3-Nano-Sim-Auto is a causal-distilled variant of [Cosmos3-Nano-Transfer-Auto](https://huggingface.co/nvidia/Cosmos3-Nano-Transfer-Auto), which is a post-trained variant of [Cosmos3-Nano](https://huggingface.co/nvidia/Cosmos3-Nano).

## Training and Evaluation Datasets

### Post-Training Datasets

**Data Modality:** Video, Text, and LiDAR.

**Post-Training Data Size:**
- **Text:** 1 Billion to 10 Trillion Tokens
- **Video:** 10,000 to 1 Million Hours
- **LiDAR:** Less than 10,000 Hours of LiDAR range/intensity-map sequences

**Data Collection Method:** Hybrid: Automatic/Sensors, Synthetic, Automated.

**Labeling Method:** Hybrid: Manually-Labeled, Automated.

**Properties:** The post-training datasets consist of multi-camera driving videos, associated English captions, and LiDAR observations sourced from NVIDIA-created driving datasets.

### Dataset Overview

- **Total Size:** 1.3B data points
- **Total Number of Datasets:** 393 dataset entries
- **Dataset partition:** Training [100%], Testing [N/A — evaluation benchmarks used separately], Validation [N/A — evaluation benchmarks used separately]
- **Time period for training data collection:** 2024–2026
- **Time period for validation data collection:** N/A (standard public benchmarks)

Raw data from internal and external sources is transformed into training-ready data through multiple stages of curation, filtering, and quality review. Data acquisition spans diverse multimodal sources — robotics, autonomous driving, industrial environments, indoor and outdoor scenes, varied lighting and weather conditions, camera viewpoints, object categories, and human activities — to broaden coverage across Physical AI operating environments. Automated filtering pipelines remove corrupted, duplicate, low-quality, and restricted content. Metadata analysis, heuristic rules, and model-assisted classifiers are applied during preprocessing to flag anomalous distributions and low-diversity subsets. Human review supplements automated filtering for selected datasets, benchmark construction, and targeted quality analysis. Datasets are balanced across modalities and task categories — visual reasoning, text-to-image, text-to-video, image-to-video, audio generation, video transfer, action-conditioned generation, and action command generation — to reduce overrepresentation of narrow domains. Synthetic and simulation-based augmentation supplements coverage of rare physical interactions and edge-case scenarios. Deduplication and provenance tracking are applied across the corpus. The resulting processed data is converted into model-ready tokenized or encoded representations through modality-specific preprocessors before training begins.

Training datasets passed through multiple layers of automated and manual safeguards designed to reduce the presence of harmful or policy-violating content across categories including weapons and weapons-related instructional content, criminal planning, child sexual abuse material (CSAM), non-consensual intimate imagery (NCII), sexual content involving minors, harassment, hate speech, profanity, threats and incitement to violence, self-harm or suicide-related content, and graphic violence. Data sources are reviewed for licensing compatibility, provenance, and alignment with internal data governance and safety policies before admission into training corpora. Automated filtering pipelines combine multiple detection strategies: hash-matching against known CSAM and NCII reference databases; classifier-based moderation models trained for explicit sexual content, hate speech, violence, weapons imagery, and other restricted categories; keyword and regex-based screening for criminal-planning, threats, and self-harm phrases in text data; metadata and provenance heuristics for source-level risk signals; and embedding-based anomaly detection to surface samples that fall outside expected distributions. Human review and targeted audits supplement automated filtering for selected datasets, benchmark construction, and safety-sensitive evaluation. For multimodal Physical AI data (robotics, autonomous driving, industrial scenes), additional filtering targets invalid action trajectories, physically implausible interactions, and unsafe control sequences. Synthetic and simulation-generated data are evaluated through internal validation before inclusion. Benchmark evaluations and red-team testing are applied post-training to surface remaining safety gaps across world generation, reasoning, audio, and action tasks. No large-scale data-filtering process can guarantee complete removal of all harmful content; residual risks may remain, particularly in rare edge cases or open-world deployment settings. Ongoing monitoring and dataset review continue post-release.

For more information about the datasets used to train this model, please see the [Public Summary of Training Content](https://docs.nvidia.com/cosmos/latest/cosmos3/index.html).

**Data Modality and Training Data Size**

| Modality | Reasoning Data Sample Count | Generation Data Sample Count |
| -------- | ------------------- | -------------------- |
| Text     | 22M                 | Not Applicable       |
| Image    | 19M                 | 767M                 |
| Video    | 1M                  | 348M                 |
| Audio    | Not Applicable      | 139M                 |
| Action   | Not Applicable      | 7M                   |

**Data Collection Method by dataset**

- Hybrid: Automatic/Sensors, Synthetic, Automated

**Labeling Method by dataset**

- Hybrid: Manually-Labeled, Automated

**Properties:** The training, testing, and evaluation datasets consist of diverse multimodal video, image, audio, action, synthetic, and sensor-conditioned data sourced from NVIDIA-owned data and publicly available, commercially permissive datasets. These datasets are curated to exclude known restricted content and to support building an Omni model that learns to generate and reason about dynamic physical environments across world reasoning and generation tasks.

### Public Datasets

| Dataset                   | Samples     |
|---------------------------|-------------|
| OpenImage                 | 1.2M        |
| Coyo700M                  | 100M        |
| YouTube Video             | 340M        |
| UMI                       | 4.5M        |

### Private Datasets

| Dataset                   | Samples     |
|---------------------------|-------------|
| Egocentric                | 7M          |
| Nexar                     | 0.6M        |
| AgiBot                    | 0.2M        |
| HOI                       | 0.3M        |

### Synthetic Datasets

| Dataset                                 | Samples     |
|-----------------------------------------|-------------|
| synthetic images generated using HiDream-I1       | 15M         |
| synthetic images generated using Qwen-Image-2512  | 14M         |
| synthetic captions generated using Qwen3-VL       | 1115M       |

## Evaluation Datasets

**Data Collection Method by dataset**

- Hybrid: Automatic/Sensors, Synthetic, Automated

**Labeling Method by dataset**

- Hybrid: Manually-Labeled, Automated

**Properties:** The training, testing, and evaluation datasets consist of diverse multimodal video, image, audio, action, synthetic, and sensor-conditioned data sourced from NVIDIA-owned data and publicly available, commercially permissive datasets. These datasets are curated to exclude known restricted content and to support building an Omni model that learns to generate and reason about dynamic physical environments across world reasoning and generation tasks.

## Quality Benchmark(s)

We provide control inputs and text prompts in the [Cosmos3 Driving Simulation Evaluation Dataset](https://huggingface.co/datasets/nvidia/Cosmos3-Driving-Simulation-Evaluation) to support evaluation. **Cosmos3-Nano-Sim-Auto** results use these text prompts; the Cosmos-Transfer2.5-2B Multiview baseline uses different prompts.

### Multi-view RGB quality

We evaluate **Cosmos3-Nano-Sim-Auto** at 720p in text-to-video (T2V) and image-to-video (I2V) settings, using a guidance scale of 1. The model generates 297 frames across seven cameras with four denoising steps. Cosmos-Transfer2.5-2B Multiview uses a guidance scale of 3. [Fréchet Inception Distance (FID)](https://arxiv.org/abs/1706.08500) compares generated and reference frame-feature distributions; [Fréchet Video Distance (FVD)](https://arxiv.org/abs/1812.01717) compares video-feature distributions, with I3D and StyleGAN-V results reported separately. [DOVER](https://github.com/VQAssessment/DOVER) evaluates video quality.

Temporal Sampson error measures geometric agreement between matched image points across frames. Adjacent Cosine Mean (ACM) measures within-view visual consistency by averaging CLIP-feature cosine similarities between each frame after the first and both its preceding frame and the first frame, with negative similarities clamped to zero. Scores are computed per camera video, then averaged across views and samples. The score ranges from 0 to 1; higher is better. ACM uses no ground-truth video and does not measure cross-view consistency. A frozen video can score highly, so ACM alone does not establish realistic motion.

Cross-view Sampson error measures agreement across camera views, evaluated over two or five view pairs.

<table>
  <thead>
    <tr>
      <th scope="col" style="text-align: left;">Model</th>
      <th scope="col" style="text-align: right;">Frame FID ↓</th>
      <th scope="col" style="text-align: right;">FVD (I3D) ↓</th>
      <th scope="col" style="text-align: right;">FVD (StyleGAN-V) ↓</th>
      <th scope="col" style="text-align: right;">DOVER technical ↑</th>
      <th scope="col" style="text-align: right;">Temporal Sampson error ↓</th>
      <th scope="col" style="text-align: right;">Adjacent Cosine Mean (ACM) ↑</th>
      <th scope="col" style="text-align: right;">Cross-view Sampson error, 2 view pairs (CSE2) ↓</th>
      <th scope="col" style="text-align: right;">Cross-view Sampson error, 5 view pairs (CSE5) ↓</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="text-align: left;">Cosmos-Transfer2.5-2B Multiview<br>(Transfer-T2V, guidance 3)</td>
      <td style="text-align: right;">61.9</td>
      <td style="text-align: right;">772</td>
      <td style="text-align: right;">770</td>
      <td style="text-align: right;"><strong>8.56</strong></td>
      <td style="text-align: right;">0.530</td>
      <td style="text-align: right;">0.885</td>
      <td style="text-align: right;"><strong>2.51</strong></td>
      <td style="text-align: right;"><strong>2.07</strong></td>
    </tr>
    <tr>
      <td style="text-align: left; background-color: #e8f4df; color: #18202b;"><strong style="color: inherit;">Cosmos3-Nano-Sim-Auto</strong><br>(T2V, guidance 1)</td>
      <td style="text-align: right; background-color: #e8f4df; color: #18202b;"><strong style="color: inherit;">48.6</strong></td>
      <td style="text-align: right; background-color: #e8f4df; color: #18202b;"><strong style="color: inherit;">480</strong></td>
      <td style="text-align: right; background-color: #e8f4df; color: #18202b;"><strong style="color: inherit;">479</strong></td>
      <td style="text-align: right; background-color: #e8f4df; color: #18202b;">7.30</td>
      <td style="text-align: right; background-color: #e8f4df; color: #18202b;"><strong style="color: inherit;">0.503</strong></td>
      <td style="text-align: right; background-color: #e8f4df; color: #18202b;"><strong style="color: inherit;">0.906</strong></td>
      <td style="text-align: right; background-color: #e8f4df; color: #18202b;">2.60</td>
      <td style="text-align: right; background-color: #e8f4df; color: #18202b;">2.24</td>
    </tr>
    <tr>
      <td style="text-align: left;">Cosmos-Transfer2.5-2B Multiview<br>(Transfer-I2V, guidance 3)</td>
      <td style="text-align: right;">41.9</td>
      <td style="text-align: right;">383</td>
      <td style="text-align: right;">382</td>
      <td style="text-align: right;"><strong>8.22</strong></td>
      <td style="text-align: right;">0.524</td>
      <td style="text-align: right;">0.878</td>
      <td style="text-align: right;">2.45</td>
      <td style="text-align: right;"><strong>1.98</strong></td>
    </tr>
    <tr>
      <td style="text-align: left; background-color: #e8f4df; color: #18202b;"><strong style="color: inherit;">Cosmos3-Nano-Sim-Auto</strong><br>(I2V, guidance 1)</td>
      <td style="text-align: right; background-color: #e8f4df; color: #18202b;"><strong style="color: inherit;">33.6</strong></td>
      <td style="text-align: right; background-color: #e8f4df; color: #18202b;"><strong style="color: inherit;">325</strong></td>
      <td style="text-align: right; background-color: #e8f4df; color: #18202b;"><strong style="color: inherit;">324</strong></td>
      <td style="text-align: right; background-color: #e8f4df; color: #18202b;">7.51</td>
      <td style="text-align: right; background-color: #e8f4df; color: #18202b;"><strong style="color: inherit;">0.505</strong></td>
      <td style="text-align: right; background-color: #e8f4df; color: #18202b;"><strong style="color: inherit;">0.900</strong></td>
      <td style="text-align: right; background-color: #e8f4df; color: #18202b;"><strong style="color: inherit;">2.36</strong></td>
      <td style="text-align: right; background-color: #e8f4df; color: #18202b;">2.09</td>
    </tr>
  </tbody>
</table>

### LiDAR generation (T2V)

We evaluate **Cosmos3-Nano-Sim-Auto** LiDAR generation in the T2V setting with four denoising steps and a guidance scale of 1. Bird's-eye-view (BEV) JSD compares generated and real point distributions viewed from above using a Jensen–Shannon measure; BEV MMD² uses [squared maximum mean discrepancy](https://www.jmlr.org/papers/v13/gretton12a.html) for a complementary distribution comparison. Fréchet Utonia distance and Utonia MMD² compare distributions of features from [Utonia](https://arxiv.org/abs/2603.03283), a pretrained point-cloud encoder that extracts features of 3D geometry. Chamfer temporal consistency (CTC) measures geometric change between adjacent ego-motion-aligned scans; vehicle CTC applies it to tracked vehicle crops aligned to object-local coordinates. Both are reported as generated-to-real CTC ratios, where 1 means matching the real scans' average temporal distance. Object support recall measures the fraction of eligible annotated objects, counted per frame, with sufficient generated LiDAR points in their box crops. Object detection F1 is the harmonic mean of precision and recall against ground-truth annotations, matching same-class detections by planar center distance below 3 m. LidarVerse results are reported for 21 and 116 scans and use a different evaluation subset.

<table>
  <thead>
    <tr>
      <th scope="col" style="text-align: left;">Model</th>
      <th scope="col" style="text-align: right;">BEV JSD, global ↓</th>
      <th scope="col" style="text-align: right;">BEV JSD, local ↓</th>
      <th scope="col" style="text-align: right;">BEV MMD^2 ↓</th>
      <th scope="col" style="text-align: right;">Frechet Utonia dist ↓</th>
      <th scope="col" style="text-align: right;">Utonia MMD^2 ↓</th>
      <th scope="col" style="text-align: right;">Temporal CTC / real, k=1 (closer to 1)</th>
      <th scope="col" style="text-align: right;">Vehicle CTC / real (closer to 1)</th>
      <th scope="col" style="text-align: right;">Object support recall (real &gt;=30, generated &gt;=10 points) ↑</th>
      <th scope="col" style="text-align: right;">Object detection F1: generated LiDAR vs GT @3m ↑</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="text-align: left;">LidarVerse (21 scans)</td>
      <td style="text-align: right;">0.151</td>
      <td style="text-align: right;">0.400</td>
      <td style="text-align: right;">0.0120</td>
      <td style="text-align: right;">33.6</td>
      <td style="text-align: right;">0.0636</td>
      <td style="text-align: right;"><strong>1.20</strong></td>
      <td style="text-align: right;"><strong>2.51</strong></td>
      <td style="text-align: right;"><strong>0.843</strong></td>
      <td style="text-align: right;"><strong>0.201</strong></td>
    </tr>
    <tr>
      <td style="text-align: left;">LidarVerse (116 scans)</td>
      <td style="text-align: right;">0.116</td>
      <td style="text-align: right;">0.300</td>
      <td style="text-align: right;">0.00644</td>
      <td style="text-align: right;">44.8</td>
      <td style="text-align: right;">0.0907</td>
      <td style="text-align: right;">1.35</td>
      <td style="text-align: right;">3.73</td>
      <td style="text-align: right;">0.788</td>
      <td style="text-align: right;">0.200</td>
    </tr>
    <tr>
      <td style="text-align: left; background-color: #e8f4df; color: #18202b;"><strong style="color: inherit;">Cosmos3-Nano-Sim-Auto</strong><br>(T2V, guidance 1)</td>
      <td style="text-align: right; background-color: #e8f4df; color: #18202b;"><strong style="color: inherit;">0.0552</strong></td>
      <td style="text-align: right; background-color: #e8f4df; color: #18202b;"><strong style="color: inherit;">0.277</strong></td>
      <td style="text-align: right; background-color: #e8f4df; color: #18202b;"><strong style="color: inherit;">0.00593</strong></td>
      <td style="text-align: right; background-color: #e8f4df; color: #18202b;"><strong style="color: inherit;">20.1</strong></td>
      <td style="text-align: right; background-color: #e8f4df; color: #18202b;"><strong style="color: inherit;">0.0354</strong></td>
      <td style="text-align: right; background-color: #e8f4df; color: #18202b;">1.28</td>
      <td style="text-align: right; background-color: #e8f4df; color: #18202b;">3.59</td>
      <td style="text-align: right; background-color: #e8f4df; color: #18202b;">0.816</td>
      <td style="text-align: right; background-color: #e8f4df; color: #18202b;">0.188</td>
    </tr>
  </tbody>
</table>


## Inference

**Acceleration Engine:** [PyTorch](https://pytorch.org/), [vLLM-Omni](https://github.com/vllm-project/vllm-omni)

**Test Hardware:** NVIDIA Blackwell GB200, NVIDIA Hopper H100, H20

Inference performance numbers below are based on vLLM-Omni runs, over 4 steps of denoising without CFG, generating 201 frames.

Empty table cells indicate that measurements are not yet reported. "-" means unsupported.

### Inference Performance

**Without LiDAR (single-GPU inference throughput, frames per second)**

| Views | Res | GB200 | H100 | H20 |
| :---: | :---: | :---: | :---: | :---: |
| 1 | 480p | 16.8 | 10.2 |  |
|  | 720p | 10 | 4.7 |  |
| 4 | 480p | 5.3 | 2.5 |  |
|  | 720p | 2.3 | 1.1 |  |
| 5 | 480p | 4.1 | 2 |  |
|  | 720p | 1.8 | 0.85 | 0.26 |
| 7 | 480p | 3 | 1.4 |  |
|  | 720p | 1.3 | 0.58 |  |
| 8 | 480p | 2.6 | 1.2 |  |
|  | 720p | 1.1 | 0.49 |  |
| 11 | 480p | 1.8 | 0.83 |  |
|  | 720p | 0.74 | - |  |

**With LiDAR (single-GPU inference throughput, frames per second)**

| Views | Res | GB200 | H100 | H20 |
| :---: | :---: | :---: | :---: | :---: |
| 1 | 480p | 7.1 | 3.4 | 1.1 |
|  | 720p | 5.1 | 2.4 |  |
| 4 | 480p | 3.4 | 1.6 | 0.54 |
|  | 720p | 1.9 | 0.84 |  |
| 5 | 480p | 2.8 | 1.3 |  |
|  | 720p | 1.5 | - | 0.21 |
| 7 | 480p | 2.2 | 1 | 0.34 |
|  | 720p | 1.1 | - |  |
| 8 | 480p | 1.9 | 0.91 |  |
|  | 720p | 0.93 | - |  |
| 11 | 480p | 1.4 | - |  |
|  | 720p | 0.65 | - |  |

Multi-GPU optimization is underway.

## Usage Example

### Quick Start

This example serves the model with [vLLM-Omni](https://github.com/vllm-project/vllm-omni) and generates seven synchronized camera videos, each 297 frames at 30 FPS and 832 × 480, rolled out autoregressively with the checkpoint's fixed four-step sampler. The inputs are the daytime sample published with Cosmos3-Nano-Transfer-Auto in [`assets/sample_data`](https://huggingface.co/nvidia/Cosmos3-Nano-Transfer-Auto/tree/main/assets/sample_data): per camera, one world-scenario (WSM) control video, one RGB video whose first frame sets the camera's starting appearance, and one caption. It does not generate LiDAR; for joint camera and LiDAR generation, see the [full notebook](https://github.com/NVIDIA/cosmos-framework/blob/main/.agents/skills/cookbooks/cosmos3/simulation/auto/run_sim_auto_with_vllm_omni.ipynb).

#### 1. Start the server

On a Linux host with an NVIDIA GPU (tested on one GB200), [Docker](https://docs.docker.com/engine/install/), and the [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html):

```bash
# A 7-camera, 297-frame rollout can take longer than the default 600 s timeouts.
docker run --runtime nvidia --gpus all --ipc=host \
  -v ~/.cache/huggingface:/root/.cache/huggingface \
  --env "HF_TOKEN=$HF_TOKEN" \
  --env VLLM_OMNI_VIDEO_SYNC_TIMEOUT=3600 \
  --env VLLM_OMNI_DLO_DP_WAVE_TIMEOUT=3600 \
  -p 127.0.0.1:8000:8000 \
  vllm/vllm-omni:cosmos3 \
  vllm serve nvidia/Cosmos3-Nano-Sim-Auto \
    --omni --model-class-name Cosmos3NanoSimAutoPipeline \
    --deploy-config /app/vllm-omni/vllm_omni/deploy/cosmos3_nano_sim_auto.yaml \
    --no-guardrails \
    --host 0.0.0.0 --port 8000 --init-timeout 1800
```

The container publishes the server on `127.0.0.1:8000` of the host. `--deploy-config` selects the Sim-Auto deployment: the AR-Diffusion engine, one request at a time, and a rolling key/value cache. `--no-guardrails` disables the Cosmos3 text and video safety checks. The first start downloads the checkpoint.

#### 2. Generate the camera videos

```bash
pip install requests huggingface_hub
```

```python
import json
from pathlib import Path

import requests
from huggingface_hub import snapshot_download

MODEL = "nvidia/Cosmos3-Nano-Sim-Auto"
SAMPLE_REPO = "nvidia/Cosmos3-Nano-Transfer-Auto"  # Publishes the shared daytime sample.
# The sample's seven cameras, in the checkpoint's camera order.
CAMERAS = [
    "camera_front_wide_120fov",
    "camera_cross_right_120fov",
    "camera_rear_right_70fov",
    "camera_rear_tele_30fov",
    "camera_rear_left_70fov",
    "camera_cross_left_120fov",
    "camera_front_tele_30fov",
]
NUM_FRAMES = 297  # Must be 4k + 1.

# Download the sample's WSM controls, RGB videos, and captions (about 70 MB).
scene = Path(snapshot_download(SAMPLE_REPO, allow_patterns=[
    "assets/sample_data/daytime_scene/wsm/*.mp4",
    "assets/sample_data/daytime_scene/rgb/*.mp4",
    "assets/sample_data/daytime_scene/captions/*.json",
])) / "assets/sample_data/daytime_scene"

def caption(camera):
    data = json.loads((scene / "captions" / f"{camera}.json").read_text())
    return data["caption_structured"]["chunk_0_300"]["caption"]

# One view per camera: its caption and the indexes of its WSM control and RGB video among the uploads.
views, files = [], []
for camera in CAMERAS:
    views.append({
        "camera_key": camera,
        "prompt": caption(camera),
        "control_reference_index": len(files),
        "vision_reference_index": len(files) + 1,
    })
    for kind in ("wsm", "rgb"):
        video = (scene / kind / f"{camera}.mp4").read_bytes()
        files.append(("input_references", (f"{kind}_{camera}.mp4", video, "video/mp4")))

response = requests.post(
    "http://127.0.0.1:8000/v1/videos/sync",
    data={
        "model": MODEL,
        "prompt": views[0]["prompt"],  # Required by the API; generation uses each view's prompt.
        "size": "832x480",
        "num_frames": NUM_FRAMES,
        "fps": 30,
        "guidance_scale": 1,  # Fixed by the distilled checkpoint,
        "num_inference_steps": 4,  # as is its four-step sampler.
        "seed": 0,
        "extra_params": json.dumps({
            "wsm": {},
            "multiview": {"views": views, "condition_video_as_image": True},
            "resolution": "480",
            "aspect_ratio": "16,9",
        }),
    },
    files=files,
    timeout=3660,
)
response.raise_for_status()
Path("sim_auto.mp4").write_bytes(response.content)
```

The server uses only the first frame of each RGB video, and trims each 300-frame control to `num_frames` and resizes it to 832 × 480. To vary weather, lighting, or time of day while keeping the same road and traffic, edit each view's `prompt`.

#### 3. Split the output by camera

The response is one camera-major MP4: 297 frames of the first camera, then 297 of the second, and so on for all seven. To split it with [FFmpeg](https://ffmpeg.org/), run:

```python
import subprocess

for index, camera in enumerate(CAMERAS):
    start, end = index * NUM_FRAMES, (index + 1) * NUM_FRAMES
    subprocess.run([
        "ffmpeg", "-v", "error", "-y", "-i", "sim_auto.mp4",
        "-vf", f"trim=start_frame={start}:end_frame={end},setpts=N/(30*TB)",
        "-r", "30", "-an", f"{camera}.mp4",
    ], check=True)
```

With the daytime sample, the output looks like this, tiled as a surround view with the front-facing cameras on top and the rear-facing cameras below. Each camera starts from the first frame of its RGB video.

<video src="https://huggingface.co/nvidia/Cosmos3-Nano-Sim-Auto/resolve/main/images/cosmos3-nano-sim-auto-quickstart.mp4" controls autoplay loop muted playsinline width="100%"></video>

### Quick Start with SGLang

[SGLang](https://github.com/sgl-project/sglang) serves the same model through its OpenAI-compatible Videos API and produces the same camera-major video as the example above. Two things differ: the server reads every input from a path it can open instead of accepting uploads, so the sample is downloaded into a directory that is mounted into the container, and generation runs as an asynchronous job that the client polls. For joint camera and LiDAR generation with SGLang, see the [SGLang notebook](https://github.com/NVIDIA/cosmos-framework/blob/main/.agents/skills/cookbooks/cosmos3/simulation/auto/run_sim-auto_with_sglang.ipynb).

#### 1. Start the server

On the same kind of host, with the published [`lmsysorg/sglang:dev`](https://hub.docker.com/r/lmsysorg/sglang/tags) image, which includes the Cosmos3 pipelines from [sgl-project/sglang#39475](https://github.com/sgl-project/sglang/pull/39475):

```bash
export SAMPLE_DIR="$PWD/cosmos3-daytime-sample"  # Receives the inputs; the server reads them from this path.
export SGLANG_HF_CACHE="${SGLANG_HF_CACHE:-$HOME/.cache/sglang-huggingface}"  # The container runs as root.
mkdir -p "$SAMPLE_DIR" "$SGLANG_HF_CACHE"
chmod 777 "$SGLANG_HF_CACHE"
docker pull lmsysorg/sglang:dev
docker run --init --runtime nvidia --gpus all --ipc=host \
  -v "$SGLANG_HF_CACHE:/root/.cache/huggingface" \
  -v "$SAMPLE_DIR:$SAMPLE_DIR" \
  --env "HF_TOKEN=$HF_TOKEN" \
  -p 127.0.0.1:30000:30000 \
  lmsysorg/sglang:dev \
  sglang serve \
    --model-path nvidia/Cosmos3-Nano-Sim-Auto \
    --host 0.0.0.0 --port 30000
```

The container publishes the server on `127.0.0.1:30000` of the host and mounts `SAMPLE_DIR` at the same path, so the paths in the request below are valid inside it. The `dev` tag moves with SGLang's main branch, so pull it before each start. The first start downloads the checkpoint; the HTTP port opens after the weights are loaded and the warmup request finishes. This pipeline runs no text or video guardrails. With N GPUs (2, 4, or 8), add `--num-gpus N --ulysses-degree N --sp-degree N` to `sglang serve` to split every chunk across them with Ulysses sequence parallelism.

#### 2. Generate the camera videos

Run this in the same shell, so `SAMPLE_DIR` is set:

```bash
pip install requests huggingface_hub
```

```python
import json
import os
import time
from pathlib import Path

import requests
from huggingface_hub import snapshot_download

MODEL = "nvidia/Cosmos3-Nano-Sim-Auto"
SAMPLE_REPO = "nvidia/Cosmos3-Nano-Transfer-Auto"  # Publishes the shared daytime sample.
SERVER = "http://127.0.0.1:30000"
SAMPLE_DIR = Path(os.environ["SAMPLE_DIR"]).resolve()  # Mounted into the server container at this path.
# The sample's seven cameras, in the checkpoint's camera order.
CAMERAS = [
    "camera_front_wide_120fov",
    "camera_cross_right_120fov",
    "camera_rear_right_70fov",
    "camera_rear_tele_30fov",
    "camera_rear_left_70fov",
    "camera_cross_left_120fov",
    "camera_front_tele_30fov",
]
NUM_FRAMES = 297  # Must be 4k + 1.

# Download the sample's WSM controls, RGB videos, and captions (about 70 MB) into SAMPLE_DIR.
scene = Path(snapshot_download(SAMPLE_REPO, local_dir=SAMPLE_DIR, allow_patterns=[
    "assets/sample_data/daytime_scene/wsm/*.mp4",
    "assets/sample_data/daytime_scene/rgb/*.mp4",
    "assets/sample_data/daytime_scene/captions/*.json",
])) / "assets/sample_data/daytime_scene"

def caption(camera):
    data = json.loads((scene / "captions" / f"{camera}.json").read_text())
    return data["caption_structured"]["chunk_0_300"]["caption"]

# One view per camera: its caption and the server-visible paths of its WSM control and RGB video.
views = [
    {
        "camera_key": camera,
        "prompt": caption(camera),
        "control_path": str(scene / "wsm" / f"{camera}.mp4"),
        "vision_path": str(scene / "rgb" / f"{camera}.mp4"),
    }
    for camera in CAMERAS
]

form = {
    "model": MODEL,
    "prompt": views[0]["prompt"],  # Required by the API; generation uses each view's prompt.
    "size": "832x480",
    "num_frames": str(NUM_FRAMES),
    "fps": "30",
    "guidance_scale": "1",  # Fixed by the distilled checkpoint,
    "num_inference_steps": "4",  # as is its four-step sampler.
    "seed": "0",
    "extra_params": json.dumps({
        "wsm": {},
        "multiview": {"views": views, "condition_video_as_image": True, "num_frames": NUM_FRAMES},
        "resolution": "480",
        "aspect_ratio": "16,9",
    }),
}

# Submit the job, poll it, and download the video. Nothing is uploaded: the form carries text fields only.
response = requests.post(f"{SERVER}/v1/videos", files=[(key, (None, value)) for key, value in form.items()], timeout=60)
response.raise_for_status()
job = response.json()
deadline = time.monotonic() + 3600
while job["status"] not in ("completed", "failed", "cancelled"):
    if time.monotonic() > deadline:
        raise TimeoutError(f"Job {job['id']} did not finish in time: {job}")
    time.sleep(10)
    job = requests.get(f"{SERVER}/v1/videos/{job['id']}", timeout=60).json()
if job["status"] != "completed":
    raise RuntimeError(json.dumps(job, indent=2))
video = requests.get(f"{SERVER}/v1/videos/{job['id']}/content", timeout=600)
video.raise_for_status()
Path("sim_auto.mp4").write_bytes(video.content)
```

The server uses only the first frame of each RGB video, and trims each 300-frame control to `num_frames` and resizes it to 832 × 480. Split the camera-major output as in step 3 above.

## Ethical Considerations

NVIDIA believes Trustworthy AI is a shared responsibility and we have established policies and practices to enable development for a wide array of AI applications. Developers should work with their internal model team to ensure this model meets requirements for the relevant industry and use case and addresses unforeseen product misuse.

Please make sure you have proper rights and permissions for all input image and video content; if image or video includes people, personal health information, or intellectual property, the image or video generated will not blur or maintain proportions of image subjects included.

Users are responsible for model inputs and outputs. Users are responsible for ensuring safe integration of this model, including implementing guardrails as well as other safety mechanisms, prior to deployment.

For more detailed information on ethical considerations for this model, please see the Model Card++ [Explainability](explainability-Cosmos3-Nano-Sim-Auto.md), [Bias](bias.md), [Safety & Security](safety.md), and [Privacy](privacy.md) subcards. Please report model quality, risk, security vulnerabilities or NVIDIA AI Concerns [here](https://www.nvidia.com/en-us/support/submit-security-vulnerability/).
