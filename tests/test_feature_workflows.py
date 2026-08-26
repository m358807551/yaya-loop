import re
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
HAN_RE = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff]")


class FeatureWorkflowTests(unittest.TestCase):
    TITLE = "Generate Feature list"
    NATIVE = "claude-code/skills/generate-feature-list/SKILL.md"
    PORTABLE = "ai-agnostic-prompts/generate-feature-list.prompt.md"

    def read(self, relative_path):
        return (REPO_ROOT / relative_path).read_text(encoding="utf-8")

    def split_wrapper_and_body(self, text):
        match = re.search(rf"(?m)^# {re.escape(self.TITLE)}$", text)
        self.assertIsNotNone(match)
        return text[: match.start()], text[match.start() :]

    def body(self):
        native_wrapper, native_body = self.split_wrapper_and_body(self.read(self.NATIVE))
        portable_wrapper, portable_body = self.split_wrapper_and_body(
            self.read(self.PORTABLE)
        )
        self.assertEqual(native_body, portable_body)
        self.assertIsNone(HAN_RE.search(native_body))
        self.assertIsNotNone(HAN_RE.search(native_wrapper))
        self.assertIsNotNone(HAN_RE.search(portable_wrapper))
        return native_body

    def test_generation_pair_is_exact_and_language_aware(self):
        body = self.body()
        for invariant in (
            "docs/methodology-config.json",
            "missing, invalid, or migration-sensitive",
            "methodology/05-document-language.md",
            "Feature titles, descriptions, acceptance criteria",
            "human-readable `source` fragments",
            "meta notes",
            "Feature notes",
            "document_language: en",
            "document_language: zh-CN",
            "language of the user's current message",
            "JSON keys, enum values, Feature IDs",
        ):
            with self.subTest(invariant=invariant):
                self.assertIn(invariant, body)


class FeatureSyncWorkflowTests(unittest.TestCase):
    TITLE = "Synchronize Feature list"
    NATIVE = "claude-code/skills/sync-feature-list/SKILL.md"
    PORTABLE = "ai-agnostic-prompts/sync-feature-list.prompt.md"

    def read(self, relative_path):
        return (REPO_ROOT / relative_path).read_text(encoding="utf-8")

    def split_wrapper_and_body(self, text):
        match = re.search(rf"(?m)^# {re.escape(self.TITLE)}$", text)
        self.assertIsNotNone(match)
        return text[: match.start()], text[match.start() :]

    def body(self):
        native_wrapper, native_body = self.split_wrapper_and_body(self.read(self.NATIVE))
        portable_wrapper, portable_body = self.split_wrapper_and_body(
            self.read(self.PORTABLE)
        )
        self.assertEqual(native_body, portable_body)
        self.assertIsNone(HAN_RE.search(native_body))
        self.assertIsNotNone(HAN_RE.search(native_wrapper))
        self.assertIsNotNone(HAN_RE.search(portable_wrapper))
        return native_body

    def test_sync_pair_is_exact_language_aware_and_history_safe(self):
        body = self.body()
        for invariant in (
            "docs/methodology-config.json",
            "missing, invalid, or migration-sensitive",
            "language of the user's current message",
            "revision `user_intent`",
            "revision `summary`",
            "document_language: en",
            "document_language: zh-CN",
            "Do not translate or rewrite existing completed history",
            "Never modify a `done` Feature's `id`, `description`, or `acceptance_criteria`",
            "JSON keys, enum values, Feature IDs",
        ):
            with self.subTest(invariant=invariant):
                self.assertIn(invariant, body)

    def test_sync_preserves_all_stages_anchor_and_diff_analysis(self):
        body = self.body()
        positions = []
        for stage in range(7):
            marker = f"## Stage {stage}:"
            with self.subTest(stage=stage):
                self.assertIn(marker, body)
            positions.append(body.index(marker))
        self.assertEqual(positions, sorted(positions))
        for invariant in (
            "synced_at_commit",
            "most recent commit touching `docs/feature-list.json` or `docs/features/`",
            "whole-document comparison",
            "counts grouped by Feature status",
            "optional statement of the user's main intent",
            "git diff --stat -M <anchor> HEAD -- docs/product/",
            "git diff --name-status -M <anchor> HEAD -- docs/product/",
            "git diff -M HEAD -- docs/product/",
            "docs/coding_rules.md docs/coding-rules/",
            "Substantive addition",
            "Substantive revision",
            "Substantive removal",
            "Editorial adjustment",
            "Source-path corrections",
            "Match with user prior",
            "Decisions required",
            "Do not modify any file before Stage 3 confirmation",
        ):
            with self.subTest(invariant=invariant):
                self.assertIn(invariant, body)

    def test_sync_preserves_status_transitions_and_regression_rules(self):
        body = self.body()
        for invariant in (
            "next never-used ID after the highest historical ID",
            "Never reuse an ID",
            "Initialize `status` to `pending`",
            "Set index `status` to `obsolete`",
            "Set index `status` to `obsolete_done`",
            "append a localized timestamped removal reason",
            "append a new Feature that removes the implemented behavior",
            "Do not modify the original index entry or detail",
            "depends on the original ID",
            "require an explicit decision and append a new Feature",
            "including `done` history",
            "Record every old-to-new mapping in `source_path_updates`",
            "depend on that revision Feature",
            "record the confirmed dependent IDs",
        ):
            with self.subTest(invariant=invariant):
                self.assertIn(invariant, body)

    def test_sync_preserves_revision_validation_commit_and_handoff(self):
        body = self.body()
        for key in (
            '"revised_at"',
            '"synced_at_commit"',
            '"anchor_commit"',
            '"user_intent"',
            '"summary"',
            '"added"',
            '"obsoleted"',
            '"revised_via_new_feature"',
            '"source_path_updates"',
            '"depends_on_warnings"',
        ):
            with self.subTest(key=key):
                self.assertIn(key, body)
        for invariant in (
            '"docs/product/**/*.md"',
            "No Feature entry or detail file was physically deleted",
            "Index IDs and `docs/features/F*.json` filename stems match one to one",
            "No dependency points to `obsolete` or `obsolete_done`",
            "meta.total_features",
            "python3 -m json.tool",
            "git add docs/feature-list.json docs/feature-list-revisions.json docs/features/",
            "chore(sync): update feature-list per docs revision",
            "Source changes must be in a separate earlier commit",
            "Never push",
            "Do not automatically start another Feature",
        ):
            with self.subTest(invariant=invariant):
                self.assertIn(invariant, body)

    def test_sync_preserves_fail_safe_exception_and_git_boundaries(self):
        body = self.body()
        for invariant in (
            "More than about 50% of source lines changed",
            "more than three module files",
            "Diff and user prior conflict materially",
            "Product module inventory and actual files differ",
            "do not auto-repair the data",
            "do not run restore automatically",
            "Any Git command fails",
            "switching branches, stash, restore, or discarding changes",
            "`reset --hard`",
            "work on `main` or `master`",
        ):
            with self.subTest(invariant=invariant):
                self.assertIn(invariant, body)


