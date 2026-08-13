#!/usr/bin/env python3
"""Render Step 4 visual references as a standalone HTML preview."""

from __future__ import annotations

import argparse
import base64
import html
import json
import mimetypes
import re
import sys
import webbrowser
from pathlib import Path
from typing import Any
from urllib.parse import unquote, urlparse

BASE_PALETTE_KEYS = (
    "ink",
    "deep-structure",
    "positive-flow",
    "cool-fill",
    "warm-fill",
    "attention",
    "friction",
    "conflict",
    "canvas",
)
ID_PATTERN = re.compile(r"^A\d{2,}$")
REMOTE_SCHEMES = {"http", "https"}


class PoolError(ValueError):
    """Raised when association-pool input is invalid."""


def text(value: Any) -> str:
    return "" if value is None else str(value).strip()


def html_text(value: Any) -> str:
    return html.escape(text(value), quote=True)


def read_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise PoolError(f"JSON 文件不存在：{path}") from exc
    except json.JSONDecodeError as exc:
        raise PoolError(f"JSON 解析失败：{exc}") from exc
    if not isinstance(data, dict):
        raise PoolError("JSON 顶层必须是对象。")
    return data


def read_palette(path: Path) -> dict[str, str]:
    try:
        css = path.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        raise PoolError(f"色板 CSS 不存在：{path}") from exc

    palette: dict[str, str] = {}
    for key in BASE_PALETTE_KEYS:
        match = re.search(
            rf"--concept-color-{re.escape(key)}\s*:\s*(#[0-9a-fA-F]{{6}})\s*;",
            css,
        )
        if not match:
            raise PoolError(f"色板缺少 --concept-color-{key}。")
        palette[key] = match.group(1).upper()
    return palette


def local_path_from_src(src: str, asset_root: Path) -> Path:
    parsed = urlparse(src)
    scheme = parsed.scheme.lower()
    if scheme in REMOTE_SCHEMES or scheme == "data":
        raise PoolError(
            "第 4 步 icon src 只能使用本地已描摹 Excalidraw 组件或临时图像参考，"
            "不能嵌入远程 URL 或 data:image。所有非 Excalidraw 入选项都必须在"
            "第 5 步先描摹为原生组件。"
        )
    if scheme == "file":
        return Path(unquote(parsed.path)).expanduser().resolve()
    if scheme:
        raise PoolError(f"不支持的 icon src 协议：{src}")
    candidate = Path(src).expanduser()
    if not candidate.is_absolute():
        candidate = asset_root / candidate
    return candidate.resolve()


def svg_color(value: Any, fallback: str = "none") -> str:
    color = text(value)
    return fallback if not color or color == "transparent" else color


