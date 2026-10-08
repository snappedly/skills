---
name: help-snappedly
description: "Help choose the Snappedly skill or workflow that fits the user's current situation."
disable-model-invocation: true
license: MIT
---

# Help Snappedly

Recommend the shortest workflow that satisfies the request and name its entry point; that entry point loads the rest of its route.

## Start from the request

| Situation | Route |
| --- | --- |
| Clear small fix, copy, styling, or layout edit | Implement directly. Inspect the affected result and review the diff locally. |
| Changed logic or a behavioral regression | Focused `/tdd` coverage at an existing seam, then applicable checks and local review. |
| Carry out the plan the conversation settled on | `/execute` (implementation, cleanup, review, and preview), then `/clean-up` as the final check and change report. |
| Carry out a tracker issue or its agent brief | `/execute` with the issue, such as `/execute #42`, then `/clean-up`. |
| Finish a batch of your own changes | `/clean-up`: cleanup, review, clear fixes, and a report showing what changed. Edits stay uncommitted. |
| Happy with the branch and want it merged | `/deploy`: commit pending changes, push, open or update the PR, merge it once its checks pass, then close out tickets and verify production as the workflow assigns. Under invocation approval, your `/deploy` approves the merge, and it asks first only when content from outside your checkout entered the delivery, such as merge conflicts it resolved. It stops at mergeable when the workflow assigns the merge to a human or a merge would deploy to production without a recorded approval gate or invocation approval. |
| Merged a PR on the host yourself | `/deploy` on its branch, or naming the PR, such as `/deploy #42`: verify the merge, then close out and verify production as the workflow assigns. |
| Inspect current changes in a browser | `/build-local`. |
| Uncertain or persistent bug | `/diagnosing-bugs`; a clear local defect can be fixed and checked directly. |
| User asks what would have prevented a bug, or how a session's difficulties should change the agent's environment | `/retro` in the same session, or with that session's log. |
| User asks to survey architectural friction across the codebase or around a PR, commit, or branch, or to investigate a missing regression-test seam | `/improve-codebase-architecture`, scoped to what the user names. |
| A design question needs a runnable experiment | `/prototype`, scoped to that question. |
| User wants to stress-test an idea | `/grill`, then `/execute` when the confirmed plan is a code change. |
| Enumerate user journeys or process outcomes and expose missing cases | `/workflow-mapping`. |
| Large effort spanning several sessions | `/grill` to settle the plan, `/research` or `/prototype` for its open questions, then `/execute` one slice at a time. |

The user's request is sufficient requirements for a clear small change unless repository policy requires a tracker issue. Use interviews, specs, tickets, and handoffs when they solve a real coordination or decision problem.

## Verification and review

Use `/tdd`'s scope guidance: visually inspect presentation edits; test changed logic. `/code-cleanup` defines applicable checks and evidence reuse. `/code-review` provides local review for low-risk changes and independent axes for substantial, high-risk, or explicitly mandated work.

Routine UI corrections inspect the affected accessibility and interaction concerns. For an explicit UI audit, request `/code-review`; it applies the pinned interface guidelines and the repository's accessibility baseline at any review depth.

## Context and handoffs

Continue in the current session while its context is useful, and compact the context with the harness when context pressure warrants it. When another session, directory, harness, or person must continue, summarize the state with unresolved questions and links to existing artifacts.

Run skills in the current agent; loading one never needs its own agent. Delegate a bounded independent task only when parallel work or an independent judgment adds value; small lookups, mechanical changes, cleanup, and local review stay in the current agent. Delegated work returns results to the caller rather than spawning another coordinator.

## Other entry points

- `/triage`: evaluate incoming issues and external PRs. Already executable tickets skip triage.
- `/research`: investigate a substantive question and capture cited findings. Answer a quick factual lookup directly.
- `/codebase-cleanup`: hunt for slop across a codebase or subsystem, such as dead code, useless tests, and unnecessary wrappers.
- `/resolving-merge-conflicts`: finish an in-progress merge or rebase, preserving intent.
- `/wait-what`: explain the last message more clearly.

## References and configuration

`/domain-modeling` is for changing domain terminology or recording a significant decision; read an existing glossary directly. `/codebase-design` supplies vocabulary when an interface decision needs it. `/writing-for-agents` guides agent-document edits, `/technical-writing` sets the standard for docs, tickets, and PR descriptions, `/pr` makes a pull request reviewable, and `/remove-slop` removes slop when asked or when a focused cleanup helps.

`/setup-snappedly-skills` configures code host, tracker, workflow, domain, and frontend conventions; existing configuration and user authorization carry forward. Recommend it when a requested workflow needs configuration the repository lacks; ordinary local edits and previews run without it.
