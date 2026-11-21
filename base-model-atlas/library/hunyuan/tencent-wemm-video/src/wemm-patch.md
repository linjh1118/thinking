# WeMM serving patches

Each version directory contains a source overlay and a manifest of SHA-256
hashes for its upstream and patched files. Choose one version per environment.

| Engine | Upstream release | PyTorch | Transformers | CUDA |
| --- | --- | --- | --- | --- |
| vLLM | [0.18.0](https://github.com/vllm-project/vllm/releases/tag/v0.18.0) | 2.10.0 | 5.2.0 | 12.9 |
| vLLM | [0.31.0](https://github.com/vllm-project/vllm/releases/tag/v0.31.0) | 2.13.0 | 5.12.1 | 12.9 |
| SGLang | [0.5.16](https://github.com/sgl-project/sglang/releases/tag/v0.5.16) | 2.11.0 | 5.12.1 | 12.9 |
| SGLang | [0.5.19](https://github.com/sgl-project/sglang/releases/tag/v0.5.19) | 2.13.0 | 5.12.1 | 12.9 |

## Install

The installer uses public packages from PyPI, PyTorch, GitHub, and NVIDIA.
It targets Linux x86_64 with glibc 2.35 or later, Python 3.12, and an NVIDIA
driver compatible with CUDA 12.9. Install FFmpeg with its shared libraries and
put `ffmpeg` and `ffprobe` on `PATH`. TorchCodec also needs CUDA 12 NPP on the
dynamic linker's search path.

SGLang builds CUDA kernels on first use. Install the CUDA 12.9 Toolkit, a C++
compiler, and Ninja. For a custom Toolkit location, set `CUDA_HOME` and put
`$CUDA_HOME/bin` on `PATH`.

```bash
python3.12 -m venv .venv-vllm
source .venv-vllm/bin/activate
bash patch/install.sh vllm 0.18.0
```

Use the engine and exact version from the table to select another profile.
The installer resolves the runtime dependencies and applies its overlay.
See the [serving guide](../docs/serving.md) for launching from a Hub ID.

### Manual install and patch

From the repository root, set `engine` and `version` to one pair from the table.
Install the dependencies in a dedicated Python 3.12 environment.

```bash
engine=vllm
version=0.18.0
profile="patch/$engine/$version"

python3.12 -m venv ".venv-$engine-$version"
source ".venv-$engine-$version/bin/activate"
python -m pip install --index-url https://pypi.org/simple uv==0.12.0
python -m uv --no-config pip install --python "$(command -v python)" \
  --default-index https://pypi.org/simple --index https://download.pytorch.org/whl/cu129 \
  --index-strategy unsafe-best-match --prerelease allow \
  --overrides "$profile/overrides.txt" -r "$profile/requirements.txt" -r patch/media.txt
```

Keep the same environment active for the patch step. If you already installed
the matching runtime yourself, set `engine` and `version` and start here.

```bash
python patch/apply.py "$engine" "$version" --dry-run
python patch/apply.py "$engine" "$version"
```

The dry run checks the installed engine version and source hashes. `apply.py`
only updates the overlay files. You can reapply the same overlay safely. Use a
fresh environment when switching engine versions.

If the host lacks CUDA 12 NPP (`libnppicc.so.12`), install it in the active
environment and add its library directory to the serving shell.

```bash
python -m pip install --index-url https://pypi.org/simple nvidia-npp-cu12==12.4.1.87
npp_lib=$(python -c 'from importlib.metadata import distribution; print(distribution("nvidia-npp-cu12").locate_file("nvidia/npp/lib"))')
export LD_LIBRARY_PATH="$npp_lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
```

Verify that the GPU and media decoders are available before starting the engine.

```bash
command -v ffmpeg && command -v ffprobe
python -c 'import torch; from torchcodec.decoders import AudioDecoder, VideoDecoder; assert torch.cuda.is_available()'
```

For the exact Docker package set, use `uv pip sync` with the profile's
`requirements.lock.txt` and the same package indexes. Before syncing the
vLLM 0.31.0 or SGLang 0.5.19 lock, install the compatible FlashAttention 2
and causal-conv1d wheels described in the
[Docker build notes](../docs/serving.md#docker-environments).

## Patch an upstream checkout

Pass `--target /path/to/upstream-checkout` to the same dry-run and apply
commands. Use the repository root for either engine. Install the patched
checkout with the upstream build instructions and the chosen profile's
dependencies. Use a fresh checkout when switching engine versions.
