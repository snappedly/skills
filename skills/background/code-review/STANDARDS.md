# Standards review

The Standards axis of [independent review](INDEPENDENT-REVIEW.md). Apply the repository's documented coding standards named in the brief, then the Fowler smell baseline and structural maintainability checks below. A documented repository standard overrides a heuristic.

Tool-enforced rules belong to the cleanup check record. A passing check on the exact reviewed content settles the rules it covers, so leave them out of manual findings. Report a failed, blocked, or missing check as a Validation gap rather than imitating the configured tool by hand.

## Fowler smells

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

## Structural maintainability checks

Apply these checks to each meaningful change:

- **Structural simplification**: find a concrete alternative that preserves behavior while removing branches, modes, helpers, or layers. A speculative redesign alone is not a finding.
- **Branching growth**: inspect new flags, nullable modes, and special cases in busy flows. Identify the invariant being scattered and recommend a cohesive state model or policy when it reduces complexity.
- **File growth**: compare baseline and target line counts. Review new source files over 1,000 lines and existing files that grow from 1,000 or fewer to over 1,000. Include counts and responsibilities that could be separated. Size prompts inspection, not an automatic blocker.
- **Abstraction quality**: question generic mechanisms that obscure a simple data shape and wrappers that expose details without reducing caller complexity. Keep abstractions that provide a real boundary.
- **Type and boundary clarity**: inspect casts, `any`, `unknown`, optional fields, and silent fallbacks that hide an invariant or shift validation to callers. Validated `unknown` at an external boundary and domain-required optionality are legitimate.
- **Ownership and reuse**: check whether feature logic enters a shared path, an API exposes implementation details, or a new helper duplicates a canonical utility. Cite the existing owner before recommending reuse.
- **Test evidence**: check verification against tdd's scope guidance: visual inspection for presentation edits and meaningful tests at seams for changed logic. Report material coverage gaps, insensitive regression tests, and side-channel assertions. Existing untested code is context, not a new finding.
- **Orchestration and atomicity**: trace dependencies and failure paths for serialized work and related state updates. For partial updates, name the inconsistent-state window and suggest a transaction, rollback, or recovery boundary.

## Evidence and reporting

For each finding, cite the changed file and line or hunk, quote enough of the change, explain the maintenance cost, and give an actionable remedy. For structural remedies, explain how the proposal preserves required behavior and name any caller or contract assumptions that need verification. Lead with structural regressions and substantiated simplifications, then report branching, boundary, file-growth, and legibility concerns by impact. Consolidate overlapping smells into one finding per root cause.

Report documented-standard violations separately from heuristic concerns. Label each smell and maintainability finding as a heuristic ("possible Feature Envy"); only a documented standard yields a hard violation.

Done when every named standards source, smell, and structural check has been applied to each meaningful change.
