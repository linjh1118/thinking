# Reinforcement learning

GRPO on [SkyRL](https://github.com/NovaSky-AI/SkyRL) with this repository's patch for the protein
modality and Qwen3.5 ([`skyrl/`](../../skyrl/)). Only the LLM (a
fresh LoRA adapter on the merged SFT weights) and the protein projector train; ESM3 features come from
a precomputed cache, and the GO block is baked into the embedding table. Rollouts run through a vLLM
multimodal model ([`bioreason2/rl/vllm_protein_mm.py`](../../bioreason2/rl/vllm_protein_mm.py)), so vLLM
applies the LoRA and the rollouts stay on-policy.

The released model's recipe, which [`grpo.sh`](grpo.sh) has as its defaults: the SFT model, one epoch
over the 2,905 scorable proteins of the SFT validation split (90 steps; the last partial batch is
dropped), batch 32 prompts x 16 rollouts,
lr 2e-5, LoRA r64/α128, KL 0.001, 4,096 generated tokens, advantages normalised by the group's standard
deviation. The reward is the judge alone: Kimi K3 at reasoning effort low and temperature 0 scores each
answer on five axes with [`judge_rubric.md`](judge_rubric.md) against every input the trace teacher had,
times a length factor (full credit to 13,000 characters, none at 16,000); an answer with no parseable GO
term scores 0. The InterPro block is in half the prompts.

**1. Environment.** A venv on the NeMo 26.06 container (`nvcr.io/nvidia/nemo:26.06`), built inside it;
it uses the container's torch, transformers and vLLM, and fetches and patches SkyRL into `skyrl/src`:

```bash
bash scripts/rl/build_env.sh <venv>
source <venv>/bin/activate
python scripts/rl/verify_env.py      # on a GPU node
```

**2. Checkpoint** (inference environment): one text-only layout for the trainer, vLLM and the exporter,
with the 200 GO tokens baked into the embedding table.

```bash
hf download nvidia/BioReason-Pro-2-9B-SFT --local-dir ckpt/sft
python -m bioreason2.rl.prepare_checkpoint --src ckpt/sft --dst ckpt/rl-init \
    --protein_projection_norm blocknorm --protein_projection_norm_target 0.0133
```

**Prompt tables** (inference environment). Steps 3 and 4 read the SFT validation split and the corpus's
labels. RL needs no traces, so both come from the public corpus; `--keep-untraced` keeps the train and
validation rows without a trace (with empty targets), which makes the tables fit for RL and evaluation
but not for SFT. Built this way, they hold the same 278,800 prompts and labels, split for split, as the
tables of the released run:

```bash
python scripts/data/fetch_corpus.py --split train
python scripts/data/fetch_corpus.py --split test
python scripts/data/prepare_corpus.py --src data/v2 --out data/v2-ep75
python scripts/data/build_question.py --v2-root data/v2-ep75 --out data/sft/v2-nofeatures --no-features --keep-untraced
python scripts/data/build_question.py --v2-root data/v2-ep75 --out data/sft/v2-features --keep-untraced
```

**3. ESM3 cache.** RL reads ESM3 layer-37 embeddings from disk. `eval.py` writes them when
`PROTEIN_EMBED_CACHE_WRITE` is set, as it generates; run it over the SFT validation split (the training
pool):

```bash
PROTEIN_EMBED_CACHE_WRITE=cache/esm3 EVAL_SPLIT=val EVALS_PATH=results/cache-val \
    CKPT_DIR=ckpt/sft SCORE=False bash scripts/eval/eval.sh
```

**4. Data** (inference environment). The released run's training proteins are in
[`data/rl/pool_ids.txt`](../../data/rl/pool_ids.txt). Each is rendered without and with the InterPro block,
and half the proteins, chosen by a hash of the id, take the InterPro render:

```bash
mkdir -p rl_data
for arm in nofeatures features; do
  python -m bioreason2.rl.build_dataset --table data/sft/v2-$arm --split val --ids data/rl/pool_ids.txt \
      --cache_dir cache/esm3 --checkpoint ckpt/rl-init --output rl_data/train_$arm.parquet
  python -m bioreason2.rl.add_judge_fields --input rl_data/train_$arm.parquet \
      --output rl_data/judge_train_$arm.parquet --truth_corpus data/v2/proteins
done
python scripts/rl/mix_features.py --without rl_data/judge_train_nofeatures.parquet \
    --with rl_data/judge_train_features.parquet --share 0.5 \
    --keep_without data/rl/overlong_ids.txt --output rl_data/train.parquet
```

`overlong_ids.txt` holds the 2 proteins the hash gives the InterPro prompt although it is longer than
the trainer's 8,704-token `max_prompt_length`; SkyRL drops such rows silently, so they keep the plain
prompt. With these lists the mix reproduces the released run's assignment exactly: 1,442 of the 2,905
training prompts carry the InterPro block.

**5. Train** on one 8-GPU node, inside the container with the venv active. The judge is any
OpenAI-compatible endpoint serving the judge model ([`bioreason2/rl/judge.py`](../../bioreason2/rl/judge.py)
is the client to adapt for another API); the run resumes from its latest checkpoint when restarted. It
logs to Weights & Biases when `WANDB_API_KEY` is set, to the console otherwise:

```bash
MODEL_PATH=ckpt/rl-init TRAIN_FILE=rl_data/train.parquet \
CACHE_DIR=cache/esm3 OUT_DIR=rl_runs/9b-judge \
SKYRL_JUDGE_URL=<https://your-endpoint/v1/chat/completions> SKYRL_JUDGE_MODEL=<Kimi K3 at your endpoint> \
JUDGE_API_KEY=<key> bash scripts/rl/grpo.sh
```

Watch `policy_entropy` rather than the reward as the health signal. The final step is the one kept.
The released run also generated for 600 held-out test proteins during training and scored them on GO
F1; that validation was for monitoring only, never selected a checkpoint, and is not part of this
recipe; score the exported model (step 6) with `scripts/eval/eval.sh` instead.

**6. Export** the final step into the layout `eval.py` and `predict.py` read (the LoRA merged, the
trained projector), in the RL environment, whose torch wrote the step's sharded state:

```bash
python -m bioreason2.rl.export_checkpoint --step_dir rl_runs/9b-judge/ckpt/global_step_90 \
    --base ckpt/sft --dst ckpt/rl --lora_alpha 128 --lora_rank 64
```
