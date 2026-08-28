from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from learning_state_lib import active_project_id, load_project, resolve_state_dir, status_summary  # pyright: ignore[reportMissingImports]


def markdown(summary: dict[str, Any]) -> str:
    current = summary.get("current_unit") or {}
    completion = summary.get("completion") or {}
    next_action = summary.get("next_action") or {}
    attempts = summary.get("attempts") or []
    lines = [
        f"# {summary.get('title') or summary.get('project_id')}",
        "",
        f"- 学习问题：{summary.get('focus_question') or '尚未设置'}",
        f"- 项目状态：`{summary.get('status')}`",
        f"- 当前单元：`{current.get('id') or '尚未设置'}`",
        f"- 最近事件：{summary.get('last_event_at') or '尚无'}",
        "",
        "## 学习信号",
        "",
        f"- 来源单元：{completion.get('unit_ready', 0)} / {completion.get('unit_total', 0)} 已完成计划要求（默认仅记录阅读覆盖）",
        f"- 用户命题：{completion.get('claim_ready', 0)} / {completion.get('claim_total', 0)} 已作沉淀决定",
        f"- 来源核验：{'已有' if completion.get('project_evidence', {}).get('source_grounding') else '尚无'}",
        f"- 检索证据：{'已有' if completion.get('project_evidence', {}).get('retrieval') else '尚无'}",
        f"- 应用证据：{'已有' if completion.get('project_evidence', {}).get('application') else '尚无'}",
        "",
        "## 唯一下一步",
        "",
        f"- Skill：`{next_action.get('skill') or '无'}`",
        f"- Mode：`{next_action.get('mode') or '—'}`",
        f"- 动作：{next_action.get('action') or '无'}",
        f"- 原因：{next_action.get('reason') or '完成政策已满足或项目已结束'}",
    ]
    blockers = [item for item in summary.get("blockers", []) if item.get("status") == "open"]
    if blockers:
        lines.extend(["", "## 阻塞", ""])
        lines.extend(f"- `{item['id']}`：{item['reason']}" for item in blockers)
    if attempts:
        lines.extend(["", "## 最近尝试", "", "| 时间 | 类型 | 执行者 | 结果 | 暴露问题 |", "|---|---|---|---|---|"])
        for attempt in attempts[-5:][::-1]:
            gaps = "；".join(attempt.get("gaps", [])) or "—"
            lines.append(
                f"| {attempt.get('at') or '—'} | `{attempt.get('kind')}` | `{attempt.get('performer')}` | "
                f"`{attempt.get('result')}` | {gaps} |"
            )
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Show the current event-derived Learning Harness state.")
    parser.add_argument("--repo-root", type=Path, required=True)
    parser.add_argument("--state-dir", type=Path)
    parser.add_argument("--project-id", help="Defaults to config.active_project_id")
    parser.add_argument("--markdown", action="store_true")
    args = parser.parse_args()

    repo_root = args.repo_root.expanduser().resolve()
    state_dir = resolve_state_dir(repo_root, args.state_dir)
    try:
        project_id = args.project_id or active_project_id(state_dir)
        if not project_id:
            raise ValueError("no active learning project; pass --project-id")
        _directory, plan, _events, snapshot = load_project(state_dir, project_id)
        summary = status_summary(plan, snapshot)
    except (FileNotFoundError, ValueError, json.JSONDecodeError) as exc:
        parser.exit(2, f"ERROR: {exc}\n")
    print(markdown(summary) if args.markdown else json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
