# Changelog

All notable changes to Snappedly Skills are recorded here.

## Unreleased

### Added

- Explicitly invoked `retro` skill for session-based recommendations to improve the agent's environment.

### Changed

- `implement-spec` now reads tracker policy explicitly, tracks dependency readiness independently of issue closure, and defines worker base, verification environment, shared-contract, and integration safeguards.
- Setup distinguishes executable-ticket closure from parent-spec closure.
- Validation evidence identifies required tests skipped because their environment is unavailable.
- `pr` honors repository templates, makes visuals optional, repairs its component-tree example, and assesses the reversibility of effects as well as code.

## [0.2.0] - 2026-09-24

### Added

- Five skills: `codebase-cleanup`, `pr`, `technical-writing`, `show-me-your-work`, and `workflow-mapping`.
- A decision-log template and helper for `show-me-your-work`.
- Security policy and private vulnerability reporting guidance.

### Changed

- Renamed `ask-snappedly` to `help-snappedly` and clarified skill selection and setup guidance.
- Expanded implementation, PR, technical-writing, work-log, cleanup, and workflow-mapping guidance.
- Replaced the private all-rights-reserved notice with the PolyForm Strict License 1.0.0 and opened the repository for noncommercial use.
- Clarified the contribution and license summaries in the README.
- `setup-snappedly-skills` now maintains `AGENTS.md` as the root agent-instruction file; removed `CLAUDE.md` from setup and agent-document guidance.

### Removed

- The TypeScript feedback-loop research note.

## [0.1.0] - 2026-09-17

### Added

- Initial private preview of 29 reusable engineering skills.
- Skills organized into `begin`, `direction`, `mainflow`, `misc`, `practices`, `tools`, and `upkeep` groups.
- Structural validation for skill frontmatter, agent metadata, and local links.
- GitHub Actions validation for pull requests and pushes to `main`.
- Repository guidance for installation, contribution, versioning, and release checks.
