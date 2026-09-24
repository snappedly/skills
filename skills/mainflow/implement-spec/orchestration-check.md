# Orchestration regression scenario

Use this worked scenario when changing orchestration instructions or investigating excessive usage. It is a modeled comparison, not measured token telemetry or a claim about every historical run.

## Two independent UI tickets

Assume tickets A and B modify independent components. Each requires its own targeted test and typecheck. The repository requires a full test suite and two production builds before handoff. Both tickets integrate without conflict. Three review axes apply.

The earlier composition required two ticket implementers, two merger agents, integrated cleanup, three reviewers, and a fix implementer. Ticket cleanup, integrated cleanup, and fix cleanup could each run the full suite and both builds. Cleanup and review also requested overlapping subsequent phases. This shows a duplication path; it does not prove a concurrent review race occurred in the reported incident.

| Event | Earlier modeled path | Bounded path |
| --- | --- | --- |
| Implement A and B | 2 implementers; targeted checks plus 2 full cleanup passes | 2 implementers; targeted tests, typechecking, scoped formatting/lint |
| Integrate | 2 merger agents | 2 direct coordinator integrations |
| Integrated validation | Another full cleanup | 1 cleanup by coordinator |
| Initial review | 3 independent axes | 3 independent axes at commit R |
| Small CSS fix | 1 fix agent, potentially full cleanup | Coordinator correction after all axes finish; affected checks |
| Follow-up | Potentially all 3 axes again | Interface only at commit F, unless the fix affects other axes |
| Further finding | Potential repeated fix/review | Stop automatic dispatch; coordinator triage |

With one CSS fix and one follow-up, the modeled earlier path uses 11 agent launches (2 implementers, 2 mergers, 3 reviewers, 1 fixer, 3 follow-up reviewers). The bounded path uses 6 launches (2 implementers, 3 reviewers, 1 follow-up reviewer), or 5 distinct agents if the Interface reviewer is reused. Cleanup is skill execution within the coordinator, not an extra agent.

If each earlier cleanup ran the required trio of full tests and two builds, the modeled path invokes that trio four times: twice for tickets, once integrated, once for the fix. The bounded path invokes it once initially, then reruns only affected members after the fix. If the CSS change affects both builds, both builds rerun; full-test evidence is reusable only if that suite's inputs exclude the CSS change. No reduction relies on skipping a required check.

Both paths still implement two tickets and integrate twice. The bounded path has one initial full cleanup, one fix batch, one affected validation pass, one initial review round, and one follow-up round. Capture actual commands and SHA transitions during a real run rather than reporting these modeled counts as measurements.

## Check the edge cases

- A failing ticket test returns to its implementer before integration.
- A missing workflow is reported as a policy gap; existing checks remain required.
- A content-preserving commit after validation binds evidence without a repeated run.
- A hook, dependency, configuration, tool, or relevant environment change invalidates affected evidence.
- A branch changing from R during review cancels obsolete work before any fix. Reports for R are not silently relabeled.
- A test-only fix considers Standards and Spec; Interface remains skipped absent UI impact.
- Any new or remaining follow-up finding reaches coordinator triage before another agent launch.
- An independent work-in-progress review snapshots new files and preserves the user's index and branch. A small local review inspects the diff and new files directly.

For a measured investigation, retain each agent's purpose, start/completion SHA and status, command invocation/result, duplicate or rerun reason, and branch change relative to the review target. Total implementation, integration, cleanup, review, and fix cycles. Compare those records with this model. Per-agent tokens and time remain unknown unless the runtime provides them.

## Dependency and worktree scenarios

Walk these instruction paths when changing scheduling or worker setup. They are review scenarios, not measured harness runs.

