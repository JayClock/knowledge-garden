from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

from learning_state_lib import ( # pyright: ignore[reportMissingImports]
    ALLOWED_MODES,
    ATTEMPT_KINDS,
    ATTEMPT_RESULTS,
    CLAIM_REQUIREMENTS,
    COVERAGE_LEVELS,
    DISTILLATION_DECISIONS,
    EVIDENCE_RESULTS,
    EXPRESSION_RESULTS,
    PROJECT_REQUIREMENTS,
    PROJECT_STATUSES,
    SUBJECT_KINDS,
    UNIT_REQUIREMENTS,
    WORKFLOW_STATUSES,
    active_project_id,
    append_events,
    evidence_ref,
    load_project,
    now_iso,
    project_dir,
    read_json,
    repo_relative,
    repository_path,
    resolve_state_dir,
    set_active_project,
    validate_identifier,
    write_json_atomic,
)


def parse_unit(value: str, repo_root: Path) -> dict[str, Any]:
    unit_id, separator, source = value.partition("=")
    if not separator:
        raise ValueError("--unit must use UNIT_ID=REPOSITORY_PATH")
    validate_identifier(unit_id, "unit_id")
    source_path = repository_path(source, repo_root)
    return {"id": unit_id, "title": Path(source_path).stem, "source_path": source_path, "locator": None}


def evidence_refs(values: list[str], repo_root: Path, locator: str | None = None) -> list[dict[str, Any]]:
    return [evidence_ref(repository_path(value, repo_root), locator) for value in values]


def session_text(args: argparse.Namespace) -> str | None:
    if getattr(args, "text_file", None):
        return args.text_file.read_text(encoding="utf-8").strip()
    value = getattr(args, "text", None)
    return value.strip() if isinstance(value, str) else None


def save_session(directory: Path, repo_root: Path, project_id: str, subject_id: str, section: str, text: str) -> str:
    if not text.strip():
        raise ValueError("session text must not be empty")
    timestamp = now_iso()
    compact = re.sub(r"[^0-9]", "", timestamp)[:14]
    base = directory / "sessions" / f"{compact}-{subject_id}-{section}.md"
    path = base
    suffix = 2
    while path.exists():
        path = base.with_name(f"{base.stem}-{suffix}{base.suffix}")
        suffix += 1
    headings = {
        "expression": "用户原始表达",
        "attempt": "用户尝试",
    }
    path.write_text(
        "# Learning Session\n\n"
        f"- project: `{project_id}`\n"
        f"- subject: `{subject_id}`\n"
        f"- recorded_at: `{timestamp}`\n\n"
        f"## {headings[section]}\n\n{text.strip()}\n",
        encoding="utf-8",
    )
    return repo_relative(path, repo_root)


def event_result(records: list[dict[str, Any]], snapshot: dict[str, Any]) -> dict[str, Any]:
    return {
        "events": [record["id"] for record in records],
        "state_seq": snapshot["derived_from_seq"],
        "next_action": snapshot.get("next_action"),
    }


def initialize_project(args: argparse.Namespace, repo_root: Path, state_dir: Path) -> dict[str, Any]:
    project_id = validate_identifier(args.project_id, "project_id")
    directory = project_dir(state_dir, project_id)
    if directory.exists():
        raise FileExistsError(f"learning project already exists: {project_id}")
    units = [parse_unit(value, repo_root) for value in args.unit]
    if len({unit["id"] for unit in units}) != len(units):
        raise ValueError("duplicate unit id")
    sources = [{"path": repository_path(value, repo_root), "unit_strategy": "file"} for value in args.source]
    timestamp = now_iso()
    plan = {
        "id": project_id,
        "title": args.title,
        "focus_question": args.focus_question,
        "sources": sources,
        "units": units,
        "completion_policy": {
            "unit": {"required": args.unit_requirement or ["coverage"]},
            "claim": {"required": args.claim_requirement or ["distillation_decision"]},
            "project": {"required": args.project_requirement or ["source_grounding", "retrieval", "application"]},
        },
        "constraints": args.constraint,
        "created_at": timestamp,
        "updated_at": timestamp,
    }
    directory.mkdir(parents=True)
    (directory / "sessions").mkdir()
    (directory / "projections").mkdir()
    (directory / "events.jsonl").write_text("", encoding="utf-8")
    write_json_atomic(directory / "plan.json", plan)
    records, snapshot = append_events(
        directory,
        plan,
        [
            {
                "actor": "user",
                "type": "project_initialized",
                "subject": {"kind": "project", "id": project_id},
                "payload": {"status": args.status, "unit_count": len(units)},
            }
        ],
    )
    set_active_project(state_dir, project_id if args.status not in {"complete", "archived"} else None)
    return {"project_id": project_id, "project_dir": str(directory), **event_result(records, snapshot)}


