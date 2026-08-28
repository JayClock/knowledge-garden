from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
INIT = SKILL_DIR / "scripts" / "init_state.py"
RECORD = SKILL_DIR / "scripts" / "record_progress.py"
STATUS = SKILL_DIR / "scripts" / "learning_status.py"
LINT = SKILL_DIR / "scripts" / "state_lint.py"
REBUILD = SKILL_DIR / "scripts" / "rebuild_snapshot.py"
HANDOFF = SKILL_DIR / "scripts" / "apply_handoff.py"
SYNC = SKILL_DIR / "scripts" / "sync_tasknote.py"
INGEST = SKILL_DIR / "scripts" / "ingest_tasknote.py"


class LearningHarnessTest(unittest.TestCase):
    def run_script(self, script: Path, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run([sys.executable, str(script), *args], check=False, capture_output=True, text=True)

    def initialize(self, root: Path) -> None:
        result = self.run_script(INIT, "--root", str(root))
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def create_source(self, root: Path) -> Path:
        source = root / "content" / "Knowledge" / "Sources" / "course" / "lesson-01.md"
        source.parent.mkdir(parents=True)
        source.write_text("# Lesson 01\n\nState connects the outer and inner loops.\n", encoding="utf-8")
        return source

    def init_project(self, root: Path, source: Path) -> Path:
        result = self.run_script(
            RECORD,
            "--repo-root",
            str(root),
            "init-project",
            "--project-id",
            "course-loop",
            "--title",
            "Course Loop",
            "--focus-question",
            "How does learning become recoverable?",
            "--source",
            str(source.parent),
            "--unit",
            f"lesson-01={source}",
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        return root / ".learning" / "projects" / "course-loop"

    def test_empty_root_and_new_project_use_event_state_only(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.initialize(root)
            lint = self.run_script(LINT, "--repo-root", str(root))
            self.assertEqual(lint.returncode, 0, lint.stdout + lint.stderr)
            project = self.init_project(root, self.create_source(root))
            self.assertTrue((project / "events.jsonl").exists())
            self.assertTrue((project / "snapshot.json").exists())
            self.assertFalse((project / "progress.json").exists())
            self.assertFalse((project / "workflows").exists())
            plan = json.loads((project / "plan.json").read_text(encoding="utf-8"))
            self.assertEqual(plan["completion_policy"]["unit"]["required"], ["coverage"])
            self.assertEqual(
                plan["completion_policy"]["project"]["required"],
                ["source_grounding", "retrieval", "application"],
            )

    def test_coverage_does_not_imply_expression_or_understanding(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.initialize(root)
            self.init_project(root, self.create_source(root))
            result = self.run_script(
                RECORD,
                "--repo-root",
                str(root),
                "coverage",
                "--project-id",
                "course-loop",
                "--unit-id",
                "lesson-01",
                "--coverage",
                "read",
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            status = self.run_script(STATUS, "--repo-root", str(root))
            summary = json.loads(status.stdout)
            unit = summary["current_unit"]
            self.assertEqual(unit["coverage"], "read")
            self.assertEqual(unit["expression_status"], "not_requested")
            self.assertEqual(unit["evidence_status"], "not_requested")
            self.assertEqual(summary["completion"]["unit_ready"], 1)
            self.assertEqual(summary["next_action"]["mode"], "deep-reading")
            self.assertIn("关键", summary["next_action"]["action"])

    def test_evidence_check_only_starts_after_human_expression(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.initialize(root)
            source = self.create_source(root)
            project = self.init_project(root, source)
            rejected = self.run_script(
                RECORD,
                "--repo-root",
                str(root),
                "evidence-check",
                "--project-id",
                "course-loop",
                "--unit-id",
                "lesson-01",
                "--result",
                "supported",
                "--evidence-ref",
                str(source),
            )
            self.assertNotEqual(rejected.returncode, 0)
            self.assertIn("qualified user expression", rejected.stderr)
            self.assertEqual(len((project / "events.jsonl").read_text(encoding="utf-8").splitlines()), 1)

    def test_snapshot_is_fully_rebuildable_from_events(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.initialize(root)
            project = self.init_project(root, self.create_source(root))
            self.run_script(
                RECORD,
                "--repo-root",
                str(root),
                "coverage",
                "--project-id",
                "course-loop",
                "--unit-id",
                "lesson-01",
                "--coverage",
                "read",
            )
            before = json.loads((project / "snapshot.json").read_text(encoding="utf-8"))
            (project / "snapshot.json").unlink()
            rebuilt = self.run_script(REBUILD, "--repo-root", str(root), "--project-id", "course-loop")
            self.assertEqual(rebuilt.returncode, 0, rebuilt.stdout + rebuilt.stderr)
            after = json.loads((project / "snapshot.json").read_text(encoding="utf-8"))
            before.pop("generated_at")
            after.pop("generated_at")
            self.assertEqual(before, after)

    def test_complete_policy_uses_units_claims_and_real_attempts(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.initialize(root)
            source = self.create_source(root)
            self.init_project(root, source)
            expression = self.run_script(
                RECORD,
                "--repo-root",
                str(root),
                "expression",
                "--project-id",
                "course-loop",
                "--unit-id",
                "lesson-01",
                "--text",
                "I think durable state connects one learning session to the next.",
                "--coverage",
                "read",
                "--qualification",
                "qualified",
            )
            self.assertEqual(expression.returncode, 0, expression.stdout + expression.stderr)
            expression_ref = json.loads(expression.stdout)["expression_ref"]
            check = self.run_script(
                RECORD,
                "--repo-root",
                str(root),
                "evidence-check",
                "--project-id",
                "course-loop",
                "--unit-id",
                "lesson-01",
                "--result",
                "supported_with_boundary",
                "--evidence-ref",
                str(source),
            )
            self.assertEqual(check.returncode, 0, check.stdout + check.stderr)
            claim = self.run_script(
                RECORD,
                "--repo-root",
                str(root),
                "claim",
                "--project-id",
                "course-loop",
                "--claim-id",
                "durable-state",
                "--text",
                "State connects learning sessions.",
                "--unit-id",
                "lesson-01",
                "--expression-ref",
                str(root / expression_ref),
            )
            self.assertEqual(claim.returncode, 0, claim.stdout + claim.stderr)
            note = root / "content" / "Knowledge" / "Notes" / "Durable state.md"
            note.parent.mkdir(parents=True)
            note.write_text("# Durable state\n", encoding="utf-8")
            distill = self.run_script(
                RECORD,
                "--repo-root",
                str(root),
                "distill",
                "--project-id",
                "course-loop",
                "--claim-id",
                "durable-state",
                "--decision",
                "new",
                "--artifact",
                str(note),
            )
            self.assertEqual(distill.returncode, 0, distill.stdout + distill.stderr)
            for kind in ("retrieval", "application"):
                attempt = self.run_script(
                    RECORD,
                    "--repo-root",
                    str(root),
                    "attempt",
                    "--project-id",
                    "course-loop",
                    "--scope",
                    "project",
                    "--scope-id",
                    "course-loop",
                    "--kind",
                    kind,
                    "--result",
                    "success",
                    "--text",
                    f"Real {kind} evidence.",
                )
                self.assertEqual(attempt.returncode, 0, attempt.stdout + attempt.stderr)
            status = json.loads(self.run_script(STATUS, "--repo-root", str(root)).stdout)
            self.assertTrue(status["completion"]["complete_by_policy"])
            complete = self.run_script(
                RECORD,
                "--repo-root",
                str(root),
                "project-status",
                "--project-id",
                "course-loop",
                "--status",
                "complete",
            )
            self.assertEqual(complete.returncode, 0, complete.stdout + complete.stderr)
            lint = self.run_script(LINT, "--repo-root", str(root))
            self.assertEqual(lint.returncode, 0, lint.stdout + lint.stderr)

    def test_handoff_is_atomic_and_suggested_next_is_not_state(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.initialize(root)
            source = self.create_source(root)
            self.init_project(root, source)
            captured = self.run_script(
                RECORD,
                "--repo-root",
                str(root),
                "expression",
                "--project-id",
                "course-loop",
                "--unit-id",
                "lesson-01",
                "--text",
                "State may connect the two loops.",
            )
            self.assertEqual(captured.returncode, 0, captured.stdout + captured.stderr)
            handoff_path = root / "handoff.json"
            handoff_path.write_text(
                json.dumps(
                    {
                        "project_id": "course-loop",
                        "unit_id": "lesson-01",
                        "skill": "visual-pkm",
                        "mode": "deep-reading",
                        "action": "verify-expression",
                        "observations": [
                            {
                                "type": "expression_qualified",
                                "subject": {"kind": "unit", "id": "lesson-01"},
                                "payload": {"result": "qualified"},
                                "evidence_refs": [],
                                "caused_by": [],
                            },
                            {
                                "type": "evidence_checked",
                                "subject": {"kind": "unit", "id": "lesson-01"},
                                "payload": {"result": "partial", "open_questions": ["What is persisted?"]},
                                "evidence_refs": [{"type": "file", "path": str(source), "locator": None}],
                                "caused_by": [],
                            }
                        ],
                        "artifact_paths": [],
                        "open_questions": [],
                        "workflow": None,
                        "suggested_next": {"skill": "learning-harness", "action": "ignore me"},
                        "needs_user_decision": False,
                    }
                ),
                encoding="utf-8",
            )
            result = self.run_script(HANDOFF, "--repo-root", str(root), "--file", str(handoff_path))
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            payload = json.loads(result.stdout)
            self.assertTrue(payload["suggested_next_ignored"])
            self.assertNotEqual(payload["next_action"]["action"], "ignore me")

    def test_tasknote_projection_and_inbox_preserve_user_content(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.initialize(root)
            self.init_project(root, self.create_source(root))
            applied = self.run_script(SYNC, "--repo-root", str(root), "--project-id", "course-loop", "--apply")
            self.assertEqual(applied.returncode, 0, applied.stdout + applied.stderr)
            task_path = root / json.loads(applied.stdout)["path"]
            content = task_path.read_text(encoding="utf-8")
            content = content.replace(
                "## 进度收件箱\n",
                "## 进度收件箱\n\n- [ ] lesson-01 | coverage=read\n",
                1,
            )
            content = content.replace("## 用户备注\n", "## 用户备注\n\nKeep this note.\n")
            task_path.write_text(content, encoding="utf-8")
            dry = self.run_script(INGEST, "--repo-root", str(root), "--project-id", "course-loop")
            self.assertEqual(dry.returncode, 0, dry.stdout + dry.stderr)
            self.assertEqual(len(json.loads(dry.stdout)["entries"]), 1)
            ingest = self.run_script(INGEST, "--repo-root", str(root), "--project-id", "course-loop", "--apply")
            self.assertEqual(ingest.returncode, 0, ingest.stdout + ingest.stderr)
            resync = self.run_script(SYNC, "--repo-root", str(root), "--project-id", "course-loop", "--apply")
            self.assertEqual(resync.returncode, 0, resync.stdout + resync.stderr)
            updated = task_path.read_text(encoding="utf-8")
            self.assertIn("Keep this note.", updated)
            self.assertIn("- [x] lesson-01 | coverage=read", updated)
            self.assertIn("learningStateSeq:", updated)
            lint = self.run_script(LINT, "--repo-root", str(root))
            self.assertEqual(lint.returncode, 0, lint.stdout + lint.stderr)

    def test_workflow_and_blocker_are_event_derived_and_resolvable(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.initialize(root)
            self.init_project(root, self.create_source(root))
            workflow = self.run_script(
                RECORD,
                "--repo-root",
                str(root),
                "workflow",
                "--project-id",
                "course-loop",
                "--workflow-id",
                "concept-loop",
                "--mode",
                "concept-visualization",
                "--unit-id",
                "lesson-01",
                "--status",
                "in_progress",
                "--step",
                "step-4-preview",
                "--data",
                '{"preview_status":"needs_regeneration"}',
            )
            self.assertEqual(workflow.returncode, 0, workflow.stdout + workflow.stderr)
            status = json.loads(self.run_script(STATUS, "--repo-root", str(root)).stdout)
            self.assertEqual(status["next_action"]["mode"], "concept-visualization")
            blocker = self.run_script(
                RECORD,
                "--repo-root",
                str(root),
                "blocker",
                "--project-id",
                "course-loop",
                "--subject-kind",
                "unit",
                "--subject-id",
                "lesson-01",
                "--reason",
                "Source is unavailable.",
            )
            self.assertEqual(blocker.returncode, 0, blocker.stdout + blocker.stderr)
            blocker_id = json.loads(blocker.stdout)["blocker_id"]
            blocked = json.loads(self.run_script(STATUS, "--repo-root", str(root)).stdout)
            self.assertEqual(blocked["next_action"]["skill"], "learning-harness")
            self.assertIn("解除", blocked["next_action"]["action"])
            resolved = self.run_script(
                RECORD,
                "--repo-root",
                str(root),
                "resolve-blocker",
                "--project-id",
                "course-loop",
                "--blocker-id",
                blocker_id,
                "--resolution",
                "Source restored.",
            )
            self.assertEqual(resolved.returncode, 0, resolved.stdout + resolved.stderr)
            resumed = json.loads(self.run_script(STATUS, "--repo-root", str(root)).stdout)
            self.assertEqual(resumed["next_action"]["mode"], "concept-visualization")
            self.assertFalse((root / ".learning" / "projects" / "course-loop" / "workflows").exists())

    def test_schema_files_are_valid_json(self) -> None:
        names = {path.name for path in (SKILL_DIR / "schemas").glob("*.json")}
        self.assertNotIn("progress.schema.json", names)
        for path in sorted((SKILL_DIR / "schemas").glob("*.json")):
            value = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(value["$schema"], "https://json-schema.org/draft/2020-12/schema")


if __name__ == "__main__":
    unittest.main()
