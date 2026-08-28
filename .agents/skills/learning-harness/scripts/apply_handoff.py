from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from learning_state_lib import ( # pyright: ignore[reportMissingImports]
    ALLOWED_MODES,
    ATTEMPT_KINDS,
    ATTEMPT_RESULTS,
    COVERAGE_LEVELS,
    DISTILLATION_DECISIONS,
    EVIDENCE_RESULTS,
    EXPRESSION_RESULTS,
    WORKFLOW_STATUSES,
    append_events,
    load_project,
    repository_path,
    resolve_state_dir,
    set_active_project,
    validate_identifier,
)

ALLOWED_OBSERVATIONS = {
    "coverage_recorded",
    "expression_qualified",
    "evidence_checked",
    "claim_registered",
    "distillation_decided",
    "attempt_recorded",
    "blocker_added",
    "blocker_resolved",
}


def read_handoff(path: Path | None) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8") if path else sys.stdin.read()
    value = json.loads(text)
    if not isinstance(value, dict):
        raise ValueError("handoff must be a JSON object")
    return value


def normalize_refs(refs: Any, repo_root: Path) -> list[dict[str, Any]]:
    if not isinstance(refs, list):
        raise ValueError("evidence_refs must be an array")
    result: list[dict[str, Any]] = []
    for ref in refs:
        if not isinstance(ref, dict) or ref.get("type") != "file" or not isinstance(ref.get("path"), str):
            raise ValueError("each evidence ref must be a file reference")
        result.append(
            {
                "type": "file",
                "path": repository_path(ref["path"], repo_root),
                "locator": ref.get("locator"),
            }
        )
    return result


def observation_spec(observation: dict[str, Any], repo_root: Path) -> dict[str, Any]:
    event_type = observation.get("type")
    if event_type not in ALLOWED_OBSERVATIONS:
        raise ValueError(f"handoff cannot emit event type: {event_type!r}")
    subject = observation.get("subject")
    payload = observation.get("payload", {})
    if not isinstance(subject, dict) or not isinstance(payload, dict):
        raise ValueError("observation requires subject and object payload")
    if not subject.get("kind") or not subject.get("id"):
        raise ValueError("observation subject requires kind and id")
    validate_identifier(str(subject["id"]), "observation subject id")
    actor = "user" if event_type in {"coverage_recorded", "claim_registered", "distillation_decided", "blocker_resolved"} else "agent"
    return {
        "actor": actor,
        "type": event_type,
        "subject": {"kind": str(subject["kind"]), "id": str(subject["id"])},
        "payload": payload,
        "evidence_refs": normalize_refs(observation.get("evidence_refs", []), repo_root),
        "caused_by": observation.get("caused_by", []),
    }


