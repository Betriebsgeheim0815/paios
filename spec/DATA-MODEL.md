# PAIOS – Datenmodell (v0.1)

**Stand:** 2026-07-13
**Grundlage:** Option A (MCP-nativ), Obsidian als Wissensspeicher, minimale Referenzimplementierung.
**Prinzip:** Alles ist Markdown + YAML-Frontmatter in einem Git-versionierten Ordner (dem „PAIOS-Vault"). Keine proprietäre Datenbank. Menschen- und KI-lesbar.

---

## 1. Grundidee

Der PAIOS-Vault ist ein **Git-Repository aus Markdown-Dateien**. Jede Datei hat einen **YAML-Frontmatter-Kopf** (strukturierte Metadaten) und einen **Markdown-Körper** (Inhalt). Das ist zugleich Obsidian-Vault und PAIOS-Datenspeicher – ein Format, zwei Nutzungen. Modelle greifen über MCP darauf zu; der Mensch über Obsidian.

**Warum so:** erfüllt Prinzip 1 (Wissen gehört dem Nutzer – reine Dateien), 4 (offene Standards), 7 (Dokumentation als zentrale Quelle) und ist ohne Migration modellunabhängig.

---

## 2. Ordnerstruktur (Referenz-Vault)

```
paios-vault/
├── 00_meta/            # PAIOS-Konfiguration, Prinzipien, dieses Datenmodell
│   ├── paios.yaml      # Vault-Manifest (Version, Konventionen)
│   └── principles.md
├── 10_knowledge/       # Wissensbausteine (Notizen, Fakten, Referenzen)
├── 20_projects/        # Projekte (je Projekt eine Datei oder ein Unterordner)
├── 30_workflows/       # standardisierte Abläufe / Playbooks
├── 40_skills/          # Skill-Definitionen (was die KI tun kann)
├── 50_memory/          # persistente Memory-Einträge (MCP-gepflegt)
└── 90_archive/         # Abgeschlossenes / Historie
```

Nummern-Präfixe geben stabile Sortierung und maschinelle Zuordnung. Ordner sind bewusst wenige (Prinzip 5: Modularität vor Komplexität).

---

## 3. Kern-Entitäten

Fünf Entitäten reichen für den minimalen Kern. Jede ist eine Markdown-Datei mit Frontmatter.

### 3.1 Knowledge (Wissensbaustein) — `10_knowledge/`
```yaml
---
id: k-2026-0001
type: knowledge
title: "Was ist MCP"
tags: [mcp, standard]
created: 2026-07-13
updated: 2026-07-13
source: "https://modelcontextprotocol.io"
links: [k-2026-0002]      # Verweise auf andere IDs / Obsidian [[Wikilinks]]
---
Fließtext des Wissens …
```

### 3.2 Project (Projekt) — `20_projects/`
```yaml
---
id: p-paios
type: project
title: "PAIOS Aufbau"
status: active            # active | paused | done
owner: "Dr. Dhoni"
created: 2026-07-13
next_task: "Referenzimplementierung"
links: [k-2026-0001]
---
Projektbeschreibung, Ziele, offene Punkte …
```

### 3.3 Workflow — `30_workflows/`
```yaml
---
id: w-doku
type: workflow
title: "Projektdokumentation erstellen"
steps: [manifest, standard, architektur, github, referenz]
model_hint: "reasoning"   # welche Modellklasse eignet sich
---
Beschreibung + Schritt-für-Schritt …
```

### 3.4 Skill — `40_skills/`
```yaml
---
id: s-continue-paios
type: skill
title: "PAIOS fortführen"
trigger: "weiter am PAIOS-Projekt"
inputs: [vault_path]
outputs: [next_document]
---
Anweisung, was der Skill tut …
```

### 3.5 Memory (Erinnerung) — `50_memory/`
```yaml
---
id: m-2026-0007
type: memory
scope: project            # global | project | session
project: p-paios
relevance: 0.9
created: 2026-07-13
---
Kurzer, atomarer Erinnerungssatz (von MCP-Memory-Server gepflegt) …
```

---

## 4. Gemeinsame Feld-Konventionen

| Feld | Pflicht | Bedeutung |
|---|---|---|
| `id` | ja | Eindeutig, präfixiert (`k-`, `p-`, `w-`, `s-`, `m-`) |
| `type` | ja | Entitätstyp (knowledge/project/workflow/skill/memory) |
| `title` | ja | Menschlicher Titel |
| `created` / `updated` | ja | ISO-Datum |
| `tags` | nein | Freie Schlagworte |
| `links` | nein | IDs verwandter Einträge; zusätzlich Obsidian-`[[Wikilinks]]` im Text |

**Verknüpfung:** doppelt gehalten – maschinell über `links:`-IDs, menschlich über Obsidian-Wikilinks. So funktioniert Navigation in Obsidian *und* Auflösung über MCP.

---

## 5. Zugriff über MCP (Referenzfluss)

1. Modell fragt via MCP: „Was weiß ich über MCP im PAIOS-Kontext?"
2. MCP-Server liest `10_knowledge/` + `50_memory/`, filtert nach `tags`/`relevance`.
3. Antwort fließt ins Modell; neue Erkenntnisse werden als `memory`-Datei zurückgeschrieben.
4. Git committet die Änderung → Versionierung, Nachvollziehbarkeit, kein Lock-in.

Benötigte MCP-Server (bestehend, nicht neu bauen): **Filesystem/Obsidian-MCP** (Lesen/Schreiben des Vaults) + **Memory-MCP** (Relevanz-Ranking, z. B. ai-memory-mcp-Ansatz).

---

## 6. Offene Punkte für die nächste Runde

1. ID-Schema final (fortlaufend vs. datumsbasiert) – aktuell Vorschlag: `typ-jahr-laufnr`.
2. Memory-Server konkret wählen (ai-memory-mcp prüfen vs. Filesystem-MCP + eigenes Frontmatter).
3. Minimaler Skill `s-continue-paios` als erste lauffähige Referenz.

**Konfidenz: Mittel–Hoch.** Struktur ist bewusst schlank; Feinheiten (Memory-Ranking, ID-Schema) erst an der Referenzimplementierung härten.
