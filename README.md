# PAIOS – Personal AI Operating System

Ein offener, modellunabhängiger Standard für persönliche Wissens- und Workflow-Arbeit.

> Dein Wissen gehört dir. Modelle sind austauschbar. Der Workflow bleibt stabil.

## Architektur

```text
Mensch → Modell → MCP (optional) → PAIOS-Vault
```

Der Vault besteht aus Markdown mit YAML-Frontmatter und kann mit Git versioniert werden.

## Schnellstart

Einmalig die kleine, fest gepinnte Schema-Abhängigkeit installieren:

```bash
python3 -m pip install -r requirements.txt
```

```sh
python tools/paios.py validate reference-vault
python tools/paios.py search reference-vault Beispiel
python tools/validate_paios.py reference-vault
python -m unittest discover -s tests -v
```

## Werkzeuge

- `tools/paios.py`: CLI mit `init`, `new`, `validate` und `search`.
- `tools/paios_core.py`: gemeinsame Regeln für Frontmatter, IDs, Pfade und Validierung.
- `tools/paios_context.py`: kompakten Projektkontext erzeugen.
- `tools/backfill_frontmatter.py`: kollisionssicheres Backfill mit Dry-Run.
- `tools/import_markdown.py`: konservativer Markdown-Import.
- `tools/paios_proposal.py`: Vorschläge erstellen, menschlich prüfen und revisionsgebunden anwenden.
- `mcp/readonly_reference.py`: read-only Referenzadapter.

Die Referenzwerkzeuge unterstützen bewusst flaches YAML-Frontmatter: skalare Werte sowie
Listen in der Form `[a, b]`. Verschachteltes YAML gehört nicht zum v1.0-Referenzprofil.

## Kontrollierte Änderungen

Ein Modell erstellt zunächst einen Proposal mit `pending`-Status. Nur `human:<name>` darf ihn
freigeben oder ablehnen. Beim Anwenden werden der freigegebene Inhalt und der SHA-256-Stand der
Zieldatei erneut geprüft. Erfolgreiche Anwendungen erzeugen einen Audit-Eintrag; ein verbliebener
Eintrag unter `00_meta/proposals/transactions/` kennzeichnet einen unterbrochenen Vorgang.

## Spezifikation

`spec/CONFORMANCE-MATRIX.md` definiert die Konformitätslevel 1 bis 3. Migrationen sind unter `spec/MIGRATION-*.md` beschrieben.

## Status

Entwicklungsstand v1.0: Referenz-Vault, gemeinsamer Vault-Kern, Validator, CLI, kontrollierter Proposal-Ablauf, read-only Adapter und CI sind vorhanden. PAIOS ist kein fertiger Anbieter-Client.

## Lizenzen

- Software und Tools: MIT
- Standard, Dokumentation und Referenz-Vault: CC BY-SA 4.0

## Mitmachen

Änderungen bitte über Branches und Pull Requests einreichen. Siehe `CONTRIBUTING.md`.
