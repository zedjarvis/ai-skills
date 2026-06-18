#!/usr/bin/env python3
"""Validate the expected shape of a generated TypeScript monorepo."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


REQUIRED_PATHS = [
    "package.json",
    "pnpm-workspace.yaml",
    "turbo.json",
    "apps/frontend/package.json",
    "apps/backend/package.json",
    "packages/shared/package.json",
    "packages/ts-config/package.json",
]


def read_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError as exc:
        raise ValueError(f"{path} is not valid JSON: {exc}") from exc


def validate(root: Path) -> list[str]:
    errors: list[str] = []
    root = root.resolve()

    if not root.exists() or not root.is_dir():
        return [f"Not a directory: {root}"]

    for relative_path in REQUIRED_PATHS:
        if not (root / relative_path).exists():
            errors.append(f"Missing {relative_path}")

    package_json = read_json(root / "package.json")
    if package_json.get("private") is not True:
        errors.append("Root package.json must set private: true")

    scripts = package_json.get("scripts", {})
    for script_name in ("dev", "build", "lint", "typecheck"):
        if script_name not in scripts:
            errors.append(f"Root package.json missing script: {script_name}")

    turbo_json = read_json(root / "turbo.json")
    if "pipeline" in turbo_json:
        errors.append("turbo.json uses stale 'pipeline' key; use 'tasks'")
    if "tasks" not in turbo_json:
        errors.append("turbo.json must define 'tasks'")

    workspace_yaml = (root / "pnpm-workspace.yaml").read_text(encoding="utf-8") if (root / "pnpm-workspace.yaml").exists() else ""
    for expected in ('"apps/*"', "'apps/*'", "- apps/*", "- \"apps/*\"", "- 'apps/*'"):
        if expected in workspace_yaml:
            break
    else:
        errors.append("pnpm-workspace.yaml must include apps/*")
    for expected in ('"packages/*"', "'packages/*'", "- packages/*", "- \"packages/*\"", "- 'packages/*'"):
        if expected in workspace_yaml:
            break
    else:
        errors.append("pnpm-workspace.yaml must include packages/*")

    for package in ("apps/frontend", "apps/backend", "packages/shared", "packages/ts-config"):
        package_json_path = root / package / "package.json"
        if package_json_path.exists():
            data = read_json(package_json_path)
            if not data.get("name"):
                errors.append(f"{package}/package.json missing name")

    for consumer in ("apps/frontend", "apps/backend"):
        data = read_json(root / consumer / "package.json")
        dependencies = data.get("dependencies", {}) | data.get("devDependencies", {})
        if "@repo/shared" in dependencies and dependencies["@repo/shared"] != "workspace:*":
            errors.append(f"{consumer} must depend on @repo/shared using workspace:*")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a generated TypeScript monorepo.")
    parser.add_argument("repo", help="Path to the generated monorepo root")
    args = parser.parse_args()

    try:
        errors = validate(Path(args.repo))
    except ValueError as exc:
        print(f"Validation failed: {exc}")
        return 1

    if errors:
        print("Monorepo validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Monorepo validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