| Starting condition | Expected outcome |
| --- | --- |
| Ticket A is integrated; dependent B is still blocked by open issue A on the tracker | Record A's integration commit and release B from the run graph. Leave issue A open until its configured closure event. |
| Worker A reports completion but its branch has not been integrated | Keep B blocked until the coordinator accepts A's integration. If A is later reverted, recompute dependent readiness. |
| A fresh worker starts on the wrong base and has uncommitted work | Preserve that work and correct the base safely before implementation; never discard it with an unconditional reset. |
| A resumed worker has commits above its assigned base | Verify ancestry and account for its commits; do not reset merely because HEAD differs from the starting SHA. |
| Workers A and B both synchronize with tip T; A integrates first | Recheck B against the new tip and integrate serially. Reuse only checks whose inputs remain equivalent. |
| A required corpus test skips because an ignored fixture is absent | Report acceptance as unverified. Set up the supported environment or serialize verification of the candidate in a prepared checkout. |
| Independent UI tickets need the same new translation key | Assign one owner/dependency or pin the exact shared key before dispatch, even if the consumers edit different files. |
| Parallel commits invoke hooks that share mutable backup state | Serialize the affected operations or use supported isolation; worktree separation is insufficient. |
| Tickets use provider closure on PR merge; the parent spec requires sign-off | Use closing references for tickets whose other prerequisites are satisfied and an ordinary link for the parent. Keep the parent open pending sign-off. |

## Saved delivery policy scenarios

These scenarios cover setup output and its consumers, including standalone implementation and PR work.

| Starting condition | Expected outcome |
| --- | --- |
| Setup records ticket closure on merge, spec closure on recorded acceptance, and human-owned merging | Save each transition separately in repository workflow configuration and add the root instruction pointer. A fresh implementation session reads those choices without asking the user to select them again. |
| Standalone `implement` finishes a verified commit; policy permits the agent to open a PR but reserves merge for a human | Create the PR within scope, then report pending human merge. Do not infer merge authority from ticket closure on merge. |
| A ticket closes on verified implementation, with closure assigned to the agent | Once the configured verification evidence exists, the standalone implementer or coordinator closes that ticket and verifies tracker state. The parent follows its own acceptance rule. |
| A worker runs `implement` under `implement-spec` | Return implementation and verification evidence to the coordinator; do not independently run delivery or closure. |
| An existing PR says `Closes` for a spec that must await sign-off | During an authorized PR update, use an ordinary spec link; during review-only work, report the mismatch without editing. |
| Required sign-off already exists and covers the candidate | Reuse it and perform the due action only if assigned to the agent. Leave human-owned actions to the human. |
| Sign-off or a custom deployment event has not happened | Keep closure pending and hand off the next actor and missing evidence. A green implementation check does not substitute for the event. |
| An older repo has no explicit closure policy | Continue authorized implementation or drafting; resolve the missing choice before enabling automatic closure or performing an undecided transition. Updating the installed skill does not rewrite repo policy. |
| A merge succeeds but provider issue closure is delayed or did not apply | Verify tracker state and report closure as pending; do not claim that a closing reference proves closure. |

## Small-work routing checks

These are expected instruction paths for review, not measured agent runs.

| Request and policy | Expected path |
| --- | --- |
| Standalone implement: adjust a heading's spacing, no broader repo requirements | Visual check, applicable static checks, local diff review; no mandatory TDD or review agents. |
| Standalone implement: fix form validation logic | Focused failing test at an existing public boundary, fix, affected checks, local review unless risk warrants independence. |
| Implement-spec: two small copy/layout tickets, no broader repo requirements | Coordinator implements both, verifies the affected views, reviews the integrated diff locally, delivers one PR/MR; no fixed worker or reviewer count. |
| Implement-spec: substantial interacting changes, independent review required | Workers return focused verification and commits; coordinator owns required integrated checks and one independent review round. |
| A worker loads implement for a ticket or review fix | Worker completion returns to the coordinator before standalone review or delivery; no nested review chain. |
| Repository explicitly requires full tests/builds | Coordinator runs required integrated checks even for small work; ticket-level requirements apply only where policy specifies them. |
| Review fix changes one input to a previously passing check | Rerun affected checks and review the fix delta; committing unchanged content alone causes no rerun. |
