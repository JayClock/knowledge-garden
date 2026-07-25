#!/usr/bin/env python3
"""Prepare, build, validate, and attach translated WebVTT subtitles.

Uses only the Python standard library so it can run anywhere in this project.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from urllib.parse import urlencode

TIMESTAMP_PATTERN = r"(?:(?:\d{2,}):)?\d{2}:\d{2}\.\d{3}"
TIMESTAMP_RE = re.compile(rf"^{TIMESTAMP_PATTERN}$")
TIMING_RE = re.compile(
    rf"^(?P<start>{TIMESTAMP_PATTERN})\s*-->\s*"
    rf"(?P<end>{TIMESTAMP_PATTERN})(?:\s+.*)?$"
)
INLINE_TIMESTAMP_RE = re.compile(rf"<{TIMESTAMP_PATTERN}>")
SOUND_EVENT_RE = re.compile(r"^\[[^\]]+\]$")
SENTENCE_END_RE = re.compile(r'''[.!?][\]"')]*$''')


@dataclass
class Cue:
    start: str
    end: str
    text: str
    identifier: str | None = None

    @property
    def start_seconds(self) -> float:
        return timestamp_to_seconds(self.start)

    @property
    def end_seconds(self) -> float:
        return timestamp_to_seconds(self.end)


def timestamp_to_seconds(value: str) -> float:
    if not TIMESTAMP_RE.fullmatch(value):
        raise ValueError(f"Invalid WebVTT timestamp: {value}")
    parts = value.split(":")
    hours = int(parts[-3]) if len(parts) == 3 else 0
    return hours * 3600 + int(parts[-2]) * 60 + float(parts[-1])


def parse_vtt(path: Path) -> list[Cue]:
    text = path.read_text(encoding="utf-8-sig").replace("\r\n", "\n").replace("\r", "\n")
    blocks = re.split(r"\n\s*\n", text.strip())
    if not blocks or not blocks[0].startswith("WEBVTT"):
        raise ValueError(f"{path}: missing WEBVTT header")

    cues: list[Cue] = []
    for block in blocks[1:]:
        lines = block.splitlines()
        if not lines or lines[0].lstrip().startswith(("NOTE", "STYLE", "REGION")):
            continue
        timing_index = next((i for i, line in enumerate(lines) if "-->" in line), None)
        if timing_index is None:
            raise ValueError(f"{path}: cue block has no timing line: {block[:100]!r}")
        match = TIMING_RE.fullmatch(lines[timing_index].strip())
        if not match:
            raise ValueError(f"{path}: invalid timing line: {lines[timing_index]!r}")
        identifier = "\n".join(lines[:timing_index]).strip() or None
        cue_text = "\n".join(lines[timing_index + 1 :]).strip()
        cues.append(Cue(match.group("start"), match.group("end"), cue_text, identifier))
    if not cues:
        raise ValueError(f"{path}: no cues found")
    return cues


def clean_source_text(text: str) -> str:
    text = " ".join(text.splitlines())
    text = INLINE_TIMESTAMP_RE.sub("", text)
    text = re.sub(r"\s+", " ", text).strip()
    text = re.sub(r"^>>\s*", "", text)
    return text


def group_cues(
    cues: list[Cue],
    *,
    max_duration: float = 7.6,
    max_chars: int = 160,
    max_gap: float = 0.75,
) -> list[dict[str, object]]:
    groups: list[dict[str, object]] = []
    current: list[Cue] = []

    def flush() -> None:
        if not current:
            return
        groups.append(
            {
                "id": len(groups) + 1,
                "start": current[0].start,
                "end": current[-1].end,
                "source": " ".join(clean_source_text(c.text) for c in current).strip(),
            }
        )
        current.clear()

    for original in cues:
        cue = Cue(original.start, original.end, clean_source_text(original.text), original.identifier)
        if SOUND_EVENT_RE.fullmatch(cue.text):
            flush()
            current.append(cue)
            flush()
            continue

        if current and cue.start_seconds - current[-1].end_seconds > max_gap:
            flush()

        if current:
            prospective_text = " ".join([*(c.text for c in current), cue.text])
            prospective_duration = cue.end_seconds - current[0].start_seconds
            if prospective_duration > max_duration or len(prospective_text) > max_chars:
                flush()

        current.append(cue)
        merged = " ".join(c.text for c in current)
        duration = current[-1].end_seconds - current[0].start_seconds
        if SENTENCE_END_RE.search(merged) and (duration >= 3.0 or len(merged) >= 70):
            flush()

    flush()
    return groups


def write_source_tsv(groups: list[dict[str, object]], path: Path) -> None:
    rows = [
        f"{int(group['id']):03d}\t{group['start']}\t{group['end']}\t{group['source']}"
        for group in groups
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(rows) + "\n", encoding="utf-8")


def load_translations(path: Path) -> dict[int, str]:
    translations: dict[int, str] = {}
    for line_number, line in enumerate(path.read_text(encoding="utf-8-sig").splitlines(), 1):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        try:
            raw_id, translated = line.split("\t", 1)
            cue_id = int(raw_id)
        except (ValueError, TypeError) as exc:
            raise ValueError(f"{path}:{line_number}: expected ID<TAB>translation") from exc
        translated = translated.strip()
        if not translated:
            raise ValueError(f"{path}:{line_number}: translation is empty")
        if cue_id in translations:
            raise ValueError(f"{path}:{line_number}: duplicate cue ID {cue_id}")
        translations[cue_id] = translated
    return translations


def write_vtt(groups: list[dict[str, object]], translations: dict[int, str], output: Path) -> None:
    expected = {int(group["id"]) for group in groups}
    supplied = set(translations)
    if missing := sorted(expected - supplied):
        raise ValueError(f"Missing translation IDs: {missing}")
    if extra := sorted(supplied - expected):
        raise ValueError(f"Unexpected translation IDs: {extra}")

    lines = ["WEBVTT", ""]
    for group in groups:
        cue_id = int(group["id"])
        lines.extend(
            [
                str(cue_id),
                f"{group['start']} --> {group['end']}",
                translations[cue_id],
                "",
            ]
        )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines), encoding="utf-8")


def validate(path: Path) -> dict[str, object]:
    raw = path.read_text(encoding="utf-8-sig")
    if "�" in raw:
        raise ValueError(f"{path}: contains Unicode replacement characters")
    cues = parse_vtt(path)
    warnings: list[str] = []
    previous_start = -1.0
    previous_end = -1.0
    for index, cue in enumerate(cues, 1):
        start = cue.start_seconds
        end = cue.end_seconds
        if not cue.text.strip():
            raise ValueError(f"{path}: cue {index} has empty text")
        if start >= end:
            raise ValueError(f"{path}: cue {index} starts at or after its end")
        if start < previous_start:
            raise ValueError(f"{path}: cue {index} is out of chronological order")
        if start < previous_end:
            warnings.append(f"cue {index} overlaps the previous cue")
        previous_start, previous_end = start, end
    return {
        "path": str(path),
        "cues": len(cues),
        "first_start": cues[0].start,
        "last_end": cues[-1].end,
        "warnings": warnings,
    }


def find_frontmatter_end(lines: list[str]) -> int:
    if not lines or lines[0].strip() != "---":
        raise ValueError("Markdown note has no YAML frontmatter")
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            return index
    raise ValueError("Markdown note has unterminated YAML frontmatter")


def attach_track(
    note: Path,
    subtitle: Path,
    *,
    property_name: str,
    language: str,
    label: str,
    link_path: str | None,
    dry_run: bool,
) -> bool:
    if not re.fullmatch(r"[A-Za-z0-9_-]+", property_name):
        raise ValueError(f"Unsafe frontmatter property name: {property_name}")
    original = note.read_text(encoding="utf-8")
    lines = original.splitlines()
    frontmatter_end = find_frontmatter_end(lines)
    target = link_path or subtitle.name
    fragment = urlencode({"lang": language, "label": label})
    wikilink = f"[[{target}#{fragment}]]"
    item_line = "  - " + json.dumps(wikilink, ensure_ascii=False)

    if subtitle.name in "\n".join(lines[1:frontmatter_end]):
        print(f"Track already present in {note}: {subtitle.name}")
        return False

    property_re = re.compile(rf"^{re.escape(property_name)}:\s*(.*)$")
    property_index = next(
        (i for i in range(1, frontmatter_end) if property_re.fullmatch(lines[i])), None
    )

    if property_index is None:
        lines[frontmatter_end:frontmatter_end] = [f"{property_name}:", item_line]
    else:
        match = property_re.fullmatch(lines[property_index])
        assert match is not None
        scalar = match.group(1).strip()
        if scalar:
            lines[property_index : property_index + 1] = [
                f"{property_name}:",
                f"  - {scalar}",
                item_line,
            ]
        else:
            insert_at = property_index + 1
            while insert_at < frontmatter_end and (
                not lines[insert_at].strip() or lines[insert_at].startswith((" ", "\t"))
            ):
                insert_at += 1
            lines.insert(insert_at, item_line)

    updated = "\n".join(lines) + ("\n" if original.endswith("\n") else "")
    if dry_run:
        print(updated)
    else:
        note.write_text(updated, encoding="utf-8")
        print(f"Attached {subtitle.name} under {property_name} in {note}")
    return True


def command_prepare(args: argparse.Namespace) -> None:
    groups = group_cues(
        parse_vtt(args.source),
        max_duration=args.max_duration,
        max_chars=args.max_chars,
        max_gap=args.max_gap,
    )
    args.groups.parent.mkdir(parents=True, exist_ok=True)
    args.groups.write_text(json.dumps(groups, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_source_tsv(groups, args.source_tsv)
    print(json.dumps({"source_cues": len(parse_vtt(args.source)), "groups": len(groups), "groups_file": str(args.groups), "source_tsv": str(args.source_tsv)}, ensure_ascii=False))


def command_build(args: argparse.Namespace) -> None:
    groups = json.loads(args.groups.read_text(encoding="utf-8"))
    write_vtt(groups, load_translations(args.translations), args.output)
    print(json.dumps(validate(args.output), ensure_ascii=False))


def command_validate(args: argparse.Namespace) -> None:
    result = validate(args.vtt)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def command_attach(args: argparse.Namespace) -> None:
    attach_track(
        args.note,
        args.subtitle,
        property_name=args.property,
        language=args.lang,
        label=args.label,
        link_path=args.link_path,
        dry_run=args.dry_run,
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    prepare = subparsers.add_parser("prepare", help="Merge fragmented source cues into translation units")
    prepare.add_argument("source", type=Path)
    prepare.add_argument("--groups", type=Path, required=True)
    prepare.add_argument("--source-tsv", type=Path, required=True)
    prepare.add_argument("--max-duration", type=float, default=7.6)
    prepare.add_argument("--max-chars", type=int, default=160)
    prepare.add_argument("--max-gap", type=float, default=0.75)
    prepare.set_defaults(func=command_prepare)

    build = subparsers.add_parser("build", help="Build translated VTT from groups and an ID/translation TSV")
    build.add_argument("--groups", type=Path, required=True)
    build.add_argument("--translations", type=Path, required=True)
    build.add_argument("--output", type=Path, required=True)
    build.set_defaults(func=command_build)

    validate_parser = subparsers.add_parser("validate", help="Validate WebVTT structure and chronology")
    validate_parser.add_argument("vtt", type=Path)
    validate_parser.set_defaults(func=command_validate)

    attach = subparsers.add_parser("attach", help="Attach a subtitle track to Markdown frontmatter")
    attach.add_argument("note", type=Path)
    attach.add_argument("subtitle", type=Path)
    attach.add_argument("--property", default="subtitles")
    attach.add_argument("--lang", default="zh-Hans")
    attach.add_argument("--label", default="中文（简体）")
    attach.add_argument("--link-path", help="Wikilink path; defaults to subtitle basename")
    attach.add_argument("--dry-run", action="store_true")
    attach.set_defaults(func=command_attach)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        args.func(args)
        return 0
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
