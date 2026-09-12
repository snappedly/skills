---
name: implement-spec
description: "Implement a whole specification through parallel ticket work, delivered as one pull or merge request."
disable-model-invocation: true
---

You have been provided a spec. This spec should have tickets associated with it, describing how to implement the spec.

The goal is one GitHub pull request or GitLab merge request that implements the entire spec on a single integration branch.

The tickets are not a list of steps. They are a **task graph** with blocking relationships between them. This means there is always a **frontier** of tickets which are ready to be grabbed.

Communication to and from subagents should be sparse. Communicate primarily through **context pointers**: to the spec, tickets, research notes, and previous commits. Don't duplicate information already available via pointers.

Read `docs/agents/workflow.md`. It is the source of truth for required checks and finding disposition. If it is missing, tell the user to run `/setup-snappedly-skills` before creating the branch.

**Implementer subagents** should be run in the background where possible for **maximum concurrency**.

## Steps

1. Read the spec and tickets. Read enough to understand the task graph.

2. (optional) Use an **exploration subagent** to conduct any exploration required by the tickets - relevant codebase files or external documentation. Ensure the exploration subagent can save files - it should save its markdown notes in a directory outside the repo, accessible by all future subagents. This lets **implementer subagents** focus on implementation rather than exploration.

3. Create an integration branch and a draft pull or merge request. Mark it as closing the spec issue and tickets according to the provider's issue-closing convention.

4. Use **implementer subagents** to implement tickets whose blockers have been merged into the integration branch. Each implementer subagent should work in its own worktree, on its own branch starting from that integrated state. Include these requirements in every implementer brief, including review-fix assignments:

   - Use /tdd where possible, at pre-agreed seams. Pass along any existing seam agreement; route missing seam decisions through the coordinator before writing those tests.
   - Run typechecking and relevant single test files regularly during implementation.
   - Run /code-cleanup on the task change, including uncommitted and untracked task files, before committing. Commit to the assigned branch only once required checks pass and lint coverage is accounted for. Return validation results and report blocked checks or coverage gaps before proceeding.

5. Once an **implementer subagent** completes, merge its work to the integration branch with a **merger subagent**.

6. If this changes the **frontier** of available tickets, kick off more **implementer subagents** to work on the new tickets. This allows for maximum concurrency.

7. Once all tickets are merged, run /code-cleanup on the integrated PR branch. It owns the final required checks, including the full suite when the repository workflow requires it. Then run /code-review on the integrated PR branch, including uncommitted and untracked task files, and supply the spec, tickets, branch base, and cleanup results. Fix review issues in a single **implementer subagent** and rerun cleanup before committing. Merge the fixes back to the PR branch. If the merge, its conflict resolution, or a changed base alters any checked input, run affected cleanup checks on the integrated branch. Reuse the fix branch's passing evidence only when the integrated files, dependencies, configuration, commands, and scope are unchanged. Review substantive changes again and pass the integrated validation evidence to that review.

8. Mark the pull or merge request as ready for review once required checks pass, every applicable review axis has completed or been handled under repository policy, and every finding has the disposition required by `docs/agents/workflow.md`. Report unresolved checks or coverage gaps before proceeding.

9. Clean up all **implementer subagent** worktrees.
