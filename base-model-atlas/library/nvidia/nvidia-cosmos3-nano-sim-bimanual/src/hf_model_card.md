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

**[Cosmos3 Examples Collection](https://huggingface.co/collections/nvidia/cosmos3-examples)** | **[Code](https://github.com/nvidia/cosmos)** | **[Technical Report](https://research.nvidia.com/labs/cosmos-lab/cosmos-simulation/technical-report.pdf)** | **[Website](https://research.nvidia.com/labs/cosmos-lab/cosmos-simulation/)**

# Model Overview: Cosmos3-Nano-Sim-Bimanual

![Cosmos3 product and examples lineage highlighting Cosmos3-Nano-Sim-Bimanual](images/cosmos3-nano-sim-bimanual-graph.png)

The highlighted checkpoint, Cosmos3-Nano-Sim-Bimanual, is a post-trained, causal-distilled variant of the Cosmos3-Nano base model.

## Description

<p align="center">
  <video src="https://huggingface.co/nvidia/Cosmos3-Nano-Sim-Bimanual/resolve/main/images/cosmos3-nano-sim-bimanual-overview.mp4" controls autoplay loop muted playsinline width="640" aria-label="Generated results only: AgiBot 008 and 006, seed 2026, on the top row; YAM 001, seed 2025, and YAM 008, seed 2027, on the bottom row. First 15 seconds at original speed."></video>
  <br>
</p>

Cosmos3-Nano-Sim-Bimanual simulates how an environment evolves in response to a bimanual robot’s actions. It supports interleaved camera navigation and robot manipulation within a single action sequence in both open-loop and closed-loop settings, enabling continuous simulation across changes in camera pose and robot arm or gripper state. Given an initial image and a sequence of control inputs, the model generates video in small latent-frame chunks conditioned on cached history and incoming robot actions or camera trajectories. Control inputs can be supplied at any point during a rollout by a policy model, such as a vision-language-action (VLA) model or a world-action model, or by a human-operated joystick. These capabilities support robotic policy evaluation and verification, reinforcement learning (RL) training, and synthetic demonstration data generation without teleoperation when control inputs are supplied by a policy model.

Cosmos3-Nano-Sim-Bimanual was developed by NVIDIA as part of the Cosmos example model family.

For a quick start, see the [Cosmos3-Nano-Sim-Bimanual skill](https://github.com/NVIDIA/cosmos-framework/tree/main/.agents/skills/cosmos3-nano-sim-bimanual).

This model is ready for commercial or non-commercial use.

## License

This model is released under [OpenMDW1.1](https://openmdw.ai/license/1-1/).

## Deployment Geography

Global

## Use Case

Physical AI for robotics: policy evaluation and verification, reinforcement learning (RL) training, and synthetic demonstration data generation with interleaved camera navigation and bimanual manipulation actions. Policy-generated control inputs enable demonstration generation without teleoperation.

## Release Date

- Hugging Face 10/20/2026 via [https://huggingface.co/collections/nvidia/cosmos3-examples](https://huggingface.co/collections/nvidia/cosmos3-examples)
- GitHub 10/20/2026 via [https://github.com/nvidia/cosmos](https://github.com/nvidia/cosmos)

## Model Architecture

**Architecture Type:** Transformer

**Network Architecture:** Mixture-of-Transformers (MoT)

Cosmos3-Nano-Sim-Bimanual is derived from [Cosmos3-Nano](https://huggingface.co/nvidia/Cosmos3-Nano) through post-training on a mixture of robot manipulation videos paired with robot actions and camera navigation videos paired with camera trajectories, followed by causal distillation. It generates video in small latent-frame chunks conditioned on cached history and incoming control inputs. The model supports interleaved robot manipulation and camera navigation within a single action sequence, maintaining scene continuity across robot motion and viewpoint changes. Additional post-training on user-provided data can adapt the model to different robot embodiments and arm configurations; see the [Cosmos3-Nano-Sim-Bimanual skill](https://github.com/NVIDIA/cosmos-framework/tree/main/.agents/skills/cosmos3-nano-sim-bimanual) for details.

This model was developed using the [Cosmos Framework](https://github.com/NVIDIA/cosmos-framework).

**Number of trainable model parameters:** 16B

## Inputs

- **Input Type(s):** Image, robot actions, camera trajectories, text (optional scene description)
- **Input Format(s):**
  - **Image:** JPG, PNG, JPEG, or WebP (initial frame)
  - **Robot actions:** JSON containing a sequence of robot state or control values with shape `(T, D)`, where `T` is the number of action steps and `D` is the embodiment-specific action dimensionality
  - **Camera trajectories:** Sequence of camera poses (for example, a 9D camera-motion representation)
  - **Text:** String
- **Input Parameters:**
  - **Image:** Two-dimensional (2D)
  - **Robot actions / Camera trajectories:** Two-dimensional sequences (time steps × control dimensions)
  - **Text:** One-dimensional (1D)
- **Other Properties Related to Input:**
  - Actions are aligned with the generated video.
  - Supported embodiment: AgiBot

## Outputs

- **Output Type(s):** Video
- **Output Format(s):**
  - **Video:** MP4 or streamed video frames
- **Output Parameters:**
  - **Video:** Three-dimensional (3D)
- **Other Properties Related to Output:**
  - Generates video at 480p with an output frame rate of 30 frames per second (fps).
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

**Cosmos3-Nano-Sim-Bimanual — V1.0 (10/20/2026)**

Cosmos3-Nano-Sim-Bimanual is a post-trained, causal-distilled variant of [Cosmos3-Nano](https://huggingface.co/nvidia/Cosmos3-Nano).

It can be integrated into a closed-loop robotic policy evaluation or training pipeline that supplies an initial image and a sequence of robot actions and camera trajectories from a policy model or human controller. The model supports this interaction by returning generated video frames as visual observations for subsequent policy or controller inputs.

## Training and Evaluation Datasets

### Post-Training Datasets

**Data Modality:** Video, Text, and paired robot-action or camera-trajectory data.

**Post-Training Data Size:**
- **Text:** 1 Billion to 10 Trillion Tokens
- **Video with paired robot-action or camera-trajectory data:** 10,000 to 1 Million Hours

**Data Collection Method:** Hybrid: Automatic/Sensors, Synthetic, Automated.

**Labeling Method:** Hybrid: Manually-Labeled, Automated.

**Properties:** The post-training datasets consist of robot manipulation and camera navigation videos, associated English captions, robot actions, and camera trajectories. The data includes real and synthetic content from vendor-provided, public, and NVIDIA-created datasets.

### Dataset Overview

- **Total Size:** 1.3B data points
- **Total Number of Datasets:** 393 dataset entries
- **Dataset partition:** Training [100%], Testing [N/A — evaluation benchmarks used separately], Validation [N/A — evaluation benchmarks used separately]
- **Time period for training data collection:** 2024–2026
- **Time period for validation data collection:** N/A (standard public benchmarks)

Raw data from internal and external sources is transformed into training-ready data through multiple stages of curation, filtering, and quality review. Data acquisition spans diverse multimodal sources — robotics, autonomous driving, industrial environments, indoor and outdoor scenes, varied lighting and weather conditions, camera viewpoints, object categories, and human activities — to broaden coverage across Physical AI operating environments. Automated filtering pipelines remove corrupted, duplicate, low-quality, and restricted content. Metadata analysis, heuristic rules, and model-assisted classifiers are applied during preprocessing to flag anomalous distributions and low-diversity subsets. Human review supplements automated filtering for selected datasets, benchmark construction, and targeted quality analysis. Datasets are balanced across modalities and task categories — visual reasoning, text-to-image, text-to-video, image-to-video, audio generation, video transfer, action-conditioned generation, and action command generation — to reduce overrepresentation of narrow domains. Synthetic and simulation-based augmentation supplements coverage of rare physical interactions and edge-case scenarios. Deduplication and provenance tracking are applied across the corpus. The resulting processed data is converted into model-ready tokenized or encoded representations through modality-specific preprocessors before training begins.

Training datasets passed through multiple layers of automated and manual safeguards designed to reduce the presence of harmful or policy-violating content across categories including weapons and weapons-related instructional content, criminal planning, child sexual abuse material (CSAM), non-consensual intimate imagery (NCII), sexual content involving minors, harassment, hate speech, profanity, threats and incitement to violence, self-harm or suicide-related content, and graphic violence. Data sources are reviewed for licensing compatibility, provenance, and alignment with internal data governance and safety policies before admission into training corpora. Automated filtering pipelines combine multiple detection strategies: hash-matching against known CSAM and NCII reference databases; classifier-based moderation models trained for explicit sexual content, hate speech, violence, weapons imagery, and other restricted categories; keyword and regex-based screening for criminal-planning, threats, and self-harm phrases in text data; metadata and provenance heuristics for source-level risk signals; and embedding-based anomaly detection to surface samples that fall outside expected distributions. Human review and targeted audits supplement automated filtering for selected datasets, benchmark construction, and safety-sensitive evaluation. For multimodal Physical AI data (robotics, autonomous driving, industrial scenes), additional filtering targets invalid action trajectories, physically implausible interactions, and unsafe control sequences. Synthetic and simulation-generated data are evaluated through internal validation before inclusion. Benchmark evaluations and red-team testing are applied post-training to surface remaining safety gaps across world generation, reasoning, audio, and action tasks. No large-scale data-filtering process can guarantee complete removal of all harmful content; residual risks may remain, particularly in rare edge cases or open-world deployment settings. Ongoing monitoring and dataset review continue post-release.

- For more information about the datasets used to train this model, please see the [**Public Summary of Training Content**](https://docs.nvidia.com/cosmos/latest/cosmos3/index.html).

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

### Camera Navigation Benchmark

#### [PAI-Bench-G](https://arxiv.org/abs/2512.01989) Image-to-Video (I2V)

We evaluate **Cosmos3-Nano-Sim-Bimanual** against LingBot-World 2.0 and Sana-WM on sustained viewpoint control. Each example supplies an initial image, a scene caption, and a camera trajectory; captions exclude camera motion. The [PAI-Bench-G](https://arxiv.org/abs/2512.01989) quality score measures video fidelity and consistency. [ViPE](https://research.nvidia.com/labs/toronto-ai/vipe/) estimates camera positions and orientations from the generated video. We fit the estimated trajectory to the input trajectory by rotation, translation, and uniform scaling (Umeyama alignment), allowing comparison independent of coordinate frame and scale. Absolute translation error (ATE) measures camera-position error after alignment; relative translation error (RTE) and relative rotation error (RRE) measure errors in camera displacement and orientation change between poses. Perceptual drift evaluates changes in video quality over time.

<table>
  <thead>
    <tr>
      <th scope="col" style="text-align: left;">Model</th>
      <th scope="col" style="text-align: right;">Video Quality ↑</th>
      <th scope="col" style="text-align: right;">ATE ↓</th>
      <th scope="col" style="text-align: right;">RTE ↓</th>
      <th scope="col" style="text-align: right;">RRE ↓</th>
      <th scope="col" style="text-align: right;">Perceptual Drift ↓</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="text-align: left;">LingBot-World 2.0</td>
      <td style="text-align: right;">65.3577</td>
      <td style="text-align: right;"><strong>4.1698</strong></td>
      <td style="text-align: right;">0.0596</td>
      <td style="text-align: right;">0.1781</td>
      <td style="text-align: right;"><strong style="color: inherit;">0.0209</strong></td>
    </tr>
    <tr>
      <td style="text-align: left;">Sana-WM</td>
      <td style="text-align: right;">65.2090</td>
      <td style="text-align: right;">6.4823</td>
      <td style="text-align: right;">0.1284</td>
      <td style="text-align: right;">0.1601</td>
      <td style="text-align: right;">0.0299</td>
    </tr>
    <tr>
      <td style="text-align: left; background-color: #e8f4df; color: #18202b;"><strong style="color: inherit;">Cosmos3-Nano-Sim-Bimanual</strong></td>
      <td style="text-align: right; background-color: #e8f4df; color: #18202b;"><strong style="color: inherit;">73.9099</strong></td>
      <td style="text-align: right; background-color: #e8f4df; color: #18202b;">4.7072</td>
      <td style="text-align: right; background-color: #e8f4df; color: #18202b;"><strong style="color: inherit;">0.0545</strong></td>
      <td style="text-align: right; background-color: #e8f4df; color: #18202b;"><strong style="color: inherit;">0.1002</strong></td>
      <td style="text-align: right; background-color: #e8f4df; color: #18202b;">0.0210</td>
    </tr>
  </tbody>
</table>

#### Sana-WM simple

The simple split of [Sana-WM-Bench](https://arxiv.org/abs/2605.15178) reports visual quality, camera alignment, and drift. We pair benchmark runs by source inputs and trajectories, using the same metrics as the [PAI-Bench-G](https://arxiv.org/abs/2512.01989) I2V evaluation.

<table>
  <thead>
    <tr>
      <th scope="col" style="text-align: left;">Model</th>
      <th scope="col" style="text-align: right;">Video Quality ↑</th>
      <th scope="col" style="text-align: right;">ATE ↓</th>
      <th scope="col" style="text-align: right;">RTE ↓</th>
      <th scope="col" style="text-align: right;">RRE ↓</th>
      <th scope="col" style="text-align: right;">Perceptual Drift ↓</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="text-align: left;">LingBot-World 2.0</td>
      <td style="text-align: right;">65.9748</td>
      <td style="text-align: right;">1.4254</td>
      <td style="text-align: right;">0.0185</td>
      <td style="text-align: right;">0.2591</td>
      <td style="text-align: right;">0.0371</td>
    </tr>
    <tr>
      <td style="text-align: left;">Sana-WM</td>
      <td style="text-align: right;">66.0599</td>
      <td style="text-align: right;">1.2159</td>
      <td style="text-align: right;">0.0192</td>
      <td style="text-align: right;">0.2356</td>
      <td style="text-align: right;">0.0223</td>
    </tr>
    <tr>
      <td style="text-align: left; background-color: #e8f4df; color: #18202b;"><strong style="color: inherit;">Cosmos3-Nano-Sim-Bimanual</strong></td>
      <td style="text-align: right; background-color: #e8f4df; color: #18202b;"><strong style="color: inherit;">77.2887</strong></td>
      <td style="text-align: right; background-color: #e8f4df; color: #18202b;"><strong style="color: inherit;">1.0040</strong></td>
      <td style="text-align: right; background-color: #e8f4df; color: #18202b;"><strong style="color: inherit;">0.0124</strong></td>
      <td style="text-align: right; background-color: #e8f4df; color: #18202b;"><strong style="color: inherit;">0.0551</strong></td>
      <td style="text-align: right; background-color: #e8f4df; color: #18202b;"><strong style="color: inherit;">0.0118</strong></td>
    </tr>
  </tbody>
</table>

#### Sana-WM hard

The hard split of [Sana-WM-Bench](https://arxiv.org/abs/2605.15178) reports visual quality, camera alignment, and drift. We pair benchmark runs by source inputs and trajectories, using the same metrics as the simple split.

<table>
  <thead>
    <tr>
      <th scope="col" style="text-align: left;">Model</th>
      <th scope="col" style="text-align: right;">Video Quality ↑</th>
      <th scope="col" style="text-align: right;">ATE ↓</th>
      <th scope="col" style="text-align: right;">RTE ↓</th>
      <th scope="col" style="text-align: right;">RRE ↓</th>
      <th scope="col" style="text-align: right;">Perceptual Drift ↓</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="text-align: left;">LingBot-World 2.0</td>
      <td style="text-align: right;">64.5462</td>
      <td style="text-align: right;">1.3423</td>
      <td style="text-align: right;"><strong>0.0161</strong></td>
      <td style="text-align: right;">0.3264</td>
      <td style="text-align: right;">0.0372</td>
    </tr>
    <tr>
      <td style="text-align: left;">Sana-WM</td>
      <td style="text-align: right;">65.5699</td>
      <td style="text-align: right;">1.3165</td>
      <td style="text-align: right;">0.0178</td>
      <td style="text-align: right;">0.1826</td>
      <td style="text-align: right;">0.0251</td>
    </tr>
    <tr>
      <td style="text-align: left; background-color: #e8f4df; color: #18202b;"><strong style="color: inherit;">Cosmos3-Nano-Sim-Bimanual</strong></td>
      <td style="text-align: right; background-color: #e8f4df; color: #18202b;"><strong style="color: inherit;">76.3971</strong></td>
      <td style="text-align: right; background-color: #e8f4df; color: #18202b;"><strong style="color: inherit;">1.3085</strong></td>
      <td style="text-align: right; background-color: #e8f4df; color: #18202b;"><strong style="color: inherit;">0.0161</strong></td>
      <td style="text-align: right; background-color: #e8f4df; color: #18202b;"><strong style="color: inherit;">0.1774</strong></td>
      <td style="text-align: right; background-color: #e8f4df; color: #18202b;"><strong style="color: inherit;">0.0161</strong></td>
    </tr>
  </tbody>
</table>

### Robot Manipulation Benchmark

#### AgiBot-World

We evaluate **Cosmos3-Nano-Sim-Bimanual** on observation prediction conditioned on AgiBot-World action sequences, an initial image, and a caption, comparing against the bidirectional DreamDojo 2B and 14B teacher models. The [PAI-Bench-G](https://arxiv.org/abs/2512.01989) quality score measures video fidelity and consistency. PSNR measures pixel-level agreement, SSIM measures image-structure agreement, and [LPIPS](https://arxiv.org/abs/1801.03924) measures differences in learned visual features. These metrics compare generated and reference frames and serve as proxies for action following. Perceptual drift evaluates changes in video quality over time.

<table>
  <thead>
    <tr>
      <th scope="col" style="text-align: left;">Model</th>
      <th scope="col" style="text-align: right;">Video Quality ↑</th>
      <th scope="col" style="text-align: right;">PSNR (dB) ↑</th>
      <th scope="col" style="text-align: right;">SSIM ↑</th>
      <th scope="col" style="text-align: right;">LPIPS ↓</th>
      <th scope="col" style="text-align: right;">Perceptual Drift ↓</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="text-align: left;">DreamDojo 2B</td>
      <td style="text-align: right;">74.5327</td>
      <td style="text-align: right;">12.1016</td>
      <td style="text-align: right;">0.6405</td>
      <td style="text-align: right;">0.3766</td>
      <td style="text-align: right;">0.0149</td>
    </tr>
    <tr>
      <td style="text-align: left;">DreamDojo 14B</td>
      <td style="text-align: right;">74.9390</td>
      <td style="text-align: right;">12.3561</td>
      <td style="text-align: right;">0.6635</td>
      <td style="text-align: right;">0.3586</td>
      <td style="text-align: right;">0.0133</td>
    </tr>
    <tr>
      <td style="text-align: left; background-color: #e8f4df; color: #18202b;"><strong style="color: inherit;">Cosmos3-Nano-Sim-Bimanual</strong></td>
      <td style="text-align: right; background-color: #e8f4df; color: #18202b;"><strong style="color: inherit;">76.0884</strong></td>
      <td style="text-align: right; background-color: #e8f4df; color: #18202b;"><strong style="color: inherit;">14.4138</strong></td>
      <td style="text-align: right; background-color: #e8f4df; color: #18202b;"><strong style="color: inherit;">0.6839</strong></td>
      <td style="text-align: right; background-color: #e8f4df; color: #18202b;"><strong style="color: inherit;">0.3454</strong></td>
      <td style="text-align: right; background-color: #e8f4df; color: #18202b;"><strong style="color: inherit;">0.0118</strong></td>
    </tr>
  </tbody>
</table>

#### AgiBot-GEAR

We evaluate **Cosmos3-Nano-Sim-Bimanual** on observation prediction conditioned on AgiBot-GEAR action sequences, an initial image, and a caption, comparing against the bidirectional DreamDojo 2B and 14B teacher models. We use the same video quality, reference-frame agreement, and drift metrics as the AgiBot-World evaluation.

<table>
  <thead>
    <tr>
      <th scope="col" style="text-align: left;">Model</th>
      <th scope="col" style="text-align: right;">Video Quality ↑</th>
      <th scope="col" style="text-align: right;">PSNR (dB) ↑</th>
      <th scope="col" style="text-align: right;">SSIM ↑</th>
      <th scope="col" style="text-align: right;">LPIPS ↓</th>
      <th scope="col" style="text-align: right;">Perceptual Drift ↓</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="text-align: left;">DreamDojo 2B</td>
      <td style="text-align: right;">72.4586</td>
      <td style="text-align: right;">11.5709</td>
      <td style="text-align: right;">0.5437</td>
      <td style="text-align: right;">0.4638</td>
      <td style="text-align: right;">0.0232</td>
    </tr>
    <tr>
      <td style="text-align: left;">DreamDojo 14B</td>
      <td style="text-align: right;">73.0033</td>
      <td style="text-align: right;">12.1113</td>
      <td style="text-align: right;">0.5818</td>
      <td style="text-align: right;">0.4326</td>
      <td style="text-align: right;">0.0218</td>
    </tr>
    <tr>
      <td style="text-align: left; background-color: #e8f4df; color: #18202b;"><strong style="color: inherit;">Cosmos3-Nano-Sim-Bimanual</strong></td>
      <td style="text-align: right; background-color: #e8f4df; color: #18202b;"><strong style="color: inherit;">74.4912</strong></td>
      <td style="text-align: right; background-color: #e8f4df; color: #18202b;"><strong style="color: inherit;">14.0158</strong></td>
      <td style="text-align: right; background-color: #e8f4df; color: #18202b;"><strong style="color: inherit;">0.6172</strong></td>
      <td style="text-align: right; background-color: #e8f4df; color: #18202b;"><strong style="color: inherit;">0.4057</strong></td>
      <td style="text-align: right; background-color: #e8f4df; color: #18202b;"><strong style="color: inherit;">0.0188</strong></td>
    </tr>
  </tbody>
</table>

## Inference

**Acceleration Engine:** [PyTorch](https://pytorch.org/), [vLLM-Omni](https://github.com/vllm-project/vllm-omni)

**Test Hardware:** NVIDIA Blackwell GB200, NVIDIA Hopper H100, H200, H20, RTX PRO 6000

### Inference Performance

Numbers are based on vLLM-Omni, using a single GPU. Empty table cells indicate that measurements are not reported.

|  | 480p inference throughput (frames/s) |
| --- | --- |
| GB200 | 54.1 |
| H100 | 32.6 |
| H200 | 32.4 |
| H20 | 10.7 |
| RTX Pro 6000 | 20.6 |

## Usage Example

### Quick Start

This example serves the model with
[vLLM-Omni](https://github.com/vllm-project/vllm-omni) and generates the mixed-action AgiBot example: 901 frames at 30 FPS from one initial
image and 900 normalized 59D actions combining robot actions and camera motion.
The checkpoint uses a fixed four-step sampler.

#### 1. Start the server

On a Linux host with an NVIDIA GPU (tested on one GB200), [Docker](https://docs.docker.com/engine/install/), and the [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html):

```bash
docker run --runtime nvidia --gpus all --ipc=host \
  -v ~/.cache/huggingface:/root/.cache/huggingface \
  --env "HF_TOKEN=$HF_TOKEN" \
  --env VLLM_OMNI_VIDEO_SYNC_TIMEOUT=1800 \
  -p 127.0.0.1:8000:8000 \
  vllm/vllm-omni:cosmos3 \
  vllm serve nvidia/Cosmos3-Nano-Sim-Bimanual \
    --omni --model-class-name Cosmos3NanoSimBimanualPipeline \
    --deploy-config /app/vllm-omni/vllm_omni/deploy/cosmos3_nano_sim_bimanual_windowed.yaml \
    --no-guardrails \
    --host 0.0.0.0 --port 8000 --init-timeout 1800
```

The container publishes the server on `127.0.0.1:8000` of the host.
`--deploy-config` selects the Bimanual deployment: one request at a time, eager
execution, and a 64-latent-frame rolling key/value cache with eight attention
sinks. `--no-guardrails` disables the Cosmos3 text and video safety checks. The
first start downloads the checkpoint. For optimized server settings and
additional examples, see the
[Bimanual vLLM-Omni notebook](https://github.com/NVIDIA/cosmos-framework/blob/main/.agents/skills/cookbooks/cosmos3/simulation/bimanual/run_bimanual_with_vllm_omni.ipynb).

#### 2. Generate the mixed-action video

Install the client dependencies in your Python environment:

```bash
pip install requests huggingface_hub
```

Run the client on the same machine as the server. The example metadata supplies
the prompt, frame count, frame rate, action domain, resolution, and seed 2026:

```python
import json
from pathlib import Path
from uuid import uuid4

import requests
from huggingface_hub import snapshot_download

MODEL = "nvidia/Cosmos3-Nano-Sim-Bimanual"
repo_dir = Path(snapshot_download(MODEL, allow_patterns=[
    "examples/inference/sim_bimanual_mixed_action_hf.jsonl",
    "assets/sim_bimanual/agibot/images/agibot_mixed_028_initial.png",
    "assets/sim_bimanual/agibot/actions/agibot_mixed_028_normalized_mixed_action.json",
    "cosmos3_nano_sim_bimanual_action_sources/action_schema.json",
]))
manifest_path = repo_dir / "examples/inference/sim_bimanual_mixed_action_hf.jsonl"
image_path = repo_dir / "assets/sim_bimanual/agibot/images/agibot_mixed_028_initial.png"
action_path = repo_dir / "assets/sim_bimanual/agibot/actions/agibot_mixed_028_normalized_mixed_action.json"
schema_path = repo_dir / "cosmos3_nano_sim_bimanual_action_sources/action_schema.json"

examples = [json.loads(line) for line in manifest_path.read_text().splitlines()]
example = next(item for item in examples if item["action_path"].endswith("/" + action_path.name))
action = json.loads(action_path.read_text())
schema = json.loads(schema_path.read_text())
domain_ids = {
    name: values["domain_id"]
    for name, values in schema["embodiments"].items()
}

extra_params = {
    "session_id": uuid4().hex,
    "reset": True,
    "close_session": True,
    "action_mode": "forward_dynamics",
    "action_space": action["action_space"],
    "action": action["action"],
    "domain_name": example["domain_name"],
    "domain_id": [domain_ids[name] for name in action["domain_names"]],
    "resolution": int(example["resolution"]),
}

with image_path.open("rb") as image_file:
    response = requests.post(
        "http://127.0.0.1:8000/v1/videos/sync",
        data={
            "model": MODEL,
            "prompt": example["prompt"],
            "num_frames": str(example["num_frames"]),
            "fps": str(example["fps"]),
            "seed": str(example["seed"]),
            "extra_params": json.dumps(extra_params),
        },
        files={"input_reference": (image_path.name, image_file, "image/png")},
        headers={"Accept": "video/mp4"},
        timeout=1860,
    )
response.raise_for_status()
Path("cosmos3-nano-sim-bimanual-mixed-028.mp4").write_bytes(response.content)
```

Generated output:

<video src="https://huggingface.co/nvidia/Cosmos3-Nano-Sim-Bimanual/resolve/main/assets/output/cosmos3-nano-sim-bimanual-quickstart.mp4" controls autoplay loop muted playsinline width="100%"></video>

The initial image is the only visual observation sent to the server. The action
values are already normalized for this checkpoint.

### Quick Start with SGLang

[SGLang](https://github.com/sgl-project/sglang) serves the same model through its OpenAI-compatible Videos API and generates the same mixed-action example. The request is the same shape, an uploaded initial image plus inline actions, but the server takes the embodiment names from the action sidecar instead of domain IDs, and generation runs as an asynchronous job that the client polls. For the other published examples with SGLang, see the [SGLang notebook](https://github.com/NVIDIA/cosmos-framework/blob/main/.agents/skills/cookbooks/cosmos3/simulation/bimanual/run_bimanual_with_sglang.ipynb).

#### 1. Start the server

On the same kind of host, with the published [`lmsysorg/sglang:dev`](https://hub.docker.com/r/lmsysorg/sglang/tags) image, which includes the Cosmos3 pipelines from [sgl-project/sglang#39475](https://github.com/sgl-project/sglang/pull/39475):

```bash
export SGLANG_HF_CACHE="${SGLANG_HF_CACHE:-$HOME/.cache/sglang-huggingface}"  # The container runs as root.
mkdir -p "$SGLANG_HF_CACHE"
chmod 777 "$SGLANG_HF_CACHE"
# The same history window as the vLLM-Omni windowed deployment above.
cat > cosmos3_bimanual_window.json <<'EOF'
{"history_mode": "sliding", "kv_cache_inference_size": 64, "attention_sink_size": 8}
EOF
docker pull lmsysorg/sglang:dev
docker run --init --runtime nvidia --gpus all --ipc=host \
  -v "$SGLANG_HF_CACHE:/root/.cache/huggingface" \
  -v "$PWD:$PWD:ro" \
  --env "HF_TOKEN=$HF_TOKEN" \
  -p 127.0.0.1:30000:30000 \
  lmsysorg/sglang:dev \
  sglang serve \
    --model-path nvidia/Cosmos3-Nano-Sim-Bimanual \
    --pipeline-config-path "$PWD/cosmos3_bimanual_window.json" \
    --host 0.0.0.0 --port 30000
```

The container publishes the server on `127.0.0.1:30000` of the host and mounts the working directory, read-only, at the same path so that it can read the pipeline-config file; the client uploads the initial image and sends the actions inline, so the server needs no other access to the client's files. `--pipeline-config-path` selects a 64-frame rolling key/value cache with eight attention sinks, the window the vLLM-Omni example uses: eight pinned frames, 55 recent frames, and the frame being generated. Without it SGLang keeps the full 901-frame history, which exhausts a 141 GB GPU on this example. The start-up log confirms the setting with `sliding history, 64-frame cache = 8 sinks + 55 recent + current`. The `dev` tag moves with SGLang's main branch, so pull it before each start. The first start downloads the checkpoint; the HTTP port opens after the weights are loaded and the warmup request finishes. The distilled checkpoint fixes the step count and guidance, so the request sets neither.

#### 2. Generate the mixed-action video

Run the client from the same directory. The example metadata supplies the prompt, frame count, frame rate, embodiment, and seed 2026:

```bash
pip install requests huggingface_hub
```

```python
import json
import time
from pathlib import Path

import requests
from huggingface_hub import snapshot_download

MODEL = "nvidia/Cosmos3-Nano-Sim-Bimanual"
SERVER = "http://127.0.0.1:30000"
repo_dir = Path(snapshot_download(MODEL, allow_patterns=[
    "examples/inference/sim_bimanual_mixed_action_hf.jsonl",
    "assets/sim_bimanual/agibot/images/agibot_mixed_028_initial.png",
    "assets/sim_bimanual/agibot/actions/agibot_mixed_028_normalized_mixed_action.json",
]))
manifest_path = repo_dir / "examples/inference/sim_bimanual_mixed_action_hf.jsonl"
image_path = repo_dir / "assets/sim_bimanual/agibot/images/agibot_mixed_028_initial.png"
action_path = repo_dir / "assets/sim_bimanual/agibot/actions/agibot_mixed_028_normalized_mixed_action.json"

examples = [json.loads(line) for line in manifest_path.read_text().splitlines() if line.strip()]
example = next(item for item in examples if item["action_path"].endswith("/" + action_path.name))
action = json.loads(action_path.read_text())  # 900 normalized 59D rows and one embodiment name per row.

# The rows travel inline; the server parses each multipart field within 1 MiB (about 0.5 MB here).
extra_params = json.dumps({
    "action_mode": "forward_dynamics",
    "domain_name": example["domain_name"],
    "domain_names": action["domain_names"],
    "action_normalization": "none",
    "action_view_point": "ego_view",
    "format_prompt_as_json": example["format_prompt_as_json"],
    "action": action["action"],
}, separators=(",", ":"))
assert len(extra_params.encode()) <= 1024 * 1024, "Shorten the rollout or raise the server's form-field limit."

form = {
    "model": MODEL,
    "prompt": example["prompt"],
    "size": "832x480",  # The 480p canvas closest to the 640 x 360 initial image.
    "num_frames": str(example["num_frames"]),
    "fps": str(example["fps"]),
    "seed": str(example["seed"]),
    "extra_params": extra_params,
}
# Submit the job with the initial image, poll it, and download the video.
with image_path.open("rb") as image_file:
    response = requests.post(
        f"{SERVER}/v1/videos", data=form,
        files={"input_reference": (image_path.name, image_file, "image/png")},
        timeout=60,
    )
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
Path("cosmos3-nano-sim-bimanual-mixed-028.mp4").write_bytes(video.content)
```

The initial image is the only visual observation sent to the server. The action values are already normalized for this checkpoint.

## Ethical Considerations

NVIDIA believes Trustworthy AI is a shared responsibility and we have established policies and practices to enable development for a wide array of AI applications. Developers should work with their internal model team to ensure this model meets requirements for the relevant industry and use case and addresses unforeseen product misuse.

Please make sure you have proper rights and permissions for all input image and video content; if image or video includes people, personal health information, or intellectual property, the image or video generated will not blur or maintain proportions of image subjects included.

Users are responsible for model inputs and outputs. Users are responsible for ensuring safe integration of this model, including implementing guardrails as well as other safety mechanisms, prior to deployment.

For more detailed information on ethical considerations for this model, please see the Model Card++ [Explainability](explainability-Cosmos3-Nano-Sim-Bimanual.md), [Bias](bias.md), [Safety & Security](safety.md), and [Privacy](privacy.md) subcards. Please report model quality, risk, security vulnerabilities or NVIDIA AI Concerns [here](https://www.nvidia.com/en-us/support/submit-security-vulnerability/).