def excalidraw_component_to_svg(path: Path) -> bytes:
    try:
        scene = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise PoolError(f"Excalidraw icon JSON 无效：{path}：{exc}") from exc
    elements = [
        element
        for element in scene.get("elements", [])
        if isinstance(element, dict) and not element.get("isDeleted")
    ]
    if not elements:
        raise PoolError(f"Excalidraw icon 没有可渲染元素：{path}")

    min_x = min(float(element.get("x", 0)) for element in elements)
    min_y = min(float(element.get("y", 0)) for element in elements)
    max_x = max(
        float(element.get("x", 0)) + abs(float(element.get("width", 0)))
        for element in elements
    )
    max_y = max(
        float(element.get("y", 0)) + abs(float(element.get("height", 0)))
        for element in elements
    )
    width = max(max_x - min_x, 1.0)
    height = max(max_y - min_y, 1.0)
    padding = max(6.0, min(max(width, height) * 0.04, 24.0))
    view_x = min_x - padding
    view_y = min_y - padding
    view_width = width + padding * 2
    view_height = height + padding * 2

    rendered: list[str] = []
    for element in elements:
        kind = text(element.get("type"))
        x = float(element.get("x", 0))
        y = float(element.get("y", 0))
        element_width = abs(float(element.get("width", 0)))
        element_height = abs(float(element.get("height", 0)))
        stroke = svg_color(element.get("strokeColor"), "none")
        fill = svg_color(element.get("backgroundColor"), "none")
        stroke_width = max(float(element.get("strokeWidth", 1)), 0.5)
        opacity = max(0.0, min(float(element.get("opacity", 100)) / 100.0, 1.0))
        angle = float(element.get("angle", 0))
        transform = ""
        if angle:
            degrees = angle * 180.0 / 3.141592653589793
            center_x = x + element_width / 2
            center_y = y + element_height / 2
            transform = f' transform="rotate({degrees:.6f} {center_x:.6f} {center_y:.6f})"'
        style = (
            f' fill="{html.escape(fill, quote=True)}"'
            f' stroke="{html.escape(stroke, quote=True)}"'
            f' stroke-width="{stroke_width:.3f}" opacity="{opacity:.3f}"'
            ' stroke-linecap="round" stroke-linejoin="round"'
        )

        if kind == "rectangle":
            radius = min(12.0, element_width / 4, element_height / 4) if element.get("roundness") else 0
            rendered.append(
                f'<rect x="{x:.6f}" y="{y:.6f}" width="{element_width:.6f}" '
                f'height="{element_height:.6f}" rx="{radius:.6f}"{style}{transform}/>'
            )
        elif kind == "ellipse":
            rendered.append(
                f'<ellipse cx="{x + element_width / 2:.6f}" cy="{y + element_height / 2:.6f}" '
                f'rx="{element_width / 2:.6f}" ry="{element_height / 2:.6f}"{style}{transform}/>'
            )
        elif kind in {"line", "arrow", "freedraw"}:
            raw_points = element.get("points", [])
            points = [
                (x + float(point[0]), y + float(point[1]))
                for point in raw_points
                if isinstance(point, list) and len(point) >= 2
            ]
            if len(points) < 2:
                continue
            point_text = " ".join(f"{px:.6f},{py:.6f}" for px, py in points)
            closed = len(points) >= 3 and (
                abs(points[0][0] - points[-1][0]) < 0.001
                and abs(points[0][1] - points[-1][1]) < 0.001
            )
            tag = "polygon" if closed or fill != "none" else "polyline"
            rendered.append(f'<{tag} points="{point_text}" fill-rule="evenodd"{style}{transform}/>')
        elif kind == "diamond":
            points = " ".join(
                f"{px:.6f},{py:.6f}"
                for px, py in (
                    (x + element_width / 2, y),
                    (x + element_width, y + element_height / 2),
                    (x + element_width / 2, y + element_height),
                    (x, y + element_height / 2),
                )
            )
            rendered.append(f'<polygon points="{points}"{style}{transform}/>')
        elif kind == "text":
            content = html.escape(text(element.get("text") or element.get("rawText")))
            font_size = float(element.get("fontSize", 20))
            rendered.append(
                f'<text x="{x:.6f}" y="{y + font_size:.6f}" '
                f'font-size="{font_size:.3f}" fill="{html.escape(stroke, quote=True)}"'
                f' opacity="{opacity:.3f}"{transform}>{content}</text>'
            )
        else:
            raise PoolError(f"Excalidraw icon 包含暂不支持的元素类型 {kind}：{path}")

    if not rendered:
        raise PoolError(f"Excalidraw icon 没有生成 SVG 图形：{path}")
    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" '
        f'viewBox="{view_x:.6f} {view_y:.6f} {view_width:.6f} {view_height:.6f}" '
        'preserveAspectRatio="xMidYMid meet">'
        + "".join(rendered)
        + "</svg>"
    )
    return svg.encode("utf-8")


def icon_src_to_html(src: str, asset_root: Path) -> str:
    local_path = local_path_from_src(src, asset_root)
    if not local_path.is_file():
        raise PoolError(f"icon 文件不存在：{local_path}")
    if local_path.suffix.lower() == ".excalidraw":
        mime = "image/svg+xml"
        raw = excalidraw_component_to_svg(local_path)
    else:
        mime = mimetypes.guess_type(local_path.name)[0]
        if mime == "image/svg+xml" or local_path.suffix.lower() == ".svg":
            mime = "image/svg+xml"
        if not mime or not mime.startswith("image/"):
            raise PoolError(f"icon 不是支持的图片或 Excalidraw 组件：{local_path}")
        raw = local_path.read_bytes()
    payload = base64.b64encode(raw).decode("ascii")
    return f"data:{mime};base64,{payload}"


