---
name: resolving-merge-conflicts
description: "Use when you need to resolve an in-progress git merge/rebase conflict."
---

1. **See the current state** of the merge/rebase. Check git history, and the conflicting files.

2. **Find the primary sources** for each conflict. Understand deeply why each change was made, and what the original intent was. Start with the conflicting code and commit messages. Follow PR or issue references when local evidence leaves intent unresolved.

3. **Resolve each hunk.** Preserve both intents where possible. Where they are incompatible, use the merge's agreed goal and primary sources to choose. If those sources do not determine the intended behavior, present the conflict and the available outcomes for user direction. Do not invent behavior or abort the operation.

4. Reuse the caller's check map. Format resolved files before read-only checks, then run affected checks and any repository-required broader validation on the integrated result. Supply results to the caller so cleanup does not repeat checks on unchanged inputs. Fix anything the merge broke.

5. **Finish the merge/rebase.** Inspect `git status` and stage only the resolved paths and other changes that belong to this merge or rebase. Preserve unrelated working-tree and index changes. Commit the merge when Git requires it. If rebasing, continue until all commits are rebased. Return the integrated result to the calling workflow so its affected cleanup checks and review cover the final tree.
