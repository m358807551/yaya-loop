import re
import unittest
from pathlib import Path
from urllib.parse import unquote


REPO_ROOT = Path(__file__).resolve().parents[1]
ENGLISH_README = REPO_ROOT / "README.md"
CHINESE_README = REPO_ROOT / "README.zh-CN.md"
HAN_TEXT = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff]")
MARKDOWN_LINK = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


class ReadmeInternationalizationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.english = ENGLISH_README.read_text(encoding="utf-8")
        cls.chinese = CHINESE_README.read_text(encoding="utf-8")

    def test_default_readme_is_english_with_bidirectional_language_links(self):
        self.assertTrue(
            self.english.startswith(
                "# Yaya Loop\n\n**English** | [简体中文](./README.zh-CN.md)"
            )
        )
        self.assertTrue(
            self.chinese.startswith(
                "# Yaya Loop\n\n[English](./README.md) | **简体中文**"
            )
        )
        english_without_language_label = self.english.replace("简体中文", "")
        self.assertIsNone(HAN_TEXT.search(english_without_language_label))
        self.assertIsNotNone(HAN_TEXT.search(self.chinese))

    def test_both_readmes_cover_the_complete_product_story(self):
        semantic_pairs = (
            (
                "After dozens or hundreds of Features, is the project still maintainable?",
                "连续开发几十个、几百个 Feature 之后，项目还能不能继续维护？",
            ),
            ("Product → Feature → Implement", "Product → Feature → Implement"),
            ("**Explicit human acceptance is required**", "**必须经过人工验收**"),
            (
                "must run in a fresh-context agent or an equivalent independent context",
                "必须由 fresh-context Agent 或等价的独立上下文执行",
            ),
            (
                "If independent review is unavailable, the Feature cannot be completed.",
                "如果无法完成独立审查，这个 Feature 就不能完成。",
            ),
            ("`must_fix`", "`must_fix`"),
            ("**600+ Features**", "**600+ 个 Feature**"),
            ("**2,000+ Git commits**", "**2000+ 个 Git Commit**"),
            ("## What does day-to-day development look like?", "## Q：用了它以后，我每天到底怎么开发？"),
            ("# How do I get started?", "# Q：我要怎么开始使用？"),
            ("### Greenfield", "### Greenfield"),
            ("### Legacy", "### Legacy"),
            (
                "a bounded set of representative completed Features",
                "一组有上限、具有代表性的已完成 Feature",
            ),
            (
                "future work confirmed by the user",
                "只有经用户明确确认才会加入的后续 pending Feature",
            ),
            ("### It is not a project-management tool", "### 它不是项目管理工具"),
            ("### It is not CI/CD", "### 它不是 CI/CD"),
            ("### It is not a code-generation model", "### 它不是代码生成模型"),
            ("### It is not a silver bullet", "### 它也不是银弹"),
            ("`document_language`", "`document_language`"),
            ("Stages 0–8", "Stage 0–8"),
            ("### Product", "### Product"),
            ("### Generate", "### Generate"),
            ("### Execute", "### Execute"),
            ("[`BOOTSTRAP.md`](./BOOTSTRAP.md)", "[`BOOTSTRAP.md`](./BOOTSTRAP.md)"),
            ("[MIT License](./LICENSE)", "[MIT License](./LICENSE)"),
        )
        for english_text, chinese_text in semantic_pairs:
            with self.subTest(english=english_text, chinese=chinese_text):
                self.assertIn(english_text, self.english)
                self.assertIn(chinese_text, self.chinese)

        self.assertIn(
            "Rules for other languages and stacks are still being expanded.",
            self.english,
        )
        self.assertIn("其他语言和技术栈的规则仍在持续补充。", self.chinese)

    def test_repository_relative_links_resolve_in_both_readmes(self):
        for readme, content in (
            (ENGLISH_README, self.english),
            (CHINESE_README, self.chinese),
        ):
            for raw_target in MARKDOWN_LINK.findall(content):
                if raw_target.startswith(("http://", "https://", "mailto:", "#")):
                    continue
                target = unquote(raw_target.split("#", 1)[0])
                resolved = (readme.parent / target).resolve()
                with self.subTest(readme=readme.name, target=raw_target):
                    self.assertTrue(
                        resolved.exists(),
                        f"Broken relative link in {readme.name}: {raw_target}",
                    )

    def test_readmes_do_not_contain_conversation_urls(self):
        for readme, content in (
            (ENGLISH_README, self.english),
            (CHINESE_README, self.chinese),
        ):
            with self.subTest(readme=readme.name):
                self.assertNotIn("chatgpt.com/c/", content)


if __name__ == "__main__":
    unittest.main()
