# Contributing to Snappedly Skills

This is a source-available repository licensed under the [PolyForm Strict License 1.0.0](LICENSE). Contributions are welcome, but the license does not permit redistributing the repository or creating derivative works outside this contribution process.

To preserve Snappedly's ability to offer commercial licenses, we can accept only contributions for which Snappedly has separate relicensing rights through an employment agreement, contractor agreement, or written contributor agreement. Open an issue before preparing a contribution if no such agreement is already in place.

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

Release preparation should update [CHANGELOG.md](CHANGELOG.md), pass validation, and use a semantic version tag with a leading `v`. Before `v1.0.0`, breaking changes may require a minor-version increment.
