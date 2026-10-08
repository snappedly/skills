---
name: domain-modeling
description: Domain modeling for a project's glossary and ADRs. Use when discussing codebase terminology, editing its domain glossary, or recording or editing an ADR.
license: MIT
---

# Domain Modeling

Build and sharpen the project's domain model as you design: challenge terms, invent edge-case scenarios, and write terms and decisions down the moment they crystallize.

## File structure

For a vocabulary lookup, apply only this section and read the selected existing files as context. Continue with the active modeling sections only when the task calls for changing terms or recording decisions.

Read `docs/agents/domain.md` when present and use its recorded glossary, map, and ADR paths. Without recorded paths, use `GLOSSARY-MAP.md` or the root `GLOSSARY.md`; existing `CONTEXT-MAP.md` and `CONTEXT.md` remain valid. References to `GLOSSARY.md` throughout this skill mean the selected glossary, including a configured or legacy path.

The default layouts for new and migrated repositories:

- **Single context** (most repos): a root `GLOSSARY.md`, with ADRs in `docs/adr/`.
- **Multiple contexts**: a root `GLOSSARY-MAP.md` points to each context's directory (such as `src/ordering/`), which holds that context's `GLOSSARY.md` and a `docs/adr/` for context-specific decisions. The root `docs/adr/` holds system-wide decisions.

Follow a map to the context the work relates to. When the match is unclear, a vocabulary lookup reads each plausible context's glossary; active modeling asks the user.

## During the session

Edit the existing authoritative files, legacy ones included, and create no second glossary beside them; `setup-snappedly-skills` migrates legacy domain filenames and their consumers. If both conventions exist and authority is unclear, resolve it before editing.

Create files lazily: the glossary when the first term is resolved, an ADR directory when its first ADR is needed.

### Challenge against the glossary

When the user uses a term that conflicts with the existing language in `GLOSSARY.md`, call it out immediately. "Your glossary defines 'cancellation' as X, but you seem to mean Y. Which is it?"

### Sharpen fuzzy language

When the user uses vague or overloaded terms, propose a precise canonical term. "You're saying 'account': do you mean the Customer or the User? Those are different things."

### Discuss concrete scenarios

When domain relationships are being discussed, invent edge-case scenarios that force the user to be precise about the boundaries between concepts.

### Cross-reference with code

When the user states how something works, check whether the code agrees. If you find a contradiction, surface it: "Your code cancels entire Orders, but you just said partial cancellation is possible. Which is right?"

### Update GLOSSARY.md inline

When a term is resolved, update `GLOSSARY.md` right there, using the format in [GLOSSARY-FORMAT.md](./GLOSSARY-FORMAT.md).

Keep `GLOSSARY.md` a glossary: domain terms and their definitions only, free of implementation detail. Specs, scratch notes, and implementation decisions belong elsewhere.

### Offer ADRs sparingly

Only offer to create an ADR when all three are true:

1. **Hard to reverse**: the cost of changing your mind later is meaningful
2. **Surprising without context**: a future reader will wonder "why did they do it this way?"
3. **The result of a real trade-off**: there were genuine alternatives and you picked one for specific reasons

[ADR-FORMAT.md](./ADR-FORMAT.md) has the template and examples of what qualifies.
