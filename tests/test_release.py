import json
import re
import unittest
from pathlib import Path
from urllib.parse import unquote


REPO_ROOT = Path(__file__).resolve().parents[1]
CURRENT_VERSION = "0.2.0"
HAN_TEXT = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff]")
MARKDOWN_LINK = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


class ReleaseV020Tests(unittest.TestCase):
    def read(self, relative_path):
        return (REPO_ROOT / relative_path).read_text(encoding="utf-8")

    def fixture(self, name):
        scenarios = self.read("methodology/06-document-language-smoke-scenarios.md")
        match = re.search(
            rf"<!-- fixture: {re.escape(name)} -->\n```json\n(.*?)\n```",
            scenarios,
            flags=re.DOTALL,
        )
        self.assertIsNotNone(match)
        return json.loads(match.group(1))

    def assert_relative_links_resolve(self, relative_path):
        source = REPO_ROOT / relative_path
        content = source.read_text(encoding="utf-8")
        for raw_target in MARKDOWN_LINK.findall(content):
            if raw_target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            target = unquote(raw_target.split("#", 1)[0])
            with self.subTest(source=relative_path, target=raw_target):
                self.assertTrue(
                    (source.parent / target).resolve().exists(),
                    f"Broken link in {relative_path}: {raw_target}",
                )

    def test_current_release_surfaces_report_v020(self):
        self.assertEqual(self.read("kit-version.txt").strip(), CURRENT_VERSION)
        self.assertIn(f"Current release: `v{CURRENT_VERSION}`", self.read("README.md"))
        self.assertIn(f"当前版本：`v{CURRENT_VERSION}`", self.read("README.zh-CN.md"))

        for relative_path in (
            "docs/methodology-config.json",
            "examples/greenfield-todo-app/docs/methodology-config.json",
        ):
            with self.subTest(relative_path=relative_path):
                config = json.loads(self.read(relative_path))
                self.assertEqual(config["kit_version"], CURRENT_VERSION)

        self.assertEqual(self.fixture("en")["config"]["kit_version"], CURRENT_VERSION)
        self.assertEqual(
            self.fixture("zh-CN")["config"]["kit_version"], CURRENT_VERSION
        )

    def test_legacy_fixtures_and_history_retain_v010(self):
        for name in ("legacy-before", "legacy-after"):
            with self.subTest(fixture=name):
                self.assertEqual(self.fixture(name)["kit_version"], "0.1.0")

        upgrade = self.read("upgrade-notes.md")
        product = self.read("docs/product.md")
        self.assertIn("## Upgrade from v0.1.0 to v0.2.0", upgrade)
        self.assertIn("### v0.1.0 · Initial release", upgrade)
        self.assertIn("v0.1.0 repository", product)

    def test_upgrade_guide_preserves_non_translating_migration_contract(self):
        upgrade = self.read("upgrade-notes.md")
        self.assertIsNone(HAN_TEXT.search(upgrade))
        for invariant in (
            "Present the apparent dominant Product language only as a proposal.",
            "Ask the maintainer to confirm a BCP 47 tag.",
            "Add only the confirmed `document_language` field with a JSON-aware edit.",
            "Preserve every existing and unknown field.",
            "Do not translate, rename, or rewrite existing Product, Feature, revision, Progress, or history content",
            "Editing the configuration field alone is not a supported language migration",
            "Do not overwrite a target project's filled `docs/coding_rules.md`",
            "Record v0.2.0 only after verification",
            "Do not use destructive Git operations or force-push",
        ):
            with self.subTest(invariant=invariant):
                self.assertIn(invariant, upgrade)

    def test_release_audit_maps_all_product_acceptance_criteria(self):
        product = self.read("docs/product/05-internationalization.md")
        product_overview = self.read("docs/product.md")
        audit = self.read("docs/release-audit-v0.2.0.md")
        self.assertIn(
            "| Internationalization | implemented |", product_overview
        )
        self.assertIn("Completed the v0.2.0 implementation", product)
        acceptance_section = product.split("## Acceptance criteria", 1)[1].split(
            "## Explicit non-goals", 1
        )[0]
        criteria = re.findall(r"(?m)^\d+\. ", acceptance_section)
        self.assertEqual(len(criteria), 8)

        audit_ids = re.findall(r"(?m)^\| I18N-AC(\d+) \|", audit)
        self.assertEqual(audit_ids, [str(number) for number in range(1, 9)])
        self.assertEqual(audit.count("| Pass |"), 8)
        for evidence in (
            "test_default_readme_is_english_with_bidirectional_language_links",
            "test_english_and_chinese_fixtures_preserve_stable_protocols",
            "test_smoke_scenarios_cover_verified_and_mismatched_languages",
            "test_native_and_portable_workflow_bodies_remain_identical",
            "test_legacy_fixture_adds_only_document_language",
            "test_bootstrap_and_contract_preserve_legacy_compatibility",
        ):
            with self.subTest(evidence=evidence):
                self.assertIn(evidence, audit)

    def test_release_audit_discloses_publication_and_support_boundaries(self):
        audit = self.read("docs/release-audit-v0.2.0.md")
        for boundary in (
            "Other well-formed BCP 47 values may be used only on a disclosed best-effort basis.",
            "automatic translation of an established project's Product",
            "a language migration performed by editing `document_language` alone",
            "guaranteed quality for every BCP 47 language",
            "does not create or push a Git tag",
            "Those external actions remain explicit maintainer operations",
        ):
            with self.subTest(boundary=boundary):
                self.assertIn(boundary, audit)

    def test_release_document_links_resolve(self):
        for relative_path in (
            "upgrade-notes.md",
            "docs/release-audit-v0.2.0.md",
            "methodology/05-document-language.md",
        ):
            self.assert_relative_links_resolve(relative_path)


if __name__ == "__main__":
    unittest.main()
