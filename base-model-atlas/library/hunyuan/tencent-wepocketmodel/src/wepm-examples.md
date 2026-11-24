# WePM Inference Examples

The runnable examples are grouped by device. Each device directory contains generation, embedding, and structured-decision tasks.

```text
examples/
├── gpu/
│   ├── demo_data/
│   │   ├── images/
│   │   ├── generation/
│   │   └── decision/
│   ├── generation/
│   ├── embedding/
│   └── decision/
└── cpu/
    ├── demo_data/
    │   ├── images/
    │   ├── generation/
    │   └── decision/
    ├── generation/
    ├── embedding/
    └── decision/
```

Task directories contain only runnable shell scripts. All JSON requests and image inputs live under the device-specific `demo_data/` directory.

The generation examples cover all supported input layouts:

- `single_text`: one text item
- `single_image`: one image item
- `interleaved`: text → image → text → image → text

The original HEIC images are preserved byte-for-byte in each device's `demo_data/images/` directory. The inference dependencies include `pillow-heif` for decoding them.

## NVIDIA GPU

```bash
bash examples/gpu/generation/run.sh single_text
bash examples/gpu/generation/run.sh single_image
bash examples/gpu/generation/run.sh interleaved
bash examples/gpu/embedding/run.sh
bash examples/gpu/decision/run.sh
```

## CPU

```bash
bash examples/cpu/generation/run.sh single_text
bash examples/cpu/generation/run.sh single_image
bash examples/cpu/generation/run.sh interleaved
bash examples/cpu/embedding/run.sh
bash examples/cpu/decision/run.sh
```

The scripts default to `tencent/WePocketModel1.0-4B`. The first online run downloads the complete Hugging Face snapshot; later runs reuse cached files. See the [model table](../README.md#model-weights) for both formats.

To select the 2B Transformers model:

```bash
export WEPM_MODEL=tencent/WePocketModel1.0-2B
```

The shared runtime requires a compatible `task_slots_v1` checkpoint. The embedding examples explicitly request 1024 dimensions, which the chosen checkpoint must support.

For a pre-downloaded local model:

```bash
export WEPM_MODEL=/path/to/WePocketModel1.0-4B
```

Local model directories are loaded without network access. Set `HF_HUB_OFFLINE=1` to use only the existing Hub cache when `WEPM_MODEL` is a repository ID. Use the [inference CLI](../inference/README.md) for `--revision`, `--cache-dir`, and `--local-files-only`.

CPU examples also accept a local WePM GGUF bundle via `WEPM_MODEL` after [building the native library](../inference/README.md#gguf-on-cpu).

GPU selection, CPU threads, and output location can be controlled with `CUDA_VISIBLE_DEVICES`, `WEPM_THREADS`, and `WEPM_OUTPUT_DIR` respectively. Set `WEPM_MIN_FREE_GIB` to override the default CUDA loading threshold of checkpoint size plus 2 GiB. Results are written to timestamped JSON files under each task's `results/` directory by default.
