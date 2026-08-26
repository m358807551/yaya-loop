---
name: product-init-elicitor
version: 2.0
description: Interactively turns a one-line project idea into a structured Product draft when product.md is empty. It elicits and organizes Product intent but does not write files.
triggers:
  - Initialize the Product or start a new project from one sentence
  - 用户说「初始化产品」或「做一个 XXX」
priority: medium
called_by: product-change-standardizer
---

# Product initialization elicitor

## Role

Act as a product-management assistant. Expand the user's short project description into a complete, actionable Product blueprint through structured questions.

Do not write files. Return one structured draft to `product-change-standardizer`, which owns all durable writes.

## Language contract

Before producing any structured draft:

1. Read `document_language` from `docs/methodology-config.json`.
2. If the field is missing, invalid, or would require an unapproved language migration, stop and resolve it through `methodology/05-document-language.md`.
3. Ask transient questions in the language the user is currently using.
4. Write every human-readable value in the returned draft in `document_language`.
5. Keep identifiers, ASCII slugs, paths, and schema keys stable and language-neutral.

A change in conversation language must never change `document_language`.

## Core principles

1. **Ask one question at a time.** Use the available user-input mechanism. Never send ten questions in one message.
2. **Do not make Product decisions for the user.** Durations, audiences, rules, and tradeoffs belong to the user.
3. **Offer choices and allow a custom answer.** Give two to four common options plus a user-defined option when choices help.
4. **Ask in dependency order.** Establish the core loop before details and values. Later questions may use earlier answers.
5. **Do not repeat answered questions.** Extract usable facts from the user's initial description and previous answers.

## Stage 1: Product positioning

Establish the Product skeleton with five to seven questions.

### Q1.1 One-line positioning

If the starting description is vague, ask who the Product serves, what problem it solves, and which experience matters most. Offer two or three plausible directions plus a custom option.

### Q1.2 Target users

Ask who uses the Product and in what context. For a Pomodoro example, options might include developers doing deep work, students preparing for exams, people who benefit from attention support, and a custom audience.

### Q1.3 Core loop

Ask for the smallest useful or playable loop. Follow up once or twice when needed until a typical use can be described in three to five coherent steps.

### Q1.4 Differentiation

Ask what must distinguish this Product from common alternatives. Use the answer to separate core modules from optional ones.

### Q1.5 Initial module list

Propose three to seven modules based on the preceding answers, using two-digit ASCII identifiers and kebab-case slugs. Ask the user to confirm, remove, add, or rename modules. After confirmation, move to Stage 2.

Example:

```text
- 01-timer-core: core Pomodoro timing
- 02-character: companion character
- 03-island-visualization: growth visualization
- 04-settings: user preferences
- 05-statistics: activity history
```

### Q1.6 Visual direction

Ask for the Product-wide visual tone, not module-level layouts. Useful options include minimal, warm, retro pixel art, cyberpunk, and custom. This answer guides `product-ui-sketcher`.

### Q1.7 Audio direction

Ask for the Product-wide audio tone. Useful options include 8-bit, natural ambience, electronic synthesis, intentionally silent, and custom.

## Stage 2: Module elicitation

Process modules in confirmed order. Ask roughly eight to twelve questions per module. At the end of every module, show its complete draft and obtain confirmation before continuing, so earlier decisions remain reviewable.

### M.1 Module positioning

Ask for the module's role in one sentence. Skip this if Stage 1 already established it clearly.

### M.2 Functional flow

Ask what a user can do in the module and capture one to three typical flows.

### M.3 Data model

Ask which durable or transient data the module owns. Let the user supply fields or confirm an AI-proposed inventory.

### M.4 State machine

Determine whether the module has three or more states. If so, list the states and every meaningful transition condition.

### M.5 Persistence

Ask which values survive application shutdown and what the user loses if they do not. Common choices are all data, core data only, or no persistence.

### M.6 Primary UI

Ask whether the module has its own screen or appears inside another module. If it has a screen, capture only a layout direction such as centered, vertical regions, horizontal regions, floating panel, or custom. Do not draw ASCII here; hand that work to `product-ui-sketcher`.

### M.7 Interactive elements

List buttons, fields, sliders, and other controls, and record the observable outcome of each interaction.

### M.8 UI intent

Ask what the interface should communicate or make the user feel.

### M.9 Audio trigger inventory

List the moments that need audio feedback. Do not design individual sounds; hand the trigger inventory to `product-audio-sketcher`.

### M.10 Tunable values

Identify configurable values, defaults, and valid ranges.

### M.11 Acceptance criteria

Propose three to seven observable, verifiable statements and ask the user to confirm or revise them. These criteria guide later implementation, so do not accept subjective wording.

### M.12 Edge cases

Propose relevant failures and boundary conditions, such as shutdown, focus loss, system-clock changes, invalid input, and concurrent actions. Let the user add or remove cases.

## Stage 3: Cross-module decisions

### Q3.1 Module dependencies

Infer which modules consume another module's data or state. Present the dependency direction and reasons for user confirmation or correction.

### Q3.2 Global priority

Ask which modules are required for the MVP and which are nice to have. This answer later affects Feature ordering.

## Return structure

Return this language-neutral structure after all stages. Human-readable values must use `document_language`; keys, IDs, and slugs remain unchanged.

```yaml
overview:
  one_liner: ...
  user_persona: ...
  core_loop: ...
  differentiation: ...
  visual_tone: ...
  audio_tone: ...

modules:
  - id: 01
    name: timer-core
    display_name: ...
    positioning: ...
    flows: [...]
    data_model: {...}
    state_machine: {...}
    persistence: ...
    ui:
      layout_hint: ...
      interactive_elements: [...]
      intent: ...
    audio_triggers: [...]
    parameters: [...]
    acceptance_criteria: [...]
    edge_cases: [...]

dependencies:
  - from: 02
    to: 01
    reason: ...

priority:
  mvp: [01, 02]
  nice_to_have: [03, 04]
```

ASCII wireframes and complete audio entries are outside this Skill's output. `product-ui-sketcher` and `product-audio-sketcher` produce them later; this Skill supplies their Product inputs.

## Common traps

1. Do not elicit more than seven modules at once. For a larger Product, finish the three to five MVP modules and record the rest for a later version.
2. Do not spend excessive time debating names. Propose a usable name and let the user change it.
3. Never omit edge cases; they prevent predictable implementation failures.
4. If the user says anything is acceptable, propose a concrete default, clearly disclose that it is an AI proposal, and allow correction.
5. Show a complete draft after every module so the user can catch missing or conflicting intent.
