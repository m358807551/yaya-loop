# 00 · Methodology overview

> Read this document to understand the mental model of the complete methodology. Every other file under `methodology/` specifies one part of this overview in greater detail.

## Mental model: three document layers and three Skill groups

```text
┌──────────────────────────────────────────────────────────────────────┐
│                    Three document layers under docs/                  │
├──────────────────────────────────────────────────────────────────────┤
│ product.md + product/*.md     ← Product intent (What)                │
│ feature-list.json             ← Lightweight work index, loaded often │
│ + features/F0XX.json          ← Feature details, loaded on demand     │
│ + feature-list-revisions.json ← Product-to-Feature revision history   │
│ coding_rules.md               ← Implementation constraints (How)      │
└──────────────────────────────────────────────────────────────────────┘
                                  ▲
                                  │ maintained by
                                  ▼
┌──────────────────────────────────────────────────────────────────────┐
│                         Three Skill groups                           │
├──────────────────────────────────────────────────────────────────────┤
│ Product Skills:                                                      │
│   product-init-elicitor        elicits a new Product                  │
│   product-change-standardizer routes every Product change            │
│   product-spec-elicitor        resolves material ambiguity            │
│   product-ui-sketcher          creates ASCII UI sketches              │
│   product-audio-sketcher       specifies audio and placeholders       │
│                                                                      │
│ Generation Skills:                                                   │
│   generate-feature-list        decomposes Product into Features       │
│   sync-feature-list            incrementally synchronizes changes     │
│                                                                      │
│ Delivery Skills:                                                     │
│   execute-next-feature         runs one Feature through eight stages  │
│   pick-refactor-smell          selects one recorded smell to refactor │
└──────────────────────────────────────────────────────────────────────┘
```

## Why these boundaries exist

| Boundary | Problem it solves |
| --- | --- |
| **Product vs. Feature vs. Coding Rules** | Separates What, Todo, and How so every change has one authoritative layer. |
| **Lightweight index plus on-demand details** | Keeps hundreds of Features scannable without loading every acceptance criterion into context. |
| **Product changes enter through the standardizer** | Routes an informal request to the right module, clarification, sketches, Product update, and incremental Feature synchronization instead of editing files ad hoc. |
| **Feature delivery uses eight stages** | Prevents an agent from treating its own implementation or test result as human acceptance. |
| **Fresh-context smell scan plus commit evidence** | Gives an independent reviewer the full Coding Rules and makes zero remaining `must_fix` findings an enforceable completion gate. |

## Complete Feature lifecycle

```text
User expresses a Product need
   │
   ▼
[product-change-standardizer] ──→ [product-spec-elicitor]
   │                                ├─→ [product-ui-sketcher]
   │                                └─→ [product-audio-sketcher]
   ▼
Update docs/product.md + docs/product/NN-*.md
   │
   ▼
[sync-feature-list] ──→ update feature-list.json + features/F0XX.json
   │
   ▼
[execute-next-feature]
   ├─ Stage 0: select Feature and produce the fixed exit report with
   │           verbatim relevant Coding Rules and source line numbers
   ├─ Stage 1: preflight resources and dependencies; register every
   │           `_placeholder_` resource in the Feature notes
   ├─ Stage 2: mark in_progress and update Progress
   ├─ Stage 3: implement with focused commits
   ├─ Stage 4: run the project-level static_check_cmd
   ├─ Stage 5: obtain explicit human acceptance
   ├─ Stage 6: delegate an independent fresh-context code-smell scan;
   │           this hard gate must produce Feature-specific
   │           `Code smell scan: pass` evidence with `must_fix: 0`
   ├─ Stage 7: mark done; the commit must contain that exact evidence
   └─ Stage 8: hand off and stop
```

## Three non-negotiable constraints

1. **A Product change must go through `product-change-standardizer`; it must not edit Product documents ad hoc.** This keeps module placement and incremental synchronization traceable.
2. **An AI must not mark a Feature `done` on its own.** Stage 5 requires explicit human acceptance, and the completion commit must include Feature-specific `Code smell scan: pass` evidence with `must_fix: 0`.
3. **An AI must not work on `main` or `master`, force-push, or run `reset --hard`.** Commits belong on a working branch, and potentially destructive Git operations require explicit authorization.

## Further reading

| To learn about | Read |
| --- | --- |
| Product overview and module documents | [01-product-doc-structure.md](./01-product-doc-structure.md) |
| Feature index, detail, and revision schemas | [02-feature-list-schema.md](./02-feature-list-schema.md) |
| The eight-stage delivery loop | [03-execute-loop.md](./03-execute-loop.md) |
| The four-layer Coding Rules architecture | [04-coding-rules-4-layers.md](./04-coding-rules-4-layers.md) |
| Document-language selection and compatibility | [05-document-language.md](./05-document-language.md) |
| Installation and first use | [README](../README.md) or [Bootstrap](../BOOTSTRAP.md) |
