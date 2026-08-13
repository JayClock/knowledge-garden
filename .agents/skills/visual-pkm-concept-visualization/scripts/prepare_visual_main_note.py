#!/usr/bin/env python3
"""Initialize a Visual Main Note and embed selected Excalidraw icon components.

The script is intentionally split at the Obsidian boundary:
- Python validates the Step 4 selection, component files, target note, and dry-run plan.
- A bundled JavaScript payload performs Drawing conversion and image-reference writes
  inside the running Obsidian/Excalidraw plugin context.

It never edits Excalidraw compressed-json directly. Temporary image references must
be traced as native .excalidraw components before --apply and supplied with
--icon-map SRC=VAULT_PATH.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import re
import shutil
import subprocess
import sys
import time
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib.parse import unquote, urlparse

ID_PATTERN = re.compile(r"^A\d{2,}$")
ICON_PREFIX = "Knowledge/Assets/Excalidraw/Icon - "
ICON_SUFFIX = ".excalidraw"
NOTES_PREFIX = "Knowledge/Notes/"
PREVIEW_IMAGE_SUFFIXES = {".svg", ".png", ".jpg", ".jpeg", ".webp", ".gif", ".bmp"}
FORBIDDEN_TRACE_FIELDS = {
    "source_tier",
    "source_label",
    "source_url",
    "rights",
    "author",
    "detail_page",
    "asset_id",
}


class PreparationError(ValueError):
    """Raised when a plan is unsafe or incomplete."""


@dataclass(frozen=True)
class ResolvedIcon:
    candidate_id: str
    label: str
    role: str
    preview_src: str
    component_path: str | None
    requires_materialization: bool


def read_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise PreparationError(f"JSON 文件不存在：{path}") from exc
    except json.JSONDecodeError as exc:
        raise PreparationError(f"JSON 解析失败：{path}：{exc}") from exc
    if not isinstance(data, dict):
        raise PreparationError("Step 4 JSON 顶层必须是对象。")
    return data


def parse_selected(raw_values: list[str]) -> list[str]:
    selected: list[str] = []
    for raw in raw_values:
        for value in re.split(r"[，,\s]+", raw.strip()):
            if not value:
                continue
            candidate_id = value.upper()
            if not ID_PATTERN.fullmatch(candidate_id):
                raise PreparationError(f"无效入选编号：{value}；应类似 A01。")
            if candidate_id not in selected:
                selected.append(candidate_id)
    if not selected:
        raise PreparationError("至少需要一个入选编号。")
    if len(selected) > 3:
        raise PreparationError("最多选择 3 个候选。")
    return selected


def parse_icon_maps(raw_values: list[str]) -> dict[str, str]:
    mappings: dict[str, str] = {}
    for raw in raw_values:
        if "=" not in raw:
            raise PreparationError(
                f"无效 --icon-map：{raw}；格式应为 PREVIEW_SRC=VAULT_COMPONENT_PATH。"
            )
        source, target = (part.strip() for part in raw.split("=", 1))
        if not source or not target:
            raise PreparationError(f"无效 --icon-map：{raw}")
        if source in mappings and mappings[source] != target:
            raise PreparationError(f"同一预览素材存在冲突映射：{source}")
        mappings[source] = target
    return mappings


def resolve_source_path(src: str, vault_root: Path) -> Path:
    parsed = urlparse(src)
    scheme = parsed.scheme.lower()
    if scheme in {"http", "https", "data"}:
        raise PreparationError(f"入选 icon 不能使用远程或 data URL：{src}")
    if scheme == "file":
        return Path(unquote(parsed.path)).expanduser().resolve()
    if scheme:
        raise PreparationError(f"不支持的 icon src 协议：{src}")
    path = Path(src).expanduser()
    return (vault_root / path).resolve() if not path.is_absolute() else path.resolve()


def vault_relative_component(path_text: str, vault_root: Path) -> str:
    path = resolve_source_path(path_text, vault_root)
    try:
        relative = path.relative_to(vault_root).as_posix()
    except ValueError as exc:
        raise PreparationError(f"Excalidraw 组件必须位于 Vault 内：{path}") from exc
    if not relative.startswith(ICON_PREFIX) or not relative.endswith(ICON_SUFFIX):
        raise PreparationError(
            "组件必须直接位于 Knowledge/Assets/Excalidraw/，"
            f"并命名为 Icon - <名称>.excalidraw：{relative}"
        )
    return relative


def validate_component(path_text: str, vault_root: Path) -> dict[str, Any]:
    relative = vault_relative_component(path_text, vault_root)
    path = vault_root / relative
    try:
        scene = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise PreparationError(f"Excalidraw 组件不存在：{relative}") from exc
    except json.JSONDecodeError as exc:
        raise PreparationError(f"Excalidraw 组件 JSON 无效：{relative}：{exc}") from exc
    if not isinstance(scene, dict) or scene.get("type") != "excalidraw":
        raise PreparationError(f"组件不是 Excalidraw 场景：{relative}")
    elements = [
        element
        for element in scene.get("elements", [])
        if isinstance(element, dict) and not element.get("isDeleted")
    ]
    if not elements:
        raise PreparationError(f"组件没有有效元素：{relative}")
    invalid = [
        element.get("type")
        for element in elements
        if element.get("type") in {"image", "frame", "embeddable"}
        or element.get("frameId") is not None
    ]
    if invalid:
        raise PreparationError(f"组件包含嵌套 image/frame/embeddable：{relative}")
    common_groups = set(elements[0].get("groupIds") or [])
    for element in elements[1:]:
        common_groups.intersection_update(element.get("groupIds") or [])
    if len(common_groups) != 1:
        raise PreparationError(f"组件必须有且只有一个覆盖全部元素的公共 group：{relative}")
    colors = sorted(
        {
            str(element.get(field) or "").strip()
            for element in elements
            for field in ("strokeColor", "backgroundColor")
            if str(element.get(field) or "").strip()
        }
    )
    return {
        "path": relative,
        "elements": len(elements),
        "group_id": next(iter(common_groups)),
        "colors": colors,
        "colors_preserved": True,
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
    }


def resolve_icons(
    data: dict[str, Any],
    selected: list[str],
    icon_maps: dict[str, str],
    vault_root: Path,
) -> tuple[list[ResolvedIcon], list[dict[str, Any]]]:
    items = data.get("items")
    if not isinstance(items, list):
        raise PreparationError("Step 4 JSON 缺少 items 数组。")
    by_id: dict[str, dict[str, Any]] = {}
    for item in items:
        if not isinstance(item, dict):
            raise PreparationError("Step 4 items 中存在非对象候选。")
        item_id = str(item.get("id", "")).strip().upper()
        if not ID_PATTERN.fullmatch(item_id):
            raise PreparationError(f"Step 4 JSON 包含无效候选编号：{item_id or '<empty>'}")
        if item_id in by_id:
            raise PreparationError(f"Step 4 JSON 候选编号重复：{item_id}")
        by_id[item_id] = item
    missing = [item_id for item_id in selected if item_id not in by_id]
    if missing:
        raise PreparationError("Step 4 JSON 中找不到入选编号：" + "、".join(missing))

    resolved: list[ResolvedIcon] = []
    component_reports: dict[str, dict[str, Any]] = {}
    seen_components: set[str] = set()
    seen_pending: set[str] = set()
    for item_id in selected:
        item = by_id[item_id]
        icons = item.get("icons")
        if not isinstance(icons, list) or not icons:
            raise PreparationError(f"{item_id} 没有 icon。")
        for icon in icons:
            if not isinstance(icon, dict):
                raise PreparationError(f"{item_id} 包含无效 icon。")
            retained = sorted(FORBIDDEN_TRACE_FIELDS.intersection(icon))
            if retained:
                raise PreparationError(
                    f"{item_id} 不应保留素材追溯字段：" + "、".join(retained)
                )
            src = str(icon.get("src", "")).strip()
            if not src:
                raise PreparationError(f"{item_id} 的 icon 缺少 src。")
            label = str(icon.get("alt") or item.get("label") or item_id).strip()
            role = str(icon.get("role") or label).strip()
            mapped = icon_maps.get(src)
            source_path = resolve_source_path(src, vault_root)
            if mapped:
                component_path = vault_relative_component(mapped, vault_root)
                if component_path in seen_components:
                    continue
                component_reports[component_path] = validate_component(component_path, vault_root)
                seen_components.add(component_path)
                resolved.append(
                    ResolvedIcon(item_id, label, role, src, component_path, False)
                )
            elif source_path.suffix.lower() == ICON_SUFFIX:
                component_path = vault_relative_component(src, vault_root)
                if component_path in seen_components:
                    continue
                component_reports[component_path] = validate_component(component_path, vault_root)
                seen_components.add(component_path)
                resolved.append(
                    ResolvedIcon(item_id, label, role, src, component_path, False)
                )
            elif source_path.suffix.lower() in PREVIEW_IMAGE_SUFFIXES:
                pending_key = str(source_path)
                if pending_key in seen_pending:
                    continue
                if not source_path.is_file():
                    raise PreparationError(f"入选临时图像参考不存在：{source_path}")
                seen_pending.add(pending_key)
                resolved.append(ResolvedIcon(item_id, label, role, src, None, True))
            else:
                raise PreparationError(
                    "入选素材既不是 Vault `.excalidraw` 组件，也不是支持的"
                    f"临时图像参考：{src}"
                )
    if not resolved:
        raise PreparationError("入选候选没有解析出 icon。")
    return resolved, list(component_reports.values())


def safe_title(title: str) -> str:
    value = title.strip()
    if not value or value in {".", ".."}:
        raise PreparationError("新知识卡标题不能为空。")
    if any(character in value for character in '/\\:*?"<>|\n\r'):
        raise PreparationError(f"新知识卡标题包含文件名非法字符：{value}")
    if value.endswith(".") or value.endswith(" "):
        raise PreparationError("新知识卡标题不能以句点或空格结尾。")
    return value


def minimal_note_from_template(vault_root: Path, title: str, core_message: str) -> str:
    template_path = vault_root / "Templates/知识卡.md"
    try:
        template = template_path.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        raise PreparationError(f"知识卡模板不存在：{template_path}") from exc
    required_markers = ("up: []", "sources: []", "# {{title}}", "> [!abstract] 核心观点")
    missing = [marker for marker in required_markers if marker not in template]
    if missing:
        raise PreparationError("知识卡模板结构已变化，缺少：" + "、".join(missing))
    message = core_message.strip()
    if not message:
        raise PreparationError("创建新卡必须提供已确认的 --core-message。")
    quote = "\n".join("> " + line if line else ">" for line in message.splitlines())
    return (
        "---\n"
        "up: []\n"
        "sources: []\n"
        "---\n"
        f"# {title}\n\n"
        "> [!abstract] 核心观点\n"
        f"{quote}\n"
    )


def frontmatter_names(frontmatter: str) -> list[str]:
    names: list[str] = []
    lines = frontmatter.splitlines()
    for index, line in enumerate(lines):
        title_match = re.match(r"^title\s*:\s*(.+?)\s*$", line, re.IGNORECASE)
        if title_match:
            names.append(title_match.group(1).strip().strip("\"'"))
            continue
        aliases_match = re.match(r"^aliases\s*:\s*(.*?)\s*$", line, re.IGNORECASE)
        if not aliases_match:
            continue
        value = aliases_match.group(1).strip()
        if value.startswith("[") and value.endswith("]"):
            names.extend(
                item.strip().strip("\"'")
                for item in value[1:-1].split(",")
                if item.strip()
            )
        elif value:
            names.append(value.strip("\"'"))
        else:
            cursor = index + 1
            while cursor < len(lines):
                item = re.match(r"^\s+-\s+(.+?)\s*$", lines[cursor])
                if not item:
                    break
                names.append(item.group(1).strip().strip("\"'"))
                cursor += 1
    return names


def scan_exact_duplicates(vault_root: Path, title: str) -> list[str]:
    normalized = title.casefold().strip()
    candidates: set[str] = set()
    notes_root = vault_root / "Knowledge/Notes"
    for path in notes_root.glob("*.md"):
        if path.stem.casefold().strip() == normalized:
            candidates.add(path.relative_to(vault_root).as_posix())
            continue
        try:
            head = path.read_text(encoding="utf-8", errors="ignore")[:8000]
        except OSError:
            continue
        if not head.startswith("---"):
            continue
        end = head.find("\n---", 3)
        if end < 0:
            continue
        frontmatter = head[4:end]
        if any(name.casefold().strip() == normalized for name in frontmatter_names(frontmatter)):
            candidates.add(path.relative_to(vault_root).as_posix())
    return sorted(candidates)


def make_backup(vault_root: Path, target_path: str) -> str | None:
    source = vault_root / target_path
    if not source.is_file():
        return None
    timestamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_dir = Path("/tmp/visual-pkm-concept-visualization/backups")
    backup_dir.mkdir(parents=True, exist_ok=True)
    safe_name = target_path.replace("/", "__")
    destination = backup_dir / f"{timestamp}__{safe_name}"
    shutil.copy2(source, destination)
    return str(destination)


def parse_eval_value(stdout: str) -> Any:
    candidates = []
    for line in stdout.splitlines():
        stripped = line.strip()
        if stripped.startswith("=>"):
            candidates.append(stripped[2:].strip())
    if not candidates:
        return None
    raw = candidates[-1]
    try:
        parsed = json.loads(raw)
        if isinstance(parsed, str):
            try:
                parsed = json.loads(parsed)
            except json.JSONDecodeError:
                pass
        return parsed
    except json.JSONDecodeError as exc:
        raise PreparationError(f"无法解析 Obsidian eval 结果：{raw[:300]}") from exc


def run_apply(
    script_dir: Path,
    config: dict[str, Any],
    vault_name: str,
    timeout: int,
) -> dict[str, Any]:
    payload_path = script_dir / "prepare_visual_main_note_apply.js"
    try:
        payload = payload_path.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        raise PreparationError(f"缺少 Obsidian 执行脚本：{payload_path}") from exc
    run_id = uuid.uuid4().hex
    config["runId"] = run_id
    code = (
        "globalThis.__VISUAL_MAIN_NOTE_CONFIG__="
        + json.dumps(config, ensure_ascii=True, separators=(",", ":"))
        + ";\n"
        + payload
    )
    try:
        completed = subprocess.run(
            ["obsidian", f"vault={vault_name}", "eval", f"code={code}"],
            text=True,
            capture_output=True,
            timeout=timeout,
            check=False,
        )
    except FileNotFoundError as exc:
        raise PreparationError("找不到 obsidian CLI。") from exc
    except subprocess.TimeoutExpired as exc:
        raise PreparationError(f"Obsidian 执行超时（{timeout}s）。") from exc
    if completed.returncode != 0:
        details = (completed.stderr or completed.stdout).strip()
        raise PreparationError(f"Obsidian 执行失败：{details[:1000]}")

    immediate = parse_eval_value(completed.stdout)
    if isinstance(immediate, dict) and immediate.get("status") == "applied":
        return immediate

    deadline = time.monotonic() + timeout
    poll_code = (
        "(()=>{const r=globalThis.__VISUAL_MAIN_NOTE_RESULT__;"
        "return JSON.stringify(r??null)})()"
    )
    while time.monotonic() < deadline:
        polled = subprocess.run(
            ["obsidian", f"vault={vault_name}", "eval", f"code={poll_code}"],
            text=True,
            capture_output=True,
            timeout=min(30, max(1, int(deadline - time.monotonic()))),
            check=False,
        )
        if polled.returncode == 0:
            state = parse_eval_value(polled.stdout)
            if isinstance(state, dict) and state.get("runId") == run_id:
                if state.get("status") == "done" and isinstance(state.get("result"), dict):
                    return state["result"]
                if state.get("status") == "error":
                    message = state.get("error") or "未知错误"
                    raise PreparationError(f"Obsidian 执行失败：{message}")
        time.sleep(0.35)
    raise PreparationError(f"Obsidian 执行结果等待超时（{timeout}s）。")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="初始化 Visual Main Note，并嵌入 Step 4 入选的 Excalidraw icon。"
    )
    parser.add_argument("--preview-json", required=True, type=Path)
    parser.add_argument(
        "--selected",
        required=True,
        action="append",
        help="入选编号；可重复或使用逗号分隔，例如 A02,A05。",
    )
    target = parser.add_mutually_exclusive_group(required=True)
    target.add_argument("--existing", help="现有 Knowledge/Notes/*.md 路径。")
    target.add_argument("--new-title", help="新知识卡的名词短语标题。")
    parser.add_argument("--core-message", help="新知识卡已确认的核心观点。")
    parser.add_argument(
        "--duplicate-check-confirmed",
        action="store_true",
        help="确认已完成人工语义重复检查；新卡 --apply 必需。",
    )
    parser.add_argument(
        "--icon-map",
        action="append",
        default=[],
        help="把临时 src 映射到已原生化组件：SRC=Knowledge/.../Icon - X.excalidraw。",
    )
    parser.add_argument("--vault-root", type=Path, default=Path.cwd())
    parser.add_argument("--vault-name", default="content")
    parser.add_argument("--max-icon-size", type=float, default=180.0)
    parser.add_argument("--gap", type=float, default=48.0)
    parser.add_argument("--timeout", type=int, default=180)
    parser.add_argument(
        "--apply",
        action="store_true",
        help="执行写入；省略时只输出 dry-run 计划。",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        vault_root = args.vault_root.expanduser().resolve()
        if not (vault_root / ".obsidian").is_dir():
            raise PreparationError(f"不是 Obsidian Vault 根目录：{vault_root}")
        preview_json = args.preview_json.expanduser().resolve()
        selected = parse_selected(args.selected)
        icon_maps = parse_icon_maps(args.icon_map)
        data = read_json(preview_json)
        icons, component_reports = resolve_icons(
            data, selected, icon_maps, vault_root
        )
        pending = [icon for icon in icons if icon.requires_materialization]
        component_paths = [
            icon.component_path for icon in icons if icon.component_path is not None
        ]

        if args.existing:
            target_path = Path(args.existing).as_posix().lstrip("./")
            if not target_path.startswith(NOTES_PREFIX) or not target_path.endswith(".md"):
                raise PreparationError("--existing 必须指向 Knowledge/Notes/*.md。")
            target_file = vault_root / target_path
            if not target_file.is_file():
                raise PreparationError(f"现有知识卡不存在：{target_path}")
            mode = "existing"
            new_content = None
            duplicate_candidates: list[str] = []
            stat = target_file.stat()
            expected_mtime = int(stat.st_mtime * 1000)
            expected_size = stat.st_size
        else:
            title = safe_title(args.new_title)
            target_path = f"{NOTES_PREFIX}{title}.md"
            if (vault_root / target_path).exists():
                raise PreparationError(f"新知识卡目标已存在：{target_path}")
            mode = "new"
            new_content = minimal_note_from_template(
                vault_root, title, args.core_message or ""
            )
            duplicate_candidates = scan_exact_duplicates(vault_root, title)
            expected_mtime = None
            expected_size = None

        plan = {
            "status": "ready" if not pending else "needs_materialization",
            "mode": mode,
            "target_note": target_path,
            "preview_json": str(preview_json),
            "selected": selected,
            "components": component_paths,
            "component_validation": component_reports,
            "pending_temp_icons": [
                {
                    "candidate_id": icon.candidate_id,
                    "label": icon.label,
                    "role": icon.role,
                    "src": icon.preview_src,
                    "required_map": (
                        f"{icon.preview_src}=Knowledge/Assets/Excalidraw/"
                        f"Icon - <稳定名称>.excalidraw"
                    ),
                }
                for icon in pending
            ],
            "duplicate_candidates": duplicate_candidates,
            "color_policy": {
                "component_colors": "preserve",
                "icon_palette_gate": False,
                "project_palette_required": False,
                "new_canvas_default": "--concept-color-canvas",
                "final_target_check_required": False,
            },
            "writes": bool(args.apply),
        }
        if not args.apply:
            print(json.dumps(plan, ensure_ascii=False, indent=2))
            return 0
        if pending:
            raise PreparationError(
                "存在尚未描摹为原生 Excalidraw 的入选临时图像参考；"
                "先重建 `.excalidraw` 组件，再用 --icon-map 提供映射。"
            )
        if mode == "new":
            if duplicate_candidates:
                raise PreparationError(
                    "发现同名或 alias 候选，停止创建：" + "、".join(duplicate_candidates)
                )
            if not args.duplicate_check_confirmed:
                raise PreparationError(
                    "新卡 --apply 前必须完成人工语义重复检查，并传入 "
                    "--duplicate-check-confirmed。"
                )
        if args.max_icon_size <= 0 or args.gap < 0:
            raise PreparationError("--max-icon-size 必须大于 0，--gap 不能小于 0。")

        backup_path = make_backup(vault_root, target_path)
        config = {
            "mode": mode,
            "targetPath": target_path,
            "newContent": new_content,
            "expectedMtime": expected_mtime,
            "expectedSize": expected_size,
            "componentPaths": component_paths,
            "selected": selected,
            "maxIconSize": args.max_icon_size,
            "gap": args.gap,
        }
        try:
            result = run_apply(
                Path(__file__).resolve().parent,
                config,
                args.vault_name,
                args.timeout,
            )
        except PreparationError as exc:
            recovery = (
                f"；转换前备份：{backup_path}"
                if backup_path
                else f"；请检查可能已创建的目标：{target_path}"
            )
            raise PreparationError(f"{exc}{recovery}") from exc
        result["backup"] = backup_path
        result["plan"] = plan
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except PreparationError as exc:
        print(f"错误：{exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
