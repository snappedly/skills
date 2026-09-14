---
name: code-cleanup
description: "Clean and validate completed changes before commit, including behavior-preserving slop removal where applicable"
---

# Code cleanup

Prepare the current task change with mechanical, behavior-preserving cleanup and final evidence from the repository's checks.

## Timing

Run once a coherent change is ready, and before committing. This skill owns the final required checks for the state it produces; implementation may run targeted checks while coding, but the calling workflow should not add a duplicate final validation stage. After review fixes, rerun cleanup for the affected scope; cleanup reruns the affected checks before substantive changes return to review. Reuse passing check results only when the checked files, dependencies, configuration, command, and scope are unchanged.

An existing request to implement or fix code authorizes this cleanup within that task. A review-only request stays read-only; report missing validation evidence without editing the code. Leave staging, commits, pushes, and deployments to the calling workflow.

## Process

1. **Establish scope.** Read applicable agent instructions and `docs/agents/workflow.md` when present. Inspect `git status --short`, `git diff`, and `git diff --cached`; include untracked task files. Include the branch/base comparison when the task spans existing commits, using the caller's base rather than assuming `main`. Identify the task's files and preserve unrelated edits. If no task change is present, report that and stop. Keep the index unchanged. For partially staged files, distinguish validation of the working copy from validation of the staged version.

2. **Discover the checks.** Reuse the caller's check map when its source configuration is unchanged and it covers the current scope. Read repository scripts, tool configuration, CI, and contribution guidance for missing or changed coverage. Identify the configured formatter and linter for each changed file type or package, their check and fix modes, and required typechecks, tests, or builds. Use the declared package manager and installed tool versions. A missing script does not mean there is no linter; check for configured tools and CI commands. When no formatter or linter covers applicable files, report the gap explicitly. Set up new tooling only when requested.

3. **Remove slop.** For an authorized implementation or fix cleanup, call the Skill tool with `remove-slop` after establishing scope. Pass the same fixed point and task files, including staged, unstaged, and untracked files. Run it when the scope contains code or prose, and report it as not applicable when it does not. Keep review-only cleanup read-only, so inspect for slop and report it without invoking the editing skill. Include its behavior-preserving code edits and meaning-preserving prose edits in the cleanup diff.

4. **Clean and validate.** Apply the configured formatter and safe lint fixes within the task scope, then run formatter and lint checks in non-mutating mode. Keep discretionary refactors and other semantic edits in implementation or review-fix work. Inspect script definitions before running them; a command named `lint` or `check` may write files. Use check-only commands when fixes cannot be scoped safely. Preserve lint rules and suppression policy; fix the code instead of weakening checks to obtain a pass.

   Run the required typechecks, tests, and builds that cover the change. Prefer supported file or package scopes; use broader checks when configuration, shared code, or repository policy requires them. Run independent read-only checks in parallel when useful. Keep fixes sequential, and avoid repeating a check already covered by an aggregate command. Check for patch whitespace errors with `git diff --check` and `git diff --cached --check`; these supplement the formatter and linter.

5. **Classify failures.** Return non-autofix lint failures and failures from typechecks, tests, or builds to implementation or review-fix work; cleanup does not make semantic edits to clear them. Identify unrelated failures using evidence from the baseline where practical; otherwise report attribution as uncertain. If a check cannot run, record the missing dependency, environment issue, or other concrete blocker. Continue independent checks and report unresolved work. After the calling workflow fixes a failure, rerun the affected cleanup checks against the final code.

6. **Report the final state.** Reinspect the diff, including untracked task files, for accidental changes. Summarize cleanup edits and report each check's command, working directory, scope, and result. Distinguish passing, failing, blocked, unconfigured, and not-applicable checks. Include lint warnings according to the repository's policy. Claim formatting, linting, or other validation passed only when the reported checks cover the final task change. Report partial staging or other coverage gaps, and carry unresolved checks into the commit handoff rather than claiming the change is ready.

Completion criterion: the final task state is accounted for by every required check, with each result reported as passing, failing, blocked, unconfigured, or not applicable, and the cleanup introduced no out-of-scope change.
