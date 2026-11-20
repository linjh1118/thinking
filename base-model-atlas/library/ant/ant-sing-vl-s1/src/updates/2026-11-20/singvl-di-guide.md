# Decision Index reproduction

This model repository contains the complete native inference entry point and the
Decision Index adapter, `inference.engine:D3Engine`. The adapter calls
`SingVLS1.predict`; it does not use the stock causal-language-model readout.

## Pinned release and public results

| Component | Revision |
|---|---|
| Downloadable model and DI adapter | `inclusionAI/SingVL_S1_4B`, revision `dd9fcbe2412068def01666b1d1a443e412f11214` |
| Originally evaluated checkpoint | `93f15cd61c1cf417d9cb2631f6be2df13510829e` |
| Original results and code snapshot | `echoxvf/SingVL_S1_4B-DI-results`, dataset revision `90ec7e159da6fa21d762f1f75876ea79049d0f4a` |
| Decision Index kit | `f5a6e4fd85fed05e77878dfc4966d0568bfb45ec` |

Use `inference.engine:D3Engine` with its default settings for both public and private evaluations. The model weights, configuration, tokenizer and processor match the original checkpoint. The new native predictor batches text questions within each request. `release.json` records the weight and code hashes.

| Complete public suite | Requests (all successful) | Batch engine | Original serial engine |
|---|---:|---:|---:|
| Text | 140,178 | 69.75 | 69.76 |
| Vision | 12,210 | 73.74949871316771 | 73.74949871316771 |

Both runs used the same PPU2 system, public suites, scoring kit and maximum of 1,638,400 pixels per image. The [batch release predictions and scores](https://huggingface.co/datasets/echoxvf/SingVL_S1_4B-DI-results/tree/709aaf417ebf1d00dd01fdb49e306573b801d488/releases/batch-65k) correspond to the batch engine. The original results and prediction code remain accessible at the submission revision above. Private scores and official RTX PRO 6000 latency qualification are maintainer-run.

## Download and install

Use Python 3.12, Git and a CUDA GPU. Run these commands from a workspace directory.
The Hub CLI downloads the code and the weights from the same pinned model release.

```bash
python -m pip install "huggingface_hub>=0.34,<2"
hf download inclusionAI/SingVL_S1_4B \
  --revision dd9fcbe2412068def01666b1d1a443e412f11214 --local-dir ./singvl-s1-4b
python -m pip install -r ./singvl-s1-4b/inference/requirements-di.txt
```

`requirements.txt` records the submitted software versions, including PyTorch
2.10.0, torchvision 0.25.0 and Transformers 5.13.1. Use hardware-compatible builds
of PyTorch and torchvision. The original public run was BF16 on independent PPU
workers. NVIDIA smoke tests also passed with Transformers 5.13.1 and PyTorch
2.12.1+cu129 on an A100; this does not establish bitwise agreement across hardware
or replace the maintainers' latency test.

To inspect the original submission snapshot without downloading model weights
again:

```bash
hf download echoxvf/SingVL_S1_4B-DI-results --repo-type dataset \
  --revision 90ec7e159da6fa21d762f1f75876ea79049d0f4a \
  --local-dir ./singvl-original-results
```

## Prepare the public suites

Build the suites using the pinned kit installed above. These commands download
the original benchmark sources; do not substitute prediction files for inputs.
Some sources require accepted terms and a logged-in Hugging Face account.

```bash
decision-index suite rebuild --work ./work
decision-index suite import \
  --rows ./work/artifacts/benchmark-suite/release-v2-rebuilt/selected-rows.jsonl.gz \
  --added-rows ./work/artifacts/benchmark-suite/release-v2-rebuilt/added-rows.jsonl.gz \
  --gsm8k-rows ./work/artifacts/benchmark-suite/release-v3-rebuilt/gsm8k-rows.jsonl.gz \
  --dir ./suite-0.3 --edition 0.3
decision-index suite verify --dir ./suite-0.3 --edition 0.3
decision-index suite rebuild --vision --work ./work
decision-index vision verify --dir ./work/vision
```

See the pinned kit's README and `docs/vision.md` for dataset access requirements.
Existing verified Public 0.3 suites can be reused.

## Run Text or Vision

The launcher sets `PYTHONPATH` to this model snapshot and uses the DI adapter
shipped here. It works from any current directory. The model argument is a local
checkpoint directory, not a Hub model ID; it defaults to the downloaded snapshot
containing the launcher.

```bash
python ./singvl-s1-4b/inference/run_decision_index.py \
  --panel text --suite-dir ./suite-0.3 \
  --device cuda:0 --out ./runs/singvl-65k-text

python ./singvl-s1-4b/inference/run_decision_index.py \
  --panel vision --suite-dir ./work/vision \
  --device cuda:0 --out ./runs/singvl-65k-vision
```

Use fresh output directories for the batch engine to avoid resuming an earlier serial run.

Add `--limit 10` and use a separate output directory for a smoke test. Such a run
is partial and its score is not the complete public benchmark result.
`--print-command` shows the resolved paths and DI command without loading weights.

Equivalent direct commands, run from the downloaded model repository root:

```bash
python -m decision_index pipeline --edition 0.3 --suite-dir /path/to/suite-0.3 \
  --engine inference.engine:D3Engine --model "$PWD" --option device=cuda:0 \
  --out /path/to/new-text-run
python -m decision_index vision pipeline --dir /path/to/vision --workers 1 \
  --engine inference.engine:D3Engine --model "$PWD" --option device=cuda:0 \
  --out /path/to/new-vision-run
```

The engine uses BF16, SDPA, prefix-bidirectional full attention, causal GDN, last-valid-input readout and disabled KV caching. For a text request with multiple questions, it sorts complete question prompts by length, then groups them so that the longest prompt length times the number of prompts in a batch is at most 65,536 tokens. Each question retains independent attention and a separate answer. Single-question and image requests follow the serial path. Limits are 256 options, four images, 65,536
text input tokens or 10,000 tokens with images, and 1,638,400 pixels per image.
Inputs exceeding capacity raise `Unsupported`; they are not truncated.

## HTTP service

For direct HTTP usage, launch the model repository's server:

```bash
python ./singvl-s1-4b/inference/serve.py \
  --model ./singvl-s1-4b --device cuda:0 --port 8173
```

Text can then use the DI kit's `http` engine. Vision can use `decide` with
`protocol=decisions`, `path=/v1/systemone`, `image_encoding=data_url` and
`max_pixels=1638400`. The native adapter above is the primary submission entry
point; both paths use the same native predictor. See `README.md` for request
examples. A file-path image request additionally requires `--image-root`.
