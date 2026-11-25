"""Three-stage index: mean-vector dot product (n1), 1-bit MaxSim (n2), int8 MaxSim with noise floor."""

from __future__ import annotations

from pathlib import Path
from typing import Sequence

import torch
import torch.nn.functional as F

DIM = 64
MAX_TOKENS = 128
SCALE = 127.0
N1_DEFAULT = 5000
N2_DEFAULT = 1000
NOISE_THETA = 0.38
NOISE_BETA = 2.5

_MASK_55 = 0x5555555555555555
_MASK_33 = 0x3333333333333333
_MASK_0F = 0x0F0F0F0F0F0F0F0F
_MUL_01 = 0x0101010101010101
_BYTE_WEIGHTS = torch.tensor([128, 64, 32, 16, 8, 4, 2, 1], dtype=torch.int16)


def _popcount64(x: torch.Tensor) -> torch.Tensor:
    x = x - ((x >> 1) & _MASK_55)
    x = (x & _MASK_33) + ((x >> 2) & _MASK_33)
    x = (x + (x >> 4)) & _MASK_0F
    return (x * _MUL_01) >> 56


def _pack64(codes: torch.Tensor) -> torch.Tensor:
    """int8 [..., 64] -> int64 [...]: sign bits of each row, eight bytes."""
    bits = (codes > 0).to(torch.int16).reshape(*codes.shape[:-1], 8, 8)
    packed = (bits * _BYTE_WEIGHTS).sum(dim=-1).to(torch.uint8)
    return packed.contiguous().view(torch.int64).squeeze(-1)


def _pack_rows(codes: torch.Tensor, chunk: int = 4096) -> torch.Tensor:
    """Packs [N, K, 64] in row chunks to bound the intermediate memory."""
    return torch.cat([_pack64(codes[i:i + chunk]) for i in range(0, codes.shape[0], chunk)], dim=0)


