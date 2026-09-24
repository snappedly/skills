---
name: setup-snappedly-skills
description: "Configure a GitHub or GitLab repository for Snappedly skills, including tracker, workflow, domain and frontend docs, and root agent instructions."
disable-model-invocation: true
---

# Setup Snappedly skills

Create the per-repo configuration that Snappedly skills read. This is a prompt-driven setup: inspect the repo, summarize what you found, ask for the decisions that affect the team, show drafts, then write.

This process requires a usable connection to a GitHub or GitLab repository. A local checkout without either provider connection cannot be configured by this skill.

Use `AGENTS.md` as the canonical root instruction file. Treat references to `agent.md` as that file.

The setup records six concerns:

- Work tracker: where work items and specs live, and how the tracker is operated.
- Team workflow: how work moves from clarification through implementation, review, merge, production approval, deployment, verification, and handoff, including the repository's feedback-loop contract.
- Triage labels: the tracker strings that represent the canonical triage roles, when a triage skill is installed.
- Domain docs: where shared vocabulary and architectural decisions live.
- Frontend conventions: the design system, tokens, and UI directories the design and audit skills read, when the repo has a user interface.
- Agent instructions: concise reporting and project configuration in `AGENTS.md`.

## Process

### 1. Explore

Read the repo before proposing configuration. Do not infer conventions from the remote alone.

- `git remote -v` and `.git/config`: identify the host and repository.
- `AGENTS.md` at the repo root: inspect existing reporting rules, any `## Agent skills` section, and whether the path is a symlink.
- `CONTRIBUTING.md`, `README.md`, and other process docs: find existing team rules that the Snappedly workflow must preserve.
- `docs/agents/`: check for configuration written by an earlier run, including `issue-tracker.md`, `workflow.md`, `triage-labels.md`, `domain.md`, and `frontend.md`.
- `CONTEXT.md` and `CONTEXT-MAP.md` at the repo root, plus `docs/adr/` and any context-scoped ADR directories.
- Git provider connection: confirm that the remote points to GitHub or GitLab and that the matching CLI connection is available (`gh auth status` or `glab auth status`).
- An installed `triage` skill: this decides whether the triage-label section applies.
- Frontend signals: a component library or design system dependency, a Tailwind, theme, or design-token configuration, a global stylesheet, a `components/`, `app/`, or `pages/` tree, a Storybook setup. These decide whether the frontend section applies.
- Monorepo signals: `pnpm-workspace.yaml`, a `workspaces` field in `package.json`, or a populated `packages/*` tree with its own `src/`.
- Feedback-loop signals: the package manager and lockfile, package scripts, TypeScript configuration, test runner, formatter/linter configuration, Git hooks, CI workflows, and any configured development or preview server.

Completion criterion: you have a file-by-file inventory, know what the root instruction file contains, know whether the triage, frontend, and multi-context choices apply, have mapped the existing feedback-loop surfaces, and have confirmed a usable GitHub or GitLab connection.

### 2. Align

Present the findings before asking questions. Take one section at a time. Lead with the recommended answer so the user can accept it briefly. Explain a choice only when it changes the resulting workflow.

#### Section A: Git provider and work tracker

The other skills read and publish work through the connected Git provider. Accept only the host detected from `git remote -v` when it is one of these:

- GitHub: use GitHub Issues and the `gh` CLI.
- GitLab: use GitLab Issues and the `glab` CLI.

If the remote is absent, points to another provider, or the matching GitHub/GitLab connection is unavailable, stop setup before drafting or writing files. Prompt the user:

> This process requires a GitHub or GitLab repository. Please share the repository or create and connect a new GitHub or GitLab repository, then run `/setup-snappedly-skills` again.

Resume only after the repo has a GitHub or GitLab remote and a usable provider connection. Do not substitute local files or another tracker.

Record the selected provider in `docs/agents/issue-tracker.md`. Keep the `PRs as a request surface` setting off unless the user explicitly opts in.

#### Section B: Team workflow

Read existing process documentation and feedback-loop surfaces first. Preserve its rules and ask the user whether the default Snappedly flow fits:

For small, clear requests: `edit -> focused verification -> local review`.

For planned multi-session work: `clarify -> specify -> ticket -> implement -> code-cleanup -> code-review -> handoff`.

Capture the source of truth and the point at which implementation may start. A clear user request can be the brief for a small change unless the team requires a tracker issue. Ticketed `/implement` work uses an executable issue or brief; planning specs and wayfinder decision tickets do not qualify. `/implement-spec` is the explicit whole-spec path. Record checks with explicit applicability for presentation edits, local logic changes, and cross-cutting or release work. Full tests and production/deployment builds are not universal defaults. Record when local review is sufficient and when independent axes are required, the allowed disposition for each kind of finding, and the information a handoff must contain. Require cleanup and applicable verification before commit. Small changes can perform these steps and local review inline; separate skill invocations and reports are optional. After review fixes, rerun only affected checks and review the changed scope.

Record a feedback-loop contract in `docs/agents/workflow.md`: the formatter/autofix command, the fastest reliable static check, the focused test command and scope, broader suite/build/release checks, and the local, agent, CI, and preview adapters that enforce them. Use the repository's existing package manager and scripts. If a surface is absent, record `not configured` or `not applicable` and explain the trigger for adding it. Do not install a test runner, formatter, linter, hook, or CI workflow merely because the repository uses TypeScript; adding tooling requires an explicit opt-in.

Use the release policy in [workflow.md](workflow.md) as the default and ask only about differences. Record:

