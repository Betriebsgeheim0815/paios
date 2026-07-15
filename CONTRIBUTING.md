# Mitwirken an PAIOS

PAIOS ist ein offener Standard. Beiträge sind willkommen.

## Grundregeln
1. **Keine Secrets** in Commits (siehe `.gitignore`).
2. Änderungen am Standard laufen über Pull Requests mit Begründung.
3. SemVer: Breaking Changes erhöhen die Major-Version.
4. Neue Entitäten/Felder müssen mit dem Validierungsskript geprüft werden.

## Vor dem PR
```bash
python tools/validate_paios.py reference-vault
```
Nur konforme Beiträge werden gemergt.