def validate_pool(
    data: dict[str, Any], min_items: int, max_items: int
) -> list[dict[str, Any]]:
    if not text(data.get("title")):
        raise PoolError("缺少 title。")
    if not text(data.get("core_message")):
        raise PoolError("缺少 core_message。")
    items = data.get("items")
    if not isinstance(items, list):
        raise PoolError("items 必须是数组。")
    if not min_items <= len(items) <= max_items:
        raise PoolError(
            f"候选数量为 {len(items)}；当前要求 {min_items}–{max_items} 个。"
        )

    seen: set[str] = set()
    normalized: list[dict[str, Any]] = []
    required_fields = ("id", "type", "label", "visualization", "emphasis")
    for index, raw_item in enumerate(items, start=1):
        if not isinstance(raw_item, dict):
            raise PoolError(f"第 {index} 个候选必须是对象。")
        for field in required_fields:
            if not text(raw_item.get(field)):
                raise PoolError(f"第 {index} 个候选缺少 {field}。")
        item_id = text(raw_item["id"])
        if not ID_PATTERN.fullmatch(item_id):
            raise PoolError(f"无效联想编号：{item_id}；应类似 A01。")
        if item_id in seen:
            raise PoolError(f"联想编号重复：{item_id}")
        seen.add(item_id)

        icons = raw_item.get("icons")
        if not isinstance(icons, list) or not icons:
            raise PoolError(f"{item_id} 至少需要一个真实 icon 素材。")
        if len(icons) > 3:
            raise PoolError(f"{item_id} 最多使用 3 个 icon，避免预览失焦。")
        for icon_index, icon in enumerate(icons, start=1):
            if not isinstance(icon, dict):
                raise PoolError(f"{item_id} 的第 {icon_index} 个 icon 必须是对象。")
            for field in ("src", "alt", "role"):
                if not text(icon.get(field)):
                    raise PoolError(f"{item_id} 的第 {icon_index} 个 icon 缺少 {field}。")
            forbidden_trace_fields = (
                "source_tier",
                "source_label",
                "source_url",
                "rights",
                "author",
                "detail_page",
                "asset_id",
            )
            retained = [field for field in forbidden_trace_fields if field in icon]
            if retained:
                raise PoolError(
                    f"{item_id} 的第 {icon_index} 个 icon 不应保留素材追溯字段："
                    + "、".join(retained)
                )
        normalized.append(raw_item)
    return normalized


def render_icon(icon: dict[str, Any], asset_root: Path) -> str:
    src = html.escape(icon_src_to_html(text(icon["src"]), asset_root), quote=True)
    alt = html_text(icon["alt"])
    role = html_text(icon.get("role") or icon["alt"])
    return (
        '<figure class="icon-item">'
        f'<img src="{src}" alt="{alt}" loading="eager" decoding="async">'
        f'<figcaption>{role}</figcaption>'
        "</figure>"
    )


def render_card(item: dict[str, Any], asset_root: Path) -> str:
    item_id = text(item["id"])
    item_type = text(item["type"])
    label = text(item["label"])
    keywords_raw = item.get("keywords", [])
    if isinstance(keywords_raw, list):
        keywords = " ".join(text(value) for value in keywords_raw)
    else:
        keywords = text(keywords_raw)
    search_text = " ".join(
        (
            item_id,
            item_type,
            label,
            text(item["visualization"]),
            text(item["emphasis"]),
            keywords,
        )
    ).lower()
    icons = "".join(render_icon(icon, asset_root) for icon in item["icons"])
    return f"""
<article class="association-card" data-id="{html_text(item_id)}"
  data-type="{html_text(item_type)}" data-search="{html.escape(search_text, quote=True)}">
  <header class="card-header">
    <span class="association-id">{html_text(item_id)}</span>
    <span class="association-type">{html_text(item_type)}</span>
  </header>
  <h2>{html_text(label)}</h2>
  <div class="icon-stage" aria-label="{html_text(label)}的图标预览">{icons}</div>
  <dl class="meaning">
    <div><dt>怎样画</dt><dd>{html_text(item['visualization'])}</dd></div>
    <div><dt>突出什么</dt><dd>{html_text(item['emphasis'])}</dd></div>
  </dl>
  <button class="select-card" type="button" aria-pressed="false">选择 {html_text(item_id)}</button>
</article>"""


