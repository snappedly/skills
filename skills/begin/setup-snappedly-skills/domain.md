# Domain docs

How Snappedly skills consume this repo's shared vocabulary and architectural decisions.

## Before exploring

- Use the glossary and map paths recorded below. If no paths are recorded, read `GLOSSARY-MAP.md` or the root `GLOSSARY.md`; accept legacy `CONTEXT-MAP.md` and `CONTEXT.md` layouts. Follow a map to the contexts relevant to the work.
- Read ADRs in `docs/adr/` that touch the area being changed. In a multi-context repo, also check the relevant context's `docs/adr/` directory.

If these files do not exist, proceed with the repository's available context. The domain-modeling workflow creates them when a term or decision needs to be recorded.

## Selected paths

[Record the resulting glossary or map path, context-specific glossary paths, and shared and context-specific ADR directories.]

## File structure

The examples use the defaults for new and migrated repositories. References to `GLOSSARY.md` mean the selected glossary, including a custom path or a legacy path awaiting migration.

Single-context repo:

```text
/
├── GLOSSARY.md
├── docs/adr/
│   ├── 0001-event-sourced-orders.md
│   └── 0002-postgres-for-write-model.md
└── src/
```

Multi-context repo:

```text
/
├── GLOSSARY-MAP.md
├── docs/adr/                          # system-wide decisions
└── src/
    ├── ordering/
    │   ├── GLOSSARY.md
    │   └── docs/adr/                  # context-specific decisions
    └── billing/
        ├── GLOSSARY.md
        └── docs/adr/
```

## Use the glossary

When an output names a domain concept, use the term defined in the relevant `GLOSSARY.md`. Keep the project's chosen term when the glossary avoids a synonym. If the needed concept is missing, flag the gap for the domain-modeling workflow instead of inventing a competing term.

## Respect ADRs

When a proposed change conflicts with an ADR, surface the conflict explicitly and identify the ADR. Continue only after the user decides whether to follow or reopen it.
