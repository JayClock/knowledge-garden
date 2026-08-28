from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
MODES = [
    "deep-reading",
    "concept-visualization",
    "spatial-mapping",
    "idea-integration",
    "knowledge-exploration",
    "narrative-composition",
    "system-review",
]


class VisualPkmStructureTest(unittest.TestCase):
    def test_router_references_every_mode(self) -> None:
        router = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
        for mode in MODES:
            self.assertIn(f"references/modes/{mode}.md", router)
            reference = SKILL_DIR / "references" / "modes" / f"{mode}.md"
            self.assertTrue(reference.exists(), mode)
            self.assertIn(f"Mode ID：`{mode}`", reference.read_text(encoding="utf-8"))

    def test_no_old_independent_skill_names_remain(self) -> None:
        forbidden = [f"visual-pkm-{mode}/SKILL.md" for mode in MODES]
        for path in SKILL_DIR.rglob("*"):
            if not path.is_file() or "__pycache__" in path.parts:
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            for value in forbidden:
                self.assertNotIn(value, text, f"{path}: {value}")

    def test_mode_evals_cover_all_modes(self) -> None:
        behavior = json.loads((SKILL_DIR / "evals" / "evals.json").read_text(encoding="utf-8"))
        self.assertEqual(behavior["skill_name"], "visual-pkm")
        self.assertEqual(set(MODES), {item["mode"] for item in behavior["evals"]})
        self.assertGreaterEqual(len(behavior["evals"]), 40)
        triggers = json.loads((SKILL_DIR / "evals" / "trigger-evals.json").read_text(encoding="utf-8"))
        self.assertEqual(len(triggers), 32)
        self.assertEqual(sum(1 for item in triggers if item["should_trigger"]), 16)

    def test_concept_scripts_are_callable(self) -> None:
        for name in (
            "prepare_visual_main_note.py",
            "render_association_pool.py",
            "svg_palette.py",
            "validate_icon_library.py",
        ):
            result = subprocess.run(
                [sys.executable, str(SKILL_DIR / "scripts" / name), "--help"],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 0, f"{name}: {result.stdout}{result.stderr}")

    def test_concept_support_references_exist(self) -> None:
        support = SKILL_DIR / "references" / "concept-visualization"
        for name in (
            "association-pool-html.md",
            "card-connections.md",
            "excalidraw-note-preparation.md",
            "human-guided-checkpoints.md",
            "material-source-order.md",
            "palette-sync-state.json",
            "palettes.md",
            "visual-zettelkasten-template.md",
        ):
            self.assertTrue((support / name).exists(), name)

    def test_palette_state_only_tracks_existing_non_icon_drawings(self) -> None:
        repo_root = SKILL_DIR.parents[2]
        state = json.loads(
            (SKILL_DIR / "references" / "concept-visualization" / "palette-sync-state.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertTrue(state["managedFiles"])
        for item in state["managedFiles"]:
            self.assertFalse(item["path"].startswith("Knowledge/Assets/Excalidraw/Icon -"))
            self.assertTrue((repo_root / "content" / item["path"]).exists(), item["path"])

    def test_palette_shell_is_syntax_valid(self) -> None:
        result = subprocess.run(
            ["bash", "-n", str(SKILL_DIR / "scripts" / "sync_excalidraw_palette.sh")],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
