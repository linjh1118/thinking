"""Shared, dependency-free JEV architecture contract for training and assets."""
from dataclasses import dataclass

TASK_SLOT_ARCHITECTURE = "task_slots_v1"


def validate_task_slots(config, *, checkpoint=False):
    """One physical slot per E/J row; two independently learned role vectors."""
    get = config.get if isinstance(config, dict) else lambda k, d=None: getattr(config, k, d)
    try:
        from .generation_slots import generation_slots_enabled
    except ImportError:
        from generation_slots import generation_slots_enabled
    if (int(get("unimodel_slot_count", 1)) != 1
            or int(get("unimodel_slot_readout_index", 0)) != 0
            or generation_slots_enabled({"unimodel_generation_slot_enable":
                get("unimodel_generation_slot_enable", False)})):
        raise ValueError("task slots require slot_count=1, readout=0 and slotless generation")
    architecture = get("unimodel_architecture", None)
    if architecture not in ((TASK_SLOT_ARCHITECTURE,) if checkpoint else (None, TASK_SLOT_ARCHITECTURE)):
        raise ValueError("legacy combined E/J checkpoint/config is incompatible with task_slots_v1")


@dataclass(frozen=True)
class DecisionConfig:
    head_type: str = "matching"
    max_candidates: int = 255

    @property
    def output_size(self):
        # Fixed independent of TP world size, so checkpoints remain portable.
        # Spare rows are never included in the decision distribution.
        return ((self.max_candidates + 127) // 128) * 128

    @classmethod
    def from_config(cls, config):
        get = config.get if isinstance(config, dict) else lambda k, d: getattr(config, k, d)
        head = get("unimodel_decision_head_type", "matching")
        capacity = get("unimodel_decision_max_candidates", 255)
        if head not in {"matching", "direct"}:
            raise ValueError("unimodel_decision_head_type must be matching or direct")
        # Read-only compatibility guard for the withdrawn attention variant.
        # Do not silently load a noncausal checkpoint as a causal model.
        if get("unimodel_decision_attention", "causal") != "causal":
            raise ValueError("JEV uses the shared causal backbone; legacy noncausal decision checkpoints/configs are unsupported")
        if isinstance(capacity, bool) or not isinstance(capacity, int) or capacity < 2:
            raise ValueError("unimodel_decision_max_candidates must be an integer >= 2")
        return cls(head, capacity)


def validate_decision_checkpoint(source, runtime, weight_names, *, allow_native_initialization=False):
    """Reject random reinitialization or architecture changes during HF load."""
    get = runtime.get if isinstance(runtime, dict) else lambda k, d: getattr(runtime, k, d)
    source_enabled = source.get("unimodel_decision_enable", False)
    runtime_enabled = get("unimodel_decision_enable", False)
    weight_names = tuple(weight_names)
    if (allow_native_initialization and runtime_enabled is True
            and source.get("model_type") == "qwen3_5"
            and not any(key.startswith("unimodel") for key in source)
            and not any("unimodel" in name or "embedding_head" in name for name in weight_names)):
        # Native backbone loading intentionally leaves newly attached modules
        # initialized by Megatron. Existing UniModel checkpoints stay strict.
        DecisionConfig.from_config(runtime)
        validate_task_slots(runtime)
        return
    if not source_enabled and not runtime_enabled:
        return
    if source_enabled is not True or runtime_enabled is not True:
        raise ValueError("JEV checkpoint enable mismatch; migrate explicitly with a fresh optimizer")
    validate_task_slots(source, checkpoint=True)
    validate_task_slots(runtime)
    saved, requested = DecisionConfig.from_config(source), DecisionConfig.from_config(runtime)
    if saved != requested:
        raise ValueError("JEV checkpoint architecture mismatch; migrate explicitly with a fresh optimizer")
    roles = ("output",) if saved.head_type == "direct" else ("query", "candidate")
    expected = {f"unimodel.decision_head.{role}.weight" for role in roles}
    actual = {name for name in weight_names if name.startswith("unimodel.decision_head.")}
    if expected != actual:
        raise ValueError(f"JEV checkpoint head weights mismatch: expected {sorted(expected)}, got {sorted(actual)}")
