---
name: resolving-merge-conflicts
description: "Resolve conflicts in an in-progress git merge or rebase."
license: MIT
---

# Resolving merge conflicts

1. **See the current state** of the merge/rebase. Check git history and the conflicting files. Done when you know which operation is in progress and every file in conflict.

2. **Find the primary sources** for each conflict. Start with the conflicting code and commit messages. Follow PR or issue references when local evidence leaves intent unresolved. Done when you can state why each side of every conflicting hunk was changed.

3. **Resolve each hunk.** Preserve both intents where possible. Where they are incompatible, use the merge's agreed goal and primary sources to choose. If those sources do not determine the intended behavior, keep the operation in progress, present the conflict and the available outcomes for user direction, and stop until the user decides. Done when every hunk is resolved, or the undetermined ones are presented and the run is paused for the user.

4. **Check the integrated result.** Reuse the caller's check map when it supplies one. Format resolved files before read-only checks, then run affected checks and any repository-required broader validation on the integrated result. Fix anything the merge broke. When rebasing, run this step once, after the last commit is rebased, not on each intermediate commit. Done when the affected checks pass or each remaining failure is recorded.

5. **Finish the merge/rebase.** Inspect `git status` and stage only the resolved paths and other changes that belong to this merge or rebase. Preserve unrelated working-tree and index changes. Commit the merge when Git requires it. If rebasing, continue the rebase and repeat steps 1–3 for each later commit that conflicts; once every commit is rebased, run step 4 on the final tree. When another workflow called this skill, return the integrated result and check results to it, so its cleanup reuses checks on unchanged inputs and its review covers the final tree; when invoked directly, report them to the user. Done when `git status` shows no merge or rebase in progress, step 4 has run on the final tree, and its results are returned or reported.
