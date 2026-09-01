#!/usr/bin/env python3
"""Validate and write a complete native Excalidraw visual into a Visual Main Note.

The input is a high-level JSON visual specification produced from the user's confirmed
core message, framework, and textual style brief. Python validates the target and plan;
a bundled JavaScript payload uses the running Obsidian Excalidraw plugin to create the
Drawing and native elements. This script never edits compressed-json directly.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import math
import re
import shutil
import subprocess
import sys
import time
import uuid
from pathlib import Path
from threading import Event
from typing import Any

NOTES_PREFIX = "Knowledge/Notes/"
ICON_PREFIX = "Knowledge/Assets/Excalidraw/Icon - "
ALLOWED_TYPES = {"rectangle", "ellipse", "diamond", "line", "arrow", "text", "icon"}
REPRESENTATION_PRIORITY = [
    "library-icon",
    "native-pictogram",
    "shape-relation",
    "text",
]
LIBRARY_DECISIONS = {"reuse", "no-match", "rejected", "not-applicable"}
REQUIRED_HAND_DRAWN_AVOIDS = {"uniform-grid", "repeated-text-cards"}
VISUAL_ID_PATTERN = re.compile(r"^[a-z0-9][a-z0-9-]{2,63}$")
COLOR_PATTERN = re.compile(r"^(transparent|#[0-9a-fA-F]{6})$")


class VisualWriteError(ValueError):
    """Raised when a direct visual write would be unsafe or incomplete."""


def read_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise VisualWriteError(f"视觉规格不存在：{path}") from exc
    except json.JSONDecodeError as exc:
        raise VisualWriteError(f"视觉规格 JSON 无效：{path}：{exc}") from exc
    if not isinstance(data, dict):
        raise VisualWriteError("视觉规格顶层必须是对象。")
    return data


def finite_number(value: Any, field: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise VisualWriteError(f"{field} 必须是数字。")
    number = value
    if not math.isfinite(number):
        raise VisualWriteError(f"{field} 必须是有限数字。")
    return number


def positive_number(value: Any, field: str) -> float:
    number = finite_number(value, field)
    if number <= 0:
        raise VisualWriteError(f"{field} 必须大于 0。")
    return number


def validate_color(value: Any, field: str) -> str:
    color = str(value).strip()
    if not COLOR_PATTERN.fullmatch(color):
        raise VisualWriteError(f"{field} 必须是 #RRGGBB 或 transparent：{color}")
    return color


def validate_component_path(path_text: str, vault_root: Path) -> str:
    path = Path(path_text)
    if path.is_absolute():
        try:
            relative = path.resolve().relative_to(vault_root).as_posix()
        except ValueError as exc:
            raise VisualWriteError(f"复用 icon 必须位于 Vault 内：{path}") from exc
    else:
        relative = path.as_posix().lstrip("./")
    if not relative.startswith(ICON_PREFIX) or not relative.endswith(".excalidraw"):
        raise VisualWriteError(
            "复用 icon 必须是 Knowledge/Assets/Excalidraw/Icon - *.excalidraw："
            f"{relative}"
        )
    file_path = vault_root / relative
    if not file_path.is_file():
        raise VisualWriteError(f"复用 icon 不存在：{relative}")
    try:
        scene = json.loads(file_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise VisualWriteError(f"复用 icon JSON 无效：{relative}：{exc}") from exc
    elements = [
        element
        for element in scene.get("elements", [])
        if isinstance(element, dict) and not element.get("isDeleted")
    ]
    if not elements:
        raise VisualWriteError(f"复用 icon 没有有效元素：{relative}")
    if any(
        element.get("type") in {"image", "frame", "embeddable"}
        or element.get("frameId") is not None
        for element in elements
    ):
        raise VisualWriteError(f"复用 icon 不是纯原生组件：{relative}")
    common_groups = set(elements[0].get("groupIds") or [])
    for element in elements[1:]:
        common_groups.intersection_update(element.get("groupIds") or [])
    if len(common_groups) != 1:
        raise VisualWriteError(f"复用 icon 必须有唯一公共 group：{relative}")
    return relative


def validate_style(style: Any, field: str) -> dict[str, Any]:
    if style is None:
        return {}
    if not isinstance(style, dict):
        raise VisualWriteError(f"{field} 必须是对象。")
    normalized: dict[str, Any] = {}
    for key in ("strokeColor", "backgroundColor"):
        if key in style:
            normalized[key] = validate_color(style[key], f"{field}.{key}")
    if "strokeWidth" in style:
        normalized["strokeWidth"] = positive_number(style["strokeWidth"], f"{field}.strokeWidth")
    if "roughness" in style:
        roughness = finite_number(style["roughness"], f"{field}.roughness")
        if roughness < 0 or roughness > 2:
            raise VisualWriteError(f"{field}.roughness 必须在 0–2。")
        normalized["roughness"] = roughness
    if "opacity" in style:
        opacity = finite_number(style["opacity"], f"{field}.opacity")
        if opacity < 0 or opacity > 100:
            raise VisualWriteError(f"{field}.opacity 必须在 0–100。")
        normalized["opacity"] = opacity
    if "fontSize" in style:
        normalized["fontSize"] = positive_number(style["fontSize"], f"{field}.fontSize")
    for key, allowed in {
        "fillStyle": {"hachure", "cross-hatch", "solid", "zigzag"},
        "strokeStyle": {"solid", "dashed", "dotted"},
        "textAlign": {"left", "center", "right"},
        "verticalAlign": {"top", "middle", "bottom"},
        "startArrowHead": {
            "arrow", "bar", "circle", "circle_outline", "triangle",
            "triangle_outline", "diamond", "diamond_outline", "none",
        },
        "endArrowHead": {
            "arrow", "bar", "circle", "circle_outline", "triangle",
            "triangle_outline", "diamond", "diamond_outline", "none",
        },
    }.items():
        if key not in style:
            continue
        value = str(style[key]).strip()
        if value not in allowed:
            raise VisualWriteError(f"{field}.{key} 取值无效：{value}")
        normalized[key] = value
    return normalized


def validate_composition_plan(
    data: dict[str, Any], defaults: dict[str, Any]
) -> dict[str, Any]:
    raw = data.get("composition_plan")
    if not isinstance(raw, dict):
        raise VisualWriteError(
            "视觉规格缺少 composition_plan；必须先规划手绘而非机械式布局。"
        )
    style = str(raw.get("style", "")).strip()
    if style != "hand-drawn":
        raise VisualWriteError("composition_plan.style 必须是 hand-drawn。")
    spatial_grammar = str(raw.get("spatial_grammar", "")).strip()
    if not spatial_grammar:
        raise VisualWriteError("composition_plan.spatial_grammar 不能为空。")

    raw_cues = raw.get("hand_drawn_cues")
    if not isinstance(raw_cues, list) or not raw_cues:
        raise VisualWriteError("composition_plan.hand_drawn_cues 必须是非空数组。")
    cues = [str(value).strip() for value in raw_cues]
    if not all(cues) or len({value.casefold() for value in cues}) != len(cues):
        raise VisualWriteError("composition_plan.hand_drawn_cues 不能为空或重复。")

    raw_avoids = raw.get("avoids")
    if not isinstance(raw_avoids, list):
        raise VisualWriteError("composition_plan.avoids 必须是数组。")
    avoids = [str(value).strip() for value in raw_avoids]
    missing_avoids = sorted(REQUIRED_HAND_DRAWN_AVOIDS - set(avoids))
    if missing_avoids:
        raise VisualWriteError(
            "composition_plan.avoids 缺少：" + "、".join(missing_avoids)
        )

    reason = str(raw.get("reason", "")).strip()
    if not reason:
        raise VisualWriteError("composition_plan.reason 不能为空。")
    if defaults.get("roughness", 0) < 1:
        raise VisualWriteError("手绘构图要求 defaults.roughness 至少为 1。")
    return {
        "style": style,
        "spatial_grammar": spatial_grammar,
        "hand_drawn_cues": cues,
        "avoids": avoids,
        "reason": reason,
    }


def validate_representation_plan(
    data: dict[str, Any], elements: list[dict[str, Any]]
) -> dict[str, Any]:
    raw = data.get("representation_plan")
    if not isinstance(raw, dict):
        raise VisualWriteError(
            "视觉规格缺少 representation_plan；必须先执行 Icon First 表达规划。"
        )
    if raw.get("priority") != REPRESENTATION_PRIORITY:
        raise VisualWriteError(
            "representation_plan.priority 必须依次为 "
            + " → ".join(REPRESENTATION_PRIORITY)
            + "。"
        )

    elements_by_key = {str(element["key"]): element for element in elements}
    raw_units = raw.get("semantic_units")
    if not isinstance(raw_units, list) or not raw_units:
        raise VisualWriteError("representation_plan.semantic_units 必须是非空数组。")

    seen_roles: set[str] = set()
    library_icon_keys: set[str] = set()
    normalized_units: list[dict[str, Any]] = []
    summary = {choice: 0 for choice in REPRESENTATION_PRIORITY}
    for index, unit in enumerate(raw_units, start=1):
        field = f"representation_plan.semantic_units[{index}]"
        if not isinstance(unit, dict):
            raise VisualWriteError(f"{field} 必须是对象。")
        role = str(unit.get("role", "")).strip()
        if not role or role in seen_roles:
            raise VisualWriteError(f"{field}.role 不能为空或重复：{role or '<empty>'}")
        seen_roles.add(role)

        search_terms = unit.get("search_terms")
        if not isinstance(search_terms, list) or not search_terms:
            raise VisualWriteError(f"{field}.search_terms 必须是非空数组。")
        terms = [str(value).strip() for value in search_terms]
        if not all(terms) or len({value.casefold() for value in terms}) != len(terms):
            raise VisualWriteError(f"{field}.search_terms 不能为空或重复。")

        library_decision = str(unit.get("library_decision", "")).strip()
        if library_decision not in LIBRARY_DECISIONS:
            raise VisualWriteError(f"{field}.library_decision 无效：{library_decision}")
        choice = str(unit.get("choice", "")).strip()
        if choice not in REPRESENTATION_PRIORITY:
            raise VisualWriteError(f"{field}.choice 无效：{choice}")
        if choice == "library-icon" and library_decision != "reuse":
            raise VisualWriteError(f"{field} 选择 library-icon 时必须记录 decision=reuse。")
        if choice != "library-icon" and library_decision == "reuse":
            raise VisualWriteError(f"{field} 已记录 reuse，choice 必须是 library-icon。")
        if choice == "native-pictogram" and library_decision == "not-applicable":
            raise VisualWriteError(
                f"{field} 选择 native-pictogram 前必须搜索本地 icon，"
                "并记录 no-match 或 rejected。"
            )

        raw_keys = unit.get("element_keys")
        if not isinstance(raw_keys, list) or not raw_keys:
            raise VisualWriteError(f"{field}.element_keys 必须是非空数组。")
        element_keys = [str(value).strip() for value in raw_keys]
        if not all(element_keys) or len(set(element_keys)) != len(element_keys):
            raise VisualWriteError(f"{field}.element_keys 不能为空或重复。")
        missing = [key for key in element_keys if key not in elements_by_key]
        if missing:
            raise VisualWriteError(f"{field}.element_keys 不存在：{', '.join(missing)}")
        selected = [elements_by_key[key] for key in element_keys]
        selected_types = {str(element["type"]) for element in selected}
        if choice == "library-icon":
            icons = {
                str(element["key"])
                for element in selected
                if element["type"] == "icon"
            }
            if not icons:
                raise VisualWriteError(f"{field} 选择 library-icon 但没有引用 icon 元素。")
            library_icon_keys.update(icons)
        elif choice in {"native-pictogram", "shape-relation"}:
            if not selected_types.intersection(
                {"rectangle", "ellipse", "diamond", "line", "arrow"}
            ):
                raise VisualWriteError(f"{field} 没有可承担图形语义的原生元素。")
        elif selected_types != {"text"}:
            raise VisualWriteError(f"{field} 选择 text 时只能引用 text 元素。")

        reason = str(unit.get("reason", "")).strip()
        if not reason:
            raise VisualWriteError(f"{field}.reason 不能为空。")
        normalized_units.append(
            {
                "role": role,
                "search_terms": terms,
                "library_decision": library_decision,
                "choice": choice,
                "element_keys": element_keys,
                "reason": reason,
            }
        )
        summary[choice] += 1

    all_icon_keys = {
        str(element["key"]) for element in elements if element["type"] == "icon"
    }
    if library_icon_keys != all_icon_keys:
        missing = sorted(all_icon_keys - library_icon_keys)
        raise VisualWriteError(
            "以下 icon 元素未登记到 library-icon 语义角色：" + "、".join(missing)
        )

    raw_justifications = raw.get("text_justifications")
    if not isinstance(raw_justifications, list):
        raise VisualWriteError("representation_plan.text_justifications 必须是数组。")
    text_keys = {
        str(element["key"]) for element in elements if element["type"] == "text"
    }
    seen_text_keys: set[str] = set()
    text_justifications: list[dict[str, str]] = []
    for index, item in enumerate(raw_justifications, start=1):
        field = f"representation_plan.text_justifications[{index}]"
        if not isinstance(item, dict):
            raise VisualWriteError(f"{field} 必须是对象。")
        key = str(item.get("key", "")).strip()
        if key not in text_keys or key in seen_text_keys:
            raise VisualWriteError(f"{field}.key 不存在、不是 text 或重复：{key}")
        reason = str(item.get("reason", "")).strip()
        if not reason:
            raise VisualWriteError(f"{field}.reason 不能为空。")
        seen_text_keys.add(key)
        text_justifications.append({"key": key, "reason": reason})
    missing_text = sorted(text_keys - seen_text_keys)
    if missing_text:
        raise VisualWriteError(
            "以下文字元素缺少必要性说明：" + "、".join(missing_text)
        )
    if not any(summary[choice] for choice in REPRESENTATION_PRIORITY[:-1]):
        raise VisualWriteError("Icon First 失败：主要语义不能全部由文字承担。")

    return {
        "priority": list(REPRESENTATION_PRIORITY),
        "semantic_units": normalized_units,
        "text_justifications": text_justifications,
        "summary": summary,
    }


def validate_visual_spec(data: dict[str, Any], vault_root: Path) -> dict[str, Any]:
    visual_id = str(data.get("visual_id", "")).strip()
    if not VISUAL_ID_PATTERN.fullmatch(visual_id):
        raise VisualWriteError("visual_id 必须是 3–64 位小写字母、数字或连字符。")
    core_message = str(data.get("core_message", "")).strip()
    if not core_message:
        raise VisualWriteError("视觉规格缺少 core_message。")
    framework = str(data.get("framework", "")).strip()
    if not framework:
        raise VisualWriteError("视觉规格缺少 framework。")
    style_brief = str(data.get("style_brief", "")).strip()
    if not style_brief:
        raise VisualWriteError("视觉规格缺少用户文字 style_brief。")

    canvas = data.get("canvas") or {}
    if not isinstance(canvas, dict):
        raise VisualWriteError("canvas 必须是对象。")
    normalized_canvas: dict[str, Any] = {
        "width": positive_number(canvas.get("width", 1200), "canvas.width"),
        "height": positive_number(canvas.get("height", 800), "canvas.height"),
    }
    if "background" in canvas:
        normalized_canvas["background"] = validate_color(
            canvas["background"], "canvas.background"
        )

    defaults = validate_style(data.get("defaults"), "defaults")
    composition_plan = validate_composition_plan(data, defaults)
    raw_elements = data.get("elements")
    if not isinstance(raw_elements, list) or not raw_elements:
        raise VisualWriteError("elements 必须是非空数组。")

    seen_keys: set[str] = set()
    normalized_elements: list[dict[str, Any]] = []
    reused_components: set[str] = set()
    for index, raw in enumerate(raw_elements, start=1):
        field = f"elements[{index}]"
        if not isinstance(raw, dict):
            raise VisualWriteError(f"{field} 必须是对象。")
        key = str(raw.get("key", "")).strip()
        if not key or key in seen_keys:
            raise VisualWriteError(f"{field}.key 不能为空或重复：{key or '<empty>'}")
        seen_keys.add(key)
        kind = str(raw.get("type", "")).strip()
        if kind not in ALLOWED_TYPES:
            raise VisualWriteError(f"{field}.type 不支持：{kind}")
        element_style = validate_style(raw.get("style"), f"{field}.style")
        effective_roughness = element_style.get(
            "roughness", defaults.get("roughness", 0)
        )
        if kind not in {"text", "icon"} and effective_roughness < 1:
            raise VisualWriteError(
                f"{field} 的有效 roughness 必须至少为 1，避免机械式线条。"
            )
        element: dict[str, Any] = {
            "key": key,
            "type": kind,
            "role": str(raw.get("role", "visual-element")).strip() or "visual-element",
            "group": str(raw.get("group", "")).strip() or None,
            "style": element_style,
        }
        if kind in {"rectangle", "ellipse", "diamond", "text", "icon"}:
            element["x"] = finite_number(raw.get("x"), f"{field}.x")
            element["y"] = finite_number(raw.get("y"), f"{field}.y")
        if kind in {"rectangle", "ellipse", "diamond"}:
            element["width"] = positive_number(raw.get("width"), f"{field}.width")
            element["height"] = positive_number(raw.get("height"), f"{field}.height")
        elif kind == "text":
            text = str(raw.get("text", "")).strip()
            if not text:
                raise VisualWriteError(f"{field}.text 不能为空。")
            element["text"] = text
            if "width" in raw:
                element["width"] = positive_number(raw["width"], f"{field}.width")
            element["textAlign"] = str(raw.get("textAlign", "left")).strip()
            if element["textAlign"] not in {"left", "center", "right"}:
                raise VisualWriteError(f"{field}.textAlign 无效。")
        elif kind in {"line", "arrow"}:
            raw_points = raw.get("points")
            if not isinstance(raw_points, list) or len(raw_points) < 2:
                raise VisualWriteError(f"{field}.points 至少需要两个点。")
            element["points"] = [
                [
                    finite_number(point[0], f"{field}.points[{point_index}].x"),
                    finite_number(point[1], f"{field}.points[{point_index}].y"),
                ]
                for point_index, point in enumerate(raw_points, start=1)
                if isinstance(point, list) and len(point) >= 2
            ]
            if len(element["points"]) != len(raw_points):
                raise VisualWriteError(f"{field}.points 中存在无效坐标。")
        elif kind == "icon":
            component = validate_component_path(str(raw.get("path", "")), vault_root)
            element["path"] = component
            reused_components.add(component)
            if "width" in raw:
                element["width"] = positive_number(raw["width"], f"{field}.width")
            if "height" in raw:
                element["height"] = positive_number(raw["height"], f"{field}.height")
        normalized_elements.append(element)

    groups = sorted(
        {str(element["group"]) for element in normalized_elements if element["group"]}
    )
    representation_plan = validate_representation_plan(data, normalized_elements)
    normalized = {
        "version": 1,
        "visual_id": visual_id,
        "core_message": core_message,
        "framework": framework,
        "style_brief": style_brief,
        "canvas": normalized_canvas,
        "defaults": defaults,
        "composition_plan": composition_plan,
        "representation_plan": representation_plan,
        "elements": normalized_elements,
        "groups": groups,
        "reused_components": sorted(reused_components),
    }
    return normalized


def safe_title(title: str) -> str:
    value = title.strip()
    if not value or value in {".", ".."}:
        raise VisualWriteError("新知识卡标题不能为空。")
    if any(character in value for character in '/\\:*?"<>|\n\r'):
        raise VisualWriteError(f"新知识卡标题包含非法字符：{value}")
    return value


def minimal_note_from_template(vault_root: Path, title: str, core_message: str) -> str:
    template_path = vault_root / "Templates/知识卡.md"
    try:
        template = template_path.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        raise VisualWriteError(f"知识卡模板不存在：{template_path}") from exc
    required = ("up: []", "sources: []", "# {{title}}", "> [!abstract] 核心观点")
    missing = [marker for marker in required if marker not in template]
    if missing:
        raise VisualWriteError("知识卡模板结构已变化，缺少：" + "、".join(missing))
    quote = "\n".join("> " + line if line else ">" for line in core_message.splitlines())
    return (
        "---\nup: []\nsources: []\n---\n"
        f"# {title}\n\n> [!abstract] 核心观点\n{quote}\n"
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
    for path in (vault_root / "Knowledge/Notes").glob("*.md"):
        if path.stem.casefold().strip() == normalized:
            candidates.add(path.relative_to(vault_root).as_posix())
            continue
        head = path.read_text(encoding="utf-8", errors="ignore")[:8000]
        if not head.startswith("---"):
            continue
        end = head.find("\n---", 3)
        if end >= 0 and any(
            name.casefold().strip() == normalized
            for name in frontmatter_names(head[4:end])
        ):
            candidates.add(path.relative_to(vault_root).as_posix())
    return sorted(candidates)


def make_backup(vault_root: Path, target_path: str) -> str | None:
    source = vault_root / target_path
    if not source.is_file():
        return None
    backup_dir = Path("/tmp/visual-pkm-concept-visualization/backups")
    backup_dir.mkdir(parents=True, exist_ok=True)
    stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    destination = backup_dir / f"{stamp}__{target_path.replace('/', '__')}"
    shutil.copy2(source, destination)
    return str(destination)


def parse_eval_value(stdout: str) -> Any:
    candidates = [
        line.strip()[2:].strip()
        for line in stdout.splitlines()
        if line.strip().startswith("=>")
    ]
    if not candidates:
        return None
    try:
        parsed = json.loads(candidates[-1])
        if isinstance(parsed, str):
            try:
                return json.loads(parsed)
            except json.JSONDecodeError:
                return parsed
        return parsed
    except json.JSONDecodeError as exc:
        raise VisualWriteError(f"无法解析 Obsidian eval 结果：{candidates[-1][:300]}") from exc


def run_apply(
    script_dir: Path,
    payload_name: str,
    config: dict[str, Any],
    vault_name: str,
    timeout: int,
    vault_root: Path | None = None,
) -> dict[str, Any]:
    payload_path = script_dir / payload_name
    try:
        payload = payload_path.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        raise VisualWriteError(f"缺少 Obsidian 执行脚本：{payload_path}") from exc
    run_id = uuid.uuid4().hex
    config["runId"] = run_id
    transport_paths: list[Path] = []
    if vault_root is None:
        code = (
            "globalThis.__VISUAL_MAIN_NOTE_CONFIG__="
            + json.dumps(config, ensure_ascii=True, separators=(",", ":"))
            + ";\n"
            + payload
        )
    else:
        config_name = f".tmp_visual-pkm-run-{run_id}.json"
        payload_name_in_vault = f".tmp_visual-pkm-run-{run_id}.js"
        config_path = vault_root / config_name
        payload_copy_path = vault_root / payload_name_in_vault
        config_path.write_text(
            json.dumps(config, ensure_ascii=False, separators=(",", ":")),
            encoding="utf-8",
        )
        payload_copy_path.write_text(payload, encoding="utf-8")
        transport_paths.extend([config_path, payload_copy_path])
        code = (
            "(async()=>{const [c,s]=await Promise.all(["
            f"app.vault.adapter.read({json.dumps(config_name)}),"
            f"app.vault.adapter.read({json.dumps(payload_name_in_vault)})"
            "]);globalThis.__VISUAL_MAIN_NOTE_CONFIG__=JSON.parse(c);"
            "return await globalThis.eval(s)})()"
        )
    try:
        try:
            completed = subprocess.run(
                ["obsidian", f"vault={vault_name}", "eval", f"code={code}"],
                text=True,
                capture_output=True,
                timeout=timeout,
                check=False,
            )
        except FileNotFoundError as exc:
            raise VisualWriteError("找不到 obsidian CLI。") from exc
        except subprocess.TimeoutExpired as exc:
            raise VisualWriteError(f"Obsidian 执行超时（{timeout}s）。") from exc
        if completed.returncode != 0:
            details = (completed.stderr or completed.stdout).strip()
            raise VisualWriteError(f"Obsidian 执行失败：{details[:1000]}")
        immediate = parse_eval_value(completed.stdout)
        if isinstance(immediate, dict) and immediate.get("status") == "applied":
            return immediate

        deadline = time.monotonic() + timeout
        poll_code = (
            "(()=>{const r=globalThis.__VISUAL_MAIN_NOTE_RESULT__;"
            "return JSON.stringify(r??null)})()"
        )
        poll_wait = Event()
        while time.monotonic() < deadline:
            polled = subprocess.run(
                ["obsidian", f"vault={vault_name}", "eval", f"code={poll_code}"],
                text=True,
                capture_output=True,
                timeout=min(30.0, max(1.0, deadline - time.monotonic())),
                check=False,
            )
            if polled.returncode == 0:
                state = parse_eval_value(polled.stdout)
                if isinstance(state, dict) and state.get("runId") == run_id:
                    if state.get("status") == "done" and isinstance(
                        state.get("result"), dict
                    ):
                        return state["result"]
                    if state.get("status") == "error":
                        raise VisualWriteError(
                            f"Obsidian 执行失败：{state.get('error') or '未知错误'}"
                        )
            poll_wait.wait(0.35)
        raise VisualWriteError(f"Obsidian 执行结果等待超时（{timeout}s）。")
    finally:
        for path in transport_paths:
            path.unlink(missing_ok=True)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="把用户确认的完整视觉规格直接写入 Visual Main Note。"
    )
    parser.add_argument("--visual-spec", required=True, type=Path)
    target = parser.add_mutually_exclusive_group(required=True)
    target.add_argument("--existing", help="现有 Knowledge/Notes/*.md 路径。")
    target.add_argument("--new-title", help="新知识卡的名词短语标题。")
    parser.add_argument("--core-message", help="新卡已确认的核心观点；默认取视觉规格。")
    parser.add_argument(
        "--duplicate-check-confirmed",
        action="store_true",
        help="确认 AI 已完成人工语义重复检查；新卡 --apply 必需。",
    )
    parser.add_argument("--vault-root", type=Path, default=Path.cwd())
    parser.add_argument("--vault-name", default="content")
    parser.add_argument("--timeout", type=int, default=180)
    parser.add_argument("--apply", action="store_true", help="执行写入；省略时只输出计划。")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        vault_root = args.vault_root.expanduser().resolve()
        if not (vault_root / ".obsidian").is_dir():
            raise VisualWriteError(f"不是 Obsidian Vault 根目录：{vault_root}")
        spec_path = args.visual_spec.expanduser().resolve()
        spec = validate_visual_spec(read_json(spec_path), vault_root)
        spec_hash = hashlib.sha256(
            json.dumps(spec, ensure_ascii=False, sort_keys=True).encode("utf-8")
        ).hexdigest()

        if args.existing:
            target_path = Path(args.existing).as_posix().lstrip("./")
            if not target_path.startswith(NOTES_PREFIX) or not target_path.endswith(".md"):
                raise VisualWriteError("--existing 必须指向 Knowledge/Notes/*.md。")
            target_file = vault_root / target_path
            if not target_file.is_file():
                raise VisualWriteError(f"现有知识卡不存在：{target_path}")
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
                raise VisualWriteError(f"新知识卡目标已存在：{target_path}")
            mode = "new"
            core_message = str(args.core_message or spec["core_message"]).strip()
            new_content = minimal_note_from_template(vault_root, title, core_message)
            duplicate_candidates = scan_exact_duplicates(vault_root, title)
            expected_mtime = None
            expected_size = None

        plan = {
            "status": "ready",
            "mode": mode,
            "target_note": target_path,
            "visual_id": spec["visual_id"],
            "framework": spec["framework"],
            "style_brief": spec["style_brief"],
            "elements": len(spec["elements"]),
            "groups": spec["groups"],
            "reused_components": spec["reused_components"],
            "icon_first": True,
            "composition_style": spec["composition_plan"]["style"],
            "spatial_grammar": spec["composition_plan"]["spatial_grammar"],
            "hand_drawn_cues": spec["composition_plan"]["hand_drawn_cues"],
            "representation_summary": spec["representation_plan"]["summary"],
            "justified_text_elements": len(
                spec["representation_plan"]["text_justifications"]
            ),
            "duplicate_candidates": duplicate_candidates,
            "spec_sha256": spec_hash,
            "writes": bool(args.apply),
        }
        if not args.apply:
            print(json.dumps(plan, ensure_ascii=False, indent=2))
            return 0
        if mode == "new":
            if duplicate_candidates:
                raise VisualWriteError(
                    "发现同名或 alias 候选，停止创建：" + "、".join(duplicate_candidates)
                )
            if not args.duplicate_check_confirmed:
                raise VisualWriteError(
                    "新卡 --apply 前必须由 AI 完成语义重复检查，并传入 "
                    "--duplicate-check-confirmed。"
                )

        backup_path = make_backup(vault_root, target_path)
        config = {
            "mode": mode,
            "targetPath": target_path,
            "newContent": new_content,
            "expectedMtime": expected_mtime,
            "expectedSize": expected_size,
            "visualSpec": spec,
            "specHash": spec_hash,
        }
        try:
            result = run_apply(
                Path(__file__).resolve().parent,
                "write_visual_main_note_apply.js",
                config,
                args.vault_name,
                args.timeout,
                vault_root,
            )
        except VisualWriteError as exc:
            recovery = (
                f"；转换前备份：{backup_path}"
                if backup_path
                else f"；请检查可能已创建的目标：{target_path}"
            )
            raise VisualWriteError(f"{exc}{recovery}") from exc
        result["backup"] = backup_path
        result["plan"] = plan
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except VisualWriteError as exc:
        print(f"错误：{exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
