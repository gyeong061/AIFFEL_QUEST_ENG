from __future__ import annotations

import traceback
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Protocol, Sequence

import numpy as np

from .gate import QualityGate
from .reproducibility import environment_snapshot, set_global_seed, stable_hash
from .run_store import RunStore
from .schemas import ComicRequest, GeneratedPanel, PipelineConfig, Reference


class Retriever(Protocol):
    def retrieve(
        self,
        *,
        style_query: str,
        reference_image: str | None,
        top_k: int,
    ) -> Sequence[Reference]: ...


class PanelGenerator(Protocol):
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
    ) -> GeneratedPanel: ...


class PanelEvaluator(Protocol):
    def evaluate(
        self,
        *,
        request: ComicRequest,
        panel: GeneratedPanel,
        references: Sequence[Reference],
        previous_panel: GeneratedPanel | None,
    ) -> dict[str, float]: ...


class QualityAwarePipeline:
    def __init__(
        self,
        *,
        retriever: Retriever,
        generator: PanelGenerator,
        evaluator: PanelEvaluator,
        panel_gate: QualityGate,
        run_gate: QualityGate,
        config: PipelineConfig,
        run_root: str | Path,
        corpus_fingerprint: str,
        project_root: str | Path = ".",
    ):
        self.retriever = retriever
        self.generator = generator
        self.evaluator = evaluator
        self.panel_gate = panel_gate
        self.run_gate = run_gate
        self.config = config
        self.run_root = Path(run_root)
        self.corpus_fingerprint = corpus_fingerprint
        self.project_root = Path(project_root)

    def _new_run_id(self, label: str | None = None) -> str:
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        prefix = f"{label}-" if label else ""
        return f"{prefix}{timestamp}-{uuid.uuid4().hex[:8]}"

    @staticmethod
    def _attempt_score(record: dict[str, Any]) -> float:
        metrics = record["metrics"]
        return float(
            metrics.get("style_fidelity", 0.0)
            + metrics.get("character_consistency", 0.0)
            + metrics.get("scene_relevance", 0.0)
            - metrics.get("estimated_cost_usd", 0.0)
        )

    def run(self, request: ComicRequest, *, label: str | None = None) -> dict[str, Any]:
        request.validate()
        seed = request.seed if request.seed is not None else self.config.seed
        set_global_seed(seed)
        run_id = self._new_run_id(label)
        store = RunStore(self.run_root, run_id)
        config_dict = self.config.to_dict()
        store.initialize(
            {
                "run_id": run_id,
                "request": request.to_dict(),
                "seed": seed,
                "config": config_dict,
                "fingerprints": {
                    "config_hash": stable_hash(config_dict),
                    "corpus_hash": self.corpus_fingerprint,
                },
                "environment": environment_snapshot(self.project_root),
            }
        )

        try:
            store.set_step("retrieval", "running")
            references = list(
                self.retriever.retrieve(
                    style_query=request.style_query,
                    reference_image=request.reference_image,
                    top_k=self.config.top_k,
                )
            )
            if not references:
                raise RuntimeError("retriever returned no references")
            if len({reference.image_id for reference in references}) != len(references):
                raise RuntimeError("retriever returned duplicate image IDs")
            store.set_step(
                "retrieval",
                "completed",
                references=[reference.to_dict() for reference in references],
            )

            selected_panels: list[GeneratedPanel] = []
            panel_records: list[dict[str, Any]] = []
            previous_panel: GeneratedPanel | None = None

            for panel_index in range(1, request.panel_count + 1):
                step_name = f"panel_{panel_index:02d}"
                store.set_step(step_name, "running")
                attempts: list[dict[str, Any]] = []
                accepted: GeneratedPanel | None = None

                for attempt in range(1, self.config.max_retries_per_panel + 2):
                    attempt_seed = seed + panel_index * 10_000 + attempt
                    panel = self.generator.generate(
                        request=request,
                        panel_index=panel_index,
                        references=references,
                        previous_panel=previous_panel,
                        attempt=attempt,
                        seed=attempt_seed,
                        output_dir=store.artifact_dir,
                    )
                    metrics = self.evaluator.evaluate(
                        request=request,
                        panel=panel,
                        references=references,
                        previous_panel=previous_panel,
                    )
                    report = self.panel_gate.evaluate(metrics)
                    attempt_record = {
                        "attempt": attempt,
                        "panel": panel.to_dict(),
                        "metrics": metrics,
                        "gate": report.to_dict(),
                    }
                    attempts.append(attempt_record)
                    store.set_step(step_name, "running", attempts=attempts)
                    if report.passed:
                        accepted = panel
                        break

                best = max(attempts, key=self._attempt_score)
                selected = accepted or GeneratedPanel(**best["panel"])
                selected_panels.append(selected)
                previous_panel = selected
                panel_status = "completed" if accepted else "failed"
                panel_record = {
                    "panel_index": panel_index,
                    "status": panel_status,
                    "selected_attempt": selected.attempt,
                    "attempts": attempts,
                }
                panel_records.append(panel_record)
                store.set_step(
                    step_name,
                    panel_status,
                    panel_index=panel_index,
                    selected_attempt=selected.attempt,
                    attempts=attempts,
                )
                if not accepted and not self.config.continue_after_panel_failure:
                    break

            selected_metrics: list[dict[str, float]] = []
            for panel_record in panel_records:
                selected_attempt = panel_record["selected_attempt"]
                match = next(
                    item for item in panel_record["attempts"] if item["attempt"] == selected_attempt
                )
                selected_metrics.append(match["metrics"])

            quality_metrics = ("style_fidelity", "character_consistency", "scene_relevance")
            aggregate = {
                name: float(np.mean([metrics[name] for metrics in selected_metrics]))
                for name in quality_metrics
            }
            aggregate["total_cost_usd"] = float(
                sum(metrics.get("estimated_cost_usd", 0.0) for metrics in selected_metrics)
            )
            run_report = self.run_gate.evaluate(aggregate)
            failed_panels = [row["panel_index"] for row in panel_records if row["status"] == "failed"]
            status = "completed" if not failed_panels and run_report.passed else "failed"
            store.finish(
                status,
                panels=panel_records,
                aggregate_metrics=aggregate,
                run_gate=run_report.to_dict(),
                failed_panels=failed_panels,
            )
            return store.state
        except Exception as error:
            store.event(
                "unhandled_error",
                error_type=type(error).__name__,
                message=str(error),
                traceback=traceback.format_exc(),
            )
            store.finish(
                "failed",
                error={"type": type(error).__name__, "message": str(error)},
            )
            raise
