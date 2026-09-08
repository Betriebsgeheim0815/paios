# PAIOS – Personal AI Operating System

Ein offener, modellunabhängiger Standard für Wissens- und Workflow-Arbeit mit KI.

> Dein Wissen gehört dir. Modelle sind austauschbar. Der Workflow bleibt stabil.

> PAIOS ist ein Standardentwurf mit Referenz-Vault und Werkzeugen, kein fertiger Anbieter oder Desktop-Client.

## Architektur

```text
Mensch → Modell (austauschbar) → MCP (optional) → PAIOS-Vault
```

Der Vault besteht aus lesbarem Markdown mit YAML-Frontmatter und kann mit Git versioniert werden.

## Schnellstart

```sh
python tools/validate_paios.py reference-vault
python -m unittest discover -s tests -v
```

Die MCP-Konfiguration in `mcp/claude_desktop_config.snippet.json` verwendet bewusst den Platzhalter `<PATH_TO_PAIOS_VAULT>`. Ersetze ihn lokal durch den absoluten Vault-Pfad.

## Repository-Struktur

- `spec/` – Standard, Datenmodell und Architektur
- `reference-vault/` – minimales Beispiel
- `tools/validate_paios.py` – strikter Konformitätsprüfer
- `tools/backfill_frontmatter.py` – kollisionssicheres Backfill
- `tests/` und `.github/workflows/` – reproduzierbare Prüfungen

## Status

Frühe Phase (v0.1). Die Spezifikation, Beispielstruktur, Validierung und optionale MCP-Referenzintegration sind vorhanden. Die Konformitätsregeln werden in `spec/VALIDATION.md` dokumentiert.

## Lizenzen

- Software und Tools: MIT
- Standard, Dokumentation und Referenz-Vault: CC BY-SA 4.0

## Mitmachen

Änderungen sind über Branches und Pull Requests willkommen. Siehe `CONTRIBUTING.md`.
