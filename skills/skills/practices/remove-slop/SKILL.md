---
name: remove-slop
description: Remove AI-generated slop from code changes and writing. Use for behavior-preserving code cleanup and meaning-preserving prose edits.
---

# Remove Slop

Clean code and writing without changing behavior, meaning, or the writer's voice.

## Process

1. For code, use the caller's fixed point or compute the task branch's merge-base with its configured base branch. Inspect staged, unstaged, committed, and untracked task files in that scope. For writing, identify the supplied text or document. Keep unrelated material out.
2. Scan the relevant material. Apply the code checks and writing rules below. Use both when the task contains code and prose.
3. Rewrite with the smallest focused edit that fixes the slop. Match the surrounding code and the intended tone.
4. Self-audit. Ask what still makes the result look AI-generated or out of place, then fix any remaining tells.
5. Report the cleanup briefly, including any item you left unchanged because it would alter behavior or meaning.

## Code

- Remove unnecessary comments and comments inconsistent with local style.
- Remove defensive checks or `try`/`catch` blocks that are abnormal for trusted code paths.
- Replace casts to `any` that only bypass type issues with a proper type or a simpler expression.
- Flatten deeply nested code with early returns when that matches local style.
- Remove other patterns inconsistent with the file and surrounding codebase.

Keep code behavior unchanged. Return a possible bug to the implementation workflow, so it receives behavior-level tests, cleanup, and review. Prefer minimal, focused edits over broad rewrites. Keep the final summary concise, from one to three sentences.

## Writing

Rule numbers are stable ids that other skills cite. A removed rule leaves a gap.

### Content

3. **Superficial -ing phrases.** "highlighting...", "ensuring...", "reflecting...", "showcasing...", "fostering...". Delete or expand with real sources.
5. **Vague attributions.** "Experts believe", "Industry reports suggest", "Some critics argue". Name the source or delete.

### Language

7. **AI vocabulary.** Additionally, crucial, delve, enduring, enhance, fostering, garner, interplay, intricate, landscape (abstract), pivotal, showcase, tapestry (abstract), testament, underscore, vibrant. Replace with plain words.
8. **Fancy ways to say "is".** "serves as", "stands as", "boasts", "features". Just say "is" or "has".
9. **"Not just X, but Y."** State the point directly instead.
10. **Rule of three.** Do not force ideas into groups of three. Use the natural number.
11. **Synonym cycling.** Protagonist, main character, central figure, hero all in one paragraph. Pick one and repeat it.
12. **False ranges.** "from X to Y" where X and Y are not on a meaningful scale. List topics directly.

### Style

13. **Em dash overuse.** Avoid em dashes entirely. Use periods or commas only. If a thought needs separation, end the sentence or use a comma.
14. **Colon overuse.** Colons are fine before a list or example. Do not use them as mid-sentence connectors. "If you're coming from traditional automation: instead of registering event handlers, you describe conditions" adds nothing with the colon. Rewrite to let the point stand on its own. "Describing when the scheduler should fire works best as plain English." Same meaning, no crutch punctuation.
15. **Boldface overuse.** Do not bold every proper noun or acronym.
16. **Inline-header lists.** A bold label and colon that restates the line, such as "**Performance:** Performance improved...", is a tell. Convert it to prose. A bold lead-in that ends in a period, names the item, and is followed by genuinely new detail, such as "**Schema in TypeScript.** Tables live in one file.", is fine.
17. **Title case headings.** Use sentence case.
18. **Decorative emojis.** Remove them from headings and bullets.
19. **Curly quotes.** Replace them with straight quotes.

### Communication artifacts

20. **Chatbot phrases.** Remove "I hope this helps!", "Let me know if...", "Of course!", "Certainly!", and "Found the smoking gun!".
22. **Sycophantic tone.** Remove phrases such as "Great question! You're absolutely right!". Respond directly.

### Filler

23. **Filler phrases.** Change "In order to" to "To" and "Due to the fact that" to "Because". Delete "It is important to note that".
24. **Excessive hedging.** Change "could potentially possibly be argued that it might" to "may".
25. **Generic conclusions.** State specific plans or facts instead of phrases such as "The future looks bright."

### Jargon

26. **Abstract metaphor nouns.** Substrate, wedge, vector, locus, vantage, nexus, primitive (as a noun), harness (as a metaphor), surface (as in "API surface"), bedrock, scaffolding (as a metaphor), modality, paradigm, gold-plating, ratchet (as a metaphor), evacuate (for moving code), endgame, north star, flywheel. Replace them with concrete words. "Substrate" becomes "base". "Wedge in" becomes "add". "Vector" becomes "way" or "method". "Gold-plating" becomes "more than the job needs". "Ratchet" becomes the mechanism's real name or "a limit that only tightens". "Evacuate" becomes "move out".

### Plain speech

27. **Say what it does, not how it feels.** Replace phrases such as "the database stays close at hand", "SQL you can read", and "types that follow your schema" with the mechanism or a number. For example, "`.toSQL()` returns the exact string sent to the database" and "a column rename fails the build". Ask what the sentence tells the reader to do or know. If you cannot restate it as a concrete instruction, fact, or number, cut it. If a sentence could appear unchanged in another project's docs, it says nothing about this project. Cut it.
28. **Shorten or split dense sentences.** If the reader has to backtrack, break the sentence in two or drop clauses. Use one idea per sentence.
29. **Active voice.** Prefer it. Change "queries are validated" to "the compiler validates queries" and "the file is parsed by the loader" to "the loader parses the file". Passive is fine when the actor is unknown or does not matter.
30. **Cut adverbs, or use a stronger verb.** Change "runs quickly" to "is fast" or give the number. Change "significantly improves" to the measured delta. An adverb propping up a weak verb means the verb is wrong.
31. **Prefer the plain word.** Change "utilize" and "leverage" to "use", "facilitate" to "help", "numerous" to "many", and "in the event that" to "if".
32. **Mannered prose.** Replace metaphor or flourish with a literal phrase. Avoid aphorisms such as "wire it or delete it", rhetorical fragments for effect, personified code, figurative verbs, and stock framing phrases. "A dial worth turning" becomes "a parameter worth varying". Say what you mean.
33. **Over-compression.** Add articles and verbs when shorthand makes the reader decode the sentence. Change "Parser rejects bad date → exit 2, no write" to "The parser rejects a bad date, exits with code 2, and writes nothing." Spell out arrows and abbreviations.