def add_unit(args: argparse.Namespace, repo_root: Path, state_dir: Path) -> dict[str, Any]:
    directory, plan, _events, _snapshot = load_project(state_dir, args.project_id)
    validate_identifier(args.unit_id, "unit_id")
    if any(unit["id"] == args.unit_id for unit in plan["units"]):
        raise ValueError(f"duplicate unit id: {args.unit_id}")
    unit = {
        "id": args.unit_id,
        "title": args.title or Path(args.source_path).stem,
        "source_path": repository_path(args.source_path, repo_root),
        "locator": args.locator,
    }
    plan["units"].append(unit)
    plan["updated_at"] = now_iso()
    write_json_atomic(directory / "plan.json", plan)
    records, snapshot = append_events(
        directory,
        plan,
        [{"actor": "user", "type": "unit_added", "subject": {"kind": "unit", "id": args.unit_id}, "payload": unit}],
    )
    set_active_project(state_dir, args.project_id)
    return {"project_id": args.project_id, "unit_id": args.unit_id, **event_result(records, snapshot)}


def record_coverage(args: argparse.Namespace, state_dir: Path) -> dict[str, Any]:
    directory, plan, _events, _snapshot = load_project(state_dir, args.project_id)
    if not any(unit["id"] == args.unit_id for unit in plan["units"]):
        raise ValueError(f"unknown unit: {args.unit_id}")
    records, snapshot = append_events(
        directory,
        plan,
        [
            {
                "actor": "user",
                "type": "coverage_recorded",
                "subject": {"kind": "unit", "id": args.unit_id},
                "payload": {"coverage": args.coverage, "locator": args.locator},
            }
        ],
    )
    set_active_project(state_dir, args.project_id)
    return {"project_id": args.project_id, "unit_id": args.unit_id, **event_result(records, snapshot)}


def record_expression(args: argparse.Namespace, repo_root: Path, state_dir: Path) -> dict[str, Any]:
    directory, plan, _events, _snapshot = load_project(state_dir, args.project_id)
    if not any(unit["id"] == args.unit_id for unit in plan["units"]):
        raise ValueError(f"unknown unit: {args.unit_id}")
    text = session_text(args)
    if not text:
        raise ValueError("expression text is required")
    expression_path = save_session(directory, repo_root, args.project_id, args.unit_id, "expression", text)
    ref = evidence_ref(expression_path)
    specs: list[dict[str, Any]] = []
    if args.coverage:
        specs.append(
            {
                "actor": "user",
                "type": "coverage_recorded",
                "subject": {"kind": "unit", "id": args.unit_id},
                "payload": {"coverage": args.coverage, "locator": args.locator},
            }
        )
    specs.append(
        {
            "actor": "user",
            "type": "expression_captured",
            "subject": {"kind": "unit", "id": args.unit_id},
            "payload": {},
            "evidence_refs": [ref],
        }
    )
    if args.qualification != "pending":
        specs.append(
            {
                "actor": "agent",
                "type": "expression_qualified",
                "subject": {"kind": "unit", "id": args.unit_id},
                "payload": {"result": args.qualification},
                "evidence_refs": [ref],
            }
        )
    records, snapshot = append_events(directory, plan, specs)
    set_active_project(state_dir, args.project_id)
    return {"project_id": args.project_id, "unit_id": args.unit_id, "expression_ref": expression_path, **event_result(records, snapshot)}


