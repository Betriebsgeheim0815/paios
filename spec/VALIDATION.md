# PAIOS-Validierung

Der Validator prüft den Vault ohne externe Python-Abhängigkeiten.

```sh
python tools/validate_paios.py path/to/vault
python -m unittest discover -s tests -v
```

## Geprüfte Regeln

- Pflichtordner und `00_meta/`-Dateien
- YAML-Frontmatter mit `id`, `type`, `title` und ISO-8601-`created`
- Typabhängige ID-Präfixe und doppelte IDs
- Projektstatus und Memory-Scope
- bekannte Secret-Muster
- optionale Level-2-Hinweise für Git und MOCs

Die MCP-Anbindung ist eine optionale externe Integration; der Validator behauptet nicht, eine laufende MCP-Verbindung zu erkennen.
