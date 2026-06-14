#!/usr/bin/env python3
"""Validate every SKILL.md and JSON manifest in the repository.

Run by CI (.github/workflows/validate.yml) and usable locally from the repo root:

    python3 .github/scripts/validate_skills.py
"""
import glob
import json
import pathlib
import re
import sys

errors = []

# 1. All JSON manifests must parse.
for pattern in ("**/marketplace.json", "**/plugin.json"):
    for f in glob.glob(pattern, recursive=True):
        try:
            json.loads(pathlib.Path(f).read_text(encoding="utf-8"))
        except Exception as exc:  # noqa: BLE001
            errors.append(f"{f}: invalid JSON: {exc}")

# 2. Every SKILL.md needs YAML frontmatter with a non-empty description.
skills = sorted(glob.glob("**/SKILL.md", recursive=True))
if not skills:
    errors.append("no SKILL.md files found")
for f in skills:
    text = pathlib.Path(f).read_text(encoding="utf-8")
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.S)
    if not m:
        errors.append(f"{f}: missing YAML frontmatter")
        continue
    if not re.search(r"(?m)^description:\s*\S", m.group(1)):
        errors.append(f"{f}: frontmatter missing a 'description:' field")

if errors:
    print("VALIDATION FAILED:")
    for e in errors:
        print(f"  - {e}")
    sys.exit(1)

print(f"OK: validated {len(skills)} skill(s) and all JSON manifests.")
