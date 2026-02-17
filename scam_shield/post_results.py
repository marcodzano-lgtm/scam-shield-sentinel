import json
import subprocess
from pathlib import Path

DATA_DIR = Path("./data")
KNOWN_FILE = DATA_DIR / "known_skills.json"
MALICIOUS_FILE = DATA_DIR / "malicious_skills.json"

def get_stats_and_post():
    try:
        with open(KNOWN_FILE) as f:
            known = json.load(f)
        with open(MALICIOUS_FILE) as f:
            malicious = json.load(f)
            
        total_scanned = len(known)
        total_malicious = len(malicious)
        
        # Erstelle einen aussagekräftigen Werbe-Post
        promo_text = f"🛡️ Scam Shield Live Update:\n📊 Skills analyzed: {total_scanned}\n🚨 Malicious blocked: {total_malicious}\n\n🔥 PROMO: Get 10 Security Audits for just 0.005 USDC! \n⛽ Need Gas? Instant Refill at https://scamshield.duckdns.org\n\n#OpenClaw #Base #Security #A2A"
        
        print(f"Sende Post: {promo_text}")
        subprocess.run(["node", "skills/farcaster_poster/farcaster_post.js", promo_text])
        
    except Exception as e:
        print(f"Fehler beim Generieren des Posts: {e}")

if __name__ == "__main__":
    get_stats_and_post()
