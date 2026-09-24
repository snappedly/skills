# Worker worktrees

## Before implementation

Each worker verifies its actual branch and base against the coordinator's assigned integration SHA before editing, and returns that base in its report. A fresh worktree starts at the assigned SHA. For resumed work, verify ancestry and account for existing commits rather than requiring HEAD equality. Correct a wrong base only on a clean, task-owned branch; preserve dirty or unrelated work before recreating or repositioning it.

Check whether the worktree can run the ticket's required verification. Ignored fixtures, local databases, generated assets, services, and credentials may be absent. Use the repository's supported environment setup where available. If verification requires a prepared checkout, the coordinator serializes access and safely makes the candidate available there, preserving unrelated work. Record the tested revision and environment. Workers must not concurrently switch or edit a shared checkout, and credentials are not copied without authorization.

Inspect required test results, including skips. Missing prerequisites leave acceptance unverified even when the command exits successfully. Report that gap to the coordinator for environment setup or verification in a suitable checkout.

## Integration

The coordinator integrates completed branches serially against the current integration tip. A worker may synchronize with an assigned tip before returning, but another integration can advance it meanwhile. Recheck ancestry at integration time; use a fast-forward when possible and resolve other integrations through the normal merge workflow. Only one actor mutates a worker branch at a time.

Conflict resolution or changed dependencies can invalidate earlier checks. Apply code-cleanup's evidence rules to the resulting inputs and run affected checks. Record the accepted integration commit before releasing dependent tickets.

Worktrees share some repository state. If hooks or other tooling mutate shared state, such as a common stash used for backups, serialize those operations or use the tool's supported isolation. Separate worktrees alone do not establish safe concurrent hook execution.
