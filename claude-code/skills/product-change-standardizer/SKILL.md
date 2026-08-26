---
name: product-change-standardizer
version: 3.0
description: The only entry point for Product initialization, requirements, features, UI, audio, and Product-level bug changes. Routes elicitation, owns Product writes, and synchronizes the Feature plan before implementation.
triggers:
  - User requests a new Product, feature, Product improvement, behavior change, or Product-level bug fix
  - User says initialize, improve, optimize, add, remove, fix, adjust, or new requirement
  - 用户说「做一个 XXX」「改进」「优化」「增加」「删除」「修复」「调整」或「新需求」
priority: high
---

# Product change standardizer

## Non-negotiable rules

1. `docs/product.md` and `docs/product/*.md` are the single source of truth for Product intent.
2. Every Product change must update Product documents first, synchronize the Feature plan second, and enter implementation only afterward.
3. This workflow is the only Product writer. Elicitors and sketchers return structured data; this workflow persists it.
4. Product documents describe **what**, not **how**. Keep technology choices and implementation details in Coding Rules, code, or implementation notes.
5. Never make a Product decision on the user's behalf.

## Language contract

Before asking for or writing a Product change:

1. Read `docs/methodology-config.json` and resolve `document_language`.
2. If it is missing or invalid, follow `methodology/05-document-language.md` and obtain confirmation before writing durable content.
3. Converse in the language the user is currently using.
4. Render every new or substantively rewritten Product heading and human-readable value in `document_language`.
5. Preserve stable paths, ASCII slugs, schema keys, enum values, Skill names, Feature IDs, and other protocol identifiers.
6. Do not translate existing content merely because configuration was added or conversation language changed. A language migration requires an explicit, scoped plan.

Smoke cases: with `document_language: en` and a Chinese conversation, converse in Chinese but write English Product content; with `document_language: zh-CN` and an English conversation, converse in English but write Simplified Chinese Product content.

## Product structure and templates

Use this stable structure:

```text
docs/
├── product.md
├── product/
│   ├── 01-<module>.md
│   ├── 02-<module>.md
│   └── ...
└── ui-mockups/
    └── <exploration>.html
```

Module filenames use a two-digit dependency-ordered prefix and a kebab-case ASCII slug. Never renumber an established module.

Before writing Product documents, read:

- `methodology/templates/README.md` for the rendering contract
- `methodology/templates/product.md.tmpl`
- `methodology/templates/product-module.md.tmpl`
- `methodology/01-product-doc-structure.md`

Preserve every required section and its semantics. Render human-readable headings and guidance in `document_language`; do not copy canonical English headings into a non-English Product or maintain a localized template tree.

## Step 1: Confirm Product intent

Restate the requested change in one or two sentences and ask whether to process it as a Product change. This prevents casual discussion from accidentally starting a write workflow.

## Step 2: Load state and choose a route

Read:

- `docs/methodology-config.json`
- `docs/product.md`, if present
- all active `docs/product/*.md`, if present
- `docs/feature-list.json`, if present

The lightweight Feature index is sufficient for routing. Do not eagerly load every Feature detail; the selected generation or synchronization workflow loads details as needed.

Choose exactly one route:

| State | Condition | Route |
| --- | --- | --- |
| A. Initialization | `product.md` is absent or only a template | `product-init-elicitor` |
| B. New module | The change introduces a module with its own responsibility | `product-spec-elicitor`, new-module mode |
| C. Existing module | The change belongs to one existing module | `product-spec-elicitor`, modification mode |
| D. Product bug | Implemented behavior contradicts Product intent | `product-spec-elicitor`, bug mode |
| E. Cross-module | The change affects multiple established modules | `product-spec-elicitor`, cross-module mode |

## Step 3: Run the selected elicitor

For initialization, run `product-init-elicitor` with the user's short description. It returns a complete overview and module draft, while UI wireframes and complete audio entries may remain pending.

For states B through E, run `product-spec-elicitor` with:

- the change description
- the selected mode
- current content of every affected module
- the resolved `document_language`

The elicitor asks only questions that materially affect the change and returns a structured patch. It must not write files.

## Step 4: Complete UI and audio dimensions

For every new or changed UI area:

1. Run `product-ui-sketcher` with its Product behavior and interactions.
2. Receive an ASCII wireframe and intent statement.
3. Ask whether to create an optional standalone HTML and Tailwind exploration under `docs/ui-mockups/`.

For every new or changed audio area:

1. Run `product-audio-sketcher` with its functional flow.
2. Obtain trigger, style, duration, and other required Product details.
3. Assign recognizable `_placeholder_*.wav` names when final assets do not exist.

These child workflows follow the same conversation and document-language boundary. Until their canonical sources are migrated, pass `document_language` explicitly and reject durable output in the wrong language.

## Step 5: Write Product documents

This workflow performs all writes:

1. **Initialization:** render the canonical overview and module templates into `document_language`.
2. **New module:** create `docs/product/NN-<slug>.md` with the next valid dependency-ordered number.
3. **Existing module:** edit only the affected sections; preserve unrelated content.
4. **Overview:** update the module inventory and dependencies when they change.
5. **Change history:** append a dated change and reason to every affected Product file, in `document_language`.
6. **Placeholders:** pass every `_placeholder_` asset path to the Feature synchronization workflow for registration in Feature notes.

Before writing, show destructive or foundational changes for a second confirmation. This includes deleting or obsoleting a module, changing the target audience or core loop, or invalidating completed Product behavior.

## Step 6: Synchronize Features

- For an initialized Product with no real Feature plan, or an explicitly authorized replacement, run `generate-feature-list`.
- For every incremental Product change, including a new module, existing behavior change, or bug correction, run `sync-feature-list`.

Wait for the selected workflow to finish and inspect its result. Never report synchronization as successful merely because it was invoked. Do not rewrite completed Feature history; create explicit follow-up work when completed behavior must change.

## Step 7: Report and stop

Report:

- Product files created or changed and the intent of each change
- the confirmed `document_language`
- Feature synchronization status
- affected Feature states
- every placeholder resource

Ask whether the Product documents are satisfactory and whether the user wants to start `execute-next-feature`. Do not implement code or start execution inside this workflow.

## Boundaries

1. Strip implementation choices from Product intent. Translate a request such as using a particular animation component into its observable transition behavior.
2. Do not write implementation code, even when the user asks to do it at the same time; finish Product and Feature synchronization first.
3. Resolve ambiguous Product decisions through the appropriate elicitor.
4. Never skip Feature generation or synchronization after a Product write.
5. Never silently edit a completed Feature. Create follow-up work or use the synchronization workflow's explicit lifecycle rules.
6. Require confirmation before deleting modules, invalidating completed behavior, or changing foundational positioning.
7. Do not let a conversation-language change rewrite or gradually mix durable Product language.

## Failure handling

- If the user rejects an elicitor draft, do not persist it; return to the elicitor for focused clarification.
- If Feature synchronization fails, report the failure and do not leave Product and Feature state presented as aligned. Offer a reviewable repair or Git rollback; never perform a destructive rollback automatically.
- If a destination module filename already exists, stop and ask whether to merge, choose a new module boundary, or use the next valid number. Never overwrite silently.
- If a child workflow returns durable prose in the wrong language, do not write it. Re-render it in `document_language` without changing its Product meaning, then show it for confirmation.

Always preserve this order:

**Product documents first → Feature synchronization second → implementation last.**
