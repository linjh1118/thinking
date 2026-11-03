---
license: openmdw-1.1
---
# Earth-2 Checkpoints: STRATA

## Description:

STRATA (Storm-resolving Tile-based autoRegressive Atmosphere Transformer Architecture) is a global, kilometer-scale AI atmosphere model that emulates the SCREAM (Simple Cloud-Resolving E3SM Atmosphere Model) global storm-resolving simulation. It autoregressively predicts the three-dimensional atmospheric state on SCREAM's native ne1024pg2 cubed-sphere grid (6 faces × 2048 × 2048 ≈ 25.2 million columns, ~4.9 km grid spacing) with a 10-minute time step. The prognostic state consists of potential temperature, zonal and meridional wind, geopotential height, vertical pressure velocity and specific humidity on 24 model levels, plus 2-m air temperature; surface pressure and liquid/ice surface precipitation fluxes are diagnosed at every step.

Inference is tile based: the global state is processed as overlapping cubed-sphere tiles (128–256 pixels with halos), so a single GPU can advance any part of the globe and a multi-GPU domain decomposition advances the full globe. Training recipes and the inference wrapper are in the public [NVlabs/STRATA](https://github.com/NVlabs/STRATA) repository (Apache-2.0); the network architecture itself lives in [NVIDIA PhysicsNeMo](https://github.com/NVIDIA/physicsnemo) as `physicsnemo.experimental.models.strata`.

This model is ready for commercial or non-commercial use.

### License/Terms of Use:

**Governing Terms**: Use of this model is governed by the [Linux Foundation OpenMDW License Agreement, version 1.1](https://github.com/OpenMDW/OpenMDW/blob/main/1.1/LICENSE.OpenMDW-1.1).
See the `LICENSE` file for the governing terms. The files `phis.npy`, `sgh30.npy` and `landfrac.npy` are derived from the CC BY 4.0 licensed STRATA-SCREAM datasets, with attribution obligations listed in `ATTRIBUTION.md`.

### Deployment Geography:

Global

### Use Case:

Kilometer-scale global atmosphere emulation for weather and climate research: short-range (hours to days) forecasting of the SCREAM state, emulation of storm-resolving simulations, and research on coupling AI emulators of different resolutions (e.g. large-scale nudging / downscaling experiments).

### Release Date:

Hugging Face: 11/02/2026 (planned) via [https://huggingface.co/nvidia/strata](https://huggingface.co/nvidia/strata)

## Reference(s):

- [Hu, Z., et al. (2026), Scaling Storm-Resolving Atmospheric AI Simulation to the Entire Planet, arXiv:2606.31248](https://arxiv.org/abs/2606.31248)
- SCREAM: Caldwell et al. (2021), [Convection-Permitting Simulations With the E3SM Global Atmosphere Model](https://doi.org/10.1029/2021MS002544)

## Model Architecture:

**Architecture Type:** Two-stage transformer ("PixelDiT"): a semantic transformer backbone operating on 4×4-pixel patches (24 blocks, width 1024, 16 heads, 3-D neighborhood attention with kernel 9 and dilation 3, gated attention, alternating depth-wise attention, stereographic 2-D rotary position embeddings, latitude/longitude index conditioning, wind-vector rotation across cube faces) followed by a pixel-resolution refinement transformer (4 blocks, width 128, kernel 9, bilinear depth-wise GELU projection with adaptive layer norm). The model is a deterministic single-step predictor trained with a regression (smooth-L1) loss on a mixed state/tendency target; no diffusion sampling is involved. 331.7 M parameters. <br>
**Network Architecture:** Transformer with Neighborhood Attention (NATTEN) <br>

This model provides the following checkpoint:

- `checkpoints/strata_v1.pth` -- ne1024pg2 grid, 10-minute time step, 331.7 M parameters (pretraining followed by a 4-step autoregressive fine-tune)

## Input:

**Input Type(s):**

- Tensor (149 channels: 145 prognostic atmospheric state channels and 4 forcing channels) <br>

**Input Format(s):** PyTorch tensors <br>

**Input Parameters:**

- Four Dimensional (4D): (batch, channel, tile height, tile width) per cubed-sphere tile; the tiled inference wrapper accepts the global state as (batch, channel, 6 faces, 2048, 2048) <br>

**Other Properties Related to Input:**

- Grid: SCREAM ne1024pg2 cubed-sphere physics grid (6 × 2048 × 2048 columns).
- Prognostic 3-D variables on 24 SCREAM hybrid model levels (archived level indices 8–31; nominal pressures ≈100, 117, 136, 158, 184, 214, 250, 290, 338, 394, 459, 534, 614, 690, 758, 814, 854, 880, 904, 927, 948, 967, 983 and 998 hPa for a 1000 hPa surface): `PotentialTemperature`, `U`, `V`, `z_mid`, `omega`, `qv`.
- Prognostic 2-D variable: `T_2m`.
- Forcing channels: `coszr` (cosine of the solar zenith angle, computed from the valid time of the atmospheric state before the tensor is assembled), `phis` (surface geopotential), `sgh30` (sub-grid orography standard deviation), `landfrac` (land fraction). The three static fields are distributed with the model as `phis.npy`, `sgh30.npy` and `landfrac.npy`.
- Inputs are normalized per channel with statistics stored in the checkpoint (also exported as `input_norm_mean.npy` / `input_norm_var.npy`; channel order in `channels.json`).

## Output:

**Output Type(s):** Tensor (148 channels: the 145 prognostic state channels at t + 10 min and 3 diagnostic channels) <br>
**Output Format:** PyTorch Tensors <br>
**Output Parameters:** Four Dimensional (4D) (batch, channel, tile height, tile width) <br>
**Other Properties Related to Output:**

- Diagnostic channels: `ps` (surface pressure), `precip_liq_surf_mass_flux`, `precip_ice_surf_mass_flux` (surface precipitation mass fluxes, m/s)
- Output lead time is one 10-minute step; longer forecasts are produced autoregressively by the wrapper.

Our AI models are designed and/or optimized to run on NVIDIA GPU-accelerated systems. By leveraging NVIDIA's hardware (e.g. GPU cores) and software frameworks (e.g., CUDA libraries), the model achieves faster training and inference times compared to CPU-only solutions.

## Software Integration:

**Runtime Engine(s):** PyTorch, NVIDIA PhysicsNeMo (with NATTEN neighborhood attention) <br>
**Supported Hardware Microarchitecture Compatibility:** <br>
* NVIDIA Ampere <br>
* NVIDIA Hopper <br>
* NVIDIA Blackwell <br>

**Supported Operating System(s):**
* Linux <br>

The integration of foundation and fine-tuned models into AI systems requires additional testing using use-case-specific data to ensure safe and effective deployment. Following the V-model methodology, iterative testing and validation at both unit and system levels are essential to mitigate risks, meet technical and functional requirements, and ensure compliance with safety and ethical standards before deployment.

## Model Version(s):

**Model Version:** v1 (`strata_v1`) <br>

# Training, Testing, and Evaluation Datasets:

## Training Dataset:

**Link:** [STRATA-SCREAM-sdecadal](https://huggingface.co/datasets/nvidia/STRATA-SCREAM-sdecadal), [STRATA-SCREAM-sdy1](https://huggingface.co/datasets/nvidia/STRATA-SCREAM-sdy1), [STRATA-SCREAM-sdy2](https://huggingface.co/datasets/nvidia/STRATA-SCREAM-sdy2) <br>

*Data Collection Method by dataset:* <br>
* Automated (numerical simulation output) <br>

*Labeling Method by dataset:* <br>
* Not Applicable (self-supervised next-step prediction; no human labels) <br>

*Data Modality:*
* Gridded geophysical time series

*Data Size:*
* ~76 TB total (sdecadal 36.8 TB, sdy1 19.6 TB, sdy2 19.7 TB); the training periods below are subsets of each store

**Properties:**
Output of three SCREAM v1 global storm-resolving simulations on the ne1024pg2 grid (~4.9 km physics grid), archived every 10 minutes on 32 model levels and published as cubed-sphere zarr stores: a 14-day segment of a transient historical (F20TR) simulation (sdecadal, 1994-10-01 to 1994-10-14) and two 7-day present-day (F2010) simulations for the DYAMOND periods (sdy1: 2016-08-01 to 2016-08-07; sdy2: 2020-01-20 to 2020-01-26). Training uses 17 simulated days: 1994-10-02 to 1994-10-10 of sdecadal, 2016-08-02 to 2016-08-05 of sdy1 and 2020-01-21 to 2020-01-24 of sdy2 (the first simulated day of every store is excluded; the remaining days of sdecadal are held out for testing and evaluation). The published sdecadal zarr store and the model code label the sdecadal dates as October 2020. The datasets are released under CC-BY-4.0. <br>

## Testing Dataset:

**Link:** same simulations as above (held-out later time periods of each simulation) <br>

*Data Collection Method by dataset:* <br>
* Automated (numerical simulation output) <br>

*Labeling Method by dataset:* <br>
* Not Applicable <br>

**Properties:**
Held-out portion of the sdecadal simulation after the training period (simulated days 11–14; validation samples every 6 hours on day 14), never seen during training (dates labelled October 2020 in the store). <br>

## Evaluation Dataset:

**Link:** same simulations as above <br>

*Data Collection Method by dataset:* <br>
* Automated (numerical simulation output) <br>

*Labeling Method by dataset:* <br>
* Not Applicable <br>

**Properties:**
Multi-day autoregressive rollouts initialized from six held-out sdecadal states at 12-hourly intervals (2020-10-11 12:00 to 2020-10-14 00:00 UTC in the store's date labelling) are scored against the SCREAM trajectory: area-weighted RMSE and bias per variable and level, radially averaged power spectra, and precipitation statistics; see the paper for results. <br>

## Inference:

**Engine:** PyTorch, PhysicsNeMo <br>
**Test Hardware:**
* H100 <br>
* A100 <br>

### Files in this repository

| file | content |
|---|---|
| `checkpoints/strata_v1.pth` | network weights (fp32), input/target normalization statistics, model/training configuration |
| `channels.json` | variable and level lists, grid and tile size |
| `input_norm_mean.npy`, `input_norm_var.npy`, `target_norm_mean.npy`, `target_norm_var.npy` | per-channel normalization statistics (also inside the checkpoint) |
| `phis.npy`, `sgh30.npy`, `landfrac.npy` | static forcing fields (float32, in the model's ne1024pg2 column order) |
| `third_party/CC-BY-4.0.txt` | license text of the CC BY 4.0 licensed SCREAM-derived files (see `ATTRIBUTION.md`) |
| `MANIFEST.md` | file sizes and SHA-256 checksums |

### Contributions

This repository distributes model weights and auxiliary files only and does not accept contributions (see `CONTRIBUTING.md`). Please report issues and propose changes to the code in the [NVlabs/STRATA](https://github.com/NVlabs/STRATA) repository.

### Minimal usage

```python
import os
os.environ["AUX_DATA_ROOT"] = "/path/to/this/repo"   # auxiliary files are resolved here
from screamcast.earth2studio_wrappers import ScreamcastModel   # pip install from https://github.com/NVlabs/STRATA
model = ScreamcastModel.from_checkpoint("/path/to/this/repo/checkpoints/strata_v1.pth")
```

## Ethical Considerations:

NVIDIA believes Trustworthy AI is a shared responsibility and we have established policies and practices to enable development for a wide array of AI applications. Developers should work with their internal model team to ensure this model meets requirements for the relevant industry and use case and addresses unforeseen product misuse.

For more detailed information on ethical considerations for this model, please see the Model Card++ [Bias](model_cards/bias.md), [Explainability](model_cards/explainability.md), [Safety & Security](model_cards/safety.md), and [Privacy](model_cards/privacy.md) subcards.

Please report model quality, risk, security vulnerabilities or NVIDIA AI Concerns on the [NVIDIA security vulnerability submission page](https://www.nvidia.com/en-us/support/submit-security-vulnerability/).
