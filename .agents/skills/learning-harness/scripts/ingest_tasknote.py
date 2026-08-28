from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

from learning_state_lib import ( # pyright: ignore[reportMissingImports]
    append_events,
    evidence_ref,
    load_project,
    now_iso,
    read_json,
    repo_relative,
    resolve_state_dir,
    set_active_project,
)

COVERAGE_RE = re.compile(r"^- \[ \] ([a-z0-9][a-z0-9._-]*) \| coverage=(unread|skimmed|read|revisited)\s*$")
EXPRESSION_RE = re.compile(r"^- \[ \] ([a-z0-9][a-z0-9._-]*) \| expression=(.+?)\s*$")


def inbox_range(lines: list[str]) -> tuple[int, int]:
    try:
        start = lines.index("## 进度收件箱") + 1
    except ValueError as exc:
        raise ValueError("TaskNote has no 进度收件箱 section") from exc
    end = len(lines)
    for index in range(start, len(lines)):
        if lines[index].startswith("## "):
            end = index
            break
    return start, end


def save_expression(directory: Path, repo_root: Path, project_id: str, unit_id: str, text: str, ordinal: int) -> str:
    compact = re.sub(r"[^0-9]", "", now_iso())[:14]
    path = directory / "sessions" / f"{compact}-{unit_id}-inbox-{ordinal}.md"
    suffix = 2
    while path.exists():
        path = path.with_name(f"{path.stem}-{suffix}{path.suffix}")
        suffix += 1
    path.write_text(
        "# Learning Session\n\n"
        f"- project: `{project_id}`\n"
        f"- subject: `{unit_id}`\n"
        f"- recorded_at: `{now_iso()}`\n"
        "- captured_from: `TaskNote 进度收件箱`\n\n"
        f"## 用户原始表达\n\n{text.strip()}\n",
        encoding="utf-8",
    )
    return repo_relative(path, repo_root)


def main() -> int:
    parser = argparse.ArgumentParser(description="Import explicit TaskNote inbox entries into the append-only learning event log.")
    parser.add_argument("--repo-root", type=Path, required=True)
    parser.add_argument("--state-dir", type=Path)
    parser.add_argument("--project-id", required=True)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    repo_root = args.repo_root.expanduser().resolve()
    state_dir = resolve_state_dir(repo_root, args.state_dir)
    try:
        directory, plan, _events, _snapshot = load_project(state_dir, args.project_id)
        projection = read_json(directory / "projections" / "tasknote.json")
        task_path = (repo_root / projection["path"]).resolve()
        content = task_path.read_text(encoding="utf-8")
        lines = content.splitlines()
        start, end = inbox_range(lines)
        known_units = {unit["id"] for unit in plan["units"]}
        parsed: list[dict[str, Any]] = []
        for index in range(start, end):
            line = lines[index]
            coverage = COVERAGE_RE.match(line)
            expression = EXPRESSION_RE.match(line)
            if coverage:
                unit_id, level = coverage.groups()
                if unit_id not in known_units:
                    raise ValueError(f"unknown unit in inbox: {unit_id}")
                parsed.append({"line": index, "kind": "coverage", "unit_id": unit_id, "coverage": level})
            elif expression:
                unit_id, text = expression.groups()
                if unit_id not in known_units:
                    raise ValueError(f"unknown unit in inbox: {unit_id}")
                parsed.append({"line": index, "kind": "expression", "unit_id": unit_id, "text": text.strip()})
        if not parsed:
            print(json.dumps({"project_id": args.project_id, "apply": args.apply, "entries": []}, ensure_ascii=False, indent=2))
            return 0
        if not args.apply:
            print(json.dumps({"project_id": args.project_id, "apply": False, "entries": parsed}, ensure_ascii=False, indent=2))
            return 0

        specs: list[dict[str, Any]] = []
        for ordinal, item in enumerate(parsed, start=1):
            if item["kind"] == "coverage":
                specs.append(
                    {
                        "actor": "user",
                        "type": "coverage_recorded",
                        "subject": {"kind": "unit", "id": item["unit_id"]},
                        "payload": {"coverage": item["coverage"], "locator": None},
                    }
                )
            else:
                session = save_expression(directory, repo_root, args.project_id, item["unit_id"], item["text"], ordinal)
                specs.append(
                    {
                        "actor": "user",
                        "type": "expression_captured",
                        "subject": {"kind": "unit", "id": item["unit_id"]},
                        "payload": {},
                        "evidence_refs": [evidence_ref(session)],
                    }
                )
        records, snapshot = append_events(directory, plan, specs)
        for item, record in zip(parsed, records, strict=True):
            lines[item["line"]] = lines[item["line"]].replace("- [ ]", "- [x]", 1) + f" <!-- {record['id']} -->"
        task_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        set_active_project(state_dir, args.project_id)
    except (FileNotFoundError, ValueError, json.JSONDecodeError, KeyError) as exc:
        parser.exit(2, f"ERROR: {exc}\n")

    print(
        json.dumps(
            {
                "project_id": args.project_id,
                "apply": True,
                "events": [record["id"] for record in records],
                "state_seq": snapshot["derived_from_seq"],
                "needs_projection_sync": True,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
