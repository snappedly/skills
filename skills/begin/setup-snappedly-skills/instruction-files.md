# Agent instruction files

`AGENTS.md` stays the canonical root instruction file. This covers the repository's other agent instruction files (`CLAUDE.md`, `.claude/CLAUDE.md`, and nested instruction files) and an `AGENTS.md` symlink.

## Propose

If shared project rules live only in `CLAUDE.md`, include their preservation in the `AGENTS.md` proposal. Keep nested rules at their existing directory scope. Resolve conflicts explicitly and check tool-specific imports rather than assuming every agent expands them. Retain Claude-specific rules in their applicable configuration or a compatibility file. Note local or ancestor instructions that affect loading, and keep their private preferences out of shared files. When Claude Code is used, check its installed version and instruction-loading mode before proposing removal or a compatibility bridge.

Removing `CLAUDE.md` is a separate, requested migration. Before proposing it, account for every unique instruction and verify that each agent the team uses loads the intended `AGENTS.md`. Check other project or ancestor Claude instruction files and hooks that can affect loading. If direct loading is unavailable or unverified, retain a `CLAUDE.md` bridge containing `@AGENTS.md`, plus any necessary Claude-specific rules.

Preserve existing symlinks and their targets unless their migration is explicitly in scope. Routine setup leaves global agent settings and `.claude/` configuration as they are.

## Write

Apply agreed instruction-file moves or bridges without losing unique rules or changing nested scope. A `CLAUDE.md` import is relative to that file; verify its target and keep imports free of cycles. Before an agreed removal, verify the resulting instructions load in the team's relevant agents. If that verification is unavailable, retain compatibility and report the gap.