def record_evidence_check(args: argparse.Namespace, repo_root: Path, state_dir: Path) -> dict[str, Any]:
    directory, plan, _events, snapshot = load_project(state_dir, args.project_id)
    unit = next((item for item in snapshot.get("units", []) if item["id"] == args.unit_id), None)
    if unit is None:
        raise ValueError(f"unknown unit: {args.unit_id}")
    if unit.get("expression_status") != "qualified":
        raise ValueError("evidence check requires a qualified user expression")
    refs = evidence_refs(args.evidence_ref, repo_root, args.locator)
    if not refs:
        raise ValueError("evidence check requires at least one --evidence-ref")
    records, snapshot = append_events(
        directory,
        plan,
        [
            {
                "actor": "agent",
                "type": "evidence_checked",
                "subject": {"kind": "unit", "id": args.unit_id},
                "payload": {"result": args.result, "open_questions": args.open_question},
                "evidence_refs": refs,
            }
        ],
    )
    set_active_project(state_dir, args.project_id)
    return {"project_id": args.project_id, "unit_id": args.unit_id, **event_result(records, snapshot)}


def register_claim(args: argparse.Namespace, repo_root: Path, state_dir: Path) -> dict[str, Any]:
    directory, plan, _events, snapshot = load_project(state_dir, args.project_id)
    claim_id = validate_identifier(args.claim_id, "claim_id")
    if any(claim["id"] == claim_id for claim in snapshot.get("claims", [])):
        raise ValueError(f"duplicate claim id: {claim_id}")
    unit_ids = args.unit_id
    known_units = {unit["id"] for unit in plan["units"]}
    unknown = set(unit_ids) - known_units
    if unknown:
        raise ValueError(f"unknown claim unit ids: {sorted(unknown)}")
    expression_paths = [repository_path(value, repo_root) for value in args.expression_ref]
    refs = [evidence_ref(path) for path in expression_paths]
    records, snapshot = append_events(
        directory,
        plan,
        [
            {
                "actor": "user",
                "type": "claim_registered",
                "subject": {"kind": "claim", "id": claim_id},
                "payload": {"text": args.text, "unit_ids": unit_ids, "expression_refs": refs},
                "evidence_refs": refs,
            }
        ],
    )
    set_active_project(state_dir, args.project_id)
    return {"project_id": args.project_id, "claim_id": claim_id, **event_result(records, snapshot)}


def record_distillation(args: argparse.Namespace, repo_root: Path, state_dir: Path) -> dict[str, Any]:
    directory, plan, _events, snapshot = load_project(state_dir, args.project_id)
    if not any(claim["id"] == args.claim_id for claim in snapshot.get("claims", [])):
        raise ValueError(f"unknown claim: {args.claim_id}")
    refs = evidence_refs(args.artifact, repo_root)
    if args.decision in {"new", "update"} and not refs:
        raise ValueError(f"decision {args.decision} requires at least one --artifact")
    records, snapshot = append_events(
        directory,
        plan,
        [
            {
                "actor": "user",
                "type": "distillation_decided",
                "subject": {"kind": "claim", "id": args.claim_id},
                "payload": {"decision": args.decision},
                "evidence_refs": refs,
            }
        ],
    )
    set_active_project(state_dir, args.project_id)
    return {"project_id": args.project_id, "claim_id": args.claim_id, **event_result(records, snapshot)}


def record_attempt(args: argparse.Namespace, repo_root: Path, state_dir: Path) -> dict[str, Any]:
    directory, plan, events, snapshot = load_project(state_dir, args.project_id)
    attempt_id = args.attempt_id or f"attempt-{(events[-1]['seq'] if events else 0) + 1:08d}"
    validate_identifier(attempt_id, "attempt_id")
    if any(attempt["id"] == attempt_id for attempt in snapshot.get("attempts", [])):
        raise ValueError(f"duplicate attempt id: {attempt_id}")
    if args.scope == "claim" and not any(claim["id"] == args.scope_id for claim in snapshot.get("claims", [])):
        raise ValueError(f"unknown claim scope: {args.scope_id}")
    if args.scope == "project" and args.scope_id != args.project_id:
        raise ValueError("project attempt scope-id must equal project-id")
    refs = evidence_refs(args.evidence_ref, repo_root)
    text = session_text(args)
    if text:
        path = save_session(directory, repo_root, args.project_id, attempt_id, "attempt", text)
        refs.append(evidence_ref(path))
    if not refs:
        raise ValueError("attempt requires --text, --text-file, or --evidence-ref")
    records, snapshot = append_events(
        directory,
        plan,
        [
            {
                "actor": "agent",
                "type": "attempt_recorded",
                "subject": {"kind": "attempt", "id": attempt_id},
                "payload": {
                    "scope": args.scope,
                    "scope_id": args.scope_id,
                    "kind": args.kind,
                    "result": args.result,
                    "gaps": args.gap,
                    "performer": args.performer,
                },
                "evidence_refs": refs,
            }
        ],
    )
    set_active_project(state_dir, args.project_id)
    return {"project_id": args.project_id, "attempt_id": attempt_id, **event_result(records, snapshot)}


