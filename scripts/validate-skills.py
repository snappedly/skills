#!/usr/bin/env python3

from pathlib import Path
import re
import sys

try:
    import yaml
except ImportError:
    print("Install validation dependencies with: python -m pip install -r requirements-validation.txt")
    sys.exit(2)


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
FRONTMATTER_KEYS = {
    "allowed-tools",
    "argument-hint",
    "description",
    "disable-model-invocation",
    "license",
    "metadata",
    "name",
}


def frontmatter(path: Path) -> dict[str, object]:
    text = path.read_text()
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


def main() -> int:
    errors: list[str] = []
    seen: dict[str, Path] = {}
    discovered = sorted(SKILLS.rglob("SKILL.md"))
    skill_files = [path for path in discovered if len(path.relative_to(ROOT).parts) == 4]

    if not skill_files:
        errors.append("no skills found under skills/<group>/<name>/SKILL.md")
    for misplaced in set(discovered) - set(skill_files):
        errors.append(
            f"{misplaced.relative_to(ROOT)}: expected skills/<group>/<name>/SKILL.md"
        )

    for skill_file in skill_files:
        relative = skill_file.relative_to(ROOT)
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
        elif name != skill_file.parent.name:
            errors.append(f"{relative}: name '{name}' does not match its directory")
        elif name in seen:
            errors.append(f"{relative}: duplicate name also used by {seen[name]}")
        else:
            seen[name] = relative

        if not isinstance(metadata.get("description"), str) or not metadata["description"]:
            errors.append(f"{relative}: missing description")

        agent_file = skill_file.parent / "agents" / "openai.yaml"
        if not agent_file.exists():
            errors.append(f"{relative}: missing agents/openai.yaml")
            continue

        try:
            agent = yaml.safe_load(agent_file.read_text())
        except yaml.YAMLError as error:
            errors.append(f"{agent_file.relative_to(ROOT)}: invalid YAML: {error}")
            continue
        if not isinstance(agent, dict) or not isinstance(agent.get("interface"), dict):
            errors.append(f"{agent_file.relative_to(ROOT)}: missing interface mapping")
            continue

        policy = agent.get("policy", {})
        if not isinstance(policy, dict):
            errors.append(f"{agent_file.relative_to(ROOT)}: policy must be a mapping")
            continue
        implicit = policy.get("allow_implicit_invocation", True)
        if not isinstance(implicit, bool):
            errors.append(
                f"{agent_file.relative_to(ROOT)}: allow_implicit_invocation must be boolean"
            )
            continue
        disable_value = metadata.get("disable-model-invocation", False)
        if not isinstance(disable_value, bool):
            errors.append(
                f"{relative}: disable-model-invocation must be boolean when present"
            )
            continue
        disabled = disable_value
        if implicit == disabled:
            errors.append(
                f"{relative}: disable-model-invocation and "
                "allow_implicit_invocation disagree"
            )

        prompt = agent["interface"].get("default_prompt")
        if prompt is not None and not isinstance(prompt, str):
            errors.append(f"{agent_file.relative_to(ROOT)}: default_prompt must be a string")
        elif prompt and isinstance(name, str) and f"${name}" not in prompt:
            errors.append(
                f"{agent_file.relative_to(ROOT)}: default_prompt must mention ${name}"
            )

        package_root = skill_file.parent.resolve()
        for markdown_file in sorted(skill_file.parent.rglob("*.md")):
            markdown_relative = markdown_file.relative_to(ROOT)
            prose = re.sub(r"```.*?```", "", markdown_file.read_text(), flags=re.DOTALL)
            for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", prose):
                if re.match(r"^[a-z]+://", target) or target.startswith("#"):
                    continue
                target_path = target.split("#", 1)[0].strip("<>")
                if not target_path:
                    continue
                resolved = (markdown_file.parent / target_path).resolve()
                if not resolved.is_relative_to(package_root):
                    errors.append(
                        f"{markdown_relative}: local link escapes skill package: {target}"
                    )
                elif not resolved.exists():
                    errors.append(f"{markdown_relative}: unresolved link {target}")

    if errors:
        print("\n".join(errors))
        return 1

    print(f"Validated {len(skill_files)} skills.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
