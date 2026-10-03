#!/usr/bin/env python3
"""Validate the data-expedition skill and package it as dist/data-expedition.skill.

Usage:
    python scripts/build_skill.py            # validate, then build the .skill file
    python scripts/build_skill.py --check    # validate only (used in CI)

The .skill file is a zip archive with the skill folder at its root, ready to be
uploaded in claude.ai (Settings -> Skills). Builds are deterministic: file
order and timestamps are fixed, so rebuilding unchanged sources yields an
identical archive.
"""

import json
import re
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL_DIR = ROOT / "skills" / "data-expedition"
DIST = ROOT / "dist"
EXCLUDE_DIRS = {"evals", "__pycache__", "node_modules"}
ALLOWED_KEYS = {"name", "description", "license", "allowed-tools", "metadata", "compatibility"}
FIXED_TIME = (2026, 1, 1, 0, 0, 0)


def fail(errors):
    for e in errors:
        print(f"ERROR: {e}")
    sys.exit(1)


def parse_frontmatter(text):
    m = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not m:
        return None
    raw = m.group(1)
    try:
        import yaml  # type: ignore

        data = yaml.safe_load(raw)
        return data if isinstance(data, dict) else None
    except ImportError:
        # Minimal fallback: single-line "key: value" pairs only.
        data = {}
        for line in raw.splitlines():
            k, sep, v = line.partition(":")
            if sep:
                data[k.strip()] = v.strip()
        return data


def validate():
    errors = []
    skill_md = SKILL_DIR / "SKILL.md"
    if not skill_md.is_file():
        fail([f"missing {skill_md}"])

    text = skill_md.read_text(encoding="utf-8")
    fm = parse_frontmatter(text)
    if fm is None:
        fail(["SKILL.md: invalid or missing YAML frontmatter"])

    extra = set(fm) - ALLOWED_KEYS
    if extra:
        errors.append(f"SKILL.md: unexpected frontmatter keys: {sorted(extra)}")

    name = str(fm.get("name", "")).strip()
    if name != SKILL_DIR.name:
        errors.append(f"SKILL.md: name '{name}' must equal folder name '{SKILL_DIR.name}'")
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", name) or len(name) > 64:
        errors.append(f"SKILL.md: invalid name '{name}'")

    desc = str(fm.get("description", "")).strip()
    if not desc:
        errors.append("SKILL.md: empty description")
    if len(desc) > 1024:
        errors.append(f"SKILL.md: description is {len(desc)} chars (max 1024)")
    if "<" in desc or ">" in desc:
        errors.append("SKILL.md: description must not contain angle brackets")

    compat = str(fm.get("compatibility", ""))
    if len(compat) > 500:
        errors.append(f"SKILL.md: compatibility is {len(compat)} chars (max 500)")

    lines = text.count("\n") + 1
    if lines > 500:
        errors.append(f"SKILL.md: {lines} lines (keep under 500)")

    # Every references/ file mentioned in SKILL.md must exist, and vice versa.
    mentioned = set(re.findall(r"references/([A-Za-z0-9_.-]+\.md)", text))
    present = {p.name for p in (SKILL_DIR / "references").glob("*.md")}
    for missing in sorted(mentioned - present):
        errors.append(f"SKILL.md references missing file references/{missing}")
    for orphan in sorted(present - mentioned):
        errors.append(f"references/{orphan} is not mentioned in SKILL.md")

    nested = [p for p in SKILL_DIR.rglob("SKILL.md") if p != skill_md]
    if nested:
        errors.append(f"nested SKILL.md files are not allowed: {nested}")

    # JSON files parse, and versions agree.
    versions = {}
    for rel in (".claude-plugin/plugin.json", ".claude-plugin/marketplace.json",
                "skills/data-expedition/evals/evals.json",
                "skills/data-expedition/evals/trigger-evals.json"):
        p = ROOT / rel
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
        except Exception as exc:  # noqa: BLE001
            errors.append(f"{rel}: {exc}")
            continue
        if rel.endswith("plugin.json"):
            versions["plugin.json"] = data.get("version")
        if rel.endswith("marketplace.json"):
            versions["marketplace.json"] = data["plugins"][0].get("version")

    changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    m = re.search(r"^## \[(\d+\.\d+\.\d+)\]", changelog, re.MULTILINE)
    versions["CHANGELOG.md"] = m.group(1) if m else None
    if len(set(versions.values())) != 1:
        errors.append(f"version mismatch: {versions}")

    if errors:
        fail(errors)
    print(f"OK: skill '{name}' is valid (version {versions['plugin.json']}, "
          f"{lines} lines in SKILL.md, description {len(desc)} chars)")
    return versions["plugin.json"]


def build():
    DIST.mkdir(exist_ok=True)
    out = DIST / "data-expedition.skill"
    files = sorted(
        p for p in SKILL_DIR.rglob("*")
        if p.is_file()
        and not any(part in EXCLUDE_DIRS for part in p.relative_to(SKILL_DIR).parts)
        and p.name != ".DS_Store"
    )
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as zf:
        for p in files:
            arc = Path(SKILL_DIR.name) / p.relative_to(SKILL_DIR)
            info = zipfile.ZipInfo(str(arc), FIXED_TIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            zf.writestr(info, p.read_bytes())
            print(f"  added {arc}")
    print(f"Built {out.relative_to(ROOT)} ({out.stat().st_size} bytes)")


if __name__ == "__main__":
    validate()
    if "--check" not in sys.argv:
        build()
