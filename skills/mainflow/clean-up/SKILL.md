---
name: clean-up
description: "Clean up and review branch changes, then show the edits and check results."
argument-hint: "Optional: the base branch, or the requirements the changes should meet"
disable-model-invocation: true
license: MIT
---

# Clean up

Clean up and review the scoped changes, then show this run's edits. Leave cleanup edits unstaged and uncommitted in the current checkout. Preserve the existing index, branch, and commit history. Load each dependency named below through the available skill invocation mechanism or its installed `SKILL.md`; when one is not installed, follow the fallback given with it and report the missing skill as a gap.

1. **Fix the scope.**
   - **Base.** Resolve the base branch from a branch argument, then the base branch `docs/agents/workflow.md` records (or, when it records none, `docs/agents/code-host.md`), then the default branch. Record the current branch, HEAD, and starting working-tree changes so the report can distinguish this run's edits from existing work.
   - **Batch.** When starting on either the resolved base or the default branch, scope this batch to uncommitted changes against that HEAD, which becomes the review base. Otherwise, the review base is the current branch's merge-base with the resolved base: use every change since it, plus uncommitted changes. Include staged, unstaged, and untracked task files, leaving out unrelated files such as local environment files or generated output. When the scope is empty, say so and stop.
   - **Requirements.** Use any requirements supplied in the arguments. Otherwise collect requirements from this session's requests, linked issues, or the PR description, and record "no requirements" when none exist.

   Done when the review base SHA, current branch, file list, starting changes, and requirements are recorded.
2. **Clean up.** Load and apply `code-cleanup`, scoped to the recorded files (without it, run the checks `docs/agents/workflow.md` requires, else the repository's formatter, linter, type check, and tests for the touched code, and inspect the diff for leftover debris). Done when cleanup's check record exists, or the fallback's check results are recorded.
3. **Review.** Load and apply `code-review` on the same scope after cleanup (without it, review the full diff locally against the requirements for correctness and maintainability). Supply the requirements and cleanup's check record so the review reuses those results. The review chooses its own depth. Done when every applicable review result has returned.
4. **Fix clear findings.** A clear finding has one obvious fix inside the scope that keeps the intended behavior. Fix them in one batch, rerun only the affected checks, and recheck only the fix delta; that recheck is the last review pass. Resume deferred checks through `code-cleanup` once their resume condition is met. Report all other unresolved findings for the user to decide, including judgment calls and changes to behavior, contracts, or scope. Done when every finding is fixed or listed with its next action or required decision.
5. **Show the changes.** Report this run's edits by file, with the relevant diff or file links. Distinguish them from existing work. If there were no cleanup edits, say so. Include the check record and fixed findings. For `/submit` or `/deploy`, include the resolved base, review base SHA, reviewed batch, and, on the base or default branch, the unreviewed commits on it, such as local commits its upstream lacks. Done when the report identifies this run's edits, and the cleanup edits remain uncommitted.
6. **List open items.** Decisions are the open findings left for the user to decide. Gaps are everything left unverified: each open finding with a next action, each failing, deferred, or blocked check, each coverage gap, each missing review axis, each missing skill, and any unreviewed commits.

   <!-- shared: open-items -->
   End the report with a horizontal rule and a **Check before you submit or deploy** heading, followed by two numbered lists: **Decisions needed** and **Gaps to check**. Write each item in plain language that someone who has not read the rest of the report can act on, and end it with your recommendation and the reason for it.

   - For a decision, say what is at stake and where, and list the options under it.
   - For a gap, say what was not verified and where, why, and the risk. When there is more than one way to close it, such as rerunning a check, verifying by hand, or accepting the risk, list the options under it.

   Write "None" under an empty list's heading.

   When you later act on these items, report each one under its current status: **Done**, **Handed off** (with where it is tracked), **Accepted**, or **Still open**. Lead each item with its outcome. An item is done once its decision is applied or what it named is verified; a gap that someone else will verify is handed off.
   <!-- /shared: open-items -->

   Done when the report ends with both lists, and every open finding and gap appears in one of them.
