#!/usr/bin/env python3
"""Validate or synchronize the Markdown side of the project Icon index.

The registry is the source of truth for icon titles, keywords, and component paths.
The script never rewrites the Excalidraw Data section.
"""

from __future__ import annotations

import argparse
import difflib
import hashlib
import json
import os
import re
import sys
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

EXCALIDRAW_MARKER = b"# Excalidraw Data"
DEFAULT_REGISTRY = (
    Path(__file__).resolve().parent.parent / "references" / "icon-index-registry.json"
)
PRESERVED_PROPERTIES = ("date", "updated")


class IndexError(ValueError):
    """Raised when registry or index validation fails."""


def text(value: Any) -> str:
    return "" if value is None else str(value).strip()


def require_text(mapping: dict[str, Any], key: str, context: str) -> str:
    value = text(mapping.get(key))
    if not value:
        raise IndexError(f"{context} 缺少 {key}。")
    return value


def load_registry(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise IndexError(f"来源注册表不存在：{path}") from exc
    except json.JSONDecodeError as exc:
        raise IndexError(f"来源注册表 JSON 无效：{exc}") from exc
    if not isinstance(data, dict):
        raise IndexError("来源注册表顶层必须是对象。")
    if data.get("schema_version") != 1:
        raise IndexError("来源注册表 schema_version 必须为 1。")
    return data


def discover_vault_root(registry: dict[str, Any], explicit: Path | None) -> Path:
    index_path = Path(require_text(registry, "index_path", "来源注册表"))
    candidates = [explicit] if explicit else [Path.cwd(), Path.cwd() / "content"]
    for candidate in candidates:
        if candidate is not None:
            root = candidate.expanduser().resolve()
            if (root / index_path).is_file():
                return root
    tried = ", ".join(str(candidate) for candidate in candidates if candidate)
    raise IndexError(f"找不到 Vault 根目录；已检查：{tried}")


def split_index(raw: bytes) -> tuple[str, bytes]:
    position = raw.find(EXCALIDRAW_MARKER)
    if position < 0:
        raise IndexError("Icon 索引缺少 # Excalidraw Data，拒绝同步。")
    head = raw[:position].decode("utf-8")
    tail = raw[position:]
    if b"```compressed-json" not in tail:
        raise IndexError("Excalidraw Data 缺少 compressed-json，拒绝同步。")
    return head, tail


def preserved_properties(head: str) -> dict[str, str]:
    match = re.match(r"^---\n(.*?)\n---\n", head, re.DOTALL)
    if not match:
        raise IndexError("Icon 索引缺少有效 frontmatter。")
    result: dict[str, str] = {}
    for key in PRESERVED_PROPERTIES:
        field = re.search(rf"^{re.escape(key)}:\s*(.+)$", match.group(1), re.MULTILINE)
        if not field:
            raise IndexError(f"Icon 索引 frontmatter 缺少 {key}。")
        result[key] = field.group(1).strip()
    return result


def validate_http_url(value: str, context: str) -> None:
    parsed = urlparse(value)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise IndexError(f"{context} 不是有效 http/https URL：{value}")


def validate_native_icon_asset(path: Path, context: str) -> None:
    try:
        scene = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise IndexError(f"{context} 不是有效 Excalidraw JSON：{exc}") from exc
    if not isinstance(scene, dict) or scene.get("type") != "excalidraw":
        raise IndexError(f"{context} 不是纯 JSON Excalidraw 场景。")
    elements = [
        element
        for element in scene.get("elements", [])
        if isinstance(element, dict) and not element.get("isDeleted")
    ]
    if not elements:
        raise IndexError(f"{context} 没有有效原生元素。")
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
        raise IndexError(f"{context} 包含未描摹的 image/frame/embeddable：{kinds}")
    common_groups = set(elements[0].get("groupIds") or [])
    for element in elements[1:]:
        common_groups.intersection_update(element.get("groupIds") or [])
    if len(common_groups) != 1:
        raise IndexError(f"{context} 必须有且只有一个覆盖全部元素的公共 group。")


def validate_registry(registry: dict[str, Any], vault_root: Path) -> None:
    metadata = registry.get("metadata")
    if not isinstance(metadata, dict):
        raise IndexError("来源注册表 metadata 必须是对象。")
    for key in ("title", "type"):
        require_text(metadata, key, "metadata")
    for key in ("aliases", "tags"):
        values = metadata.get(key)
        if not isinstance(values, list) or not values or not all(text(x) for x in values):
            raise IndexError(f"metadata.{key} 必须是非空字符串数组。")

    asset_root = Path(require_text(registry, "asset_root", "来源注册表"))
    master_suffix = require_text(registry, "master_suffix", "来源注册表")

    groups = registry.get("source_groups")
    if not isinstance(groups, list) or not groups:
        raise IndexError("source_groups 必须是非空数组。")
    group_rules: dict[str, dict[str, Any]] = {}
    for number, group in enumerate(groups, start=1):
        if not isinstance(group, dict):
            raise IndexError(f"第 {number} 个 source_group 必须是对象。")
        group_id = require_text(group, "id", f"第 {number} 个 source_group")
        if group_id in group_rules:
            raise IndexError(f"source_group id 重复：{group_id}")
        require_text(group, "label", f"source_group {group_id}")
        require_text(group, "statement", f"source_group {group_id}")
        required_fields = group.get("required_entry_fields", [])
        if not isinstance(required_fields, list) or not all(
            text(field) for field in required_fields
        ):
            raise IndexError(
                f"source_group {group_id} 的 required_entry_fields 必须是字符串数组。"
            )
        group_rules[group_id] = group

    entries = registry.get("entries")
    if not isinstance(entries, list) or not entries:
        raise IndexError("entries 必须是非空数组。")
    ids: set[str] = set()
    assets: set[str] = set()
    for number, entry in enumerate(entries, start=1):
        if not isinstance(entry, dict):
            raise IndexError(f"第 {number} 个 entry 必须是对象。")
        context = f"第 {number} 个 entry"
        entry_id = require_text(entry, "id", context)
        title = require_text(entry, "title", context)
        asset = require_text(entry, "asset", context)
        if entry_id in ids:
            raise IndexError(f"entry id 重复：{entry_id}")
        if asset in assets:
            raise IndexError(f"asset 重复：{asset}")
        ids.add(entry_id)
        assets.add(asset)
        if Path(asset).name != entry_id:
            raise IndexError(f"{entry_id} 与 asset 文件名不一致：{asset}")
        if not entry_id.endswith(master_suffix):
            raise IndexError(f"{entry_id} 不符合母版后缀 {master_suffix}。")
        try:
            Path(asset).relative_to(asset_root)
        except ValueError as exc:
            raise IndexError(f"{entry_id} 不在 asset_root 下：{asset}") from exc
        asset_path = vault_root / asset
        if not asset_path.is_file():
            raise IndexError(f"{entry_id} 的实际文件不存在：{asset_path}")
        validate_native_icon_asset(asset_path, entry_id)
        if not title:
            raise IndexError(f"{entry_id} 缺少 title。")

        keywords = entry.get("keywords")
        if (
            not isinstance(keywords, list)
            or not 1 <= len(keywords) <= 8
            or not all(text(keyword) for keyword in keywords)
        ):
            raise IndexError(f"{entry_id} 的 keywords 必须包含 1–8 个非空字符串。")
        if len({text(keyword) for keyword in keywords}) != len(keywords):
            raise IndexError(f"{entry_id} 的 keywords 不能重复。")

        source_group = require_text(entry, "source_group", entry_id)
        if source_group not in group_rules:
            raise IndexError(f"{entry_id} 引用了未知 source_group：{source_group}")
        group_rule = group_rules[source_group]
        for field in group_rule.get("required_entry_fields", []):
            require_text(entry, text(field), entry_id)

        links = entry.get("links")
        if not isinstance(links, list) or not links:
            raise IndexError(f"{entry_id} 至少需要一个来源链接。")
        source_urls: list[str] = []
        for link_number, link in enumerate(links, start=1):
            if not isinstance(link, dict):
                raise IndexError(f"{entry_id} 的第 {link_number} 个来源必须是对象。")
            require_text(link, "label", f"{entry_id} 的第 {link_number} 个来源")
            url = require_text(link, "url", f"{entry_id} 的第 {link_number} 个来源")
            validate_http_url(url, f"{entry_id} 的第 {link_number} 个来源")
            source_urls.append(url)

        required_fragment = text(group_rule.get("required_url_fragment"))
        if required_fragment and not any(
            required_fragment in url for url in source_urls
        ):
            raise IndexError(
                f"{entry_id} 的来源 URL 未固定到要求的版本：{required_fragment}"
            )
        required_host = text(group_rule.get("required_url_host"))
        if required_host and not any(
            urlparse(url).netloc == required_host for url in source_urls
        ):
            raise IndexError(
                f"{entry_id} 的来源 URL 缺少要求的主机：{required_host}"
            )

    notices = registry.get("notices", [])
    if not isinstance(notices, list) or not all(text(notice) for notice in notices):
        raise IndexError("notices 必须是字符串数组。")


def render_frontmatter(metadata: dict[str, Any], preserved: dict[str, str]) -> str:
    lines = [
        "---",
        "excalidraw-plugin: parsed",
        f"title: {require_text(metadata, 'title', 'metadata')}",
        "aliases:",
    ]
    lines.extend(f"  - {text(value)}" for value in metadata["aliases"])
    lines.append("tags:")
    lines.extend(f"  - {text(value)}" for value in metadata["tags"])
    lines.extend(
        [
            f"type: {require_text(metadata, 'type', 'metadata')}",
            f"date: {preserved['date']}",
            f"updated: {preserved['updated']}",
            "---",
        ]
    )
    return "\n".join(lines)


def render_head(registry: dict[str, Any], preserved: dict[str, str]) -> str:
    metadata = registry["metadata"]
    title = text(metadata["title"])
    asset_root = text(registry["asset_root"])
    master_suffix = text(registry["master_suffix"])
    entries = registry["entries"]
    lines = [
        render_frontmatter(metadata, preserved),
        f"# {title}",
        "",
        "> [!info] 视觉词汇表",
        (
            f"> {len(entries)} 个 Excalidraw icon 组件统一存放于 `{asset_root}/`，"
            f"文件名以 `{master_suffix}` 结尾。本索引通过嵌入组件文件提供预览，"
            "并保留复用所需的检索关键词。"
        ),
        "",
        "> [!important] 标签是检索把手，不是意义定义",
        "> `关键词` 只用于找到可重组的视觉零件，不规定图标的固定含义。",
        "",
        "<!-- icon-index:start -->",
    ]

    for entry in entries:
        entry_id = text(entry["id"])
        keywords = ", ".join(f"`{text(keyword)}`" for keyword in entry["keywords"])
        lines.extend(
            [
                "",
                f"<!-- icon-entry:{entry_id}:start -->",
                f"## {text(entry['title'])}",
                "",
                f"![[{text(entry['asset'])}|180]]",
                "",
                f"- **关键词**：{keywords}",
                f"<!-- icon-entry:{entry_id}:end -->",
            ]
        )
    lines.extend(["", "<!-- icon-index:end -->", "", ""])
    return "\n".join(lines)


def show_diff(current: str, expected: str, index_path: Path) -> None:
    diff = difflib.unified_diff(
        current.splitlines(),
        expected.splitlines(),
        fromfile=str(index_path),
        tofile=f"{index_path}（registry）",
        lineterm="",
    )
    for line in diff:
        print(line)


def synchronize(
    registry_path: Path, vault_root: Path | None, check: bool, apply: bool
) -> int:
    registry = load_registry(registry_path)
    root = discover_vault_root(registry, vault_root)
    validate_registry(registry, root)
    index_path = root / text(registry["index_path"])
    raw = index_path.read_bytes()
    current_head, tail = split_index(raw)
    expected_head = render_head(registry, preserved_properties(current_head))
    tail_hash = hashlib.sha256(tail).hexdigest()

    if current_head == expected_head:
        print(f"Icon 索引已同步：{len(registry['entries'])} 个条目")
        print(f"Excalidraw Data SHA-256：{tail_hash}")
        return 0

    if check:
        print("Icon 索引与来源注册表不一致。", file=sys.stderr)
        show_diff(current_head, expected_head, index_path)
        return 1

    if not apply:
        raise IndexError("必须选择 --check 或 --apply。")

    replacement = expected_head.encode("utf-8") + tail
    temporary = index_path.with_name(f".{index_path.name}.tmp-icon-index-sync")
    temporary.write_bytes(replacement)
    os.replace(temporary, index_path)
    print(f"已同步 Icon 索引：{len(registry['entries'])} 个条目")
    print(f"已保留 Excalidraw Data SHA-256：{tail_hash}")
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="从固定来源注册表检查或同步 Icon 索引普通 Markdown。"
    )
    parser.add_argument(
        "--registry",
        type=Path,
        default=DEFAULT_REGISTRY,
        help=f"来源注册表路径（默认：{DEFAULT_REGISTRY}）",
    )
    parser.add_argument(
        "--vault-root",
        type=Path,
        help="Obsidian Vault 根目录；省略时检查当前目录及 ./content。",
    )
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true", help="只检查，不写文件。")
    mode.add_argument("--apply", action="store_true", help="同步普通 Markdown。")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        return synchronize(
            args.registry.expanduser().resolve(),
            args.vault_root,
            args.check,
            args.apply,
        )
    except (IndexError, OSError) as exc:
        print(f"错误：{exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
