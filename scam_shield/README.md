# Scam Shield Autopilot v2

Dieser Skill ist Teil des Scam Shield Imperiums und dient der automatischen Erkennung und Meldung potenziell bösartiger OpenClaw-Skills auf GitHub. Er integriert sich mit Farcaster, um Berichte zu posten.

## Funktionen

*   Scannt GitHub-Repositories nach OpenClaw-Skills.
*   Analysiert Skill-Code auf verdächtige Muster (z.B. Remote Exec, Dynamic Eval, Credential Interest).
*   Postet Berichte über entdeckte Bedrohungen auf Farcaster.

## Einrichtung

Um diesen Skill zu nutzen, müssen folgende Umgebungsvariablen in der `openclaw.json` (im `env`-Objekt) Ihres OpenClaw-Setups konfiguriert werden:

*   `GITHUB_SEARCH_TOKEN`: Ein GitHub Personal Access Token mit den Rechten `repo` (für den Backup-Push) und `public_repo` (für GitHub-Suchanfragen).
*   `NEYNAR_API_KEY`: Ihr API-Schlüssel von Neynar (für Farcaster-Interaktionen).
*   `NEYNAR_SIGNER_UUID`: Ihre Signer UUID für Neynar.

## Nutzung

Der Skill kann manuell ausgeführt werden:

```bash
python3 ~/.openclaw/workspace/skills/scam_shield/main.py
```

Für den automatischen Betrieb richten Sie einen täglichen Cron-Job ein, der dieses Skript ausführt.

## Entwicklung

Der Code ist so konzipiert, dass alle sensiblen Informationen über Umgebungsvariablen bezogen werden, um maximale Sicherheit und Transparenz zu gewährleisten.
