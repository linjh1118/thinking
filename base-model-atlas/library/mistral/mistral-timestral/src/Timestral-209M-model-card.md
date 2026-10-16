---
pipeline_tag: time-series-forecasting
library_name: timestral
tags:
- time-series
- forecasting
- foundation-model
model-index:
- name: Timestral-209M
  results:
  - task:
      type: time-series-forecasting
      name: Time Series Forecasting
    dataset:
      name: GIFT-Eval
      type: Salesforce/GiftEval
    metrics:
    - name: MASE
      type: mase
      value: 0.658
    - name: CRPS
      type: crps
      value: 0.446
    source:
      name: GIFT-Eval leaderboard
      url: https://huggingface.co/spaces/Salesforce/GIFT-Eval
  - task:
      type: time-series-forecasting
      name: Time Series Forecasting
    dataset:
      name: TIME
      type: Real-TSF/TIME
    metrics:
    - name: MASE
      type: mase
      value: 0.626
    - name: CRPS
      type: crps
      value: 0.522
    source:
      name: TIME leaderboard
      url: https://huggingface.co/spaces/Real-TSF/TIME-leaderboard
  - task:
      type: time-series-forecasting
      name: Time Series Forecasting
    dataset:
      name: fev-bench
      type: autogluon/fev-bench
    metrics:
    - name: SQL skill score
      type: skill-score
      value: 50.39
    - name: MASE skill score
      type: skill-score
      value: 39.49
    source:
      name: fev-bench leaderboard
      url: https://huggingface.co/spaces/autogluon/fev-bench
license: other
---


<h1><img src="timestral-hourglass.png" alt="" style="display:inline; height:1em; width:auto; margin:0 0.3em 0 0; vertical-align:-0.1em;"> Timestral-209M</h1>


Timestral is a **family of time series foundation models** for zero-shot forecasting, available in [**5M**](https://huggingface.co/mistralai/Timestral-5M), [**28M**](https://huggingface.co/mistralai/Timestral-28M), [**123M**](https://huggingface.co/mistralai/Timestral-123M), and [**209M**](https://huggingface.co/mistralai/Timestral-209M) parameter versions. 
This repository contains the 209M checkpoint.

Timestral supports univariate and multivariate forecasting, past-only and known-future covariates, and probabilistic predictions across 21 quantiles. It accepts up to 32,768 historical time steps and forecasts up to 1,024 steps in a single forward pass.

We’re releasing the source code in our [GitHub repository](https://github.com/mistralai/timestral/) to make it easy to run Timestral and reproduce our benchmark results.

## Model Details

- **Size:** 209M parameters.
- **Architecture:** patch-based transformer with time attention and variate attention, 24 layers, embedding dimension 768.
- **Patching:** 32 time steps per patch. Each patch is embedded from its values together with their missing-value indicators.
- **Context length:** up to 32,768 time steps (1,024 patches). 
- **Forecast horizon**: Up to 1,024 time steps (32 patches) in a single forward pass. Longer horizons are forecast block by block, with each block's median forecast appended to the context.
- **Outputs:** 21 quantiles (0.01, 0.05, 0.1, 0.15, …, 0.85, 0.9, 0.95, 0.99). 
- **Inputs:** univariate or multivariate target variates, plus past-only and known-future covariates, numeric or categorical (categorical covariates are target-encoded). Missing values are marked as NaN.
- **Inference:** PyTorch on CPU or GPU.


## Benchmarks
Timestral-209M achieves **state-of-the-art zero-shot accuracy** across three major forecasting benchmarks: [GIFT-Eval](https://huggingface.co/spaces/Salesforce/GIFT-Eval), [TIME](https://huggingface.co/spaces/Real-TSF/TIME-leaderboard), and [fev-bench](https://huggingface.co/spaces/autogluon/fev-bench).

### Timestral-209M compared with other models
| Benchmark | Metric | [Timestral-209M](https://huggingface.co/mistralai/Timestral-209M) | t0-gamma | TimesFM-3 | Toto-2.0-2.5B | Chronos-2 |
|---|---|---|---|---|---|---|
| GIFT-Eval | MASE ↓ | **0.658** | 0.661 | 0.667 | 0.696 | 0.698 |
| | CRPS ↓ | **0.446** | 0.452 | 0.456 | 0.476 | 0.485 |
| TIME | MASE ↓ | **0.626** | 0.637 | 0.640 | 0.642 | 0.662 |
| | CRPS ↓ | **0.522** | 0.534 | 0.536 | 0.539 | 0.556 |
| fev-bench | SQL skill score ↑ | **50.39** | 49.42 | 48.99 | 44.42 | 47.28 |
| | MASE skill score ↑ | **39.49** | 37.99 | 37.82 | 32.54 | 35.50 |

### Results across the Timestral family
| Benchmark | Metric | [Timestral-5M](https://huggingface.co/mistralai/Timestral-5M) | [Timestral-28M](https://huggingface.co/mistralai/Timestral-28M) | [Timestral-123M](https://huggingface.co/mistralai/Timestral-123M) | [Timestral-209M](https://huggingface.co/mistralai/Timestral-209M) |
|---|---|---|---|---|---|
| GIFT-Eval | MASE ↓ | 0.705 | 0.678 | 0.659 | **0.658** |
| | CRPS ↓ | 0.479 | 0.461 | 0.448 | **0.446** |
| TIME | MASE ↓ | 0.652 | 0.638 | 0.628 | **0.626** |
| | CRPS ↓ | 0.545 | 0.534 | 0.525 | **0.522** |
| fev-bench | SQL skill score ↑ | 46.19 | 48.42 | 50.18 | **50.39** |
| | MASE skill score ↑ | 34.54 | 37.27 | 39.19 | **39.49** |

The Pareto-front plot below illustrates the trade-off between model size and forecasting performance across the Timestral family.

![Pareto front of model size versus forecasting performance for the Timestral models](https://cdn-uploads.huggingface.co/production/uploads/6a883eae29d17c41f6dbdfd4/FoDdgcwd64Zwg4L29FShg.png)

## Usage

### Install

Set up your environment:

```bash
pip install git+https://github.com/mistralai/timestral.git   # Python >= 3.10, torch >= 2.4
```

Or from a clone with [uv](https://docs.astral.sh/uv/), using the versions pinned in `uv.lock`:

```bash
git clone https://github.com/mistralai/timestral.git && cd timestral
uv sync --frozen
source .venv/bin/activate
```

### Run the model

Here is a simple example using synthetic data.

```python
import numpy as np
import torch
from timestral import TimestralForecaster

model = TimestralForecaster.from_pretrained(
    "mistralai/Timestral-209M",
    device="cuda" if torch.cuda.is_available() else "cpu"
)

# Synthetic example: one series with 1,000 historical observations.
context = np.random.default_rng(42).standard_normal(1000).cumsum()
forecast = model.forecast(context, prediction_length=96)

median = forecast.median
lower, upper = forecast.quantile(0.1), forecast.quantile(0.9)
```

Check out our [GitHub repository](https://github.com/mistralai/timestral/) for more details!

## Additional Resources
- [Blog post](https://mistral.ai/news/timestral/)
- [GitHub repository](https://github.com/mistralai/timestral/)
- Tech report: coming soon!


## License

Models have been released under a Modified MIT license: See [here](https://huggingface.co/mistralai/Timestral-209M/blob/main/LICENSE).

*You must not use this model in a manner that infringes, misappropriates, or otherwise violates any third party’s rights, including intellectual property rights*