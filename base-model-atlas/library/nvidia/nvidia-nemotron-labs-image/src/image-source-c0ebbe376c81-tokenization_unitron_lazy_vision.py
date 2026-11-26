# Copyright (c) 2026, NVIDIA CORPORATION.  All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Lazy Unitron visual-token wrapper.

The model checkpoint has embedding rows for dense Unitron visual IDs, but the
HF tokenizer should not materialize every ``<|vis_i|>`` as an added token.
This wrapper keeps text tokenization delegated to the base tokenizer and maps
Unitron visual/framing token strings to IDs by formula from
``unitron_extension_manifest.json``.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import time
from pathlib import Path
from typing import Any

try:
    from transformers import BatchEncoding
except Exception:  # pragma: no cover - import is validated in the container env.
    BatchEncoding = dict


_UNITRON_TOKEN_RE = re.compile(
    r"(<\|img_start\|>|<\|img_end\|>|<\|vis_row\|>|"
    r"<\|vid_start\|>|<\|vid_end\|>|<\|aud_start\|>|<\|aud_end\|>|"
    r"<\|vis_\d+\|>|<\|aud_\d+\|>)"
)


def _is_unitron_token(token: str) -> bool:
    if token in {
        "<|img_start|>",
        "<|img_end|>",
        "<|vis_row|>",
        "<|vid_start|>",
        "<|vid_end|>",
        "<|aud_start|>",
        "<|aud_end|>",
    }:
        return True
    return (
        (token.startswith("<|vis_") or token.startswith("<|aud_"))
        and token.endswith("|>")
    )


def _load_manifest(path: Path) -> dict[str, Any]:
    manifest_path = path / "unitron_extension_manifest.json"
    if not manifest_path.is_file():
        raise FileNotFoundError(f"missing {manifest_path}")
    with manifest_path.open() as f:
        manifest = json.load(f)
    if "unitron_token_ranges" in manifest:
        return manifest

    # Backward-compatible derivation for older materialized checkpoints.
    base = int(manifest["base_vocab_size"])
    framing = list(manifest.get("framing_tokens") or [])
    n_vision = int(manifest.get("n_vision", 0))
    n_audio = int(manifest.get("n_audio", 0))
    ranges: dict[str, Any] = {
        "framing": {tok: base + i for i, tok in enumerate(framing)}
    }
    cursor = base + len(framing)
    ranges["vision"] = {
        "token_format": "<|vis_{i}|>",
        "start_id": cursor,
        "end_id": cursor + n_vision,
        "count": n_vision,
    }
    cursor += n_vision
    if n_audio:
        ranges["audio"] = {
            "token_format": "<|aud_{i}|>",
            "start_id": cursor,
            "end_id": cursor + n_audio,
            "count": n_audio,
        }
    manifest["unitron_token_ranges"] = ranges
    return manifest


def _strip_unitron_tokens_from_config(data: dict[str, Any]) -> dict[str, Any]:
    data = dict(data)
    data.pop("auto_map", None)
    extra = data.get("extra_special_tokens")
    if isinstance(extra, list):
        data["extra_special_tokens"] = [
            tok for tok in extra if not (isinstance(tok, str) and _is_unitron_token(tok))
        ]
    for key in ("additional_special_tokens",):
        value = data.get(key)
        if isinstance(value, list):
            data[key] = [
                tok for tok in value if not (isinstance(tok, str) and _is_unitron_token(tok))
            ]
    return data


def _write_slim_tokenizer_dir(src: Path, dst: Path) -> None:
    dst.mkdir(parents=True, exist_ok=True)
    for name in (
        "special_tokens_map.json",
        "chat_template.jinja",
        "vocab.json",
        "merges.txt",
        "spiece.model",
        "tokenizer.model",
        "added_tokens.json",
    ):
        src_file = src / name
        if src_file.is_file():
            shutil.copy2(src_file, dst / name)

    cfg_path = src / "tokenizer_config.json"
    if cfg_path.is_file():
        with cfg_path.open() as f:
            cfg = json.load(f)
        with (dst / "tokenizer_config.json").open("w") as f:
            json.dump(_strip_unitron_tokens_from_config(cfg), f, indent=2, ensure_ascii=False)
            f.write("\n")

    tok_path = src / "tokenizer.json"
    if tok_path.is_file():
        with tok_path.open() as f:
            tok = json.load(f)
        added = tok.get("added_tokens")
        if isinstance(added, list):
            tok["added_tokens"] = [
                item for item in added
                if not _is_unitron_token(str(item.get("content", "")))
            ]
        with (dst / "tokenizer.json").open("w") as f:
            json.dump(tok, f, ensure_ascii=False)

    manifest_path = src / "unitron_extension_manifest.json"
    if manifest_path.is_file():
        shutil.copy2(manifest_path, dst / "unitron_extension_manifest.json")


