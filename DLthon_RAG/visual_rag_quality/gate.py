from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Mapping


@dataclass(frozen=True)
class GateCheck:
    metric: str
    value: float | None
    status: str
    message: str


@dataclass(frozen=True)
class GateReport:
    status: str
    passed: bool
    checks: list[GateCheck]

    def to_dict(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "passed": self.passed,
            "checks": [asdict(check) for check in self.checks],
        }


class QualityGate:
    """Evaluate metrics with separate warning and failure thresholds."""

    def __init__(self, rules: Mapping[str, Mapping[str, Any]]):
        self.rules = {name: dict(rule) for name, rule in rules.items()}
        self._validate_rules()

    def _validate_rules(self) -> None:
        for metric, rule in self.rules.items():
            direction = rule.get("direction", "min")
            if direction not in {"min", "max"}:
                raise ValueError(f"{metric}: direction must be min or max")
            if "fail" not in rule:
                raise ValueError(f"{metric}: fail threshold is required")
            if "warn" in rule:
                fail, warn = float(rule["fail"]), float(rule["warn"])
                if direction == "min" and warn < fail:
                    raise ValueError(f"{metric}: min-rule warn must be >= fail")
                if direction == "max" and warn > fail:
                    raise ValueError(f"{metric}: max-rule warn must be <= fail")

    def evaluate(self, metrics: Mapping[str, float]) -> GateReport:
        checks: list[GateCheck] = []
        for name, rule in self.rules.items():
            raw_value = metrics.get(name)
            if raw_value is None:
                checks.append(GateCheck(name, None, "fail", "required metric is missing"))
                continue

            value = float(raw_value)
            fail = float(rule["fail"])
            warn = float(rule.get("warn", fail))
            direction = rule.get("direction", "min")

            if direction == "min":
                if value < fail:
                    status, message = "fail", f"{value:.4f} < fail {fail:.4f}"
                elif value < warn:
                    status, message = "warn", f"{value:.4f} < warn {warn:.4f}"
                else:
                    status, message = "pass", f"{value:.4f} >= warn {warn:.4f}"
            else:
                if value > fail:
                    status, message = "fail", f"{value:.4f} > fail {fail:.4f}"
                elif value > warn:
                    status, message = "warn", f"{value:.4f} > warn {warn:.4f}"
                else:
                    status, message = "pass", f"{value:.4f} <= warn {warn:.4f}"
            checks.append(GateCheck(name, value, status, message))

        statuses = {check.status for check in checks}
        overall = "fail" if "fail" in statuses else "warn" if "warn" in statuses else "pass"
        return GateReport(status=overall, passed=overall != "fail", checks=checks)

