# Snappedly Skills

> Source-available collection of reusable engineering skills for AI coding agents.

[![Validate skills](https://github.com/snappedly/skills/actions/workflows/validate-skills.yml/badge.svg)](https://github.com/snappedly/skills/actions/workflows/validate-skills.yml)

Snappedly Skills packages the workflows and engineering practices we use to move from an unclear request to a verified change. Each skill is self-contained, composable, and backed by the repository conventions it needs.

## Install

For permitted noncommercial use, install the collection with the Skills CLI:

```bash
npx skills add snappedly/skills
```

For updates:

```bash
npx skills update
```

## Getting started

Run `setup-snappedly-skills` for the first time in a target repository. It records the git tracker, team workflow and feedback-loop contract, triage label mapping, domain-document layout, frontend conventions, and root agent instructions in that repository. The other skills read those files instead of carrying project-specific policy.

If direction is needed, start with the direction skills and then move to the mainflow.

## Main workflow

The default flow for multi-session work is:

`grill-with-docs` → `to-spec` → `to-tickets` → `implement-spec`

For a smaller change, implement directly or use `implement` once the request is clear. Presentation edits use visual checks; changed logic uses focused tests. Cleanup and review stay in the current agent for low-risk work. Use `build-local` when a browser preview is useful. Use `handoff` when another session or directory needs to continue the work.

## Skill groups

Each skill lives at `skills/<group>/<name>/SKILL.md`. The catalog follows the directory tree:

| Directory | Purpose | Skills |
| --- | --- | --- |
| `begin/` | Choose and configure the workflow | `help-snappedly`, `setup-snappedly-skills` |
| `direction/` | Explore ideas and settle design decisions | `grill-me`, `prototype`, `research`, `wayfinder` |
| `mainflow/` | Shape and implement planned work | `grill-with-docs`, `to-spec`, `to-tickets`, `implement-spec`, `build-local` |
| `tools/` | Standalone workflow tools | `code-review`, `frontend-design`, `handoff`, `implement`, `wait-what`, `wizard`, `show-me-your-work`, `workflow-mapping` |
| `misc/` | Local maintenance and learning | `teach` |
| `upkeep/` | Maintain the codebase and triage incoming work | `codebase-cleanup`, `diagnosing-bugs`, `improve-codebase-architecture`, `resolving-merge-conflicts`, `triage` |
| `practices/` | Reusable engineering disciplines and references | `code-cleanup`, `codebase-design`, `domain-modeling`, `frontend-guidelines`, `pr`, `remove-slop`, `tdd`, `technical-writing`, `writing-for-agents` |

## Skills list

| Workflow concern | Skill |
| --- | --- |
| Choose the Snappedly skill or workflow for the current situation | `help-snappedly` |
| Configure a repository for Snappedly skills | `setup-snappedly-skills` |
| Stress-test a plan or decision | `grill-me` |
| Build a throwaway prototype to answer a design question | `prototype` |
| Investigate a question and capture cited findings | `research` |
| Plan a large effort as a decision-ticket map | `wayfinder` |
| Clarify an idea and record its decisions | `grill-with-docs` |
| Publish a spec | `to-spec` |
| Publish a dependency-aware ticket graph | `to-tickets` |
| Implement a complete spec as one pull or merge request | `implement-spec` |
| Serve a verified local build URL | `build-local` |
| Review a change with depth proportional to risk | `code-review` |
| Continue work in another session | `handoff` |
| Implement approved work | `implement` |
| Teach a concept over several sessions | `teach` |
| Recover when context did not land | `wait-what` |
| Generate a wizard for manual setup steps | `wizard` |
| Keep a decision and evidence log for reviewed work | `show-me-your-work` |
| Map workflow scenarios, outcomes, and missing cases | `workflow-mapping` |
| Diagnose hard bugs and regressions | `diagnosing-bugs` |
| Find opportunities to improve codebase architecture | `improve-codebase-architecture` |
| Sweep a codebase for unnecessary code and tests | `codebase-cleanup` |
| Resolve an in-progress merge or rebase conflict | `resolving-merge-conflicts` |
| Triage tracker work | `triage` |
| Clean and validate changes before review or commit | `code-cleanup` |
| Design deep modules and clear seams | `codebase-design` |
| Build the shared domain model | `domain-modeling` |
| Set the visual direction for a UI surface | `frontend-design` |
| Audit UI code against interface guidelines | `frontend-guidelines` |
| Create and review PRs with clear evidence and reviewer guidance | `pr` |
| Remove AI-generated slop from code and writing | `remove-slop` |
| Drive behavior-first tests | `tdd` |
| Write and review docs, RFCs, READMEs, PR descriptions, and commit messages | `technical-writing` |
| Write documents for agents | `writing-for-agents` |

## Validation

Install the validation dependency and run the repository check:

```bash
python -m pip install -r requirements-validation.txt
python scripts/validate-skills.py
```

The same check runs in GitHub Actions for pull requests and pushes to `main`.

## Updating older workflow configuration

Installed skills and existing repository instructions are separate copies. After updating skills, review `AGENTS.md` and `docs/agents/workflow.md` for blanket test-first, full-suite/build, and independent-review requirements. Update those clauses to the agreed verification scope; preserved repository requirements still take precedence over skill defaults. The setup workflow template supplies the new defaults.

## Contributing

Contributions are welcome from people who can grant Snappedly the relicensing rights described in [CONTRIBUTING.md](CONTRIBUTING.md). Please open an issue before starting work if no contributor agreement is already in place.

## License

This repository is licensed under the [PolyForm Strict License 1.0.0](LICENSE). You may use these skills for noncommercial purposes. The license does not permit distributing them, modifying them, or creating new works based on them. Contact Snappedly to request a commercial license.
