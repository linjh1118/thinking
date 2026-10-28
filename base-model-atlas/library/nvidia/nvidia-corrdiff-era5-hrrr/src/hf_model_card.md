---
license: openmdw-1.1
---
# Model Overview

## Description:

corrdiff-era5-hrrr is a high-resolution generative downscaling (super-resolution) model. It predicts 99 state variables at km scale over the Continental United States (CONUS) from coarse global ERA5 reanalysis, with dense vertical resolution in the atmospheric boundary layer. It shares the state variables, conditioning variables, HRRR grid, and Diffusion Transformer (DiT) backbone with neighborhood attention (NATTEN) of StormCast-CONUS. corrdiff-era5-hrrr super-resolves ERA5 onto the HRRR grid at the same timestep, and trains with rectified flow matching. Repeated sampling from the same ERA5 input produces an ensemble of km-scale states consistent with the coarse input.

For training recipes see [NVIDIA PhysicsNeMo](https://github.com/NVIDIA/physicsnemo), for inference see [NVIDIA Earth2Studio](https://github.com/NVIDIA/earth2studio).

This model is ready for commercial or non-commercial use.

### License/Terms of Use:

**Governing Terms**: Use of this model is governed by the [Linux Foundation OpenMDW License Agreement, version 1.1](https://github.com/OpenMDW/OpenMDW/blob/main/1.1/LICENSE.OpenMDW-1.1).

### Deployment Geography:

Global

### Use Case:

Km-scale downscaling of global reanalysis and ensemble generation over CONUS, for renewable-energy resource assessment, climate and catastrophe-risk research, hydrology, and atmospheric science

### Release Date:

Hugging Face 09/28/2026 via [https://huggingface.co/nvidia/corrdiff-era5-hrrr](https://huggingface.co/nvidia/corrdiff-era5-hrrr)

## Reference(s):

- CorrDiff: [Residual Diffusion Modeling for Km-scale Atmospheric Downscaling](https://arxiv.org/abs/2309.15214) <br>
- StormCast v1: [Kilometer-Scale Convection Allowing Model Emulation using Generative Diffusion Modeling](https://arxiv.org/abs/2408.10958) <br>

## Model Architecture:

**Architecture Type:** corrdiff-era5-hrrr uses a Diffusion Transformer (DiT) architecture with neighborhood attention (NATTEN), 678M parameters. <br>
**Network Architecture:** Diffusion Transformer (DiT) with Neighborhood Attention (NATTEN) <br>
**This model was developed based on:** Not Applicable. The model was trained from scratch on paired ERA5/HRRR data; no pre-trained base model was used. <br>
**Number of model parameters:** 6.8 × 10<sup>8</sup> <br>

## Input:

**Input Type(s):**

- Tensor (125 Surface and Model level variables - 99 state variables and 26 conditioning variables.)
- DateTime (NumPy Array) <br>

**Input Format(s):** PyTorch Tensor / NumPy array <br>
**Input Parameters:**

- Four Dimensional (4D) (batch, variable, latitude, longitude) <br>
- Input DateTime (1D) <br>

**Other Properties Related to Input:**

- Input latitude/longitude grid: HRRR Lambert Conformal Conic projection, 3 km resolution, 1024×1792 grid
- Input state weather variables: `u10m`, `v10m`, `t2m`, `mslp`, `u_hl1`, `u_hl2`, `u_hl3`, `u_hl4`, `u_hl5`, `u_hl6`, `u_hl7`, `u_hl8`, `u_hl9`, `u_hl10`, `u_hl11`, `u_hl13`, `u_hl15`, `u_hl20`, `u_hl25`, `u_hl30`, `v_hl1`, `v_hl2`, `v_hl3`, `v_hl4`, `v_hl5`, `v_hl6`, `v_hl7`, `v_hl8`, `v_hl9`, `v_hl10`, `v_hl11`, `v_hl13`, `v_hl15`, `v_hl20`, `v_hl25`, `v_hl30`, `t_hl1`, `t_hl2`, `t_hl3`, `t_hl4`, `t_hl5`, `t_hl6`, `t_hl7`, `t_hl8`, `t_hl9`, `t_hl10`, `t_hl11`, `t_hl13`, `t_hl15`, `t_hl20`, `t_hl25`, `t_hl30`, `q_hl1`, `q_hl2`, `q_hl3`, `q_hl4`, `q_hl5`, `q_hl6`, `q_hl7`, `q_hl8`, `q_hl9`, `q_hl10`, `q_hl11`, `q_hl13`, `q_hl15`, `q_hl20`, `q_hl25`, `q_hl30`, `z_hl1`, `z_hl2`, `z_hl3`, `z_hl4`, `z_hl5`, `z_hl6`, `z_hl7`, `z_hl8`, `z_hl9`, `z_hl10`, `z_hl11`, `z_hl13`, `z_hl15`, `z_hl20`, `z_hl25`, `z_hl30`, `p_hl1`, `p_hl2`, `p_hl3`, `p_hl4`, `p_hl5`, `p_hl6`, `p_hl7`, `p_hl8`, `p_hl9`, `p_hl10`, `p_hl11`, `p_hl13`, `p_hl15`, `p_hl20`, `refc`  <br>
- Conditioning weather variables: `u10m`, `v10m`, `t2m`, `tcwv`, `mslp`, `sp`, `u1000`, `u850`, `u500`, `u250`, `v1000`, `v850`, `v500`, `v250`, `z1000`, `z850`, `z500`, `z250`, `t1000`, `t850`, `t500`, `t250`, `q1000`, `q850`, `q500`, `q250`
- Cosine of solar zenith angle (computed)
- Constant inputs: mean and standard deviation of surface elevation in pixel; land/water mask

For variable naming information, review the `HRRR` Lexicon at [Earth2Studio](https://github.com/NVIDIA/earth2studio/blob/main/earth2studio/lexicon/hrrr.py), but `u`, `v`, `t`, `z` and `p` refer to winds, temperature, geopotential, and pressure (respectively). Variables marked with `_hl` refer to natural/hybrid model levels.

## Output:

**Output Type(s):** Tensor (99 Surface and Model level variables) <br>
**Output Format:** PyTorch Tensors <br>
**Output Parameters:** Four Dimensional (4D) (batch, variable, latitude, longitude) <br>
**Other Properties Related to Output:**

- Output latitude/longitude grid: HRRR Lambert Conformal Conic projection, 3 km resolution, 1024×1792 grid
- Output state weather variables: `u10m`, `v10m`, `t2m`, `mslp`, `u_hl1`, `u_hl2`, `u_hl3`, `u_hl4`, `u_hl5`, `u_hl6`, `u_hl7`, `u_hl8`, `u_hl9`, `u_hl10`, `u_hl11`, `u_hl13`, `u_hl15`, `u_hl20`, `u_hl25`, `u_hl30`, `v_hl1`, `v_hl2`, `v_hl3`, `v_hl4`, `v_hl5`, `v_hl6`, `v_hl7`, `v_hl8`, `v_hl9`, `v_hl10`, `v_hl11`, `v_hl13`, `v_hl15`, `v_hl20`, `v_hl25`, `v_hl30`, `t_hl1`, `t_hl2`, `t_hl3`, `t_hl4`, `t_hl5`, `t_hl6`, `t_hl7`, `t_hl8`, `t_hl9`, `t_hl10`, `t_hl11`, `t_hl13`, `t_hl15`, `t_hl20`, `t_hl25`, `t_hl30`, `q_hl1`, `q_hl2`, `q_hl3`, `q_hl4`, `q_hl5`, `q_hl6`, `q_hl7`, `q_hl8`, `q_hl9`, `q_hl10`, `q_hl11`, `q_hl13`, `q_hl15`, `q_hl20`, `q_hl25`, `q_hl30`, `z_hl1`, `z_hl2`, `z_hl3`, `z_hl4`, `z_hl5`, `z_hl6`, `z_hl7`, `z_hl8`, `z_hl9`, `z_hl10`, `z_hl11`, `z_hl13`, `z_hl15`, `z_hl20`, `z_hl25`, `z_hl30`, `p_hl1`, `p_hl2`, `p_hl3`, `p_hl4`, `p_hl5`, `p_hl6`, `p_hl7`, `p_hl8`, `p_hl9`, `p_hl10`, `p_hl11`, `p_hl13`, `p_hl15`, `p_hl20`, `refc`  <br>

Our AI models are designed and/or optimized to run on NVIDIA GPU-accelerated systems. By leveraging NVIDIA’s hardware (e.g. GPU cores) and software frameworks (e.g., CUDA libraries), the model achieves faster training and inference times compared to CPU-only solutions.

## Software Integration

**Runtime Engine(s):** Not Applicable <br>
**Supported Hardware Microarchitecture Compatibility:** <br>
* NVIDIA Ampere <br>
* NVIDIA Blackwell <br>
* NVIDIA Hopper <br>

**Supported Operating System(s):**
* Linux <br>

The integration of foundation and fine-tuned models into AI systems requires additional testing using use-case-specific data to ensure safe and effective deployment. Following the V-model methodology, iterative testing and validation at both unit and system levels are essential to mitigate risks, meet technical and functional requirements, and ensure compliance with safety and ethical standards before deployment.

## Model Version(s):

**Model Version:** v0 <br>

# Training, Testing, and Evaluation Datasets:

## Training Dataset:

**Link:** [ERA5](https://cds.climate.copernicus.eu/) <br>

*Data Collection Method by dataset:* <br>
* Automatic/Sensors <br>

*Labeling Method by dataset:* <br>
* Automatic/Sensors <br>

*Data Modality:*
* Gridded geophysical time series

*Data Size:*
* 150 GB subset used for model training

**Properties:**
ERA5 data for the period 2018-07-12 – 2025-09-30. ERA5 provides hourly estimates of various
atmospheric, land, and oceanic climate variables. The data covers the Earth on a 30km
grid and resolves the atmosphere at 137 levels. <br>

**Link:** [HRRR](https://rapidrefresh.noaa.gov/hrrr/) <br>

*Data Collection Method by dataset:* <br>
* Automatic/Sensors <br>

*Labeling Method by dataset:* <br>
* Automatic/Sensors <br>

*Data Modality:*
* Gridded geophysical time series

*Data Size:*
* 15 TB subset used for model training

**Properties:**
HRRR data for the date range of 2018-07-12 to 2025-09-30. The HRRR is a NOAA real-time 3-km resolution, hourly updated, cloud-resolving, convection-allowing atmospheric model, initialized by 3 km grids with 3 km radar assimilation. <br>

**Link:** [ASTER GDEM/ASTWBD](https://asterweb.jpl.nasa.gov/gdem.asp) <br>

*Data Collection Method by dataset:* <br>
* Automatic/Sensors <br>

*Labeling Method by dataset:* <br>
* Automatic/Sensors <br>

*Data Modality:*
* Gridded geophysical static data

*Data Size:*
* 120 MB upsampled subset used for model training

**Properties:**
Global digital elevation model (DEM) and water body map. Native resolution ~30 m/pixel, upsampled to HRRR grid. <br>

## Testing/Evaluation Dataset:

**Link:** [ERA5](https://cds.climate.copernicus.eu/) <br>

*Data Collection Method by dataset:* <br>
* Automatic/Sensors <br>

*Labeling Method by dataset:* <br>
* Automatic/Sensors <br>

**Properties:**
ERA5 data for the date range of 2025-10-01 - 2025-12-31. ERA5 provides hourly estimates of various
atmospheric, land, and oceanic climate variables. The data covers the Earth on a 30km
grid and resolves the atmosphere at 137 levels. <br>

**Link:** [HRRR](https://rapidrefresh.noaa.gov/hrrr/) <br>

*Data Collection Method by dataset:* <br>
* Automatic/Sensors <br>

*Labeling Method by dataset:* <br>
* Automatic/Sensors <br>

**Properties:**
HRRR data for the date range of 2025-10-01 - 2025-12-31. The HRRR is a NOAA real-time 3-km resolution, hourly updated, cloud-resolving, convection-allowing atmospheric model, initialized by 3 km grids with 3 km radar assimilation. <br>

**Link:** [ASTER GDEM/ASTWBD](https://asterweb.jpl.nasa.gov/gdem.asp) <br>

*Data Collection Method by dataset:* <br>
* Automatic/Sensors <br>

*Labeling Method by dataset:* <br>
* Automatic/Sensors <br>

**Properties:**
Global digital elevation model (DEM) and water body map. Native resolution ~30 m/pixel, upsampled to HRRR grid. <br>

## Inference:

**Acceleration Engine:** [PyTorch](https://pytorch.org/) / [Earth2Studio](https://github.com/NVIDIA/earth2studio) <br>
**Test Hardware:**
* NVIDIA Hopper (H100 80 GB) <br>


## Ethical Considerations:

NVIDIA believes Trustworthy AI is a shared responsibility and we have established policies and practices to enable development for a wide array of AI applications. Developers should work with their internal model team to ensure this model meets requirements for the relevant industry and use case and addresses unforeseen product misuse.

For more detailed information on ethical considerations for this model, please see the Model Card++ [Explainability](https://huggingface.co/nvidia/corrdiff-era5-hrrr/blob/main/explainability.md), [Bias](https://huggingface.co/nvidia/corrdiff-era5-hrrr/blob/main/bias.md), [Safety & Security](https://huggingface.co/nvidia/corrdiff-era5-hrrr/blob/main/safety.md), and [Privacy](https://huggingface.co/nvidia/corrdiff-era5-hrrr/blob/main/privacy.md) Subcards.

Please report model quality, risk, security vulnerabilities or NVIDIA AI Concerns through the [NVIDIA security vulnerability submission form](https://www.nvidia.com/en-us/support/submit-security-vulnerability/).
