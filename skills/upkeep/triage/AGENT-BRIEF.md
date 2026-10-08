# Writing Agent Briefs

An agent brief is a structured comment posted on a tracker item or an external change request when it moves to `ready-for-agent`. It marks the item as executable and is the contract an AFK agent works from; the original body and discussion are context.

The brief states **what the agent should do**. For an issue, that's building the change from nothing. For a PR, it's what's left to do *to the existing diff*: finish it, close gaps, address review points; "Current behavior" then describes the state of the diff.

## Principles

### Durability over precision

The issue may sit in `ready-for-agent` for days or weeks while the codebase changes. Write the brief so it stays useful as files are renamed, moved, or refactored:

- Describe interfaces, types, and behavioral contracts, naming the specific types, function signatures, or config shapes the agent should look for or modify.
- Leave out file paths, line numbers, and assumptions about the current implementation structure: they go stale.

### Behavioral, not procedural

Describe **what** the system should do and leave the **how** to the agent, which explores the codebase fresh and makes its own implementation decisions. For example:

- "The `SkillConfig` type should accept an optional `schedule` field of type `CronExpression`"
- "When a user runs `/triage` with no arguments, they should see a summary of issues needing attention"

### Complete acceptance criteria

Every agent brief must have concrete acceptance criteria, each independently verifiable, so the agent knows when it's done. For example: "Running `gh issue list --label needs-triage` returns issues that have been through initial classification".

### Explicit scope boundaries

State what is out of scope, so the agent neither gold-plates nor makes assumptions about adjacent features.

## Template

```markdown
## Agent Brief

**Work item type:** executable
**Category:** bug / enhancement
**Summary:** one-line description of what needs to happen

**Current behavior:**
Describe what happens now. For bugs, this is the broken behavior.
For enhancements, this is the status quo the feature builds on.

**Desired behavior:**
Describe what should happen after the agent's work is complete.
Be specific about edge cases and error conditions.

**Key interfaces:**
- `TypeName`: what needs to change and why
- `functionName()` return type: what it currently returns vs what it should return
- Config shape: any new configuration options needed

**Acceptance criteria:**
- [ ] Specific, testable criterion 1
- [ ] Specific, testable criterion 2
- [ ] Specific, testable criterion 3

**Out of scope:**
- Thing that should NOT be changed or addressed in this issue
- Adjacent feature that might seem related but is separate
```

## Examples

### Bug

```markdown
## Agent Brief

**Work item type:** executable
**Category:** bug
**Summary:** Skill description truncation drops mid-word, producing broken output

**Current behavior:**
When a skill description exceeds 1024 characters, it is truncated at exactly
1024 characters regardless of word boundaries. This produces descriptions
that end mid-word (e.g. "Use when the user wants to confi").

**Desired behavior:**
Truncation should break at the last word boundary before 1024 characters
and append "..." to indicate truncation.

**Key interfaces:**
- The `SkillMetadata` type's `description` field: no type change needed,
  but the validation/processing logic that populates it needs to respect
  word boundaries
- Any function that reads SKILL.md frontmatter and extracts the description

**Acceptance criteria:**
- [ ] Descriptions under 1024 chars are unchanged
- [ ] Descriptions over 1024 chars are truncated at the last word boundary
      before 1024 chars
- [ ] Truncated descriptions end with "..."
- [ ] The total length including "..." does not exceed 1024 chars

**Out of scope:**
- Changing the 1024 char limit itself
- Multi-line description support
```

### PR follow-up

```markdown
## Agent Brief

**Work item type:** executable
**Category:** enhancement
**Summary:** Finish the contributor's `--json` output flag for `triage list`

**Current behavior:**
The PR adds a `--json` flag that serializes the issue list to JSON. CI shows the
happy path passing, and the diff matches the project's command structure. Two gaps
remain: errors are still printed as human text (not JSON), and the new flag has
no test coverage.

**Desired behavior:**
With `--json`, all output (including errors) is well-formed JSON on stdout,
and the command's exit codes are unchanged. The existing human-readable output
is untouched when the flag is absent.

**Key interfaces:**
- The command's error path should emit `{ "error": string }` under `--json`
  instead of the plain-text error
- Reuse the existing serializer the PR already added; don't introduce a second

**Acceptance criteria:**
- [ ] `triage list --json` emits valid JSON for both success and error cases
- [ ] Exit codes match the non-JSON command
- [ ] A test covers the `--json` success output and one error case
- [ ] Default (non-JSON) output is byte-for-byte unchanged

**Out of scope:**
- Adding `--json` to any other command
- Changing the JSON shape of the success payload the PR already defined
```
