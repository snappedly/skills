---
name: deslop
description: Remove AI-generated code slop and clean up code style
---

# Remove AI code slop

Use the caller's fixed point or compute the task branch's merge-base with its configured base branch. Inspect staged, unstaged, committed, and untracked task files in that scope. Remove AI-generated slop introduced by the task.

## Focus Areas

- Extra comments that are unnecessary or inconsistent with local style
- Defensive checks or try/catch blocks that are abnormal for trusted code paths
- Casts to `any` used only to bypass type issues
- Deeply nested code that should be simplified with early returns
- Other patterns inconsistent with the file and surrounding codebase

## Guardrails

- Keep behavior unchanged. Return a possible bug to the implementation workflow so it receives behavior-level tests, cleanup, and review.
- Prefer minimal, focused edits over broad rewrites.
- Keep the final summary concise (1-3 sentences).
