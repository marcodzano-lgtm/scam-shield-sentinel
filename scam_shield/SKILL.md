---
name: Scam Shield
version: 1.0.0
description: Autonomer Scam-Detector für OpenClaw Skills. Scannt ClawHub, analysiert mit Gemini 3 Flash, postet Alerts auf Telegram, stellt x402-API bereit.
author: DeinImperium
permissions:
  - network
  - filesystem:read
  - filesystem:write:./data
  - command:python3
---

# Scam Shield Skill

## 🔍 Funktion
- Scannt ClawHub/Clawmart alle 6h nach NEUEN/UPDATE-Skills
- Lädt ZIP herunter, extrahiert SKILL.md + Scripts
- Führt 3-stufige Analyse durch:
  1. **Statische Pattern-Analyse** (curl | bash, base64, eval, .env, ~/.ssh)
  2. **Gemini 3 Flash Analyse** (Zero-Shot Malware Classification)
  3. **Vertrauens-Score** (Autor-Reputation, Downloads)
- Postet Warnungen auf Telegram (optional)
- Bietet x402-geschützten API-Endpunkt für Abfragen

## ⚙️ Konfiguration
Umgebungsvariablen (in openclaw.json):
- `SCAM_SHIELD_TELEGRAM_BOT_TOKEN` – für autonome Posts (optional)
- `SCAM_SHIELD_TELEGRAM_CHAT_ID` – Ziel-Kanal/Group (optional)
- `VT_API_KEY` – optional, für VirusTotal (nicht erforderlich)

## 🚀 Verwendung
Der Skill läuft vollautonom via Cron. Manuelle Befehle:
- `/query <signature>` – Prüft eine Signatur gegen die x402-Datenbank (Kosten: 0.001 USDC)
- `/scan_now` – Sofortscan ausführen
- `/get_stats` – Anzahl analysierte Skills, gefundene Scams

## 💰 x402 Monetarisierung
Jede Abfrage über die API oder den `/query` Befehl löst im x402-Netzwerk eine Transaktion von 0.001 USDC an die Wallet des Agenten aus. Dies geschieht autonom auf der Base L2.

## ⚠️ Sicherheitshinweis
Dieser Skill hat NETWORK-Zugriff und schreibt in ./data. Kein Zugriff auf .env des Hauptsystems.
