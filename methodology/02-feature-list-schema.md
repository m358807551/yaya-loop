# 02 · Feature-list three-file schema

## Three-file structure

```text
docs/
├── feature-list.json              ← Lightweight index loaded each session
├── features/
│   ├── F001.json                  ← Detail loaded on demand
│   ├── F002.json
│   └── ...
└── feature-list-revisions.json    ← Revision log maintained by sync-feature-list
```

The split keeps the main index small—five or six fields per Feature—so an agent can scan hundreds of Features. Acceptance criteria and other details are loaded only for the current work, while the separate revision log preserves Product evolution.

Human-readable JSON values must follow `document_language`. Keys, schema structure, enum values, Feature IDs, paths, and timestamps must remain stable as defined in [05-document-language.md](./05-document-language.md).

---

## File 1: `docs/feature-list.json`

```json
{
  "meta": {
    "generated_from": [
      "docs/product.md",
      "docs/product/**/*.md",
      "docs/coding_rules.md"
    ],
    "generated_at": "2026-05-23T05:46:48Z",
    "total_features": 2,
    "details_dir": "docs/features/",
    "revisions_file": "docs/feature-list-revisions.json",
    "notes": "Decompose in module dependency order, then deliver data, rules, and presentation or interaction slices within each module."
  },
  "features": [
    {
      "id": "F001",
      "title": "Create the project shell and open an empty main window",
      "status": "done",
      "depends_on": [],
      "estimated_scope": "small",
      "completed_at": "2026-05-16T10:30:00Z"
    },
    {
      "id": "F002",
      "title": "Show the first interactive Product behavior",
      "status": "pending",
      "depends_on": ["F001"],
      "estimated_scope": "medium",
      "completed_at": null
    }
  ]
}
```

### Feature index fields

| Field | Type | Requirement |
| --- | --- | --- |
| `id` | string | `F` plus three digits, increasing from `F001`. The index ID and detail filename must match exactly. |
| `title` | string | A verb phrase describing what the user or system will be able to do. |
| `status` | enum | One of `pending`, `in_progress`, `done`, `obsolete`, `obsolete_done`, or `blocked`. |
| `depends_on` | string[] | Strict prerequisite Feature IDs. Infrastructure Features use `[]`. Stored only in the index. |
| `estimated_scope` | enum | `small` fits one implementation and verification session; `medium` fits one session with multiple debugging passes; `large` must be decomposed and is invalid in a final generated plan. |
| `completed_at` | string \| null | ISO 8601 completion timestamp, or `null` until completion. |

---

## File 2: `docs/features/F0XX.json`

Each Feature has one detail file:

```json
{
  "id": "F042",
  "description": "The player can place a 1×2 wooden-wall blueprint from the construction panel. After a worker delivers materials and builds it, the wall becomes an obstacle for pathfinding.",
  "acceptance_criteria": [
    "The construction panel shows Wooden Wall and selecting it enters placement mode",
    "A 1×2 footprint follows the pointer and distinguishes valid from invalid positions",
    "Placing an order leaves a blueprint and a worker delivers two units of wood",
    "After five seconds of construction the wall appears and blocks pathfinding"
  ],
  "source": "product/04-building.md#wooden-wall",
  "notes": "TODO: Demolition refunds are outside this Feature and should be handled later."
}
```

### Feature detail fields

| Field | Type | Requirement |
| --- | --- | --- |
| `id` | string | Must match the index entry and the file stem. |
| `description` | string | Two to four sentences describing an observable outcome: What, not How. |
| `acceptance_criteria` | string[] | Concrete statements describing how a human can verify completion; subjective adjectives are insufficient. |
| `source` | string | Exact Product module and heading, such as `product/04-building.md#wooden-wall`; use `infrastructure` for infrastructure work. |
| `notes` | string | Initially empty. On completion, record implementation decisions, placeholders, deferred work, and non-blocking smell findings. |

---

## File 3: `docs/feature-list-revisions.json`

`sync-feature-list` appends one revision record for every incremental synchronization:

