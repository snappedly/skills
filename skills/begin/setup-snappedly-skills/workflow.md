# Team workflow

How work moves from an agreed request to a production-verified change.

## Source of truth

[Name the work item or brief that holds the approved spec or requirements. State how maintenance work without a separate spec is recorded.]

## Ready to implement

[State what must be agreed before implementation starts and any exceptions to the verification defaults below.]

The main flow is `/grill` (optional), `/execute`, `/clean-up`, then `/submit` for a person to review and merge, or `/deploy` to skip that review and have the agent merge; every step after `/grill` reads this file for checks, review depth, finding disposition, and the delivery and closure table below. A small, clear user request can serve as the implementation brief. Ticketed work starts from an executable issue or agent brief, which `/execute` takes as its plan. A planning spec is not an executable work item; its executable child tickets carry the work.

`/clean-up` leaves its edits unstaged and uncommitted on the current branch and shows what it changed. `/submit` and `/deploy` commit pending task changes, cleanup edits included, before delivery, or deliver the existing HEAD when none remain. An explicit commit request can also commit the batch; on the base or default branch it first creates a task branch, as `/submit` and `/deploy` do. Recorded commit checks, conventions, delivery actors, and approval requirements still apply.

## Verification scope

Use tdd's scope guidance even when no skill is invoked: visually inspect styling, layout, and copy changes at the viewports recorded under Feedback loops and exercise static link corrections. Test changed logic, state, validation, and behavioral regressions at existing seams. For mixed changes, verify each part appropriately. Select established seams autonomously; clarify unresolved contracts.

## Feedback loops

Use this section as the repository's feedback-loop contract. Record commands exactly as the repository invokes them and write `not configured` or `not applicable` when a surface does not exist.

### Fast local and agent loop

- Format/autofix: [command, staged scope, and whether it restages changes, or `not configured`].
- Static feedback: [typecheck and/or lint command, scope, or `not configured`].
- Focused behavior: [test command and public seam scope for changed logic, or `not configured`].
- Frontend feedback: [preview command, server ownership, URL setting, and visual scope, or `not applicable`].
- Viewports: [the named viewport sizes visual checks cover, such as a mobile and a desktop width, or `not applicable`].

The default sequence is format changed files, run the fastest reliable static check, then run focused tests for changed behavior. Use the repository's package manager and established scripts. An agent reports the command, result, and scope for every applicable check.

### Broader and release loop

- Full suite: [command and applicability].
- Build/package output: [command and applicability].
- Cross-cutting, migration, smoke, or release checks: [commands and applicability].
- CI enforcement: [workflow, required jobs, and changed-file/package scope].
- Hook enforcement: [pre-commit, pre-push, or other hook behavior, or `not configured`].

Broader checks are required when repository policy, dependency/build/package changes, security or data-integrity risk, or delivery needs justify them. Adding tooling requires an explicit project decision; until then, document missing coverage and the trigger for adding it.

## Required checks

[List configured commands, directories, and applicability for presentation edits, local logic changes, and cross-cutting or release work. Prefer affected-file/package checks and focused tests. Require full suites and production/deployment builds only where risk or delivery needs justify them. Record browser-test server ownership and any supported external-preview setting.]

Complete cleanup and applicable verification before a change is delivered. A small change can perform these steps and its local review inline; separate skill invocations and reports are optional. Reuse passing checks on unchanged inputs. After review fixes, rerun only the affected checks and review the changed scope.

## Review findings

Small, low-risk changes receive a local review of the diff against the request, applicable standards, and UI concerns. Independent Standards, Spec, and applicable Interface review is reserved for substantial cross-module changes, security or data-integrity risks, or explicit requirements.

[Record any repository-specific overrides, required independent reviews, and finding-disposition rules below.]

- Every applicable review axis must complete unless the user explicitly waives a missing axis under repository policy.
- A heuristic Standards concern may be fixed and re-reviewed, or explicitly accepted or deferred by the user.
- A Spec gap or documented-standard violation requires a fix or an explicit user change to the source requirement or standard.
- An Interface violation requires a fix or an explicit user waiver under repository policy.

