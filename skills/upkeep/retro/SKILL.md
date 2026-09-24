---
name: retro
description: "Review a coding session and recommend evidence-backed improvements to the agent's environment."
disable-model-invocation: true
---

# Retro

Use session evidence to improve future work. A retrospective produces prioritized recommendations; implement them only when the user's request includes that work. Preserve existing authorization rather than adding another approval step. Run in the current agent by default.

## Inspect the session

Use the current session unless the user names another. Read only the relevant available transcript, tool results, and existing decision logs. Point to specific events; distinguish observed failures from inferred causes. State missing or incomplete evidence, and avoid conclusions about portions of a session you cannot inspect.

For each observed difficulty, inspect the relevant repository configuration before proposing a remedy. Existing check commands, CI, hooks, standards, and `docs/agents/workflow.md` may already address it but be disconnected, unclear, or broken.

## Choose improvements

Consider these remedies where the evidence supports them:

- **Navigation:** add a pointer where the agent looked, when needed information was difficult to find.
- **Checks:** repair existing enforcement first. For a mechanical failure with no adequate check, propose the cheapest reliable check through the repository's existing tools.
- **Standards:** clarify judgment calls in existing standards or workflow docs. Keep applicable standards available to both implementation and review, including work handled by one agent.
- **Instructions:** clarify or remove steering that caused confusion or added no useful direction. Keep `AGENTS.md` concise and point to existing documentation. Use `writing-for-agents` when editing agent documents.
- **Tooling and access:** reduce demonstrated tool cost or expose needed information through a scoped capability, such as readable development logs. A recommendation does not authorize credential changes or broader access.

Consider maintenance cost, runtime overhead, and false positives. A noisy or redundant check may need narrowing or removal. Do not add tools merely to fill a category, or create a new standards file when an existing one fits.

## Return findings

Order candidates by observed consequence and likely recurrence. For each, report the event and evidence pointer, the proposed change and destination, and how to verify improvement. Mark uncertain causes explicitly. No quota applies: report no actionable findings when the evidence supports none.

Keep unrequested changes as recommendations. When implementation is authorized, apply the selected remedies within scope and run the affected checks; carry unresolved candidates forward explicitly. A retrospective is optional maintenance, not an automatic implementation closeout step.
