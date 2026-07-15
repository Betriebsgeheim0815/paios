---
id: doc-setup-mcp
type: meta
title: "PAIOS – MCP-Setup"
created: 2026-07-14
---

# PAIOS – MCP-Server verbinden

Verbindet den PAIOS-Vault (Speicherschicht) und ein persistentes Gedächtnis über MCP mit jedem MCP-fähigen Client (Claude Desktop, Cursor u. a.).

## Voraussetzungen
- **Node.js** installiert (`node --version`, empfohlen ≥ 18). Prüfen; ggf. von nodejs.org installieren.
- Ein MCP-fähiger Client (z. B. Claude Desktop).

## Zwei Server
| Name | Paket | Aufgabe |
|---|---|---|
| `paios-vault` | `@modelcontextprotocol/server-filesystem` | Lesen/Schreiben des Vaults |
| `paios-memory` | `@modelcontextprotocol/server-memory` | persistentes Gedächtnis |

## Einrichtung (Claude Desktop, Windows)

1. Config-Datei öffnen (ggf. anlegen):
   `%APPDATA%\Claude\claude_desktop_config.json`
2. Den Inhalt aus `claude_desktop_config.snippet.json` einfügen. Falls die Datei
   bereits einen `mcpServers`-Block hat, nur die beiden Einträge dort ergänzen.
3. Claude Desktop **vollständig beenden und neu starten**.
4. Test: Im Chat nach einer Datei aus dem Vault fragen – der Client sollte über
   `paios-vault` darauf zugreifen.

## Hinweise
- Der Pfad im Snippet zeigt bereits auf Ihren PAIOS-Ordner.
- Der Filesystem-Server erlaubt Schreibzugriff nur innerhalb des angegebenen Ordners.
- Für stärkeres Memory-Ranking später: `ai-memory-mcp` als Alternative prüfen (lokal, SQLite).
- **Keine Secrets** in den Vault – auch nicht über MCP.

## Konfidenz
Mittel–Hoch. Paketnamen entsprechen dem offiziellen MCP-Servers-Repo (Stand Trainingswissen); bitte einmalig gegen die aktuelle MCP-Doku prüfen, da sich Paketnamen ändern können.
