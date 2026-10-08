---
name: improve-codebase-architecture
description: Find deepening opportunities across a codebase or around a PR, commit, or branch, present them as a visual HTML report, then grill through whichever one you pick.
disable-model-invocation: true
license: MIT
---

# Improve Codebase Architecture

Surface architectural friction and propose **deepening opportunities**: refactors that turn shallow modules into deep ones. The aim is testability and AI-navigability.

Load and apply `codebase-design` for the architecture vocabulary and principles this command is built on. If it isn't installed, tell the user and use the deep-module vocabulary it draws on: Ousterhout's module, interface, depth, deep, and shallow; Feathers's seam; adapter, leverage, and locality; the deletion test below; the dependency categories in-process, local-substitutable, ports & adapters, and mock; and, for design-it-twice, sketching two contrasting interfaces before choosing one. Name everything in two vocabularies: `codebase-design`'s terms, used exactly, for the architecture, and the selected domain glossary's terms for the domain. If the glossary defines "Order," talk about "the Order intake module," not "the FooBarHandler," and not "the Order service."

## Process

### 1. Explore

**Scope before you scan**, taking the scope from what the invocation names:

- **Direction**: the user named a module, a subsystem, or a pain point. Take it. The scan is complete when every module it involves has been checked.
- **Change set**: the user named a PR, a commit or commit range, a branch, or their current changes. Start from the diff and read outward, looking for friction the change ran into as well as friction it introduced: one concept forcing edits across many modules (no **locality**), a new caller repeating setup around a shallow module, a change routing around an existing seam because its interface didn't fit. The scan is complete when every module the change touches, its callers, and sibling modules that solve the same problem have been checked.
- **Whole codebase**: the user named nothing. A working tree with uncommitted edits still gets this scope. Split the codebase into areas (top-level packages or directories) and scan every one. Deepening a module pays off by making future changes to it easier (YAGNI), so walk back a good stretch of the commit history (`git log --oneline`) to find the hot spots, the files and areas that keep coming up: scan them first, and count their churn toward their candidates' recommendation strength. The scan is complete when every area has been checked.

Scan in the current agent. When the scope is too large to read in one context, split it into areas and delegate each area to a subagent. Give it the area, the selected scope's bullet with what the user named, the rest of this step, and the `codebase-design` vocabulary. Each subagent returns the candidates in its area that pass the deletion test, with their files, the friction, and the proposed deepening, and lists any friction that crosses into another area. Follow up each cross-area friction in the current agent before presenting candidates.

Read the File structure section of the installed `domain-modeling/SKILL.md` (without that skill, use the paths `docs/agents/domain.md` records, else the root `GLOSSARY-MAP.md` or `GLOSSARY.md`, or legacy `CONTEXT-MAP.md` or `CONTEXT.md`) to select the glossary, map, and ADR paths. Read the selected glossary and the area's ADRs as read-only context before exploring. References to `GLOSSARY.md` below mean the selected glossary.

Explore the selected scope and note where you experience friction:

- Where does understanding one concept require bouncing between many small modules?
- Where are modules **shallow**, with an interface nearly as complex as the implementation?
- Where have pure functions been extracted just for testability, but the real bugs hide in how they're called (no **locality**)?
- Where do tightly-coupled modules leak across their seams?
- Which parts of the codebase are untested, or hard to test through their current interface?

Apply `codebase-design`'s **deletion test** to anything you suspect is shallow: imagine deleting the module. If complexity vanishes, it was a pass-through: it **passes the deletion test** and is a candidate. If complexity reappears across N callers, it was earning its keep.

### 2. Present candidates as an HTML report

Include every candidate that passes the deletion test, ranked by recommendation strength. The scan sets the count: one candidate is a full report, and so is ten. When the scan finds none, tell the user in one line and stop.

**ADR conflicts**: ADRs record decisions this command doesn't re-litigate. Include a candidate that contradicts an existing ADR only when the friction is real enough to warrant revisiting the ADR, and give its card an ADR callout saying why.

Write the report as a single HTML file in the OS temp directory, named `architecture-review-<timestamp>.html`, so nothing lands in the repo and each run gets a fresh file. Read [HTML-REPORT.md](HTML-REPORT.md) before writing it: it holds the scaffold, the candidate card, the diagram patterns, and the style. Open the file for the user and tell them its absolute path.

Stop at the candidates: interface design belongs to the grilling loop. After the file is written, ask the user: "Which of these would you like to explore?"

### 3. Grilling loop

Once the user picks a candidate, load and apply `grill` to walk the decision tree with them: constraints, dependencies, the shape of the deepened module, what sits behind the seam, what tests survive. If `grill` isn't installed, interview the user through that tree yourself, one round of open decisions at a time, and say so.

Side effects happen inline as decisions crystallize:

- **Naming a deepened module after a concept not in `GLOSSARY.md`, or sharpening a fuzzy term?** Load and apply `domain-modeling` and update the glossary right there; without that skill, edit the selected glossary directly.
- **User rejects the candidate with a load-bearing reason?** Offer an ADR, framed as: _"Want me to record this as an ADR so future architecture reviews don't re-suggest it?"_ A reason is load-bearing when a future review needs it to avoid re-suggesting the same thing; ephemeral reasons ("not worth it right now") and self-evident ones aren't.
- **Want to explore alternative interfaces for the deepened module?** Use `codebase-design`'s design-it-twice pattern.

**Done when** the user agrees on the deepened module's interface or rejects the candidate. The deliverable is that agreed interface, plus an ADR or ticket when the user wants one; implement the refactor only when the user asks.