def add_blocker(args: argparse.Namespace, state_dir: Path) -> dict[str, Any]:
    directory, plan, events, snapshot = load_project(state_dir, args.project_id)
    known_subjects = {
        "project": {args.project_id},
        "unit": {unit["id"] for unit in plan["units"]},
        "claim": {claim["id"] for claim in snapshot.get("claims", [])},
    }
    if args.subject_id not in known_subjects[args.subject_kind]:
        raise ValueError(f"unknown blocked subject: {args.subject_kind}/{args.subject_id}")
    blocker_id = args.blocker_id or f"blocker-{(events[-1]['seq'] if events else 0) + 1:08d}"
    validate_identifier(blocker_id, "blocker_id")
    records, snapshot = append_events(
        directory,
        plan,
        [
            {
                "actor": "agent",
                "type": "blocker_added",
                "subject": {"kind": "blocker", "id": blocker_id},
                "payload": {
                    "reason": args.reason,
                    "blocked_subject": {"kind": args.subject_kind, "id": args.subject_id},
                },
            }
        ],
    )
    set_active_project(state_dir, args.project_id)
    return {"project_id": args.project_id, "blocker_id": blocker_id, **event_result(records, snapshot)}


def resolve_blocker(args: argparse.Namespace, state_dir: Path) -> dict[str, Any]:
    directory, plan, _events, snapshot = load_project(state_dir, args.project_id)
    blocker = next((item for item in snapshot.get("blockers", []) if item["id"] == args.blocker_id), None)
    if blocker is None or blocker.get("status") != "open":
        raise ValueError(f"unknown or closed blocker: {args.blocker_id}")
    records, snapshot = append_events(
        directory,
        plan,
        [
            {
                "actor": "user",
                "type": "blocker_resolved",
                "subject": {"kind": "project", "id": args.blocker_id},
                "payload": {"resolution": args.resolution},
            }
        ],
    )
    set_active_project(state_dir, args.project_id)
    return {"project_id": args.project_id, "blocker_id": args.blocker_id, **event_result(records, snapshot)}


def update_workflow(args: argparse.Namespace, state_dir: Path) -> dict[str, Any]:
    directory, plan, _events, _snapshot = load_project(state_dir, args.project_id)
    if args.unit_id and not any(unit["id"] == args.unit_id for unit in plan["units"]):
        raise ValueError(f"unknown workflow unit: {args.unit_id}")
    workflow_id = validate_identifier(args.workflow_id, "workflow_id")
    data: dict[str, Any] = {}
    if args.data:
        parsed = json.loads(args.data)
        if not isinstance(parsed, dict):
            raise ValueError("--data must decode to an object")
        data = parsed
    records, snapshot = append_events(
        directory,
        plan,
        [
            {
                "actor": "agent",
                "type": "workflow_updated",
                "subject": {"kind": "workflow", "id": workflow_id},
                "payload": {
                    "mode": args.mode,
                    "unit_id": args.unit_id,
                    "status": args.status,
                    "step": args.step,
                    "data": data,
                },
            }
        ],
    )
    set_active_project(state_dir, args.project_id)
    return {"project_id": args.project_id, "workflow_id": workflow_id, **event_result(records, snapshot)}


def change_project_status(args: argparse.Namespace, state_dir: Path) -> dict[str, Any]:
    directory, plan, _events, snapshot = load_project(state_dir, args.project_id)
    if args.status == "complete" and not snapshot.get("completion", {}).get("complete_by_policy"):
        raise ValueError("completion policy is not satisfied")
    records, snapshot = append_events(
        directory,
        plan,
        [
            {
                "actor": "user",
                "type": "project_status_changed",
                "subject": {"kind": "project", "id": args.project_id},
                "payload": {"status": args.status},
            }
        ],
    )
    set_active_project(state_dir, None if args.status in {"complete", "archived"} else args.project_id)
    return {"project_id": args.project_id, "status": args.status, **event_result(records, snapshot)}


