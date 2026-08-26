# 03 · The eight-stage execute-next-feature loop

> This is the tool-independent specification for `execute-next-feature`. The Claude Code Skill and the agent-agnostic Prompt derive from the same behavior; only tool syntax and project-specific static-check configuration differ.

## Global rules

These rules apply in every stage:

1. **Do not expand scope without approval.** Implement only the current Feature and its acceptance criteria.
2. **Stop on material ambiguity.** Record the question in Progress and ask the user instead of guessing.
3. **An AI must not mark a Feature `done` on its own.** Completion requires explicit human acceptance in Stage 5, a passing fresh-context scan in Stage 6, and gate evidence in the Stage 7 commit.
4. **Do not work on `main` or `master`.** Every implementation commit belongs on a working branch.
5. **Do not run destructive Git operations.** Force operations, `reset --hard`, and history rewriting are prohibited.
6. **Make placeholders explicit.** Every placeholder uses the `_placeholder_` prefix and is recorded in the Feature notes.
7. **Keep Feature JSON valid.** JSON string values must escape double quotes as specified in [02-feature-list-schema.md](./02-feature-list-schema.md), and every write must be checked with `python3 -m json.tool <path> > /dev/null`.
8. **Use the committed rule snapshot from Feature start.** If the current Feature changes Yaya Loop workflow rules, those changes govern the next Feature; they do not retroactively change the stages or completion gates of the Feature implementing them.

---

## Stage 0: preflight and exit report

**Entry condition:** The user requests execution of the next, current, or specified Feature.

**Output:** One eligible Feature is selected, the environment and committed rule snapshot are ready, and the fixed exit report proves that relevant rules were read.

### Procedure

1. Read `docs/feature-list.json`. If it does not exist, tell the user to run `generate-feature-list` and stop.
2. Check for a Feature with `status = in_progress`. If one exists, ask whether to resume it or abandon it before selecting another.
3. Select the Feature:
   - If the user specified an ID, select it.
   - Otherwise, select the first `pending` Feature whose `depends_on` entries are all `done`.
   - If none is eligible, explain whether all work is complete, prerequisites are blocked, or remaining Features are obsolete.
4. Inspect `estimated_scope`. If it is `large`, stop and require decomposition through `sync-feature-list`.
5. Check Git state:
   - Stop on `main` or `master`.
   - If the worktree is dirty, ask the user to choose whether to commit, stash, or restore those changes. Do not continue before the choice is resolved.
6. Load only the required context:
   - `docs/progress.md`, if present
   - the complete selected detail file at `docs/features/F0XX.json`
   - the complete `docs/product.md` overview and relevant Product module
   - relevant sections of `docs/coding_rules.md` and any included engine or language rule files
   - the `notes` field of every dependency Feature
7. Treat the committed rules loaded at this point as the execution snapshot for the current Feature.
8. Emit the following report exactly in the current conversation language. The quoted rule text and source line numbers must be real; vague summaries do not satisfy the gate.

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

Stage 1 must not begin until this report has been emitted.

---

## Stage 1: resource and dependency preflight

**Entry condition:** Stage 0 is complete.

**Output:** A start-work checklist approved by the user.

### Procedure

1. List every required non-code resource: images, audio, fonts, configuration data, third-party libraries, and editor or engine actions that the AI cannot perform.
2. Classify each resource:
   - **Available:** record its path and intended use.
   - **Missing or uncertain:** offer three choices:
     1. pause until the user provides it
     2. continue with a visibly recognizable `_placeholder_` resource and record it in Feature notes
     3. skip this Feature and return to Stage 0
3. List every file expected to be added or modified and classify each modification as focused or a rewrite.
4. Identify changes outside the expected core area as a design warning.
5. Estimate the number and purpose of implementation commits.
6. Present the checklist and wait for explicit approval.

Do not modify implementation files before the user approves this checklist.

---

## Stage 2: mark work started

**Entry condition:** The user approved the Stage 1 checklist.

**Output:** The Feature is `in_progress`, and Progress records the start.

### Procedure

1. Change the Feature's index status to `in_progress`.
2. Update `docs/progress.md`:
   - archive any previous Current work and Progress content under History with a timestamp
   - set Current work to the current Feature ID and title
   - reset Progress and add `Started at <ISO 8601 timestamp>`
   - preserve Context notes
3. A `chore(F0XX): start feature` commit is optional and is omitted by default.

---

## Stage 3: implement

