# Code host: [provider or local delivery]

Repository: [remote URL or local path]. The code host and work tracker are independent. Work item operations live in `docs/agents/issue-tracker.md`.

## Connection and operations

- Connection: [available CLI, API, app, or manual owner; where authentication is configured, without secrets].
- Acting account: [operation that names the code host account the agent acts under, such as `gh api user --jq .login`; `deploy` checks it under invocation approval].
- Branches: [inspect, push, and fetch operations].
- Change requests: [create, read with comments and diff, update, and list operations; or the team's review equivalent].
- Review capability: [hosted change requests, local branch review, or another review equivalent; selected delivery policy lives in `docs/agents/workflow.md`].
- Checks and review: [how to inspect their current state].
- Merge or delivery: [operation only; the base branch, merge strategy, and who may merge or deliver live in `docs/agents/workflow.md`].
- Base branch protection: [the rule that requires a merged change request for every change to the base branch, its bypass actors, and the operation that reads it back; or why the base branch has none; `not applicable` without hosted change requests].
- Work-item links: [link syntax and whether it automatically closes an item on the configured work tracker].

## Change request titles

Title convention: [existing repository rules, or the accepted default format, allowed types, description, and breaking-change rules; `not applicable` when there is no titled review equivalent].

Scope policy: [approved scopes and their meanings, or `none`; selection and omission rules; maintainer approval process for scope changes].

For titled review equivalents, derive the title from the final diff and validate it against this policy. Publish through [the host's verified explicit title argument or field for create/update]. Read back the published title through [the verified read operation] and correct any mismatch.

## Request surface

External change requests enter triage: [yes or no].

[If yes: how to distinguish external requests from in-flight team work; the code-host values and operations for each triage state role and for the `bug` and `enhancement` category roles, of which each triaged request carries exactly one; how to comment on and close or decline a request; and any triage action that cannot run until an unavailable operation has a path. If no: `not applicable`.]

A change request identifier must include its provider when it could be confused with a tracker item.