def _slim_cache_dir(src: Path) -> Path:
    cache_root = Path(
        os.environ.get(
            "UNITRON_SLIM_TOKENIZER_CACHE",
            os.path.join(os.environ.get("HF_HOME", str(Path.home() / ".cache" / "huggingface")), "unitron_slim_tokenizers"),
        )
    )
    key = hashlib.sha1(str(src.resolve()).encode("utf-8")).hexdigest()[:16]
    return cache_root / key


def _ensure_slim_tokenizer_dir(src: Path) -> Path:
    manifest = _load_manifest(src)
    if manifest.get("tokenizer_mode") == "virtual":
        return src

    dst = _slim_cache_dir(src)
    ready = dst / ".ready"
    if ready.is_file():
        return dst

    lock = dst.with_suffix(".lock")
    lock.parent.mkdir(parents=True, exist_ok=True)
    while True:
        try:
            os.mkdir(lock)
            break
        except FileExistsError:
            if ready.is_file():
                return dst
            time.sleep(0.5)
    try:
        if not ready.is_file():
            tmp = dst.with_suffix(".tmp")
            if tmp.exists():
                shutil.rmtree(tmp)
            _write_slim_tokenizer_dir(src, tmp)
            if dst.exists():
                shutil.rmtree(dst)
            os.replace(tmp, dst)
            ready.write_text("ok\n")
    finally:
        try:
            os.rmdir(lock)
        except OSError:
            pass
    return dst


