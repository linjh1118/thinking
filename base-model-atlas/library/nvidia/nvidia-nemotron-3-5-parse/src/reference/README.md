# Reference examples

## ParseBench reproduction

The [ParseBench pipeline bundle](parsebench/pipeline/README.md) provides runnable single-, double-, and triple-pass inference, shared postprocessing, public-data preparation, and evaluation with the pinned official scorer.

| Pipeline | Reproduced ParseBench score |
| --- | ---: |
| Single | 72.72 |
| Double | 74.88 |
| Triple | 75.14 |
| Triple, region union | 75.20 |

Start with the [installation and data-preparation instructions](parsebench/pipeline/README.md). Exact model, dataset, renderer, and scorer identities are recorded in [expected_results.json](parsebench/pipeline/expected_results.json), with measured coverage and category scores in [validation_metrics.json](parsebench/pipeline/validation_metrics.json).

Other files in this reference directory retain their original measurements and manifests; their settings and results may differ from this pipeline bundle.

The headline score uses triple-pass inference with `--triple-regions union`. Default triple-pass inference uses detector regions only; region union adds full-page Table/Chart regions subject to overlap filtering.
