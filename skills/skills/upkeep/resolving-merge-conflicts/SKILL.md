---
name: resolving-merge-conflicts
description: "Use when you need to resolve an in-progress git merge/rebase conflict."
---

1. **See the current state** of the merge/rebase. Check git history, and the conflicting files.

2. **Find the primary sources** for each conflict. Understand deeply why each change was made, and what the original intent was. Read the commit messages, check the PRs, check original issues/tickets.

3. **Resolve each hunk.** Preserve both intents where possible. Where they are incompatible, use the merge's agreed goal and primary sources to choose. If those sources do not determine the intended behavior, present the conflict and the available outcomes for user direction. Do not invent behavior or abort the operation.

4. Discover the project's **automated checks** and run them, typically typecheck, then tests, then format. Fix anything the merge broke.

5. **Finish the merge/rebase.** Inspect `git status` and stage only the resolved paths and other changes that belong to this merge or rebase. Preserve unrelated working-tree and index changes. Commit the merge when Git requires it. If rebasing, continue until all commits are rebased. Return the integrated result to the calling workflow so its affected cleanup checks and review cover the final tree.
