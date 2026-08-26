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

    def test_bootstrap_persists_document_language_before_product_generation(self):
        bootstrap = (REPO_ROOT / "BOOTSTRAP.md").read_text(encoding="utf-8")

        self.assertNotIn("用户主语言是中文", bootstrap)
        self.assertLess(
            bootstrap.index("## STEP 0.5: Resolve document language"),
            bootstrap.index("## STEP 2：按项目状态走不同分支"),
        )
        self.assertIn('"document_language": "<DOCUMENT_LANGUAGE>"', bootstrap)
        self.assertIn(
            "Do not translate, rename, or otherwise rewrite any existing Product",
            bootstrap,
        )
        self.assertIn(
            "必须保留已确认的 `document_language` 和所有未知字段",
            bootstrap,
        )
        self.assertNotIn("cat > docs/methodology-config.json", bootstrap)
        self.assertIn(
            "上面的对象只展示必需字段，不代表配置文件只允许包含这些字段",
            bootstrap,
        )
        self.assertIn(
            "A change in conversation language must never change the stored document language",
            bootstrap,
        )

    def test_templates_are_english_sources_with_language_aware_rendering(self):
        templates = REPO_ROOT / "methodology" / "templates"
        rendering_contract = (templates / "README.md").read_text(encoding="utf-8")

        self.assertIn("canonical English templates", rendering_contract)
        self.assertIn("Read `document_language`", rendering_contract)
        self.assertIn(
            "must not weaken, omit, merge, or reinterpret a required section",
            rendering_contract,
        )
        for stable_value in (
            "JSON keys",
            "Feature IDs",
            "_placeholder_",
            "must_fix",
            "Code smell scan: pass",
        ):
            with self.subTest(stable_value=stable_value):
                self.assertIn(stable_value, rendering_contract)

        expected_headings = {
            "product.md.tmpl": (
                "## One-line positioning",
                "## Core loop",
                "## Module list",
                "## Change history",
            ),
            "product-module.md.tmpl": (
                "## Module positioning",
                "## Functional flow",
                "## Acceptance criteria",
                "## Edge cases",
            ),
            "progress.md.tmpl": (
                "## Current work",
                "## Progress",
                "## Context notes",
                "## History",
            ),
        }
        for filename, headings in expected_headings.items():
            content = (templates / filename).read_text(encoding="utf-8")
            with self.subTest(filename=filename):
                for heading in headings:
                    self.assertIn(heading, content)

        feature_detail = json.loads(
            (templates / "feature-detail.json.tmpl").read_text(encoding="utf-8")
        )
        self.assertEqual(
            list(feature_detail),
            ["id", "description", "acceptance_criteria", "source", "notes"],
        )
        self.assertTrue(feature_detail["description"].startswith("In 2–4 sentences"))


if __name__ == "__main__":
    unittest.main()
