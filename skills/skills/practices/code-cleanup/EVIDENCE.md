# Validation evidence and reuse


Record each command, working directory, scope, result, and the content checked. For committed content, use its full SHA. For pre-commit checks, record HEAD plus an immutable patch or content digest covering staged, unstaged, and untracked task content. Preserve the relevant configuration, dependency/tool versions, and environment assumptions in the check record. Use existing Git diffs, blob/tree IDs, or check outputs; do not build a custom manifest or cache framework.

After validation, the caller may commit. Verify that the commit contains the checked content, including new files, and bind the evidence to that SHA. A content-preserving commit, cherry-pick, or merge does not require running checks again. Hooks or conflict resolution that change checked inputs invalidate affected results.

Across later commits, reuse a passing result only when its checked files and relevant dependencies, configuration, command, directory, scope, tool versions, and environment assumptions remain unchanged. Record the original validated SHA, current target SHA, and concrete comparison supporting reuse. Consider transitive inputs, not just files named in the command. If coverage or equivalence cannot be established, rerun the affected check. A changed SHA, report timestamp, or evidence label alone does not invalidate a result.

A fix may require a full test/build rerun when it affects inputs to that check. Explain that dependency; never reuse evidence merely to meet the budget. Repository-required CI still runs, but the coordinator need not duplicate equivalent passing CI locally.

