---
name: to-tickets
description: Break a plan, spec, or conversation into executable tracer-bullet tickets with blocking edges, published to the configured GitHub or GitLab tracker.
disable-model-invocation: true
---

# To Tickets

Break a plan, spec, or conversation into a set of **tickets**: tracer-bullet vertical slices, each declaring the tickets that **block** it.

Read the existing tracker and label configuration or reuse it from context. If a publishing destination or required label mapping is missing, draft the breakdown and clarify the missing value; use `/setup-snappedly-skills` when repository-wide configuration is needed.

## Process

### 1. Gather context

Work from whatever is already in the conversation context. If the user passes a reference (a spec path, an issue number or URL) as an argument, fetch it and read its full body and comments.

### 2. Explore the codebase (optional)

If you have not already explored the codebase, do so to understand the current state of the code. Ticket titles and descriptions should use the project's domain glossary vocabulary, and respect ADRs in the area you're touching.

Introduce prerequisite refactoring only when a concrete obstacle prevents the requested implementation; ordinary cleanup stays with its change.

### 3. Draft vertical slices

Break the accepted work into **tracer bullet** tickets. Count distinct outcomes and real dependencies, not files or layers. Keep the user's accepted outcomes and constraints as the boundary; leave optional improvements out unless the user accepts them or they are necessary to deliver an outcome. One cohesive outcome can remain one ticket even when it crosses layers.

<vertical-slice-rules>

- Each slice completes one observable outcome through the layers it actually needs. A UI-only outcome needs no invented schema or API work.
- A completed slice is demoable or verifiable on its own
- Each slice is sized to fit in a single fresh context window
- Keep small related changes together; create a separate prerequisite only when it genuinely blocks delivery.
- For a multi-slice plan, make the first ticket the smallest slice that validates the critical path or a risky shared assumption. State that evidence in its acceptance criteria.

</vertical-slice-rules>

Give each ticket its **blocking edges**: the other tickets that must complete before it can start. List the tracer bullet in "Blocked by" for each later ticket whose implementation depends on its unverified path or contract. A ticket with no blockers can start immediately.

**Wide refactors are the exception to vertical slicing.** A **wide refactor** is one mechanical change (rename a column, retype a shared symbol) whose **blast radius** fans across the whole codebase, so a single edit breaks thousands of call sites at once and no vertical slice can land green. Don't force it into a tracer bullet; sequence it as **expand–contract**. First expand: add the new form beside the old so nothing breaks. Then migrate the call sites over in batches sized by blast radius (per package, per directory), each batch its own ticket blocked by the expand, keeping CI green batch to batch because the old form still exists. Finally contract: delete the old form once no caller remains, in a ticket blocked by every migrate batch. When even the batches can't stay green alone, keep the sequence but let them share an integration branch that all block a final integrate-and-verify ticket; green is promised only there.

### 4. Resolve the breakdown

Present the proposed breakdown as a numbered list. For each ticket, show:

- **Title**: short descriptive name
- **Blocked by**: which other tickets (if any) must complete first
- **What it delivers**: the end-to-end behaviour this ticket makes work

Resolve material uncertainty about granularity or blocking edges with one focused question. Combine related changes when splitting would add coordination without an independently verifiable outcome.

Reuse an already approved breakdown. If the user authorized publishing and left granularity to you, proceed with the scoped breakdown; ask only about unresolved scope or dependencies that materially change delivery. Keep optional improvements out of executable tickets unless the user accepts them.

### 5. Publish the tickets to the configured tracker

Apply `technical-writing` to every ticket title and body before publishing.

Publish the approved tickets. **How** depends on the tracker `/setup-snappedly-skills` configured; the tickets are the same either way, only the shape of the blocking edges changes:
- **Issue tracker (GitHub, GitLab)** → publish one issue per ticket in dependency order (blockers first) so each ticket's blocking edges can reference real identifiers. Use the platform's native blocking / sub-issue relationship where it has one; otherwise set each ticket's "Blocked by" to the blocking issues. Apply the `ready-for-agent` triage label unless instructed otherwise; the tickets are agent-grabbable by construction.

Each created ticket is an executable work item. A parent spec or source request remains a planning or intake item. If it already has `ready-for-agent`, remove that state after all child tickets and their blocking relationships exist, then add links to the executable children. Do not close the parent.

Work the **frontier**: any ticket whose blockers are all done. For a purely linear chain that means top to bottom.
Keep the parent open; limit parent edits to the child links and planning-state correction described above.

<issue-template>

**Work item type:** executable

## Parent

A reference to the parent issue on the tracker (if the source was an existing issue, otherwise omit this section).

## What to build

The end-to-end behaviour this ticket makes work, from the user's perspective, not layer-by-layer implementation.

## Acceptance criteria

- [ ] Criterion 1
- [ ] Criterion 2

## Blocked by

- A reference to each blocking ticket, or "None (can start immediately)".

</issue-template>

Avoid specific file paths or code snippets: they go stale fast. Exception: if a prototype produced a snippet that encodes a decision more precisely than prose can (state machine, reducer, schema, type shape), inline it and note briefly that it came from a prototype. Trim to the decision-rich parts, not a working demo, just the important bits.
