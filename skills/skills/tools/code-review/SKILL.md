---
name: code-review
description: "Review the changes since a fixed point (commit, branch, tag, or merge-base) along separate axes: Standards (documented coding standards and structural maintainability), Spec (does the code match what the originating issue/spec asked for?), and Interface (does UI code follow the web interface guidelines?) when the change touches a user interface. Runs the reviews in parallel sub-agents and reports them side by side. Use when the user wants to review a branch, a PR, work-in-progress changes, or asks to \"review since X\"."
---

Separate-axis review of a branch or work-in-progress change against a fixed point:

- **Standards**: does the code conform to this repo's documented coding standards, and does its structure remain maintainable?
- **Spec**: does the code faithfully implement the originating issue / spec?
- **Interface**, when the change touches a user interface: does the UI code follow the web interface guidelines?

Each axis runs as a **parallel sub-agent** so they don't pollute each other's context, then this skill aggregates their findings.

Run `code-cleanup` before this review and treat its final validation results as review input. Read `docs/agents/workflow.md` when present for the repository's finding-disposition policy. For a review-only request, inspect the supplied change without editing it; report missing validation evidence. After fixes, rerun cleanup for the affected scope and review substantive changes again.

## Process

### 1. Pin the comparison

Inspect `git status --short` and use the caller's scope. For an uncommitted task with no supplied base, compare against `HEAD`. For a branch or PR, use the supplied base or a base established by the task; ask only if the base is unknown.

Resolve refs to commit SHAs and capture the comparison once:

- For a committed branch review, compute `git merge-base <base-sha> <head-sha>`, then use `git diff <merge-base-sha> <head-sha>` and `git log <base-sha>..<head-sha> --oneline`.
- For work in progress, use `git diff <baseline-sha>` to include both staged and unstaged tracked changes. The baseline is `HEAD` for an uncommitted task, or the merge-base for a task spanning branch commits. Read untracked task files separately, since `git diff` omits them. Respect an explicitly staged-only request with `git diff --cached <baseline-sha>`.

Record the baseline, target, scoped paths, untracked paths, diff command, and applicable commit list. Validate refs and confirm the scoped change is non-empty, including untracked files, before dispatching reviewers. Preserve the index and keep the reviewed files unchanged while the reviewers run. If they change, refresh the comparison and repeat affected review work.

### 2. Identify the requirements sources

Look for the complete originating requirements, in this order:

1. The spec, tickets, or other requirements supplied by the user or calling implementation workflow. Preserve every supplied source rather than choosing only the top-level spec.
2. Issue references in the commit messages (`#123`, `Closes #45`, GitLab `!67`, etc.), fetched via the workflow in `docs/agents/issue-tracker.md`. If tracker configuration is needed but missing, recommend `/setup-snappedly-skills`.
3. A spec file under `docs/`, `specs/`, or `.scratch/` matching the branch name or feature.
4. If nothing is found, ask the user where the requirements are. If they confirm there are none, the **Spec** sub-agent will skip and report "no requirements available".

Completion criterion: record every supplied requirements source plus any authoritative source found through the fallback search, or record that the user explicitly confirmed there are no requirements.

### 3. Identify the standards sources

Anything in the repo that documents how code should be written, such as `CODING_STANDARDS.md` or `CONTRIBUTING.md`.

On top of whatever the repo documents, the Standards axis always carries the **smell baseline** below, a fixed set of Fowler code smells (_Refactoring_, ch.3), and the **structural maintainability checks** that follow it. Both apply even when a repo documents nothing. Three rules bind both:

- **The repo overrides.** A documented repo standard always wins; where it endorses something the baseline would flag, suppress the smell.
- **Always a judgement call.** Each smell and structural maintainability concern is a labelled heuristic ("possible Feature Envy"), never a hard violation. A documented-standard breach is a hard finding.
- **Tool results are evidence.** Do not restate a rule as a manual finding when a passing cleanup check covered the exact reviewed state. Carry failed, blocked, or missing checks into the Validation section instead of silently skipping the rule or manually imitating the configured tool.

Each smell reads *what it is* → *how to fix*; match it against the diff:

