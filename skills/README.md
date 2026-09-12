# snappedly-skills

Snappedly's reusable engineering skills. They share a small per-repository contract written by `setup-snappedly-skills`.

## Main workflow

The default delivery flow is:

`grill-with-docs` → `to-spec` → `to-tickets` → `implement` → `deliver`

Run `code-cleanup` once a task change is ready, before review and before committing. It formats and lints the changed code, then owns the final repository checks for the state it produces. After review fixes, rerun cleanup for the affected scope; cleanup reruns the affected checks before substantive changes return to review. Reuse passing checks only when their inputs and scope are unchanged. The skill supports automatic agent invocation. For enforcement independent of the agent, use pre-commit hooks locally and required CI checks before merge.

`implement` drives TDD where applicable, cleanup, review, review fixes, and the final commit. `deliver` follows the target repository's configured merge, production approval, deployment, verification, and recovery policy. The [setup workflow template](skills/start/setup-snappedly-skills/workflow.md) contains the default policy.

| Workflow concern | Skill |
| --- | --- |
| Stress-test a plan or decision | `grill-me` |
| Build the shared domain model | `domain-modeling` |
| Triage tracker work | `triage` |
| Publish a spec | `to-spec` |
| Publish a dependency-aware ticket graph | `to-tickets` |
| Drive behavior-first tests | `tdd` |
| Implement approved work | `implement` |
| Merge, request production approval, deploy, and verify | `deliver` |
| Clean and validate changes before review or commit | `code-cleanup` |
| Review standards, spec, and UI guidelines separately | `code-review` |
| Diagnose hard bugs and regressions | `diagnosing-bugs` |
| Continue work in another session | `handoff` |

`grill-me`, `domain-modeling`, `tdd`, `code-cleanup`, `code-review`, and `diagnosing-bugs` are supporting skills. Cleanup runs within an authorized implementation task; a review-only request stays read-only. Tracker mutations require explicit invocation.

## Extended catalog

The source tree groups skills by role:

- Start: `setup-snappedly-skills`, `ask-snappedly`.
- Shaping: `grill-me`, `research`, `prototype`, `wayfinder`.
- Main workflow: `grill-with-docs`, `to-spec`, `to-tickets`, `implement`, `implement-spec`, `build-local`, `deliver`.
- Review: `code-cleanup`, `code-review`.
- Upkeep: `triage`, `diagnosing-bugs`, `improve-codebase-architecture`, `resolving-merge-conflicts`.
- Frontend: `frontend-design`, `frontend-guidelines`.
- Practices: `tdd`, `codebase-design`, `domain-modeling`, `deslop`, `prevent-slop`.
- Tools: `handoff`, `wizard`, `teach`, `wait-what`, `writing-for-agents`.

## Install

The repository is directly installable with the [`skills`](https://github.com/vercel-labs/skills) CLI. Install every skill for Codex in the current project with:

```bash
npx skills add snappedly/tools/skills --agent codex --skill '*' --yes
```

Use `--global` to make the skills available in every project:

```bash
npx skills add snappedly/tools/skills --global --agent codex --skill '*' --yes
```

For a project install, the CLI records the source and installed skill paths in `skills-lock.json`. It tracks global installs in its global lock file. After pushing an update to this repository, refresh a project-scoped install with:

```bash
npx skills update --project --yes
```

For a global install, use:

```bash
npx skills update --global --yes
```

Updates are pull-based. The CLI does not watch GitHub or run when this repository changes, so run the update command manually or from a scheduled job on the machine that owns the installed skills.

Install `setup-snappedly-skills` first for a target repository. It records the GitHub or GitLab tracker, team workflow, triage label mapping, domain-document layout, frontend conventions, and root agent instructions in that repository. The other skills read those files instead of carrying project-specific policy.
