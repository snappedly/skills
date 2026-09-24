---
name: codebase-cleanup
description: Scan a whole codebase for unnecessary code and tests, and remove only clear, behavior-preserving redundancy. Use for repository-wide cleanup; use code-cleanup for one change or remove-slop for focused edits.
---

# Codebase cleanup

Make a focused pass over the requested codebase to remove concrete sources of maintenance burden. Preserve runtime behavior and public contracts. If the user asks for an audit only, report candidates without editing.

## Establish the scope

1. Read applicable `AGENTS.md` files and repository workflow instructions. Check `git status` and preserve existing edits, staged content, and untracked files.
2. Follow the user's named package or area. Otherwise, scan authored code and tests across the repository. Skip generated, vendored, dependency, and build-output directories unless they are in scope. In a large monorepo, work package by package and report any areas not covered.
3. Read `CONTEXT.md` and relevant ADRs when present. Learn how the project discovers code through exports, registration, reflection, plugins, configuration, or string-based lookup before calling something unused.

## Look for evidenced slop

Use code search and the project's available language tools to trace candidates to their callers and tests. A search with no matches is a lead, not proof that code is unused.

- **Pass-through wrappers:** Remove a private wrapper only when it adds no domain meaning, policy, validation, observability, laziness, or useful extension point, and inlining it makes the callers clearer. Keep public compatibility wrappers and adapters that enforce a real contract.
- **Low-value tests:** Remove a test only when it asserts no meaningful behavior or duplicates another test without covering a distinct input, contract, boundary, or failure mode. Inspect assertions, fixtures, parameterized cases, snapshots, and integration paths before deciding. Keep regression, edge-case, and public-contract tests even when they look similar.
- **Apparently dead code:** Verify references through exports and dynamic discovery before removing it. Retain code used through reflection, registration, plugins, templates, or external interfaces.
- **Redundant logic and helpers:** Simplify duplicated implementations, needless forwarding layers, and branches or guards whose conditions cannot occur in the established call path. Do not refactor for taste or replace a concrete implementation with a speculative abstraction.

For every edit, be able to explain what complexity or maintenance burden it removes and why callers cannot observe a behavior change. If that case is uncertain, leave the code intact and report the evidence needed to decide.

## Make and report changes

Apply small, reviewable edits within the requested scope. Keep unrelated work untouched. Do not broaden cleanup into API changes, architecture redesign, formatting sweeps, or behavior fixes. Do not add replacement tests just to preserve a removed test's count.

Inspect the final diff and report the cleanup made, the code and test areas covered, and any worthwhile candidates left untouched with the reason. Do not claim that behavior was verified unless the user requested verification and the relevant checks were run.
