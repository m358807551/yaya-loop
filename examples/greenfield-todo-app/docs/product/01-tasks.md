# 01-tasks · Todo list

## Module positioning

Own all Todo data and user interactions. This is the MVP's only business module.

## Functional flow

```
1. Page load → read Todos from localStorage and render the list.
2. User enters text and presses Enter → add a Todo (`id = uuid`, `text`, `done = false`, `createdAt`).
3. User selects a checkbox → toggle that Todo's `done` state.
4. User selects "Clear completed" → remove every Todo with `done = true`.
5. Any change → write the updated list back to localStorage.
```

## Data model

`Todo` type:

| Field | Type | Default | Description |
|------|------|--------|------|
| `id` | string (UUID) | Generated | Globally unique identifier |
| `text` | string | Required | Single-line Todo content |
| `done` | boolean | false | Completion state |
| `createdAt` | number (timestamp in ms) | `Date.now()` | Creation time used for stable ordering |

Storage: the localStorage key is `todomate:todos:v1`, and its value is a JSON-encoded `Todo[]`. The `v1` suffix reserves room for future migrations.

## UI sketch

```
┌──────────────────────────────────────────┐
│  TodoMate                                │
├──────────────────────────────────────────┤
│  [_________________________] [Add ↵]     │
├──────────────────────────────────────────┤
│  [ ] Buy groceries                       │
│  [✓] W̶r̶i̶t̶e̶ ̶c̶o̶d̶e̶                         │
│  [ ] Watch a movie                       │
│  [✓] T̶a̶k̶e̶ ̶o̶u̶t̶ ̶t̶h̶e̶ ̶t̶r̶a̶s̶h̶                 │
├──────────────────────────────────────────┤
│             [Clear completed (2)]        │
└──────────────────────────────────────────┘
```

Key interactions:
- Input receives focus → placeholder disappears.
- Enter → submit and clear the input.
- Checkbox selection → toggle immediately and show visual feedback.
- "Clear completed" displays the current completed count and is disabled when the count is zero.

## Numeric rules

- Todo text is limited to 200 characters; truncate any excess.
- Render the list in descending `createdAt` order, newest first.

## Acceptance criteria

1. Open the page, enter "Buy groceries," and press Enter → the list gains "Buy groceries" and the input clears.
2. Select the checkbox beside "Buy groceries" → its text becomes gray and struck through.
3. Select it again → its normal appearance returns.
4. Add five Todos, complete two, and select "Clear completed" → three Todos remain.
5. Refresh the page → the remaining three Todos are still present.
6. Enter more than 200 characters → only the first 200 characters are accepted.

## Edge cases

- Duplicate Todo text is allowed; IDs distinguish entries and this release does not deduplicate them.
- Empty strings are rejected; trim on submission and ignore an empty result.
- If localStorage is unavailable, such as in a restricted privacy mode, fall back to in-memory storage and warn: "Your data will be lost when you close this page."

## Change history

- 2026-05-25: Initialized the module.
