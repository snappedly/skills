# Changelog

All notable changes to Snappedly Skills are recorded here.

## [Unreleased]

### Added

- `setup-snappedly-skills` recommends protecting the base branch so every change arrives through a merged PR. The rule blocks direct pushes and force pushes for everyone, administrators included, and requires no approving review, so agents can still merge PRs. Setup applies it through the code host's API when it has admin access, or gives you the settings to apply, then reads the rule back and records it in `docs/agents/code-host.md`.

### Changed

- `setup-snappedly-skills` recommends retiring each repository `CLAUDE.md`. Claude Code reads `AGENTS.md` only when no `CLAUDE.md` exists, so a leftover `CLAUDE.md` hid the `AGENTS.md` that setup writes. Setup moves each rule `AGENTS.md` lacks into the `AGENTS.md` at the same directory, puts Claude-specific rules in `.claude/rules/`, and asks about conflicting rules. When a teammate's Claude Code cannot read `AGENTS.md` directly, setup proposes a `CLAUDE.md` that only imports `AGENTS.md` instead.

### Updating existing repositories

Rerun `setup-snappedly-skills` to review base branch protection and migrate an existing `CLAUDE.md`. Setup keeps existing branch rules, flags any that would block an agent merge, and records a declined rule with its reason so later runs do not ask again.

For `CLAUDE.md`, setup shows where each rule goes and removes the file only when you agree. If you keep it, setup adds an `AGENTS.md` import and records your reason in the file so later runs do not ask again while it holds.

## [1.2.0] - 2026-10-09

### Added

- `deploy` supports invocation approval. When the workflow records it, the approver's instruction to merge approves merging what their checkout holds, including a merge that deploys to production. `deploy` is the usual form of that instruction, and the same run continues through close-out; a direct instruction in chat merges without `deploy`'s checks and close-out. `deploy` merges only under the approver's code host account. It asks before merging only when content from outside the checkout entered the delivery, such as commits pushed from elsewhere or merge conflicts it resolved. The approver can then let it merge, or merge on the code host and say so.
- `deploy` verifies production after the merge when the workflow assigns that to the agent. It waits up to 15 minutes for the release of the merged commit and reports verification as pending when the release starts later.

### Fixed

- After a person merges a PR, running `deploy` again on its branch, or naming the PR, verifies the merge, closes out tickets and the parent spec, and verifies production. It previously reported an empty batch and stopped.
- `deploy` preserves a merged PR's remote branch when its tip has changed and makes deletion conditional on the original merged head, including when close-out resumes later.
- Production verification requires the merged commit to remain deployed while its checks run, so an earlier release cannot satisfy ticket closure after a rollback.
- `setup-snappedly-skills` requires every agent step in the workflow to have something that starts it, such as a merge under invocation approval or the merger running `deploy` again, so no agent step waits on an event the agent never sees.
- `setup-snappedly-skills` replaces the older template's instruction that `deploy` ends at merge with the close-out boundary, preserving the repository's release actors and approval gates.

### Security

- `deploy` stops before any PR merge that would deploy to production when the workflow records neither a deployment approval gate nor invocation approval. It previously checked this only in repositories without a workflow file.

### Updating existing repositories

After updating the skills, rerun `setup-snappedly-skills`. Until you do, `deploy` stops before a PR merge that would deploy to production without a recorded deployment approval gate or invocation approval.

Setup proposes invocation approval in these cases:

- A person merges, and nothing starts the agent steps after the merge.
- The agent merges after an approval your code host cannot record.
- An agent merge would deploy to production without a deployment approval gate.

It applies the change only when you agree, and then also records how to check which code host account `deploy` acts under. If you decline, setup asks you to resolve the case another way, records what starts each agent step after the merge, and does not propose it again. New setups recommend that `deploy` merges when you run it, using invocation approval when the merge deploys to production. Setup also adds a Verify production row to the workflow.

## [1.1.0] - 2026-10-08

### Changed

- `clean-up` leaves edits unstaged and uncommitted on the current branch and shows what it changed, with check results and review findings. Committing requires an explicit request or `deploy`.
- `deploy` commits the task's pending changes, cleanup's edits included, before delivery, delivers the existing commit when none remain, and creates the task branch when you start on the base or default branch, which `clean-up` no longer does. Setup migrates existing workflow and agent instructions to this handoff and keeps delivery approval rules.

### Fixed

- GitHub issue discovery fetches every page before filtering and counting triage queues. Existing repositories receive the corrected operation when setup runs again.
- `deploy` follows configured local, branch-only, and integration-branch delivery without requiring a hosted pull request.
- `writing-for-agents` documents both Claude Code and Codex invocation settings and keeps them aligned.
- Shared-reference guidance keeps distributed skill dependencies inside installed packages while allowing repository-owned context outside them.
- The diagnostic reproduction script prints the complete capture header and starts the first answer on its own line.

### Updating existing repositories

After updating the skills, rerun `setup-snappedly-skills` to refresh GitHub issue discovery in `docs/agents/issue-tracker.md` and migrate active workflow and agent instructions to the handoff from cleanup to deploy. Existing tracker destinations, triage filters, commit checks, and delivery approval rules are preserved.

## [1.0.0] - 2026-10-08

The first public release of Snappedly Skills.

### Added

- 26 skills in six groups:
  - Begin: `help-snappedly` and `setup-snappedly-skills`.
  - Direction: `prototype` and `research`.
  - Mainflow: `grill`, `execute`, `clean-up`, and `deploy`.
  - Tools: `build-local`, `retro`, `wait-what`, and `workflow-mapping`.
  - Upkeep: `codebase-cleanup`, `diagnosing-bugs`, `improve-codebase-architecture`, `resolving-merge-conflicts`, and `triage`.
  - Background: `code-cleanup`, `code-review`, `codebase-design`, `domain-modeling`, `pr`, `remove-slop`, `tdd`, `technical-writing`, and `writing-for-agents`.
- The main workflow: `grill` settles a plan, `execute` carries it out or works from an issue you name, `clean-up` checks and commits the result, and `deploy` opens the pull request and merges it once its checks pass.
- `setup-snappedly-skills` records your code host, work tracker, team workflow, domain docs, and frontend conventions under `docs/agents/`, and the other skills read them from there.
- The MIT License. Each skill folder carries a `LICENSE.txt`, so installed copies keep their copyright notices, and `THIRD_PARTY_NOTICES.md` credits the projects the skills adapt.
- Validation of skill frontmatter, Codex metadata, license files, local links, and release notes, run in CI on Python 3.9 and 3.12.
- A code of conduct, a security policy, issue forms, and [GitHub Discussions](https://github.com/snappedly/skills/discussions) for questions and ideas.

### Upgrading from a preview release

Preview releases shipped skills that 1.0.0 does not include. `npx skills update` reports them as failed and leaves them installed. To remove them, run:

```bash
npx skills remove ask-snappedly cleanup-local deliver deslop frontend-design frontend-guidelines grill-me grill-with-docs handoff implement implement-spec prevent-slop ship show-me-your-work teach to-spec to-tickets wayfinder wizard wrap-up
```

The command skips any skill you don't have. Add `-g` if you installed the skills globally. Then rerun `/setup-snappedly-skills` in each project. It updates references to renamed skills and proposes removing configuration that only the removed skills read.

[1.2.0]: https://github.com/snappedly/skills/releases/tag/v1.2.0
[1.1.0]: https://github.com/snappedly/skills/releases/tag/v1.1.0
[1.0.0]: https://github.com/snappedly/skills/releases/tag/v1.0.0
