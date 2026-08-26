# Claude Code installation

> This directory is the ready-to-install Claude Code distribution. Copy it into a target project's `.claude/` directory, then restart Claude Code to discover all nine Skills and both Hooks.
>
> Codex, Aider, Cursor, and other non-Claude agents should use [`../ai-agnostic-prompts/`](../ai-agnostic-prompts/) together with [`../git-hooks/`](../git-hooks/).

## Install from the target project root

These commands assume Yaya Loop is available at `~/code/yaya-loop/`.

```bash
mkdir -p .claude/skills .claude/hooks

# 1. Install all nine Skills.
cp -r ~/code/yaya-loop/claude-code/skills/* .claude/skills/

# 2. Install both Hooks and preserve executable permissions.
cp ~/code/yaya-loop/claude-code/hooks/*.py .claude/hooks/
chmod +x .claude/hooks/*.py

# 3a. If .claude/settings.json does not exist, install the example.
cp ~/code/yaya-loop/claude-code/settings.example.json .claude/settings.json

# 3b. If it exists, merge the hooks object from settings.example.json
# into the existing file instead of overwriting project settings.
```

## Installed files

```text
claude-code/
├── skills/
│   ├── execute-next-feature/SKILL.md
│   ├── generate-feature-list/SKILL.md
│   ├── sync-feature-list/SKILL.md
│   ├── pick-refactor-smell/SKILL.md
│   ├── product-init-elicitor/SKILL.md
│   ├── product-change-standardizer/SKILL.md
│   ├── product-spec-elicitor/SKILL.md
│   ├── product-ui-sketcher/SKILL.md
│   └── product-audio-sketcher/SKILL.md
├── hooks/
│   ├── gate-feature-done.py
│   └── check-feature-list.py
├── settings.example.json
└── install.md
```

`gate-feature-done.py` is the PreToolUse completion gate. It blocks a new `done` transition unless the current assistant transcript contains Feature-specific `Code smell scan: pass` evidence with `must_fix: 0`.

`check-feature-list.py` is the PostToolUse structural check. It blocks invalid Feature JSON and warns when index IDs and detail files temporarily differ.

## Verify the installation

1. Restart Claude Code and confirm that all nine Skills appear in Skill discovery.
2. Confirm both Hook paths in `.claude/settings.json` and executable files in `ls -l .claude/hooks/`.
3. In a test project, attempt to change a Feature to `done` without Stage 6 evidence. The PreToolUse Hook should block the edit and show the required evidence format.
4. Ask Claude Code to `do the next Feature`. Stage 0 should quote real Coding Rules with line numbers in its exit report.

## Relationship to Methodology

The nine `SKILL.md` files are executable distributions of the tool-independent specifications under [`../methodology/`](../methodology/). YAML frontmatter supplies Claude Code discovery metadata; canonical workflow bodies preserve the same behavior as portable Prompts.

- Customize a Skill at `.claude/skills/<name>/SKILL.md`.
- Customize a Hook at `.claude/hooks/<name>.py` and keep it executable.
- Do not weaken human acceptance, independent review, completion evidence, or Git safety gates.

## Upgrade

Back up project customizations before replacing installed files:

```bash
cp -r .claude .claude.backup-$(date +%Y%m%d)
cp -r ~/code/yaya-loop/claude-code/skills/* .claude/skills/
cp ~/code/yaya-loop/claude-code/hooks/*.py .claude/hooks/
chmod +x .claude/hooks/*.py
```

Merge Hook settings rather than overwriting project-specific `.claude/settings.json` content. See [`../upgrade-notes.md`](../upgrade-notes.md) for migration details.

## Troubleshooting

- **A Hook does not run:** confirm the `hooks` object, exact installed paths, and executable permissions.
- **A Skill is missing:** restart Claude Code and confirm `.claude/skills/<name>/SKILL.md` has valid YAML frontmatter.
- **Stage 0 cannot cite Coding Rules:** confirm `docs/coding_rules.md` exists and Bootstrap STEP 3 completed.
- **Feature JSON is rejected:** run `python3 -m json.tool <path>` and fix the reported syntax error.
