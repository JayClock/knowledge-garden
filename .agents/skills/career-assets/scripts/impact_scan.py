#!/usr/bin/env python3
"""Find or mark artifacts derived from changed career claims."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def load_manifest(path: Path) -> dict[str, Any] | None:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    if not isinstance(value, dict) or not isinstance(value.get("claim_ids"), list):
        return None
    if not isinstance(value.get("artifact"), str):
        return None
    return value


def manifest_paths(state_dir: Path) -> list[Path]:
    candidates = list((state_dir / "manifests").rglob("*.json"))
    candidates.extend((state_dir / "opportunities").glob("*/manifests/*.json"))
    return sorted(set(candidates))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--state-dir", type=Path, required=True)
    parser.add_argument("--claim-id", action="append", required=True)
    parser.add_argument("--mark-stale", action="store_true")
    args = parser.parse_args()

    state_dir = args.state_dir.expanduser().resolve()
    changed = set(args.claim_id)
    impacted: list[dict[str, Any]] = []

    for path in manifest_paths(state_dir):
        manifest = load_manifest(path)
        if manifest is None:
            continue
        matched = sorted(changed.intersection(manifest["claim_ids"]))
        if not matched:
            continue
        previous_status = manifest.get("status")
        if args.mark_stale and previous_status == "current":
            manifest["status"] = "stale"
            path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        impacted.append(
            {
                "manifest": str(path),
                "artifact": manifest["artifact"],
                "matched_claim_ids": matched,
                "previous_status": previous_status,
                "status": manifest.get("status"),
            }
        )

    print(json.dumps({"changed_claim_ids": sorted(changed), "impacted": impacted}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
