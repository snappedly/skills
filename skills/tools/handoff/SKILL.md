---
name: handoff
description: Compact the current conversation into a handoff document for another agent to pick up.
argument-hint: "What will the next session be used for?"
disable-model-invocation: true
---

Write a handoff document summarising the current conversation so a fresh agent can continue the work. Save to the temporary directory of the user's OS - not the current workspace.

Include suggested skills only when the next task needs them, with each invocation condition. Carry forward completed work and valid checks so the next agent resumes rather than replays the workflow.

For delivery or closure work, include the repository workflow policy path, current PR/MR and ticket/spec states, and pending events with their responsible actor and required evidence. Link existing sign-off so the next session can check its scope and reuse it.

Do not duplicate content already captured in other artifacts (specs, plans, ADRs, issues, commits, diffs). Reference them by path or URL instead.

Redact any sensitive information, such as API keys, passwords, or personally identifiable information.

If the user passed arguments, treat them as a description of what the next session will focus on and tailor the doc accordingly.
