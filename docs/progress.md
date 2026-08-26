# Project progress

## Current work

F010 - Make Bootstrap select and persist document_language

## Progress

- Started at `2026-08-26T05:38:17Z`.
- Added STEP 0.5 to resolve and persist document_language before Product generation for greenfield, legacy, and already-bootstrapped projects.
- Updated later Bootstrap stages to preserve, verify, and report the confirmed language without translating existing content.
- Clarified non-binding language inference and BCP 47 confirmation behavior in the canonical contract.
- Added a repository test that locks Bootstrap ordering, persistence, non-translation, and conversation-language independence.
- Replaced the destructive full-file config example with a JSON-aware merge contract that preserves unknown project fields, and added a regression assertion against the old overwrite pattern.

## Context notes

- Self-hosting uses Product, Feature, Progress, acceptance, and handoff state without recursively installing copies of Yaya Loop's distributable Skills, Prompts, or Hooks.
- The first planned initiative is internationalization with one English canonical workflow source and project-selected natural-language knowledge.

## History

### 2026-08-26T05:30:31Z - Self-hosting initialization

Current work before F009:

No Feature was in progress. The repository was defining its initial self-hosted Product and Feature backlog.

Progress:

- Confirmed that self-hosted Product documents cover the complete Yaya Loop product.
- Confirmed English as the document language while maintainer conversation may remain Chinese.
- Drafted the Product overview, five product modules, repository rules, and self-hosted methodology configuration.
- Generated the initial self-hosted Feature plan with eight reverse-engineered completed Features and eighteen pending internationalization Features.

### 2026-08-26T05:34:14Z - F009 completed

Current work:

F009 - Define the document-language contract and compatibility behavior

Progress:

- Started at `2026-08-26T05:30:31Z`.
- Added the canonical document-language contract covering BCP 47 configuration, rendering boundaries, stable protocols, legacy compatibility, and explicit language migration.
- Linked the new contract from the Methodology overview without changing later Bootstrap, template, Skill, Prompt, Hook, example, or README behavior.
- All acceptance criteria were verified by human review.
- Fresh-context code-smell scan passed with zero must_fix findings; three implementation clarifications were recorded in F009 notes for later Features.

### 2026-08-26T05:38:17Z - F009 handoff

Current work before F010:

No Feature was in progress.

Progress:

- F009 completed at `2026-08-26T05:34:14Z` and awaited the next explicit instruction.
