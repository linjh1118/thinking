---
license: openmdw-1.1
---

# Earth-2 Checkpoints: HealDA v2

## Description

HealDA v2 is a global machine-learning data-assimilation model that maps a
48-hour sequence of satellite and conventional observations to a 104-channel,
0.25° atmospheric analysis on a regular latitude–longitude grid. The analysis
can serve as an initial condition for off-the-shelf machine-learning weather
forecast models.

Unlike HealDA v1, which processes one analysis time independently, HealDA v2
uses causal video data assimilation across eight consecutive 6-hourly analysis
times. Each frame uses observations within ±3 hours of its analysis time, so
the complete sequence covers 48 hours from the earliest to the latest
observation time. Temporal attention allows later analyses to use information
from earlier frames without using future model states. The public inference API
returns only the final analysis frame.

This checkpoint predicts 104 atmospheric, ocean-surface, cloud, and land-surface
fields. It was trained with source-level NNJA satellite and conventional
observations, including microwave and infrared sounders, GNSS radio occultation,
satellite-derived winds, and in-situ observations.

For training recipes see [HealDA](https://github.com/NVlabs/HealDA), for inference see [NVIDIA Earth2Studio](https://github.com/NVIDIA/earth2studio).

This model is ready for commercial or non-commercial use.

### License/Terms of Use

**Governing Terms:** Use of this model is governed by the [Linux Foundation
OpenMDW License Agreement, version
1.1](https://github.com/OpenMDW/OpenMDW/blob/main/1.1/LICENSE.OpenMDW-1.1).
See the [LICENSE.OpenMDW-1.1.md](LICENSE.OpenMDW-1.1.md) file distributed with the model for the governing terms.

**Additional Information:** [Apache License, Version 2.0](https://www.apache.org/licenses/LICENSE-2.0).

### Deployment Geography

Global

## Use Case

Industry, academic, and government research teams interested in global data
assimilation, observing-system studies, and initialization of medium-range
machine-learning weather forecasts. Model analyses are statistical estimates
and should not be the sole basis for safety-critical decisions.

## Release Date

Hugging Face 10/01/2026 via [nvidia/healda-v2](https://huggingface.co/nvidia/healda-v2)

## Reference(s)

**Papers:**

- [HealDA: Highlighting the importance of initial errors in end-to-end AI
  weather forecasts](https://arxiv.org/abs/2601.17636)

**Code:**

- [PhysicsNeMo](https://github.com/NVIDIA/physicsnemo)
- [Earth2Studio](https://github.com/NVIDIA/earth2studio)

## Model Architecture

**Architecture Type:** Custom observation encoder + HEALPix Diffusion
Transformer (DiT) backbone + mesh-to-grid decoder, used as a deterministic
regression model. <br>

**Network Architecture:** Sensor-specific point-cloud embedders encode irregular
observations. Observation-to-pixel cross-attention places those features into an
internal HEALPix latent representation. A DiT backbone applies spatial
self-attention and causal temporal attention across eight analysis frames. A
GraphCast-style mesh-to-grid decoder maps the latent representation directly to
the native 0.25° regular latitude–longitude output grid. <br>

**This model was developed based on:** HealDA v1 and the Earth2Studio /
PhysicsNeMo HEALPix transformer stack. <br>

**Number of model parameters:** 917.42 million (~0.92 billion). <br>

## Input(s)

**Input Type(s):**

- Tensor (satellite and conventional observations represented as point-cloud data)
- Tensor (eight ERA5-derived static conditioning channels and geographic features)
- Tensor (day of year)
- Tensor (second of day)

**Input Format(s):** PyTorch tensors <br>

**Input Parameters:**

- Observations: variable-length point clouds organized into eight 6-hourly frames
- Static conditioning: eight global 0.25° ERA5-derived channels on a
  `721 × 1440` latitude–longitude grid and their internal HEALPix representation
- Day of year: two-dimensional tensor `(batch, time)`
- Second of day: two-dimensional tensor `(batch, time)`
- Sequence length: eight analysis frames

**Other Properties Related to Input:**

- Observation context: ±3 hours around each frame. Eight frames separated by six
  hours provide a 48-hour span from the earliest to latest observation time.
- Microwave sounders: ATMS, AMSU-A, AMSU-B, and MHS.
- Infrared sounders: AIRS, IASI, and CrIS.
- Conventional observations: surface stations, aircraft, radiosondes, and buoys,
  including pressure, temperature, humidity, and wind measurements.
- GNSS radio occultation: bending-angle observations.
- Satellite-derived winds: atmospheric motion vectors and ASCAT scatterometer winds.
- Time-invariant conditioning uses eight channels from ERA5 invariant datasets:
  orography (`orog`), land-sea mask (`lsm`), standard deviation of subgrid
  orography (`sdor`), subgrid-orography slope (`slor`), subgrid-orography
  anisotropy (`isor`), standard deviation of filtered subgrid orography (`sdfor`),
  and the sine and cosine of subgrid-orography orientation (`anor_sin`,
  `anor_cos`). Time-varying conditioning includes calendar and solar-zenith
  features.

## Output(s)

**Output Type(s):** Tensor (104-channel global atmospheric, ocean-surface,
cloud, and land-surface analysis) <br>

**Output Format(s):** PyTorch tensor <br>

**Output Parameters:** The public inference API returns the final analysis on a
`721 × 1440` latitude–longitude grid. The tensor has shape equivalent to
`(batch, 104, latitude=721, longitude=1440)`; interfaces that retain a time
dimension expose it with length one. <br>

**Other Properties Related to Output:**

- Output grid: global regular latitude–longitude grid at 0.25° resolution,
  represented by 721 latitude points and 1,440 longitude points.
- Pressure levels: 1000, 925, 850, 700, 600, 500, 400, 300, 250, 200, 150, 100,
  and 50 hPa.
- Three-dimensional fields on all 13 pressure levels: zonal wind (`U`), meridional
  wind (`V`), temperature (`T`), geopotential (`Z`), specific humidity (`Q`), and
  vertical velocity (`W`).
- Additional 10 hPa fields: `U`, `V`, `T`, and `Z`. The checkpoint does not predict
  `Q` or `W` at 10 hPa.
- Surface and column fields: total-column water vapour (`tcwv`), 2 m temperature
  (`tas`), 10 m wind (`uas`, `vas`), 100 m wind (`100u`, `100v`), mean sea-level
  pressure (`pres_msl`), sea-surface temperature (`sst`), sea-ice concentration
  (`sic`), surface pressure (`sp`), 2 m dewpoint (`d2m`), skin temperature (`skt`),
  and total-column water (`tcw`).
- Cloud fields: total, low, medium, and high cloud cover (`tcc`, `lcc`, `mcc`,
  `hcc`).
- Land fields: soil temperature in layers 1 and 2 (`stl1`, `stl2`), volumetric soil
  water in layers 1 and 2 (`swvl1`, `swvl2`), and snow depth (`sd`).

Our AI models are designed and/or optimized to run on NVIDIA GPU-accelerated
systems. By leveraging NVIDIA hardware and CUDA software libraries, the model
achieves faster training and inference than CPU-only execution.

## Software Integration

**Runtime Engine(s):** PyTorch / PhysicsNeMo <br>

**Supported Hardware Microarchitecture Compatibility:**

- NVIDIA Ampere
- NVIDIA Blackwell
- NVIDIA Hopper

**Supported Operating System(s):**

- Linux

The integration of foundation and fine-tuned models into AI systems requires
additional testing using use-case-specific data to ensure safe and effective
deployment. Following the V-model methodology, iterative testing and validation
at both unit and system levels are essential to mitigate risks, meet technical
and functional requirements, and ensure compliance with safety and ethical
standards before deployment.

## Model Version(s)

**Model version:** HealDA v2, 104-channel, 0.25° checkpoint. <br>

# Training, Testing, and Evaluation Datasets

## Training Dataset

**Data Modality:**

- Other: numerical geophysical point observations and gridded reanalysis fields

**Training Data Size:**

- 35,068 nominal six-hourly ERA5 target times across 2000–2021 and 2023–2024,
  before availability filtering, paired with a variable number of NNJA point
  observations

**Link:** [ERA5](https://cds.climate.copernicus.eu/) <br>

**Data Collection Method by dataset:**

- Automatic/Sensors (observations combined with numerical-model reanalysis)

**Labeling Method by dataset:**

- Automatic/Sensors

**Properties:**

Six-hourly ERA5 reanalysis fields on the native 0.25° regular
latitude–longitude grid are used as supervised targets. Training uses 2000–2021
and 2023–2024. Calendar year 2022 is held out for validation, and 2025 onward is
reserved for out-of-sample testing. <br>

ERA5 supplies all gridded atmospheric targets and all static conditioning
fields. NNJA observations are used only as observation inputs to the data-assimilation
model. <br>

Per-channel normalization is computed for the 0.25° grid. Area-weighted loss
and metrics account for the unequal cell areas of a regular latitude–longitude
grid. Domain masks prevent fields such as sea-surface temperature, sea-ice
concentration, and soil moisture from being scored outside their valid physical
domains. <br>

**License:** [Creative Commons Attribution 4.0 International (CC BY
4.0)](https://creativecommons.org/licenses/by/4.0/). <br>

**Attribution:** Modified from ECMWF Reanalysis data (ERA5), © European Centre
for Medium-Range Weather Forecasts (ECMWF), distributed through the NSF NCAR
ERA5 mirror. <br>

**Source:** [NOAA–NASA Joint Archive (NNJA) of Observations for Earth System
Reanalysis](https://www.psl.noaa.gov/data/nnja_obs/), distributed through the
public `s3://noaa-reanalyses-pds/observations/reanalysis/` archive. <br>

**License:** [Creative Commons Attribution 4.0 International (CC BY
4.0)](https://creativecommons.org/licenses/by/4.0/). <br>

**Attribution:** NOAA NASA Joint Archive (NNJA),
https://www.psl.noaa.gov/data/nnja_obs/. <br>

**Additional acknowledgement for NNJA `amv/merged`:** EUMETSAT (2021),
*Atmospheric Motion Vectors Climate Data Record Release 2 — MFG and MSG — 0
degree*, European Organisation for the Exploitation of Meteorological
Satellites, [doi:10.15770/EUM_SEC_CLM_0020](https://doi.org/10.15770/EUM_SEC_CLM_0020). <br>

**Data Collection Method by dataset:**

- Automatic/Sensors

**Labeling Method by dataset:**

- Automatic/Sensors

**Properties:**

Satellite observations include microwave and infrared sounders. Conventional
observations include PrepBUFR surface, aircraft, radiosonde, and buoy reports,
GNSS radio occultation, and dedicated satellite-wind products. The observing
system changes over time as instruments enter and leave service. Observation
inputs follow the same training, validation, and out-of-sample test periods as
the corresponding ERA5 targets. NNJA is an experimental research dataset under
active development, and archived content may change as quality-control updates
are applied. <br>

### Data Processing Description

ERA5 fields are sampled at six-hour intervals on the native 0.25° grid.
Observations are quality controlled, normalized by channel (and by pressure
level for conventional observations), spatially thinned, and encoded as
irregular point clouds. Each training example contains eight sequential analysis
frames with causal temporal attention.

## Testing Dataset

**Links:** [ERA5](https://cds.climate.copernicus.eu/) and the corresponding
held-out [NNJA observations](https://www.psl.noaa.gov/data/nnja_obs/). <br>

**Data Collection Method by dataset:**

- Automatic/Sensors

**Labeling Method by dataset:**

- Automatic/Sensors

**Properties:**

Data from 2025 onward is reserved for out-of-sample testing and is not used for
optimization or model selection. Test coverage extends through the latest
available matched ERA5 and NNJA observations. <br>

## Evaluation Dataset

**Links:** [ERA5](https://cds.climate.copernicus.eu/) and the corresponding
held-out [NNJA observations](https://www.psl.noaa.gov/data/nnja_obs/). <br>

**Benchmark Score:** Not reported. <br>

**Data Collection Method by dataset:**

- Automatic/Sensors

**Labeling Method by dataset:**

- Automatic/Sensors

**Properties:**

Validation uses calendar year 2022. Analysis error is evaluated against ERA5 on
the native 0.25° grid using latitude-area weighting. Downstream forecast
comparisons use matched forecast models, initialization dates, grids, regridding
methods, and verification targets. <br>

## Inference

**Acceleration Engine:** PyTorch / PhysicsNeMo <br>

**Test Hardware:**

- NVIDIA Hopper (H100)
- NVIDIA Blackwell (B300 / GB300)

## Ethical Considerations

NVIDIA believes Trustworthy AI is a shared responsibility and we have
established policies and practices to enable development for a wide array of AI
applications. Developers should work with their internal model team to ensure
this model meets requirements for the relevant industry and use case and
addresses unforeseen product misuse.

For more detailed information on ethical considerations for this model, please
see the Model Card++ [Bias](model_card/bias.md), [Explainability](model_card/explainability.md),
[Safety & Security](model_card/safety.md), and [Privacy](model_card/privacy.md) Subcards.

Please report model quality, risk, security vulnerabilities, or NVIDIA AI
Concerns [here](https://www.nvidia.com/en-us/support/submit-security-vulnerability/).

