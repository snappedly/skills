---
name: diagnosing-bugs
description: Diagnose uncertain, persistent, or intermittent bugs and performance regressions. Use for explicit diagnosis requests or when a focused reproduction and fix do not explain the failure; ordinary visual corrections need no full diagnosis loop.
---

# Diagnosing Bugs

Start with the smallest useful investigation. For a clear local defect, inspect the symptom, fix its evidenced cause, and verify the affected behavior directly or with a focused regression test. Escalate to the full loop when the cause remains uncertain, the first fix fails, or the bug is intermittent or crosses boundaries.

For workflow slowdowns, captured thread events and timings are the initial evidence: trace the expensive steps to their callers and instructions. Replaying a long agent run is optional validation, not a prerequisite for correcting an evidenced instruction problem. State which conclusions are measured and which remain untested.

When exploring the codebase, read `CONTEXT.md` (if it exists) to get a clear mental model of the relevant modules, and check ADRs in the area you're touching.

## Redact

This skill has you show commands, outputs and captured artifacts. **Redact every secret first**: write `<REDACTED>` in its place. Build loops against env vars, so the credential stays in the environment rather than in what you show. Captured artifacts carry auth headers: quote only the lines that carry the signal.

If the redacted output is not enough to diagnose the bug, say so and ask the user.

## Escalate when needed

For uncertain, persistent, intermittent, or cross-boundary failures, read [DIAGNOSIS-LOOP.md](DIAGNOSIS-LOOP.md) and follow its reproduction, hypothesis, and verification loop. A clear local defect or an evidenced workflow-instruction problem can finish through the focused path above.
