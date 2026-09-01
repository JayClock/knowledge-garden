from __future__ import annotations

import json
import subprocess
import sys
import tempfile
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
            "write_visual_main_note.py",
            "extract_visual_icons.py",
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

    def test_direct_visual_scripts_plan_without_writes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            vault = Path(directory)
            (vault / ".obsidian").mkdir()
            (vault / "Templates").mkdir()
            (vault / "Knowledge/Notes").mkdir(parents=True)
            (vault / "Knowledge/Assets/Excalidraw").mkdir(parents=True)
            (vault / "Templates/知识卡.md").write_text(
                "---\nup: []\nsources: []\n---\n# {{title}}\n\n> [!abstract] 核心观点\n",
                encoding="utf-8",
            )
            (vault / "Knowledge/Notes/过滤.md").write_text(
                "---\nup: []\nsources: []\n---\n# 过滤\n", encoding="utf-8"
            )
            visual_spec = vault / "visual-spec.json"
            visual_spec.write_text(
                json.dumps(
                    {
                        "visual_id": "filtering-visual",
                        "core_message": "过滤降低噪声，但不删除。",
                        "framework": "过程式",
                        "style_brief": "从左到右，深蓝和橙色，手绘粗线。",
                        "defaults": {"roughness": 1},
                        "composition_plan": {
                            "style": "hand-drawn",
                            "spatial_grammar": "asymmetric organic flow",
                            "hand_drawn_cues": [
                                "scale contrast",
                                "curved paths",
                                "uneven spacing",
                            ],
                            "avoids": ["uniform-grid", "repeated-text-cards"],
                            "reason": "用不规则路径表现过滤与回流。",
                        },
                        "representation_plan": {
                            "priority": [
                                "library-icon",
                                "native-pictogram",
                                "shape-relation",
                                "text",
                            ],
                            "semantic_units": [
                                {
                                    "role": "过滤动作",
                                    "search_terms": ["筛网", "过滤", "filter"],
                                    "library_decision": "no-match",
                                    "choice": "native-pictogram",
                                    "element_keys": ["filter"],
                                    "reason": "本地没有准确表达暂时过滤的组件。",
                                },
                                {
                                    "role": "输入流",
                                    "search_terms": ["输入", "流动", "input flow"],
                                    "library_decision": "not-applicable",
                                    "choice": "shape-relation",
                                    "element_keys": ["flow"],
                                    "reason": "方向箭头比独立 icon 更准确。",
                                },
                            ],
                            "text_justifications": [],
                        },
                        "elements": [
                            {
                                "key": "filter",
                                "type": "diamond",
                                "x": 300,
                                "y": 160,
                                "width": 180,
                                "height": 220,
                                "group": "filter",
                                "role": "过滤",
                            },
                            {
                                "key": "flow",
                                "type": "arrow",
                                "points": [[0, 260], [300, 260]],
                                "role": "输入",
                            },
                        ],
                    },
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )
            write_plan = subprocess.run(
                [
                    sys.executable,
                    str(SKILL_DIR / "scripts/write_visual_main_note.py"),
                    "--visual-spec",
                    str(visual_spec),
                    "--existing",
                    "Knowledge/Notes/过滤.md",
                    "--vault-root",
                    str(vault),
                ],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(write_plan.returncode, 0, write_plan.stderr)
            write_data = json.loads(write_plan.stdout)
            self.assertFalse(write_data["writes"])
            self.assertEqual(write_data["elements"], 2)
            self.assertEqual(write_data["groups"], ["filter"])
            self.assertTrue(write_data["icon_first"])
            self.assertEqual(write_data["composition_style"], "hand-drawn")
            self.assertEqual(write_data["spatial_grammar"], "asymmetric organic flow")
            self.assertEqual(
                write_data["hand_drawn_cues"],
                ["scale contrast", "curved paths", "uneven spacing"],
            )
            self.assertEqual(
                write_data["representation_summary"],
                {
                    "library-icon": 0,
                    "native-pictogram": 1,
                    "shape-relation": 1,
                    "text": 0,
                },
            )
            self.assertEqual(write_data["justified_text_elements"], 0)

            invalid_spec = json.loads(visual_spec.read_text(encoding="utf-8"))
            invalid_spec["elements"].append(
                {
                    "key": "unjustified-label",
                    "type": "text",
                    "x": 20,
                    "y": 20,
                    "text": "过滤",
                }
            )
            visual_spec.write_text(
                json.dumps(invalid_spec, ensure_ascii=False), encoding="utf-8"
            )
            invalid_plan = subprocess.run(
                [
                    sys.executable,
                    str(SKILL_DIR / "scripts/write_visual_main_note.py"),
                    "--visual-spec",
                    str(visual_spec),
                    "--existing",
                    "Knowledge/Notes/过滤.md",
                    "--vault-root",
                    str(vault),
                ],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(invalid_plan.returncode, 2)
            self.assertIn("缺少必要性说明", invalid_plan.stderr)

            text_only_spec = json.loads(visual_spec.read_text(encoding="utf-8"))
            text_only_spec["elements"] = [
                {
                    "key": "text-only",
                    "type": "text",
                    "x": 20,
                    "y": 20,
                    "text": "过滤不是删除",
                }
            ]
            text_only_spec["representation_plan"]["semantic_units"] = [
                {
                    "role": "核心命题",
                    "search_terms": ["过滤", "删除", "filter"],
                    "library_decision": "no-match",
                    "choice": "text",
                    "element_keys": ["text-only"],
                    "reason": "错误地把全部意义退回文字。",
                }
            ]
            text_only_spec["representation_plan"]["text_justifications"] = [
                {"key": "text-only", "reason": "错误的文字主视觉。"}
            ]
            visual_spec.write_text(
                json.dumps(text_only_spec, ensure_ascii=False), encoding="utf-8"
            )
            text_only_plan = subprocess.run(
                [
                    sys.executable,
                    str(SKILL_DIR / "scripts/write_visual_main_note.py"),
                    "--visual-spec",
                    str(visual_spec),
                    "--existing",
                    "Knowledge/Notes/过滤.md",
                    "--vault-root",
                    str(vault),
                ],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(text_only_plan.returncode, 2)
            self.assertIn("主要语义不能全部由文字承担", text_only_plan.stderr)

            extraction_spec = vault / "icon-extraction.json"
            extraction_spec.write_text(
                json.dumps(
                    {
                        "visual_id": "filtering-visual",
                        "icons": [
                            {
                                "group": "filter",
                                "keywords": ["筛网", "过滤", "降噪"],
                                "source": "Own",
                            }
                        ],
                    },
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )
            extraction_plan = subprocess.run(
                [
                    sys.executable,
                    str(SKILL_DIR / "scripts/extract_visual_icons.py"),
                    "--note",
                    "Knowledge/Notes/过滤.md",
                    "--extraction-spec",
                    str(extraction_spec),
                    "--vault-root",
                    str(vault),
                ],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(extraction_plan.returncode, 0, extraction_plan.stderr)
            extraction_data = json.loads(extraction_plan.stdout)
            self.assertFalse(extraction_data["writes"])
            self.assertEqual(len(extraction_data["automatic_candidates"]), 1)

    def test_concept_support_references_exist(self) -> None:
        support = SKILL_DIR / "references" / "concept-visualization"
        for name in (
            "direct-visual-generation.md",
            "icon-first-generation.md",
            "card-connections.md",
            "visual-main-note-write.md",
            "human-guided-checkpoints.md",
            "material-source-order.md",
            "palette-sync-state.json",
            "palettes.md",
            "visual-zettelkasten-template.md",
        ):
            self.assertTrue((support / name).exists(), name)

    def test_concept_mode_uses_direct_generation(self) -> None:
        concept_paths = [
            SKILL_DIR / "references" / "modes" / "concept-visualization.md",
            SKILL_DIR / "references" / "concept-visualization" / "direct-visual-generation.md",
            SKILL_DIR / "references" / "concept-visualization" / "icon-first-generation.md",
            SKILL_DIR / "references" / "concept-visualization" / "visual-main-note-write.md",
            SKILL_DIR / "references" / "concept-visualization" / "human-guided-checkpoints.md",
            SKILL_DIR / "references" / "concept-visualization" / "visual-zettelkasten-template.md",
        ]
        combined = "\n".join(path.read_text(encoding="utf-8") for path in concept_paths)
        self.assertIn("write_visual_main_note.py", combined)
        self.assertIn("extract_visual_icons.py", combined)
        self.assertIn("完整视觉", combined)
        self.assertIn("自动判断", combined)
        self.assertIn("Icon First", combined)
        self.assertIn("composition_plan", combined)
        self.assertIn("hand-drawn", combined)
        self.assertIn("representation_plan", combined)
        self.assertIn("text_justifications", combined)

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
