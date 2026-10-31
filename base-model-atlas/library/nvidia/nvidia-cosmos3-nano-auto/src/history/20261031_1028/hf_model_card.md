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

# Model Overview: Cosmos3-Nano-Transfer-Auto

![Cosmos3 product and examples lineage highlighting Cosmos3-Nano-Transfer-Auto](images/cosmos3-nano-transfer-auto-graph.png)

The highlighted checkpoint, Cosmos3-Nano-Transfer-Auto, is a post-trained variant of the Cosmos3-Nano base model.

## Description

<p align="center">
  <video src="https://huggingface.co/nvidia/Cosmos3-Nano-Transfer-Auto/resolve/main/images/cosmos3-nano-transfer-auto-golden-hour.mp4" controls autoplay loop muted playsinline width="100%" aria-label="Cosmos3-Nano-Transfer-Auto: Golden hour, 11 synchronized camera views and LiDAR"></video>
</p>

Cosmos3-Nano-Transfer-Auto generates synchronized multi-view camera videos and LiDAR observations. It supports up to 11 standard and fisheye camera views. Generation is conditioned on a text prompt, World Scenario Map (WSM) controls for each camera view, and aligned LiDAR controls when LiDAR output is requested. The WSM inputs encode driving-scene structure, including traffic signs, traffic lights, lane markings, and object cuboids, while the text prompt specifies appearance attributes such as weather, lighting, and time of day. This enables the same driving scenario to be regenerated at scale with controlled variations in scene appearance. The model uses bidirectional generation for batch synthetic data generation and serves as the source checkpoint for causal distillation into Cosmos3-Nano-Sim-Auto, which provides closed-loop simulation with the same multi-view, multi-sensor output modalities.

Cosmos3-Nano-Transfer-Auto was developed by NVIDIA as part of the Cosmos example model family.

