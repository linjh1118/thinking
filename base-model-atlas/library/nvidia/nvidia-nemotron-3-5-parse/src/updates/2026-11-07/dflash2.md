# DFlash2 for Nemotron 3.5 Parse

An optional 89.3M-parameter drafter that accelerates the target model's decoding.
It requires the target model and shares its embeddings and output head.

```bash
hf download nvidia/Nemotron-3.5-Parse --local-dir ./parse35
vllm serve ./parse35 \
  --served-model-name nemotron-parse \
  --trust-remote-code \
  --speculative-config '{"method":"dflash","model":"./parse35/dflash2","num_speculative_tokens":32}'
```

Use vLLM with native Nemotron Parse and DFlash2 support. No model-specific package,
worker plugin, selector hook or source modification is required. The usual Parse
prompts and postprocessing apply. See [serving](../docs/serving.md).

## Performance

![Pages per second across concurrency](performance/concurrency.png)

The curve uses the fastest tested native draft length at each concurrency.
Set `num_speculative_tokens` to the chosen length for your workload; the server
keeps that length fixed.

The curve uses one H200, BF16, 2,078 ParseBench pages and three trials per point.
See [the benchmark protocol and downloadable data](performance/README.md).
The basic command above does not set every benchmark option. These single-pass
measurements are separate from the reference triple-pass quality scores. Verified
speculative execution can change greedy outputs because attention execution shapes
differ; the curve does not establish exact-output or parsing-quality equivalence.

The drafter supports up to 32 speculative tokens and a 16,384-position context.
Its inference weights occupy approximately 179 MB. Use the local `./parse35/dflash2`
folder; `nvidia/Nemotron-3.5-Parse/dflash2` is not a Hub model ID.

## Draft-length tuning

Native single-pass pages/s on one H200, BF16, 2,078 pages; median of three runs. A dash means no three-run result under this native protocol. These are separate from HTTP multipass timings.

| Concurrency | 8 tokens | 16 tokens | 24 tokens | 32 tokens | Best tested length |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 2.58 | 3.37 | 3.97 | 4.10 | 32 |
| 2 | 4.39 | 6.00 | 6.64 | 6.71 | 32 |
| 4 | 7.24 | 9.26 | 10.63 | 10.66 | 32 |
| 8 | 11.43 | 13.35 | 14.54 | 14.31 | 24 |
| 16 | 14.42 | 16.55 | 17.36 | 17.25 | 24 |
| 32 | 17.70 | 18.72 | 19.09 | 17.53 | 24 |
| 64 | 19.06 | 19.71 | 19.51 | 18.82 | 16 |
| 128 | 19.55 | 20.15 | 19.94 | 19.23 | 16 |
| 256 | 19.32 | 20.36 | 19.86 | 19.41 | 16 |
| 512 | 19.61 | 20.44 | 20.38 | 19.58 | 16 |

All values use the same documented native settings. These are best tested choices rather than a universal optimum.

## License

The parent repository's [OpenMDW-1.1 license](../LICENSE),
[tokenizer attribution](../TOKENIZER_ATTRIBUTION.md), and
[third-party notices](../THIRD_PARTY_NOTICES.md) apply.
