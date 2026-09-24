---
name: workflow-mapping
description: "Map user journeys and process scenarios, showing outcomes, logic mismatches, and missing cases."
disable-model-invocation: true
---

# Workflow mapping

Turn the supplied context into concrete scenario/result tables the user can inspect to decide whether the workflow behaves as intended. Apply this to user journeys, business processes, or automation; use the domain's own names for actors, objects, events, and states.

## 1. Establish the boundaries

Use the conversation and relevant code, tests, and specifications to identify entry points, actors, state, relationships, triggers, completion conditions, and observable side effects. Follow the logic through the components that determine the outcome, including downstream updates and failure handling.

State the scope and assumptions briefly. Distinguish intended behavior from implemented behavior: user decisions and specifications describe intent; code describes implementation; tests show which examples have assertions. When these disagree, preserve the disagreement. When only a proposal is available, label the map as proposed behavior.

Proceed once the workflow's boundaries and sources are identified. If missing context prevents a meaningful map, ask a focused question; otherwise carry the unknowns into the map.

## 2. Enumerate the paths

Build scenarios from reachable states and events. Each scenario names the starting conditions and the action or event sequence needed to distinguish its result. Follow the journey until completion, failure, cancellation, or a waiting state; for waiting states, identify what resumes progress.

Inspect these dimensions where the context supports them:

- Normal entry, eligibility, rejection, and no-op cases; missing prerequisites and boundary values.
- Success, failure, partial success, cancellation, and recovery at each step with observable effects.
- Repeated actions, duplicate events, retries, reopening, and reactivation after completion.
- Changed ordering, concurrent actions, stale observations, and interrupted work between side effects.
- Related objects: none, one, or several; mixed child states; links added or removed; parent status and rule precedence.
- Human intervention, permission changes, external dependency failures, and handoffs between actors or systems.

Include interactions that change the result, especially competing rules and event order. Group equivalent inputs only when they follow the same rule and produce the same effects; describe the grouping. For loops, cover first entry, repetition, and exit. Explain unreachable combinations using the rule that excludes them.

Finish when each identified entry point, decision branch, state transition, and relevant interaction has a scenario or an explicit coverage gap. Bound claims of completeness to this model and the evidence inspected; disclose unexplored combinations when the state space is too large.

## 3. Present the map

Lead with a short scope statement, then tables grouped by meaningful workflow stage or journey. Use stable case IDs so follow-up decisions can refer to individual rows.

| Case | Scenario | Result |
| --- | --- | --- |
| W1 | Starting conditions → action or event sequence | Observable outcome, state changes, side effects, and any next step |

Keep each row concrete enough for the user to say “yes, that is what I want” or name a correction. Include consequential no-ops, which objects change, and when effects occur. Split cases when their outcomes differ. Add a small diagram only when it clarifies branching or ordering that the table obscures.

Label results as implemented, specified, proposed, or unknown wherever the distinction affects interpretation. Attach concise source references to claims about existing behavior; shared references can sit directly below a group of rows. Code inspection supports a traced outcome, while an observed execution supports a verified outcome.

## 4. Surface gaps and decisions

After the map, list newly surfaced cases and unresolved behavior in a separate table:

| Cases | Gap or mismatch | Consequence | Decision or correction needed |
| --- | --- | --- | --- |
| Case IDs | Missing rule, conflicting intent, implementation mismatch, or missing test coverage | What a user or process experiences | A focused question or a clearly labeled recommendation |

Give each newly surfaced possibility a scenario row, even when its result is unknown. Say which cases are absent from the supplied requirements or tests; claims about what the user has considered require their confirmation. Keep missing tests distinct from demonstrated defects. Resolve intended outcomes from stated requirements where possible; otherwise leave the decision visible.

Conclude with the coverage boundary: what was inspected, assumptions still in use, and paths still unresolved. Mapping itself authorizes analysis; implement corrections when the user's request also authorizes them. When the user clarifies a rule, update affected cases and their interactions while preserving case IDs.
