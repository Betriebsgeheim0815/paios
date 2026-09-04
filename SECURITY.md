# Sicherheitsrichtlinie

PAIOS speichert Wissen in Dateien und kann über MCP Schreibwerkzeuge anbieten.
MCP-Server und importierte Wissensartefakte sind Vertrauensgrenzen.

- Zugangsdaten, Tokens und private Schlüssel gehören niemals in Vault oder Git.
- Erteile dem Filesystem-Server nur Zugriff auf den kleinsten nötigen Ordner.
- Lese-, Änderungs- und Löschoperationen sollen getrennt freigegeben werden.
- Vor destruktiven Änderungen muss ein Mensch den konkreten Diff prüfen.
- MCP-Pakete sind auf geprüfte Versionen festzulegen.

## Sicherheitslücke melden

Bitte keine Sicherheitslücke öffentlich als Issue melden. Nutze **Security →
Report a vulnerability** im Repository oder kontaktiere den Eigentümer
vertraulich über GitHub.
