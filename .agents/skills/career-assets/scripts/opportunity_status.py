#!/usr/bin/env python3
"""Report stage, coverage, blockers, and next route for career opportunities."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


NEXT_ROUTES = {
    "intake": "career-positioning",
    "mapped": "resume-package",
    "packaged": "interview-package",
    "practicing": "career-assets",
    "submitted": "career-retro",
    "interviewed": "career-retro",
    "closed": "career-retro",
}


def read_object(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read JSON object {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object: {path}")
    return value


def load_claim_statuses(state_dir: Path) -> dict[str, str]:
    document = read_object(state_dir / "claims.json")
    claims = document.get("claims", [])
    if not isinstance(claims, list):
        raise ValueError("claims.json claims must be an array")
    return {
        claim["id"]: claim.get("status", "unknown")
        for claim in claims
        if isinstance(claim, dict) and isinstance(claim.get("id"), str)
    }


def manifest_summary(opportunity_dir: Path) -> list[dict[str, Any]]:
    summaries: list[dict[str, Any]] = []
    for path in sorted((opportunity_dir / "manifests").glob("*.json")):
        try:
            manifest = read_object(path)
        except (OSError, ValueError, json.JSONDecodeError):
            summaries.append({"manifest": str(path), "status": "invalid"})
            continue
        summaries.append(
            {
                "manifest": str(path),
                "artifact": manifest.get("artifact"),
                "artifact_type": manifest.get("artifact_type"),
                "status": manifest.get("status"),
            }
        )
    return summaries


def feedback_count(state_dir: Path, opportunity_id: str) -> int:
    path = state_dir / "feedback.jsonl"
    if not path.exists():
        return 0
    count = 0
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(value, dict) and value.get("opportunity_id") == opportunity_id:
            count += 1
    return count


def build_status(state_dir: Path, path: Path, claims: dict[str, str]) -> dict[str, Any]:
    opportunity = read_object(path)
    opportunity_id = opportunity.get("id", path.parent.name)
    requirements = opportunity.get("requirements", [])
    if not isinstance(requirements, list):
        requirements = []
    selected = opportunity.get("selected_claim_ids", [])
    if not isinstance(selected, list):
        selected = []

    requirement_gaps = [
        item.get("id")
        for item in requirements
        if isinstance(item, dict) and bool(item.get("gap"))
    ]
    uncovered_requirements = [
        item.get("id")
        for item in requirements
        if isinstance(item, dict) and not item.get("claim_ids")
    ]
    selected_statuses = {claim_id: claims.get(claim_id, "unknown") for claim_id in selected}
    non_confirmed = [claim_id for claim_id, status in selected_statuses.items() if status != "confirmed"]
    manifests = manifest_summary(path.parent)
    stale_artifacts = [item.get("artifact") for item in manifests if item.get("status") != "current"]

    blockers: list[str] = []
    stage = opportunity.get("stage")
    if stage != "intake" and not requirements:
        blockers.append("requirements are empty")
    if stage in {"mapped", "packaged", "practicing", "submitted", "interviewed", "closed"} and not selected:
        blockers.append("selected_claim_ids are empty")
    if non_confirmed:
        blockers.append("selected claims are not confirmed")
    if stage in {"packaged", "practicing", "submitted", "interviewed", "closed"} and not manifests:
        blockers.append("artifact manifests are missing")
    if stale_artifacts:
        blockers.append("artifacts are stale or invalid")

    return {
        "id": opportunity_id,
        "stage": stage,
        "target": opportunity.get("target"),
        "requirements": {
            "total": len(requirements),
            "gaps": requirement_gaps,
            "uncovered": uncovered_requirements,
        },
        "selected_claims": selected_statuses,
        "artifacts": manifests,
        "feedback_records": feedback_count(state_dir, str(opportunity_id)),
        "blockers": blockers,
        "recommended_next_skill": "career-evidence" if non_confirmed else NEXT_ROUTES.get(str(stage), "career-assets"),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--state-dir", type=Path, required=True)
    parser.add_argument("--opportunity-id")
    args = parser.parse_args()

    state_dir = args.state_dir.expanduser().resolve()
    try:
        claims = load_claim_statuses(state_dir)
        if args.opportunity_id:
            paths = [state_dir / "opportunities" / args.opportunity_id / "opportunity.json"]
        else:
            paths = sorted((state_dir / "opportunities").glob("*/opportunity.json"))
        statuses = [build_status(state_dir, path, claims) for path in paths]
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False))
        return 2

    print(json.dumps({"opportunities": statuses}, ensure_ascii=False, indent=2))
    return 1 if any(status["blockers"] for status in statuses) else 0


if __name__ == "__main__":
    raise SystemExit(main())
