from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from learning_state_lib import (  # pyright: ignore[reportMissingImports]
    ALLOWED_MODES,
    ATTEMPT_KINDS,
    ATTEMPT_RESULTS,
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
    "expression_qualified",
    "evidence_checked",
    "attempt_recorded",
    "blocker_added",
}
RESULT_STATUSES = {"passed", "partial", "blocked", "needs_user_decision"}
ACTION_OBSERVATIONS = {
    "qualify-expression": {"expression_qualified", "blocker_added"},
    "verify-expression": {"evidence_checked", "blocker_added"},
    "run-retrieval": {"attempt_recorded", "blocker_added"},
    "resume-workflow": ALLOWED_OBSERVATIONS,
}


def read_result(path: Path | None) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8") if path else sys.stdin.read()
    value = json.loads(text)
    if not isinstance(value, dict):
        raise ValueError("action result must be a JSON object")
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


def normalize_artifacts(paths: Any, repo_root: Path) -> list[str]:
    if not isinstance(paths, list) or not all(isinstance(path, str) for path in paths):
        raise ValueError("artifact_paths must be an array of paths")
    return [repository_path(path, repo_root) for path in paths]


def observation_spec(observation: dict[str, Any], repo_root: Path) -> dict[str, Any]:
    event_type = observation.get("type")
    if event_type not in ALLOWED_OBSERVATIONS:
        raise ValueError(f"action result cannot emit event type: {event_type!r}")
    subject = observation.get("subject")
    payload = observation.get("payload", {})
    if not isinstance(subject, dict) or not isinstance(payload, dict):
        raise ValueError("observation requires subject and object payload")
    if not subject.get("kind") or not subject.get("id"):
        raise ValueError("observation subject requires kind and id")
    validate_identifier(str(subject["id"]), "observation subject id")
    return {
        "actor": "agent",
        "type": event_type,
        "subject": {"kind": str(subject["kind"]), "id": str(subject["id"])},
        "payload": payload,
        "evidence_refs": normalize_refs(observation.get("evidence_refs", []), repo_root),
        "caused_by": observation.get("caused_by", []),
    }


def validate_command(result: dict[str, Any], snapshot: dict[str, Any]) -> dict[str, Any]:
    command = snapshot.get("next_command")
    if not isinstance(command, dict):
        raise ValueError("project has no executable command")
    if command.get("skill") != "visual-pkm":
        raise ValueError("current command belongs to learning-harness, not visual-pkm")
    expected = {
        "command_id": command.get("id"),
        "based_on_seq": command.get("based_on_seq"),
        "skill": command.get("skill"),
        "mode": command.get("mode"),
        "action": command.get("action"),
        "subject": command.get("subject"),
    }
    for field, expected_value in expected.items():
        if result.get(field) != expected_value:
            raise ValueError(f"action result {field} does not match current command")
    if result.get("based_on_seq") != snapshot.get("derived_from_seq"):
        raise ValueError("action result is stale")
    return command


def validate_command_observations(command: dict[str, Any], observations: list[dict[str, Any]]) -> None:
    action = command["action"]
    allowed = ACTION_OBSERVATIONS.get(action, set())
    for observation in observations:
        event_type = observation.get("type")
        if event_type not in allowed:
            raise ValueError(f"{event_type} is not allowed for command action {action}")
        subject = observation.get("subject")
        if event_type in {"expression_qualified", "evidence_checked"}:
            if subject != command.get("subject"):
                raise ValueError(f"{event_type} subject must match the current command")
        if action == "run-retrieval" and event_type == "attempt_recorded":
            payload = observation.get("payload", {})
            if payload.get("scope") != "project" or payload.get("scope_id") != command.get("subject", {}).get("id"):
                raise ValueError("retrieval attempt scope must match the current project command")


def validate_observations(observations: list[dict[str, Any]], plan: dict[str, Any], snapshot: dict[str, Any]) -> None:
    known_units = {unit["id"] for unit in plan.get("units", [])}
    known_claims = {claim["id"] for claim in snapshot.get("claims", [])}
    captured_units = {unit["id"] for unit in snapshot.get("units", []) if unit.get("expression_refs")}
    qualified_units = {
        unit["id"] for unit in snapshot.get("units", []) if unit.get("expression_status") == "qualified"
    }
    for observation in observations:
        event_type = observation.get("type")
        subject = observation.get("subject", {})
        payload = observation.get("payload", {})
        subject_kind = subject.get("kind") if isinstance(subject, dict) else None
        subject_id = subject.get("id") if isinstance(subject, dict) else None
        refs = observation.get("evidence_refs", [])
        if event_type in {"expression_qualified", "evidence_checked"}:
            if subject_kind != "unit" or subject_id not in known_units:
                raise ValueError(f"{event_type} requires a known unit subject")
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


