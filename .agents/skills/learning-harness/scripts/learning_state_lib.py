from __future__ import annotations

import fcntl
import json
import os
import re
import tempfile
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Iterator

PROJECT_STATUSES = {"draft", "active", "paused", "complete", "archived"}
COVERAGE_LEVELS = {"unread", "skimmed", "read", "revisited"}
EXPRESSION_RESULTS = {"not_requested", "pending", "qualified", "insufficient"}
EVIDENCE_RESULTS = {
    "not_requested",
    "pending",
    "supported",
    "supported_with_boundary",
    "partial",
    "contradicted",
    "blocked",
}
DISTILLATION_DECISIONS = {"new", "update", "skip"}
ATTEMPT_KINDS = {"retrieval", "comparison", "counterexample", "output", "application"}
ATTEMPT_RESULTS = {"success", "partial", "failure"}
WORKFLOW_STATUSES = {"pending", "in_progress", "blocked", "complete", "cancelled"}
ACTORS = {"user", "agent", "tool"}
SUBJECT_KINDS = {"project", "unit", "claim", "attempt", "blocker", "workflow"}
EVENT_TYPES = {
    "project_initialized",
    "project_status_changed",
    "unit_added",
    "coverage_recorded",
    "expression_captured",
    "expression_qualified",
    "evidence_checked",
    "claim_registered",
    "distillation_decided",
    "attempt_recorded",
    "blocker_added",
    "blocker_resolved",
    "workflow_updated",
    "plan_adjusted",
}
ALLOWED_SKILLS = {"learning-harness", "visual-pkm"}
ALLOWED_MODES = {
    "deep-reading",
    "concept-visualization",
    "spatial-mapping",
    "idea-integration",
    "knowledge-exploration",
    "narrative-composition",
    "system-review",
}
UNIT_REQUIREMENTS = {"coverage"}
CLAIM_REQUIREMENTS = {"distillation_decision"}
PROJECT_REQUIREMENTS = {"source_grounding", "retrieval", "application"}
IDENTIFIER_RE = re.compile(r"^[a-z0-9][a-z0-9._-]*$")


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def resolve_state_dir(root: Path, override: Path | None = None) -> Path:
    configured = override or (Path(os.environ["LEARNING_STATE_DIR"]) if os.environ.get("LEARNING_STATE_DIR") else None)
    return (configured or root / ".learning").expanduser().resolve()


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json_atomic(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, delete=False) as handle:
        json.dump(value, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
        temporary = Path(handle.name)
    temporary.replace(path)


def validate_identifier(value: str, label: str) -> str:
    if not IDENTIFIER_RE.fullmatch(value):
        raise ValueError(f"{label} must match {IDENTIFIER_RE.pattern}: {value!r}")
    return value


def project_dir(state_dir: Path, project_id: str) -> Path:
    return state_dir / "projects" / validate_identifier(project_id, "project_id")


def repo_relative(path: Path, repo_root: Path) -> str:
    return path.expanduser().resolve().relative_to(repo_root.expanduser().resolve()).as_posix()


def repository_path(value: str | Path, repo_root: Path, *, must_exist: bool = True) -> str:
    candidate = Path(value).expanduser()
    path = candidate.resolve() if candidate.is_absolute() else (repo_root / candidate).resolve()
    try:
        relative = path.relative_to(repo_root.resolve()).as_posix()
    except ValueError as exc:
        raise ValueError(f"path must remain inside repository: {value}") from exc
    if must_exist and not path.exists():
        raise FileNotFoundError(path)
    return relative


def set_active_project(state_dir: Path, project_id: str | None) -> None:
    config_path = state_dir / "config.json"
    config = read_json(config_path)
    if project_id is not None:
        validate_identifier(project_id, "project_id")
    config["active_project_id"] = project_id
    write_json_atomic(config_path, config)


def active_project_id(state_dir: Path) -> str | None:
    config = read_json(state_dir / "config.json")
    value = config.get("active_project_id")
    if value is None:
        return None
    if not isinstance(value, str):
        raise ValueError("config.active_project_id must be a string or null")
    return validate_identifier(value, "active_project_id")


@contextmanager
def project_lock(directory: Path) -> Iterator[None]:
    directory.mkdir(parents=True, exist_ok=True)
    lock_path = directory / "events.jsonl"
    with lock_path.open("a+", encoding="utf-8") as handle:
        fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(handle.fileno(), fcntl.LOCK_UN)


def read_events(directory: Path) -> list[dict[str, Any]]:
    path = directory / "events.jsonl"
    if not path.exists():
        raise FileNotFoundError(path)
    events: list[dict[str, Any]] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"invalid JSONL at {path}:{line_number}: {exc}") from exc
        if not isinstance(event, dict):
            raise ValueError(f"event must be an object at {path}:{line_number}")
        events.append(event)
    return events


