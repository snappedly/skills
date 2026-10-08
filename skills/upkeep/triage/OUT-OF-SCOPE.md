# Out-of-Scope Knowledge Base

The `.out-of-scope/` directory in a repo stores persistent records of rejected feature requests. Each record keeps the reasoning after the issue closes, and lets triage surface the previous decision instead of re-litigating it when a matching request arrives.

## File format

Keep one file per **concept**, not per issue: multiple requests for the same thing are grouped under one file. Name it in short, descriptive kebab-case that tells someone browsing the directory what was rejected without opening the file: `dark-mode.md`, `plugin-system.md`, `graphql-api.md`.

Write it as a short design document rather than a database entry: paragraphs, code samples, and examples that make the reasoning clear to someone encountering it for the first time.

````markdown
# Dark Mode

This project does not support dark mode or user-facing theming.

## Why this is out of scope

The rendering pipeline assumes a single color palette defined in
`ThemeConfig`. Supporting multiple themes would require:

- A theme context provider wrapping the entire component tree
- Per-component theme-aware style resolution
- A persistence layer for user theme preferences

This is a significant architectural change that doesn't align with the
project's focus on content authoring. Theming is a concern for downstream
consumers who embed or redistribute the output.

```ts
// The current ThemeConfig interface is not designed for runtime switching:
interface ThemeConfig {
  colors: ColorPalette; // single palette, resolved at build time
  fonts: FontStack;
}
```

## Prior requests

- #42: "Add dark mode support"
- #87: "Night theme for accessibility"
- #134: "Dark theme option"
````

### Writing the reason

Give a substantive reason that explains why, rather than "we don't want this". Good reasons reference:

- Project scope or philosophy ("This project focuses on X; theming is a downstream concern")
- Technical constraints ("Supporting this would require Y, which conflicts with our Z architecture")
- Strategic decisions ("We chose to use A instead of B because...")

The reason should be durable: a temporary circumstance ("we're too busy right now") marks a deferral, not a rejection.

## When a request matches a prior rejection

Surface the match to the maintainer: "This is similar to `.out-of-scope/dark-mode.md`. We rejected this before because [reason]. Do you still feel the same way?"

The maintainer may:

- **Confirm**: close the new item through the write flow below, which adds it to the existing file's "Prior requests" list.
- **Reconsider**: delete or update the out-of-scope file, leaving old issues closed as historical records; the new item proceeds through normal triage.
- **Disagree**: the requests are related but distinct; proceed with normal triage.

## When to write to `.out-of-scope/`

Write here when an **enhancement** is *rejected* as `wontfix`, whether it arrived as an issue or a PR: recording a rejected PR keeps the same request from returning as fresh code.

1. If a matching `.out-of-scope/` file exists, append the new item to its "Prior requests" list. Otherwise create a file for the concept with the decision, the reason, and the item as its first prior request.
2. Publish the record through the delivery policy in `docs/agents/workflow.md`. When that file records no publish transition, or the policy leaves the commit or push to a human, ask the maintainer how to publish it, and finish steps 3 and 4 once it is published or its change request is open.
3. Comment on the item explaining the decision and, once the record is published, linking it: the file on the base branch, or the change request that adds it.
4. Close the item with the `wontfix` role.
