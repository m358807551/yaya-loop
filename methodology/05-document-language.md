# 05 · Document language contract

> This document defines how Yaya Loop chooses the language of durable project knowledge without localizing its machine protocols or duplicating its canonical workflow sources.

## 1. Two language contexts

Yaya Loop separates two concepts:

- **Conversation language** is the language currently used between the user and the AI. It is session-level interaction state and is not persisted by Yaya Loop.
- **Document language** is the language used for durable, human-readable project knowledge. It is persisted in the project and remains stable across sessions.

Changing the language of a conversation must not change the language of project documents.

## 2. Configuration contract

Every newly initialized project must store `document_language` in `docs/methodology-config.json` before Yaya Loop generates Product or Feature content.

```json
{
  "document_language": "en",
  "static_check_cmd": "python3 -m unittest discover -s tests -v",
  "engine": "example-engine",
  "language": "example-programming-language",
  "kit_version": "0.2.0"
}
```

The value of `document_language` must be a BCP 47 language tag. Initial verified values are:

- `en` for English
- `zh-CN` for Simplified Chinese

Other well-formed BCP 47 tags may be used on a best-effort basis, but the agent must disclose that they are not verified by the initial international release. Yaya Loop's existing `language` field continues to identify the programming language and must not be reused for document language.

Yaya Loop recommends conventional BCP 47 casing: lowercase language, title-case script, and uppercase region. Bootstrap preserves the exact value explicitly confirmed by the user and does not silently normalize it. Empty values, whitespace, and underscore forms such as `zh_CN` are invalid and must be confirmed again in a hyphenated form. Private-use, grandfathered, and other unusual tags require explicit confirmation and remain best-effort rather than verified.

## 3. Language selection

For a new project:

1. Infer a reasonable proposed default from the language currently used by the user.
2. Ask the user to confirm the proposed document language once.
3. Persist the confirmed BCP 47 tag before generating durable Product or Feature content.
4. Use the persisted value as the authority in every later workflow.

If the user's preference cannot be inferred, propose `en` and ask for confirmation. Inference is only a default; country, IP address, timezone, operating-system locale, and account location must not silently select the language.

Every inferred value is non-binding until the user confirms it. If the evidence is mixed or weak, report that uncertainty instead of presenting a dominant language as fact.

## 4. Content governed by document_language

The following generated, human-readable project knowledge must use `document_language`:

- Product headings, prose, tables, diagrams, UI labels, and audio descriptions
- Feature titles, descriptions, acceptance criteria, and human-readable source annotations
- Feature notes and revision-log explanations
- Progress, context notes, implementation decisions, and durable handoff records
- Project-specific natural-language additions written into generated documents

Transient questions, explanations, reports, and verification instructions shown to the user follow the current conversation language. They do not need to match `document_language` unless they are also persisted into the project.

Quoted user-interface text, proper nouns, code samples, and external references may legitimately contain another language. Language checks must not reject content solely because individual characters or examples use a different script.

## 5. Stable protocol elements

The following elements must remain stable English or language-neutral protocol values in every project:

- JSON keys and schema structure
- Feature IDs such as `F009`
- Status values such as `pending`, `in_progress`, and `done`
- Scope values such as `small`, `medium`, and `large`
- Repository paths, structural filenames, and ASCII slugs
- Skill names and public command names
- Conventional Commit types such as `feat`, `fix`, and `docs`
- Placeholder prefixes such as `_placeholder_`
- Review severity values `must_fix`, `suggest`, and `acceptable`
- Gate evidence including `Code smell scan: pass`
- ISO 8601 timestamps and programming-language identifiers

An agent must translate meaning-bearing prose, not keys, enums, IDs, evidence strings, paths, or identifiers.

## 6. Canonical-source policy

Yaya Loop's executable workflow sources use one canonical English version. This includes Methodology specifications, Skills, Prompts, templates, Coding Rules sources, Hooks, and default examples.

Do not create parallel trees such as `methodology.zh-CN/`, localized Skill bodies, or translated Coding Rules libraries. Human-facing entry documents may have explicitly approved translations, such as `README.zh-CN.md`, but those translations are not executable workflow sources.

When rendering an English canonical template into another document language, preserve every required section and its semantics. Rendering must not weaken, omit, or reinterpret workflow requirements.

## 7. Projects missing document_language

An existing initialized project may predate this contract. If `docs/methodology-config.json` exists without `document_language`:

1. Inspect the apparent dominant language of `docs/product.md` and the active Product modules. Active modules are files linked from the module list in `docs/product.md`, excluding entries explicitly marked obsolete or archived; if no usable list exists, inspect current files under `docs/product/` as a fallback.
2. Present that language only as a non-binding migration proposal and ask the user to confirm it. If no language clearly dominates, report the uncertainty and ask the user to choose.
3. Persist the confirmed tag without translating existing files.
4. Record the migration in Progress or upgrade notes appropriate to the project.
5. Apply the confirmed language to new durable content from that point forward.

Do not select a language from Feature titles alone when Product documents are available, because historical Feature data may contain mixed or imported content.

## 8. Existing mixed-language projects

If existing durable documents already contain multiple languages:

1. Report the mixture and identify the dominant Product language.
2. Ask the user to choose the authoritative `document_language`.
3. Persist the choice without silently translating historical content.
4. Write new standalone content in the configured language.
5. Before substantively editing an existing section written in another language, ask whether to localize that section now or preserve it for a later migration.

Historical completed Features and revision records may remain in their original language. Active Product requirements, pending Features, and current Progress should converge only through explicit, reviewable edits.

## 9. Changing an established document language

Editing the configuration field alone is not a supported language migration. A user who explicitly requests a different document language must receive a scoped migration plan covering at least:

- active Product documents and headings
- pending and in-progress Feature natural-language fields
- current Progress and context notes
- source anchors or links affected by translated headings
- verification that machine protocol values remain unchanged

Yaya Loop must not start this migration because the user merely changes conversation language. The initial international release does not automatically translate established projects.

## 10. Workflow obligations

Every workflow that creates or updates durable project knowledge must:

1. Read `docs/methodology-config.json` before writing.
2. Resolve missing configuration through the compatibility rules above.
3. Produce human-readable durable content in `document_language`.
4. Preserve the stable protocol elements in section 5.
5. Stop and ask when an edit would create an unapproved language migration.

These obligations apply equally to native agent integrations and agent-agnostic Prompts.

## 11. Initial release boundaries

The first international release verifies English and Simplified Chinese project knowledge. It does not require:

- a runtime localization framework or translation service
- localized copies of canonical workflow sources
- localized Hook error catalogs
- automatic translation of an existing project
- region-specific variants of English
- verified output for every BCP 47 language tag

Support claims in public documentation must not exceed behavior covered by Bootstrap checks, repository tests, and documented smoke scenarios.
