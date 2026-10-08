---
name: clean-up
description: "Clean up, review, fix, and commit everything you've changed on the current branch in one pass."
argument-hint: "Optional: the base branch, or the requirements the changes should meet"
disable-model-invocation: true
license: MIT
---

# Clean up

Finish a batch of changes in one pass. This skill is the caller for `code-cleanup` and `code-review`: it owns the scope, the fixes, and the commit. Load each dependency named below through the available skill invocation mechanism or its installed `SKILL.md`; when one is not installed, follow the fallback given with it and report the missing skill as a gap.

1. **Fix the scope.**
   - **Base.** Resolve the base branch from a branch argument, then the base branch `docs/agents/workflow.md` records (or, when it records none, `docs/agents/code-host.md`), then the default branch. Record the starting branch and HEAD before switching branches.
   - **Batch.** When starting on either the resolved base or the default branch, scope this batch to uncommitted changes against that HEAD, which becomes the review base. Otherwise, the review base is the current branch's merge-base with the resolved base: use every change since it, plus uncommitted changes. Include staged, unstaged, and untracked task files, leaving out unrelated files such as local environment files or generated output. When the scope is empty, say so and stop.
   - **Requirements.** Use any requirements supplied in the arguments. Otherwise collect requirements from this session's requests, linked issues, or the PR description, and record "no requirements" when none exist.
   - **Task branch.** For a batch starting on the base or default branch, create a new branch named for the change at the recorded HEAD and carry the uncommitted work onto it. Keep measuring the batch from the recorded HEAD after switching, not from the resolved base, so commits where the default branch already differs from the configured base stay outside this batch. Preserve the starting branch's ref and the user's index.

   Done when the review base SHA, task branch, file list, and requirements are recorded.
2. **Clean up.** Load and apply `code-cleanup`, scoped to the recorded files (without it, run the checks `docs/agents/workflow.md` requires, else the repository's formatter, linter, type check, and tests for the touched code, and inspect the diff for leftover debris). Done when cleanup's check record exists, or the fallback's check results are recorded.
3. **Review.** Load and apply `code-review` on the same scope after cleanup (without it, review the full diff locally against the requirements for correctness and maintainability). Supply the requirements and cleanup's check record so the review reuses those results. The review chooses its own depth. Done when every applicable review result has returned.
4. **Fix clear findings.** A clear finding has one obvious fix inside the scope that keeps the intended behavior. Fix them in one batch, rerun only the affected checks, and recheck only the fix delta; that recheck is the last review pass. Report judgment calls, behavior changes, contract or scope changes, and anything still open after the recheck for the user to decide. Done when every finding is fixed or listed as open with the decision it needs.
5. **Commit.** The user's invocation authorizes this commit. Commit the scope to the recorded task branch with a message in the repository's convention, including when checks fail or findings stay open. When the review reports a reviewer whose cancellation is unconfirmed, leave the scope uncommitted and report that instead. Let repository hooks run; if a hook rejects the commit, report its output and leave the changes staged. Done when the commit exists, or the hook failure or held commit is reported.

Report the commit SHA, resolved base branch, review base SHA, reviewed batch, cleanup edits, check results, fixed findings, and open findings with the decision each needs. Include any branch divergence excluded from the batch so deployment can reconcile its full diff with the reviewed scope.