def evidence_ref(path: str, locator: str | None = None) -> dict[str, Any]:
    return {"type": "file", "path": path, "locator": locator}


def _event_record(project_id: str, seq: int, spec: dict[str, Any]) -> dict[str, Any]:
    event_type = str(spec.get("type", ""))
    actor = str(spec.get("actor", ""))
    if event_type not in EVENT_TYPES:
        raise ValueError(f"unknown event type: {event_type!r}")
    if actor not in ACTORS:
        raise ValueError(f"unknown event actor: {actor!r}")
    subject = spec.get("subject")
    if not isinstance(subject, dict) or subject.get("kind") not in SUBJECT_KINDS or not subject.get("id"):
        raise ValueError("event subject requires a valid kind and id")
    payload = spec.get("payload", {})
    refs = spec.get("evidence_refs", [])
    caused_by = spec.get("caused_by", [])
    if not isinstance(payload, dict) or not isinstance(refs, list) or not isinstance(caused_by, list):
        raise ValueError("event payload, evidence_refs, and caused_by must have valid container types")
    return {
        "seq": seq,
        "id": f"evt-{seq:08d}",
        "at": str(spec.get("at") or now_iso()),
        "actor": actor,
        "type": event_type,
        "project_id": project_id,
        "subject": subject,
        "payload": payload,
        "evidence_refs": refs,
        "caused_by": caused_by,
    }


