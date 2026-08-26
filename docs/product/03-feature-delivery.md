# Feature delivery and quality gates

## Module positioning

This module executes one eligible Feature through bounded implementation, automated verification, human acceptance, independent code-smell review, completion evidence, and handoff.

## Core flows

1. Select an eligible pending or in-progress Feature and load only the context it requires.
2. Report relevant Coding Rules and inspect resources, dependencies, branch state, and planned changes.
3. Mark the Feature in progress, implement in small commits, and maintain progress notes.
4. Run the configured static checks and present observable behavior for human verification.
5. After explicit human acceptance, run a fresh-context code-smell scan.
6. Resolve all `must_fix` findings, record non-blocking findings, and commit completion evidence.
7. Hand off the next eligible Feature without starting it automatically.

## State model

```text
pending -> in_progress -> done
   |             |
   |             +-> blocked
   +-> obsolete
done -> obsolete_done
```

An AI cannot move a Feature to `done` without explicit human acceptance and passing code-smell evidence.

## Acceptance criteria

1. Implementation does not begin on `main` or `master` and does not silently include unrelated changes.
2. Static verification uses the command stored in the methodology configuration.
3. Observable product behavior remains pending until a human explicitly accepts it.
4. Completion is blocked while any code-smell finding remains `must_fix`.
5. The completion commit includes Feature-specific evidence with `must_fix: 0`.
6. The workflow stops after handoff instead of automatically starting another Feature.

## Edge cases

- Changes to Yaya Loop's own workflow rules take effect on the next Feature; the current Feature follows the committed rules that existed when it started.
- Failed or unavailable independent review blocks completion rather than being silently skipped.
- Dirty worktrees, oversized Features, missing assets, and contradictory rules must pause for a maintainer decision.

## Change history

- 2026-08-26: Added the initial reverse-engineered module definition and the self-modification rule snapshot.
