#!/usr/bin/env bash
# Human-in-the-loop reproduction loop.
# The agent copies this file and edits the steps below. The user runs the copy
# in their own terminal, since its prompts need someone to answer them:
#
#   bash <path-to-copy>
#
# then pastes the "Captured" block it prints at the end back to the agent.
#
# Three helpers:
#   step "<instruction>"           → show instruction, wait for Enter
#   capture VAR "<question>"       → read a one-line answer into VAR
#   capture_paste VAR "<request>"  → read a multi-line paste into VAR, up to a
#                                    line containing only END
#
# The Captured block prints a one-line value as KEY=VALUE and a multi-line
# value as KEY<<END, its lines, then END.
#
# The user pastes captured values back to the agent, so capture observations,
# and leave signing in to the user as a `step`.

set -euo pipefail

CAPTURED=()
LINE=""

# _read reads one line into LINE. If input runs out, as it does when no one is
# at a terminal to answer, it stops the loop with instructions.
_read() {
  LINE=""
  if IFS= read -r LINE || [[ -n "$LINE" ]]; then
    LINE="${LINE%$'\r'}"
    return 0
  fi
  printf '\n!!! Input ended before the loop finished. Run it in your own terminal\n' >&2
  printf '!!! and answer every prompt:  bash %s\n' "$0" >&2
  exit 1
}

step() {
  printf '\n>>> %s\n    [Enter when done] ' "$1"
  _read
}

capture() {
  printf '\n>>> %s\n    > ' "$2"
  _read
  printf -v "$1" '%s' "$LINE"
  CAPTURED+=("$1")
}

capture_paste() {
  local text=""
  printf '\n>>> %s\n    (paste it, then type END on its own line)\n' "$2"
  while _read && [[ "$LINE" != "END" ]]; do
    text="${text:+$text$'\n'}$LINE"
  done
  printf -v "$1" '%s' "$text"
  CAPTURED+=("$1")
}

print_captured() {
  local key value
  printf '\n--- Captured: paste from here to the '--- End captured ---' line back to the agent ---\n'
  for key in ${CAPTURED[@]+"${CAPTURED[@]}"}; do
    value="${!key}"
    if [[ "$value" == *$'\n'* ]]; then
      printf '%s<<END\n%s\nEND\n' "$key" "$value"
    else
      printf '%s=%s\n' "$key" "$value"
    fi
  done
  printf -- '--- End captured ---\n'
}

# --- edit below ---------------------------------------------------------

step "Open the app at http://localhost:3000 and sign in."

capture ERRORED "Click the 'Export' button. Did it throw an error? (y/n)"

capture_paste ERROR_MSG "Paste the error message (or 'none'):"

# --- edit above ---------------------------------------------------------

print_captured