```json
{
  "revision_log": [
    {
      "revised_at": "2026-05-20T08:30:00Z",
      "synced_at_commit": "78cfcb9",
      "anchor_commit": "e25178b",
      "user_intent": "Add a daily schedule system",
      "summary": "Added the schedule module and F063 through F066; marked F046 and F047 obsolete because the new system replaces them.",
      "added": ["F063", "F064", "F065", "F066"],
      "obsoleted": ["F046", "F047"],
      "revised_via_new_feature": [],
      "source_path_updates": [],
      "depends_on_warnings": []
    }
  ]
}
```

The initial file must contain `{"revision_log": []}`.

---

## Feature status transitions

```text
pending ──(execute Stage 2)──→ in_progress ──(execute Stage 7 after acceptance)──→ done
   │                              │
   │                              └──(user abandons current work)──→ pending
   │
   ├──(sync determines it is no longer relevant)──→ obsolete
   └──(replacement work is represented by a new Feature)──→ obsolete

done ──(sync determines implemented Product behavior was removed)──→ obsolete_done
pending ──(a prerequisite unexpectedly becomes invalid)──→ blocked
```

- `obsolete` means the Feature was retired before implementation.
- `obsolete_done` means the behavior was implemented and later removed through Product evolution. The distinction preserves traceability because related code may still exist.
- An AI must not perform the `in_progress` to `done` transition without explicit human acceptance and a completed fresh-context smell scan with zero remaining `must_fix` findings.

---

## Hard constraints

### JSON string values must escape double quotes

An unescaped `"` inside a JSON string makes the file invalid. Use `\"` when a literal quotation mark is required, or rewrite the sentence to avoid it.

Invalid:

```text
"description": "Open the preview and confirm that "Game Over" appears"
```

Valid JSON:

```json
"description": "Open the preview and confirm that \"Game Over\" appears"
```

Every write must be followed immediately by validation:

```bash
python3 -m json.tool docs/feature-list.json > /dev/null
python3 -m json.tool docs/features/F0XX.json > /dev/null
python3 -m json.tool docs/feature-list-revisions.json > /dev/null
```

### ID consistency

All of the following must be equal:

- the set of IDs in `feature-list.json` `features[]`
- the set of filename stems under `docs/features/F*.json`
- `meta.total_features`

An index entry without a detail file, or a detail file without an index entry, is invalid.

### Dependencies must point backward

- A Feature `F0NN` must not depend on a Feature whose numeric ID is greater than `NN`.
- `generate-feature-list` must verify this invariant after generation.
- `sync-feature-list` must place new Features so the invariant remains true.

---

## Decomposition rules used by `generate-feature-list`

1. **Each Feature is the smallest independently verifiable complete behavior.** Describe what a user can do or what the system produces, not a class to implement.
2. **The first Feature establishes runnable infrastructure.** It has no dependencies.
3. **Follow module dependencies.** Deliver the core behavior of a prerequisite module before dependent modules.
4. **Follow Coding Rules architecture.** For example, when data and presentation are separated, deliver the data behavior before its presentation or interaction.
5. **Do not emit `large`.** Decompose an oversized Feature until every final entry is `small` or `medium`.
6. **Do not over-design.** Generate only behavior explicitly required by Product documents; omit speculation and explicitly deferred edge cases.
7. **Describe What and observable acceptance, not How.**

## Workflow ownership

| Operation | Owning Skill | Files changed |
| --- | --- | --- |
| Initial decomposition | `generate-feature-list` | Creates the index, all detail files, and an empty revision log. |
| Incremental Product synchronization | `sync-feature-list` | Updates the index and details, then appends a revision record. |
| Deliver one Feature | `execute-next-feature` | Transitions status and appends implementation knowledge to the detail notes. |
| Select one recorded smell | `pick-refactor-smell` | Reads Feature notes and does not modify the Feature plan. |

Claude Code integrations live under `claude-code/skills/`; portable Prompt versions live under `ai-agnostic-prompts/`.
