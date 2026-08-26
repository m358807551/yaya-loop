# Adoption and agent integrations

## Module positioning

This module installs and exposes Yaya Loop's workflow in greenfield and existing projects across different AI coding agents and technology stacks without making one agent the product's permanent source of truth.

## Core flows

1. Detect whether a target repository is new, existing, or already initialized.
2. Derive or elicit Product state appropriate to that repository.
3. Install Coding Rules selected for the target engine and programming language.
4. Expose workflow capabilities through native Claude Code Skills and Hooks or agent-agnostic Prompts and Git gates.
5. Validate installed structure, JSON consistency, rule loading, and upgrade compatibility.

## Distribution surfaces

- `BOOTSTRAP.md` is the agent-readable installation entry point.
- `claude-code/` contains native Skills, Hooks, and configuration examples.
- `ai-agnostic-prompts/` contains portable workflow instructions for other agents.
- `git-hooks/` provides completion-gate enforcement where native tool hooks are unavailable.
- `coding-rules-library/` provides stack-specific rule sources.
- `methodology/` is the canonical, tool-independent workflow specification.

## Acceptance criteria

1. A user can initialize Yaya Loop in a new or existing repository from one documented entry point.
2. Claude Code and agent-agnostic distributions enforce equivalent workflow invariants.
3. Installed projects retain their own Product state and project-specific Coding Rules.
4. Yaya Loop's source repository can self-host Product and Feature state without copying its distributable assets into duplicate installed locations.
5. Repository tests detect invalid schemas, inconsistent examples, and broken completion gates.
6. Upgrades preserve project-owned decisions and clearly identify manual migrations.

## Edge cases

- The Yaya Loop source repository must not recursively install copies of its own Skills, Prompts, or Hook sources.
- An intended integration may be unavailable in the current agent environment; the workflow must disclose the fallback.
- Monorepos and mixed-language projects require an explicit project boundary and static-check command.

## Change history

- 2026-08-26: Added the initial reverse-engineered module definition and self-hosting boundary.