class UnitronLazyVisionTokenizer:
    """Tokenizer wrapper with formula-based Unitron visual IDs."""

    @classmethod
    def register_for_auto_class(cls, *_args: Any, **_kwargs: Any) -> None:
        """Compatibility hook called by transformers dynamic-module loading."""
        return None

    def __init__(self, base_tokenizer: Any, manifest: dict[str, Any]) -> None:
        self.base_tokenizer = base_tokenizer
        self.manifest = manifest
        ranges = manifest["unitron_token_ranges"]
        self._framing_ids: dict[str, int] = {
            str(k): int(v) for k, v in (ranges.get("framing") or {}).items()
        }
        vision = ranges["vision"]
        self._vis_start = int(vision["start_id"])
        self._vis_end = int(vision["end_id"])
        audio = ranges.get("audio") or {}
        self._aud_start = int(audio["start_id"]) if audio else None
        self._aud_end = int(audio["end_id"]) if audio else None
        self.unitron_visual_range = (
            min([self._vis_start, *self._framing_ids.values()]),
            self._vis_end,
        )
        self.unitron_token_ranges = ranges
        self._model_vocab_size = int(
            manifest.get("embedding_rows")
            or manifest.get("model_vocab_size")
            or self._vis_end
        )

    @classmethod
    def from_pretrained(
        cls,
        pretrained_model_name_or_path: str,
        *args: Any,
        pad_token: str | None = None,
        trust_remote_code: bool | None = None,
        **kwargs: Any,
    ) -> "UnitronLazyVisionTokenizer":
        from transformers import AutoTokenizer

        src = Path(pretrained_model_name_or_path)
        if not src.is_dir():
            raise ValueError("UnitronLazyVisionTokenizer requires a local checkpoint path")
        manifest = _load_manifest(src)
        tokenizer_dir = _ensure_slim_tokenizer_dir(src)
        tokenizer_kwargs = dict(kwargs)
        tokenizer_kwargs.pop("trust_remote_code", None)
        # The outer AutoTokenizer call may reach this class via tokenizer_config
        # auto_map. Loading the delegated base tokenizer from the same directory
        # with trust_remote_code=True would recursively instantiate this wrapper.
        tokenizer_kwargs["trust_remote_code"] = False
        base = AutoTokenizer.from_pretrained(str(tokenizer_dir), *args, **tokenizer_kwargs)
        if pad_token is not None:
            base.pad_token = pad_token
        return cls(base, manifest)

    def _unitron_token_to_id(self, token: str) -> int | None:
        if token in self._framing_ids:
            return self._framing_ids[token]
        if token.startswith("<|vis_") and token.endswith("|>"):
            try:
                idx = int(token[len("<|vis_"):-len("|>")])
            except ValueError:
                return None
            token_id = self._vis_start + idx
            return token_id if self._vis_start <= token_id < self._vis_end else None
        if self._aud_start is not None and token.startswith("<|aud_") and token.endswith("|>"):
            try:
                idx = int(token[len("<|aud_"):-len("|>")])
            except ValueError:
                return None
            token_id = self._aud_start + idx
            return token_id if token_id < self._aud_end else None
        return None

    def _unitron_id_to_token(self, token_id: int) -> str | None:
        for tok, tid in self._framing_ids.items():
            if tid == token_id:
                return tok
        if self._vis_start <= token_id < self._vis_end:
            return f"<|vis_{token_id - self._vis_start}|>"
        if self._aud_start is not None and self._aud_start <= token_id < self._aud_end:
            return f"<|aud_{token_id - self._aud_start}|>"
        return None

    def _encode_mixed(self, text: str) -> list[int]:
        ids: list[int] = []
        pos = 0
        for match in _UNITRON_TOKEN_RE.finditer(text):
            if match.start() > pos:
                ids.extend(
                    self.base_tokenizer.encode(
                        text[pos:match.start()],
                        add_special_tokens=False,
                    )
                )
            token = match.group(0)
            token_id = self._unitron_token_to_id(token)
            if token_id is None:
                ids.extend(self.base_tokenizer.encode(token, add_special_tokens=False))
            else:
                ids.append(token_id)
            pos = match.end()
        if pos < len(text):
            ids.extend(self.base_tokenizer.encode(text[pos:], add_special_tokens=False))
        return ids

    def encode(
        self,
        text: Any,
        *args: Any,
        add_special_tokens: bool = True,
        return_tensors: str | None = None,
        **kwargs: Any,
    ) -> Any:
        if not isinstance(text, str) or _UNITRON_TOKEN_RE.search(text) is None:
            return self.base_tokenizer.encode(
                text,
                *args,
                add_special_tokens=add_special_tokens,
                return_tensors=return_tensors,
                **kwargs,
            )

        ids = self._encode_mixed(text)
        if add_special_tokens:
            ids = self.base_tokenizer.build_inputs_with_special_tokens(ids)
        ids = self._maybe_truncate(ids, kwargs.get("truncation"), kwargs.get("max_length"))
        if return_tensors is None:
            return ids
        if return_tensors == "pt":
            import torch

            return torch.tensor([ids], dtype=torch.long)
        raise ValueError(f"unsupported return_tensors={return_tensors!r}")

    def _maybe_truncate(
        self,
        ids: list[int],
        truncation: Any,
        max_length: int | None,
    ) -> list[int]:
        if not truncation:
            return ids
        limit = max_length or getattr(self.base_tokenizer, "model_max_length", None)
        if limit is None or limit <= 0 or limit > 10**20:
            return ids
        return ids[: int(limit)]

    def __call__(
        self,
        text: Any = None,
        text_pair: Any = None,
        *args: Any,
        add_special_tokens: bool = True,
        padding: bool | str = False,
        truncation: bool | str | None = None,
        max_length: int | None = None,
        return_tensors: str | None = None,
        return_attention_mask: bool | None = None,
        **kwargs: Any,
    ) -> Any:
        if text_pair is not None:
            return self.base_tokenizer(
                text,
                text_pair=text_pair,
                *args,
                add_special_tokens=add_special_tokens,
                padding=padding,
                truncation=truncation,
                max_length=max_length,
                return_tensors=return_tensors,
                return_attention_mask=return_attention_mask,
                **kwargs,
            )
        if isinstance(text, str) and _UNITRON_TOKEN_RE.search(text) is None:
            return self.base_tokenizer(
                text,
                *args,
                add_special_tokens=add_special_tokens,
                padding=padding,
                truncation=truncation,
                max_length=max_length,
                return_tensors=return_tensors,
                return_attention_mask=return_attention_mask,
                **kwargs,
            )
        if isinstance(text, (list, tuple)) and all(
            isinstance(item, str) and _UNITRON_TOKEN_RE.search(item) is None
            for item in text
        ):
            return self.base_tokenizer(
                text,
                *args,
                add_special_tokens=add_special_tokens,
                padding=padding,
                truncation=truncation,
                max_length=max_length,
                return_tensors=return_tensors,
                return_attention_mask=return_attention_mask,
                **kwargs,
            )

        is_batched = isinstance(text, (list, tuple))
        texts = list(text) if is_batched else [text]
        encoded = []
        for item in texts:
            ids = self.encode(
                "" if item is None else str(item),
                *args,
                add_special_tokens=add_special_tokens,
                truncation=truncation,
                max_length=max_length,
                return_tensors=None,
                **kwargs,
            )
            record = {"input_ids": ids}
            if return_attention_mask is not False:
                record["attention_mask"] = [1] * len(ids)
            encoded.append(record)

        if padding or return_tensors is not None:
            batch = self.base_tokenizer.pad(
                encoded,
                padding=padding,
                max_length=max_length,
                return_tensors=return_tensors,
            )
        else:
            batch = BatchEncoding({
                key: [record[key] for record in encoded]
                for key in encoded[0]
            })

        if is_batched or return_tensors is not None:
            return batch
        return BatchEncoding({key: value[0] for key, value in batch.items()})

    def apply_chat_template(self, conversation: Any, *args: Any, **kwargs: Any) -> Any:
        tokenize = bool(kwargs.pop("tokenize", True))
        return_tensors = kwargs.pop("return_tensors", None)
        rendered = self.base_tokenizer.apply_chat_template(
            conversation,
            *args,
            tokenize=False,
            **kwargs,
        )
        if not tokenize:
            return rendered
        ids = self._encode_mixed(rendered)
        if return_tensors is None:
            return ids
        if return_tensors == "pt":
            import torch

            return torch.tensor([ids], dtype=torch.long)
        raise ValueError(f"unsupported return_tensors={return_tensors!r}")

    def convert_tokens_to_ids(self, tokens: Any) -> Any:
        if isinstance(tokens, list):
            return [self.convert_tokens_to_ids(tok) for tok in tokens]
        token_id = self._unitron_token_to_id(str(tokens))
        if token_id is not None:
            return token_id
        return self.base_tokenizer.convert_tokens_to_ids(tokens)

    def convert_ids_to_tokens(self, ids: Any, *args: Any, **kwargs: Any) -> Any:
        if isinstance(ids, list):
            return [self.convert_ids_to_tokens(i, *args, **kwargs) for i in ids]
        token = self._unitron_id_to_token(int(ids))
        if token is not None:
            return token
        return self.base_tokenizer.convert_ids_to_tokens(ids, *args, **kwargs)

    def _decode_mixed(self, ids: Any, *args: Any, **kwargs: Any) -> str:
        if hasattr(ids, "tolist"):
            ids = ids.tolist()
        if isinstance(ids, int):
            ids = [ids]
        pieces: list[str] = []
        text_ids: list[int] = []
        for token_id in ids:
            unitron_token = self._unitron_id_to_token(int(token_id))
            if unitron_token is None:
                text_ids.append(int(token_id))
                continue
            if text_ids:
                pieces.append(self.base_tokenizer.decode(text_ids, *args, **kwargs))
                text_ids = []
            pieces.append(unitron_token)
        if text_ids:
            pieces.append(self.base_tokenizer.decode(text_ids, *args, **kwargs))
        return "".join(pieces)

    def decode(self, token_ids: Any, *args: Any, **kwargs: Any) -> str:
        if hasattr(token_ids, "tolist"):
            token_ids = token_ids.tolist()
        ids = [token_ids] if isinstance(token_ids, int) else list(token_ids)
        if not any(self._unitron_id_to_token(int(token_id)) is not None for token_id in ids):
            return self.base_tokenizer.decode(ids, *args, **kwargs)
        return self._decode_mixed(ids, *args, **kwargs)

    def batch_decode(self, sequences: Any, *args: Any, **kwargs: Any) -> list[str]:
        if hasattr(sequences, "tolist"):
            sequences = sequences.tolist()
        return [self.decode(seq, *args, **kwargs) for seq in sequences]

    def get_vocab(self) -> dict[str, int]:
        vocab = dict(self.base_tokenizer.get_vocab())
        vocab.update(self._framing_ids)
        vocab["<|vis_0|>"] = self._vis_start
        vocab[f"<|vis_{self._vis_end - self._vis_start - 1}|>"] = self._vis_end - 1
        return vocab

    def __len__(self) -> int:
        return self._model_vocab_size

    def __copy__(self):
        copied = self.__class__.__new__(self.__class__)
        copied.__dict__.update(self.__dict__)
        return copied

    def __getattr__(self, name: str) -> Any:
        base_tokenizer = self.__dict__.get("base_tokenizer")
        if base_tokenizer is None:
            raise AttributeError(name)
        return getattr(base_tokenizer, name)
