---
name: code-review
description: "Review the changes since a fixed point (commit, branch, tag, or merge-base) along separate axes: Standards (documented coding standards and structural maintainability), Spec (does the code match what the originating issue/spec asked for?), and Interface (does the UI code follow the web interface guidelines?) when the change touches a user interface. Runs the reviews in parallel sub-agents and reports them side by side. Use when the user wants to review a branch, a PR, work-in-progress changes, or asks to \"review since X\"."
---

Separate-axis review of a committed branch change against one immutable target SHA. A working-tree revision is not a SHA and cannot be reviewed or handed off as one.

- **Standards**: does the code conform to this repo's documented coding standards, and does its structure remain maintainable?
- **Spec**: does the code faithfully implement the originating issue or spec?
- **Interface**, when the change touches a user-facing interface: does the UI code follow the web interface guidelines?

Each applicable axis runs as an independent read-only sub-agent. Axes may run in parallel with one another, never with mutation of the target branch. The coordinator aggregates their results before any fix work starts.

Run `code-cleanup` before this review and treat its committed, SHA-keyed validation evidence as input. `code-review` owns the review comparison and findings, not cleanup or fixes. A caller such as `implement-spec` owns phase transitions and schedules cleanup. Standalone review reports missing cleanup evidence instead of recursively invoking it.

## Review barrier and convergence bound

The review target is a record, not a moving branch:

```text
baseSha + targetSha + scopedPaths + requirements + cleanupEvidence
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

Before dispatch, resolve and capture the exact committed `baseSha` and `targetSha`, comparison command, changed paths, untracked paths discovered before the final commit, requirements sources, applicable axes, and cleanup evidence. Every in-scope path discovered as staged, unstaged, or untracked must be committed or explicitly excluded before dispatch. Pass `targetSha` and the same path scope to every reviewer. Each result must repeat `targetSha`, the reviewed paths, status, findings, `inputFingerprint`, and evidence timestamp.

Once the first axis starts, the target branch is immutable. Do not edit, stage, merge, rebase, or run cleanup against it until every active axis has returned or has been explicitly cancelled. If the target SHA changes, reject only results for the old SHA, record the expected and observed SHAs and the reason, cancel obsolete axes promptly, and do not silently launch a complete new review cycle. After the branch is intentionally advanced, freeze the new SHA and reuse unaffected evidence whose fingerprints match, or rerun only the affected axis or file scope.

Aggregate all applicable axes before assigning fixes. Allow one normal fix batch and one follow-up review. The follow-up must list the changed files and explain why each included axis is affected. Do not relaunch unaffected axes. Any new finding after the follow-up, whether hard or heuristic and regardless of axis, a missing required axis, or an exhausted orchestration budget stops automatic convergence and requires coordinator or user triage under repository policy.

### Immutable evidence and reuse

The review target is a committed SHA resolved with `git rev-parse --verify <ref>^{commit}`. Do not label a working-tree revision as `targetSha`. Cleanup may produce preliminary working-tree results, but `code-review` accepts only final evidence whose `outputSha` is a committed target, with all in-scope content committed or explicitly excluded.

For each check, `inputFingerprint` is a SHA-256 of a canonical manifest containing the checked path list and content hashes, dependency manifests and resolved tool versions, configuration files and content hashes, exact command, working directory, and scope selector. Cleanup evidence may be reused on a later committed target when the current target's fingerprint exactly matches the earlier result. The evidence must name both `validatedSha`, the original committed SHA inspected, and `currentTargetSha`, the committed target receiving the reused result, plus `reusedFromSha` and the matching fingerprint. A changed target SHA alone does not require a new check. Run a new target check when any checked content, dependency, configuration input, command, working directory, scope, or evidence identity changes, or when earlier evidence came from a mutable working tree.

## Process

### 1. Pin the comparison

Inspect `git status --short` and use the caller's supplied scope. For an uncommitted task with no supplied base, use `HEAD` only as the baseline for scope discovery. Commit the task before dispatch and resolve the resulting commit as `targetSha`. For a branch or pull/merge request, resolve the supplied base and head, compute their merge-base, and capture the resulting `baseSha` and `targetSha` once. Use the recorded SHA in every command and prompt. Read untracked task files separately because ordinary `git diff` omits them. Confirm that the scoped change is non-empty before dispatching reviewers.

Preserve the index and keep reviewed files unchanged while axes run. If they change, stop the affected review, refresh the comparison only after the old set is complete or cancelled, and follow the stale-result rule above.

### 2. Identify requirements sources

Look for complete requirements in this order:

1. The spec, tickets, or other requirements supplied by the caller. Preserve every source.
2. Issue references in commit messages (`#123`, `Closes #45`, GitLab `!67`, and similar), fetched through the workflow in `docs/agents/issue-tracker.md` when configured.
3. A matching spec file under `docs/`, `specs/`, or `.scratch/`.
4. If none exists, ask where the requirements are. If the caller confirms there are none, record that the Spec axis is skipped for lack of requirements.

