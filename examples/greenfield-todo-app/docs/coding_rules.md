# AI-assisted development · Coding Rules for TodoMate

> This project was initialized with Yaya Loop. Layers 1 and 2 come from the kit template; Layers 3 and 4 reference the web-frontend and TypeScript stubs.
>
> See `methodology/templates/coding_rules.md.tmpl` in the kit for the complete Layers 1 and 2. This shortened reference example shows their structure and retains the platform and language references.

---

# Part 1 · Collaboration contract

(See the kit template for the complete text. This example is intentionally abbreviated.)

## 1.2 Workflow constraints

- Implement every Feature through the full `execute-next-feature` Skill or Prompt. Do not skip preflight or human acceptance and go directly to implementation.
- An AI must never mark a Feature `done` by itself. A human must explicitly confirm acceptance in speech or writing.
- Name every placeholder resource with the `_placeholder_` prefix and record it in the Feature notes.

**For `execute-next-feature`, the Stage 0 exit report—including verbatim rules and line references—and the Stage 6 code-smell scan are hard gates. The final commit message must include the current Feature ID and the complete `Code smell scan: pass` evidence line with `must_fix: 0`, or the Git commit-msg Hook will reject it.**

---

# Part 2 · General design patterns and architecture principles

(See the kit template for the complete text.)

Key points:
- Prefer the Command pattern: represent each action as a command object.
- Separate data from presentation; the data layer must not know about the UI.
- Manage state with an explicit state machine where state transitions are non-trivial.
- Avoid God Objects, business logic in UI callbacks, unguarded singletons, scattered state, premature abstraction, and magic numbers.

---

# Part 3 · Engine and platform practices

## 3.1 Current platform

web-frontend（Vite + React 18 + TypeScript）

Follow: @docs/coding-rules/engine-rules.md

---

# Part 4 · Programming-language practices

## 4.1 Current language

TypeScript 5.x

Follow: @docs/coding-rules/language-rules.md
