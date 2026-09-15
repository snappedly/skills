---
name: code-review
description: "Review a branch, PR, or working change for correctness, requirements, maintainability, and applicable UI concerns, with depth proportional to risk."
---

Review the caller's change read-only, with depth proportional to risk. The calling workflow owns cleanup, fixes, and convergence. This skill returns findings once and never recursively launches cleanup or implementation.

Read `docs/agents/workflow.md` when present for finding disposition. Consume supplied cleanup evidence; for a review-only request, report missing evidence without editing or committing the user's files.

## Choose review depth

For a small, low-risk change, review in the current agent: inspect the diff and affected context, compare with the user request, and check applicable standards and UI concerns. Reuse validation evidence. Report concrete findings and gaps briefly. This path needs no reviewer agents, immutable snapshot artifact, exhaustive smell checklist, or separate axis reports. Recheck only the fix delta after a correction.

Read [INDEPENDENT-REVIEW.md](INDEPENDENT-REVIEW.md) and use its independent-axis process when the user or repository explicitly requires it, or for substantial cross-module changes or security or data-integrity risks. Whole-spec delivery follows the same risk criteria. A UI file, new test, or explicit request to review a small diff does not by itself require independent agents.
