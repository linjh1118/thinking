# Invoker-Render deployment

This guide covers the native SGLang/SGLang-Omni deployment of **Invoker-Render**, the causal four-step streaming model of Code World Model 2.0: environment preparation, model assets, streaming sessions, file inference, and browser access. The default command line uses the `cwm` recipe and `production` deployment profile, and the service reports the model as `invoker-render`.

中文概述：本文说明 Invoker-Render（Code World Model 2.0 的因果四步流式模型）的环境、模型资产、流式服务、文件推理与浏览器部署。默认使用 `cwm` recipe 与 `production` 配置。运行时保留 H3 架构名及 `cwm_*` 字段，以兼容 checkpoint 与协议；项目介绍见[中文首页](../README.zh-CN.md)。

## Environment

Use a compatible Linux NVIDIA CUDA environment and Python 3.11 or 3.12. The production topology requires eight GPUs on one node. Memory capacity depends on the checkpoint and placement; the state reservation is not a minimum GPU-memory specification.

Provision the serving environment against the vendored [SGLang package manifest](../src/sglang/python/pyproject.toml) and [Omni package manifest](../src/sglang/projects/minimax_h3/frameworks/sglang-omni/pyproject.toml). These describe a multi-model runtime, not a minimal Invoker-Render-only installation. Preserve Omni's resolver overrides. In particular, do not combine incompatible `cache-dit` requirements from SGLang's optional diffusion extras and Omni, or bypass resolution with `--no-deps`.

There is no standalone minimal lockfile for this application. SGLang and Omni share dependencies with a broader multi-model runtime, so installing their extras independently can produce conflicting requirements. Resolve the target environment before deployment and verify the installed packages with the checks below. Editable builds must use the SGLang version required by Omni's manifest; this repository's Git revision is not an upstream package version.

Run the tools through `invoker_render.py` at the repository root so the vendored sources take precedence over unrelated installations. Each command forwards its options to a module under `src/sglang/projects/minimax_h3/tools/`:

| Command | Tool module |
| --- | --- |
| `prepare` | `prepare_omni_h3` |
| `serve` | `serve_omni_h3` |
| `infer` | `infer_omni_h3` |
| `web-adapter` | `serve_omni_h3_web` |
| `web` | `serve_web` |
| `check-env` | `check_omni_installed_requirements.py` |

```sh
PY=/path/to/serving-env/bin/python

"$PY" -m pip check
"$PY" invoker_render.py check-env
```

The checker reports dependency and platform conflicts, including explicitly handled compatibility exceptions. Resolve missing packages and unexpected conflicts in the serving environment; do not edit installed package metadata to hide them. Dependency checks do not establish CUDA-kernel or driver compatibility.

For CUDA 13 wheels, make the installed runtime/JIT libraries discoverable before worker startup:

```sh
NVIDIA_LIB=$("$PY" -c 'import sysconfig; print(sysconfig.get_paths()["purelib"] + "/nvidia")')
export LD_LIBRARY_PATH="${CUDA_COMPAT_LIB_DIR:+$CUDA_COMPAT_LIB_DIR:}$NVIDIA_LIB/cu13/lib:$NVIDIA_LIB/cudnn/lib:$NVIDIA_LIB/cusparselt/lib:$NVIDIA_LIB/nccl/lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
```

`CUDA_COMPAT_LIB_DIR`, if required, must point to a forward-compatibility library approved for the actual driver/GPU. Library paths do not make unsupported hardware compatible. The production decoder uses the vendored FA3 kernel; the explicit FA2 path instead requires a working `flash_attn_varlen_func` installation. CPU tests cannot establish CUDA-kernel compatibility.

## Model contract

- Frozen recipe: `configs/recipes/omni-h3-cwm.json`.
- Protocol: `cwm_causal/v1`; position policy: `cwm_frame_aligned_v1`.
- Four deterministic Euler steps, shift 12, on the fixed-history H3 stream: a nine-latent bootstrap, then five-latent chunks, with segment boundaries at latents 45 and 70.
- `sink_latents=1` and `recent_latents=12`: the first latent's proxy and clean video stay pinned as the attention sink next to the twelve most recent latents; proxy and clean history share one cache.
- A 47-latent RoPE reference controls long-stream static-position shifts. Proxy and target rows for the same frame share coordinates; the reference is not a proxy/target time offset. When the shift changes, the static prefix (text, first image, sink) is recomputed.
- First-image and proxy VAE encoding use the BF16 encoder and the posterior mean; no posterior noise is sampled.
- The proxy encoder defaults to full H3. An explicit TAE bundle can replace only proxy encoding with `--proxy-encoder tae --tae-weights PATH`; the static first image, CWM recipe, DiT and causal decoder remain on the existing path.
- The first image reaches Qwen as a single image.
- The proxy is uploaded on its original canvas (448×256 for the reference deployment) and resized once to 1344×768 before encoding, nearest-neighbour by default (`--cwm-proxy-resize`). No crop is introduced.
- The prompt is the frozen system prompt recorded in the artifact (`encoders.recipe.system_prompt`). File inference does not validate it; other prompts are outside the trained contract.

