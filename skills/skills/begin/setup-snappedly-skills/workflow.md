# Team workflow

How work moves from an agreed request to a production-verified change.

## Source of truth

[Name the GitHub or GitLab issue that holds the approved spec or requirements. State how maintenance work without a separate spec is recorded.]

## Ready to implement

[State what must be agreed before implementation starts and any exceptions to the verification defaults below.]

A small, clear user request can serve as the implementation brief. Ticketed `/implement` work starts from an executable issue or an agent brief whose work item type is executable. A planning spec and a wayfinder decision ticket are not executable work items. `/implement-spec` is the explicit path for delivering a complete planning spec through its child ticket graph.

## Verification scope

Use tdd's scope guidance even when no skill is invoked: visually inspect styling, layout, and copy changes at relevant viewport sizes and exercise static link corrections. Test changed logic, state, validation, and behavioral regressions at existing public boundaries. For mixed changes, verify each part appropriately. Select established seams autonomously; clarify unresolved contracts.

## Required checks

[List configured commands, directories, and applicability for presentation edits, local logic changes, and cross-cutting or release work. Prefer affected-file/package checks and focused tests. Require full suites and production/deployment builds only where risk or delivery needs justify them. Record browser-test server ownership and any supported external-preview setting.]

Reuse passing checks on unchanged inputs. Run broader checks when dependencies or required policy make them relevant.

## Review findings

Small, low-risk changes receive a local review of the diff against the request, applicable standards, and UI concerns. Independent Standards, Spec, and applicable Interface review is reserved for substantial cross-module changes, security or data-integrity risks, or explicit requirements. Whole-spec delivery follows the same risk criteria.

[Record any repository-specific overrides, required independent reviews, and finding-disposition rules below.]

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
