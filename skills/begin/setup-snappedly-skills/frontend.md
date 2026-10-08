# Frontend conventions

How Snappedly skills read this repo's design language and audit its user interface.

## Design system

[The component library or design system in use, and where its components live. Write "none yet" when the repo has no system.]

Treat these components as the vocabulary of any new surface. Compose what exists before adding a new primitive, and when a surface genuinely needs one, add it to the system rather than beside it.

## Tokens

[Where color, type, spacing, radius, and motion values are defined: a Tailwind config, a theme file, CSS custom properties, or "none yet".]

Reference tokens rather than literal values. A design that needs a value the tokens don't carry is proposing a change to the tokens, so raise it as one.

## UI directories

[The directories holding user-facing interface, as glob patterns.]

The `code-review` Interface axis audits changes under these paths, and any other user-facing component, route, template, or style; it skips a change that touches none of these.

## Visual direction

**Direction: [established | open].**

Set this to `established` when new work follows the system above. New surfaces then treat the system as the brief and design only what it leaves open: the shape of a hero, the hierarchy of a new screen, the copy.

Set it to `open` for a greenfield product, a redesign, or a named surface where a new look is wanted, and say which surface. Work on that surface then sets palette, type, and layout from scratch.

## Accessibility baseline

[Any conformance target the team commits to, for example WCAG 2.2 AA, plus rules the audit treats as non-negotiable. Write "the web interface guidelines as shipped" when there is nothing extra.]
