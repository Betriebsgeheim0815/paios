# PAIOS Read-only MCP

Dieses Verzeichnis beschreibt die sichere Integrationsgrenze für MCP. PAIOS bleibt auch ohne MCP voll nutzbar.

`readonly_reference.py` bietet zwei lesende Operationen:

- `read ENTRY_ID` liest einen Eintrag über seine ID.
- `search TEXT` sucht in IDs, Titeln und Inhalten.

Die Implementierung schreibt keine Dateien, lässt keine Pfade außerhalb des Vaults zu und akzeptiert keine Schreiboperationen. Ein MCP-Server darf diese Funktionen als read-only Tools exponieren.

## Sicherheitsregeln

1. Vault-Pfad explizit konfigurieren.
2. Keine Secrets in Tool-Antworten oder Beispielen.
3. Schreiben nur in einem separaten, bestätigten Adapter.
4. MCP niemals als Datenbank oder Single Point of Truth behandeln.
