#!/usr/bin/env python3
"""Prepare monochrome SVGs for palette-driven reuse and create colored variants.

The source SVG keeps its geometry and attribution metadata. Color is exposed through
CSS custom property ``--icon-color`` with a black fallback. For an imported card,
create a temporary variant instead of changing the reusable source's chosen color.
Variant colors may be supplied as a HEX value or resolved from the project's canonical
CSS custom properties.
"""

from __future__ import annotations

import argparse
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Iterable

COLOR_VAR = "--icon-color"
FALLBACK = "#000000"
SVG_TAG_RE = re.compile(r"<svg\b[^>]*>", re.IGNORECASE | re.DOTALL)
STYLE_RE = re.compile(r'\bstyle=(?P<quote>["\'])(?P<value>.*?)(?P=quote)', re.IGNORECASE | re.DOTALL)
BLACK_PAINT_RE = re.compile(
    r'(?P<attr>\b(?:fill|stroke))=(?P<quote>["\'])(?:#000000|#000|black)(?P=quote)',
    re.IGNORECASE,
)
HEX_RE = re.compile(r"^#[0-9A-Fa-f]{6}$")
CSS_DECL_RE = re.compile(r"^\s*(--[A-Za-z0-9_-]+)\s*:\s*([^;]+);", re.MULTILINE)
CSS_VAR_REF_RE = re.compile(r"^var\(\s*(--[A-Za-z0-9_-]+)(?:\s*,\s*[^)]+)?\s*\)$")
DEFAULT_PALETTE_CSS = (
    Path(__file__).resolve().parents[4]
    / "content/Knowledge/Assets/Styles/concept-visualization-palette.css"
)


def _append_root_attribute(tag: str, attribute: str) -> str:
    closing = "/>" if tag.rstrip().endswith("/>") else ">"
    body = tag.rstrip()[: -len(closing)].rstrip()
    return f"{body} {attribute}{closing}"


def _set_root_style(tag: str, declaration: str) -> str:
    match = STYLE_RE.search(tag)
    declaration = declaration.strip().rstrip(";") + ";"
    if not match:
        return _append_root_attribute(tag, f'style="{declaration}"')

    value = match.group("value").strip()
    if value and not value.endswith(";"):
        value += ";"
    value = f"{value} {declaration}".strip()
    quote = match.group("quote")
    return tag[: match.start()] + f"style={quote}{value}{quote}" + tag[match.end() :]


def prepare_text(text: str) -> tuple[str, bool]:
    """Return SVG text with a variable color hook and whether it changed."""
    original = text
    text = BLACK_PAINT_RE.sub(lambda m: f'{m.group("attr")}={m.group("quote")}currentColor{m.group("quote")}', text)

    match = SVG_TAG_RE.search(text)
    if not match:
        raise ValueError("missing <svg> root element")
    tag = match.group(0)

    if "data-color-variable=" not in tag:
        tag = _append_root_attribute(tag, f'data-color-variable="{COLOR_VAR}"')

    if f"var({COLOR_VAR}" not in tag:
        tag = _set_root_style(tag, f"color: var({COLOR_VAR}, {FALLBACK})")

    root_has_fill = re.search(r"\bfill\s*=", tag, re.IGNORECASE)
    if not root_has_fill:
        tag = _append_root_attribute(tag, 'fill="currentColor"')
    else:
        tag = BLACK_PAINT_RE.sub(
            lambda m: f'{m.group("attr")}={m.group("quote")}currentColor{m.group("quote")}',
            tag,
        )

    text = text[: match.start()] + tag + text[match.end() :]
    ET.fromstring(text)
    return text, text != original


def set_variant_color(text: str, color: str) -> str:
    if not HEX_RE.fullmatch(color):
        raise ValueError(f"invalid color {color!r}; expected #RRGGBB")
    text, _ = prepare_text(text)
    match = SVG_TAG_RE.search(text)
    assert match
    tag = match.group(0)
    style_match = STYLE_RE.search(tag)
    assert style_match
    style = style_match.group("value")
    declaration_re = re.compile(rf"{re.escape(COLOR_VAR)}\s*:\s*#[0-9A-Fa-f]{{6}}\s*;?")
    if declaration_re.search(style):
        style = declaration_re.sub(f"{COLOR_VAR}: {color.upper()};", style)
    else:
        if style.strip() and not style.rstrip().endswith(";"):
            style += ";"
        style = f"{style} {COLOR_VAR}: {color.upper()};".strip()
    quote = style_match.group("quote")
    tag = tag[: style_match.start()] + f"style={quote}{style}{quote}" + tag[style_match.end() :]
    result = text[: match.start()] + tag + text[match.end() :]
    ET.fromstring(result)
    return result