## Delivery and closure

This policy governs implementation delivery and completion-based closure. Apply it within the requested task and configured delegation; a review-only task stays read-only. Code-host operations come from `docs/agents/code-host.md`. Work-item operations and relationships come from `docs/agents/issue-tracker.md`.

- Base branch: [the branch change requests target and merge into]
- Merge strategy: [merge, squash, or rebase]

| Transition | Trigger and prerequisites | Actor | Required evidence |
| --- | --- | --- | --- |
| Publish branch and create or update change request when required | [When to publish; draft or ready; applicable checks; branch-only delivery or another review equivalent when explicitly chosen] | [Agent or human] | [Commit, checks, or other evidence] |
| Merge or deliver change | [Checks and approvals required before merge or delivery] | [Agent, agent on a named human's instruction to merge, such as `/deploy` (invocation approval), provider automation, or human] | [Passing checks and recorded approval, if required] |
| Close executable ticket | [Verified implementation, merge, sign-off, deployment verification, or named event] | [Agent, provider automation, or human] | [Evidence proving this ticket meets the condition] |
| Close parent spec | [Independent acceptance condition for the whole spec] | [Agent, provider automation, or human] | [Whole-spec acceptance evidence] |
| Last child ticket closes without closing the spec | [Comment on the spec that it is ready for acceptance, or report only] | [Agent] | [Comment link, or the report] |
| Verify production | [The release of the merged commit; checks under Verification and recovery] | [Agent, provider automation, or human] | [Released revision and verification results] |

[Record whether preview deployments may run before production approval. For required sign-off, name the approver, where approval is recorded, and the revision or scope it covers. For invocation approval, name the approver, their code host account, and where approval is recorded. For each agent transition that follows a human or external event, name what starts the agent. Define custom events with observable completion conditions. Use `not applicable` for unused transitions.]

Under invocation approval, the named approver's instruction to merge approves merging the hosted change request that carries what their checkout holds at that moment, which they are expected to have reviewed. `/deploy` is one form of that instruction. The agent cannot tell who sent an instruction, so one queued, scheduled, or sent by another agent in the approver's session also counts as their approval.

Every agent transition needs something that starts the agent: an earlier agent step in the same run, such as a merge under invocation approval, or a recorded event, such as the merger running `/deploy` again after merging on the host. Follow each transition's configured actor and prerequisites. Reuse applicable recorded approval; ask only for missing decisions or sign-off. If an event is pending, leave that transition pending and report the next actor and evidence needed. Verify the resulting change-request or tracker state after an authorized action, including provider automation; issuing a command or adding a closing reference is not proof of closure.

Use automatic closing references only for items configured to close on that merge and whose other closure prerequisites are satisfied. Use ordinary links for items awaiting another event or human closure. Apply ticket and parent-spec rules separately: completing child tickets does not itself establish spec acceptance.

## Production release

A human must approve the exact production candidate before deployment starts. The approval request names the commit and immutable artifact when available, target environment, changes, validation, migrations, verification plan, and recovery procedure. Any changed candidate requires a new approval. Under invocation approval, the candidate is the approved change merged onto the current base, so a base that only moved ahead keeps the approval; content the approver's checkout did not hold needs the approval request above. `/deploy` ends after the merge's close-out, including production verification when the agent owns it, and reports the next step this section names; the release itself follows the approval and process recorded here.

[State what happens after merge and who starts the release, how the release system identifies the candidate and enforces approval, the deployment command or workflow, and the production environment. If merging triggers production, name the deployment-system approval gate that pauses it, or record invocation approval as the production approval.]

## Verification and recovery

[State the production checks and health signals that verify the changed behavior. State the rollback or roll-forward procedure, who may run it, and migration constraints that can make rollback unsafe.]

## Handoff

[State what a handoff must report. Include required check results, skipped review axes and reasons, finding dispositions, change request or review record and merged revision, ticket and spec states, pending delivery/closure events and their next actor, and open follow-up work. For a production release, also include the candidate and approval state, deployment result, verification evidence, and open recovery work.]
