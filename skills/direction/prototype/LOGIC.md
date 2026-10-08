# Logic Prototype

A single, self-contained HTML file (a **shareable demo**) that lets anyone drive a state model by clicking buttons. Because it's one file with nothing to install, you can hand it to a non-developer (a designer, a PM, a domain expert) and let them feel the model for themselves.

## Process

### 1. State the question

Before writing code, write down what state model and what question you're prototyping: one paragraph in a visible intro at the top of the demo, not just a comment. A logic prototype that answers the wrong question is pure waste, so make the question explicit enough to check, whether the user is watching now or returning to it AFK.

### 2. Isolate the logic in a portable module

Put the actual logic (the bit that's answering the question) in a single `<script>` block written as a small, pure module that could be lifted out and dropped into the real codebase later. The page around it is throwaway; this module isn't.

Pick the shape that fits the question, _not_ the one easiest to wire to a page:

- **A pure reducer**: `(state, action) => state`. Good when actions are discrete events and state is a single value.
- **A state machine**: explicit states and transitions. Good when "which actions are even legal right now" is part of the question.
- **A small set of pure functions** over a plain data type. Good when there's no implicit current state, just transformations.
- **A class or module with a clear method surface** when the logic genuinely owns ongoing internal state.

Keep it **pure**: the page calls into the module, and the module never touches the DOM, `document`, or a button handler. That one-way flow is what makes the prototype useful past its own lifetime: once the question's answered, the validated module lifts into the real codebase on its own.

### 3. Build the shareable HTML file

One file of plain HTML/CSS/JS with everything inline, no framework, bundler, or server, so it opens by double-click and survives being emailed around.

Write it for a non-developer: every label, button, and state field is in **domain language**, reading like the business, not the reducer.

Lay it out with a clean hierarchy, top to bottom:

1. **Title and the question** from step 1.
2. **Current state**: the full relevant state, rendered as a readable panel (labeled fields, not a raw JSON dump). Where it helps a non-developer follow, call out what just changed.
3. **Free-play buttons**: one button per action, always available, so anyone can poke at the model in any order.
4. **Guided walkthroughs**: a set of **scenarios**, one per tab. Each tab holds a short plain-language description of the scenario (the situation it sets up and what to watch for) and underneath it, the ordered **buttons to press** for that scenario. Each step is a real button: clicking it performs that action and moves to the next step. Starting a walkthrough resets to a known initial state so the scenario runs the same way every time.

Choose scenarios that cover the happy path and the awkward cases, the ones hard to reason about on paper: a tricky edge case, an attempt at something that should be illegal.

Keep it beautiful but restrained: clean typography, generous spacing, one accent color, and nothing that competes with the state and the buttons.

### 4. Hand it over

Open the file for the user or send it to them. The moments that matter are when they say "wait, that shouldn't be possible" or "huh, I assumed X would be different": those are the bugs in the _idea_, which is the whole point. Add the actions or scenarios they ask for.

### 5. Capture the answer

Capture it as **Capture the answer** in [SKILL.md](SKILL.md) describes. When integrating the decision is authorized, the validated module lifts into the real codebase and the HTML shell stays out of production, since it's built for clicking through by hand.
