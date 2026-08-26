# Template rendering contract

The files in this directory are Yaya Loop's canonical English templates. They define document structure and semantics; they are not a second document-language setting.

## Rendering procedure

Before rendering a template into a target project, the agent must:

1. Read `document_language` from `docs/methodology-config.json`.
2. Preserve every required section, its order where order carries workflow meaning, and the intent of its guidance.
3. If `document_language` is `en`, write the human-readable content in natural American English.
4. If `document_language` is not `en`, render headings, guidance, examples, and other human-readable values in that language. Translate meaning naturally; do not preserve English sentence structure mechanically.
5. Keep the stable protocol elements below unchanged.

Do not remove a section merely because it is not currently applicable. Keep its heading and record that it is not applicable, or use the section's documented empty form. A localized rendering must not weaken, omit, merge, or reinterpret a required section.

## Required structures

- `product.md.tmpl`: positioning, target users, core loop, module list, module dependencies, visual direction, audio direction, and change history.
- `product-module.md.tmpl`: positioning, functional flow, data model, state machine, UI sketch, audio entries, numeric rules, acceptance criteria, edge cases, and change history.
- `feature-detail.json.tmpl`: `id`, `description`, `acceptance_criteria`, `source`, and `notes`.
- `progress.md.tmpl`: current work, progress, context notes, and history.
- `feature-list.json.tmpl` and `feature-list-revisions.json.tmpl`: their complete JSON schema structure.

## Stable protocol elements

Never translate or rename JSON keys, enum values, Feature IDs, repository paths, structural filenames, placeholder prefixes such as `_placeholder_`, Conventional Commit types, review severities (`must_fix`, `suggest`, and `acceptable`), or gate evidence such as `Code smell scan: pass`.

Human-readable JSON values—including Feature titles, descriptions, acceptance criteria, notes, revision explanations, and decomposition notes—must follow `document_language`. ISO 8601 timestamps and machine identifiers remain language-neutral.
