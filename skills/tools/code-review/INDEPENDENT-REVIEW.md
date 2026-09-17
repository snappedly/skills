# Independent review

Use this process only when selected by `SKILL.md`. Reviewers stay read-only; the caller owns fixes and convergence.

## Pin and freeze

Resolve base and target once. For a committed branch, use the fixed merge-base and target SHAs in diff commands and reviewer briefs. Include all supplied requirements and task paths.

For standalone work-in-progress review, preserve the index and capture an immutable snapshot of the requested staged/unstaged/untracked content (patch plus new-file contents or an isolated Git snapshot). Record HEAD and the snapshot identity. Do not commit the user's branch merely to review it. Integrated implement-spec reviews use a committed target.

All reviewers inspect the same target. The coordinator must keep its target branch and reviewed content unchanged until all active axes return or cancellation is confirmed. Unexpected changes invalidate affected results: record old/new targets and why, cancel obsolete agents, then reassess only affected axes. Unchanged axis results may be carried forward with an explicit comparison of their files, context, requirements, and standards.

Validation evidence follows code-cleanup's reuse rules. Committing identical checked content requires no new validation. Reviews assess correctness and requirements; they do not rerun the supplied checks.

## Requirements and applicability

Use every spec and ticket supplied by the caller. Fetch missing sources once and pass local pointers to reviewers. Otherwise inspect issue references and matching spec files, then ask only if the requirements cannot be established. Skip Spec only with an explicit no-requirements disposition.

Interface applies to changed user-facing components, routes, templates, styles, design configuration, or UI paths documented by the repository. Record the UI scope. A change confined to tooling or prose skips Interface. Standards remains independent from Spec.

## Standards reference

Find repository documents that describe coding standards, then apply the fixed Fowler smell baseline and structural maintainability checks below. A documented repository standard overrides a heuristic. Smell and maintainability findings are judgement calls, never hard violations. Passing cleanup evidence for the exact checked inputs is evidence and should not be restated as a manual tool finding. A review fix is not allowed to mutate the frozen target while any axis is running.

Use these Fowler smell definitions and remedies from _Refactoring_:

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

### Structural maintainability checks

Apply these structural checks to each meaningful change in the Standards axis:

- **Structural simplification**: find a concrete alternative that preserves behavior while removing branches, modes, helpers, or layers. A speculative redesign alone is not a finding.
- **Branching growth**: inspect new flags, nullable modes, and special cases in busy flows. Identify the invariant being scattered and recommend a cohesive state model or policy when it reduces complexity.
- **File growth**: compare baseline and target line counts. Review new source files over 1,000 lines and existing files that grow from 1,000 or fewer to over 1,000. Include counts and responsibilities that could be separated. Size prompts inspection, not an automatic blocker.
- **Abstraction quality**: question generic mechanisms that obscure a simple data shape and wrappers that expose details without reducing caller complexity. Keep abstractions that provide a real boundary.
- **Type and boundary clarity**: inspect casts, `any`, `unknown`, optional fields, and silent fallbacks that hide an invariant or shift validation to callers. Validated `unknown` at an external boundary and domain-required optionality are legitimate.
- **Ownership and reuse**: check whether feature logic enters a shared path, an API exposes implementation details, or a new helper duplicates a canonical utility. Cite the existing owner before recommending reuse.
- **Test evidence**: check verification against tdd's scope guidance: visual inspection for presentation edits and meaningful tests at public boundaries for changed logic. Report material coverage gaps, insensitive regression tests, and side-channel assertions. Existing untested code is context, not a new finding.
- **Orchestration and atomicity**: trace dependencies and failure paths for serialized work and related state updates. For partial updates, name the inconsistent-state window and suggest a transaction, rollback, or recovery boundary.

### Evidence and reporting

For each finding, cite the changed file and line or hunk, quote enough of the change, explain the maintenance cost, and give an actionable remedy. For structural remedies, explain how the proposal preserves required behavior and name any caller or contract assumptions that need verification. Lead with structural regressions and substantiated simplifications, then report branching, boundary, file-growth, and legibility concerns by impact. Consolidate overlapping smells into one finding per root cause. Keep documented violations distinct from heuristic concerns. Report only problems introduced or materially worsened by the scoped change.

Carry failed, blocked, or missing tool checks into Validation. Preserve the repository's finding-disposition rules; no axis may treat an unverified check as passed.

The Standards axis is complete only when it has enumerated applicable standards sources and prepared the full smell baseline, maintainability checks, evidence guidance, and tooling guidance for the reviewer.

## Dispatch once

Launch one agent per applicable axis in parallel. Keep briefs scoped; pass the fixed target, comparison, paths, cleanup results, requirements pointers, and the relevant instructions below. Reviewers read these instructions from their provided path rather than receiving the whole conversation.

- Standards reads the full baseline and structural guidance above, plus repository standards. Report documented violations separately from heuristic concerns.
- Spec checks every supplied requirement for missing, partial, incorrect, or unrequested behavior. Cite the requirement for each finding.
- Interface reads the `frontend-guidelines` pinned rules, audits the UI scope against applicable rules, and returns its `file:line` report, clean-file passes, and guidelines pin date.

Review surrounding context as needed; report issues introduced or worsened by the change. Each result names its exact target, scope, findings, and coverage gaps. Use completion notifications and close completed agents. If an axis fails, report it as missing and let the coordinator decide on a budgeted retry or policy-authorized waiver.

Set a completion deadline before dispatch (default five minutes per axis). On expiry, inspect progress once and cancel stalled work; preserve useful partial findings. Finish locally when independent review is optional. When independence is required, report the missing coverage and follow repository policy. Retry only for a concrete recoverable cause within the budget, with at most one replacement; use completion notifications instead of repeated status polling.

## Aggregate and follow up

Wait for every applicable axis before fixes. Return Validation, Standards, Spec, and applicable Interface results separately, with counts, skip reasons, and finding dispositions. Preserve each axis's conclusions; do not hide one behind another.

For an authorized follow-up, review only the fix delta and affected context through affected axes. Reuse existing reviewers where possible and explain each inclusion or skip. A CSS-only correction need not relaunch Spec unless it affects a requirement; a test-only correction need not launch Interface.

Record earlier findings as fixed, still open, or explicitly resolved/accepted/deferred/waived under repository policy. Any new or remaining finding after the bounded follow-up returns to coordinator triage. This skill launches no further fix or review cycle on its own.
