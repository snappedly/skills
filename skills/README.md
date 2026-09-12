# snappedly-skills

Snappedly's reusable engineering skills. They share a small per-repository contract written by `setup-snappedly-skills`.

## Main workflow

The default flow is:

`grill-with-docs` → `to-spec` → `to-tickets` → `implement` → `handover`

| Workflow concern | Skill |
| --- | --- |
| Stress-test a plan or decision | `grill-me` |
| Build the shared domain model | `domain-modeling` |
| Triage tracker work | `triage` |
| Publish a spec | `to-spec` |
| Publish a dependency-aware ticket graph | `to-tickets` |
| Drive behavior-first tests | `tdd` |
| Implement approved work | `implement` |
| Clean and validate changes before review or commit | `code-cleanup` |
| Review standards, spec, and UI guidelines separately | `code-review` |
| Diagnose hard bugs and regressions | `diagnosing-bugs` |
| Continue work in another session | `handoff` |

`grill-me`, `domain-modeling`, `tdd`, `code-cleanup`, `code-review`, and `diagnosing-bugs` are supporting skills. Cleanup runs within an authorized implementation task; a review-only request stays read-only. Tracker mutations require explicit invocation.

## Extended catalog

The source tree groups skills by role:

- Start: `setup-snappedly-skills`, `ask-snappedly`.
- Shaping: `grill-me`, `research`, `prototype`, `wayfinder`.
- Main workflow: `grill-with-docs`, `to-spec`, `to-tickets`, `implement`, `implement-spec`, `build-local`.
- Review: `code-cleanup`, `code-review`.
- Upkeep: `triage`, `diagnosing-bugs`, `improve-codebase-architecture`, `resolving-merge-conflicts`.
- Frontend: `frontend-design`, `frontend-guidelines`.
- Practices: `tdd`, `codebase-design`, `domain-modeling`, `remove-slop`.
- Tools: `handoff`, `wizard`, `teach`, `wait-what`, `writing-for-agents`.

## Install

You can install the repository directly with the [`skills`](https://github.com/vercel-labs/skills) CLI. Install every skill for Codex in the current project with:

```bash
npx skills add snappedly/tools/skills
```

For a project install, the CLI records the source and installed skill paths in `skills-lock.json`. It tracks global installs in its global lock file. After pushing an update to this repository, refresh a project-scoped install with:

```bash
npx skills update
```

Install `setup-snappedly-skills` first for a target repository. It records the git tracker, team workflow, triage label mapping, domain-document layout, frontend conventions, and root agent instructions in that repository. The other skills read those files instead of carrying project-specific policy.
