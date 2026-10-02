from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
INIT = SKILL_DIR / "scripts" / "init_state.py"
LINT = SKILL_DIR / "scripts" / "state_lint.py"
IMPACT = SKILL_DIR / "scripts" / "impact_scan.py"
STATUS = SKILL_DIR / "scripts" / "opportunity_status.py"


class CareerHarnessScriptsTest(unittest.TestCase):
    def run_script(self, script: Path, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(script), *args],
            check=False,
            capture_output=True,
            text=True,
        )

    def initialize(self, root: Path) -> Path:
        result = self.run_script(INIT, "--root", str(root))
        self.assertEqual(result.returncode, 0, result.stderr)
        return root / ".career"

    def test_initialized_state_is_valid(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            state = self.initialize(root)
            result = self.run_script(LINT, "--state-dir", str(state), "--repo-root", str(root))
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            claims = json.loads((state / "claims.json").read_text(encoding="utf-8"))
            self.assertEqual(claims, {"schema_version": 1, "claims": []})

    def test_history_path_initialization_and_no_overwrite(self) -> None:
        for with_content in (False, True):
            with self.subTest(with_content=with_content), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                if with_content:
                    (root / "content").mkdir()
                state = self.initialize(root)
                config_path = state / "config.json"
                config = json.loads(config_path.read_text(encoding="utf-8"))
                prefix = "content/" if with_content else ""
                self.assertEqual(config["paths"]["career_history"], f"{prefix}Knowledge/Outputs/职业经历.md")
                self.assertFalse((root / config["paths"]["career_history"]).exists())
                config["paths"]["career_history"] = "custom/经历.md"
                config_path.write_text(json.dumps(config), encoding="utf-8")
                self.initialize(root)
                self.assertEqual(json.loads(config_path.read_text(encoding="utf-8")), config)

    def test_history_path_rejects_missing_and_invalid_values(self) -> None:
        for value in (None, "", "../outside.md", str(Path.home() / "outside.md"), "history.txt"):
            with self.subTest(value=value), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                state = self.initialize(root)
                path = state / "config.json"
                config = json.loads(path.read_text(encoding="utf-8"))
                if value is None:
                    del config["paths"]["career_history"]
                else:
                    config["paths"]["career_history"] = value
                path.write_text(json.dumps(config), encoding="utf-8")
                lint = self.run_script(LINT, "--state-dir", str(state), "--repo-root", str(root))
                self.assertNotEqual(lint.returncode, 0, lint.stdout)
                self.assertIn("career_history", lint.stdout)

    def test_history_requires_matching_manifest_and_preserves_text(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            state = self.initialize(root)
            config = json.loads((state / "config.json").read_text(encoding="utf-8"))
            history = root / config["paths"]["career_history"]
            history.parent.mkdir(parents=True)
            text = "# 职业经历\n\n用户补充，待确认。\n"
            history.write_text(text, encoding="utf-8")
            args = ("--state-dir", str(state), "--repo-root", str(root))
            missing = self.run_script(LINT, *args)
            self.assertNotEqual(missing.returncode, 0)
            self.assertIn("requires manifests/career-history.json", missing.stdout)
            manifest = {
                "schema_version": 1,
                "artifact": config["paths"]["career_history"],
                "artifact_type": "career_history",
                "generated_by": "career-evidence",
                "opportunity_id": None,
                "claim_ids": [],
                "status": "stale",
            }
            manifest_path = state / "manifests" / "career-history.json"
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
            valid = self.run_script(LINT, *args)
            self.assertEqual(valid.returncode, 0, valid.stdout + valid.stderr)
            manifest["artifact"] = "wrong.md"
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
            invalid = self.run_script(LINT, *args)
            self.assertNotEqual(invalid.returncode, 0)
            self.assertIn("must match configured path", invalid.stdout)
            self.assertEqual(history.read_text(encoding="utf-8"), text)

    def test_confirmed_claim_and_manifest_are_valid(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            state = self.initialize(root)
            claims_path = state / "claims.json"
            claims = json.loads(claims_path.read_text(encoding="utf-8"))
            claims["claims"].append(
                {
                    "id": "project.example.scope",
                    "statement": "直接实现示例项目核心模块",
                    "kind": "project_contribution",
                    "project_id": "example",
                    "ownership": "direct",
                    "completion": "implemented",
                    "status": "confirmed",
                    "evidence": [{"type": "user_confirmation", "locator": "用户明确确认"}],
                    "metrics": [],
                    "constraints": [],
                    "tags": ["example"],
                }
            )
            claims_path.write_text(json.dumps(claims, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

            opportunity_dir = state / "opportunities" / "2026-example-role"
            manifest_dir = opportunity_dir / "manifests"
            manifest_dir.mkdir(parents=True)
            (opportunity_dir / "opportunity.json").write_text(
                json.dumps(
                    {
                        "schema_version": 1,
                        "id": "2026-example-role",
                        "stage": "packaged",
                        "target": {"company": "示例公司", "role": "工程师", "jd_source": "user", "deadline": None},
                        "requirements": [
                            {
                                "id": "req-1",
                                "text": "核心模块经验",
                                "priority": "must",
                                "claim_ids": ["project.example.scope"],
                                "gap": False,
                            }
                        ],
                        "selected_claim_ids": ["project.example.scope"],
                        "artifacts": ["outputs/resume.md"],
                        "feedback_ids": [],
                        "decisions": [],
                    },
                    ensure_ascii=False,
                    indent=2,
                )
                + "\n",
                encoding="utf-8",
            )
            output_dir = opportunity_dir / "outputs"
            output_dir.mkdir()
            (output_dir / "resume.md").write_text("# Resume\n", encoding="utf-8")
            manifest_path = manifest_dir / "resume.json"
            manifest_path.write_text(
                json.dumps(
                    {
                        "schema_version": 1,
                        "artifact": ".career/opportunities/2026-example-role/outputs/resume.md",
                        "artifact_type": "resume",
                        "opportunity_id": "2026-example-role",
                        "generated_by": "resume-package",
                        "claim_ids": ["project.example.scope"],
                        "status": "current",
                    },
                    ensure_ascii=False,
                    indent=2,
                )
                + "\n",
                encoding="utf-8",
            )
            (state / "feedback.jsonl").write_text(
                json.dumps(
                    {
                        "id": "feedback-1",
                        "opportunity_id": "2026-example-role",
                        "stage": "interview",
                        "signal": "回答需要压缩",
                        "classification": "expression_gap",
                        "affected_claim_ids": ["project.example.scope"],
                        "affected_artifacts": [".career/opportunities/2026-example-role/outputs/resume.md"],
                        "next_skill": "interview-package",
                    },
                    ensure_ascii=False,
                )
                + "\n",
                encoding="utf-8",
            )

            lint = self.run_script(LINT, "--state-dir", str(state), "--repo-root", str(root))
            self.assertEqual(lint.returncode, 0, lint.stdout + lint.stderr)
            self.assertIn("1 feedback records", lint.stdout)
            status = self.run_script(
                STATUS,
                "--state-dir",
                str(state),
                "--opportunity-id",
                "2026-example-role",
            )
            self.assertEqual(status.returncode, 0, status.stdout + status.stderr)
            self.assertIn('"recommended_next_skill": "interview-package"', status.stdout)
            impact = self.run_script(
                IMPACT,
                "--state-dir",
                str(state),
                "--claim-id",
                "project.example.scope",
                "--mark-stale",
            )
            self.assertEqual(impact.returncode, 0, impact.stdout + impact.stderr)
            self.assertEqual(json.loads(manifest_path.read_text(encoding="utf-8"))["status"], "stale")
            stale_status = self.run_script(
                STATUS,
                "--state-dir",
                str(state),
                "--opportunity-id",
                "2026-example-role",
            )
            self.assertNotEqual(stale_status.returncode, 0)
            self.assertIn("artifacts are stale or invalid", stale_status.stdout)

    def test_practice_only_mapped_opportunity_routes_to_interview_package(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            state = self.initialize(root)
            claims_path = state / "claims.json"
            claims = json.loads(claims_path.read_text(encoding="utf-8"))
            claims["claims"].append(
                {
                    "id": "career.example",
                    "statement": "已确认的练习事实",
                    "kind": "timeline",
                    "ownership": "not_applicable",
                    "completion": "validated",
                    "status": "confirmed",
                    "evidence": [{"type": "user_confirmation", "locator": "用户确认"}],
                    "metrics": [],
                    "constraints": [],
                    "tags": [],
                }
            )
            claims_path.write_text(json.dumps(claims, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

            opportunity_dir = state / "opportunities" / "2026-practice-role"
            opportunity_dir.mkdir(parents=True)
            (opportunity_dir / "opportunity.json").write_text(
                json.dumps(
                    {
                        "schema_version": 1,
                        "id": "2026-practice-role",
                        "stage": "mapped",
                        "purpose": "interview_practice",
                        "target": {"company": "示例公司", "role": "工程师", "jd_source": "user", "deadline": None},
                        "requirements": [
                            {
                                "id": "req-1",
                                "text": "练习要求",
                                "priority": "must",
                                "claim_ids": ["career.example"],
                                "gap": False,
                            }
                        ],
                        "selected_claim_ids": ["career.example"],
                        "artifacts": [],
                        "feedback_ids": [],
                        "decisions": [],
                    },
                    ensure_ascii=False,
                    indent=2,
                )
                + "\n",
                encoding="utf-8",
            )

            status = self.run_script(
                STATUS,
                "--state-dir",
                str(state),
                "--opportunity-id",
                "2026-practice-role",
            )
            self.assertEqual(status.returncode, 0, status.stdout + status.stderr)
            self.assertIn('"recommended_next_skill": "interview-package"', status.stdout)

    def test_resume_policy_requires_claim_and_content_marker(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            state = self.initialize(root)
            policy_claim = {
                "id": "career.capability.agent-harness-efficiency",
                "statement": "使用 Agent Harness 提升研发交付的可控性",
                "kind": "positioning",
                "ownership": "direct",
                "completion": "validated",
                "status": "confirmed",
                "evidence": [{"type": "user_confirmation", "locator": "用户确认"}],
                "metrics": [],
                "constraints": [],
                "tags": ["agent-harness"],
            }
            claims_path = state / "claims.json"
            claims = json.loads(claims_path.read_text(encoding="utf-8"))
            claims["claims"].append(policy_claim)
            claims_path.write_text(json.dumps(claims, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

            config_path = state / "config.json"
            config = json.loads(config_path.read_text(encoding="utf-8"))
            config["resume_policy"] = {
                "required_claim_ids": [policy_claim["id"]],
                "required_artifact_types": ["resume"],
                "content_check_artifact_types": ["resume"],
                "content_markers_any": ["Agent Harness"],
            }
            config_path.write_text(json.dumps(config, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

            opportunity_dir = state / "opportunities" / "2026-policy-role"
            manifest_dir = opportunity_dir / "manifests"
            output_dir = opportunity_dir / "outputs"
            manifest_dir.mkdir(parents=True)
            output_dir.mkdir()
            opportunity_path = opportunity_dir / "opportunity.json"
            opportunity = {
                "schema_version": 1,
                "id": "2026-policy-role",
                "stage": "mapped",
                "purpose": "application",
                "target": {"company": "示例公司", "role": "工程师", "jd_source": "user", "deadline": None},
                "requirements": [],
                "selected_claim_ids": [],
                "artifacts": ["outputs/resume.md"],
                "feedback_ids": [],
                "decisions": [],
            }
            opportunity_path.write_text(json.dumps(opportunity, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            resume_path = output_dir / "resume.md"
            resume_path.write_text("# Resume\n", encoding="utf-8")
            manifest_path = manifest_dir / "resume.json"
            manifest = {
                "schema_version": 1,
                "artifact": ".career/opportunities/2026-policy-role/outputs/resume.md",
                "artifact_type": "resume",
                "opportunity_id": "2026-policy-role",
                "generated_by": "resume-package",
                "claim_ids": [],
                "status": "current",
            }
            manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

            invalid = self.run_script(LINT, "--state-dir", str(state), "--repo-root", str(root))
            self.assertNotEqual(invalid.returncode, 0)
            self.assertIn("missing resume policy claim", invalid.stdout)
            self.assertIn("artifact must contain one of", invalid.stdout)

            opportunity["selected_claim_ids"] = [policy_claim["id"]]
            opportunity_path.write_text(json.dumps(opportunity, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            manifest["claim_ids"] = [policy_claim["id"]]
            manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            resume_path.write_text("# Resume\n\n研发提效：Agent Harness\n", encoding="utf-8")

            valid = self.run_script(LINT, "--state-dir", str(state), "--repo-root", str(root))
            self.assertEqual(valid.returncode, 0, valid.stdout + valid.stderr)

    def test_confirmed_claim_without_evidence_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            state = self.initialize(root)
            claims_path = state / "claims.json"
            claims = json.loads(claims_path.read_text(encoding="utf-8"))
            claims["claims"].append(
                {
                    "id": "project.invalid",
                    "statement": "没有证据的事实",
                    "kind": "project_scope",
                    "ownership": "direct",
                    "completion": "implemented",
                    "status": "confirmed",
                    "evidence": [],
                    "metrics": [],
                    "constraints": [],
                    "tags": [],
                }
            )
            claims_path.write_text(json.dumps(claims, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            result = self.run_script(LINT, "--state-dir", str(state), "--repo-root", str(root))
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("confirmed claim requires evidence", result.stdout)


if __name__ == "__main__":
    unittest.main()
