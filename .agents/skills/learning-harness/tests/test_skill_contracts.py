from __future__ import annotations

import json
import unittest
from pathlib import Path

SKILLS_ROOT = Path(__file__).resolve().parents[2]
LEARNING = SKILLS_ROOT / "learning-harness"
VISUAL = SKILLS_ROOT / "visual-pkm"
MODES = {
    "deep-reading",
    "concept-visualization",
    "spatial-mapping",
    "idea-integration",
    "knowledge-exploration",
    "narrative-composition",
    "system-review",
}


class LearningHarnessContractTest(unittest.TestCase):
    def test_only_two_ai_facing_semantic_skills(self) -> None:
        learning = (LEARNING / "SKILL.md").read_text(encoding="utf-8")
        visual = (VISUAL / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("events.jsonl", learning)
        self.assertIn("apply_action_result.py", learning)
        self.assertIn("action_result", visual)
        self.assertIn("observations:", visual)
        self.assertNotIn("checkpoints:", visual)
        self.assertFalse((SKILLS_ROOT / "VISUAL_PKM_USAGE.md").exists())

    def test_visual_pkm_executes_commands_and_reports_action_results(self) -> None:
        router = (VISUAL / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("command_id:", router)
        self.assertIn("based_on_seq:", router)
        self.assertIn("action: verify-expression", router)
        self.assertIn("不选择其他 mode 或 action", router)
        for mode in MODES:
            self.assertTrue((VISUAL / "references" / "modes" / f"{mode}.md").exists())
            self.assertIn(f"references/modes/{mode}.md", router)

    def test_learning_has_only_event_progress_contract(self) -> None:
        all_text = "\n".join(path.read_text(encoding="utf-8") for path in LEARNING.rglob("*.md"))
        self.assertNotIn("checkpoints:", all_text)
        self.assertNotIn("current_phase", all_text)
        self.assertFalse((LEARNING / "schemas" / "progress.schema.json").exists())
        self.assertTrue((LEARNING / "schemas" / "command.schema.json").exists())
        self.assertTrue((LEARNING / "schemas" / "action-result.schema.json").exists())
        state_lib = (LEARNING / "scripts" / "learning_state_lib.py").read_text(encoding="utf-8")
        self.assertNotIn('write_json_atomic(directory / "progress.json"', state_lib)
        self.assertIn('snapshot["next_command"] = derive_next_command', state_lib)
        result_schema = json.loads((LEARNING / "schemas" / "action-result.schema.json").read_text(encoding="utf-8"))
        observation_types = result_schema["properties"]["observations"]["items"]["properties"]["type"]["enum"]
        self.assertEqual(
            observation_types,
            ["expression_qualified", "evidence_checked", "attempt_recorded", "blocker_added"],
        )

    def test_behavior_and_trigger_evals_are_well_formed(self) -> None:
        behavior = json.loads((LEARNING / "evals" / "evals.json").read_text(encoding="utf-8"))
        self.assertEqual(behavior["skill_name"], "learning-harness")
        self.assertGreaterEqual(len(behavior["evals"]), 8)
        self.assertEqual(len({item["id"] for item in behavior["evals"]}), len(behavior["evals"]))
        triggers = json.loads((LEARNING / "evals" / "trigger-evals.json").read_text(encoding="utf-8"))
        self.assertGreaterEqual(sum(item["should_trigger"] for item in triggers), 8)
        self.assertGreaterEqual(sum(not item["should_trigger"] for item in triggers), 8)

    def test_new_projects_default_to_tasknote_projection(self) -> None:
        content = (LEARNING / "SKILL.md").read_text(encoding="utf-8")
        recorder = (LEARNING / "scripts" / "record_progress.py").read_text(encoding="utf-8")
        self.assertIn("`init-project` 默认创建", content)
        self.assertIn('"--no-tasknote"', recorder)
        self.assertIn("create_default_tasknote", recorder)

    def test_progressive_disclosure_references_exist(self) -> None:
        content = (LEARNING / "SKILL.md").read_text(encoding="utf-8")
        for reference in (
            "references/state-schema.md",
            "references/routing.md",
            "references/completion-gates.md",
            "references/tasknotes-projection.md",
        ):
            self.assertIn(reference, content)
            self.assertTrue((LEARNING / reference).exists())


if __name__ == "__main__":
    unittest.main()
