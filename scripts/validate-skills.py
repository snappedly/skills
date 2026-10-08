#!/usr/bin/env python3

from pathlib import Path
from urllib.parse import unquote
import json
import re
import sys

try:
    import yaml
except ImportError:
    print("Install validation dependencies with: python -m pip install -r requirements-validation.txt")
    sys.exit(2)


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
README = ROOT / "README.md"
FRONTMATTER_KEYS = {
    "allowed-tools",
    "argument-hint",
    "compatibility",
    "description",
    "disable-model-invocation",
    "license",
    "metadata",
    "name",
}
SKILL_NAME = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")
MAX_NAME_LENGTH = 64
MAX_DESCRIPTION_LENGTH = 1024
MAX_COMPATIBILITY_LENGTH = 500
# Codex shows short_description in its skill list and expects 25 to 64 characters.
SHORT_DESCRIPTION_LENGTHS = (25, 64)
LINK_TARGETS = (
    # Inline links and images, with an optional <target> wrapper and title.
    re.compile(r"!?\[[^\]]*\]\(\s*(<[^>\n]*>|[^)\s]+)(?:\s+(?:\"[^\"]*\"|'[^']*'|\([^)]*\)))?\s*\)"),
    # Reference-style definitions, such as [label]: target. Footnotes are skipped.
    re.compile(r"^ {0,3}\[(?!\^)[^\]]+\]:[ \t]*(<[^>\n]*>|\S+)", re.MULTILINE),
    # HTML href and src attributes.
    re.compile(r"\b(?:href|src)\s*=\s*[\"']([^\"']+)[\"']", re.IGNORECASE),
)
URI_SCHEME = re.compile(r"[a-z][a-z0-9+.-]*:", re.IGNORECASE)
RELEASE_NOTES = ROOT / "changelog.json"
CHANGE_TYPES = {"feature", "improvement", "fix", "security", "deprecation"}
PRIVATE_TEXT = re.compile(
    r"//|www\.|\b(?:github\.com|gitlab\.com|bitbucket\.org)\b|@[\w-]+|\b(?:PR|pull request)\s*#?\d+"
    r"|\(#\d+\)|\[[^\]]*\]\s*[(\[]|<[^>]+>|[\r\n]",
    re.IGNORECASE,
)


def frontmatter(path: Path) -> dict[str, object]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError("missing opening frontmatter delimiter")

    try:
        header, _ = text[4:].split("\n---\n", 1)
    except ValueError as error:
        raise ValueError("missing closing frontmatter delimiter") from error

    try:
        values = yaml.safe_load(header)
    except yaml.YAMLError as error:
        raise ValueError(f"invalid YAML: {error}") from error
    if not isinstance(values, dict):
        raise ValueError("frontmatter must be a mapping")
    return values


def public_text(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip()) and not PRIVATE_TEXT.search(value)


def validate_links(markdown_file: Path, package_root: Path, errors: list[str]) -> None:
    relative = markdown_file.relative_to(ROOT)
    prose = re.sub(r"(```|~~~).*?\1", "", markdown_file.read_text(encoding="utf-8"), flags=re.DOTALL)
    prose = re.sub(r"`[^`\n]*`", "", prose)
    for pattern in LINK_TARGETS:
        for target in pattern.findall(prose):
            target = target.strip("<>").strip()
            if not target or target.startswith(("#", "//")) or URI_SCHEME.match(target):
                continue
            target_path = unquote(re.split(r"[?#]", target, maxsplit=1)[0])
            resolved = (markdown_file.parent / target_path).resolve()
            if not resolved.is_relative_to(package_root):
                errors.append(f"{relative}: local link escapes skill package: {target}")
            elif not resolved.exists():
                errors.append(f"{relative}: unresolved link {target}")


