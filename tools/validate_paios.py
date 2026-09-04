#!/usr/bin/env python3
"""PAIOS-Konformitätsprüfung nach Standard v0.2 (nur Standardbibliothek)."""
from __future__ import annotations
import datetime as dt
import re
import sys
from collections import defaultdict
from pathlib import Path

REQUIRED_DIRS = ("00_meta", "10_knowledge", "20_projects", "50_memory")
RECOMMENDED_DIRS = ("30_workflows", "40_skills", "90_archive")
VALID_TYPES = {"knowledge", "project", "workflow", "skill", "memory", "meta", "moc"}
PREFIXES = {"knowledge": "k-", "project": "p-", "workflow": "w-", "skill": "s-", "memory": "m-"}
ID_RE = re.compile(r"^[kpwsm]-\d{4}-\d+$|^(doc|moc)-[a-z0-9-]+$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
SECRETS = (re.compile(r"sk-[A-Za-z0-9]{16,}"), re.compile(r"AIza[0-9A-Za-z\-_]{20,}"), re.compile(r"ghp_[A-Za-z0-9]{20,}"), re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"))

def frontmatter(text: str):
    if not text.startswith("---\n"):
        return None, "Frontmatter muss in der ersten Zeile mit --- beginnen"
    match = re.search(r"\n---(?:\n|$)", text[4:])
    if not match:
        return None, "Frontmatter-Abschluss --- fehlt"
    fields = {}
    for number, line in enumerate(text[4:4 + match.start()].splitlines(), 2):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line.startswith((" ", "\t", "-")) or ":" not in line:
            return None, f"nicht unterstütztes YAML in Frontmatter-Zeile {number}"
        key, value = (part.strip() for part in line.split(":", 1))
        if key in fields:
            return None, f"doppelter Schlüssel '{key}'"
        fields[key] = value
    return fields, None

def valid_date(value: str) -> bool:
    try:
        return bool(DATE_RE.fullmatch(value)) and (dt.date.fromisoformat(value) is not None)
    except ValueError:
        return False

def links(value: str):
    if not value.startswith("[") or not value.endswith("]"):
        return None
    content = value[1:-1].strip()
    return [] if not content else [item.strip().strip('"\'') for item in content.split(",")]

def validate(vault: Path):
    errors, warnings, ids, file_links, checked = [], [], defaultdict(list), {}, 0
    for directory in REQUIRED_DIRS:
        if not (vault / directory).is_dir(): errors.append(f"Pflichtordner fehlt: {directory}/")
    for directory in RECOMMENDED_DIRS:
        if not (vault / directory).is_dir(): warnings.append(f"Empfohlener Ordner fehlt: {directory}/")
    for filename in ("paios.yaml", "principles.md"):
        if not (vault / "00_meta" / filename).is_file(): errors.append(f"00_meta/{filename} fehlt")
    for path in sorted(vault.rglob("*.md")):
        if ".obsidian" in path.parts or "90_archive" in path.parts: continue
        checked += 1; rel = path.relative_to(vault); fields, problem = frontmatter(path.read_text(encoding="utf-8", errors="replace"))
        if problem:
            errors.append(f"{problem}: {rel}"); continue
        for name in ("id", "type", "title", "created"):
            if not fields.get(name): errors.append(f"Pflichtfeld '{name}' fehlt: {rel}")
        kind, identifier = fields.get("type"), fields.get("id", "")
        if kind not in VALID_TYPES: errors.append(f"Ungültiger type '{kind}': {rel}")
        if identifier and not ID_RE.fullmatch(identifier): errors.append(f"id entspricht nicht dem Schema: {identifier} ({rel})")
        if kind in PREFIXES and identifier and not identifier.startswith(PREFIXES[kind]): errors.append(f"id-Präfix passt nicht zu type '{kind}': {rel}")
        if identifier.startswith(("doc-", "moc-")) and kind not in {"meta", "moc"}: errors.append(f"sprechende id nur für meta/moc: {rel}")
        for field in ("created", "updated"):
            if field in fields and not valid_date(fields[field].strip('"\'')): errors.append(f"{field} ist kein ISO-Datum YYYY-MM-DD: {rel}")
        if kind == "project" and fields.get("status") not in {"active", "paused", "done"}: errors.append(f"project benötigt status: {rel}")
        if kind == "skill" and not fields.get("trigger"): errors.append(f"skill benötigt trigger: {rel}")
        if kind == "memory" and fields.get("scope") not in {"global", "project", "session"}: errors.append(f"memory benötigt scope: {rel}")
        if kind == "memory" and fields.get("scope") == "project" and not fields.get("project"): errors.append(f"memory benötigt project-ID: {rel}")
        if kind == "knowledge" and not fields.get("source"): warnings.append(f"knowledge ohne source: {rel}")
        if identifier: ids[identifier].append(rel)
        if "links" in fields:
            file_links[rel] = links(fields["links"])
            if file_links[rel] is None: errors.append(f"links muss eine flache Liste sein: {rel}")
    for identifier, paths in ids.items():
        if len(paths) > 1: errors.append(f"id ist nicht eindeutig: {identifier}")
    for rel, targets in file_links.items():
        if targets:
            for target in targets:
                if target not in ids: errors.append(f"links-Ziel existiert nicht: {target} ({rel})")
    for path in vault.rglob("*"):
        if path.is_file() and path.suffix.lower() in {".md", ".txt", ".json", ".yaml", ".yml"} and ".obsidian" not in path.parts:
            if any(pattern.search(path.read_text(encoding="utf-8", errors="ignore")) for pattern in SECRETS): errors.append(f"Möglicher Secret-Fund: {path.relative_to(vault)}")
    if not any((candidate / ".git").exists() for candidate in (vault, *vault.parents)): warnings.append("Kein Git-Repository für Vault gefunden.")
    return errors, warnings, checked

if __name__ == "__main__":
    if len(sys.argv) != 2 or not Path(sys.argv[1]).is_dir():
        print("Nutzung: python validate_paios.py <pfad-zum-vault>"); raise SystemExit(2)
    errors, warnings, checked = validate(Path(sys.argv[1]).resolve())
    print(f"PAIOS-Validierung: {checked} Primärdateien")
    for warning in warnings: print(f"[WARN] {warning}")
    for error in errors: print(f"[FEHLER] {error}")
    print("Ergebnis: NICHT konform" if errors else f"Ergebnis: Level 1 KONFORM ({len(warnings)} Warnungen)")
    raise SystemExit(1 if errors else 0)
