# Migration von v0.1 zu v0.2

1. Sicherung und Git-Commit erstellen.
2. `python tools/backfill_frontmatter.py --dry-run VAULT` ausführen.
3. Backfill ohne `--dry-run` ausführen und Änderung prüfen.
4. `python tools/validate_paios.py VAULT` ausführen.
5. Links und typabhängige Felder ergänzen.

Die Migration ist absichtlich konservativ: bestehende Dateien werden nicht überschrieben, wenn bereits Frontmatter vorhanden ist. Jeder Schritt sollte als eigener Git-Commit nachvollziehbar bleiben.
