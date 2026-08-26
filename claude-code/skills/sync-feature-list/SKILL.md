---
name: sync-feature-list
description: Incrementally synchronize an existing three-file Feature plan with committed Product or Coding Rules changes by analyzing Git diffs. Use for Feature-list updates and realignment, not initial generation. English triggers: sync feature list, update tasks from Product, realign Feature plan. 中文触发：同步 feature-list、更新任务列表、重新对齐 feature-list。
---

# Synchronize Feature list

Run Feature-list synchronization as the seven-stage workflow defined below.

The core method is to identify source changes through Git diffs against a recorded anchor. Never infer historical change merely by comparing the current Product with the current Feature plan.

## Language and history contract

Before producing durable Feature content:

1. Read `document_language` from `docs/methodology-config.json`.
2. Resolve missing, invalid, or migration-sensitive configuration through `methodology/05-document-language.md` before writing Feature or revision files.
3. Use the language of the user's current message for conversation, questions, and the transient diff report.
4. Write every newly created or substantively revised Feature title, description, acceptance criterion, human-readable `source` fragment, note, revision `user_intent`, and revision `summary` in `document_language`.
5. Do not translate or rewrite existing completed history solely because its language differs from `document_language`. A `done` Feature is a historical record and changes only through the explicit new-Feature rules below.
6. Keep JSON keys, enum values, Feature IDs, dependency IDs, paths, commit hashes, timestamps, commands, evidence, and revision structure language-neutral and exactly as specified here.

With `document_language: en` and a Chinese conversation, discuss the diff in Chinese while writing new durable Feature prose in English. With `document_language: zh-CN` and an English conversation, discuss the diff in English while writing new durable Feature prose in Simplified Chinese. Existing completed prose remains unchanged in either case.

## Three-file structure

| Path | Role | Access pattern |
|---|---|---|
| `docs/feature-list.json` | Index: each Feature's `id`, `title`, `status`, `depends_on`, `estimated_scope`, and `completed_at` | Read the full index for scanning; update the index together with corresponding details |
| `docs/features/F0XX.json` | Detail: `id`, `description`, `acceptance_criteria`, `source`, and `notes` | Read details on demand; update each affected detail together with the index |
| `docs/feature-list-revisions.json` | Append-only `revision_log` | Read the last entry for the previous anchor; append one entry in Stage 5 |

## Source documents

Synchronization watches:

- `docs/product.md` for Product-wide intent, module inventory, dependencies, and direction;
- every `docs/product/NN-xxx.md` module file for behavior, data and state, UI, audio, values, acceptance, and edge cases;
- `docs/coding_rules.md` and its imported engine and language rules for collaboration, architecture, and technology constraints.

Between synchronizations, module files may be added, deleted, renamed—including numeric-prefix changes—or modified. The diff analysis must handle all four cases.

## Global invariants

1. Identify source changes from Git diff, not AI inference, so every update remains precise and traceable.
2. Treat the Feature plan as an append-only ledger. Removal changes status to `obsolete` or `obsolete_done`; revision of a `done` Feature creates a new Feature.
3. Never modify a `done` Feature's `id`, `description`, or `acceptance_criteria`. Do not revise its implemented behavior in place; use the status-specific new-Feature rules below. The only other permitted changes are the explicit removal status and note updates or source-path correction defined in Stage 4.
4. Never modify Feature-list files before explicit user confirmation in Stage 3.
5. Work only on a non-`main`, non-`master` branch. Before applying changes, the working tree must contain no unrelated modifications.
6. Never place an unescaped `"` inside a Feature-list JSON string. Escape it as `\"`, or use natural quotation marks appropriate to `document_language` when they cannot be mistaken for JSON delimiters.
7. After writing any Feature-list JSON, validate `docs/feature-list.json`, `docs/feature-list-revisions.json`, and every affected `docs/features/F0XX.json` with `python3 -m json.tool <path> > /dev/null`.

## Stage 0: preflight and anchor

**Entry:** the user invokes this workflow.

**Output:** a ready environment and an identified comparison anchor.

