# Migrate domain documents

## Identify the files and destinations

Inspect the root legacy files, paths recorded in `docs/agents/domain.md`, and files linked from context maps. Check repository-owned context directories for additional domain `CONTEXT.md` files. Keep the existing bounded contexts and directory scopes. Migrate only domain files; unrelated context documents, dependency files, and generated copies keep their names even when the names match.

For each legacy domain file, inspect its current working contents, any existing destination, and references to its path. Map `CONTEXT.md` to `GLOSSARY.md` and `CONTEXT-MAP.md` to `GLOSSARY-MAP.md` in the same directory. Keep other custom glossary paths unless the user requests a change. If a legacy path is a symlink, inspect its target and consumers before proposing how to replace the link, and leave the target in place.

## Preserve the content

Account for each source section in the proposal:

- Domain terms, definitions, chosen synonyms, and useful domain scope belong in the glossary. Preserve their meaning; a filename migration does not authorize changing the domain model.
- A context map retains the context list, boundaries, relationships, and links, using the migrated paths.
- Relevant architecture, implementation, setup, process, or operational notes belong in suitable existing documentation. If none exists, create a focused document, such as `docs/architecture.md` or `docs/project-overview.md`. Link the destination from the documentation or agent instructions that previously exposed this information. Preserve actual decision records in their appropriate location; overview text stays documentation rather than becoming an ADR.
- Remove obsolete or duplicate material only when repository evidence establishes that it is obsolete or the destination already preserves it. Identify omissions in the proposal. When relevance is uncertain, preserve the material and flag the uncertainty.

A file containing only general project context may move entirely to suitable documentation; a glossary is created only where there are terms to hold.

When both names exist, merge the useful content rather than overwrite either file. Deduplicate equivalent definitions. If definitions or instructions conflict and the repository does not establish an authority, present the conflict for resolution before removing the source. Preserve unresolved content until the decision is made.

## Update consumers

Update `docs/agents/domain.md`, map links, agent instructions, documentation links, and affected scripts, CI, or configuration together. Search for references to the old paths, including relative paths, imports, and links with section anchors. When sections move to different destinations, update those references to the actual destination and verify the anchors.

When retained content moves between directories, rebase its outgoing relative links, image paths, and imports to preserve their targets. If a referenced file or section also moves, use its resulting path and anchor. For example, moving a section from root `CONTEXT.md` to `docs/architecture.md` changes a link to `./src/schema.ts` into `../src/schema.ts`.

References that intentionally describe migration history or legacy compatibility may remain. Report external consumers that cannot be inspected. If a known consumer still requires an old file, resolve that dependency before removal, so the migrated glossary stays the single source of truth.

## Write and verify

For a straightforward rename with no existing destination, verify the preserved content and consumer changes against the planned destination, then use `git mv` for tracked files or a filesystem move for untracked files. For splits or merges, write the destinations and update consumers, then compare them with the source contents before deleting the old file. Throughout, work from the current working-tree contents and leave unrelated edits intact; never restore a source from `HEAD`.

Before removing each old path, verify that every retained section has a destination, glossary definitions retain their meaning, map links and retained outgoing references resolve to their intended files and sections, recorded paths identify the resulting files, and active repository references no longer require the old file. Run the relevant document or consumer checks when available. If preservation or a required consumer update is incomplete, keep the source and report the remaining work.

On a repeat run after migration, read and update the existing glossary and documentation, keeping the migrated glossary as the only one.
