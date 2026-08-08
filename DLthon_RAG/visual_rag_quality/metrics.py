from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path
from typing import Any, Mapping, Sequence

import numpy as np

from .reproducibility import stable_hash
from .run_store import atomic_write_json
from .schemas import EvaluationArtifact


def precision_at_k(retrieved_styles: Sequence[str], relevant_styles: set[str], k: int) -> float:
    if k < 1:
        raise ValueError("k must be at least 1")
    hits = sum(style in relevant_styles for style in retrieved_styles[:k])
    return hits / k


def average_precision_at_k(retrieved_styles: Sequence[str], relevant_styles: set[str], k: int) -> float:
    if not relevant_styles:
        raise ValueError("relevant_styles must not be empty")
    hits = 0
    accumulated = 0.0
    for rank, style in enumerate(retrieved_styles[:k], start=1):
        if style in relevant_styles:
            hits += 1
            accumulated += hits / rank
    return accumulated / min(len(relevant_styles), k)


def evaluate_rankings(
    *,
    method: str,
    corpus_hash: str,
    queries: Sequence[Mapping[str, Any]],
    rankings: Mapping[str, Sequence[str]],
    candidates: Mapping[str, Mapping[str, Any]],
    k: int = 5,
    metadata: Mapping[str, Any] | None = None,
) -> EvaluationArtifact:
    """Create a comparison-safe evaluation artifact from exact query IDs."""
    query_ids = [str(query["query_id"]) for query in queries]
    if len(query_ids) != len(set(query_ids)):
        raise ValueError("query_id must be unique")

    per_query: list[dict[str, Any]] = []
    by_style_p: dict[str, list[float]] = defaultdict(list)
    by_style_ap: dict[str, list[float]] = defaultdict(list)

    for query in queries:
        query_id = str(query["query_id"])
        if query_id not in rankings:
            raise ValueError(f"ranking is missing for query {query_id}")
        target = str(query["target_style_id"])
        relevant = set(map(str, query.get("relevant_style_ids", [target])))
        candidate_ids = list(map(str, rankings[query_id]))
        missing = [candidate_id for candidate_id in candidate_ids if candidate_id not in candidates]
        if missing:
            raise ValueError(f"unknown candidate IDs for {query_id}: {missing[:3]}")
        styles = [str(candidates[candidate_id]["style_id"]) for candidate_id in candidate_ids]
        p_value = precision_at_k(styles, relevant, k)
        ap_value = average_precision_at_k(styles, relevant, k)
        record = {
            "query_id": query_id,
            "group_id": str(query.get("group_id", query_id)),
            "target_style_id": target,
            f"precision_at_{k}": p_value,
            f"ap_at_{k}": ap_value,
            "retrieved_ids": candidate_ids[:k],
        }
        per_query.append(record)
        by_style_p[target].append(p_value)
        by_style_ap[target].append(ap_value)

    metric = f"precision_at_{k}"
    aggregate = {
        f"micro_precision_at_{k}": float(np.mean([row[metric] for row in per_query])),
        f"macro_precision_at_{k}": float(np.mean([np.mean(values) for values in by_style_p.values()])),
        f"macro_map_at_{k}": float(np.mean([np.mean(values) for values in by_style_ap.values()])),
        "query_count": len(per_query),
        "style_count": len(by_style_p),
    }
    normalized_queries = [dict(query) for query in queries]
    return EvaluationArtifact(
        method=method,
        corpus_hash=corpus_hash,
        eval_set_hash=stable_hash(normalized_queries),
        metric=metric,
        k=k,
        per_query=per_query,
        metadata={**dict(metadata or {}), "aggregate": aggregate},
    )


def save_evaluation(path: str | Path, artifact: EvaluationArtifact) -> None:
    atomic_write_json(path, artifact.to_dict())


def load_evaluation(path: str | Path) -> dict[str, Any]:
    with Path(path).open("r", encoding="utf-8") as stream:
        return json.load(stream)

