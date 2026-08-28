from __future__ import annotations

import argparse
import json
from pathlib import Path

from learning_state_lib import (  # pyright: ignore[reportMissingImports]
    active_project_id,
    project_dir,
    read_json,
    rebuild_snapshot,
    resolve_state_dir,
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Rebuild snapshot.json only from plan.json and events.jsonl.")
    parser.add_argument("--repo-root", type=Path, required=True)
    parser.add_argument("--state-dir", type=Path)
    parser.add_argument("--project-id")
    args = parser.parse_args()
    repo_root = args.repo_root.expanduser().resolve()
    state_dir = resolve_state_dir(repo_root, args.state_dir)
    try:
        project_id = args.project_id or active_project_id(state_dir)
        if not project_id:
            raise ValueError("no active learning project; pass --project-id")
        directory = project_dir(state_dir, project_id)
        plan = read_json(directory / "plan.json")
        snapshot = rebuild_snapshot(directory, plan)
    except (FileNotFoundError, ValueError, json.JSONDecodeError) as exc:
        parser.exit(2, f"ERROR: {exc}\n")
    print(json.dumps({"project_id": project_id, "state_seq": snapshot["derived_from_seq"]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
