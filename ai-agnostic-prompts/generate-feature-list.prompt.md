# Generate Feature list · portable prompt

> Use this workflow to generate an initial Feature plan or a user-confirmed complete replacement. Use `sync-feature-list` for incremental Product changes. English triggers: generate feature list, initialize task list, decompose the product. 中文触发：生成 feature-list、初始化任务列表、拆解产品功能。
>
> Copy everything from `# Generate Feature list` onward into your AI coding agent. It is behaviorally identical to the native Claude Code Skill.

---

# Generate Feature list

## Purpose and routing boundary

Use this workflow only when:

- `docs/feature-list.json` does not exist and the project needs its first Feature plan; or
- the user explicitly requests a complete replacement of the existing Feature plan.

For every incremental Product change, use `sync-feature-list` instead.

If `docs/feature-list.json` already exists and the user has not explicitly authorized replacement, explain the choice between incremental synchronization and complete regeneration, then wait for confirmation. Never infer permission to discard an existing plan.

## Language contract

Before generating durable Feature content:

1. Read `document_language` from `docs/methodology-config.json`.
2. Resolve missing, invalid, or migration-sensitive configuration through `methodology/05-document-language.md` before writing any Feature files.
3. Use the language of the user's current message for conversation.
4. Write Feature titles, descriptions, acceptance criteria, human-readable `source` fragments, meta notes, and Feature notes in `document_language`.
5. Keep JSON keys, enum values, Feature IDs, dependency IDs, scopes, timestamps, filenames, paths, commands, and structural validation language-neutral and exactly as specified here.

With `document_language: en` and a Chinese conversation, discuss the plan in Chinese but write Feature prose in English. With `document_language: zh-CN` and an English conversation, discuss the plan in English but write Feature prose in Simplified Chinese.

## Three-file output structure

Generate all three artifact types together:

| Path | Content |
|---|---|
| `docs/feature-list.json` | Lightweight index containing `meta` and each Feature's `id`, `title`, `status`, `depends_on`, `estimated_scope`, and `completed_at` |
| `docs/features/F0XX.json` | One detail file per Feature containing `id`, `description`, `acceptance_criteria`, `source`, and `notes` |
| `docs/feature-list-revisions.json` | Initial empty revision log: `{"revision_log": []}` |

When the user explicitly confirms complete regeneration, remove every stale `docs/features/F*.json` detail before writing the replacement set so old data cannot contaminate the new index. Resolve and report the exact files before removing them; do not use an unresolved or broad destructive glob.

## Required inputs

Read every relevant input before planning:

| Path | Role |
|---|---|
| `docs/product.md` | Product positioning, users, core loop, module inventory, module dependencies, and Product-wide direction |
| `docs/product/NN-xxx.md` | Complete module behavior, data and state, UI, audio, values, acceptance criteria, and edge cases |
| `docs/coding_rules.md` | Collaboration contract, architecture rules, and imported engine and language constraints |
| `docs/coding-rules/engine-rules.md` | Engine rules imported by `docs/coding_rules.md`, when present |
| `docs/coding-rules/language-rules.md` | Language rules imported by `docs/coding_rules.md`, when present |

Read in this order:

1. Read `docs/product.md` to obtain the module inventory and dependency graph.
2. Read every `docs/product/*.md` module file in the topological order declared by the Product overview.
3. Read `docs/coding_rules.md` and every engine or language rule file it imports. Treat architecture and technology constraints as hard constraints on granularity and ordering.

If the Product module inventory and the actual module files differ in number, identity, or naming, stop and report the exact mismatch. Do not guess or generate files until the inconsistency is resolved.

## Decomposition rules

1. **Each Feature must be the smallest independently verifiable complete behavior.** Describe what a user can do or what observable result the system produces, not an implementation class or internal layer.
2. **Order by strict dependencies.** A Feature may depend only on earlier Feature IDs. The first Feature must establish runnable infrastructure and must not depend on Product behavior.
3. **Follow module dependencies.** If module A depends on module B, plan B's core Features before A's dependent Features.
4. **Follow architecture constraints.** When Coding Rules require data/presentation separation or pure core rules, schedule data and rule behavior before its presentation behavior.
5. **Fit one AI session.** `small` and `medium` are allowed; any proposed `large` Feature must be split before output.
6. **Do not overdesign.** Include only behavior committed in Product. Exclude explicitly out-of-scope behavior and edge cases that Product explicitly chooses not to handle.
7. **Describe what plus observable acceptance, never how.** Every acceptance criterion must state how a human or automated check can verify the result; reject adjectives such as “correct” without an observable condition.
8. **Prefer complete coverage to elegance.** Every committed module behavior and numeric rule needs corresponding Feature coverage.
9. **Make `source` precise.** Point to the module path and section, for example `product/03-combat.md#Numeric rules`; use `infrastructure` only for infrastructure Features.

