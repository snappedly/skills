#!/usr/bin/env python3

from pathlib import Path
import json
import os
import re
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
RELEASE_NOTES = "changelog.json"
DOCS_SECTION = re.compile(r"^## Docs site[ \t]*\n(.*?)(?=^## |\Z)", re.DOTALL | re.MULTILINE)
DOCS_PR = re.compile(r"\bsnappedly/snappedly-website(?:#|/pull/)\d+\b")
NO_CHANGE = re.compile(r"^(?:[-*][ \t]+)?No change:[ \t]*\S", re.MULTILINE)
COMMENT = re.compile(r"<!--.*?-->", re.DOTALL)


def newest_release(notes: str) -> str | None:
    releases = json.loads(notes)
    return releases[0]["version"] if releases else None


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: check-release-docs.py <base-ref>, with the pull request body in PR_BODY")
        return 2
    base = subprocess.run(
        ["git", "show", f"{sys.argv[1]}:{RELEASE_NOTES}"], cwd=ROOT, capture_output=True, text=True, check=True
    ).stdout
    release = newest_release((ROOT / RELEASE_NOTES).read_text(encoding="utf-8"))
    if release == newest_release(base):
        print("No new release, so no docs site check.")
        return 0

    body = os.environ.get("PR_BODY", "").replace("\r\n", "\n")
    section = DOCS_SECTION.search(body)
    docs = COMMENT.sub("", section.group(1)) if section else ""
    if DOCS_PR.search(docs) or NO_CHANGE.search(docs):
        print(f"Release {release} states its docs site change.")
        return 0

    print(
        f"Release {release} needs a '## Docs site' section in the pull request description. Link the "
        "snappedly/snappedly-website pull request that updates the Skills pages on docs.snappedly.com, or write "
        "'No change:' and the reason. See Releases in CONTRIBUTING.md."
    )
    return 1


if __name__ == "__main__":
    sys.exit(main())