If tracker configuration is missing, recommend `/setup-snappedly-skills`. Do not pretend that an unverified tracker or workflow policy supplied the missing requirements.

### 3. Identify standards sources

Find repository documents that describe coding standards, then apply the fixed Fowler smell baseline and structural maintainability checks below. A documented repository standard overrides a heuristic. Smell and maintainability findings are judgement calls, never hard violations. Passing cleanup evidence for the exact checked input fingerprint is evidence and should not be restated as a manual tool finding. A review fix is not allowed to mutate the frozen target while any axis is running.

On top of repository standards, the Standards axis applies this fixed Fowler smell baseline from _Refactoring_: Mysterious Name, Duplicated Code, Feature Envy, Data Clumps, Primitive Obsession, Repeated Switches, Shotgun Surgery, Divergent Change, Speculative Generality, Message Chains, Middle Man, and Refused Bequest. Each smell is a heuristic, never a hard violation. A documented repository standard overrides a heuristic. Passing cleanup evidence for the exact checked input is evidence, not a second manual finding.

Use these definitions and remedies:

- **Mysterious Name**: a function, variable, or type name does not reveal what it does or holds. Rename it, or simplify the design if no honest name exists.
- **Duplicated Code**: the same logic shape appears in more than one hunk or file. Extract the shared behavior and call it from both sites.
- **Feature Envy**: a method reaches into another object's data more than its own. Move the method to the data it uses.
- **Data Clumps**: the same small group of fields or parameters travels together. Bundle them in a type and pass that type.
- **Primitive Obsession**: a primitive or string stands in for a domain concept that needs its own type. Introduce the smallest type that states the contract.
- **Repeated Switches**: the same conditional cascade on one type recurs across the change. Use one shared map or a polymorphic owner.
- **Shotgun Surgery**: one logical change forces scattered edits across many files. Gather the behavior in one owner.
- **Divergent Change**: one file or module changes for several unrelated reasons. Split the responsibilities.
- **Speculative Generality**: an abstraction, parameter, or hook serves needs outside the request. Delete it or inline it until a real need appears.
- **Message Chains**: a caller depends on a long navigation chain such as `a.b().c().d()`. Hide the walk behind a method on the first object.
- **Middle Man**: a class or function mostly delegates to another object. Remove it and call the real owner directly.
- **Refused Bequest**: a subclass or implementer ignores most of what it inherits. Drop the inheritance or use composition.

#### Structural maintainability checks

Apply these structural checks to each meaningful change in the Standards axis:

- **Structural simplification**: find a concrete alternative that preserves behavior while removing branches, modes, helpers, or layers. A speculative redesign alone is not a finding.
- **Branching growth**: inspect new flags, nullable modes, and special cases in busy flows. Identify the invariant being scattered and recommend a cohesive state model or policy when it reduces complexity.
- **File growth**: compare baseline and target line counts. Review new source files over 1,000 lines and existing files that grow from 1,000 or fewer to over 1,000. Include counts and responsibilities that could be separated. Size prompts inspection, not an automatic blocker.
- **Abstraction quality**: question generic mechanisms that obscure a simple data shape and wrappers that expose details without reducing caller complexity. Keep abstractions that provide a real boundary.
- **Type and boundary clarity**: inspect casts, `any`, `unknown`, optional fields, and silent fallbacks that hide an invariant or shift validation to callers. Validated `unknown` at an external boundary and domain-required optionality are legitimate.
- **Ownership and reuse**: check whether feature logic enters a shared path, an API exposes implementation details, or a new helper duplicates a canonical utility. Cite the existing owner before recommending reuse.
- **Test evidence**: check that changed behavior has a test at an agreed seam. Report untested behavior, tests that cannot fail against unfixed code, and side-channel assertions. Existing untested code is context, not a new finding.
- **Orchestration and atomicity**: trace dependencies and failure paths for serialized work and related state updates. For partial updates, name the inconsistent-state window and suggest a transaction, rollback, or recovery boundary.

