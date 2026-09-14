---
name: code-cleanup
description: "Clean and validate completed changes before commit, including behavior-preserving slop removal where applicable"
---

# Code cleanup

Perform mechanical cleanup and required validation for one coherent change. Return evidence to the caller, which owns commits, phase transitions, and finding disposition. Run this skill in the current agent; it does not need a dedicated agent.

## Scope and ownership

Read applicable agent instructions, `docs/agents/workflow.md`, CI, and check configuration. Use the caller's base and task scope, including staged, unstaged, and untracked task files. Preserve unrelated work and the index. A review-only request stays read-only and reports missing evidence.

Under implement-spec, ticket agents run targeted tests, typechecking, formatting/lint, and local cleanup. One integrated cleanup owns repository-required full tests and builds. Standalone cleanup runs the required checks for the caller's change. Repository policy overrides default scoping; record broader requirements in the budget.

## Clean, then validate

1. Discover configured checks and their actual scripts, fix/check modes, directories, and file/package scopes. Use installed tools and the declared package manager. Report uncovered file types; add tooling only when requested.
2. Apply remove-slop in the current agent when the authorized scope contains code or prose. Otherwise record it as not applicable. Keep edits behavior- or meaning-preserving.
3. Finish scoped formatting and safe lint fixes before read-only checks. Keep semantic fixes with the implementation workflow. Preserve lint rules and suppression policy.
4. Run required checks that lack valid evidence. Independent read-only checks may run in parallel; file mutations must finish first. An aggregate command covers its components. Include whitespace checks for the applicable committed, unstaged, and staged diffs.
5. Return failures or blockers with attribution supported by baseline evidence where practical. Report uncertain attribution honestly. Continue independent checks; do not recursively launch fixes, review, or another cleanup pass.

## Evidence and reuse

Record each command, working directory, scope, result, and the content checked. For committed content, use its full SHA. For pre-commit checks, record HEAD plus an immutable patch or content digest covering staged, unstaged, and untracked task content. Preserve the relevant configuration, dependency/tool versions, and environment assumptions in the check record. Use existing Git diffs, blob/tree IDs, or check outputs; do not build a custom manifest or cache framework.

After validation, the caller may commit. Verify that the commit contains the checked content, including new files, and bind the evidence to that SHA. A content-preserving commit, cherry-pick, or merge does not require running checks again. Hooks or conflict resolution that change checked inputs invalidate affected results.

Across later commits, reuse a passing result only when its checked files and relevant dependencies, configuration, command, directory, scope, tool versions, and environment assumptions remain unchanged. Record the original validated SHA, current target SHA, and concrete comparison supporting reuse. Consider transitive inputs, not just files named in the command. If coverage or equivalence cannot be established, rerun the affected check. A changed SHA, report timestamp, or evidence label alone does not invalidate a result.

A fix may require a full test/build rerun when it affects inputs to that check. Explain that dependency; never reuse evidence merely to meet the budget. Repository-required CI still runs, but the coordinator need not duplicate equivalent passing CI locally.

## Result

Return cleanup edits and a compact check record with passing, failing, blocked, unconfigured, or not-applicable status, warnings, coverage gaps, and reuse/rerun reasons. Pre-commit results remain explicitly identified until bound to a commit. Claim validation only for the content and scope actually covered. Supply this record to review and handoff without rerunning unchanged checks.
