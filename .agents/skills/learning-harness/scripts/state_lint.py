from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path
from typing import Any

from learning_state_lib import ( # pyright: ignore[reportMissingImports]
    ACTORS,
    ALLOWED_MODES,
    ATTEMPT_KINDS,
    ATTEMPT_RESULTS,
    CLAIM_REQUIREMENTS,
    COVERAGE_LEVELS,
    DISTILLATION_DECISIONS,
    EVIDENCE_RESULTS,
    EVENT_TYPES,
    EXPRESSION_RESULTS,
    PROJECT_REQUIREMENTS,
    PROJECT_STATUSES,
    SUBJECT_KINDS,
    UNIT_REQUIREMENTS,
    WORKFLOW_STATUSES,
    reduce_snapshot,
    read_events,
    read_json,
    resolve_state_dir,
)


def repo_path(value: Any, label: str, repo_root: Path, errors: list[str], *, must_exist: bool = True) -> None:
    if not isinstance(value, str) or not value:
        errors.append(f"{label} must be a non-empty repository-relative path")
        return
    path = (repo_root / value).resolve()
    try:
        path.relative_to(repo_root)
    except ValueError:
        errors.append(f"{label} escapes repository: {value!r}")
        return
    if must_exist and not path.exists():
        errors.append(f"{label} does not exist: {value}")


def validate_refs(refs: Any, label: str, repo_root: Path, errors: list[str]) -> int:
    if not isinstance(refs, list):
        errors.append(f"{label} must be an array")
        return 0
    for index, ref in enumerate(refs):
        if not isinstance(ref, dict) or ref.get("type") != "file":
            errors.append(f"{label}[{index}] must be a file reference")
            continue
        repo_path(ref.get("path"), f"{label}[{index}].path", repo_root, errors)
    return len(refs)


def normalized_snapshot(value: dict[str, Any]) -> dict[str, Any]:
    result = copy.deepcopy(value)
    result.pop("generated_at", None)
    return result


def validate_plan(plan: Any, directory: Path, repo_root: Path, errors: list[str]) -> dict[str, Any] | None:
    if not isinstance(plan, dict):
        errors.append(f"{directory}/plan.json must be an object")
        return None
    project_id = directory.name
    if plan.get("id") != project_id:
        errors.append(f"{project_id}: plan.id must match directory name")
    for field in ("title", "focus_question", "created_at", "updated_at"):
        if not isinstance(plan.get(field), str) or not plan[field]:
            errors.append(f"{project_id}: plan.{field} must be a non-empty string")
    sources = plan.get("sources")
    if not isinstance(sources, list):
        errors.append(f"{project_id}: plan.sources must be an array")
    else:
        for index, source in enumerate(sources):
            if not isinstance(source, dict):
                errors.append(f"{project_id}: sources[{index}] must be an object")
            else:
                repo_path(source.get("path"), f"{project_id}.sources[{index}].path", repo_root, errors)
    units = plan.get("units")
    if not isinstance(units, list):
        errors.append(f"{project_id}: plan.units must be an array")
        units = []
    ids: list[str] = []
    for index, unit in enumerate(units):
        if not isinstance(unit, dict):
            errors.append(f"{project_id}: units[{index}] must be an object")
            continue
        unit_id = unit.get("id")
        if not isinstance(unit_id, str) or not unit_id:
            errors.append(f"{project_id}: units[{index}].id must be a string")
        else:
            ids.append(unit_id)
        repo_path(unit.get("source_path"), f"{project_id}.units[{index}].source_path", repo_root, errors)
    if len(ids) != len(set(ids)):
        errors.append(f"{project_id}: duplicate unit id")

    policy = plan.get("completion_policy")
    if not isinstance(policy, dict):
        errors.append(f"{project_id}: completion_policy must be an object")
    else:
        scopes = {
            "unit": UNIT_REQUIREMENTS,
            "claim": CLAIM_REQUIREMENTS,
            "project": PROJECT_REQUIREMENTS,
        }
        for scope, allowed in scopes.items():
            required = policy.get(scope, {}).get("required") if isinstance(policy.get(scope), dict) else None
            if not isinstance(required, list) or not set(required).issubset(allowed):
                errors.append(f"{project_id}: invalid {scope} completion requirements")
    if not isinstance(plan.get("constraints"), list):
        errors.append(f"{project_id}: constraints must be an array")
    return plan


