# Yaya Loop repository coding rules

## 1. Scope and sources of truth

- `docs/product.md` and `docs/product/*.md` define product intent.
- `methodology/` defines the canonical tool-independent workflow behavior.
- `claude-code/skills/` and `ai-agnostic-prompts/` are distribution surfaces derived from the same behavior; neither may silently diverge.
- Schemas, enum values, evidence strings, filenames, and public commands are compatibility surfaces.
- Do not copy Yaya Loop's distributable Skills, Prompts, or Hooks into duplicate self-installed locations in this repository.

## 2. Change discipline

- Keep each change focused on one Feature and avoid unrelated cleanup.
- Resolve ambiguity before changing workflow semantics.
- Do not work directly on `main` or `master`.
- Do not use destructive Git operations or push, merge, or rewrite history without explicit maintainer authorization.
- Preserve existing public paths unless a Product decision and migration note explicitly authorize a breaking change.
- A Feature that modifies workflow rules follows the committed rules that existed when the Feature started; new rules govern the next Feature.

## 3. Documentation and protocol rules

- Write Yaya Loop's canonical executable instructions in natural American English.
- Write self-hosted Product and Feature knowledge in the configured `document_language`.
- Preserve machine-readable names in English: JSON keys, enums, Feature IDs, evidence strings, placeholder prefixes, paths, and Conventional Commit types.
- Prefer clear normative words: use `must` for requirements, `should` for recommendations, and `may` for optional behavior.
- Do not translate by mechanically preserving Chinese sentence structure; preserve meaning and workflow invariants.
- Keep relative repository links valid and avoid environment-specific conversation URLs.

## 4. Mirrored workflow surfaces

- When a workflow rule changes, inspect the corresponding Claude Skill, agent-agnostic Prompt, Methodology document, template, Hook, example, and test.
- Avoid manual duplication when a shared source or test can prevent drift, but do not introduce a generation framework without a demonstrated maintenance benefit.
- Trigger metadata should remain discoverable to English users and retain concise Chinese trigger examples where useful.

## 5. Python and shell

- Keep repository tooling compatible with the supported Python versions in CI and prefer the standard library unless a dependency is justified.
- Hooks must fail safely with actionable messages and must not modify user data unexpectedly.
- Quote shell paths and variables, avoid destructive globs, and keep commands non-interactive in automated checks.
- Preserve executable bits on Hook entry points.

## 6. JSON and templates

- Every JSON and JSON template file must parse successfully after placeholder handling appropriate to that template.
- Keep `docs/feature-list.json`, `docs/features/F0XX.json`, and `docs/feature-list-revisions.json` structurally consistent.
- Human-readable JSON values may follow `document_language`; keys and enum values must not.
- Do not place unescaped double quotes inside JSON string values.

## 7. Verification

- Run `git diff --check` before committing.
- Run `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v` for repository changes.
- Documentation changes must be checked for broken relative links and contradictions with canonical workflow behavior.
- Internationalization changes require English and Chinese smoke scenarios, including a conversation language that differs from `document_language`.

## 8. Completion

- Automated checks do not replace human acceptance of observable documentation and workflow behavior.
- Complete the Feature-specific code-smell review and leave the required stable evidence before marking a Feature done.
