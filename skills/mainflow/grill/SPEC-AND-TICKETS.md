# Spec and tracer-bullet tickets

A plan too big for one `/execute` run becomes a **planning spec**, which records the settled design, and executable child tickets, which carry the work. Each ticket is a **tracer bullet**, a thin vertical slice that runs end to end through every layer its behavior touches, so the team can merge it, see it work, and correct the plan before the next slice starts.

## Slice the plan

1. **Start with the tracer bullet.** The first ticket is the thinnest path that works end to end. It takes one input through every layer to one visible result, using the real dependencies. Stub, hard-code, or leave out everything the path does not need. Make it exercise the plan's riskiest assumption, so a wrong approach shows up in the first PR.
2. **Widen the path one behavior at a time.** Each later ticket adds one behavior to the working path, such as another case, entry point, data shape, or error path. It is a vertical slice too, and the system still works and can be demonstrated when it merges.
3. **Build each layer inside the slice that first uses it.** A ticket named after a layer, such as "add the tables", "build the endpoints", or "build the screens", is a horizontal slice that nobody can see working until the others land. Re-cut it along behaviors.
4. **Size each ticket for one run.** A ticket fits one `/execute` session and one reviewable PR. Split a bigger slice along behaviors, and combine a slice too small to demonstrate on its own with its neighbor.
5. **Order by dependency.** The tracer bullet blocks every other ticket. Name each ticket's blockers. Once their blockers close, `/execute` on the spec carries out the unblocked tickets together, in parallel where they share no files or contracts.

Done when every behavior in the plan belongs to exactly one ticket or to the spec's out-of-scope list, the first ticket is a tracer bullet, and every ticket is a vertical slice with its blockers named.

### Example

Plan: users export any report as CSV with the active filters applied, and large exports run in the background.

1. Tracer bullet: the export button on the sales report downloads a CSV of one column from the real query. No filters and no other reports.
2. Export every column, with dates and currency formatted. Blocked by 1.
3. Apply the active filters to the export. Blocked by 1.
4. Add export to the other report pages. Blocked by 1.
5. Run large exports in the background and notify the user when the file is ready. Blocked by 2 and 3.

## Propose the tickets

Ask the split question in grill's round format, with the split as the recommended answer and the proposed tickets listed under it: for each ticket, a title, the end-to-end behavior it delivers, and its blockers. The ticket boundaries are the user's decisions, so revise them until the user agrees.

## Publish

Publish only after the user confirms the shared understanding, tickets included. Read `docs/agents/issue-tracker.md` for the tracker, its work item mapping, and its parent and child operations. Without it, give the drafts in the conversation and recommend `/setup-snappedly-skills` to configure a tracker. Load and apply `technical-writing` to every title and body before publishing. Without it, write plain, specific prose and say that it is missing. Describe behavior, interfaces, and contracts rather than file paths and line numbers, so the tickets stay true while the code changes.

1. Create the spec:

   ```markdown
   **Work item type:** planning spec, not executable

   ## Problem
   What users or the system need, and why.

   ## Decisions
   Each decision settled during the grill, with its reason.

   ## Acceptance
   The condition that accepts the whole spec, beyond its tickets closing.

   ## Tickets
   Filled in after the tickets exist, in order, with the tracer bullet first.

   ## Out of scope
   ```

2. Create the tickets in dependency order, so each blocker exists before a ticket names it:

   ```markdown
   **Work item type:** executable

   ## What to build
   The end-to-end behavior this slice delivers. For the tracer bullet, also what it stubs or leaves out.

   ## Acceptance criteria
   - [ ] Behavior that a person can observe or a test can check through the real path

   ## Blocked by
   The blocking tickets, or none.

   ## Out of scope
   Behavior that later tickets deliver.
   ```

3. Link each ticket to the spec through the parent and child operation that `issue-tracker.md` records. When triage roles are configured, give the `ready-for-agent` state to the tickets with no open blockers, and report the others as waiting on their blockers.
4. Fill in the spec's Tickets section, then read the spec and each ticket back from the tracker.

Done when the spec and every ticket exist in the tracker, every ticket links to the spec, and the spec lists the tickets in order. Report each item with its link and blockers. Recommend `/execute` on the spec in a fresh session; its first run builds the tracer bullet alone. Also recommend that after each run's change merges, the user updates the remaining tickets with what it revealed before the next run starts.
