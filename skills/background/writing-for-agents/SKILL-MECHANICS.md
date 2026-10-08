# Skill mechanics

The skill-specific branch of [`writing-for-agents`](SKILL.md): what changes when the document is a skill (frontmatter, the invocation choice, and router skills). Everything else about writing it is the universal reference in `SKILL.md`.

## Invocation

Two choices, trading the two loads:

- A **model-invoked** skill keeps a `description`, so the agent can fire it autonomously, and other skills can reach it. You can still type its name: model-invocation always _includes_ user reach; a description only ever adds agent discovery, never removes the human's. The description is the skill's top-level context pointer, forced to stay loaded at all times: permanent context load in exchange for discoverability. A model-invoked skill whose content is all reference is also one home for shared reference: another skill can invoke it, so reference needed by several skills lives in one place. Write a model-facing description carrying the trigger branches (the pointer-writing rules in `SKILL.md` apply in full).
- A **user-invoked** skill strips the description from the agent's reach: only the human typing its name can invoke it, and no other skill can. Zero context load, but it spends cognitive load: you are the index that must remember it exists. The `description` becomes human-facing: a one-line summary, trigger lists stripped.

For Claude Code, omit `disable-model-invocation` from `SKILL.md` for model invocation, or set it to `true` for user invocation. For Codex, set `policy.allow_implicit_invocation` in `agents/openai.yaml` to `true` for model invocation or `false` for user invocation. Codex defaults to `true` when the setting is absent. Keep both settings aligned when a skill supports both hosts, preserving unrelated metadata.

Pick model-invocation only when the agent must reach the skill on its own, or another skill must. If it only ever fires by hand, make it user-invoked and pay no context load.

Keep distributed supporting files inside the skill package, because installers may copy only that folder. For guidance shared by several skills, use a named model-invoked reference skill and document its required installation. Repository or host context, such as team conventions, can remain outside skill packages. Name where to find that context and what to do if it is absent.

## Loading dependencies

Write dependencies as explicit instructions to load and apply the named model-invoked skill. Load each dependency separately when its branch applies. Use the agent's exposed skill-invocation mechanism; if none exists, read the installed `SKILL.md` and the references required for that branch. Reuse unchanged guidance already in context.

Loading guidance does not launch an agent or authorize work beyond the caller's scope. Recommend user-invoked entry points to the user rather than calling them as dependencies. When configuration is missing, continue independent drafting or inspection and recommend setup only for the repository decisions it needs.

## Splitting by invocation

The invocation cut of splitting (the sequence cut lives in `SKILL.md`): split off a model-invoked skill when you have a distinct leading word that should trigger it on its own (a trigger word you actually use in your prompts), or another skill must reach it. You pay context load for the new always-loaded description, so that independent reach has to be worth it.

## Router skills

When user-invoked skills multiply past what you can remember, that piled-up cognitive load is cured by a **router skill**: one user-invoked skill that names the others and when to reach for each, so the human has one skill to remember instead of many. It can only hint, never fire them: a user-invoked skill's description is out of the agent's reach, so nothing but the human can reach it.
