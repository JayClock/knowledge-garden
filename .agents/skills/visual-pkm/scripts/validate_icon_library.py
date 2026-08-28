#!/usr/bin/env python3
"""Validate filename-indexed Excalidraw Icon Library components."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

DEFAULT_ASSET_ROOT = Path("Knowledge/Assets/Excalidraw")
ICON_NAME_PATTERN = re.compile(r"^Icon - (.+) - (.+)\.excalidraw$")


class LibraryError(ValueError):
    """Raised when the filename-indexed Icon Library is invalid."""


def discover_vault_root(explicit: Path | None, asset_root: Path) -> Path:
    candidates = [explicit] if explicit else [Path.cwd(), Path.cwd() / "content"]
    for candidate in candidates:
        if candidate is None:
            continue
        root = candidate.expanduser().resolve()
        if (root / asset_root).is_dir():
            return root
    tried = ", ".join(str(candidate) for candidate in candidates if candidate)
    raise LibraryError(f"找不到 Vault 根目录；已检查：{tried}")


def parse_icon_filename(name: str) -> tuple[list[str], str]:
    match = ICON_NAME_PATTERN.fullmatch(name)
    if not match:
        raise LibraryError(
            "Icon Library 文件名必须采用 "
            f"Icon - 关键词1, 关键词2 - 来源.excalidraw：{name}"
        )

    keywords = [item.strip() for item in match.group(1).split(",")]
    if not keywords or not all(keywords):
        raise LibraryError(f"文件名必须包含逗号分隔的非空关键词：{name}")
    if len({keyword.casefold() for keyword in keywords}) != len(keywords):
        raise LibraryError(f"文件名中的关键词不能重复：{name}")
    if any(" - " in keyword for keyword in keywords):
        raise LibraryError(f"关键词不能包含保留分隔符 ` - `：{name}")

    source = match.group(2).strip()
    if not source:
        raise LibraryError(f"文件名末尾必须标明来源：{name}")
    if "," in source or " - " in source:
        raise LibraryError(f"来源不能包含逗号或保留分隔符 ` - `：{name}")
    return keywords, source


def validate_native_icon_asset(path: Path) -> None:
    try:
        scene = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise LibraryError(f"{path.name} 不是有效 Excalidraw JSON：{exc}") from exc
    if not isinstance(scene, dict) or scene.get("type") != "excalidraw":
        raise LibraryError(f"{path.name} 不是纯 JSON Excalidraw 场景。")

    elements = [
        element
        for element in scene.get("elements", [])
        if isinstance(element, dict) and not element.get("isDeleted")
    ]
    if not elements:
        raise LibraryError(f"{path.name} 没有有效原生元素。")

    unsupported = [
        element
        for element in elements
        if element.get("type") in {"image", "frame", "embeddable"}
        or element.get("frameId") is not None
    ]
    if unsupported:
        kinds = ", ".join(
            f"{element.get('id', '<unknown>')}:{element.get('type', '<unknown>')}"
            for element in unsupported[:8]
        )
        raise LibraryError(f"{path.name} 包含 image/frame/embeddable：{kinds}")

    common_groups = set(elements[0].get("groupIds") or [])
    for element in elements[1:]:
        common_groups.intersection_update(element.get("groupIds") or [])
    if len(common_groups) != 1:
        raise LibraryError(f"{path.name} 必须有且只有一个覆盖全部元素的公共 group。")


def validate_library(vault_root: Path, asset_root: Path) -> int:
    paths = sorted((vault_root / asset_root).glob("Icon - *.excalidraw"))
    if not paths:
        raise LibraryError(f"没有找到 Icon Library 组件：{vault_root / asset_root}")
    for path in paths:
        parse_icon_filename(path.name)
        validate_native_icon_asset(path)
    return len(paths)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="只读检查 Icon Library 文件名与原生 Excalidraw 组件结构。"
    )
    parser.add_argument("--vault-root", type=Path, help="Obsidian Vault 根目录。")
    parser.add_argument(
        "--asset-root",
        type=Path,
        default=DEFAULT_ASSET_ROOT,
        help="相对 Vault 的 icon 组件目录。",
    )
    parser.add_argument("--check", action="store_true", help="只检查，不写文件。")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not args.check:
        print("错误：必须使用 --check；脚本不会自动改名或写入文件。", file=sys.stderr)
        return 2
    if args.asset_root.is_absolute():
        print("错误：--asset-root 必须是相对 Vault 的路径。", file=sys.stderr)
        return 2
    try:
        root = discover_vault_root(args.vault_root, args.asset_root)
        count = validate_library(root, args.asset_root)
        print(f"Icon Library 已通过检查：{count} 个组件")
        print("索引方式：Icon - 关键词1, 关键词2 - 来源.excalidraw")
        print("未使用 Markdown 清单或 JSON 注册表")
        return 0
    except (LibraryError, OSError) as exc:
        print(f"错误：{exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
