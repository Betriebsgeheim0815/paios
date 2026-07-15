#!/usr/bin/env python3
"""
PAIOS Frontmatter-Backfill
Rüstet Legacy-Markdown-Dateien im Vault mit minimalem, konformem Frontmatter aus.

Nutzung:
    python backfill_frontmatter.py <pfad-zum-vault> [--dry-run]

Regeln:
- Nur .md Primärdateien; überspringt .obsidian/, 90_archive/ und Dateien, die bereits Frontmatter haben.
- type wird aus dem Top-Level-Ordner abgeleitet; id fortlaufend je Präfix; title aus Dateiname.
"""

import sys
import re
import datetime
from pathlib import Path

FOLDER_TYPE = {
    "00_meta": ("meta", "doc"),
    "10_knowledge": ("knowledge", "k"),
    "20_projects": ("project", "p"),
    "30_workflows": ("workflow", "w"),
    "40_skills": ("skill", "s"),
    "50_memory": ("memory", "m"),
    "60_prompts": ("knowledge", "k"),
}
YEAR = datetime.date.today().year
TODAY = datetime.date.today().isoformat()


def has_frontmatter(text):
    return text.lstrip().startswith("---")


def top_folder(rel_parts):
    return rel_parts[0] if rel_parts else ""


def yaml_safe(title):
    title = title.replace('"', "'")
    return f'"{title}"'


def main():
    if len(sys.argv) < 2:
        print("Nutzung: python backfill_frontmatter.py <vault> [--dry-run]")
        sys.exit(2)
    vault = Path(sys.argv[1])
    dry = "--dry-run" in sys.argv
    counters = {}
    changed, skipped = 0, 0

    for md in sorted(vault.rglob("*.md")):
        parts = md.relative_to(vault).parts
        if ".obsidian" in parts or "90_archive" in parts:
            continue
        tf = top_folder(parts)
        if tf not in FOLDER_TYPE:
            skipped += 1
            continue
        etype, prefix = FOLDER_TYPE[tf]
        text = md.read_text(encoding="utf-8", errors="ignore")

        # Fall B: hat bereits Frontmatter -> fehlende Pflichtfelder einfügen
        if has_frontmatter(text):
            stripped = text.lstrip()
            end = stripped.find("\n---", 3)
            if end == -1:
                skipped += 1
                continue
            block = stripped[3:end]
            existing = {ln.split(":", 1)[0].strip() for ln in block.splitlines() if ":" in ln}
            need = [f for f in ("id", "type", "title", "created") if f not in existing]
            if not need:
                skipped += 1
                continue
            counters[prefix] = counters.get(prefix, 0) + 1
            num = f"{counters[prefix]:04d}"
            _id = f"{prefix}-{YEAR}-{num}"
            add = ""
            if "id" in need: add += f"id: {_id}\n"
            if "type" in need: add += f"type: {etype}\n"
            if "title" in need: add += f"title: {yaml_safe(md.stem)}\n"
            if "created" in need: add += f"created: {TODAY}\n"
            if dry:
                print(f"WOULD PATCH {md.relative_to(vault)} (+{','.join(need)})")
            else:
                new_text = stripped[:3] + "\n" + add + block.lstrip("\n") + stripped[end:]
                md.write_text(new_text, encoding="utf-8")
            changed += 1
            continue

        counters[prefix] = counters.get(prefix, 0) + 1
        num = f"{counters[prefix]:04d}"
        _id = f"{prefix}-{YEAR}-{num}" if prefix != "doc" else f"doc-{md.stem.lower().replace(' ', '-')[:40]}"
        title = md.stem
        fm = (
            "---\n"
            f"id: {_id}\n"
            f"type: {etype}\n"
            f"title: {yaml_safe(title)}\n"
            f"created: {TODAY}\n"
            "tags: [legacy]\n"
            "---\n\n"
        )
        if dry:
            print(f"WOULD ADD [{etype}] {_id} -> {md.relative_to(vault)}")
        else:
            md.write_text(fm + text, encoding="utf-8")
        changed += 1

    print(f"\n{'DRY-RUN ' if dry else ''}Fertig. Geändert: {changed}, übersprungen: {skipped}")


if __name__ == "__main__":
    main()
