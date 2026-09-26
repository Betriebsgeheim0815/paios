# PAIOS – Projektstatus

## Verfügbar

- Offener Standardentwurf für Markdown- und YAML-basierte KI-Wissensarbeit.
- Referenz-Vault, Validator, Migration, Importer und GitHub-Actions-CI.
- Referenz-CLI mit `init`, `new`, `validate`, `search` und Kontext-Export.
- Lokaler Read-only-Adapter mit exakter Frontmatter-ID-Suche, JSON-Suche, Duplikaterkennung und Schutz vor Symlink-Ausbrüchen.
- Gemeinsamer Verarbeitungskern und kontrollierter Proposal-Ablauf mit Review, Revisionstest und Audit.

## Verifiziert

Bei jedem Push validiert GitHub Actions den Referenz-Vault und führt die Unittest-Suite aus. Die Read-only-Grenze ist durch Verhaltenstests abgesichert.

## Bekannte Grenzen und nächste Prioritäten

1. Einen echten MCP-Transportserver mit Protokolltests auf den Read-only-Kern setzen.
2. Level 3 mit Datenschutzfeldern, Exportfiltern und Backlink-Prüfung spezifizieren.
3. Branch-Schutz und verpflichtende CI-Prüfungen für `main` verifizieren.

Öffentliche Dateien enthalten keine lokalen Maschinenpfade oder privaten Backup-Angaben.
