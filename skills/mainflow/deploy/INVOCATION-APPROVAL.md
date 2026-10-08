# Invocation approval

Step 5's route when `workflow.md` assigns the merge to the agent on a named human's `/deploy`. Their invocation approves merging what their checkout held when they invoked deploy. Drift is content that checkout did not hold: the replayed commits and conflict resolutions step 2 noted on any pass.

1. **Account.** Check the code host account deploy acts under with the acting-account operation in `code-host.md`, else the host's current-user operation, such as `gh api user --jq .login`. When it is not the approver's, stop as step 5 does for a human merge.
2. **Drift.** With no drift, continue to step 3. Otherwise ask before merging, through the harness's question tool, or in chat when it has none. Show the drift, link the change request, and show its head commit, check results, base, and merge strategy; when the merge deploys to production, make the question the approval request that `workflow.md`'s production release section describes. Offer three answers: merge now, already merged on the host, or stop. On the answer, read the change request first, then take the first case that applies:
   - Merged: go to step 5's **Verify**, reporting a merged head that differs from the one shown.
   - Already merged: ask again with the change request's current state.
   - Merge now: a head or target base that changed since the question takes step 5's **Restart**. Otherwise, once step 4's done conditions and the account check still hold, continue to step 3 with the answer as the approval.
   - Any other reply, stop included: end the run as step 5 does for a human merge.
3. **Merge.** Merge with the configured operation and strategy, matched to the approved head, and record the approval, the invocation or the drift answer, where `workflow.md` records approval, else in the report. Continue at step 5's **Verify**.

Done when the change request is merged under a recorded approval, or the run has stopped with step 6 pending.