def render_html(
    data: dict[str, Any], items: list[dict[str, Any]], asset_root: Path, palette: dict[str, str]
) -> str:
    title = html_text(data["title"])
    core_message = html_text(data["core_message"])
    types = sorted({text(item["type"]) for item in items})
    type_buttons = "".join(
        f'<button class="filter-chip" type="button" data-filter="{html_text(item_type)}">'
        f"{html_text(item_type)}</button>"
        for item_type in types
    )
    cards = "".join(render_card(item, asset_root) for item in items)
    css_vars = "\n".join(
        f"    --concept-color-{key}: {value};" for key, value in palette.items()
    )
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="color-scheme" content="light">
  <title>{title}</title>
  <style>
  :root {{
{css_vars}
    --page: var(--concept-color-warm-fill);
    --card: var(--concept-color-canvas);
    --ink: var(--concept-color-ink);
    --muted: var(--concept-color-deep-structure);
    --focus: var(--concept-color-positive-flow);
  }}
  * {{ box-sizing: border-box; }}
  body {{
    margin: 0;
    color: var(--ink);
    background: var(--page);
    font-family: ui-rounded, "PingFang SC", "Microsoft YaHei", system-ui, sans-serif;
    line-height: 1.55;
  }}
  button, input {{ font: inherit; }}
  .page {{ width: min(1480px, calc(100% - 32px)); margin: 0 auto; padding: 34px 0 64px; }}
  .hero {{ max-width: 960px; margin-bottom: 22px; }}
  .eyebrow {{ color: var(--muted); font-weight: 800; letter-spacing: .08em; text-transform: uppercase; }}
  h1 {{ margin: 6px 0 10px; font-size: clamp(1.8rem, 4vw, 3.3rem); line-height: 1.12; }}
  .core-message {{ margin: 0; font-size: 1.1rem; max-width: 70ch; }}
  .toolbar {{
    position: sticky; top: 0; z-index: 10; display: grid; gap: 12px;
    margin: 24px 0; padding: 14px; border: 2px solid var(--ink); border-radius: 18px;
    background: color-mix(in srgb, var(--card) 94%, transparent); box-shadow: 4px 5px 0 var(--ink);
  }}
  .toolbar-row {{ display: flex; flex-wrap: wrap; gap: 8px; align-items: center; }}
  #search {{
    flex: 1 1 280px; min-height: 44px; padding: 8px 12px; border: 2px solid var(--muted);
    border-radius: 12px; color: var(--ink); background: white;
  }}
  button {{ cursor: pointer; }}
  .filter-chip, .copy-button {{
    min-height: 40px; padding: 7px 12px; border: 2px solid var(--muted); border-radius: 999px;
    color: var(--ink); background: var(--card); font-weight: 750;
  }}
  .filter-chip[aria-pressed="true"], .copy-button {{ color: var(--card); background: var(--muted); }}
  .selection-status {{ font-weight: 800; }}
  .asset-warning {{ color: var(--concept-color-conflict); font-weight: 800; }}
  .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(290px, 1fr)); gap: 20px; align-items: stretch; }}
  .association-card {{
    display: flex; flex-direction: column; min-height: 100%; padding: 18px;
    border: 2px solid var(--ink); border-radius: 22px; background: var(--card);
    box-shadow: 5px 6px 0 color-mix(in srgb, var(--deep-shadow, var(--ink)) 88%, transparent);
  }}
  .association-card.is-selected {{ outline: 5px solid var(--focus); outline-offset: 3px; }}
  .association-card.asset-error {{ border-color: var(--concept-color-conflict); }}
  .association-card[hidden] {{ display: none; }}
  .card-header {{ display: flex; justify-content: space-between; gap: 10px; align-items: center; }}
  .association-id {{ font-size: 1.05rem; font-weight: 900; color: var(--muted); }}
  .association-type {{ padding: 3px 9px; border-radius: 999px; background: var(--concept-color-cool-fill); font-size: .78rem; font-weight: 800; }}
  .association-card h2 {{ margin: 9px 0 8px; font-size: 1.3rem; line-height: 1.25; }}
  .icon-stage {{
    display: flex; justify-content: center; align-items: center; gap: 12px; min-height: 166px;
    margin: 6px 0 14px; padding: 10px; border-radius: 18px;
    background: white; border: 1px solid color-mix(in srgb, var(--muted) 40%, white);
  }}
  .icon-item {{ flex: 1 1 0; min-width: 0; max-width: 150px; margin: 0; text-align: center; }}
  .icon-item img {{ display: block; width: 100%; height: 128px; object-fit: contain; margin: 0 auto; }}
  .icon-item figcaption {{ margin-top: 5px; color: var(--muted); font-size: .76rem; font-weight: 750; }}
  .meaning {{ display: grid; gap: 10px; margin: 0 0 12px; }}
  .meaning div {{ display: grid; gap: 2px; }}
  dt {{ color: var(--muted); font-size: .78rem; font-weight: 900; }}
  dd {{ margin: 0; }}
  .select-card {{
    width: 100%; min-height: 44px; margin-top: 14px; border: 2px solid var(--muted);
    border-radius: 12px; color: var(--card); background: var(--muted); font-weight: 900;
  }}
  .select-card[aria-pressed="true"] {{ color: var(--ink); background: var(--concept-color-cool-fill); }}
  .selection-next-step {{ margin: 10px 4px 0; color: var(--muted); font-size: .82rem; font-weight: 700; }}
  .empty {{ padding: 32px; text-align: center; font-weight: 800; }}
  @media (max-width: 620px) {{
    .page {{ width: min(100% - 20px, 1480px); padding-top: 20px; }}
    .toolbar {{ position: static; }}
    .grid {{ grid-template-columns: 1fr; }}
  }}
  @media print {{
    .toolbar, .select-card {{ display: none; }}
    .page {{ width: 100%; padding: 0; }}
    .grid {{ grid-template-columns: repeat(2, 1fr); gap: 10px; }}
    .association-card {{ break-inside: avoid; box-shadow: none; }}
  }}
  </style>
