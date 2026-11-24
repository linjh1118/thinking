"""True Multi-Granularity Visual Bottleneck for Qwen3.5 UniModel training."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any, Iterable, Sequence

import torch
import torch.nn.functional as F

from mbridge.models.qwen3_5.mgvb_utils import (
    build_mgvb_visual_positions,
    cell_assignment,
    cell_edges,
    merged_grid_shape,
    native_visual_positions,
    partition_spatial_grid,
)

MGVB_ADDITIVE_METRICS = frozenset({
    "mgvb/reconstruction_loss", "mgvb/diversity_loss", "mgvb/aux_loss",
})


def _as_bool(value: Any, default: bool = False) -> bool:
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"1", "true", "yes", "y", "on"}


def is_mgvb_enabled(hf_config: Any) -> bool:
    return _as_bool(getattr(hf_config, "unimodel_mgvb_enable", False))


class _RMSNorm(torch.nn.Module):
    def __init__(self, hidden_size: int, *, eps: float = 1e-6, device=None, dtype=None) -> None:
        super().__init__()
        self.weight = torch.nn.Parameter(torch.ones(hidden_size, device=device, dtype=dtype))
        self.eps = float(eps)

    def forward(self, value: torch.Tensor) -> torch.Tensor:
        normalized = value.float() * torch.rsqrt(
            value.float().square().mean(dim=-1, keepdim=True) + self.eps
        )
        return normalized.to(value.dtype) * self.weight


class _AdapterResidual(torch.nn.Module):
    def __init__(self, adapter_dim: int, hidden_size: int, *, device=None, dtype=None) -> None:
        super().__init__()
        self.norm = torch.nn.LayerNorm(adapter_dim, device=device, dtype=dtype)
        self.fc1 = torch.nn.Linear(adapter_dim, adapter_dim * 2, bias=False, device=device, dtype=dtype)
        self.fc2 = torch.nn.Linear(adapter_dim * 2, hidden_size, bias=False, device=device, dtype=dtype)
        torch.nn.init.zeros_(self.fc2.weight)

    def forward(self, value: torch.Tensor) -> torch.Tensor:
        return self.fc2(F.gelu(self.fc1(self.norm(value))))


@dataclass
class MGVBForwardOutput:
    embeddings: list[torch.Tensor]
    positions: list[torch.Tensor]


class MultiGranularityVisualBottleneck(torch.nn.Module):
    """Replace long native visual sequences with a fixed G/R/F token bank."""

    def __init__(
        self,
        hidden_size: int,
        *,
        adapter_dim: int = 512,
        token_budget: int = 256,
        global_tokens: int = 8,
        region_tokens: int = 64,
        num_global_heads: int = 8,
        device=None,
        dtype=None,
    ) -> None:
        super().__init__()
        self.hidden_size = int(hidden_size)
        self.adapter_dim = int(adapter_dim)
        self.token_budget = int(token_budget)
        self.global_tokens = int(global_tokens)
        self.region_tokens = int(region_tokens)
        self.fine_tokens = self.token_budget - self.global_tokens - self.region_tokens
        self.num_global_heads = int(num_global_heads)
        if self.hidden_size < 1 or self.adapter_dim < 1:
            raise ValueError("MGVB hidden and adapter dimensions must be positive")
        if self.token_budget < 3:
            raise ValueError("MGVB token budget must be at least three")
        if min(self.global_tokens, self.region_tokens, self.fine_tokens) < 1:
            raise ValueError(
                "MGVB budget must leave positive global, region, and fine branches; "
                f"got total={self.token_budget}, global={self.global_tokens}, "
                f"region={self.region_tokens}, fine={self.fine_tokens}"
            )
        if self.adapter_dim % self.num_global_heads:
            raise ValueError(
                f"adapter_dim={self.adapter_dim} must be divisible by num_global_heads={self.num_global_heads}"
            )

        self.input_norm = _RMSNorm(hidden_size, device=device, dtype=dtype)
        self.input_proj = torch.nn.Linear(hidden_size, adapter_dim, bias=False, device=device, dtype=dtype)
        self.query_proj = torch.nn.Linear(hidden_size * 2, adapter_dim, bias=False, device=device, dtype=dtype)
        self.null_query = torch.nn.Parameter(torch.zeros(adapter_dim, device=device, dtype=dtype))

        self.global_queries = torch.nn.Parameter(
            torch.empty(global_tokens, adapter_dim, device=device, dtype=dtype)
        )
        self.global_key = torch.nn.Linear(adapter_dim, adapter_dim, bias=False, device=device, dtype=dtype)
        self.global_value = torch.nn.Linear(adapter_dim, adapter_dim, bias=False, device=device, dtype=dtype)
        self.global_query_condition = torch.nn.Linear(
            adapter_dim, adapter_dim, bias=False, device=device, dtype=dtype
        )
        self.global_residual = _AdapterResidual(adapter_dim, hidden_size, device=device, dtype=dtype)

        self.region_value = torch.nn.Linear(adapter_dim, adapter_dim, bias=False, device=device, dtype=dtype)
        self.region_query = torch.nn.Linear(adapter_dim, adapter_dim, bias=False, device=device, dtype=dtype)
        self.region_position = torch.nn.Linear(4, adapter_dim, bias=False, device=device, dtype=dtype)
        self.region_score = torch.nn.Linear(adapter_dim, 1, bias=False, device=device, dtype=dtype)
        self.region_residual = _AdapterResidual(adapter_dim, hidden_size, device=device, dtype=dtype)

        self.fine_value = torch.nn.Linear(adapter_dim, adapter_dim, bias=False, device=device, dtype=dtype)
        self.fine_query = torch.nn.Linear(adapter_dim, adapter_dim, bias=False, device=device, dtype=dtype)
        self.fine_position = torch.nn.Linear(4, adapter_dim, bias=False, device=device, dtype=dtype)
        self.fine_score = torch.nn.Linear(adapter_dim, 1, bias=False, device=device, dtype=dtype)
        self.fine_residual = _AdapterResidual(adapter_dim, hidden_size, device=device, dtype=dtype)

        self.granularity_embedding = torch.nn.Embedding(3, hidden_size, device=device, dtype=dtype)
        self.output_position = torch.nn.Linear(4, hidden_size, bias=False, device=device, dtype=dtype)
        self.reconstruction_position = torch.nn.Linear(
            4, hidden_size, bias=False, device=device, dtype=dtype
        )
        self.reconstruction_norm = torch.nn.LayerNorm(hidden_size, device=device, dtype=dtype)
        self.reconstruction_fc1 = torch.nn.Linear(
            hidden_size, adapter_dim, bias=False, device=device, dtype=dtype
        )
        self.reconstruction_fc2 = torch.nn.Linear(
            adapter_dim, hidden_size, bias=False, device=device, dtype=dtype
        )

        torch.nn.init.normal_(self.global_queries, mean=0.0, std=0.02)
        torch.nn.init.zeros_(self.global_query_condition.weight)
        torch.nn.init.zeros_(self.region_query.weight)
        torch.nn.init.zeros_(self.fine_query.weight)
        torch.nn.init.zeros_(self.region_position.weight)
        torch.nn.init.zeros_(self.fine_position.weight)
        torch.nn.init.zeros_(self.region_score.weight)
        torch.nn.init.zeros_(self.fine_score.weight)
        torch.nn.init.normal_(self.granularity_embedding.weight, mean=0.0, std=0.002)
        torch.nn.init.normal_(self.output_position.weight, mean=0.0, std=0.002)
        torch.nn.init.normal_(self.reconstruction_position.weight, mean=0.0, std=0.002)

        self.unimodel_last_mgvb_metrics: dict[str, torch.Tensor] | None = None
        self.unimodel_last_mgvb_losses: dict[str, torch.Tensor] | None = None

    @staticmethod
    def _normalized_coordinates(
        temporal: int,
        height: int,
        width: int,
        *,
        device: torch.device,
        dtype: torch.dtype,
    ) -> torch.Tensor:
        positions = native_visual_positions(
            [temporal, height, width],
            spatial_merge_size=1,
            device=device,
        ).to(dtype=dtype)
        denominators = positions.new_tensor(
            [max(temporal - 1, 1), max(height - 1, 1), max(width - 1, 1)]
        )
        normalized = positions / denominators
        area = positions.new_full((positions.shape[0], 1), 1.0 / max(height * width, 1))
        return torch.cat([normalized, area], dim=-1)

    def _query(self, query_embedding: torch.Tensor | None, reference: torch.Tensor) -> torch.Tensor:
        if query_embedding is None:
            return self.null_query.to(device=reference.device, dtype=reference.dtype)
        if query_embedding.shape[-1] != self.hidden_size * 2:
            raise ValueError(
                f"MGVB query embedding must have size {self.hidden_size * 2}, got {query_embedding.shape}"
            )
        return self.query_proj(
            query_embedding.to(device=reference.device, dtype=self.query_proj.weight.dtype)
        ).to(dtype=reference.dtype)

    @staticmethod
    def _segment_softmax(
        logits: torch.Tensor,
        segment_ids: torch.Tensor,
        segment_count: int,
    ) -> torch.Tensor:
        work = logits.float()
        # P800's XPU backend does not implement aten::scatter_reduce.two_out.
        # Build the small segment-by-edge attention matrix instead: MGVB has at
        # most one row per output token (64 region / 184 fine by default), so
        # this remains bounded while using only well-supported softmax/gather
        # kernels.  Every segment is non-empty by the spatial-cell contract.
        row_ids = torch.arange(segment_count, device=segment_ids.device).unsqueeze(1)
        membership = row_ids.eq(segment_ids.unsqueeze(0))
        segmented_logits = work.unsqueeze(0).expand(segment_count, -1).masked_fill(
            ~membership, -torch.inf
        )
        segmented_weights = F.softmax(segmented_logits, dim=-1)
        weights = segmented_weights.gather(0, segment_ids.unsqueeze(0)).squeeze(0)
        return weights.to(logits.dtype)

    def _segment_pool(
        self,
        *,
        native: torch.Tensor,
        adapter: torch.Tensor,
        normalized_positions: torch.Tensor,
        query: torch.Tensor,
        token_indices: torch.Tensor,
        segment_ids: torch.Tensor,
        segment_count: int,
        value_proj: torch.nn.Linear,
        query_proj: torch.nn.Linear,
        position_proj: torch.nn.Linear,
        score_proj: torch.nn.Linear,
    ) -> tuple[torch.Tensor, torch.Tensor]:
        edge_adapter = adapter.index_select(0, token_indices)
        score_hidden = value_proj(edge_adapter)
        score_hidden = score_hidden + query_proj(query).unsqueeze(0)
        score_hidden = score_hidden + position_proj(normalized_positions.index_select(0, token_indices))
        logits = score_proj(torch.tanh(score_hidden)).squeeze(-1)
        weights = self._segment_softmax(logits, segment_ids, segment_count)

        pooled_native = native.new_zeros((segment_count, native.shape[-1]))
        pooled_native.index_add_(
            0,
            segment_ids,
            native.index_select(0, token_indices) * weights.to(native.dtype).unsqueeze(-1),
        )
        pooled_adapter = adapter.new_zeros((segment_count, adapter.shape[-1]))
        pooled_adapter.index_add_(
            0,
            segment_ids,
            edge_adapter * weights.to(adapter.dtype).unsqueeze(-1),
        )
        return pooled_native, pooled_adapter

    @staticmethod
    def _position_features(
        positions: torch.Tensor,
        temporal: int,
        height: int,
        width: int,
        *,
        dtype: torch.dtype,
    ) -> torch.Tensor:
        values = positions.to(dtype=dtype)
        denominators = values.new_tensor(
            [max(temporal - 1, 1), max(height - 1, 1), max(width - 1, 1)]
        )
        normalized = values / denominators
        area = values.new_zeros((values.shape[0], 1))
        return torch.cat([normalized, area], dim=-1)

    def _decorate(
        self,
        tokens: torch.Tensor,
        positions: torch.Tensor,
        granularity: int,
        temporal: int,
        height: int,
        width: int,
    ) -> torch.Tensor:
        type_ids = torch.full(
            (tokens.shape[0],), granularity, dtype=torch.long, device=tokens.device
        )
        position_features = self._position_features(
            positions,
            temporal,
            height,
            width,
            dtype=self.output_position.weight.dtype,
        )
        return (
            tokens
            + self.granularity_embedding(type_ids).to(tokens.dtype)
            + self.output_position(position_features).to(tokens.dtype)
        )

    def _compress_one(
        self,
        native: torch.Tensor,
        grid_thw,
        query_embedding: torch.Tensor | None,
        spatial_merge_size: int,
    ) -> tuple[torch.Tensor, torch.Tensor, dict[str, torch.Tensor], dict[str, torch.Tensor]]:
        temporal, height, width = merged_grid_shape(grid_thw, spatial_merge_size)
        expected = temporal * height * width
        if native.shape != (expected, self.hidden_size):
            raise ValueError(
                f"MGVB expected native embeddings {(expected, self.hidden_size)}, got {tuple(native.shape)}"
            )
        native_positions = native_visual_positions(
            grid_thw, spatial_merge_size, device=native.device
        )
        zero = native.sum() * 0.0
        if expected <= self.token_budget:
            metrics = {
                "mgvb/native_visual_tokens": native.new_tensor(float(expected)),
                "mgvb/compact_visual_tokens": native.new_tensor(float(expected)),
                "mgvb/compression_ratio": native.new_tensor(1.0),
                "mgvb/global_tokens": native.new_tensor(0.0),
                "mgvb/region_tokens": native.new_tensor(0.0),
                "mgvb/fine_tokens": native.new_tensor(float(expected)),
                "mgvb/bypass_ratio": native.new_tensor(1.0),
            }
            return native, native_positions, metrics, {"reconstruction": zero, "diversity": zero}

        adapter = self.input_proj(self.input_norm(native))
        query = self._query(query_embedding, adapter)
        normalized_positions = self._normalized_coordinates(
            temporal,
            height,
            width,
            device=native.device,
            dtype=adapter.dtype,
        )

        conditioned_queries = self.global_queries.to(adapter.dtype)
        conditioned_queries = conditioned_queries + self.global_query_condition(query).unsqueeze(0)
        head_dim = self.adapter_dim // self.num_global_heads
        global_query_heads = conditioned_queries.view(
            self.global_tokens, self.num_global_heads, head_dim
        )
        global_key_heads = self.global_key(adapter).view(
            expected, self.num_global_heads, head_dim
        )
        global_value_heads = self.global_value(adapter).view(
            expected, self.num_global_heads, head_dim
        )
        global_logits = torch.einsum(
            "ghd,nhd->ghn", global_query_heads.float(), global_key_heads.float()
        ) / math.sqrt(head_dim)
        global_weights = F.softmax(global_logits, dim=-1).to(adapter.dtype)
        # Average the head maps for a stable direct native-feature path; the
        # learned multi-head values supply the branch residual.
        global_native = global_weights.mean(dim=1).to(native.dtype).matmul(native)
        global_adapter = torch.einsum(
            "ghn,nhd->ghd", global_weights, global_value_heads
        ).reshape(self.global_tokens, self.adapter_dim)
        global_tokens = global_native + self.global_residual(global_adapter).to(native.dtype)

        region_cells = partition_spatial_grid(temporal, height, width, self.region_tokens)
        region_token_indices, region_ids = cell_edges(
            region_cells,
            height,
            width,
            halo=1,
            device=native.device,
        )
        region_native, region_adapter = self._segment_pool(
            native=native,
            adapter=adapter,
            normalized_positions=normalized_positions,
            query=query,
            token_indices=region_token_indices,
            segment_ids=region_ids,
            segment_count=self.region_tokens,
            value_proj=self.region_value,
            query_proj=self.region_query,
            position_proj=self.region_position,
            score_proj=self.region_score,
        )
        region_tokens = region_native + self.region_residual(region_adapter).to(native.dtype)

        fine_cells = partition_spatial_grid(temporal, height, width, self.fine_tokens)
        fine_token_indices, fine_ids = cell_edges(
            fine_cells,
            height,
            width,
            device=native.device,
        )
        fine_native, fine_adapter = self._segment_pool(
            native=native,
            adapter=adapter,
            normalized_positions=normalized_positions,
            query=query,
            token_indices=fine_token_indices,
            segment_ids=fine_ids,
            segment_count=self.fine_tokens,
            value_proj=self.fine_value,
            query_proj=self.fine_query,
            position_proj=self.fine_position,
            score_proj=self.fine_score,
        )
        fine_tokens = fine_native + self.fine_residual(fine_adapter).to(native.dtype)

        positions = build_mgvb_visual_positions(
            grid_thw,
            spatial_merge_size=spatial_merge_size,
            token_budget=self.token_budget,
            global_tokens=self.global_tokens,
            region_tokens=self.region_tokens,
            device=native.device,
        )
        global_positions = positions[: self.global_tokens]
        region_positions = positions[
            self.global_tokens : self.global_tokens + self.region_tokens
        ]
        fine_positions = positions[self.global_tokens + self.region_tokens :]
        global_tokens = self._decorate(
            global_tokens, global_positions, 0, temporal, height, width
        )
        region_tokens = self._decorate(
            region_tokens, region_positions, 1, temporal, height, width
        )
        fine_tokens = self._decorate(
            fine_tokens, fine_positions, 2, temporal, height, width
        )
        compact = torch.cat([global_tokens, region_tokens, fine_tokens], dim=0)
        if compact.shape != (self.token_budget, self.hidden_size):
            raise RuntimeError(f"MGVB emitted invalid compact shape {tuple(compact.shape)}")

        reconstruction_loss = zero.float()
        diversity_loss = zero.float()
        if self.training and torch.is_grad_enabled():
            region_assignment = cell_assignment(
                region_cells, height, width, device=native.device
            )
            fine_assignment = cell_assignment(fine_cells, height, width, device=native.device)
            reconstruction_context = (
                global_tokens.mean(dim=0, keepdim=True)
                + region_tokens.index_select(0, region_assignment)
                + fine_tokens.index_select(0, fine_assignment)
            ) / 3.0
            reconstruction_context = reconstruction_context + self.reconstruction_position(
                normalized_positions.to(self.reconstruction_position.weight.dtype)
            ).to(reconstruction_context.dtype)
            reconstruction = self.reconstruction_fc2(
                F.gelu(self.reconstruction_fc1(self.reconstruction_norm(reconstruction_context)))
            )
            target = native.detach()
            reconstruction_loss = (
                1.0 - F.cosine_similarity(reconstruction.float(), target.float(), dim=-1).mean()
            ) + 0.1 * F.smooth_l1_loss(reconstruction.float(), target.float())

            normalized_global = F.normalize(global_tokens.float(), p=2, dim=-1)
            similarities = normalized_global.matmul(normalized_global.transpose(0, 1)).square()
            off_diagonal = 1.0 - torch.eye(
                self.global_tokens,
                device=similarities.device,
                dtype=similarities.dtype,
            )
            diversity_loss = (similarities * off_diagonal).sum() / max(
                self.global_tokens * (self.global_tokens - 1), 1
            )

        metrics = {
            "mgvb/native_visual_tokens": native.new_tensor(float(expected)),
            "mgvb/compact_visual_tokens": native.new_tensor(float(self.token_budget)),
            "mgvb/compression_ratio": native.new_tensor(float(self.token_budget / expected)),
            "mgvb/global_tokens": native.new_tensor(float(self.global_tokens)),
            "mgvb/region_tokens": native.new_tensor(float(self.region_tokens)),
            "mgvb/fine_tokens": native.new_tensor(float(self.fine_tokens)),
            "mgvb/bypass_ratio": native.new_tensor(0.0),
        }
        return compact, positions, metrics, {
            "reconstruction": reconstruction_loss,
            "diversity": diversity_loss,
        }

    def forward(
        self,
        image_embeddings: Iterable[torch.Tensor],
        *,
        image_grid_thw: Sequence[torch.Tensor] | torch.Tensor,
        query_embeddings: Sequence[torch.Tensor | None] | None = None,
        spatial_merge_size: int = 1,
    ) -> MGVBForwardOutput:
        image_embeddings = list(image_embeddings)
        if len(image_embeddings) != len(image_grid_thw):
            raise ValueError(
                f"MGVB received {len(image_embeddings)} image tensors but {len(image_grid_thw)} grids"
            )
        if query_embeddings is not None and len(query_embeddings) != len(image_embeddings):
            raise ValueError(
                f"MGVB received {len(query_embeddings)} queries for {len(image_embeddings)} images"
            )

        outputs: list[torch.Tensor] = []
        positions: list[torch.Tensor] = []
        all_metrics: dict[str, list[torch.Tensor]] = {}
        all_losses: dict[str, list[torch.Tensor]] = {"reconstruction": [], "diversity": []}
        for index, native in enumerate(image_embeddings):
            query = query_embeddings[index] if query_embeddings is not None else None
            compact, coords, metrics, losses = self._compress_one(
                native,
                image_grid_thw[index],
                query,
                spatial_merge_size,
            )
            outputs.append(compact)
            positions.append(coords)
            for key, value in metrics.items():
                all_metrics.setdefault(key, []).append(value.detach().float())
            for key, value in losses.items():
                all_losses[key].append(value)

        self.unimodel_last_mgvb_metrics = {
            key: torch.stack(values).mean() for key, values in all_metrics.items() if values
        }
        self.unimodel_last_mgvb_losses = {
            # Additive image numerators; normalize against the original logical
            # batch in the engine, never against this execution microbatch.
            key: torch.stack(values).sum() for key, values in all_losses.items() if values
        }
        return MGVBForwardOutput(outputs, positions)


def attach_mgvb(model: torch.nn.Module | list[torch.nn.Module], *, hf_config: Any) -> int:
    if not is_mgvb_enabled(hf_config):
        return 0
    if _as_bool(getattr(hf_config, "unimodel_mgve_enable", False)):
        raise ValueError("UNIMODEL_MGVB_ENABLE and UNIMODEL_MGVE_ENABLE cannot both be true")

    roots = model if isinstance(model, list) else [model]
    attached = 0
    for root in roots:
        while hasattr(root, "module"):
            root = root.module
        if not getattr(root, "pre_process", True):
            continue
        if hasattr(root, "unimodel_mgvb"):
            raise RuntimeError("UniModel MGVB was attached more than once")
        language_model = getattr(root, "language_model", None)
        hidden_size = int(
            getattr(
                getattr(language_model, "config", None),
                "hidden_size",
                getattr(getattr(hf_config, "text_config", None), "hidden_size", 0),
            )
        )
        if hidden_size < 1:
            raise ValueError("cannot infer hidden_size for UniModel MGVB")
        reference = next(root.parameters(), None)
        module = MultiGranularityVisualBottleneck(
            hidden_size,
            adapter_dim=int(getattr(hf_config, "unimodel_mgvb_adapter_dim", 512)),
            token_budget=int(
                getattr(
                    hf_config,
                    "unimodel_mgvb_token_budget",
                    getattr(hf_config, "unimodel_mgvb_total_budget", 256),
                )
            ),
            global_tokens=int(getattr(hf_config, "unimodel_mgvb_global_tokens", 8)),
            region_tokens=int(getattr(hf_config, "unimodel_mgvb_region_tokens", 64)),
            num_global_heads=int(getattr(hf_config, "unimodel_mgvb_num_global_heads", 8)),
            device=reference.device if reference is not None else None,
            dtype=reference.dtype if reference is not None else None,
        )
        for parameter in module.parameters():
            setattr(parameter, "average_gradients_across_tp_domain", True)
        root.unimodel_mgvb = module
        attached += 1
    return attached


def _iter_roots(model: torch.nn.Module | list[torch.nn.Module]):
    roots = model if isinstance(model, list) else [model]
    for root in roots:
        while hasattr(root, "module"):
            root = root.module
        yield root


def reset_mgvb_state(model: torch.nn.Module | list[torch.nn.Module]) -> None:
    for root in _iter_roots(model):
        mgvb = getattr(root, "unimodel_mgvb", None)
        if mgvb is not None:
            mgvb.unimodel_last_mgvb_metrics = None
            mgvb.unimodel_last_mgvb_losses = None


def collect_mgvb_metrics(model: torch.nn.Module | list[torch.nn.Module]) -> dict[str, torch.Tensor]:
    collected: dict[str, list[torch.Tensor]] = {}
    for root in _iter_roots(model):
        mgvb = getattr(root, "unimodel_mgvb", None)
        metrics = getattr(mgvb, "unimodel_last_mgvb_metrics", None) if mgvb is not None else None
        if not metrics:
            continue
        for key, value in metrics.items():
            collected.setdefault(key, []).append(value.detach().float())
    return {key: torch.stack(values).mean() for key, values in collected.items() if values}


def mgvb_auxiliary_loss(
    model: torch.nn.Module | list[torch.nn.Module],
    *,
    hf_config: Any,
    device: torch.device,
    global_sample_count: int,
    dp_size: int,
) -> tuple[torch.Tensor, dict[str, torch.Tensor]]:
    """Sum image losses per logical example, averaged over the source batch.

    Text-only examples contribute zero; graph-free HNs do not contribute.
    E/OPD query-positive(-rollout) groups count as one logical example. DDP
    averages gradients, hence the DP factor on each rank's additive numerator.
    The caller cancels Megatron's microbatch averaging exactly once and applies
    the configured window denominator separately.
    """
    if global_sample_count < 1 or dp_size < 1:
        raise ValueError("MGVB requires positive source batch and DP sizes")
    scales = {
        "reconstruction": float(getattr(hf_config, "unimodel_mgvb_reconstruction_loss_scale", 0.05)),
        "diversity": float(getattr(hf_config, "unimodel_mgvb_diversity_loss_scale", 0.01)),
    }
    total = torch.zeros((), device=device)
    raw: dict[str, list[torch.Tensor]] = {key: [] for key in scales}
    for root in _iter_roots(model):
        mgvb = getattr(root, "unimodel_mgvb", None)
        losses = getattr(mgvb, "unimodel_last_mgvb_losses", None) if mgvb is not None else None
        if not losses:
            continue
        for key in scales:
            value = losses.get(key)
            if value is not None:
                raw[key].append(value.to(device=device))

    metrics: dict[str, torch.Tensor] = {}
    for key, values in raw.items():
        if not values:
            continue
        value = torch.stack(values).sum() * (dp_size / global_sample_count)
        metrics[f"mgvb/{key}_loss"] = value.detach().float()
        total = total + scales[key] * value
    if metrics:
        metrics["mgvb/aux_loss"] = total.detach().float()
    return total, metrics
