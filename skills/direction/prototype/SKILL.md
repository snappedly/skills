---
name: prototype
description: Build a throwaway prototype to answer a design question. Use when the user wants to sanity-check whether a state model or logic feels right, or explore what a UI should look like.
license: MIT
---

# Prototype

A prototype is **throwaway code that answers a question**. The question decides the shape.

## Pick a branch

Identify which question is being answered, using the user's prompt, the surrounding code, or by asking if the user is around:

- **"Does this logic / state model feel right?"** (business logic, state transitions, data shape, or an API before it's written: anything that looks reasonable on paper but only feels wrong once pushed through real cases) → [LOGIC.md](LOGIC.md), a shareable HTML demo that drives the model.
- **"What should this look like?"** (a page, a layout, options for a screen) → [UI.md](UI.md), one treatment or a set of variants rendered on a real route.

The two branches produce very different artifacts, so getting this wrong wastes the whole prototype. If the question is genuinely ambiguous and the user isn't reachable, default to whichever branch better matches the surrounding code (a backend module → logic; a page or component → UI) and state the assumption at the top of the prototype.

## Rules that apply to both

1. **Throwaway from day one, and clearly marked as such.** Locate the prototype code close to where it will actually be used (next to the module or page it's prototyping for) so context is obvious, but name it so a casual reader can see it's a prototype, not production.
2. **Trivial to run.** A UI prototype starts from one command in the project's task runner. A logic demo is a single HTML file the user double-clicks.
3. **In-memory state by default.** The prototype depends on nothing its question doesn't need. If the question explicitly involves a database, hit a scratch DB or a local file with a clear "PROTOTYPE, wipe me" name.
4. **Runnable is the bar.** Write only what answers the question: error handling only where the prototype would otherwise not run, and no tests or abstractions; a prototype that needs tests is no longer a prototype. The point is to learn something fast.
5. **Surface the state.** After every action (logic) or on every variant switch (UI), print or render the full relevant state so the user can see what changed.
6. **Capture the answer.** Report the question, verdict, and artifact location. Then list every prototype file and edit, including changes to real pages and any shared switcher, and ask the user whether to delete them, move them to a separate branch, or keep them, so a later commit cannot carry them into production unawares. Integrate the decision into production code only when that work is authorized. A prototype request is done when the answer is reported and every listed file is deleted, moved, or kept as the user chose.