**Entry condition:** Stage 2 is complete.

**Output:** Focused implementation changes, durable progress notes, and one or more atomic commits.

### Procedure

1. Follow the Coding Rules snapshot loaded in Stage 0. If a rule conflicts with the Feature, stop and ask rather than silently deviating.
2. Update Progress after every meaningful substep. Record blockers before asking the user.
3. Keep commits atomic:
   - A simple Feature may use one implementation commit.
   - A broader Feature should separate coherent structures, wiring, and tests.
4. Use this commit format:

   ```text
   <type>(F0XX): <imperative summary>

   <optional two-to-four-line explanation>
   <list cross-Feature files, placeholders, or intentionally omitted edges when applicable>
   ```

   Valid types are `feat`, `fix`, `refactor`, `test`, `docs`, and `chore`.
5. Before each commit:
   - confirm the branch is not `main` or `master`
   - stage explicit paths; do not use `git add .` or `git add -A`
   - review the staged file list against the commit's purpose
6. At implementation completion, report:
   - files and their changes
   - commit hashes and first lines
   - how every acceptance criterion is satisfied
   - assumptions, intentionally omitted behavior, and placeholders

---

## Stage 4: self-verification

**Entry condition:** Stage 3 implementation is complete.

**Output:** Automated-verification results and a human-verification checklist.

### Procedure

1. Classify every acceptance criterion:
   - **Machine-verifiable:** compilation, type checking, lint, tests, or static checks.
   - **Human-verifiable:** observable behavior requiring product judgment.
2. Read `static_check_cmd` from `docs/methodology-config.json` and run it synchronously.
3. If a check can hang, wrap it in an explicit timeout. Do not treat a background process as completed verification.
4. If any automated check fails, return to Stage 3 and repair it; do not enter Stage 5.
5. Write one concrete human-verification instruction for each observable acceptance criterion.
6. Ask the user to report the result of every item.

Automated checks provide evidence, not human acceptance.

---

## Stage 5: human acceptance

**Entry condition:** Stage 4 completed and supplied a verification checklist.

**Output:** An explicit human decision for the observable acceptance criteria.

### Procedure

1. Wait for the user's result.
2. If the user explicitly confirms all items, enter Stage 6.
3. If an item fails, record it in Progress, return to Stage 3, preserve existing commits and `in_progress`, then repeat Stages 4 and 5 after repair.
4. If the response is ambiguous, ask whether any acceptance criterion remains unmet. Record an explicitly accepted minor deferral in notes; repair a material gap before completion.

An AI must never infer acceptance from passing tests or from its own confidence.

---

## Stage 6: fresh-context code-smell scan

**Entry condition:** The user explicitly accepted the Feature in Stage 5.

**Output:** A fresh-context JSON review, fixes for every blocking finding, recorded non-blocking suggestions, and exact completion-gate evidence.

This stage is mandatory even for small or documentation-only Features. Completion remains blocked while any `must_fix` finding exists.

### 6.1 Delegate the independent review

Use a fresh-context sub-agent or equivalent independent context. The reviewer must first read the complete project Coding Rules and must not modify files or perform Git writes.

Provide the reviewer with all files changed since Feature start and this checklist:

- files exceeding roughly 300 lines
- duplicated knowledge or business rules
- type dispatch in components that should not own type meaning
- magic numbers or strings
- shared enums or constants duplicated across three or more files
- God Object growth
- engine- or language-specific anti-patterns
- presentation and domain-logic coupling
- comments that restate what instead of explaining why
- evidence of a defect needing two or more repair attempts

Severity has stable meanings:

- `must_fix`: likely to cause later Features to fail, or already the source of a recurring defect
- `suggest`: likely to worsen as the project grows but not blocking today
- `acceptable`: a preference or tiny issue whose repair would add disproportionate complexity

The reviewer must return only valid JSON:

```json
{
  "must_fix": [
    {
      "file": "<path>",
      "line": 123,
      "smell": "<diagnosis>",
      "rule_ref": "coding_rules.md L<line>",
      "fix_suggestion": "<focused repair>"
    }
  ],
  "suggest": [
    {
      "file": "<path>",
      "smell": "<diagnosis>",
      "note": "<future guidance>"
    }
  ],
  "acceptable": [
    {
      "file": "<path>",
      "smell": "<diagnosis>",
      "reason": "<why repair is disproportionate>"
    }
  ]
}
```

### 6.2 Process the review

