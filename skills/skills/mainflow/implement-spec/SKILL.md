---
name: implement-spec
description: "Implement a whole specification through parallel ticket work, delivered as one pull or merge request."
disable-model-invocation: true
---

Deliver the supplied spec and its ticket dependency graph on one integration branch, in one GitHub pull request or GitLab merge request. The **frontier** contains tickets whose blockers are integrated.

Read `docs/agents/workflow.md`. It is the source of truth for required checks and finding disposition. If it is missing, tell the user to run `/setup-snappedly-skills` before creating the branch.

Keep the coordinator focused on scheduling, integration, and final delivery. Workers own implementation and targeted investigation.

## Steps

1. Read the spec, tickets, and repository workflow once. Record the graph and existing test-seam agreements in a shared run brief outside the tracked tree. Include pointers to required instructions and the repository's check commands with their scopes. Update this brief when requirements, policy, or check configuration changes; workers read the relevant sources instead of rediscovering the whole workflow.

2. Use a shared exploration agent only when multiple tickets need the same unresolved investigation. Save its findings with source paths in the run brief's directory. Otherwise let the assigned implementer investigate its ticket.

3. Create an integration branch and a draft pull or merge request. Mark it as closing the spec issue and tickets according to the provider's issue-closing convention.

4. Assign frontier tickets to background implementers in separate worktrees starting from the current integration commit. Bound concurrency by available workers and independent file ownership. Group small related tickets in one assignment when their dependency order can be preserved; serialize tickets that would compete over the same files. If delegation is unavailable, perform these assignments sequentially. Give each assignment its ticket and spec pointers, integration SHA, owned scope, run-brief path, and these requirements:

   - Use /tdd where possible, at pre-agreed seams. Pass along any existing seam agreement; route missing seam decisions through the coordinator before writing those tests.
   - Run affected tests during implementation and typechecks when the changed scope needs them. Reuse passing evidence while its inputs remain unchanged.
   - Run /code-cleanup on the assigned change, including uncommitted and untracked task files, before committing. Supply the shared check guidance and existing results. Commit only once required checks pass and lint coverage is accounted for. Repository policy determines when broad checks are required.
   - Return the commit SHA, completed ticket IDs, changed paths, check commands/scopes/results, and blockers. Keep detailed logs in files and return their paths. Report completion or a concrete blocker; use completion notifications or a blocking wait instead of repeated status polling.

5. The coordinator serially merges completed work into the integration branch. Perform routine merges directly. Delegate conflict investigation only when it needs substantial context, preferably to the implementer that owns the change. Check merge results before marking tickets integrated.

6. Update the recorded frontier after each integration and dispatch newly ready work. Reuse an implementer's context for related fixes when supported. Refresh ticket contents only when requirements change or a blocker needs clarification.

7. Once all tickets are integrated, run /code-cleanup on the integrated PR branch with the accumulated validation evidence. It owns final required checks, including the full suite where required. Then run /code-review with the spec and ticket pointers, fixed comparison SHAs, task scope including untracked files, and those cleanup results. Fix findings in one implementer assignment, rerun affected cleanup, and integrate the fixes. Reuse passing evidence only when files, dependencies, configuration, command, and scope are unchanged; otherwise rerun affected checks. Review substantive fixes and their affected callers against the prior reviewed state, retaining earlier findings and coverage. Broaden review when a fix changes a shared assumption or requirement.

8. Mark the pull or merge request as ready for review once required checks pass, every applicable review axis has completed or been handled under repository policy, and every finding has the disposition required by `docs/agents/workflow.md`. Report unresolved checks or coverage gaps before proceeding.

9. Remove this run's implementer worktrees after their work is integrated, workers have stopped, and the worktrees are clean. Preserve failed or dirty worktrees and report them. Use ordinary non-force Git worktree removal scoped to the recorded paths. This delivery step does not invoke the global `cleanup-local` maintenance skill or update installed skills.
