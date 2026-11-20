"""Native Transformers readout for the Sing VL S1 checkpoint."""
import hashlib
import json
import math
import re
from pathlib import Path

from PIL import Image
import torch
import transformers
from transformers import AutoProcessor, Qwen3_5ForConditionalGeneration

MODEL_ID = "sing-vl-s1"
TEXT_MAX_TOKENS = 65_536
VISION_MAX_TOKENS = 10_000
PUBLIC_IMAGE_MAX_PIXELS = 1_638_400
INSTRUCTION = "Solve the multiple-choice question and output ONLY the index token of the correct option.\n\n"
ANSWER_PREFIX = "<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
IMAGE_SLOT = "<|vision_start|><|image_pad|><|vision_end|>"
TRAILING_IMAGES = re.compile(r"(?:\s*<image>\s*)+$")
CONTROL_MARKER = re.compile(r"<video>|<\|(?:im_|vision_|image_pad|video_pad)")


class Unsupported(ValueError):
    pass


def as_text(value):
    return value if isinstance(value, str) else json.dumps(value, ensure_ascii=False, separators=(",", ":"))


def questions_for_state(state, questions, image_count):
    if not isinstance(questions, dict) or not questions:
        raise ValueError("questions must be a nonempty object")
    state = "" if image_count and state == {} else as_text(state)
    if CONTROL_MARKER.search(state):
        raise Unsupported("state contains a reserved model-control marker")
    if image_count and "<image>" not in state:
        state = "<image>\n" * image_count + state
    if state.count("<image>") != image_count:
        raise Unsupported("the number of <image> placeholders must match the images")
    for question_id, question in questions.items():
        if not isinstance(question, dict):
            raise ValueError("each question must be an object")
        kind = question.get("type")
        if kind not in ("choice", "noul", "score"):
            raise Unsupported("supported question types are choice, noul and score")
        criteria = question.get("criteria")
        if kind == "score":
            if not isinstance(criteria, list) or not 2 <= len(criteria) <= 10:
                raise Unsupported("score criteria must be an ordered array of 2..10 levels")
            criteria = {str(level): description for level, description in enumerate(criteria)}
        if kind == "noul" and (criteria is None or criteria == {}):
            criteria = {"true": "Yes", "false": "No"}
        if not isinstance(criteria, dict) or not 2 <= len(criteria) <= 256:
            raise Unsupported("supports 2..256 options per choice")
        if kind == "noul" and set(criteria) != {"true", "false"}:
            raise Unsupported("noul criteria must be true/false")
        instructions = as_text(question.get("instructions", ""))
        options = {key: key if value is None else as_text(value) for key, value in criteria.items()}
        if CONTROL_MARKER.search(instructions) or any(CONTROL_MARKER.search(value) for value in options.values()):
            raise Unsupported("question contains a reserved model-control marker")
        if "<image>" in instructions:
            raise Unsupported("place image markers in state")
        yield question_id, kind, state, instructions, options


def reference_images(state, options):
    """Resolve option references to images already present in the state."""
    for key, value in options.items():
        if "<image>" not in value:
            continue
        needle = f"({key}) {value}"
        if state.count(needle) != 1:
            raise Unsupported(f"ambiguous image reference for option {key}")
        offset = state.index(needle) + len(f"({key}) ")
        index = state[:offset].count("<image>") + 1
        references = iter(range(index, index + value.count("<image>")))
        options[key] = re.sub(r"<image>", lambda _: f"[Image {next(references)} above]", value)
    indices = iter(range(1, state.count("<image>") + 1))
    return re.sub(r"<image>", lambda _: f"[Image {next(indices)}] <image>", state)


def render(state, instructions, options, labels):
    if any("<image>" in value for value in options.values()):
        state = reference_images(state, options)
    question = state + instructions
    trailing = TRAILING_IMAGES.search(question)
    if trailing and question[:trailing.start()].rstrip():
        question = trailing.group().strip() + "\n" + question[:trailing.start()].rstrip()
    question = question.rstrip()
    if question.endswith("Choices:"):
        question = question[:-len("Choices:")].rstrip()
    lines = "\n".join(f"{label}: {value}" for label, value in zip(labels, options.values()))
    user = (INSTRUCTION + "### Question:\n" + question + "\n\n### Options:\n" + lines).strip()
    return "<|im_start|>user\n" + user.replace("<image>", IMAGE_SLOT) + ANSWER_PREFIX


