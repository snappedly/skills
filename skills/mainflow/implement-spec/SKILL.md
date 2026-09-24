---
name: implement-spec
description: "Implement a whole specification through parallel ticket work, delivered as one pull or merge request."
disable-model-invocation: true
---

Deliver the spec and its dependency-aware ticket graph on one integration branch and one pull or merge request. Use `pr` when creating the pull or merge request. The coordinator owns phase transitions; code-cleanup returns validation evidence and code-review returns findings.

Read the spec, all tickets, and `docs/agents/workflow.md`. The workflow defines required checks and finding dispositions. If it is missing, recommend `/setup-snappedly-skills` before branch creation. For an already authorized task, inspect existing CI and contribution rules, state any policy gaps, and preserve the user's scope.

## Select scope and ownership

Invoking implement-spec chooses whole-spec delivery, not a fixed testing or agent count. Assess the integrated change first. For a small, low-risk spec, implement its tickets in the current agent, use focused verification and local cleanup, review the integrated diff locally, and deliver the requested PR/MR. Use the independent review phases below only for substantial cross-module work, security or data-integrity risk, or explicit user/repository requirements.

Assign each check and review once. Workers, including workers using implement, perform ticket or fix implementation, focused checks, local cleanup, and a self-check of their diff. The coordinator owns integrated checks, review selection, finding disposition, and delivery. State this boundary in each brief. Worker completion returns to the coordinator; it does not start another review or orchestration chain.

TDD applies to changed logic according to its scope guidance. Presentation-only tickets use visual verification even inside a large spec. Required integrated checks still cover interactions across tickets.

## Budget and delegation

Before launching agents, state a short budget: implementation assignments, optional exploration, initial applicable review axes, at most one fix assignment, follow-up axes, and expected full validation passes. Derive counts from independent work and risk, rather than UI file or ticket count. Small related tickets normally use no agents; substantial independent tickets may use workers and the required review axes. Cleanup and conflict-free integration stay with the coordinator. Plan one integrated validation pass with the applicable checks; reserve a fix assignment or follow-up reviewers only when needed.

Use implementers in separate worktrees for independent tickets. Share pointers to requirements, relevant files, verification scope, existing test boundaries, and the integrated starting SHA. Small sequential work may stay with the coordinator when delegation adds no reasoning benefit. The coordinator performs conflict-free merges, cleanup, and small final corrections directly. Loading a skill does not require launching another agent. Exploration and conflict resolution agents need a concrete unresolved question and a place in the budget.

Keep briefs bounded to the assignment; avoid copying the full conversation. Reuse a reviewer for a relevant follow-up when possible. Close completed agents. Cancel superseded work promptly, confirm cancellation before mutating its target, and preserve unfinished changes before removing worktrees. Use completion notifications; wait only when the next step depends on the result.

Compare actual launches and full validation passes with the budget before adding work. On an overrun, stop automatic scheduling and report the cause and a concrete reduced plan. Resume only with an explicit coordinator decision within existing authority, or a user decision when scope, requirements, or finding policy would change. Never silently raise the budget.

Keep the ticket graph, verification scope, source pointers, and check commands in the existing run record. Refresh them when requirements or configuration change. Bound parallel work by available workers and independent file ownership; group small related tickets when their dependency order permits, or implement sequentially if delegation is unavailable. Workers return commit SHAs, completed tickets, changed paths, check results, and blockers, with file pointers for detailed logs.

## Phases

| Phase | Work and completion condition |
| --- | --- |
| Implement / integrate | Launch the ready frontier from the current integrated SHA. Implementers run relevant tests and typechecking, scoped formatting/lint, and local cleanup before committing. Integrate completed tickets serially; release newly unblocked tickets. Independent worktrees may keep implementing during integration. |
| Cleanup | After all tickets are integrated, run code-cleanup once on the coherent change. Finish edits, validate, then commit. Bind passing evidence to that commit after verifying it contains the checked content; committing alone requires no repeated checks. |
| Freeze / review | Record the exact target commit and base. For local review, the coordinator inspects the integrated diff once. When independent review is selected, all applicable axes review that same immutable target in parallel. No edit, merge, rebase, staging, cleanup, or fix may affect the target branch until every axis returns or cancellation is confirmed. Aggregate all findings once. |
| Fix / validate | Resolve the aggregate in one batch, directly for small corrections or through one implementer. Run only affected cleanup checks, commit the final content, and preserve evidence for unchanged inputs. |
| Follow-up | Review the fix delta and necessary context locally, or freeze the new SHA and use affected axes when independent review is required. Reuse unchanged findings and check evidence. |
| Handoff | Report final SHA, required checks, axis results, finding dispositions, budget totals, and PR/MR link. Mark ready only when applicable checks and finding policy permit. |

Ticket checks establish local correctness; the integrated cleanup owns any required full-suite tests and production builds. A spec invocation alone does not make those checks required. Follow repository policy if it explicitly requires a broader ticket check, and account for that cost in the budget. Run checks after meaningful changes, not after every edit. Reuse aggregate check results rather than running their components again. Code-cleanup defines evidence reuse; supply its existing results to reviewers rather than invoking cleanup again.

Create or resume the integration branch and draft request with the provider's issue-closing references. If no diff exists yet, create the draft after the first integrated commit. Include verification scope in implementer and fix briefs: use tdd's scope guidance for visual edits versus changed logic. Workers may select established test boundaries; route unresolved contract decisions through the coordinator. Prose-only edits need no artificial keyword tests.

For integrated review, commit all task content, including new files. Preserve unrelated changes separately; an exclusion must not hide an unimplemented requirement. Reviewers use fixed SHAs rather than moving branch names. If a target unexpectedly changes, cancel obsolete work, record old/new SHAs and invalidate affected results. Reuse an unaffected axis only after checking its files, relevant context, requirements, and standards are unchanged, and record the carry-forward reason. A stale result must never be silently relabeled as a review of the new SHA.

## Bounded convergence

Allow one normal fix batch and one follow-up. A local CSS correction normally affects Interface; a test-only correction normally affects Standards and possibly Spec. Explain exceptions from the actual change, including effects on shared code.

Any new or still-open finding after follow-up stops automatic fix/review dispatch. The coordinator triages the full set once: reject an unsupported finding with evidence, make a small authorized correction with affected validation, or request a user decision if the remedy changes scope or policy. Substantive corrections need an explicitly budgeted affected review. Do not waive hard findings, accept heuristic findings without the required authority, or start repeated cycles automatically.

## Run record

Maintain one compact record in the existing task notes or PR evidence. Reuse command outputs and agent reports. Record each agent's ID, purpose, start/completion SHA and status; each check's command, directory, scope, target, result and rerun/duplicate reason; and each integration or review-target change with old/new SHAs and reason. Working-tree checks use the content identity described by code-cleanup until bound to a commit.

At handoff total implementation assignments, integrations (including coordinator merges), cleanup passes, initial/follow-up review rounds and axes, fix batches, agent launches, full validation passes, and duplicate commands. Missing telemetry stays unknown.

Detailed before/after replay belongs to an investigation, not every spec run. For an orchestration investigation, use the scenario in [orchestration-check.md](orchestration-check.md); distinguish measured events from modeled costs.

After delivery, remove only this run's recorded implementer worktrees once workers have stopped, their commits are integrated, and the worktrees are clean. Use non-force Git worktree removal; preserve failed or dirty worktrees and report them.
