# PAIOS – Projektstatus

## Verfügbar

- Offener Standardentwurf für Markdown- und YAML-basierte KI-Wissensarbeit.
- Referenz-Vault, Validator, Migration, Importer und GitHub-Actions-CI.
- Referenz-CLI mit `init`, `new`, `validate`, `search` und Kontext-Export.
- Lokaler Read-only-Adapter mit exakter Frontmatter-ID-Suche, JSON-Suche, Duplikaterkennung und Schutz vor Symlink-Ausbrüchen.

## Verifiziert

Bei jedem Push validiert GitHub Actions den Referenz-Vault und führt die Unittest-Suite aus. Die Read-only-Grenze ist durch Verhaltenstests abgesichert.

## Bekannte Grenzen und nächste Prioritäten

1. Versionsangaben in `STANDARD.md`, Datenmodell, Vault-Manifest und Validator zu einer normativen v0.2 synchronisieren.
2. Kompakte Werkzeug-Wrapper in ein wartbares, gemeinsam genutztes Python-Paket überführen.
3. Einen echten MCP-Transportserver mit Protokolltests auf den Read-only-Kern setzen.
4. Schreibzugriffe erst nach einer expliziten Berechtigungs-, Validierungs-, Versions- und Audit-Spezifikation ergänzen.

Öffentliche Dateien enthalten keine lokalen Maschinenpfade oder privaten Backup-Angaben.
