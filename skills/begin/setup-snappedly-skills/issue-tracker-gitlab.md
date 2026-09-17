# Issue tracker: GitLab

Work items and specs for this repo live as GitLab issues. Use the `glab` CLI for tracker operations.

## Conventions

- Create an issue with `glab issue create --title "..." --description "..."`.
- Read an issue with `glab issue view <number> --comments` and use `-F json` when structured output helps.
- List issues with `glab issue list -F json` and filter by the labels and states the calling skill needs.
- Comment with `glab issue note <number> --message "..."`; GitLab calls comments notes.
- Apply or remove labels with `glab issue update <number> --label "..."` or `--unlabel "..."`.
- Close with `glab issue close <number>`. Post a closing explanation first with `glab issue note`.

Infer the project from `git remote -v`; `glab` uses the current clone automatically.

## Merge requests as a request surface

**MRs as a request surface: no.** Set this to `yes` only when this repo treats external merge requests as feature requests. When enabled, use the matching `glab mr` commands and include external MRs in triage. Keep maintainer-owned in-flight MRs out of request discovery.

GitLab numbers issues and merge requests separately, so `#42` is unambiguous once the calling workflow identifies the surface.

## When a skill publishes work

Create a GitLab issue unless the calling skill says to update an existing issue.

## When a skill fetches work

Run `glab issue view <number> --comments` for an issue reference. Fetch a merge request with `glab mr view <number> --comments` and its diff when MRs are in scope.

## Blocking relationships

When the workflow supports parent and child work, prefer GitLab's native relationships. If a relationship is unavailable on the project's tier, record the parent or blocker in the issue description using the convention named by the calling skill.