def validate_event_semantics(
    event: dict[str, Any],
    known_units: set[str],
    seen_claims: set[str],
    captured_units: set[str],
    qualified_units: set[str],
    open_blockers: set[str],
    errors: list[str],
) -> None:
    event_id = event.get("id", "event")
    event_type = event.get("type")
    actor = event.get("actor")
    user_authority = {
        "project_initialized",
        "project_status_changed",
        "unit_added",
        "coverage_recorded",
        "expression_captured",
        "claim_registered",
        "distillation_decided",
        "blocker_resolved",
        "plan_adjusted",
    }
    agent_authority = {"expression_qualified", "evidence_checked", "attempt_recorded", "blocker_added", "workflow_updated"}
    if event_type in user_authority and actor != "user":
        errors.append(f"{event_id}: {event_type} must preserve user authority")
    if event_type in agent_authority and actor != "agent":
        errors.append(f"{event_id}: {event_type} must be recorded by an agent sensor")
    subject = event.get("subject", {})
    subject_id = subject.get("id")
    payload = event.get("payload", {})
    refs = event.get("evidence_refs", [])
    if event_type in {"coverage_recorded", "expression_captured", "expression_qualified", "evidence_checked"} and subject_id not in known_units:
        errors.append(f"{event_id}: unknown unit subject {subject_id!r}")
    if event_type == "coverage_recorded" and payload.get("coverage") not in COVERAGE_LEVELS:
        errors.append(f"{event_id}: invalid coverage")
    if event_type == "expression_captured":
        if not refs:
            errors.append(f"{event_id}: expression_captured requires evidence")
        captured_units.add(str(subject_id))
        qualified_units.discard(str(subject_id))
    if event_type == "expression_qualified":
        if subject_id not in captured_units:
            errors.append(f"{event_id}: expression qualification requires a captured user expression")
        if payload.get("result") not in EXPRESSION_RESULTS - {"not_requested", "pending"}:
            errors.append(f"{event_id}: invalid expression qualification")
        elif payload.get("result") == "qualified":
            qualified_units.add(str(subject_id))
        else:
            qualified_units.discard(str(subject_id))
    if event_type == "evidence_checked":
        if subject_id not in qualified_units:
            errors.append(f"{event_id}: evidence check requires a qualified user expression")
        if payload.get("result") not in EVIDENCE_RESULTS - {"not_requested", "pending"}:
            errors.append(f"{event_id}: invalid evidence result")
        if not refs:
            errors.append(f"{event_id}: evidence_checked requires source evidence")
    if event_type == "claim_registered":
        if subject_id in seen_claims:
            errors.append(f"{event_id}: duplicate claim {subject_id}")
        if not isinstance(payload.get("text"), str) or not payload["text"].strip():
            errors.append(f"{event_id}: claim text is required")
        if not set(payload.get("unit_ids", [])).issubset(known_units):
            errors.append(f"{event_id}: claim references unknown units")
        seen_claims.add(str(subject_id))
    if event_type == "distillation_decided":
        if subject_id not in seen_claims:
            errors.append(f"{event_id}: distillation references unknown claim")
        decision = payload.get("decision")
        if decision not in DISTILLATION_DECISIONS:
            errors.append(f"{event_id}: invalid distillation decision")
        if decision in {"new", "update"} and not refs:
            errors.append(f"{event_id}: {decision} requires an artifact")
    if event_type == "attempt_recorded":
        if payload.get("kind") not in ATTEMPT_KINDS or payload.get("result") not in ATTEMPT_RESULTS:
            errors.append(f"{event_id}: invalid attempt kind or result")
        if payload.get("performer", "user") not in {"user", "agent", "joint"}:
            errors.append(f"{event_id}: invalid attempt performer")
        if payload.get("scope") not in {"project", "claim"}:
            errors.append(f"{event_id}: invalid attempt scope")
        if payload.get("scope") == "claim" and payload.get("scope_id") not in seen_claims:
            errors.append(f"{event_id}: attempt references unknown claim")
        if not refs:
            errors.append(f"{event_id}: attempt requires evidence")
    if event_type == "blocker_added":
        open_blockers.add(str(subject_id))
    if event_type == "blocker_resolved":
        if subject_id not in open_blockers:
            errors.append(f"{event_id}: blocker is unknown or already closed")
        else:
            open_blockers.remove(str(subject_id))
    if event_type == "workflow_updated":
        if payload.get("mode") not in ALLOWED_MODES or payload.get("status") not in WORKFLOW_STATUSES:
            errors.append(f"{event_id}: invalid workflow mode or status")
        if not isinstance(payload.get("step"), str) or not payload["step"]:
            errors.append(f"{event_id}: workflow step is required")
    if event_type == "project_status_changed" and payload.get("status") not in PROJECT_STATUSES:
        errors.append(f"{event_id}: invalid project status")


