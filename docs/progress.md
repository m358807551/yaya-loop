# Project progress

## Current work

F026 - Document the upgrade perform the release audit and publish v0.2.0

## Progress

- Started at `2026-08-26T13:00:56Z` from commit `3da9241`.
- Confirmed F025 is done, the worktree is clean on `dev`, and F026 has no external resource or runtime-dependency requirements.
- Approved scope: canonical English upgrade guidance, an eight-criterion internationalization release audit, precise v0.2.0 version updates, unsupported-behavior disclosure, and release consistency tests.
- Historical v0.1.0 records and Legacy migration fixtures remain historical; established projects must not be translated automatically.
- Rewrote the upgrade guide as canonical English with a confirmation-based, JSON-aware, non-translating v0.1.0 → v0.2.0 migration, verification, rollback, and release notes.
- Added the v0.2.0 release audit mapping all eight Internationalization acceptance criteria to evidence and explicitly separating supported behavior, non-goals, and maintainer-controlled publication actions.
- Updated the Product overview and Internationalization history from planned to implemented for the verified release.
- Updated current release surfaces to 0.2.0 while preserving historical v0.1.0 Product, changelog, and Legacy fixture evidence.
- Added dependency-free release tests for version consistency, historical boundaries, upgrade safety, eight-criterion evidence, support/publication limits, and release-document links.
- First complete release verification passed with 69 repository tests.
- Strengthened final release coverage by discovering native/portable workflow pairs from both distribution directories and validating every smoke scenario's Setup, Expected result, Prohibited behavior, and scenario-specific invariants in isolation.
- Recorded the scope of the automated smoke result without claiming automatic certification of external Coding Agent environments.
- Final automated verification passed with all 69 tests, JSON parsing, release-link checks, and diff checks successful; implementation is ready for human acceptance. No tag, merge, push, or external release action has been performed.
- Human acceptance passed at `2026-08-26T13:08:37Z`; the mandatory fresh-context Code Smell Scan is next.
- The first fresh-context scan found one `must_fix`: DL-01 through DL-04 and dual-language suite Pass claims exceeded the recorded static evidence.
- Executed all four canonical scenarios in separate disposable repositories; 28 scenario assertions passed across questions, confirmations, generated prose, stable protocols, Legacy preservation, and prohibited behavior.
- Exported the current Kit into separate `en` and `zh-CN` repositories and passed the complete 69-test suite in each configuration.
- Added structured durable smoke evidence and release-test enforcement; final repository verification and renewed human acceptance remain pending because this repair changes visible release evidence.

## Context notes

- Self-hosting uses Product, Feature, Progress, acceptance, and handoff state without recursively installing copies of Yaya Loop's distributable Skills, Prompts, or Hooks.
- The first planned initiative is internationalization with one English canonical workflow source and project-selected natural-language knowledge.

## History

### 2026-08-26T13:00:56Z - F026 started

Current work before F026:

No Feature was in progress.

Progress:

- F025 completed at `2026-08-26T12:55:20Z` after human acceptance, 63 passing tests, and a fresh-context scan with zero `must_fix` findings.

### 2026-08-26T12:55:20Z - F025 completed

Current work:

F025 - Add document-language compatibility and smoke-test coverage

Progress:

- Added four canonical language smoke scenarios and paired English/Chinese stable-protocol fixtures.
- Added Legacy before/after migration fixtures that preserve unknown fields and established content.
- Added standard-library compatibility and exact nine-pair distribution-parity tests; all 63 repository tests pass.
- Human acceptance passed.
- Code smell scan: pass (feature: F025, must_fix: 0, suggest: 2, acceptable: 0).

### 2026-08-26T12:41:10Z - F025 started

Current work before F025:

No Feature was in progress.

Progress:

- F024 completed at `2026-08-26T12:40:19Z` after final human acceptance, 58 passing tests, and a definitive fresh-context scan with zero `must_fix` or `suggest` findings.

### 2026-08-26T12:40:19Z - F024 completed

Current work:

F024 - Publish the English README and preserve the complete Chinese README

Progress:

- Published complete natural-English and Simplified Chinese entry points with bidirectional language navigation and meaning-equivalent Product positioning.
- Aligned mandatory independent review, bounded Legacy history, explicitly confirmed future work, support disclaimers, internal contracts, and repository links across both languages.
- Human acceptance passed after visible repairs; all 58 repository tests and README link/language checks pass.
- Code smell scan: pass (feature: F024, must_fix: 0, suggest: 0, acceptable: 2).

### 2026-08-26T12:17:22Z - F024 started

Current work before F024:

No Feature was in progress.

Progress:

- F023 completed at `2026-08-26T12:16:17Z` after final human acceptance, 54 passing tests, and a definitive fresh-context scan with zero `must_fix` findings.

### 2026-08-26T12:16:17Z - F023 completed

Current work:

F023 - Convert the default example into a complete English reference project

Progress:

