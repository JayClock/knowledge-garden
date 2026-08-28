from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

from learning_state_lib import ( # pyright: ignore[reportMissingImports]
    load_project,
    now_iso,
    read_json,
    repo_relative,
    resolve_state_dir,
    status_summary,
    write_json_atomic,
)

BODY_START = "<!-- learning-harness:managed:start -->"
BODY_END = "<!-- learning-harness:managed:end -->"
MANAGED_FIELDS = {
    "status",
    "learningId",
    "learningStatus",
    "learningActivity",
    "learningCurrentUnit",
    "learningNextSkill",
    "learningNextMode",
    "learningNextAction",
    "learningLastEvent",
    "learningSourceReady",
    "learningClaimsReady",
    "learningSourceGrounding",
    "learningRetrieval",
    "learningApplication",
    "learningStateSeq",
}


def yaml_value(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, int):
        return str(value)
    if value is None:
        return '""'
    return json.dumps(str(value), ensure_ascii=False)


def split_frontmatter(content: str) -> tuple[list[str], str]:
    if not content.startswith("---\n"):
        return [], content
    end = content.find("\n---\n", 4)
    if end < 0:
        raise ValueError("existing TaskNote has invalid frontmatter")
    return content[4:end].splitlines(), content[end + 5 :]


def update_frontmatter(lines: list[str], managed: dict[str, Any]) -> str:
    kept: list[str] = []
    for line in lines:
        match = re.match(r"^([A-Za-z][A-Za-z0-9_-]*):", line)
        if match and match.group(1) in MANAGED_FIELDS:
            continue
        kept.append(line)
    if not kept:
        kept = ["priority: none", "tags:", "  - task", "  - learning", "taskSourceType: taskNotes"]
    kept.extend(f"{key}: {yaml_value(value)}" for key, value in managed.items())
    return "---\n" + "\n".join(kept).rstrip() + "\n---\n"


def sanitize_filename(value: str) -> str:
    cleaned = re.sub(r'[\\/:*?"<>|]', "-", value).strip().rstrip(".")
    return cleaned or "Learning Project"


def vault_link(path: str | None, vault_prefix: str) -> str:
    if not path:
        return "—"
    normalized = path
    prefix = vault_prefix.rstrip("/") + "/" if vault_prefix else ""
    if prefix and normalized.startswith(prefix):
        normalized = normalized[len(prefix) :]
    if normalized.endswith(".md"):
        normalized = normalized[:-3]
    return f"[[{normalized}]]"


def cell(value: Any) -> str:
    return str(value if value not in {None, ""} else "—").replace("|", "\\|").replace("\n", " ")


def optional_semantic_status(value: Any) -> str:
    return "—" if value == "not_requested" else cell(value)


def managed_frontmatter(summary: dict[str, Any]) -> dict[str, Any]:
    completion = summary.get("completion", {})
    action = summary.get("next_action") or {}
    current = summary.get("current_unit") or {}
    evidence = completion.get("project_evidence", {})
    return {
        "status": "done" if summary.get("status") in {"complete", "archived"} else "open",
        "learningId": summary.get("project_id"),
        "learningStatus": summary.get("status"),
        "learningActivity": action.get("mode") or action.get("skill") or "none",
        "learningCurrentUnit": current.get("id") or "",
        "learningNextSkill": action.get("skill") or "",
        "learningNextMode": action.get("mode") or "",
        "learningNextAction": action.get("action") or "",
        "learningLastEvent": summary.get("last_event_at") or "",
        "learningSourceReady": f"{completion.get('unit_ready', 0)}/{completion.get('unit_total', 0)}",
        "learningClaimsReady": f"{completion.get('claim_ready', 0)}/{completion.get('claim_total', 0)}",
        "learningSourceGrounding": bool(evidence.get("source_grounding")),
        "learningRetrieval": bool(evidence.get("retrieval")),
        "learningApplication": bool(evidence.get("application")),
        "learningStateSeq": int(summary.get("state_seq", 0)),
    }


