---
name: implement
description: "Implement a clear request, executable ticket, or agent brief with verification proportional to risk."
disable-model-invocation: true
---

Implement the user request, spec, or tickets.

Use a clear user request as the brief for a small change; no separate ticket is needed unless repository policy requires it. For ticketed work, confirm that the requested work is one executable issue, ticket, or agent brief. A planning spec or wayfinder decision ticket must first go through `/to-tickets`; use `/implement-spec` only when the user explicitly asks to deliver the whole spec as one integrated pull request.

Read `docs/agents/workflow.md`. It is the source of truth for required checks and finding disposition. If it is missing, use applicable agent instructions, CI, and contribution rules; report material policy gaps without blocking an otherwise authorized small edit.

## When assigned by a coordinator

If implement-spec or another coordinator assigned this ticket or fix, its brief defines the worker scope. Implement it, run focused verification and local cleanup, inspect the diff, and return the requested commit, check results, and gaps. Stop there. Integrated validation, independent review, follow-up dispatch, and PR/MR delivery belong to the coordinator; a worker does not start the standalone completion workflow below. Explicit repository requirements for ticket-level checks still apply; report their cost and results for reuse.

## Implement and verify

Choose verification using /tdd's scope guidance: visually inspect presentation edits, use focused test-first coverage for changed logic, and broaden checks for shared or high-risk behavior. Follow existing frontend conventions; a spacing or copy correction needs no design exercise.

Run focused checks after meaningful changes. Passing checks on the final unchanged inputs count as validation evidence.

For standalone work, choose completion by risk. For a small, low-risk edit, finish formatting and applicable checks, inspect the full task diff including new files against the request, and report the result. This is sufficient cleanup and local review; separate skill invocations and reports are optional. For larger work, run /code-cleanup on the task change, then /code-review on the same scope, including uncommitted and untracked files. Supply the user request, spec, or ticket as requirements. Both run in the current agent for a small, low-risk change. Independent review is reserved for the criteria in /code-review or explicit repository requirements. After a fix, rerun only affected checks and inspect the fix delta; unchanged work needs no repeated review round.

Commit your work to the current branch once required checks pass, the selected local review or required independent axes have completed or been handled under repository policy, and every finding has the disposition required by `docs/agents/workflow.md`. If checks are blocked or coverage is missing, report the gap before proceeding; a completed cleanup report alone does not establish readiness to commit.

Implementation stops at the verified commit. Continue with the repository's own pull or merge request and release process.
