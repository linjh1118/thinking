#!/usr/bin/env python3
# SPDX-FileCopyrightText: Copyright (c) 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: OpenMDW-1.1

"""Run tennis point video inference with NVIDIA-NemotronLabs-AI-for-Media-Sports-Tennis on Hugging Face."""

from __future__ import annotations

import argparse
import importlib.util
import os
import shutil
import subprocess
import sys
import tempfile
import warnings
from contextlib import contextmanager
from pathlib import Path

os.environ.setdefault("OMP_NUM_THREADS", "1")

import torch
from huggingface_hub import snapshot_download
from transformers import AutoConfig, AutoModel, AutoProcessor
from transformers.video_utils import VideoMetadata

DEFAULT_REPO_ID = "nvidia/NVIDIA-NemotronLabs-AI-for-Media-Sports-Tennis"
DEFAULT_DEMO_VIDEO_REL = "media/full_tennis_point.mp4"
DEFAULT_QUESTION = (
    "What happened in this point? Provide a detailed caption. "
    '(Major - "Major" is the player in the white sleeveless tennis dress with a pleated skirt. '
    "She is wearing white shoes and has dark hair tied back in a ponytail.; "
    'Mustermann - "Mustermann" is the player in the black sleeveless top and black pleated skirt '
    "with white piping along the sides and hem. She is wearing white shoes and has blonde hair "
    "tied back in a ponytail. She is holding a green and black tennis racket with a red grip.)"
)
PROCESSOR_METADATA_KEYS = ("num_patches", "num_tokens", "imgs_sizes")


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-id", default=os.environ.get("HF_REPO_ID", DEFAULT_REPO_ID))
    parser.add_argument(
        "--video",
        help=(
            "Path to a tennis point clip (.mp4). Default: bundled "
            f"{DEFAULT_DEMO_VIDEO_REL} from the Hub snapshot after download."
        ),
    )
    parser.add_argument("--question", default=os.environ.get("QUESTION", DEFAULT_QUESTION))
    parser.add_argument("--video-fps", type=float, default=float(os.environ.get("VIDEO_FPS", "2.0")))
    parser.add_argument(
        "--max-video-frames",
        type=int,
        default=int(os.environ.get("MAX_VIDEO_FRAMES", "128")),
    )
    parser.add_argument(
        "--max-new-tokens",
        type=int,
        default=int(os.environ.get("MAX_NEW_TOKENS", "256")),
    )
    parser.add_argument("--enable-thinking", action="store_true")
    parser.add_argument("--no-audio", action="store_true")
    parser.add_argument("--extract-audio-wav", action="store_true")
    parser.add_argument(
        "--cache-dir",
        default=os.environ.get("HF_HOME") or os.environ.get("HF_HUB_CACHE"),
    )
    parser.add_argument(
        "--download-only",
        action="store_true",
        help="Download weights to the local HF cache and exit",
    )
    parser.add_argument(
        "--local-files-only",
        action="store_true",
        help="Use cached weights only (skip Hub network access)",
    )
    parser.add_argument(
        "--revision",
        default=os.environ.get("HF_REPO_REVISION"),
        help="Optional Hub commit to pin custom modeling code",
    )
    return parser


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    return build_arg_parser().parse_args(argv)


def trim_generated_ids(input_ids: torch.Tensor, generated_ids: torch.Tensor) -> list[torch.Tensor]:
    if hasattr(generated_ids, "sequences"):
        generated_ids = generated_ids.sequences
    if generated_ids.dim() == 1:
        return [generated_ids[input_ids.shape[-1] :]]
    if input_ids.dim() == 1:
        input_ids = input_ids.unsqueeze(0)
    return [out_ids[len(in_ids) :] for in_ids, out_ids in zip(input_ids, generated_ids)]


