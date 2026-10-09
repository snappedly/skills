# Agent instruction files

`AGENTS.md` is the canonical instruction file at each directory scope. This covers the repository's `CLAUDE.md` files (`CLAUDE.md` or `.claude/CLAUDE.md`, at the root or in a subdirectory), other nested instruction files, and an `AGENTS.md` symlink. Setup recommends retiring each repository `CLAUDE.md` once `AGENTS.md` carries its rules.

## Claude Code loading

Claude Code v2.1.277 and later reads `AGENTS.md` directly, but only when no `CLAUDE.md`, `.claude/CLAUDE.md`, or `CLAUDE.local.md` exists in the working directory or any directory above it. A subdirectory's `AGENTS.md` loads only when that subdirectory has none of the three. Where one exists, Claude Code reads the `CLAUDE.md` files instead, so a `CLAUDE.md` that does not import `AGENTS.md` hides it from Claude, `## Agent skills` block included. `~/.claude/CLAUDE.md`, a managed `CLAUDE.md`, and `.claude/rules/` files keep loading alongside `AGENTS.md`.

Direct loading is unavailable on earlier versions, when **Project instructions** in `/config` is `claude-md` or `managed-only`, and when the built-in plugin that reads `AGENTS.md` is disabled. Before v2.1.281, some Amazon Bedrock and telemetry-disabled sessions could not load it either. `InstructionsLoaded` hooks do not fire for an `AGENTS.md` read directly.

## Propose

Account for every instruction in each repository `CLAUDE.md` against the `AGENTS.md` at the same scope; a `.claude/CLAUDE.md` maps to the `AGENTS.md` beside its `.claude/` directory. Give each instruction one destination:

- **Already in `AGENTS.md`**: nothing to move.
- **Shared project rule or context**: the `AGENTS.md` at the same directory scope, creating a nested `AGENTS.md` for a nested rule.
- **Conflict with `AGENTS.md`**: ask which rule holds, and keep the answer in `AGENTS.md`.
- **Claude-specific rule**, such as one naming plan mode, a Claude Code hook, or a Claude-only subagent: a `.claude/rules/` file, with `paths` frontmatter matching its directory when it came from a nested file.
- **`@path` import**: other agents leave the import unexpanded, so inline short imported content, or replace the import with a plain pointer that states when to read the file.
- **Loader workaround**, such as `@AGENTS.md`, a sentence telling the agent to read `AGENTS.md`, or a symlink to `AGENTS.md`: nothing to move.
- **Stale instruction**, such as a command or path the repository no longer has: drop it only on repository evidence, and flag it in the proposal. When relevance is uncertain, move it and flag the uncertainty.

Recommend removing each `CLAUDE.md` whose instructions all have a destination, provided Claude Code reads `AGENTS.md` directly for the team. Check the local `claude --version` and **Project instructions** setting, and ask the user which versions, providers, and settings their teammates use. Where direct loading is unavailable or unverified, recommend a bridge instead: a `CLAUDE.md` holding only `@AGENTS.md` and a block-level HTML comment recording why it remains. Retire root and nested `CLAUDE.md` files together, because one left in a subdirectory hides the root `AGENTS.md` from sessions started there.

When `AGENTS.md` is a symlink to `CLAUDE.md`, the migration replaces the symlink with a regular `AGENTS.md` holding the content. Preserve other symlinks and their targets. Propose removing a project `SessionStart` hook that prints `AGENTS.md`, since direct loading makes its output a second copy. Keep a bridge when the team relies on `InstructionsLoaded` hooks firing for the project instructions.

`CLAUDE.local.md` files and `CLAUDE.md` files above the repository root are private and outside the migration, but they also hide `AGENTS.md`. Report each one found, and tell its owner to move its content to `~/.claude/CLAUDE.md` or `~/.claude/rules/`, or set **Project instructions** to `claude-md-and-agents-md`.

When the user declines a removal, keep that `CLAUDE.md` with `@AGENTS.md` as its first line, so Claude Code still loads `AGENTS.md`, and record the reason in a block-level HTML comment in the file. A repeat run proposes the removal again only when the recorded reason no longer holds. Outside this migration, setup leaves global agent settings and `.claude/` configuration as they are.

## Write

Write each instruction to its confirmed destination before removing or reducing its source, keeping its directory scope. A `CLAUDE.md` import is relative to that file; verify its target and keep imports free of cycles. Update repository references to a removed `CLAUDE.md`, such as links in docs, scripts, or CI, to the file that now holds the content.

Done when every instruction from each removed or reduced `CLAUDE.md` is in its destination or reported as dropped, and each remaining `CLAUDE.md` imports its sibling `AGENTS.md` and records why it remains.
