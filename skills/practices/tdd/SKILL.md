---
name: tdd
description: Test-driven development for changed logic, state transitions, validation, and behavioral regressions, or explicit test-first requests. Visual styling, layout, copy, and documentation edits use direct inspection unless they change a behavioral contract. Also the reference for test quality and test seams.
---

# Test-Driven Development

TDD is the red → green loop. This skill is the reference that makes that loop produce tests worth keeping: what a good test is, where tests go, the anti-patterns, and the rules of the loop. Choose coverage proportional to the changed contract; consult detailed examples when needed.

When exploring the codebase, read `CONTEXT.md` (if it exists) so test names and interface vocabulary match the project's domain language, read `docs/agents/workflow.md` when present for the repository's feedback-loop contract, and respect ADRs in the area you're touching.

## Choose verification first

- Visual styling, layout, typography, copy, and static link corrections: edit and inspect the affected route at relevant viewport sizes; exercise a changed link. Use existing focused checks where useful. These changes need no artificial failing test or new test harness.
- State, validation, calculations, permissions, API contracts, and interaction logic: use a focused failing test at an existing public boundary. Frontend logic belongs here too.
- Mixed work: test the changed logic and visually inspect presentation. The presence of UI files alone does not select TDD.

After each vertical slice, use the smallest applicable loop from the repository contract: format changed files, run the fastest reliable static check, then run focused behavior tests. Broaden to the full suite, build, preview, or release checks only when the contract or the change's risk requires it.

Honor explicit test-first requests and repository-required checks. When meaningful automated coverage requires disproportionate new infrastructure, use the smallest reliable direct check and report the gap; escalate only for a concrete risk or required coverage.

## What a good test is

Tests verify behavior through public interfaces, not implementation details. Code can change entirely; tests shouldn't. A good test reads like a specification: "user can checkout with valid cart" tells you exactly what capability exists, and it survives refactors because it doesn't care about internal structure.

See [tests.md](tests.md) for examples and [mocking.md](mocking.md) for mocking guidelines.

## Seams: where tests go

A **seam** is the public boundary you test at: the interface where you observe behavior without reaching inside. Tests live at seams, never against internals.

Reuse the public boundary and conventions of nearby tests. Choose the seam autonomously when the request and existing interface establish the contract. Ask only when the expected behavior or interface decision is unresolved, or repository policy explicitly requires confirmation.

When the shape of that interface is itself in question (how deep the module is, where the seam belongs, what the interface should expose), call the Skill tool with "codebase-design" for the vocabulary. It is the shared source of the module, interface, depth, seam, adapter, leverage and locality terms, and it is a reference to consult, not a session to run.

## Anti-patterns

- **Implementation-coupled**: mocks internal collaborators, tests private methods, or verifies through a side channel (querying the database instead of using the interface). The tell: the test breaks when you refactor but behavior hasn't changed.
- **Tautological**: the assertion recomputes the expected value the way the code does (`expect(add(a, b)).toBe(a + b)`, a snapshot derived by hand the same way, a constant asserted equal to itself), so it passes by construction and can never disagree with the code. Expected values must come from an independent source of truth: a known-good literal, a worked example, the spec.
- **Horizontal slicing**: writing all tests first, then all implementation. Bulk tests verify _imagined_ behavior: you test the _shape_ of things rather than user-facing behavior, the tests go insensitive to real changes, and you commit to test structure before understanding the implementation. Work in **vertical slices** instead: one test → one implementation → repeat, each test a **tracer bullet** that responds to what the last cycle taught you.

## Rules of the loop

- **Red before green.** Write the failing test first, then only enough code to pass it. Don't anticipate future tests or add speculative features.
- **One slice at a time.** One seam, one test, one minimal implementation per cycle.
- **Red-capable.** Observe a new regression test fail for the intended reason before the fix. If implementation already exists, use a safe isolated comparison when proving sensitivity adds value; never disturb unrelated work. Existing passing tests remain useful evidence without deliberately breaking production code.
- **Refactor locally while green.** Keep it within the changed behavior; a small cleanup does not require a separate review workflow.