def import_checkpoint_video_io(snapshot_dir: str):
    video_io_path = Path(snapshot_dir) / "video_io.py"
    if not video_io_path.is_file():
        raise FileNotFoundError(f"checkpoint video_io.py not found under {snapshot_dir}")
    module_name = f"checkpoint_video_io_{abs(hash(snapshot_dir))}"
    spec = importlib.util.spec_from_file_location(module_name, video_io_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"failed to load {video_io_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_video_frames(checkpoint_video_io, video_path: str, fps: int, max_video_frames: int):
    if not os.path.isfile(video_path):
        raise FileNotFoundError(f"Video not found: {video_path}")

    frame_urls, metadata = checkpoint_video_io.sample_video_frames_to_data_urls(
        video_path,
        fps=fps,
        nframe_max=max_video_frames,
    )
    frames = [checkpoint_video_io.pil_image_from_base64(url) for url in frame_urls]
    metadata = VideoMetadata(
        total_num_frames=metadata.total_num_frames,
        fps=metadata.fps,
        frames_indices=metadata.frames_indices,
    )
    return frames, metadata


def ffmpeg_executable() -> str:
    ffmpeg = shutil.which("ffmpeg")
    if ffmpeg:
        return ffmpeg
    try:
        import imageio_ffmpeg
    except ImportError as exc:
        raise RuntimeError(
            "Audio from video requires ffmpeg. Install imageio-ffmpeg or add ffmpeg to PATH, "
            "or pass --no-audio."
        ) from exc
    return imageio_ffmpeg.get_ffmpeg_exe()


def video_has_audio_stream(video_path: str) -> bool:
    ffprobe = shutil.which("ffprobe")
    if ffprobe:
        proc = subprocess.run(
            [
                ffprobe,
                "-v",
                "error",
                "-select_streams",
                "a",
                "-show_entries",
                "stream=index",
                "-of",
                "csv=p=0",
                video_path,
            ],
            capture_output=True,
            text=True,
        )
        if proc.returncode == 0:
            return bool(proc.stdout.strip())
    ffmpeg = shutil.which("ffmpeg") or ffmpeg_executable()
    probe = subprocess.run(
        [ffmpeg, "-hide_banner", "-i", video_path],
        capture_output=True,
        text=True,
    )
    stderr = probe.stderr or ""
    return any(line.strip().startswith("Stream") and " Audio:" in line for line in stderr.splitlines())


def ensure_ffmpeg_on_path() -> None:
    ffmpeg = shutil.which("ffmpeg")
    if ffmpeg:
        return
    try:
        import imageio_ffmpeg
    except ImportError:
        return
    bindir = os.path.join(os.environ.get("CACHE_DIR", "/tmp"), "bin")
    os.makedirs(bindir, exist_ok=True)
    link = os.path.join(bindir, "ffmpeg")
    if not os.path.exists(link):
        os.symlink(imageio_ffmpeg.get_ffmpeg_exe(), link)
    os.environ["PATH"] = f"{bindir}{os.pathsep}{os.environ.get('PATH', '')}"


@contextmanager
def extracted_audio_wav(video_path: str, sampling_rate: int = 16000):
    ffmpeg = ffmpeg_executable()
    tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    tmp.close()
    try:
        subprocess.run(
            [
                ffmpeg,
                "-nostdin",
                "-y",
                "-i",
                video_path,
                "-vn",
                "-acodec",
                "pcm_s16le",
                "-ar",
                str(sampling_rate),
                "-ac",
                "1",
                tmp.name,
            ],
            check=True,
            capture_output=True,
        )
    except subprocess.CalledProcessError as exc:
        os.unlink(tmp.name)
        stderr = exc.stderr.decode("utf-8", errors="replace") if exc.stderr else ""
        raise RuntimeError(f"Failed to extract audio from {video_path}.\n{stderr}") from exc
    try:
        yield tmp.name
    finally:
        os.unlink(tmp.name)


def resolve_video_path(video_arg: str | None, snapshot_dir: str) -> str:
    if video_arg:
        return video_arg
    demo_path = Path(snapshot_dir) / DEFAULT_DEMO_VIDEO_REL
    if demo_path.is_file():
        return str(demo_path)
    raise SystemExit(
        "error: --video is required unless the Hub repo includes "
        f"{DEFAULT_DEMO_VIDEO_REL} (not found under {snapshot_dir})"
    )


def resolve_snapshot_dir(repo_id, cache_dir, revision, local_files_only) -> str:
    revision_label = revision or "latest"
    print(f"[video_inference] Resolving snapshot for {repo_id} @ {revision_label} ...")
    kwargs = {
        "repo_id": repo_id,
        "repo_type": "model",
        "cache_dir": cache_dir,
        "local_files_only": local_files_only,
    }
    if revision:
        kwargs["revision"] = revision
    path = snapshot_download(**kwargs)
    print(f"[video_inference] Model snapshot: {path}")
    return path


def load_model_and_processor(repo_id, cache_dir, revision, local_files_only):
    load_kwargs = {
        "trust_remote_code": True,
        "cache_dir": cache_dir,
        "local_files_only": local_files_only,
    }
    if revision:
        load_kwargs["revision"] = revision

    print(f"[video_inference] Loading processor and model from {repo_id} ...")
    processor = AutoProcessor.from_pretrained(repo_id, **load_kwargs)
    config = AutoConfig.from_pretrained(repo_id, **load_kwargs)
    config.video_pruning_rate = 0.0
    model = AutoModel.from_pretrained(
        repo_id,
        config=config,
        torch_dtype=torch.bfloat16,
        device_map={"": 0} if torch.cuda.is_available() else None,
        low_cpu_mem_usage=True,
        **load_kwargs,
    )
    if hasattr(model, "vision_model") and hasattr(model.vision_model, "radio_model"):
        model.vision_model.radio_model.summary_idxs = None
    model.eval()
    return model, processor


def run_inference(
    model,
    processor,
    checkpoint_video_io,
    video_path,
    question,
    video_fps,
    max_video_frames,
    max_new_tokens,
    enable_thinking,
    include_audio,
    extract_audio_wav,
) -> str:
    frames, video_metadata = load_video_frames(
        checkpoint_video_io,
        video_path,
        fps=max(0, int(video_fps)),
        max_video_frames=max_video_frames,
    )
    print(f"[video_inference] Sampled {len(frames)} frame(s) from {video_path}")

    use_audio = include_audio
    if include_audio and not video_has_audio_stream(video_path):
        print(f"[video_inference] No audio stream in {video_path}; running video-only inference.")
        use_audio = False

    media = processor.video_token
    if use_audio:
        media = f"{media}\n{processor.audio_token}\n"
    prompt = processor.tokenizer.apply_chat_template(
        [{"role": "user", "content": f"{media}{question}"}],
        tokenize=False,
        add_generation_prompt=True,
        enable_thinking=enable_thinking,
    )

    processor_kwargs = {
        "text": [prompt],
        "videos": frames,
        "return_tensors": "pt",
        "do_sample_frames": False,
        "videos_kwargs": {"video_metadata": video_metadata},
    }
    audio_sampling_rate = 16000
    if use_audio:
        processor_kwargs["audio_kwargs"] = {"sampling_rate": audio_sampling_rate}
        if extract_audio_wav:
            with extracted_audio_wav(video_path, sampling_rate=audio_sampling_rate) as wav:
                processor_kwargs["audio"] = [wav]
                inputs = processor(**processor_kwargs)
        else:
            processor_kwargs["audio"] = [video_path]
            try:
                inputs = processor(**processor_kwargs)
            except Exception as exc:
                print(f"[video_inference] Direct MP4 audio failed ({exc}); extracting WAV with ffmpeg")
                with extracted_audio_wav(video_path, sampling_rate=audio_sampling_rate) as wav:
                    processor_kwargs["audio"] = [wav]
                    inputs = processor(**processor_kwargs)
    else:
        inputs = processor(**processor_kwargs)

    for key in PROCESSOR_METADATA_KEYS:
        inputs.pop(key, None)

    device = next(model.parameters()).device
    inputs = {k: v.to(device) if isinstance(v, torch.Tensor) else v for k, v in inputs.items()}

    with torch.no_grad():
        generated_ids = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=False,
            output_hidden_states=False,
        )
    trimmed = trim_generated_ids(inputs["input_ids"], generated_ids)
    return processor.batch_decode(
        trimmed,
        skip_special_tokens=True,
        clean_up_tokenization_spaces=False,
    )[0].strip()


