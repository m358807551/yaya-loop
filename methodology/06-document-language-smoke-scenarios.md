# 06 · Document-language smoke scenarios

> These scenarios verify Yaya Loop's initial internationalization contract without treating conversation language as durable project state or translating stable machine protocols.

## How to run the scenarios

Run each scenario in a disposable repository initialized from the current Kit. Record the agent's questions, the confirmed language, generated files, and validation output. A scenario passes only when every expected result and prohibited behavior below is satisfied.

The initially verified document languages are `en` and `zh-CN`. Other BCP 47 tags remain best-effort and must not be described as verified by these scenarios.

## Stable protocol fixture

The following paired snapshots describe the same pending Feature. Natural-language values change with `document_language`; keys, enums, IDs, dependencies, paths, timestamps, placeholder prefixes, and completion evidence do not.

<!-- fixture: en -->
```json
{
  "config": {
    "document_language": "en",
    "static_check_cmd": "python3 -m unittest discover -s tests -v",
    "engine": "example-engine",
    "language": "python",
    "kit_version": "0.1.0",
    "bootstrap_at": "2026-08-26T00:00:00Z",
    "bootstrap_mode": "greenfield"
  },
  "feature": {
    "id": "F900",
    "title": "Add profile export",
    "status": "pending",
    "depends_on": ["F899"],
    "estimated_scope": "small",
    "completed_at": null
  },
  "detail": {
    "id": "F900",
    "description": "Let the user export a profile as JSON.",
    "acceptance_criteria": ["Selecting Export downloads one JSON file."],
    "source": "product/01-profile.md#acceptance-criteria",
    "notes": "Keep the existing profile schema."
  },
  "protocol": {
    "detail_path": "docs/features/F900.json",
    "placeholder": "_placeholder_profile.json",
    "completion_evidence": "Code smell scan: pass (feature: F900, must_fix: 0, suggest: 0, acceptable: 0)"
  }
}
```

<!-- fixture: zh-CN -->
```json
{
  "config": {
    "document_language": "zh-CN",
    "static_check_cmd": "python3 -m unittest discover -s tests -v",
    "engine": "example-engine",
    "language": "python",
    "kit_version": "0.1.0",
    "bootstrap_at": "2026-08-26T00:00:00Z",
    "bootstrap_mode": "greenfield"
  },
  "feature": {
    "id": "F900",
    "title": "增加用户资料导出",
    "status": "pending",
    "depends_on": ["F899"],
    "estimated_scope": "small",
    "completed_at": null
  },
  "detail": {
    "id": "F900",
    "description": "允许用户把资料导出为 JSON。",
    "acceptance_criteria": ["点击导出后下载一个 JSON 文件。"],
    "source": "product/01-profile.md#acceptance-criteria",
    "notes": "保持现有用户资料 schema。"
  },
  "protocol": {
    "detail_path": "docs/features/F900.json",
    "placeholder": "_placeholder_profile.json",
    "completion_evidence": "Code smell scan: pass (feature: F900, must_fix: 0, suggest: 0, acceptable: 0)"
  }
}
```

## Scenario DL-01 · English conversation and English documents

### Setup

- Start with a new repository that has no `docs/methodology-config.json`.
- Speak English to the agent.
- Confirm `en` when the agent proposes the document language.

### Expected result

- The agent communicates in English.
- `document_language` is persisted as `en` before Product or Feature generation.
- Product headings and prose, Feature titles and details, and Progress entries use natural English.
- The English stable-protocol fixture above represents the generated protocol shape.

### Prohibited behavior

- Do not infer the document language from country, IP address, timezone, or operating-system locale.
- Do not translate JSON keys, enum values, IDs, paths, placeholders, or evidence.

## Scenario DL-02 · Chinese conversation and Simplified Chinese documents

### Setup

- Start with a new repository that has no `docs/methodology-config.json`.
- Speak Simplified Chinese to the agent.
- Confirm `zh-CN` when the agent proposes the document language.

### Expected result

- The agent communicates in Simplified Chinese.
- `document_language` is persisted as `zh-CN` before Product or Feature generation.
- Product headings and prose, Feature titles and details, and Progress entries use natural Simplified Chinese.
- The Chinese stable-protocol fixture above differs from the English fixture only in `document_language` and human-readable values.

### Prohibited behavior

- Do not persist conversation language as a second language setting.
- Do not create localized Methodology, Skill, Prompt, template, Coding Rules library, or Hook trees.

## Scenario DL-03 · Chinese conversation and English documents

### Setup

- Start with a project whose `docs/methodology-config.json` contains `"document_language": "en"`.
- Speak Simplified Chinese to the agent and request a Product change.

### Expected result

- The agent's questions, reports, and human-verification instructions use Simplified Chinese.
- New durable Product, Feature, revision, Progress, and handoff prose uses natural English.
- The stored `document_language` remains `en`.
- Stable protocol elements remain identical to Scenario DL-01.

### Prohibited behavior

- Do not change `document_language` to `zh-CN` because the conversation changed.
- Do not mix Chinese conversation text into durable project knowledge unless it is a quoted UI label, proper noun, code sample, or external reference.

## Scenario DL-04 · Legacy configuration without document_language

### Setup

- Start with an initialized legacy project whose Product documents are predominantly Chinese.
- Use this existing configuration, including the unknown `team_policy` field:

<!-- fixture: legacy-before -->
```json
{
  "static_check_cmd": "pytest",
  "engine": "django",
  "language": "python",
  "kit_version": "0.1.0",
  "bootstrap_at": "2026-01-01T00:00:00Z",
  "bootstrap_mode": "legacy",
  "team_policy": "preserve-me"
}
```

- Let the agent present `zh-CN` only as a non-binding proposal, then explicitly confirm `en` as the authoritative document language.

### Expected result

- The agent reports that the existing Product appears predominantly Chinese and asks for confirmation.
- Only `document_language` is added; every existing and unknown configuration field is preserved.

<!-- fixture: legacy-after -->
```json
{
  "document_language": "en",
  "static_check_cmd": "pytest",
  "engine": "django",
  "language": "python",
  "kit_version": "0.1.0",
  "bootstrap_at": "2026-01-01T00:00:00Z",
  "bootstrap_mode": "legacy",
  "team_policy": "preserve-me"
}
```

- Existing Chinese Product and completed Feature history remains unchanged.
- New standalone durable content uses English from that point forward.
- Progress records the confirmed migration decision and that no automatic translation occurred.

### Prohibited behavior

- Do not silently choose `zh-CN` from the apparent Product language.
- Do not replace the configuration object, discard unknown fields, or reuse programming-language `language` as document language.
- Do not translate established Product, completed Feature history, or current code during configuration migration.

## Automated compatibility gate

The repository test suite must verify:

1. all JSON fixtures in this document parse;
2. English and Chinese fixtures preserve identical machine projections;
3. the Legacy migration adds only `document_language` and preserves unknown fields;
4. Bootstrap and the document-language contract retain confirmation, preservation, and no-silent-translation rules;
5. every native Claude Skill and portable Prompt pair has an identical canonical English body; and
6. repository tests and `git diff --check` pass without additional runtime dependencies.
