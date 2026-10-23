---
name: retro
description: "Review a coding session and recommend evidence-backed improvements to the agent's environment."
disable-model-invocation: true
license: MIT
---

# Retro

A retrospective proposes prioritized remedies. Implement only the remedies the user approves, either in the request that started the retro or by replying to **Recommended changes**.

## Inspect the session

Use the current session unless the user names another. Read the relevant transcript, tool results, and existing decision logs, and point to specific events. State what evidence is missing or incomplete, and draw conclusions only from the parts of the session you could inspect.

For each observed difficulty, inspect the relevant repository configuration before proposing a remedy. Existing check commands, CI, hooks, standards, and `docs/agents/workflow.md` may already address it but be disconnected, unclear, or broken.

For code changes, also check whether required feedback-loop commands run through CI or local hooks. Report missing or broken enforcement where those checks should protect the changed work. A documented command alone does not establish that it runs.

Done when every observed difficulty has an evidence pointer and the repository configuration bearing on it has been inspected.

## Choose improvements

Consider these remedies where the evidence supports them:

- **Navigation:** add a pointer where the agent looked, when needed information was difficult to find.
- **Checks:** repair existing enforcement first. For a mechanical failure with no adequate check, propose the cheapest reliable check through the repository's existing tools.
- **Standards:** clarify judgment calls in existing standards or workflow docs. Keep applicable standards available to both implementation and review, including work handled by one agent.
- **Instructions:** clarify or remove steering that caused confusion or added no useful direction. Load and apply `writing-for-agents` when editing agent documents; if it is not installed, say so and hold them to its core standard: each meaning in one place, positive instructions, and a clear completion criterion for every step.
- **Tooling and access:** reduce demonstrated tool cost or expose needed information through a scoped capability, such as readable development logs. A recommendation does not authorize credential changes or broader access.

Weigh each remedy's maintenance cost, runtime overhead, and false positives; a noisy or redundant check may need narrowing or removal. Extend an existing standards file when one fits.

## Return findings

Order findings by observed consequence and likely recurrence. For each, report the event and evidence pointer, whether its cause is observed or inferred, the proposed remedy and its destination, and how to verify improvement. No quota applies: report no actionable findings when the evidence supports none.

Unless the request already approved implementation, end the report with a horizontal rule and a **Recommended changes** heading. Under it, number the remedies in the same order as the findings, one line per remedy. Each line names the change and its destination in plain language that someone who has not read the rest of the report can approve.

When the user approves remedies, apply them within scope and run the affected checks. Done when every remedy is applied with its checks run, or listed as unapplied with the reason.
