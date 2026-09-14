---
name: code-cleanup
description: "Clean and validate completed changes before commit, including behavior-preserving slop removal where applicable"
---

# Code cleanup

Prepare a coherent task change with mechanical, behavior-preserving cleanup and final evidence from the repository's checks. This skill owns checks and evidence for one state. The calling workflow owns phase transitions, commits, pushes, and deployments.

## Timing and ownership

Run once when an integrated change is ready, before review or commit. Ticket implementers may run targeted tests and typechecking, but they do not run the integrated full suite or production builds independently. `implement-spec` schedules the single integrated cleanup pass and any bounded post-fix rerun. This skill returns evidence; it must not recursively start review, fixes, or another cleanup pass.

After a review fix, rerun only checks affected by the final fix. Reuse prior evidence only when every checked file, dependency, configuration input, command, working directory, and scope has the same content fingerprint. A changed SHA alone is not a reason to rerun, and it is not a reason to pretend that evidence still applies.

## Immutable evidence contract

At the start of every pass, capture:

- `inputSha`, the exact commit being cleaned;
- `scope`, including staged, unstaged, and untracked task paths;
- the baseline or merge-base used for the comparison; and
- the applicable workflow and check configuration.

Cleanup may make behavior-preserving formatting or slop edits. It may inspect a working tree while doing so, but a working-tree revision is not a SHA and cannot be final evidence. After cleanup edits are complete, commit every in-scope change, resolve `outputSha` with `git rev-parse --verify <commit>^{commit}`, and rerun every affected check against that committed SHA. If cleanup made no edits, `outputSha` may equal `inputSha`. Before review or handoff, every in-scope staged, unstaged, and untracked path must be committed or explicitly excluded. Do not report final evidence while relevant mutable content remains outside `outputSha`.

For each check, compute `inputFingerprint` as a SHA-256 of a canonical manifest containing the checked path list and content hashes, dependency manifests and resolved tool versions, configuration files and content hashes, exact command, working directory, and scope selector. Every final result records `validatedSha` as the committed SHA it inspected, `currentTargetSha`, `inputFingerprint`, the path scope, command, working directory, configuration and dependency inputs, and status. If a later committed target reuses the result, also record `reusedFromSha` and why the current target has the same fingerprint. A new target check is required when any checked content, dependency, configuration input, command, working directory, scope, or evidence identity changes, or when the prior evidence was produced from an uncommitted working tree. A changed target SHA alone does not require a rerun.

The target state must not be reviewed while cleanup is mutating it. If another process changes the branch during a pass, stop, mark the affected result stale with both SHAs, and return control to the coordinator. Do not merge or launch reviewers from inside this skill.

## Process

1. **Establish scope.** Read applicable agent instructions and `docs/agents/workflow.md` when present. Inspect `git status --short`, `git diff`, and `git diff --cached`; include untracked task files and the caller's base/merge-base when the task spans commits. Preserve unrelated edits and keep the index unchanged. If no task change is present, report that and stop. Distinguish working-copy validation from staged validation for partially staged files.

2. **Discover the checks.** Read repository scripts, tool configuration, CI, and contribution guidance. Identify formatter and linter check/fix modes, typechecks, tests, and builds, including their working directories and scopes. A missing script does not prove that a file type has no configured tool. Report formatter/linter coverage gaps explicitly and do not install new tooling unless requested.

3. **Remove slop.** For an authorized implementation or fix, call the `remove-slop` skill after scope is fixed when the scope contains code or prose, passing the same SHA, paths, staged/unstaged state, and untracked task files. Keep its behavior-preserving code edits and meaning-preserving prose edits in this cleanup scope. If the scope contains no code or prose, including documentation files with no prose to edit, report `remove-slop: not applicable` and do not launch it. For review-only work, do not edit; inspect and report instead.

4. **Clean and validate.** Apply only scoped formatter and safe lint fixes, then run formatter and lint checks in non-mutating mode. Run the required typechecks, tests, and builds that cover this target. Run independent read-only checks in parallel where useful, but do not duplicate a check already covered by an aggregate command. Include `git diff --check` and `git diff --cached --check` as whitespace checks.

   The integrated pass owns repository-required full-suite tests and production builds when policy requires them. A review-fix pass owns only affected checks unless shared code, dependencies, configuration, the workflow, or repository policy makes a broader check necessary. Explain that reason when broad validation is repeated.

5. **Classify failures and stale evidence.** Return non-autofix lint failures and typecheck, test, or build failures to implementation or fix work; cleanup does not make semantic edits to clear them. Identify unrelated failures using baseline evidence where practical, otherwise mark attribution uncertain. If a check cannot run, record the concrete blocker. Continue independent checks. Compare the current target's `inputFingerprint` with each earlier result. If the target SHA changes but the fingerprint matches, record the original `validatedSha`, current target SHA, and reuse decision. If any fingerprint input changes, invalidate only the affected evidence and identify the exact rerun and reason.

6. **Report the final state.** Reinspect the complete scoped diff, including untracked task files, then confirm that the final in-scope state is committed. Report `inputSha`, committed `outputSha`, `validatedSha`, current target SHA, `inputFingerprint`, path scope, each command and result, and whether each check is passing, failing, blocked, unconfigured, or not applicable. Include warnings, partial staging, coverage gaps, cleanup edits, stale-result dispositions, reused evidence, and rerun reasons. Claim readiness only when the reported evidence covers the final committed target state.

Completion criterion: one coherent target state is fully accounted for by required checks, with each result traceable to an immutable SHA and no out-of-scope change introduced.
