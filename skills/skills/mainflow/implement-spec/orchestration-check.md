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