Load merged weights directly; do not apply training LoRA a second time. Keep the checkpoint's upstream architecture identifiers. The loader retains checkpoint-layout detection, FFN conversion and FP32 RoPE frequency reconstruction. CWM enables online AdaLN, first-denoise/history fusion and the lossless DiT norm by default; online AdaLN needs a native-layout checkpoint, so Diffusers-layout exports must be prepared with `--execution-config configs/runs/omni-h3-cwm-diffusers-execution.json` (same topology, `minimax_h3_adaln_online: false`).

## Deployment profiles

| Setting | `production` — default | `reference` — explicit | `overlap` — experimental |
| --- | --- | --- | --- |
| Recipe | `cwm` | Explicit recipe | Explicit recipe |
| Codec placement | E4 2/3/6/7; DTP4 0/1/4/5 | No separate groups | E4 2/3/6/7; DTP4 0/1/4/5 |
| Decoder | Fast causal | Reference | Fast causal |
| Spatial attention | FA3 | FA2 | FA3 |
| Suffix attention / compact KV | Default / off | Default / off | FA3 / on |
| Compile / CUDA Graph / fused post | Off | Off | On |
| Compile mode | Default | Default | max-autotune-no-cudagraphs |
| DiT norm (CWM / legacy) | Lossless / exact | Lossless / exact | Lossless |
| Online AdaLN / first-denoise fusion (CWM) | On | On | On |

The production CWM execution preset is `configs/runs/omni-h3-cwm-execution.json`: TP1/Ulysses8 on eight GPUs. Decoder TP4 is separate from DiT TP1. The `overlap` profile is not a synonym for the production codec-overlap feature: it additionally enables unvalidated compiler/Graph options.

Explicit CLI overrides remain available for deployment work and are not covered automatically by production acceptance. `--no-codec-parallel` clears implicit ranks and codec-dependent tuning; explicit contradictory ranks/options fail. `--no-decoder-compile` also clears implicit compiler mode and fused post. `--no-decoder-compact-suffix-kv` clears implicit FA3 suffix attention. Independent explicitly requested options are not silently discarded.

Legacy `longlive` and `continuous5` artifacts require `--deployment-profile reference` or `overlap` and retain their own fixed-v2 contracts. Do not combine those artifacts with the CWM model contract. The lower-level `prepare_native_bundle` API preserves its legacy default; the public CLI selects `cwm` and `production`.

## Prepare a bundle

Provide a matching frozen artifact, a complete merged checkpoint, encoder assets, causal decoder configuration/weights, and frozen stereo-silence tensors. Preparation hashes and references those files without copying or modifying model weights. The output directory must not already exist.

```sh
ARTIFACT=/assets/invoker-render/artifact.json
SILENCE=/assets/invoker-render/silence.safetensors
BUNDLE=/assets/invoker-render/bundle

"$PY" invoker_render.py prepare \
  --artifact "$ARTIFACT" --cwm-silence "$SILENCE" \
  --decoder-config /assets/causal-decoder/config.json \
  --decoder-weights /assets/causal-decoder/decoder.safetensors \
  --state-reservation-gib 48 --output "$BUNDLE"
```

This selects `--recipe cwm --deployment-profile production`. The 48 GiB state reservation is an example deployment budget; calibrate it for the workload. The resulting `native-runtime.json` records `model_name: invoker-render`, recipe, codec, placement, canvas, numerical policy and pinned assets.

To prepare an opt-in TAE proxy bundle, provide the released TAE checkpoint as an external asset. The prepare step records its path and digest in `native-runtime.json` and does not copy the checkpoint into the repository or bundle:

