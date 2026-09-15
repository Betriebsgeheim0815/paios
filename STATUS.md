# PAIOS – Projektstatus

## Verfügbar

- Offener Standardentwurf für Markdown- und YAML-basierte KI-Wissensarbeit.
- Referenz-Vault, Validator, Migration, Importer und GitHub-Actions-CI.
- Referenz-CLI mit `init`, `new`, `validate`, `search` und Kontext-Export.
- Lokaler Read-only-Adapter mit exakter Frontmatter-ID-Suche, JSON-Suche, Duplikaterkennung und Schutz vor Symlink-Ausbrüchen.

## Verifiziert

Bei jedem Push validiert GitHub Actions den Referenz-Vault und führt die Unittest-Suite aus. Die Read-only-Grenze ist durch Verhaltenstests abgesichert.

## Bekannte Grenzen und nächste Prioritäten

1. Kompakte Werkzeug-Wrapper in ein wartbares, gemeinsam genutztes Python-Paket überführen.
2. Einen echten MCP-Transportserver mit Protokolltests auf den Read-only-Kern setzen.
3. Schreibzugriffe erst nach einer expliziten Berechtigungs-, Validierungs-, Versions- und Audit-Spezifikation ergänzen.
4. Branch-Schutz und verpflichtende CI-Prüfungen für `main` aktivieren.

Öffentliche Dateien enthalten keine lokalen Maschinenpfade oder privaten Backup-Angaben.
