---
name: grill
description: Grill the user about a plan, decision, or idea. Use when the user wants to stress-test their thinking or asks to be grilled.
license: MIT
---

Interview the user relentlessly until you reach a shared understanding. Map this as a **design tree**: every decision branches into the decisions that hang off it.

Work the tree in **rounds**. The **frontier** is every decision whose prerequisites are already settled: the questions you can ask _now_ without guessing at answers you have not heard yet, including answers to other questions in the same round. Ask the whole frontier in one round, numbering each question and giving your recommended answer, then wait for the user's answers.

Format a round like so:

```
❓ **Q1** - **<question title>**: <question body, might be multiple paragraphs, including multiple choices>

➡️ <your recommended answer>

---

❓ **Q2** - **<question title>**: <question body, might be multiple paragraphs, including multiple choices>

➡️ <your recommended answer>
```

Word each question so that "yes" accepts your recommended answer.

Each round of answers settles decisions and pushes the frontier outward: recompute it and ask the next round.

Finding _facts_ is your job; the _decisions_ are the user's. When a frontier question needs a fact from the environment (filesystem, tools, etc.), look it up directly; delegate it to a subagent with a fresh context window only when the lookup is substantial and independent of useful work you can continue, and keep asking independent questions while it is pending.

When the plan is a code change and no calling skill owns the next step, its size is a branch of the tree, settled once the rest of the plan is. The plan fits when one `/execute` run can land it as one reviewable PR. It is too big when it bundles several behaviors that could each ship and be demonstrated alone, when later parts depend on what earlier parts reveal, or when the work will span several sessions. Then recommend splitting it into a planning spec and **tracer-bullet** tickets, as [SPEC-AND-TICKETS.md](SPEC-AND-TICKETS.md) directs.

The session is done when the frontier is empty: every branch of the design tree visited, nothing left silently assumed. Then ask the user to confirm the shared understanding, and act on it only once they do. When the confirmed plan is a code change and no calling skill owns the next step, recommend `/execute` to carry it out. After a confirmed split, publish the spec and tickets as SPEC-AND-TICKETS.md directs instead.
