---
name: setup-snappedly-skills
description: "Configure a repository's code host, work tracker, workflow, domain and frontend docs, and root agent instructions for Snappedly skills."
disable-model-invocation: true
license: MIT
---

# Setup Snappedly skills

Create or update the per-repo configuration that Snappedly skills read: the `docs/agents/*.md` files, seeded from the templates beside this file, and the root `AGENTS.md`.

## Repeat runs

On a repeat run, `AGENTS.md` and `docs/agents/*.md` hold the team's recorded choices. Compare them with the repository and this skill's current requirements, and preserve each choice unless the user requests a change or it fails a current requirement. A new default alone does not replace a recorded choice. Draft from the existing configuration, using the templates only to fill missing content.

Older configuration needs these migrations as part of the run, without a separate request:

- Replace references to the renamed `wrap-up` and `ship` skills with `clean-up` and `deploy`. The renames change no recorded choice.
- Add the handoff paragraph, beginning "`/clean-up` leaves its edits", from [workflow.md](workflow.md#ready-to-implement) to `docs/agents/workflow.md` when it is missing, and give the earlier template sentence "Complete cleanup and applicable verification before commit" the current Required checks wording. In `docs/agents/workflow.md`, `AGENTS.md`, and the other agent instruction files Explore found, rewrite rules that conflict with the handoff: cleanup that stages, branches, or commits; a separate commit or clean working tree before deploy; or `/clean-up`, `code-review`, or their check record sequenced before a commit rather than before delivery. Keep rules that name a check or command to run at or before a commit, which `/deploy`'s commit observes, and rules that commit already satisfies, such as committing before a change request opens. For `CONTRIBUTING.md` and other human process docs, propose only conflicting rules, apply them when confirmed, and record a declined change under Ready to implement in `docs/agents/workflow.md` so a repeat run does not propose it again. Done when every agent instruction agrees with the handoff and each declined change is recorded.
- When an older `issue-tracker.md` holds change-request operations, move them and their request-surface policy into `code-host.md` and their closure policy into the delivery and closure section of `workflow.md`, carrying each over unchanged.
- Replace GitHub issue-list operations that stop at the CLI's default limit with the paginated operation in [issue-tracker-github.md](issue-tracker-github.md). Preserve the configured tracker repository and triage filters, and retain any existing operation that already exhausts all pages.
- Give the base branch and merge strategy their own lines in `workflow.md`, taking each from wherever the configuration already records it, `code-host.md` included. Move a merge actor recorded in `code-host.md` into the workflow's merge transition, asking when it conflicts with the actor recorded there. Then remove the base branch, strategy, and actor from `code-host.md` so its merge line names only the operation. When nothing records a base branch or strategy, propose the default branch or the host's default merge method and confirm it.
- Propose invocation approval for a hosted change request in any of these cases:
  - The merge belongs to a human, and an agent transition after the merge has nothing recorded that starts the agent.
  - The merge belongs to the agent after a human approval the code host cannot record, such as an approval of one's own change request.
  - An agent merge deploys to production with neither invocation approval nor a deployment-system approval gate recorded.

  On acceptance, name the approver and their code host account, record where approval is recorded, and add and verify the acting-account operation in `code-host.md`. In `workflow.md`, set the Merge or deliver change row, with the approver's instruction to merge replacing any approval the code host cannot record as its prerequisite; rewrite the file's other sentences about who merges or what gates the merge; and add the template's invocation approval paragraph and its Production release sentence on invocation approval, plus the approval-request sentence ("The approval request names…") when that section lacks it. Update every agent instruction file that states who merges or what gates the merge, such as `AGENTS.md`, in the same change; for human process docs, propose conflicting rules as the handoff migration above does.

  On decline, resolve what made the proposal apply: assign the merge to a human, record a deployment-system approval gate for a merge that deploys, or replace an approval the code host cannot record with one it can. Then record what starts each agent transition after the merge, such as the merger running `/deploy` again, or reassign the transition, and record the declined proposal under Delivery and closure in `workflow.md` so a repeat run does not propose it again.
- Add the template's Verify production row when it is missing, taking its trigger and actor from the recorded release and verification policy, and ask when none records them. When `workflow.md` lacks it, add the template's sentence that every agent transition needs something that starts the agent.
- Replace the old template sentence beginning "`/deploy` ends at merge" in `docs/agents/workflow.md` with the current template's sentence beginning "`/deploy` ends after the merge's close-out". Update copies of that template boundary in `AGENTS.md` and the other agent instruction files Explore found. Preserve the recorded actors, release triggers, and approval gates. Apply this migration whether invocation approval is accepted, declined, or not proposed; for human process docs, propose conflicting changes as the handoff migration above does.
- Refresh the root `### Code host` instruction so agents apply the title policy before every change-request create or update, including outside `pr`.
- Migrate legacy domain `CONTEXT.md` and `CONTEXT-MAP.md` files as Section D directs.
- For blanket test-first, full-build, and independent-review clauses in workflow or root instructions: when they came from older setup defaults, propose scoped replacements and confirm the team's intent; when their origin is unclear, ask. Preserve documented team overrides, and update every affected file to the agreed scope together.

## Process

### 1. Explore

Inventory the repository, file by file:

- Code host: `git remote -v` and `.git/config` identify the host and repository. Confirm how the agent can inspect and publish branches and change requests there, through the host's CLI, API, or another available connection. A local-only repository may record local delivery if the team does not require a hosted change request.
- Work tracker: identify it from the repository and existing configuration, independently of the code host; a GitHub remote is no evidence of GitHub Issues. Confirm how the agent can read and publish work, set the required fields, read parent and child relationships, and observe state.
- `AGENTS.md` at the repo root: existing reporting rules, any `## Agent skills` section, and whether the path is a symlink.
- Other agent instruction files: repository `CLAUDE.md`, `.claude/CLAUDE.md`, and relevant nested instruction files, with their unique rules, imports, and symlink targets.
- `CONTRIBUTING.md`, `README.md`, and other process docs: existing team rules that the Snappedly workflow must preserve.
- Change-request naming: documented title rules, title checks, and recent requests on the code host. Compare scope usage with domain docs and repository structure; recent titles are evidence for a proposal, not an approved scope list.
- `docs/agents/`: every file an earlier run wrote. Note recorded choices, local edits, missing required information, and conflicts with the current repo.
- Domain docs: recorded glossary and map paths, `GLOSSARY.md` and `GLOSSARY-MAP.md`, or legacy `CONTEXT.md` and `CONTEXT-MAP.md`, plus shared and context-scoped ADR directories.
- Installed `triage` skill: it decides whether Section C's role map applies.
- Frontend signals: a component library or design system dependency, a Tailwind, theme, or design-token configuration, a global stylesheet, a `components/`, `app/`, or `pages/` tree, a Storybook setup. These decide whether Section E applies.
- Monorepo signals: `pnpm-workspace.yaml`, a `workspaces` field in `package.json`, or a populated `packages/*` tree with its own `src/`.
- Feedback-loop signals: the package manager and lockfile, package scripts, TypeScript configuration, test runner, formatter/linter configuration, Git hooks, CI workflows, and any configured development or preview server.

Completion criterion: you have a file-by-file inventory, know what the root instruction file contains, know whether the triage, frontend, multi-context, and instruction-file branches apply, have mapped the existing feedback-loop surfaces, have identified the code host and tracker operations, and can name each migration, missing item, or conflict. If an existing setup satisfies the current requirements and the user requested no changes, report that no changes are needed and stop.

### 2. Align

Present the findings before asking questions. Take one section at a time. For a new setup, lead with the recommended answer so the user can accept it briefly. On a repeat run, present recorded answers only for sections needing attention and ask only about missing information or conflicts. Apply a clear user-requested change without re-asking. Ask before removing a section or file that appears no longer applicable. Explain a choice only when it changes the resulting workflow.

#### Section A: Code host and work tracker

The code host and work tracker are independent choices, each recorded in its own file with only **verified** operations: each has a usable connection you have checked, or an identified manual owner. Record where authentication is configured, never the credentials. When either connection is missing, draft the configuration, continue with the sections that do not depend on it, and ask only for the missing connection or routing choice.

Fill `docs/agents/code-host.md` from [code-host.md](code-host.md). If the host does not support change requests, record the team's review and delivery equivalent. For a new setup, external change requests enter triage only when the user explicitly opts in.

Take the title convention from existing repository rules. When title rules are missing, load and apply the installed `pr` skill through the available invocation mechanism or its `SKILL.md`, and include its default title and scope rules in `code-host.md` so agents can apply them outside the skill. Without `pr`, propose its default: the Conventional Commits form `type(scope): description`, or `type: description` without a scope, with lowercase types and scopes and `!` before the colon for a breaking change, using the types `feat`, `fix`, `perf`, `refactor`, `docs`, `style`, `test`, `build`, `ci`, `chore`, and `revert`. For the default convention, propose a small list of stable lowercase scopes with their meanings, derived from domain docs, repository structure, and recent change requests; prefer meaningful repository areas over folder names. Have the user confirm the list with the setup proposal, or record `none` if scopes are unnecessary. On a repeat run, propose scope changes when the user requests them or repository evidence shows the list needs revision, and preserve a recorded choice to use no scopes.

Fill `docs/agents/issue-tracker.md` from [issue-tracker-github.md](issue-tracker-github.md) for GitHub Issues; for another tracker, write the same contract using its real operations, URL, and identifier format. Verify read access plus the permissions or authenticated capability needed to create and update work. Scope every tracker command to that destination, even when it matches the code remote, and verify the target with a known work item before publication. If parent relationships are unavailable, record a body convention that preserves them, by default the `## Parent` section the GitHub template names. If a required operation has no usable path, state that the affected skill cannot publish through this tracker yet.

#### Section B: Team workflow

Fill `docs/agents/workflow.md` from [workflow.md](workflow.md): its fixed text is the proposed default, and each placeholder needs the team's answer. The repository's existing process docs and feedback-loop surfaces are the source of truth where they conflict with a default. If the repo has a clear workflow but no Snappedly workflow configuration, summarize it and confirm that Snappedly skills should follow it.

When no team workflow is recorded, ask whether the default Snappedly flow fits. For most work, the main flow: `grill (optional) -> execute -> clean-up -> deploy`. A small, clear request done directly uses `edit -> focused verification -> local review`, then `clean-up` and `deploy` when the user wants it finished and merged.

For the feedback-loop contract, record the commands and adapters the repository already has, using its package manager and scripts. For an absent surface, record `not configured` or `not applicable` and the trigger for adding it. Adding a test runner, formatter, linter, hook, or CI workflow requires an explicit opt-in, even in a TypeScript repository that has none.

For a new setup, ask how the user wants delivery and closure handled. On a repeat run, when a required transition is missing or ambiguous, present related existing policy as a proposed answer and confirm only the unresolved choice:

- Is delivery through one hosted change request, another review equivalent, or an explicitly chosen integration branch? When should the agent publish it, and who should merge or deliver it after which checks or approvals: the agent, a human, or, for a hosted change request, the agent on a named human's instruction to merge, such as `/deploy`, which approves merging what their checkout holds (invocation approval)? For a hosted change request, recommend that the agent merges on a named human's instruction: under invocation approval when the merge deploys to production without a deployment-system approval gate, and otherwise as a plain agent merge.
- Which base branch do change requests target, and which merge strategy does the merge use: merge, squash, or rebase?
- When should an executable ticket close: verified implementation, change-request merge, human sign-off, deployment verification, or another named event?
- Separately, when should the parent spec close? Does it require acceptance beyond completing its child tickets? When its last child closes without closing the spec, should the agent comment on the spec that it is ready for acceptance, or only report it? `deploy` follows the recorded answer.
- Who verifies production after a release, and what starts the release? `deploy` runs the verification when the agent owns it.
- For each transition, who acts: the agent, provider automation, or a human? If sign-off is required, who gives it, where is it recorded, and what work does it cover? For an agent transition that follows a human or external event, what starts the agent: a merge under invocation approval, the merger running `/deploy` again with the merged change request, or another recorded event? Without one, assign the transition to provider automation or a human.

Write the confirmed answers in the delivery and closure section: the base branch and merge strategy on their own lines, and each transition in its table with the evidence that establishes the event. Merge permission is its own answer: a closure-on-merge choice grants none.

When no production release policy is recorded, propose the template's release policy as the default and ask only about differences and the repository's specifics. If a merge automatically deploys to production, an agent merge needs an approval gate in the deployment system or invocation approval, whose instruction approves the production candidate.

#### Section C: Triage roles

When `triage` is not installed, skip this section and record triage roles and categories as `not configured` in `issue-tracker.md`.

When `triage` is installed, fill `docs/agents/triage-labels.md` from [triage-labels.md](triage-labels.md), keeping that filename even when the roles are not labels, and point to it from `issue-tracker.md` rather than copying the mapping there. Keep an existing mapping unless the tracker or the user's choice has changed, and ask only about missing or conflicting roles. For a new mapping, propose the tracker's simplest workable representation, often labels, and ask one focused question about it. Record the `bug` and `enhancement` category mapping in `issue-tracker.md`: each triaged item carries exactly one category role, `bug` or `enhancement`.

#### Section D: Domain docs

For a new setup, propose the single-context layout from [domain.md](domain.md). Offer the multi-context layout only when exploration found monorepo signals. Fill `docs/agents/domain.md` from that template with the resulting paths. On a repeat run, preserve the recorded layout; when the repository no longer supports it, explain the conflict and ask how to update it.

Legacy domain `CONTEXT.md` and `CONTEXT-MAP.md` files migrate to glossary naming on first-time and repeat runs alike, unless the user explicitly chose to keep the legacy names; setup is current only once they are migrated. Read [domain-migration.md](domain-migration.md) and include the migration in the setup proposal.

Setup creates glossary, map, and ADR files only to hold content preserved by a migration. Otherwise, the `domain-modeling` skill creates them when a real term or decision needs recording.

#### Section E: Frontend conventions

Run this section when exploration found frontend signals. Fill `docs/agents/frontend.md` from [frontend.md](frontend.md), recording where the design language already lives so UI work extends it instead of inventing a competing one.

#### Section F: Root agent instructions

`AGENTS.md` is the canonical root instruction file; treat references to `agent.md` as that file, and create it when missing. It carries the canonical `## Agent skills` block from step 4 alongside the project's other instructions, plus the optional `## Reporting` rule when the team accepts it.

When the repo has `CLAUDE.md`, `.claude/CLAUDE.md`, nested instruction files, or an `AGENTS.md` symlink, read [instruction-files.md](instruction-files.md) and include their handling in the proposal.

For a new setup, offer this section in the proposal as an optional rule, and add it to `AGENTS.md` only when the user accepts it. On a repeat run, preserve existing reporting guidance and propose this rule only when the user requests it:

```markdown
## Reporting

When reporting information to me, be extremely concise, sacrificing grammar for concision.
```

Completion criterion: every applicable section has an explicit answer, every agent transition has something that starts the agent, `AGENTS.md` exposes the required project rules, and every recorded provider operation is verified.

### 3. Confirm

For a new setup, show the user the exact draft before writing:

- `docs/agents/code-host.md`, `issue-tracker.md`, `workflow.md`, and `domain.md`, plus `triage-labels.md` when `triage` is installed and `frontend.md` when Section E ran.
- The canonical `## Agent skills` block for `AGENTS.md`, and the optional reporting section.
- The domain-document migration, including content destinations, reference updates, and legacy file removals.
- Any instruction-file changes, including preserved rules, compatibility files, and proposed removals.

On a repeat run, show a focused diff for each proposed edit and the complete content of any new file. Let the user edit the proposal before proceeding.

Completion criterion: the user has confirmed every proposed change, and every recorded provider operation is verified.

### 4. Write

Write only the confirmed changes. In `AGENTS.md`, preserve surrounding content and update existing matching sections in place. Write each applicable `docs/agents/` file from the template step 2 names; on a repeat run, edit only confirmed sections and create only missing required files. Apply the domain migration as [domain-migration.md](domain-migration.md) directs, and instruction-file changes as [instruction-files.md](instruction-files.md) directs.

For a new `## Agent skills` block, use this shape, filling each line with the confirmed configuration. On a repeat run, edit only affected entries. Include the `### Triage roles` subsection only when `triage` is installed, and the `### Frontend` subsection only when Section E ran:

```markdown
## Agent skills

### Code host

[one-line summary of where code is reviewed and delivered]. Before creating or updating any change request, read `docs/agents/code-host.md` and apply its title rules, including outside the `pr` skill.

### Work tracker

[one-line summary of where work is tracked]. See `docs/agents/issue-tracker.md`.

### Team workflow

[one-line summary of the agreed flow, feedback-loop contract, and production approval boundary]. Read `docs/agents/workflow.md` before implementation, change-request creation or merge, and completion-based ticket or spec closure; it defines the configured actors, events, and evidence.

### Triage roles

[one-line summary of the triage mapping]. See `docs/agents/triage-labels.md`.

### Domain docs

[one-line summary of the selected single-context or multi-context layout]. See `docs/agents/domain.md`.

### Frontend

[one-line summary of the design system in use and the directories holding user-facing interface]. See `docs/agents/frontend.md`.
```

Completion criterion: `AGENTS.md` and every applicable `docs/agents/` file contain the confirmed configuration, unchanged content remains intact, each migration is applied or reported incomplete, and no duplicate managed sections or unfinished template placeholders remain.

### 5. Finish

Tell the user which files were written and which Snappedly skills read them. Explain that `AGENTS.md` is the canonical project-instruction file and `docs/agents/*.md` files are the direct editing points for small convention changes. Re-run this setup when those conventions change or when a Snappedly release calls for a repository configuration update.

For a domain migration, report the removed legacy paths, the destinations of their useful content, and any integration that could not be verified.

Completion criterion: the user can locate each configuration file and knows which file to edit for each kind of change.
