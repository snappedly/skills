# Domain docs

How Snappedly skills consume this repo's shared vocabulary and architectural decisions.

## Before exploring

- Read `CONTEXT.md` at the repo root, or `CONTEXT-MAP.md` if it exists. Follow the map to the contexts relevant to the work.
- Read ADRs in `docs/adr/` that touch the area being changed. In a multi-context repo, also check the relevant context's `docs/adr/` directory.

If these files do not exist, proceed with the repository's available context. The domain-modeling workflow creates them when a term or decision needs to be recorded.

## File structure

Single-context repo:

```text
/
├── CONTEXT.md
├── docs/adr/
│   ├── 0001-event-sourced-orders.md
│   └── 0002-postgres-for-write-model.md
└── src/
```

Multi-context repo:

```text
/
├── CONTEXT-MAP.md
├── docs/adr/                          # system-wide decisions
└── src/
    ├── ordering/
    │   ├── CONTEXT.md
    │   └── docs/adr/                  # context-specific decisions
    └── billing/
        ├── CONTEXT.md
        └── docs/adr/
```

## Use the glossary

When an output names a domain concept, use the term defined in the relevant `CONTEXT.md`. Keep the project's chosen term when the glossary avoids a synonym. If the needed concept is missing, flag the gap for the domain-modeling workflow instead of inventing a competing term.

## Respect ADRs

When a proposed change conflicts with an ADR, surface the conflict explicitly and identify the ADR. Continue only after the user decides whether to follow or reopen it.