```sh
TAE=/assets/taeh3/taeh3_official.pth

"$PY" invoker_render.py prepare \
  --artifact "$ARTIFACT" --cwm-silence "$SILENCE" \
  --proxy-encoder tae --tae-weights "$TAE" \
  --decoder-config /assets/causal-decoder/config.json \
  --decoder-weights /assets/causal-decoder/decoder.safetensors \
  --state-reservation-gib 48 --output /assets/invoker-render/bundle-tae
```

The generated codec contains `encoder: tae` and `tae_weights`. Realtime loading places the encoder on the encoder-group leader, broadcasts its normalized 24-channel latents, and keeps H3 for the first image. Use a separate bundle when comparing H3 and TAE proxy conditioning.

Existing CWM artifacts and bundles that carry an earlier CWM recipe (re-noise sampling, five-latent bootstrap, sampled posterior) must be regenerated before reuse. Create a new artifact manifest with the current frozen recipe and `encoders.recipe.posterior` set to `mean`, preserving its weight/configuration paths, then prepare a new bundle. Do not modify historical output receipts to relabel earlier runs; changing the recipe does not regenerate cached session state, so start a new session with the new bundle.

## Serve and run files

```sh
"$PY" invoker_render.py serve --model-path "$BUNDLE" --port 18860
```

The service binds loopback. `/v1/models` reports the prepared model name. `/v1/session` provides the streaming session protocol. For the production bundle, manifest-driven defaults select realtime execution, codec overlap and independent CPU RGB delivery. `--verify-assets` explicitly rehashes all pinned files before startup.

Reference/shared-group bundles do not automatically enable codec overlap. `--no-codec-overlap` also defaults CPU delivery off; explicitly requesting CPU delivery still requires overlap. E4 is realtime-only.

File inputs must include a 1344×768 first image, an original-canvas 24 FPS proxy video matching the artifact, and a nonempty UTF-8 prompt. Input length is `17*N+5`, with at least 39 frames. Preserve EOS and frame provenance rather than padding or cropping the source arbitrarily.

```sh
"$PY" invoker_render.py infer \
  --model-path "$BUNDLE" --artifact "$ARTIFACT" \
  --uri ws://127.0.0.1:18860/v1/session \
  --first-image /inputs/first.png --proxy-video /inputs/proxy.mkv \
  --prompt-file /inputs/prompt.txt --seed 42 \
  --output-dir /outputs/invoker-render-001
```

The first chunks after a service start include decoder compilation and can take a few minutes with the default CWM bundle; later chunks run at streaming speed. `--timeout` (default 900 seconds) bounds each session step rather than the whole run.

Successful artifacts are `video.mp4` and `inference.json`. Check output-frame count, native EOS and close acknowledgement. Media FPS is not generation throughput. Matching seeds do not imply bitwise equality between live packet encoding and offline whole-video encoding; a local client receipt alone does not prove server-side checkpoint identity.

## Browser client

The native service is reused; the web adapter does not launch another DiT. Start the CPU media adapter, then the browser gateway in a second terminal:

```sh
"$PY" invoker_render.py web-adapter \
  --model-path "$BUNDLE" --artifact "$ARTIFACT" \
  --native-uri ws://127.0.0.1:18860/v1/session --port 18861

"$PY" invoker_render.py web \
  --backend http://127.0.0.1:18861 --port 18862 --incremental-proxy
```

Open `http://127.0.0.1:18862/`. Select a matching first image before generation. Stop and drain a session before changing scene. Browser recording and source-specific options are documented in the [client guide](../src/sglang/projects/minimax_h3/web/playable/README.md). External games and their assets are opt-in and are not bundled.

For remote access, configure `--public-url` and a private `--access-key-file` together, and terminate HTTPS at a trusted proxy. Do not expose unauthenticated loopback services directly. A running native endpoint does not by itself validate browser playback or source/game alignment.

## Timing and output verification

Native completion metadata uses the `native_worker_monotonic` clock and `proxy_prepare`, `render`, and `codec` stages, each with dispatch/completion timestamps and wall time. These are completion boundaries, not separately synchronized GPU-kernel profiles. Worker, server and browser clocks cannot be directly subtracted. Missing trace metadata remains valid for older producers, and splitting output packets does not create new compute samples.

For each deployment, check the returned model identity, asset hashes when requested, accepted and delivered frame counts, native EOS, and session close acknowledgement. Review the resulting video as well: valid transport and timestamps do not establish perceptual quality. Benchmark generation speed separately from the 24 FPS media timeline, especially when changing parallelism, decoder, compiler, or CUDA Graph settings.
