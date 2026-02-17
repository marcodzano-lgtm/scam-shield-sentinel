#!/usr/bin/env python3
import os
import json
import time
import urllib.request
import urllib.parse
import subprocess
from datetime import datetime
from pathlib import Path

# ============= KONFIGURATION =============
# Pfade
DATA_DIR = Path("./data")
DATA_DIR.mkdir(exist_ok=True)
KNOWN_SKILLS_FILE = DATA_DIR / "known_skills.json"
MALICIOUS_SKILLS_FILE = DATA_DIR / "malicious_skills.json"
CONFIG_FILE = Path.home() / ".openclaw" / "openclaw.json"

# Helper zum Laden der Secrets direkt aus der JSON Config
def load_env_from_json():
    secrets = {}
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, 'r') as f:
                data = json.load(f)
                secrets = data.get("env", {})
        except Exception as e:
            print(f"Fehler beim Laden der Config: {e}")
    return secrets

# Lade Secrets (Vorrang: Environment Vars -> JSON Config)
config_env = load_env_from_json()

GITHUB_TOKEN = os.environ.get("GITHUB_SEARCH_TOKEN") or config_env.get("GITHUB_SEARCH_TOKEN")
NEYNAR_API_KEY = os.environ.get("NEYNAR_API_KEY") or config_env.get("NEYNAR_API_KEY")
TELEGRAM_TOKEN = os.environ.get("SCAM_SHIELD_TELEGRAM_BOT_TOKEN") or config_env.get("SCAM_SHIELD_TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("SCAM_SHIELD_TELEGRAM_CHAT_ID") or config_env.get("SCAM_SHIELD_TELEGRAM_CHAT_ID")

SCAN_INTERVAL = 3600  # Alle 60 Minuten
OUR_WALLET = "0x8F9222257C9a39a684fC6aAeEa03A556FBbccAc8"

# ============= HELPER =============
def log(message, level="info"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {level.upper()}: {message}")

def load_json(filepath):
    if filepath.exists():
        try:
            with open(filepath, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_json(filepath, data):
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)

def send_telegram(message):
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        log("Telegram Token fehlt, Nachricht nicht gesendet.", "warning")
        return
    
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    try:
        req = urllib.request.Request(
            url, 
            data=json.dumps(payload).encode(), 
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req) as res:
            pass
    except Exception as e:
        log(f"Telegram Fehler: {e}", "error")

# ============= QUELLEN SCANNER =============
def fetch_github_skills():
    if not GITHUB_TOKEN:
        log("Kein GitHub Token gefunden! GitHub-Suche deaktiviert.", "warning")
        return []
        
    log(f"Using GitHub Token (first 5 chars): {GITHUB_TOKEN[:5] if GITHUB_TOKEN else 'None'}...")
    log("📡 Scanne GitHub nach neuen Skills...")
    query = "openclaw skill OR autonomous agent skill created:>2025-12-01"
    encoded_query = urllib.parse.quote(query)
    url = f"https://api.github.com/search/repositories?q={encoded_query}&sort=created&order=desc&per_page=50"
    
    req = urllib.request.Request(url, headers={
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "ScamShield-Sentinel"
    })
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            return data.get("items", [])
    except urllib.error.HTTPError as http_error:
        error_body = http_error.read().decode('utf-8', errors='ignore')
        log(f"GitHub API HTTP Fehler: Status {http_error.code}, Reason: {http_error.reason}, Body: {error_body}", "error")
        return []
    except Exception as e:
        log(f"GitHub API Fehler: {e}", "error")
        return []

# ============= ANALYSE ENGINE =============
def analyze_repo_content(repo_url, full_name):
    # API URL bauen
    api_url = repo_url.replace("github.com", "api.github.com/repos") + "/contents"
    req = urllib.request.Request(api_url, headers={
        "Authorization": f"token {GITHUB_TOKEN}",
        "User-Agent": "ScamShield-Sentinel"
    })
    
    findings = []
    suspicious_keywords = [
        "eval(", "exec(", "subprocess", "os.system", "curl ", "wget ", 
        "wallet_private_key", "mnemonic", "base64", "obfuscate"
    ]

    try:
        with urllib.request.urlopen(req) as response:
            contents = json.loads(response.read().decode())
            
            for item in contents:
                if item["type"] == "file" and (item["name"].endswith(".py") or item["name"].endswith(".js")):
                    file_req = urllib.request.Request(item["download_url"])
                    with urllib.request.urlopen(file_req) as f:
                        code = f.read().decode('utf-8', errors='ignore')
                        
                        for word in suspicious_keywords:
                            if word in code:
                                findings.append(f"Suspicious keyword '{word}' in {item['name']}")
                        
                        if "approve" in code and "max_uint" in code.lower():
                             findings.append("⚠️ HIGH RISK: Potential Wallet Drainer (Infinite Approval)")

    except Exception as e:
        log(f"Content Analyse Fehler für {full_name}: {e}", "error")
        
    return findings

# ============= MAIN LOOP =============
def run_sentinel():
    log("🛡️ Scam Shield Sentinel gestartet (v2.0 - Config Loaded).")
    
    if GITHUB_TOKEN:
        log("✅ GitHub Token geladen.")
    else:
        log("❌ GitHub Token fehlt immer noch! GitHub-Suche kann nicht ausgeführt werden.", "error")


    send_telegram("🛡️ **Scam Shield Sentinel** ist online und hat die Konfiguration geladen.")

    while True:
        try:
            known = load_json(KNOWN_SKILLS_FILE)
            malicious = load_json(MALICIOUS_SKILLS_FILE)
            
            # 1. GitHub Scan
            repos = fetch_github_skills()
            new_threats = []
            
            for repo in repos:
                url = repo["html_url"]
                full_name = repo["full_name"]
                
                if url in known:
                    continue 
                
                log(f"🔍 Analysiere neuen Skill: {full_name}")
                findings = analyze_repo_content(url, full_name)
                
                skill_data = {
                    "name": full_name,
                    "url": url,
                    "findings": findings,
                    "scanned_at": datetime.now().isoformat()
                }
                
                known[url] = skill_data
                
                if findings:
                    malicious[url] = skill_data
                    new_threats.append(f"🚨 *{full_name}*\nFindings: {', '.join(findings)}\n[Link]({url})")
                    log(f"🚨 THREAT: {full_name}", "warning")
            
            save_json(KNOWN_SKILLS_FILE, known)
            save_json(MALICIOUS_SKILLS_FILE, malicious)
            
            if new_threats:
                msg = f"⚠️ **Bedrohungsbericht** ⚠️\n\n" + "\n\n".join(new_threats)
                send_telegram(msg)
                
                # Auto-Post
                promo = f"🛡️ Scam Shield Alert: Blocked {len(new_threats)} new malicious agents.\n🔍 Verify skills: https://scamshield.duckdns.org\n#OpenClaw #Security"
                subprocess.run(["node", "skills/farcaster_poster/farcaster_post.js", promo])
            
            else:
                log(f"Scan beendet. {len(repos)} Repos geprüft.")

            log(f"Schlafe für {SCAN_INTERVAL} Sekunden...")
            time.sleep(SCAN_INTERVAL)
            
        except KeyboardInterrupt:
            log("Sentinel gestoppt.")
            break
        except Exception as e:
            log(f"CRITICAL LOOP ERROR: {e}", "error")
            send_telegram(f"❌ **Systemfehler** im Sentinel: {e}")
            time.sleep(60)

if __name__ == "__main__":
    run_sentinel()
