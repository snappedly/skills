---
name: code-cleanup
description: "Clean and validate completed changes before commit, including behavior-preserving slop removal where applicable"
---

# Code cleanup

Perform mechanical cleanup and required validation for one coherent change. Return evidence to the caller, which owns commits, phase transitions, and finding disposition. Run this skill in the current agent; it does not need a dedicated agent.

## Scope and ownership

Read applicable agent instructions, `docs/agents/workflow.md`, CI, and check configuration. Use the caller's base and task scope, including staged, unstaged, and untracked task files. Preserve unrelated work and the index. A review-only request stays read-only and reports missing evidence.

Under implement-spec, ticket agents run targeted tests, typechecking, formatting/lint, and local cleanup. One integrated cleanup owns repository-required full tests and builds. Standalone cleanup runs the required checks for the caller's change. Repository policy overrides default scoping; record broader requirements in the caller's existing notes.

## Match checks to the change

When repository policy leaves scope open, use configured checks for affected files or packages and relevant focused tests. Presentation edits use preview evidence and applicable static checks; full suites and production or deployment builds need a concrete dependency risk, a delivery requirement, or explicit policy. Broaden for shared runtime, dependency, build, security, or data changes.

For a small change handled in one agent, use the steps below and return a compact command/result record after inspecting the final diff; stop there. The detailed content-binding rules below apply when evidence crosses agents, commits, or handoffs. Reuse a passing check while its inputs remain unchanged.

Before browser tests, inspect their server configuration. Let the test runner own its server, or use its supported external-server setting with a verified preview of the same working tree. Check both port and framework lock/output ownership. Resolve a collision before retrying; changing only the port may leave a shared lock conflict. Stop only task-owned servers, and restore a requested preview after testing if needed.

## Clean, then validate

1. Reuse the caller's check map when its source configuration is unchanged and covers the task. For missing or changed coverage, discover configured checks and their actual scripts, fix/check modes, directories, and file/package scopes. Use installed tools and the declared package manager. Report uncovered file types; add tooling only when requested.
2. Remove obvious accidental clutter in the task diff while preserving behavior and meaning. Consult remove-slop for requested cleanup or when its detailed guidance is useful; ordinary formatting needs no separate invocation or prose audit.
3. Finish scoped formatting and safe lint fixes before read-only checks. Keep semantic fixes with the implementation workflow. Preserve lint rules and suppression policy.
4. Run required checks that lack valid evidence. Independent read-only checks may run in parallel; file mutations must finish first. An aggregate command covers its components. Include whitespace checks for the applicable committed, unstaged, and staged diffs.
5. Return failures or blockers with attribution supported by baseline evidence where practical. Report uncertain attribution honestly. Continue independent checks; do not recursively launch fixes, review, or another cleanup pass.

## Evidence across agents or revisions

When evidence crosses agents, commits, or handoffs, use [EVIDENCE.md](EVIDENCE.md) for content binding and reuse. A small change within one agent uses the compact record described above.

## Result

Return cleanup edits and a compact check record with passing, failing, blocked, unconfigured, or not-applicable status, warnings, coverage gaps, and reuse/rerun reasons. Pre-commit results remain explicitly identified until bound to a commit. Claim validation only for the content and scope actually covered. Supply this record to review and handoff without rerunning unchanged checks.
