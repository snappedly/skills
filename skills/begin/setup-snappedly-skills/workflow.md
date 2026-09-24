# Team workflow

How work moves from an agreed request to a production-verified change.

## Source of truth

[Name the GitHub or GitLab issue that holds the approved spec or requirements. State how maintenance work without a separate spec is recorded.]

## Ready to implement

[State what must be agreed before implementation starts and any exceptions to the verification defaults below.]

A small, clear user request can serve as the implementation brief. Ticketed `/implement` work starts from an executable issue or an agent brief whose work item type is executable. A planning spec and a wayfinder decision ticket are not executable work items. `/implement-spec` is the explicit path for delivering a complete planning spec through its child ticket graph.

## Verification scope

Use tdd's scope guidance even when no skill is invoked: visually inspect styling, layout, and copy changes at relevant viewport sizes and exercise static link corrections. Test changed logic, state, validation, and behavioral regressions at existing public boundaries. For mixed changes, verify each part appropriately. Select established seams autonomously; clarify unresolved contracts.

## Feedback loops

Use this section as the repository's feedback-loop contract. Agents and humans should be able to discover the shortest trustworthy path from an edit to evidence without learning a tool-specific workflow. Record commands exactly as the repository invokes them and write `not configured` or `not applicable` when a surface does not exist.

### Fast local and agent loop

- Format/autofix: [command, staged scope, and whether it restages changes, or `not configured`].
- Static feedback: [typecheck and/or lint command, scope, or `not configured`].
- Focused behavior: [test command and public seam scope for changed logic, or `not configured`].
- Frontend feedback: [preview command, server ownership, URL setting, and visual scope, or `not applicable`].

The default sequence is format changed files, run the fastest reliable static check, then run focused tests for changed behavior. Use the repository's package manager and established scripts. An agent reports the command, result, and scope for every applicable check.

### Broader and release loop

- Full suite: [command and applicability].
- Build/package output: [command and applicability].
- Cross-cutting, migration, smoke, or release checks: [commands and applicability].
- CI enforcement: [workflow, required jobs, and changed-file/package scope].
- Hook enforcement: [pre-commit, pre-push, or other hook behavior, or `not configured`].

Broader checks are required when repository policy, dependency/build/package changes, security or data-integrity risk, or delivery needs justify them. Do not install new tooling from this contract without an explicit project decision; document missing coverage and the trigger for adding it.

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

## Delivery and closure

This policy governs implementation delivery and completion-based closure. Apply it within the requested task and configured delegation; a review-only task stays read-only. Provider commands and relationships come from `docs/agents/issue-tracker.md`.

| Transition | Trigger and prerequisites | Actor | Required evidence |
| --- | --- | --- | --- |
| Push branch and create/update PR/MR | [When to publish; draft or ready; applicable checks] | [Agent or human] | [Commit, checks, or other evidence] |
| Merge PR/MR | [Checks and approvals required before merge] | [Agent, provider automation, or human] | [Passing checks and recorded approval, if required] |
| Close executable ticket | [Verified implementation, merge, sign-off, deployment verification, or named event] | [Agent, provider automation, or human] | [Evidence proving this ticket meets the condition] |
| Close parent spec | [Independent acceptance condition for the whole spec] | [Agent, provider automation, or human] | [Whole-spec acceptance evidence] |

[Record the base branch, merge strategy, and whether preview deployments may run before production approval. For required sign-off, name the approver, where approval is recorded, and the revision or scope it covers. Define custom events with observable completion conditions. Use `not applicable` for unused transitions.]

Follow each transition's configured actor and prerequisites. Reuse applicable recorded approval; ask only for missing decisions or sign-off. If an event is pending, leave that transition pending and report the next actor and evidence needed. Verify the resulting PR/MR or tracker state after an authorized action, including provider automation; issuing a command or adding a closing reference is not proof of closure.

Use automatic closing references only for items configured to close on that merge and whose other closure prerequisites are satisfied. Use ordinary links for items awaiting another event or human closure. Apply ticket and parent-spec rules separately: completing child tickets does not itself establish spec acceptance. Integration into a task branch establishes dependency readiness independently of tracker closure.

## Production release

A human must approve the exact production candidate before deployment starts. The approval request names the commit and immutable artifact when available, target environment, changes, validation, migrations, verification plan, and recovery procedure. Any changed candidate requires a new approval.

[State how the release system identifies the candidate and enforces approval, the deployment command or workflow, and the production environment. If merging triggers production, name the deployment-system approval gate that pauses it.]

## Verification and recovery

[State the production checks and health signals that verify the changed behavior. State the rollback or roll-forward procedure, who may run it, and migration constraints that can make rollback unsafe.]

## Handoff

[State what a handoff must report. Include required check results, skipped review axes and reasons, finding dispositions, pull or merge request and merged revision, ticket and spec states, pending delivery/closure events and their next actor, production candidate and approval state, deployment result, verification evidence, and open recovery or follow-up work.]