def adjust_plan(args: argparse.Namespace, state_dir: Path) -> dict[str, Any]:
    directory, plan, _events, _snapshot = load_project(state_dir, args.project_id)
    changes: dict[str, Any] = {}
    if args.focus_question:
        plan["focus_question"] = args.focus_question
        changes["focus_question"] = args.focus_question
    policy = plan["completion_policy"]
    if args.unit_requirement:
        policy["unit"]["required"] = args.unit_requirement
        changes["unit_requirements"] = args.unit_requirement
    if args.claim_requirement:
        policy["claim"]["required"] = args.claim_requirement
        changes["claim_requirements"] = args.claim_requirement
    if args.project_requirement:
        policy["project"]["required"] = args.project_requirement
        changes["project_requirements"] = args.project_requirement
    if not changes:
        raise ValueError("no plan adjustment supplied")
    plan["updated_at"] = now_iso()
    write_json_atomic(directory / "plan.json", plan)
    records, snapshot = append_events(
        directory,
        plan,
        [
            {
                "actor": "user",
                "type": "plan_adjusted",
                "subject": {"kind": "project", "id": args.project_id},
                "payload": {"changes": changes},
            }
        ],
    )
    set_active_project(state_dir, args.project_id)
    return {"project_id": args.project_id, "changes": changes, **event_result(records, snapshot)}


