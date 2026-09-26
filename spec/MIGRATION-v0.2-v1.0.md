# Migration von v0.2 zu v1.0

1. Vor der Migration einen Git-Commit oder ein Backup erstellen.
2. `00_meta/paios.yaml` auf `version: 1.0` setzen.
3. Metadatenfelder auf die in `spec/STANDARD.md` definierten Datentypen prüfen.
4. Für Level 2 `00_meta/mcp.json` mit `enabled: true` und `mode: read-only` anlegen.
5. Schreibvorschläge auf das SHA-256-basierte Proposal-Schema umstellen.
6. Bestehende numerische `base_revision`-Werte neu erzeugen; sie sind mit v1.0 nicht kompatibel.
7. `python tools/validate_paios.py <vault>` ausführen und Fehler vor dem Commit beheben.

Die Major-Version ist erforderlich, weil die neue `base_revision`-Semantik bestehende Proposal-Dateien inkompatibel macht.
