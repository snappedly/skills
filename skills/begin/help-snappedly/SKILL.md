---
name: help-snappedly
description: "Help choose the Snappedly skill or workflow that fits the user's current situation."
disable-model-invocation: true
---

# Help Snappedly

Choose the shortest workflow that satisfies the request. A skill is guidance for the current task, not a reason to add another task or start another agent. Recommend the relevant entry point; do not load every skill in the route.

## Start from the request

| Situation | Route |
| --- | --- |
| Clear small fix, copy, styling, or layout edit | Implement directly, or use `/implement` when requested. Inspect the affected result and review the diff locally. |
| Changed logic or a behavioral regression | Focused `/tdd` coverage at an existing public boundary, then applicable checks and local review. |
| Inspect current changes in a browser | `/build-local`; reuse a verified preview and finish once it is ready for inspection. |
| Uncertain or persistent bug | `/diagnosing-bugs`; a clear local defect can be fixed and checked directly. |
| Open visual direction or requested redesign | `/frontend-design`; existing UI corrections follow the established design. |
| A design question needs a runnable experiment | `/prototype`, scoped to that question. |
| User wants to stress-test an idea | `/grill-me`, or `/grill-with-docs` when domain records are useful. |
| Multi-session implementation needs planning | `/to-spec` then `/to-tickets`; `/implement` handles executable tickets. |
| Explicitly deliver a whole spec as one PR/MR | `/implement-spec`. |
| Huge effort with unresolved dependent decisions | `/wayfinder`. |

The user's request is sufficient requirements for a clear small change unless repository policy requires a tracker issue. Use interviews, specs, tickets, and handoffs when they solve a real coordination or decision problem. Working in a repository alone does not require an interview.

## Verification and review

Use `/tdd`'s scope guidance: visually inspect presentation edits; test changed logic. `/code-cleanup` defines applicable checks and evidence reuse. `/code-review` provides local review for low-risk changes and independent axes for substantial, high-risk, or explicitly mandated work. These can run in the current agent; loading a skill never requires its own agent.

`/frontend-guidelines` is available for an explicit UI audit. Routine corrections inspect the affected accessibility and interaction concerns. `/frontend-design` covers open design decisions, rather than every frontend edit.

## Context and handoffs

Continue in the current session while its context is useful. Read files and references only when needed; reuse unchanged requirements and check results. Use `/compact` when context pressure warrants it. Use `/handoff` when another session, directory, harness, or person must continue; retain unresolved questions and links to existing artifacts. A phase transition or prototype does not by itself require a fresh session, branch, or handoff file.

Delegate only a bounded independent task when parallel work or an independent judgment adds value. Keep small lookups, mechanical changes, cleanup, and local review in the current agent. Delegated work returns results to the caller rather than spawning another coordinator.

## Other entry points

- `/triage`: evaluate incoming issues and external PRs/MRs. Already executable tickets need no triage.
- `/research`: investigate a substantive question and capture cited findings. A quick factual lookup needs no research artifact or agent.
- `/improve-codebase-architecture`: explicitly survey architectural friction. An incidental maintainability concern does not start a survey.
- `/resolving-merge-conflicts`: finish an in-progress merge or rebase, preserving intent.
- `/wizard`: produce a procedure for steps only a human can perform.
- `/teach`: sustained learning and practice.
- `/wait-what`: explain the last message more clearly.

## References and configuration

`/domain-modeling` changes domain terminology and records significant decisions; reading an existing glossary does not invoke it. `/codebase-design` supplies vocabulary when an interface decision needs it. `/writing-for-agents` guides agent-document edits, and `/remove-slop` supports requested or useful focused cleanup.

`/setup-snappedly-skills` configures tracker, workflow, domain, and frontend conventions. Existing configuration and user authorization carry forward. Missing setup is relevant when a requested workflow needs that configuration; it is not a prerequisite for an ordinary local edit or preview.
