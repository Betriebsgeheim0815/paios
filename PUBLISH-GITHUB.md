# PAIOS auf GitHub veröffentlichen

Das lokale Repo ist bereits initialisiert und committet (`C:\Users\user\PAIOS_Repo`).
Zum Veröffentlichen fehlt nur Ihre GitHub-Anmeldung.

## Variante A – GitHub CLI (empfohlen)
```powershell
cd C:\Users\user\PAIOS_Repo
gh auth login              # einmalig anmelden
gh repo create paios --public --source=. --remote=origin --push
```

## Variante B – manuell
1. Auf github.com ein leeres Repo `paios` anlegen (ohne README).
2. Dann:
```powershell
cd C:\Users\user\PAIOS_Repo
git branch -M main
git remote add origin https://github.com/<DEIN-USER>/paios.git
git push -u origin main
```

## Vor dem Push prüfen
- `.gitignore` blockt Secrets – trotzdem kurz `git ls-files` ansehen.
- Lizenz final festlegen (Vorschlag: Docs CC BY-SA 4.0, Tools MIT).

## Hinweis
Ich (KI-BOT) pushe nicht mit Ihren Zugangsdaten. Der letzte Schritt liegt bei Ihnen.
