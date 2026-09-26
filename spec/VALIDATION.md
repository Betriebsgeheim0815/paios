# PAIOS-Validierung

Der Validator prüft den Vault ohne externe Python-Abhängigkeiten.

```sh
python tools/validate_paios.py path/to/vault
python -m unittest discover -s tests -v
```

## Geprüfte Regeln

- Pflichtordner und `00_meta/`-Dateien
- Manifestversion und vollständige Entitätsliste
- YAML-Frontmatter mit `id`, `type`, `title` und ISO-8601-`created`
- Typabhängige ID-Präfixe und doppelte IDs
- Typ/Ordner-Zuordnung, Projektstatus, Skill-Trigger und Memory-Scope
- vorhandene Ziele für `links`
- bekannte Secret-Muster
- Level 2: empfohlene Ordner, MOCs, Git-Versionierung und `00_meta/mcp.json`

Nur Level 1 und Level 2 sind implementiert. Andere Level werden ausdrücklich abgelehnt.

Die MCP-Anbindung ist eine optionale externe Integration; der Validator behauptet nicht, eine laufende MCP-Verbindung zu erkennen.
