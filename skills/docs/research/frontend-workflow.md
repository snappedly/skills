# Frontend workflow research

Date: 2026-09-11

## Question and scope

How do mature teams connect visual design direction, accessibility and interface-guideline review, prototyping, implementation, and CI or review gates?

This note uses first-party sources only: W3C and WAI standards and guidance, Storybook documentation, the Vercel Web Interface Guidelines repository, and the GOV.UK Service Manual. The sources describe different layers of the work. WCAG defines testable accessibility requirements, WCAG-EM describes an evaluation process, Storybook documents component-level checks, Vercel provides a code-review checklist, and GOV.UK describes product discovery and service-level review. The workflow below is a synthesis, not a claim that any one source prescribes the whole system.

## The workflow these sources support

The handoff between stages should be explicit. Each stage produces an artifact that the next stage can inspect.

| Stage | Handoff artifact | Review question |
| --- | --- | --- |
| Design direction | A brief with the audience, user job, visual point of view, tokens, content rules, and accessibility constraints | Is the direction specific to the product, and can the intended experience work without color, hover, or motion as its only signal? |
| Prototype | A clearly marked, runnable prototype with a question, competing variants or states, and a recorded verdict | Which risky design or interaction decision should production code carry forward? |
| Implementation | Production components plus stories or equivalent fixtures for important states and user paths | Does each state render, behave, and expose the expected semantics? |
| Pull request | Automated render, interaction, accessibility, and visual checks plus a human interface-guideline review | Are new failures absent, and are visual changes intentional and explained? |
| Release or major milestone | A representative accessibility evaluation, manual and assistive-technology evidence, and a cross-functional review | Is the whole in-scope experience ready, rather than only the happy-path screenshot? |

This staged model follows WAI's direction to evaluate accessibility early and throughout development, Storybook's use of stories as test cases, and GOV.UK's separation of prototypes, production code, regular testing, and formal assessment. It is an implementation recommendation, not a new standard. ([WAI evaluation overview](https://www.w3.org/WAI/test-evaluate/), [Storybook UI testing](https://storybook.js.org/docs/writing-tests), [GOV.UK prototypes](https://www.gov.uk/service-manual/design/making-prototypes), [GOV.UK accessibility testing](https://www.gov.uk/service-manual/helping-people-to-use-your-service/testing-for-accessibility))

## What the primary sources actually say

### W3C and WAI: accessibility is a development activity, not a final scan

