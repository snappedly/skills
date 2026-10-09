# Base branch protection

Applies when `workflow.md` delivers through a hosted change request. Setup recommends a code host rule that makes a merged change request the only way to change the base branch. The rule blocks direct pushes, such as a task branch merged locally and pushed to the base, while agents keep merging change requests through the host's merge operation.

## Inspect

Read every active rule on the base branch, from rulesets and classic branch protection where the host has both. On GitHub, `gh api repos/{owner}/{repo}/rules/branches/{branch}` lists ruleset rules, `gh api repos/{owner}/{repo}/rulesets/{id}` shows a ruleset's bypass actors and modes, and `gh api repos/{owner}/{repo}/branches/{branch}/protection` returns classic protection, or a 404 when there is none. Check whether the connection can administer the repository, such as `.permissions.admin` from `gh api repos/{owner}/{repo}`, and whether the host offers protection for it: GitHub offers it for private repositories only on paid plans.

Find automation that pushes to the base branch directly, such as a release job that commits version bumps or a bot that updates generated files.

## Propose

Propose a rule on the base branch, or keep the existing one when it already does this:

- Every change needs a change request. No actor can bypass it by pushing directly, administrators included; a bypass limited to merging change requests keeps the rule intact.
- Force pushes and deletion of the branch are blocked.
- No approving review is required, unless `workflow.md` records an approval on the code host as a merge prerequisite. Under invocation approval, the agent opens and merges the change request under the approver's account, and GitHub does not count an approval from the change request's author, so a required review blocks the merge.
- The recorded merge strategy is allowed.

On GitHub, that is a branch ruleset targeting the base branch with the `pull_request` rule at zero required approvals, plus the `non_fast_forward` and `deletion` rules, and no bypass actor in `always` mode. With classic branch protection, the equivalent is "Require a pull request before merging" with "Do not allow bypassing the above settings".

Preserve stricter rules the team already has, such as required checks or reviews. Flag any that conflict with the recorded merge actor, strategy, or operation, such as a required review the merger cannot obtain, required linear history under the merge strategy, or a merge queue the configured operation bypasses. For automation that must push to the base branch, propose its identity as the only bypass actor, or ask how it should deliver instead.

## Apply and record

On acceptance, create or update the rule through the host's API when the connection can administer the repository. Otherwise give the user the exact settings and wait for them to confirm they applied them. Then read the active rules back and compare them with the proposal.

Record the result on the base branch protection line of `code-host.md`: the rule, its bypass actors, and the operation that reads it back. When the host offers no protection for the repository, or the user declines, record that with the reason, and propose the rule again on a repeat run only when the reason no longer holds.

Done when the read-back matches the confirmed rule, or `code-host.md` records why the base branch has none.