1. Check `docs/feature-list.json`.
   - If it does not exist, direct the user to `generate-feature-list` and stop.
   - If it exists, read the full index for status, dependency, and count fields. Read `docs/feature-list-revisions.json` when present; on first synchronization it may be absent. Read individual detail files only when Stage 2 mapping or Stage 4 changes require them.
2. Check Git.
   - On `main` or `master`, pause and ask the user to switch to a work branch.
   - If unrelated working-tree changes exist outside source Markdown, ask the user whether to commit, stash, or discard them. Never perform stash, restore, or discard without explicit confirmation.
   - Uncommitted source Markdown may be analyzed, but it must be committed separately before Stage 4 applies Feature-plan changes so the diff and next anchor remain meaningful.
3. Determine the anchor commit.
   - Prefer `synced_at_commit` from the last `revision_log` entry.
   - If absent, search Git history for the most recent commit touching `docs/feature-list.json` or `docs/features/`.
   - If none exists, use the commit where `docs/feature-list.json` first appeared.
   - If no anchor can be found, explain that the workflow must fall back to whole-document comparison and obtain confirmation before continuing.
4. Report the current branch, anchor hash/date/subject, and counts grouped by Feature status.

## Stage 1: user prior

**Entry:** Stage 0 passed.

**Output:** an optional statement of the user's main intent for this synchronization.

Ask the user to summarize the source-document change before reading the diff—for example, a new module, a revised scoring rule, or new pause-screen copy. Explain that this helps distinguish semantic changes from editorial changes. If the user asks you to inspect the diff without a prior, continue without one. Store the answer for Stage 2 and the durable revision entry.

## Stage 2: Git-diff analysis

**Entry:** Stage 1 finished or was skipped.

**Output:** a precise diff report; no files modified.

### 2.1 Collect the complete diff

Inspect committed changes from the anchor to `HEAD` and any remaining source working-tree changes. Cover all source paths and enable rename detection for module files:

```bash
git diff <anchor> HEAD -- docs/product.md
git diff HEAD -- docs/product.md

git diff --stat -M <anchor> HEAD -- docs/product/
git diff --name-status -M <anchor> HEAD -- docs/product/
git diff -M <anchor> HEAD -- docs/product/
git diff -M HEAD -- docs/product/

git diff <anchor> HEAD -- docs/coding_rules.md docs/coding-rules/
git diff HEAD -- docs/coding_rules.md docs/coding-rules/
```

`-M` is mandatory for module paths so a rename such as `02-foo.md` to `03-foo.md` is not misclassified as one deletion plus one addition.

### 2.2 Classify every change

Use the user prior and actual diff to classify every hunk:

- **Substantive addition:** a new Product rule, constraint, or module.
- **Substantive revision:** changed behavior, value, condition, or meaning.
- **Substantive removal:** removed behavior, newly explicit exclusion, or deleted module.
- **Editorial adjustment:** wording, formatting, typo, or pure rename with unchanged meaning. It produces no Feature change.

A path rename with unchanged content is editorial. A rename plus content change has both a path correction and the appropriate substantive classification.

### 2.3 Map changes to existing Features

Use each detail file's `source` to map additions, revisions, and removals:

- addition → propose one or more new Features;
- revision → identify every affected Feature ID;
- removal → identify every affected Feature ID.

For a module-file rename, identify every detail whose `source` uses the old path. A source-path correction is reported separately and is not itself a substantive Feature change.

### 2.4 Analyze downstream regression

For every substantively revised `done` Feature, list every Feature whose `depends_on` directly contains that ID. Explain that those implementations rely on the old behavior and ask whether explicit regression verification is required.

### 2.5 Report the diff

Render the report in the current conversation language while preserving these sections:

```markdown
## Diff report based on anchor `<hash>`

### Editorial adjustments — no Feature change
- <wording, formatting, typo, or pure rename>

### Source-path corrections
- `<old path>` → `<new path>`: affected Features <IDs>

### Substantive changes

#### Additions — N
1. Source: <path and section>
   Change: <brief explanation>
   Proposed action: add Feature <title>, depends on <IDs>

#### Revisions — N
1. Affected Feature: <ID and status>
   Change: <brief explanation>
   Proposed action: <status-dependent action>
   Downstream impact: <dependent Features that may need regression>

#### Removals — N
1. Affected Feature: <ID and status>
   Change: <brief explanation>
   Proposed action: <status-dependent action>

### Match with user prior
<what matched and what the diff revealed unexpectedly>

### Decisions required
- <each unresolved choice>
```

