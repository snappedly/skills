---
name: teach
description: "Teach a concept over several sessions with practice, retrieval, and a small stateful learning record."
disable-model-invocation: true
---

# Teach

Teach the user a concept or skill in a way that can continue across sessions. Use the current directory as the learning workspace unless the user names another location.

## Establish the lesson

1. Ask what the user wants to be able to do, not only what topic they want explained.
2. Check their current understanding with a short task or explanation.
3. Inspect the repository and its vocabulary when the lesson is project-specific.
4. Create or read a small progress file such as `.scratch/learning/<slug>.md`.

Completion criterion: the target ability, starting point, next lesson, and progress-file path are clear.

## Teach and check

Explain one idea at a time in plain language. Use the project's domain terms. Ask the user to predict, apply, or explain the idea before giving the answer. Use a small example that changes one variable at a time. Correct misconceptions directly and connect each exercise to the target ability.

At the end of a session, record what the user can do, what remains uncertain, the next exercise, and any useful references. Do not write a generic lecture or claim mastery from recognition alone.

Completion criterion: the user has completed a task that demonstrates the target ability, or the record names the exact gap and the next practice step.