def managed_body(summary: dict[str, Any], vault_prefix: str) -> str:
    action = summary.get("next_action") or {}
    current = summary.get("current_unit") or {}
    lines = [
        BODY_START,
        "## 今天",
        "",
        f"- 学习问题：{summary.get('focus_question')}",
        f"- 当前来源：{vault_link(current.get('source_path'), vault_prefix)}",
        f"- 唯一下一步：{action.get('action') or '无'}",
        f"- 原因：{action.get('reason') or '完成政策已满足或项目已结束'}",
        "",
        "## 来源推进",
        "",
        "| 单元 | 来源 | 覆盖 | 用户表达 | 证据核对 | 最近活动 |",
        "|---|---|---|---|---|---|",
    ]
    for unit in summary.get("units", []):
        lines.append(
            f"| `{cell(unit.get('id'))}` | {vault_link(unit.get('source_path'), vault_prefix)} | "
            f"`{cell(unit.get('coverage'))}` | `{optional_semantic_status(unit.get('expression_status'))}` | "
            f"`{optional_semantic_status(unit.get('evidence_status'))}` | {cell(unit.get('updated_at'))} |"
        )
    lines.extend(["", "## 用户命题与产物", ""])
    claims = summary.get("claims", [])
    if claims:
        lines.extend(["| 命题 | 来源单元 | 沉淀 | 产物 |", "|---|---|---|---|"])
        for claim in claims:
            distillation = claim.get("distillation", {})
            artifacts = "、".join(vault_link(path, vault_prefix) for path in distillation.get("artifact_paths", [])) or "—"
            lines.append(
                f"| {cell(claim.get('text'))} | {cell(', '.join(claim.get('unit_ids', [])))} | "
                f"`{cell(distillation.get('decision'))}` | {artifacts} |"
            )
    else:
        lines.append("- 暂无用户候选命题。")
    lines.extend(["", "## 检索与应用", ""])
    attempts = summary.get("attempts", [])
    if attempts:
        lines.extend(["| 时间 | 类型 | 执行者 | 结果 | 暴露问题 |", "|---|---|---|---|---|"])
        for attempt in attempts[-8:][::-1]:
            lines.append(
                f"| {cell(attempt.get('at'))} | `{cell(attempt.get('kind'))}` | `{cell(attempt.get('performer'))}` | "
                f"`{cell(attempt.get('result'))}` | {cell('；'.join(attempt.get('gaps', [])))} |"
            )
    else:
        lines.append("- 尚无检索或应用尝试。")
    blockers = [item for item in summary.get("blockers", []) if item.get("status") == "open"]
    lines.extend(["", "## 阻塞", ""])
    lines.extend(f"- `{item['id']}`：{item['reason']}" for item in blockers) if blockers else lines.append("- 无")
    lines.append(BODY_END)
    return "\n".join(lines)


def user_zone(existing_body: str) -> str:
    if BODY_END in existing_body:
        suffix = existing_body.split(BODY_END, 1)[1].lstrip("\n")
    else:
        suffix = existing_body.strip()
    if "## 进度收件箱" not in suffix:
        inbox = (
            "## 进度收件箱\n\n"
            "<!-- 使用未勾选条目记录；格式为 UNIT_ID | coverage=read，或 UNIT_ID | expression=自己的复述。learning-harness 导入后会勾选。 -->\n"
        )
        suffix = inbox + ("\n" + suffix if suffix else "")
    if "## 用户备注" not in suffix:
        suffix = suffix.rstrip() + "\n\n## 用户备注\n"
    return suffix.rstrip() + "\n"


def render(title: str, existing: str | None, frontmatter: dict[str, Any], body: str) -> str:
    if existing is not None and (BODY_START not in existing or BODY_END not in existing):
        raise ValueError("existing TaskNote is not managed by learning-harness")
    lines, old_body = split_frontmatter(existing) if existing is not None else ([], "")
    prefix = update_frontmatter(lines, frontmatter)
    zone = user_zone(old_body)
    return f"{prefix}\n# 学习 - {title}\n\n{body}\n\n{zone}"


def main() -> int:
    parser = argparse.ArgumentParser(description="Project event-derived learning state into a TaskNote.")
    parser.add_argument("--repo-root", type=Path, required=True)
    parser.add_argument("--state-dir", type=Path)
    parser.add_argument("--project-id", required=True)
    parser.add_argument("--path", help="Repository-relative TaskNote path")
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    repo_root = args.repo_root.expanduser().resolve()
    state_dir = resolve_state_dir(repo_root, args.state_dir)
    try:
        directory, plan, _events, snapshot = load_project(state_dir, args.project_id)
        config = read_json(state_dir / "config.json")
        paths = config.get("paths", {})
        task_root = str(paths.get("task_root", "content/TaskNotes/Tasks")).rstrip("/")
        vault_prefix = str(paths.get("vault_root", "content"))
        target_relative = args.path or f"{task_root}/学习 - {sanitize_filename(str(plan['title']))}.md"
        target = (repo_root / target_relative).resolve()
        target.relative_to(repo_root)
        summary = status_summary(plan, snapshot)
        content = render(plan["title"], target.read_text(encoding="utf-8") if target.exists() else None, managed_frontmatter(summary), managed_body(summary, vault_prefix))
    except (FileNotFoundError, ValueError, json.JSONDecodeError) as exc:
        parser.exit(2, f"ERROR: {exc}\n")

    result = {"project_id": args.project_id, "path": target_relative, "apply": args.apply, "would_create": not target.exists()}
    if args.apply:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        metadata = {
            "path": repo_relative(target, repo_root),
            "source_seq": snapshot["derived_from_seq"],
            "updated_at": now_iso(),
        }
        write_json_atomic(directory / "projections" / "tasknote.json", metadata)
        result["source_seq"] = metadata["source_seq"]
    else:
        result["content"] = content
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
