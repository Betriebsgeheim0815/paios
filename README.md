# PAIOS – Personal AI Operating System

**Ein modellunabhängiger Wissens- und Workflow-Standard.**
Dein Wissen gehört dir. Modelle sind austauschbar. Der Workflow bleibt stabil.

> „Das Git für KI-Wissensarbeit."

## Was ist PAIOS?

PAIOS ist **kein Programm und kein Anbieter**, sondern ein offener Standard dafür, wie ein Mensch sein Wissen, seine Projekte und Arbeitsabläufe modellunabhängig strukturiert, versioniert und über KI-Anbieter hinweg trägt.

- **Format:** Markdown + YAML-Frontmatter, versioniert mit Git
- **Speicher:** lokaler Wissensspeicher (Referenz: Obsidian-Vault)
- **Schnittstelle:** MCP (Model Context Protocol)
- **Modell:** austauschbar (Claude / GPT / Gemini …)

## Architektur

```
Mensch → Modell (austauschbar) → MCP → PAIOS-Vault (Markdown + Git)
```

## Repo-Struktur

```
paios/
├── README.md                 # dieses Dokument
├── LICENSE                   # offene Lizenz (Vorschlag: CC BY-SA 4.0 / MIT für Tools)
├── MANIFEST.md               # Warum PAIOS existiert
├── spec/
│   ├── STANDARD.md           # Die Spezifikation (MUSS/SOLLTE/KANN)
│   ├── ARCHITECTURE.md       # Architekturhandbuch
│   └── DATA-MODEL.md         # Datenmodell + Entitäten
├── reference-vault/          # minimaler, konformer Beispiel-Vault
│   ├── 00_meta/
│   ├── 10_knowledge/
│   ├── 20_projects/
│   ├── 30_workflows/
│   ├── 40_skills/
│   ├── 50_memory/
│   └── 90_archive/
├── tools/
│   └── validate_paios.py     # Konformitäts-Prüfer (Standard §10)
├── .gitignore
└── CONTRIBUTING.md
```

## Schnellstart

```bash
# Vault auf Konformität prüfen
python tools/validate_paios.py path/to/vault
```

## Status

Frühe Phase (v0.1). Standard, Architektur und Referenzstruktur stehen; Validierung ist implementiert.

## Lizenz

Dual-Lizenz:
- **Software/Tools** (v. a. `tools/`) unter **MIT** — siehe [`LICENSE`](LICENSE).
- **Dokumentation & Standard** (README, MANIFEST, `spec/`, `reference-vault/`, `mcp/`) unter
  **CC BY-SA 4.0** — siehe [`LICENSE-DOCS`](LICENSE-DOCS).