def resize_image(image, factor, min_pixels, max_pixels):
    if image.mode == "RGBA":
        rgb = Image.new("RGB", image.size, "white")
        rgb.paste(image, mask=image.getchannel("A"))
    else:
        rgb = image.convert("RGB")
    width, height = rgb.size
    if max(width, height) / min(width, height) > 200:
        raise Unsupported("image aspect ratio exceeds 200")
    w, h = (max(factor, round(d / factor) * factor) for d in (width, height))
    if w * h > max_pixels:
        scale = math.sqrt(max_pixels / (width * height))
        w, h = (max(factor, math.floor(d * scale / factor) * factor) for d in (width, height))
    elif w * h < min_pixels:
        scale = math.sqrt(min_pixels / (width * height))
        w, h = (math.ceil(d * scale / factor) * factor for d in (width, height))
    return rgb.resize((w, h), Image.Resampling.BICUBIC)


def bidirectional_prompt(_module, args, kwargs):
    """Apply SingVL's noncausal full attention and causal GDN without a KV cache."""
    attention = kwargs["attention_mask"]
    if kwargs.get("use_cache") or kwargs.get("past_key_values") is not None:
        raise ValueError("Sing VL S1 expects complete prompts without a cache")
    if isinstance(attention, dict):
        # The text batch path supplies the per-layer masks directly, with right padding.
        if set(attention) != {"full_attention", "linear_attention"} or attention["linear_attention"] is not None:
            raise ValueError("unexpected Sing VL S1 batch attention masks")
        mask = attention["full_attention"]
        ids = kwargs["input_ids"]
        if mask is not None and (mask.dtype != torch.bool or mask.shape != (ids.size(0), 1, 1, ids.size(1))):
            raise ValueError("full attention requires a per-row boolean key mask")
        return args, kwargs
    if (attention is None or attention.ndim != 2 or attention.shape[0] != 1
            or not attention.bool().all().item()):
        raise ValueError("Sing VL S1 expects a single unpadded prompt without a cache")
    kwargs["attention_mask"] = {"full_attention": None, "linear_attention": None}
    return args, kwargs


