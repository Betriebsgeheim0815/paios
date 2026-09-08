# PAIOS – Personal AI Operating System

Ein offener, modellunabhängiger Standard für persönliche Wissens- und Workflow-Arbeit.

> Dein Wissen gehört dir. Modelle sind austauschbar. Der Workflow bleibt stabil.

## Architektur

```text
Mensch → Modell → MCP (optional) → PAIOS-Vault
```

Der Vault besteht aus Markdown mit YAML-Frontmatter und kann mit Git versioniert werden.

## Schnellstart

```sh
python tools/paios.py validate reference-vault
python tools/paios.py search reference-vault Beispiel
python tools/validate_paios.py reference-vault
python -m unittest discover -s tests -v
```

## Werkzeuge

- `tools/paios.py`: CLI mit `init`, `new`, `validate` und `search`.
- `tools/paios_context.py`: kompakten Projektkontext erzeugen.
- `tools/backfill_frontmatter.py`: kollisionssicheres Backfill mit Dry-Run.
- `tools/import_markdown.py`: konservativer Markdown-Import.
- `mcp/readonly_reference.py`: read-only Referenzadapter.

## Spezifikation

`spec/CONFORMANCE-MATRIX.md` definiert die Konformitätslevel 1 bis 3. Die Migration von v0.1 ist in `spec/MIGRATION-v0.1-v0.2.md` beschrieben.

## Status

Entwicklungsstand v0.2: Referenz-Vault, Validator, CLI-Grundlage, Importer, Vorlagen, read-only MCP-Adapter und CI sind vorhanden. PAIOS ist kein fertiger Anbieter-Client.

## Lizenzen

- Software und Tools: MIT
- Standard, Dokumentation und Referenz-Vault: CC BY-SA 4.0

## Mitmachen

Änderungen bitte über Branches und Pull Requests einreichen. Siehe `CONTRIBUTING.md`.
