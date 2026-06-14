#!/usr/bin/env python3
"""Validate every SKILL.md and JSON manifest in the repository.

Run by CI (.github/workflows/validate.yml) and usable locally from the repo root:

    python3 .github/scripts/validate_skills.py
"""
import json
import pathlib
import re
import sys

errors = []


def find(name):
    """Find files by name anywhere in the tree, including hidden dirs like
    .claude-plugin/ (glob.glob skips dot-directories; pathlib.rglob does not),
    but excluding the .git directory."""
    return sorted(
        p for p in pathlib.Path(".").rglob(name) if ".git" not in p.parts
    )


# 1. All JSON manifests must parse — and there must be at least one.
manifests = find("marketplace.json") + find("plugin.json")
if not manifests:
    errors.append("no marketplace.json/plugin.json manifests found")
for f in manifests:
    try:
        json.loads(f.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        errors.append(f"{f}: invalid JSON: {exc}")

# 2. Every SKILL.md needs YAML frontmatter with a non-empty description.
skills = find("SKILL.md")
if not skills:
    errors.append("no SKILL.md files found")
for f in skills:
    text = f.read_text(encoding="utf-8")
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

print(f"OK: validated {len(skills)} skill(s) and {len(manifests)} JSON manifest(s).")
