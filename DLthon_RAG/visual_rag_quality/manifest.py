from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterable, Mapping

from .reproducibility import sha256_file, stable_hash
from .run_store import atomic_write_json


REQUIRED_FIELDS = {"image_id", "path", "style_id", "group_id"}


def load_jsonl(path: str | Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    with Path(path).open("r", encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, start=1):
            if not line.strip():
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError as error:
                raise ValueError(f"invalid JSONL at line {line_number}: {error}") from error
    return records


def build_corpus_manifest(
    corpus_root: str | Path,
    records: Iterable[Mapping[str, Any]],
) -> dict[str, Any]:
    """Hash an explicit, labeled image list without storing absolute paths."""
    root = Path(corpus_root).resolve()
    normalized: list[dict[str, Any]] = []
    seen_ids: set[str] = set()

    for source in records:
        missing = REQUIRED_FIELDS - set(source)
        if missing:
            raise ValueError(f"manifest record is missing fields: {sorted(missing)}")
        image_id = str(source["image_id"])
        if image_id in seen_ids:
            raise ValueError(f"duplicate image_id: {image_id}")
        seen_ids.add(image_id)

        relative = Path(str(source["path"]))
        if relative.is_absolute():
            raise ValueError(f"manifest path must be relative: {relative}")
        absolute = (root / relative).resolve()
        try:
            absolute.relative_to(root)
        except ValueError as error:
            raise ValueError(f"manifest path escapes corpus root: {relative}") from error
        if not absolute.is_file():
            raise FileNotFoundError(absolute)

        normalized.append(
            {
                "image_id": image_id,
                "path": relative.as_posix(),
                "style_id": str(source["style_id"]),
                "group_id": str(source["group_id"]),
                "size": absolute.stat().st_size,
                "sha256": sha256_file(absolute),
                "metadata": dict(source.get("metadata", {})),
            }
        )

    normalized.sort(key=lambda row: row["image_id"])
    if not normalized:
        raise ValueError("corpus manifest must contain at least one image")
    fingerprint_payload = [
        {
            key: row[key]
            for key in ("image_id", "path", "style_id", "group_id", "size", "sha256")
        }
        for row in normalized
    ]
    return {
        "schema_version": 1,
        "image_count": len(normalized),
        "style_count": len({row["style_id"] for row in normalized}),
        "group_count": len({row["group_id"] for row in normalized}),
        "sha256": stable_hash(fingerprint_payload),
        "images": normalized,
    }


def save_manifest(path: str | Path, manifest: Mapping[str, Any]) -> None:
    atomic_write_json(path, dict(manifest))

