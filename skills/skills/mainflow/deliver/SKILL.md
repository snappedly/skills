---
name: deliver
description: "Deliver a verified change through its configured pull or merge request, production approval, deployment, verification, and recovery workflow."
---

# Deliver

Deliver a completed change according to `docs/agents/workflow.md`. That file defines who may merge, who approves production, and how to deploy, verify, and recover.

If `docs/agents/workflow.md` is missing or does not name the merge, deployment, production approval, verification, and recovery rules, tell the user to run `/setup-snappedly-skills`. Prepare any read-only evidence you can, but do not invent release policy.

## Prepare the review request

1. Identify the work item, requirements, base, task branch, final commit, and existing pull or merge request. Resume the existing request when one exists. Confirm the working tree contains no uncommitted task changes; return remaining implementation work to the implementation flow.
2. Confirm that `code-cleanup` results cover the final commit and that every applicable `code-review` axis completed. Resolve findings according to `docs/agents/workflow.md`. If the evidence covers another tree, rerun the affected cleanup and review work before delivery.
3. Push the task branch and create or update the pull or merge request. Its description must state the problem, resulting behavior, requirements links, validation, manual checks, and release or migration notes. Link the work item using the repository's issue-closing policy.
4. Wait for required checks and reviews on the current request revision. Fix task-related failures within the authorized work. Run cleanup after a fix, and return substantive changes to review. Refresh the evidence whenever the revision or integration result changes.

Completion criterion: the current pull or merge request revision satisfies every merge requirement in `docs/agents/workflow.md`, with no unresolved task finding or check.

## Merge and prepare production

If merging would start an unapproved production deployment, stop before merging. Explain which repository or deployment setting must provide the production approval gate. Preview deployments may continue when the repository policy allows them.

Once the production gate is confirmed, merge the pull or merge request using the configured strategy. Record the resulting default-branch commit and the production artifact or candidate derived from it.

Prepare the approval request with:

- The exact commit and immutable artifact identifier, when the release system supplies one.
- The target production environment and change summary.
- Required-check and review results for that candidate.
- Migration steps, expected user impact, verification plan, and configured recovery procedure.

Ask the approver named in `docs/agents/workflow.md` to approve this production candidate. Wait for explicit approval. A new commit, rebuilt artifact with different contents, changed migration, or changed target environment creates a new candidate and requires new approval.

Completion criterion: the merged revision is known, the release candidate is immutable or otherwise identified precisely, and the configured approver has explicitly approved that candidate for the named production environment.

## Deploy and verify

After approval, start or resume the configured deployment. Monitor it to completion and record the provider's deployment result and deployed revision.

Run the production verification defined in `docs/agents/workflow.md`. Verify the changed user behavior and applicable health signals, not only deployment status or an HTTP response. Redact secrets and sensitive production data from reports.

If deployment or verification fails, use the configured recovery procedure within the task's authorization. When recovery requires a new destructive action or a decision the policy does not pre-authorize, present the failing evidence and exact recovery action for human direction. Verify recovery and record follow-up work.

Update the work item with the pull or merge request, merged revision, production deployment, verification result, and any recovery or follow-up issue. Distinguish merged, deployed, and production-verified states. Close the work item according to its configured closing point.

Completion criterion: production runs the approved revision, the configured verification passed, and the work item links to the merge and deployment evidence. A recovered failed release is complete only when recovery verification passes and follow-up work is recorded.
