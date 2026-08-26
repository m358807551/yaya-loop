import re
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
HAN_RE = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff]")


class ExecutionWorkflowTests(unittest.TestCase):
    TITLE = "Execute one Feature"
    NATIVE = "claude-code/skills/execute-next-feature/SKILL.md"
    PORTABLE = "ai-agnostic-prompts/execute-next-feature.prompt.md"

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

    def test_execution_pair_is_exact_and_language_aware(self):
        body = self.body()
        for invariant in (
            "docs/methodology-config.json",
            "missing, invalid, or migration-sensitive",
            "language of the user's current message",
            "Feature notes, Progress entries and history, acceptance records, TODOs, and handoff state",
            "document_language: en",
            "document_language: zh-CN",
            "committed workflow and Coding Rules snapshot",
            "those changes govern the next Feature",
            "JSON keys, enum values, Feature IDs",
        ):
            with self.subTest(invariant=invariant):
                self.assertIn(invariant, body)

    def test_execution_preserves_all_ordered_stage_gates(self):
        body = self.body()
        positions = []
        expected = {
            0: "preflight and exit report",
            1: "resource and dependency preflight",
            2: "mark work started",
            3: "implement",
            4: "self-verification",
            5: "human acceptance",
            6: "fresh-context code-smell scan",
            7: "mark complete",
            8: "handoff",
        }
        for stage, title in expected.items():
            marker = f"## Stage {stage}: {title}"
            with self.subTest(stage=stage):
                self.assertIn(marker, body)
            positions.append(body.index(marker))
        self.assertEqual(positions, sorted(positions))

    def test_stage_zero_and_one_preserve_selection_context_and_approval(self):
        body = self.body()
        for invariant in (
            "route to `generate-feature-list`",
            "If any Feature is `in_progress`",
            "first `pending` Feature whose dependencies are all `done`",
            "`estimated_scope` is `large`",
            "require decomposition through `sync-feature-list`",
            "git status",
            "git branch --show-current",
            "commit, stash, or restore",
            "do not continue Stage 0 until the dirty state and the user's choice are resolved",
            "selected `docs/features/F0XX.json` in full",
            "the `notes` of every completed dependency Feature",
            "=== Stage 0 exit report ===",
            "verbatim text and line numbers",
            "Do not enter Stage 1 before emitting this report",
            "image, audio file, font, configuration dataset, third-party dependency",
            "`_placeholder_` recorded in notes",
            "wait for explicit approval",
            "Do not modify implementation files before approval",
        ):
            with self.subTest(invariant=invariant):
                self.assertIn(invariant, body)

    def test_implementation_and_verification_contracts_are_preserved(self):
        body = self.body()
        for invariant in (
            "Change only the index status to `in_progress`",
            "Archive prior Current work and Progress",
            "preserve Context notes",
            "A `chore(F0XX): start feature` commit is optional",
            "Append a Progress entry after every meaningful substep",
            "<type>(F0XX): <imperative summary>",
            "`feat`, `fix`, `refactor`, `test`, `docs`, and `chore`",
            "stage explicit paths rather than `git add .` or `git add -A`",
            "Read and synchronously run `static_check_cmd`",
            "never treat a background process as completed verification",
            "On any automated failure, return to Stage 3",
            "Automated evidence never replaces human acceptance",
            "Never infer acceptance from tests or confidence",
        ):
            with self.subTest(invariant=invariant):
                self.assertIn(invariant, body)

    def test_independent_review_and_completion_evidence_are_preserved(self):
        body = self.body()
        for smell in (
            "files longer than roughly 300 lines",
            "duplicated knowledge or rules",
            "type dispatch owned by the wrong component",
            "magic numbers or strings",
            "constants/enums duplicated across three or more files",
            "God Object growth",
            "engine/language anti-patterns",
            "presentation/domain coupling",
            "comments that restate what rather than why",
            "defect needing two or more repair attempts",
        ):
            with self.subTest(smell=smell):
                self.assertIn(smell, body)
        for invariant in (
            '"must_fix"',
            '"suggest"',
            '"acceptable"',
            '"rule_ref"',
            '"fix_suggestion"',
            "make no edits or Git writes",
            "cannot delegate to a sub-agent",
            "open a new independent session",
            "main implementation context must never substitute",
            "Re-scan until `must_fix` is empty",
            "independent focused `refactor(F0XX): <summary>` commit for each finding",
            "must not silently change accepted behavior",
            "Append each `suggest` to Feature notes with a `TODO` prefix",
            "Code smell scan: pass (feature: F0XX, must_fix: 0, suggest: <N>, acceptable: <M>)",
            "If review fails, times out, returns invalid JSON, or cannot read rules, stop",
            "Even when all three arrays are empty, emit the report and final evidence line",
            "Do not continue while the post-repair `static_check_cmd` is failing",
            "Remain in Stage 6, repair the failure, rerun verification, and re-scan",
            "Acceptance criteria all verified by human review.",
        ):
            with self.subTest(invariant=invariant):
                self.assertIn(invariant, body)

    def test_completion_handoff_git_and_exception_boundaries_are_preserved(self):
        body = self.body()
        for invariant in (
            "Set index `status` to `done`",
            "`completed_at` to the current ISO 8601 timestamp",
            "Archive Current work and Progress under History",
            "chore(F0XX): mark feature as done",
            "Do not push, switch branches, merge",
            "first `pending` Feature whose dependencies are all `done`",
            "Start the next Feature only when the user has explicitly authorized continuation",
            "merge, rebase, or cherry-pick",
            "force push",
            "`reset --hard`",
            "direct `.git/` edits",
            "Propose revision through `sync-feature-list`",
            "Implementation needs out-of-scope files",
            "Persist current state in Progress",
            "unrelated work mid-Feature",
        ):
            with self.subTest(invariant=invariant):
                self.assertIn(invariant, body)


if __name__ == "__main__":
    unittest.main()
