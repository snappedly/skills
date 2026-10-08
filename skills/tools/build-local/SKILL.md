---
name: build-local
description: "Preview the current working tree locally at a verified URL, using a development server or production build and tracking the process you own."
disable-model-invocation: true
license: MIT
---

# Build local

A preview request ends at a usable preview of the working tree, uncommitted changes included. TDD, cleanup, code review, commits, and production or deployment builds run only when the user requested them or the selected preview mode requires them. On follow-up visual edits, reuse the verified server and inspect the changed result; repeat setup only when its inputs changed.

**Process ownership.** You own only the server process you start. Keep an ownership record you can consult later in the session: the background process handle your tools provide when available, otherwise its exact PID and command, plus a precise way to stop it. Stop only owned processes, never by broad name. Leave every other server running, including one whose ownership is unclear, and choose another port.

## Select and prepare

1. Identify the working tree containing the user's changes and the project root within it. Identify the package manager from its manifest and lockfile, then read the scripts and port settings needed for the selected preview mode. Run commands from that working tree so the preview includes its current files.
2. Honor the target and mode named by the user. Otherwise, prefer the project's development server for inspecting edits and iterating. Use a production build and its compatible serve command when the user wants to check built output or the project requires it.
3. Inspect any existing ownership record. Reuse a server only when the working tree, project root, mode, command, PID relationship, port, and URL all match, and verify its freshness as described in the next section before presenting its URL.
4. For production previews, build the current files before serving them. Reuse existing output only when there is evidence its source files, dependencies, and build configuration are unchanged. For development previews, run the preparation required by the project's development command. Keep a last-known-good instance available when the project supports isolated output. Pass the port through the project's supported option or environment variable.

Completion criterion: the working tree, selected target and mode, required preparation or build, serve command, port, and process ownership are recorded before a server starts.

## Coordinate with tests

Before starting a preview that will coexist with browser tests, inspect the test runner's server command, port, reuse/external-URL setting, and framework lock/output directory. Choose one server owner: let tests start their server, or point them at a verified owned preview using the supported configuration. Another port alone may still collide on the framework lock. If tests require exclusive ownership, stop the owned preview first and restore it afterward when the user still needs it.

Completion criterion: each server, port, and framework lock has exactly one owner.

## Serve and verify

Bind to loopback unless the preview runtime requires another setting. Start the server as a background process and record its ownership. Wait only for bounded readiness (use the configured startup timeout, otherwise 60 seconds), then verify the URL with the lightest reliable check; the healthy server keeps running. On startup failure or timeout, inspect the error and ownership before retrying.

Verify that the preview reflects the current changes. For a development server, confirm compilation or reload has completed; restart the owned server when configuration or environment changes require it. Use a browser or preview tool when available to inspect the changed route and representative states. A successful HTTP response alone does not establish that the changed behavior is visible. Report any behavior you could not inspect.

Return a clickable URL and identify the working tree and preview mode. Keep the server available for the user's inspection, and stop it when the user finishes or asks you to stop. If the server cannot keep running after your reply, explain that limitation and provide the command and working directory the user can run locally.

If preparation, build, or verification fails, report the command or check that failed. Preserve any last-known-good URL, but label it as an earlier version rather than a preview of the current changes.

Completion criterion: required preparation or build passed, the URL is reachable, the current changes were verified to the extent the available tools allow, and the server remains available for inspection with process ownership and a stop method recorded. Report unmet criteria as limitations or blockers rather than claiming the preview is ready.
