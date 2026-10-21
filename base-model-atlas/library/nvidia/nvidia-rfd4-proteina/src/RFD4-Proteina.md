---
license: bsd-3-clause
library_name: rfd4-proteina
language:
- en
datasets:
- nvidia/RFD4-Proteina
tags:
- biology
- protein-design
- biomolecular-design
- structure-generation
- flow-matching
- annotated-cif
---
<p align="center"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/wordmark-dark.webp"><img src="assets/wordmark.webp" width="520" alt="RFD4-Proteína"></picture></p>
<p align="center"><strong>Sequence and structure, designed together.</strong><br>Baker Lab × NVIDIA GenAIR</p>
<p align="center"><a href="https://rfd4-proteina.org/">Project page</a> · <a href="https://github.com/RosettaCommons/RFD4-Proteina">Code</a> · <a href="https://rfd4-proteina.org/latest/">Documentation</a> · <a href="https://huggingface.co/datasets/nvidia/RFD4-Proteina">Training data</a> · <a href="https://huggingface.co/spaces/nvidia/rfd4-proteina-zerogpu">Studio (ZeroGPU)</a> · <a href="https://huggingface.co/spaces/nvidia/rfd4-proteina-space">Studio (dedicated GPU)</a></p>

# RFD4-Proteína

RFD4-Proteína is a flow-matching model for biomolecular design. It generates protein sequences and all-atom structures together, conditioned on the molecular context you want to preserve: a binding target, an enzyme motif, a ligand, or selected structural features.

<img src="assets/design-gallery.png" width="1050" alt="Examples from the project: nanobody complex, protein–DNA binder, RNA pseudoknot, ligand pocket, glycan complex, and protein assembly.">

## Where to find each entry point

This repository is the **canonical native bundle**. `config.json` and `model.safetensors` at
the root are the *native* weights, loaded by `Proteina.from_pretrained`.

