# AI-agnostic prompts · usage guide

> This directory is for coding agents that do not load Claude Code Skills directly, including Codex, Aider, Cursor, and similar tools. Each Prompt is a self-contained Markdown workflow.

Claude Code users normally use the corresponding files under `claude-code/skills/`, where YAML metadata supports automatic discovery.

## How to use a Prompt

Choose the workflow from the table below, then either paste the Prompt into the agent conversation or ask the agent to read the installed file from `docs/methodology-prompts/`.

The executable body in each portable Prompt matches its native Skill. Distribution wrappers may differ so each environment can explain discovery and invocation naturally.

## English commands and Chinese discovery examples

| User intent | English command example | Concise Chinese trigger | Prompt |
|---|---|---|---|
| Initialize Product for a new project | `Initialize this project from my Product idea.` | `从零初始化项目` | [product-init-elicitor.prompt.md](./product-init-elicitor.prompt.md) |
| Standardize a Product change | `Add X`, `Change Y`, or `Fix Product behavior Z.` | `增加 X` / `修改 Y` / `修复 Z` | [product-change-standardizer.prompt.md](./product-change-standardizer.prompt.md) |
| Clarify one Product change | `Help me specify this change.` | `把这个变更说清楚` | [product-spec-elicitor.prompt.md](./product-spec-elicitor.prompt.md) |
| Sketch Product UI | `Sketch the UI for this behavior.` | `画个 UI 草图` | [product-ui-sketcher.prompt.md](./product-ui-sketcher.prompt.md) |
| Specify Product audio | `Define the audio requirements.` | `这里需要什么音效` | [product-audio-sketcher.prompt.md](./product-audio-sketcher.prompt.md) |
| Generate the initial Feature plan | `Generate the Feature list.` | `生成 feature-list` | [generate-feature-list.prompt.md](./generate-feature-list.prompt.md) |
| Synchronize Product changes | `Synchronize the Feature list.` | `同步 feature-list` | [sync-feature-list.prompt.md](./sync-feature-list.prompt.md) |
| Execute eligible work | `Do the next Feature.` or `Implement F007.` | `做下一个 feature` / `实现 F007` | [execute-next-feature.prompt.md](./execute-next-feature.prompt.md) |
| Select a refactor smell | `Pick one smell to refactor.` | `挑一个坏味道重构` / `扫一下 suggest` | [pick-refactor-smell.prompt.md](./pick-refactor-smell.prompt.md) |

## Installed-file example

```text
Read docs/methodology-prompts/execute-next-feature.prompt.md and follow it to do the next Feature.
```

If the agent supports file references, an equivalent command may be:

```text
@docs/methodology-prompts/execute-next-feature.prompt.md
```

## Native Skills and portable Prompts

| Capability | Claude Code Skill | Portable Prompt |
|---|---|---|
| Discovery | YAML metadata and triggers | User selects or references the Prompt |
| Workflow behavior | Canonical executable body | The same canonical executable body |
| Stage 6 independent review | Delegate to a fresh-context sub-agent | Delegate when supported; otherwise ask the user to run the supplied review in a new independent session and return strict JSON |
| Completion gate | Claude Hook plus Git Hook | Git Hook; the Prompt must still enforce human acceptance and `must_fix: 0` evidence |

The methodology is the same in both distributions. Only discovery and capability-specific fallback mechanics differ.

## Project-specific adaptation

Projects may add compatible constraints, static-check commands, or technology-specific rules. Do not weaken or remove Stage gates, stable evidence, human completion authority, Feature schema fields, or Git safety boundaries.
