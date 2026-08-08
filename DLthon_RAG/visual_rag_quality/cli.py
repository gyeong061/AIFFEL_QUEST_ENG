from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from .comparison import compare_paired, save_comparison
from .demo_components import (
    DemoPanelEvaluator,
    DemoPanelGenerator,
    DemoRetriever,
    make_demo_evaluation,
)
from .gate import QualityGate
from .metrics import load_evaluation, save_evaluation
from .pipeline import QualityAwarePipeline
from .schemas import ComicRequest, PipelineConfig


def run_demo(config_path: str, output_path: str) -> dict[str, Any]:
    config = PipelineConfig.from_json(config_path)
    output = Path(output_path)
    run_root = output / "runs"
    evaluation_root = output / "evaluations"
    run_root.mkdir(parents=True, exist_ok=True)
    evaluation_root.mkdir(parents=True, exist_ok=True)

    request = ComicRequest(
        request_id="demo-story-001",
        story="A lost robot meets a cat on a rainy day.",
        style_query="soft ink style",
        panel_count=config.panel_count,
        seed=config.seed,
    )
    runs: dict[str, dict[str, Any]] = {}
    for method, quality in (("baseline", 0.57), ("candidate", 0.76)):
        pipeline = QualityAwarePipeline(
            retriever=DemoRetriever(),
            generator=DemoPanelGenerator(method, quality),
            evaluator=DemoPanelEvaluator(),
            panel_gate=QualityGate(config.panel_gate),
            run_gate=QualityGate(config.run_gate),
            config=config,
            run_root=run_root,
            corpus_fingerprint="demo-corpus-v1",
            project_root=Path(config_path).resolve().parent.parent,
        )
        runs[method] = pipeline.run(request, label=method)

    baseline_eval = make_demo_evaluation("baseline", 0.52, seed=config.seed)
    candidate_eval = make_demo_evaluation("candidate", 0.72, seed=config.seed)
    baseline_path = evaluation_root / "baseline.json"
    candidate_path = evaluation_root / "candidate.json"
    save_evaluation(baseline_path, baseline_eval)
    save_evaluation(candidate_path, candidate_eval)

    comparison_config = config.comparison
    report = compare_paired(
        baseline_eval.to_dict(),
        candidate_eval.to_dict(),
        bootstrap_samples=int(comparison_config.get("bootstrap_samples", 5000)),
        confidence=float(comparison_config.get("confidence", 0.95)),
        seed=config.seed,
        minimum_improvement=float(comparison_config.get("minimum_improvement", 0.0)),
        regression_tolerance=float(comparison_config.get("regression_tolerance", 0.01)),
    )
    comparison_path = output / "comparison.json"
    save_comparison(comparison_path, report)
    summary = {
        "baseline_run": str(run_root / runs["baseline"]["run_id"] / "run.json"),
        "candidate_run": str(run_root / runs["candidate"]["run_id"] / "run.json"),
        "comparison": str(comparison_path),
        "verdict": report["verdict"],
        "mean_delta": report["mean_delta"],
        "confidence_interval": report["confidence_interval"],
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return summary


def run_compare(args: argparse.Namespace) -> None:
    baseline = load_evaluation(args.baseline)
    candidate = load_evaluation(args.candidate)
    report = compare_paired(
        baseline,
        candidate,
        bootstrap_samples=args.bootstrap_samples,
        confidence=args.confidence,
        seed=args.seed,
        minimum_improvement=args.minimum_improvement,
        regression_tolerance=args.regression_tolerance,
    )
    save_comparison(args.output, report)
    print(json.dumps(report, ensure_ascii=False, indent=2))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Visual RAG quality and reproducibility tools")
    subparsers = parser.add_subparsers(dest="command", required=True)

    demo = subparsers.add_parser("demo", help="run a no-API end-to-end quality demo")
    demo.add_argument("--config", default="configs/default.json")
    demo.add_argument("--output", default="outputs/demo")

    compare = subparsers.add_parser("compare", help="compare two evaluation artifacts")
    compare.add_argument("--baseline", required=True)
    compare.add_argument("--candidate", required=True)
    compare.add_argument("--output", default="comparison.json")
    compare.add_argument("--bootstrap-samples", type=int, default=5000)
    compare.add_argument("--confidence", type=float, default=0.95)
    compare.add_argument("--seed", type=int, default=42)
    compare.add_argument("--minimum-improvement", type=float, default=0.0)
    compare.add_argument("--regression-tolerance", type=float, default=0.01)
    compare.set_defaults(handler=run_compare)
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    if args.command == "demo":
        run_demo(args.config, args.output)
    else:
        args.handler(args)


if __name__ == "__main__":
    main()
