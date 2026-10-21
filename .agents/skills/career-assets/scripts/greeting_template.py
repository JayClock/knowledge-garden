#!/usr/bin/env python3
"""Render/check the authorized private greeting prompt; never infer career facts."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any

from practice_log import digest_claims, read_object

MANIFEST = "manifests/job-greeting-template.json"
PLACEHOLDER = "{{CANDIDATE_RESUME}}"
CONTACT_CLAIM_IDS = {"career.contact.phone", "career.contact.email"}
CONTACT_LINE = re.compile(
    r"^\s*(?:电话|联系电话|手机(?:号码|号)?|邮箱|电子邮箱|联系邮箱|phone|mobile|e-?mail)\s*[:：]",
    re.IGNORECASE,
)


def resume_for_greeting(text: str) -> str:
    """Omit standalone contact lines without editing the reviewed source resume."""
    return "\n".join(
        line for line in text.splitlines()
        if not CONTACT_LINE.match(re.sub(r"[*_`]", "", line))
    ).strip()


def contained_path(root: Path, value: Any) -> Path:
    if not isinstance(value, str) or not value.strip() or Path(value).is_absolute():
        raise ValueError("path must be relative and non-empty")
    path = (root / value).resolve()
    if not path.is_relative_to(root.resolve()):
        raise ValueError(f"path escapes its root: {value}")
    return path


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build(state_dir: Path, repo_root: Path, config: dict[str, Any]) -> tuple[Path, str, dict[str, Any]]:
    settings = config.get("greeting_template")
    if not isinstance(settings, dict):
        raise ValueError("config.greeting_template must be an object")
    artifact = contained_path(repo_root, settings.get("artifact"))
    if artifact.suffix != ".md" or artifact.is_relative_to(repo_root / "content"):
        raise ValueError("greeting template must be a private Markdown file outside content/")
    source_manifest_path = contained_path(state_dir, settings.get("resume_manifest"))
    manifest_path = contained_path(state_dir, MANIFEST)
    if source_manifest_path == manifest_path:
        raise ValueError("resume_manifest cannot be the greeting template manifest")
    source = read_object(source_manifest_path)
    if source.get("status") != "current" or source.get("artifact_type") != "resume":
        raise ValueError("greeting template requires a current resume manifest")
    resume_path = contained_path(repo_root, source.get("artifact"))
    if source.get("artifact_sha256") != sha256(resume_path):
        raise ValueError("resume artifact_sha256 does not match; review the resume and its manifest first")

    claim_ids = source.get("claim_ids")
    if (
        not isinstance(claim_ids, list)
        or not claim_ids
        or any(not isinstance(item, str) or not item.strip() for item in claim_ids)
        or len(set(claim_ids)) != len(claim_ids)
    ):
        raise ValueError("resume manifest needs unique, non-empty claim_ids")
    claim_doc = read_object(state_dir / "claims.json")
    raw_claims = claim_doc.get("claims")
    if not isinstance(raw_claims, list) or any(not isinstance(item, dict) for item in raw_claims):
        raise ValueError("claims.json needs a claims array of objects")
    claims = {item.get("id"): item for item in raw_claims}
    for claim_id in claim_ids:
        if claim_id not in claims or claims[claim_id].get("status") != "confirmed":
            raise ValueError(f"resume uses unknown or non-confirmed claim: {claim_id}")

    claims_digest = digest_claims(claim_ids, claims)
    if source.get("claims_sha256") != claims_digest:
        raise ValueError("resume claims_sha256 changed; review the resume and its manifest first")

    prompt_path = contained_path(repo_root, settings.get("prompt_template"))
    prompt = prompt_path.read_text(encoding="utf-8")
    if prompt.count(PLACEHOLDER) != 1:
        raise ValueError(f"prompt_template must contain exactly one {PLACEHOLDER}")
    resume = resume_for_greeting(resume_path.read_text(encoding="utf-8"))
    if not resume:
        raise ValueError("resume must not be empty after removing contact lines")
    fence = "`" * max(3, max((len(run) + 1 for run in re.findall(r"`+", resume)), default=0))
    rendered = prompt.replace(PLACEHOLDER, f"{fence}markdown\n{resume}\n{fence}").rstrip() + "\n"
    prompt_claim_ids = [claim_id for claim_id in claim_ids if claim_id not in CONTACT_CLAIM_IDS]

    files = {("state", source_manifest_path), ("repo", resume_path), ("repo", prompt_path)}
    watch_sources = settings.get("watch_sources", [])
    watch_globs = settings.get("watch_globs", [])
    if not isinstance(watch_sources, list) or not isinstance(watch_globs, list):
        raise ValueError("watch_sources and watch_globs must be arrays")
    for value in watch_sources:
        files.add(("repo", contained_path(repo_root, value)))
    for pattern in watch_globs:
        contained_path(repo_root, pattern)
        for path in repo_root.glob(pattern):
            if path.is_file():
                files.add(("repo", contained_path(repo_root, path.relative_to(repo_root).as_posix())))
    sections = source.get("source_sections", [])
    if not isinstance(sections, list) or any(not isinstance(item, dict) for item in sections):
        raise ValueError("resume source_sections must be an array of objects")
    for section in sections:
        files.add(("repo", contained_path(repo_root, section.get("path"))))
    if artifact in {path for _, path in files}:
        raise ValueError("greeting template cannot overwrite a source")
    source_files = [
        {
            "root": kind,
            "path": path.relative_to(state_dir if kind == "state" else repo_root).as_posix(),
            "sha256": sha256(path),
        }
        for kind, path in sorted(files, key=lambda item: (item[0], item[1].as_posix()))
    ]
    return artifact, rendered, {
        "schema_version": 1,
        "artifact": artifact.relative_to(repo_root).as_posix(),
        "artifact_type": "greeting_template",
        "opportunity_id": None,
        "generated_by": "resume-package",
        "claim_ids": sorted(prompt_claim_ids),
        "status": "current",
        "artifact_sha256": hashlib.sha256(rendered.encode("utf-8")).hexdigest(),
        "claims_sha256": digest_claims(prompt_claim_ids, claims),
        "source_files": source_files,
    }


def validate_saved_template(
    state_dir: Path, repo_root: Path, config: dict[str, Any], errors: list[str], warnings: list[str]
) -> None:
    if "greeting_template" not in config:
        return
    try:
        manifest = read_object(contained_path(state_dir, MANIFEST))
        if manifest.get("status") == "stale":
            warnings.append("greeting template is stale; review materials and sync before reuse")
            return
        artifact, rendered, expected = build(state_dir, repo_root, config)
        for key, value in expected.items():
            if manifest.get(key) != value:
                errors.append(f"greeting template {key} changed; review materials and sync")
        if artifact.read_bytes() != rendered.encode("utf-8"):
            errors.append("greeting template content changed or is out of date; review before syncing")
    except (OSError, ValueError, TypeError) as exc:
        errors.append(f"greeting template: {exc}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("check", "sync", "mark-stale"))
    parser.add_argument("--state-dir", type=Path, required=True)
    parser.add_argument("--repo-root", type=Path, required=True)
    parser.add_argument("--reviewed", action="store_true", help="agent has reviewed facts and source changes")
    parser.add_argument("--overwrite-edited", action="store_true", help="explicitly allow replacing reviewed manual edits")
    args = parser.parse_args()
    state_dir = args.state_dir.expanduser().resolve()
    repo_root = args.repo_root.expanduser().resolve()
    try:
        config = read_object(state_dir / "config.json")
        if "greeting_template" not in config:
            if args.command != "check":
                raise ValueError("configure greeting_template only after saving/maintenance is authorized")
            print("Greeting template is not configured; nothing to check")
            return 0
        manifest_path = contained_path(state_dir, MANIFEST)
        if args.command == "mark-stale":
            manifest = read_object(manifest_path)
            manifest["status"] = "stale"
            manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
            print("Greeting template marked stale; content preserved")
            return 0
        if args.command == "check":
            errors: list[str] = []
            warnings: list[str] = []
            validate_saved_template(state_dir, repo_root, config, errors, warnings)
            for issue in errors + warnings:
                print(issue)
            if not errors and not warnings:
                print("Greeting template is current")
            return 1 if errors or warnings else 0
        if not args.reviewed:
            raise ValueError("sync requires --reviewed after semantic review; source hashes do not confirm career facts")
        artifact, rendered, manifest = build(state_dir, repo_root, config)
        if artifact.exists() and not args.overwrite_edited:
            previous = read_object(manifest_path)
            if previous.get("artifact") != manifest["artifact"] or previous.get("artifact_sha256") != sha256(artifact):
                raise ValueError("template was manually edited; preserve/merge changes before using --overwrite-edited")
        if manifest_path.exists():
            previous = read_object(manifest_path)
            if all(previous.get(key) == value for key, value in manifest.items()) and artifact.is_file():
                if artifact.read_bytes() == rendered.encode("utf-8"):
                    print(f"Greeting template already current: {manifest['artifact']}")
                    return 0
        manifest["reviewed_at"] = datetime.now().astimezone().isoformat(timespec="seconds")
        artifact.parent.mkdir(parents=True, exist_ok=True)
        manifest_path.parent.mkdir(parents=True, exist_ok=True)
        artifact.write_text(rendered, encoding="utf-8", newline="\n")
        manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
        print(f"Greeting template synced: {manifest['artifact']}")
        return 0
    except (OSError, ValueError, TypeError) as exc:
        print(f"ERROR: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
