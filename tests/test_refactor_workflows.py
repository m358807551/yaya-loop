import re
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
HAN_RE = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff]")


class RefactorWorkflowTests(unittest.TestCase):
    TITLE = "Pick one refactor smell"
    NATIVE = "claude-code/skills/pick-refactor-smell/SKILL.md"
    PORTABLE = "ai-agnostic-prompts/pick-refactor-smell.prompt.md"

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
        canonical_prose = native_body
        for stable_marker in (
            "`代码气味`",
            "`重构`",
            "`未来`",
            "`推到`",
            "`出过 bug`",
            "`踩坑`",
            "`修了 N 次`",
        ):
            canonical_prose = canonical_prose.replace(stable_marker, "")
        self.assertIsNone(HAN_RE.search(canonical_prose))
        self.assertIsNotNone(HAN_RE.search(native_wrapper))
        self.assertIsNotNone(HAN_RE.search(portable_wrapper))
        return native_body

    def test_refactor_pair_is_exact_and_language_aware(self):
        body = self.body()
        for invariant in (
            "docs/methodology-config.json",
            "missing, invalid, or migration-sensitive",
            "language of the user's current message",
            "Preserve every extracted note excerpt verbatim",
            "Never translate or rewrite historical Feature notes",
            "writes no files",
            "durable Feature note, TODO, acceptance record, or Progress entry",
            "document_language: en",
            "document_language: zh-CN",
        ):
            with self.subTest(invariant=invariant):
                self.assertIn(invariant, body)

    def test_scan_markers_and_candidate_fields_are_preserved(self):
        body = self.body()
        for marker in (
            "`TODO`",
            "`suggest`",
            "`Code smell`",
            "`代码气味`",
            "`refactor`",
            "`重构`",
            "`future`",
            "`defer`",
            "`未来`",
            "`推到`",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, body)
        for invariant in (
            "Feature ID",
            "Feature title from the index",
            "verbatim excerpt of at most 200 characters",
            "code file paths named in the note",
            "If no candidate exists",
        ):
            with self.subTest(invariant=invariant):
                self.assertIn(invariant, body)

    def test_fixed_severity_rubric_and_ranking_are_preserved(self):
        body = self.body()
        for invariant in (
            "High severity — red",
            "at least three files",
            "caused a bug, pitfall, or repeated repair",
            "`出过 bug`",
            "`踩坑`",
            "`修了 N 次`",
            "blocks at least two pending Features",
            "Medium severity — yellow",
            "hardcoded constants or an SRP/DRY violation",
            "duplicated in two places",
            "one Boolean controlling two meanings",
            "Low severity — green",
            "style preferences",
            "resolved or superseded by a later Feature",
            "same-file accumulation",
            "apply it as a high-severity bonus",
            "Score multiple candidates from the same Feature independently",
        ):
            with self.subTest(invariant=invariant):
                self.assertIn(invariant, body)

    def test_report_selection_handoff_and_exceptions_are_preserved(self):
        body = self.body()
        for invariant in (
            "exactly one recommendation",
            "Number continuously across all three severity groups",
            "reason must compare the chosen candidate with alternatives",
            "Do not enter Plan mode, spawn an Explore agent, edit, or commit",
            "Requests complete notes for F0YY",
            "Re-run Stages 1–3 with X as the filter",
            "Do not invoke `generate-feature-list`, `sync-feature-list`, or `execute-next-feature`",
            "More than 15 candidates match",
            "top three medium candidates",
            "The user's selection is ambiguous",
        ):
            with self.subTest(invariant=invariant):
                self.assertIn(invariant, body)

    def test_portable_usage_guide_is_english_first_and_complete(self):
        guide = self.read("ai-agnostic-prompts/00-how-to-use.md")
        self.assertTrue(guide.startswith("# AI-agnostic prompts · usage guide"))
        self.assertIn("English commands and Chinese discovery examples", guide)
        self.assertIn("Concise Chinese trigger", guide)
        for prompt in (
            "product-init-elicitor.prompt.md",
            "product-change-standardizer.prompt.md",
            "product-spec-elicitor.prompt.md",
            "product-ui-sketcher.prompt.md",
            "product-audio-sketcher.prompt.md",
            "generate-feature-list.prompt.md",
            "sync-feature-list.prompt.md",
            "execute-next-feature.prompt.md",
            "pick-refactor-smell.prompt.md",
        ):
            with self.subTest(prompt=prompt):
                self.assertIn(f"](./{prompt})", guide)
        for command in (
            "Initialize this project from my Product idea.",
            "Generate the Feature list.",
            "Synchronize the Feature list.",
            "Do the next Feature.",
            "Pick one smell to refactor.",
            "从零初始化项目",
            "生成 feature-list",
            "同步 feature-list",
            "做下一个 feature",
            "挑一个坏味道重构",
        ):
            with self.subTest(command=command):
                self.assertIn(command, guide)
        self.assertIn("new independent session and return strict JSON", guide)
        self.assertIn("Do not weaken or remove Stage gates", guide)


if __name__ == "__main__":
    unittest.main()
