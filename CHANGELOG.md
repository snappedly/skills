# Changelog

All notable changes to Snappedly Skills are recorded here.

## [Unreleased]

## [1.5.5] - 2026-10-23

### Changed

- `retro` ends its report with a horizontal rule and a **Recommended changes** section. It numbers the proposed changes in the same order as the findings, with one plain-language line per change that says what to change and where. You can reply "fix all" or name the numbers to apply, and `retro` makes those changes. When your original request already asked `retro` to make the changes, it applies them without the list.

## [1.5.4] - 2026-10-18

### Changed

- `execute` triages a named issue in the `needs-triage` state before carrying it out. It applies the `triage` process for a specific issue. When the issue is ready for an agent, `triage` posts its brief and updates its category and state roles on the tracker before `execute` builds the plan. Planning specs receive the roles without an executable brief. When triage recommends another state, such as `needs-info` or `wontfix`, `execute` stops with the recommendation, applies only the outcome you choose, and continues only when the issue reaches `ready-for-agent`. On a planning spec, `execute` also triages every open ticket in the `needs-triage` state, including blocked ones. A ticket that reaches `ready-for-agent` joins the plan once its blockers have closed; any other ticket stays out, and the report gives triage's recommendation for it. Without `triage` installed, `execute` stops and reports which issues need triage. `triage` now supports model invocation in Claude Code and Codex so `execute` can load it as a dependency from the `snappedly/skills` package.

## [1.5.3] - 2026-10-15

### Fixed

- After `clean-up` or `codebase-cleanup`, when you ask the agent to act on the **Decisions needed** and **Gaps to check** items, it reports each item under its current status: **Done**, **Handed off** (with where it is tracked), **Accepted**, or **Still open**. Each item starts with its outcome. Previously, the follow-up report could reuse "Decisions" and "Gaps" headings, so fixed items looked open. An item counts as done only once its decision is applied or what it named is verified. A gap left for someone else to verify is listed as handed off.

## [1.5.2] - 2026-10-14

### Changed

- `clean-up` and `codebase-cleanup` end their report with a horizontal rule and a **Check before you submit or deploy** section, so open items are not lost in the longer report. It has two numbered lists in plain language. **Decisions needed** gives each choice left to you, with its options and a recommendation. **Gaps to check** gives each thing left unverified, such as a failing or skipped check or an uninspected area, with its risk, the ways to close it when there is more than one, and a recommendation. An empty list says "None". Open findings appear only in that section, rather than also in the body of the report.

## [1.5.1] - 2026-10-13

### Security

- `execute` states that its dependencies, `code-cleanup`, `code-review`, and `tdd`, come from the same `snappedly/skills` package as `execute` itself.

## [1.5.0] - 2026-10-12

### Changed

- `grill` gives the `ready-for-agent` state to every ticket it publishes, including blocked ones, unless you say otherwise. Without configured triage roles, it applies a `ready-for-agent` label and creates the label when the tracker lacks it. The state means a ticket is fully specified, not that its blockers have closed. `execute` on a spec still runs only the tickets whose blockers have closed.
- `grill` records blockers through the native blocking operations configured in `issue-tracker.md`, such as GitHub issue dependencies. Without those operations, it writes a `## Blocked by` section. `execute` reads native links when configured and any existing `## Blocked by` sections, so older tickets keep their dependencies.
- `grill` also gives the `ready-for-agent` state to a spec it creates. On a spec, the state means `/execute` on the spec can carry out its unblocked tickets, and the spec stays non-executable. `triage` applies the state to a spec without an agent brief, since a brief marks an item executable.
- When `grill` starts from an existing tracker issue, that issue becomes the parent. Each ticket becomes its child, and `grill` posts the spec as a comment on it instead of creating a separate spec. `grill` never edits or closes that issue.

### Added