def validate_observations(observations: list[dict[str, Any]], plan: dict[str, Any], snapshot: dict[str, Any]) -> None:
    known_units = {unit["id"] for unit in plan.get("units", [])}
    known_claims = {claim["id"] for claim in snapshot.get("claims", [])}
    captured_units = {unit["id"] for unit in snapshot.get("units", []) if unit.get("expression_refs")}
    qualified_units = {
        unit["id"] for unit in snapshot.get("units", []) if unit.get("expression_status") == "qualified"
    }
    open_blockers = {item["id"] for item in snapshot.get("blockers", []) if item.get("status") == "open"}
    for observation in observations:
        event_type = observation.get("type")
        subject = observation.get("subject", {})
        payload = observation.get("payload", {})
        subject_kind = subject.get("kind") if isinstance(subject, dict) else None
        subject_id = subject.get("id") if isinstance(subject, dict) else None
        refs = observation.get("evidence_refs", [])
        if event_type in {"coverage_recorded", "expression_qualified", "evidence_checked"}:
            if subject_kind != "unit" or subject_id not in known_units:
                raise ValueError(f"{event_type} requires a known unit subject")
        if event_type == "coverage_recorded" and payload.get("coverage") not in COVERAGE_LEVELS:
            raise ValueError("coverage_recorded has an invalid coverage")
        if event_type == "expression_qualified":
            if subject_id not in captured_units:
                raise ValueError("expression_qualified requires a captured user expression")
            if payload.get("result") not in EXPRESSION_RESULTS - {"not_requested", "pending"}:
                raise ValueError("expression_qualified has an invalid result")
            if payload.get("result") == "qualified":
                qualified_units.add(str(subject_id))
            else:
                qualified_units.discard(str(subject_id))
        if event_type == "evidence_checked":
            if subject_id not in qualified_units:
                raise ValueError("evidence_checked requires a qualified user expression")
            if payload.get("result") not in EVIDENCE_RESULTS - {"not_requested", "pending"} or not refs:
                raise ValueError("evidence_checked requires a valid result and source evidence")
        if event_type == "claim_registered":
            if subject_kind != "claim" or subject_id in known_claims:
                raise ValueError("claim_registered requires a new claim subject")
            if not isinstance(payload.get("text"), str) or not payload["text"].strip():
                raise ValueError("claim_registered requires user claim text")
            if not set(payload.get("unit_ids", [])).issubset(known_units):
                raise ValueError("claim_registered references an unknown unit")
            known_claims.add(str(subject_id))
        if event_type == "distillation_decided":
            decision = payload.get("decision")
            if subject_kind != "claim" or subject_id not in known_claims or decision not in DISTILLATION_DECISIONS:
                raise ValueError("distillation_decided references an invalid claim or decision")
            if decision in {"new", "update"} and not refs:
                raise ValueError(f"distillation decision {decision} requires an artifact")
        if event_type == "attempt_recorded":
            if subject_kind != "attempt":
                raise ValueError("attempt_recorded requires an attempt subject")
            if payload.get("kind") not in ATTEMPT_KINDS or payload.get("result") not in ATTEMPT_RESULTS or not refs:
                raise ValueError("attempt_recorded requires a valid kind, result, and evidence")
            if payload.get("performer", "user") not in {"user", "agent", "joint"}:
                raise ValueError("attempt_recorded has an invalid performer")
            if payload.get("scope") == "claim" and payload.get("scope_id") not in known_claims:
                raise ValueError("attempt_recorded references an unknown claim")
            if payload.get("scope") == "project" and payload.get("scope_id") != plan["id"]:
                raise ValueError("attempt_recorded references the wrong project")
        if event_type == "blocker_added":
            blocked = payload.get("blocked_subject", {})
            valid_ids = {"project": {plan["id"]}, "unit": known_units, "claim": known_claims}
            if subject_kind != "blocker" or blocked.get("id") not in valid_ids.get(blocked.get("kind"), set()):
                raise ValueError("blocker_added references an unknown subject")
            open_blockers.add(str(subject_id))
        if event_type == "blocker_resolved":
            if subject_kind != "blocker" or subject_id not in open_blockers:
                raise ValueError("blocker_resolved references an unknown or closed blocker")
            open_blockers.remove(str(subject_id))


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate and atomically apply a visual-pkm learning handoff.")
    parser.add_argument("--repo-root", type=Path, required=True)
    parser.add_argument("--state-dir", type=Path)
    parser.add_argument("--file", type=Path, help="JSON handoff file; defaults to stdin")
    args = parser.parse_args()

    repo_root = args.repo_root.expanduser().resolve()
    state_dir = resolve_state_dir(repo_root, args.state_dir)
    try:
        handoff = read_handoff(args.file)
        project_id = handoff.get("project_id")
        if not isinstance(project_id, str):
            raise ValueError("handoff.project_id is required")
        if handoff.get("skill") != "visual-pkm":
            raise ValueError("handoff.skill must be visual-pkm")
        if handoff.get("mode") not in ALLOWED_MODES:
            raise ValueError("handoff.mode is invalid")
        observations = handoff.get("observations")
        if not isinstance(observations, list):
            raise ValueError("handoff.observations must be an array")
        if not all(isinstance(item, dict) for item in observations):
            raise ValueError("every observation must be an object")
        directory, plan, _events, snapshot_before = load_project(state_dir, project_id)
        validate_observations(observations, plan, snapshot_before)
        specs = [observation_spec(item, repo_root) for item in observations]

        workflow = handoff.get("workflow")
        if workflow is not None:
            if not isinstance(workflow, dict):
                raise ValueError("handoff.workflow must be an object or null")
            workflow_id = validate_identifier(str(workflow.get("id", "")), "workflow id")
            status = workflow.get("status")
            unit_id = handoff.get("unit_id")
            if status not in WORKFLOW_STATUSES:
                raise ValueError("workflow status is invalid")
            if unit_id is not None and unit_id not in {unit["id"] for unit in plan["units"]}:
                raise ValueError("workflow references an unknown unit")
            if not isinstance(workflow.get("step"), str) or not workflow["step"]:
                raise ValueError("workflow.step is required")
            if not isinstance(workflow.get("data", {}), dict):
                raise ValueError("workflow.data must be an object")
            specs.append(
                {
                    "actor": "agent",
                    "type": "workflow_updated",
                    "subject": {"kind": "workflow", "id": workflow_id},
                    "payload": {
                        "mode": handoff["mode"],
                        "unit_id": handoff.get("unit_id"),
                        "status": status,
                        "step": workflow.get("step"),
                        "data": workflow.get("data", {}),
                    },
                }
            )
        if not specs:
            raise ValueError("handoff contains no state observations")

        records, snapshot = append_events(directory, plan, specs)
        set_active_project(state_dir, project_id)
    except (FileNotFoundError, ValueError, json.JSONDecodeError) as exc:
        parser.exit(2, f"ERROR: {exc}\n")

    print(
        json.dumps(
            {
                "project_id": project_id,
                "events": [record["id"] for record in records],
                "state_seq": snapshot["derived_from_seq"],
                "next_action": snapshot.get("next_action"),
                "suggested_next_ignored": handoff.get("suggested_next") is not None,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