def append_events(directory: Path, plan: dict[str, Any], specs: Iterable[dict[str, Any]]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    project_id = str(plan["id"])
    materialized = list(specs)
    if not materialized:
        raise ValueError("at least one event is required")
    with project_lock(directory):
        existing = read_events(directory)
        start = int(existing[-1]["seq"]) + 1 if existing else 1
        records = [_event_record(project_id, start + index, spec) for index, spec in enumerate(materialized)]
        with (directory / "events.jsonl").open("a", encoding="utf-8") as handle:
            for record in records:
                handle.write(json.dumps(record, ensure_ascii=False, separators=(",", ":")) + "\n")
            handle.flush()
            os.fsync(handle.fileno())
        snapshot = reduce_snapshot(plan, [*existing, *records])
        write_json_atomic(directory / "snapshot.json", snapshot)
    return records, snapshot


def load_project(state_dir: Path, project_id: str, *, repair_snapshot: bool = True) -> tuple[Path, dict[str, Any], list[dict[str, Any]], dict[str, Any]]:
    directory = project_dir(state_dir, project_id)
    plan = read_json(directory / "plan.json")
    events = read_events(directory)
    snapshot_path = directory / "snapshot.json"
    expected_seq = int(events[-1]["seq"]) if events else 0
    snapshot: dict[str, Any] | None = None
    if snapshot_path.exists():
        value = read_json(snapshot_path)
        if isinstance(value, dict):
            snapshot = value
    if snapshot is None or snapshot.get("derived_from_seq") != expected_seq:
        if not repair_snapshot:
            raise ValueError(f"stale or missing snapshot: {snapshot_path}")
        snapshot = reduce_snapshot(plan, events)
        write_json_atomic(snapshot_path, snapshot)
    return directory, plan, events, snapshot


def rebuild_snapshot(directory: Path, plan: dict[str, Any]) -> dict[str, Any]:
    with project_lock(directory):
        snapshot = reduce_snapshot(plan, read_events(directory))
        write_json_atomic(directory / "snapshot.json", snapshot)
    return snapshot


def _unit_template(unit: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": unit["id"],
        "title": unit.get("title") or unit["id"],
        "source_path": unit["source_path"],
        "locator": unit.get("locator"),
        "coverage": "unread",
        "expression_status": "not_requested",
        "expression_refs": [],
        "evidence_status": "not_requested",
        "evidence_refs": [],
        "open_questions": [],
        "updated_at": None,
    }


def _unit_ready(unit: dict[str, Any], required: set[str]) -> bool:
    checks = {"coverage": unit.get("coverage") in {"read", "revisited"}}
    return all(checks.get(name, False) for name in required)


def _claim_ready(claim: dict[str, Any], required: set[str]) -> bool:
    checks = {"distillation_decision": claim.get("distillation", {}).get("decision") in DISTILLATION_DECISIONS}
    return all(checks.get(name, False) for name in required)


def _attempt_satisfies(requirement: str, attempt: dict[str, Any]) -> bool:
    if attempt.get("result") != "success":
        return False
    kind = attempt.get("kind")
    if requirement == "retrieval":
        return kind in {"retrieval", "comparison", "counterexample"}
    if requirement == "application":
        return kind == "application"
    return False


def _project_requirement_satisfied(
    requirement: str,
    units: list[dict[str, Any]],
    attempts: list[dict[str, Any]],
) -> bool:
    if requirement == "source_grounding":
        return any(unit.get("evidence_status") in {"supported", "supported_with_boundary"} for unit in units)
    return any(_attempt_satisfies(requirement, attempt) for attempt in attempts)


def _command(
    snapshot: dict[str, Any],
    *,
    skill: str,
    action: str,
    subject: dict[str, str],
    instruction: str,
    reason: str,
    mode: str | None = None,
    workflow: dict[str, Any] | None = None,
) -> dict[str, Any]:
    sequence = int(snapshot.get("derived_from_seq", 0))
    command: dict[str, Any] = {
        "id": f"cmd-{sequence:08d}",
        "based_on_seq": sequence,
        "skill": skill,
        "action": action,
        "subject": subject,
        "instruction": instruction,
        "reason": reason,
    }
    if mode is not None:
        command["mode"] = mode
    if workflow is not None:
        command["workflow"] = workflow
    return command


def derive_next_command(plan: dict[str, Any], snapshot: dict[str, Any]) -> dict[str, Any] | None:
    project_subject = {"kind": "project", "id": plan["id"]}
    if snapshot.get("status") in {"complete", "archived"}:
        return None
    if snapshot.get("status") == "paused":
        return _command(
            snapshot,
            skill="learning-harness",
            action="resume-project",
            subject=project_subject,
            instruction="取得用户确认后恢复项目，再从事件派生的当前游标继续",
            reason="项目当前处于 paused 状态",
        )
    blockers = [item for item in snapshot.get("blockers", []) if item.get("status") == "open"]
    if blockers:
        blocker = blockers[-1]
        return _command(
            snapshot,
            skill="learning-harness",
            action="resolve-blocker",
            subject=blocker.get("subject") or project_subject,
            instruction=f"解除已记录阻塞：{blocker['reason']}",
            reason="继续推进前需要先解决并关闭该阻塞",
        )

    active_workflows = [
        workflow
        for workflow in snapshot.get("workflows", [])
        if workflow.get("status") not in {"complete", "cancelled"}
    ]
    if active_workflows:
        workflow = sorted(
            active_workflows,
            key=lambda item: (item.get("updated_at") or "", item.get("id") or ""),
            reverse=True,
        )[0]
        return _command(
            snapshot,
            skill="visual-pkm",
            mode=workflow["mode"],
            action="resume-workflow",
            subject={"kind": "workflow", "id": workflow["id"]},
            instruction=f"恢复 workflow {workflow['id']}，从 {workflow['step']} 执行一个局部动作",
            reason="存在未完成的可恢复工作流",
            workflow=workflow,
        )

    unit_required = set(plan.get("completion_policy", {}).get("unit", {}).get("required", UNIT_REQUIREMENTS))
    units = snapshot.get("units", [])
    if not units:
        return _command(
            snapshot,
            skill="learning-harness",
            action="add-source-unit",
            subject=project_subject,
            instruction="请用户添加第一个可恢复的来源单元",
            reason="项目计划尚无来源单元",
        )
    current_id = snapshot.get("cursor", {}).get("unit_id")
    unit_order = [unit["id"] for unit in units]
    ordered = sorted(units, key=lambda item: (item.get("id") != current_id, unit_order.index(item["id"])))
    claim_required = set(plan.get("completion_policy", {}).get("claim", {}).get("required", CLAIM_REQUIREMENTS))
    for unit in ordered:
        subject = {"kind": "unit", "id": unit["id"]}
        if "coverage" in unit_required and unit.get("coverage") not in {"read", "revisited"}:
            return _command(
                snapshot,
                skill="learning-harness",
                action="record-coverage",
                subject=subject,
                instruction="请用户亲自阅读当前单元，再把真实阅读范围记录为 coverage；未进入语义核验时不要求表达",
                reason="当前来源单元尚未完成阅读覆盖",
            )
        if unit.get("expression_refs"):
            if unit.get("expression_status") != "qualified":
                return _command(
                    snapshot,
                    skill="visual-pkm",
                    mode="deep-reading",
                    action="qualify-expression",
                    subject=subject,
                    instruction="判断已记录表达是否构成用户自己的认知起点并报告结果",
                    reason="该单元已经进入语义核验，但用户表达尚未确认",
                )
            if unit.get("evidence_status") not in {"supported", "supported_with_boundary"}:
                return _command(
                    snapshot,
                    skill="visual-pkm",
                    mode="deep-reading",
                    action="verify-expression",
                    subject=subject,
                    instruction="对照来源核验用户表达、条件、边界和可能误读并报告证据",
                    reason=f"该语义动作的证据核对状态为 {unit.get('evidence_status')}",
                )
        unresolved = [
            claim
            for claim in snapshot.get("claims", [])
            if unit["id"] in claim.get("unit_ids", []) and not _claim_ready(claim, claim_required)
        ]
        if unresolved:
            claim = unresolved[0]
            return _command(
                snapshot,
                skill="learning-harness",
                action="record-distillation-decision",
                subject={"kind": "claim", "id": claim["id"]},
                instruction="请用户决定该命题应新建知识卡、更新已有卡或跳过沉淀，并记录真实产物",
                reason="该单元产生了尚未处理的用户候选命题",
            )

    for claim in snapshot.get("claims", []):
        if not _claim_ready(claim, claim_required):
            return _command(
                snapshot,
                skill="learning-harness",
                action="record-distillation-decision",
                subject={"kind": "claim", "id": claim["id"]},
                instruction="请用户决定该命题应新建知识卡、更新已有卡或跳过沉淀，并记录真实产物",
                reason="存在尚未处理的用户候选命题",
            )

    required = list(plan.get("completion_policy", {}).get("project", {}).get("required", PROJECT_REQUIREMENTS))
    attempts = snapshot.get("attempts", [])
    for requirement in required:
        if _project_requirement_satisfied(requirement, units, attempts):
            continue
        if requirement == "source_grounding":
            return _command(
                snapshot,
                skill="learning-harness",
                action="capture-key-understanding",
                subject=project_subject,
                instruction="请用户从已读来源中选择一个关键或不确定的理解，指定来源单元并用自己的话表达",
                reason="项目尚无用户主导且经过来源核验的关键理解",
            )
        if requirement == "retrieval":
            return _command(
                snapshot,
                skill="visual-pkm",
                mode="knowledge-exploration",
                action="run-retrieval",
                subject=project_subject,
                instruction="请用户脱离来源完成一次复述、比较或反例测试，并报告真实结果",
                reason="项目尚无成功的检索证据",
            )
        if requirement == "application":
            return _command(
                snapshot,
                skill="learning-harness",
                action="record-application",
                subject=project_subject,
                instruction="请用户在真实任务中应用本项目知识，再记录结果、失败与证据",
                reason="项目尚无成功的真实应用证据",
            )

    return _command(
        snapshot,
        skill="learning-harness",
        action="confirm-completion",
        subject=project_subject,
        instruction="请用户确认是否将项目标记为 complete",
        reason="完成政策已经满足，但项目状态只能由用户确认",
    )


def reduce_snapshot(plan: dict[str, Any], events: list[dict[str, Any]]) -> dict[str, Any]:
    units = {unit["id"]: _unit_template(unit) for unit in plan.get("units", [])}
    claims: dict[str, dict[str, Any]] = {}
    attempts: list[dict[str, Any]] = []
    blockers: dict[str, dict[str, Any]] = {}
    workflows: dict[str, dict[str, Any]] = {}
    status = "draft"
    last_active_unit = plan.get("units", [{}])[0].get("id") if plan.get("units") else None
    last_session_at: str | None = None

    for event in events:
        event_type = event.get("type")
        subject = event.get("subject", {})
        subject_id = subject.get("id")
        payload = event.get("payload", {})
        refs = event.get("evidence_refs", [])
        at = event.get("at")

        if event_type == "project_initialized":
            status = payload.get("status", "active")
        elif event_type == "project_status_changed":
            status = payload.get("status", status)
        elif event_type == "coverage_recorded" and subject_id in units:
            unit = units[subject_id]
            unit["coverage"] = payload.get("coverage", unit["coverage"])
            if payload.get("locator") is not None:
                unit["locator"] = payload["locator"]
            unit["updated_at"] = at
            last_active_unit = subject_id
        elif event_type == "expression_captured" and subject_id in units:
            unit = units[subject_id]
            for ref in refs:
                if ref not in unit["expression_refs"]:
                    unit["expression_refs"].append(ref)
            unit["expression_status"] = "pending"
            unit["updated_at"] = at
            last_active_unit = subject_id
            last_session_at = at
        elif event_type == "expression_qualified" and subject_id in units:
            unit = units[subject_id]
            unit["expression_status"] = payload.get("result", "pending")
            unit["updated_at"] = at
            last_active_unit = subject_id
        elif event_type == "evidence_checked" and subject_id in units:
            unit = units[subject_id]
            unit["evidence_status"] = payload.get("result", "pending")
            unit["evidence_refs"] = refs
            for question in payload.get("open_questions", []):
                if question not in unit["open_questions"]:
                    unit["open_questions"].append(question)
            unit["updated_at"] = at
            last_active_unit = subject_id
        elif event_type == "claim_registered":
            claims[subject_id] = {
                "id": subject_id,
                "text": payload.get("text", ""),
                "unit_ids": list(payload.get("unit_ids", [])),
                "expression_refs": list(payload.get("expression_refs", [])),
                "distillation": {"decision": None, "artifact_paths": [], "updated_at": None},
                "created_at": at,
                "updated_at": at,
            }
        elif event_type == "distillation_decided" and subject_id in claims:
            claims[subject_id]["distillation"] = {
                "decision": payload.get("decision"),
                "artifact_paths": [ref["path"] for ref in refs if isinstance(ref, dict) and ref.get("path")],
                "updated_at": at,
            }
            claims[subject_id]["updated_at"] = at
        elif event_type == "attempt_recorded":
            attempts.append(
                {
                    "id": subject_id,
                    "scope": payload.get("scope"),
                    "scope_id": payload.get("scope_id"),
                    "kind": payload.get("kind"),
                    "result": payload.get("result"),
                    "performer": payload.get("performer", "user"),
                    "gaps": list(payload.get("gaps", [])),
                    "evidence_refs": refs,
                    "at": at,
                }
            )
            last_session_at = at
        elif event_type == "blocker_added":
            blockers[subject_id] = {
                "id": subject_id,
                "status": "open",
                "reason": payload.get("reason", ""),
                "subject": payload.get("blocked_subject") or {"kind": "project", "id": plan["id"]},
                "created_at": at,
                "resolved_at": None,
            }
        elif event_type == "blocker_resolved" and subject_id in blockers:
            blockers[subject_id]["status"] = "resolved"
            blockers[subject_id]["resolution"] = payload.get("resolution", "")
            blockers[subject_id]["resolved_at"] = at
        elif event_type == "workflow_updated":
            workflows[subject_id] = {
                "id": subject_id,
                "mode": payload.get("mode"),
                "unit_id": payload.get("unit_id"),
                "status": payload.get("status"),
                "step": payload.get("step"),
                "data": payload.get("data", {}),
                "updated_at": at,
            }
            if payload.get("unit_id") in units:
                last_active_unit = payload["unit_id"]

    unit_list = list(units.values())
    claim_list = list(claims.values())
    unit_required = set(plan.get("completion_policy", {}).get("unit", {}).get("required", UNIT_REQUIREMENTS))
    claim_required = set(plan.get("completion_policy", {}).get("claim", {}).get("required", CLAIM_REQUIREMENTS))
    project_required = list(plan.get("completion_policy", {}).get("project", {}).get("required", PROJECT_REQUIREMENTS))
    unit_ready_count = sum(_unit_ready(unit, unit_required) for unit in unit_list)
    claim_ready_count = sum(_claim_ready(claim, claim_required) for claim in claim_list)
    project_evidence = {
        requirement: _project_requirement_satisfied(requirement, unit_list, attempts)
        for requirement in project_required
    }
    complete_by_policy = (
        unit_ready_count == len(unit_list)
        and claim_ready_count == len(claim_list)
        and all(project_evidence.values())
        and not any(item.get("status") == "open" for item in blockers.values())
    )

    incomplete_ids = [unit["id"] for unit in unit_list if not _unit_ready(unit, unit_required)]
    units_with_open_claims = {
        unit_id
        for claim in claim_list
        if not _claim_ready(claim, claim_required)
        for unit_id in claim.get("unit_ids", [])
    }
    units_with_open_semantics = {
        unit["id"]
        for unit in unit_list
        if unit.get("expression_refs")
        and (
            unit.get("expression_status") != "qualified"
            or unit.get("evidence_status") not in {"supported", "supported_with_boundary"}
        )
    }
    if (
        last_active_unit in incomplete_ids
        or last_active_unit in units_with_open_claims
        or last_active_unit in units_with_open_semantics
    ):
        current_unit = last_active_unit
    else:
        current_unit = incomplete_ids[0] if incomplete_ids else last_active_unit
    snapshot: dict[str, Any] = {
        "project_id": plan["id"],
        "derived_from_seq": int(events[-1]["seq"]) if events else 0,
        "status": status,
        "cursor": {"unit_id": current_unit},
        "units": unit_list,
        "claims": claim_list,
        "attempts": attempts,
        "blockers": list(blockers.values()),
        "workflows": list(workflows.values()),
        "last_session_at": last_session_at,
        "completion": {
            "unit_ready": unit_ready_count,
            "unit_total": len(unit_list),
            "claim_ready": claim_ready_count,
            "claim_total": len(claim_list),
            "project_evidence": project_evidence,
            "complete_by_policy": complete_by_policy,
        },
        "last_event_at": events[-1]["at"] if events else None,
        "generated_at": now_iso(),
    }
    snapshot["next_command"] = derive_next_command(plan, snapshot)
    return snapshot


def status_summary(plan: dict[str, Any], snapshot: dict[str, Any]) -> dict[str, Any]:
    current_id = snapshot.get("cursor", {}).get("unit_id")
    current_unit = next((unit for unit in snapshot.get("units", []) if unit.get("id") == current_id), None)
    attempts = snapshot.get("attempts", [])
    return {
        "project_id": plan["id"],
        "title": plan["title"],
        "focus_question": plan["focus_question"],
        "status": snapshot["status"],
        "current_unit": current_unit,
        "units": snapshot.get("units", []),
        "claims": snapshot.get("claims", []),
        "attempts": attempts,
        "attempt_counts": {
            result: sum(1 for attempt in attempts if attempt.get("result") == result)
            for result in sorted(ATTEMPT_RESULTS)
        },
        "blockers": snapshot.get("blockers", []),
        "workflows": snapshot.get("workflows", []),
        "completion": snapshot.get("completion", {}),
        "last_session_at": snapshot.get("last_session_at"),
        "last_event_at": snapshot.get("last_event_at"),
        "next_command": snapshot.get("next_command"),
        "state_seq": snapshot.get("derived_from_seq", 0),
    }
