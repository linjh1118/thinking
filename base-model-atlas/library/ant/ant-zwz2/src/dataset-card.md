---
language:
- en
task_categories:
- visual-question-answering
size_categories:
- 10K<n<100K
tags:
- zwz2
- multimodal
- visual-reasoning
- synthetic-data
- reinforcement-learning
- grpo
---

# ZwZ2-RL-VQA

<!-- Replace PAPER_URL with the final v2 paper URL. -->
<p align="center">
  📃 <a href="https://arxiv.org/pdf/2610.37037">Paper</a> | 🏠 <a href="https://github.com/inclusionAI/Zooming-without-Zooming-v2">Project</a> | 🤗 <a href="https://huggingface.co/collections/inclusionAI/zooming-without-zooming-v2">Collection</a>
</p>

## ✨ Dataset Summary

**ZwZ2-RL-VQA** is the training dataset of **Zooming-without-Zooming-v2 (ZwZ2)**. It contains **20,662 multiple-choice visual questions** for connecting evidence across image regions and supports the reinforcement-learning stage of **ZwZ2-4B, ZwZ2-9B, and ZwZ2-27B**.

Built with **EvidenceConnect**, the dataset goes beyond recognizing isolated objects or attributes. Questions require locating relevant facts, binding them to the right entities, and combining them through comparison, aggregation, matching, or multi-step reasoning. Privileged zoomed views assist question construction and verification; the training policy receives a **full-image view with colored region outlines**, not the privileged crop layout.

The images originate from **SA-1B**. Questions and multiple-choice annotations are synthetically constructed and automatically checked. This is a training resource for reinforcement learning with verifiable rewards (**RLVR**), not a held-out evaluation benchmark or a collection of human-written reasoning traces.

## 📋 At a Glance

| Property | Description |
|---|---|
| Training examples | 20,662 |
| Input per example | One full-image policy view and one English question |
| Question format | Four options, A–D |
| Reference answer | One option letter |
| Image source | SA-1B |
| Data format | Parquet with nested prompt and reward fields |
| Training use | Rule-based answer rewards, including GRPO |
| Model family | ZwZ2-4B / ZwZ2-9B / ZwZ2-27B |

The count refers to question–image records, not necessarily distinct underlying SA-1B photographs. Different questions can refer to the same original photograph with different region annotations. The separate full-image-only synthesis ablation is not included in this dataset description.

## ⚙️ Data Construction

1. **Select visual evidence.** Identify related regions in visually rich images and form groups of 3–7 regions that can support a compositional question.
2. **Generate with privileged views.** Use zoomed region layouts to construct questions requiring evidence from multiple regions.
3. **Check answers and dependencies.** Use independent VLM answer agreement and drop-one region tests to assess reference-answer reliability and dependence on the selected visual evidence.
4. **Construct multiple-choice tasks.** Convert verified questions into four-option questions with a rule-verifiable correct letter.
5. **Export full-image policy inputs.** Pair each question with the corresponding full image and colored region outlines, retaining the prompt, reference letter, and training metadata.

The distinction between **synthesis views** and **policy inputs** is important: privileged crops are a data-construction tool, not additional observations that must be supplied to the trained model at inference time.

## 🗂️ Data Format

The training Parquet uses the following schema:

| Field | Type | Meaning |
|---|---|---|
| `images` | List of strings | One image-file reference per record; the image bytes are not embedded in this field. |
| `data_source` | String | Source identifier used by the training pipeline. |
| `prompt` | List of `{role, content}` | One user message containing an `<image>` marker, the question, four options, and an answer instruction. |
| `ability` | String | Existing task/category metadata; see the note below. |
| `reward_model` | `{ground_truth, style}` | `ground_truth` is `A`, `B`, `C`, or `D`; `style` is `rule`. |
| `extra_info` | `{answer, question}` | A copy of the reference letter and complete question text for bookkeeping. |

The source identifiers are `syn_sa1b` (**18,292 records**) and `multi_region_vqa` (**2,370 records**). The `ability` field retains the original export labels. In particular, `position-qa` is a coarse legacy label for the 18,292 `syn_sa1b` records; it should **not** be interpreted as an audited semantic classification of every question. Other labels include conditional localization, multi-object counting, attribute comparison, cross-region OCR, and multi-hop reasoning.

### 📝 Example

The following question and answer come from the training data. The image reference is replaced with an illustrative relative filename; this code block alone is not a complete visual sample.

