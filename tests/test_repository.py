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

    def test_language_rule_sources_have_no_han_and_preserve_stable_paths(self):
        languages = REPO_ROOT / "coding-rules-library" / "languages"
        expected_files = {
            "_stub-template.md",
            "csharp.md",
            "gdscript.md",
            "python.md",
            "rust.md",
            "typescript.md",
        }
        self.assertEqual({path.name for path in languages.glob("*.md")}, expected_files)

        han_pattern = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff]")
        expected_headings = {
            "_stub-template.md": "# {{LANGUAGE_NAME}} best practices",
            "csharp.md": "# C# best practices",
            "gdscript.md": "# GDScript best practices",
            "python.md": "# Python best practices",
            "rust.md": "# Rust best practices",
            "typescript.md": "# TypeScript best practices",
        }
        for path in languages.glob("*.md"):
            content = path.read_text(encoding="utf-8")
            with self.subTest(path=path.name):
                self.assertIsNone(han_pattern.search(content))
                self.assertTrue(content.startswith(expected_headings[path.name]))

        for filename in expected_files - {"gdscript.md"}:
            content = (languages / filename).read_text(encoding="utf-8")
            with self.subTest(stub=filename):
                self.assertIn("**Incomplete stub:**", content)
                self.assertIn("TODO:", content)

        required_stub_topics = {
            "_stub-template.md": (
                "{{LANGUAGE_VERSION}}",
                "Static typing and type checking",
                "Control flow and error handling",
                "Concurrency and asynchronous work",
                "Standard linting and formatting tools",
                "Anti-pattern checklist",
                "Community references",
            ),
            "csharp.md": (
                "C# 12 / .NET 8 and later",
                "nullable reference types",
                "CancellationToken",
                "IAsyncDisposable",
                "dotnet format",
                "async void",
                "Community references",
            ),
            "python.md": (
                "Python 3.11 and later",
                "type hints for every public API",
                "EAFP and LBYL",
                "asyncio, threading, and multiprocessing",
                "Prefer Ruff",
                "mutable defaults",
                "Community references",
            ),
            "rust.md": (
                "Rust 1.75 and later (Edition 2021)",
                "ownership, borrowing, and lifetimes",
                "Propagate `Result<T, E>`",
                "`Send + Sync` constraints",
                "cargo fmt --check",
                "pervasive `unwrap`",
                "Community references",
            ),
            "typescript.md": (
                "TypeScript 5.4 and later",
                "complete `strict` family",
                "discriminated unions",
                "`AbortController` for cancellation",
                "ESLint and Prettier",
                "unawaited Promises",
                "Community references",
            ),
        }
        for filename, topics in required_stub_topics.items():
            content = (languages / filename).read_text(encoding="utf-8")
            for topic in topics:
                with self.subTest(stub=filename, topic=topic):
                    self.assertIn(topic, content)

        required_stub_headings = {
            "_stub-template.md": (
                "Static typing and type checking",
                "Naming conventions",
                "Member order and code organization",
                "Control flow and error handling",
                "Collections and iteration",
                "Concurrency and asynchronous work",
                "Memory and lifetimes",
                "Documentation conventions",
                "Standard linting and formatting tools",
                "Anti-pattern checklist",
                "Community references",
            ),
            "csharp.md": (
                "Static typing and nullable references",
                "Naming conventions",
                "Member order",
                "Control flow and exceptions",
                "Collections and LINQ",
                "Asynchronous work and concurrency",
                "Memory and performance",
                "Documentation and XML comments",
                "Linting and formatting",
                "Anti-pattern checklist",
                "Community references",
            ),
            "python.md": (
                "Static typing and type hints",
                "Naming conventions",
                "Module organization",
                "Control flow and exceptions",
                "Collections and iteration",
                "Asynchronous work and concurrency",
                "Data classes and immutability",
                "Documentation and typing tools",
                "Linting and formatting",
                "Anti-pattern checklist",
                "Community references",
            ),
            "rust.md": (
                "Type system and ownership",
                "Naming conventions",
                "Project organization",
                "Error handling",
                "Collections and iteration",
                "Asynchronous work and concurrency",
                "Performance and memory",
                "Unsafe boundaries",
                "Documentation and tests",
                "Linting and formatting",
                "Anti-pattern checklist",
                "Community references",
            ),
            "typescript.md": (
                "Static typing and strict mode",
                "Naming conventions",
                "Module organization",
                "Control flow and error handling",
                "Collections and functional APIs",
                "Asynchronous work and concurrency",
                "Utility and advanced types",
                "Linting and formatting",
                "Anti-pattern checklist",
                "Community references",
            ),
        }
        for filename, headings in required_stub_headings.items():
            content = (languages / filename).read_text(encoding="utf-8")
            actual_headings = tuple(
                re.findall(r"(?m)^## \d+\. (.+)$", content)
            )
            with self.subTest(stub=filename):
                self.assertEqual(actual_headings, headings)

        required_stub_todos = {
            "_stub-template.md": (
                "TODO: Document the strength of this language's type system (static, gradual, or dynamic), whether strict mode must be enabled, and how generics should be used.",
                "TODO: Define casing for variables, functions, classes, constants, modules, and filenames, including conventions for Boolean values and function names.",
                "TODO: Define the standard order within a module, such as imports, constants, types, functions, and the main entry point. Distinguish official guidance from community convention.",
                "TODO: Define the error-handling model (exceptions, Result, or null), resource cleanup (finally, defer, context manager, or Drop), and the preference between guard clauses and a single exit.",
                "TODO: Document the standard collection types and their performance characteristics, mutation hazards during iteration, and the readability and performance boundaries for functional APIs such as map, filter, and reduce.",
                "TODO: Document the asynchronous model (async/await, goroutines, actors, or event loop), common deadlock and race hazards, and cancellation semantics.",
                "TODO: Explain garbage collection, manual management, or ownership; reference versus copy semantics; and common leak patterns.",
                "TODO: Define comment and documentation syntax, which APIs require documentation, and tool-recognized forms such as `///`, `\"\"\"`, `##`, JSDoc, or rustdoc.",
                "TODO: Identify the project's linter and formatter and the essential rule sets to enable.",
                "TODO: List common language-specific traps, such as mutable Python defaults, JavaScript `this` binding, or incorrect Rust lifetime alignment.",
            ),
            "csharp.md": (
                "TODO: Enable nullable reference types; define the boundaries for `?` and `!`; explain when to use `required`.",
                "TODO: Define the boundaries between PascalCase and camelCase; the `I` prefix for interfaces; the `Async` suffix for asynchronous methods; and `_camelCase` for private fields.",
                "TODO: Define the order of using directives, namespace declarations, classes, fields, constructors, properties, and methods, based on Microsoft's official guidance.",
                "TODO: Define exceptions versus a `Result<T, E>` pattern; guard clauses versus a single exit; and the use of `using`, using declarations, and `IAsyncDisposable`.",
                "TODO: Define when to expose `IEnumerable`, `IReadOnlyList`, `IList`, or `List`; set performance boundaries for LINQ, especially lazy chains on hot paths; and choose between `ToList` and `ToArray`.",
                "TODO: Require async/await through the full call chain; define where `ConfigureAwait(false)` belongs; propagate `CancellationToken`; and restrict `ValueTask` to justified cases.",
                "TODO: Define `struct` versus `class`; appropriate uses of `Span<T>`, `Memory<T>`, and `ArrayPool`; and string construction with interpolation or `StringBuilder`.",
                "TODO: Require `///` for public APIs and define minimum expectations for `<summary>`, `<param>`, and `<returns>`.",
                "TODO: Choose a baseline using `dotnet format`, EditorConfig, and Roslyn analyzers, and document the tradeoffs of StyleCop and SonarLint.",
                "TODO: Cover `async void`, broad `catch (Exception)`, structs larger than 16 bytes, mutable structs, and missing Dispose patterns.",
            ),
            "python.md": (
                "TODO: Require type hints for every public API; decide whether to use `from __future__ import annotations`; define when to use `TypeVar`, `ParamSpec`, and `Self`.",
                "TODO: Define snake_case for functions and variables, PascalCase for classes, CONSTANT_CASE for constants, lowercase module names, `_` for non-public names, and the narrow boundary for `__` name mangling.",
                "TODO: Define the role of `__init__.py` and re-exports; choose between relative and absolute imports; explain regular packages versus namespace packages.",
                "TODO: Define the preference for guard clauses; the boundary between EAFP and LBYL; a custom exception hierarchy; `finally` versus context managers; and appropriate use of the `else` clause on `try`.",
                "TODO: Choose among list, tuple, set, and dict; define when a comprehension remains readable and when to expand it into a loop; explain the memory benefit of generators; prohibit unsafe mutation during iteration.",
                "TODO: Define the boundaries among asyncio, threading, and multiprocessing; cover `async with` and `async for`; preserve task cancellation through `CancelledError`; account for the GIL when selecting concurrency.",
                "TODO: Choose among `dataclass`, `pydantic.BaseModel`, and `attrs`; define when to use `frozen=True`; justify uses of `__slots__`.",
                "TODO: Select one docstring style from Google, NumPy, or reStructuredText and define a baseline for mypy or pyright and Ruff.",
                "TODO: Prefer Ruff or define a justified flake8, isort, and Black stack; record enabled rule sets and CI integration.",
                "TODO: Cover mutable defaults such as `def f(x=[])`, wildcard imports, bare `except`, list mutation during iteration, dictionaries used as enums, and business logic in `__init__.py`.",
            ),
            "rust.md": (
                "TODO: Establish a practical model for ownership, borrowing, and lifetimes; identify when `Clone` is a design smell; define the boundary for `Copy`; prefer `From` and `TryFrom` over unjustified `as` casts.",
                "TODO: Define snake_case for functions and variables, PascalCase for types and traits, SCREAMING_SNAKE_CASE for constants, getters without a `get_` prefix, and constructors named `new`, `with_xxx`, or `try_new`.",
                "TODO: Define how crates, modules, and files correspond; choose between `mod.rs` and same-named module files; identify when to use a workspace; set a minimum bar for feature flags.",
                "TODO: Propagate `Result<T, E>` through the call chain and use `?`; define application and library error types; choose between thiserror and anyhow; restrict panic to documented invariant failures.",
                "TODO: Choose among `Vec`, `VecDeque`, `HashMap`, and `BTreeMap`; set readability boundaries for Iterator chains; document patterns such as `collect::<Result<_, _>>()`.",
                "TODO: Choose among Tokio, async-std, and smol; document `Send + Sync` constraints; select among mpsc, oneshot, and broadcast channels; define ownership and shutdown for spawned tasks.",
                "TODO: Choose among `Box`, `Rc`, and `Arc`; define appropriate uses of `Cow<'_, T>` and zero-copy `&str` or `&[u8]`; require evidence before adding `#[inline]`.",
                "TODO: Define legitimate reasons for unsafe code, minimize each unsafe block, and document common undefined-behavior hazards such as aliasing, lifetime extension, and uninitialized memory.",
                "TODO: Define `///` documentation and doctests, `#[cfg(test)]` modules, integration-test directory conventions, and cargo doc style.",
                "TODO: Define rustfmt configuration and the default and recommended Clippy lints; require CI to run `cargo fmt --check` and `cargo clippy -- -D warnings`.",
                "TODO: Cover pervasive `unwrap`, unnecessary `Clone` and `mut`, over-generalized types and `where` clauses, `Arc<Mutex<_>>` used instead of borrowing, and ignored lifetime warnings.",
            ),
            "typescript.md": (
                "TODO: Enable the complete `strict` family in tsconfig; define the boundaries among `any`, `unknown`, and `never`; treat unjustified `as` assertions as a warning sign.",
                "TODO: Define PascalCase for types, camelCase for variables and functions, and CONSTANT_CASE for constants; decide whether interfaces use an `I` prefix; define when to use `type` versus `interface`.",
                "TODO: Document the tradeoffs of barrel files such as `index.ts`; choose named or default exports; detect and prevent circular imports.",
                "TODO: Choose between exceptions and a Result pattern such as neverthrow or fp-ts; prefer guard clauses where they clarify flow; represent fallible returns with discriminated unions when appropriate.",
                "TODO: Set readability boundaries for array `map`, `filter`, and `reduce`; choose between `for...of` and `forEach`; define appropriate uses of Immer and `structuredClone` for immutable updates.",
                "TODO: Preserve async/await through the call chain; use `AbortController` for cancellation; define when to use `Promise.all`, `Promise.allSettled`, and `Promise.race`.",
                "TODO: Define appropriate uses of `Pick`, `Omit`, `Partial`, `Required`, and `Record`; limit conditional and mapped types when they harm readability; explain when `satisfies` is preferable to an annotation or assertion.",
                "TODO: Define an ESLint and Prettier baseline, select typescript-eslint strict rule sets, and establish import ordering.",
                "TODO: Cover pervasive `any`, `as` assertions that bypass the type system, empty catch blocks, unawaited Promises, and `Object.assign` used where object spread is clearer.",
            ),
        }
        for filename, todos in required_stub_todos.items():
            content = (languages / filename).read_text(encoding="utf-8")
            actual_todos = tuple(re.findall(r"(?m)^TODO: .+$", content))
            with self.subTest(stub=filename):
                self.assertEqual(actual_todos, todos)

        gdscript = (languages / "gdscript.md").read_text(encoding="utf-8")
        self.assertNotIn("Incomplete stub", gdscript)
        self.assertNotIn("TODO:", gdscript)
        required_gdscript_rules = (
            "GDScript 2.0",
            "Godot 4.3 and later",
            "Type every variable, parameter, and return value",
            "Untyped Declarations to Warning or Error",
            "28%–59% performance benefit",
            "Dictionary[String, ItemData]",
            "Nested generics support only one typed level",
            "A failed Object cast returns `null`",
            "A failed built-in type cast raises a runtime error",
            "A `.gd` filename must be the `snake_case` form of its `class_name`",
            "Start Booleans with `is_`, `has_`, `can_`, or `should_`",
            "Official GDScript member order",
            "Indent with tabs, not spaces",
            "directly reading or writing that property name accesses the underlying value and does not recurse",
            "this helper is not the setter itself",
            "Use `.emit()` in Godot 4",
            "Signal parameters should be statically typed whenever their types can be expressed",
            "Prefer Callable connections",
            "Invoke a lambda with `.call()`",
            "Closures capture values at creation time",
            "A lambda cannot be `static`",
            "use a direct `for` loop in per-frame or large-array hot paths",
            "GDScript has no try-catch",
            "Assertions are ignored in non-debug builds",
            "their conditions are not evaluated in release exports",
            "An assertion expression must never contain side effects",
            "There is no `throw`, `try`, `except`, or `finally` in GDScript",
            "Return `null` and require the caller to check it",
            "Use `is_instance_valid(node)`",
            "Default arrays and dictionaries to empty containers rather than `null`",
            "GDScript 4 uses `##` documentation comments",
            "Avoid scattered returns in the middle of a function",
            "Do not mutate a collection while iterating it",
            "GDScript uses Python-style `a if condition else b`",
            "Prefer ordinary `Array[T]`",
            "Static variables normally prevent their script Resource from unloading",
            "their values persist across Scene changes for the lifetime of the running process",
            "They reset when the application or script is actually reloaded",
            "Use an Autoload for explicit global ownership and lifecycle management",
            "serialized Resources or files for durable storage across application runs",
            "Node and Object `==` compares reference identity, not value equality",
            "Combining `@onready` and `@export` on one variable",
            "String-based `emit_signal(\"name\", args)`",
            "String-based `connect(\"signal\", self, \"method\")`",
            "`@warning_ignore(\"unused_variable\")` suppresses one warning temporarily",
        )
        for rule in required_gdscript_rules:
            with self.subTest(gdscript_rule=rule):
                self.assertIn(rule, gdscript)

        required_typed_examples = (
            "button.pressed.connect(func() -> void: print(\"clicked\"))",
            "func(a: Enemy, b: Enemy) -> bool",
            "func(enemy: Enemy) -> bool",
            "func(accumulator: int, enemy: Enemy) -> int",
            "var damages: Array[int] = []",
            "var items: Array[int] = []",
            "for index: int in range(",
        )
        for example in required_typed_examples:
            with self.subTest(typed_example=example):
                self.assertIn(example, gdscript)
        self.assertGreaterEqual(gdscript.count("for enemy: Enemy in"), 4)
        self.assertNotRegex(gdscript, r"(?m)^\s*for\s+\w+\s+in\s+")
        self.assertNotRegex(gdscript, r"func\([^)]*\)(?!\s*->)")
        self.assertNotIn(":= []", gdscript)
        self.assertNotIn(": Array =", gdscript)

        bootstrap = (REPO_ROOT / "BOOTSTRAP.md").read_text(encoding="utf-8")
        self.assertIn("coding-rules-library/engines/<engine>.md", bootstrap)
        self.assertIn("`languages/`", bootstrap)
        self.assertGreaterEqual(bootstrap.count("docs/coding-rules/language-rules.md"), 2)


if __name__ == "__main__":
    unittest.main()
