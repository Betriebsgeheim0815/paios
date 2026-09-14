# PAIOS Read-only-MCP-Referenz

Dieses Verzeichnis definiert eine sichere Lesegrenze für PAIOS-Vaults. Der Vault bleibt die Quelle der Wahrheit; der Adapter schreibt keine Dateien.

## Aufruf

`python mcp/readonly_reference.py <VAULT> search "Suchtext"`

`python mcp/readonly_reference.py <VAULT> read k-2026-0001`

## Verhalten

- `read` gleicht die ID exakt mit dem Feld `id` im YAML-Frontmatter ab.
- Fehlende IDs enden mit Exit-Code 1; doppelte IDs mit Exit-Code 2.
- `search` liefert JSON mit relativem Pfad, ID, Titel und einem kurzen Ausschnitt.
- Symbolische Links, die aus dem Vault herausführen, werden ignoriert.
- Es gibt keine Schreib-, Lösch- oder Pfadlese-Operation.

## Sicherheitsregeln

1. Vault-Pfad explizit konfigurieren.
2. Keine Secrets in Vault, Tool-Antworten oder Beispielen.
3. Schreiben nur über einen separaten, bestätigten und validierten Adapter.
4. MCP niemals als Datenbank oder Single Point of Truth behandeln.

Die Datei `readonly_reference.py` ist eine lokale Referenz-CLI, noch kein vollständiger MCP-Transportserver.