class FeatureGenerationContractTests(unittest.TestCase):
    TITLE = "Generate Feature list"
    NATIVE = "claude-code/skills/generate-feature-list/SKILL.md"
    PORTABLE = "ai-agnostic-prompts/generate-feature-list.prompt.md"

    def read(self, relative_path):
        return (REPO_ROOT / relative_path).read_text(encoding="utf-8")

    def split_wrapper_and_body(self, text):
        match = re.search(rf"(?m)^# {re.escape(self.TITLE)}$", text)
        self.assertIsNotNone(match)
        return text[: match.start()], text[match.start() :]

    def body(self):
        _, native_body = self.split_wrapper_and_body(self.read(self.NATIVE))
        _, portable_body = self.split_wrapper_and_body(self.read(self.PORTABLE))
        self.assertEqual(native_body, portable_body)
        return native_body

    def test_generation_routing_and_replacement_boundary_are_preserved(self):
        body = self.body()
        for invariant in (
            "does not exist",
            "explicitly requests a complete replacement",
            "For every incremental Product change, use `sync-feature-list`",
            "wait for confirmation",
            "Never infer permission to discard an existing plan",
            "remove every stale `docs/features/F*.json`",
            "Resolve and report the exact files before removing them",
            "do not use an unresolved or broad destructive glob",
        ):
            with self.subTest(invariant=invariant):
                self.assertIn(invariant, body)

    def test_generation_inputs_and_decomposition_rules_are_preserved(self):
        body = self.body()
        for path in (
            "docs/product.md",
            "docs/product/NN-xxx.md",
            "docs/coding_rules.md",
            "docs/coding-rules/engine-rules.md",
            "docs/coding-rules/language-rules.md",
        ):
            with self.subTest(path=path):
                self.assertIn(path, body)
        self.assertIn("Read every relevant input before planning", body)
        self.assertIn("topological order", body)
        self.assertIn("stop and report the exact mismatch", body)
        for invariant in (
            "smallest independently verifiable complete behavior",
            "first Feature must establish runnable infrastructure",
            "depend only on earlier Feature IDs",
            "module A depends on module B",
            "data/presentation separation",
            "pure core rules",
            "any proposed `large` Feature must be split",
            "Include only behavior committed in Product",
            "observable acceptance",
            "Every committed module behavior and numeric rule",
            "Make `source` precise",
        ):
            with self.subTest(invariant=invariant):
                self.assertIn(invariant, body)

    def test_generation_schema_and_initial_values_are_stable(self):
        body = self.body()
        for path in (
            "docs/feature-list.json",
            "docs/features/F0XX.json",
            "docs/feature-list-revisions.json",
        ):
            with self.subTest(path=path):
                self.assertIn(path, body)
        for key in (
            '"generated_from"',
            '"generated_at"',
            '"total_features"',
            '"details_dir"',
            '"revisions_file"',
            '"id"',
            '"title"',
            '"status"',
            '"depends_on"',
            '"estimated_scope"',
            '"completed_at"',
            '"description"',
            '"acceptance_criteria"',
            '"source"',
            '"notes"',
            '"revision_log"',
        ):
            with self.subTest(key=key):
                self.assertIn(key, body)
        for stable_value in (
            "F001",
            "pending",
            "small",
            "medium",
            "in_progress",
            "done",
            "obsolete",
            "obsolete_done",
            "blocked",
            "infrastructure",
            "ISO 8601",
            "python3 -m json.tool <path> > /dev/null",
        ):
            with self.subTest(stable_value=stable_value):
                self.assertIn(stable_value, body)

    def test_generation_self_check_and_handoff_are_preserved(self):
        body = self.body()
        for invariant in (
            "No `depends_on` entry points to a later Feature ID",
            "No final `estimated_scope` is `large`",
            "Every referenced dependency ID exists",
            "set of index IDs equals the set",
            "Fix every failed check",
            "no more than six sentences",
            "If any question remains, stop and wait",
            "Do not write JSON",
            "write the index, every detail file, and the empty revision log together",
            "Do not implement or start the first Feature",
            "`execute-next-feature`",
        ):
            with self.subTest(invariant=invariant):
                self.assertIn(invariant, body)


if __name__ == "__main__":
    unittest.main()