- **Mysterious Name**: a function, variable, or type whose name doesn't reveal what it does or holds. → rename it; if no honest name comes, the design's murky.
- **Duplicated Code**: the same logic shape appears in more than one hunk or file in the change. → extract the shared shape, call it from both.
- **Feature Envy**: a method that reaches into another object's data more than its own. → move the method onto the data it envies.
- **Data Clumps**: the same few fields or params keep travelling together (a type wanting to be born). → bundle them into one type, pass that.
- **Primitive Obsession**: a primitive or string standing in for a domain concept that deserves its own type. → give the concept its own small type.
- **Repeated Switches**: the same `switch`/`if`-cascade on the same type recurs across the change. → replace with polymorphism, or one map both sites share.
- **Shotgun Surgery**: one logical change forces scattered edits across many files in the diff. → gather what changes together into one module.
- **Divergent Change**: one file or module is edited for several unrelated reasons. → split so each module changes for one reason.
- **Speculative Generality**: abstraction, parameters, or hooks added for needs the spec doesn't have. → delete it; inline back until a real need shows.
- **Message Chains**: long `a.b().c().d()` navigation the caller shouldn't depend on. → hide the walk behind one method on the first object.
- **Middle Man**: a class or function that mostly just delegates onward. → cut it, call the real target direct.
- **Refused Bequest**: a subclass or implementer that ignores or overrides most of what it inherits. → drop the inheritance, use composition.

#### Structural maintainability checks

Apply these maintainability checks to each meaningful change in the Standards axis, alongside the Fowler smells. Produce review findings; carry out fixes only when the user has authorized implementation.

Inspect surrounding code, callers, and existing helpers as needed to understand the diff. Report problems introduced or materially worsened by the change. Use existing debt as context, rather than expanding the review into a whole-repository audit.

- **Structural simplification**: look for a concrete alternative that preserves required behavior while removing branches, modes, helpers, or layers. Prefer reducing the concepts a reader must understand over moving the same complexity into more files. Describe the simpler flow and what it eliminates; a speculative redesign alone is not a finding.
- **Branching growth**: inspect new flags, nullable modes, and special cases inserted into busy or unrelated flows. Trace the affected paths and identify the invariant or decision being scattered. Recommend a cohesive state model, policy, or helper when it reduces that complexity.
- **File growth**: compare line counts at the recorded baseline and review target, accounting for renames and new files. For work in progress, count the working copy or index according to the chosen scope. Review new source files over 1,000 lines and existing files growing from 1,000 lines or fewer to over 1,000. Include the before/after counts and the responsibilities that could be separated. Size prompts inspection, not an automatic blocker; weigh cohesion and documented exceptions. Generated files and mechanical data do not justify a decomposition finding by line count alone. Files already over the threshold still warrant review when the diff adds unrelated responsibilities.
- **Abstraction quality**: question generic mechanisms that obscure a simple data shape and wrappers that expose implementation details without reducing caller complexity. Extend the Middle Man and Speculative Generality checks by showing which layer can disappear or which contract can become simpler. Retain abstractions that provide a real boundary, even when their implementation is short.
- **Type and boundary clarity**: inspect casts, `any`, `unknown`, optional fields, and silent fallbacks when they hide an invariant or shift validation onto callers. Identify the contract and where it should be established. Validated `unknown` at an external boundary and optionality required by the domain are legitimate uses.
- **Ownership and reuse**: check whether feature logic enters a shared path, an API exposes implementation details, or a new helper duplicates an existing canonical utility. Cite the existing owner or helper and verify its semantics fit before recommending reuse or moving logic.
- **Test evidence**: check that behavior added or changed by the diff is covered by a test at an agreed seam. Report untested behavior, a test that cannot fail against the unfixed code, and assertions made through a side channel rather than the interface under test. Treat a test never demonstrated red as unverified, and ask for that falsification evidence; the `tdd` skill defines the seam, red-capable, and good-test vocabulary. Report these as findings and leave the remedy to the implementation workflow, because a test written against finished code ratifies whatever that code does. Existing untested code is context, not a finding.
- **Orchestration and atomicity**: trace dependencies and failure paths for serialized work and related state updates. Suggest parallel execution only when work is independent and ordering, resource limits, and side effects permit it. For partial updates, name the failure window and inconsistent state, then suggest an appropriate transaction, rollback, or recovery boundary.

#### Evidence and reporting

For each baseline finding, label it as a possible smell or maintainability concern, cite the changed file and lines, quote the relevant hunk, explain the concrete maintenance cost, and give an actionable remedy. For structural remedies, explain how the proposal preserves required behavior and name any caller or contract assumptions that need verification.

Within Standards, lead with structural regressions and substantiated simplifications, followed by branching, boundary, file-growth, and legibility concerns as their impact warrants. Consolidate overlapping smells into one finding per root cause. Keep documented violations distinct from heuristic concerns, even when they concern the same hunk. Apply the repository override and tooling-evidence rule to all these checks.

Completion criterion: enumerate the applicable standards sources and prepare the full baseline, maintainability, evidence, and tooling guidance for the Standards reviewer.

### 4. Decide whether the Interface axis applies

The **Interface** axis runs only when the scoped change touches user-facing interface. Inspect the scoped paths from step 1 for the signals:

