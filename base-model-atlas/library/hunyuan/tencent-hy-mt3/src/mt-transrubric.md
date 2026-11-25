# TransRubric: Rubric-Based Automatic Evaluation for Translation

English | [中文](README_zh.md)

TransRubric is a rubric-based LLM-as-a-judge evaluation method for fine-grained and interpretable translation quality assessment. Given a translation task, a candidate translation, and a task-specific rubric, a TransRubric judge identifies concrete issues with their error categories and severity levels, and produces a pointwise translation quality score on a 0–100 scale.

This repository releases resources for applying TransRubric: sample-specific rubrics for four test sets derived from FLORES-200, WMT26 GenMT, and HardMTBench, prompt templates for constructing translation rubrics, and the pointwise translation judge prompt. The source texts, references, instructions, and benchmark-specific metadata come from the corresponding upstream benchmarks; the sample-specific `rubric` field is the added evaluation resource.

## Released Rubric Resources

| File | Upstream benchmark | Coverage | Directions / pairs | Samples |
| --- | --- | --- | --- | ---: |
| `testsets/flores200_33langs_rubric.jsonl` | FLORES-200 | 33 languages | 1,056 directions | 106,656 |
| `testsets/flores200_low_resource_rubric.jsonl` | FLORES-200 | 64 additional lower-resource languages paired with Chinese or English | 256 directions | 25,856 |
| `testsets/wmt26_genmt_rubric.jsonl` | WMT26 GenMT | 20 language pairs | 20 pairs | 4,303 |
| `testsets/hardmtbench_rubric.jsonl` | HardMTBench | 12 knowledge-intensive domains, Chinese and English | 2 directions | 20,000 |

The WMT26 GenMT subset excludes English-to-Ligurian, English-to-Ladin, and English-to-Northern-Sami.

## Data Format

Each JSONL record follows the same top-level schema:

| Field | Type | Description |
| --- | --- | --- |
| `id` | string | Unique sample identifier. WMT26 IDs are inherited from `doc_id`; FLORES IDs are generated from record order in the released files. |
| `benchmark` | string | Upstream benchmark: `flores200`, `wmt26`, or `hardmtbench`. |
| `subset` | string | Benchmark subset: `33langs`, `low_resource`, `genmt`, or `full`. |
| `source_language` | string | Source-language name or code retained from the upstream data. |
| `target_language` | string | Target-language name or code retained from the upstream data. |
| `source_text` | string | Source text to translate. |
| `task_prompt` | string | Complete translation task prompt. |
| `reference` | string or null | Upstream reference translation, when available. |
| `reference_type` | string or null | Reference type supplied by the upstream data, such as `human`, `synthetic`, or `none`. |
| `rubric` | list[string] | Sample-specific evaluation criteria added by TransRubric. |
| `meta` | object | Benchmark-specific upstream metadata. |

Language identifiers retain the representation used by each upstream benchmark. FLORES uses language names in Chinese, WMT26 uses language-script codes, and HardMTBench uses `Chinese` and `English`.

For HardMTBench, `meta` retains the upstream `pair_id`, translation direction, domain and sub-domain, domain keywords, bilingual terminology, and difficulty scores. The released file excludes rubric-construction candidates and model-generation artifacts such as `response_list` and `model_res`.

Example:

