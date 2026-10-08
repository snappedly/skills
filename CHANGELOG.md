# Changelog

All notable changes to Snappedly Skills are recorded here.

## [Unreleased]

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

[1.1.0]: https://github.com/snappedly/skills/releases/tag/v1.1.0
[1.0.0]: https://github.com/snappedly/skills/releases/tag/v1.0.0