- Component, page, route, template, or view files: `.tsx`, `.jsx`, `.vue`, `.svelte`, `.astro`, `.html`, and the project's equivalents.
- Stylesheets and style configuration: `.css`, `.scss`, a Tailwind or theme config, a design-token file.
- Whatever the repo's own layout marks as user-facing interface, per `docs/agents/frontend.md` when it exists.

A change confined to backend, infrastructure, tooling, or documentation skips this axis; record that it was skipped. When it applies, record the UI files in scope: that list is the axis's audit scope, and the axis reviews the change, not the whole surface.

Completion criterion: record either the complete UI file list for this change or the concrete reason the Interface axis does not apply.

### 5. Spawn the sub-agents in parallel

**Standards sub-agent prompt** should include:

- The recorded comparison from step 1, including untracked files to read, and the cleanup check results when available.
- The paths or fetched contents of every requirements source from step 2, including tickets, or the explicit statement that no requirements are available. The Standards reviewer needs the requirements to assess speculative generality and behavior-preserving simplifications, but it still reviews only the Standards axis.
- The list of standards-source files you found in step 3, **plus the smell baseline, structural maintainability checks, and evidence and reporting guidance from step 3** pasted in full (the sub-agent has no other access to it).
- The brief: "Report every substantiated finding, per file or hunk where relevant: (a) each place the diff violates a documented standard, citing the standard file and rule; and (b) each baseline smell or structural maintainability concern, naming it and quoting the hunk. Distinguish hard violations from judgement calls. A documented repo standard overrides the baseline. Follow the supplied evidence, reporting, and tooling guidance. When no requirements exist, omit Speculative Generality and other conclusions that require knowing the requested scope. Keep each finding concise."

**Spec sub-agent prompt** should include:

- The same recorded comparison from step 1, including untracked files to read.
- The paths or fetched contents of every requirements source from step 2, including tickets.
- The brief: "Report every substantiated instance of: (a) a requirement that is missing or partial; (b) behavior the requirements did not ask for; and (c) a requirement that looks implemented incorrectly. Quote the relevant requirements source for each finding and keep each finding concise."

**Interface sub-agent prompt** should include:

- The recorded comparison from step 1, the UI file list from step 4, and every requirements source from step 2 when available.
- The brief: "Call the Skill tool with 'frontend-guidelines' to load the rules, then audit these UI files against every rule in them. Report in the terse `file:line` format that skill specifies, grouped by file, with `✓ pass` for a clean file. Report what this change introduced or worsened; leave pre-existing issues in lines the change didn't touch. Read enough surrounding code to tell a real violation from a rule already satisfied by a wrapper, a shared class, or a token. Use the requirements to distinguish intentional behavior without leaving the Interface axis. Name the guidelines pin date."

If no requirements source exists, skip the Spec sub-agent and note this in the final report. If step 4 found no UI in scope, skip the Interface sub-agent and note that too. If an applicable reviewer fails, report the missing axis and ask the user whether to retry or continue with a partial review. A partial review is not ready for commit or handoff unless the user explicitly waives the missing axis under repository policy. Do not claim the review is complete while an applicable axis is missing.

Completion criterion: every applicable reviewer returned a report, has a recorded skip reason, or is explicitly recorded as missing after the user chose to continue with a partial review.

### 6. Aggregate

Start with `## Validation`, summarizing the cleanup checks and their coverage of the reviewed state. For a review-only request without cleanup evidence, say which evidence is missing.

Present each report under its own `## Standards`, `## Spec`, and `## Interface` heading, verbatim or lightly cleaned. Omit the heading for a skipped axis and say why it was skipped. Do **not** merge or rerank findings, because the axes are deliberately separate (see _Why separate axes_). On a follow-up review, record each earlier finding as fixed, resolved by an explicit user change to its source, accepted or deferred under repository policy, waived under repository policy, or still open.

End with a one-line summary containing the total findings per axis and the worst issue _within each axis_, if any. State whether every applicable axis ran; if one did not, name the missing review and do not describe the review as complete. Do not pick a single winner across axes.

Completion criterion: the report accounts for validation and every axis, preserves the axes' separate conclusions, and states whether the review itself completed.

## Why separate axes

A change can pass one axis and fail another:

- Code that follows every standard but implements the wrong thing → **Standards pass, Spec fail.**
- Code that does exactly what the issue asked but breaks the project's conventions → **Spec pass, Standards fail.**
- A feature that is well built and exactly as specified, whose buttons are unreachable by keyboard → **Standards and Spec pass, Interface fail.**

Reporting them separately stops one axis from masking another. Interface is the axis most easily masked: an accessibility or theming defect is invisible to a reviewer reading for structure or requirements, and a passing Standards axis reads as an all-clear it never gave.
