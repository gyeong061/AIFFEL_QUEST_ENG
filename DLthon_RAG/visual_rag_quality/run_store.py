from __future__ import annotations

import json
import os
import tempfile
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def atomic_write_json(path: str | Path, payload: dict[str, Any]) -> None:
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    handle, temporary_name = tempfile.mkstemp(
        dir=destination.parent,
        prefix=f".{destination.name}.",
        suffix=".tmp",
    )
    try:
        with os.fdopen(handle, "w", encoding="utf-8") as stream:
            json.dump(payload, stream, ensure_ascii=False, indent=2, sort_keys=True)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary_name, destination)
    finally:
        if os.path.exists(temporary_name):
            os.unlink(temporary_name)


class RunStore:
    """Crash-safe state and event storage for one pipeline run."""

    def __init__(self, root: str | Path, run_id: str):
        self.run_dir = Path(root) / run_id
        self.run_dir.mkdir(parents=True, exist_ok=False)
        self.state_path = self.run_dir / "run.json"
        self.event_path = self.run_dir / "events.jsonl"
        self.artifact_dir = self.run_dir / "artifacts"
        self.artifact_dir.mkdir()
        self._state: dict[str, Any] = {}

    @property
    def state(self) -> dict[str, Any]:
        return deepcopy(self._state)

    def initialize(self, payload: dict[str, Any]) -> None:
        self._state = {
            "schema_version": 1,
            "status": "running",
            "created_at": utc_now(),
            "updated_at": utc_now(),
            "steps": {},
            **payload,
        }
        atomic_write_json(self.state_path, self._state)
        self.event("run_started")

    def update(self, **changes: Any) -> None:
        self._state.update(changes)
        self._state["updated_at"] = utc_now()
        atomic_write_json(self.state_path, self._state)

    def set_step(self, name: str, status: str, **details: Any) -> None:
        steps = self._state.setdefault("steps", {})
        steps[name] = {"status": status, "updated_at": utc_now(), **details}
        self.update(steps=steps)
        self.event("step_updated", step=name, status=status, **details)

    def event(self, event_type: str, **payload: Any) -> None:
        record = {"timestamp": utc_now(), "event": event_type, **payload}
        with self.event_path.open("a", encoding="utf-8") as stream:
            stream.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")
            stream.flush()
            os.fsync(stream.fileno())

    def finish(self, status: str, **details: Any) -> None:
        if status not in {"completed", "failed"}:
            raise ValueError("run status must be completed or failed")
        self.update(status=status, finished_at=utc_now(), **details)
        self.event("run_finished", status=status)