### 2.6 Stop before writing

Stage 2 only reports. Do not modify any file before Stage 3 confirmation.

## Stage 3: user review and decision

**Entry:** Stage 2 produced the report.

**Output:** an explicit decision for every proposed change.

Offer three choices:

1. Confirm all proposed actions and proceed.
2. Adjust named actions; revise the report and ask for confirmation again.
3. Cancel synchronization; stop without modifying files.

Never enter Stage 4 without explicit confirmation.

## Stage 4: apply confirmed changes

**Entry:** the user confirmed the final Stage 3 report, and source Markdown is committed separately.

**Output:** a consistent index and affected detail files. Every addition or revision must update the correct sides together.

### Field ownership

| Field | Location |
|---|---|
| `id` | index and detail |
| `title`, `status`, `depends_on`, `estimated_scope`, `completed_at` | index only |
| `description`, `acceptance_criteria`, `source`, `notes` | detail only |

### Additions

- Append `{id, title, status, depends_on, estimated_scope, completed_at}` to the index and create the matching `{id, description, acceptance_criteria, source, notes}` detail.
- Use the next never-used ID after the highest historical ID. Never reuse an ID left by an obsolete Feature.
- Initialize `status` to `pending`, `completed_at` to `null`, and detail `notes` to `""`.
- When a Feature expands a capability supplied by a `done` Feature, say so in its description.
- Point `source` to the precise module path and section.
- Write all new human-readable values in `document_language`.

### Removals

| Current status | Confirmed action |
|---|---|
| `pending` | Set index `status` to `obsolete`; append a localized timestamped removal reason to detail `notes` |
| `in_progress` | Set index `status` to `obsolete`; append the reason; warn that written code may require an explicitly authorized rollback |
| `done` | Set index `status` to `obsolete_done`; append a localized timestamped removal reason to detail `notes`; preserve `id`, `description`, and `acceptance_criteria`; append a new Feature that removes the implemented behavior, with dependencies chosen from actual impact |
| `obsolete` or `obsolete_done` | Keep status unchanged; append a localized note that exclusion was confirmed again |

Do not translate or substantively rewrite the removed `done` Feature. Its status transition and removal note record the confirmed Product deletion; the new removal Feature carries the implementation work.

### Revisions

| Current status | Confirmed action |
|---|---|
| `pending` | Update detail `description` and `acceptance_criteria`; append a localized timestamped revision note; change index `title` only when the title is affected |
| `in_progress` | Apply the `pending` action and warn that current implementation may need adjustment |
| `done` | Do not modify the original index entry or detail. Append a new Feature that revises the implementation for the new Product rule, depends on the original ID, and states the new behavior in its acceptance criteria |
| `obsolete` or `obsolete_done` | Normally do nothing. If the user wants reactivation, require an explicit decision and append a new Feature |

### Source-path corrections

- Update only the detail `source` path for every affected Feature, including `done` history, so references continue to resolve after a module rename.
- Record every old-to-new mapping in `source_path_updates`.
- Do not treat path correction as substantive revision.

### Downstream regression

For each dependent Feature identified in Stage 2.4:

- when regression is required, append a Feature named for verifying the dependent behavior after the new revision Feature and depend on that revision Feature;
- when regression is declined, record the confirmed dependent IDs in the new revision Feature's `notes`.

## Stage 5: update metadata, validate, and commit

**Entry:** Stage 4 completed.

**Output:** updated metadata, one appended revision entry, validation evidence, and a Git commit.

1. Update `meta.total_features` and set `meta.generated_at` to the synchronization timestamp. Keep `meta.generated_from` exactly:

```json
["docs/product.md", "docs/product/**/*.md", "docs/coding_rules.md"]
```

2. Append this stable object to `docs/feature-list-revisions.json`; do not write it into index metadata:

