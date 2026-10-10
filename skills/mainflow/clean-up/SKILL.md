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
4. **Fix clear findings.** A clear finding has one obvious fix inside the scope that keeps the intended behavior. Fix them in one batch, rerun only the affected checks, and recheck only the fix delta; that recheck is the last review pass. Report judgment calls, behavior changes, contract or scope changes, and anything still open after the recheck for the user to decide. Done when every finding is fixed or listed as open with the decision it needs.
5. **Show the changes.** Report this run's edits by file, with the relevant diff or file links. Distinguish them from existing work. If there were no cleanup edits, say so. Include the check record, fixed findings, and open findings with the decision each needs. For `/submit` or `/deploy`, include the resolved base, review base SHA, reviewed batch, and, on the base or default branch, the unreviewed commits on it, such as local commits its upstream lacks.

   Done when the report identifies this run's edits and unresolved findings, and the cleanup edits remain uncommitted.
