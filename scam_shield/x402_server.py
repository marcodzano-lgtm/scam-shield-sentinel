#!/usr/bin/env python3
"""
x402 Threat-Intelligence Server v2 (Gemini Research Edition)
Lauscht auf Port 8888, implementiert 402 Payment Required Logik.
"""
import http.server
import socketserver
import json
import urllib.parse
from pathlib import Path

PORT = 8888
MALICIOUS_FILE = Path("./data/malicious_skills.json")
TREASURY_LOG = Path("./TREASURY_LOG.md")
OUR_WALLET = "0x8F9222257C9a39a684fC6aAeEa03A556FBbccAc8"

def load_malicious():
    if MALICIOUS_FILE.exists():
        with open(MALICIOUS_FILE) as f:
            return json.load(f)
    return {}

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path != "/check":
            self.send_response(404)
            self.end_headers()
            return

        # PRÜFUNG: x402 Payment Header (Simulation für M2M-Ökonomie)
        # In einer vollen Implementierung würden wir hier den L402-Token validieren
        payment_header = self.headers.get("X-402-Payment-Proof")
        
        if not payment_header:
            # Sende 402 Payment Required zurück
            self.send_response(402)
            self.send_header("Content-Type", "application/json")
            self.send_header("X-402-Amount", "0.001")
            self.send_header("X-402-Currency", "USDC")
            self.send_header("X-402-Wallet", OUR_WALLET)
            self.end_headers()
            response = {
                "error": "Payment Required",
                "amount": "0.001 USDC",
                "address": OUR_WALLET,
                "network": "Base L2"
            }
            self.wfile.write(json.dumps(response).encode())
            return

        # Wenn bezahlt (Header vorhanden):
        qs = urllib.parse.parse_qs(parsed.query)
        skill = qs.get("skill", [None])[0]
        
        malicious_db = load_malicious()
        result = {"skill": skill, "malicious": False, "details": None}
        
        for url, data in malicious_db.items():
            if skill and (skill.lower() in url.lower() or data.get("name", "").lower() == skill.lower()):
                result["malicious"] = True
                result["details"] = data
                break

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(result, indent=2).encode())
        
        # Logging der Einnahme
        with open(TREASURY_LOG, "a") as f:
            f.write(f"\n[x402-REVENUE] {datetime.datetime.now().isoformat()} - 0.001 USDC for skill check: {skill}")

if __name__ == "__main__":
    import datetime
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"x402 Server (Gemini Optimized) running on port {PORT}")
        httpd.serve_forever()
