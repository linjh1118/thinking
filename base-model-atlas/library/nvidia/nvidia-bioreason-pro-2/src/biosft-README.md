---
license: other
license_name: openmdw-1.1
license_link: https://openmdw.ai/license/1.1/
base_model: Qwen/Qwen3.5-9B
datasets:
- wanglab/bioreason-pro-v2
language:
- en
tags:
- biology
- protein-function-prediction
- gene-ontology
- bionemo
---

# BioReason-Pro 2 SFT

This repository holds the BioReason-Pro 2 SFT checkpoint, licensed under the [OpenMDW License Agreement, version 1.1](LICENSE). Third-party material in this repository and the components the code downloads separately are listed in [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md). The code is at [NVIDIA-BioNeMo/BioReason-Pro-2](https://github.com/NVIDIA-BioNeMo/BioReason-Pro-2) (MIT).

This project is currently not accepting contributions.

See the [GitHub repository](https://github.com/NVIDIA-BioNeMo/BioReason-Pro-2) for instructions on running inference, evaluation and training.

---

# Model Overview

### Description:
BioReason-Pro 2 predicts a protein's function from its sequence and biological context, writing a reasoning trace, a function summary and Gene Ontology (GO) terms. BioReason-Pro 2 was developed by NVIDIA as a part of the BioReason-Pro model family (NVIDIA BioNeMo). See the [GitHub repository](https://github.com/NVIDIA-BioNeMo/BioReason-Pro-2) for installation, quick start and usage.

This card covers two checkpoints:

| Checkpoint | Training |
|---|---|
| [BioReason-Pro 2 SFT](https://huggingface.co/nvidia/BioReason-Pro-2-9B-SFT) | Supervised fine-tuning (SFT) on 272,688 reasoning traces |
| [BioReason-Pro 2 RL](https://huggingface.co/nvidia/BioReason-Pro-2-9B-RL) | The SFT checkpoint plus reinforcement learning (RL) with Group Relative Policy Optimization (GRPO) |

This is an initial research release: its outputs are hypotheses for expert review and experimental validation, not verified annotations.

This model is ready for commercial or non-commercial use.

### License/Terms of Use:
GOVERNING TERMS: This model is governed by the [OpenMDW License Agreement, version 1.1 (OpenMDW-1.1)](https://openmdw.ai/license/1.1/).

ADDITIONAL INFORMATION: The language model backbone, [Qwen3.5-9B](https://huggingface.co/Qwen/Qwen3.5-9B), is licensed under the [Apache License 2.0](https://huggingface.co/Qwen/Qwen3.5-9B/blob/main/LICENSE). The protein encoder, [ESM3 open small (biohub/esm3-sm-open-v1)](https://huggingface.co/biohub/esm3-sm-open-v1), is licensed under the MIT License; it is not included in the released checkpoints and is downloaded separately. The code that trains, runs and evaluates the model is licensed under the [MIT License](https://github.com/NVIDIA-BioNeMo/BioReason-Pro-2/blob/main/LICENSE), with third-party material listed in [THIRD_PARTY_NOTICES.md](https://github.com/NVIDIA-BioNeMo/BioReason-Pro-2/blob/main/THIRD_PARTY_NOTICES.md). The training data come from the Wang Lab corpus, [wanglab/bioreason-pro-v2](https://huggingface.co/datasets/wanglab/bioreason-pro-v2), licensed under [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/); see the [GitHub repository](https://github.com/NVIDIA-BioNeMo/BioReason-Pro-2) for details.

### Deployment Geography:
Global

### Use Case:
Life-science researchers and developers, such as computational biologists and protein scientists. Expected uses:
- Annotating poorly characterized proteins with GO terms and a rationale.
- Generating hypotheses to guide experiments.
- Triaging large protein sets.
- Research on protein function prediction.

The model is not intended for clinical, diagnostic or patient-care decisions.

### Release Date:
Hugging Face 11/24/2026 via https://huggingface.co/nvidia/BioReason-Pro-2-9B-SFT <br>
Hugging Face 11/24/2026 via https://huggingface.co/nvidia/BioReason-Pro-2-9B-RL <br>
GitHub 11/24/2026 via https://github.com/NVIDIA-BioNeMo/BioReason-Pro-2

## References(s):
- Code: [NVIDIA-BioNeMo/BioReason-Pro-2](https://github.com/NVIDIA-BioNeMo/BioReason-Pro-2)
- Wang Lab corpus: [wanglab/bioreason-pro-v2](https://huggingface.co/datasets/wanglab/bioreason-pro-v2)
- Paper: a paper describing BioReason-Pro 2 is in preparation; this card will link it when it is available.
- Qwen3.5-9B: [Qwen/Qwen3.5-9B](https://huggingface.co/Qwen/Qwen3.5-9B)
- ESM3 open small: [biohub/esm3-sm-open-v1](https://huggingface.co/biohub/esm3-sm-open-v1)
- GO-GPT: [wanglab/gogpt-v2](https://huggingface.co/wanglab/gogpt-v2)
- GRPO: Shao, Z. et al. (2024), [arXiv:2402.03300](https://arxiv.org/abs/2402.03300); trainer: [SkyRL](https://github.com/NovaSky-AI/SkyRL)

## Model Architecture:
**Architecture Type:** Transformer

**Network Architecture:** Other: a multimodal protein-language model with four parts:
- Qwen3.5-9B decoder, fine-tuned with Low-Rank Adaptation (LoRA) and merged.
- ESM3 open small protein encoder, frozen; not included in the checkpoint and downloaded separately.
- NVIDIA-trained protein projector.
- NVIDIA-trained GO graph encoder and projector.

**This model was developed based on:** Qwen3.5-9B and ESM3 open small.

**Number of model parameters:** 9.1*10^9 in the released checkpoint; the frozen ESM3 open small encoder (1.4*10^9) is downloaded separately.

## Input(s):
**Input Type(s):** Text, Other: Protein sequence, Other: Protein structure (optional)

**Input Format(s):**
- Protein sequence: String (one-letter amino-acid codes)
- Text: String (organism and GO term predictions from GO-GPT; optionally, the protein's InterProScan results and known interaction partners)
- Protein structure: Protein Data Bank (PDB) or mmCIF file (optional)

**Input Parameters:**
- Protein sequence: One-Dimensional (1D)
- Text: One-Dimensional (1D)
- Protein structure: Three-Dimensional (3D) atomic coordinates

**Other Properties Related to Input:** Up to 2,000 residues per protein; longer sequences are truncated. Text context window: 16,384 tokens.

## Output(s)

**Output Type(s):** Text

**Output Format(s):**
- Text: String

**Output Parameters:**
- Text: One-Dimensional (1D)

**Other Properties Related to Output:** A reasoning trace, then a function summary, InterPro entries, GO terms and interaction partners (up to 8,000 tokens). No sequences or structures are generated.

Our AI models are designed and/or optimized to run on NVIDIA GPU-accelerated systems. By leveraging NVIDIA’s hardware (e.g. GPU cores) and software frameworks (e.g., CUDA libraries), the model achieves faster training and inference times compared to CPU-only solutions.

## Software Integration:
**Runtime Engine(s):**
* Not Applicable (N/A); runs with PyTorch, Transformers and vLLM.

**Supported Hardware Microarchitecture Compatibility:**
* NVIDIA Hopper (H100 80 GB)

Inference needs one 80 GB GPU. SFT ran on four 8-GPU H100 nodes and RL on one 8-GPU H100 node.

**Supported Operating System(s):**
* Linux

The integration of foundation and fine-tuned models into AI systems requires additional testing using use-case-specific data to ensure safe and effective deployment. Following the V-model methodology, iterative testing and validation at both unit and system levels are essential to mitigate risks, meet technical and functional requirements, and ensure compliance with safety and ethical standards before deployment.

## Model Version(s):
- BioReason-Pro 2 SFT (`nvidia/BioReason-Pro-2-9B-SFT`), 9B.
- BioReason-Pro 2 RL (`nvidia/BioReason-Pro-2-9B-RL`), 9B.

To integrate the model into an AI system, install the `bioreason2` Python package from the [GitHub repository](https://github.com/NVIDIA-BioNeMo/BioReason-Pro-2) and call it as a library, or run its prediction script, which serves the model with vLLM on one GPU and writes results to a file.

## Training, Testing, and Evaluation Datasets:

### Dataset Overview
**Total Size:** 278,800 protein records: 272,688 train (about 2% held out as validation) and 6,112 test. <br>
**Total Number of Datasets:** 1, built from the [Wang Lab corpus](https://huggingface.co/datasets/wanglab/bioreason-pro-v2) and not publicly released; see the [GitHub repository](https://github.com/NVIDIA-BioNeMo/BioReason-Pro-2) for the splits.

**Dataset partition:** Training 96%, Testing 2%, Validation 2% <br>
**Time period for training data collection:** Public database releases (Gene Ontology 2023-01-01, UniProtKB 2026_02); traces generated August–September 2026. <br>
**Time period for testing data collection:** Same as training. <br>
**Time period for validation data collection:** Same as training.

## Training Dataset:

### Data Modality:
* Text
* Other: Protein sequences
* Other: Protein structures
* Other: Gene Ontology graph

### Training Data Size: 
**Text Training Data Size:**
* Less than a Billion Tokens

**Non-Audio, Image, Text Training Data Size:**
* Less than a Million Protein Sequences (272,688)
* Less than a Million Protein Structures (one per protein where available)
* Less than a Million Graphs (one Gene Ontology graph, release 2023-01-01)

**Data Collection Method by dataset:**
* Hybrid: Automated, Synthetic

**Labeling Method by dataset:**
* Hybrid: Manually-Labeled, Automated, Synthetic

**Properties:** 272,688 protein records (about 2% held out as validation). Modalities: protein sequences, optional 3D structures and text. Nature of content: public scientific data from protein databases plus synthetic (model-written) reasoning traces; no personal data. Linguistic characteristics: English.

### Testing Dataset:

Data Collection Method by dataset:
* Hybrid: Automated, Synthetic

Labeling Method by dataset:
* Hybrid: Manually-Labeled, Automated, Synthetic

**Properties:** 6,112 protein records, none shared with the training split. Modalities: protein sequences, optional 3D structures and text. Nature of content: public scientific data from protein databases plus synthetic (model-written) reasoning traces; no personal data. Linguistic characteristics: English.

### Evaluation Dataset:

**Benchmark Score:** See the table below.

Data Collection Method by dataset:
* Hybrid: Automated, Synthetic

Labeling Method by dataset:
* Hybrid: Manually-Labeled, Automated

**Properties:** The 6,112-protein test split: protein sequences, optional 3D structures and text. Nature of content: public scientific data from protein databases with curated GO labels; no personal data. Linguistic characteristics: English. GO metrics use CAFA (Critical Assessment of Functional Annotation) evaluation software on all 6,112 proteins. The LLM judge (NVIDIA Nemotron 3.5 Super VL) scores answers from 1 to 10 on five axes, on a fixed 1,000-protein sample.

Overall test-set scores, without / with InterProScan results in the input:

| Metric | SFT | RL |
|---|---|---|
| LLM judge, mean of 5 axes | 7.24 / 7.72 | 7.74 / 8.43 |
| LLM judge, molecular function | 7.61 / 8.05 | 8.05 / 8.60 |
| LLM judge, biological process | 7.12 / 7.51 | 7.37 / 8.06 |
| LLM judge, cellular component | 8.13 / 8.37 | 8.39 / 8.71 |
| LLM judge, specificity | 9.41 / 9.62 | 9.53 / 9.82 |
| LLM judge, reliability | 3.92 / 5.06 | 5.34 / 6.97 |
| Fmax | 0.629 / 0.640 | 0.662 / 0.667 |

## Inference: 
**Acceleration (Engine used to optimize the runtime if applicable) Engine:** [vLLM 0.27.1](https://github.com/vllm-project/vllm) <br>
**Test Hardware Set-Up (GPU Architecture, Model):**
* NVIDIA Hopper H100 80 GB
* Minimum: one NVIDIA GPU with 80 GB of memory

## Ethical Considerations:
NVIDIA believes Trustworthy AI is a shared responsibility and we have established policies and practices to enable development for a wide array of AI applications.  Developers should work with their internal model team to ensure this model meets requirements for the relevant industry and use case and addresses unforeseen product misuse.

For more detailed information on ethical considerations for this model, please see the Model Card++ [Bias](./bias.md), [Explainability](./explainability.md), [Safety & Security](./safety.md), and [Privacy](./privacy.md) Subcards.

Users are responsible for ensuring the model's outputs are appropriately evaluated and comply with applicable safety regulations and ethical standards.

Users are responsible for model inputs and outputs. Users are responsible for ensuring safe integration of this model, including implementing guardrails as well as other safety mechanisms, prior to deployment.

Please report model quality, risk, security vulnerabilities or NVIDIA AI Concerns [here](https://www.nvidia.com/en-us/support/submit-security-vulnerability/).

## Citation

```bibtex
@article{nainani2026biologicalreasoning,
  author = {Nainani, Jatin and Fallahpour, Adibvafa and Srinivasan, Savitha and Choi, Benedict and Seyed-Ahmadi, Arman and Pearce, Michael and Bigelow, Eric and Idehpour, Parsa and Wilber, Jared and St. John, Peter and St. John, John and Wang, Bo and Jain, Archa and Rvachov, Timur and Goodarzi, Hani and Wang, Nicholas},
  title = {Building stronger biological reasoning models},
  journal = {Goodfire Research},
  year = {2026},
  url = {https://www.goodfire.com/research/building-stronger-biological-reasoning-models}
}

@article{Fallahpour2026.03.19.712954,
  author = {Fallahpour, Adibvafa and Seyed-Ahmadi, Arman and Idehpour, Parsa and Ibrahim, Omar and Gupta, Purav and Naimer, Jack and Zhu, Kevin and Shah, Arnav and Ma, Shihao and Adduri, Abhinav and G{\"u}loglu, Talu and Liu, Nuo and Cui, Haotian and Jain, Arihant and de Castro, Max and Fallahpour, Amirfaham and Cembellin-Prieto, Antonio and Stiles, John S. and Nem{\v c}ko, Filip and Nevue, Alexander A. and Moon, Hyungseok C. and Sosnick, Lucas and Markham, Olivia and Duan, Haonan and Lee, Michelle Y. Y. and Salvador, Andrea F. M. and Maddison, Chris J. and Thaiss, Christoph A. and Ricci-Tam, Chiara and Plosky, Brian S. and Burke, Dave P. and Hsu, Patrick D. and Goodarzi, Hani and Wang, Bo},
  title = {BioReason-Pro: Advancing Protein Function Prediction with Multimodal Biological Reasoning},
  elocation-id = {2026.03.19.712954},
  year = {2026},
  doi = {10.64898/2026.03.19.712954},
  publisher = {Cold Spring Harbor Laboratory},
  URL = {https://www.biorxiv.org/content/early/2026/03/20/2026.03.19.712954},
  eprint = {https://www.biorxiv.org/content/early/2026/03/20/2026.03.19.712954.full.pdf},
  journal = {bioRxiv}
}
```
