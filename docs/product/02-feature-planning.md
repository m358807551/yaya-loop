# Feature planning and synchronization

## Module positioning

This module converts durable Product intent into a dependency-ordered queue of small, independently verifiable Features and keeps that queue aligned as the Product changes.

## Core flows

1. Read the complete Product and relevant Coding Rules.
2. Decompose observable behavior into Features that fit within one agent session.
3. Store a lightweight index separately from lazily loaded Feature details.
4. Incrementally synchronize Product changes without discarding completed history.
5. Record synchronization anchors and revisions for later sessions.

## Data and state

- `docs/feature-list.json` is the lightweight status and dependency index.
- `docs/features/F0XX.json` contains description, acceptance criteria, source, and notes.
- `docs/feature-list-revisions.json` records synchronization history.
- Machine fields and enum values remain stable even when natural-language content uses another language.

## Acceptance criteria

1. Every planned Feature has an ID, bounded observable outcome, dependency list, scope estimate, and acceptance criteria.
2. No final Feature has `estimated_scope` set to `large`.
3. Dependencies only point to existing earlier Features and contain no cycles.
4. Feature details identify the Product section that justifies the work.
5. Incremental synchronization preserves completed Features and records why new, revised, blocked, or obsolete work changed.
6. Index IDs, detail filenames, and the recorded Feature count remain consistent.

## Edge cases

- Product changes may invalidate previously completed behavior; this must create explicit follow-up work rather than rewrite history.
- A missing synchronization anchor must stop the workflow and request a migration decision.
- Natural-language quotation must never produce invalid JSON.

## Change history

- 2026-08-26: Added the initial reverse-engineered module definition.
