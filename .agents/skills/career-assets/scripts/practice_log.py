#!/usr/bin/env python3
"""Snapshot, append, and resume private oral-practice records (stdlib only)."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
from datetime import datetime
from pathlib import Path
from typing import Any

SAFE_ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*\Z")
DIGEST = re.compile(r"[0-9a-f]{64}\Z")
CUES = ("none", "keywords", "full")
NEXT_SKILLS = ("interview-package", "career-evidence", "career-positioning")


def nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def positive(value: Any) -> bool:
    return (type(value) is int and value > 0) or (type(value) is float and math.isfinite(value) and value > 0)


def contained_file(root: Path, value: Any) -> Path:
    if not nonempty(value) or Path(value).is_absolute():
        raise ValueError("path must be relative")
    path = (root / value).resolve()
    if not path.is_relative_to(root.resolve()) or not path.is_file():
        raise ValueError(f"path must resolve to a file inside {root}: {value}")
    return path


def read_object(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise ValueError(f"cannot read JSON object {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object: {path}")
    return value


def digest_claims(claim_ids: list[str], claims: dict[str, dict[str, Any]]) -> str:
    payload = [claims[claim_id] for claim_id in sorted(claim_ids)]
    raw = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def snapshot(state_dir: Path, repo_root: Path, manifest_name: str, claims: dict[str, dict[str, Any]]) -> dict[str, Any]:
    manifest_path = contained_file(state_dir, manifest_name)
    manifest = read_object(manifest_path)
    if manifest.get("status") != "current" or manifest.get("artifact_type") != "interview_script":
        raise ValueError("practice source requires a current interview_script manifest")
    artifact = manifest.get("artifact")
    artifact_path = contained_file(repo_root, artifact)
    if artifact_path.suffix != ".md":
        raise ValueError("practice source must be a Markdown file")
    claim_ids = manifest.get("claim_ids")
    if not isinstance(claim_ids, list) or not claim_ids or any(not nonempty(item) for item in claim_ids):
        raise ValueError("source manifest needs non-empty claim_ids")
    if len(set(claim_ids)) != len(claim_ids):
        raise ValueError("source manifest has duplicate claim_ids")
    for claim_id in claim_ids:
        if claim_id not in claims or claims[claim_id].get("status") != "confirmed":
            raise ValueError(f"source uses unknown or non-confirmed claim: {claim_id}")
    return {
        "manifest": manifest_path.relative_to(state_dir).as_posix(),
        "artifact": artifact,
        "sha256": hashlib.sha256(artifact_path.read_bytes()).hexdigest(),
        "claim_ids": sorted(claim_ids),
        "claims_sha256": digest_claims(claim_ids, claims),
    }


def validate_session(record: Any, state_dir: Path, claims: dict[str, dict[str, Any]], label: str, errors: list[str]) -> None:
    def check(condition: bool, message: str) -> None:
        if not condition:
            errors.append(f"{label}: {message}")

    if not isinstance(record, dict):
        check(False, "session must be an object")
        return
    check(type(record.get("schema_version")) is int and record["schema_version"] == 1, "invalid schema_version")
    for key in ("id", "project_id"):
        check(isinstance(record.get(key), str) and bool(SAFE_ID.fullmatch(record[key])), f"invalid {key}")
    timestamp = record.get("recorded_at")
    try:
        parsed = datetime.fromisoformat(timestamp) if isinstance(timestamp, str) else None
        check(parsed is not None and parsed.utcoffset() is not None, "recorded_at needs an ISO timestamp with timezone")
    except ValueError:
        check(False, "invalid recorded_at")
    opportunity_id = record.get("opportunity_id")
    check("opportunity_id" in record, "missing opportunity_id (use null for general practice)")
    if opportunity_id is not None:
        if not isinstance(opportunity_id, str) or not SAFE_ID.fullmatch(opportunity_id):
            check(False, "invalid opportunity_id")
        else:
            path = state_dir / "opportunities" / opportunity_id / "opportunity.json"
            check(path.resolve().is_relative_to(state_dir.resolve()) and path.is_file(), "unknown opportunity_id")
    check(record.get("status") in ("completed", "interrupted"), "invalid status")
    previous = record.get("resumes_session_id")
    check("resumes_session_id" in record and (previous is None or nonempty(previous)), "invalid resumes_session_id")

    source = record.get("source")
    if not isinstance(source, dict):
        check(False, "source must be an object")
    else:
        for key in ("manifest", "artifact"):
            value = source.get(key)
            root = state_dir if key == "manifest" else None
            valid_path = isinstance(value, str) and bool(value.strip()) and not Path(value).is_absolute() and ".." not in Path(value).parts
            check(bool(valid_path), f"invalid source.{key}")
            if valid_path and root is not None and isinstance(value, str):
                check((root / value).resolve().is_relative_to(root.resolve()), f"source.{key} escapes state directory")
        for key in ("sha256", "claims_sha256"):
            check(isinstance(source.get(key), str) and bool(DIGEST.fullmatch(source[key])), f"invalid source.{key}")
        claim_ids = source.get("claim_ids")
        if not isinstance(claim_ids, list) or not claim_ids or any(not nonempty(item) for item in claim_ids):
            check(False, "source.claim_ids must be a non-empty string array")
        else:
            check(len(set(claim_ids)) == len(claim_ids), "duplicate source.claim_ids")
            for claim_id in claim_ids:
                check(claim_id in claims, f"source references unknown claim: {claim_id}")

    attempts = record.get("attempts")
    attempt_ids: set[str] = set()
    if not isinstance(attempts, list):
        check(False, "attempts must be an array")
        attempts = []
    if record.get("status") == "completed":
        check(bool(attempts), "completed session requires an actual attempt")
    for attempt in attempts:
        if not isinstance(attempt, dict):
            check(False, "attempt must be an object")
            continue
        attempt_id = attempt.get("id")
        check(nonempty(attempt_id), "attempt needs id")
        if isinstance(attempt_id, str):
            check(attempt_id not in attempt_ids, "duplicate attempt id")
        check(attempt.get("exercise") in ("overview", "follow_up", "retry", "retest"), "invalid attempt exercise")
        check(nonempty(attempt.get("question")), "attempt needs question")
        check(positive(attempt.get("target_seconds")), "attempt target_seconds must be positive")
        check(attempt.get("cue_level") in CUES, "invalid attempt cue_level")
        input_kind = attempt.get("input_kind")
        check(input_kind in ("text", "transcript", "self_report", "audio"), "invalid input_kind")
        check("response" in attempt, "attempt needs response (nullable for audio)")
        check("audio_ref" in attempt and (attempt.get("audio_ref") is None or nonempty(attempt.get("audio_ref"))), "invalid audio_ref")
        if input_kind == "audio":
            check(nonempty(attempt.get("audio_ref")), "audio attempt needs audio_ref")
            check(attempt.get("response") is None or nonempty(attempt.get("response")), "invalid audio response")
        else:
            check(nonempty(attempt.get("response")), "text/transcript/self_report attempt needs original response")
        basis = attempt.get("duration_basis")
        duration = attempt.get("duration_seconds")
        check("duration_seconds" in attempt, "missing duration_seconds (use null when unknown)")
        check(basis in ("unknown", "user_timer", "media_metadata"), "invalid duration_basis")
        check(duration is None if basis == "unknown" else positive(duration), "duration must match its measurement basis")
        if basis == "media_metadata":
            check(nonempty(attempt.get("audio_ref")), "media_metadata duration needs audio_ref")
        retry_of = attempt.get("retry_of")
        check("retry_of" in attempt, "missing retry_of (use null when not retrying)")
        if attempt.get("exercise") == "retry":
            check(isinstance(retry_of, str) and retry_of in attempt_ids, "retry_of must reference an earlier attempt")
        else:
            check(retry_of is None, "only retry exercises may set retry_of")
        if isinstance(attempt_id, str):
            attempt_ids.add(attempt_id)

    observations = record.get("observations")
    if not isinstance(observations, list):
        check(False, "observations must be an array")
        observations = []
    if record.get("status") == "completed":
        check(bool(observations), "completed session needs an observation")
        check(nonempty(record.get("adjustment")), "completed session needs one adjustment")
    else:
        check("adjustment" in record and (record.get("adjustment") is None or nonempty(record.get("adjustment"))), "invalid adjustment")
    for observation in observations:
        if not isinstance(observation, dict):
            check(False, "observation must be an object")
            continue
        check(isinstance(observation.get("attempt_id"), str) and observation["attempt_id"] in attempt_ids, "observation references unknown attempt")
        check(observation.get("observer") in ("user", "ai"), "invalid observer")
        check(observation.get("dimension") in ("structure", "mechanism", "fact_consistency", "delivery"), "invalid observation dimension")
        for key in ("evidence", "interpretation"):
            check(nonempty(observation.get(key)), f"observation needs {key}")

    next_step = record.get("next_step")
    if not isinstance(next_step, dict):
        check(False, "next_step must be one object, not a task list")
    else:
        check(nonempty(next_step.get("task")), "next_step needs task")
        check(next_step.get("cue_level") in CUES, "invalid next_step cue_level")
        check(next_step.get("next_skill") in NEXT_SKILLS, "invalid next_step next_skill")
        target = next_step.get("target_seconds")
        check("target_seconds" in next_step and (positive(target) or (target is None and next_step.get("next_skill") != "interview-package")), "next_step needs target_seconds for oral practice")


def source_changes(source: dict[str, Any], state_dir: Path, repo_root: Path, claims: dict[str, dict[str, Any]]) -> list[str]:
    try:
        current = snapshot(state_dir, repo_root, source["manifest"], claims)
    except (OSError, ValueError, KeyError) as exc:
        return [f"source unavailable or no longer current: {exc}"]
    return [f"source.{key} changed" for key in current if current[key] != source.get(key)]


def load_sessions(state_dir: Path, repo_root: Path, claims: dict[str, dict[str, Any]], errors: list[str], warnings: list[str]) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    seen: dict[str, dict[str, Any]] = {}
    for path in sorted((state_dir / "practice").glob("*/sessions.jsonl")):
        if not path.resolve().is_relative_to(state_dir.resolve()):
            errors.append(f"practice log escapes state directory: {path}")
            continue
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except (OSError, UnicodeError) as exc:
            errors.append(f"cannot read practice log {path}: {exc}")
            continue
        for line_number, line in enumerate(lines, 1):
            if not line.strip():
                continue
            label = f"{path}:{line_number}"
            try:
                record = json.loads(line)
            except json.JSONDecodeError as exc:
                errors.append(f"invalid practice JSONL: {label}: {exc}")
                continue
            count = len(errors)
            validate_session(record, state_dir, claims, label, errors)
            if len(errors) != count:
                continue
            if record["project_id"] != path.parent.name:
                errors.append(f"{label}: project_id must match directory name")
            validate_resume(record, seen, label, errors)
            seen[record["id"]] = record
            records.append(record)
            warnings.extend(f"{label}: {change}; historical record retained" for change in source_changes(record["source"], state_dir, repo_root, claims))
    return records


def validate_resume(record: dict[str, Any], seen: dict[str, dict[str, Any]], label: str, errors: list[str]) -> None:
    if record["id"] in seen:
        errors.append(f"{label}: duplicate session id")
    previous_id = record["resumes_session_id"]
    if previous_id is not None:
        previous = seen.get(previous_id)
        if previous is None or any(previous[key] != record[key] for key in ("project_id", "opportunity_id")):
            errors.append(f"{label}: resumes_session_id must reference an earlier session in the same project and opportunity context")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("snapshot", "record", "status"))
    parser.add_argument("--state-dir", type=Path, required=True)
    parser.add_argument("--repo-root", type=Path, required=True)
    parser.add_argument("--manifest", help="State-relative manifest path, for snapshot")
    parser.add_argument("--input", type=Path, help="Authorized session JSON, for record")
    parser.add_argument("--project-id", help="Project to resume")
    parser.add_argument("--opportunity-id", help="Existing opportunity; omitted means general practice only")
    args = parser.parse_args()
    state_dir = args.state_dir.expanduser().resolve()
    repo_root = args.repo_root.expanduser().resolve()
    errors: list[str] = []
    warnings: list[str] = []
    try:
        raw_claims = read_object(state_dir / "claims.json")["claims"]
        claims = {claim["id"]: claim for claim in raw_claims}
        if args.command == "snapshot":
            if not args.manifest:
                parser.error("snapshot requires --manifest")
            output = snapshot(state_dir, repo_root, args.manifest, claims)
        else:
            records = load_sessions(state_dir, repo_root, claims, errors, warnings)
            if errors:
                raise ValueError("\n".join(errors))
            if args.command == "record":
                if args.input is None:
                    parser.error("record requires --input")
                record = read_object(args.input)
                validate_session(record, state_dir, claims, str(args.input), errors)
                if not errors:
                    validate_resume(record, {item["id"]: item for item in records}, str(args.input), errors)
                if errors:
                    raise ValueError("\n".join(errors))
                warnings.extend(source_changes(record["source"], state_dir, repo_root, claims))
                path = state_dir / "practice" / record["project_id"] / "sessions.jsonl"
                if not path.resolve().is_relative_to(state_dir):
                    raise ValueError("practice log escapes state directory")
                # A malformed or unterminated existing line must never be merged with the next record.
                existing = path.read_bytes() if path.exists() else b""
                if existing and not existing.endswith(b"\n"):
                    raise ValueError("existing practice log needs a final newline; no data changed")
                line = json.dumps(record, ensure_ascii=False, allow_nan=False) + "\n"
                path.parent.mkdir(parents=True, exist_ok=True)
                with path.open("a", encoding="utf-8") as stream:
                    stream.write(line)
                output = {"recorded": record["id"], "path": str(path), "warnings": warnings}
            else:
                matches = [item for item in records if item["opportunity_id"] == args.opportunity_id and (args.project_id is None or item["project_id"] == args.project_id)]
                projects = sorted({item["project_id"] for item in matches})
                if len(projects) > 1:
                    output = {"needs_project_selection": True, "projects": projects}
                elif not matches:
                    output = {"last_session": None, "recommended_next_skill": "interview-package", "needs_rebaseline": False}
                else:
                    latest = matches[-1]
                    changes = source_changes(latest["source"], state_dir, repo_root, claims)
                    output = {
                        "last_session": latest,
                        "needs_rebaseline": bool(changes),
                        "source_changes": changes,
                        "recommended_next_skill": "interview-package" if changes else latest["next_step"]["next_skill"],
                        "next_step": {"task": "先核对底稿与相关 claims 的变化，再确认本轮复测任务。", "target_seconds": None, "cue_level": "none", "next_skill": "interview-package"} if changes else latest["next_step"],
                    }
        print(json.dumps(output, ensure_ascii=False, indent=2, allow_nan=False))
        return 0
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f"ERROR: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
