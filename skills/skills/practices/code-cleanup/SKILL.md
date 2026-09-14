---
name: code-cleanup
description: "Clean and validate completed changes before commit, including behavior-preserving slop removal where applicable"
---

# Code cleanup

Prepare a coherent task change with mechanical, behavior-preserving cleanup and final evidence from the repository's checks. This skill owns checks and evidence for one state. The calling workflow owns phase transitions, commits, pushes, and deployments.

## Timing and ownership

Run once when an integrated change is ready, before review or commit. Ticket implementers may run targeted tests and typechecking, but they do not run the integrated full suite or production builds independently. `implement-spec` schedules the single integrated cleanup pass and any bounded post-fix rerun. This skill returns evidence; it must not recursively start review, fixes, or another cleanup pass.

After a review fix, rerun only checks affected by the final fix. Reuse prior evidence only when every checked file, dependency, configuration input, command, working directory, and scope is unchanged, and the evidence is keyed to the same target SHA. A changed SHA is not a reason to pretend that evidence still applies.

## Immutable evidence contract

At the start of every pass, capture:

- `inputSha`, the exact commit being cleaned;
- `scope`, including staged, unstaged, and untracked task paths;
- the baseline or merge-base used for the comparison; and
- the applicable workflow and check configuration.

Cleanup may make behavior-preserving formatting or slop edits. If it does, finish those edits before validation and report `outputSha`, the exact commit or working-tree revision validated. Every result must name the SHA it actually inspected, the path scope, command, working directory, configuration/dependency inputs, and status. A result without this identity is incomplete.

The target state must not be reviewed while cleanup is mutating it. If another process changes the branch during a pass, stop, mark the affected result stale with both SHAs, and return control to the coordinator. Do not merge or launch reviewers from inside this skill.

## Process

1. **Establish scope.** Read applicable agent instructions and `docs/agents/workflow.md` when present. Inspect `git status --short`, `git diff`, and `git diff --cached`; include untracked task files and the caller's base/merge-base when the task spans commits. Preserve unrelated edits and keep the index unchanged. If no task change is present, report that and stop. Distinguish working-copy validation from staged validation for partially staged files.

2. **Discover the checks.** Read repository scripts, tool configuration, CI, and contribution guidance. Identify formatter and linter check/fix modes, typechecks, tests, and builds, including their working directories and scopes. A missing script does not prove that a file type has no configured tool. Report formatter/linter coverage gaps explicitly and do not install new tooling unless requested.

3. **Remove slop.** For an authorized implementation or fix, call the `remove-slop` skill after scope is fixed, passing the same SHA, paths, staged/unstaged state, and untracked task files. Keep its behavior-preserving code edits and meaning-preserving prose edits in this cleanup scope. For review-only work, do not edit; inspect and report instead.

4. **Clean and validate.** Apply only scoped formatter and safe lint fixes, then run formatter and lint checks in non-mutating mode. Run the required typechecks, tests, and builds that cover this target. Run independent read-only checks in parallel where useful, but do not duplicate a check already covered by an aggregate command. Include `git diff --check` and `git diff --cached --check` as whitespace checks.

   The integrated pass owns repository-required full-suite tests and production builds when policy requires them. A review-fix pass owns only affected checks unless shared code, dependencies, configuration, the workflow, or repository policy makes a broader check necessary. Explain that reason when broad validation is repeated.

5. **Classify failures and stale evidence.** Return non-autofix lint failures and typecheck, test, or build failures to implementation or fix work; cleanup does not make semantic edits to clear them. Identify unrelated failures using baseline evidence where practical, otherwise mark attribution uncertain. If a check cannot run, record the concrete blocker. Continue independent checks. If the target SHA, files, dependencies, configuration, command, or scope changes, invalidate only the affected evidence and identify the exact rerun needed.

6. **Report the final state.** Reinspect the complete scoped diff, including untracked task files. Report `inputSha`, `outputSha`, path scope, each command and result, and whether each check is passing, failing, blocked, unconfigured, or not applicable. Include warnings, partial staging, coverage gaps, cleanup edits, and stale-result dispositions. Claim readiness only when the reported evidence covers the final target state.

Completion criterion: one coherent target state is fully accounted for by required checks, with each result traceable to an immutable SHA and no out-of-scope change introduced.
