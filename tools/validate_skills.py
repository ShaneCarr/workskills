#!/usr/bin/env python3
"""Validate portable skill package structure and metadata."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
NAME = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
ALLOWED_FIELDS = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}


def parse_frontmatter(path: Path) -> dict[str, str]:
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0] != "---":
        raise ValueError("missing opening frontmatter delimiter")
    try:
        end = lines.index("---", 1)
    except ValueError as error:
        raise ValueError("missing closing frontmatter delimiter") from error
    metadata = {}
    for line in lines[1:end]:
        if not line.strip():
            continue
        key, separator, value = line.partition(":")
        if not separator:
            raise ValueError(f"invalid frontmatter line: {line}")
        metadata[key.strip()] = value.strip()
    return metadata


def validate() -> list[str]:
    errors = []
    seen = set()
    for directory in sorted(path for path in SKILLS.iterdir() if path.is_dir()):
        skill = directory / "SKILL.md"
        if not skill.is_file():
            errors.append(f"{directory.name}: missing SKILL.md")
            continue
        try:
            metadata = parse_frontmatter(skill)
        except ValueError as error:
            errors.append(f"{directory.name}: {error}")
            continue
        name = metadata.get("name", "")
        if name != directory.name:
            errors.append(f"{directory.name}: frontmatter name is {name!r}")
        if not NAME.fullmatch(name):
            errors.append(f"{directory.name}: invalid portable skill name")
        if name in seen:
            errors.append(f"{directory.name}: duplicate name")
        seen.add(name)
        if not metadata.get("description"):
            errors.append(f"{directory.name}: missing description")
        if len(name) > 64:
            errors.append(f"{directory.name}: name exceeds 64 characters")
        if len(metadata.get("description", "")) > 1024:
            errors.append(f"{directory.name}: description exceeds 1024 characters")
        if metadata.get("license") != "MIT":
            errors.append(f"{directory.name}: license must be MIT")
        unknown = set(metadata) - ALLOWED_FIELDS
        if unknown:
            errors.append(f"{directory.name}: unknown frontmatter fields {sorted(unknown)}")
    return errors


def main() -> int:
    errors = validate()
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print(f"Validated {len(list(SKILLS.glob('*/SKILL.md')))} skills.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