#### Evidence and reporting

For each finding, cite the changed file and line or hunk, quote enough of the change, explain the maintenance cost, and give an actionable remedy. For structural remedies, explain how the proposal preserves required behavior and name any caller or contract assumptions that need verification. Lead with structural regressions and substantiated simplifications, then report branching, boundary, file-growth, and legibility concerns by impact. Consolidate overlapping smells into one finding per root cause. Keep documented violations distinct from heuristic concerns. Report only problems introduced or materially worsened by the scoped change.

The Standards axis is complete only when it has enumerated applicable standards sources and prepared the full smell baseline, maintainability checks, evidence guidance, and tooling guidance for the reviewer.

### 4. Decide whether Interface applies

Run Interface only when the scoped change includes user-facing component, page, route, template, view, stylesheet, style configuration, or paths marked as interface by `docs/agents/frontend.md`. Record the complete UI file list. A tooling, infrastructure, backend, or documentation change skips Interface with that concrete reason. When it applies, the Interface axis reviews those files only, not the whole product.

### 5. Run the applicable axes

Dispatch Standards, Spec, and Interface prompts in parallel only after the barrier is recorded. Prompts include the fixed comparison, target SHA, scoped paths, requirements, cleanup evidence, and the relevant axis rules. Every reviewer must return a report or an explicit skip reason.

**Standards sub-agent prompt** includes:

- the recorded comparison, including untracked paths discovered before the final commit, and cleanup results;
- every requirements source, or the explicit statement that none is available;
- the repository standards sources, complete Fowler baseline, structural checks, and evidence guidance above; and
- the brief to report documented violations separately from heuristic smells, cite each finding by file and line or hunk, quote the relevant change, explain the maintenance cost, and give an actionable remedy.

**Spec sub-agent prompt** includes every supplied requirements source and the brief to report each missing or partial requirement, unrequested behavior, or incorrect implementation, with a quotation from the source for each finding.

**Interface sub-agent prompt** includes the recorded comparison, complete UI file list, requirements, and the brief to call the Skill tool with `frontend-guidelines`, audit every applicable rule, and report in the skill's terse `file:line` format grouped by file. It must use `✓ pass` for a clean file, identify what the change introduced or worsened, leave untouched pre-existing issues out, and name the guidelines pin date.

If no requirements source exists, skip the Spec sub-agent and record that reason. If no UI file is in scope, skip the Interface sub-agent and record that reason. If an agent fails, record the missing axis and stop before handoff unless repository policy contains an explicit waiver. Never describe a partial review as complete. Cancel an obsolete agent as soon as its target SHA is stale.

### 6. Aggregate and hand off

Start with `## Validation`, naming the cleanup evidence, committed target SHA, scope, input fingerprint, and any stale or blocked checks. Present each applicable axis under its own heading, preserving separate conclusions. On a follow-up, record each earlier finding as fixed, resolved by an explicit source change, accepted/deferred, waived under policy, or still open. Record every new finding, even a heuristic one, as new.

End with one line containing finding counts and the worst issue within each axis, and state whether every applicable axis ran. Include the review budget status and the reason for any follow-up scope. The caller may begin one coordinated fix batch only after this aggregate is complete. After the fix, review only affected axes/files once. Stop for any new finding after that follow-up and escalate under the convergence bound.

## Why separate axes

A change can pass one axis and fail another. Separate reports keep a standards concern, a spec gap, and an interface defect from masking one another. The shared immutable target and aggregate barrier preserve that independence without permitting stale findings or unbounded review loops.
