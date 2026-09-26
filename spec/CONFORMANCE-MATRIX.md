# PAIOS v1.0 – Konformitätsmatrix

Die Matrix trennt strukturelle Gültigkeit von semantischer und integrativer Gültigkeit.

| Bereich | Level 1 | Level 2 | Level 3 |
|---|---|---|---|
| Ordner | Pflichtordner vorhanden | empfohlene Ordner | Erweiterungen dokumentiert |
| Frontmatter | id, type, title, created | typabhängige Felder | Versionierung |
| IDs | syntaktisch gültig | eindeutig | historisch stabil |
| Links | Liste und Ziel existieren | MOCs vorhanden | Backlinks aktualisiert |
| Sicherheit | offensichtliche Secrets ablehnen | Privacy-Felder | Exportfilter |
| Git | nicht erforderlich | empfohlen | Audit und Commit-Regeln |
| MCP | nicht erforderlich | dokumentierte Read-only-Anbindung (`00_meta/mcp.json`) | kontrollierte Schreibrechte |

Die Referenzimplementierung prüft Level 1 und Level 2. Level 3 beschreibt die weitere
Entwicklungsrichtung und wird vom Validator nicht als implementiert ausgegeben.