def validate_project(directory: Path, repo_root: Path, errors: list[str], warnings: list[str]) -> tuple[int, int]:
    try:
        plan_value = read_json(directory / "plan.json")
    except (FileNotFoundError, json.JSONDecodeError) as exc:
        errors.append(f"{directory}: {exc}")
        return 0, 0
    plan = validate_plan(plan_value, directory, repo_root, errors)
    if plan is None:
        return 0, 0
    if (directory / "progress.json").exists():
        errors.append(f"{directory}: progress.json is forbidden")
    if (directory / "workflows").exists():
        errors.append(f"{directory}: mutable workflows directory is forbidden")
    try:
        events = read_events(directory)
    except (FileNotFoundError, ValueError) as exc:
        errors.append(str(exc))
        return len(plan.get("units", [])), 0
    known_units = {unit["id"] for unit in plan.get("units", []) if isinstance(unit, dict) and isinstance(unit.get("id"), str)}
    seen_claims: set[str] = set()
    captured_units: set[str] = set()
    qualified_units: set[str] = set()
    open_blockers: set[str] = set()
    for index, event in enumerate(events, start=1):
        label = f"{directory}/events.jsonl:{index}"
        expected_id = f"evt-{index:08d}"
        if event.get("seq") != index or event.get("id") != expected_id:
            errors.append(f"{label}: event sequence/id is not contiguous")
        if event.get("project_id") != plan["id"]:
            errors.append(f"{label}: project_id mismatch")
        if event.get("actor") not in ACTORS or event.get("type") not in EVENT_TYPES:
            errors.append(f"{label}: invalid actor or event type")
        subject = event.get("subject")
        if not isinstance(subject, dict) or subject.get("kind") not in SUBJECT_KINDS or not subject.get("id"):
            errors.append(f"{label}: invalid subject")
        if not isinstance(event.get("payload"), dict) or not isinstance(event.get("caused_by"), list):
            errors.append(f"{label}: payload/caused_by has invalid type")
        validate_refs(event.get("evidence_refs"), f"{label}.evidence_refs", repo_root, errors)
        validate_event_semantics(
            event,
            known_units,
            seen_claims,
            captured_units,
            qualified_units,
            open_blockers,
            errors,
        )

    try:
        stored = read_json(directory / "snapshot.json")
    except (FileNotFoundError, json.JSONDecodeError) as exc:
        errors.append(f"{directory}: {exc}")
        stored = None
    expected = reduce_snapshot(plan, events)
    if not isinstance(stored, dict) or normalized_snapshot(stored) != normalized_snapshot(expected):
        errors.append(f"{directory}: snapshot.json does not match event replay")
    elif stored.get("status") == "complete" and not stored.get("completion", {}).get("complete_by_policy"):
        errors.append(f"{directory}: complete status violates completion policy")
    elif stored.get("completion", {}).get("complete_by_policy") and stored.get("status") not in {"complete", "archived"}:
        warnings.append(f"{directory}: completion policy is satisfied; user may mark the project complete")

    projection = directory / "projections" / "tasknote.json"
    if projection.exists() and isinstance(stored, dict):
        try:
            metadata = read_json(projection)
            if metadata.get("source_seq", 0) < stored.get("derived_from_seq", 0):
                warnings.append(f"{directory}: TaskNote projection is stale")
        except json.JSONDecodeError as exc:
            errors.append(f"{projection}: {exc}")
    return len(plan.get("units", [])), len(events)


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate event replay and all Learning Harness invariants.")
    parser.add_argument("--repo-root", type=Path, required=True)
    parser.add_argument("--state-dir", type=Path)
    args = parser.parse_args()
    repo_root = args.repo_root.expanduser().resolve()
    state_dir = resolve_state_dir(repo_root, args.state_dir)
    errors: list[str] = []
    warnings: list[str] = []
    try:
        config = read_json(state_dir / "config.json")
        if not isinstance(config, dict):
            errors.append(f"{state_dir}/config.json must be an object")
    except (FileNotFoundError, json.JSONDecodeError) as exc:
        errors.append(str(exc))
    project_count = unit_count = event_count = 0
    projects_root = state_dir / "projects"
    if projects_root.exists():
        for directory in sorted(path for path in projects_root.iterdir() if path.is_dir()):
            project_count += 1
            units, events = validate_project(directory, repo_root, errors, warnings)
            unit_count += units
            event_count += events
    for warning in warnings:
        print(f"WARNING: {warning}")
    for error in errors:
        print(f"ERROR: {error}")
    if errors:
        return 1
    print(f"Checked {project_count} learning projects, {unit_count} units, {event_count} events")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
