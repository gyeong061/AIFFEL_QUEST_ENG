from __future__ import annotations

import hashlib
import importlib.metadata
import json
import os
import platform
import random
import subprocess
import sys
from pathlib import Path
from typing import Any, Iterable

import numpy as np


def canonical_json(value: Any) -> str:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        default=str,
    )


def stable_hash(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def sha256_file(path: str | Path, chunk_size: int = 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        while chunk := stream.read(chunk_size):
            digest.update(chunk)
    return digest.hexdigest()


def fingerprint_files(paths: Iterable[str | Path], root: str | Path | None = None) -> dict[str, Any]:
    root_path = Path(root).resolve() if root else None
    records: list[dict[str, Any]] = []
    for item in sorted((Path(p).resolve() for p in paths), key=str):
        relative = str(item.relative_to(root_path)) if root_path else str(item)
        records.append(
            {
                "path": relative.replace("\\", "/"),
                "size": item.stat().st_size,
                "sha256": sha256_file(item),
            }
        )
    return {"files": records, "sha256": stable_hash(records)}


def set_global_seed(seed: int) -> None:
    os.environ["PYTHONHASHSEED"] = str(seed)
    random.seed(seed)
    np.random.seed(seed)
    try:
        import torch

        torch.manual_seed(seed)
        if torch.cuda.is_available():
            torch.cuda.manual_seed_all(seed)
        if hasattr(torch.backends, "cudnn"):
            torch.backends.cudnn.deterministic = True
            torch.backends.cudnn.benchmark = False
    except ImportError:
        pass


def git_commit(path: str | Path = ".") -> str | None:
    try:
        completed = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=Path(path),
            check=True,
            capture_output=True,
            text=True,
            timeout=5,
        )
        return completed.stdout.strip()
    except (FileNotFoundError, subprocess.SubprocessError):
        return None


def environment_snapshot(project_root: str | Path = ".") -> dict[str, Any]:
    packages = {
        dist.metadata["Name"]: dist.version
        for dist in importlib.metadata.distributions()
        if dist.metadata.get("Name")
    }
    return {
        "python": sys.version,
        "platform": platform.platform(),
        "executable": sys.executable,
        "git_commit": git_commit(project_root),
        "packages": dict(sorted(packages.items(), key=lambda pair: pair[0].lower())),
    }

