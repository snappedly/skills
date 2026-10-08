---
name: pr
description: "Reviewability for a pull request or configured review equivalent. Use when creating, updating, or reviewing a PR's title, description, or commit history."
license: MIT
---

# PR

Prepare the code host's change request or review equivalent so a reviewer can quickly understand the intent, important files, and risk, while the code's behavior stays unchanged.

Read `docs/agents/workflow.md` and `docs/agents/code-host.md`, and `docs/agents/issue-tracker.md` for linked work items. In a repo configured before `code-host.md` existed, use any code-host operations recorded in `issue-tracker.md` until setup is refreshed. Follow the configured delivery and closure policy when creating or updating the request, including its actor, readiness, and closing-reference rules. Check existing closing references as well as new ones against ticket and parent-spec policy. When the code host and tracker differ, use links unless their integration explicitly supports automatic closure at the configured event. Resolve missing policy before adding automatic closure or performing an otherwise undecided delivery action; continue drafting and review meanwhile. Merge and ticket closure need their own authorization beyond a PR-body task; when they are in scope, follow the same policy and verify the resulting state.

## Workflow

1. Resolve the target change request from the user-provided URL or current branch. When creating one, use the intended head and base branches.
2. Inspect commits, diff size, changed paths, generated files, and the existing title and description.
3. Identify reviewability issues: noisy commits, stale description, unrelated changes, mixed mechanical and logic changes, missing tests, or unclear reviewer entry points. When the change is too large for notes to make it reviewable, recommend splitting it.
4. For a review-only request, stay read-only on the branch and the code host: assess the change request against the title, body, and history guidance below and return concrete findings and missing evidence. When correctness and maintainability review is also requested, load and apply `code-review` and report these findings with its result; without that skill, review those concerns directly at the same standard and note that it is missing.
5. When creating or updating a change request, address the issues within the requested scope through the description and review notes; a body-only request leaves the title and history as they are. Restructure commits only through History Cleanup below. Done when the description matches the current diff and the tree still matches the intended code.
6. For title creation or updates, derive and validate the title using the rules below. Publish it through the configured code host's explicit title argument or field. Read back the published title and correct any mismatch.

## Change request titles

Repository title rules, from the title policy in `docs/agents/code-host.md`, root instructions, or contribution guidance, take precedence over these defaults.

By default, use the Conventional Commits form `type(scope): description`, or `type: description` without a scope. Use lowercase types and scopes. Write a concise description of the resulting change in plain language. Add `!` before the colon for a breaking change.

| Type | Change |
| --- | --- |
| `feat` | New feature |
| `fix` | Bug fix |
| `perf` | Performance improvement |
| `refactor` | Code restructuring with unchanged behavior |
| `docs` | Documentation |
| `style` | Code formatting with unchanged behavior |
| `test` | Tests |
| `build` | Build system or dependencies |
| `ci` | CI workflows |
| `chore` | Routine maintenance |
| `revert` | Undo an earlier change |

Use a scope from the repository's documented approved list when one area dominates the change, choosing the primary affected domain regardless of file paths. Feature-specific tests and documentation keep that feature's scope. Omit the scope when several areas are affected, no approved scope fits, or no list is configured. Use approved scope names exactly. A new or revised scope needs maintainer approval, so recommend `setup-snappedly-skills` to the user when the list needs additions or revision.

Examples without configured scopes: `feat: add repository setup`, `fix: preserve invitation status`, and `chore: update dependencies`. With an approved `auth` scope: `fix(auth): preserve sign-in sessions`.

## PR Body

Read the repository's applicable PR template and contribution guidance first. Preserve its required structure and fit the intent, evidence, and merge risk into the appropriate fields. Use the template below when no repository template governs.

```markdown
## Summary

<TL;DR that matches the actual diff>

<optional diagram, diff-sketch, or tree>

## Evidence

- **Before:** <screenshot/output/failing test run>
  **After:** <screenshot/output/passing test run>

## Merge Danger

**Door:** <one-way or two-way>

<optional: description>

**Blast Radius:** <one-word description>

<optional: potential ramifications of merge>
```

Skip all preambles and keep prose brief. Read the File structure section of the installed `domain-modeling/SKILL.md` (without that skill, use the paths `docs/agents/domain.md` records, else the root `GLOSSARY-MAP.md` or `GLOSSARY.md`, or legacy `CONTEXT-MAP.md` or `CONTEXT.md`) and the selected glossary as read-only context. Use its domain language.

Separate core files from generated or mechanical files. Link issue trackers, dashboards, or design docs when they explain intent.

### Summary

Include a visual only when it explains the change more clearly than concise prose; [VISUALS.md](VISUALS.md) gives the forms and when each fits.

### Evidence

Concrete evidence that the change works, including its test coverage. Report only evidence actually observed; state when before evidence or execution results are unavailable.

Screenshots are S-tier when the environment is set up for them and the change is visual.

Execution-based evidence is A-tier: test results and console output. Name the exact test that failed before and passes now, and show what it asserts, in pseudocode when its code is too long to quote.

### Merge Danger

Name the door: one-way or two-way. Destructive actions and hard-to-reverse decisions are one-way doors. Assess reversibility of effects as well as code: reverting a commit may not restore deleted data, reverse a migration, or undo messages already sent. Use the spec and rollout context to state any recovery limits, and call out risky behavior changes, migration order, and the rollout plan.

For the blast radius, consider every surface the change can reach, such as layout shift, breakage for consumers, or mobile responsiveness.

## History Cleanup

Rewrite history or force-push only when the user asks for it or agrees to your plan. Before rewriting, inspect the change request through the configured code host, then fetch and print the original head commit and tree:

```bash
git fetch <remote> <head-branch> <base-branch>
git rev-parse <remote>/<head-branch> '<remote>/<head-branch>^{tree}'
```

Record both printed SHAs in your notes as `<original-sha>` and `<original-tree>`; later commands may run in a fresh shell, so use the recorded values rather than shell variables.

Good commit groupings usually follow dependency order:

1. Schema/storage or generated API definitions.
2. Core logic.
3. Wiring and integration.
4. UI or surface behavior.
5. Tests.

After rewriting, verify content identity by comparing the printed tree with `<original-tree>`:

```bash
git rev-parse 'HEAD^{tree}'
git diff <original-sha> HEAD --stat
```

Push only when the trees match or every difference is part of the agreed plan. Use a lease on the recorded commit so the push fails if someone else updated the branch:

```bash
git push --force-with-lease=<head-branch>:<original-sha> <remote> HEAD:<head-branch>
```

## Guardrails

- Surface every meaningful behavior change to reviewers; a commit or note labeled cleanup carries only behavior-preserving work.
- Let hooks run; bypass them only when the user explicitly asks.
