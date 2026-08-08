from __future__ import annotations

from collections import defaultdict
from pathlib import Path
from typing import Any, Mapping

import numpy as np

from .run_store import atomic_write_json


def _indexed_rows(artifact: Mapping[str, Any]) -> dict[str, Mapping[str, Any]]:
    rows = artifact.get("per_query", [])
    indexed = {str(row["query_id"]): row for row in rows}
    if len(indexed) != len(rows):
        raise ValueError("evaluation artifact contains duplicate query IDs")
    return indexed


def validate_comparable(baseline: Mapping[str, Any], candidate: Mapping[str, Any]) -> None:
    for field in ("corpus_hash", "eval_set_hash", "metric", "k"):
        if baseline.get(field) != candidate.get(field):
            raise ValueError(f"cannot compare: {field} differs")
    baseline_ids = set(_indexed_rows(baseline))
    candidate_ids = set(_indexed_rows(candidate))
    if baseline_ids != candidate_ids:
        missing = sorted(baseline_ids - candidate_ids)
        extra = sorted(candidate_ids - baseline_ids)
        raise ValueError(f"cannot compare: query IDs differ; missing={missing[:3]}, extra={extra[:3]}")


def compare_paired(
    baseline: Mapping[str, Any],
    candidate: Mapping[str, Any],
    *,
    bootstrap_samples: int = 5000,
    confidence: float = 0.95,
    seed: int = 42,
    minimum_improvement: float = 0.0,
    regression_tolerance: float = 0.01,
) -> dict[str, Any]:
    """Compare exact queries with a group/cluster paired bootstrap."""
    validate_comparable(baseline, candidate)
    metric = str(baseline["metric"])
    baseline_rows = _indexed_rows(baseline)
    candidate_rows = _indexed_rows(candidate)
    query_ids = sorted(baseline_rows)

    groups: dict[str, list[float]] = defaultdict(list)
    query_deltas: list[dict[str, Any]] = []
    for query_id in query_ids:
        left, right = baseline_rows[query_id], candidate_rows[query_id]
        if str(left.get("group_id", query_id)) != str(right.get("group_id", query_id)):
            raise ValueError(f"cannot compare: group_id differs for {query_id}")
        group_id = str(left.get("group_id", query_id))
        delta = float(right[metric]) - float(left[metric])
        groups[group_id].append(delta)
        query_deltas.append({"query_id": query_id, "group_id": group_id, "delta": delta})

    group_ids = sorted(groups)
    rng = np.random.default_rng(seed)
    bootstrap_means = np.empty(bootstrap_samples, dtype=np.float64)
    for index in range(bootstrap_samples):
        sampled = rng.choice(group_ids, size=len(group_ids), replace=True)
        values = [value for group_id in sampled for value in groups[str(group_id)]]
        bootstrap_means[index] = float(np.mean(values))

    alpha = (1.0 - confidence) / 2.0
    lower, upper = np.quantile(bootstrap_means, [alpha, 1.0 - alpha])
    deltas = np.array([row["delta"] for row in query_deltas], dtype=np.float64)
    wins = int(np.sum(deltas > 0))
    losses = int(np.sum(deltas < 0))
    ties = int(np.sum(deltas == 0))

    if lower > minimum_improvement:
        verdict = "improved"
    elif upper < -regression_tolerance:
        verdict = "regressed"
    else:
        verdict = "inconclusive"

    return {
        "baseline_method": baseline.get("method"),
        "candidate_method": candidate.get("method"),
        "metric": metric,
        "query_count": len(query_ids),
        "group_count": len(group_ids),
        "mean_delta": float(np.mean(deltas)),
        "confidence": confidence,
        "confidence_interval": [float(lower), float(upper)],
        "probability_above_minimum": float(np.mean(bootstrap_means > minimum_improvement)),
        "wins": wins,
        "losses": losses,
        "ties": ties,
        "minimum_improvement": minimum_improvement,
        "regression_tolerance": regression_tolerance,
        "verdict": verdict,
        "fingerprints": {
            "corpus_hash": baseline["corpus_hash"],
            "eval_set_hash": baseline["eval_set_hash"],
        },
        "per_query_delta": query_deltas,
    }


def save_comparison(path: str | Path, report: Mapping[str, Any]) -> None:
    atomic_write_json(path, dict(report))