```json
{
  "revised_at": "<ISO 8601 timestamp>",
  "synced_at_commit": "<HEAD source-document commit hash>",
  "anchor_commit": "<comparison anchor commit hash>",
  "user_intent": "<localized Stage 1 prior, or null>",
  "summary": "<localized one-sentence revision summary>",
  "added": ["F0XX", "F0YY"],
  "obsoleted": ["F0AA"],
  "revised_via_new_feature": [
    {"original": "F0BB", "regression": "F0CC"}
  ],
  "source_path_updates": [
    {"feature": "F005", "from": "product/02-foo.md", "to": "product/03-foo.md"}
  ],
  "depends_on_warnings": ["F0DD", "F0EE"]
}
```

`synced_at_commit` is the next run's anchor and is mandatory. It must identify the committed source-document state analyzed by this synchronization. `source_path_updates` preserves rename traceability, including mappings for immutable completed history.

3. Complete this self-check; return to Stage 4 if any item fails:

- [ ] No Feature entry or detail file was physically deleted.
- [ ] No `done` Feature's `id`, `description`, or `acceptance_criteria` was modified; any removal status/note update or source-path correction matches the explicit Stage 4 rules.
- [ ] Index IDs and `docs/features/F*.json` filename stems match one to one.
- [ ] Every new ID was never used before.
- [ ] Every `depends_on` ID exists.
- [ ] No dependency points to `obsolete` or `obsolete_done`; any unavoidable case was raised before writing.
- [ ] Every non-historical detail `source` resolves to an existing module file and section after renames.
- [ ] The last revision entry contains the correct `synced_at_commit`.
- [ ] `meta.total_features`, index length, and detail-file count are equal.
- [ ] The index, revision log, and every affected detail pass `python3 -m json.tool`.

4. Stage and commit only Feature-plan files:

```text
git add docs/feature-list.json docs/feature-list-revisions.json docs/features/
git commit -m "chore(sync): update feature-list per docs revision

Anchor: <short anchor hash>
Added: <N> features
Obsoleted: <N> features
Revised via new feature: <N> features

<localized one-sentence summary>"
```

Source changes must be in a separate earlier commit. If they are still uncommitted, pause before Stage 4 and ask the user to commit them so `synced_at_commit` can identify the analyzed source state.

5. Never push.

## Stage 6: handoff

**Entry:** Stage 5 completed.

**Output:** a synchronization summary in the current conversation language.

Report:

- the anchor hash used for analysis;
- counts of added, obsoleted, regression, and source-path-update records;
- the next executable Feature, when one exists;
- rollback warnings for obsolete in-progress work and every outstanding regression concern.

Do not automatically start another Feature. Wait for the user's instruction.

## Exception handling

| Condition | Required response |
|---|---|
| No anchor can be found | Offer whole-document comparison, disclose reduced precision, and require confirmation |
| More than about 50% of source lines changed, or more than three module files were added or removed | Pause and recommend smaller synchronizations or explicit `generate-feature-list` regeneration |
| Diff and user prior conflict materially | Pause, enumerate mismatches, and ask the user to check for unintended source edits |
| Product module inventory and actual files differ | Pause, list the discrepancy, and require Product repair rather than guessing |
| Any index, detail, or revision JSON is invalid, including unescaped quotes | Stop and report the original error; do not auto-repair the data |
| Stage 4 fails while writing | Stop and explain that recovery requires explicit user authorization; do not run restore automatically |
| Any Git command fails | Stop and report the original error; do not attempt automatic repair |

## Git boundaries

- Allowed on a work branch: `git diff`, `git log`, staging only `docs/feature-list.json`, `docs/feature-list-revisions.json`, and `docs/features/`, then the synchronization commit.
- Require explicit confirmation: switching branches, stash, restore, or discarding changes.
- Forbidden: force operations, `reset --hard`, work on `main` or `master`, and push.

## Workflow map

```text
Stage 0: preflight and anchor
    ↓
Stage 1: optional user prior
    ↓
Stage 2: Git-diff analysis and report
    ↓
Stage 3: explicit user decision ── rejected or adjusted → revise Stage 2 report
    ↓
Stage 4: apply confirmed index/detail changes
    ↓
Stage 5: update metadata and revision log, validate, commit
    ↓
Stage 6: summarize and wait
```