</head>
<body>
<main class="page">
  <header class="hero">
    <div class="eyebrow">Step 4 visual references · {len(items)} candidates</div>
    <h1>{title}</h1>
    <p class="core-message"><strong>本轮核心信息：</strong>{core_message}</p>
  </header>
  <section class="toolbar" aria-label="联想池筛选与选择">
    <div class="toolbar-row">
      <input id="search" type="search" placeholder="搜索编号、联想、动作或强调…" aria-label="搜索联想">
      <button class="filter-chip" type="button" data-filter="all" aria-pressed="true">全部</button>
      {type_buttons}
    </div>
    <div class="toolbar-row">
      <span class="selection-status" aria-live="polite">已选 0/3：尚未选择</span>
      <button class="copy-button" type="button">复制编号，继续落地</button>
      <span class="asset-warning" role="status" aria-live="polite"></span>
    </div>
    <p class="selection-next-step">把入选编号贴回对话并授权“初始化并嵌入”后：本地原生 Excalidraw 组件会直接复用；其他入选图像参考会先描摹为 Vault 内原生 Excalidraw icon，不复制或嵌入源图；随后只把这些 icon 松散放入知识卡初始视图，由你亲自组合。</p>
  </section>
  <section class="grid" aria-label="视觉联想候选">{cards}</section>
  <p class="empty" hidden>没有符合当前筛选条件的候选。</p>
