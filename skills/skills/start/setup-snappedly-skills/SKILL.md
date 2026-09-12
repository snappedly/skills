---
name: setup-snappedly-skills
description: "Configure a GitHub or GitLab repository for Snappedly skills, including tracker, workflow, domain and frontend docs, and root agent instructions."
disable-model-invocation: true
---

# Setup Snappedly skills

Create the per-repo configuration that Snappedly skills read. This is a prompt-driven setup: inspect the repo, summarize what you found, ask for the decisions that affect the team, show drafts, then write.

This process requires a usable connection to a GitHub or GitLab repository. A local checkout without either provider connection cannot be configured by this skill.

Use the canonical root filenames `AGENTS.md` and `CLAUDE.md`. Treat references to `agent.md` or `claude.md` as those files.

The setup records six concerns:

- Work tracker: where work items and specs live, and how the tracker is operated.
- Team workflow: how work moves from clarification through implementation, review, merge, production approval, deployment, verification, and handoff.
- Triage labels: the tracker strings that represent the canonical triage roles, when a triage skill is installed.
- Domain docs: where shared vocabulary and architectural decisions live.
- Frontend conventions: the design system, tokens, and UI directories the design and audit skills read, when the repo has a user interface.
- Agent instructions: concise reporting in `AGENTS.md`, plus the tool context guide in `CLAUDE.md`.

## Process

### 1. Explore

Read the repo before proposing configuration. Do not infer conventions from the remote alone.

- `git remote -v` and `.git/config`: identify the host and repository.
- `AGENTS.md` and `CLAUDE.md` at the repo root: inspect existing reporting rules, the Tool Context Guide, any `## Agent skills` section, and whether either path is a symlink.
- `CONTRIBUTING.md`, `README.md`, and other process docs: find existing team rules that the Snappedly workflow must preserve.
- `docs/agents/`: check for configuration written by an earlier run, including `issue-tracker.md`, `workflow.md`, `triage-labels.md`, `domain.md`, and `frontend.md`.
- `CONTEXT.md` and `CONTEXT-MAP.md` at the repo root, plus `docs/adr/` and any context-scoped ADR directories.
- Git provider connection: confirm that the remote points to GitHub or GitLab and that the matching CLI connection is available (`gh auth status` or `glab auth status`).
- An installed `triage` skill: this decides whether the triage-label section applies.
- Frontend signals: a component library or design system dependency, a Tailwind, theme, or design-token configuration, a global stylesheet, a `components/`, `app/`, or `pages/` tree, a Storybook setup. These decide whether the frontend section applies.
- Monorepo signals: `pnpm-workspace.yaml`, a `workspaces` field in `package.json`, or a populated `packages/*` tree with its own `src/`.

Completion criterion: you have a file-by-file inventory, know what each root instruction file contains, know whether the triage, frontend, and multi-context choices apply, and have confirmed a usable GitHub or GitLab connection.

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

Read existing process documentation first. Preserve its rules and ask the user whether the default Snappedly flow fits:

`clarify -> specify -> ticket -> implement -> code-cleanup -> code-review -> deliver -> handoff`

Capture the agreed GitHub or GitLab issue as the source of truth for work and the point at which implementation may start. Individual `/implement` work must be marked as an executable issue or have an executable agent brief; planning specs and wayfinder decision tickets do not qualify. `/implement-spec` is the explicit whole-spec path. Record the checks that `code-cleanup` must run, the review axes, the allowed disposition for each kind of finding, and the information a handoff must contain. Include `code-cleanup` after implementation and before review or commit. After review fixes, cleanup reruns checks affected by the final integrated state before substantive changes return to review.

Use the release policy in [workflow.md](workflow.md) as the default and ask only about differences. Record:

- The base branch, pull or merge request requirements, merge strategy, issue-closing point, and whether a preview deployment may run before production approval.
- How the release system identifies the production candidate and prevents an unapproved candidate from deploying. If a merge automatically deploys to production, require an approval gate in the deployment system before agent-controlled merge can be selected.
- The command or workflow that deploys the approved candidate, plus the production environment.
- The production verification steps and health signals that establish that the changed behavior works.
- The rollback or roll-forward procedure, its authorization boundary, and any migration constraint that can make rollback unsafe.

Record the result in `docs/agents/workflow.md`.

