---
name: execute-next-feature
description: Execute the next, current, or specified Feature through preflight, implementation, verification, human acceptance, independent review, completion, and handoff. Do not use for initial planning or Product synchronization. English triggers: do the next Feature, implement F007, continue the task. 中文触发：做下一个 feature、实现 F007、继续推进任务、开始干活。
---

# Execute one Feature

This is a mandatory Stage 0–8 workflow. Skipping a stage or its entry gate is a workflow violation.

## Language and rule-snapshot contract

1. Read `document_language` from `docs/methodology-config.json`. Resolve missing, invalid, or migration-sensitive configuration through `methodology/05-document-language.md` before writing durable project knowledge.
2. Use the language of the user's current message for conversation, reports, questions, and verification instructions.
3. Write durable Feature notes, Progress entries and history, acceptance records, TODOs, and handoff state in `document_language`.
4. Keep JSON keys, enum values, Feature IDs, paths, commands, commit types, timestamps, and evidence strings language-neutral and exactly as specified here.
5. With `document_language: en` and a Chinese conversation, converse in Chinese but persist English project knowledge. With `document_language: zh-CN` and an English conversation, converse in English but persist Simplified Chinese project knowledge.
6. Use the committed workflow and Coding Rules snapshot loaded at Feature start. If this Feature changes workflow rules, those changes govern the next Feature, not the Feature implementing them.

## Global rules

1. Do not expand scope without approval. Implement only the current Feature and its acceptance criteria.
2. Stop on material ambiguity. Record the question in Progress and ask instead of guessing.
3. Never mark a Feature `done` without explicit human acceptance, a passing fresh-context scan, and completion evidence.
4. Do not work on `main` or `master`.
5. Do not run force operations, `reset --hard`, history rewriting, or other destructive Git operations.
6. Prefix every placeholder with `_placeholder_` and register it in Feature notes.
7. Escape double quotes in Feature JSON strings and validate every written index or detail with `python3 -m json.tool <path> > /dev/null`.
8. Use the three-file structure: the lightweight index at `docs/feature-list.json`, details at `docs/features/F0XX.json`, and the synchronization-owned revision log at `docs/feature-list-revisions.json`. This workflow does not read or write the revision log.

## Stage 0: preflight and exit report

**Entry:** the user requests the next, current, or specified Feature.

**Output:** one eligible Feature, a ready environment, a committed rule snapshot, and fixed exit evidence.

1. Read `docs/feature-list.json`; if absent, route to `generate-feature-list` and stop.
2. If any Feature is `in_progress`, ask whether to resume it or abandon it before selecting another.
3. Use a user-specified ID, or select the first `pending` Feature whose dependencies are all `done`. If none is eligible, explain whether work is complete, blocked, or obsolete.
4. If `estimated_scope` is `large`, stop and require decomposition through `sync-feature-list`.
5. Run `git status` and `git branch --show-current`. Stop on `main` or `master`. For a dirty tree, ask whether the user will commit, stash, or restore; do not perform the choice without authorization.
6. Load required context:
   - `docs/progress.md`, when present;
   - the selected `docs/features/F0XX.json` in full;
   - `docs/product.md` and every Product module relevant to the Feature;
   - relevant `docs/coding_rules.md` sections and every imported engine/language rule needed by the Feature;
   - the `notes` of every completed dependency Feature.
7. Treat the committed files now loaded as the current Feature's rule snapshot.
8. Report the Feature ID/title, dependencies, and branch, then emit this fixed block in the current conversation language. Rule quotations and line numbers must be real:

```text
=== Stage 0 exit report ===
Read:
- docs/coding_rules.md, including referenced engine and language rules ✓
- docs/product.md overview ✓
- docs/product/<relevant-module>.md ✓
- docs/progress.md, if present ✓

Rules directly relevant to this Feature, with verbatim text and line numbers:
- <file> L<line>: "<verbatim rule>"
- <file> L<line>: "<verbatim rule>"

Rules this Feature is most likely to violate or must handle carefully:
<one or two concrete sentences>
```

Do not enter Stage 1 before emitting this report.

## Stage 1: resource and dependency preflight

**Entry:** Stage 0 completed.

**Output:** a start-work checklist explicitly approved by the user.