- Converted the Greenfield Product, Feature, Coding Rules, configuration, and Progress reference to complete natural English while preserving machine contracts.
- Rebuilt the Legacy walkthrough with dependency-ordered canonical modules, complete section inventories, exact anchored Feature sources, and pre-bootstrap evidence.
- Added regression coverage for exact template rendering, machine state, Markdown anchors, English prose, and localized workflow-tree exclusion.
- Human acceptance passed after the final visible repair; all 54 repository tests pass.
- Code smell scan: pass (feature: F023, must_fix: 0, suggest: 2, acceptable: 2).

### 2026-08-26T11:38:31Z - F023 started

Current work before F023:

No Feature was in progress.

Progress:

- F022 completed at `2026-08-26T11:37:55Z` after human acceptance, plural-message repair, 50 passing tests, and a fresh-context scan with zero remaining must_fix or suggest findings.

### 2026-08-26T11:37:55Z - F022 completed

Current work:

F022 - Convert installation guidance and Hook-facing text to canonical English

Progress:

- Rewrote both installation guides and all direct Hook-facing text as canonical English.
- Preserved Hook parsing, status detection, failure behavior, return codes, commands, paths, and executable permissions.
- Human acceptance passed; all 50 tests pass.
- Fresh-context review corrected multi-Feature plural wording before passing.
- Code smell scan: pass (feature: F022, must_fix: 0, suggest: 0, acceptable: 1).

### 2026-08-26T11:30:55Z - F022 started

Current work before F022:

No Feature was in progress.

Progress:

- F021 completed at `2026-08-26T11:30:17Z` after human acceptance, scoring repair, 46 passing tests, and a fresh-context scan with zero remaining must_fix or suggest findings.

### 2026-08-26T11:30:17Z - F021 completed

Current work:

F021 - Internationalize refactor selection and portable usage guidance

Progress:

- Rewrote refactor selection as an exact native/portable English pair and made portable usage guidance English-first with bilingual discovery.
- Preserved stable markers, rubric thresholds, one comparative recommendation, read-only behavior, Plan handoff, and historical excerpts.
- Human acceptance passed; all 46 tests pass.
- Fresh-context review restored Bug tokens and same-file severity scoring before passing.
- Code smell scan: pass (feature: F021, must_fix: 0, suggest: 0, acceptable: 3).

### 2026-08-26T11:03:41Z - F021 started

Current work before F021:

No Feature was in progress.

Progress:

- F020 completed at `2026-08-26T11:03:01Z` after human acceptance, semantic gate repair, 41 passing tests, and a fresh-context scan with zero remaining must_fix or suggest findings.

### 2026-08-26T11:03:01Z - F020 completed

Current work:

F020 - Internationalize Feature execution workflows

Progress:

- Rewrote Feature execution as an exact native/portable canonical English pair under the committed start-rule snapshot.
- Preserved Stage 0–8 gates, human acceptance, independent review, evidence, Progress, verification, commits, exceptions, and Git boundaries.
- Made durable execution knowledge follow `document_language` while conversation remains transient.
- Human acceptance passed; all 41 repository tests pass.
- Fresh-context review repaired three omitted gates before passing.
- Code smell scan: pass (feature: F020, must_fix: 0, suggest: 0, acceptable: 2).

### 2026-08-26T10:35:13Z - F020 started

Current work before F020:

No Feature was in progress.

Progress:

- F019 completed at `2026-08-26T10:34:22Z` after human acceptance, 35 passing tests, and a fresh-context scan with zero must_fix findings.

### 2026-08-26T10:34:22Z - F019 completed

Current work:

F019 - Internationalize Feature-list synchronization workflows

Progress:

- Rewrote Feature-list synchronization as an exact native/portable canonical English pair.
- Preserved all seven stages, Git anchor/diff analysis, status-specific history behavior, revision logging, validation, exceptions, and Git boundaries.
- Made new and revised durable prose follow `document_language` without translating completed history.
- Human acceptance passed; all 35 repository tests pass.
- Code smell scan: pass (feature: F019, must_fix: 0, suggest: 2, acceptable: 3).

### 2026-08-26T10:22:46Z - F019 started

Current work before F019:

No Feature was in progress.

Progress:

- F018 completed at `2026-08-26T10:22:17Z` after human acceptance, 30 passing tests, and a fresh-context scan with zero must_fix findings.

### 2026-08-26T10:22:17Z - F018 completed

Current work:

F018 - Internationalize Feature-list generation workflows

Progress:

- Rewrote initial Feature-list generation as an exact native/portable canonical English pair.
- Preserved initial-generation and confirmed-replacement routing, complete input loading, decomposition rules, the three-file schema, validation, and the no-auto-execution boundary.
- Made durable Feature prose follow `document_language` while keeping protocol fields stable.
- Human acceptance passed; all 30 repository tests pass.
- Code smell scan: pass (feature: F018, must_fix: 0, suggest: 1, acceptable: 4).

### 2026-08-26T10:16:36Z - F018 started

Current work before F018:

No Feature was in progress.

Progress:

- F017 completed at `2026-08-26T10:15:56Z` after human acceptance, semantic repair, 25 passing tests, and a fresh-context scan with zero remaining must_fix or suggest findings.

### 2026-08-26T10:15:56Z - F017 completed

Current work:

F017 - Internationalize Product specification UI and audio workflows

