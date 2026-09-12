---
name: frontend-guidelines
description: Audit UI code against the Web Interface Guidelines, reported at `file:line`. Use when asked to "review my UI", "check accessibility", "audit design", "review UX", or when another skill needs these rules.
---

# Frontend Guidelines

Audit user-facing interface code against the Web Interface Guidelines: accessibility, focus states, forms, animation, typography, performance, touch, theming, i18n, hydration, copy, and the anti-pattern list.

## The rules

[`GUIDELINES.md`](GUIDELINES.md) is a **pinned copy** of the guidelines and the source of truth for every audit. Reading the pin rather than the network keeps the audit deterministic, offline-capable, and usable inside a sub-agent with no web access, which is how `code-review` runs this skill as its Interface axis.

## Process

1. Read [`GUIDELINES.md`](GUIDELINES.md) in full, including its output format.
2. Resolve the files under audit from the caller's argument, file list, or pattern. Ask the user which files to review when none was supplied.
3. Apply every rule to every file. Read enough surrounding code to tell a real violation from a rule satisfied elsewhere: a label rendered by a wrapper, a focus ring set by a shared class, a token that already honours `prefers-reduced-motion`.
4. Report findings in the format `GUIDELINES.md` specifies: grouped by file, one terse `file:line` line per finding, `✓ pass` for a clean file. State the issue and its location; explain only when the fix is non-obvious.

Completion criterion: every rule applied to every file under audit, each finding carrying a `file:line`, and every audited file either listed with findings or marked `✓ pass`.

## Refreshing the pin

Refresh on request, or when a finding turns on a rule you have reason to think changed. Otherwise audit against the pin as it stands.

```bash
curl -fsSL https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md
```

Compare the result against `GUIDELINES.md`, apply the rule changes, and update the commit and retrieval date in its provenance header:

```bash
curl -fsSL "https://api.github.com/repos/vercel-labs/web-interface-guidelines/commits?path=command.md&per_page=1"
```

Keep the upstream wording; the pin is a copy, not a rewrite. Report which rules changed. If the fetch fails, say so and audit against the existing pin rather than skipping rules.
