---
name: research
description: Investigate a substantive question against primary sources and capture cited findings. Use for requested research reports or delegated reading; answer a single factual lookup directly.
license: MIT
---

Delegate one bounded research question to a subagent only when the user asks for background work or you have independent work to continue. An agent assigned research does the reading itself.

1. Investigate the question against **primary sources** (official docs, source code, specs, first-party APIs). Follow every claim back to the source that owns it, and keep to the question asked.
2. Write the findings as Markdown, citing each claim's source.
3. When the caller asked for the findings back, return them. Otherwise save them as a single file where the repo already keeps such notes; with no convention, choose a location and report the path.

Done when every part of the question is answered from a cited primary source or reported as open with what is missing, and the findings are returned or saved.
