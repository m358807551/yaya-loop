import os
import re
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
HAN_RE = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff]")


class InstallationGuidanceTests(unittest.TestCase):
    def read(self, relative_path):
        return (REPO_ROOT / relative_path).read_text(encoding="utf-8")

    def test_claude_install_guide_is_complete_english(self):
        guide = self.read("claude-code/install.md")
        self.assertTrue(guide.startswith("# Claude Code installation"))
        self.assertIsNone(HAN_RE.search(guide))
        for command in (
            "mkdir -p .claude/skills .claude/hooks",
            "cp -r ~/code/yaya-loop/claude-code/skills/* .claude/skills/",
            "cp ~/code/yaya-loop/claude-code/hooks/*.py .claude/hooks/",
            "chmod +x .claude/hooks/*.py",
            "cp ~/code/yaya-loop/claude-code/settings.example.json .claude/settings.json",
        ):
            with self.subTest(command=command):
                self.assertIn(command, guide)
        for name in (
            "execute-next-feature",
            "generate-feature-list",
            "sync-feature-list",
            "pick-refactor-smell",
            "product-init-elicitor",
            "product-change-standardizer",
            "product-spec-elicitor",
            "product-ui-sketcher",
            "product-audio-sketcher",
            "gate-feature-done.py",
            "check-feature-list.py",
        ):
            with self.subTest(name=name):
                self.assertIn(name, guide)
        self.assertIn("merge the hooks object", guide)
        self.assertIn("instead of overwriting project settings", guide)
        self.assertIn("upgrade-notes.md", guide)

    def test_git_hook_install_guide_is_complete_english(self):
        guide = self.read("git-hooks/install.md")
        self.assertTrue(guide.startswith("# Git Hook installation for non-Claude agents"))
        self.assertIsNone(HAN_RE.search(guide))
        for invariant in (
            "cp ~/code/yaya-loop/git-hooks/commit-msg .git/hooks/commit-msg",
            "chmod +x .git/hooks/commit-msg",
            "pending` or `in_progress` to `done`",
            "Code smell scan: pass (feature: F001, must_fix: 0, suggest: 0, acceptable: 0)",
            "git commit --no-verify",
            "Python 3 and Git",
            "macOS, Linux, and WSL",
            "PR and CI integration",
        ):
            with self.subTest(invariant=invariant):
                self.assertIn(invariant, guide)

    def test_hook_sources_are_english_executable_and_syntactically_valid(self):
        paths = (
            "claude-code/hooks/gate-feature-done.py",
            "claude-code/hooks/check-feature-list.py",
            "git-hooks/commit-msg",
        )
        for relative_path in paths:
            path = REPO_ROOT / relative_path
            source = path.read_text(encoding="utf-8")
            with self.subTest(path=relative_path):
                self.assertIsNone(HAN_RE.search(source))
                self.assertTrue(os.access(path, os.X_OK))
                compile(source, str(path), "exec")

    def test_hook_evidence_and_failure_contracts_remain_stable(self):
        gate = self.read("claude-code/hooks/gate-feature-done.py")
        commit_hook = self.read("git-hooks/commit-msg")
        checker = self.read("claude-code/hooks/check-feature-list.py")
        for source in (gate, commit_hook):
            with self.subTest(source=source[:40]):
                self.assertIn(r"feature:\s*(F\d+)", source)
                self.assertIn(r"must_fix:\s*0", source)
                self.assertIn(r"suggest:\s*\d+", source)
                self.assertIn(r"acceptable:\s*\d+", source)
                self.assertIn("re.IGNORECASE | re.MULTILINE", source)
                self.assertIn(
                    "Code smell scan: pass (feature: F0XX, must_fix: 0, suggest: N, acceptable: M)",
                    source,
                )
        self.assertIn("sys.exit(2)", gate)
        self.assertIn("return 1", commit_hook)
        self.assertIn("return 0", commit_hook)
        self.assertIn("return 2", checker)
        self.assertIn("return True", checker)
        self.assertIn("WARNING: index references ids without detail files", checker)
        self.assertIn("language-appropriate typographic quotation marks", checker)


if __name__ == "__main__":
    unittest.main()