```json
{
  "id": "flores200_33langs_000001",
  "benchmark": "flores200",
  "subset": "33langs",
  "source_language": "中文",
  "target_language": "英语",
  "source_text": "他们通常会提供特别的食品、饮料和娱乐活动，让客人保持愉悦，留在赌场。",
  "task_prompt": "将以下文本翻译为英语，注意只需要输出翻译后的结果，不要额外解释：\n他们通常会提供特别的食品、饮料和娱乐活动，让客人保持愉悦，留在赌场。",
  "reference": "They usually have special food, drink and entertainment offers, to keep guests in a good mood, and keep them at the premise.",
  "reference_type": null,
  "rubric": [
    "指令遵循：输出必须仅为英文译文，不包含解释或其他多余内容。",
    "语义完整：译文须覆盖原文的核心信息，不得漏译或增译关键信息。",
    "逻辑关系：须准确表达提供食品、饮料和娱乐活动是为了让客人保持愉悦并继续留在赌场，不得弱化或颠倒该目的关系。",
    "行为主体：须明确留在赌场的是客人，不得因代词或句法结构不当而误解为提供服务的一方留在赌场。"
  ],
  "meta": {
    "l1": "wikivoyage",
    "l2": "英语",
    "l3": "中文",
    "l4": "travel",
    "class": "中文-英语-wikivoyage"
  }
}
```

## Rubric Construction Prompts

[`transrubric_prompts.py`](transrubric_prompts.py) provides the complete prompt templates for a three-stage rubric construction workflow:

1. `RUBRIC_DRAFT_PROMPT` generates an initial source-grounded rubric.
2. `RUBRIC_DELTA_PROMPT` identifies missing discriminative criteria from unlabeled candidate translations.
3. `RUBRIC_MERGE_PROMPT` conservatively merges valid new criteria into the rubric.

The corresponding message builders are:

```python
build_rubric_draft_messages(...)
build_rubric_delta_messages(...)
build_rubric_merge_messages(...)
```

Rubric items are written in Simplified Chinese and are intended to be concrete, verifiable checks rather than rigid reference translations.

## Translation Judge Prompt

`TRANSLATION_JUDGE_PROMPT` performs pointwise evaluation of one candidate translation against the translation task and its sample-specific rubric. It returns structured issues, an overall summary, a confidence value, and a translation quality score from 0 to 100.

The helper below only constructs model messages; users may pass the returned messages to their preferred multilingual model or inference framework.

```python
import json

from transrubric_prompts import build_translation_evaluation_messages

with open(
    "testsets/flores200_33langs_rubric.jsonl",
    encoding="utf-8",
) as f:
    sample = json.loads(next(f))

messages = build_translation_evaluation_messages(
    task_prompt=sample["task_prompt"],
    candidate_response="Candidate translation",
    rubric=sample["rubric"],
    response_id=sample["id"],
)
```

The rubric is a verification checklist, not a reference answer or evidence that an error exists. Equivalent and natural translations should be accepted.

## Project Structure

```text
TransRubric/
├── README.md
├── README_zh.md
├── transrubric_prompts.py
└── testsets/
    ├── flores200_33langs_rubric.jsonl
    ├── flores200_low_resource_rubric.jsonl
    ├── wmt26_genmt_rubric.jsonl
    └── hardmtbench_rubric.jsonl
```

## Data Sources

The test data is derived from the open-source FLORES-200, WMT26 GenMT, and HardMTBench benchmarks. The released files retain their source texts, references, instructions, and benchmark-specific metadata, while adding sample-specific rubrics and a unified release schema.

- [FLORES-200](https://github.com/facebookresearch/flores)
- [WMT26 General Machine Translation Shared Task](https://github.com/wmt-conference/wmt26-general-mt)
- [HardMTBench](https://github.com/jasonNLP/HardMTBench)

## References

If you use a TransRubric test set, please also cite its corresponding upstream benchmark:

- NLLB Team et al. (2022). *No Language Left Behind: Scaling Human-Centered Machine Translation*.
- Kocmi et al. (2026). *Findings of the WMT26 General Machine Translation Shared Task: Contrastive Dynamic Human Evaluation at Scale*.
- Li, Z., Zheng, M., Song, M., and Fei, T. (2026). [*HardMTBench: Stress-Testing Chinese-English Translation on Knowledge-Intensive Domains*](https://aclanthology.org/2026.findings-emnlp.235/). In *Findings of the Association for Computational Linguistics: EMNLP 2026*, pages 4947–4957, Budapest, Hungary. Association for Computational Linguistics.