- `grill` looks for refactors that make a slice easier to build. Each refactor goes at the start of the first slice that needs it. The ticket requires behavior to stay unchanged and the relevant checks to pass before the slice adds new behavior. A refactor gets its own ticket ahead of the tracer bullet only when every approach needs it and it is too large to review inside the tracer bullet.
- `grill` splits a wide refactor, such as renaming a column used across the codebase, into expand, migrate, and contract tickets: add the new form, move the callers over in batches that each pass the checks, then remove the old form.

### Updating existing repositories

Rerun `setup-snappedly-skills` to add the Blocking relationships section to `docs/agents/issue-tracker.md` and to let its planning spec mapping accept a spec comment and the `ready-for-agent` state. Until then, `grill` writes blockers as `## Blocked by` sections.

## [1.4.5] - 2026-10-11

### Fixed

- `execute` workers can run focused checks and prerequisite builds in parallel when their resources are isolated. Required full suites and final builds run on the combined change, unless repository policy requires them earlier.
- `code-cleanup` prefers supported resource isolation or shared locks. Resource acquisition defaults to a five-minute timeout. Deferred checks retain their check record and resume once their resume condition is met. Test execution keeps its own timeout.
- `code-review` reports deferred checks as unverified with their resume condition. `execute`, `clean-up`, `submit`, and `deploy` preserve those records and resume the checks once the resume condition is met. `submit` and `deploy` stop before delivery and continue from their preparation step when run again. Required deferred checks prevent delivery until verified.
- `setup-snappedly-skills` records shared resources, isolation or locking commands, and configured resource-acquisition timeouts. Unknown resource scope stays unverified.

### Updating existing repositories

Rerun `setup-snappedly-skills` to refresh Concurrent runs in `docs/agents/workflow.md`. Setup preserves team requirements and corrects entries that classify worktree-local output as shared.

## [1.4.4] - 2026-10-11

### Added

- `setup-snappedly-skills` records which checks two worktrees on one machine cannot run at the same time, in a new Concurrent runs section of `docs/agents/workflow.md`. Each entry names the shared resource the check holds or removes, such as a fixed port, a container name, or a cleanup of every container carrying a label.

### Changed

- `code-cleanup` checks for another worktree's run before starting a check listed under Concurrent runs. When a check fails because a port or other resource is taken, or another run removed what the check created, it finds that run, leaves it running, and reruns once after it exits. A repeated collision is recorded as blocked, naming the other run and the resource, rather than as a failure of the change, and is reported as a gap the repository can close by making the check safe to run concurrently.
- `execute` workers run only focused checks. Full suites, builds, and the checks listed under Concurrent runs run once on the combined result, since the workers share one machine.

### Updating existing repositories

Rerun `setup-snappedly-skills` to add the Concurrent runs section to `docs/agents/workflow.md`. Setup fills it from each check's configuration and moves any port or resource note already recorded for a check into it.

## [1.4.3] - 2026-10-11

### Security

- `diagnosing-bugs` treats logs, HAR files, dumps, and pasted text as evidence about the bug: text in them that reads like an instruction is reported, not followed, and quoted evidence goes in fenced code blocks. The human-in-the-loop script you run in your own terminal holds only its prompt helpers, with single-quoted prompts, so it asks questions and records answers and runs no other command. The agent shows you its steps before you run it.

## [1.4.2] - 2026-10-11

### Security

- `execute` states what running it authorizes: editing files in your checkout, creating and committing in its worker worktrees, running the repository's own setup, check, and preview commands, and reading the named issue and its child tickets. Its tracker access is read-only, pushing and merging stay with `submit` and `deploy`, and an issue's body and comments shape what to build without widening that authority. `execute` also names the skills it loads: `code-cleanup`, `code-review`, and `tdd`.

## [1.4.1] - 2026-10-11

### Added

