---
license: apache-2.0
pipeline_tag: tabular-regression
tags:
- arxiv:2609.04540
---

# Mitra-v2 Regressor

Mitra-v2 regressor is a tabular foundation model that is pre-trained on purely synthetic datasets sampled from a mix of random regressors, including the new Hybrid SCM prior. It is the second generation of the Mitra regressor ([autogluon/mitra-regressor](https://huggingface.co/autogluon/mitra-regressor)), pre-trained with a 10x longer context, three times as many features, and an improved optimizer, and it replaces the scalar mean-squared-error head of Mitra-v1 with a 1,000-bin distributional head. On the TabArena and TALENT benchmarks it delivers state-of-the-art accuracy at the level of TabFM and EXAONE Tabular, while surpassing TabPFN-3 by a wide margin. The classification model is at [autogluon/mitra-classifier-2](https://huggingface.co/autogluon/mitra-classifier-2), and the inference and fine-tuning code with our evaluation results is at [autogluon/mitra-finetune](https://huggingface.co/autogluon/mitra-finetune).

## Architecture

Mitra-v2 is based on a 12-layer 2D Transformer of 76.7 M parameters (attention across rows and across columns), pre-trained by incorporating an in-context learning paradigm. Regression is cast as classification over 1,000 target bins: the model predicts a distribution over bins and the point prediction is the mean of that distribution. Apart from this head the architecture is unchanged from Mitra-v1.

## Usage

To use Mitra-v2 regressor, install AutoGluon and the `mitra-finetune` package by running:

```sh
pip install uv
uv pip install "autogluon.tabular[mitra]>=1.6" "tabarena>=0.1.0"
uv pip install git+https://huggingface.co/autogluon/mitra-finetune
```

A minimal example showing how to fine-tune and predict with the Mitra-v2 regressor using the same recipe as our reported results (50-step fine-tuning with 8-fold bagging). The recipe fine-tunes and bags eight copies of the model and requires a CUDA GPU; each `predict` call runs one bagged fine-tune:

```python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.datasets import fetch_california_housing
from sklearn.metrics import root_mean_squared_error
from huggingface_hub import snapshot_download
from mitra_finetune import MitraFinetune

# Load dataset
housing_data = fetch_california_housing()
X = pd.DataFrame(housing_data.data, columns=housing_data.feature_names)
y = pd.Series(housing_data.target, name="target")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
X_train, y_train = X_train.iloc[:2000], y_train.iloc[:2000]   # small subsample for a quick example

# Download the Mitra-v2 regressor weights
ckpt_dir = snapshot_download("autogluon/mitra-regressor-2")

# Fine-tune and predict
model = MitraFinetune(checkpoint_dir=ckpt_dir, problem_type="regression")
model.fit(X_train, y_train)
pred = model.predict(X_test)
print("RMSE:", root_mean_squared_error(y_test, pred))
```

The `mitra-finetune` package is required for regression: stock AutoGluon's Mitra regressor expects the scalar head of Mitra-v1, whereas these weights carry the 1,000-bin head, which the package wires into AutoGluon at fit time.

### Predictive distributions

The 1,000-bin head predicts a full distribution per row, not only its mean. `predict_distribution` runs one bagged fine-tune of its own (the same recipe as `predict`; call it instead of `predict` when you need both) and returns it as a `RegressionDistribution` (one histogram per bag child in target units, evaluated as their equal-weight mixture) for probabilistic scoring:

```python
dist = model.predict_distribution(X_test)   # or model.predict(X_test, output_type="full")
print("RMSE:", root_mean_squared_error(y_test, dist.point_prediction))   # the fit's predict() output
print("CRPS:", dist.crps(y_test).mean())
quantiles = dist.quantile([0.1, 0.5, 0.9])  # shape (n_test, 3)
edges, probs = dist.bin_edges, dist.probabilities   # (8, 1001), (8, n_test, 1000)
```

See the `mitra-finetune` README for the full interface (`mean`, `cdf`, `pdf`, `log_prob`, `quantile`, `crps`, and the raw `bin_edges` / `probabilities`).

## License

This project is licensed under the Apache-2.0 License.

## Reference

[Mitra-v2 Technical Report](https://arxiv.org/abs/2609.04540) (Amazon, 2026), also available on the [Hub](https://huggingface.co/autogluon/mitra-finetune/blob/main/Mitra_v2_Technical_Report.pdf).

```
@article{mitrav2_2026,
  title={{Mitra-v2} Technical Report},
  author={Tao, Yefan and Zhang, Xiyuan and Liu, Xinyi and Han, Boran and Maddix, Danielle and Fang, Haoyang and Han, Zhen and Gai, Jiading and Liu, Xuanqing and Bohlke-Schneider, Michael and Wang, Yuyang (Bernie) and Friedland, Gerald and Mah, Kevan and Lee, Chris and Kong, Chris},
  journal={arXiv preprint arXiv:2609.04540},
  year={2026}
}
```

The original Mitra:

```
@article{zhang2025mitra,
  title={Mitra: Mixed synthetic priors for enhancing tabular foundation models},
  author={Zhang, Xiyuan and Maddix, Danielle C and Yin, Junming and Erickson, Nick and Ansari, Abdul Fatir and Han, Boran and Zhang, Shuai and Akoglu, Leman and Faloutsos, Christos and Mahoney, Michael W and others},
  journal={arXiv preprint arXiv:2510.21204},
  year={2025}
}
```

Amazon Science blog: [Mitra: Mixed synthetic priors for enhancing tabular foundation models](https://www.amazon.science/blog/mitra-mixed-synthetic-priors-for-enhancing-tabular-foundation-models)