def validate_release_notes(errors: list[str]) -> None:
    name = RELEASE_NOTES.name
    try:
        notes = json.loads(RELEASE_NOTES.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        errors.append(f"{name}: {error}")
        return
    if not isinstance(notes, list):
        errors.append(f"{name}: expected an array of releases")
        return

    versions: set[str] = set()
    previous = None
    for index, note in enumerate(notes):
        label = f"{name}[{index}]"
        if not isinstance(note, dict) or set(note) != {"version", "title", "changes"}:
            errors.append(f"{label}: expected exactly version, title, and changes")
            continue
        version = note["version"]
        if not isinstance(version, str) or not re.fullmatch(r"\d+\.\d+\.\d+", version):
            errors.append(f"{label}: version must look like 1.2.3")
        elif version in versions:
            errors.append(f"{label}: duplicate version {version}")
        else:
            versions.add(version)
            release = tuple(int(part) for part in version.split("."))
            if previous and release > previous[0]:
                errors.append(
                    f"{label}: version {version} is newer than {previous[1]} above it; list releases newest first"
                )
            previous = (release, version)
        if not public_text(note["title"]):
            errors.append(f"{label}: title must be plain customer-facing text")
        changes = note["changes"]
        if not isinstance(changes, list) or not changes:
            errors.append(f"{label}: changes must be a non-empty array")
            continue
        for change in changes:
            if not isinstance(change, dict) or set(change) != {"type", "summary"}:
                errors.append(f"{label}: each change needs exactly type and summary")
            elif not isinstance(change["type"], str) or change["type"] not in CHANGE_TYPES:
                errors.append(f"{label}: change type must be one of {sorted(CHANGE_TYPES)}")
            elif not public_text(change["summary"]):
                errors.append(
                    f"{label}: summaries must be plain customer-facing text without links or attribution"
                )

    released = re.search(r"^## \[(\d+\.\d+\.\d+)\]", (ROOT / "CHANGELOG.md").read_text(encoding="utf-8"), re.MULTILINE)
    if released and released.group(1) not in versions:
        errors.append(f"{name}: missing public release notes for {released.group(1)}, the latest CHANGELOG.md release")


def main() -> int:
    errors: list[str] = []
    seen: dict[str, Path] = {}
    discovered = sorted(SKILLS.rglob("SKILL.md"))
    def well_placed(path: Path) -> bool:
        return len(path.relative_to(ROOT).parts) == 4

    skill_files = [path for path in discovered if well_placed(path)]

    if not skill_files:
        errors.append("no skills found under skills/<group>/<name>/SKILL.md")
    for misplaced in set(discovered) - set(skill_files):
        errors.append(
            f"{misplaced.relative_to(ROOT)}: expected skills/<group>/<name>/SKILL.md"
        )

    for agent_file in sorted(SKILLS.rglob("agents/openai.yaml")):
        if not (agent_file.parent.parent / "SKILL.md").exists():
            errors.append(f"{agent_file.relative_to(ROOT)}: package directory has no SKILL.md")

    for skill_file in skill_files:
        relative = skill_file.relative_to(ROOT)
        package_root = skill_file.parent.resolve()
        for markdown_file in sorted(skill_file.parent.rglob("*.md")):
            validate_links(markdown_file, package_root, errors)

        try:
            metadata = frontmatter(skill_file)
        except ValueError as error:
            errors.append(f"{relative}: {error}")
            continue

        unexpected = set(metadata) - FRONTMATTER_KEYS
        if unexpected:
            errors.append(f"{relative}: unsupported frontmatter keys {sorted(unexpected)}")

        name = metadata.get("name")
        if not isinstance(name, str) or not name:
            errors.append(f"{relative}: missing name")
        elif not SKILL_NAME.fullmatch(name) or len(name) > MAX_NAME_LENGTH:
            errors.append(
                f"{relative}: name '{name}' must be at most {MAX_NAME_LENGTH} characters of "
                "lowercase letters, digits, and single hyphens between them"
            )
        elif name != skill_file.parent.name:
            errors.append(f"{relative}: name '{name}' does not match its directory")
        elif name in seen:
            errors.append(f"{relative}: duplicate name also used by {seen[name]}")
        else:
            seen[name] = relative

        description = metadata.get("description")
        if not isinstance(description, str) or not description.strip():
            errors.append(f"{relative}: missing description")
        else:
            if len(description) > MAX_DESCRIPTION_LENGTH:
                errors.append(
                    f"{relative}: description is {len(description)} characters; the limit is {MAX_DESCRIPTION_LENGTH}"
                )
            if "<" in description or ">" in description:
                errors.append(f"{relative}: description must not contain < or >")

        compatibility = metadata.get("compatibility")
        if compatibility is not None and (
            not isinstance(compatibility, str)
            or not compatibility.strip()
            or len(compatibility) > MAX_COMPATIBILITY_LENGTH
        ):
            errors.append(
                f"{relative}: compatibility must be 1 to {MAX_COMPATIBILITY_LENGTH} characters when present"
            )

        # `npx skills add` copies only the skill folder, so each one carries its own notices.
        if metadata.get("license") != "MIT":
            errors.append(f"{relative}: license must be MIT")
        license_file = skill_file.parent / "LICENSE.txt"
        if not license_file.exists():
            errors.append(f"{relative}: missing LICENSE.txt")
        elif "Copyright (c) 2026 Snappedly" not in license_file.read_text(encoding="utf-8"):
            errors.append(f"{license_file.relative_to(ROOT)}: missing the Snappedly copyright notice")

        agent_file = skill_file.parent / "agents" / "openai.yaml"
        agent_relative = agent_file.relative_to(ROOT)
        if not agent_file.exists():
            errors.append(f"{relative}: missing agents/openai.yaml")
            continue

        try:
            agent = yaml.safe_load(agent_file.read_text(encoding="utf-8"))
        except yaml.YAMLError as error:
            errors.append(f"{agent_relative}: invalid YAML: {error}")
            continue
        if not isinstance(agent, dict) or not isinstance(agent.get("interface"), dict):
            errors.append(f"{agent_relative}: missing interface mapping")
            continue

        interface = agent["interface"]
        for key in ("display_name", "short_description"):
            if not isinstance(interface.get(key), str) or not interface[key].strip():
                errors.append(f"{agent_relative}: interface.{key} must be a non-empty string")
        short_description = interface.get("short_description")
        shortest, longest = SHORT_DESCRIPTION_LENGTHS
        if isinstance(short_description, str) and not shortest <= len(short_description) <= longest:
            errors.append(
                f"{agent_relative}: interface.short_description is {len(short_description)} characters; "
                f"use {shortest} to {longest}"
            )

        policy = agent.get("policy", {})
        if not isinstance(policy, dict):
            errors.append(f"{agent_relative}: policy must be a mapping")
            continue
        implicit = policy.get("allow_implicit_invocation", True)
        if not isinstance(implicit, bool):
            errors.append(f"{agent_relative}: allow_implicit_invocation must be boolean")
            continue
        disable_value = metadata.get("disable-model-invocation", False)
        if not isinstance(disable_value, bool):
            errors.append(
                f"{relative}: disable-model-invocation must be boolean when present"
            )
            continue
        if implicit == disable_value:
            errors.append(
                f"{relative}: disable-model-invocation and "
                "allow_implicit_invocation disagree"
            )

        prompt = interface.get("default_prompt")
        if prompt is not None and not isinstance(prompt, str):
            errors.append(f"{agent_relative}: default_prompt must be a string")
        elif prompt and isinstance(name, str) and f"${name}" not in prompt:
            errors.append(f"{agent_relative}: default_prompt must mention ${name}")

    readme = README.read_text(encoding="utf-8")
    for name in sorted(seen):
        if f"`{name}`" not in readme:
            errors.append(f"{README.name}: missing skill `{name}`")

    validate_release_notes(errors)

    if errors:
        print("\n".join(errors))
        return 1

    print(f"Validated {len(skill_files)} skills and {RELEASE_NOTES.name}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