def execute(args: argparse.Namespace, *, print_answer: bool = True) -> tuple[int, str | None]:
    cache_dir = os.path.abspath(args.cache_dir) if args.cache_dir else None
    if cache_dir:
        os.makedirs(cache_dir, exist_ok=True)
        os.environ.setdefault("HF_HOME", cache_dir)
        print(f"[video_inference] Using cache directory: {cache_dir}")

    snapshot_dir = resolve_snapshot_dir(
        args.repo_id, cache_dir, args.revision, args.local_files_only
    )

    if args.download_only:
        print("[video_inference] Download complete.")
        return 0, None

    video_path = resolve_video_path(args.video, snapshot_dir)
    if not args.video:
        print(f"[video_inference] Using bundled demo video: {video_path}")

    checkpoint_video_io = import_checkpoint_video_io(snapshot_dir)
    model, processor = load_model_and_processor(
        args.repo_id, cache_dir, args.revision, args.local_files_only
    )
    if not args.no_audio and not args.extract_audio_wav:
        ensure_ffmpeg_on_path()

    answer = run_inference(
        model=model,
        processor=processor,
        checkpoint_video_io=checkpoint_video_io,
        video_path=video_path,
        question=args.question,
        video_fps=args.video_fps,
        max_video_frames=args.max_video_frames,
        max_new_tokens=args.max_new_tokens,
        enable_thinking=args.enable_thinking,
        include_audio=not args.no_audio,
        extract_audio_wav=args.extract_audio_wav,
    )
    if print_answer:
        print(answer)
    return 0, answer


def main(argv: list[str] | None = None) -> int:
    warnings.filterwarnings("ignore", message="PySoundFile failed", category=UserWarning)
    os.environ.setdefault("MKL_NUM_THREADS", "1")
    rc, _ = execute(parse_args(argv))
    return rc


if __name__ == "__main__":
    sys.exit(main())
