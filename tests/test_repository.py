import json
import os
import re
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
                "## Target users",
                "## Core loop",
                "## Module list",
                "## Module dependencies",
                "## Visual direction",
                "## Audio direction",
                "## Change history",
            ),
            "product-module.md.tmpl": (
                "## Module positioning",
                "## Functional flow",
                "## Data model",
                "## State machine (if applicable)",
                "## UI sketch",
                "## Audio entries",
                "## Numeric rules",
                "## Acceptance criteria",
                "## Edge cases",
                "## Change history",
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

    def test_core_methodology_is_english_and_preserves_normative_invariants(self):
        methodology = REPO_ROOT / "methodology"
        selected = {
            "00-overview.md": ("# 00 · Methodology overview", "Three non-negotiable constraints"),
            "01-product-doc-structure.md": (
                "# 01 · Product document structure",
                "Module filename rules",
            ),
            "02-feature-list-schema.md": (
                "# 02 · Feature-list three-file schema",
                "Hard constraints",
            ),
            "04-coding-rules-4-layers.md": (
                "# 04 · Four-layer Coding Rules architecture",
                "Layer 1: collaboration contract",
            ),
        }
        contents = {}
        for filename, required_text in selected.items():
            content = (methodology / filename).read_text(encoding="utf-8")
            contents[filename] = content
            with self.subTest(filename=filename):
                for text in required_text:
                    self.assertIn(text, content)

        combined = "\n".join(contents.values())
        for removed_heading in ("方法论总览", "文档结构规范", "三文件 schema", "四层结构"):
            with self.subTest(removed_heading=removed_heading):
                self.assertNotIn(removed_heading, combined)

        overview = contents["00-overview.md"]
        for invariant in (
            "product-change-standardizer",
            "explicit human acceptance",
            "Code smell scan: pass",
            "must_fix: 0",
            "verbatim relevant Coding Rules and source line numbers",
            "register every",
            "`_placeholder_` resource in the Feature notes",
            "delegate an independent fresh-context code-smell scan",
            "this hard gate must produce Feature-specific",
            "the commit must contain that exact evidence",
            "main` or `master",
            "force-push",
            "reset --hard",
        ):
            with self.subTest(overview_invariant=invariant):
                self.assertIn(invariant, overview)

        schema = contents["02-feature-list-schema.md"]
        for invariant in (
            "pending`, `in_progress`, `done`, `obsolete`, `obsolete_done`, or `blocked",
            "must not depend on a Feature whose numeric ID is greater",
            "Do not emit `large`",
            "explicit human acceptance",
            "zero remaining `must_fix` findings",
        ):
            with self.subTest(schema_invariant=invariant):
                self.assertIn(invariant, schema)
        for block in re.findall(r"```json\n(.*?)\n```", schema, flags=re.DOTALL):
            json.loads(block)

        coding_rules = contents["04-coding-rules-4-layers.md"]
        for invariant in (
            "A higher layer wins when rules conflict",
            "preferred organization for action logic",
            "trivial pure calculations",
            "explicit fallback or actionable error when a resource fails to load",
            "uses assertions to protect invariants",
            "@docs/coding-rules/engine-rules.md",
            "@docs/coding-rules/language-rules.md",
            "must disclose the deviation and reason",
        ):
            with self.subTest(coding_rules_invariant=invariant):
                self.assertIn(invariant, coding_rules)

    def test_core_methodology_relative_links_resolve(self):
        methodology = REPO_ROOT / "methodology"
        selected = (
            "00-overview.md",
            "01-product-doc-structure.md",
            "02-feature-list-schema.md",
            "04-coding-rules-4-layers.md",
        )
        for filename in selected:
            path = methodology / filename
            content = path.read_text(encoding="utf-8")
            for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", content):
                if target.startswith(("http://", "https://", "#")):
                    continue
                resolved = (path.parent / target.split("#", 1)[0]).resolve()
                with self.subTest(filename=filename, target=target):
                    self.assertTrue(resolved.exists(), f"Broken link: {path} -> {target}")

    def test_execution_spec_preserves_all_stages_and_completion_gates(self):
        execution = (REPO_ROOT / "methodology" / "03-execute-loop.md").read_text(
            encoding="utf-8"
        )

        self.assertIn("# 03 · The eight-stage execute-next-feature loop", execution)
        for stage in range(9):
            with self.subTest(stage=stage):
                self.assertRegex(execution, rf"(?m)^## Stage {stage}: ")

        required_invariants = (
            "Use the committed rule snapshot from Feature start",
            "=== Stage 0 exit report ===",
            "with verbatim text and line numbers",
            "Do not modify implementation files before the user approves",
            "run it synchronously",
            "An AI must never infer acceptance",
            "This stage is mandatory even for small or documentation-only Features",
            "Use a fresh-context sub-agent or equivalent independent context",
            "must_fix",
            "suggest",
            "acceptable",
            "If independent review fails, times out, returns invalid JSON",
            "do not introduce behavior changes after human acceptance",
            "repeat Stages 4 through 6 after the repair",
            "must not silently change accepted behavior",
            "Do not start the next Feature automatically unless the user has explicitly authorized",
            "reset --hard",
        )
        for invariant in required_invariants:
            with self.subTest(invariant=invariant):
                self.assertIn(invariant, execution)

        evidence = (
            "Code smell scan: pass (feature: F0XX, must_fix: 0, "
            "suggest: <N>, acceptable: <M>)"
        )
        self.assertGreaterEqual(execution.count(evidence), 2)
        for block in re.findall(r"```json\n(.*?)\n```", execution, flags=re.DOTALL):
            json.loads(block)

        target = REPO_ROOT / "methodology" / "02-feature-list-schema.md"
        self.assertTrue(target.exists())

    def test_coding_rules_template_preserves_four_layers_and_stable_evidence(self):
        template = (
            REPO_ROOT / "methodology" / "templates" / "coding_rules.md.tmpl"
        ).read_text(encoding="utf-8")

        for heading in (
            "# Part 1 · Collaboration contract",
            "# Part 2 · General design and architecture",
            "# Part 3 · Engine or platform practices",
            "# Part 4 · Programming-language practices",
        ):
            with self.subTest(heading=heading):
                self.assertIn(heading, template)

        collaboration = template.split("## 1.1 Collaboration discipline", 1)[1].split(
            "## 1.2 Workflow constraints", 1
        )[0]
        self.assertEqual(len(re.findall(r"(?m)^\d\. \*\*", collaboration)), 7)

        required_invariants = (
            "A higher layer wins when rules conflict",
            "A Feature that changes Yaya Loop workflow rules follows the committed rules",
            "verbatim relevant rules and line-number citations",
            "independent fresh-context code-smell scan",
            "Prefer a command object for logic that represents doing one thing",
            "three or more states",
            "Keep core rules pure.",
            "Keep core rules pure so they can be called and asserted without an engine or UI",
            "proactively apply the preferred pattern without asking for confirmation each time",
            "Provide a recognizable fallback resource or an actionable error",
            "Use assertions during development to protect invariants",
            "@docs/coding-rules/engine-rules.md",
            "@docs/coding-rules/language-rules.md",
        )
        for invariant in required_invariants:
            with self.subTest(invariant=invariant):
                self.assertIn(invariant, template)

        evidence = (
            "Code smell scan: pass (feature: F0XX, must_fix: 0, "
            "suggest: <N>, acceptable: <M>)"
        )
        self.assertIn(evidence, template)
        self.assertNotIn("core rules pure where practical", template)
        self.assertEqual(template.count("{{ENGINE_NAME}}"), 1)
        self.assertEqual(template.count("{{LANGUAGE_NAME}}"), 1)
        for removed_heading in ("协作契约", "通用设计模式", "引擎 / 平台最佳实践", "编程语言最佳实践"):
            with self.subTest(removed_heading=removed_heading):
                self.assertNotIn(removed_heading, template)

    def test_engine_rule_sources_have_no_han_and_preserve_stable_paths(self):
        engines = REPO_ROOT / "coding-rules-library" / "engines"
        expected_files = {
            "_stub-template.md",
            "backend-service.md",
            "godot.md",
            "unity.md",
            "unreal.md",
            "web-frontend.md",
        }
        self.assertEqual({path.name for path in engines.glob("*.md")}, expected_files)

        han_pattern = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff]")
        expected_headings = {
            "_stub-template.md": "# {{ENGINE_NAME}} best practices",
            "backend-service.md": "# Backend service best practices",
            "godot.md": "# Godot best practices",
            "unity.md": "# Unity best practices",
            "unreal.md": "# Unreal Engine best practices",
            "web-frontend.md": "# Web frontend best practices",
        }
        for path in engines.glob("*.md"):
            content = path.read_text(encoding="utf-8")
            with self.subTest(path=path.name):
                self.assertIsNone(han_pattern.search(content))
                self.assertTrue(content.startswith(expected_headings[path.name]))

        for filename in expected_files - {"godot.md"}:
            content = (engines / filename).read_text(encoding="utf-8")
            with self.subTest(stub=filename):
                self.assertIn("**Incomplete stub:**", content)
                self.assertIn("TODO:", content)

        godot = (engines / "godot.md").read_text(encoding="utf-8")
        self.assertNotIn("Incomplete stub", godot)
        self.assertNotIn("TODO:", godot)
        required_godot_rules = (
            "Godot 4.3 and later",
            "scenes are reusable objects",
            "Golden rule: call down, signal up",
            'get_node("../../SomeNode/SomeOtherNode")',
            "button.pressed.connect(_on_pressed)",
            "Emit the signal and return immediately",
            "a sender must not depend on whether anyone listened",
            "Appropriate Autoload uses",
            "read-only global configuration such as game constants or difficulty values",
            "One `.tres` file is one shared in-memory Resource",
            "Use `.tres` during development",
            "Use binary `.res` only for release or genuinely large resource data",
            "Local to Scene",
            'ResourceSaver.save(res, "user://save.tres")',
            "A Resource has no `_process`",
            "emit_changed()",
            "Use `@onready` only to resolve child-node references after the Scene tree is ready",
            "Never combine `@export` and `@onready`",
            "Recommended GDScript member order",
            "Put physics, movement, and collision in `_physics_process`",
            "Remove empty `_process` or `_physics_process` callbacks",
            "is_instance_valid(self)",
            "Godot 4 uses `instantiate()`, not Godot 3's `instance()`",
            "Destroy with `queue_free()`, not `free()`",
            'do not use `set_deferred("process_mode", ...)` to deactivate pooled objects',
            "MultiMeshInstance2D",
            "Rising Orphan Nodes",
            "Use `snake_case` for Scene files",
            "Use `PascalCase` for node names",
            "Godot anti-pattern checklist",
            "Remote Scene tree",
            "Play Current Scene, F6",
        )
        for rule in required_godot_rules:
            with self.subTest(godot_rule=rule):
                self.assertIn(rule, godot)

        bootstrap = (REPO_ROOT / "BOOTSTRAP.md").read_text(encoding="utf-8")
        self.assertIn("coding-rules-library/engines/<engine>.md", bootstrap)
        self.assertIn("coding-rules-library/engines/_stub-template.md", bootstrap)
        self.assertGreaterEqual(bootstrap.count("docs/coding-rules/engine-rules.md"), 3)


if __name__ == "__main__":
    unittest.main()
