# snappedly-skills

Snappedly's reusable engineering skills. They share a small per-repository contract written by `setup-snappedly-skills`.

## Main workflow

The default flow for multi-session work is:

`grill-with-docs` → `to-spec` → `to-tickets` → `implement-spec`

For a smaller change, start `implement` once the request is clear, then run `build-local` to test locally. Use `handoff` when another session or directory needs to continue the work.

## Skill groups

Each skill lives at `skills/<group>/<name>/SKILL.md`. The catalog follows the directory tree:

| Directory | Purpose | Skills |
| --- | --- | --- |
| `begin/` | Choose and configure the workflow | `ask-snappedly`, `setup-snappedly-skills` |
| `direction/` | Explore ideas and settle design decisions | `grill-me`, `prototype`, `research`, `wayfinder` |
| `mainflow/` | Shape and implement planned work | `grill-with-docs`,  `to-spec`, `to-tickets`, `implement-spec` |
| `tools/` | Standalone workflow tools | `code-review`, `handoff`, `implement`, `teach`, `wait-what`, `wizard` |
| `upkeep/` | Maintain the codebase and triage incoming work | `diagnosing-bugs`, `improve-codebase-architecture`, `resolving-merge-conflicts`, `triage` |
| `practices/` | Reusable engineering disciplines and references | `code-cleanup`, `codebase-design`, `domain-modeling`, `frontend-design`, `frontend-guidelines`, `remove-slop`, `tdd`, `writing-for-agents` |

## Skills list

| Workflow concern | Skill |
| --- | --- |
| Stress-test a plan or decision | `grill-me` |
| Build the shared domain model | `domain-modeling` |
| Triage tracker work | `triage` |
| Clarify an idea and record its decisions | `grill-with-docs` |
| Publish a spec | `to-spec` |
| Publish a dependency-aware ticket graph | `to-tickets` |
| Drive behavior-first tests | `tdd` |
| Implement approved work | `implement` |
| Implement a complete spec as one pull or merge request | `implement-spec` |
| Serve a verified local build URL | `build-local` |
| Clean and validate changes before review or commit | `code-cleanup` |
| Review standards, spec, and UI guidelines separately | `code-review` |
| Diagnose hard bugs and regressions | `diagnosing-bugs` |
| Continue work in another session | `handoff` |

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
