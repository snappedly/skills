---
name: codebase-cleanup
description: Hunt for slop across an existing codebase, including useless tests, unnecessary wrappers, dead code, and redundant abstractions. Use for cleanup across a repository or subsystem.
---

# Codebase cleanup

Hunt through the current repository, or the target the user names, for slop: code and tests whose maintenance cost buys no useful behavior, clarity, or protection against regressions. Remove confirmed slop while preserving runtime behavior and public contracts. An audit-only request produces findings without edits.

## Hunt

1. **Map the scope.** Read repository instructions and inspect the working tree. Inventory the authored source, tests, and supporting scripts by package or directory; exclude generated and vendored material. Use the whole repository unless the user names a narrower scope. Finish with a checklist of areas to inspect.
2. **Inspect every area.** Read implementations alongside their callers and tests, using the slop criteria below. Follow suspicious patterns across files and packages. Track each area's findings or record that no actionable slop was found. Search results guide inspection; they do not replace reading the code. This step is complete when every inventoried area has been inspected or has a concrete access blocker recorded.
3. **Resolve each candidate.** Establish what purpose it serves, what removal would change, and what evidence supports the simplification. Consult relevant domain docs, ADRs, or history when intent is unclear. Classify each candidate as a confirmed cleanup, useful code to retain, or an unresolved finding with a specific missing fact. Continue investigating while that fact is available in the repository.

## Slop criteria

- **Unnecessary wrappers and abstractions.** Look for functions that merely forward arguments, layers that rename the same operation, and generic machinery built around a single concrete use. Compare the callers before and after removal. Keep abstractions that meaningfully simplify callers, express domain intent, enforce policy, or isolate an actual dependency. A hypothetical future use alone does not justify a layer.
- **Useless tests.** Ask which plausible regression each test catches. Look for tautologies, assertions against mock setup, tests that reproduce the implementation, tests of trivial forwarding, and cases already protected by equivalent assertions through the same path. Identify any unique protection before deleting or consolidating a test. Different input values alone do not establish useful coverage; distinct edge cases, failure modes, contracts, and integration paths do. Runtime cost or flakiness alone is a separate maintenance issue.
- **Dead code.** Look for unused helpers, obsolete branches, stale fixtures, and abandoned compatibility paths. Check exports, configuration, registration, and dynamic discovery before removal. A search with no matches is a lead, not proof of disuse.
- **Redundant logic.** Look for repeated transformations, duplicated state, unnecessary conversions, impossible guards, and exception handling that only restates the runtime's behavior. Trace the actual call path and failure semantics before simplifying.

These are search directions, not a quota. Judge each candidate by the maintenance burden removed and the useful behavior or clarity retained.

## Clean up and verify

Apply confirmed cleanups in coherent batches, preserving existing user work. Update affected callers and remove artifacts made obsolete by the cleanup. Keep changes that require a product decision or a public contract change as findings with file references and the decision needed.

Run the relevant existing tests and configured static checks for changed areas, plus repository-required checks. For test removals, explain the missing value or identify the surviving coverage; a green suite alone cannot justify deleting a test. Add tests only for meaningful coverage gaps exposed by the work.

Finish when every area in the inventory is accounted for, every candidate has a disposition, and the final diff and applicable checks have been reviewed. Report the cleanups, scan coverage, unresolved findings, and verification results. Describe blocked or uninspected areas explicitly so a partial scan cannot be mistaken for a completed hunt.
