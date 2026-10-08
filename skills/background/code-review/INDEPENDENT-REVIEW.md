# Independent review

## Pin and freeze

Resolve base and target once. For a committed branch, use the fixed merge-base and target SHAs in diff commands and reviewer briefs.

For standalone work-in-progress review, capture an immutable snapshot of the requested staged, unstaged, and untracked content: a patch plus new-file contents, or an isolated Git snapshot that leaves the user's branch and index untouched. Record HEAD and the snapshot identity.

Every reviewer inspects the same frozen target. Keep the target branch and reviewed content unchanged until every active axis returns or its cancellation is confirmed. An unexpected change invalidates affected results: record the old and new targets and why, cancel obsolete agents, then reassess only affected axes. An unchanged axis result may carry forward with an explicit comparison of its files, context, requirements, and standards.

## Choose axes

Standards runs on every review, whether or not Spec runs.

Spec uses every requirement the caller supplies: request, plan, spec, or ticket. Fetch missing sources once and pass local pointers to reviewers. Otherwise inspect issue references and matching spec files, then ask only if the requirements cannot be established. Skip Spec only with an explicit no-requirements disposition.

Interface applies to files under the UI directories in `docs/agents/frontend.md` and to any other changed user-facing component, route, template, style, or design configuration. A change touching none of these skips Interface. Record the UI scope, and the accessibility baseline `frontend.md` records.

## Dispatch once

Set a completion deadline (default five minutes per axis), then launch one read-only reviewer per applicable axis in parallel. Brief each with the fixed target and comparison, task paths, the cleanup check record, requirement pointers, and its axis instructions below; reviewers read referenced files from their paths rather than receiving the whole conversation. Every reviewer takes the check record as validation evidence rather than rerunning those checks, reports only issues the change introduces or materially worsens, and returns its exact target, scope, findings, and coverage gaps.

- **Standards** reads [STANDARDS.md](STANDARDS.md) and the repository's coding-standards documents. Its brief is ready when it names every applicable standards source.
- **Spec** checks every supplied requirement for missing, partial, incorrect, or unrequested behavior and cites the requirement for each finding.
- **Interface** reads the pinned [GUIDELINES.md](GUIDELINES.md) and audits the UI scope against every applicable rule, treating the accessibility baseline's rules as findings rather than judgment calls. It reads enough surrounding code to tell a real violation from a rule satisfied elsewhere, such as a label rendered by a wrapper or a focus ring set by a shared class. It returns its `file:line` report, clean-file passes, and guidelines pin date.

When reviewer agents cannot be launched, because the environment cannot start them or no launch attempt returns a running reviewer, and independent review is optional, run each applicable axis yourself from its instructions above and report that coverage as local. If the user or repository requires independent review, report the review as not performed.

Wait on completion notifications rather than polling. Close each completed reviewer once its result is recorded, unless the caller expects a follow-up review that may reuse it; list each kept reviewer's ID in the report so the caller closes it when that follow-up ends or is ruled out. At the initial deadline, inspect each late reviewer once. If it is still making progress, extend its deadline by the original allowance once (five additional minutes by default) and record the new deadline. Otherwise cancel it. At the extended deadline, cancel any reviewer that has not returned, even if it is still making progress. Confirm cancellation before releasing the frozen target. If cancellation cannot be confirmed, keep the target frozen, record that axis as missing with its cause unknown, and end the review as incomplete; the caller makes no fixes or commit until the user decides. Preserve useful partial findings from every failed or canceled reviewer and mark its axis as missing coverage.

Once every reviewer has returned or its cancellation is confirmed, handle missing coverage:

- If at least one reviewer was running but no axis completed, report the review as not performed, retain partial findings, and leave the retry to the user. There is no local substitute in this case.
- If at least one axis completed and independent review is optional, finish each missing axis locally. Report which coverage was independent and which was local.
- If at least one axis completed and independent review is required, follow repository policy. Retry a missing axis only for a concrete recoverable cause within the caller's budget, if any, with at most one replacement per missing axis. Any policy-authorized waiver belongs to the coordinator.

Report observed failures and timeouts separately from their causes. State a cause only when evidence establishes it; otherwise record it as unknown. Multiple failed axes alone do not establish a model, quota, or tooling failure. Unresolved coverage remains incomplete under `SKILL.md`.

## Aggregate and follow up

The caller begins fixes only after every reviewer has returned or its cancellation is confirmed and every missing axis has a coverage disposition. Return Validation (the check record and its gaps), Standards, Spec, and applicable Interface results as separate sections, with counts, skip reasons, and finding dispositions, preserving each axis's conclusions.

When the caller requests a follow-up review of its fixes, review only the fix delta and affected context through affected axes. Reuse reviewers kept open from the first pass where possible, and explain each inclusion or skip. A CSS-only correction need not relaunch Spec unless it affects a requirement; a test-only correction need not launch Interface.

Record earlier findings as fixed, still open, or explicitly resolved, accepted, deferred, or waived under repository policy. Any new or remaining finding after the bounded follow-up returns to coordinator triage.
