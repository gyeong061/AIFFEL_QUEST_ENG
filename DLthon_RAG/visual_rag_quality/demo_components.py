from __future__ import annotations

from pathlib import Path
from typing import Any, Sequence

import numpy as np
from PIL import Image, ImageDraw

from .metrics import evaluate_rankings
from .schemas import ComicRequest, EvaluationArtifact, GeneratedPanel, Reference


class DemoRetriever:
    """Deterministic retriever used to verify the pipeline without model downloads."""

    STYLES = ("ink", "watercolor", "comic", "vector")

    def retrieve(
        self,
        *,
        style_query: str,
        reference_image: str | None,
        top_k: int,
    ) -> Sequence[Reference]:
        query = style_query.lower()
        style = next((name for name in self.STYLES if name in query), "ink")
        return [
            Reference(
                image_id=f"{style}-{index:03d}",
                path=f"demo://{style}/{index:03d}.png",
                style_id=style,
                score=1.0 - index * 0.03,
                group_id=f"demo-group-{index}",
                metadata={"demo": True, "reference_image_used": bool(reference_image)},
            )
            for index in range(top_k)
        ]


class DemoPanelGenerator:
    """Create deterministic placeholder panels and latent quality metadata."""

    def __init__(self, method: str, quality_bias: float):
        self.method = method
        self.quality_bias = quality_bias

    def generate(
        self,
        *,
        request: ComicRequest,
        panel_index: int,
        references: Sequence[Reference],
        previous_panel: GeneratedPanel | None,
        attempt: int,
        seed: int,
        output_dir: Path,
    ) -> GeneratedPanel:
        rng = np.random.default_rng(seed)
        quality = float(np.clip(self.quality_bias + 0.05 * (attempt - 1) + rng.normal(0, 0.03), 0, 1))
        base = np.array([230, 224, 205], dtype=np.int16)
        jitter = rng.integers(-25, 26, size=3)
        color = tuple(np.clip(base + jitter, 0, 255).astype(np.uint8).tolist())
        image = Image.new("RGB", (512, 512), color)
        draw = ImageDraw.Draw(image)
        draw.rectangle((24, 24, 488, 488), outline=(30, 30, 30), width=5)
        draw.ellipse((130, 90, 382, 342), outline=(30, 30, 30), width=8)
        draw.text((48, 430), f"{self.method} | panel {panel_index} | attempt {attempt}", fill=(20, 20, 20))
        filename = f"panel-{panel_index:02d}-attempt-{attempt:02d}.png"
        path = output_dir / filename
        image.save(path)
        return GeneratedPanel(
            panel_index=panel_index,
            path=str(path),
            attempt=attempt,
            seed=seed,
            metadata={
                "method": self.method,
                "latent_quality": quality,
                "previous_panel_used": previous_panel is not None,
                "reference_ids": [reference.image_id for reference in references],
            },
        )


class DemoPanelEvaluator:
    """Deterministic evaluator for exercising gates; not a real image metric."""

    def evaluate(
        self,
        *,
        request: ComicRequest,
        panel: GeneratedPanel,
        references: Sequence[Reference],
        previous_panel: GeneratedPanel | None,
    ) -> dict[str, float]:
        rng = np.random.default_rng(panel.seed + 991)
        quality = float(panel.metadata["latent_quality"])
        continuity_bonus = 0.02 if previous_panel else 0.0
        return {
            "style_fidelity": float(np.clip(quality + rng.normal(0, 0.025), 0, 1)),
            "character_consistency": float(
                np.clip(quality - 0.03 + continuity_bonus + rng.normal(0, 0.025), 0, 1)
            ),
            "scene_relevance": float(np.clip(quality + 0.02 + rng.normal(0, 0.025), 0, 1)),
            "estimated_cost_usd": 0.046,
        }


def make_demo_evaluation(method: str, quality: float, *, seed: int = 42, k: int = 5) -> EvaluationArtifact:
    """Generate paired synthetic retrieval results with shared random difficulty."""
    styles = list(DemoRetriever.STYLES)
    candidates: dict[str, dict[str, Any]] = {
        f"{style}-{index:03d}": {"style_id": style}
        for style in styles
        for index in range(50)
    }
    queries = [
        {
            "query_id": f"query-{index:03d}",
            "text": f"demo query {index}",
            "target_style_id": styles[index % len(styles)],
            "relevant_style_ids": [styles[index % len(styles)]],
            "group_id": f"content-{index // 2:03d}",
        }
        for index in range(80)
    ]

    rng = np.random.default_rng(seed)
    shared_draws = rng.random((len(queries), k))
    rankings: dict[str, list[str]] = {}
    for query_index, query in enumerate(queries):
        target = str(query["target_style_id"])
        difficulty = 0.12 * np.sin(query_index)
        threshold = float(np.clip(quality + difficulty, 0.05, 0.95))
        ranking: list[str] = []
        for rank in range(k):
            if shared_draws[query_index, rank] < threshold:
                style = target
            else:
                wrong = [style for style in styles if style != target]
                style = wrong[(query_index + rank) % len(wrong)]
            ranking.append(f"{style}-{(query_index * k + rank) % 50:03d}")
        rankings[str(query["query_id"])] = ranking

    return evaluate_rankings(
        method=method,
        corpus_hash="demo-corpus-v1",
        queries=queries,
        rankings=rankings,
        candidates=candidates,
        k=k,
        metadata={"demo": True, "quality_parameter": quality},
    )