def add_text_source(parser: argparse.ArgumentParser) -> None:
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--text")
    group.add_argument("--text-file", type=Path)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Record Learning Harness facts as append-only events.")
    parser.add_argument("--repo-root", type=Path, required=True)
    parser.add_argument("--state-dir", type=Path)
    commands = parser.add_subparsers(dest="command", required=True)

    init = commands.add_parser("init-project")
    init.add_argument("--project-id", required=True)
    init.add_argument("--title", required=True)
    init.add_argument("--focus-question", required=True)
    init.add_argument("--source", action="append", default=[])
    init.add_argument("--unit", action="append", default=[])
    init.add_argument("--unit-requirement", action="append", choices=sorted(UNIT_REQUIREMENTS))
    init.add_argument("--claim-requirement", action="append", choices=sorted(CLAIM_REQUIREMENTS))
    init.add_argument("--project-requirement", action="append", choices=sorted(PROJECT_REQUIREMENTS))
    init.add_argument("--constraint", action="append", default=[])
    init.add_argument("--status", choices=sorted(PROJECT_STATUSES), default="active")

    add = commands.add_parser("add-unit")
    add.add_argument("--project-id", required=True)
    add.add_argument("--unit-id", required=True)
    add.add_argument("--title")
    add.add_argument("--source-path", required=True)
    add.add_argument("--locator")

    coverage = commands.add_parser("coverage")
    coverage.add_argument("--project-id", required=True)
    coverage.add_argument("--unit-id", required=True)
    coverage.add_argument("--coverage", choices=sorted(COVERAGE_LEVELS), required=True)
    coverage.add_argument("--locator")

    expression = commands.add_parser("expression")
    expression.add_argument("--project-id", required=True)
    expression.add_argument("--unit-id", required=True)
    add_text_source(expression)
    expression.add_argument("--qualification", choices=sorted(EXPRESSION_RESULTS - {"not_requested"}), default="pending")
    expression.add_argument("--coverage", choices=sorted(COVERAGE_LEVELS))
    expression.add_argument("--locator")

    check = commands.add_parser("evidence-check")
    check.add_argument("--project-id", required=True)
    check.add_argument("--unit-id", required=True)
    check.add_argument("--result", choices=sorted(EVIDENCE_RESULTS - {"not_requested", "pending"}), required=True)
    check.add_argument("--evidence-ref", action="append", default=[])
    check.add_argument("--locator")
    check.add_argument("--open-question", action="append", default=[])

    claim = commands.add_parser("claim")
    claim.add_argument("--project-id", required=True)
    claim.add_argument("--claim-id", required=True)
    claim.add_argument("--text", required=True)
    claim.add_argument("--unit-id", action="append", default=[])
    claim.add_argument("--expression-ref", action="append", default=[])

    distill = commands.add_parser("distill")
    distill.add_argument("--project-id", required=True)
    distill.add_argument("--claim-id", required=True)
    distill.add_argument("--decision", choices=sorted(DISTILLATION_DECISIONS), required=True)
    distill.add_argument("--artifact", action="append", default=[])

    attempt = commands.add_parser("attempt")
    attempt.add_argument("--project-id", required=True)
    attempt.add_argument("--attempt-id")
    attempt.add_argument("--scope", choices=("project", "claim"), required=True)
    attempt.add_argument("--scope-id", required=True)
    attempt.add_argument("--kind", choices=sorted(ATTEMPT_KINDS), required=True)
    attempt.add_argument("--result", choices=sorted(ATTEMPT_RESULTS), required=True)
    attempt.add_argument("--performer", choices=("user", "agent", "joint"), default="user")
    add_text_source(attempt)
    attempt.add_argument("--evidence-ref", action="append", default=[])
    attempt.add_argument("--gap", action="append", default=[])

    blocker = commands.add_parser("blocker")
    blocker.add_argument("--project-id", required=True)
    blocker.add_argument("--blocker-id")
    blocker.add_argument("--subject-kind", choices=sorted(SUBJECT_KINDS - {"workflow"}), default="project")
    blocker.add_argument("--subject-id", required=True)
    blocker.add_argument("--reason", required=True)

    resolve = commands.add_parser("resolve-blocker")
    resolve.add_argument("--project-id", required=True)
    resolve.add_argument("--blocker-id", required=True)
    resolve.add_argument("--resolution", required=True)

    workflow = commands.add_parser("workflow")
    workflow.add_argument("--project-id", required=True)
    workflow.add_argument("--workflow-id", required=True)
    workflow.add_argument("--mode", choices=sorted(ALLOWED_MODES), required=True)
    workflow.add_argument("--unit-id")
    workflow.add_argument("--status", choices=sorted(WORKFLOW_STATUSES), required=True)
    workflow.add_argument("--step", required=True)
    workflow.add_argument("--data")

    status = commands.add_parser("project-status")
    status.add_argument("--project-id", required=True)
    status.add_argument("--status", choices=sorted(PROJECT_STATUSES), required=True)

    plan = commands.add_parser("plan")
    plan.add_argument("--project-id", required=True)
    plan.add_argument("--focus-question")
    plan.add_argument("--unit-requirement", action="append", choices=sorted(UNIT_REQUIREMENTS))
    plan.add_argument("--claim-requirement", action="append", choices=sorted(CLAIM_REQUIREMENTS))
    plan.add_argument("--project-requirement", action="append", choices=sorted(PROJECT_REQUIREMENTS))
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    repo_root = args.repo_root.expanduser().resolve()
    state_dir = resolve_state_dir(repo_root, args.state_dir)
    try:
        if args.command == "init-project":
            result = initialize_project(args, repo_root, state_dir)
        elif args.command == "add-unit":
            result = add_unit(args, repo_root, state_dir)
        elif args.command == "coverage":
            result = record_coverage(args, state_dir)
        elif args.command == "expression":
            result = record_expression(args, repo_root, state_dir)
        elif args.command == "evidence-check":
            result = record_evidence_check(args, repo_root, state_dir)
        elif args.command == "claim":
            result = register_claim(args, repo_root, state_dir)
        elif args.command == "distill":
            result = record_distillation(args, repo_root, state_dir)
        elif args.command == "attempt":
            result = record_attempt(args, repo_root, state_dir)
        elif args.command == "blocker":
            result = add_blocker(args, state_dir)
        elif args.command == "resolve-blocker":
            result = resolve_blocker(args, state_dir)
        elif args.command == "workflow":
            result = update_workflow(args, state_dir)
        elif args.command == "project-status":
            result = change_project_status(args, state_dir)
        elif args.command == "plan":
            result = adjust_plan(args, state_dir)
        else:
            raise ValueError(f"unsupported command: {args.command}")
    except (FileNotFoundError, FileExistsError, ValueError, json.JSONDecodeError) as exc:
        parser.exit(2, f"ERROR: {exc}\n")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
