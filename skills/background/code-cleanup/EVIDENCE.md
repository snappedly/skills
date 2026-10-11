# Validation evidence and reuse

Record each command, working directory, scope, result, and the content checked. For committed content, use its full SHA. For pre-commit checks, record HEAD plus an immutable patch or content digest covering staged, unstaged, and untracked task content. Preserve the relevant configuration, dependency/tool versions, and environment assumptions in the check record. Build the record from existing Git diffs, blob/tree IDs, and check outputs.

Distinguish command success from coverage: inspect skipped tests and missing prerequisites. A required acceptance test skipped because fixtures, services, or credentials are absent remains unverified, even with a zero exit code. Record the gap and required environment rather than reusing the result as passing acceptance evidence.

After validation, the caller may commit. Verify that the commit contains the checked content, including new files, and bind the evidence to that SHA. A content-preserving commit, cherry-pick, or merge does not require running checks again. Hooks or conflict resolution that change checked inputs invalidate affected results.

Across later commits, reuse a passing result only when its checked files and relevant dependencies, configuration, command, directory, scope, tool versions, and environment assumptions remain unchanged. Record the original validated SHA, current target SHA, and concrete comparison supporting reuse. Consider transitive inputs, not just files named in the command. If coverage or equivalence cannot be established, rerun the affected check. A changed SHA, report timestamp, or evidence label alone does not invalidate a result.

A fix may require a full test/build rerun when it affects inputs to that check. Explain that dependency and rerun the check. When the caller's deadline or execution budget prevents the rerun, record it as blocked. Repository-required CI still runs, but the coordinator need not duplicate equivalent passing CI locally.

## Deferred checks

Use the repository's resource-acquisition timeout, defaulting to five minutes, capped by the caller's remaining time. If the resource remains occupied, mark the check deferred and continue independent work. Check execution uses its own timeout.

Preserve the check record, adding the resource, collision evidence, and resume condition. Use the harness's persistent task state or a caller-owned file outside tracked source and disposable worker worktrees. If persistence is unavailable, return the record for the caller to retain.

Resume only after the resource becomes available or its isolation or locking is fixed. Carry the deferral across cleanup passes and handoffs until then. On resumption, reuse any active check through the harness's task controls and validate current content under the evidence rules above. If the retry also collides, mark the check blocked.

When only deferred checks remain, use the harness's supported continuation mechanism when available, or give the command for manual resumption.
