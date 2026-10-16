---
pipeline_tag: time-series-forecasting
library_name: timestral
tags:
- time-series
- forecasting
- foundation-model
model-index:
- name: Timestral-28M
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
      value: 0.678
    - name: CRPS
      type: crps
      value: 0.461
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
      value: 0.638
    - name: CRPS
      type: crps
      value: 0.534
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
      value: 48.42
    - name: MASE skill score
      type: skill-score
      value: 37.27
    source:
      name: fev-bench leaderboard
      url: https://huggingface.co/spaces/autogluon/fev-bench
license: other
---


<h1><img src="timestral-hourglass.png" alt="" style="display:inline; height:1em; width:auto; margin:0 0.3em 0 0; vertical-align:-0.1em;"> Timestral-28M</h1>


Timestral is a **family of time series foundation models** for zero-shot forecasting, available in [**5M**](https://huggingface.co/mistralai/Timestral-5M), [**28M**](https://huggingface.co/mistralai/Timestral-28M), [**123M**](https://huggingface.co/mistralai/Timestral-123M), and [**209M**](https://huggingface.co/mistralai/Timestral-209M) parameter versions. 
This repository contains the 28M checkpoint. 

>[!Note]
> For more information about our Timestral family, go to the main model page: [Timestral-209M](https://huggingface.co/mistralai/Timestral-209M).


## Model Details

- **Size:** 28M parameters.
- **Architecture:** patch-based transformer with time attention and variate attention, 12 layers, embedding dimension 256.
- **Patching:** 32 time steps per patch. Each patch is embedded from its values together with their missing-value indicators.
- **Context length:** up to 32,768 time steps (1,024 patches). 
- **Forecast horizon**: Up to 1,024 time steps (32 patches) in a single forward pass. Longer horizons are forecast block by block, with each block's median forecast appended to the context.
- **Outputs:** 21 quantiles (0.01, 0.05, 0.1, 0.15, …, 0.85, 0.9, 0.95, 0.99). 
- **Inputs:** univariate or multivariate target variates, plus past-only and known-future covariates, numeric or categorical (categorical covariates are target-encoded). Missing values are marked as NaN.
- **Inference:** PyTorch on CPU or GPU.

## Benchmarks
Timestral-209M achieves **state-of-the-art zero-shot accuracy** across three major forecasting benchmarks: [GIFT-Eval](https://huggingface.co/spaces/Salesforce/GIFT-Eval), [TIME](https://huggingface.co/spaces/Real-TSF/TIME-leaderboard), and [fev-bench](https://huggingface.co/spaces/autogluon/fev-bench).

Smaller Timestral models offer a trade-off between model size and forecasting performance. All Timestreal models outperform every other model at the respective model size. See the Pareto-front plot on the [main model page](https://huggingface.co/mistralai/Timestral-209M).

### Results across the Timestral family
| Benchmark | Metric | [Timestral-5M](https://huggingface.co/mistralai/Timestral-5M) | [Timestral-28M](https://huggingface.co/mistralai/Timestral-28M) | [Timestral-123M](https://huggingface.co/mistralai/Timestral-123M) | [Timestral-209M](https://huggingface.co/mistralai/Timestral-209M) |
|---|---|---|---|---|---|
| GIFT-Eval | MASE ↓ | 0.705 | 0.678 | 0.659 | **0.658** |
| | CRPS ↓ | 0.479 | 0.461 | 0.448 | **0.446** |
| TIME | MASE ↓ | 0.652 | 0.638 | 0.628 | **0.626** |
| | CRPS ↓ | 0.545 | 0.534 | 0.525 | **0.522** |
| fev-bench | SQL skill score ↑ | 46.19 | 48.42 | 50.18 | **50.39** |
| | MASE skill score ↑ | 34.54 | 37.27 | 39.19 | **39.49** |

## License

Models have been released under a Modified MIT license: See [here]((https://huggingface.co/mistralai/Timestral-28M/blob/main/LICENSE).

*You must not use this model in a manner that infringes, misappropriates, or otherwise violates any third party’s rights, including intellectual property rights*