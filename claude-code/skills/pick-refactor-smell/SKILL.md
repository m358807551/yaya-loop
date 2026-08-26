---
name: pick-refactor-smell
description: Scan durable Feature notes for unresolved code smells, rank them with the fixed high/medium/low rubric, recommend exactly one candidate, and hand the user's choice to Plan mode. This workflow never edits or commits. English triggers: pick a smell to refactor, scan suggestions, find refactor TODOs. 中文触发：挑一个坏味道重构、扫一下 suggest、看看 notes 里的重构待办。
---

# Pick one refactor smell

Use this three-stage workflow to scan, rank, and select one unresolved code smell from Feature notes, then hand the selected problem to Plan mode.

## Language contract

1. Read `document_language` from `docs/methodology-config.json`. Resolve missing, invalid, or migration-sensitive configuration through `methodology/05-document-language.md` before proposing durable project notes.
2. Use the language of the user's current message for questions, ranking explanations, recommendations, and the transient report.
3. Preserve every extracted note excerpt verbatim even when it uses another language. Never translate or rewrite historical Feature notes merely for this report.
4. This selector writes no files. If the downstream refactor later records a durable Feature note, TODO, acceptance record, or Progress entry, that new prose must use `document_language`.
5. Keep Feature IDs, paths, `TODO`, `suggest`, severity thresholds, numeric scores, commands, and workflow names stable.

With `document_language: en` and a Chinese conversation, discuss candidates in Chinese, preserve original excerpts, and require any later durable note to be English. With `document_language: zh-CN` and an English conversation, discuss candidates in English and require later durable notes to be Simplified Chinese.

## Scope

- Use this workflow when the user wants to refactor but does not know which recorded smell to choose.
- Use it with a Feature or category filter when the user asks to inspect only a subset, such as one Feature or cross-file smells.
- If the user already knows the exact smell, skip selection and enter Plan mode for that smell.
- If the problem comes from an external observation or bug report rather than Feature notes, skip this workflow and enter Plan mode directly.

## Global rules

1. Discover and select only. Do not write code, modify files, or commit. After selection, announce the Plan-mode handoff and stop.
2. Apply the fixed rubric exactly; do not improvise severity.
3. Prefer coverage to a short list. Do not hide important candidates merely to simplify the report.
4. Do not invoke another Skill. The user's next instruction controls the downstream refactor.

## Stage 1: scan

**Entry:** the user invokes this workflow.

**Output:** an unranked candidate list.

1. Check `docs/features/`. If absent, direct the user to `generate-feature-list` and stop.
2. Read every `docs/features/F*.json` and extract the `notes` field. Read `docs/feature-list.json` for titles, statuses, and reverse dependency analysis.
3. Split notes by line or sentence and extract any paragraph containing at least one stable marker:
   - `TODO`
   - `suggest`
   - `Code smell` or the Chinese equivalent `代码气味`
   - `refactor` or `重构`
   - `future`, `defer`, `未来`, or `推到`
4. Record for every candidate:
   - Feature ID;
   - concise Feature title from the index;
   - a verbatim excerpt of at most 200 characters;
   - code file paths named in the note, when any.
5. If no candidate exists, report in the current conversation language that Feature notes contain no unresolved smell and that the user may describe an external observation directly. Stop before Stage 2.

## Stage 2: rank with the fixed rubric

**Entry:** Stage 1 found at least one candidate.

**Output:** candidates grouped and ordered by stable severity.

### High severity — red

A candidate is high when any condition holds:

- it affects at least three files, counted from named paths plus concrete impact analysis;
- notes say it caused a bug, pitfall, repeated repair, `BUG`, or `bug`;
- it blocks at least two pending Features, determined by reverse lookup of index `depends_on`.

### Medium severity — yellow

When no high condition applies, a candidate is medium when any condition holds:

- it is local to one file but harms maintainability, such as hardcoded constants or an SRP/DRY violation;
- a rule or pattern is duplicated in two places, including shared constants coupled across files;
- naming or responsibility is confusing, such as one Boolean controlling two meanings.

### Low severity — green

Every other candidate is low, including:

- style preferences such as dictionary-driven code versus several constants;
- tiny improvements;
- findings explicitly resolved or superseded by a later Feature.

### Ranking adjustments

- Score multiple candidates from the same Feature independently.
- When candidates from different Features reference the same file, label them `same-file accumulation` and increase their priority within the applicable severity.
- When notes define a strong follow-up chain, list the dependency explicitly.

## Stage 3: report, recommend, and stop

**Entry:** Stage 2 ranked the candidates.

**Output:** one report, exactly one recommendation, and a user choice.

Render localized headings and explanations in the current conversation language while preserving this structure:

```markdown
## Code-smell scan report — N candidates

### High severity — M
1. **F0XX: <title>** | Files: `path`
   Excerpt: <verbatim excerpt, at most 200 characters>
   Reason: <the exact rubric condition>

### Medium severity — K
2. **F0YY: <title>** | Files: `path`
   Excerpt: <verbatim excerpt>
   Reason: <the exact rubric condition>

### Low severity — L
3. **F0ZZ: <title>** | Files: `path`
   Excerpt: <verbatim excerpt>
   Reason: <the exact rubric condition>

### Recommendation

Refactor **F0XX: <title>** first.
Reason: <one comparative sentence explaining why it outranks the other candidates>

Next: enter Plan mode and ask to refactor F0XX.
```

Number continuously across all three severity groups; do not reset numbering. Provide exactly one recommendation. Its reason must compare the chosen candidate with alternatives rather than merely praise it. Do not enter Plan mode, spawn an Explore agent, edit, or commit; wait for the user's choice.

## Response routing

| User response | Action |
|---|---|
| Selects an ID, item number, or the recommendation | Tell the user to enter Plan mode or ask directly to start planning that refactor; then stop |
| Requests complete notes for F0YY | Read and show `docs/features/F0YY.json` notes verbatim, then ask whether to select it |
| Requests another scan filtered to category X | Re-run Stages 1–3 with X as the filter |
| Declines all candidates | Confirm that no refactor will be started and stop |
| Gives an ambiguous answer | Ask whether to use the single recommendation or choose another candidate; never assume |

## Relationship to other workflows

- This is a selection entry point; the next user instruction determines the downstream Plan workflow.
- Do not invoke `generate-feature-list`, `sync-feature-list`, or `execute-next-feature` from this workflow.
- `generate-feature-list` creates the initial plan; `sync-feature-list` synchronizes Product changes; `execute-next-feature` implements pending Features rather than revisiting smells left by completed work.
- Actual refactoring uses Plan mode because exploration, affected files, design, verification, and commit decomposition depend on the selected problem.

## Exception handling

| Condition | Required response |
|---|---|
| `docs/features/` is absent | Direct the user to `generate-feature-list` and stop |
| Any `docs/features/F*.json` is invalid | Report the exact path and parse error; stop until the user repairs it |
| No note matches | Report a clean smell backlog and stop |
| More than 15 candidates match | Offer high severity plus the top three medium candidates first and follow the user's preference |
| The user's selection is ambiguous | Ask whether to use the recommendation or another candidate |
