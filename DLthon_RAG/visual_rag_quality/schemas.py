from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class ComicRequest:
    request_id: str
    story: str
    style_query: str
    panel_count: int = 4
    reference_image: str | None = None
    seed: int | None = None

    def validate(self) -> None:
        if not self.request_id.strip():
            raise ValueError("request_id must not be empty")
        if not self.story.strip():
            raise ValueError("story must not be empty")
        if not self.style_query.strip() and not self.reference_image:
            raise ValueError("style_query or reference_image is required")
        if self.panel_count < 1:
            raise ValueError("panel_count must be at least 1")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class Reference:
    image_id: str
    path: str
    style_id: str
    score: float
    group_id: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class GeneratedPanel:
    panel_index: int
    path: str
    attempt: int
    seed: int
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class PipelineConfig:
    project_name: str = "visual-rag-quality-lab"
    seed: int = 42
    top_k: int = 5
    panel_count: int = 4
    max_retries_per_panel: int = 2
    continue_after_panel_failure: bool = True
    panel_gate: dict[str, dict[str, Any]] = field(default_factory=dict)
    run_gate: dict[str, dict[str, Any]] = field(default_factory=dict)
    comparison: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_json(cls, path: str | Path) -> "PipelineConfig":
        with Path(path).open("r", encoding="utf-8") as stream:
            raw = json.load(stream)
        return cls(**raw)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class EvaluationArtifact:
    method: str
    corpus_hash: str
    eval_set_hash: str
    metric: str
    k: int
    per_query: list[dict[str, Any]]
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
