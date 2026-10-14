---
name: codebase-cleanup
description: Hunt for slop across an existing codebase or subsystem, such as dead code, useless tests, and unnecessary wrappers and abstractions.
license: MIT
---

# Codebase cleanup

Hunt through the current repository, or the target the user names, for slop: code and tests whose maintenance cost buys no useful behavior, clarity, or protection against regressions. Remove confirmed slop while preserving runtime behavior and public contracts. An audit-only request produces findings without edits.

## Hunt

1. **Map the scope.** Read repository instructions and inspect the working tree. Inventory the authored source, tests, and supporting scripts by package or directory; exclude generated and vendored material. Finish with a checklist of areas to inspect.
2. **Inspect every area.** Read implementations alongside their callers and tests, using the slop criteria below. Follow suspicious patterns across files and packages. Track each area's findings or record that no actionable slop was found. Search results guide inspection; they do not replace reading the code. This step is complete when every inventoried area has been inspected or has a concrete access blocker recorded.
3. **Resolve each candidate.** Establish what purpose it serves, what removal would change, and what evidence supports the simplification. Consult relevant domain docs, ADRs, or history when intent is unclear. Classify each candidate as a confirmed cleanup, useful code to retain, or an unresolved finding with a specific missing fact. Continue investigating while that fact is available in the repository.

## Slop criteria

- **Unnecessary wrappers and abstractions.** Look for functions that merely forward arguments, layers that rename the same operation, and generic machinery built around a single concrete use. Compare the callers before and after removal. Keep abstractions that meaningfully simplify callers, express domain intent, enforce policy, or isolate an actual dependency. A hypothetical future use alone does not justify a layer.
- **Useless or stale tests.** Ask which plausible regression each test catches. Look for tests for removed features or superseded behavior, tautologies, assertions against mock setup, tests that reproduce the implementation, tests of trivial forwarding, and cases already protected by equivalent assertions through the same path. Identify any unique protection before deleting or consolidating a test. Different input values alone do not establish useful coverage; distinct edge cases, failure modes, contracts, and integration paths do. Runtime cost or flakiness alone is a separate maintenance issue.
- **Dead code.** Look for unused helpers, obsolete branches, stale fixtures, and abandoned compatibility paths. Check exports, configuration, registration, and dynamic discovery before removal. A search with no matches is a lead, not proof of disuse.
- **Redundant logic.** Look for repeated transformations, duplicated state, unnecessary conversions, impossible guards, and exception handling that only restates the runtime's behavior. Trace the actual call path and failure semantics before simplifying.

These are search directions, not a quota. Judge each candidate by the maintenance burden removed and the useful behavior or clarity retained.

## Clean up and verify

Apply confirmed cleanups in coherent batches, preserving existing user work. Update affected callers and remove artifacts made obsolete by the cleanup. Keep changes that require a product decision or a public contract change as findings with file references and the decision needed.

Run the relevant existing tests and configured static checks for changed areas, plus repository-required checks. For test removals, explain the missing value or identify the surviving coverage; a green suite alone cannot justify deleting a test. Add tests only for meaningful coverage gaps exposed by the work.

After making cleanup changes and completing verification, load and apply `code-review` through the available skill invocation mechanism or its installed `SKILL.md`; if it is not installed, review the diff yourself for correctness, behavior preservation, and maintainability at the same standard, and say so. Scope the review to the cleanup changes, including uncommitted and untracked task files. Supply the cleanup request, behavior-preservation requirements, and verification evidence. Resolve actionable review findings, rerun affected checks, and review only the fix delta after corrections.

Finish when every area in the inventory is accounted for, every candidate has a disposition, and applicable checks and any required code review are complete.

## Report

1. **Summarize the hunt.** Report the cleanups, scan coverage, verification results, and review outcome.
2. **List open items.** Decisions are the changes kept as findings because they need a product decision or a public contract change. Gaps are everything left unverified: each unresolved finding with its missing fact, each check that failed or did not run, each missing review axis, and each blocked or uninspected area, so a partial scan cannot be mistaken for a completed hunt.

   <!-- shared: open-items -->
   End the report with a horizontal rule and a **Check before you submit or deploy** heading, followed by two numbered lists: **Decisions needed** and **Gaps to check**. Write each item in plain language that someone who has not read the rest of the report can act on, and end it with your recommendation and the reason for it.

   - For a decision, say what is at stake and where, and list the options under it.
   - For a gap, say what was not verified and where, why, and the risk. When there is more than one way to close it, such as rerunning a check, verifying by hand, or accepting the risk, list the options under it.

   Write "None" under an empty list's heading.
   <!-- /shared: open-items -->

   Done when the report ends with both lists, and every decision and gap appears in one of them.