class ThreeStageIndex:
    def __init__(self, n1: int = N1_DEFAULT, n2: int = N2_DEFAULT, chunk: int = 256):
        self.n1, self.n2, self.chunk = n1, n2, chunk
        self.ids: list[str] = []
        self.modalities: list[str] = []
        self._position: dict[str, int] = {}
        self._avg: list[torch.Tensor] = []
        self._codes: list[torch.Tensor] = []
        self._frozen: dict | None = None

    def __len__(self) -> int:
        return len(self.ids)

    def add(self, doc_id: str, vectors: torch.Tensor, modality: str) -> None:
        v = vectors.float()
        v = v[v.norm(dim=-1) > 0]
        if not 0 < v.shape[0] <= MAX_TOKENS:
            raise ValueError(f"{doc_id}: {v.shape[0]} vectors, expected 1..{MAX_TOKENS}")
        if doc_id in self._position:
            raise ValueError(f"duplicate doc_id: {doc_id}")
        self._position[doc_id] = len(self.ids)
        self.ids.append(doc_id)
        self.modalities.append(modality)
        self._avg.append(F.normalize(v.mean(dim=0), dim=0))
        self._codes.append(torch.round(v * SCALE).clamp(-127, 127).to(torch.int8))
        self._frozen = None

    def _freeze(self) -> dict:
        n = len(self.ids)
        lengths_list = [c.shape[0] for c in self._codes]
        lengths = torch.tensor(lengths_list, dtype=torch.long)
        codes = torch.zeros(n, MAX_TOKENS, DIM, dtype=torch.int8)
        for i, c in enumerate(self._codes):
            codes[i, : c.shape[0]] = c
        avg = torch.stack(self._avg)
        self._frozen = self._build(avg, codes, lengths, self.modalities)
        self._avg = list(avg)
        self._codes = [codes[i, :k] for i, k in enumerate(lengths_list)]
        return self._frozen

    @staticmethod
    def _build(avg, codes, lengths, modalities) -> dict:
        by_modality: dict[str, torch.Tensor] = {}
        for name in sorted(set(modalities)):
            by_modality[name] = torch.tensor([i for i, m in enumerate(modalities) if m == name], dtype=torch.long)
        return {
            "avg": avg,
            "codes": codes,
            "bits": _pack_rows(codes),
            "valid": torch.arange(MAX_TOKENS)[None, :] < lengths[:, None],
            "by_modality": by_modality,
            "all": torch.arange(avg.shape[0], dtype=torch.long),
        }

    def search(self, query: torch.Tensor, *, weights: torch.Tensor | None = None,
               modality: str | None = None, candidates: Sequence[str] | None = None,
               topk: int = 10, n1: int | None = None, n2: int | None = None) -> list[tuple[str, float]]:
        """Top-k (doc_id, score) for one query [L, 64]; ``candidates`` restricts the pool."""
        if not self.ids:
            return []
        f = self._frozen or self._freeze()
        pool = f["by_modality"].get(modality, torch.empty(0, dtype=torch.long)) if modality else f["all"]
        if candidates is not None:
            allowed = torch.tensor([self._position[name] for name in candidates], dtype=torch.long)
            pool = pool[torch.isin(pool, allowed)]
        if pool.numel() == 0:
            return []
        n1 = self.n1 if n1 is None else n1
        n2 = self.n2 if n2 is None else n2
        u = F.normalize(query.float(), dim=-1)
        if weights is None:
            weights = torch.ones(u.shape[0])

        if n1 < pool.numel():
            mean_query = F.normalize(u.mean(dim=0), dim=0)
            s1 = f["avg"][pool] @ mean_query
            cand = pool[s1.topk(n1).indices]
        else:
            cand = pool

        if n2 < cand.numel():
            query_bits = _pack64(torch.round(u * SCALE).clamp(-127, 127).to(torch.int8))
            s2 = self._hamming_maxsim(query_bits, cand, f)
            cand = cand[s2.topk(n2).indices]

        s3 = self._noise_floor_maxsim(u, weights.float(), cand, f)
        top = s3.topk(min(topk, cand.numel()))
        return [(self.ids[int(cand[j])], float(score)) for score, j in zip(top.values, top.indices)]

    def _hamming_maxsim(self, query_bits: torch.Tensor, cand: torch.Tensor, f: dict) -> torch.Tensor:
        scores = []
        for start in range(0, cand.numel(), self.chunk):
            idx = cand[start:start + self.chunk]
            dist = _popcount64(query_bits[:, None, None] ^ f["bits"][idx][None])
            dist = dist.masked_fill(~f["valid"][idx][None], DIM)
            best = dist.amin(dim=2).float()
            scores.append((1.0 - best / DIM).sum(dim=0))
        return torch.cat(scores)

    def _noise_floor_maxsim(self, u: torch.Tensor, weights: torch.Tensor, cand: torch.Tensor, f: dict) -> torch.Tensor:
        scores = []
        for start in range(0, cand.numel(), self.chunk):
            idx = cand[start:start + self.chunk]
            sim = torch.einsum("lh,ckh->clk", u, f["codes"][idx].float()) / SCALE
            sim = sim.masked_fill(~f["valid"][idx][:, None, :], float("-inf"))
            best = sim.amax(dim=2)
            best = torch.where(torch.isfinite(best), best, torch.zeros_like(best))
            boosted = best + NOISE_BETA * F.relu(best - NOISE_THETA)
            scores.append((boosted * weights[None, :]).sum(dim=1))
        return torch.cat(scores)

    def save(self, path: str | Path) -> None:
        f = self._frozen or self._freeze()
        lengths = f["valid"].sum(dim=1)
        torch.save({"ids": self.ids, "modalities": self.modalities, "avg": f["avg"],
                    "codes": f["codes"], "lengths": lengths}, str(path))

    @classmethod
    def load(cls, path: str | Path, **kwargs) -> "ThreeStageIndex":
        blob = torch.load(str(path), map_location="cpu", weights_only=True)
        index = cls(**kwargs)
        index.ids = list(blob["ids"])
        index.modalities = list(blob["modalities"])
        index._position = {doc_id: i for i, doc_id in enumerate(index.ids)}
        index._avg = list(blob["avg"])
        index._codes = [blob["codes"][i, :n] for i, n in enumerate(blob["lengths"].tolist())]
        index._frozen = cls._build(blob["avg"], blob["codes"], blob["lengths"], index.modalities)
        return index
