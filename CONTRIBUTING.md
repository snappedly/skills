# Contributing to Snappedly Skills

This is a private repository shared with invited collaborators. Contributions should stay within the authorized group and should not be redistributed outside it.

## Before opening a pull request

1. Keep each skill at `skills/<group>/<name>/SKILL.md`.
2. Keep the `name` frontmatter value aligned with the skill directory.
3. Add or update `agents/openai.yaml` when the skill's invocation metadata changes.
4. Keep supporting Markdown files local to the skill package.
5. Update the README or changelog when a user-facing workflow changes.
6. Run the validation check:

   ```bash
   python scripts/validate-skills.py
   ```

## Pull requests

Describe the user-facing change, the skills affected, and the validation you ran. Keep unrelated workflow changes in separate pull requests. If a change alters invocation behavior, explain the intended implicit or explicit invocation policy in the pull request description.

## Releases

Release preparation should update [CHANGELOG.md](CHANGELOG.md), pass validation, and use a semantic version tag with a leading `v`. The current private-preview line begins at `v0.1.0`.
