# Product workflow

## Module positioning

This module turns natural-language product intent into durable, structured Product documents that remain the single source of truth for what a project should do.

## Core flows

1. Initialize a Product from a short project description through focused elicitation.
2. Route every later requirement, correction, or product-level bug through the product change workflow.
3. Update the affected Product module before any implementation work begins.
4. Preserve module ownership, dependencies, acceptance criteria, and change history.

## Data and state

- `docs/product.md` stores positioning, users, the core loop, module inventory, and dependencies.
- `docs/product/NN-name.md` stores detailed behavior and acceptance boundaries for one module.
- Product state evolves through explicit changes; source documents are never silently rewritten from implementation guesses.

## Interaction model

The maintainer describes intent in natural language. The agent asks only questions that materially change product behavior, proposes structured drafts, and requests confirmation for destructive or foundational changes.

## Acceptance criteria

1. A new project can turn a short description into a Product overview and module documents.
2. A later product change updates Product documents before changing Features or source code.
3. Product documents describe observable intent and avoid implementation-specific decisions.
4. Each module contains concrete acceptance criteria and explicitly excluded edge cases.
5. A change remains traceable through module history and subsequent Feature synchronization.

## Edge cases

- Existing projects may require reverse engineering and human correction before their Product is trustworthy.
- Ambiguous requirements must pause for clarification rather than being silently converted into product decisions.
- Product and implementation may temporarily disagree during migration; the discrepancy must be surfaced explicitly.

## Change history

- 2026-08-26: Added the initial reverse-engineered module definition.