def expand_paths(values: Iterable[str]) -> list[Path]:
    paths: list[Path] = []
    for value in values:
        path = Path(value)
        if path.is_dir():
            paths.extend(sorted(path.glob("*.svg")))
        elif path.suffix.lower() == ".svg":
            paths.append(path)
    return list(dict.fromkeys(paths))


def cmd_prepare(args: argparse.Namespace) -> int:
    paths = expand_paths(args.paths)
    if not paths:
        raise SystemExit("no SVG files found")
    changed = 0
    for path in paths:
        text = path.read_text(encoding="utf-8")
        prepared, did_change = prepare_text(text)
        if did_change:
            changed += 1
            if args.write:
                path.write_text(prepared, encoding="utf-8")
        print(f"{'updated' if did_change else 'ready  '} {path}")
    if not args.write and changed:
        print(f"dry run: {changed} file(s) would change; pass --write to update", file=sys.stderr)
    return 0


def load_css_properties(path: Path) -> dict[str, str]:
    """Load custom-property declarations from a simple project palette file."""
    text = path.read_text(encoding="utf-8")
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.DOTALL)
    properties = {name: value.strip() for name, value in CSS_DECL_RE.findall(text)}
    if not properties:
        raise ValueError(f"no CSS custom properties found in {path}")
    return properties


def resolve_css_color(path: Path, variable: str) -> str:
    """Resolve a HEX color through direct values or var(--name) aliases."""
    if not variable.startswith("--"):
        raise ValueError(f"invalid CSS variable {variable!r}; expected a name beginning with --")
    properties = load_css_properties(path)
    current = variable
    seen: set[str] = set()
    while True:
        if current in seen:
            raise ValueError(f"circular CSS variable reference involving {current}")
        seen.add(current)
        value = properties.get(current)
        if value is None:
            raise ValueError(f"CSS variable {current!r} not found in {path}")
        if HEX_RE.fullmatch(value):
            return value.upper()
        reference = CSS_VAR_REF_RE.fullmatch(value)
        if not reference:
            raise ValueError(f"CSS variable {current!r} does not resolve to #RRGGBB: {value!r}")
        current = reference.group(1)


def cmd_variant(args: argparse.Namespace) -> int:
    source = Path(args.source)
    output = Path(args.output)
    color = args.color
    if args.color_var:
        color = resolve_css_color(Path(args.palette_css), args.color_var)
    assert color
    output.parent.mkdir(parents=True, exist_ok=True)
    result = set_variant_color(source.read_text(encoding="utf-8"), color)
    output.write_text(result, encoding="utf-8")
    print(output)
    return 0


def cmd_check(args: argparse.Namespace) -> int:
    paths = expand_paths(args.paths)
    if not paths:
        raise SystemExit("no SVG files found")
    failed = 0
    for path in paths:
        try:
            text = path.read_text(encoding="utf-8")
            ET.fromstring(text)
            root = SVG_TAG_RE.search(text)
            assert root and f'data-color-variable="{COLOR_VAR}"' in root.group(0)
            assert f"var({COLOR_VAR}" in root.group(0)
            print(f"ok     {path}")
        except Exception as exc:  # report all files in one pass
            failed += 1
            print(f"failed {path}: {exc}", file=sys.stderr)
    return 1 if failed else 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    prepare = sub.add_parser("prepare", help="add --icon-color support to monochrome SVGs")
    prepare.add_argument("paths", nargs="+", help="SVG files or directories")
    prepare.add_argument("--write", action="store_true", help="modify source files in place")
    prepare.set_defaults(func=cmd_prepare)

    variant = sub.add_parser("variant", help="write a colored copy without changing the source")
    variant.add_argument("source")
    variant.add_argument("output")
    color = variant.add_mutually_exclusive_group(required=True)
    color.add_argument("--color", help="#RRGGBB")
    color.add_argument(
        "--color-var",
        help="CSS custom property; use --color-var=--concept-color-ink syntax",
    )
    variant.add_argument(
        "--palette-css",
        default=str(DEFAULT_PALETTE_CSS),
        help=f"CSS variable file (default: {DEFAULT_PALETTE_CSS})",
    )
    variant.set_defaults(func=cmd_variant)

    check = sub.add_parser("check", help="validate XML and variable-color markers")
    check.add_argument("paths", nargs="+", help="SVG files or directories")
    check.set_defaults(func=cmd_check)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        return args.func(args)
    except (OSError, ValueError, ET.ParseError) as exc:
        parser.error(str(exc))
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
