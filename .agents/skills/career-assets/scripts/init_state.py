#!/usr/bin/env python3
"""Initialize a repository-local Career Harness state directory."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Any


def write_json(path: Path, value: Any) -> bool:
    if path.exists():
        return False
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return True


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True, help="Git/project root")
    parser.add_argument("--state-dir", type=Path, help="Override state directory")
    args = parser.parse_args()

    root = args.root.expanduser().resolve()
    configured = os.environ.get("CAREER_STATE_DIR")
    state_dir = args.state_dir or (Path(configured) if configured else root / ".career")
    state_dir = state_dir.expanduser().resolve()
    state_dir.mkdir(parents=True, exist_ok=True)
    (state_dir / "opportunities").mkdir(exist_ok=True)
    (state_dir / "manifests").mkdir(exist_ok=True)

    content_prefix = "content/" if (root / "content").is_dir() else ""
    created: list[str] = []

    files = {
        "config.json": {
            "schema_version": 1,
            "paths": {
                "career_history": f"{content_prefix}Knowledge/Outputs/职业经历.md",
                "base_introduction": f"{content_prefix}Knowledge/Outputs/自我介绍.md",
                "source_roots": [f"{content_prefix}Knowledge/Sources"],
                "project_output_root": f"{content_prefix}Knowledge/Outputs",
            },
        },
        "claims.json": {
            "schema_version": 1,
            "claims": [],
        },
        "positioning.json": {
            "schema_version": 1,
            "market_title": "",
            "capability_axis": "",
            "status": "candidate",
            "base_claim_ids": [],
            "target_role_families": [],
            "open_questions": [],
        },
    }

    for name, value in files.items():
        if write_json(state_dir / name, value):
            created.append(name)

    feedback = state_dir / "feedback.jsonl"
    if not feedback.exists():
        feedback.write_text("", encoding="utf-8")
        created.append("feedback.jsonl")

    print(json.dumps({"state_dir": str(state_dir), "created": created}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