- The base branch, pull or merge request requirements, merge strategy, separate closure points for executable tickets and their parent spec, and whether a preview deployment may run before production approval.
- How the release system identifies the production candidate and prevents an unapproved candidate from deploying. If a merge automatically deploys to production, require an approval gate in the deployment system before agent-controlled merge can be selected.
- The command or workflow that deploys the approved candidate, plus the production environment.
- The production verification steps and health signals that establish that the changed behavior works.
- The rollback or roll-forward procedure, its authorization boundary, and any migration constraint that can make rollback unsafe.

Record the result in `docs/agents/workflow.md`.

Use tdd's verification scope as the default: presentation and copy changes use visual/direct checks; changed logic uses focused failing tests at existing public boundaries. Agents select established seams without another approval round; ask when the contract is unresolved. Capture any team overrides in the same file. When updating older configuration, identify blanket test-first, full-build, and independent-review clauses in workflow and root instructions and replace them consistently with the agreed scope. Summarize the workflow, feedback-loop contract, and production approval boundary in the `### Team workflow` line of the `## Agent skills` block so both load in every session.

If the repo already has a clear workflow, summarize it and confirm that Snappedly skills should follow it. Treat the repo's existing rules as the source of truth when they conflict with the default flow.

#### Section C: Triage labels

Skip this section when no `triage` skill is installed. An uninstalled skill needs no label mapping.

When `triage` is installed, ask exactly one question:

> Keep the default triage labels? (recommended: yes)

The canonical roles are `needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, and `wontfix`. On yes, use those strings. On no, collect the user's mapping to existing tracker labels and record it in `docs/agents/triage-labels.md`.

#### Section D: Domain docs

Use a single context by default: one `CONTEXT.md` at the repo root and `docs/adr/` for shared decisions. Offer a multi-context layout only when exploration found monorepo signals. If selected, use a root `CONTEXT-MAP.md` with a `CONTEXT.md` and context-scoped ADR directory for each bounded context.

Record the consumer rules and selected layout in `docs/agents/domain.md`. Do not create `CONTEXT.md`, `CONTEXT-MAP.md`, or ADRs during setup. The domain-modeling workflow creates them when a real term or decision needs recording.

#### Section E: Frontend conventions

Skip this section when the repo has no user interface. A backend or library repo needs no design configuration.

When exploration found frontend signals, record where the design language already lives, so the design skills extend it instead of inventing a competing one:

- The design system or component library in use, and where its components live.
- Where design tokens are defined: a Tailwind config, a theme file, CSS custom properties, or nothing yet.
- The directories holding user-facing interface. This is the scope the `code-review` Interface axis audits.
- Whether visual direction is open (a greenfield product or a redesign) or the established system is the brief.
- Any accessibility conformance target the team commits to.

Ask only what exploration could not answer, and lead with what you found. Record the result in `docs/agents/frontend.md`.

#### Section F: Root agent instructions

Maintain the canonical root instruction file. Preserve surrounding project instructions in `AGENTS.md` and update existing matching sections in place.

Add or update this section in `AGENTS.md`:

```markdown
## Reporting

When reporting information to me, be extremely concise, sacrificing grammar for concision.
```

If `AGENTS.md` is missing, create it. Keep the `## Agent skills` block there as the canonical project configuration.

Completion criterion: every applicable section has an explicit answer, `AGENTS.md` exposes the required project rules, and no repo file has been written from an unconfirmed choice or without a usable GitHub or GitLab connection.

### 3. Confirm

Show the user the exact draft before writing:

- The `## Agent skills` block to write to `AGENTS.md`.
- `docs/agents/issue-tracker.md`.
- `docs/agents/workflow.md`.
- `docs/agents/domain.md`.
- `docs/agents/triage-labels.md` when the triage section ran.
- `docs/agents/frontend.md` when the frontend section ran.
- The `AGENTS.md` reporting section and canonical `## Agent skills` block.

Use the GitHub or GitLab tracker template and the other seed templates in this skill directory as starting points. Replace their bracketed guidance with the repo's confirmed facts. Let the user edit the draft before proceeding.

Completion criterion: the user has confirmed the root instruction file and every applicable configuration file, after a usable GitHub or GitLab connection was confirmed.

### 4. Write

Update or create `AGENTS.md`. Preserve surrounding content and update existing matching sections in place rather than appending duplicates. Keep the concise `## Reporting` rule and the `## Agent skills` block there.

Use this block, filling each line with the confirmed configuration:

```markdown
## Agent skills

### Work tracker

[one-line summary of where work is tracked]. See `docs/agents/issue-tracker.md`.

### Team workflow

[one-line summary of the agreed flow]. See `docs/agents/workflow.md`.

### Triage labels

[one-line summary of the label vocabulary]. See `docs/agents/triage-labels.md`.

### Domain docs

[one-line summary of the selected single-context or multi-context layout]. See `docs/agents/domain.md`.

### Frontend

[one-line summary of the design system in use and the directories holding user-facing interface]. See `docs/agents/frontend.md`.
```

Add the `## Reporting` section shown in step 2 above to `AGENTS.md`.

Include the `### Triage labels` subsection and its file only when the triage section ran, and the `### Frontend` subsection and its file only when the frontend section ran. Write `docs/agents/issue-tracker.md` from the matching GitHub or GitLab tracker template. Write `docs/agents/workflow.md`, `docs/agents/domain.md`, and `docs/agents/frontend.md` from their seed templates.

Completion criterion: `AGENTS.md` and every applicable `docs/agents/` file contain the confirmed GitHub or GitLab configuration, with no duplicate managed sections or unfinished template placeholders.

### 5. Finish

Tell the user which files were written and which Snappedly skills will read them. Explain that `AGENTS.md` is the canonical project-instruction file and `docs/agents/*.md` files are the direct editing points for small convention changes. Re-run this setup only when the tracker, team workflow, labels, domain layout, frontend conventions, or root agent instructions change.

Completion criterion: the user can locate each configuration file and knows which file to edit for each kind of change.
