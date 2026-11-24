"""Generation-only slot policy, shared by training and serving.

The request ID carries an explicit slotless marker. Never infer task identity
from token values: a literal pad/EOS at the end of a prompt is not a soft slot.
"""

GENERATION_SLOT_KEY = "unimodel_generation_slot_enable"
SLOTLESS_REQUEST_PREFIX = "unimodel-slotless:"


def generation_slots_enabled(settings):
    value = settings.get(GENERATION_SLOT_KEY, not settings.get("unimodel_decision_enable", False))
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, str)):
        value = str(value).strip().lower()
        if value in {"1", "true", "yes", "y", "on"}:
            return True
        if value in {"0", "false", "no", "n", "off"}:
            return False
    raise ValueError(f"{GENERATION_SLOT_KEY} must be a boolean")


def generation_request_id(request_id, enabled):
    if str(request_id).startswith(SLOTLESS_REQUEST_PREFIX):
        raise ValueError("request ID already contains a reserved slot policy marker")
    return str(request_id) if enabled else SLOTLESS_REQUEST_PREFIX + str(request_id)


def prefill_slot_requests(embedding, forward_batch, count):
    """One explicit policy per full prefill; embedding requests remain slotted."""
    enabled = getattr(embedding, "_unimodel_generation_slot_enable", True)
    rids = getattr(forward_batch, "rids", None)
    if rids is None:
        if not enabled:
            raise RuntimeError("slotless generation requires SGLang forward request IDs")
        return [True] * count
    if len(rids) != count:
        raise RuntimeError("slot policy request IDs do not match prefill boundaries")
    slotted = [not str(rid).startswith(SLOTLESS_REQUEST_PREFIX) for rid in rids]
    if enabled and not all(slotted):
        raise RuntimeError("slotless request sent to a slotted generation checkpoint")
    return slotted
