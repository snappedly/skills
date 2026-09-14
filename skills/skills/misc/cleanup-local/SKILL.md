---
name: cleanup-local
description: "Purge verified clean, pushed T3Code worktrees and branches, then update globally installed skills from recorded sources."
disable-model-invocation: true
---

# Cleanup local

Use this only after the user explicitly invokes `cleanup-local`. Invocation authorizes the local purge and global skill updates without another confirmation. Remote branches remain unchanged. Run both phases; if cleanup is blocked, record the reason and continue with skill updates.

## Scope and safety

The default scope is every T3-managed repository represented under `${T3_WORKTREES_ROOT:-$HOME/.t3/worktrees}`, plus the current repository if it is not under that root. A T3 worktree is a registered worktree whose path is under that root and whose directory name starts with `t3code-`, or whose branch name starts with `t3code/`. Keep ordinary local branches and worktrees outside this scope.

Preserve the current worktree unconditionally. Use the local T3 state gate below to protect other active or unsettled chats. Treat a locked worktree, a worktree outside the T3 root, or a worktree whose ownership is unclear as active and preserve it. Never use `rm -rf`, `git worktree remove --force`, or a broad process-kill command.

## Candidate contract

Delete a local branch only when conditions 1, 2, and 5 hold, together with either remote proof in condition 3 or 4:

