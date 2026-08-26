# 01 · Product document structure

## Two-level structure

```text
docs/
├── product.md              ← Scannable Product overview
└── product/
    ├── 01-<core-module>.md ← Detailed module specification
    ├── 02-<other>.md
    └── ...
```

The two levels serve different context needs. `product.md` must remain short enough to scan as a whole, while module documents provide detail on demand. A person or agent should understand the Product shape in about 30 seconds and enter one module in a few minutes.

Generated headings and prose must follow the project's configured `document_language`; the section semantics below must remain intact in every language. See [05-document-language.md](./05-document-language.md).

## Standard `product.md` sections

Write these sections in this order. A document rendered from the canonical template must preserve every template section; when a section does not apply, retain its heading and state that it is not applicable. A project may add specialized sections, but the standard semantics must remain easy to locate.

| Section semantics | Required? | Content |
| --- | --- | --- |
| Title and version summary | Yes | Current version plus a one-sentence description of that version's complete loop. |
| One-line positioning | Yes | A sentence that makes the Product and its complete short experience immediately understandable. |
| Target users | Yes | Primary users, usage context, and expected frequency. An MVP may target maintainer self-testing. |
| Core loop | Yes | A numbered, coherent action sequence for each version such as V0.1 or V0.2. |
| Module list | Yes | Number, filename, module name, and `draft`, `done`, or `obsolete` status. |
| Module dependencies | Yes | An ASCII dependency diagram, with cross-cutting modules identified separately. |
| Visual direction | Recommended | Palette, typography, and UI tone used as input to UI sketches. |
| Audio direction | Recommended | Sound-effect and music direction used as input to audio entries. |
| Change history | Yes | Reverse-chronological date, Product change, and reason. |

## Standard `product/NN-name.md` sections

A module document is more detailed than the overview. A rendered template must retain its standard headings and explicitly mark inapplicable sections rather than deleting them. Optional additions such as Version evolution may be included when useful, but unrelated concerns must not be collapsed in a way that hides Product behavior.

| Section semantics | Content |
| --- | --- |
| Module positioning | The module's role and the modules or actors it interacts with. |
| Version evolution (optional) | How the module changes across V0.x releases. |
| Functional flow | Step-by-step user or system behavior, optionally with an ASCII diagram. |
| Data model | Field, type, default value, and meaning. |
| State machine | State values and transition rules, when applicable. |
| UI sketch | ASCII wireframe and key interactions, produced by `product-ui-sketcher`. |
| Audio entries | Trigger, filename, style, and duration, produced by `product-audio-sketcher`. |
| Numeric rules | Formulas, thresholds, and configuration values. |
| Acceptance criteria | Concrete statements of how completed behavior can be verified. |
| Edge cases | Known cases intentionally deferred to later Features. |
| Change history | Reverse-chronological record of changes to this module. |

## Module filename rules

- Use a two-digit prefix and a kebab-case ASCII slug, such as `01-pawn-core.md`, `02-map.md`, or `13-mining.md`.
- Order numbers by module dependency: a module must appear before modules that depend on it.
- Once assigned, module numbers must not be reordered. New modules use the next available number.
- An obsolete module must be renamed with the `_obsolete-` prefix rather than deleted, preserving traceability.

## Version convention

- Use `V<MAJOR>.<MINOR>`, such as `V0.9`.
- Keep MAJOR at `0` during the MVP phase; increment it for the first formal release.
- Increment MINOR when the user-observable core loop expands.
- Small changes within the same loop remain in the current version rather than creating a new version number.

## When to create a module

- **Create a module** when a new system has its own data model and an independent interaction entry point.
- **Extend an existing module** when new behavior, values, or UI remain within that module's established responsibility.

When the boundary is unclear, use `product-change-standardizer`; it owns the routing decision.

## Anti-examples

- Do not put implementation choices such as a vector type or pathfinding algorithm in Product documents. Those choices belong in Coding Rules, code, or implementation notes.
- Do not describe numeric behavior with subjective terms such as “high damage”; provide a formula or concrete value.
- Do not use subjective acceptance language such as “renders smoothly”; state an observable threshold or outcome.
- Do not put speculative future ideas in active Product requirements. Keep them in a separate `docs/ideas.md` until approved as Product intent.