Progress:

- Rewrote Product specification, UI sketching, and audio sketching Skills and portable Prompts as canonical English paired workflows.
- Made durable Product prose follow `document_language` while preserving stable patch keys, ASCII conventions, UI paths, sfx/bgm identifiers, and `_placeholder_` filenames.
- Added exact-pair and semantic regression coverage; all 25 repository tests pass.
- Human acceptance passed.
- Fresh-context review restored canonical language-configuration handling and the complete standalone Tailwind HTML contract before passing.
- Code smell scan: pass (feature: F017, must_fix: 0, suggest: 0, acceptable: 3).

### 2026-08-26T09:57:43Z - F017 started

Current work before F017:

No Feature was in progress.

Progress:

- F016 completed at `2026-08-26T09:56:35Z` after human acceptance, semantic repair, 21 passing tests, and a fresh-context scan with zero remaining must_fix findings.

### 2026-08-26T09:56:35Z - F016 completed

Current work:

F016 - Internationalize Product initialization and change-standardization workflows

Progress:

- Rewrote Product initialization and Product change-standardization Skills and portable Prompts as canonical English paired workflows.
- Added persisted document-language behavior, transient conversation-language behavior, bilingual trigger discovery, mismatch smoke cases, and exact native/portable body equivalence.
- Preserved the complete initialization question inventory, seven-step standardizer flow, write boundaries, failure handling, and Feature routing semantics.
- Human acceptance passed; all 21 tests pass.
- Fresh-context scan restored two weakened rules before passing.
- Code smell scan: pass (feature: F016, must_fix: 0, suggest: 1, acceptable: 3).

### 2026-08-26T09:45:28Z - F016 started

Current work before F016:

No Feature was in progress.

Progress:

- F015 completed at `2026-08-26T09:42:24Z` after human acceptance, iterative accuracy repairs, 20 passing tests, and a definitive fresh-context scan with zero remaining must_fix findings.

### 2026-08-26T09:42:24Z - F015 completed

Current work:

F015 - Convert programming-language Coding Rules to canonical English

Progress:

- Started at `2026-08-26T08:12:22Z`.
- Rewrote five language sources as explicit actionable English stubs and the complete GDScript 2.0 source as canonical English without changing stable paths.
- Added exact regression contracts for all stub headings and TODO clauses, English-only sources, Bootstrap paths, GDScript technical invariants, and fully typed examples.
- Human acceptance passed.
- Fresh-context review corrected setter, assertion, signal, typing, Node equality, and static-variable lifecycle semantics before completion.
- All 20 repository tests pass.
- Code smell scan: pass (feature: F015, must_fix: 0, suggest: 0, acceptable: 3).

### 2026-08-26T08:12:22Z - F015 started

Current work before F015:

No Feature was in progress.

Progress:

- F014 completed at `2026-08-26T08:10:41Z` after human acceptance and a fresh-context scan with zero remaining must_fix findings.

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

### 2026-08-26T07:15:56Z - F013 completed

Current work:

F013 - Convert the execution specification and Coding Rules template to English

Progress:

- Started at `2026-08-26T07:08:35Z`.
- Rewrote the complete Stage 0–8 execution specification in natural American English while preserving entry conditions, outputs, fixed report and evidence formats, human authority, independent review, Git boundaries, and exception handling.
- Rewrote the canonical four-layer Coding Rules template in English and made the self-modification rule snapshot explicit without changing its placeholders or external rule paths.
- Added regression coverage for all nine Stage headings, execution gates, independent-review JSON, exact Hook evidence, seven collaboration rules, four Coding Rules layers, stable placeholders, and rule-snapshot behavior.
- Restored the post-acceptance ban on behavior-changing smell repairs, the unqualified core-rule purity recommendation, and proactive Pattern guide behavior after fresh-context review detected semantic weakening; pinned all three in tests.
- All acceptance criteria were verified by human review.
- Fresh-context code-smell scan passed with zero remaining must_fix or suggest findings.

### 2026-08-26T08:10:41Z - F014 completed

Current work:

F014 - Convert engine Coding Rules to canonical English

Progress:

- Started at `2026-08-26T07:17:02Z`.
- Rewrote the generic engine stub and the backend, Unity, Unreal, and web-frontend stubs in natural American English while keeping them visibly incomplete, actionable, and at their stable installation paths.
- Rewrote the complete Godot 4.3+ engine rules in English while preserving Scene composition, call-down/signal-up communication, Autoload, Resource, export/onready, lifecycle, performance, naming, signal-connection, anti-pattern, and debugging constraints.
- Added regression checks for the stable engine file set, English-only canonical prose, explicit stub status, Bootstrap copy paths, and the detailed Godot technical rule inventory.
- Restored five categorical Godot constraints after fresh-context review found modal weakening in signal return behavior, read-only global configuration, development-time `.tres`, exclusive child-reference use of `@onready`, and pooled-object deactivation; strengthened tests to assert full normative sentences and the Bootstrap destination path.
- All acceptance criteria were verified by human review.
- Fresh-context code-smell scan passed with zero remaining must_fix or suggest findings.
