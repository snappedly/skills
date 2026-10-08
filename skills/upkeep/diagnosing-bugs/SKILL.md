---
name: diagnosing-bugs
description: Diagnose bugs and performance regressions whose cause is uncertain, intermittent, or survives a first fix. Use for explicit diagnosis requests; a routine visual correction is fixed directly.
license: MIT
---

# Diagnosing Bugs

Start with the smallest useful investigation. For a clear local defect, inspect the symptom, fix its evidenced cause, and verify the affected behavior directly or with a focused regression test. When the cause remains uncertain, the first fix fails, or the bug is intermittent or crosses boundaries, read [DIAGNOSIS-LOOP.md](DIAGNOSIS-LOOP.md) and follow its reproduction, hypothesis, and verification loop.

For a slow agent or skill run, start from the run's recorded tool calls and their timings: trace the expensive steps to the instructions that prompted them, and correct an evidenced instruction problem through the focused path above. Repeating the full run is optional validation. State which conclusions are measured and which remain untested.

When exploring the codebase, read the File structure section of the installed `domain-modeling/SKILL.md` (without that skill, use the paths `docs/agents/domain.md` records, else the root `GLOSSARY-MAP.md` or `GLOSSARY.md`, or legacy `CONTEXT-MAP.md` or `CONTEXT.md`) and the selected glossary as read-only context. Check ADRs in the area you're touching.

## Redact

This skill has you show commands, outputs and captured artifacts. **Redact every secret first**: write `<REDACTED>` in its place. Build loops against env vars, so the credential stays in the environment rather than in what you show. Captured artifacts carry auth headers: quote only the lines that carry the signal.

If the redacted output is not enough to diagnose the bug, say so and ask the user.