1. List every required image, audio file, font, configuration dataset, third-party dependency, and editor/engine action the AI cannot perform.
2. Mark each resource:
   - available: record path and use;
   - missing or uncertain: offer pausing for the user, using a visible `_placeholder_` recorded in notes, or skipping this Feature and returning to Stage 0.
3. List every file expected to be added or modified and whether the change is focused or a rewrite. Flag unexpected changes outside the core area.
4. Estimate commit count and purpose.
5. Present the checklist and wait for explicit approval. Do not modify implementation files before approval.

## Stage 2: mark work started

**Entry:** the user approved Stage 1.

**Output:** index status is `in_progress`; Progress records the start.

1. Change only the index status to `in_progress`.
2. Archive prior Current work and Progress under History with a timestamp; set Current work to the Feature; reset Progress to `Started at <ISO 8601 timestamp>`; preserve Context notes.
3. A `chore(F0XX): start feature` commit is optional and omitted by default unless the maintainer prefers it.

## Stage 3: implement

**Entry:** Stage 2 completed.

**Output:** focused changes, durable progress, and atomic commits.

1. Follow the Stage 0 Coding Rules snapshot. Stop on conflict instead of silently deviating.
2. Append a Progress entry after every meaningful substep and record blockers before asking the user.
3. Use one commit for a simple Feature or multiple coherent commits for broader work. Do not create one oversized commit.
4. Commit format:

```text
<type>(F0XX): <imperative summary>

<optional two-to-four-line explanation>
<cross-Feature files, placeholders, and intentionally omitted edges when applicable>
```

Allowed types are `feat`, `fix`, `refactor`, `test`, `docs`, and `chore`.

5. Before each commit, confirm the branch is not `main` or `master`, stage explicit paths rather than `git add .` or `git add -A`, and verify the staged list matches the commit purpose.
6. At implementation completion report files, commit hashes/subjects, acceptance-criterion coverage, assumptions, intentionally omitted behavior, and placeholders.

## Stage 4: self-verification

**Entry:** implementation completed.

**Output:** automated results and a human-verification checklist.

1. Classify each acceptance criterion as machine-verifiable or human-verifiable.
2. Read and synchronously run `static_check_cmd` from `docs/methodology-config.json`. Use its configured timeout for commands that can hang; never treat a background process as completed verification.
3. On any automated failure, return to Stage 3 and repair it; do not enter Stage 5.
4. Give one concrete human-verification instruction per observable criterion and ask the user to report every result.

Automated evidence never replaces human acceptance.

## Stage 5: human acceptance

**Entry:** Stage 4 supplied the checklist.

**Output:** an explicit human decision.

1. Wait for the user.
2. Explicit confirmation of all items enters Stage 6.
3. A failed item is recorded in Progress; return to Stage 3, preserve existing commits and `in_progress`, then repeat verification after repair.
4. For an ambiguous response, ask whether any criterion remains unmet. Record an explicitly accepted minor deferral in notes; repair a material gap.

Never infer acceptance from tests or confidence.

## Stage 6: fresh-context code-smell scan

**Entry:** explicit Stage 5 acceptance.

**Output:** independent JSON review, zero remaining blockers, durable suggestions, and exact gate evidence.

This stage is mandatory for every Feature, including documentation-only work.

### 6.1 Independent review

Delegate to a fresh-context agent. It must read the complete Coding Rules, inspect every file changed since Feature start, make no edits or Git writes, and check:

- files longer than roughly 300 lines;
- duplicated knowledge or rules;
- type dispatch owned by the wrong component;
- magic numbers or strings;
- constants/enums duplicated across three or more files;
- God Object growth;
- engine/language anti-patterns;
- presentation/domain coupling;
- comments that restate what rather than why;
- evidence of a defect needing two or more repair attempts.

Severity is stable: `must_fix` blocks later work or is a recurring-defect source; `suggest` may worsen with growth but does not block; `acceptable` is disproportionate to repair.

The reviewer returns only valid JSON:

```json
{
  "must_fix": [
    {"file":"<path>","line":123,"smell":"<diagnosis>","rule_ref":"coding_rules.md L<line>","fix_suggestion":"<repair>"}
  ],
  "suggest": [
    {"file":"<path>","smell":"<diagnosis>","note":"<future guidance>"}
  ],
  "acceptable": [
    {"file":"<path>","smell":"<diagnosis>","reason":"<why repair is disproportionate>"}
  ]
}
```

