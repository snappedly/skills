---
name: grill
description: Grill the user about a plan, decision, or idea. Use when the user wants to stress-test their thinking or asks to be grilled.
license: MIT
---

Interview the user relentlessly until you reach a shared understanding. Map this as a **design tree**: every decision branches into the decisions that hang off it.

Work the tree in **rounds**. The **frontier** is every decision whose prerequisites are already settled: the questions you can ask _now_ without guessing at answers you haven't heard yet, including answers to other questions in the same round. Ask the whole frontier in one round, numbering each question and giving your recommended answer, then wait for the user's answers.

Format a round like so:

```
❓ **Q1** - **<question title>**: <question body, might be multiple paragraphs, including multiple choices>

➡️ <your recommended answer>

---

❓ **Q2** - **<question title>**: <question body, might be multiple paragraphs, including multiple choices>

➡️ <your recommended answer>
```

Each round of answers settles decisions and pushes the frontier outward: recompute it and ask the next round.

Finding _facts_ is your job; the _decisions_ are the user's. When a frontier question needs a fact from the environment (filesystem, tools, etc.), look it up directly; delegate only when the lookup is substantial and independent of useful work you can continue, and keep asking independent questions while it is pending.

The session is done when the frontier is empty: every branch of the design tree visited, nothing left silently assumed. Then ask the user to confirm the shared understanding, and act on it only once they do. When the confirmed plan is a code change and no calling skill owns the next step, recommend `/execute` to carry it out.
