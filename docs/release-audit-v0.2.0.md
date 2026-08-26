# Yaya Loop v0.2.0 release audit

## Release decision

v0.2.0 is the initial international project-knowledge release. It keeps one canonical English source for executable workflows, provides complete English and Simplified Chinese repository entry points, and makes durable target-project prose follow a confirmed `document_language` without translating stable machine protocols.

This audit maps every acceptance criterion in [`product/05-internationalization.md`](./product/05-internationalization.md) to repository evidence. It does not treat unsupported behavior as implemented.

## Product acceptance evidence

| ID | Product acceptance criterion | Verification evidence | Result |
| --- | --- | --- | --- |
| I18N-AC1 | The repository defaults to a complete English README; the complete Simplified Chinese README links back. | `tests/test_readmes.py`: `test_default_readme_is_english_with_bidirectional_language_links`, `test_both_readmes_cover_the_complete_product_story`, and relative-link checks. | Pass |
| I18N-AC2 | A newly initialized English project produces English Product and Feature prose. | [`../methodology/06-document-language-smoke-scenarios.md`](../methodology/06-document-language-smoke-scenarios.md) DL-01 and the `en` fixture; `tests/test_document_language.py`: stable-protocol and scenario coverage tests; the English Greenfield reference under [`../examples/greenfield-todo-app/`](../examples/greenfield-todo-app/). | Pass |
| I18N-AC3 | A newly initialized Chinese project produces Chinese Product and Feature prose. | Smoke scenario DL-02 and the `zh-CN` fixture; `test_english_and_chinese_fixtures_preserve_stable_protocols`; Bootstrap's confirmed `zh-CN` path. | Pass |
| I18N-AC4 | A user may discuss an English-document project in Chinese without changing durable output language. | Smoke scenario DL-03; `test_smoke_scenarios_cover_verified_and_mismatched_languages`; language-contract assertions across Product, Generate, Execute, and refactor workflows. | Pass |
| I18N-AC5 | Canonical workflow rules have one English source rather than parallel localized implementations. | `test_native_and_portable_workflow_bodies_remain_identical`; workflow-specific pair tests; `test_examples_do_not_duplicate_workflow_source_trees`; canonical-source rules in `methodology/05-document-language.md`. | Pass |
| I18N-AC6 | Existing projects without language configuration use confirmation-based migration without translation. | Smoke scenario DL-04 and Legacy before/after fixtures; `test_legacy_fixture_adds_only_document_language`; `test_bootstrap_and_contract_preserve_legacy_compatibility`; the v0.1.0 → v0.2.0 procedure in [`../upgrade-notes.md`](../upgrade-notes.md). | Pass |
| I18N-AC7 | Automated checks operate independently of document language. | Paired fixtures preserve keys, enums, IDs, dependencies, paths, timestamps, placeholder prefixes, and completion evidence; Hook tests run against stable evidence; the complete standard-library suite passes in both language modes. | Pass |
| I18N-AC8 | English-facing documentation limits support claims to verified behavior. | README support disclaimer; the `en` and `zh-CN` verified-value boundary in `methodology/05-document-language.md`; best-effort disclosure and prohibited claims in the smoke guide; release consistency tests. | Pass |

## Release-wide verification

The release gate runs only repository-owned, dependency-free checks:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
python3 -m json.tool docs/feature-list.json > /dev/null
python3 -m json.tool docs/feature-list-revisions.json > /dev/null
python3 -m json.tool docs/methodology-config.json > /dev/null
for feature_file in docs/features/*.json; do python3 -m json.tool "$feature_file" > /dev/null || exit 1; done
git diff --check
```

The automated suite covers:

- all repository JSON and JSON templates;
- README, Methodology, release-audit, and upgrade-guide relative links;
- exact native Skill and portable Prompt body parity;
- Hook parsing, evidence, status transitions, and executable entry points;
- English and Chinese stable-protocol fixtures;
- conversation/document-language mismatch behavior;
- Legacy configuration migration and unknown-field preservation;
- English canonical examples and the bilingual README entry points; and
- current-release version consistency while preserving historical v0.1.0 evidence.

## Supported behavior in v0.2.0

- `en` and `zh-CN` are the initially verified document-language values.
- Other well-formed BCP 47 values may be used only on a disclosed best-effort basis.
- Conversation language is transient and may differ from `document_language`.
- New durable Product, Feature, revision, Progress, and handoff prose follows `document_language`.
- Keys, enums, IDs, paths, filenames, placeholders, commit types, and evidence remain stable.
- Existing projects missing the field receive a proposal and explicit confirmation before a JSON-aware, non-translating configuration update.

## Unsupported or intentionally excluded behavior

v0.2.0 does not provide or claim:

- translated copies of executable Methodology, Skills, Prompts, templates, Coding Rules libraries, or Hooks;
- a general runtime localization framework or message catalog;
- automatic translation of an established project's Product, Feature history, Progress, or code;
- a language migration performed by editing `document_language` alone;
- guaranteed quality for every BCP 47 language or region-specific English variant;
- complete localization of every Hook error; or
- automatic upgrade, branch switching, merging, tagging, pushing, or release publication.

## Maintainer-controlled publication boundary

Completing F026 updates repository release artifacts to v0.2.0 and records verification evidence. It does not create or push a Git tag, merge `dev`, publish a GitHub release, or push any branch. Those external actions remain explicit maintainer operations after human acceptance and Feature completion.
