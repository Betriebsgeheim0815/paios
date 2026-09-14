# PAIOS Provenienz und kontrollierte Vorschlaege v0.3

## Zweck

PAIOS trennt kanonische Geschaeftsdaten von Modellbeitraegen. Markdown, YAML-Frontmatter und Git bleiben die dauerhafte Datenbasis.

## Sicherheitsgrenzen

- Ein Modell darf keine kanonische Datei direkt aendern.
- Ein Modell darf Projektcode, Tests sowie CI- und MCP-Konfiguration nur in einem isolierten Feature-Branch aendern.
- Der Branch wird ueber einen Pull Request (PR) gegen main reviewt.
- Continuous Integration (CI) fuehrt automatische Tests, Schema-Pruefungen und Boundary-Checks aus und zeigt den geprueften Aenderungsumfang.
- MCP ist eine austauschbare Integrationsschicht fuer Modelle, nicht die primaere Datenbank.

## Proposal-Struktur

Jeder Vorschlag enthaelt mindestens `proposal_id`, `entity_id`, `operation`, `actor`, `base_revision`, `created_at`, `status`, `patch` und `provenance`.

`base_revision` ist die Revision der Zieldatei zum Zeitpunkt des Vorschlags. Vor einer spaeteren Anwendung muss sie erneut geprueft werden.

## Review-Gates

1. Sicherheit und Umfang: keine Secrets, privaten Pfade oder direkten Vault-Mutationen.
2. Verhalten und Tests: neue Regeln werden zuerst durch Tests beschrieben und anschliessend implementiert.
3. Auslieferung und PR-Qualitaet: gruenes CI, pruefbarer Diff, keine Konflikte und menschliche Merge-Freigabe.

## Offene Standards

JSON Schema validiert Proposal-Dateien. MCP standardisiert den Werkzeugzugriff. Dublin Core und PROV-O werden bei Bedarf ueber dokumentierte Mappings angebunden, ohne die kanonische Dateibasis zu ersetzen.
