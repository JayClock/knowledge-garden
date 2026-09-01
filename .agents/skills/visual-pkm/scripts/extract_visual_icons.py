#!/usr/bin/env python3
"""Extract reusable native groups from a completed Visual Main Note into Icon Library.

The AI decides which completed visual groups are context-independent and reusable, then
records that mechanical decision in an extraction JSON. The script validates names and
targets; a bundled Obsidian payload reads the saved Drawing through the Excalidraw API
and creates pure, single-group `.excalidraw` component files. No user icon-selection
step or hand editing of compressed-json is involved.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

from write_visual_main_note import VisualWriteError, read_json, run_apply

NOTES_PREFIX = "Knowledge/Notes/"
ICON_DIR = "Knowledge/Assets/Excalidraw"
VISUAL_ID_PATTERN = re.compile(r"^[a-z0-9][a-z0-9-]{2,63}$")
RESERVED_SEPARATOR = " - "


class ExtractionError(VisualWriteError):
    """Raised when automatic icon extraction is unsafe or incomplete."""


def safe_name_part(value: Any, field: str) -> str:
    text = str(value).strip()
    if not text:
        raise ExtractionError(f"{field} 不能为空。")
    if any(character in text for character in '/\\:*?"<>|\n\r'):
        raise ExtractionError(f"{field} 包含文件名非法字符：{text}")
    if RESERVED_SEPARATOR in text:
        raise ExtractionError(f"{field} 不能包含保留分隔符 `{RESERVED_SEPARATOR}`。")
    return text


def validate_extraction_spec(data: dict[str, Any]) -> dict[str, Any]:
    visual_id = str(data.get("visual_id", "")).strip()
    if not VISUAL_ID_PATTERN.fullmatch(visual_id):
        raise ExtractionError("visual_id 必须是 3–64 位小写字母、数字或连字符。")
    raw_icons = data.get("icons")
    if not isinstance(raw_icons, list):
        raise ExtractionError("icons 必须是数组；没有可提取项时使用空数组。")

    seen_groups: set[str] = set()
    seen_paths: set[str] = set()
    icons: list[dict[str, Any]] = []
    for index, raw in enumerate(raw_icons, start=1):
        field = f"icons[{index}]"
        if not isinstance(raw, dict):
            raise ExtractionError(f"{field} 必须是对象。")
        group = safe_name_part(raw.get("group"), f"{field}.group")
        if group in seen_groups:
            raise ExtractionError(f"自动提取 group 重复：{group}")
        seen_groups.add(group)
        keywords_raw = raw.get("keywords")
        if not isinstance(keywords_raw, list) or not keywords_raw:
            raise ExtractionError(f"{field}.keywords 必须是非空数组。")
        keywords = [
            safe_name_part(value, f"{field}.keywords") for value in keywords_raw
        ]
        if any("," in keyword for keyword in keywords):
            raise ExtractionError(f"{field}.keywords 单项不能包含逗号。")
        if len({keyword.casefold() for keyword in keywords}) != len(keywords):
            raise ExtractionError(f"{field}.keywords 不能重复。")
        source = safe_name_part(raw.get("source", "Own"), f"{field}.source")
        if "," in source:
            raise ExtractionError(f"{field}.source 不能包含逗号。")
        filename = f"Icon - {', '.join(keywords)} - {source}.excalidraw"
        path = f"{ICON_DIR}/{filename}"
        if path in seen_paths:
            raise ExtractionError(f"自动提取目标重复：{path}")
        seen_paths.add(path)
        icons.append(
            {
                "group": group,
                "keywords": keywords,
                "source": source,
                "path": path,
                "reason": str(raw.get("reason", "")).strip(),
            }
        )
    return {"version": 1, "visual_id": visual_id, "icons": icons}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="从已完成 Visual Main Note 自动提取可复用 icon 到 Icon Library。"
    )
    parser.add_argument("--note", required=True, help="Knowledge/Notes/*.md 路径。")
    parser.add_argument("--extraction-spec", required=True, type=Path)
    parser.add_argument(
        "--duplicate-check-confirmed",
        action="store_true",
        help="确认 AI 已搜索并排除语义重复组件；--apply 必需。",
    )
    parser.add_argument("--vault-root", type=Path, default=Path.cwd())
    parser.add_argument("--vault-name", default="content")
    parser.add_argument("--timeout", type=int, default=180)
    parser.add_argument("--apply", action="store_true", help="执行落库；省略时只输出计划。")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        vault_root = args.vault_root.expanduser().resolve()
        if not (vault_root / ".obsidian").is_dir():
            raise ExtractionError(f"不是 Obsidian Vault 根目录：{vault_root}")
        note_path = Path(args.note).as_posix().lstrip("./")
        if not note_path.startswith(NOTES_PREFIX) or not note_path.endswith(".md"):
            raise ExtractionError("--note 必须指向 Knowledge/Notes/*.md。")
        if not (vault_root / note_path).is_file():
            raise ExtractionError(f"Visual Main Note 不存在：{note_path}")
        spec = validate_extraction_spec(
            read_json(args.extraction_spec.expanduser().resolve())
        )
        existing = [
            icon["path"] for icon in spec["icons"] if (vault_root / icon["path"]).exists()
        ]
        plan = {
            "status": "ready" if not existing else "needs_duplicate_resolution",
            "note": note_path,
            "visual_id": spec["visual_id"],
            "automatic_candidates": spec["icons"],
            "existing_paths": existing,
            "writes": bool(args.apply),
        }
        if not args.apply:
            print(json.dumps(plan, ensure_ascii=False, indent=2))
            return 0
        if not args.duplicate_check_confirmed:
            raise ExtractionError(
                "自动落库前必须由 AI 搜索 Icon Library 并传入 "
                "--duplicate-check-confirmed。"
            )
        if existing:
            raise ExtractionError(
                "目标文件已存在；应复用或更名，不能覆盖：" + "、".join(existing)
            )
        if not spec["icons"]:
            print(
                json.dumps(
                    {
                        "status": "applied",
                        "note": note_path,
                        "visual_id": spec["visual_id"],
                        "created_icons": [],
                        "message": "AI 判断成品中没有适合独立落库的组件。",
                    },
                    ensure_ascii=False,
                    indent=2,
                )
            )
            return 0

        result = run_apply(
            Path(__file__).resolve().parent,
            "extract_visual_icons_apply.js",
            {"notePath": note_path, "extractionSpec": spec},
            args.vault_name,
            args.timeout,
            vault_root,
        )
        result["plan"] = plan
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except VisualWriteError as exc:
        print(f"错误：{exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
