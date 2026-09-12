---
name: implement
description: "Implement a piece of work based on a spec or set of tickets."
disable-model-invocation: true
---

Implement the work described by the user in the spec or tickets.

Confirm that the requested work is one executable issue, ticket, or agent brief. A planning spec or wayfinder decision ticket must first go through `/to-tickets`; use `/implement-spec` only when the user explicitly asks to deliver the whole spec as one integrated pull request.

Read `docs/agents/workflow.md`. It is the source of truth for required checks and finding disposition. If it is missing, tell the user to run `/setup-snappedly-skills` before the change can be committed.

Use /tdd where possible, at pre-agreed seams.

Run typechecking and relevant single test files regularly while implementing. Treat them as development feedback, not final validation evidence.

Once done, run /code-cleanup on the task change. It owns the final required checks for the state it produces. Then use /code-review on that same scope, including uncommitted and untracked files, and supply the spec or ticket as the review's requirements. After review fixes, rerun cleanup for the affected scope and review substantive changes again.

Commit your work to the current branch once required checks pass, every applicable review axis has completed or been handled under repository policy, and every finding has the disposition required by `docs/agents/workflow.md`. If checks are blocked or coverage is missing, report the gap before proceeding; a completed cleanup report alone does not establish readiness to commit.

Implementation stops at the verified commit. Use `/deliver` to push it, merge it, obtain production approval, deploy it, and verify it.