def checkpoint_spec(
    checkpoint: dict[str, Any],
    result: dict[str, Any],
    command: dict[str, Any],
    plan: dict[str, Any],
) -> dict[str, Any]:
    workflow_id = validate_identifier(str(checkpoint.get("id", "")), "workflow id")
    status = checkpoint.get("status")
    if status not in WORKFLOW_STATUSES:
        raise ValueError("workflow checkpoint status is invalid")
    if not isinstance(checkpoint.get("step"), str) or not checkpoint["step"]:
        raise ValueError("workflow checkpoint step is required")
    if not isinstance(checkpoint.get("data", {}), dict):
        raise ValueError("workflow checkpoint data must be an object")
    previous = command.get("workflow") if isinstance(command.get("workflow"), dict) else None
    unit_id = previous.get("unit_id") if previous else None
    if unit_id is None and command.get("subject", {}).get("kind") == "unit":
        unit_id = command["subject"]["id"]
    if unit_id is not None and unit_id not in {unit["id"] for unit in plan.get("units", [])}:
        raise ValueError("workflow checkpoint references an unknown unit")
    return {
        "actor": "agent",
        "type": "workflow_updated",
        "subject": {"kind": "workflow", "id": workflow_id},
        "payload": {
            "mode": result["mode"],
            "unit_id": unit_id,
            "status": status,
            "step": checkpoint["step"],
            "data": checkpoint.get("data", {}),
        },
    }


def validate_result_shape(result: dict[str, Any], repo_root: Path) -> list[str]:
    if result.get("skill") != "visual-pkm":
        raise ValueError("action result skill must be visual-pkm")
    if result.get("mode") not in ALLOWED_MODES:
        raise ValueError("action result mode is invalid")
    if result.get("status") not in RESULT_STATUSES:
        raise ValueError("action result status is invalid")
    needs_decision = result.get("needs_user_decision")
    if not isinstance(needs_decision, bool):
        raise ValueError("needs_user_decision must be boolean")
    if (result["status"] == "needs_user_decision") != needs_decision:
        raise ValueError("needs_user_decision must match result status")
    for field in ("gaps", "open_questions"):
        value = result.get(field)
        if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
            raise ValueError(f"{field} must be an array of strings")
    return normalize_artifacts(result.get("artifact_paths"), repo_root)


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate and atomically apply one visual-pkm action result.")
    parser.add_argument("--repo-root", type=Path, required=True)
    parser.add_argument("--state-dir", type=Path)
    parser.add_argument("--file", type=Path, help="Action result JSON file; defaults to stdin")
    args = parser.parse_args()

    repo_root = args.repo_root.expanduser().resolve()
    state_dir = resolve_state_dir(repo_root, args.state_dir)
    try:
        result = read_result(args.file)
        project_id = result.get("project_id")
        if not isinstance(project_id, str):
            raise ValueError("action result project_id is required")
        validate_result_shape(result, repo_root)
        directory, plan, _events, snapshot_before = load_project(state_dir, project_id)
        command = validate_command(result, snapshot_before)
        observations = result.get("observations")
        if not isinstance(observations, list) or not all(isinstance(item, dict) for item in observations):
            raise ValueError("observations must be an array of objects")
        validate_command_observations(command, observations)
        validate_observations(observations, plan, snapshot_before)
        specs = [observation_spec(item, repo_root) for item in observations]

        checkpoint = result.get("workflow_checkpoint")
        if checkpoint is not None:
            if not isinstance(checkpoint, dict):
                raise ValueError("workflow_checkpoint must be an object or null")
            specs.append(checkpoint_spec(checkpoint, result, command, plan))
        if result["status"] == "blocked":
            has_blocker = any(spec.get("type") == "blocker_added" for spec in specs)
            checkpoint_blocked = isinstance(checkpoint, dict) and checkpoint.get("status") == "blocked"
            if not has_blocker and not checkpoint_blocked:
                raise ValueError("blocked result requires a blocker observation or blocked workflow checkpoint")
        if not specs:
            raise ValueError("action result contains no state observations or workflow checkpoint")

        records, snapshot = append_events(directory, plan, specs)
        set_active_project(state_dir, project_id)
    except (FileNotFoundError, ValueError, json.JSONDecodeError) as exc:
        parser.exit(2, f"ERROR: {exc}\n")

    print(
        json.dumps(
            {
                "project_id": project_id,
                "command_id": result["command_id"],
                "events": [record["id"] for record in records],
                "state_seq": snapshot["derived_from_seq"],
                "next_command": snapshot.get("next_command"),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