class SingVLS1:
    def __init__(self, model, device="cuda:0", image_max_pixels=PUBLIC_IMAGE_MAX_PIXELS, batch_token_budget=65_536):
        if batch_token_budget < 1:
            raise ValueError("batch_token_budget must be positive")
        self.batch_token_budget = int(batch_token_budget)
        self.batch_oom_splits = 0
        self.model_path = str(Path(model).resolve())
        self.device = torch.device(device)
        self.processor = AutoProcessor.from_pretrained(self.model_path, local_files_only=True)
        self.tokenizer = self.processor.tokenizer
        self.model = Qwen3_5ForConditionalGeneration.from_pretrained(
            self.model_path, local_files_only=True, dtype=torch.bfloat16, attn_implementation="sdpa",
        ).to(self.device).eval()
        config = self.model.config
        if config.jev_prefix_attention_mode != "prefix_bidir" or config.jev_gdn_mode != "causal":
            raise ValueError("checkpoint does not declare the Sing VL S1 attention contract")
        readout = config.jev_soft_choice
        if readout["version"] != "soft-choice-full-vocab-v2" or readout["readout"] != "last-valid-input-position":
            raise ValueError("checkpoint does not declare the Sing VL S1 readout")
        self.choice_ids = readout["token_ids"]
        self.labels = [self.tokenizer.decode([idx], clean_up_tokenization_spaces=False) for idx in self.choice_ids]
        if (len(set(self.choice_ids)) != 256 or not all(re.fullmatch("[A-Z]{2}", label) for label in self.labels)
                or any(self.tokenizer.encode(label, add_special_tokens=False) != [idx]
                       for idx, label in zip(self.choice_ids, self.labels))):
            raise ValueError("checkpoint's 256 choice tokens do not match the tokenizer")
        language = self.model.model.language_model
        for layer in language.layers:
            if hasattr(layer, "self_attn"):
                layer.self_attn.is_causal = False
        language.register_forward_pre_hook(bidirectional_prompt, with_kwargs=True)
        self.model.config.use_cache = language.config.use_cache = False
        self.image_id = config.image_token_id
        image_processor = self.processor.image_processor
        self.merge_size = image_processor.merge_size
        self.image_factor = image_processor.patch_size * self.merge_size
        self.min_pixels = int(config.jev_prefix_media["IMAGE_MIN_TOKEN_NUM"]) * self.image_factor ** 2
        if image_max_pixels < self.min_pixels:
            raise ValueError("image_max_pixels is smaller than the checkpoint's minimum image area")
        self.image_max_pixels = int(image_max_pixels)
        self.max_text_tokens = min(TEXT_MAX_TOKENS, config.text_config.max_position_embeddings)

    def encode_images(self, images):
        if not images:
            return {}
        prepared = [resize_image(image, self.image_factor, self.min_pixels, self.image_max_pixels) for image in images]
        return dict(self.processor.image_processor(images=prepared, return_tensors="pt", do_resize=False))

    def encode(self, prompt, image_features):
        ids = self.tokenizer.encode(prompt, add_special_tokens=False)
        if image_features:
            grid = image_features["image_grid_thw"]
            if ids.count(self.image_id) != len(grid):
                raise Unsupported("expanded media tokens do not match the images")
            counts = iter(grid.prod(dim=-1).tolist())
            ids = [part for token in ids for part in (
                [self.image_id] * (next(counts) // self.merge_size ** 2) if token == self.image_id else [token]
            )]
        limit = VISION_MAX_TOKENS if image_features else self.max_text_tokens
        if len(ids) > limit:
            raise Unsupported(f"maximum model length is {limit} tokens; got {len(ids)}")
        tokens = torch.tensor([ids], dtype=torch.long)
        batch = {"input_ids": tokens, "attention_mask": torch.ones_like(tokens), **image_features}
        if image_features:
            batch["mm_token_type_ids"] = (tokens == self.image_id).to(torch.int32)
        return batch, ids

    def _last_logits(self, model_inputs):
        self.model.model.rope_deltas = None
        output = self.model(**model_inputs, use_cache=False, logits_to_keep=1)
        return output.logits[:, -1]

    def _score_serial(self, requests, image_features):
        for key, kind, state, instructions, options in requests:
            batch, ids = self.encode(render(state, instructions, options, self.labels), image_features)
            model_inputs = {name: value.to(self.device) for name, value in batch.items()}
            logits = self._last_logits(model_inputs)[0, self.choice_ids[:len(options)]].float()
            yield key, kind, options, ids, logits

    def _text_batches(self, rows):
        current = []
        for row in sorted(rows, key=lambda item: len(item[3])):
            if current and len(row[3]) * (len(current) + 1) > self.batch_token_budget:
                yield current
                current = []
            current.append(row)
        if current:
            yield current

    def _score_text_batch(self, rows):
        lengths = [len(row[3]) for row in rows]
        width = max(lengths)
        input_ids = torch.full((len(rows), width), self.tokenizer.pad_token_id, dtype=torch.long)
        for i, row in enumerate(rows):
            input_ids[i, :lengths[i]] = torch.tensor(row[3], dtype=torch.long)
        input_ids = input_ids.to(self.device)
        lengths_tensor = torch.tensor(lengths, device=self.device)
        if len(rows) == 1:
            logits = self._last_logits({"input_ids": input_ids, "attention_mask": torch.ones_like(input_ids)})
        else:
            # Right padding preserves each real token's original RoPE position and cannot
            # influence any earlier token in the causal GDN. In full attention pad keys
            # must be invisible to all queries in the same row.
            key_mask = None
            if lengths[0] != lengths[-1]:
                valid = torch.arange(width, device=self.device)[None, :] < lengths_tensor[:, None]
                key_mask = valid[:, None, None, :]
            masks = {"full_attention": key_mask, "linear_attention": None}
            backbone = self.model.model.language_model
            hidden = backbone(input_ids=input_ids, attention_mask=masks, use_cache=False,
                              return_dict=True).last_hidden_state
            row_indices = torch.arange(len(rows), device=self.device)
            logits = self.model.lm_head(hidden[row_indices, lengths_tensor - 1, :])
        most_options = max(len(row[2]) for row in rows)
        return logits[:, self.choice_ids[:most_options]].float()

    def _score_batched_text(self, requests):
        rows = []
        for key, kind, state, instructions, options in requests:
            _, ids = self.encode(render(state, instructions, options, self.labels), {})
            rows.append((key, kind, options, ids))
        for batch in self._text_batches(rows):
            yield from self._score_with_oom_retry(batch)

    def _score_with_oom_retry(self, rows):
        try:
            logits = self._score_text_batch(rows)
        except torch.cuda.OutOfMemoryError:
            if self.device.type != "cuda" or len(rows) == 1:
                raise
        else:
            for i, (key, kind, options, ids) in enumerate(rows):
                yield key, kind, options, ids, logits[i, :len(options)]
            return
        # The failed forward's traceback (and its CUDA tensors) has left scope here.
        self.batch_oom_splits += 1
        with torch.cuda.device(self.device):
            torch.cuda.empty_cache()
        mid = len(rows) // 2
        yield from self._score_with_oom_retry(rows[:mid])
        yield from self._score_with_oom_retry(rows[mid:])

    def predict(self, state, questions, images=()):
        return self._predict(state, questions, images, batch_text=True)

    def predict_serial(self, state, questions, images=()):
        """Run the release's one-prompt-at-a-time path for comparison."""
        return self._predict(state, questions, images, batch_text=False)

    @torch.inference_mode()
    def _predict(self, state, questions, images, batch_text):
        if len(images) > 4:
            raise Unsupported("at most four images per request")
        requests = list(questions_for_state(state, questions, len(images)))
        image_features = self.encode_images(images)
        image_grid = image_features["image_grid_thw"].tolist() if image_features else None
        image_tokens = sum(math.prod(grid) // self.merge_size ** 2 for grid in image_grid or ())
        answers, details = {}, {}
        if batch_text and not image_features and len(requests) > 1:
            scored = self._score_batched_text(requests)
        else:
            scored = self._score_serial(requests, image_features)
        for question_id, kind, options, ids, logits in scored:
            if not torch.isfinite(logits).all():
                raise ValueError("nonfinite candidate logits")
            probabilities = dict(zip(options, logits.softmax(-1).tolist()))
            if kind == "noul":
                answers[question_id] = {"type": "noul", "noul": probabilities["true"]}
            elif kind == "score":
                total = math.fsum(probabilities.values())
                probabilities = {level: probability / total for level, probability in probabilities.items()}
                answers[question_id] = {
                    "type": "score",
                    "score": math.fsum(int(level) * probability for level, probability in probabilities.items()),
                    "probabilities": probabilities,
                    "legend": dict(zip(probabilities, questions[question_id]["criteria"])),
                }
            else:
                answers[question_id] = {
                    "type": "choice", "choice": max(probabilities, key=probabilities.get),
                    "probabilities": probabilities,
                }
            details[question_id] = {
                "input_tokens": len(ids),
                "input_ids_sha256": hashlib.sha256(json.dumps([ids]).encode()).hexdigest(),
                "image_grid_thw": image_grid,
                "image_tokens": image_tokens,
                "candidate_logits": logits.tolist(),
            }
        usage = {"input_tokens": sum(item["input_tokens"] for item in details.values()), "output_tokens": 0}
        answers = {key: answers[key] for key in questions}
        details = {key: details[key] for key in questions}
        return {"model": MODEL_ID, "answers": answers, "usage": usage}, details

    def runtime(self):
        return {
            "torch": torch.__version__, "transformers": transformers.__version__, "device": str(self.device),
            "precision": "bfloat16", "attention": "bidirectional full attention, causal GDN, no KV cache",
            "image_max_pixels": self.image_max_pixels, "text_max_tokens": self.max_text_tokens,
            "vision_max_tokens": VISION_MAX_TOKENS,
        }
