---
id: doc-manifest
type: meta
title: "PAIOS Manifest"
version: 1.0
created: 2026-07-13
owner: "Dr. Dhoni"
---

# PAIOS Manifest

**PAIOS – Personal AI Operating System.** Ein modellunabhängiger Wissens- und Workflow-Standard, der dem Menschen die Kontrolle über sein Wissen zurückgibt, während KI-Modelle zu austauschbaren Werkzeugen werden.

---

## 1. Warum PAIOS existiert

KI-Wissen zersplittert. Jeder Anbieter – ChatGPT, Claude, Gemini – speichert Kontext in seinem eigenen, geschlossenen Gedächtnis. Beim Wechsel des Modells geht der Zusammenhang verloren; der Workflow muss jedes Mal neu gebaut werden. Der Nutzer arbeitet für das Modell, nicht das Modell für den Nutzer.

PAIOS kehrt dieses Verhältnis um: **Das Wissen bleibt beim Menschen. Das Modell kommt und geht.**

---

## 2. Was PAIOS ist

PAIOS ist **kein Programm und kein weiterer Anbieter**, sondern ein **offener Standard** dafür, wie ein Mensch sein Wissen, seine Projekte und Arbeitsabläufe modellunabhängig strukturiert, versioniert und über Anbieter hinweg trägt.

- **Format:** Markdown + YAML-Frontmatter, versioniert mit Git.
- **Speicher:** ein lokaler, dem Nutzer gehörender Wissensspeicher (Referenz: Obsidian-Vault).
- **Schnittstelle:** MCP (Model Context Protocol) als offene Brücke zu beliebigen Modellen.
- **Rolle der KI:** austauschbarer Spezialist, der auf den Speicher zugreift – nicht dessen Besitzer.

PAIOS ist damit „das Git für KI-Wissensarbeit": ein Standard plus Referenzstruktur, nicht eine Software, die man kaufen muss.

---

## 3. Die sieben Prinzipien

1. **Wissen gehört dem Nutzer.** Reine Dateien, kein Anbieter-Silo.
2. **Modelle sind austauschbar.** Kein Lock-in an ein Modell.
3. **Der Workflow bleibt stabil.** Anbieterwechsel ändert die Arbeitsweise nicht.
4. **Offene Standards bevorzugen.** Markdown, Git, offene Schnittstellen (MCP).
5. **Modularität vor Komplexität.** Wenige, klare Bausteine.
6. **Der Mensch definiert Ziele; die KI unterstützt bei der Umsetzung.**
7. **Dokumentation ist die zentrale Wissensquelle.**

---

## 4. Was PAIOS NICHT ist

- **Kein neuer Modell-Standard** – PAIOS baut auf MCP auf, statt zu konkurrieren.
- **Kein Cloud-Dienst** – der Speicher liegt beim Nutzer; keine Abhängigkeit von einem Anbieter.
- **Kein reines Memory-Tool** – PAIOS standardisiert eine *Arbeitsweise*, nicht nur das Speichern von Fakten.
- **Kein Geheimnis-Tresor** – Zugangsdaten gehören in einen Passwort-Manager, niemals in den Vault.

---

## 5. Die Architektur in einem Satz

> **Obsidian (Wissensspeicher) → MCP (offene Schnittstelle) → austauschbares Modell.**
> Der Mensch führt; die Dokumentation ist die Wahrheit; Git bewahrt die Geschichte.

---

## 6. Das Versprechen

Wer nach PAIOS arbeitet, verliert beim nächsten Modellwechsel nichts. Sein Wissen wächst kumulativ, bleibt lesbar für Mensch und Maschine, und gehört ihm – heute, und wenn das heute führende Modell längst abgelöst ist.

---

*Version 1.0 – lebendes Dokument. Änderungen werden versioniert.*
