# Git Hook installation for non-Claude agents

> Codex, Aider, Cursor, and other agents without Claude Code's PreToolUse Hook can install this Git `commit-msg` Hook as a completion-gate fallback.
>
> Claude Code users normally install [`../claude-code/hooks/gate-feature-done.py`](../claude-code/hooks/gate-feature-done.py), which can block an invalid `done` edit before commit time.

## What it installs

| File | Hook type | Purpose |
|---|---|---|
| `commit-msg` | Git `commit-msg` Hook | When staged changes newly mark a Feature `done`, require matching Feature-specific `Code smell scan: pass` evidence with `must_fix: 0` |

The Hook does not replace Stage 5 human acceptance or Stage 6 independent review. It verifies only stable completion evidence at commit time.

## Install from the target project root

These commands assume Yaya Loop is available at `~/code/yaya-loop/`.

```bash
cp ~/code/yaya-loop/git-hooks/commit-msg .git/hooks/commit-msg
chmod +x .git/hooks/commit-msg
```

If the project already has a `commit-msg` Hook, merge the checks deliberately instead of overwriting it.

## Verify rejection and acceptance

Use a disposable branch or test repository with an existing `docs/feature-list.json`.

1. Stage a change that moves a Feature from `pending` or `in_progress` to `done`.
2. Attempt a commit without scan evidence. The Hook should reject it and print the required format.
3. Retry with Feature-specific evidence:

```text
Code smell scan: pass (feature: F001, must_fix: 0, suggest: 0, acceptable: 0)
```

The Feature ID must match the newly completed Feature; counts are decimal integers and `must_fix` must be zero.

## Limitations

- The Hook runs only at commit time. It cannot warn about an uncommitted edit; Claude Code's PreToolUse Hook blocks earlier.
- Git permits `git commit --no-verify`. This intentional escape hatch cannot be disabled by a local Hook. Review bypasses when completion evidence matters.
- The Hook verifies evidence syntax and Feature matching. It cannot prove that human acceptance or independent review occurred.

## Compatibility

- Requires Python 3 and Git.
- Uses only the Python standard library.
- Supported environments: macOS, Linux, and WSL.
- Native Windows Git Bash should work but is not verified.

## PR and CI integration

Repositories using pull requests may reproduce the same check in CI. A local Hook can be bypassed with `--no-verify`, while protected CI cannot. Yaya Loop does not currently ship a CI template; `commit-msg` is the reference behavior.
