from __future__ import annotations

import copy
import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
PRACTICE = SKILL_DIR / "scripts" / "practice_log.py"
LINT = SKILL_DIR / "scripts" / "state_lint.py"
INIT = SKILL_DIR / "scripts" / "init_state.py"


class OralPracticeTest(unittest.TestCase):
    def run_script(self, script: Path, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run([sys.executable, str(script), *args], capture_output=True, text=True, check=False)

    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.state = self.root / ".career"
        initialized = self.run_script(INIT, "--root", str(self.root), "--state-dir", str(self.state))
        self.assertEqual(initialized.returncode, 0, initialized.stderr)
        self.claim = {
            "id": "example.scope", "statement": "直接实现协同模块", "kind": "project_scope",
            "project_id": "example", "ownership": "direct", "completion": "implemented", "status": "confirmed",
            "evidence": [{"type": "user_confirmation", "locator": "用户确认"}],
            "metrics": [], "constraints": [], "tags": [],
        }
        self.save(self.state / "claims.json", {"schema_version": 1, "claims": [self.claim]})
        self.artifact = self.root / "project.md"
        self.artifact.write_text("# 项目介绍\n\n协同模块。\n", encoding="utf-8")
        self.manifest = self.state / "manifests" / "interview-example.json"
        self.save(self.manifest, {
            "schema_version": 1, "artifact": "project.md", "artifact_type": "interview_script",
            "generated_by": "interview-package", "claim_ids": [self.claim["id"]], "status": "current",
            "opportunity_id": None,
        })
        self.args = ("--state-dir", str(self.state), "--repo-root", str(self.root))
        self.source = self.get_snapshot()

    def save(self, path: Path, value: object) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    def get_snapshot(self) -> dict:
        result = self.run_script(PRACTICE, "snapshot", *self.args, "--manifest", "manifests/interview-example.json")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        return json.loads(result.stdout)

    def session(self, session_id: str = "practice-001", project_id: str = "example") -> dict:
        return {
            "schema_version": 1, "id": session_id, "recorded_at": "2026-10-04T10:00:00+08:00",
            "project_id": project_id, "opportunity_id": None, "resumes_session_id": None,
            "source": copy.deepcopy(self.source), "status": "completed",
            "attempts": [{
                "id": "a1", "exercise": "overview", "question": "介绍项目", "target_seconds": 120,
                "cue_level": "none", "input_kind": "transcript", "response": "我实现了协同模块。",
                "audio_ref": None, "duration_seconds": None, "duration_basis": "unknown", "retry_of": None,
            }],
            "observations": [{
                "attempt_id": "a1", "observer": "ai", "dimension": "structure",
                "evidence": "只说了‘我实现了协同模块’", "interpretation": "尚未说明问题来源",
            }],
            "adjustment": "先说明问题再介绍动作",
            "next_step": {"task": "无提示重讲开场", "target_seconds": 60, "cue_level": "none", "next_skill": "interview-package"},
        }

    def record(self, value: dict) -> subprocess.CompletedProcess[str]:
        path = self.root / "session-input.json"
        self.save(path, value)
        return self.run_script(PRACTICE, "record", *self.args, "--input", str(path))

    def status(self, *args: str) -> dict:
        result = self.run_script(PRACTICE, "status", *self.args, *args)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        return json.loads(result.stdout)

    def test_snapshot_and_status_are_read_only(self) -> None:
        before = {path: path.read_bytes() for path in self.root.rglob("*") if path.is_file()}
        self.assertEqual(self.source["sha256"], hashlib.sha256(self.artifact.read_bytes()).hexdigest())
        self.assertEqual(len(self.source["claims_sha256"]), 64)
        self.assertIsNone(self.status()["last_session"])
        after = {path: path.read_bytes() for path in self.root.rglob("*") if path.is_file()}
        self.assertEqual(before, after)

    def test_append_resume_and_no_fact_or_stage_changes(self) -> None:
        protected = [self.state / name for name in ("claims.json", "positioning.json", "feedback.jsonl")]
        protected += [self.manifest, self.artifact]
        before = {path: path.read_bytes() for path in protected}
        first = self.session()
        result = self.record(first)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        second = self.session("practice-002")
        second["resumes_session_id"] = first["id"]
        second["next_step"]["task"] = "无提示解释协同对象生命周期"
        result = self.record(second)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        status = self.status("--project-id", "example")
        self.assertEqual(status["next_step"], second["next_step"])
        self.assertFalse(status["needs_rebaseline"])
        log = self.state / "practice" / "example" / "sessions.jsonl"
        self.assertEqual([json.loads(line) for line in log.read_text(encoding="utf-8").splitlines()], [first, second])
        self.assertEqual(before, {path: path.read_bytes() for path in protected})
        self.assertFalse(any((self.state / "opportunities").iterdir()))
        lint = self.run_script(LINT, *self.args)
        self.assertEqual(lint.returncode, 0, lint.stdout + lint.stderr)
        self.assertIn("2 practice sessions", lint.stdout)

    def test_source_and_claim_drift_preserve_history(self) -> None:
        self.assertEqual(self.record(self.session()).returncode, 0)
        log = self.state / "practice" / "example" / "sessions.jsonl"
        before = log.read_bytes()
        for drift in ("artifact", "claims", "manifest"):
            with self.subTest(drift=drift):
                if drift == "artifact":
                    self.artifact.write_text("# 更新后底稿\n", encoding="utf-8")
                elif drift == "claims":
                    self.claim["statement"] = "更新后已确认事实"
                    self.save(self.state / "claims.json", {"schema_version": 1, "claims": [self.claim]})
                else:
                    manifest = json.loads(self.manifest.read_text(encoding="utf-8"))
                    manifest["status"] = "stale"
                    self.save(self.manifest, manifest)
                status = self.status("--project-id", "example")
                self.assertTrue(status["needs_rebaseline"])
                self.assertIn("先核对", status["next_step"]["task"])
                self.assertEqual(log.read_bytes(), before)
                lint = self.run_script(LINT, *self.args)
                self.assertEqual(lint.returncode, 0, lint.stdout + lint.stderr)
                self.assertIn("historical record retained", lint.stdout)

    def test_record_preserves_snapshot_taken_before_source_change(self) -> None:
        value = self.session()
        self.artifact.write_text("# 练习期间变化\n", encoding="utf-8")
        result = self.record(value)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertTrue(json.loads(result.stdout)["warnings"])
        self.assertEqual(self.status()["last_session"]["source"], self.source)

    def test_contexts_are_isolated_and_cross_context_resume_is_rejected(self) -> None:
        opportunity = self.state / "opportunities" / "example-role" / "opportunity.json"
        self.save(opportunity, {"id": "example-role", "stage": "practicing"})
        before = opportunity.read_bytes()
        general = self.session()
        self.assertEqual(self.record(general).returncode, 0)
        targeted = self.session("practice-targeted")
        targeted["opportunity_id"] = "example-role"
        targeted["next_step"]["task"] = "岗位特定追问"
        self.assertEqual(self.record(targeted).returncode, 0)
        self.assertEqual(self.status()["last_session"]["id"], general["id"])
        self.assertEqual(self.status("--opportunity-id", "example-role")["last_session"]["id"], targeted["id"])
        invalid = self.session("practice-invalid")
        invalid["resumes_session_id"] = targeted["id"]
        self.assertNotEqual(self.record(invalid).returncode, 0)
        self.assertEqual(opportunity.read_bytes(), before)

    def test_multiple_projects_require_selection(self) -> None:
        self.assertEqual(self.record(self.session()).returncode, 0)
        self.assertEqual(self.record(self.session("other-001", "other")).returncode, 0)
        status = self.status()
        self.assertTrue(status["needs_project_selection"])
        self.assertEqual(status["projects"], ["example", "other"])

    def test_invalid_records_are_rejected_without_writes(self) -> None:
        mutations = [
            lambda value: value.update(project_id="../escape"),
            lambda value: value.update(opportunity_id="../../outside"),
            lambda value: value["source"].update(artifact="../outside.md"),
            lambda value: value["source"].update(claim_ids=["unknown"]),
            lambda value: value.update(recorded_at="2026-10-04T10:00:00"),
            lambda value: value.update(attempts=[]),
            lambda value: value.update(observations=[]),
            lambda value: value["attempts"][0].update(response=""),
            lambda value: value["attempts"][0].update(duration_seconds=90),
            lambda value: value["attempts"][0].update(duration_basis="user_timer"),
            lambda value: value["attempts"][0].update(duration_seconds=True, duration_basis="user_timer"),
            lambda value: value["attempts"][0].update(exercise="retry", retry_of="a1"),
            lambda value: value["attempts"][0].update(input_kind="audio", response=None),
            lambda value: value["attempts"][0].update(cue_level=[]),
            lambda value: value["next_step"].update(next_skill=[]),
            lambda value: value.update(next_step=[value["next_step"]]),
            lambda value: value["next_step"].update(target_seconds=None),
            lambda value: value.update(resumes_session_id="missing"),
        ]
        for mutation in mutations:
            with self.subTest(mutation=mutation):
                value = self.session()
                mutation(value)
                result = self.record(value)
                self.assertNotEqual(result.returncode, 0)
                self.assertNotIn("Traceback", result.stderr)
                self.assertFalse((self.state / "practice").exists())

    def test_interrupted_without_attempt_and_evidence_route(self) -> None:
        value = self.session()
        value.update(status="interrupted", attempts=[], observations=[], adjustment=None)
        value["next_step"] = {"task": "核对个人协同服务职责", "target_seconds": None, "cue_level": "none", "next_skill": "career-evidence"}
        self.assertEqual(self.record(value).returncode, 0)
        self.assertEqual(self.status()["recommended_next_skill"], "career-evidence")

    def test_retry_links_and_user_measured_duration(self) -> None:
        value = self.session()
        retry = copy.deepcopy(value["attempts"][0])
        retry.update(id="a2", exercise="retry", retry_of="a1", cue_level="keywords", duration_seconds=58, duration_basis="user_timer")
        value["attempts"].append(retry)
        self.assertEqual(self.record(value).returncode, 0)
        self.assertEqual(self.status()["last_session"]["attempts"][1]["duration_seconds"], 58)

    def test_duplicate_malformed_jsonl_and_unterminated_lines_do_not_overwrite(self) -> None:
        self.assertEqual(self.record(self.session()).returncode, 0)
        log = self.state / "practice" / "example" / "sessions.jsonl"
        original = log.read_bytes()
        duplicate = self.record(self.session())
        self.assertNotEqual(duplicate.returncode, 0)
        self.assertEqual(log.read_bytes(), original)
        log.write_bytes(original + b"{invalid}\n")
        malformed = self.run_script(LINT, *self.args)
        self.assertNotEqual(malformed.returncode, 0)
        self.assertIn("invalid practice JSONL", malformed.stdout)
        self.assertNotEqual(self.record(self.session("practice-002")).returncode, 0)
        self.assertEqual(log.read_bytes(), original + b"{invalid}\n")
        log.write_bytes(original.rstrip(b"\n"))
        self.assertNotEqual(self.record(self.session("practice-002")).returncode, 0)
        self.assertEqual(log.read_bytes(), original.rstrip(b"\n"))

    def test_unrelated_claim_changes_do_not_invalidate_practice(self) -> None:
        self.assertEqual(self.record(self.session()).returncode, 0)
        unrelated = copy.deepcopy(self.claim)
        unrelated.update(id="other.scope", statement="另一个项目事实")
        self.save(self.state / "claims.json", {"schema_version": 1, "claims": [unrelated, self.claim]})
        self.assertEqual(self.source, self.get_snapshot())
        self.assertFalse(self.status()["needs_rebaseline"])

    def test_lint_handles_invalid_field_types_and_encoding_without_traceback(self) -> None:
        path = self.state / "practice" / "example" / "sessions.jsonl"
        path.parent.mkdir(parents=True)
        value = self.session()
        value["attempts"][0]["cue_level"] = []
        path.write_text(json.dumps(value) + "\n", encoding="utf-8")
        result = self.run_script(LINT, *self.args)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("invalid attempt cue_level", result.stdout)
        self.assertNotIn("Traceback", result.stderr)
        path.write_bytes(b"\xff\n")
        result = self.run_script(LINT, *self.args)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("cannot read practice log", result.stdout)
        self.assertNotIn("Traceback", result.stderr)

    def test_audio_reference_and_media_duration(self) -> None:
        value = self.session()
        value["attempts"][0].update(input_kind="audio", response=None, audio_ref="/private/local-recording.m4a", duration_seconds=120, duration_basis="media_metadata")
        value["observations"][0].update(observer="user", dimension="delivery", evidence="用户自评：开场有停顿", interpretation="下轮复测开场")
        self.assertEqual(self.record(value).returncode, 0)
        self.assertEqual(self.status()["last_session"]["attempts"][0]["response"], None)

    def test_snapshot_rejects_unconfirmed_and_path_escape(self) -> None:
        self.claim["status"] = "candidate"
        self.save(self.state / "claims.json", {"schema_version": 1, "claims": [self.claim]})
        rejected = self.run_script(PRACTICE, "snapshot", *self.args, "--manifest", "manifests/interview-example.json")
        self.assertNotEqual(rejected.returncode, 0)
        escaped = self.run_script(PRACTICE, "snapshot", *self.args, "--manifest", "../outside.json")
        self.assertNotEqual(escaped.returncode, 0)


if __name__ == "__main__":
    unittest.main()
