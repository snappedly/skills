---
name: to-spec
description: "Turn the current conversation into a spec and publish it to the project issue tracker: no interview, just synthesis of what you've already discussed."
disable-model-invocation: true
---

This skill takes the current conversation context and codebase understanding and produces a spec. Do NOT interview the user; just synthesize what you already know.

Read the existing tracker configuration or reuse it from context. If the publishing destination cannot be established, prepare the local draft and ask for that missing destination; use `/setup-snappedly-skills` when repository-wide configuration is needed.

## Process

1. Explore the repo to understand the current state of the codebase, if you haven't already. Use the project's domain glossary vocabulary throughout the spec, and respect any ADRs in the area you're touching.

2. Describe verification proportional to the work, using tdd's scope guidance. Reuse established test boundaries and prior decisions. Ask only when a new interface or unresolved behavioral contract materially changes the plan; existing seams need no confirmation round.

3. Write the spec using the template below. Apply `technical-writing` to its title and body, then publish it to the configured GitHub or GitLab issue tracker. A spec is a planning artifact, not an executable work item. Do not apply `ready-for-agent` to it. `to-tickets` applies that state to the implementation tickets it creates. For a change small enough to implement as one issue, skip `to-spec` and put the agreed requirements in that executable issue instead; apply `technical-writing` to that issue too.

<spec-template>

**Work item type:** planning spec, not executable

## Problem Statement

The problem that the user is facing, from the user's perspective.

## Solution

The solution to the problem, from the user's perspective.

## User Stories

A concise numbered list of distinct user outcomes. Each user story may use the format:

1. As an <actor>, I want a <feature>, so that <benefit>

<user-story-example>
1. As a mobile bank customer, I want to see balance on my accounts, so that I can make better informed decisions about my spending
</user-story-example>

Cover the agreed scope once, without padding stories or inventing adjacent features.

## Implementation Decisions

A list of implementation decisions that were made. This can include:

- The modules that will be built/modified
- The interfaces of those modules that will be modified
- Technical clarifications from the developer
- Architectural decisions
- Schema changes
- API contracts
- Specific interactions

Do NOT include specific file paths or code snippets. They may end up being outdated very quickly.

Exception: if a prototype produced a snippet that encodes a decision more precisely than prose can (state machine, reducer, schema, type shape), inline it within the relevant decision and note briefly that it came from a prototype. Trim to the decision-rich parts, not a working demo, just the important bits.

## Testing Decisions

A list of testing decisions that were made. Include:

- The observable outcomes that verification must establish
- Which modules will be tested
- Prior art for the tests (i.e. similar types of tests in the codebase)

## Out of Scope

A description of the things that are out of scope for this spec.

## Further Notes

Any further notes about the feature.

</spec-template>
