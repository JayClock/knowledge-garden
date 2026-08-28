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
}


class LearningHarnessContractTest(unittest.TestCase):
    def test_only_two_ai_facing_semantic_skills(self) -> None:
        learning = (LEARNING / "SKILL.md").read_text(encoding="utf-8")
        visual = (VISUAL / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("events.jsonl", learning)
        self.assertIn("apply_handoff.py", learning)
        self.assertIn("observations:", visual)
        self.assertNotIn("checkpoints:", visual)
        self.assertFalse((SKILLS_ROOT / "VISUAL_PKM_USAGE.md").exists())

    def test_visual_pkm_uses_handoff_and_modes(self) -> None:
        router = (VISUAL / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("learning_handoff:", router)
        self.assertIn("action: verify-expression", router)
        for mode in MODES:
            self.assertTrue((VISUAL / "references" / "modes" / f"{mode}.md").exists())
            self.assertIn(f"references/modes/{mode}.md", router)

    def test_learning_has_only_event_progress_contract(self) -> None:
        all_text = "\n".join(path.read_text(encoding="utf-8") for path in LEARNING.rglob("*.md"))
        self.assertNotIn("checkpoints:", all_text)
        self.assertNotIn("current_phase", all_text)
        self.assertFalse((LEARNING / "schemas" / "progress.schema.json").exists())
        self.assertNotIn('write_json_atomic(directory / "progress.json"', (LEARNING / "scripts" / "learning_state_lib.py").read_text(encoding="utf-8"))

    def test_behavior_and_trigger_evals_are_well_formed(self) -> None:
        behavior = json.loads((LEARNING / "evals" / "evals.json").read_text(encoding="utf-8"))
        self.assertEqual(behavior["skill_name"], "learning-harness")
        self.assertGreaterEqual(len(behavior["evals"]), 8)
        self.assertEqual(len({item["id"] for item in behavior["evals"]}), len(behavior["evals"]))
        triggers = json.loads((LEARNING / "evals" / "trigger-evals.json").read_text(encoding="utf-8"))
        self.assertGreaterEqual(sum(item["should_trigger"] for item in triggers), 8)
        self.assertGreaterEqual(sum(not item["should_trigger"] for item in triggers), 8)

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
