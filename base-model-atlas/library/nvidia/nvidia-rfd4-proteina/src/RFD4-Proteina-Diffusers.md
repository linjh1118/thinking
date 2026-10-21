---
license: bsd-3-clause
library_name: diffusers
base_model: nvidia/RFD4-Proteina
language:
- en
tags:
- biology
- protein-design
- biomolecular-design
- structure-generation
- flow-matching
- annotated-cif
- diffusers
---
<p align="center"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/wordmark-dark.webp"><img src="assets/wordmark.webp" width="520" alt="RFD4-Proteína"></picture></p>
<p align="center"><strong>Sequence and structure, designed together.</strong><br>Baker Lab × NVIDIA GenAIR</p>
<p align="center"><a href="https://rfd4-proteina.org/">Project page</a> · <a href="https://huggingface.co/nvidia/RFD4-Proteina">Original release</a> · <a href="https://github.com/RosettaCommons/RFD4-Proteina">Code</a> · <a href="https://huggingface.co/datasets/nvidia/RFD4-Proteina">Training data</a> · <a href="https://huggingface.co/docs/diffusers/api/pipelines/rfd4_proteina">Diffusers docs</a></p>

# RFD4-Proteína for Diffusers

RFD4-Proteína is a flow-matching model for biomolecular design. It generates protein sequences and all-atom structures together, conditioned on the molecular context you want to preserve: a binding target, an enzyme motif, a ligand, or selected structural features.

