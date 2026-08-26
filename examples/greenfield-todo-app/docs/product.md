# TodoMate · MVP

> Current version: **V0.1 · Single-device local Todo application**

## One-line positioning

Validate the minimum viable form of a frontend-only Todo application through a five-minute loop: open the page, enter a task, mark it complete, and clear completed tasks.

## Target users

- **Primary user:** An individual developer who normally keeps tasks in Markdown and wants to try a more visual alternative.
- **Usage context:** Developer self-testing during the MVP phase and occasional demos to colleagues.
- **Usage frequency:** Several times per day, for 30 seconds to five minutes at a time.

## Core loop

### V0.1 loop

```
1. The user opens the page and sees an empty Todo list with an input at the top.
2. The user enters text and presses Enter to add an incomplete Todo.
3. The user selects a Todo's checkbox to toggle its completion state.
4. Completed Todos appear gray with strikethrough text.
5. The user selects "Clear completed" to remove every completed Todo.
6. The user closes and reopens the page; all remaining data persists in localStorage.
```

This release is incomplete if any step in this loop is missing.

## Module list

| No. | File | Module | Status |
|------|------|--------|------|
| 01 | [01-tasks.md](./product/01-tasks.md) | Todo list | draft |

## Module dependencies

```
infrastructure ──→ 01-tasks
```

## Visual direction

- Minimal and flat: white background, black text, and one blue-gray accent color.
- Use the system sans-serif font with generous line spacing.
- Completed items use strikethrough text at 50% opacity.
- No animation or shadows; keep attention on the content.

## Audio direction

No audio. This frontend-only Todo application does not need sound effects.

## Change history

- 2026-05-25: Initialized the project and defined the V0.1 MVP loop.
