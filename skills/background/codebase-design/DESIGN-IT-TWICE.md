# Design It Twice

Design the interface for a chosen deepening candidate several distinct ways, then compare. Based on "Design It Twice" (Ousterhout): your first idea is unlikely to be the best.

## Process

### 1. Frame the problem space

Before designing, write a user-facing explanation of the problem space for the chosen candidate:

- The constraints any new interface would need to satisfy
- The dependencies it would rely on, and which category they fall into (see [DEEPENING.md](DEEPENING.md))
- A rough code sketch that makes the constraints concrete: an illustration, not a proposal

Show this to the user, then immediately proceed to Step 2. The user reads and thinks while the designs are produced.

### 2. Produce the designs

For a small interface decision, sketch two distinct designs locally. For substantial decisions benefiting from independent judgment, spawn two bounded design agents in parallel. Add another only for a materially different constraint the first two do not cover. Each design must offer a distinct interface for the module.

Give each design a different one of these constraints. By default, the two designs take the first two constraints; swap in a later one when it fits the candidate better, such as ports and adapters when a dependency is remote or external.

- "Minimize the interface: aim for 1–3 entry points max. Maximize leverage per entry point."
- "Maximize flexibility: support many use cases and extension."
- "Optimize for the most common caller: make the default case trivial."
- "Design around ports & adapters for cross-seam dependencies."

Read the File structure section of the installed `domain-modeling/SKILL.md` (without that skill, use the paths `docs/agents/domain.md` records, else the root `GLOSSARY-MAP.md` or `GLOSSARY.md`, or legacy `CONTEXT-MAP.md` or `CONTEXT.md`) and the selected domain glossary as read-only context. Write a technical brief, separate from the Step 1 explanation: file paths, coupling details, the dependency category, what sits behind the seam, and the vocabulary to name things with. On the local path, sketch both designs from that brief. On the agent path, put the brief in each sub-agent's prompt with its constraint, the [SKILL.md](SKILL.md) design glossary, and the selected domain glossary's path or relevant map entry.

Each design gives:

1. Interface (types, methods, params, plus invariants, ordering, error modes)
2. Usage example showing how callers use it
3. What the implementation hides behind the seam
4. Dependency strategy and adapters
5. Trade-offs: where leverage is high, where it's thin

### 3. Present and compare

Present designs sequentially so the user can absorb each one, then compare them in prose by **depth**, **locality**, and **seam placement**.

After comparing, give your own recommendation: which design you think is strongest and why. If elements from different designs would combine well, propose a hybrid. Be opinionated: the user wants a strong read, not a menu.
