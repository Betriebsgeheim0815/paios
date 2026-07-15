#!/usr/bin/env python3
"""
PAIOS Konformitäts-Validierung (Standard v0.1, §10)
Prüft einen PAIOS-Vault auf Level 1 / Level 2 Konformität.

Nutzung:
    python validate_paios.py <pfad-zum-vault>

Keine externen Abhängigkeiten (nur Standardbibliothek).
Exit-Code 0 = Level 1 bestanden, 1 = nicht bestanden.
"""

import sys
import re
from pathlib import Path

# Robuste Ausgabe unabhängig von der Konsolen-Codepage (Windows cp1252 etc.)
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

REQUIRED_DIRS = ["00_meta", "10_knowledge", "20_projects", "50_memory"]
RECOMMENDED_DIRS = ["30_workflows", "40_skills", "90_archive"]
REQUIRED_META = ["paios.yaml", "principles.md"]
REQUIRED_FM = ["id", "type", "title", "created"]
VALID_TYPES = {"knowledge", "project", "workflow", "skill", "memory", "meta", "moc"}
ID_PATTERN = re.compile(r"^[a-z]+-\d{4}-\d+$|^(doc|moc)-[a-z0-9-]+$")
SECRET_PATTERNS = [
    re.compile(r"sk-[A-Za-z0-9]{16,}"),
    re.compile(r"AIza[0-9A-Za-z\-_]{20,}"),
    re.compile(r"ghp_[A-Za-z0-9]{20,}"),
    re.compile(r"xox[baprs]-[A-Za-z0-9-]{10,}"),
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
]


def parse_frontmatter(text):
    """Sehr einfacher YAML-Frontmatter-Parser (nur top-level key: value)."""
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    if end == -1:
        return None
    block = text[3:end].strip().splitlines()
    fm = {}
    for line in block:
        if ":" in line and not line.strip().startswith("#"):
            k, _, v = line.partition(":")
            fm[k.strip()] = v.strip()
    return fm


def validate(vault: Path):
    errors, warnings = [], []

    # §3 Pflichtordner
    for d in REQUIRED_DIRS:
        if not (vault / d).is_dir():
            errors.append(f"Pflichtordner fehlt: {d}/")
    for d in RECOMMENDED_DIRS:
        if not (vault / d).is_dir():
            warnings.append(f"Empfohlener Ordner fehlt: {d}/")

    # §3 00_meta Pflichtdateien
    for f in REQUIRED_META:
        if not (vault / "00_meta" / f).is_file():
            errors.append(f"00_meta/{f} fehlt")

    # Primärdateien prüfen
    checked = 0
    for md in vault.rglob("*.md"):
        if ".obsidian" in md.parts or "90_archive" in md.parts:
            continue
        checked += 1
        text = md.read_text(encoding="utf-8", errors="ignore")
        rel = md.relative_to(vault)

        # §5 Frontmatter
        fm = parse_frontmatter(text)
        if fm is None:
            errors.append(f"Kein Frontmatter: {rel}")
            continue
        for field in REQUIRED_FM:
            if field not in fm:
                errors.append(f"Pflichtfeld '{field}' fehlt: {rel}")
        # §5 type
        if fm.get("type") not in VALID_TYPES:
            errors.append(f"Ungültiger type '{fm.get('type')}': {rel}")
        # §6 id
        if "id" in fm and not ID_PATTERN.match(fm["id"]):
            warnings.append(f"id entspricht nicht dem Schema: {fm['id']} ({rel})")

    # §2/§10 Secrets
    for f in vault.rglob("*"):
        if f.is_file() and f.suffix in (".md", ".txt", ".json", ".yaml", ".yml"):
            if ".obsidian" in f.parts:
                continue
            try:
                content = f.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                continue
            for pat in SECRET_PATTERNS:
                if pat.search(content):
                    errors.append(f"Möglicher Secret-Fund: {f.relative_to(vault)}")
                    break

    # Level 2 (weich)
    if not (vault / ".git").exists():
        warnings.append("Kein Git-Repository (Level 2 empfiehlt Git).")

    return errors, warnings, checked


def main():
    if len(sys.argv) != 2:
        print("Nutzung: python validate_paios.py <pfad-zum-vault>")
        sys.exit(2)
    vault = Path(sys.argv[1])
    if not vault.is_dir():
        print(f"Pfad ist kein Verzeichnis: {vault}")
        sys.exit(2)

    errors, warnings, checked = validate(vault)

    print(f"\nPAIOS-Validierung: {vault}")
    print(f"Geprüfte Primärdateien: {checked}")
    print("-" * 50)
    for w in warnings:
        print(f"  [WARN] {w}")
    for e in errors:
        print(f"  [FEHLER] {e}")
    print("-" * 50)

    if errors:
        print(f"Ergebnis: NICHT konform (Level 1) — {len(errors)} Fehler, {len(warnings)} Warnungen")
        sys.exit(1)
    elif warnings:
        print(f"Ergebnis: Level 1 KONFORM (mit {len(warnings)} Warnungen für Level 2)")
        sys.exit(0)
    else:
        print("Ergebnis: Level 2 KONFORM — vollständig.")
        sys.exit(0)


if __name__ == "__main__":
    main()
