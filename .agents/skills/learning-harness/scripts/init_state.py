from __future__ import annotations

import argparse
import json
from pathlib import Path

from learning_state_lib import resolve_state_dir, write_json_atomic  # pyright: ignore[reportMissingImports]


def main() -> int:
    parser = argparse.ArgumentParser(description="Initialize the event-sourced Learning Harness state root.")
    parser.add_argument("--root", type=Path, required=True, help="Git repository root")
    parser.add_argument("--state-dir", type=Path, help="Override LEARNING_STATE_DIR")
    args = parser.parse_args()

    root = args.root.expanduser().resolve()
    state_dir = resolve_state_dir(root, args.state_dir)
    state_dir.mkdir(parents=True, exist_ok=True)
    (state_dir / "projects").mkdir(exist_ok=True)
    content_prefix = "content/" if (root / "content").is_dir() else ""
    config_path = state_dir / "config.json"
    if config_path.exists():
        parser.exit(2, f"ERROR: state root already exists: {config_path}\n")

    write_json_atomic(
        config_path,
        {
            "active_project_id": None,
            "paths": {
                "vault_root": content_prefix.rstrip("/"),
                "source_roots": [f"{content_prefix}Knowledge/Sources"],
                "note_root": f"{content_prefix}Knowledge/Notes",
                "map_root": f"{content_prefix}Knowledge/Maps",
                "output_root": f"{content_prefix}Knowledge/Outputs",
                "task_root": f"{content_prefix}TaskNotes/Tasks",
                "task_view": f"{content_prefix}TaskNotes/Views/learning-progress.base",
            },
            "state_policy": {
                "fact_source": "events.jsonl",
                "snapshot_is_derived": True,
                "vault_writes_require_separate_authorization": True,
                "tasknote_projection_is_derived": True,
            },
        },
    )
    print(json.dumps({"state_dir": str(state_dir)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