| Call | Weights | Location | Status |
|---|---|---|---|
| `Proteina.from_pretrained("nvidia/RFD4-Proteina")` | Native | root of this repo | **Supported** |
| `RFD4ProteinaPipeline.from_pretrained("nvidia/RFD4-Proteina-Diffusers")` | Diffusers | [its own repo](https://huggingface.co/nvidia/RFD4-Proteina-Diffusers) | **Supported**, Diffusers from git until the next release |

It is one model throughout — nothing is retrained. The Diffusers weights are the same tensors
re-prefixed and split across `transformer/` and `vae/`. Diffusers needs `model_index.json` at the
root of whatever it is pointed at, so it has its own repository. Annotated-CIF preprocessing for
Diffusers is in [`nvidia/RFD4-Proteina-prep`](https://huggingface.co/nvidia/RFD4-Proteina-prep).

> **Diffusers from git until the next release.** `nvidia/RFD4-Proteina-Diffusers` holds the same 2026-10-19
> release. `RFD4ProteinaPipeline` was merged into Diffusers on 2026-10-20 ([huggingface/diffusers#15088](https://github.com/huggingface/diffusers/pull/15088)) and ships in the next
> release; until then install Diffusers from GitHub, as in the snippet below.

Training data lives in the companion [dataset repository](https://huggingface.co/datasets/nvidia/RFD4-Proteina).

## At a glance

| | Details |
|---|---|
| **Model** | Joint sequence–structure generation with a matched flow model and autoencoder |
| **Inputs** | Annotated CIF structures or YAML condition specifications |
| **Outputs** | Designed molecular structures in CIF format, with generated residue identities and coordinates |
| **Weights** | EMA weights; 435,622,465 stored parameters across the paired bundle, in FP32 |
| **Download** | 1.74 GB for `model.safetensors`, plus `config.json`; training data is a separate download |
| **Runtime** | RFD4 Python package; Linux x86_64, Python 3.12, supported NVIDIA GPU and CUDA 13-compatible driver |
| **License** | [BSD 3-Clause](LICENSE) for the RFD4 model and weights; optional third-party assets have separate terms |

The bundle includes both model components. Use the RFD4 loader below; this is a native RFD4 bundle.

## Checkpoints in this release

The release is a **matched pair**: a flow model and the autoencoder it was trained against. They are not interchangeable across releases — the autoencoder defines the latent space the flow model generates in, and mixing a flow model with a different autoencoder produces nonsense rather than an error.

| | Current release (2026-10-19) | Previous release |
|---|---|---|
| Flow model | `rfd4-proteina-flow-release-2026-10-19`: the pretrained base (step 320000) with a rank-32 LoRA fine-tune merged in | `chk_epoch_00000169_step_000000340000-ema` |
| Autoencoder | `rfd4-proteina-ae-release-2026-10-19` | `2026_09_04_release_ae_z16_400k-ema` |
| Latent dimension | 32 | 16 |
| Residue vocabulary | 147 classes | 33 classes |
| Stored parameters | 435,622,465 | 434,348,737 |

The 2026-10-19 pair supersedes the 2026-10-15 pair (`2026_10_15_hero_s43_c512_80k-ema` and `2026_10_15_unified_ae_s43_400k-ema`), which has the same architecture. The pretrained base alone is in `base/`, and the LoRA adapter that turns it into the release model is in `adapter/` (PEFT format, rank 32 on `to_qkv` and `to_out_node`); the release bundle at the root is exactly the base plus the adapter, merged.

The current release's autoencoder is **unified**: one autoencoder covering proteins, nucleic acids and small molecules, with a 147-class residue vocabulary in place of the previous 33-class protein vocabulary, and a 32-dimensional latent in place of 16. This is the change that makes the two releases incompatible with each other's components.

| File | Use |
|---|---|
| [`config.json`](config.json) + `model.safetensors` | Recommended paired bundle for `Proteina.from_pretrained` |
| `base/` and `adapter/` | The pretrained base bundle and the PEFT adapter that makes it the release model (`adapter_path=` in the native runtime) |
| `flow_checkpoints/rfd4_proteina_flow-ema.ckpt` | Native Lightning flow EMA weights |
| `ae_checkpoints/rfd4_proteina_ae-ema.ckpt` | Matching native Lightning autoencoder EMA weights |
| [`release-checkpoints.json`](release-checkpoints.json) | Pair identity, stable aliases, source filenames, and SHA-256 checksums |
| [`provenance.json`](provenance.json) | Source archive and original checkpoint provenance |

The published `.ckpt` files carry **EMA weights and hyperparameters only**. The duplicate `SimpleEMA` shadow copy, optimizer, scheduler and loop state are removed, which is why they are 1.74 GB and 1.03 GB rather than 4.21 GB and 3.10 GB. Their weight tensors are bit-identical to the full training checkpoints, whose SHA-256 values are recorded in `release-checkpoints.json`. They initialize weights for inference or fine-tuning; **resuming an interrupted training run needs the full checkpoint**, which is not distributed here.

Stable filenames always select the current release; the dated training filename of each is recorded in `release-checkpoints.json`. Pin a Hub revision and verify the SHA-256 sidecars for exact identity. These EMA exports initialize weights; resuming optimizer and scheduler state requires a full training checkpoint.

## Start with one design

### 1. Install

Pick one route; the [quickstart](https://rfd4-proteina.org/latest/quickstart.html) covers all three in detail.

**GitHub** (recommended: the full workflow with annotated inputs, reward-guided search and refolding metrics):

```bash
git clone https://github.com/RosettaCommons/RFD4-Proteina.git
cd RFD4-Proteina
make setup
source .venv/bin/activate
```

**PyPI** (the model inside your own Python environment):

```bash
python3.12 -m venv .venv && source .venv/bin/activate
pip install --extra-index-url https://download.pytorch.org/whl/cu132 "rfd4-proteina[metrics-cuda13]"
```

**Diffusers:** see [Loading the model](#diffusers) below.

**Container images** (no build needed): prebuilt RFD4-Proteína runtime images for Linux x86_64 are in [`runtime/`](runtime), as Apptainer (`.sif`) and SquashFS for Enroot/Pyxis (`.sqsh`) files with SHA-256 sidecars. `cu13` (CUDA 13), `cu12` (CUDA 12) and `cpu` (no GPU; imports, CLI and CPU metrics only) variants exist, built from the public [Apptainer recipe](https://github.com/RosettaCommons/RFD4-Proteina/blob/main/apptainer/rfd4-proteina.def). They contain the code and its dependencies, not model weights or the AF2/AF3 oracles; pass `hf_ckpt_path=nvidia/RFD4-Proteina` and a writable `HF_HOME`.

```bash
hf download nvidia/RFD4-Proteina runtime/rfd4-proteina-cu13-amd64.sif runtime/rfd4-proteina-cu13-amd64.sif.sha256 --local-dir .
apptainer exec --nv runtime/rfd4-proteina-cu13-amd64.sif rfd4-generate hf_ckpt_path=nvidia/RFD4-Proteina inputs=in.cif out_dir=./runs
```

Setup caches the paired model bundle; downloads use `HF_HOME` when set. You do not need the training dataset for generation. If access to this repository is restricted, run `hf auth login` first. See [installation](https://rfd4-proteina.org/latest/installation.html) for hardware and build requirements.

### 2. Generate a small protein

From the checkout root (with the PyPI install, use the packaged example instead: `inputs=$(python -c "import rfproteina, pathlib; print(pathlib.Path(rfproteina.__file__).parent / 'data/benchmarks/monomer/monomer-short.cif')")`):

```bash
rfd4-generate inputs=data/benchmarks/monomer/monomer-short.cif \
  hf_ckpt_path=nvidia/RFD4-Proteina \
  hf_ckpt_revision=a06e2509c7033b010fc43614e9fd840303588502 \
  num_replicates=1 out_dir=./runs/first '~metrics' compile_lengths=null
```

Find the generated CIF under `runs/first/inference_samples/`. This first run disables external scoring and compilation to keep setup simple. For repeated runs, use the normal compiled configuration described in [running the model](https://rfd4-proteina.org/latest/how-to/run-the-model.html); compilation has an initial warmup cost.

### 3. Design a PD-L1 binder or an enzyme scaffold

```bash
hf download nvidia/RFD4-Proteina \
  --revision a06e2509c7033b010fc43614e9fd840303588502 \
  --local-dir ./rfd4-examples \
  examples/protein_binder/input.cif examples/enzyme_design/input.cif

rfd4-generate inputs=./rfd4-examples/examples/protein_binder/input.cif \
  hf_ckpt_path=nvidia/RFD4-Proteina \
  hf_ckpt_revision=a06e2509c7033b010fc43614e9fd840303588502 \
  num_replicates=1 out_dir=./runs/pdl1 '~metrics' compile_lengths=null
```

For enzyme motif scaffolding, replace the input with `./rfd4-examples/examples/enzyme_design/input.cif` and choose a new output directory. The annotations specify what to hold fixed and what to design; an ordinary, unannotated structure is not a complete design specification.

| Design goal | Start here |
|---|---|
| Protein–protein binder | [PD-L1 input](examples/protein_binder/input.cif) · [example output](examples/protein_binder/design.cif) |
| Enzyme motif scaffolding | [Enzyme input](examples/enzyme_design/input.cif) · [example output](examples/enzyme_design/design.cif) |
| Antibody design | [HER2 input](examples/antibody_design/input.cif) · [example output](examples/antibody_design/design.cif) |
| Unconditional monomer | [100-residue spec](examples/monomer.cif) — a length specification, no input coordinates |
| Prepare your own conditions | [Annotated CIFs and Python input preparation](https://rfd4-proteina.org/latest/how-to/input_prep/index.html) · [YAML specifications](https://rfd4-proteina.org/latest/how-to/input_prep/yaml-json.html) |
| Interactive design | [AtomWorks Studio](https://huggingface.co/spaces/nvidia/rfd4-proteina-space) on a dedicated GPU pool · [the same Studio on ZeroGPU](https://huggingface.co/spaces/nvidia/rfd4-proteina-zerogpu) if you would rather spend your own Hugging Face quota. Both screen every input and design with SecureDNA and refuse flagged requests. |

## Loading the model

### Native RFD4 (this repository)

Load the matched model and autoencoder once and reuse them across runs:

```python
from pathlib import Path
from huggingface_hub import hf_hub_download
from hydra import compose, initialize_config_dir
import rootutils
import rfproteina
from rfproteina.proteina import Proteina
from rfproteina.generate import run_generation

revision = "a06e2509c7033b010fc43614e9fd840303588502"
input_cif = hf_hub_download(
    "nvidia/RFD4-Proteina", "examples/enzyme_design/input.cif", revision=revision,
)
model = Proteina.from_pretrained("nvidia/RFD4-Proteina", revision=revision)
config_dir = rootutils.find_root(rfproteina.__file__, indicator=".project-root") / "configs"
with initialize_config_dir(config_dir=str(config_dir), version_base="1.3"):
    cfg = compose(config_name="inference", overrides=[
        f"inputs={input_cif}", "out_dir=./runs/enzyme",
        "num_replicates=1", "~metrics", "compile_lengths=null",
    ])
run_generation(cfg, model=model)
print(list(Path("runs/enzyme/inference_samples").rglob("*_generated.cif*")))
```

`from_pretrained` loads in evaluation mode on CPU by default; `run_generation` uses the native CUDA inference workflow. A local exported bundle directory also works as the model argument.

### Diffusers

```bash
# RFD4-Proteina was merged into Diffusers on 2026-10-20 and ships in the next release.
# Until that release, install Diffusers from git:
pip install git+https://github.com/huggingface/diffusers git+https://huggingface.co/nvidia/RFD4-Proteina-prep@c9959efdebd75ac7fe9129fbbf0e291a6e0487d5 accelerate

# Once the release is out, this is enough:
# pip install diffusers git+https://huggingface.co/nvidia/RFD4-Proteina-prep@c9959efdebd75ac7fe9129fbbf0e291a6e0487d5
```

```python
import torch
from diffusers import RFD4ProteinaPipeline
from rfd4_proteina_prep import prepare_cif, write_cif

pipe = RFD4ProteinaPipeline.from_pretrained("nvidia/RFD4-Proteina-Diffusers", dtype=torch.bfloat16).to("cuda:0")
features, atoms = prepare_cif("input.cif", seed=42, device=pipe.device)
required = ["padding_mask", "is_in_context_conditioning", "supports_local_latent", "token_type",
            "atom37_mask", "coords_nm"]
conditioning = {name: value for name, value in features.items() if name not in required}
output = pipe(
    padding_mask=features["padding_mask"],
    is_in_context_conditioning=features["is_in_context_conditioning"],
    supports_local_latent=features["supports_local_latent"],
    token_type=features["token_type"],
    atom37_mask=features["atom37_mask"],
    conditioning_features=conditioning,
    generator=torch.Generator("cuda:0").manual_seed(42),
)
write_cif(output, features, atoms, "design.cif")
```

This needs Diffusers installed from git, as shown above. Partial diffusion and inverse folding work in this port. See the [repository](https://huggingface.co/nvidia/RFD4-Proteina-Diffusers) for details.

### Compute presets

The released recipes differ only in how often the trunk is recycled per sampling step, as `(steps, recycle depth)` bands over 60 steps. `thinking_low|medium|high` are the front-loaded schedules, and the default is medium. The native runtime also has flat and mid-peak schedules for each budget; see the [running guide](https://rfd4-proteina.org/latest/how-to/run-the-model.html#recycling-schedules) for which one suits a task.

| Preset | Bands | Trunk passes |
|---|---|---:|
| Low | `[[10,4],[10,3],[10,2],[30,1]]` | 120 |
| **Medium (default)** | `[[5,6],[10,5],[5,4],[10,3],[20,2],[10,1]]` | **180** |
| High | `[[10,9],[10,8],[10,5],[20,3],[10,2]]` | 300 |

In the native runtime select one with `recycle_strategy=thinking_low|thinking_medium|thinking_high`.

## Hardware requirements

Tested and confirmed on the following NVIDIA GPUs. Linux x86_64, Python 3.12, and a CUDA 13-compatible driver are required.

| Architecture | Data center | Workstation and desktop |
|---|---|---|
| Blackwell | B200, B300, GB200, GB300, RTX PRO 6000 Blackwell Server Edition | RTX PRO 6000 Blackwell Workstation Edition, GB10 (DGX Spark) |
| Hopper | H100 SXM, H100 PCIe, H100 NVL, H200, H200 NVL, GH200 144GB | |
| Ada Lovelace | L40S | RTX 6000 Ada Generation |
| Ampere | A100 SXM4 40GB and 80GB, A100 PCIe 40GB and 80GB | |

Weights are 1.74 GB in FP32. Peak GPU memory depends on token count, batch size and recycle depth rather than on the weights; the quickstart above runs at batch size 1 with compilation disabled. Refolding and metrics need the selected oracle's own environment and weights, which are a separate download.

## Measured design efficiency

> **These numbers were measured on the previous release pair**, in the October 9, 2026 frozen project benchmark, which predates the current checkpoints. They have not been re-measured on the current release and should not be read as describing it.

The table uses one consistent high-thinking setting for RFD4 and the strongest non-RFD4 comparator in each family. **Metric:** mean per-target structurally distinct computational passers per GPU-hour, including generation and common AF3 evaluation. Higher is better.

| Benchmark | Targets | RFD4-Proteína, high thinking | Best other method in this comparison |
|---|---:|---:|---|
| Protein binders | 24 | **71.60** | Proteina-Complexa · 13.24 |
| Small-molecule binders | 77 | **112.25** | BoltzGen · 15.48 |
| Atomic Motif Enzyme | 37 | **91.18** | AlphaProtein-novo (Codesign) · 26.02 |
| DNA binders | 3 | **41.97** | BoltzGen (fixed DNA) · 9.46 |

There are 200 original attempts per target. Failed attempts consume time; setup, compilation, CPU scoring, and idle allocation time are excluded. Values are means of target-level rates, not pooled totals or single-design latency.

Conditioning differs between some methods: PPI uses RFD4 backbone conditioning versus all-atom conditioning for several baselines; DNA compares unfixed RFD4 inputs with fixed-DNA baselines; Proteina-Complexa's small-molecule route uses fixed ligands. Only three DNA targets are included. Computational passers do not establish experimental activity.

[Benchmark provenance](benchmarks/provenance.json) · [Full comparison table](benchmarks/summary.csv) · [Per-target source data](benchmarks/source_data.csv) · [Benchmark methods and pass criteria](benchmarks/METHODS.md)

## Training data and limitations

The companion [dataset card](https://huggingface.co/datasets/nvidia/RFD4-Proteina) describes the available training snapshot, component-specific filters, source terms, and loading format. Its upload date or proposed sampling mix should not be interpreted as the exact training history of every checkpoint.

Use the model for computational biomolecular design and follow designs with appropriate structural and experimental evaluation. Performance depends on the target, input annotations, sampling settings, and training coverage. Generation-only quickstarts omit external refolding and scoring; see [evaluation and metrics](https://rfd4-proteina.org/latest/how-to/evaluate-with-metrics.html) to add them.

<details>
<summary><strong>Other repository files</strong></summary>

**Third-party software and weights.** The BSD 3-Clause license covers the RFD4-Proteína model, weights and code only. The optional `alphafold2/runtime/` and `openfold3/runtime/` container images package third-party software (AlphaFold2- and AlphaFold3-derived code, OpenFold3 and their dependencies) that stays under its own upstream licenses, some of which restrict commercial use or redistribution. The ported OpenFold3 weights in `openfold3/weights/` are Apache-2.0 (see the provenance file). Review each upstream license before using the images, and do not assume the BSD license applies to them. Neither oracle is needed for generation.

Optional [AF3/OpenFold3 runtime images](openfold3/runtime) are available for Linux x86_64 with CUDA 12 or CUDA 13 in Apptainer (`.sif`), SquashFS (`.sqsh`) and Docker (`.docker.tar`) formats, with SHA-256 checksums. [OpenFold3 weights](openfold3/weights) are downloaded separately. These files are only needed for refolding and metrics; generation does not use them.

</details>

## License

The RFD4-Proteína model and weights are released under the [BSD 3-Clause License](LICENSE), Copyright (c) 2026, Institute for Protein Design, University of Washington. Optional third-party assets distributed alongside the model — the AlphaFold2 and OpenFold3/AlphaFold3 refolding images and the OpenFold3 payload — carry their own upstream terms; see the note under *Other repository files* and their provenance files. The training data has its own source terms, described on the [dataset card](https://huggingface.co/datasets/nvidia/RFD4-Proteina).

## Citation

When reporting results, cite the RFD4-Proteína project together with the exact model revision, code revision, seed, inputs and sampling configuration you used, plus any source datasets and evaluation tools.

```bibtex
@software{rfd4_proteina_2026,
  title  = {RFD4-Proteína: joint sequence and all-atom structure design},
  author = {{Baker Lab, Institute for Protein Design, University of Washington} and {NVIDIA GenAIR}},
  year   = {2026},
  url    = {https://huggingface.co/nvidia/RFD4-Proteina},
  note   = {Model revision a06e2509c7033b010fc43614e9fd840303588502}
}
```

## Attribution and support

Developed by the Baker Lab at the Institute for Protein Design, University of Washington, and NVIDIA GenAIR.

[Code and issues](https://github.com/RosettaCommons/RFD4-Proteina/issues) · [Model history](https://huggingface.co/nvidia/RFD4-Proteina/commits/main) · [License](LICENSE)