```json
{
  "images": ["images/example_marked_original.png"],
  "data_source": "multi_region_vqa",
  "prompt": [
    {
      "role": "user",
      "content": "<image>Based on the visual characteristics of the vessels in the purple box and the orange box, which one has a flat roof?\n\nA. both vessels\nB. purple box\nC. neither vessel\nD. orange box\n\nAnswer with the option letter."
    }
  ],
  "ability": "conditional_localization",
  "reward_model": {"ground_truth": "B", "style": "rule"},
  "extra_info": {
    "answer": "B",
    "question": "<image>Based on the visual characteristics of the vessels in the purple box and the orange box, which one has a flat roof?\n\nA. both vessels\nB. purple box\nC. neither vessel\nD. orange box\n\nAnswer with the option letter."
  }
}
```

## 🚀 Getting Started

Install the reader:

```bash
pip install datasets pyarrow
export DATASET_FILE="/path/to/downloaded/train.parquet"
```

```python
import os
from datasets import load_dataset

train = load_dataset(
    "parquet",
    data_files={"train": os.environ["DATASET_FILE"]},
    split="train",
)

example = train[0]
print("Examples:", len(train))
print(example["prompt"][0]["content"])
print("Reference:", example["reward_model"]["ground_truth"])
print("Image reference:", example["images"][0])
```

This loads the annotations, **not the referenced images**. Resolve image references against the downloaded image assets before training. Relative paths need an explicit dataset root; paths from another machine are not portable. Preserve the corresponding marked full-image view: replacing it with an unmarked photograph can invalidate questions referring to colored boxes. See the [Hugging Face loading guide](https://huggingface.co/docs/datasets/loading) for Parquet loading options.

## 💬 Prompt and Answer Format

The Parquet prompt asks for an option letter. The **ZwZ2 model chat template** supplies the final-answer convention:

```text
<answer>B</answer>
```

The stored reference is the bare letter `B`, **not** the string `<answer>B</answer>`. The training reward adapter must extract the option from the model response before comparing it with `reward_model.ground_truth`.

- Preserve the question, option order, correct letter, and region-color references together.
- Use the packaged model chat template and the intended non-thinking setting when reproducing ZwZ2 training or inference. A custom system message can replace the template's default answer-format instruction.
- Treat the Parquet's `<image>` as a placeholder for the training loader. When converting to structured multimodal chat messages, let the processor insert the image tokens instead of duplicating them.
- A missing or malformed answer must not silently become a correct prediction. Preserve the chosen reward parser's treatment of multiple or conflicting answer tags.

## 🔍 Quality and Scope

Structural checks on the source training export confirm that all 20,662 records have one image reference, one user prompt, and a valid A–D reference letter. The reference letter agrees with `extra_info.answer`, and the user content agrees with `extra_info.question` throughout the export. The reference-letter distribution is **A: 5,177; B: 4,998; C: 5,184; D: 5,303**.

These checks establish format consistency, not perfect visual correctness. Synthetic labels may still contain ambiguity or errors, and model-agreement checks can share failure modes. Colored outlines can affect visual interpretation. Source-image and synthesis-model biases may also carry into the data.

Use the dataset for multimodal training and controlled research comparisons. Do not report performance on these training examples as held-out generalization. If creating validation or test partitions, group records by the underlying source image to avoid splitting variants of the same photograph across partitions.

## 🤗 Models and Data

| Release | Description |
|---|---|
| [ZwZ2-4B](https://huggingface.co/inclusionAI/ZwZ2-4B) | Based on Qwen3.5-4B |
| [ZwZ2-9B](https://huggingface.co/inclusionAI/ZwZ2-9B) | Based on Qwen3.5-9B |
| [ZwZ2-27B](https://huggingface.co/inclusionAI/ZwZ2-27B) | Based on Qwen3.6-27B |
| [ZwZ2-RL-VQA](https://huggingface.co/datasets/inclusionAI/ZwZ2-RL-VQA) | Shared training dataset |

The [project repository](https://github.com/inclusionAI/Zooming-without-Zooming-v2) contains the data synthesis, GRPO training, and 25-benchmark evaluation workflows. See its `data_synthesis/` and `verl/` instructions to generate data or train a model.

## 📄 Source Images and Usage Terms

SA-1B images remain subject to their upstream terms. The [official SA-1B dataset page](https://ai.meta.com/datasets/segment-anything/) describes its research use and limited data license. Synthetic question annotations do not remove those image restrictions or grant blanket permission to redistribute the source images.

Consult the license accompanying the released annotations and the applicable source-image terms before use or redistribution.

## 🔗 Related Work

This dataset belongs to **Zooming-without-Zooming-v2 (ZwZ2)** and is distinct from the first-generation ZwZ-RL-VQA dataset.

**First-generation ZwZ:** [Paper](https://huggingface.co/papers/2602.11858) · [Code](https://github.com/inclusionAI/Zooming-without-Zooming)
