import json
import re
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = REPO_ROOT / "examples"
GREENFIELD_DOCS = EXAMPLES / "greenfield-todo-app" / "docs"
HAN_TEXT = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff]")


class ExampleProjectTests(unittest.TestCase):
    def test_greenfield_reference_uses_english_natural_language(self):
        sources = [
            GREENFIELD_DOCS / "product.md",
            GREENFIELD_DOCS / "product" / "01-tasks.md",
            GREENFIELD_DOCS / "coding_rules.md",
            GREENFIELD_DOCS / "progress.md",
            GREENFIELD_DOCS / "coding-rules" / "engine-rules.md",
            GREENFIELD_DOCS / "coding-rules" / "language-rules.md",
            GREENFIELD_DOCS / "feature-list.json",
            *sorted((GREENFIELD_DOCS / "features").glob("F*.json")),
        ]

        for path in sources:
            with self.subTest(path=path.relative_to(REPO_ROOT)):
                content = path.read_text(encoding="utf-8")
                self.assertIsNone(HAN_TEXT.search(content))

        product = sources[0].read_text(encoding="utf-8")
        module = sources[1].read_text(encoding="utf-8")
        coding_rules = sources[2].read_text(encoding="utf-8")
        for heading in (
            "## One-line positioning",
            "## Target users",
            "## Core loop",
            "## Module list",
            "## Module dependencies",
            "## Visual direction",
            "## Audio direction",
            "## Change history",
        ):
            self.assertIn(heading, product)
        for heading in (
            "## Module positioning",
            "## Functional flow",
            "## Data model",
            "## UI sketch",
            "## Numeric rules",
            "## Acceptance criteria",
            "## Edge cases",
            "## Change history",
        ):
            self.assertIn(heading, module)
        for invariant in (
            "An AI must never mark a Feature `done` by itself",
            "Stage 0 exit report",
            "Stage 6 code-smell scan",
            "must_fix: 0",
            "@docs/coding-rules/engine-rules.md",
            "@docs/coding-rules/language-rules.md",
        ):
            self.assertIn(invariant, coding_rules)

        for reference in re.findall(r"@([^\s]+\.md)", coding_rules):
            with self.subTest(reference=reference):
                self.assertTrue((GREENFIELD_DOCS.parent / reference).is_file())

        progress = (GREENFIELD_DOCS / "progress.md").read_text(encoding="utf-8")
        for invariant in (
            "F002 is the next eligible Feature",
            "F001 completed",
            "document_language`: `en",
            "Code smell scan: pass (feature: F001, must_fix: 0",
        ):
            self.assertIn(invariant, progress)

        config = json.loads(
            (GREENFIELD_DOCS / "methodology-config.json").read_text(encoding="utf-8")
        )
        self.assertEqual(
            config,
            {
                "document_language": "en",
                "static_check_cmd": "npm run typecheck && npm test",
                "engine": "web-frontend",
                "language": "typescript",
                "kit_version": "0.1.0",
                "bootstrap_at": "2026-05-25T10:00:00Z",
                "bootstrap_mode": "greenfield",
            },
        )

    def test_greenfield_feature_graph_and_sources_are_consistent(self):
        index = json.loads(
            (GREENFIELD_DOCS / "feature-list.json").read_text(encoding="utf-8")
        )
        features = index["features"]
        ids = [feature["id"] for feature in features]
        detail_paths = sorted((GREENFIELD_DOCS / "features").glob("F*.json"))

        self.assertEqual(ids, [path.stem for path in detail_paths])
        self.assertEqual(index["meta"]["total_features"], len(features))
        self.assertEqual(len(ids), len(set(ids)))

        seen = set()
        for summary, detail_path in zip(features, detail_paths):
            with self.subTest(feature=summary["id"]):
                detail = json.loads(detail_path.read_text(encoding="utf-8"))
                self.assertEqual(summary["id"], detail["id"])
                self.assertIn(summary["estimated_scope"], {"small", "medium"})
                self.assertTrue(set(summary["depends_on"]).issubset(seen))
                self.assertTrue(detail["description"].strip())
                self.assertTrue(detail["acceptance_criteria"])

                source = detail["source"]
                if source != "infrastructure":
                    relative_path, anchor = source.split("#", 1)
                    source_path = GREENFIELD_DOCS / relative_path
                    self.assertTrue(source_path.is_file())
                    source_text = source_path.read_text(encoding="utf-8").lower()
                    self.assertIn(f"## {anchor.replace('-', ' ')}", source_text)
                seen.add(summary["id"])

    def test_legacy_walkthrough_is_complete_natural_english(self):
        path = EXAMPLES / "legacy-import-walkthrough.md"
        content = path.read_text(encoding="utf-8")

        self.assertIsNone(HAN_TEXT.search(content))
        for inferred_heading in (
            "## One-line positioning [REVERSE-ENGINEERED]",
            "## Target users [REVERSE-ENGINEERED]",
            "## Core loop [REVERSE-ENGINEERED]",
            "## Module list [REVERSE-ENGINEERED]",
            "## Module dependencies [REVERSE-ENGINEERED]",
            "## Visual direction [REVERSE-ENGINEERED]",
            "## Audio direction [REVERSE-ENGINEERED]",
        ):
            self.assertIn(inferred_heading, content)
        required_flow = (
            "## Step 0 · Detect the project state",
            "## Step 1 · Resolve the agent and document language",
            "## Step 2 · Reverse-engineer the existing system",
            "### 2.3 Draft the Product overview",
            "### 2.5 Reconstruct a bounded Feature history",
            "## Visual direction [REVERSE-ENGINEERED]",
            "## Audio direction [REVERSE-ENGINEERED]",
            "## Step 3 · Create project-specific Coding Rules",
            "## Step 4 · Initialize Progress and handoff state",
            "## Steps 5–6 · Install the integration and run smoke checks",
            '"document_language": "en"',
            "[REVERSE-ENGINEERED]",
            "docs/feature-list.json",
            "docs/features/F0XX.json",
            "static_check_cmd",
            "does not automatically start F016",
            "product/03-customers.md#data-model",
            "product/02-inventory.md#inventory-allocation",
            "Implemented before bootstrap; reverse-engineered from code at commit `<anchor>`",
        )
        for expected in required_flow:
            with self.subTest(expected=expected):
                self.assertIn(expected, content)

    def test_examples_do_not_duplicate_workflow_source_trees(self):
        forbidden_directory_names = {
            "methodology",
            "claude-code",
            "ai-agnostic-prompts",
            "coding-rules-library",
            "git-hooks",
        }
        duplicated = [
            path.relative_to(EXAMPLES)
            for path in EXAMPLES.rglob("*")
            if path.is_dir() and path.name in forbidden_directory_names
        ]
        self.assertEqual(duplicated, [])


if __name__ == "__main__":
    unittest.main()