Capture the test-first clause in the same file: a new feature, a bug fix, or changed logic starts with a failing test at a seam agreed before the test is written. Record it as repository policy that holds whichever skill is driving the change, including work that invokes no skill at all. Summarize the workflow and production approval boundary in the `### Team workflow` line of the `## Agent skills` block so both load in every session.

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

Always maintain both canonical root instruction files. Preserve surrounding project instructions and update an existing matching section in place.

Add or update this section in `AGENTS.md`:

```markdown
## Reporting

When reporting information to me, be extremely concise, sacrificing grammar for concision.
```

Add or update this exact block in `CLAUDE.md`:

```markdown
# Tool Context Guide

## IMPORTANT: System Rules Injection
Always read and strictly adhere to the rules, tech stack details, and coding standards defined in the root folder file:
[AGENTS.md](./AGENTS.md)

Before executing any development tasks, internalize the constraints inside `./AGENTS.md`. It serves as the primary source of truth for this codebase. The instructions below only supplement it.

## Tool-Specific Overrides
* Run tests using the tool's native execution environment when available.
```

If either file is missing, create it. If `AGENTS.md` and `CLAUDE.md` resolve to the same symlink target, update the target once and verify both paths contain the required rules. Keep the `## Agent skills` block in `AGENTS.md` as the canonical project configuration.

Completion criterion: every applicable section has an explicit answer, both root instruction paths expose the required rules, and no repo file has been written from an unconfirmed choice or without a usable GitHub or GitLab connection.

### 3. Confirm

Show the user the exact draft before writing:

- The `## Agent skills` block to write to `AGENTS.md`.
- `docs/agents/issue-tracker.md`.
- `docs/agents/workflow.md`.
- `docs/agents/domain.md`.
- `docs/agents/triage-labels.md` when the triage section ran.
- `docs/agents/frontend.md` when the frontend section ran.
- The `AGENTS.md` reporting section and canonical `## Agent skills` block.
- The exact `CLAUDE.md` Tool Context Guide block.

Use the GitHub or GitLab tracker template and the other seed templates in this skill directory as starting points. Replace their bracketed guidance with the repo's confirmed facts. Let the user edit the draft before proceeding.

Completion criterion: the user has confirmed both root instruction files and every applicable configuration file, after a usable GitHub or GitLab connection was confirmed.

### 4. Write

Ensure both canonical root instruction files exist:

1. Update or create `AGENTS.md`.
2. Update or create `CLAUDE.md`.

If one path is a symlink to the other, edit the target once and preserve the symlink. Preserve surrounding content in either file. Update existing matching sections in place rather than appending duplicates.

Keep the concise `## Reporting` rule and the `## Agent skills` block in `AGENTS.md`. Keep the exact `# Tool Context Guide` block in `CLAUDE.md`.

Use this block, filling each line with the confirmed configuration:

```markdown
## Agent skills

### Work tracker

[one-line summary of where work is tracked]. See `docs/agents/issue-tracker.md`.

### Team workflow

[one-line summary of the agreed delivery flow]. See `docs/agents/workflow.md`.

### Triage labels

[one-line summary of the label vocabulary]. See `docs/agents/triage-labels.md`.

### Domain docs

[one-line summary of the selected single-context or multi-context layout]. See `docs/agents/domain.md`.

### Frontend

[one-line summary of the design system in use and the directories holding user-facing interface]. See `docs/agents/frontend.md`.
```

Add the `## Reporting` section shown in step 2 above to `AGENTS.md`. Add the exact `# Tool Context Guide` block shown in step 2 above to `CLAUDE.md`.

Include the `### Triage labels` subsection and its file only when the triage section ran, and the `### Frontend` subsection and its file only when the frontend section ran. Write `docs/agents/issue-tracker.md` from the matching GitHub or GitLab tracker template. Write `docs/agents/workflow.md`, `docs/agents/domain.md`, and `docs/agents/frontend.md` from their seed templates.

Completion criterion: `AGENTS.md`, `CLAUDE.md`, and every applicable `docs/agents/` file contain the confirmed GitHub or GitLab configuration, with no duplicate managed sections or unfinished template placeholders.

### 5. Finish

Tell the user which files were written and which Snappedly skills will read them. Explain that `AGENTS.md` is the canonical project-instruction file, `CLAUDE.md` points tools to it, and `docs/agents/*.md` files are the direct editing points for small convention changes. Re-run this setup only when the tracker, team workflow, labels, domain layout, frontend conventions, or root agent instructions change.

Completion criterion: the user can locate each configuration file and knows which file to edit for each kind of change.
