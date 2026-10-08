---
name: code-review
description: "Review a branch, PR, or working change for correctness, requirements, maintainability, and applicable UI concerns, with depth proportional to risk."
license: MIT
---

Review the caller's change read-only and return findings once. The calling workflow owns cleanup, fixes, and convergence, so this skill never launches cleanup, implementation, or another review cycle itself.

Read `docs/agents/workflow.md` when present for finding disposition. Take validation evidence from the caller's cleanup check record and reuse it under code-cleanup's reuse rules rather than rerunning those checks. Without a check record, as in a direct request to review a PR, run the repository's configured read-only checks yourself or list them as not run; a check listed as not run is unverified coverage, not a gap that needs the user's decision. Report failed or blocked checks, and required checks the record shows could have run but did not, as gaps; an unverified check never counts as passed. Neither a check the repository records as `not configured` or `not applicable` nor one that runs only after a push, such as CI, is a gap. A review with a missing review axis is incomplete. Lead the report with every gap and missing axis; the caller treats each as an open finding that needs the user's decision rather than as a pass.

## Choose review depth

For a small, low-risk change, review in the current agent: inspect the full diff, including untracked files, and its affected context, compare it with the supplied requirements or the user's request, and check it against applicable repository standards and, for a UI change, its accessibility and interaction concerns. Return one brief report of concrete findings and gaps. After a correction, recheck only the fix delta.

Read [INDEPENDENT-REVIEW.md](INDEPENDENT-REVIEW.md) and use its independent-axis process when the user or repository explicitly requires it, or for substantial cross-module changes or security or data-integrity risks. A small diff stays on the local path even when it touches a UI file, adds a test, or arrives as an explicit review request.

## UI audit

When the user asks for a UI audit, apply the pinned [GUIDELINES.md](GUIDELINES.md) on whichever path the depth choice selected: on the local path, run the Interface axis instructions from INDEPENDENT-REVIEW.md yourself. Read `docs/agents/frontend.md` when present for the UI directories and the accessibility baseline; the baseline's rules are findings, never judgment calls. Done when every UI file in scope has a `file:line` finding or a pass against every applicable rule, reported with the guidelines pin date.
