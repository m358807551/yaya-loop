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
