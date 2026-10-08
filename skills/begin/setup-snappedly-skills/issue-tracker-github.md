# Issue tracker: GitHub

Work items and specs for this repo live as GitHub issues in [owner/repository URL]. Use the `gh` CLI for tracker operations. Replace `<owner/repo>` below with this tracker repository, even when it matches the code remote. The code host is configured separately in `docs/agents/code-host.md`; it may be different.

Before completion-based closure or adding automatic closing references, read the delivery and closure policy in `docs/agents/workflow.md`. It defines when each ticket or spec closes and who acts; the commands below do not establish completion or authority to close it.

## Conventions

- Create an issue with `gh issue create --repo <owner/repo> --title "..." --body "..."`.
- Read an issue with `gh issue view <number> --repo <owner/repo> --comments`, including labels when the workflow needs them.
- List issues with `gh issue list --repo <owner/repo> --state open --json number,title,body,labels,comments` and filter by the labels and states the calling skill needs.
- Comment with `gh issue comment <number> --repo <owner/repo> --body "..."`.
- Apply or remove labels with `gh issue edit <number> --repo <owner/repo> --add-label "..."` or `--remove-label "..."`.
- Close with `gh issue close <number> --repo <owner/repo> --comment "..."`.

Use the same explicit repository for parent and triage operations. Qualify an issue reference with its provider or URL when it could be confused with a change request.

Triage roles: [refer to `docs/agents/triage-labels.md` when `triage` is installed, or `not configured`].

Triage categories: [labels or fields for the `bug` and `enhancement` category roles when `triage` is installed, or `not configured`]. Each triaged item carries exactly one category role, `bug` or `enhancement`.

## Work item mapping

- Executable ticket: GitHub issue with `**Work item type:** executable` in its body or its agent brief comment, plus the configured `ready-for-agent` state when triage roles are configured.
- Planning spec: GitHub issue with `**Work item type:** planning spec, not executable` in its body; do not mark it `ready-for-agent`.

## When a skill publishes work

Create a GitHub issue unless the calling skill says to update an existing issue.

## When a skill fetches work

Run the scoped `gh issue view` command above for an issue reference. Fetch change requests through `docs/agents/code-host.md` when they are in scope.

## Parent and child relationships

Prefer GitHub's native sub-issues for parent and child work.

- Parent and child: [the verified operations to read an issue's parent and its sub-issues, or `body convention` when sub-issues are unavailable].

Body convention: record the parent under a `## Parent` heading in the child's body, referencing it by number or URL. Where sub-issues are unavailable, read a child's parent from that section, and find a parent's children by searching for issues whose `## Parent` section references it.
