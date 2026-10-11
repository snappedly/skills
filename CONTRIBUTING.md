# Contributing to Snappedly Skills

Snappedly Skills is open source under the [MIT License](LICENSE). Contributions are welcome.

By submitting a contribution, you agree that it is licensed under the MIT License and that you have the right to license it on those terms.

Everyone who takes part in this project follows the [Code of Conduct](CODE_OF_CONDUCT.md).

Ask questions and discuss ideas in [Discussions](https://github.com/snappedly/skills/discussions). Report bugs and request features with the issue forms.

## Before opening a pull request

1. Keep each skill at `skills/<group>/<name>/SKILL.md`.
2. Keep the `name` frontmatter value aligned with the skill directory, and list each skill in the README.
3. Follow the [Agent Skills specification](https://agentskills.io/specification) for frontmatter. This repository also allows two Claude Code extensions that the specification does not define: `disable-model-invocation` and `argument-hint`.
4. Add or update `agents/openai.yaml` when the skill's invocation metadata changes.
5. Keep supporting Markdown files local to the skill package.
6. Give each skill `license: MIT` frontmatter and a `LICENSE.txt` file. `npx skills add` copies only the skill folder, so the file must carry every copyright notice that applies to the skill. When a skill adapts another project's work, add that project's notice to the skill's `LICENSE.txt` and to [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
7. Update the README or changelog when a user-facing workflow changes. When setup changes required repository configuration, explain the migration for existing repositories and update the setup skill's repeat-run path.
8. Install the validation dependencies, then run the validation check. The check needs Python 3.12 or later.

   ```bash
   python -m pip install -r requirements-validation.txt
   python scripts/validate-skills.py
   ```

## What validation checks

- Frontmatter uses only the specification's fields and the two extensions above. A `name` is at most 64 lowercase letters, digits, and single hyphens. A `description` is at most 1,024 characters and contains no `<` or `>`.
- Each skill has an `agents/openai.yaml` file with a `display_name` and a `short_description` of 25 to 64 characters, the length Codex expects. Its `allow_implicit_invocation` value is the opposite of `disable-model-invocation`. Every `agents/openai.yaml` file belongs to a skill package with a `SKILL.md` file.
- Each skill has `license: MIT` frontmatter and a `LICENSE.txt` file with the Snappedly copyright notice.
- Local links, images, reference definitions, and `href` or `src` attributes resolve to files inside the skill package.
- The README names every skill.
- Each shared block listed in `SHARED_BLOCKS` in `scripts/validate-skills.py` appears exactly once in each file listed for it, between `<!-- shared: name -->` and `<!-- /shared: name -->` lines, and every copy is identical. Skills install as separate folders, so text that two skills share, such as the `prepare-delivery` steps in `deploy` and `submit`, is copied into each skill. Validation fails on a missing, duplicated, or differing copy, a malformed or unmatched marker, and a block `SHARED_BLOCKS` does not list. Edit one copy, then paste it over the others. To share new text, wrap each copy in markers and add the block to `SHARED_BLOCKS`.
- `changelog.json` lists releases newest first, and each entry follows the rules in [Releases](#releases).
- A pull request that adds a release to `changelog.json` has a `## Docs site` section in its description, as [Releases](#releases) describes. This check runs only in CI, because it reads the pull request description.

## Pull requests

Changes reach `main` through a pull request, and validation must pass before it can merge. Describe the user-facing change, the skills affected, and the validation you ran. Keep unrelated workflow changes in separate pull requests. If a change alters invocation behavior, explain the intended implicit or explicit invocation policy in the pull request description.

## Releases

Release preparation should update [CHANGELOG.md](CHANGELOG.md) and [changelog.json](changelog.json), update the docs site, pass validation, and use a semantic version tag with a leading `v`. A breaking change requires a major-version increment.

`changelog.json` holds the customer-facing notes for the [Skills changelog on docs.snappedly.com](https://docs.snappedly.com/changelog/?product=skills). For each release, add an entry with these fields:

- `version`: the release version without the leading `v`, such as `1.0.0`.
- `title`: a Title Case summary of the release.
- `changes`: one or more objects, each with a `type` and a `summary`. The type is `feature`, `improvement`, `fix`, `security`, or `deprecation`. The summary describes the resulting behavior in plain text.

Write skill names in Title Case, such as Codebase Cleanup. Leave out links, PR numbers, attribution, and code formatting. Validation rejects links and attribution. It also fails when the newest release in `CHANGELOG.md` has no entry in `changelog.json`.

The docs site reads `changelog.json` from `main`. It shows an entry only after the matching `v<version>` GitHub release is published, and it dates the entry from that release. Draft releases and prereleases stay hidden. The changelog needs no website change or deployment. To correct published wording, edit the entry on `main`.

### Docs site

The Skills pages on [docs.snappedly.com](https://docs.snappedly.com/skills/) describe what each skill does, how it starts, which skills it uses, and the repository configuration it needs. Maintainers keep them in the private `snappedly/snappedly-website` repository under `apps/docs/src/content/docs/skills/`.

For each release, check those pages against every change since the previous release, including added, removed, and renamed skills, and update the diagrams with the prose. Then add a `## Docs site` section to the release pull request's description with one of these:

- The `snappedly/snappedly-website` pull request that updates the pages, as a URL or a reference such as `snappedly/snappedly-website#123`.
- `No change:` and the reason, such as `No change: the release changes only skill wording that the docs do not quote.`

Validation fails a release pull request without either. Merge the docs pull request after you publish the GitHub release, so the docs never describe a skill that users cannot install yet.
