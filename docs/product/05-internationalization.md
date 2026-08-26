# Internationalization

## Module positioning

This module makes Yaya Loop approachable to English-speaking users while preserving a first-class Chinese entry point and ensuring generated project knowledge consistently uses the language chosen by each project.

## Product decisions

- English is the single canonical language for Yaya Loop's executable specifications, Skills, Prompts, templates, Coding Rules sources, Hooks, and default examples.
- `README.md` is the complete English repository entry point and `README.zh-CN.md` is a complete, meaning-equivalent Simplified Chinese entry point.
- Canonical workflow sources are not duplicated into translated rule trees.
- A target project persists one `document_language` value using a BCP 47 language tag such as `en` or `zh-CN`.
- Conversation follows the language currently used by the user; changing conversation language does not change `document_language`.
- Human-readable Product and Feature knowledge follows `document_language`; machine protocols remain stable English identifiers.

## Core flows

1. During bootstrap, infer a reasonable document-language default from the user's current language and ask for confirmation once.
2. Persist the confirmed `document_language` before generating Product or Feature content.
3. Render human-readable project knowledge in that language while preserving canonical section semantics.
4. Keep JSON keys, enum values, IDs, paths, placeholder prefixes, commit types, and gate evidence unchanged.
5. On an existing project without language configuration, infer the dominant Product language, request confirmation, and add the setting without translating existing content.
6. Treat changing an established document language as an explicit migration rather than gradually mixing languages.

## Language boundaries

Content governed by `document_language` includes Product prose, Feature titles and details, acceptance criteria, revision notes, progress notes, and other durable project knowledge.

Stable protocol elements include JSON keys, Feature IDs, status and scope enums, filenames, Skill names, Conventional Commit types, `_placeholder_`, `must_fix`, `suggest`, `acceptable`, and `Code smell scan: pass` evidence.

## Acceptance criteria

1. The repository homepage defaults to a complete natural-English README with a working link to the complete Simplified Chinese README, and the Chinese README links back.
2. A newly initialized English project produces English Product and Feature natural-language content.
3. A newly initialized Chinese project produces Chinese Product and Feature natural-language content.
4. A user may discuss an English-document project in Chinese without changing the language of new durable project content.
5. Canonical workflow rules have one English source rather than parallel English and Chinese implementations.
6. Existing projects without language configuration receive a confirmation-based, non-translating migration path.
7. Automated checks continue to operate independently of the selected document language.
8. English-facing documentation does not claim full language support until the corresponding bootstrap and workflow behavior is verified.

## Explicit non-goals for the first international release

- Maintaining translated copies of Methodology, Skills, Prompts, Coding Rules, or Templates.
- Building a general runtime localization framework or message catalog.
- Localizing every Hook error message.
- Automatically translating an established project.
- Supporting region-specific English variants or guaranteeing every possible language in the initial release.

## Edge cases

- The user's conversation language may differ from the configured document language.
- Existing Product and Feature content may already be mixed-language; migration must not silently normalize it.
- Examples and quoted user-interface strings may legitimately contain another language and must not be rejected by naive character scans.
- English canonical instructions must preserve Chinese trigger discoverability without duplicating entire workflows.

## Change history

- 2026-08-26: Added the initial internationalization product specification after maintainer review.