### 6.2 Process review

1. Repair every `must_fix` in the main context, using an independent focused `refactor(F0XX): <summary>` commit for each finding, and rerun `static_check_cmd`.
2. A repair must not silently change accepted behavior. If it may, ask the user and return to Stage 3, then repeat Stages 4–6.
3. Re-scan until `must_fix` is empty.
4. Append each `suggest` to Feature notes with a `TODO` prefix. Summarize `acceptable` only in the report.

### 6.3 Report and evidence

```text
## Code-smell scan report (F0XX)

### Fixed now (must_fix)
- <finding, rule, repair commit>

### Recorded in notes (suggest)
- <finding and future guidance>

### Accepted without change (acceptable)
- <finding and reason>

Code smell scan: pass (feature: F0XX, must_fix: 0, suggest: <N>, acceptable: <M>)
```

The final line is stable Hook-compatible evidence. If review fails, times out, returns invalid JSON, or cannot read rules, stop; never bypass the gate.

Even when all three arrays are empty, emit the report and final evidence line and state that no code smells were found.

## Stage 7: mark complete

**Entry:** Feature-specific `Code smell scan: pass` evidence with `must_fix: 0`.

**Output:** `done` status, durable notes, archived Progress, and completion commit.

1. Set index `status` to `done` and `completed_at` to the current ISO 8601 timestamp.
2. Append implementation decisions, placeholders/replacement guidance, omitted edges, handoff information, and `TODO`-prefixed Stage 6 suggestions to the detail `notes`.
3. Archive Current work and Progress under History with completion time; clear active sections.
4. Commit explicit paths with:

```text
chore(F0XX): mark feature as done

Acceptance criteria all verified by human review.
Code smell scan: pass (feature: F0XX, must_fix: 0, suggest: <N>, acceptable: <M>)
<optional durable completion note>
```

5. Report the Feature, every Feature commit, acceptance coverage, placeholders, and TODOs.
6. Do not push, switch branches, merge, or operate on `main` or `master`.

## Stage 8: handoff

**Entry:** Stage 7 completed.

**Output:** next eligible Feature and choices.

1. Read the latest lightweight index and find the first `pending` Feature whose dependencies are all `done`.
2. Report the completed Feature, commit count, placeholder count, next eligible Feature, and reasonable choices such as continuing, broader review, or a maintainer-controlled milestone.
3. Stop. Start the next Feature only when the user has explicitly authorized continuation.

## Git permissions

Allowed on a work branch without new confirmation: read-only Git commands, explicit-path `git add`, and workflow-compliant commits.

Require explicit authorization: create/switch branches; merge, rebase, or cherry-pick; delete branches/tags; restore or stash.

Prohibited: force push, `reset --hard`, direct `.git/` edits, history rewriting, commits/merges/pushes on `main` or `master`, and automatic push.

If Git fails, stop and report the original error without unapproved recovery.

## Exception handling

| Condition | Required response |
|---|---|
| Acceptance criteria are ambiguous or contradictory | Propose revision through `sync-feature-list`; do not reinterpret them here |
| A completed dependency is materially incomplete | Report the gap and ask whether to repair, explicitly work around it, or pause |
| Implementation needs out-of-scope files | List files and reasons; ask whether to expand this Feature or create another |
| A file, command, test, or Git operation fails | Stop, preserve the original error, and use only workflow-defined safe repair |
| Context is close to exhaustion | Persist current state in Progress before handing off to a new session |
| The user requests unrelated work mid-Feature | Identify it as out of scope and propose another Feature |

## Workflow map

```text
Stage 0  Preflight and fixed exit report
   ↓
Stage 1  Resource/dependency checklist → human approval
   ↓
Stage 2  Mark in_progress and initialize Progress
   ↓
Stage 3  Implement with atomic commits
   ↓
Stage 4  Run static_check_cmd and prepare human checks
   ↓
Stage 5  Obtain explicit human acceptance
   ↓
Stage 6  Independent fresh-context scan → must_fix: 0 evidence
   ↓
Stage 7  Mark done and commit Hook-compatible evidence
   ↓
Stage 8  Hand off and stop unless continuation was pre-authorized
```