The [WAI evaluation overview](https://www.w3.org/WAI/test-evaluate/) says to evaluate accessibility early and throughout development because early problems are easier to fix. It also says that no single tool can determine whether a site meets accessibility standards and that knowledgeable human evaluation is required. The same page points teams toward tool-assisted checks, conformance reports, combined expertise, and involving people with disabilities.

The [WCAG Evaluation Methodology 2.0](https://www.w3.org/TR/WCAG-EM/) provides a repeatable evaluation process. Its five steps are to define scope, explore the product, select a representative sample, evaluate that sample, and report findings. It says the methodology does not replace quality assurance throughout development. It also says the scope should include all views, states, and functionality of the target product. Sampling is useful for large products, but a sampled evaluation alone does not support a WCAG conformance claim for an entire website. The methodology strongly recommends involving real people with a wide range of abilities, while noting that tools assist rather than replace human evaluation.

The [WCAG 2.2 Recommendation](https://www.w3.org/TR/WCAG22/) defines success criteria as testable, technology-neutral statements. That makes WCAG a useful source for acceptance criteria, but not a visual style guide or a complete test plan.

The [ARIA Authoring Practices Guide](https://www.w3.org/WAI/ARIA/apg/) supplies patterns and functional examples for roles, states, properties, keyboard support, landmarks, and accessible names. The [Using ARIA](https://www.w3.org/TR/using-aria/) guidance gives the first rule of ARIA: use a native HTML element or attribute when it already provides the required semantics and behavior. It also says interactive ARIA controls must work with the keyboard. These sources make semantic choice and keyboard behavior implementation decisions that belong in design and component review, not polish added at the end.

### Storybook: make component states the shared design and test artifact

[Storybook's UI testing guide](https://storybook.js.org/docs/writing-tests) calls stories test cases for components in their states and configurations. It presents development and testing as the same feedback loop and says stories can be reused in other testing tools.

[Interaction testing](https://storybook.js.org/docs/writing-tests/interaction-testing) puts the initial state, simulated user behavior, and assertions in a story. The `play` function can model clicks, typing, and form submission, and the resulting tests can run in Storybook, the terminal, or CI. This gives a component state a place where its user path is both reviewable and executable.

[Accessibility testing](https://storybook.js.org/docs/writing-tests/accessibility-testing) uses `axe-core`-based checks in the Storybook workflow. Its `parameters.a11y.test` setting can turn checks off, report warnings as `todo`, or make violations fail in the Storybook UI and CLI or CI. The documented progression is useful for adoption: fail on new violations, mark existing failures as visible temporary work, then remove the exceptions as they are fixed. Automated checks still cover only what the rules can detect, so they do not replace the WAI and GOV.UK human-review requirements.

[Visual testing](https://storybook.js.org/docs/writing-tests/visual-testing) compares screenshots of stories with known-good baselines. Storybook turns every story into a visual test when visual testing is enabled, and the docs describe cross-browser testing through Chromatic. This is a review of rendered appearance, not a substitute for a design brief or a check of whether the chosen direction is appropriate.

[Testing in CI](https://storybook.js.org/docs/writing-tests/in-ci) recommends running the same Storybook test command locally and in CI. The documented workflow publishes the Storybook when useful, reports the result as a pull-request status check, and can link a failure to the failing story. The source makes the gate concrete: a component state that is easy to inspect locally can become an executable PR check with a debugging path.

### Vercel: a short, file-level interface review, not a conformance standard

The [Vercel Web Interface Guidelines README](https://github.com/vercel-labs/web-interface-guidelines/blob/main/README.md) describes the list as living and non-exhaustive. It covers decisions such as keyboard operation, visible focus, focus management, hit targets, zoom, loading states, and content behavior.

The repository's [`command.md`](https://github.com/vercel-labs/web-interface-guidelines/blob/main/command.md) turns that list into a review command. It asks the reviewer to read the changed files, check rules such as native semantic elements, labels, `aria-label` for icon-only buttons, visible focus, reduced motion, and useful error messages, and report findings grouped by file in terse `file:line` form. The source also lists anti-patterns such as disabling zoom, blocking paste, `transition: all`, click handlers on non-interactive elements, unlabeled inputs, and icon buttons without an accessible name.

This is a good human review overlay because it is concrete and easy to apply to a diff. It should remain an overlay. The repository calls itself non-exhaustive, and its preferences include product and framework opinions. WCAG, WAI-ARIA, manual review, and assistive-technology testing remain the authority for accessibility acceptance.

### GOV.UK: prototype before commitment, then use regular and formal review

The GOV.UK [Making prototypes](https://www.gov.uk/service-manual/design/making-prototypes) guidance says teams must prototype to explore, share, and test designs before committing to a build. It encourages trying multiple prototypes and discarding designs that do not test well. It says code prototypes are useful for realistic user research and for exposing web constraints, but prototype code does not need production standards and should not simply be copied into the live service.

The GOV.UK [Testing for accessibility](https://www.gov.uk/service-manual/helping-people-to-use-your-service/testing-for-accessibility) guidance sets WCAG 2.2 AA as the minimum for a service working to the Service Standard. It says to think about accessibility from the start, test regularly throughout development, support common assistive technologies, test with disabled and older users, and complete a formal accessibility audit before public beta. It also separates automated, manual, assistive-technology, and formal audit activities.

The GOV.UK [service assessment guidance](https://www.gov.uk/service-manual/service-assessments/how-service-assessments-work) describes a peer review by a panel that normally includes a lead assessor, user researcher, designer, and technical lead. The [booking guidance](https://www.gov.uk/service-manual/service-assessments/book-a-service-assessment) asks for a service brief, a recent prototype or development environment, and a high-level technical architecture diagram. The exact government process is not a requirement for a product team, but the review shape is relevant: the final gate examines evidence from design, research, implementation, and technical delivery together.

## Implications

The current skill layout already has the right nouns: [`frontend-design`](../../skills/frontend/frontend-design/SKILL.md), [`prototype`](../../skills/shaping/prototype/SKILL.md), [`web-design-guidelines`](../../skills/frontend/web-design-guidelines/SKILL.md), [`implement`](../../skills/workflow/implement/SKILL.md), and [`code-review`](../../skills/review/code-review/SKILL.md). The missing piece is the contract between them.

### 1. Make design direction a reviewable contract

Keep the existing visual-design emphasis on subject matter, distinctive choices, tokens, wireframes, content, and self-critique. Add a small handoff section to the design output with:

- the intended audience and primary job
- the visual choices that are intentional, including type, color, spacing, layout, imagery, and motion
- the accessibility target and known constraints, such as contrast, zoom, focus, reduced motion, and non-color cues
- the states and content extremes that the design must cover
- the question that still needs a prototype

This preserves visual authorship while making the choices inspectable by the next skill. WAI's early-evaluation guidance and WCAG's testable criteria support recording accessibility constraints before implementation. ([WAI evaluation overview](https://www.w3.org/WAI/test-evaluate/), [WCAG 2.2](https://www.w3.org/TR/WCAG22/))

### 2. Treat the prototype verdict as the handoff, not the prototype code

The existing prototype skill already says to state the question, compare UI variants, mark the code as throwaway, and capture the answer. Make the captured answer a small decision record with the winning variant, why it won, the tested states or user path, accessibility issues found, and constraints that production code must preserve. Keep the prototype itself on its throwaway branch and rewrite the production implementation. That matches GOV.UK's distinction between realistic code prototypes and production code.

### 3. Use one state matrix across design, stories, review, and CI

For each meaningful component or route, define the states before implementation and use the same names everywhere. The exact matrix depends on the product, but it should usually ask about the default path, loading, empty, error, long content, focus and keyboard path, narrow viewport, and reduced motion. This is a synthesis from WCAG-EM's requirement to include views, states, and functionality, Storybook's story-as-test model, and the existing prototype skill's insistence on surfacing state. It should be treated as a convention, not as a WCAG checklist.

The matrix gives each skill a clear responsibility:

- `frontend-design` defines the visual treatment and content for each state.
- `prototype` explores the uncertain states and records the decision.
- implementation creates production components and stories for the agreed states.
- `web-design-guidelines` reviews the changed files and reports concrete `file:line` findings.
- CI runs the stories and blocks regressions.
- release review samples complete flows and states for manual and assistive-technology testing.

### 4. Make component stories the implementation seam

When the stack supports Storybook or an equivalent fixture system, require stories for the states that matter to a design decision. Add interaction assertions for behavior, accessibility checks for machine-detectable violations, and visual baselines for intentional appearance. Prefer native HTML and APG patterns before inventing custom ARIA widgets, and make keyboard behavior part of the interaction story where the control is interactive. ([Using ARIA](https://www.w3.org/TR/using-aria/), [ARIA APG](https://www.w3.org/WAI/ARIA/apg/), [Storybook interaction tests](https://storybook.js.org/docs/writing-tests/interaction-testing))

Do not make a visual baseline the only approval. A screenshot can pass while the accessible name, keyboard order, focus management, or error announcement is wrong. Conversely, an automated accessibility check can pass while the layout is confusing or the visual direction has drifted.

### 5. Split automated gates from human review

Use a small, explicit gate set:

1. Local development: render the changed states, exercise the important user path, run automated accessibility checks, and inspect the design against the brief.
2. Pull request CI: run the same component or Storybook checks, fail new accessibility errors, run interaction tests, and compare visual baselines. Publish or otherwise expose the changed stories so a failure is inspectable. Storybook documents this pattern as a PR status check.
3. Pull request human review: run the Vercel-style interface checklist on changed files and review the design contract. Treat intentional visual diffs as an explicit decision, not as blanket snapshot approval.
4. Release or major milestone: use a representative WCAG-EM-style scope, manual checks, assistive-technology checks, and, where the product risk warrants it, an external or formal accessibility audit. Include design, research, and technical perspectives in the review.

The CI gate should block regressions that a machine can observe. The human gate should cover semantics, user experience, design intent, and tool blind spots. The release gate should establish evidence for the complete in-scope experience, not imply that a green component suite is a conformance claim.

### 6. Record exceptions as work, not as silent configuration

If existing stories cannot pass accessibility checks, use a visible temporary exception with an owner, reason, affected states, and removal condition. Storybook documents `todo` as a way to keep existing violations visible while the team fixes them. A review should require an expiry or follow-up issue for each exception. The same rule applies to an intentional visual-baseline change and to a waived interface-guideline finding.

## Recommended skill-level outcome

The smallest useful design change is a shared frontend delivery contract, referenced by the existing skills rather than a new all-purpose skill:

```text
brief
  -> design direction + accessibility constraints
  -> prototype question and verdict
  -> state matrix
  -> production components + stories
  -> local review
  -> PR CI: render, interaction, a11y, visual
  -> human interface/design review
  -> release: representative manual and assistive-technology evaluation
```

The contract should define required evidence at each arrow and name what can block progress. It should not claim that visual review, automated a11y checks, or a selected sample alone proves accessibility conformance. That boundary is explicit in the WAI sources and keeps the skills composable.

## Sources

- [WAI: Evaluating Web Accessibility Overview](https://www.w3.org/WAI/test-evaluate/)
- [W3C: WCAG Evaluation Methodology 2.0](https://www.w3.org/TR/WCAG-EM/)
- [W3C: Web Content Accessibility Guidelines (WCAG) 2.2](https://www.w3.org/TR/WCAG22/)
- [WAI: ARIA Authoring Practices Guide](https://www.w3.org/WAI/ARIA/apg/)
- [W3C: Using ARIA](https://www.w3.org/TR/using-aria/)
- [Storybook: How to test UIs](https://storybook.js.org/docs/writing-tests)
- [Storybook: Interaction tests](https://storybook.js.org/docs/writing-tests/interaction-testing)
- [Storybook: Accessibility tests](https://storybook.js.org/docs/writing-tests/accessibility-testing)
- [Storybook: Visual tests](https://storybook.js.org/docs/writing-tests/visual-testing)
- [Storybook: Testing in CI](https://storybook.js.org/docs/writing-tests/in-ci)
- [Vercel: Web Interface Guidelines README](https://github.com/vercel-labs/web-interface-guidelines/blob/main/README.md)
- [Vercel: Web Interface Guidelines review command](https://github.com/vercel-labs/web-interface-guidelines/blob/main/command.md)
- [GOV.UK Service Manual: Making prototypes](https://www.gov.uk/service-manual/design/making-prototypes)
- [GOV.UK Service Manual: Testing for accessibility](https://www.gov.uk/service-manual/helping-people-to-use-your-service/testing-for-accessibility)
- [GOV.UK Service Manual: What happens at a service assessment](https://www.gov.uk/service-manual/service-assessments/how-service-assessments-work)
- [GOV.UK Service Manual: Book a service assessment](https://www.gov.uk/service-manual/service-assessments/book-a-service-assessment)
