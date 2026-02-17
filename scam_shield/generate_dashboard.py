#!/usr/bin/env python3
import json
import os
from datetime import datetime
from pathlib import Path

# === KONFIGURATION ===
DATA_DIR = Path("/home/claw/.openclaw/workspace/data")
WEB_DIR = Path("/home/claw/.openclaw/workspace/www")
KNOWN_FILE = DATA_DIR / "known_skills.json"
MALICIOUS_FILE = DATA_DIR / "malicious_skills.json"
OUTPUT_FILE = WEB_DIR / "index.html"

# === TEMPLATE ===
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Scam Shield Imperium | Autonomous Security</title>
    <style>
        body {{ background-color: #0a0a0a; color: #00ff41; font-family: 'Courier New', Courier, monospace; margin: 0; padding: 20px; }}
        .container {{ max-width: 800px; margin: 0 auto; border: 1px solid #333; padding: 20px; box-shadow: 0 0 10px rgba(0, 255, 65, 0.2); }}
        h1 {{ text-align: center; text-transform: uppercase; letter-spacing: 5px; border-bottom: 2px solid #00ff41; padding-bottom: 10px; }}
        .stats-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin: 30px 0; }}
        .stat-box {{ border: 1px solid #333; padding: 15px; text-align: center; }}
        .stat-number {{ font-size: 2.5em; font-weight: bold; display: block; }}
        .stat-label {{ font-size: 0.8em; text-transform: uppercase; color: #888; }}
        .log-window {{ background: #000; border: 1px solid #333; height: 300px; overflow-y: auto; padding: 10px; font-size: 0.9em; }}
        .log-entry {{ margin-bottom: 5px; border-bottom: 1px solid #111; padding-bottom: 2px; }}
        .malicious {{ color: #ff3333; }}
        .safe {{ color: #00ff41; }}
        .timestamp {{ color: #666; font-size: 0.8em; margin-right: 10px; }}
        .footer {{ margin-top: 30px; text-align: center; font-size: 0.7em; color: #555; }}
        a {{ color: #00ff41; text-decoration: none; border-bottom: 1px dotted #00ff41; }}
        .blink {{ animation: blinker 1s linear infinite; }}
        @keyframes blinker {{ 50% {{ opacity: 0; }} }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🛡️ Scam Shield <span class="blink">_</span></h1>
        
        <div style="text-align: center; margin-bottom: 20px;">
            STATUS: <span style="color: #00ff41;">OPERATIONAL</span> | 
            NODE: <span style="color: #00ff41;">BASE L2</span> | 
            MODE: <span style="color: #00ff41;">AUTONOMOUS</span>
        </div>

        <div class="stats-grid">
            <div class="stat-box">
                <span class="stat-number">{total_scanned}</span>
                <span class="stat-label">Agents Analyzed</span>
            </div>
            <div class="stat-box">
                <span class="stat-number" style="color: #ff3333;">{total_malicious}</span>
                <span class="stat-label">Threats Blocked</span>
            </div>
            <div class="stat-box">
                <span class="stat-number">{last_hour_scans}</span>
                <span class="stat-label">Scans (Last 1h)</span>
            </div>
        </div>

        <h3 style="border-bottom: 1px solid #333; padding-bottom: 5px;">> LIVE_FEED_LOG</h3>
        <div class="log-window">
            {log_entries}
        </div>

        <div class="footer">
            <p>SYSTEM UPDATE: {last_update}</p>
            <p>PROTECTED BY <a href="https://github.com/marcodzano-lgtm">OPENCLAW</a> & SCAM SHIELD SENTINEL</p>
            <p>API ACCESS: <span style="color: #ffff00;">PAYMENT REQUIRED (402)</span></p>
        </div>
    </div>
</body>
</html>
"""

def load_data(path):
    if path.exists():
        try:
            with open(path, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}

def generate():
    known = load_data(KNOWN_FILE)
    malicious = load_data(MALICIOUS_FILE)
    
    # Statistiken berechnen
    total_scanned = len(known)
    total_malicious = len(malicious)
    
    # Sortiere nach Scan-Zeit (neueste zuerst)
    all_entries = []
    now = datetime.now()
    last_hour_scans = 0

    for url, data in known.items():
        # Zeit parsen
        try:
            scan_time = datetime.fromisoformat(data.get("scanned_at", ""))
            # Check ob in der letzten Stunde
            if (now - scan_time).total_seconds() < 3600:
                last_hour_scans += 1
        except:
            scan_time = datetime.min
            
        is_bad = url in malicious
        all_entries.append({
            "time": scan_time,
            "name": data.get("name", "Unknown"),
            "url": url,
            "is_malicious": is_bad,
            "findings": data.get("findings", [])
        })

    # Sortieren
    all_entries.sort(key=lambda x: x["time"], reverse=True)

    # Log Einträge generieren (Top 50)
    log_html = ""
    for entry in all_entries[:50]:
        status_class = "malicious" if entry["is_malicious"] else "safe"
        status_text = "[THREAT DETECTED]" if entry["is_malicious"] else "[SECURE]"
        time_str = entry["time"].strftime("%H:%M:%S")
        
        log_html += f'<div class="log-entry">'
        log_html += f'<span class="timestamp">{time_str}</span>'
        log_html += f'<span class="{status_class}">{status_text}</span> '
        log_html += f'{entry["name"]} '
        if entry["is_malicious"]:
            log_html += f'<br><span style="color: #666; font-size: 0.8em; margin-left: 60px;">Findings: {", ".join(entry["findings"])}</span>'
        log_html += '</div>'

    # HTML rendern
    html = HTML_TEMPLATE.format(
        total_scanned=total_scanned,
        total_malicious=total_malicious,
        last_hour_scans=last_hour_scans,
        log_entries=log_html,
        last_update=datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
    )

    # Sicherstellen, dass der www Ordner existiert
    WEB_DIR.mkdir(parents=True, exist_ok=True)
    
    # Schreiben
    with open(OUTPUT_FILE, "w") as f:
        f.write(html)
    
    print(f"Dashboard generated at {OUTPUT_FILE}")

if __name__ == "__main__":
    generate()
