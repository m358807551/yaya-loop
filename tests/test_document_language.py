import json
import re
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SMOKE_SCENARIOS = (
    REPO_ROOT / "methodology" / "06-document-language-smoke-scenarios.md"
)
HAN_TEXT = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff]")


class DocumentLanguageCompatibilityTests(unittest.TestCase):
    WORKFLOW_PAIRS = {
        "execute-next-feature": "Execute one Feature",
        "generate-feature-list": "Generate Feature list",
        "pick-refactor-smell": "Pick one refactor smell",
        "product-audio-sketcher": "Product audio sketcher",
        "product-change-standardizer": "Product change standardizer",
        "product-init-elicitor": "Product initialization elicitor",
        "product-spec-elicitor": "Product specification elicitor",
        "product-ui-sketcher": "Product UI sketcher",
        "sync-feature-list": "Synchronize Feature list",
    }

    @classmethod
    def setUpClass(cls):
        cls.scenarios = SMOKE_SCENARIOS.read_text(encoding="utf-8")

    def fixture(self, name):
        match = re.search(
            rf"<!-- fixture: {re.escape(name)} -->\n```json\n(.*?)\n```",
            self.scenarios,
            flags=re.DOTALL,
        )
        self.assertIsNotNone(match, f"missing fixture: {name}")
        return json.loads(match.group(1))

    def test_english_and_chinese_fixtures_preserve_stable_protocols(self):
        english = self.fixture("en")
        chinese = self.fixture("zh-CN")

        self.assertEqual(list(english), ["config", "feature", "detail", "protocol"])
        self.assertEqual(list(english), list(chinese))

        self.assertEqual(list(english["config"]), list(chinese["config"]))
        self.assertEqual(
            list(english["config"]),
            [
                "document_language",
                "static_check_cmd",
                "engine",
                "language",
                "kit_version",
                "bootstrap_at",
                "bootstrap_mode",
            ],
        )
        self.assertEqual(english["config"]["document_language"], "en")
        self.assertEqual(chinese["config"]["document_language"], "zh-CN")
        for key in english["config"]:
            if key != "document_language":
                self.assertEqual(english["config"][key], chinese["config"][key])

        self.assertEqual(list(english["feature"]), list(chinese["feature"]))
        for key in english["feature"]:
            if key != "title":
                self.assertEqual(english["feature"][key], chinese["feature"][key])
        self.assertEqual(english["feature"]["status"], "pending")
        self.assertEqual(english["feature"]["estimated_scope"], "small")

        self.assertEqual(list(english["detail"]), list(chinese["detail"]))
        for key in ("id", "source"):
            self.assertEqual(english["detail"][key], chinese["detail"][key])
        for key in ("description", "acceptance_criteria", "notes"):
            self.assertNotEqual(english["detail"][key], chinese["detail"][key])

        self.assertEqual(english["protocol"], chinese["protocol"])
        self.assertEqual(english["protocol"]["detail_path"], "docs/features/F900.json")
        self.assertTrue(english["protocol"]["placeholder"].startswith("_placeholder_"))
        self.assertEqual(
            english["protocol"]["completion_evidence"],
            "Code smell scan: pass (feature: F900, must_fix: 0, suggest: 0, acceptable: 0)",
        )

        english_prose = json.dumps(english, ensure_ascii=False)
        chinese_prose = json.dumps(chinese, ensure_ascii=False)
        self.assertIsNone(HAN_TEXT.search(english_prose))
        self.assertIsNotNone(HAN_TEXT.search(chinese_prose))

    def test_legacy_fixture_adds_only_document_language(self):
        before = self.fixture("legacy-before")
        after = self.fixture("legacy-after")

        self.assertNotIn("document_language", before)
        self.assertEqual(after["document_language"], "en")
        self.assertEqual(
            {key: value for key, value in after.items() if key != "document_language"},
            before,
        )
        self.assertEqual(after["team_policy"], "preserve-me")
        self.assertEqual(after["language"], "python")

    def test_smoke_scenarios_cover_verified_and_mismatched_languages(self):
        for scenario in (
            "Scenario DL-01 · English conversation and English documents",
            "Scenario DL-02 · Chinese conversation and Simplified Chinese documents",
            "Scenario DL-03 · Chinese conversation and English documents",
            "Scenario DL-04 · Legacy configuration without document_language",
        ):
            with self.subTest(scenario=scenario):
                self.assertIn(scenario, self.scenarios)

        for invariant in (
            "The stored `document_language` remains `en`.",
            "Do not change `document_language` to `zh-CN` because the conversation changed.",
            "Only `document_language` is added; every existing and unknown configuration field is preserved.",
            "Existing Chinese Product and completed Feature history remains unchanged.",
            "Do not silently choose `zh-CN`",
            "Do not create localized Methodology, Skill, Prompt, template, Coding Rules library, or Hook trees.",
            "without additional runtime dependencies",
        ):
            with self.subTest(invariant=invariant):
                self.assertIn(invariant, self.scenarios)

    def test_bootstrap_and_contract_preserve_legacy_compatibility(self):
        bootstrap = (REPO_ROOT / "BOOTSTRAP.md").read_text(encoding="utf-8")
        contract = (
            REPO_ROOT / "methodology" / "05-document-language.md"
        ).read_text(encoding="utf-8")

        for invariant in (
            "add or replace only `document_language` and preserve every other field",
            "A change in conversation language must never change the stored document language",
            "Initially verified document languages are `en` and `zh-CN`",
            "underscore forms such as `zh_CN` are invalid",
            "Do not translate, rename, or otherwise rewrite any existing Product",
            "必须保留已确认的 `document_language` 和所有未知字段",
            "do not edit the field merely because the conversation language changed",
        ):
            with self.subTest(bootstrap_invariant=invariant):
                self.assertIn(invariant, bootstrap)

        for invariant in (
            "Present that language only as a non-binding migration proposal",
            "Persist the confirmed tag without translating existing files",
            "Historical completed Features and revision records may remain in their original language",
            "Support claims in public documentation must not exceed behavior covered",
            "06-document-language-smoke-scenarios.md",
        ):
            with self.subTest(contract_invariant=invariant):
                self.assertIn(invariant, contract)

        smoke_link = REPO_ROOT / "methodology" / "06-document-language-smoke-scenarios.md"
        self.assertTrue(smoke_link.is_file())

    def test_native_and_portable_workflow_bodies_remain_identical(self):
        for slug, title in self.WORKFLOW_PAIRS.items():
            native = (
                REPO_ROOT / "claude-code" / "skills" / slug / "SKILL.md"
            ).read_text(encoding="utf-8")
            portable = (
                REPO_ROOT / "ai-agnostic-prompts" / f"{slug}.prompt.md"
            ).read_text(encoding="utf-8")
            heading = f"# {title}"
            native_match = re.search(rf"(?m)^{re.escape(heading)}$", native)
            portable_match = re.search(rf"(?m)^{re.escape(heading)}$", portable)
            with self.subTest(workflow=slug):
                self.assertIsNotNone(native_match)
                self.assertIsNotNone(portable_match)
                native_start = native_match.start()
                portable_start = portable_match.start()
                self.assertEqual(native[native_start:], portable[portable_start:])
                self.assertIn("document_language", native[native_start:])


if __name__ == "__main__":
    unittest.main()