1. If `must_fix` is empty, continue to the report.
2. If `must_fix` is non-empty:
   - repair each finding in the main context
   - use a focused `refactor(F0XX): <summary>` commit for each coherent repair
   - rerun `static_check_cmd`
   - confirm that no blocking finding remains
3. Append every `suggest` item to Feature notes with a `TODO` prefix. Suggestions do not block completion.
4. Summarize `acceptable` items in the report without adding them to notes.

### 6.3 Report and gate evidence

```text
## Code-smell scan report (F0XX)

### Fixed now (must_fix)
- <finding, source rule, and repair commit>

### Recorded in notes (suggest)
- <finding and future guidance>

### Accepted without change (acceptable)
- <finding and reason>

Code smell scan: pass (feature: F0XX, must_fix: 0, suggest: <N>, acceptable: <M>)
```

The final line is a stable, Hook-compatible evidence string. Replace `F0XX` and the counts with the current Feature. `must_fix` records remaining blockers and must be `0` before Stage 7.

If independent review fails, times out, returns invalid JSON, or cannot read the rules, stop. Do not bypass Stage 6.

---

## Stage 7: mark complete

**Entry condition:** Stage 6 emitted Feature-specific `Code smell scan: pass` evidence with `must_fix: 0`.

**Output:** The Feature is `done`, durable notes and Progress are archived, and the completion commit carries gate evidence.

### Procedure

1. Update `docs/feature-list.json`:
   - set `status` to `done`
   - set `completed_at` to the current ISO 8601 timestamp
2. Append to `docs/features/F0XX.json` notes:
   - key implementation decisions
   - placeholder paths and replacement guidance
   - intentionally omitted edges
   - information needed by later Features
   - Stage 6 `suggest` items, prefixed with `TODO`
3. Archive Current work and Progress under History with the completion timestamp, then clear the active sections.
4. Create the completion commit with explicit paths and this message structure:

   ```text
   chore(F0XX): mark feature as done

   Acceptance criteria all verified by human review.
   Code smell scan: pass (feature: F0XX, must_fix: 0, suggest: <N>, acceptable: <M>)
   <optional durable completion note>
   ```

5. Report the Feature, all Feature commits, acceptance coverage, placeholders, and remaining TODOs.
6. Do not push, switch branches, merge, or operate on `main` or `master`.

---

## Stage 8: handoff

**Entry condition:** Stage 7 is complete.

**Output:** A handoff naming the next eligible Feature.

### Procedure

1. Read the latest lightweight index.
2. Find the first `pending` Feature whose dependencies are all `done`.
3. Report:
   - the completed Feature, commit count, and placeholder count
   - the next eligible Feature, if any
   - reasonable choices such as starting it, pausing for broader review, or creating a maintainer-controlled milestone
4. Stop. Do not start the next Feature automatically unless the user has explicitly authorized that continuation.

---

## Git permissions

### Allowed without additional confirmation on a working branch

- `git status`, `git log`, `git diff`, and `git branch --show-current`
- `git add <explicit-paths>`
- a workflow-compliant `git commit`

### Require explicit user authorization

- creating or switching branches
- merge, rebase, or cherry-pick
- deleting a branch or tag
- restore or stash operations that may discard or hide work

### Prohibited

- force-push of any kind
- `reset --hard`
- direct edits under `.git/`
- history-rewriting operations such as `filter-branch`
- commits, merges, or pushes on `main` or `master`
- automatic pushes

If a Git command fails, stop and report the original error. Do not attempt an unapproved recovery.

---

## Exception handling

| Condition | Required response |
| --- | --- |
| Acceptance criteria are ambiguous or contradictory | Propose a Feature revision through `sync-feature-list`; do not silently reinterpret them. |
| A completed dependency is materially incomplete | Report the gap and ask whether to repair it, work around it explicitly, or pause. |
| Implementation requires out-of-scope files | List the files and reasons, then ask whether to expand this Feature or create another. |
| A file, command, test, or Git operation fails | Stop, preserve the original error, and ask for direction when the workflow does not define a safe repair. |
| Context is close to exhaustion | Persist current state in Progress before handing off to a new session. |
| The user requests unrelated work mid-Feature | Identify it as out of scope and propose a separate Feature. |

---

## Quick reference

```text
Stage 0  Preflight and fixed exit report
   ↓
Stage 1  Resource and dependency checklist → human approval
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
Stage 8  Hand off and stop
```
