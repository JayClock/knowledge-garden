from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1]
SCRIPT = SKILL / "scripts" / "greeting_template.py"
LINT = SKILL / "scripts" / "state_lint.py"
INIT = SKILL / "scripts" / "init_state.py"
PROMPT = SKILL.parent / "resume-package" / "assets" / "job-greeting-prompt.md"


class GreetingTemplateTest(unittest.TestCase):
    def run_script(self, script: Path, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(script), *args], capture_output=True, text=True,
            encoding="utf-8", env={**os.environ, "PYTHONUTF8": "1"}, check=False,
        )

    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        initialized = self.run_script(INIT, "--root", str(self.root))
        self.assertEqual(initialized.returncode, 0, initialized.stderr)
        self.state = self.root / ".career"
        self.args = ("--state-dir", str(self.state), "--repo-root", str(self.root))
        self.resume = self.state / "resume.md"
        self.resume.write_text("# Candidate\n\nConfirmed project\n\n```ts\nconst id = 1\n```\n", encoding="utf-8")
        self.prompt = self.root / "prompt.md"
        self.prompt.write_text(PROMPT.read_text(encoding="utf-8"), encoding="utf-8")
        self.project = self.root / "project-one.md"
        self.project.write_text("Project notes, including unconfirmed metrics not for copying\n", encoding="utf-8")
        self.claim = {
            "id": "project.scope", "statement": "Confirmed project", "kind": "project_scope",
            "ownership": "direct", "completion": "implemented", "status": "confirmed",
            "evidence": [{"type": "user_confirmation", "locator": "Confirmed by user"}],
            "metrics": [], "constraints": [], "tags": [],
        }
        self.claims = [self.claim]
        self.save_claims()
        self.resume_manifest_path = self.state / "manifests" / "resume.json"
        self.resume_manifest = {
            "schema_version": 1, "artifact": ".career/resume.md", "artifact_type": "resume",
            "generated_by": "resume-package", "opportunity_id": None,
            "claim_ids": ["project.scope"], "status": "current",
            "source_sections": [{"path": "project-one.md"}],
        }
        self.save_resume_manifest()
        self.config_path = self.state / "config.json"
        self.config = json.loads(self.config_path.read_text(encoding="utf-8"))
        self.config["greeting_template"] = {
            "artifact": ".career/templates/greeting.md", "resume_manifest": "manifests/resume.json",
            "prompt_template": "prompt.md", "watch_sources": ["project-one.md"],
            "watch_globs": ["project-*.md"],
        }
        self.save_config()
        self.output = self.state / "templates" / "greeting.md"
        self.manifest_path = self.state / "manifests" / "job-greeting-template.json"

    def save_claims(self) -> None:
        (self.state / "claims.json").write_text(json.dumps({"schema_version": 1, "claims": self.claims}), encoding="utf-8")

    def save_resume_manifest(self) -> None:
        self.resume_manifest["artifact_sha256"] = hashlib.sha256(self.resume.read_bytes()).hexdigest()
        selected = sorted(
            (claim for claim in self.claims if claim["id"] in self.resume_manifest["claim_ids"]),
            key=lambda claim: claim["id"],
        )
        payload = json.dumps(selected, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        self.resume_manifest["claims_sha256"] = hashlib.sha256(payload.encode("utf-8")).hexdigest()
        self.resume_manifest_path.write_text(json.dumps(self.resume_manifest), encoding="utf-8")

    def save_config(self) -> None:
        self.config_path.write_text(json.dumps(self.config), encoding="utf-8")

    def sync(self, *extra: str) -> subprocess.CompletedProcess[str]:
        return self.run_script(SCRIPT, "sync", *self.args, "--reviewed", *extra)

    def assert_success(self, result: subprocess.CompletedProcess[str]) -> None:
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_render_and_lint_are_valid_and_idempotent(self) -> None:
        self.assert_success(self.sync())
        text = self.output.read_text(encoding="utf-8")
        self.assertIn("## 角色", text)
        self.assertIn("## input", text)
        self.assertIn("## rules", text)
        self.assertIn("## outputformat", text)
        self.assertIn("````markdown\n" + self.resume.read_text(encoding="utf-8").strip() + "\n````", text)
        self.assertNotIn("unconfirmed metrics", text)
        before = (self.output.read_bytes(), self.manifest_path.read_bytes())
        self.assert_success(self.sync())
        self.assertEqual(before, (self.output.read_bytes(), self.manifest_path.read_bytes()))
        self.assert_success(self.run_script(SCRIPT, "check", *self.args))
        self.assert_success(self.run_script(LINT, *self.args))
        self.assertEqual(before, (self.output.read_bytes(), self.manifest_path.read_bytes()))

    def test_boss_helper_output_is_system_only_and_directly_copyable(self) -> None:
        self.assert_success(self.sync())
        text = self.output.read_text(encoding="utf-8")
        self.assertTrue(text.startswith("## 角色\n"))
        self.assertIn("Confirmed project", text)
        self.assertIn("当前岗位信息由 User 消息传入。", text)
        for removed in ("# System 消息", "# User 消息", "{{ jobData.", "{{CANDIDATE_RESUME}}",
                        "只有用户明确要求时", "请用户发送岗位信息", "只追问一个关键问题", "提供招聘截图"):
            self.assertNotIn(removed, text)
        self.assertIn("不索取材料", text)
        self.assertIn("无书信格式", text)
        self.assertIn("待分析数据", text)

    def test_contact_lines_are_omitted_without_editing_resume_or_claims(self) -> None:
        for claim_id, statement in (
            ("career.contact.phone", "联系电话为 13800000000"),
            ("career.contact.email", "邮箱为 candidate@example.com"),
        ):
            self.claims.append({**self.claim, "id": claim_id, "statement": statement})
            self.resume_manifest["claim_ids"].append(claim_id)
        self.save_claims()
        contact_lines = "**电话**：13800000000｜**邮箱**：candidate@example.com\nEmail: candidate@example.com\n"
        self.resume.write_text("# Candidate\n\n上海｜5 年软件开发经验\n" + contact_lines + "\nConfirmed project\n", encoding="utf-8")
        self.save_resume_manifest()
        before = (self.resume.read_bytes(), (self.state / "claims.json").read_bytes(), self.resume_manifest_path.read_bytes())
        self.assert_success(self.sync())
        text = self.output.read_text(encoding="utf-8")
        self.assertNotIn("13800000000", text)
        self.assertNotIn("candidate@example.com", text)
        self.assertIn(self.resume.read_text(encoding="utf-8").replace(contact_lines, "").strip(), text)
        manifest = json.loads(self.manifest_path.read_text(encoding="utf-8"))
        self.assertEqual(manifest["claim_ids"], ["project.scope"])
        payload = json.dumps([self.claim], ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        self.assertEqual(manifest["claims_sha256"], hashlib.sha256(payload.encode("utf-8")).hexdigest())
        self.assert_success(self.run_script(SCRIPT, "check", *self.args))
        self.assert_success(self.run_script(LINT, *self.args))
        self.assertEqual(before, (self.resume.read_bytes(), (self.state / "claims.json").read_bytes(), self.resume_manifest_path.read_bytes()))

    def test_contact_only_resume_is_rejected(self) -> None:
        self.resume.write_text("电话：13800000000\n邮箱：candidate@example.com\n", encoding="utf-8")
        self.save_resume_manifest()
        result = self.sync()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("after removing contact lines", result.stdout)
        self.assertFalse(self.output.exists())

    def test_sync_requires_review_and_check_never_creates_files(self) -> None:
        result = self.run_script(SCRIPT, "sync", *self.args)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("--reviewed", result.stdout)
        self.assertNotEqual(self.run_script(SCRIPT, "check", *self.args).returncode, 0)
        self.assertFalse(self.output.exists())
        self.assertFalse(self.manifest_path.exists())

    def test_resume_changes_require_reviewed_manifest_then_propagate(self) -> None:
        self.assert_success(self.sync())
        before = self.output.read_bytes()
        self.resume.write_text("# Candidate\n\nUpdated confirmed project\n", encoding="utf-8")
        self.assertNotEqual(self.run_script(SCRIPT, "check", *self.args).returncode, 0)
        result = self.sync()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("artifact_sha256", result.stdout)
        self.assertEqual(before, self.output.read_bytes())
        self.save_resume_manifest()
        self.assert_success(self.sync())
        self.assertIn("Updated confirmed project", self.output.read_text(encoding="utf-8"))
        self.assert_success(self.run_script(LINT, *self.args))

    def test_project_and_new_glob_sources_invalidate_until_review(self) -> None:
        self.assert_success(self.sync())
        before = self.output.read_bytes()
        self.project.write_text("New project explanation, pending semantic review\n", encoding="utf-8")
        result = self.run_script(LINT, *self.args)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("source_files changed", result.stdout)
        self.assertEqual(before, self.output.read_bytes())
        self.assert_success(self.sync())
        self.assertEqual(before, self.output.read_bytes())
        extra = self.root / "project-two.md"
        extra.write_text("New project for selection review\n", encoding="utf-8")
        self.assertNotEqual(self.run_script(SCRIPT, "check", *self.args).returncode, 0)
        self.assert_success(self.sync())
        extra.unlink()
        self.assertNotEqual(self.run_script(SCRIPT, "check", *self.args).returncode, 0)

    def test_rule_changes_propagate_without_hardcoded_resume(self) -> None:
        self.assert_success(self.sync())
        self.prompt.write_text(self.prompt.read_text(encoding="utf-8") + "\nRule clarification\n", encoding="utf-8")
        self.assertNotEqual(self.run_script(SCRIPT, "check", *self.args).returncode, 0)
        self.assert_success(self.sync())
        self.assertIn("Rule clarification", self.output.read_text(encoding="utf-8"))

    def test_changed_claim_or_stale_source_cannot_pass_as_current(self) -> None:
        self.assert_success(self.sync())
        self.claim["statement"] = "Corrected project scope"
        self.save_claims()
        result = self.run_script(LINT, *self.args)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("claims_sha256 changed", result.stdout)
        self.assertNotEqual(self.sync().returncode, 0)
        self.save_resume_manifest()
        self.assert_success(self.sync())
        self.assert_success(self.run_script(SCRIPT, "check", *self.args))
        self.claim["status"] = "candidate"
        self.save_claims()
        result = self.sync()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("non-confirmed claim", result.stdout)
        self.claim["status"] = "confirmed"
        self.save_claims()
        self.resume_manifest["status"] = "stale"
        self.save_resume_manifest()
        self.assertNotEqual(self.sync().returncode, 0)

    def test_manual_edits_are_preserved_unless_explicitly_overridden(self) -> None:
        self.assert_success(self.sync())
        self.output.write_text("User manual edits\n", encoding="utf-8")
        self.assertNotEqual(self.sync().returncode, 0)
        self.assertEqual(self.output.read_text(encoding="utf-8"), "User manual edits\n")
        self.assert_success(self.sync("--overwrite-edited"))
        self.assert_success(self.run_script(SCRIPT, "check", *self.args))

    def test_stale_mark_preserves_content_but_blocks_reuse(self) -> None:
        self.assert_success(self.sync())
        before = self.output.read_bytes()
        self.assert_success(self.run_script(SCRIPT, "mark-stale", *self.args))
        self.assertEqual(before, self.output.read_bytes())
        self.assertNotEqual(self.run_script(SCRIPT, "check", *self.args).returncode, 0)
        result = self.run_script(LINT, *self.args)
        self.assert_success(result)
        self.assertIn("greeting template is stale", result.stdout)
        self.assert_success(self.sync())
        self.assert_success(self.run_script(SCRIPT, "check", *self.args))

    def test_public_or_escaping_paths_and_bad_placeholder_are_rejected(self) -> None:
        for artifact in ("content/private.md", "../outside.md", ".career/resume.md"):
            with self.subTest(artifact=artifact):
                self.config["greeting_template"]["artifact"] = artifact
                self.save_config()
                self.assertNotEqual(self.sync().returncode, 0)
        self.config["greeting_template"]["artifact"] = ".career/templates/greeting.md"
        self.save_config()
        self.prompt.write_text("Missing placeholder\n", encoding="utf-8")
        self.assertNotEqual(self.sync().returncode, 0)
        self.assertFalse(self.output.exists())

    def test_disabled_feature_is_backward_compatible(self) -> None:
        del self.config["greeting_template"]
        self.save_config()
        self.assert_success(self.run_script(SCRIPT, "check", *self.args))
        self.assert_success(self.run_script(LINT, *self.args))
        self.assertNotEqual(self.sync().returncode, 0)
        self.assertFalse(self.output.exists())


if __name__ == "__main__":
    unittest.main()