## Stable JSON schemas

### Index: `docs/feature-list.json`

```json
{
  "meta": {
    "generated_from": [
      "docs/product.md",
      "docs/product/**/*.md",
      "docs/coding_rules.md"
    ],
    "generated_at": "<ISO 8601 timestamp>",
    "total_features": 1,
    "details_dir": "docs/features/",
    "revisions_file": "docs/feature-list-revisions.json",
    "notes": "<decomposition summary in document_language>"
  },
  "features": [
    {
      "id": "F001",
      "title": "<verb phrase in document_language>",
      "status": "pending",
      "depends_on": [],
      "estimated_scope": "small",
      "completed_at": null
    }
  ]
}
```

`estimated_scope` may be `small` or `medium` in final output. `large` is a diagnostic value that requires further decomposition and must never remain in generated output.

### Detail: `docs/features/F0XX.json`

```json
{
  "id": "F001",
  "description": "<two to four sentences in document_language describing observable outcomes>",
  "acceptance_criteria": [
    "<specific observable condition in document_language>",
    "<specific observable condition in document_language>"
  ],
  "source": "<module path and localized section, or infrastructure>",
  "notes": ""
}
```

### Revision log: `docs/feature-list-revisions.json`

```json
{
  "revision_log": []
}
```

## Field invariants

- `id`: start at `F001`, increase sequentially, and preserve three digits. Index IDs, detail IDs, and detail filename stems must match one to one.
- `depends_on`: include only strict prerequisite Feature IDs. Store it only in the index. The infrastructure Feature has an empty array.
- `acceptance_criteria`: use concrete manual, visual, or automated checks; do not use adjective-only claims.
- `source`: point to an existing Product module and section; use `infrastructure` for the infrastructure Feature. For the uncommon cross-module case, identify the primary module.
- `estimated_scope`: store only in the index. `small` fits one implementation and verification session; `medium` fits one session with multiple debugging passes; split every `large` proposal.
- `status`: initialize every Feature to `pending`. Other stable values—`in_progress`, `done`, `obsolete`, `obsolete_done`, and `blocked`—belong to execution and synchronization workflows. Store status only in the index.
- `completed_at`: initialize every value to `null` and store it only in the index.
- `notes`: initialize every detail value to an empty string and store it only in detail files.
- `revision_log`: initialize it to an empty array and store it only in `docs/feature-list-revisions.json`.

Never place an unescaped `"` inside a JSON string. Escape embedded ASCII double quotes as `\"`, or use natural quotation marks appropriate to `document_language` when they cannot be mistaken for JSON delimiters.

Validate the index, every detail file, and the revision log with:

`python3 -m json.tool <path> > /dev/null`

## Mandatory self-check

Before reporting completion, verify every item:

- [ ] The first Feature is runnable infrastructure with no Product-behavior dependency.
- [ ] No `depends_on` entry points to a later Feature ID.
- [ ] No final `estimated_scope` is `large`.
- [ ] Every committed core behavior in every Product module has Feature coverage.
- [ ] No explicitly excluded or deliberately unhandled behavior appears in the plan.
- [ ] Feature order reflects Coding Rules such as data/presentation separation and pure core rules.
- [ ] Every detail `source` resolves to an existing Product module and section, or is exactly `infrastructure`.
- [ ] Every referenced dependency ID exists.
- [ ] Every initial status is `pending`, every `completed_at` is `null`, and every detail `notes` is `""`.
- [ ] `docs/feature-list-revisions.json` is exactly the empty revision-log structure.
- [ ] The set of index IDs equals the set of `docs/features/F*.json` filename stems and equals `meta.total_features` in count.
- [ ] The index, every detail file, and the revision log pass JSON parsing without unescaped double quotes.

Fix every failed check before presenting the generated files as complete.

## Output sequence

1. After reading all inputs, give the user a plan summary of no more than six sentences. State the decomposition order and layers, total Feature count, approximate count per module, and every Product contradiction or ambiguity.
2. If any question remains, stop and wait for the user's answer. Do not write JSON.
3. When there is no unresolved question, write the index, every detail file, and the empty revision log together. Create `docs/features/` if necessary.
4. Run the complete self-check and JSON validation. Only after all checks pass, report the generated files and identify the first executable Feature.
5. Do not implement or start the first Feature. Execution belongs to `execute-next-feature`.
