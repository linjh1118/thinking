---
tags:
  - autonomous-driving
  - reward-model
  - text-classification
  - vision-language
---

# AlpaJudge

AlpaJudge is a family of learned judges for evaluating autonomous-driving reasoning. This
repository provides one reference-based checkpoint and one reference-free checkpoint.

### License/Terms of Use:

**Model weights:** The model weights are released under the [OpenMDW-1.1](https://openmdw.ai/license/1-1/) license.

**Source code:** Apache License 2.0, as provided in the [AlpaJudge GitHub repository](https://github.com/NVlabs/alpajudge).

## Checkpoints

| Variant | Folder | Inputs | Output |
| --- | --- | --- | --- |
| AlpaJudge-RB | [`reference-based/`](./reference-based) | Question, reference answer, and candidate answer; no images | One alignment probability in `[0, 1]` |
| AlpaJudge-RF | [`reference-free/`](./reference-free) | Front-wide/front-tele frames, ego meta-action history and future, and a candidate rationale | Five rubric probabilities plus the aggregated action, component, and overall scores |

Both variants are available from
[`nvidia/alpajudge`](https://huggingface.co/nvidia/alpajudge) in the subfolders shown above.

## Download

Authenticate with an account that can access the repository, then download only the variant you
need:

```python
from pathlib import Path

from huggingface_hub import snapshot_download

variant = "reference-based"  # or "reference-free"
repo_dir = Path(
    snapshot_download(
        "nvidia/alpajudge",
        allow_patterns=f"{variant}/*",
    )
)
checkpoint = repo_dir / variant
```

Use the `alpajudge` inference package to load either subfolder. See the
[usage guide](https://github.com/NVlabs/alpajudge#readme) for setup, complete RB and RF examples,
input contracts, score definitions, and limitations.
