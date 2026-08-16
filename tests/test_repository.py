import json
import os
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


class RepositoryTests(unittest.TestCase):
    def test_json_files_and_templates_are_valid(self):
        candidates = list(REPO_ROOT.rglob("*.json")) + list(REPO_ROOT.rglob("*.json.tmpl"))
        candidates = [path for path in candidates if ".git" not in path.parts]
        self.assertTrue(candidates)
        for path in candidates:
            with self.subTest(path=path.relative_to(REPO_ROOT)):
                json.loads(path.read_text(encoding="utf-8"))

    def test_greenfield_example_index_matches_detail_files(self):
        docs = REPO_ROOT / "examples" / "greenfield-todo-app" / "docs"
        index = json.loads((docs / "feature-list.json").read_text(encoding="utf-8"))
        index_ids = {entry["id"] for entry in index["features"]}
        detail_files = sorted((docs / "features").glob("F*.json"))
        detail_ids = {path.stem for path in detail_files}

        self.assertEqual(index_ids, detail_ids)
        self.assertEqual(index["meta"]["total_features"], len(index_ids))
        for path in detail_files:
            with self.subTest(path=path.name):
                detail = json.loads(path.read_text(encoding="utf-8"))
                self.assertEqual(detail["id"], path.stem)

    def test_claude_settings_register_both_hooks(self):
        settings = json.loads(
            (REPO_ROOT / "claude-code" / "settings.example.json").read_text(encoding="utf-8")
        )
        self.assertIn("PreToolUse", settings["hooks"])
        self.assertIn("PostToolUse", settings["hooks"])

    def test_hook_entrypoints_are_executable(self):
        entrypoints = [
            REPO_ROOT / "claude-code" / "hooks" / "gate-feature-done.py",
            REPO_ROOT / "claude-code" / "hooks" / "check-feature-list.py",
            REPO_ROOT / "git-hooks" / "commit-msg",
        ]
        for path in entrypoints:
            with self.subTest(path=path.relative_to(REPO_ROOT)):
                self.assertTrue(os.access(path, os.X_OK))


if __name__ == "__main__":
    unittest.main()
