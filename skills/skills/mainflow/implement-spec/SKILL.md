---
name: implement-spec
description: "Implement a whole specification through parallel ticket work, delivered as one pull or merge request."
disable-model-invocation: true
---

You have been provided a spec. This spec should have tickets associated with it, describing how to implement the spec.

The goal is one GitHub pull request or GitLab merge request that implements the entire spec on a single integration branch.

The tickets are a **task graph**, not a list of steps. Read the blockers and work only the current frontier. Independent tickets may run in parallel; phase transitions and review fixes do not.

Read `docs/agents/workflow.md` before creating the branch. It is the source of truth for required checks and finding disposition. If it is missing, tell the user to run `/setup-snappedly-skills` before creating the branch. If an existing integration branch is being resumed, record the missing configuration as a validation gap and do not claim that repository policy was verified.

## Execution contract

The coordinator owns the phase transitions. Implementers, cleanup, and reviewers return evidence or findings; they do not start another phase recursively.

Before launching work, record an orchestration budget:

- one implementer per ready ticket in the current frontier, with later waves released only after their blockers are integrated;
- zero merger agents for conflict-free integrations, which the coordinator may perform directly; use a resolver only when a conflict requires independent reasoning;
- one integrated cleanup pass before review;
- one parallel set of applicable review axes for one frozen target SHA;
- one coordinated fix batch and at most one affected-axis follow-up review;
- the expected full-suite, typecheck, and build commands, including which evidence may be reused.

The budget is a stop condition, not a target. If actual launches, validation passes, or review cycles would exceed it, pause and report the overage with the smallest safe simplification. Do not automatically add agents or another full validation cycle.

For a two-ticket UI spec, record the trace before work starts. The unbounded path observed in the motivating run included two implementers, merger agents, cleanup at ticket and integration stages, three review axes, a fix assignment, and repeated validation/review work. The bounded path is two ticket implementers, direct conflict-free integration, one integrated cleanup, one applicable review set, one coordinated fix batch, and one affected-axis follow-up. Keep the actual launch and command counts in the handoff. This comparison shows where duplicate full-suite or build commands were removed without removing a required check.

## State machine and barriers

Run these phases in order. Only independent ticket work inside the implementation phase and independent review axes inside a frozen review phase may run concurrently.

| Phase | Integration branch | Allowed work | Exit record |
| --- | --- | --- | --- |
| Frontier / implement | Must not be reviewed or cleaned by the integration workflow | Implementers use separate worktrees and branches for ready tickets. They use `/tdd` at agreed seams and run targeted tests and typechecking. | Ticket commit, changed paths, targeted check results, and remaining frontier. |
| Integrate | Mutable; no review may be active | Coordinator merges conflict-free ticket branches directly. A conflict may use one resolver. Do not run the full suite or production build once per ticket. | Integrated commit SHA and merged ticket list. |
| Cleanup | Mutable only for the cleanup task | Run `/code-cleanup` once on the coherent integrated change. It owns the repository-required full validation for this state. | Cleanup evidence keyed to the cleanup output SHA, with scope and commands. |
| Freeze / review | **Immutable** | Record the exact target SHA and file scope. Run each applicable review axis in parallel as read-only work. Do not merge, edit, stage, or clean the target branch while any axis is active. | One result per applicable axis, all naming the same target SHA, then one aggregate report. |
| Fix | Mutable only after every review axis has returned or been cancelled | Implement one coordinated batch for the complete finding set. Do not start cleanup or follow-up review while fix work is still arriving. | Fix commit SHA, changed files, finding dispositions, and affected checks/axes. |
| Follow-up | Freeze again at the post-fix SHA | Run at most one follow-up review, only for changed files and genuinely affected axes. State the reason for every axis included or skipped. | Follow-up results keyed to the new SHA. A new hard finding stops the workflow for coordinator or user triage. |
| Handoff | Immutable | Update the draft request, report validation and dispositions, and mark it ready only when policy permits. | Pull or merge request URL, final SHA, check evidence, review state, and open follow-up work. |

Every cleanup and review result is keyed to the immutable SHA it inspected. A result for another SHA is stale. Reject only that result, record the expected and observed SHAs, cancel obsolete work, and never silently restart a complete review cycle. If the branch must advance, wait for the old review set to finish or be cancelled, then freeze the new SHA and rerun only the affected check or axis.

## Process

1. Read the complete spec and its tickets, enough to understand the graph and current frontier. Preserve ticket references as context pointers rather than copying their contents into every brief.

2. If exploration is needed, use one exploration subagent and save its notes outside the repository so future implementers can read the same file. Do not launch exploration that does not unblock a ticket.

3. Create the integration branch and a draft pull or merge request before ticket implementation. Mark it as closing the spec issue and tickets according to the provider's issue-closing convention. If the caller supplied an existing integration branch, verify its base and record its starting SHA instead of creating another branch.

4. Launch one implementer per ready ticket, in the background when useful. Every implementer brief must include:

   - the spec, ticket, blocker state, base/integration SHA, and any exploration note;
   - the agreed `/tdd` seam, or an explicit note that this docs-only task has no behavior seam and therefore adds no test;
   - targeted tests and typechecking to run during implementation;
   - the instruction to inspect its own scoped change for cleanup and prose slop, but not to run the integrated full suite or production builds;
   - the requirement to report blocked checks and coverage gaps before committing.

   Implementers commit only their assigned branch. They do not merge, mutate the integration branch, or launch review.

5. Integrate completed ticket branches after their blockers are satisfied. Prefer a direct conflict-free merge or cherry-pick by the coordinator. Use a merger/resolver subagent only for a real conflict or independent reasoning need, and record why it was needed.

6. Once the frontier is empty, run the single integrated `/code-cleanup` pass. Reuse a check only when its files, dependencies, configuration, command, working directory, and scope are unchanged and its evidence names the same target SHA. Full-suite tests and production builds run once for the integrated state when required by repository policy.

7. Freeze the cleanup output SHA and run `/code-review` once. Pass the spec, all tickets, branch base, cleanup evidence, target SHA, and scoped paths. Wait for every applicable axis before starting any fix. A missing applicable axis is not complete unless repository policy records an explicit waiver.

8. If findings require changes, assign one fix batch after the review barrier. Merge it only after all reviewers have returned. Run cleanup only for checks affected by the fix, reusing unchanged evidence under the exact conditions above. Freeze the resulting SHA and run the single bounded follow-up review for affected axes and files.

9. If the follow-up reports a new hard finding, or if the budget would be exceeded, stop the automatic loop and present a concise coordinator/user decision with the exact SHA, finding, check gap, and available options. Do not start a second fix-and-review cycle automatically.

10. Mark the pull or merge request ready only after required checks pass, every applicable review axis has completed or been handled under policy, and every finding has a recorded disposition. Include the before/after orchestration trace in the handoff. For the representative two-ticket UI case, the bounded trace should show at most one implementer per ready ticket, one integrated cleanup, one applicable review set, and one fix/follow-up cycle, while preserving all required checks.

11. Remove implementer worktrees after their commits are integrated or their work is cancelled. Record cancelled agents and the reason so obsolete work is not mistaken for missing evidence.
