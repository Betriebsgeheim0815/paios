# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

> Kommunikation auf **Deutsch**. Additiv & nicht-destruktiv arbeiten (das Repo liegt unter
> OneDrive-Sync). Keine Secrets lesen, schreiben oder zitieren.

## Was das ist

**PAIOS – Personal AI Operating System** ist ein **offener Standard**, kein Programm und kein
Anbieter: „das Git für KI-Wissensarbeit". Das Wissen gehört dem Menschen und liegt als reine
Textdateien vor; KI-Modelle sind austauschbare Werkzeuge, die über MCP darauf zugreifen.

```
Mensch → austauschbares Modell → MCP → PAIOS-Vault (Markdown + YAML-Frontmatter + Git)
```

**Die Spezifikation `spec/STANDARD.md` ist die maßgebliche Quelle.** Tools (`tools/`) und der
Beispiel-Vault (`reference-vault/`) folgen ihr — bei Widerspruch gewinnt der Standard; ändert sich
das gewünschte Verhalten, wird zuerst der Standard bewusst versioniert (SemVer), dann ziehen
Validator und Referenz-Vault nach.

## Commands

Reines Dokumentations-/Standard-Repo — **kein Build, kein Lint, kein Test-Framework, keine CI**.
Die Tools sind Python 3 (getestet mit 3.11) und nutzen **nur die Standardbibliothek**.

```bash
# Vault auf Konformität prüfen (Standard §10)
python tools/validate_paios.py <pfad-zum-vault>
#   Exit 0 = Level 1/2 konform · 1 = nicht konform · 2 = Aufruffehler
#   prüft: Pflichtordner, 00_meta/paios.yaml + principles.md,
#          Frontmatter-Pflichtfelder, ID-Schema, Secret-Muster, Git-Präsenz

# Vor jedem PR (CONTRIBUTING.md): den Referenz-Vault validieren
python tools/validate_paios.py reference-vault

# Legacy-Markdown mit minimalem, konformem Frontmatter nachrüsten
python tools/backfill_frontmatter.py <pfad-zum-vault> [--dry-run]
#   leitet type aus dem Top-Level-Ordner ab; überspringt .obsidian/,
#   90_archive/ und Dateien, die bereits Frontmatter haben

# Veröffentlichen (macht der User selbst — kein Push mit fremden Credentials)
gh repo create paios --public --source=. --push    # Details: PUBLISH-GITHUB.md
```

## Struktur

- `spec/STANDARD.md` — **normative** Spezifikation (RFC-2119 MUSS/SOLLTE/KANN). Einstiegspunkt.
- `spec/ARCHITECTURE.md`, `spec/DATA-MODEL.md` — Architekturhandbuch und Entitäten-/Datenmodell.
- `reference-vault/` — minimaler, konformer Beispiel-Vault (Ziel des Validators).
- `tools/` — `validate_paios.py` (Konformitätsprüfer), `backfill_frontmatter.py`.
- `mcp/` — `SETUP-MCP.md` + `claude_desktop_config.snippet.json`: zwei MCP-Server,
  `paios-vault` (`@modelcontextprotocol/server-filesystem`) und `paios-memory` (`…/server-memory`).
- `MANIFEST.md` (Warum), `STATUS.md` (aktueller Stand), `README.md`, `CONTRIBUTING.md`.

## Verbindliche Konventionen (aus `spec/STANDARD.md`; von `validate_paios.py` erzwungen)

- **Vault-Ordner** mit Nummernpräfix — Pflicht: `00_meta`, `10_knowledge`, `20_projects`,
  `50_memory`; empfohlen: `30_workflows`, `40_skills`, `90_archive`; optional: `60_prompts`.
  `00_meta/` MUSS `paios.yaml` **und** `principles.md` enthalten.
- **Dateiformat** — jede Primärdatei = YAML-Frontmatter (`---`) + Markdown-Körper, UTF-8.
  Dateinamen klein, ohne Sonderzeichen, mit `-`, möglichst = `id`.
- **Frontmatter-Pflichtfelder** — `id`, `type`, `title`, `created` (ISO-8601 `YYYY-MM-DD`).
  `type` ∈ {knowledge, project, workflow, skill, memory, meta, moc}. Optional: `updated`, `tags`,
  `links`, `source`, `status`, `owner`.
- **IDs** — Schema `<präfix>-<jahr>-<laufnr>` (z. B. `k-2026-0001`). Präfixe: `k` knowledge,
  `p` project, `w` workflow, `s` skill, `m` memory. `doc-`/`moc-`-Dokumente dürfen sprechende IDs
  führen. IDs **nie** wiederverwenden. (Regex maßgeblich in `tools/validate_paios.py`.)
- **Verknüpfung** — maschinell über `links:` (Liste von IDs), menschlich über `[[Wikilinks]]`;
  je Kategorie eine `_<name>.md`-MOC.
- **Keine Secrets** im Vault/Repo. `.gitignore` blockt gängige Muster; der Validator meldet
  Secret-artige Funde als **Fehler** (nicht nur Warnung).
- **Konformität** — Level 1: Pflichtordner + `paios.yaml`/`principles.md` + gültiges Frontmatter +
  ID-Schema + keine Secrets. Level 2 ergänzt: MOCs je Kategorie, Git, MCP-Anbindung.

## Gotchas / aktueller Stand

- **Repo-Pfad in der Doku ist veraltet:** `STATUS.md`/`PUBLISH-GITHUB.md` nennen
  `C:\Users\user\PAIOS_Repo`; tatsächlich liegt das aktive Git-Repo unter
  `…\OneDrive\KI - AI\06_Projekte\PAIOS_Repo`.
- **Lizenz** ist dual: `LICENSE` (MIT, für `tools/`) und `LICENSE-DOCS` (CC BY-SA 4.0, für die
  Dokumentation/Spec). Neue Dateien entsprechend zuordnen.
- Git: erst zwei Commits, **kein Remote**; `STATUS.md` ist **untracked**.
- **MCP** ist nur *vorbereitet* — braucht installiertes **Node.js** (siehe `mcp/SETUP-MCP.md`);
  Paketnamen der MCP-Server vor Nutzung gegen die aktuelle MCP-Doku gegenprüfen.
- Bei jeder Standard-Änderung: Version in `spec/STANDARD.md` bumpen **und** `validate_paios.py`
  sowie `reference-vault/` konsistent mitziehen; danach `validate_paios.py reference-vault` (Exit 0).
