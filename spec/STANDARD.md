---
id: doc-standard
type: meta
title: "PAIOS Standard"
version: 0.2
status: draft
created: 2026-07-13
owner: "Dr. Dhoni"
links: [doc-manifest, PAIOS_Datenmodell]
---

# PAIOS Standard v0.2 (Spezifikation)

Dieser Standard spezifiziert verbindlich, wie ein PAIOS-konformer Wissensspeicher (ein „PAIOS-Vault") aufgebaut ist. Er übersetzt das Manifest in prüfbare Regeln.

**Schlüsselwörter** MUSS / SOLLTE / KANN entsprechen RFC 2119 (MUST/SHOULD/MAY).

---

## 1. Geltungsbereich

Der Standard definiert Ordnerstruktur, Dateiformat, Metadaten, Identifikatoren, Verknüpfungen und die Schnittstelle zu Modellen. Er ist implementierungsneutral: jede Umgebung, die Markdown-Dateien liest/schreibt, KANN PAIOS-konform sein. Die Referenz nutzt Obsidian + MCP.

---

## 2. Der Vault

- Ein PAIOS-Vault MUSS ein Verzeichnis mit ausschließlich offenen Textformaten als Primärdaten sein (Markdown `.md`).
- Der Vault SOLLTE mit Git versioniert sein.
- Der Vault DARF Binärdateien (Bilder, Audio) als Anhänge enthalten; diese sind Sekundärdaten.
- Zugangsdaten/Secrets DÜRFEN NICHT im Vault gespeichert werden.

## 3. Ordnerstruktur

Ein Vault MUSS folgende Top-Level-Kategorien führen (Nummernpräfix ist verbindlich für Sortierung/Zuordnung):

| Ordner | Zweck | Pflicht |
|---|---|---|
| `00_meta/` | Konfiguration, Prinzipien, Standard, Manifest | MUSS |
| `10_knowledge/` | Wissensbausteine | MUSS |
| `20_projects/` | Projekte | MUSS |
| `30_workflows/` | Abläufe/Playbooks | SOLLTE |
| `40_skills/` | Skill-Definitionen | SOLLTE |
| `50_memory/` | persistente Erinnerungen | MUSS |
| `60_prompts/` | Prompt-Bibliothek | KANN |
| `90_archive/` | Abgeschlossenes/Historie | SOLLTE |

`00_meta/` MUSS mindestens `paios.yaml` und `principles.md` enthalten.

## 4. Dateiformat

- Jede Primärdatei MUSS aus **YAML-Frontmatter** (`---`) + **Markdown-Körper** bestehen.
- Encoding MUSS UTF-8 sein.
- Der portable Kern verwendet flaches Frontmatter: skalare Werte und Listen
  im Format `[wert-1, wert-2]`.
- Dateinamen SOLLTEN klein, ohne Sonderzeichen, mit `-` getrennt sein und die `id` widerspiegeln.

## 5. Metadaten (Frontmatter)

### 5.1 Pflichtfelder (alle Entitäten)
| Feld | Typ | Regel |
|---|---|---|
| `id` | string | MUSS eindeutig, präfixiert (§6) |
| `type` | enum | MUSS ∈ {knowledge, project, workflow, skill, memory, meta, moc} |
| `title` | string | MUSS vorhanden |
| `created` | date | MUSS ISO-8601 (`YYYY-MM-DD`) |
| `updated` | date | SOLLTE bei jeder Änderung gesetzt werden |

### 5.2 Optionale Felder
`tags` (Liste), `links` (Liste von IDs), `source` (URL/Herkunft), `status`, `owner`.

## 6. Identifikatoren

- Schema: `<präfix>-<jahr>-<laufnr>` (z. B. `k-2026-0001`).
- Präfixe MUSS: `k-` knowledge, `p-` project, `w-` workflow, `s-` skill, `m-` memory.
- `meta`/`moc`-Dokumente KÖNNEN sprechende IDs führen (z. B. `doc-standard`, `moc-paios`).
- Eine `id` DARF NICHT wiederverwendet werden.
- Jede `links:`-ID MUSS auf eine im selben Vault vorhandene ID verweisen.

## 7. Verknüpfungen

- Maschinell: über `links:` (Liste von IDs) im Frontmatter — MUSS für Beziehungen genutzt werden.
- Menschlich: über Obsidian-`[[Wikilinks]]` im Körper — SOLLTE ergänzend genutzt werden.
- Jede Kategorie SOLLTE eine `_<name>.md`-Übersichtsseite (MOC) führen.

## 8. Entitäten (Kurzschemata)

Verbindliche Minimalfelder je Typ (zusätzlich zu §5.1):

- **knowledge:** `source` SOLLTE. Körper = Wissensinhalt.
- **project:** `status` MUSS ∈ {active, paused, done}; `next_task` SOLLTE.
- **workflow:** `steps` (Liste) SOLLTE.
- **skill:** `trigger` MUSS; `inputs`/`outputs` SOLLTEN.
- **memory:** `scope` MUSS ∈ {global, project, session}; bei `project` MUSS `project`-ID gesetzt sein; `relevance` (0–1) KANN.

(Ausführliche Beispiele: siehe `PAIOS_Datenmodell`.)

## 9. Modell-Schnittstelle (MCP)

- Der Zugriff MUSS über offene Schnittstellen erfolgen; Referenz: MCP.
- Lese-/Schreibzugriff auf den Vault SOLLTE über einen Filesystem-/Obsidian-MCP-Server laufen.
- Persistentes Gedächtnis SOLLTE über einen Memory-MCP-Server erfolgen; Ergebnisse werden als `memory`-Dateien in `50_memory/` zurückgeschrieben.
- Jede modellseitige Änderung SOLLTE per Git committet werden (Nachvollziehbarkeit).
- Schreib- und Löschwerkzeuge MÜSSEN auf den kleinsten nötigen Vault-Pfad
  begrenzt sein. Vor destruktiven oder umfangreichen Änderungen MUSS ein Mensch
  den Diff bestätigen.

## 10. Konformität

Ein Vault ist **PAIOS-konform (Level 1)**, wenn:
1. die Pflichtordner (§3) existieren,
2. `00_meta/paios.yaml` + `principles.md` vorhanden sind,
3. alle Primärdateien gültigen Frontmatter mit Pflichtfeldern (§5.1) haben,
4. IDs dem Schema (§6) folgen,
5. keine Secrets im Vault liegen.

**Level 2** ergänzt: MOC-Seiten je Kategorie, Git-Versionierung, MCP-Anbindung.

## 11. Versionierung des Standards

Dieser Standard ist ein lebendes Dokument (SemVer). Breaking Changes erhöhen die Major-Version. Aktuelle Version: **0.1 (Draft)**.

---

## Offene Punkte (v0.2)
- Validierungs-Skript (prüft Konformität automatisch).
- Verbindliches Vokabular für `tags`.
- Konfliktregeln bei gleichzeitigen Schreibzugriffen mehrerer Modelle.
