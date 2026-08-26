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
