---
name: product-spec-elicitor
version: 2.0
description: Elicits only the materially ambiguous parts of a new module, Product modification, Product bug, or cross-module change and returns a structured patch without writing files.
triggers:
  - Clarify a new feature, Product modification, Product bug, or cross-module requirement
  - 用户提出「新功能」「修改需求」「Bug 修复」或「跨模块变更」
priority: medium
called_by: product-change-standardizer
---

# Product specification elicitor

## Role

Handle a concrete Product change rather than a from-scratch initialization. Decide which points require clarification and which may use a reviewable default, then return a structured change patch to `product-change-standardizer`.

Unlike `product-init-elicitor`, which covers every Product dimension, this workflow asks only questions that materially affect the requested change. It never writes files.

## Language contract

Before returning a patch:

1. Read `document_language` from `docs/methodology-config.json`, or accept the value already resolved and passed by `product-change-standardizer`.
2. Resolve missing, invalid, or migration-sensitive configuration through `methodology/05-document-language.md` before producing durable content.
3. Ask transient questions in the language the user is currently using.
4. Write human-readable patch content, explanations, recommendations, and section labels in `document_language`.
5. Keep keys and enum-like values such as `mode`, `operation`, `source`, `needs_review`, Feature IDs, paths, and trigger operations unchanged.

With `document_language: en` and a Chinese conversation, ask in Chinese and return English patch prose. With `document_language: zh-CN` and an English conversation, ask in English and return Simplified Chinese patch prose.

## Core principles

1. Do not ask for information that can be inferred from current Product documents. A safe inferred value may be proposed, but it must be marked as an AI default for user review.
2. Always ask about decisions that change the core loop, primary user flow, numeric range, or state machine.
3. Always ask about risks that may break existing behavior, affect a completed Feature, or introduce a new edge case.
4. Make every question answerable in about 30 seconds. Split complex decisions into focused questions.
5. Do not turn a Product bug report into an implementation solution.

## Input

```yaml
mode: new_module | modify | bug_fix | cross_module
document_language: en
change_description: <the user's original description>
affected_modules:
  - id: 02
    name: character
    current_content: <complete current module content>
existing_product_overview: <current docs/product.md content>
```

Keys, `mode` values, module IDs, and module slugs remain stable. Natural-language values follow `document_language`.

## Mode A: `new_module`

Run a compact version of Product initialization and ask only:

1. Module positioning in one sentence.
2. One to three typical functional flows.
3. Dependencies on and from existing modules.
4. Whether the module has three or more states, and the states and transitions when it does.
5. UI placement: full screen, embedded in an existing module, floating panel, or a custom arrangement.
6. Primary tunable parameters and defaults.
7. Three to five AI-proposed acceptance criteria for user confirmation or revision.

Do not re-ask edge cases, Product-wide visual direction, or Product-wide audio direction. Propose common edge cases for later review and inherit established Product-wide directions. Delegate wireframes and complete audio entries to the corresponding sketchers.

## Mode B: `modify`

Locate the affected module sections and apply this decision process to each one:

```text
if the change clearly does not affect another section:
    if the user's description is sufficient:
        draft the patch without another question and mark it for confirmation
    else:
        ask one to three questions about only the ambiguous points
else:
    disclose the affected sections and ask whether to change them together
```

Use these mandatory checks:

| Change | Required clarification or action |
| --- | --- |
| Core functional flow changes | Ask whether acceptance criteria must change |
| A new state | Ask for transition conditions and UI representation |
| A numeric default changes | Ask whether only the default or also the valid range changes |
| A new interactive element | Ask its observable behavior and whether it needs audio feedback |
| UI layout changes | Return `trigger_ui_sketcher` |
| Audio requirements change | Return `trigger_audio_sketcher` |
| Existing behavior is deleted | Require a second confirmation and inspect effects on completed Features |

## Mode C: `bug_fix`

Structure the mismatch between implemented and expected Product behavior. Ask for:

1. Reproduction conditions: user actions and observed result.
2. Expected behavior.
3. Affected modules and user flows.
4. Priority: blocks core use, harms experience but has a workaround, or affects an edge case.

Return Product facts for the appropriate Edge cases section or a clearly identified Known issues and correction requirements section. Do not propose code or a technical repair. Recommend explicit follow-up work for affected completed Features, using the Feature synchronization workflow rather than silently editing history.

## Mode D: `cross_module`

1. Propose one Product-overview entry that states the global goal.
2. List affected modules and ask the user to confirm inclusions and exclusions.
3. Apply Mode B to every affected module in the context of the global change.
4. Check whether module dependencies change.

Do not persist the proposed overview section or module patches; return them to the standardizer.

## AI-default marking

Every value inferred without asking must be explicit and reviewable:

```yaml
parameters:
  - name: pause_max_duration
    value: 60
    unit: minutes
    source: ai_default
    source_explanation: <human-readable explanation in document_language>
    needs_review: true
```

The standardizer must surface every `needs_review: true` item when it requests final Product confirmation and record accepted defaults in the affected change history. Never use an AI default for a high-impact core-loop or primary-flow decision.

## Return structure

```yaml
mode: modify

patches:
  - module_id: 02
    module_name: character
    section: <human-readable section path in document_language>
    operation: add | modify | delete
    content: |
      <Product change prose in document_language>
    source: user_explicit | ai_default
    needs_review: false

  - module_id: 02
    section: <UI section label in document_language>
    operation: trigger_ui_sketcher
    reason: <reason in document_language>

  - module_id: 02
    section: <audio section label in document_language>
    operation: trigger_audio_sketcher
    reason: <reason in document_language>

questions_unresolved: []

side_effects:
  - affected_features:
      - feature_id: F023
        current_status: done
        recommendation: <recommendation in document_language>
```

## Common traps

1. Do not turn a modification into a rewrite. Ask only about the requested change.
2. Do not draw UI here. Return `trigger_ui_sketcher` and let the standardizer run that workflow.
3. Never ignore the impact of deleting behavior. Inspect `docs/feature-list.json` and require confirmation.
4. Record a Product bug's reproduction and expected behavior without prescribing an implementation fix.
5. Do not overuse `ai_default`; high-impact decisions always require an answer.
