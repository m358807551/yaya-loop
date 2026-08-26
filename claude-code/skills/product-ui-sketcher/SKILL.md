---
name: product-ui-sketcher
version: 2.0
description: Turns Product behavior and interaction details into an ASCII wireframe and intent explanation, with an optional standalone HTML and Tailwind visual exploration.
triggers:
  - Sketch a Product UI, ASCII wireframe, or optional HTML mockup
  - 用户要求「UI 线框」「ASCII 界面」或「HTML mockup」
priority: medium
called_by: product-change-standardizer
---

# Product UI sketcher

## Role

Create a Product-blueprint wireframe, not a final visual design. Show where elements are and what interactions do. Do not lock implementation into specific colors, fonts, animation, pixels, or framework choices.

The durable Product artifact is the ASCII wireframe plus its intent and interaction notes. An HTML and Tailwind exploration is optional and independently replaceable.

## Language contract

Before producing output:

1. Read `document_language` from `docs/methodology-config.json`, or accept the confirmed value passed by `product-change-standardizer`.
2. Ask transient questions in the language the user is currently using.
3. Write wireframe labels, interaction tables, intent explanations, HTML-visible text, comments, and `notes_for_standardizer` in `document_language`.
4. Set the optional HTML document's `lang` attribute to the confirmed BCP 47 `document_language` value.
5. Keep ASCII symbols, YAML keys, HTML paths, module slugs, state identifiers, and interaction-marker syntax stable.

With `document_language: en` and a Chinese conversation, discuss in Chinese but produce English UI prose. With `document_language: zh-CN` and an English conversation, discuss in English but produce Simplified Chinese UI prose.

## Core principles

1. **ASCII is the durable source.** The Product module always receives the ASCII representation.
2. **HTML is opt-in.** Generate it only when `want_html_mockup: true` has been explicitly confirmed.
3. **Intent is mandatory.** Explain why the layout supports Product behavior.
4. **Do not prescribe colors, fonts, animation, pixel dimensions, or spacing in Product prose.** Those belong to implementation or later visual refinement.
5. **Mark every interactive element.** Use the fixed syntax below.

## Input

```yaml
document_language: en
module_name: timer-core
context: <Product behavior in document_language>
interactive_elements:
  - name: <label in document_language>
    behavior: <observable result in document_language>
display_elements:
  - <display requirement in document_language>
intent: <Product intent in document_language>
want_html_mockup: false
visual_tone: <Product-wide visual direction in document_language>
```

`module_name`, paths, keys, and Boolean values stay stable. Human-readable values follow `document_language`.

## Fixed ASCII conventions

Use these meanings consistently across the project:

| Element | Stable representation |
| --- | --- |
| Container | `┌─┐ │ │ └─┘` or emphasized `┏━┓ ┃ ┃ ┗━┛` |
| Divider | horizontal `├─┤` or vertical `│` |
| Text | render the actual Product label in `document_language` |
| Button | `[label]` |
| Primary CTA | `[[label]]` |
| Input | `< placeholder >` |
| Select | `[option ▾]` |
| Checkbox | `[ ]` or `[x]` |
| Radio | `( )` or `(•)` |
| Slider | `─────●────────` |
| Progress | `━━━━━━━━━━░░░░░░` |
| Image or icon | `[image: description]` or `[icon: description]`, localized naturally |
| Scroll area | add `↕` to the right edge |
| Collapsible area | `▸ label` or `▾ label` |
| List item | `• content` |
| Data value | use a realistic example such as `25:00`, not a token such as `MM:SS` |

Only one `[[primary CTA]]` may appear in one interface state.

## Required Product output

Return content that the standardizer can place in the module's UI section. Its localized headings must preserve these semantics:

1. **Primary layout:** one ASCII wireframe.
2. **Interaction details:** a table mapping each element and condition to observable behavior.
3. **Intent:** why hierarchy, grouping, and feedback support the Product goal.
4. **State differences:** list meaningful differences rather than drawing every state, unless layouts differ substantially.
5. **Visual exploration:** include the optional HTML path only when generated.

Example structure, with labels rendered in `document_language`:

````markdown
### <Primary layout>

```
┌──────────────────────────────────────┐
│          [image: companion]          │
│                25:00                 │
│       ━━━━━━━━━━━━━━━━━━━━           │
│          [[Start]]  [Settings]       │
│          Sessions today: 3           │
└──────────────────────────────────────┘
```

### <Interaction details>

| <Element> | <Condition> | <Behavior> |
| --- | --- | --- |
| `[[Start]]` | <user activates> | <start countdown and show Pause> |

### <Intent>

- <reason for visual hierarchy in document_language>

### <State differences>

- `idle`: <difference in document_language>
- `running`: <difference in document_language>
- `paused`: <difference in document_language>
- `completed`: <difference in document_language>

### <Visual exploration>

<localized reference to `docs/ui-mockups/timer-core.html`>
````

## Optional HTML and Tailwind exploration

Run this section only when `want_html_mockup: true`.

- Path: `docs/ui-mockups/{module-name}.html`, without a numeric prefix.
- Put all primary states in one file rather than creating one file per state.
- Translate the ASCII structure into static semantic HTML; avoid JavaScript unless native HTML such as `<details>` cannot express the exploration.
- Use Tailwind only to express the confirmed `visual_tone`. It is exploratory, not a final engine or framework implementation.
- Keep visible labels and explanatory comments in `document_language`.
- Set `<html lang="<document_language>">` and `<meta charset="UTF-8">`.

The file must begin with a localized comment preserving these meanings:

```html
<!--
  This is a replaceable visual exploration, not the final implementation.
  Product intent: docs/product/NN-xxx.md
  implementation constraints: docs/coding_rules.md
  Replacing this file does not change the Product blueprint.
-->
```

Possible tone mappings are implementation examples for the mockup only:

- warm: `bg-stone-*` or `bg-amber-*`
- minimal and cool: `bg-slate-*` or `bg-neutral-*`
- retro pixel: `font-mono` and high contrast
- cyberpunk: `bg-zinc-900` with restrained neon accents

## Common traps

1. Do not decorate the ASCII wireframe; simple boxes and bullets are enough.
2. Do not put color descriptions inside ASCII. Explain visual intent separately.
3. Do not invent pixel widths or spacing values in Product documents.
4. Do not turn the optional HTML into a complete application.
5. List state differences instead of drawing many nearly identical wireframes.
6. Never use more than one primary CTA marker in one interface state.

## Return structure

```yaml
ascii_wireframe: |
  <localized Markdown ready for the Product UI section>

html_mockup:
  generated: true | false
  path: docs/ui-mockups/timer-core.html
  content: |
    <complete HTML when generated>

notes_for_standardizer:
  - <localized note about related Product data, UI, or audio changes>
```

When `generated` is `false`, omit `path` and `content`. `notes_for_standardizer` may request another Product workflow, but this sketcher does not edit Product files or call it directly.
