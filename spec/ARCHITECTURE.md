---
id: doc-architecture
type: meta
title: "PAIOS Architekturhandbuch"
version: 0.1
status: draft
created: 2026-07-13
owner: "Dr. Dhoni"
links: [doc-manifest, doc-standard, PAIOS_Datenmodell]
---

# PAIOS Architekturhandbuch v0.1

Beschreibt, wie die PAIOS-Komponenten technisch zusammenwirken. Das Manifest sagt *warum*, der Standard sagt *was*, dieses Handbuch sagt *wie*.

---

## 1. Schichtenmodell

PAIOS ist in vier klar getrennte Schichten aufgebaut:

```
┌─────────────────────────────────────────────┐
│  4. Mensch (Dr. Dhoni)                        │  Ziele, Entscheidungen
├─────────────────────────────────────────────┤
│  3. Modell-Schicht (austauschbar)             │  Claude / GPT / Gemini …
│     Zugriff ausschließlich über MCP           │
├─────────────────────────────────────────────┤
│  2. Schnittstellen-Schicht (MCP-Server)       │  Vault-Server, Memory-Server
├─────────────────────────────────────────────┤
│  1. Speicher-Schicht (PAIOS-Vault)            │  Markdown + YAML, Git, Obsidian
└─────────────────────────────────────────────┘
```

**Prinzip:** Jede Schicht kennt nur ihre direkten Nachbarn. Modelle sprechen nie direkt mit dem Dateisystem, sondern immer über MCP. So bleibt die Speicherschicht modellunabhängig (Prinzip 2).

---

## 2. Schicht 1 – Speicher (PAIOS-Vault)

- Physisch: ein Verzeichnis mit Markdown-Dateien (siehe Standard §3).
- Versionierung: Git. Jeder sinnvolle Zustand ist ein Commit; Historie ist die Wahrheit.
- Sichtbarkeit für den Menschen: Obsidian (Wikilinks, Graph, Suche).
- **Regel:** keine Secrets, keine proprietären Binärformate als Primärdaten.

## 3. Schicht 2 – Schnittstelle (MCP)

Zwei Server-Rollen (bestehende Bausteine, kein Eigenbau):

| Server | Aufgabe | Referenz |
|---|---|---|
| **Vault-Server** | Lesen/Schreiben von Dateien, Suche, Frontmatter-Parsing | Filesystem-/Obsidian-MCP |
| **Memory-Server** | Relevanz-Ranking, Recall, Zurückschreiben nach `50_memory/` | ai-memory-mcp-Ansatz |

- Beide MÜSSEN nur über offene MCP-Endpunkte ansprechbar sein.
- Schreibzugriffe SOLLTEN einen Git-Commit auslösen.

## 4. Schicht 3 – Modell (austauschbar)

- Jedes MCP-fähige Modell KANN eingesetzt werden.
- Modellwahl ist eine reine Konfigurationsfrage („Model-Router"), nicht Teil des Datenbestands.
- Der **Router** ordnet Aufgaben Modellklassen zu (z. B. Reasoning, Coding, Bild) — als Konvention im Frontmatter-Feld `model_hint`, nicht als harte Bindung.

## 5. Schicht 4 – Mensch

- Definiert Ziele und trifft Entscheidungen (Prinzip 6).
- Arbeitet primär in Obsidian; KI-Aktionen erscheinen als Datei-/Git-Änderungen und sind damit prüfbar.

---

## 6. Referenzabläufe (Sequenzen)

### 6.1 Wissen abrufen
1. Mensch/Modell stellt Frage.
2. Modell ruft Vault-Server (Suche in `10_knowledge/`, `50_memory/`) via MCP.
3. Vault-Server liefert passende Dateien (Frontmatter-gefiltert).
4. Modell antwortet, gestützt auf den Vault-Inhalt.

### 6.2 Erkenntnis speichern
1. Modell erzeugt neue Erkenntnis.
2. Memory-Server schreibt `m-…`-Datei nach `50_memory/` (Scope, Relevanz).
3. Vault-Server committet → Git-Historie.

### 6.3 Modellwechsel
1. Nutzer wechselt das Modell (Router-Konfiguration).
2. Neues Modell greift auf denselben Vault via MCP zu.
3. **Kein Wissensverlust** – der Kontext lag nie im Modell, sondern im Vault.

---

## 7. Technologie-Entscheidungen (mit Begründung)

| Baustein | Wahl | Warum | Alternative |
|---|---|---|---|
| Format | Markdown + YAML | offen, menschen-/maschinenlesbar | JSON (weniger lesbar) |
| Versionierung | Git | Standard, Historie, Rollback | keine (Datenverlust-Risiko) |
| Speicher-App | Obsidian | lokal, Markdown, Wikilinks, Plugins | Logseq, reines Git |
| Schnittstelle | MCP | Cross-Vendor-Standard 2026 | proprietäre API (Lock-in) |
| Memory | MCP-Memory-Server | erprobt, lokal | Eigenbau (Aufwand) |

## 8. Nicht-funktionale Anforderungen

- **Portabilität:** Vault MUSS ohne PAIOS-Software lesbar bleiben (reine Dateien).
- **Nachvollziehbarkeit:** jede KI-Änderung MUSS als Git-Commit sichtbar sein.
- **Sicherheit:** Secrets außerhalb des Vaults; Vault nicht ungeschützt in Cloud-Sync mit Klartext-Geheimnissen.
- **Modularität:** Komponenten einzeln austauschbar (Modell, Memory-Server, Speicher-App).

## 9. Risiken & Gegenmaßnahmen

| Risiko | Gegenmaßnahme |
|---|---|
| MCP-Server nicht verfügbar | Vault bleibt als Dateien nutzbar (Degradation, kein Ausfall) |
| Gleichzeitige Schreibzugriffe | Git-Merge + Konfliktregeln (Standard v0.2) |
| Wildwuchs/Inkonsistenz | Konformitäts-Validierungsskript (geplant) |
| Cloud-Sync-Leck | Secrets-Regel + `.gitignore` + Passwort-Manager |

---

## 10. Nächste Bausteine
1. **GitHub-Struktur** – öffentliches Repo für Standard + Referenz-Vault-Vorlage.
2. **Validierungsskript** – prüft Konformität (Standard §10).
3. **MCP-Setup-Anleitung** – Vault- und Memory-Server konkret verbinden.

*Version 0.1 (Draft) – lebendes Dokument.*
