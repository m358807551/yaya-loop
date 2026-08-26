# Project progress

## Current work

F013 - Convert the execution specification and Coding Rules template to English

## Progress

- Started at `2026-08-26T07:08:35Z`.
- Rewrote the complete Stage 0–8 execution specification in natural American English while preserving entry conditions, outputs, fixed report and evidence formats, human authority, independent review, Git boundaries, and exception handling.
- Rewrote the canonical four-layer Coding Rules template in English and made the self-modification rule snapshot explicit without changing its placeholders or external rule paths.

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

### 2026-08-26T05:49:06Z - F010 completed

Current work:

F010 - Make Bootstrap select and persist document_language

Progress:

- Started at `2026-08-26T05:38:17Z`.
- Added STEP 0.5 to resolve and persist document_language before Product generation for greenfield, legacy, and already-bootstrapped projects.
- Updated later Bootstrap stages to preserve, verify, and report the confirmed language without translating existing content.
- Clarified non-binding language inference and BCP 47 confirmation behavior in the canonical contract.
- Added a repository test that locks Bootstrap ordering, persistence, non-translation, and conversation-language independence.
- Replaced the destructive full-file config example with a JSON-aware merge contract that preserves unknown project fields, and added a regression assertion against the old overwrite pattern.
- All acceptance criteria were verified by human review.
- Fresh-context code-smell scan passed after its one must_fix finding was repaired; two non-blocking suggestions were recorded in F010 notes for F025.

### 2026-08-26T06:52:04Z - F011 completed

Current work:

F011 - Convert Product and Feature templates to canonical English rendering sources

Progress:

- Started at `2026-08-26T05:49:06Z`.
- Added one canonical template rendering contract that preserves required section semantics while localizing human-readable content according to document_language.
- Rewrote the Product, Product module, Feature detail, and Progress template sources in natural English without changing stable machine protocols.
- Added regression coverage for canonical English headings, required-section preservation, stable protocol examples, and the Feature detail JSON schema.
- Expanded the required-section regression inventory after fresh-context review found that several contractually required Product headings were not yet pinned by tests.
- All acceptance criteria were verified by human review.
- Fresh-context review passed after its one must_fix test-coverage finding was repaired; no non-blocking suggestions remain.

### 2026-08-26T07:07:29Z - F012 completed

Current work:

F012 - Convert core Methodology specifications to canonical English

Progress:

- Started at `2026-08-26T06:54:12Z`.
- Rewrote the Methodology overview and Product document structure in natural American English while preserving the standardizer route, human completion authority, document hierarchy, module naming, and Product semantics.
- Rewrote the Feature three-file schema and four-layer Coding Rules architecture in English while preserving stable fields, enums, dependency direction, status transitions, layer precedence, and completion gates.
- Added regression checks for English canonical headings, completion and schema invariants, valid embedded JSON examples, and resolvable relative links across the migrated Methodology documents.
- Restored Stage 0 rule citations, Stage 1 placeholder registration, Stage 6 independent review evidence, the full command-pattern scope, resource-loading fallback, and invariant assertions after fresh-context review detected translation loss; expanded tests to pin each restored rule.
- All acceptance criteria were verified by human review.
- Fresh-context code-smell scan passed with zero remaining must_fix findings; two non-blocking test improvements were recorded in F012 notes for F025.
