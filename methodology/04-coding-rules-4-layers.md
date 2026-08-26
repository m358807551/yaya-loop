# 04 · Four-layer Coding Rules architecture

## Overview

`docs/coding_rules.md` is the governing implementation contract for an AI coding agent. It has four layers, from general and highest priority to stack-specific. A higher layer wins when rules conflict unless a lower layer represents a mandatory platform or engine constraint.

```text
┌──────────────────────────────────────────────────────────┐
│ Layer 1 · Collaboration contract                         │
│   How the AI and human work together                     │
│   Stack-independent and highest priority                 │
│   Provided by the kit                                    │
├──────────────────────────────────────────────────────────┤
│ Layer 2 · General design and architecture                │
│   Commands, state machines, composition, data-driven work│
│   Independent of language and engine                     │
│   Provided by the kit                                    │
├──────────────────────────────────────────────────────────┤
│ Layer 3 · Engine or platform practices                   │
│   Select one source from coding-rules-library/engines/   │
│   Included as @docs/coding-rules/engine-rules.md         │
├──────────────────────────────────────────────────────────┤
│ Layer 4 · Programming-language practices                 │
│   Select one source from coding-rules-library/languages/ │
│   Included as @docs/coding-rules/language-rules.md       │
└──────────────────────────────────────────────────────────┘
```

## Layer 1: collaboration contract

Layer 1 lives in the main `coding_rules.md`, prefilled from `methodology/templates/coding_rules.md.tmpl`. It covers:

- seven collaboration disciplines: avoid over-design, confirm ambiguity before acting, work in small steps, preserve project consistency, disclose uncertainty, respect rejected decisions, and do not expand scope without approval
- workflow constraints: use `execute-next-feature`, never let the AI self-accept a Feature, and follow the Git safety protocol
- delivery reporting: change summary, impact, intentionally omitted work, and verification guidance
- explicit disclosure when a rule must be deviated from

Projects should not modify this layer unless the user's collaboration preferences genuinely differ from the defaults.

## Layer 2: general design and architecture

Layer 2 also lives in the main `coding_rules.md`. It includes:

- the command pattern as the preferred organization for a multi-step operation
- separation of data and presentation, explicit state machines, layered logic, composition over inheritance, data-driven behavior, pure core rules, dependency injection, and serializable runtime state
- a pattern selection table
- anti-patterns such as God Objects, business logic in UI callbacks, pervasive raw singletons, scattered state, premature abstractions, magic values, and long procedural functions
- organization by feature, single responsibility, minimal entry points, centralized configuration, and avoidance of miscellaneous utility dumping grounds
- error handling that distinguishes expected failures from exceptional failures and never silently swallows exceptions
- measurement before performance optimization

This layer is stable kit content and remains independent of a particular stack.

## Layer 3: engine or platform practices

Engine behavior varies too much to embed in the main file. The main file names the current engine or platform and includes one external project rule file:

```markdown
## 3.1 Current engine or platform

godot4.3 <!-- or unity, unreal, web-frontend, backend-service, ... -->

Follow: @docs/coding-rules/engine-rules.md
```

Copy `docs/coding-rules/engine-rules.md` from `coding-rules-library/engines/<engine>.md` when a suitable source exists. If the source is a stub, Bootstrap must ask whether to fill its essential sections now or retain explicit TODOs. If no source exists, begin with `coding-rules-library/engines/_stub-template.md`.

An engine rule file should cover:

- lifecycle, scenes or nodes, and resource management
- signals, events, or messaging
- debugging tools and editor integration
- engine-specific performance traps

## Layer 4: programming-language practices

The main file names the implementation language and includes one external project rule file:

```markdown
## 4.1 Current language

gdscript <!-- or csharp, typescript, python, rust, ... -->

Follow: @docs/coding-rules/language-rules.md
```

Select `docs/coding-rules/language-rules.md` from `coding-rules-library/languages/<language>.md`, using the same real-source, stub, and missing-source behavior as Layer 3.

A language rule file should cover:

- type system, static checks, and naming conventions
- memory, lifetime, and reference rules
- language-specific traps such as GDScript lambda capture, TypeScript strictness, or mutable Python default arguments
- standard-library and third-party ecosystem conventions

## Cross-layer naming and readability

The main `coding_rules.md` should establish stack-independent conventions:

- Name by intent rather than container type: `enemies`, not `enemyList`.
- Use one term for one concept; do not alternate among `tile`, `cell`, and `block` without a domain distinction.
- Prefix booleans consistently with `is_`, `has_`, `can_`, or `should_` as appropriate to the language.
- Use verb phrases for functions, such as `spawn_enemy` or `apply_damage`.
- Use an action-oriented name for command classes, such as `RocketMaker` or `DamageCalculator`.
- Avoid abbreviations except established domain terms such as `pos`, `vel`, `hp`, or `fps`.
- Comments should explain why, not restate what the code says.

## Deviating from a rule

The four layers are guidance with explicit priorities, not an excuse to ignore project reality. An agent may deviate when:

- the user explicitly requests a different approach
- established project style conflicts with the rule and migration cost is disproportionate
- a mandatory platform or engine convention conflicts with a more general preference

The agent must disclose the deviation and reason, for example: `This implementation deviates from Coding Rules section X because Y.`

## Files written into a project

```text
docs/
├── coding_rules.md                       ← Layers 1 and 2 plus includes
└── coding-rules/
    ├── engine-rules.md                   ← Layer 3
    └── language-rules.md                 ← Layer 4
```

## Evolution guidance

- Keep all three project files focused. Let fresh-context code-smell scans reveal demonstrated gaps before adding more rules.
- Prefer the highest layer that accurately owns a rule. For example, a general event-naming rule belongs in Layer 2 rather than in Godot-specific guidance.
- If a rule is repeatedly bypassed, either revise the rule or align the codebase. Do not preserve permanent contradiction.
