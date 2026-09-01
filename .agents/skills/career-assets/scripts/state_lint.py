#!/usr/bin/env python3
"""Validate Career Harness claims, opportunities, and artifact manifests."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

CLAIM_STATUSES = {"candidate", "confirmed", "contested", "deprecated", "reference_only"}
OWNERSHIP = {"direct", "collaborative", "team", "not_applicable"}
COMPLETION = {"implemented", "validated", "ongoing", "design_only", "planned", "unknown"}
CLAIM_KINDS = {
    "timeline",
    "positioning",
    "project_scope",
    "project_contribution",
    "result",
    "boundary",
    "failure",
    "reflection",
}
STAGES = {"intake", "mapped", "packaged", "practicing", "submitted", "interviewed", "closed"}
ARTIFACT_STATUSES = {"current", "stale", "archived"}
FEEDBACK_CLASSES = {
    "fact_gap",
    "evidence_gap",
    "positioning_gap",
    "selection_gap",
    "expression_gap",
    "delivery_error",
    "market_mismatch",
    "harness_gap",
}
NEXT_SKILLS = {
    "career-evidence",
    "career-positioning",
    "resume-package",
    "interview-package",
    "career-retro",
    "career-assets",
}


def load_json(path: Path, errors: list[str]) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        errors.append(f"missing file: {path}")
    except json.JSONDecodeError as exc:
        errors.append(f"invalid JSON: {path}: {exc}")
    return None


def require_string(value: Any, label: str, errors: list[str]) -> None:
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{label} must be a non-empty string")


def require_string_list(value: Any, label: str, errors: list[str]) -> list[str]:
    if not isinstance(value, list):
        errors.append(f"{label} must be an array")
        return []
    result: list[str] = []
    for index, item in enumerate(value):
        if not isinstance(item, str) or not item.strip():
            errors.append(f"{label}[{index}] must be a non-empty string")
        else:
            result.append(item)
    return result


def validate_feedback(state_dir: Path, claims: dict[str, dict[str, Any]], errors: list[str]) -> int:
    path = state_dir / "feedback.jsonl"
    if not path.exists():
        errors.append(f"missing file: {path}")
        return 0
    count = 0
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        count += 1
        label = f"{path}:{line_number}"
        try:
            feedback = json.loads(line)
        except json.JSONDecodeError as exc:
            errors.append(f"invalid JSONL: {label}: {exc}")
            continue
        if not isinstance(feedback, dict):
            errors.append(f"{label} must be an object")
            continue
        for field in ("id", "opportunity_id", "stage", "signal"):
            require_string(feedback.get(field), f"{label}.{field}", errors)
        opportunity_id = feedback.get("opportunity_id")
        if isinstance(opportunity_id, str) and not (state_dir / "opportunities" / opportunity_id / "opportunity.json").exists():
            errors.append(f"{label}: unknown opportunity {opportunity_id}")
        if feedback.get("classification") not in FEEDBACK_CLASSES:
            errors.append(f"{label}: invalid classification {feedback.get('classification')!r}")
        if feedback.get("next_skill") not in NEXT_SKILLS:
            errors.append(f"{label}: invalid next_skill {feedback.get('next_skill')!r}")
        affected = feedback.get("affected_claim_ids")
        if not isinstance(affected, list):
            errors.append(f"{label}: affected_claim_ids must be an array")
        else:
            for claim_id in affected:
                if claim_id not in claims:
                    errors.append(f"{label}: references unknown claim {claim_id}")
        if not isinstance(feedback.get("affected_artifacts"), list):
            errors.append(f"{label}: affected_artifacts must be an array")
    return count


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--state-dir", type=Path, required=True)
    parser.add_argument("--repo-root", type=Path, required=True)
    args = parser.parse_args()

    state_dir = args.state_dir.expanduser().resolve()
    repo_root = args.repo_root.expanduser().resolve()
    errors: list[str] = []
    warnings: list[str] = []
    resume_required_claim_ids: list[str] = []
    resume_required_artifact_types: set[str] = set()
    resume_content_check_artifact_types: set[str] = set()
    resume_content_markers: list[str] = []

    config = load_json(state_dir / "config.json", errors)
    claim_doc = load_json(state_dir / "claims.json", errors)
    positioning = load_json(state_dir / "positioning.json", errors)

    if isinstance(config, dict):
        paths = config.get("paths")
        if not isinstance(paths, dict):
            errors.append("config.paths must be an object")
        else:
            for key in ("base_introduction", "source_roots", "project_output_root"):
                if key not in paths:
                    errors.append(f"config.paths missing {key}")
        resume_policy = config.get("resume_policy", {})
        if not isinstance(resume_policy, dict):
            errors.append("config.resume_policy must be an object")
        else:
            resume_required_claim_ids = require_string_list(
                resume_policy.get("required_claim_ids", []),
                "config.resume_policy.required_claim_ids",
                errors,
            )
            resume_required_artifact_types = set(
                require_string_list(
                    resume_policy.get("required_artifact_types", []),
                    "config.resume_policy.required_artifact_types",
                    errors,
                )
            )
            resume_content_check_artifact_types = set(
                require_string_list(
                    resume_policy.get("content_check_artifact_types", []),
                    "config.resume_policy.content_check_artifact_types",
                    errors,
                )
            )
            resume_content_markers = require_string_list(
                resume_policy.get("content_markers_any", []),
                "config.resume_policy.content_markers_any",
                errors,
            )

    claims: dict[str, dict[str, Any]] = {}
    if isinstance(claim_doc, dict):
        raw_claims = claim_doc.get("claims")
        if not isinstance(raw_claims, list):
            errors.append("claims.json claims must be an array")
            raw_claims = []

        for index, claim in enumerate(raw_claims):
            label = f"claims[{index}]"
            if not isinstance(claim, dict):
                errors.append(f"{label} must be an object")
                continue
            claim_id = claim.get("id")
            require_string(claim_id, f"{label}.id", errors)
            if not isinstance(claim_id, str) or not claim_id.strip():
                continue
            if claim_id in claims:
                errors.append(f"duplicate claim id: {claim_id}")
                continue
            claims[claim_id] = claim
            require_string(claim.get("statement"), f"{claim_id}.statement", errors)
            if claim.get("kind") not in CLAIM_KINDS:
                errors.append(f"{claim_id}: invalid kind {claim.get('kind')!r}")
            if claim.get("ownership") not in OWNERSHIP:
                errors.append(f"{claim_id}: invalid ownership {claim.get('ownership')!r}")
            if claim.get("completion") not in COMPLETION:
                errors.append(f"{claim_id}: invalid completion {claim.get('completion')!r}")
            if claim.get("status") not in CLAIM_STATUSES:
                errors.append(f"{claim_id}: invalid status {claim.get('status')!r}")

            evidence = claim.get("evidence")
            if not isinstance(evidence, list):
                errors.append(f"{claim_id}: evidence must be an array")
                evidence = []
            if claim.get("status") == "confirmed" and not evidence:
                errors.append(f"{claim_id}: confirmed claim requires evidence")
            for evidence_index, item in enumerate(evidence):
                evidence_label = f"{claim_id}.evidence[{evidence_index}]"
                if not isinstance(item, dict):
                    errors.append(f"{evidence_label} must be an object")
                    continue
                evidence_type = item.get("type")
                if evidence_type == "file":
                    path = item.get("path")
                    require_string(path, f"{evidence_label}.path", errors)
                    if isinstance(path, str) and path and not (repo_root / path).exists():
                        errors.append(f"{claim_id}: evidence path does not exist: {path}")
                elif evidence_type == "user_confirmation":
                    require_string(item.get("locator"), f"{evidence_label}.locator", errors)
                else:
                    errors.append(f"{evidence_label}: unsupported type {evidence_type!r}")

            for field in ("metrics", "constraints", "tags"):
                if not isinstance(claim.get(field), list):
                    errors.append(f"{claim_id}: {field} must be an array")

    for claim_id in resume_required_claim_ids:
        claim = claims.get(claim_id)
        if claim is None:
            errors.append(f"config.resume_policy references unknown claim: {claim_id}")
        elif claim.get("status") != "confirmed":
            errors.append(f"config.resume_policy requires non-confirmed claim: {claim_id}")

    if isinstance(positioning, dict):
        if positioning.get("status") not in {"candidate", "confirmed", "contested"}:
            errors.append(f"invalid positioning.status: {positioning.get('status')!r}")
        for claim_id in positioning.get("base_claim_ids", []):
            if claim_id not in claims:
                errors.append(f"positioning references unknown claim: {claim_id}")

    opportunity_files = sorted((state_dir / "opportunities").glob("*/opportunity.json"))
    for path in opportunity_files:
        opportunity = load_json(path, errors)
        if not isinstance(opportunity, dict):
            continue
        opportunity_id = opportunity.get("id")
        require_string(opportunity_id, f"{path}.id", errors)
        if isinstance(opportunity_id, str) and opportunity_id != path.parent.name:
            errors.append(f"{path}: id must match directory name")
        stage = opportunity.get("stage")
        if stage not in STAGES:
            errors.append(f"{path}: invalid stage {stage!r}")
        selected = opportunity.get("selected_claim_ids", [])
        if not isinstance(selected, list):
            errors.append(f"{path}: selected_claim_ids must be an array")
            selected = []
        for claim_id in selected:
            claim = claims.get(claim_id)
            if claim is None:
                errors.append(f"{path}: unknown selected claim {claim_id}")
            elif stage in {"packaged", "practicing", "submitted", "interviewed", "closed"} and claim.get("status") != "confirmed":
                errors.append(f"{path}: outward stage uses non-confirmed claim {claim_id}")
        if opportunity.get("purpose", "application") == "application" and stage != "intake":
            for claim_id in resume_required_claim_ids:
                if claim_id not in selected:
                    errors.append(f"{path}: missing resume policy claim {claim_id}")
        requirements = opportunity.get("requirements", [])
        if not isinstance(requirements, list):
            errors.append(f"{path}: requirements must be an array")
        elif stage != "intake" and not requirements:
            warnings.append(f"{path}: stage {stage} has no requirements")

    manifest_files = sorted((state_dir / "manifests").rglob("*.json"))
    manifest_files += sorted((state_dir / "opportunities").glob("*/manifests/*.json"))
    for path in dict.fromkeys(manifest_files):
        manifest = load_json(path, errors)
        if not isinstance(manifest, dict):
            continue
        artifact = manifest.get("artifact")
        generated_by = manifest.get("generated_by")
        require_string(artifact, f"{path}.artifact", errors)
        require_string(generated_by, f"{path}.generated_by", errors)
        if isinstance(generated_by, str) and generated_by not in NEXT_SKILLS:
            errors.append(f"{path}: invalid generated_by {generated_by!r}")
        status = manifest.get("status")
        if status not in ARTIFACT_STATUSES:
            errors.append(f"{path}: invalid status {status!r}")
        resolved_artifact_path: Path | None = None
        if isinstance(artifact, str) and artifact:
            artifact_path = Path(artifact)
            if artifact_path.is_absolute():
                errors.append(f"{path}: artifact must be repository-relative: {artifact}")
            else:
                candidate_path = repo_root / artifact_path
                resolved_artifact_path = candidate_path
                if status == "current" and not candidate_path.exists():
                    errors.append(f"{path}: current artifact does not exist: {artifact}")
        claim_ids = manifest.get("claim_ids")
        if not isinstance(claim_ids, list):
            errors.append(f"{path}: claim_ids must be an array")
            continue
        artifact_type = manifest.get("artifact_type")
        if status == "current" and artifact_type in resume_required_artifact_types:
            for claim_id in resume_required_claim_ids:
                if claim_id not in claim_ids:
                    errors.append(f"{path}: missing resume policy claim {claim_id}")
        if (
            status == "current"
            and artifact_type in resume_content_check_artifact_types
            and resume_content_markers
            and resolved_artifact_path is not None
            and resolved_artifact_path.is_file()
        ):
            try:
                artifact_text = resolved_artifact_path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                errors.append(f"{path}: resume policy content check requires a UTF-8 text artifact")
            else:
                if not any(marker in artifact_text for marker in resume_content_markers):
                    errors.append(f"{path}: artifact must contain one of {resume_content_markers!r}")
        for claim_id in claim_ids:
            claim = claims.get(claim_id)
            if claim is None:
                errors.append(f"{path}: references unknown claim {claim_id}")
            elif status == "current" and claim.get("status") != "confirmed":
                errors.append(f"{path}: current artifact uses non-confirmed claim {claim_id}")

    feedback_count = validate_feedback(state_dir, claims, errors)

    for warning in warnings:
        print(f"WARNING: {warning}")
    for error in errors:
        print(f"ERROR: {error}")
    print(
        f"Checked {len(claims)} claims, {len(opportunity_files)} opportunities, "
        f"{len(manifest_files)} manifests, {feedback_count} feedback records"
    )
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