</main>
<script>
(() => {{
  const cards = [...document.querySelectorAll('.association-card')];
  const chips = [...document.querySelectorAll('.filter-chip')];
  const search = document.querySelector('#search');
  const status = document.querySelector('.selection-status');
  const copyButton = document.querySelector('.copy-button');
  const assetWarning = document.querySelector('.asset-warning');
  const empty = document.querySelector('.empty');
  const storageKey = `association-pool:${{document.title}}`;
  let activeType = 'all';
  let selected = [];
  try {{ selected = JSON.parse(localStorage.getItem(storageKey) || '[]'); }} catch (_) {{ selected = []; }}
  selected = selected.filter(id => cards.some(card => card.dataset.id === id)).slice(0, 3);

  function updateSelection() {{
    cards.forEach(card => {{
      const on = selected.includes(card.dataset.id);
      card.classList.toggle('is-selected', on);
      const button = card.querySelector('.select-card');
      button.setAttribute('aria-pressed', String(on));
      button.textContent = on ? `取消 ${{card.dataset.id}}` : `选择 ${{card.dataset.id}}`;
    }});
    status.textContent = `已选 ${{selected.length}}/3：${{selected.join('、') || '尚未选择'}}`;
    localStorage.setItem(storageKey, JSON.stringify(selected));
  }}

  function applyFilters() {{
    const query = search.value.trim().toLowerCase();
    let visible = 0;
    cards.forEach(card => {{
      const typeMatches = activeType === 'all' || card.dataset.type === activeType;
      const searchMatches = !query || card.dataset.search.includes(query);
      card.hidden = !(typeMatches && searchMatches);
      if (!card.hidden) visible += 1;
    }});
    empty.hidden = visible !== 0;
  }}

  cards.forEach(card => {{
    card.querySelector('.select-card').addEventListener('click', () => {{
      const id = card.dataset.id;
      if (selected.includes(id)) selected = selected.filter(value => value !== id);
      else if (selected.length < 3) selected.push(id);
      else {{ status.textContent = '最多选择 3 个；请先取消一个。'; return; }}
      updateSelection();
    }});
  }});

  chips.forEach(chip => chip.addEventListener('click', () => {{
    activeType = chip.dataset.filter;
    chips.forEach(item => item.setAttribute('aria-pressed', String(item === chip)));
    applyFilters();
  }}));
  search.addEventListener('input', applyFilters);

  copyButton.addEventListener('click', async () => {{
    const value = selected.join(', ');
    if (!value) {{ status.textContent = '请先选择 1–3 个联想。'; return; }}
    try {{
      await navigator.clipboard.writeText(value);
    }} catch (_) {{
      const helper = document.createElement('textarea');
      helper.value = value; document.body.appendChild(helper); helper.select();
      document.execCommand('copy'); helper.remove();
    }}
    copyButton.textContent = '已复制';
    setTimeout(() => copyButton.textContent = '复制编号，继续落地', 1200);
  }});

  let failedAssets = 0;
  document.querySelectorAll('.icon-item img').forEach(image => image.addEventListener('error', () => {{
    failedAssets += 1;
    image.closest('.association-card').classList.add('asset-error');
    assetWarning.textContent = `${{failedAssets}} 个素材加载失败，请替换后再选择。`;
  }}));

  updateSelection();
  applyFilters();
}})();
</script>
</body>
</html>
"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="把第 4 步视觉参考 JSON 渲染为供人类选择入选 icon 的独立 HTML。"
    )
    parser.add_argument("input_json", type=Path)
    parser.add_argument("output_html", type=Path)
    parser.add_argument(
        "--asset-root",
        type=Path,
        default=Path.cwd(),
        help="JSON 中相对 icon 路径的根目录；默认当前工作目录。",
    )
    parser.add_argument(
        "--palette-css",
        type=Path,
        default=Path("Knowledge/Assets/Styles/concept-visualization-palette.css"),
        help="项目语义色板 CSS；相对路径按 asset-root 解析。",
    )
    parser.add_argument("--min-items", type=int, default=1)
    parser.add_argument("--max-items", type=int, default=24)
    parser.add_argument("--open", action="store_true", dest="open_preview")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    asset_root = args.asset_root.expanduser().resolve()
    palette_path = args.palette_css.expanduser()
    if not palette_path.is_absolute():
        palette_path = asset_root / palette_path
    try:
        if args.min_items < 1 or args.max_items < args.min_items:
            raise PoolError("候选数量范围无效。")
        data = read_json(args.input_json.expanduser().resolve())
        items = validate_pool(data, args.min_items, args.max_items)
        palette = read_palette(palette_path.resolve())
        output = args.output_html.expanduser().resolve()
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(render_html(data, items, asset_root, palette), encoding="utf-8")
    except PoolError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    print(output)
    if args.open_preview:
        if not webbrowser.open(output.as_uri()):
            print("warning: 无法自动打开浏览器，请手动打开上面的 HTML。", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