1. The branch is T3-managed and is not a protected branch (`main`, `master`, `develop`, `dev`, `trunk`, `production`, the remote's default branch, or an explicitly named protected branch).
2. Every worktree linked to the branch is a removable T3 worktree, is not the current worktree, is not locked or prunable, and has no tracked or untracked changes. Check with `git status --porcelain=v1 --untracked-files=all` and inspect for an in-progress merge, rebase, cherry-pick, revert, or bisect. If `git worktree remove` later refuses the path, leave both the path and its branch.
3. After refreshing remote-tracking refs with `git fetch --all --prune`, the branch has a configured remote upstream and its tip object ID exactly equals the upstream tip object ID. An upstream that is another local branch is not proof of a push.
4. As an alternative to condition 3, a branch with a gone remote upstream qualifies when its tip is an ancestor of the freshly fetched remote default branch. If the remote default cannot be identified or fetched, preserve it. A branch with no upstream, a local tip ahead of or diverging from its upstream, or an unverifiable remote is never a candidate.
5. The T3 state gate classifies every matching chat as settled or terminal and finds no active session. Missing or ambiguous T3 state is a preserve condition.

Do not infer that a branch was pushed from its age, its commit message, a pull request, or a matching tree. Only fetch may refresh or prune remote-tracking refs; never delete remote branches. A branch with multiple linked worktrees qualifies only if all of them pass the contract.

## T3 state gate

Use the local T3 projection database at `${T3_STATE_DB:-$HOME/.t3/userdata/state.sqlite}`. Read it with `sqlite3 -readonly` (or Python's standard-library `sqlite3` in read-only/query-only mode) and query only these projection tables:

- `projection_threads`: `thread_id`, `project_id`, `branch`, `worktree_path`, `settled_override`, `settled_at`, `unsettled_at`, `deleted_at`, `archived_at`
- `projection_thread_sessions`: `thread_id`, `status`
- `provider_session_runtime`: `thread_id`, `status`
- `projection_projects`: `project_id`, `workspace_root`

Match a candidate by exact worktree path first. For a local branch with no linked worktree, match its branch name only when the joined project `workspace_root` is the repository root being inspected; this avoids treating an identically named branch in another repository as evidence. A matching chat is **active** when its thread session is `running` or `ready`, or its provider runtime is `running`. A matching chat is **unsettled** when it has `unsettled_at`, an override other than `settled`, or no settled marker while it is not terminal. A matching chat is **settled** when `settled_override = 'settled'` and `settled_at` is present. A matching chat is **terminal** when it has `deleted_at` or `archived_at`, has no unsettled marker, and has no active session.

If any matching chat is active, unsettled, or ambiguous, preserve the branch and worktree. Require at least one matching chat, and require every non-terminal matching chat to be explicitly settled. If the database, tables, or columns are unavailable, preserve the candidate and report that T3 state could not be verified. Do not read message bodies or modify the database.

Only `stopped` and `error` thread-session statuses, and `stopped` provider-runtime status, establish inactivity. A missing row, null status, or any other unrecognized status is ambiguous and preserves the candidate, even if the chat is settled, archived, or deleted.

## Inventory

1. Resolve the current worktree and common Git directory. If the current directory is not in a repository and the T3 root does not exist, report that cleanup has no scope and continue to skill updates.
2. Discover the repositories represented by `.git` files at the worktree-instance level below the T3 root. Resolve each file with Git and group instances by their common Git directory. Record an unresolved `.git` pointer as a stale missing-worktree record and preserve it for separate review; never infer branch or chat state from it. Include the current repository even when it has no T3 worktree under the root.
3. For each repository, refresh remote refs, then use `git worktree list --porcelain` as the source of truth for registered worktrees. Use `git for-each-ref` for local branches and record each branch's upstream, local object ID, upstream object ID, worktree path, lock state, and status.
4. Query the T3 state gate for each T3-managed branch and linked worktree. Classify it as `candidate` or as a specific preserve reason: current, protected, outside scope, locked, detached, dirty, operation in progress, missing worktree, no upstream, ahead/diverged, remote unavailable, gone and unmerged, active chat, unsettled chat, ambiguous chat state, or removal refused.

Do not wait after the inventory. Keep a compact internal record of candidates and preserve reasons so the final report can state what was removed and what was skipped.

Batch the initial T3 query and index its rows by worktree path and repository/branch. Inventory refs and worktrees once per common Git directory, and fetch once per repository. Apply scope and chat exclusions before inspecting worktree contents. Reuse these inventories during classification; retain the immediate checks below before each deletion.

Inventory completion criterion: every discovered `.git` pointer, T3-managed local branch, and matching T3 chat has either a candidate entry or a named preserve reason, and no deletion has occurred before the T3 gate passes.

## Purge and verify

For each candidate, rerun the cheap T3 session/state and Git status/upstream checks immediately before deletion. If a chat becomes active or unsettled, or any Git proof changes, preserve that item and continue with the rest.

1. Remove each linked worktree with `git worktree remove <path>` without `--force`. Do not remove the branch while any linked worktree remains.
2. Delete the local branch only after all of its linked worktrees were removed. For a branch whose local and upstream object IDs still match, `git branch -D -- <branch>` is permitted because the remote branch is the retained copy. For a gone-upstream branch proven merged into the protected default, use `git branch -d -- <branch>`.
3. If either command fails, preserve the remaining local state and record the command and reason. Never substitute a forceful worktree removal or an unverified branch deletion.

After the purge, rerun `git worktree list --porcelain`, the local-branch inventory, and the T3 state query. Verify that the current worktree is intact, removed branches and paths are gone, no active or unsettled chat was removed, and no remote branches were modified. Remote-tracking refs may have been refreshed or pruned by the fetch. Report removed items, preserved items with reasons, and stale missing worktree records that require a separate `git worktree prune` review.

Mutation completion criterion: every candidate is either verified removed or has a recorded failure, the current worktree remains usable, no active or unsettled T3 chat was removed, and no unverified or remote deletion was performed.

## Phase 2: update skills from known sources

Update only globally installed skills whose source is already recorded by the skills CLI. The known-source inventory is the JSON output of:

```bash
npx skills list -g --json
```

Run the canonical non-interactive update for that global inventory:

```bash
npx skills update -g -y
```

This updates all global skills from their recorded sources without a scope prompt. Keep the current project checkout out of scope: do not update project skills, install missing skills, add arbitrary sources, or replace a failed update with a raw Git operation. If the updater exits unsuccessfully, record the command failure and continue to the final report.

Afterward, run `npx skills list -g --json` again and record the before-and-after inventory. Treat a skill being replaced while this skill is running as effective on the next invocation; finish the current run from the already-loaded instructions.

## Report and completion

Report removed items, preserved counts grouped by reason, failures, and the skill updater's result. Keep full inventories available for inspection rather than printing every unchanged entry. Include stale worktree records from the cleanup phase.

The run succeeds when the cleanup phase has verified its postconditions and the global skill updater has completed successfully. If either phase fails, report the run as incomplete with the phase and reason.
