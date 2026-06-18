#!/usr/bin/env python3
"""Validate a local Agent Skill folder with lightweight checks."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


NAME_RE = re.compile(r"^[a-z0-9](?:[a-z0-9-]{0,62}[a-z0-9])?$")


def parse_frontmatter(text: str) -> tuple[dict[str, str], list[str]]:
    errors: list[str] = []
    if not text.startswith("---\n"):
        return {}, ["SKILL.md must start with YAML frontmatter delimiter '---'."]

    end = text.find("\n---", 4)
    if end == -1:
        return {}, ["SKILL.md frontmatter must close with '---'."]

    frontmatter = text[4:end].strip().splitlines()
    values: dict[str, str] = {}
    for line in frontmatter:
        if not line.strip():
            continue
        if ":" not in line:
            errors.append(f"Invalid frontmatter line: {line}")
            continue
        key, value = line.split(":", 1)
        values[key.strip()] = value.strip().strip('"').strip("'")
    return values, errors


def validate(skill_path: Path) -> list[str]:
    errors: list[str] = []
    skill_path = skill_path.resolve()

    if not skill_path.exists():
        return [f"Skill folder does not exist: {skill_path}"]
    if not skill_path.is_dir():
        return [f"Skill path is not a directory: {skill_path}"]

    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        return [f"Missing required file: {skill_md}"]

    folder_name = skill_path.name
    if not NAME_RE.match(folder_name) or "--" in folder_name:
        errors.append("Folder name must use lowercase letters, numbers, and single hyphens only.")

    values, fm_errors = parse_frontmatter(skill_md.read_text(encoding="utf-8"))
    errors.extend(fm_errors)

    name = values.get("name", "")
    description = values.get("description", "")

    if not name:
        errors.append("Missing required frontmatter field: name")
    elif name != folder_name:
        errors.append(f"Frontmatter name '{name}' must match folder name '{folder_name}'.")
    elif not NAME_RE.match(name) or "--" in name:
        errors.append("Frontmatter name must use lowercase letters, numbers, and single hyphens only.")

    if not description:
        errors.append("Missing required frontmatter field: description")
    elif len(description) > 1024:
        errors.append("Description must be 1024 characters or fewer.")
    elif len(description.split()) < 12:
        errors.append("Description is probably too vague; include what the skill does and when to use it.")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a local Agent Skill folder.")
    parser.add_argument("skill_folder", help="Path to the skill folder to validate")
    args = parser.parse_args()

    errors = validate(Path(args.skill_folder))
    if errors:
        print("Skill validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Skill validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
