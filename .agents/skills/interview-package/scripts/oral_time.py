#!/usr/bin/env python3
"""Estimate Chinese interview speaking time from Markdown text."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


def extract_section(text: str, heading: str | None) -> str:
    if not heading:
        return text
    pattern = re.compile(rf"^(#+)\s+{re.escape(heading)}\s*$", re.MULTILINE)
    match = pattern.search(text)
    if not match:
        raise ValueError(f"section not found: {heading}")
    level = len(match.group(1))
    tail = text[match.end() :]
    next_heading = re.search(rf"^#{{1,{level}}}\s+", tail, re.MULTILINE)
    return tail[: next_heading.start()] if next_heading else tail


def spoken_characters(markdown: str) -> int:
    text = re.sub(r"\A---\s*\n.*?\n---\s*\n", "", markdown, flags=re.DOTALL)
    text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
    text = re.sub(r"!\[([^]]*)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"\[([^]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"\[\[([^]|]+)\|([^]]+)\]\]", r"\2", text)
    text = re.sub(r"\[\[([^]]+)\]\]", r"\1", text)
    text = re.sub(r"^\s{0,3}#{1,6}\s+.*$", "", text, flags=re.MULTILINE)
    text = re.sub(r"^\s*>\s?", "", text, flags=re.MULTILINE)
    text = re.sub(r"[`*_~|>\-]", "", text)
    return len(re.sub(r"\s+", "", text))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=Path)
    parser.add_argument("--section")
    parser.add_argument("--min-seconds", type=float, default=90)
    parser.add_argument("--max-seconds", type=float, default=120)
    parser.add_argument("--slow-cpm", type=float, default=280)
    parser.add_argument("--fast-cpm", type=float, default=320)
    args = parser.parse_args()

    text = args.file.read_text(encoding="utf-8")
    try:
        text = extract_section(text, args.section)
    except ValueError as exc:
        print(str(exc))
        return 2
    count = spoken_characters(text)
    fastest = count / args.fast_cpm * 60
    slowest = count / args.slow_cpm * 60
    overlaps = slowest >= args.min_seconds and fastest <= args.max_seconds
    result = {
        "file": str(args.file),
        "section": args.section,
        "non_whitespace_characters": count,
        "estimated_seconds": {"fast": round(fastest, 1), "slow": round(slowest, 1)},
        "target_seconds": {"min": args.min_seconds, "max": args.max_seconds},
        "within_target_range": overlaps,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if overlaps else 1


if __name__ == "__main__":
    raise SystemExit(main())
