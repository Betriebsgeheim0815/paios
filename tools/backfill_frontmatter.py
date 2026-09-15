#!/usr/bin/env python3
"""Add minimal, conforming frontmatter to legacy PAIOS Markdown files."""

import datetime
import sys
from pathlib import Path

FOLDER_TYPE = {
    "00_meta": ("meta", "doc"), "10_knowledge": ("knowledge", "k"),
    "20_projects": ("project", "p"), "30_workflows": ("workflow", "w"),
    "40_skills": ("skill", "s"), "50_memory": ("memory", "m"),
    "60_prompts": ("knowledge", "k"),
}
YEAR = datetime.date.today().year
TODAY = datetime.date.today().isoformat()


def has_frontmatter(text):
    return text.lstrip().startswith("---")


def yaml_safe(title):
    return '"' + title.replace('"', "'") + '"'


def main():
    if len(sys.argv) < 2:
        print("Usage: python backfill_frontmatter.py <vault> [--dry-run]")
        sys.exit(2)
    vault = Path(sys.argv[1])
    dry = "--dry-run" in sys.argv
    counters = {}
    changed = skipped = 0
    for markdown in sorted(vault.rglob("*.md")):
        parts = markdown.relative_to(vault).parts
        if ".obsidian" in parts or "90_archive" in parts:
            skipped += 1
            continue
        folder = parts[0] if parts else ""
        if folder not in FOLDER_TYPE:
            skipped += 1
            continue
        entity_type, prefix = FOLDER_TYPE[folder]
        text = markdown.read_text(encoding="utf-8", errors="ignore")
        if has_frontmatter(text):
            skipped += 1
            continue
        counters[prefix] = counters.get(prefix, 0) + 1
        identifier = f"{prefix}-{YEAR}-{counters[prefix]:04d}"
        frontmatter = ("---\n" f"id: {identifier}\n" f"type: {entity_type}\n"
                       f"title: {yaml_safe(markdown.stem)}\n" f"created: {TODAY}\n"
                       "tags: [legacy]\n---\n\n")
        print(f"{'WOULD ADD' if dry else 'ADD'} {identifier} -> {markdown.relative_to(vault)}")
        if not dry:
            markdown.write_text(frontmatter + text, encoding="utf-8")
        changed += 1
    prefix = "DRY-RUN " if dry else ""
    print(f"\n{prefix}Finished. Changed: {changed}, skipped: {skipped}")


if __name__ == "__main__":
    main()
