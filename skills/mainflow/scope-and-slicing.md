# Scope and tracer bullets

Use this guidance when shaping, ticketing, or implementing planned work.

## Keep the agreed scope

Treat the user's requested outcome and accepted constraints as the boundary. Include behavior the user agreed to and work required to deliver it. Keep optional enhancements, general hardening, and adjacent cleanup out unless the user accepts them or they are a concrete blocker. A change can touch several files and still be one outcome; file count and layer count do not determine workflow size.

## Choose the lightest workflow

A single observable outcome with no material unresolved contract or dependency graph fits one executable issue or brief, or direct implementation when repository policy permits. Skip the planning spec and ticket graph. Use the full planning chain when the work has multiple accepted outcomes, meaningful dependencies, material risk, or a need for cross-session coordination. Preserve repository-required steps in either path.

## Start broad work with a tracer bullet

For accepted work that needs multiple slices, choose the smallest end-to-end slice through only the layers it needs. Prefer the slice that verifies the critical path or a risky shared assumption. Verify it before repeating the same approach across later slices, and use the result to refine the remaining plan. Each later slice must deliver a distinct accepted outcome or a real prerequisite. If evidence changes the agreed outcome, contract, or scope, pause for the user's decision before expanding the work.
