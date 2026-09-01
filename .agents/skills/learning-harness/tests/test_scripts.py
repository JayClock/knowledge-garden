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
APPLY_RESULT = SKILL_DIR / "scripts" / "apply_action_result.py"
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
            projection = json.loads((project / "projections" / "tasknote.json").read_text(encoding="utf-8"))
            tasknote = root / projection["path"]
            self.assertTrue(tasknote.exists())
            self.assertEqual(tasknote.name, "学习 - Course Loop.md")
            self.assertEqual(projection["source_seq"], 1)
            plan = json.loads((project / "plan.json").read_text(encoding="utf-8"))
            self.assertEqual(plan["completion_policy"]["unit"]["required"], ["coverage"])
            self.assertEqual(
                plan["completion_policy"]["project"]["required"],
                ["source_grounding", "retrieval", "application"],
            )
            snapshot = json.loads((project / "snapshot.json").read_text(encoding="utf-8"))
            self.assertEqual(snapshot["next_command"]["skill"], "learning-harness")
            self.assertEqual(snapshot["next_command"]["action"], "record-coverage")

    def test_init_project_can_explicitly_skip_tasknote_projection(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.initialize(root)
            source = self.create_source(root)
            result = self.run_script(
                RECORD,
                "--repo-root",
                str(root),
                "init-project",
                "--project-id",
                "course-without-tasknote",
                "--title",
                "Course Without TaskNote",
                "--focus-question",
                "How can this project avoid a Vault projection?",
                "--source",
                str(source.parent),
                "--unit",
                f"lesson-01={source}",
                "--no-tasknote",
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual(payload["tasknote_projection"]["status"], "disabled")
            project = root / ".learning" / "projects" / "course-without-tasknote"
            self.assertFalse((project / "projections" / "tasknote.json").exists())
            self.assertFalse((root / "content" / "TaskNotes" / "Tasks" / "学习 - Course Without TaskNote.md").exists())

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
            self.assertEqual(summary["next_command"]["skill"], "learning-harness")
            self.assertEqual(summary["next_command"]["action"], "capture-key-understanding")

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

    def test_action_result_must_match_current_command_and_state_seq(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.initialize(root)
            source = self.create_source(root)
            project = self.init_project(root, source)
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
                "--coverage",
                "read",
            )
            self.assertEqual(captured.returncode, 0, captured.stdout + captured.stderr)
            command = json.loads(self.run_script(STATUS, "--repo-root", str(root)).stdout)["next_command"]
            self.assertEqual(command["action"], "qualify-expression")

            result_path = root / "action-result.json"
            qualification = {
                "command_id": command["id"],
                "based_on_seq": command["based_on_seq"],
                "project_id": "course-loop",
                "skill": command["skill"],
                "mode": command["mode"],
                "action": command["action"],
                "subject": command["subject"],
                "status": "passed",
                "observations": [
                    {
                        "type": "expression_qualified",
                        "subject": {"kind": "unit", "id": "lesson-01"},
                        "payload": {"result": "qualified"},
                        "evidence_refs": [],
                        "caused_by": [],
                    }
                ],
                "gaps": [],
                "artifact_paths": [],
                "open_questions": [],
                "workflow_checkpoint": None,
                "needs_user_decision": False,
            }
            result_path.write_text(json.dumps(qualification), encoding="utf-8")
            applied = self.run_script(APPLY_RESULT, "--repo-root", str(root), "--file", str(result_path))
            self.assertEqual(applied.returncode, 0, applied.stdout + applied.stderr)
            payload = json.loads(applied.stdout)
            self.assertEqual(payload["command_id"], command["id"])
            self.assertEqual(payload["next_command"]["action"], "verify-expression")

            event_count = len((project / "events.jsonl").read_text(encoding="utf-8").splitlines())
            stale = self.run_script(APPLY_RESULT, "--repo-root", str(root), "--file", str(result_path))
            self.assertNotEqual(stale.returncode, 0)
            self.assertIn("does not match current command", stale.stderr)
            self.assertEqual(len((project / "events.jsonl").read_text(encoding="utf-8").splitlines()), event_count)

            verify = json.loads(self.run_script(STATUS, "--repo-root", str(root)).stdout)["next_command"]
            unrelated = {
                **qualification,
                "command_id": verify["id"],
                "based_on_seq": verify["based_on_seq"],
                "action": verify["action"],
                "subject": verify["subject"],
                "observations": [
                    {
                        "type": "coverage_recorded",
                        "subject": {"kind": "unit", "id": "lesson-01"},
                        "payload": {"coverage": "revisited"},
                        "evidence_refs": [],
                        "caused_by": [],
                    }
                ],
            }
            result_path.write_text(json.dumps(unrelated), encoding="utf-8")
            rejected = self.run_script(APPLY_RESULT, "--repo-root", str(root), "--file", str(result_path))
            self.assertNotEqual(rejected.returncode, 0)
            self.assertIn("not allowed for command action", rejected.stderr)

            evidence_result = {
                **qualification,
                "command_id": verify["id"],
                "based_on_seq": verify["based_on_seq"],
                "action": verify["action"],
                "subject": verify["subject"],
                "status": "partial",
                "observations": [
                    {
                        "type": "evidence_checked",
                        "subject": {"kind": "unit", "id": "lesson-01"},
                        "payload": {"result": "partial", "open_questions": ["What is persisted?"]},
                        "evidence_refs": [{"type": "file", "path": str(source), "locator": None}],
                        "caused_by": [],
                    }
                ],
                "gaps": ["The persistence boundary is unclear."],
            }
            result_path.write_text(json.dumps(evidence_result), encoding="utf-8")
            checked = self.run_script(APPLY_RESULT, "--repo-root", str(root), "--file", str(result_path))
            self.assertEqual(checked.returncode, 0, checked.stdout + checked.stderr)
            self.assertEqual(json.loads(checked.stdout)["next_command"]["action"], "verify-expression")

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
                "step-4-generate",
                "--data",
                '{"target_note_mode":"existing","target_note_path":"Knowledge/Notes/示例.md","visual_id":"example-visual","framework":"过程式","style_expression_ref":"evt-00000012"}',
            )
            self.assertEqual(workflow.returncode, 0, workflow.stdout + workflow.stderr)
            status = json.loads(self.run_script(STATUS, "--repo-root", str(root)).stdout)
            self.assertEqual(status["next_command"]["mode"], "concept-visualization")
            self.assertEqual(status["next_command"]["action"], "resume-workflow")
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
            self.assertEqual(blocked["next_command"]["skill"], "learning-harness")
            self.assertEqual(blocked["next_command"]["action"], "resolve-blocker")
            self.assertIn("解除", blocked["next_command"]["instruction"])
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
            self.assertEqual(resumed["next_command"]["mode"], "concept-visualization")
            self.assertEqual(resumed["next_command"]["action"], "resume-workflow")
            self.assertFalse((root / ".learning" / "projects" / "course-loop" / "workflows").exists())

    def test_schema_files_are_valid_json(self) -> None:
        names = {path.name for path in (SKILL_DIR / "schemas").glob("*.json")}
        self.assertNotIn("progress.schema.json", names)
        for path in sorted((SKILL_DIR / "schemas").glob("*.json")):
            value = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(value["$schema"], "https://json-schema.org/draft/2020-12/schema")


if __name__ == "__main__":
    unittest.main()