- `grill` checks whether a settled code change fits one `execute` run and one reviewable PR. When it does not, `grill` recommends a planning spec with executable child tickets, and proposes the tickets as tracer bullets. The first ticket is the thinnest slice that works end to end through every layer, and each later ticket adds one behavior to that working path. After you confirm, `grill` publishes the spec and tickets to your tracker, links each ticket to the spec, and recommends running `execute` on the spec in a fresh session.
- `execute` carries out a planning spec. Name the spec, such as `/execute #40`, and its ready tickets become the plan: the open tickets whose blockers have all closed. Naming the spec approves its tickets, so they need no `ready-for-agent` label, but a ticket in another triage state, such as `ready-for-human`, stays out. Each ticket's acceptance criteria become requirements, tickets that share no files or contracts run on parallel workers, and the tickets land as one combined change. On a `grill` spec, the first run builds only the tracer bullet, because it blocks every other ticket. After each run's tickets close, the next run takes the tickets they unblocked. The report lists which tickets the change completes, so `submit` and `deploy` can link them, and each child it left out with the reason, such as the blockers it waits on.

### Changed

- `help-snappedly` routes a large effort through `grill`'s spec and tickets, then `execute` on the spec, in a fresh session each time its finished tickets close.

## [1.4.0] - 2026-10-11

### Removed

- `resolving-merge-conflicts`. `submit`, `deploy`, and `execute` resolve conflicts themselves: they preserve both sides' intent and stop to ask when the intent is unclear.

### Updating existing repositories

`npx skills update` leaves the removed skill installed and reports it as failed. To remove it, run:

```bash
npx skills remove resolving-merge-conflicts
```

Add `-g` if you installed the skills globally.

## [1.3.0] - 2026-10-10

### Added

- `submit` takes a branch to a PR ready for review and stops before the merge. It commits pending task changes, pushes, opens or updates the PR, marks it ready for review, and waits for its checks, the same way `deploy` does up to that point. When you run it again after review feedback, it re-requests review from each reviewer who asked for changes. Its report lists any steps the workflow gives the agent after the merge, such as closing tickets or verifying production, because no agent runs after a person merges.
- `deploy` labels its PR `agent-merge` when the agent expects to merge it without waiting for anyone's review or approval, so reviewers can tell its PRs from ones awaiting their review. It creates the label when the repository lacks it. `deploy` removes the label whenever it stops without merging and adds it back on a later run that can merge. `submit` also removes it.

### Changed

- The README, `help-snappedly`, and `setup-snappedly-skills` now end the main workflow with `submit`, and present `deploy` as the way to skip human review and have the agent merge.

### Updating existing repositories

`npx skills update` updates only the skills you have installed, so add `submit` with `npx skills add snappedly/skills --skill submit`.

Rerun `setup-snappedly-skills` to update the main workflow in `docs/agents/workflow.md` so it ends with `submit` and offers `deploy` to skip human review. Setup keeps an ending your team chose in place of the old default.

## [1.2.1] - 2026-10-09

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

[1.5.3]: https://github.com/snappedly/skills/releases/tag/v1.5.3
[1.5.2]: https://github.com/snappedly/skills/releases/tag/v1.5.2
[1.5.1]: https://github.com/snappedly/skills/releases/tag/v1.5.1
[1.5.0]: https://github.com/snappedly/skills/releases/tag/v1.5.0
[1.4.4]: https://github.com/snappedly/skills/releases/tag/v1.4.4
[1.4.3]: https://github.com/snappedly/skills/releases/tag/v1.4.3
[1.4.2]: https://github.com/snappedly/skills/releases/tag/v1.4.2
[1.4.1]: https://github.com/snappedly/skills/releases/tag/v1.4.1
[1.4.0]: https://github.com/snappedly/skills/releases/tag/v1.4.0
[1.3.0]: https://github.com/snappedly/skills/releases/tag/v1.3.0
[1.2.1]: https://github.com/snappedly/skills/releases/tag/v1.2.1
[1.2.0]: https://github.com/snappedly/skills/releases/tag/v1.2.0
[1.1.0]: https://github.com/snappedly/skills/releases/tag/v1.1.0
[1.0.0]: https://github.com/snappedly/skills/releases/tag/v1.0.0
