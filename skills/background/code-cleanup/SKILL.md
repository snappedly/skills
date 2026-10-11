---
name: code-cleanup
description: "Clean and validate a completed change before commit, and return its check record."
license: MIT
---

# Code cleanup

Clean up and validate one coherent change, then return evidence to the caller, which owns commits, phase transitions, and finding disposition.

## Scope and ownership

Read applicable agent instructions, `docs/agents/workflow.md`, CI, and check configuration. Use the caller's base and task scope, including staged, unstaged, and untracked task files. Preserve unrelated work and the index. A review-only request stays read-only and reports missing evidence.

For delegated work, workers run focused tests, typechecks, formatting, lint, prerequisite builds, and local cleanup. Run repository-required full suites and final builds once on the combined change. Follow repository policy when it requires earlier or broader checks, and record those requirements in the caller's notes.

## Match checks to the change

When repository policy leaves scope open, use configured checks for affected files or packages and relevant focused tests. Presentation edits use preview evidence and applicable static checks; full suites and production or deployment builds need a concrete dependency risk, a delivery requirement, or explicit policy. Broaden for shared runtime, dependency, build, security, or data changes.

## Coordinate concurrent checks

Run independent checks in parallel when their resources are isolated. Build output and locks inside separate worktrees are isolated files.

Before browser tests, inspect their server configuration. Let the test runner own its server, or use its supported external-server setting with a verified preview of the same working tree. Check both port and framework lock/output ownership. Resolve a collision before retrying; changing only the port may leave a shared lock conflict. Stop only task-owned servers, and restore a requested preview after testing if needed.

For checks with shared resources, read `workflow.md`'s Concurrent runs section and the check configuration. Prefer supported settings that give each run its own ports and resource names, with teardown limited to that run's resources. Otherwise use the repository's lock to serialize every run using that resource, holding it through teardown. When neither is available, report the remaining race as a coverage gap. Checking for another process does not reserve the resource.

Before using a shared resource, or after a failure that suggests a collision, identify the resource and any run using or removing it. Preserve other tasks' processes and resources. When a check must wait, has a confirmed collision, or resumes from deferral, follow [Deferred checks](EVIDENCE.md#deferred-checks). Record failures without collision evidence as failed.

## Clean, then validate

1. Reuse the caller's check map when its source configuration is unchanged and covers the task. For missing or changed coverage, discover configured checks and their actual scripts, fix/check modes, directories, and file/package scopes. Use installed tools and the declared package manager. Report uncovered file types; add tooling only when requested.
2. Remove obvious accidental clutter in the task diff while preserving behavior and meaning. Load and apply `remove-slop` for requested cleanup or when its detailed guidance is useful; without that skill, do the cleanup directly at the same standard and note that it is missing.
3. Finish scoped formatting and safe lint fixes before read-only checks. Keep semantic fixes with the implementation workflow. Preserve lint rules and suppression policy.
4. Run required checks that lack valid evidence. Independent read-only checks may run in parallel; file mutations must finish first. An aggregate command covers its components. Include whitespace checks for the applicable committed, unstaged, and staged diffs.
5. Return failures or blockers with attribution supported by baseline evidence where practical, marking uncertain attribution as uncertain. Continue independent checks; fixes, review, and further cleanup passes belong to the caller.

## Evidence

A passing check stays valid evidence, through review and handoff, while its inputs remain unchanged. For a small change handled in one agent, a compact command/result record taken after inspecting the final diff is enough. When evidence crosses agents, commits, or handoffs, use [EVIDENCE.md](EVIDENCE.md) for content binding and reuse.

## Result

Return cleanup edits and a compact check record with passing, failing, deferred, blocked, unconfigured, or not-applicable status, warnings, coverage gaps, and reuse/rerun reasons. Include the saved record or its location and the resume condition for deferred checks. Deferred and blocked checks remain unverified and prevent delivery when required. Pre-commit results remain explicitly identified until bound to a commit. Claim validation only for the content and scope actually covered. Done when every required check has a status in the record.
