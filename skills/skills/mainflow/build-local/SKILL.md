---
name: build-local
description: "Preview the current working tree locally at a verified URL, using a development server or production build and tracking the process you own."
disable-model-invocation: true
---

# Build local

Use this when the user wants to inspect current changes, including uncommitted changes, in a browser or at a local URL.

## Select and prepare

1. Identify the working tree containing the user's changes and the project root within it. Read its manifest, package-manager lockfile, development scripts, build scripts, preview scripts, and port settings. Run commands from that working tree so the preview includes its current files.
2. Honor the target and mode named by the user. Otherwise, prefer the project's development server for inspecting edits and iterating. Use a production build and its compatible serve command when the user wants to check built output or the project requires it.
3. Inspect any existing task-owned lease or process record. Reuse a server only when the working tree, project root, mode, command, PID relationship, port, and URL all match. Verify freshness in the next section before presenting a reused URL. If ownership is unclear, leave the process alone and choose another port.
4. For production previews, build the current files before serving them. Reuse existing output only when there is evidence its source files, dependencies, and build configuration are unchanged. For development previews, run the preparation required by the project's development command. Keep a last-known-good instance available when the project supports isolated output. Pass the port through the project's supported option or environment variable.

Completion criterion: the working tree, selected target and mode, required preparation or build, serve command, port, and process ownership are recorded before a server starts.

## Serve and verify

Bind to loopback unless the preview runtime requires another setting. Retain the process handle or record the exact PID and command. Wait for readiness and verify the URL with the lightest reliable check.

Verify that the preview reflects the current changes. For a development server, confirm compilation or reload has completed; restart the owned server when configuration or environment changes require it. Use browser or collaborative preview tools when available to inspect the changed route and representative states. A successful HTTP response alone does not establish that the changed behavior is visible. Report any behavior you could not inspect.

Return a clickable URL and identify the working tree and preview mode. A request to inspect the preview includes keeping the server available for the user's inspection. Use a runtime-managed session or lease when available; otherwise retain the owned process handle and provide a precise way to stop it. Stop it when the user finishes or asks you to stop. If the runtime cannot keep it available after the turn, explain that limitation and provide the command and working directory the user can run locally.

Never kill processes by broad name or stop another project's server. If preparation, build, or verification fails, report the command or check that failed. Preserve any last-known-good URL, but label it as an earlier version rather than a preview of the current changes.

Completion criterion: required preparation or build passed, the URL is reachable, the current changes were verified to the extent the available tools allow, and the server remains available for inspection with process ownership and a stop method recorded. Report unmet criteria as limitations or blockers rather than claiming the preview is ready.
