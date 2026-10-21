---
license: bsd-3-clause
library_name: diffusers
tags:
- modular-diffusers
- biology
- protein-design
- annotated-cif
---
<p align="center"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/wordmark-dark.webp"><img src="assets/wordmark.webp" width="420" alt="RFD4-Proteína"></picture></p>
<p align="center"><a href="https://rfd4-proteina.org/">Project page</a> · <a href="https://huggingface.co/nvidia/RFD4-Proteina">Model</a> · <a href="https://huggingface.co/nvidia/RFD4-Proteina-Diffusers">Diffusers weights</a> · <a href="https://huggingface.co/datasets/nvidia/RFD4-Proteina">Training data</a> · <a href="https://github.com/RosettaCommons/RFD4-Proteina">Code</a></p>

# rfd4-proteina-prep

Annotated-CIF input preparation and output export for the
[Diffusers](https://github.com/huggingface/diffusers) `RFD4ProteinaPipeline`.

The pipeline itself only consumes prepared feature tensors. This package holds the domain-specific parts that turn an
annotated CIF file (the RFD4 condition annotations written by AtomWorks Studio) into those tensors, and the generated
tensors back into an annotated CIF. It builds on [AtomWorks](https://github.com/RosettaCommons/atomworks) and has no
dependency on the original RFD4 runtime.

## Install and authenticate

Python 3.11 or newer is required. The repository and the model are public, so no authentication is needed for the downloads below; log in only if you hit rate limits, and keep tokens out of notebooks and shell history.

```bash
pip install huggingface_hub
hf auth login
hf auth whoami
hf download nvidia/RFD4-Proteina-prep --local-dir rfd4-prep
pip install ./rfd4-prep
pip install git+https://github.com/huggingface/diffusers
```

`RFD4ProteinaPipeline` was merged into Diffusers on 2026-10-20 ([huggingface/diffusers#15088](https://github.com/huggingface/diffusers/pull/15088)) and ships in the next release, so install Diffusers from GitHub until then. The model revision below is the one whose parameter names and shapes match that code. Older model revisions, including `b21bec64`, use different parameter names and do not load. The helper does
not convert weights or silently repair compatibility. `trust_remote_code=True` loads Python from the helper repo;
inspect `block.py` and pin a revision for reproducible use. It does not install dependencies automatically.

## Hub custom block: download, prepare, generate, export

Both interfaces use the same installed `rfd4_proteina_prep` implementation. The custom block is a thin wrapper,
not a second vendored copy of the chemistry code, and does not add AtomWorks to Diffusers itself.

```python
import torch
from huggingface_hub import HfApi, hf_hub_download
from diffusers import ModularPipeline, RFD4ProteinaPipeline

helper_repo = "nvidia/RFD4-Proteina-prep"
# Resolve once so code and inputs come from one immutable snapshot.
helper_revision = HfApi().model_info(helper_repo).sha
model_revision = "92fc3ae50e336b2ec59c713c19cfd43e5d3e923b"
helper = ModularPipeline.from_pretrained(
    helper_repo, revision=helper_revision, trust_remote_code=True
)
input_cif = hf_hub_download(helper_repo, "examples/inputs/protein_binder.cif", revision=helper_revision)
prepared = helper(cif_path=input_cif, seed=42, device="cuda:0")
features, atoms = prepared.get("features"), prepared.get("atom_array")

pipe = RFD4ProteinaPipeline.from_pretrained(
    "nvidia/RFD4-Proteina-Diffusers", revision=model_revision, dtype=torch.bfloat16
).to("cuda:0")
# The tensors the pipeline takes as arguments; the annotations go in one mapping. `coords_nm` is one of
# them: partial diffusion and inverse folding read it by name, and a full run ignores it.
required = ["padding_mask", "is_in_context_conditioning", "supports_local_latent", "token_type",
            "atom37_mask", "coords_nm"]
inputs = {name: features[name] for name in required}
conditioning = {name: value for name, value in features.items() if name not in required}
output = pipe(**inputs, conditioning_features=conditioning, generator=torch.Generator("cuda:0").manual_seed(42))
cif_path = helper(
    pipeline_output=output, features=features, atom_array=atoms,
    output_path="design.cif", output="cif_path",
)
print(cif_path)
```

Use a new output filename each time. Export refuses to overwrite an existing file. `row` selects a batch row
when generating several designs of the same prepared input. Tensor coordinates are in nanometers; CIF coordinates
are in angstroms. Keep the atom mapping together with its features, not a different example's mapping.

The regular Python API remains available without remote-code loading:

```python
from rfd4_proteina_prep import prepare_cif, write_cif
features, atoms = prepare_cif(input_cif, seed=42, device=pipe.device)
required = ["padding_mask", "is_in_context_conditioning", "supports_local_latent", "token_type",
            "atom37_mask", "coords_nm"]
inputs = {name: features[name] for name in required}
conditioning = {name: value for name, value in features.items() if name not in required}
output = pipe(**inputs, conditioning_features=conditioning, generator=torch.Generator("cuda:0").manual_seed(42))
write_cif(output, features, atoms, "another-design.cif")
```

`prepare_cif` returns a single-example batch; `seed` controls expansion of flexible segments and preserves the
Python, NumPy and CPU PyTorch global random states.

## Downloadable non-antibody examples

The catalog includes all seven non-antibody task presets from the model's Studio gallery, plus the three
web-editor examples. **Antibody and VHH/nanobody inputs are excluded.** Existing assets in the separate model
repository are not deleted. Inputs are copied without changing their annotations. Source revisions, SHA-256
hashes, task-specific arguments and model/code pins are recorded in [examples/manifest.json](examples/manifest.json).

| Example | Input | Special invocation |
| --- | --- | --- |
| PD-L1 protein binder | [protein_binder.cif](examples/inputs/protein_binder.cif) | Default conditioned generation |
| Catalytic-motif enzyme | [enzyme_design.cif](examples/inputs/enzyme_design.cif) | Default |
| 1QJG motif scaffold | [motif_scaffolding.cif](examples/inputs/motif_scaffolding.cif) | Default |
| SAM ligand binder | [small_molecule_binder.cif](examples/inputs/small_molecule_binder.cif) | Default |
| Unconditional protein | [unconditional.cif](examples/inputs/unconditional.cif) | Default |
| 2KL8 inverse folding | [inverse_folding.cif](examples/inputs/inverse_folding.cif) | `inverse_folding=True`, both `partial_t` values zero |
| 2KL8 partial diffusion | [partial_diffusion.cif](examples/inputs/partial_diffusion.cif) | Start times derived from the checkpoint schedule; 40% remaining |
| Studio PD-L1 | [ppi_pdl1.cif](examples/studio/ppi_pdl1.cif) | Default |
| Studio PH2 active site | [mcsa_ph2.cif](examples/studio/mcsa_ph2.cif) | Default |
| Studio IAI ligand binder | [disco_iai.cif](examples/studio/disco_iai.cif) | Default |

To check every input without downloading weights or using a GPU:

```bash
python rfd4-prep/examples/run_hub_examples.py --prepare-only --out prep-check
```

To generate all ten presets with the pinned checkpoint, or a selected subset:

```bash
python rfd4-prep/examples/run_hub_examples.py --out designs
python rfd4-prep/examples/run_hub_examples.py --tasks protein_binder inverse_folding --out selected-designs
```

The runner downloads files with `hf_hub_download`, verifies hashes, uses each task's options, and writes a
revision-bearing report. Choose a fresh output directory for each run. It has no dependency on a Studio checkout.
Use this runner rather than `run_examples.py`, which needs a local checkout of the inputs. The two target
different APIs on purpose: this one installs and enforces the pinned Diffusers revision in the manifest, while
`run_examples.py` runs against whatever Diffusers is installed and so follows the current argument names.

Validation for this addition: all ten inputs produce identical tensors to the installed package at
`199dfd7f83db1487a02fc1f9f15536e32a9a6a6b`; CPU tests cover RNG preservation, real CIF round-trip export,
batch-row selection, non-overwriting behavior, and explicit remote-code trust. The pinned Diffusers classes match
all checkpoint parameter names and shapes. **New GPU generations and biological quality have not been validated
by these checks.** No generated output is presented as a result of this addition. Refolding, scoring and Studio's
search services are separate; the helper only performs CIF preparation and export.

## AtomWorks version

The pin is **PyPI `atomworks[ml]==3.0.4`**, and it is worth being explicit because the version numbering is
ambiguous. The RFD4 repository pins AtomWorks by git commit rather than by release, and a commit it pinned declares
`version = "3.0.1"` in its own `pyproject.toml` while carrying the 3.0.3 API. So "3.0.1" means two different things
depending on where you read it, and installing PyPI 3.0.1 gives you an `AnnotateCovalentModifications` signature this
package no longer calls.

**This pin is one release ahead of RFD4's `main`, which still asks for 3.0.3.** That is deliberate. 3.0.4 is a
drop-in: it adds `has_annotation` and lets `insert_atoms` take a pre-built block, so the annotation and
concatenation paths this package already calls get cheaper without any call site changing. Verified identical output
over 1,724 quantities on ten inputs, and about 6-8% off the coordinate-transfer path that dominates `write_cif`
(127 to 120 ms on a 98-residue redesign, 956 to 887 ms on a 493-residue one). RFD4 requires 3.0.4 on the branch
carrying its batched coordinate transfer, so this is where upstream is going rather than away from it.

## Keeping up with the RFD4 repository

The modules under `_cif/` are the RFD4 datapipe, vendored unedited. They are not an inference-only fork: the training
paths are present and `is_inference` selects between them at runtime, exactly as upstream, because
`build_design_validation_pipeline` upstream *is* `build_design_train_pipeline(is_inference=True)`. Keeping both halves
is what makes a release cheap to take — `python tools/vendor_from_main.py --rfd4 ... --out <dir>` regenerates the
whole set mechanically, and the only edits it applies are an import rewrite for the flat layout, plus the two
substitutions recorded in `check_vendored.py` (the DDP logger becomes plain `logging`; two data files are read from
this package rather than a repository checkout).

Taking a new RFD4 release is a short, repeatable loop — regenerate, read the diff, check the copy, diff the output.
**[MAINTAINING.md](MAINTAINING.md) is the runbook**, including the input set to test against and the downstream
integrations to warn. In outline it is four commands, and the diff you read is the upstream change and nothing else:

```bash
python tools/vendor_from_main.py --rfd4 /path/to/RFD4-Proteina --commit origin/main --out /tmp/new
diff -r /tmp/new src/rfd4_proteina_prep/_cif      # only cath_mapping.py should be local-only
cp /tmp/new/*.py src/rfd4_proteina_prep/_cif/
python tools/check_vendored.py --rfd4 /path/to/RFD4-Proteina --against origin/main
```

Regenerating at the currently vendored commit reproduces the shipped tree exactly, so a non-empty diff in step 2 is
always upstream's doing, never an artefact of the vendoring. `tools/feature_snapshot.py` then records what
`prepare_cif` produces before and after, because matching RFD4's source and feeding the model the same tensors are
different claims — a release once dropped a whole conditioning channel while the drift checker stayed green.

Each module records the commit it came from in its header. `tools/check_vendored.py` checks both halves of that
claim:

```bash
python tools/check_vendored.py --rfd4 /path/to/RFD4-Proteina --against origin/main            # does the copy match?
python tools/check_vendored.py --rfd4 /path/to/RFD4-Proteina --against origin/main --mode pin # has the source moved?
```

The default content check compares the copy against the source definition by definition rather than line by line, so
the rewritten imports, the dropped jaxtyping annotations and the different line width do not register. A clean run
means every remaining difference is listed in that file's `ACCEPTED` table with the reason it stays — and each entry
is pinned to the exact pair of versions it was agreed for, so it stops applying the moment either side moves. Neither
mode rewrites anything: porting a change needs a human. Exit status is 0 clean, 1 drift, 2 unusable.

`--against` matters. The RFD4 checkout's `HEAD` may hold the package under a different name than the recorded source
paths use, in which case no source can be read; the tool reports that and exits 2 rather than calling it a pass.

## Fine-tuning

The datapipe's training path ships with this package, so the same code that featurizes an inference input can build
training batches. The design tasks it samples from live in `_cif/transforms_design_task.py` and need one extra
dependency:

```bash
pip install 'rfd4-proteina-prep[train]'
```

Inference never imports those modules, so a plain install is unchanged by their presence. What this package does *not*
provide is the rest of a training run: the dataset loader, the task configuration, the noising schedule and the loss.
`build_design_train_pipeline` is the featurizer, not the trainer.

Source attribution and third-party licenses: [THIRD_PARTY_LICENSES.txt](THIRD_PARTY_LICENSES.txt).

To generate several designs of one input, ask the pipeline for them and replicate the features to match, which is
what RFD4 itself does: its collate step repeats each sample `num_replicates` times before batching, so every
per-row quantity has one row per design and `row` indexes them all alike.

```python
designs = 8
output = pipe(
    **inputs,
    conditioning_features=conditioning,
    num_designs_per_prompt=designs,
    generator=[torch.Generator("cuda:0").manual_seed(seed) for seed in range(designs)],
)
replicated = {
    name: value.repeat_interleave(designs, dim=0) if torch.is_tensor(value) else value
    for name, value in features.items()
}
for row in range(designs):
    write_cif(output, replicated, atoms, f"design_{row}.cif", row=row)
```

Use `repeat_interleave`, not `repeat`: an input's designs sit together, so output row `r` belongs to input
`r // designs`. Passing the features unreplicated raises `IndexError` on the second design rather than writing the
wrong row.
