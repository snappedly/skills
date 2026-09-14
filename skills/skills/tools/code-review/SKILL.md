---
name: code-review
description: "Review the changes since a fixed point (commit, branch, tag, or merge-base) along separate axes: Standards (documented coding standards and structural maintainability), Spec (does the code match what the originating issue/spec asked for?), and Interface (does the UI code follow the web interface guidelines?) when the change touches a user interface. Runs the reviews in parallel sub-agents and reports them side by side. Use when the user wants to review a branch, a PR, work-in-progress changes, or asks to \"review since X\"."
---

Separate-axis review of a branch or work-in-progress change against one immutable target SHA.

- **Standards**: does the code conform to this repo's documented coding standards, and does its structure remain maintainable?
- **Spec**: does the code faithfully implement the originating issue or spec?
- **Interface**, when the change touches a user-facing interface: does the UI code follow the web interface guidelines?

Each applicable axis runs as an independent read-only sub-agent. Axes may run in parallel with one another, never with mutation of the target branch. The coordinator aggregates their results before any fix work starts.

Run `code-cleanup` before this review and treat its SHA-keyed validation evidence as input. `code-review` owns the review comparison and findings, not cleanup or fixes. A caller such as `implement-spec` owns phase transitions and schedules cleanup. Standalone review reports missing cleanup evidence instead of recursively invoking it.

## Review barrier and convergence bound

The review target is a record, not a moving branch:

```text
baseSha + targetSha + scopedPaths + untrackedPaths + requirements + cleanupEvidence
        |
        v
 freeze target -> run all applicable axes in parallel -> wait for every axis
        |                                                   |
        +------------ no mutation, merge, staging, or fix --+
                                                            v
                                                     aggregate findings
                                                            |
                                         one coordinated fix batch, if needed
                                                            v
                                              affected cleanup checks only
                                                            v
                                  freeze new SHA and follow up once on affected axes
```

Before dispatch, capture the exact `baseSha`, `targetSha`, comparison command, changed and untracked paths, requirements sources, applicable axes, and cleanup evidence. Pass `targetSha` and the same path scope to every reviewer. Each result must repeat `targetSha`, the reviewed paths, status, findings, and evidence timestamp.

Once the first axis starts, the target branch is immutable. Do not edit, stage, merge, rebase, or run cleanup against it until every active axis has returned or has been explicitly cancelled. If the target SHA changes, reject only results for the old SHA, record the expected and observed SHAs and the reason, cancel obsolete axes promptly, and do not silently launch a complete new review cycle. After the branch is intentionally advanced, freeze the new SHA and rerun only the affected axis or file scope.

Aggregate all applicable axes before assigning fixes. Allow one normal fix batch and one follow-up review. The follow-up must list the changed files and explain why each included axis is affected. Do not relaunch unaffected axes. A new hard finding after the follow-up, a missing required axis, or an exhausted orchestration budget stops automatic convergence and requires coordinator or user triage under repository policy.

## Process

### 1. Pin the comparison

Inspect `git status --short` and use the caller's supplied scope. For an uncommitted task with no supplied base, compare against `HEAD`. For a branch or pull/merge request, resolve the supplied base and head, compute their merge-base, and capture the resulting `baseSha` and `targetSha` once. Use the recorded SHA in every command and prompt. Read untracked task files separately because ordinary `git diff` omits them. Confirm that the scoped change is non-empty before dispatching reviewers.

Preserve the index and keep reviewed files unchanged while axes run. If they change, stop the affected review, refresh the comparison only after the old set is complete or cancelled, and follow the stale-result rule above.

### 2. Identify requirements sources

Look for complete requirements in this order:

1. The spec, tickets, or other requirements supplied by the caller. Preserve every source.
2. Issue references in commit messages (`#123`, `Closes #45`, GitLab `!67`, and similar), fetched through the workflow in `docs/agents/issue-tracker.md` when configured.
3. A matching spec file under `docs/`, `specs/`, or `.scratch/`.
4. If none exists, ask where the requirements are. If the caller confirms there are none, record that the Spec axis is skipped for lack of requirements.

If tracker configuration is missing, recommend `/setup-snappedly-skills`. Do not pretend that an unverified tracker or workflow policy supplied the missing requirements.

### 3. Identify standards sources

Find repository documents that describe coding standards, then apply the fixed Fowler smell baseline and structural maintainability checks below. A documented repository standard overrides a heuristic. Smell and maintainability findings are judgement calls, never hard violations. Passing cleanup evidence for the exact target is evidence and should not be restated as a manual tool finding.

The baseline includes Mysterious Name, Duplicated Code, Feature Envy, Data Clumps, Primitive Obsession, Repeated Switches, Shotgun Surgery, Divergent Change, Speculative Generality, Message Chains, Middle Man, and Refused Bequest. Also inspect structural simplification, branching growth, file growth, abstraction quality, type and boundary clarity, ownership and reuse, test evidence, and orchestration/atomicity. Report only problems introduced or materially worsened by the scoped change.

For every finding, distinguish documented violations from heuristics, cite the changed file and line or hunk, quote enough of the relevant change, explain the maintenance cost, and give an actionable remedy. A review fix is not allowed to mutate the frozen target while any axis is running.

### 4. Decide whether Interface applies

Run Interface only when the scoped change includes user-facing component, page, route, template, view, stylesheet, style configuration, or paths marked as interface by `docs/agents/frontend.md`. Record the complete UI file list. A tooling, infrastructure, backend, or documentation-only change skips Interface with that concrete reason.

### 5. Run the applicable axes

Dispatch Standards, Spec, and Interface prompts in parallel only after the barrier is recorded. Prompts include the fixed comparison, target SHA, scoped paths, requirements, cleanup evidence, and the relevant axis rules. Every reviewer must return a report or an explicit skip reason.

If an agent fails, record the missing axis and stop before handoff unless repository policy contains an explicit waiver. Never describe a partial review as complete. Cancel an obsolete agent as soon as its target SHA is stale.

### 6. Aggregate and hand off

Start with `## Validation`, naming the cleanup evidence, target SHA, scope, and any stale or blocked checks. Present each applicable axis under its own heading, preserving separate conclusions. On a follow-up, record each earlier finding as fixed, resolved by an explicit source change, accepted/deferred, waived under policy, or still open.

End with one line containing finding counts and the worst issue within each axis, and state whether every applicable axis ran. Include the review budget status and the reason for any follow-up scope. The caller may begin one coordinated fix batch only after this aggregate is complete. After the fix, review only affected axes/files once, then stop or escalate under the convergence bound.

## Why separate axes

A change can pass one axis and fail another. Separate reports keep a standards concern, a spec gap, and an interface defect from masking one another. The shared immutable target and aggregate barrier preserve that independence without permitting stale findings or unbounded review loops.
