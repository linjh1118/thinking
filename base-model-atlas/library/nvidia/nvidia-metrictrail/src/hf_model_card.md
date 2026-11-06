---
license: other
license_name: nvidia-open-model-license
license_link: >-
  https://developer.download.nvidia.com/licenses/NVIDIA-OneWay-Noncommercial-License-22Mar2022.pdf?t=eyJscyI6ImdzZW8iLCJsc2QiOiJ
---

## Description:

MetricTrail estimates camera motion and per-frame metric depth from long RGB
image sequences for visual odometry and 3D reconstruction research. It combines
single-image metric depth, learned sparse correspondences, and local geometric
optimization, with supplied or RGB-estimated intrinsics and optional rectified
stereo. MetricTrail 1.0 was developed by NVIDIA.

The repository provides a CLI that exports camera trajectories and caches
per-frame depth. Model weights are not included in the source repository;
the DINO-DPVO checkpoint is planned for a separate Hugging Face release.
The CLI does not export dense point clouds or meshes. The dense-reconstruction
results below use a separate research evaluation workflow.

This model is for research and development only.

### License/Terms of Use:

Use of the model weights is governed by the [NVIDIA License](https://developer.download.nvidia.com/licenses/NVIDIA-OneWay-Noncommercial-License-22Mar2022.pdf), which limits use to noncommercial research or evaluation, subject to the agreement. Use of the DPVO base model is governed by the [MIT License](https://opensource.org/license/mit). Original NVIDIA-authored source and documentation marked Apache-2.0 use the [Apache License 2.0](../LICENSE). Incorporated source, separately obtained upstream weights, and datasets retain their applicable terms; DINOv3 uses the [DINOv3 License](https://github.com/facebookresearch/dinov3/blob/main/LICENSE.md). See [THIRD_PARTY_NOTICES.md](../THIRD_PARTY_NOTICES.md) and the [repository license scope](../README.md#license) for inherited MIT and BSD terms and the removal of legacy retrieval, alignment, and optical-flow helpers. Separately obtained retrieval tools retain their own applicable terms. Source licenses do not replace model-weight or dataset terms.

### Deployment Geography:

Global

### Use Case:

- Research on long-video camera-motion estimation and metric 3D reconstruction.
- Studying metric-depth priors, visual representations, and sparse local
  optimization for visual odometry and mapping.
- Reconstructing indoor and outdoor scenes for computer vision, graphics,
  simulation, and robotics research, with independent validation of geometry.
- Comparing calibrated monocular, RGB-only calibration, and calibrated stereo
  reconstruction under the reported protocols.

### Release Date:

Hugging Face 11/05/2026 via [https://huggingface.co/nvidia/metrictrail](https://huggingface.co/nvidia/metrictrail)


## Model Architecture:

**Architecture Type:** Learned recurrent visual odometry with frozen visual
foundation-model features and explicit bundle adjustment.

**Network Architecture:** DPVO's sparse patch correspondence network with
learned residual feature-fusion adapters, a frozen DINOv3-S/16 encoder, and a
frozen MoGe-2 metric-depth provider. The complete system includes camera
calibration and optional pose-graph correction.

**Number of model parameters:** The DINO-DPVO checkpoint for the separate
Hugging Face release contains
**3,425,860 learned parameters (3.43 million)** across 100 FP32 weight/bias
tensors. This count excludes the frozen DINOv3 backbone, external MoGe-2 depth
model, calibration dependencies, and optional SALAD and RoMa models.

The local estimator alternates learned patch matching with joint optimization
of camera poses and sparse patch inverse depths in a bounded active window.
MoGe-2 independently predicts metric camera-Z depth for each image. These
predictions initialize patch depths and remain robust soft constraints during
optimization; multi-view evidence can override unreliable prior measurements.
In the dense-reconstruction workflow, frame-level depth maps are
placed in a shared world frame using the recovered poses and are not themselves
bundle-adjustment variables.

Frozen DINOv3 features augment the matching map and recurrent patch context
through learned residual adapters. Its 384-dimensional features are projected
to 64 channels and split into two 32-channel branches that augment the
128-channel matching stream and 384-dimensional recurrent context. Final
residual projections are initialized to zero so adaptation starts from the
official DPVO checkpoint's predictions.

We train MetricTrail for 15,000 optimizer steps with global batch size 16 on
16 NVIDIA A100 80GB GPUs, taking approximately seven hours. Fusion branches
first warm up on 5,000 TartanAir clips with odometry frozen; odometry and fusion
branches are then jointly fine-tuned on the remaining 235,000 clips. DINOv3 stays
frozen, and MoGe-2 is not used during adaptation. Joint training uses AdamW,
learning rates of 8e-6 for odometry and 8e-5 for fusion, weight decay 1e-6,
linear OneCycle annealing with 1% warmup, gradient clipping at 10, and seed 1234. Each clip
uses 80 patches per frame and 18 recurrent refinements. The frozen DINOv3
forward pass uses BF16; adapters, odometry, differentiable bundle adjustment,
and losses use FP32.

## Input:

**Input Type(s):** A temporally ordered RGB image sequence and camera parameters;
optionally synchronized left/right image sequences for stereo. A JSON
configuration selects the data adapter and processing settings.

**Input Format(s):** Prepared PNG frames or KITTI NPZ files containing `images`
as `uint8 [N,3,H,W]`. The repository also supplies Oxford Spires and LaMAria
inventory adapters. Loaders produce CHW RGB `float32` images in `[0,1]`.
Arbitrary video containers are not decoded by this CLI. 

Optional loop correction consumes a saved local trajectory NPZ, its successful
JSON sidecar, and an externally generated candidate JSON containing frame pairs
and scores. The candidate file records the baseline NPZ's SHA256; the candidate
file's own SHA256 must also be supplied.

**Input Parameters:** A configured frame inventory with at least 16 images,
positive FPS, and image dimensions `(H,W)`. Intrinsics use `[fx,fy,cx,cy]` in
processed-image pixel coordinates. In calibrated KITTI mode, `intrinsics`, `K`,
or `input_intrinsics` in the NPZ may be a four-vector, a 3 x 3 matrix, or an
`[N,4]` array; the last format uses its first row as the shared camera model.
Supplied-intrinsic adapters also exist for VBR and LaMAria. RGB-only mode
estimates one shared camera model.

Stereo takes a synchronized, rectified right-image PNG inventory and a positive
`stereo_baseline_m`, with a fixed horizontal rig translation. The public
configuration does not expose an arbitrary stereo extrinsic matrix. Metric
camera-Z depth is predicted internally by MoGe-2 ViT-L without a normal head,
available as `Ruicheng/moge-2-vitl`.

**Other Properties Related to Input:**

- Training uses 15-frame clips resized while preserving aspect ratio and
  center-cropped to 480 x 640. Inference raster size depends on the protocol;
  the canonical KITTI input is 280 x 504, and the 7Scenes trajectory
  protocol uses 434 x 574. The shipped KITTI and VBR configurations use
  280 x 504; Oxford uses 378 x 518. The 7Scenes evaluation uses a separate
  workflow; this repository does not include a 7Scenes adapter.
- Images and camera intrinsics must undergo consistent resize and crop
  transforms. Stereo requires synchronization, rectification, and a correct
  horizontal baseline consistent with the processed images.
- RGB-only calibration estimates intrinsics from a finite prefix, fixes the
  camera model, and replays that prefix before continuing online. Our
  evaluation initializes with the first 32 frames, and robust128
  calibration uses 128 selected keyframes. The repository exposes configurable
  calibration budgets. A shared focal correction is optimized while the
  principal point remains fixed.
- The implementation's metric-depth validity check requires a valid provider
  mask, finite depth, and camera-Z depth in the inclusive range 0.2-500 m.
  If a full-resolution prediction, its registered stride-4 depth raster, or
  all sampled patch centers contain no valid depth, the sequence terminates
  and the run cannot commit a successful complete trajectory. Failed runs may
  leave cache or older output files; use stage validation to establish success.
- `max_frames=0` uses the full configured inventory. The default DPVO frame
  buffer has capacity 32,768; buffer exhaustion raises an error. The bounded
  active optimization window does not make sequence duration or total cached
  data unlimited. The shared-intrinsic model assumes consistent camera geometry.

## Output:

**Output Type(s):** Per-frame camera trajectories, intrinsics, cached frame-level
metric depth and provider masks, and processing/audit metadata.

**Output Format(s):** Trajectory NPZ files with accompanying JSON records.
The frontend cache stores raw `depth.f32` and `mask.u8` arrays with JSON contract,
progress, and successful-completion records. It does not export dense point
clouds, meshes, or sparse patch geometry.

**Output Parameters:** `c2w` and inverse `w2c` have shape `[N,4,4]`;
`intrinsics` has shape `[N,4]`. The trajectory includes `frame_ids`,
`source_frame_ids`, `input_hw`, and stereo metadata. Poses refer to `cam0`, the
left camera for stereo. Cached camera-Z depth is FP32 `[N,H,W]`; the raw provider
mask is `uint8 [N,H,W]`. Consumers must also check finite depth and range;
the cached mask alone is not the final validity test.

KITTI local predictions are written under `output_root/local/inference/`;
other adapters use `output_root/local/inference/predictions/`. The separate
loop-correction command writes optional LC predictions under
`output_root/LC/inference/` and also retains `local_c2w` and the loop-edge count.
Depth caches are under
`output_root/frontend-cache/<dataset>/<case>/`.

Dense geometry is assembled by back-projecting camera-Z depth with intrinsics
and transforming it by `c2w`. The CLI outputs the depth and poses needed for
this operation but does not export dense reconstructions. Metric scale remains
an estimate. Learned correspondence weights should not be interpreted as
calibrated pose or depth uncertainty.

**Other Properties Related to Output:** Output length follows the processed
frame inventory. Trajectories use meters for translation and homogeneous
camera-to-world/world-to-camera matrices; cached depth uses meters along the
camera Z axis. Depth predictions are valid only where the provider mask is
valid, values are finite, and depth is in the inclusive range 0.2-500 m.
The pipeline raises an error for frames with no usable depth priors. Check
successful-completion records before consuming outputs; failed runs can retain
intermediate caches or older files. The model does not provide calibrated
pose/depth uncertainty or a guarantee of geometric correctness.

Our AI models are designed and/or optimized to run on NVIDIA GPU-accelerated
systems. By leveraging NVIDIA's hardware (e.g. GPU cores) and software frameworks
(e.g., CUDA libraries), the model achieves faster training and inference times
compared to CPU-only solutions. MetricTrail requires CUDA for the provided
pipeline; its reported benchmarks do not include a measured CPU comparison.

## Software Integration:

**Runtime Engine(s):** PyTorch/CUDA. The documented environment is Python 3.10,
PyTorch 2.5.1 and CUDA 12.4, with xformers for MoGe-2 attention, yacs, OpenCV,
Pillow, and SciPy. Separately invoked loop correction uses NumPy/SciPy on CPU,
with no PyTorch/CUDA, PyPose, FAISS or SALAD runtime dependency. The package
metadata permits broader versions, but those combinations have not been validated.
No precompiled DPVO CUDA extensions are included. Before tracking, build
`cuda_corr`, `cuda_ba`, and `lietorch_backends`
from source in the inference environment, using a compatible C++ compiler,
the CUDA toolkit including `nvcc`, and Eigen 3.4.0 headers. 

**Supported Hardware Microarchitecture Compatibility:**

NVIDIA Ampere (A100)

A CUDA device is required. Compatibility with other GPUs and a minimum memory
requirement have not been established.

**Supported Operating System(s):** Linux x86_64 is the documented tracking
environment. DPVO CUDA extensions must be built from source before tracking.
Validation results for other environments are not documented.

Run with `PYTHONNOUSERSITE=1`. The primary command is
`python -m metrictrail.cli --config <config.json>`; the default device is
`cuda:0`. `--case`, `--resume`, `--preflight`, and
`--stop-after {calibration,local}` control selection and stage execution.
Preflight checks external files and relevant runtime imports; it does not
validate model quality. 

The main pipeline ends at the local trajectory with `enable_lc: false`.
Run optional loop correction separately on CPU with
`python -m metrictrail.lc_cli --config <config.json> --case <case> --candidate-file <candidates.json> --candidate-sha256 <sha256>`.
MetricTrail consumes the supplied candidate pairs; it does not perform place
retrieval or launch an external retrieval tool.

Validate the implementation, camera model, data preprocessing, output
conventions, failure handling, and use-case performance before integrating
the system into a larger application. A measured benchmark memory footprint
does not by itself establish a supported hardware requirement.

The integration of foundation and fine-tuned models into AI systems requires
additional testing using use-case-specific data to ensure safe and effective
deployment. Following the V-model methodology, iterative testing and validation
at both unit and system levels are essential to mitigate risks, meet technical
and functional requirements, and ensure compliance with safety and ethical
standards before deployment.

## Model Version(s):

**MetricTrail 1.0:** The registered research model release. Integrate this version
by preparing RGB frame inventories and a JSON configuration, obtaining the
separately distributed MetricTrail checkpoint and compatible upstream weights
under their respective terms, and invoking
`python -m metrictrail.cli --config <config.json>`. The caller consumes validated
trajectory NPZ files, JSON completion records, and optional depth/mask caches,
and evaluates them for its intended research use.

**Checkpoint:** The multi-dataset-adapted DINO-DPVO checkpoint will be released
separately on Hugging Face. Place it at `ckpt/dino_dpvo_multidataset15k.pth`
or set `paths.dino_dpvo_checkpoint` to its local path. It is not included in the
source repository. **Source revision:**
`7ead0eca3f8a6a1266a21974c8077cc53940ccf5`.
Checkpoint SHA256:
`d0aa57e165b159fc84bdb9d94918ad9b508c153acfb4c46f5058ab80421fb5f5`.
The checkpoint records format version 1 and training phase `joint`.
The Python package version `0.1.0` is a separate software version.

The frozen DINOv3 backbone is excluded from the DINO-DPVO checkpoint and must be
obtained separately as `dinov3_vits16_pretrain_lvd1689m-08c60483.pth`.
Its validated SHA256 is
`08c60483bc63c04f533611e34bf70b120eedb7240f469bc16e9e20bf344b941d`.
MoGe-2 and optional calibration and RoMa dependencies are also separate
downloads.
Optional loop-retrieval tools are obtained and run independently to generate
the candidate files consumed by the loop-correction command.

The released configuration supports monocular/stereo tracking and optional
revisit focal refinement. Core configs disable loop closure. The separate
postprocessor uses externally supplied identity-edge candidates, with
VBR-specific residual scales and default scales for other datasets.
The new postprocessor has not been benchmark-validated.
Native DPVO loops and global BA are rejected by the configuration
schema. Focal refinement performs one coarse matching attempt, keeps the stage-A
focal if refused, and reruns tracking after an accepted correction. Other
global-BA/refinement variants evaluated below are not exposed by this CLI.

## Training, Testing, and Evaluation Datasets:

### Training Dataset:

#### Data Modality:

- Video
- Other: Camera-pose and induced patch-motion supervision

#### Training Data Size:

**Video Training Data Size:** Less than 10,000 hours of unique MetricTrail
fine-tuning video. This excludes repeated sampling
and the inherited pretraining of DPVO, DINOv3, MoGe-2, and optional components.

Training, including warmup, uses the following sampled clip exposures.
The table counts clip exposures; unique sequence and image counts and full
upstream dataset sizes are not shown. Each clip contains 15 frames.

| Dataset | Sampled clip exposures | Source content |
| --- | ---: | --- |
| TartanAir | 56,000 | Synthetic simulated environments |
| TartanGround | 46,000 | Synthetic ground-robot environments |
| CarlaOcc | 46,000 | Synthetic driving scenes |
| LightwheelOcc | 46,000 | Synthetic driving scenes |
| OmniWorld-Game | 46,000 | Game-scene video; only the Game subset |
| Total | 240,000 | Five project-specific training sources |

**Camera-Pose Supervision Data Size:** 240,000 clips with 15 camera poses per
clip, totaling 3,600,000 frame-level pose exposures.

**Induced Patch-Motion Supervision Data Size:** The same 240,000 clips, with
80 sampled source patches per frame (1,200 per clip), totaling 288,000,000
sampled patch exposures. Motion targets are derived from camera poses, depths,
and intrinsics.

These are sampled training exposures, including warmup and joint fine-tuning,
not unique annotations. Patch exposures count sampled source patches; valid
patch-to-frame motion targets and recurrent reuse are not counted separately.

**Data Collection Method by dataset:** Synthetic. Existing datasets: simulation
for TartanAir, TartanGround, CarlaOcc, and LightwheelOcc; game capture for
OmniWorld-Game.

**Labeling Method by dataset:** Synthetic. The local estimator uses the original DPVO
pose and induced patch-motion supervision. Simulation/game-derived geometry
and camera metadata supply the supervision. The per-source annotation manifests
have not been verified.

Images are resized with preserved aspect ratio and center-cropped to
480 x 640. No training clip exceeds 15 frames, and no evaluation sequence
or dedicated long-trajectory pose corpus is used. A fine-tuning validation
split, exact downloaded revisions, acquisition dates, unique example count,
and complete sample-level provenance are not documented.

The initialized DPVO checkpoint and frozen DINOv3 and MoGe-2 components
carry additional upstream pretraining history. DINOv3-S/16 was
pretrained on LVD-1689M. The five-source fine-tuning list does not describe
all data used to train these upstream components.

**Other Dataset Properties:** Fine-tuning uses synthetic simulation/game scenes,
RGB video, camera poses, and induced patch-motion supervision. Dataset content
and assets retain their providers' terms. The fine-tuning data contain no real
personal information and satisfy applicable privacy requirements and
dataset-review conditions. This applies to the five fine-tuning datasets;
the personal-data content of externally pretrained components is not specified.
A sample-level provenance inventory is not included.
Linguistic characteristics are Not Applicable to the geometric training task:
no text prompt, natural-language output, or language-specific evaluation is used.

### Testing Dataset:

We evaluate MetricTrail on the following existing captured benchmarks. Testing
and quantitative evaluation refer to these benchmark protocols; a separate
project-specific held-out test partition is not specified.

| Benchmark | Reported coverage and input | Task |
| --- | --- | --- |
| KITTI Odometry | Sequences 00-10, all frames; monocular or calibrated stereo | Long-sequence trajectories |
| Oxford Spires | Ten sequences, 38,380 frames, stride 1 | Trajectories and dense reconstruction |
| VBR | All seven sequences, stride 1; 8,815-18,846 frames per sequence, routes up to 5.20 km | Long-sequence trajectories |
| 7Scenes | Dense-reconstruction protocol; additional trajectory evaluation on 18 official test sequences at stride 5 | Indoor geometry and trajectories |
| TUM-Dynamic | Captured sequences with dynamic content; complete sequence/frame counts are not specified in the main protocol | Dense reconstruction |
| KITTI video depth | 13 videos, 1,269 frames | Frame-level depth |
| TUM RGB-D | All nine Freiburg1 sequences, 8,694 associated frames, stride 1 | Trajectories |
| LaMAria | Five full sequences: R_01, R_04, R_06, R_07, R_08; monocular grayscale, no dataset-specific fine-tuning | Out-of-domain trajectories |
| Wild-SLAM MoCap | All ten dynamic sequences, 9,039 associated RGB frames, stride 1 | Trajectories with dynamic content |

**Data Collection Method by dataset:** Automatic/Sensors. Existing captured
camera/sensor datasets.

**Labeling Method by dataset:** Hybrid: Automatic/Sensors, Automated.
Benchmark-provided reference trajectories,
geometry/depth, and calibration are used for comparison as applicable.

**Other Dataset Properties:** These are captured RGB or grayscale camera
sequences, with benchmark-specific depth, calibration, and reference trajectories.
The coverage and available frame counts are listed above.
Indoor, outdoor, driving, handheld, and dynamic scenes may
include identifiable people, private interiors, readable text, or locations.
Benchmark footage retains its providers' terms. Linguistic characteristics are
Not Applicable to the evaluated geometric tasks; incidental text in frames is
not a language input or a language-performance benchmark.

Additional in-the-wild reconstructions are qualitative examples and do not
constitute a quantified, representative deployment test set.

### Evaluation Dataset:

The results below use research evaluation workflows. The repository provides
prediction generation but does not include benchmark evaluation scripts.
Its shipped configuration does not expose the indoor global-BA/refinement
variants or dense export workflow used in these evaluations.

Trajectory accuracy is full-sequence absolute trajectory error (ATE), measured
as RMSE after a single proper Sim(3) alignment per sequence. Main long-sequence
results use meters; additional indoor/dynamic trajectory results use centimeters.
Dataset averages give sequence-level results equal weight in the reported
additional protocols. LC denotes the original SALAD/PyPose loop-closure workflow
used in our evaluations. These results do not establish numerical or benchmark
equivalence for the new external-candidate NumPy/SciPy postprocessor. 

| Benchmark / configuration | Average ATE |
| --- | ---: |
| KITTI Odometry, RGB-only calibration, without LC | 14.05 m |
| KITTI Odometry, RGB-only calibration, with LC | 9.78 m |
| KITTI Odometry, supplied intrinsics, with LC | 7.39 m |
| KITTI Odometry, calibrated stereo, with LC | 3.00 m |
| Oxford Spires, RGB-only calibration, without / with LC | 1.77 / 1.77 m |
| VBR, RGB-only calibration with revisit focal refinement, without / with LC | 16.36 / 10.88 m |
| 7Scenes, RGB-only calibration, local / with global BA | 6.7 / 6.3 cm |
| TUM RGB-D, RGB-only calibration, local / global BA / global BA plus refinement | 8.4 / 4.9 / 4.4 cm |
| TUM RGB-D, supplied intrinsics, local / global BA / global BA plus refinement | 7.5 / 4.1 / 3.7 cm |
| LaMAria, RGB-only calibration / supplied intrinsics | 8.73 / 8.58 m |
| Wild-SLAM MoCap, RGB-only calibration / supplied intrinsics | 2.70 / 1.65 cm |

VBR aggregate results include an optional **retrospective** revisit-based focal
refinement. Under matched settings, this improves base-calibration ATE from
33.51 to 16.36 m without LC and from 27.95 to 10.88 m with LC. Refinement
averages 7.1 minutes per routed sequence, dominated by RGB correspondence
matching. These results should not be described as end-to-end online results
at the KITTI steady-state throughput.

Dense reconstruction uses RGB-estimated intrinsics without LC. Results are
evaluated after sequence-level Sim(3) alignment followed by point-to-point ICP.
CD is symmetric Chamfer distance; F1 is measured at the indicated distance
threshold.

| Benchmark | CD (m, lower is better) | F1 (%, higher is better) | Threshold |
| --- | ---: | ---: | --- |
| 7Scenes | 0.04 | 97.60 | 0.25 m |
| TUM-Dynamic | 0.13 | 89.58 | 0.25 m |
| Oxford Spires | 0.98 | 95.12 | 4 m |

KITTI video-depth evaluation fits one multiplicative scale per video without
a shift. Abs Rel is **0.057** and delta-1 accuracy
(depth-ratio error below 1.25) is **97.8%**. Dense depth comes from the frozen
frame-level provider; it is not a densely optimized output of local BA.

**Data Collection Method by dataset:** Automatic/Sensors. The captured benchmarks
described under
[Testing Dataset](#testing-dataset).

**Labeling Method by dataset:** Hybrid: Automatic/Sensors, Automated.
Reference-trajectory, geometry, and depth
comparison under the alignment protocols above. Sim(3), ICP, and depth-scale
alignment measure agreement after alignment; these scores do not establish
unaligned metric-scale accuracy, calibrated uncertainty, demographic parity,
or safe downstream control.

**Other Dataset Properties:** Quantitative evaluation uses the same benchmark
coverage, data counts, modalities, scene content, and sensor-derived references
listed under [Testing Dataset](#testing-dataset). The separate tasks are
trajectory estimation, dense reconstruction, and frame-level depth, under the
alignment protocols above. Exact TUM-Dynamic counts and the dense-reconstruction
7Scenes frame inventory are not documented; the 18-sequence
7Scenes count refers to the additional trajectory protocol. No separate
evaluation dataset with language inputs is used, so linguistic characteristics
are Not Applicable. Captured footage may contain personal or identifying scene
information and retains its providers' terms.

### Inference:

**Acceleration Engine:** PyTorch/CUDA with DPVO CUDA extensions and xformers
attention for MoGe-2. The default configuration enables FP16 for MoGe-2 and a
depth-overlap queue of four. DINOv3 feature extraction uses BF16; the trained
checkpoint stores FP32 tensors. No TensorRT or Triton export is provided.

**Test Hardware:** NVIDIA Ampere A100. The inference GPU's memory capacity and a
minimum supported hardware configuration are not specified.

The following measurements use KITTI-02. Latency means
time to first output; throughput means steady-state processing; memory means
peak allocated GPU memory.

| Configuration | First-output latency | Steady-state throughput | Peak GPU memory |
| --- | ---: | ---: | ---: |
| Supplied intrinsics | Approximately 0.7 s | 12.70 FPS | 3.21 GB |
| RGB-only calibration | Approximately 175 s | 12.70 FPS | 6.81 GB |

RGB-only startup includes initial MoGe-2 camera prediction, geometric
calibration, and prefix replay. Memory subsequently drops to 3.21 GB.
These measurements are specific to the reported KITTI configuration and do
not include a general latency guarantee for optional retrospective refinement.

Known limitations include dependence on depth-provider accuracy, degraded
sparse correspondence under low parallax, rapid rotation, rolling shutter,
and motion blur, and sensitivity to the shared camera model. Dynamic-scene
reconstruction improvements are not uniform: the TUM-Dynamic scores trail
leading evaluated methods. MetricTrail uses no explicit
dynamic-object mask or dynamics-specific objective. Optional retrieved loop
edges assume near-duplicate views are approximately coincident without
pairwise geometric verification; incorrect matches can affect the trajectory.

## Ethical Considerations:

NVIDIA believes Trustworthy AI is a shared responsibility and we have established
policies and practices to enable development for a wide array of AI applications.
Developers should work with their internal model team to ensure this model meets
requirements for the relevant industry and use case and addresses unforeseen
product misuse.

Please make sure you have proper rights and permissions for all input image and
video content; if image or video includes people, personal health information,
or intellectual property, the image or video generated will not blur or maintain
proportions of image subjects included.

Please report model quality, risk, security vulnerabilities or NVIDIA AI Concerns
[here](https://www.nvidia.com/en-us/support/submit-security-vulnerability/).