For a quick start, see the [Cosmos3-Nano-Transfer-Auto skill](https://github.com/NVIDIA/cosmos-framework/tree/main/.agents/skills/cosmos3-nano-transfer-auto).

This model is ready for commercial or non-commercial use.

## License

This model is released under [OpenMDW1.1](https://openmdw.ai/license/1-1/).

## Deployment Geography

Global

## Use Case

Physical AI for autonomous vehicles: synchronized multi-sensor synthetic data generation at scale for training and evaluating perception and driving models.

## Release Date

- Hugging Face 10/20/2026 via [https://huggingface.co/collections/nvidia/cosmos3-examples](https://huggingface.co/collections/nvidia/cosmos3-examples)
- GitHub 10/20/2026 via [https://github.com/nvidia/cosmos](https://github.com/nvidia/cosmos)

## Model Architecture

**Architecture Type:** Transformer

**Network Architecture:** Mixture-of-Transformers (MoT)

Cosmos3-Nano-Transfer-Auto is derived from [Cosmos3-Nano](https://huggingface.co/nvidia/Cosmos3-Nano) through post-training on multi-sensor driving data, including LiDAR. The model jointly denoises the full multi-view sequence using bidirectional temporal context, conditioned on the text prompt, WSM camera controls, and aligned LiDAR controls when generating LiDAR. It produces synchronized camera videos for up to 11 views and corresponding LiDAR observations.

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
  - Supported camera rigs contain 1–11 views (Hyperion 8.1 camera set: including front-wide 120°, front-tele 30°, cross-left/right 120°, rear-left/right 70°, rear-tele 30°, and front/left/right/rear fisheye 200°) and 128-beam rotating LiDAR. Adaptation to other rigs requires additional post-training.
  - WSM controls are produced by a WSM renderer; see the [Cosmos3-Nano-Transfer-Auto skill](https://github.com/NVIDIA/cosmos-framework/tree/main/.agents/skills/cosmos3-nano-transfer-auto) for details.

## Outputs

- **Output Type(s):** Video (multi-view, synchronized), LiDAR
- **Output Format(s):**
  - **Video:** MP4, one stream per camera view (standard and fisheye)
  - **LiDAR:** Range and intensity maps, converted to 3D point clouds with per-point intensity
- **Output Parameters:**
  - **Video:** Three-dimensional (3D), per view
  - **LiDAR:** Three-dimensional (3D)
- **Other Properties Related to Output:**
  - Camera videos and LiDAR observations are spatially and temporally synchronized.
  - Generates up to 300 frames per view at 480p or 720p, with output video frame rates of 10–30 frames per second (fps).
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

**Cosmos3-Nano-Transfer-Auto — V1.0 (10/20/2026)**

Cosmos3-Nano-Transfer-Auto is a post-trained variant of [Cosmos3-Nano](https://huggingface.co/nvidia/Cosmos3-Nano).

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

We provide control inputs and text prompts in the [Cosmos3 Driving Simulation Evaluation Dataset](https://huggingface.co/datasets/nvidia/Cosmos3-Driving-Simulation-Evaluation) to support evaluation. **Cosmos3-Nano-Transfer-Auto** results use these text prompts; the Cosmos-Transfer2.5-2B Multiview baseline uses different prompts.

### Multi-view RGB quality

We evaluate **Cosmos3-Nano-Transfer-Auto** at 720p in text-to-video (T2V) and image-to-video (I2V) settings, using a guidance scale of 3. [Fréchet Inception Distance (FID)](https://arxiv.org/abs/1706.08500) compares generated and reference frame-feature distributions; [Fréchet Video Distance (FVD)](https://arxiv.org/abs/1812.01717) compares video-feature distributions, with I3D and StyleGAN-V results reported separately. [DOVER](https://github.com/VQAssessment/DOVER) evaluates video quality.

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
      <td style="text-align: right;">8.56</td>
      <td style="text-align: right;">0.530</td>
      <td style="text-align: right;">0.885</td>
      <td style="text-align: right;">2.51</td>
      <td style="text-align: right;">2.07</td>
    </tr>
    <tr>
      <td style="text-align: left; background-color: #e8f4df; color: #18202b;"><strong style="color: inherit;">Cosmos3-Nano-Transfer-Auto</strong><br>(T2V, guidance 3)</td>
      <td style="text-align: right; background-color: #e8f4df; color: #18202b;"><strong style="color: inherit;">45.5</strong></td>
      <td style="text-align: right; background-color: #e8f4df; color: #18202b;"><strong style="color: inherit;">488</strong></td>
      <td style="text-align: right; background-color: #e8f4df; color: #18202b;"><strong style="color: inherit;">487</strong></td>
      <td style="text-align: right; background-color: #e8f4df; color: #18202b;"><strong style="color: inherit;">9.01</strong></td>
      <td style="text-align: right; background-color: #e8f4df; color: #18202b;"><strong style="color: inherit;">0.473</strong></td>
      <td style="text-align: right; background-color: #e8f4df; color: #18202b;"><strong style="color: inherit;">0.906</strong></td>
      <td style="text-align: right; background-color: #e8f4df; color: #18202b;"><strong style="color: inherit;">2.01</strong></td>
      <td style="text-align: right; background-color: #e8f4df; color: #18202b;"><strong style="color: inherit;">1.63</strong></td>
    </tr>
    <tr>
      <td style="text-align: left;">Cosmos-Transfer2.5-2B Multiview<br>(Transfer-I2V, guidance 3)</td>
      <td style="text-align: right;">41.9</td>
      <td style="text-align: right;">383</td>
      <td style="text-align: right;">382</td>
      <td style="text-align: right;">8.22</td>
      <td style="text-align: right;">0.524</td>
      <td style="text-align: right;">0.878</td>
      <td style="text-align: right;">2.45</td>
      <td style="text-align: right;">1.98</td>
    </tr>
    <tr>
      <td style="text-align: left; background-color: #e8f4df; color: #18202b;"><strong style="color: inherit;">Cosmos3-Nano-Transfer-Auto</strong><br>(I2V, guidance 3)</td>
      <td style="text-align: right; background-color: #e8f4df; color: #18202b;"><strong style="color: inherit;">27.8</strong></td>
      <td style="text-align: right; background-color: #e8f4df; color: #18202b;"><strong style="color: inherit;">238</strong></td>
      <td style="text-align: right; background-color: #e8f4df; color: #18202b;"><strong style="color: inherit;">237</strong></td>
      <td style="text-align: right; background-color: #e8f4df; color: #18202b;"><strong style="color: inherit;">8.27</strong></td>
      <td style="text-align: right; background-color: #e8f4df; color: #18202b;"><strong style="color: inherit;">0.472</strong></td>
      <td style="text-align: right; background-color: #e8f4df; color: #18202b;"><strong style="color: inherit;">0.902</strong></td>
      <td style="text-align: right; background-color: #e8f4df; color: #18202b;"><strong style="color: inherit;">2.25</strong></td>
      <td style="text-align: right; background-color: #e8f4df; color: #18202b;"><strong style="color: inherit;">1.80</strong></td>
    </tr>
  </tbody>
</table>

### LiDAR generation

We evaluate **Cosmos3-Nano-Transfer-Auto** LiDAR generation in the T2V setting with a guidance scale of 3. Bird's-eye-view (BEV) JSD compares generated and real point distributions viewed from above using a Jensen–Shannon measure; BEV MMD² uses [squared maximum mean discrepancy](https://www.jmlr.org/papers/v13/gretton12a.html) for a complementary distribution comparison. Fréchet Utonia distance and Utonia MMD² compare distributions of features from [Utonia](https://arxiv.org/abs/2603.03283), a pretrained point-cloud encoder that extracts features of 3D geometry. Chamfer temporal consistency (CTC) measures geometric change between adjacent ego-motion-aligned scans; vehicle CTC applies it to tracked vehicle crops aligned to object-local coordinates. Both are reported as generated-to-real CTC ratios, where 1 means matching the real scans' average temporal distance. Object support recall measures the fraction of eligible annotated objects, counted per frame, with sufficient generated LiDAR points in their box crops. Object detection F1 is the harmonic mean of precision and recall against ground-truth annotations, matching same-class detections by planar center distance below 3 m. LidarVerse results are reported for 21 and 116 scans and use a different evaluation subset.

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
      <td style="text-align: right;">1.20</td>
      <td style="text-align: right;"><strong>2.51</strong></td>
      <td style="text-align: right;">0.843</td>
      <td style="text-align: right;">0.201</td>
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
      <td style="text-align: left; background-color: #e8f4df; color: #18202b;"><strong style="color: inherit;">Cosmos3-Nano-Transfer-Auto</strong><br>(T2V, guidance 3)</td>
      <td style="text-align: right; background-color: #e8f4df; color: #18202b;"><strong style="color: inherit;">0.0401</strong></td>
      <td style="text-align: right; background-color: #e8f4df; color: #18202b;"><strong style="color: inherit;">0.220</strong></td>
      <td style="text-align: right; background-color: #e8f4df; color: #18202b;"><strong style="color: inherit;">0.00347</strong></td>
      <td style="text-align: right; background-color: #e8f4df; color: #18202b;"><strong style="color: inherit;">12.8</strong></td>
      <td style="text-align: right; background-color: #e8f4df; color: #18202b;"><strong style="color: inherit;">0.0208</strong></td>
      <td style="text-align: right; background-color: #e8f4df; color: #18202b;"><strong style="color: inherit;">1.17</strong></td>
      <td style="text-align: right; background-color: #e8f4df; color: #18202b;">2.53</td>
      <td style="text-align: right; background-color: #e8f4df; color: #18202b;"><strong style="color: inherit;">0.885</strong></td>
      <td style="text-align: right; background-color: #e8f4df; color: #18202b;"><strong style="color: inherit;">0.237</strong></td>
    </tr>
  </tbody>
</table>

## Inference

**Acceleration Engine:** [PyTorch](https://pytorch.org/), [vLLM-Omni](https://github.com/vllm-project/vllm-omni)

**Test Hardware:** NVIDIA Blackwell GB200, NVIDIA Hopper H100, H200, H20

Inference performance numbers below are based on vLLM-Omni runs, over 35 steps of denoising with CFG, generating 201 frames.

Empty table cells indicate that measurements are not yet reported. "-" means unsupported.

### Inference Performance - per NFE

Each per-NFE time is the end-to-end time from the tables below divided by 70 NFEs (35 denoising steps with CFG).

**Without LiDAR (per NFE, in seconds)**

| Views | Res | GB200 x1 | GB200 x2 | GB200 x4 | H100 x1 | H100 x2 | H100 x4 | H100 x8 | H20 x1 | H20 x2 | H20 x4 | H20 x8 | H200 x1 | H200 x2 | H200 x4 | H200 x8 |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | 480p | 1.2s | 0.6s | 0.4s | 2.4s | 1.3s | 0.8s | 0.6s |  |  |  |  | 2.4s | 1.3s | 0.8s | 0.6s |
|  | 720p | 5.1s | 2.8s | 1.6s | 10s | 5.6s | 3.1s | 2.0s |  |  | 13s | 7.5s | 10s | 5.6s | 3.1s | 2.0s |
| 4 | 480p | 5.3s | 2.9s | 1.6s | 11s | 5.7s | 3.3s | 2.3s |  |  | 13s | 7.5s | 11s | 5.7s | 3.3s | 2.3s |
|  | 720p | 22s | 12s | 6.3s | 44s | 24s | 13s | 8.3s |  |  | 55s | 31s | 46s | 25s | 13s | 8.1s |
| 5 | 480p | 6.7s | 3.7s | 2.1s | 14s | 7.3s | 4.2s | 2.9s |  |  |  |  | 14s | 7.2s | 4.3s | 2.9s |
|  | 720p | 28s | 15s | 8.1s | 56s | 30s | 17s | 10s |  |  |  | 39s | 58s | 31s | 17s | 10s |
| 7 | 480p | 9.7s | 5.3s | 3.0s | 20s | 12s | 7.2s | 5.3s |  |  | 26s | 16s | 20s | 12s | 7.0s | 5.1s |
|  | 720p | 40s | 21s | 11s | 81s | 44s | 24s | 15s |  |  | 101s |  | 85s | 45s | 24s | 15s |
| 8 | 480p | 11s | 6.0s | 3.5s | 23s | 13s | 8.1s | 6.0s |  |  | 30s | 18s | 23s | 13s | 8.0s | 5.8s |
|  | 720p | 46s | 25s | 13s | 94s | 51s | 28s | 17s |  |  | 116s | 65s | 97s | 51s | 28s | 17s |
| 11 | 480p | 16s | 8.6s | 4.9s | 33s | 19s | 11s | 8.3s |  |  |  | 26s | 33s | 19s | 11s | 8.1s |
|  | 720p | 66s | 35s | 19s | - | 73s | 40s | 24s |  |  | 166s | 92s | 141s | 75s | 40s | 24s |

**With LiDAR (per NFE, in seconds)**

| Views | Res | GB200 x1 | GB200 x2 | GB200 x4 | H100 x1 | H100 x2 | H100 x4 | H100 x8 | H20 x1 | H20 x2 | H20 x4 | H20 x8 | H200 x1 | H200 x2 | H200 x4 | H200 x8 |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | 480p | 8.8s | 4.8s | 2.7s | 20s | 11s | 5.9s | 3.4s |  | 44s | 23s | 12s | 20s | 11s | 5.8s | 3.4s |
|  | 720p | 13s | 6.9s | 3.7s | 28s | 15s | 8.3s | 4.8s |  |  | 33s |  | 29s | 15s | 8.3s | 4.7s |
| 4 | 480p | 13s | 7.2s | 3.9s | 30s | 16s | 9.3s | 6.0s |  |  | 35s |  | 30s | 16s | 9.3s | 5.8s |
|  | 720p | 31s | 16s | 8.9s | 67s | 36s | 20s | 12s |  |  | 77s | 43s | 69s | 36s | 20s | 12s |
| 5 | 480p | 16s | 8.6s | 4.7s | 34s | 19s | 11s | 6.8s |  |  | 39s | 22s | 34s | 18s | 10s | 6.8s |
|  | 720p | 37s | 20s | 11s | 81s | 43s | 24s | 14s |  |  | 93s |  | 81s | 44s | 24s | 14s |
| 7 | 480p | 19s | 10s | 5.7s | 41s | 22s | 13s | 8.5s |  |  |  |  | 41s | 22s | 13s | 8.4s |
|  | 720p | 50s | 26s | 14s | - | 58s | 32s | 19s |  |  | 125s | 69s | 112s | 59s | 32s | 19s |
| 8 | 480p | 21s | 11s | 6.4s | 44s | 25s | 14s | 9.3s |  |  |  | 30s | 44s | 24s | 14s | 9.3s |
|  | 720p | 56s | 30s | 16s | - | 65s | 36s | 22s |  |  | 142s | 79s | 125s | 67s | 36s | 21s |
| 11 | 480p | 27s | 14s | 8.1s | 56s | 31s | 18s | 12s |  |  |  | 38s | 56s | 31s | 18s | 12s |
|  | 720p | 77s | 41s | 22s | - | - | 50s | 30s |  |  |  | 107s | 171s | 90s | 49s | 29s |

### Inference Performance - end2end

**Without LiDAR (end-to-end inference time)**

| Views | Res | GB200 x1 | GB200 x2 | GB200 x4 | H100 x1 | H100 x2 | H100 x4 | H100 x8 | H20 x1 | H20 x2 | H20 x4 | H20 x8 | H200 x1 | H200 x2 | H200 x4 | H200 x8 |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | 480p | 1m22s | 0m45s | 0m28s | 2m47s | 1m29s | 0m56s | 0m41s |  |  |  |  | 2m51s | 1m31s | 0m57s | 0m40s |
|  | 720p | 5m54s | 3m13s | 1m55s | 11m41s | 6m32s | 3m40s | 2m21s |  |  | 15m30s | 8m48s | 11m59s | 6m31s | 3m40s | 2m18s |
| 4 | 480p | 6m11s | 3m22s | 1m53s | 12m32s | 6m39s | 3m52s | 2m42s |  |  | 15m07s | 8m45s | 12m32s | 6m37s | 3m53s | 2m41s |
|  | 720p | 25m22s | 13m28s | 7m23s | 50m58s | 27m54s | 15m21s | 9m38s |  |  | 64m36s | 36m13s | 53m45s | 28m37s | 15m27s | 9m30s |
| 5 | 480p | 7m49s | 4m18s | 2m27s | 15m49s | 8m28s | 4m57s | 3m25s |  |  |  |  | 15m54s | 8m25s | 5m00s | 3m24s |
|  | 720p | 32m19s | 17m13s | 9m24s | 65m36s | 35m01s | 19m35s | 12m09s |  |  |  | 45m46s | 68m13s | 36m18s | 19m35s | 11m53s |
| 7 | 480p | 11m20s | 6m08s | 3m29s | 23m28s | 13m47s | 8m24s | 6m08s |  |  | 30m08s | 18m36s | 23m27s | 13m36s | 8m10s | 5m56s |
|  | 720p | 46m21s | 24m36s | 13m24s | 93m58s | 51m19s | 28m20s | 17m21s |  |  | 117m28s |  | 98m43s | 52m33s | 28m18s | 17m04s |
| 8 | 480p | 12m57s | 7m03s | 4m02s | 27m03s | 15m36s | 9m30s | 6m58s |  |  | 34m46s | 21m15s | 27m05s | 15m40s | 9m23s | 6m48s |
|  | 720p | 53m57s | 28m40s | 15m40s | 109m12s | 59m36s | 32m19s | 20m03s |  |  | 135m49s | 75m32s | 112m56s | 60m02s | 32m46s | 19m43s |
| 11 | 480p | 18m27s | 10m04s | 5m40s | 38m33s | 22m08s | 13m21s | 9m41s |  |  |  | 29m59s | 39m04s | 22m00s | 13m14s | 9m25s |
|  | 720p | 77m31s | 41m05s | 22m29s | - | 84m38s | 46m28s | 27m50s |  |  | 193m47s | 107m25s | 164m35s | 87m16s | 46m49s | 27m40s |

**With LiDAR (end-to-end inference time)**

| Views | Res | GB200 x1 | GB200 x2 | GB200 x4 | H100 x1 | H100 x2 | H100 x4 | H100 x8 | H20 x1 | H20 x2 | H20 x4 | H20 x8 | H200 x1 | H200 x2 | H200 x4 | H200 x8 |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | 480p | 10m15s | 5m35s | 3m06s | 23m12s | 12m34s | 6m51s | 3m58s |  | 51m33s | 26m41s | 14m13s | 23m39s | 12m27s | 6m44s | 3m55s |
|  | 720p | 15m07s | 8m00s | 4m18s | 33m08s | 17m41s | 9m42s | 5m34s |  |  | 38m25s |  | 33m40s | 17m50s | 9m40s | 5m32s |
| 4 | 480p | 15m31s | 8m22s | 4m36s | 35m05s | 19m11s | 10m52s | 6m59s |  |  | 40m56s |  | 35m13s | 19m09s | 10m48s | 6m47s |
|  | 720p | 35m48s | 19m03s | 10m25s | 78m32s | 42m00s | 22m56s | 13m54s |  |  | 90m18s | 49m57s | 80m16s | 41m57s | 23m02s | 13m44s |
| 5 | 480p | 18m35s | 10m00s | 5m32s | 39m09s | 21m35s | 12m25s | 7m59s |  |  | 45m47s | 26m01s | 39m27s | 21m30s | 12m14s | 7m54s |
|  | 720p | 42m51s | 22m48s | 12m30s | 94m27s | 50m22s | 27m37s | 16m54s |  |  | 108m29s |  | 94m57s | 50m48s | 27m39s | 16m25s |
| 7 | 480p | 22m35s | 12m02s | 6m40s | 47m16s | 26m12s | 15m01s | 9m57s |  |  |  |  | 47m20s | 26m04s | 14m59s | 9m51s |
|  | 720p | 57m48s | 30m38s | 16m50s | - | 68m04s | 37m19s | 22m12s |  |  | 145m47s | 81m01s | 130m18s | 68m28s | 37m14s | 22m07s |
| 8 | 480p | 24m41s | 13m17s | 7m28s | 51m33s | 28m36s | 16m29s | 10m51s |  |  |  | 35m11s | 51m38s | 28m20s | 16m21s | 10m48s |
|  | 720p | 65m27s | 34m53s | 19m05s | - | 76m06s | 41m45s | 25m24s |  |  | 165m19s | 91m47s | 145m15s | 77m40s | 42m09s | 25m04s |
| 11 | 480p | 30m55s | 16m40s | 9m30s | 64m47s | 36m16s | 20m54s | 13m41s |  |  |  | 44m53s | 65m14s | 35m47s | 20m41s | 13m37s |
|  | 720p | 89m47s | 47m45s | 25m58s | - | - | 57m47s | 34m26s |  |  |  | 125m07s | 199m14s | 105m01s | 57m42s | 34m06s |


## Usage Example

### Quick Start

This example serves the model with [vLLM-Omni](https://github.com/vllm-project/vllm-omni) and generates seven synchronized camera videos, each 201 frames at 30 FPS and 832 × 480. The inputs are the daytime sample in [`assets/sample_data`](https://huggingface.co/nvidia/Cosmos3-Nano-Transfer-Auto/tree/main/assets/sample_data): one world-scenario (WSM) control video and one caption per camera. It does not generate LiDAR; for joint camera and LiDAR generation, see the [full notebook](https://github.com/NVIDIA/cosmos-framework/blob/main/.agents/skills/cookbooks/cosmos3/simulation/auto/run_auto_with_vllm_omni.ipynb).

#### 1. Start the server

On a Linux host with an NVIDIA GPU (tested on one GB200), [Docker](https://docs.docker.com/engine/install/), and the [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html):

```bash
# One 7-camera request can take longer than the default 600 s timeouts.
docker run --runtime nvidia --gpus all --ipc=host \
  -v ~/.cache/huggingface:/root/.cache/huggingface \
  --env "HF_TOKEN=$HF_TOKEN" \
  --env VLLM_OMNI_VIDEO_SYNC_TIMEOUT=1800 \
  --env VLLM_OMNI_DLO_DP_WAVE_TIMEOUT=1800 \
  -p 127.0.0.1:8000:8000 \
  vllm/vllm-omni:cosmos3 \
  vllm serve nvidia/Cosmos3-Nano-Transfer-Auto \
    --omni --model-class-name Cosmos3MultiviewPipeline \
    --no-guardrails \
    --host 0.0.0.0 --port 8000 --init-timeout 1800
```

The container publishes the server on `127.0.0.1:8000` of the host. `--no-guardrails` disables the Cosmos3 text and video safety checks. With two GPUs, add `--cfg-parallel-size 2`. The first start downloads the checkpoint. The first request also compiles the transformer, so it takes longer than later ones.

#### 2. Generate the camera videos

```bash
pip install requests huggingface_hub
```

```python
import json
from pathlib import Path

import requests
from huggingface_hub import snapshot_download

MODEL = "nvidia/Cosmos3-Nano-Transfer-Auto"
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
NUM_FRAMES = 201
# Set CAPTION_FOLDER="captions_with_timestamp" to use timestamped captions, which better match the
# model's training style and have empirically produced better inference results. Set it to
# "captions" to try the original paragraph-style captions. Both formats are supported.
CAPTION_FOLDER = "captions_with_timestamp"

# Download the sample's WSM controls, captions, and negative prompt (about 4 MB).
scene = Path(snapshot_download(MODEL, allow_patterns=[
    "assets/sample_data/daytime_scene/wsm/*.mp4",
    f"assets/sample_data/daytime_scene/{CAPTION_FOLDER}/*.json",
    "assets/sample_data/daytime_scene/captions/negative_prompt.txt",
])) / "assets/sample_data/daytime_scene"

def caption(camera):
    data = json.loads((scene / CAPTION_FOLDER / f"{camera}.json").read_text())
    return data["caption_structured"]["chunk_0_300"]["caption"]

# One negative caption, applied to every camera.
negative_prompt = (scene / "captions" / "negative_prompt.txt").read_text().strip()

# One view per camera: its caption and the index of its control among the uploads.
views = [
    {"camera_key": camera, "prompt": caption(camera), "control_reference_index": index}
    for index, camera in enumerate(CAMERAS)
]
files = [
    ("input_references", (f"{camera}.mp4", (scene / "wsm" / f"{camera}.mp4").read_bytes(), "video/mp4"))
    for camera in CAMERAS
]

response = requests.post(
    "http://127.0.0.1:8000/v1/videos/sync",
    data={
        "model": MODEL,
        "prompt": views[0]["prompt"],  # Required by the API; generation uses each view's prompt.
        "size": "832x480",
        "num_frames": NUM_FRAMES,
        "fps": 30,
        "num_inference_steps": 35,
        "guidance_scale": 3,
        "flow_shift": 10,
        "seed": 0,
        "extra_params": json.dumps({
            "wsm": {},
            "multiview": {"views": views},
            "per_view_negative_prompt": negative_prompt,
            "resolution": "480",
            "aspect_ratio": "16,9",
        }),
    },
    files=files,
    timeout=1860,
)
response.raise_for_status()
Path("transfer_auto.mp4").write_bytes(response.content)
```

The server trims each 300-frame control to `num_frames` and resizes it to 832 × 480. To vary weather, lighting, or time of day while keeping the same road and traffic, edit each view's `prompt`.

#### 3. Split the output by camera

The response is one camera-major MP4: 201 frames of the first camera, then 201 of the second, and so on for all seven. To split it with [FFmpeg](https://ffmpeg.org/), run:

```python
import subprocess

for index, camera in enumerate(CAMERAS):
    start, end = index * NUM_FRAMES, (index + 1) * NUM_FRAMES
    subprocess.run([
        "ffmpeg", "-v", "error", "-y", "-i", "transfer_auto.mp4",
        "-vf", f"trim=start_frame={start}:end_frame={end},setpts=N/(30*TB)",
        "-r", "30", "-an", f"{camera}.mp4",
    ], check=True)
```

With the daytime sample, the output looks like this, tiled as a surround view with the front-facing cameras on top and the rear-facing cameras below.

<video src="https://huggingface.co/nvidia/Cosmos3-Nano-Transfer-Auto/resolve/main/images/cosmos3-nano-transfer-auto-quickstart.mp4" controls autoplay loop muted playsinline width="100%"></video>

### Quick Start with SGLang

[SGLang](https://github.com/sgl-project/sglang) serves the same model through its OpenAI-compatible Videos API and produces the same camera-major video as the example above. Two things differ: the server reads every input from a path it can open instead of accepting uploads, so the sample is downloaded into a directory that is mounted into the container, and generation runs as an asynchronous job that the client polls. For joint camera and LiDAR generation with SGLang, see the [SGLang notebook](https://github.com/NVIDIA/cosmos-framework/blob/main/.agents/skills/cookbooks/cosmos3/simulation/auto/run_auto_with_sglang.ipynb).

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
    --model-path nvidia/Cosmos3-Nano-Transfer-Auto \
    --host 0.0.0.0 --port 30000
```

The container publishes the server on `127.0.0.1:30000` of the host and mounts `SAMPLE_DIR` at the same path, so the paths in the request below are valid inside it. The `dev` tag moves with SGLang's main branch, so pull it before each start. The first start downloads the checkpoint; the HTTP port opens after the weights are loaded and the warmup request finishes. With N GPUs (2, 4, or 8), add `--num-gpus N --ulysses-degree N --sp-degree N` to `sglang serve` to split the camera-major sequence across them with Ulysses sequence parallelism; `--enable-cfg-parallel` additionally runs the two guidance branches on separate GPU groups and doubles the GPUs required.

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

MODEL = "nvidia/Cosmos3-Nano-Transfer-Auto"
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
NUM_FRAMES = 201
# Set CAPTION_FOLDER="captions_with_timestamp" to use timestamped captions, which better match the
# model's training style and have empirically produced better inference results. Set it to
# "captions" to try the original paragraph-style captions. Both formats are supported.
CAPTION_FOLDER = "captions_with_timestamp"

# Download the sample's WSM controls, captions, and negative prompt (about 4 MB) into SAMPLE_DIR.
scene = Path(snapshot_download(MODEL, local_dir=SAMPLE_DIR, allow_patterns=[
    "assets/sample_data/daytime_scene/wsm/*.mp4",
    f"assets/sample_data/daytime_scene/{CAPTION_FOLDER}/*.json",
    "assets/sample_data/daytime_scene/captions/negative_prompt.txt",
])) / "assets/sample_data/daytime_scene"

def caption(camera):
    data = json.loads((scene / CAPTION_FOLDER / f"{camera}.json").read_text())
    return data["caption_structured"]["chunk_0_300"]["caption"]

# One negative caption, applied to every camera.
negative_prompt = (scene / "captions" / "negative_prompt.txt").read_text().strip()

# One view per camera: its caption and the server-visible path of its WSM control.
views = [
    {"camera_key": camera, "prompt": caption(camera), "control_path": str(scene / "wsm" / f"{camera}.mp4")}
    for camera in CAMERAS
]

form = {
    "model": MODEL,
    "prompt": views[0]["prompt"],  # Required by the API; generation uses each view's prompt.
    "size": "832x480",
    "num_frames": str(NUM_FRAMES),
    "fps": "30",
    "num_inference_steps": "35",
    "guidance_scale": "3",
    "flow_shift": "10",
    "seed": "0",
    "extra_params": json.dumps({
        "wsm": {},
        "multiview": {"views": views},
        "per_view_negative_prompt": negative_prompt,
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
Path("transfer_auto.mp4").write_bytes(video.content)
```

The server trims each 300-frame control to `num_frames` and resizes it to 832 × 480. Split the camera-major output as in step 3 above.

## Ethical Considerations

NVIDIA believes Trustworthy AI is a shared responsibility and we have established policies and practices to enable development for a wide array of AI applications. Developers should work with their internal model team to ensure this model meets requirements for the relevant industry and use case and addresses unforeseen product misuse.

Please make sure you have proper rights and permissions for all input image and video content; if image or video includes people, personal health information, or intellectual property, the image or video generated will not blur or maintain proportions of image subjects included.

Users are responsible for model inputs and outputs. Users are responsible for ensuring safe integration of this model, including implementing guardrails as well as other safety mechanisms, prior to deployment.

For more detailed information on ethical considerations for this model, please see the Model Card++ [Explainability](explainability-Cosmos3-Nano-Transfer-Auto.md), [Bias](bias.md), [Safety & Security](safety.md), and [Privacy](privacy.md) subcards. Please report model quality, risk, security vulnerabilities or NVIDIA AI Concerns [here](https://www.nvidia.com/en-us/support/submit-security-vulnerability/).
