# Team workflow

How work moves from an agreed request to a production-verified change.

## Source of truth

[Name the GitHub or GitLab issue that holds the approved spec or requirements. State how maintenance work without a separate spec is recorded.]

## Ready to implement

[State what must be agreed before implementation starts. Include the test seams that require user confirmation.]

An individual `/implement` run starts from an executable issue or an agent brief whose work item type is executable. A planning spec and a wayfinder decision ticket are not executable work items. `/implement-spec` is the explicit path for delivering a complete planning spec through its child ticket graph.

## Delivery flow

`clarify -> specify -> ticket -> implement -> code-cleanup -> code-review -> deliver -> handoff`

- New features, bug fixes, and changed logic start with a failing test at an agreed seam.
- Implementation may run targeted checks for feedback. `code-cleanup` owns the final required checks for the state it produces.
- After review fixes, rerun cleanup for the affected scope. If a merge, conflict resolution, or changed base alters checked inputs, rerun affected checks on the integrated branch before substantive changes return to review.

## Required checks

[List the formatter, linter, typecheck, test, and build commands that `code-cleanup` must run, including their working directories and when each one applies.]

## Review findings

[State which review axes apply and record any repository-specific override to the defaults below.]

- Every applicable review axis must complete unless the user explicitly waives a missing axis under repository policy.
- A heuristic Standards concern may be fixed and re-reviewed, or explicitly accepted or deferred by the user.
- A Spec gap or documented-standard violation requires a fix or an explicit user change to the source requirement or standard.
- An Interface violation requires a fix or an explicit user waiver under repository policy.

## Pull or merge request

The agent may push the task branch, create or update its GitHub pull request or GitLab merge request, fix task-related failures, and merge after every required check and repository review passes.

[State the base branch, pull or merge request requirements, merge strategy, issue-closing point, and whether preview deployments may run before production approval.]

## Production release

A human must approve the exact production candidate before deployment starts. The approval request names the commit and immutable artifact when available, target environment, changes, validation, migrations, verification plan, and recovery procedure. Any changed candidate requires a new approval.

[State how the release system identifies the candidate and enforces approval, the deployment command or workflow, and the production environment. If merging triggers production, name the deployment-system approval gate that pauses it.]

## Verification and recovery

[State the production checks and health signals that verify the changed behavior. State the rollback or roll-forward procedure, who may run it, and migration constraints that can make rollback unsafe.]

## Handoff

[State what a handoff must report. Include required check results, skipped review axes and reasons, finding dispositions, pull or merge request and merged revision, production candidate and approval state, deployment result, verification evidence, and open recovery or follow-up work.]