This repository is the [Diffusers](https://github.com/huggingface/diffusers) release of the model: the same EMA weights as [`nvidia/RFD4-Proteina`](https://huggingface.co/nvidia/RFD4-Proteina), loaded with `RFD4ProteinaPipeline.from_pretrained()`. No native RFD4 package is needed at runtime.

<img src="assets/design-gallery.png" width="1050" alt="Examples from the project: nanobody complex, protein–DNA binder, RNA pseudoknot, ligand pocket, glycan complex, and protein assembly.">

<sub>Examples from the project, as shown on the [original model card](https://huggingface.co/nvidia/RFD4-Proteina).</sub>

> ### This release needs Diffusers from git until the next release
>
> These weights are the **2026-10-19 release**: a 147-class residue vocabulary and a 32-dimensional
> latent, produced by a LoRA fine-tune of the pretrained base that is merged into these weights.
> Support for them was merged into Diffusers on 2026-10-20 ([huggingface/diffusers#15088](https://github.com/huggingface/diffusers/pull/15088)) and ships in the next
> release; until then install Diffusers from GitHub, as in the Quickstart. An older Diffusers will fail to load this repository rather than sample it
> incorrectly.
>
> You also need the matching [`nvidia/RFD4-Proteina-prep`](https://huggingface.co/nvidia/RFD4-Proteina-prep),
> which supplies the chirality and element features this checkpoint's encoder requires.

## At a glance

| | Details |
|---|---|
| **Model** | Joint sequence–structure generation with a matched flow transformer and autoencoder |
| **Pipeline** | `RFD4ProteinaPipeline`: `transformer` + `vae` + a backbone and a local-latent `RFD4ProteinaScheduler` |
| **Inputs** | Annotated CIF structures, prepared with [`rfd4-proteina-prep`](https://huggingface.co/nvidia/RFD4-Proteina-prep) |
| **Outputs** | Atom37 coordinates and residue identities, written back to annotated CIF |
| **Weights** | EMA weights, 435.6 million parameters, stored in FP32 (1.74 GB); runs in BF16 |
| **Sampler** | Released `thinking_medium` recipe: 60 steps, 180 trunk passes |
| **Fine-tuning** | The release is a LoRA fine-tune of the pretrained base, merged into these weights. The base and the adapter (Diffusers LoRA format, `lora/`) are on the `pretrain-base` branch. |
| **Runtime** | `diffusers` and `rfd4-proteina-prep`; Python 3.11 or newer; a CUDA GPU is recommended |
| **License** | [BSD 3-Clause](LICENSE) for the RFD4 model and weights |

## Quickstart

```bash
# RFD4-Proteina was merged into Diffusers on 2026-10-20 and ships in the next release.
# Until that release, install Diffusers from git:
pip install git+https://github.com/huggingface/diffusers git+https://huggingface.co/nvidia/RFD4-Proteina-prep@c9959efdebd75ac7fe9129fbbf0e291a6e0487d5 accelerate

# Once the release is out, this is enough:
# pip install diffusers git+https://huggingface.co/nvidia/RFD4-Proteina-prep@c9959efdebd75ac7fe9129fbbf0e291a6e0487d5
```

```python
import torch
from huggingface_hub import hf_hub_download
from diffusers import RFD4ProteinaPipeline
from rfd4_proteina_prep import prepare_cif, write_cif

pipe = RFD4ProteinaPipeline.from_pretrained("nvidia/RFD4-Proteina-Diffusers", dtype=torch.bfloat16).to("cuda:0")

# An annotated CIF says what to hold fixed and what to design: here a PD-L1 target and a 50-120 residue binder.
input_cif = hf_hub_download("nvidia/RFD4-Proteina-Diffusers", "examples/protein_binder/input.cif")
features, atoms = prepare_cif(input_cif, seed=42, device=pipe.device)

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

`output.coords_nm` holds the generated atom37 coordinates in nanometers, with `output.residue_type`, `output.emit_mask` and `output.atom_mask` describing the designed residues. Pass one `torch.Generator` per design when generating a batch. See the [pipeline documentation](https://huggingface.co/docs/diffusers/api/pipelines/rfd4_proteina) for partial diffusion, inverse folding, callbacks, quantization and compilation.

## Examples

Each `examples/<name>/` folder holds the AtomWorks Studio input (`input.cif`), the design generated with this pipeline (`design.cif`) and a C-alpha preview (`design.png`). All designs use one sample, seed 42, BF16 and one NVIDIA H200. Left in each preview: the conditioning that was held fixed (grey, with ligand or motif atoms in red). Right: the generated design.

| Example | Task | Tokens |
|---|---|---:|
| [Protein binder · PD-L1](examples/protein_binder) | Fixed PD-L1 target with hotspots; designs a 50–120 residue binder | 171 |
| [Antibody · HER2 CDR H3](examples/antibody_design) | Fixed framework and target; redesigns CDR H3 | 280 |
| [VHH · PD-L1 CDRs](examples/nanobody) | Fixed VHH framework and target; redesigns the CDRs | 235 |
| [Enzyme · catalytic motif](examples/enzyme_design) | Scaffolds a catalytic motif of side-chain atoms | 193 |
| [Motif scaffolding · 1QJG](examples/motif_scaffolding) | Scaffolds an indexed motif | 79 |
| [Small-molecule binder · SAM](examples/small_molecule_binder) | Designs a pocket around a ligand | 177 |
| [Unconditional protein](examples/unconditional) | No conditioning: samples a protein | 250 |
| [Inverse folding · 2KL8](examples/inverse_folding) | Keeps the backbone and designs the sequence | 59 |
| [Partial diffusion · 2KL8](examples/partial_diffusion) | Re-designs 2KL8 from a noised start at the point where 40% of the schedule remains, running all 60 steps over that range | 59 |

<details>
<summary><strong>Preview gallery</strong></summary>

<img src="examples/protein_binder/design.png" alt="Protein binder, PD-L1" width="720"/>
<img src="examples/antibody_design/design.png" alt="Antibody, HER2 CDR H3" width="720"/>
<img src="examples/nanobody/design.png" alt="VHH, PD-L1 CDRs" width="720"/>
<img src="examples/enzyme_design/design.png" alt="Enzyme, catalytic motif" width="720"/>
<img src="examples/motif_scaffolding/design.png" alt="Motif scaffolding, 1QJG" width="720"/>
<img src="examples/small_molecule_binder/design.png" alt="Small-molecule binder, SAM" width="720"/>
<img src="examples/unconditional/design.png" alt="Unconditional protein" width="720"/>
<img src="examples/inverse_folding/design.png" alt="Inverse folding, 2KL8" width="720"/>
<img src="examples/partial_diffusion/design.png" alt="Partial diffusion, 2KL8" width="720"/>

</details>

These examples demonstrate the conditioning workflow. They are not experimental binding or catalytic-activity results, and example selection does not establish biological design quality. `examples/examples.json` lists the sampling task of each input. To reproduce one, download its `input.cif` from this repository and run it the way the Quickstart above does. The seven non-antibody inputs are also packaged in [`rfd4-proteina-prep`](https://huggingface.co/nvidia/RFD4-Proteina-prep), whose `examples/run_hub_examples.py` regenerates them against pinned model, prep and Diffusers revisions.

## Precision and speed

The pipeline runs the transformer and autoencoder in the dtype they are loaded in; the sampler state and feature embeddings stay in FP32. BF16 weights are recommended: on one H200 a 250-token design takes 5.0 s in BF16 and 14.1 s in FP32, and 2.8 s after regional compilation (`transformer.compile_repeated_blocks(fullgraph=True, dynamic=True)`, about 15 s of one-time warmup). Generating several designs of one input in one call amortizes the per-step overhead, which dominates small designs: per design, 64 tokens take 0.39 s at batch 8 (2.6 s alone), 128 tokens 1.1 s (2.7 s alone) and 250 tokens 4.0 s (5.0 s alone), in under 5 GB at batch 8.

Time and memory grow with the number of tokens. One BF16 design with the 60-step recipe on an H200:

| Tokens | Generation | Peak GPU memory |
| ---: | ---: | ---: |
| 64 | 2.7 s | 0.9 GB |
| 128 | 2.7 s | 1.0 GB |
| 256 | 5.1 s | 1.4 GB |
| 384 | 10.1 s | 2.0 GB |
| 512 | 17.6 s | 2.8 GB |
| 768 | 49.5 s | 5.2 GB |
| 1024 | 96.8 s | 8.6 GB |

Even 1024-token designs fit a 16 GB GPU. Preparing the input (about 0.1 s after the first call) and writing the CIF (0.4–1.9 s) are not bottlenecks.

The pair bias enters attention as an additive mask, so `set_attention_backend()` accepts only backends that take dense masks (`native`, `_native_cudnn`, `_native_efficient`, `_native_math`, `flex`); FlashAttention-style backends raise an error.

The same seed can end in a different design in BF16 and FP32, because the sampler amplifies rounding differences. The designs are statistically equivalent: over 24 seeds on each of four example inputs, the BF16 and FP32 distributions of radius of gyration, hydrophobic fraction, backbone geometry (C-alpha spacing and clashes) and helix content cannot be told apart (two-sample Kolmogorov–Smirnov p ≥ 0.07 in all 24 comparisons). Refolding-based success rates were not compared. Designs dominated by fixed conditioning (antibody, nanobody, motif scaffolding, inverse folding, partial diffusion) agree within 0.15 Å C-alpha RMSD between the two precisions; de-novo designs (binder, enzyme, small-molecule binder, unconditional) differ by 1–2.3 Å for the same seed.

## Repository contents

| Path | Use |
|---|---|
| `model_index.json` | Pipeline definition for `RFD4ProteinaPipeline.from_pretrained` |
| `transformer/`, `vae/` | Denoiser and autoencoder configs and safetensors weights |
| `bb_ca_scheduler/`, `local_latents_scheduler/` | `RFD4ProteinaScheduler` configs with the released sampler recipe (the recycle schedule is `recycle_depths` in `model_index.json`) |
| [`provenance.json`](provenance.json) | Source bundle hashes, sampler recipe and converter version |
| `examples/` | Studio inputs, generated designs and previews |

## Conversion and verification

The weights are converted from the original bundle with `scripts/convert_rfd4_proteina_to_diffusers.py` in the Diffusers repository. The fused query/key/value projections are split; every other tensor is unchanged, and the conversion fails on any missing or unexpected tensor. [`provenance.json`](provenance.json) records the SHA-256 of the source `model.safetensors` and `config.json`.

With FP32 weights, the Diffusers implementation and the original implementation agree to about 1e-7 relative error on the denoiser outputs (backbone, latents, sequence and insertion logits) and produce identical decoded coordinates and residues on the same inputs. To convert a future checkpoint, run the converter on its bundle and verify against the original code in the same way.

## Training data and limitations

The companion [dataset card](https://huggingface.co/datasets/nvidia/RFD4-Proteina) describes the available training snapshot. Use the model for computational biomolecular design and follow designs with appropriate structural and experimental evaluation. Performance depends on the target, input annotations, sampling settings and training coverage. Generation-only runs omit external refolding and scoring. See the [original model card](https://huggingface.co/nvidia/RFD4-Proteina) for benchmark results and the [evaluation and metrics guide](https://rfd4-proteina.org/latest/how-to/evaluate-with-metrics.html).

## Attribution and support

Developed by the Baker Lab at the Institute for Protein Design, University of Washington, and NVIDIA GenAIR. When reporting results, cite the RFD4-Proteína project, the exact model and code revisions, and any source datasets or evaluation tools used.

[Code and issues](https://github.com/RosettaCommons/RFD4-Proteina/issues) · [Original model](https://huggingface.co/nvidia/RFD4-Proteina) · [License](LICENSE)
