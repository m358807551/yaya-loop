# Yaya Loop

## One-line positioning

Yaya Loop is a portable development workflow for people who want AI coding agents to deliver many small, verifiable features over the lifetime of a software project without gradually losing product intent, engineering constraints, or human control.

## Target users

- Independent developers and small teams building real projects with AI coding agents over many iterations.
- Developers who want to work in an unfamiliar language, framework, or engine while retaining product-level control through natural language and verification.
- Maintainers who have found that prompt-by-prompt development becomes difficult to govern as a codebase grows.

Yaya Loop is not optimized for one-off scripts or projects small enough to finish reliably in a few prompts.

## Core loop

1. A maintainer expresses a product need or correction in natural language.
2. Yaya Loop records the durable product intent in Product documents.
3. The Product is decomposed or synchronized into small Features with explicit scope, dependencies, and acceptance criteria.
4. An AI coding agent implements one eligible Feature under the repository's Coding Rules.
5. Automated checks verify machine-observable properties and a human verifies real behavior.
6. A fresh-context code review identifies blocking and non-blocking code smells.
7. The Feature is marked done with auditable evidence, context is handed off, and the loop stops until the next explicit instruction.

## Product principles

- **Project state outlives chat state.** Durable intent and progress live in the repository, not only in a conversation.
- **One bounded Feature at a time.** Yaya Loop reduces the agent's freedom to make unrelated changes.
- **Humans retain product authority.** An AI cannot declare observable product behavior accepted on the user's behalf.
- **Machine protocols stay stable.** IDs, schema keys, enum values, paths, and gate evidence remain language-neutral and automation-friendly.
- **One canonical workflow source.** Executable rules are not duplicated into drifting localized variants.
- **Portable across agents and stacks.** The workflow is not tied to one coding agent, engine, or programming language.

## Module list

| No. | File | Module | Status |
| --- | --- | --- | --- |
| 01 | [01-product-workflow.md](./product/01-product-workflow.md) | Product workflow | implemented |
| 02 | [02-feature-planning.md](./product/02-feature-planning.md) | Feature planning and synchronization | implemented |
| 03 | [03-feature-delivery.md](./product/03-feature-delivery.md) | Feature delivery and quality gates | implemented |
| 04 | [04-adoption-and-integrations.md](./product/04-adoption-and-integrations.md) | Adoption and agent integrations | implemented |
| 05 | [05-internationalization.md](./product/05-internationalization.md) | Internationalization | planned |

## Module dependencies

```text
01 Product workflow
        |
        v
02 Feature planning
        |
        v
03 Feature delivery

04 Adoption and integrations enables modules 01-03 across projects and agents.
05 Internationalization applies across modules 01-04 without translating machine protocols.
```

## Scope boundaries

Yaya Loop is not a project-management dashboard, CI/CD platform, code-generation model, or guarantee that unclear product thinking will produce good software. It provides a controlled development loop around an existing AI coding agent.

## Change history

- 2026-08-26: Reverse-engineered the initial self-hosted Product from the v0.1.0 repository and added the planned internationalization module.
