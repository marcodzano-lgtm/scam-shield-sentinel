import urllib.request
import json
import os
import re

NEYNAR_API_KEY = os.environ.get("NEYNAR_API_KEY")

def discover_via_farcaster():
    print("Suche neue Skills via Farcaster (Neynar)...")
    url = "https://api.neynar.com/v2/farcaster/cast/search?q=clawhub.ai/skill/&limit=20"
    req = urllib.request.Request(url, headers={"api_key": NEYNAR_API_KEY})
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            casts = data.get("result", {}).get("casts", [])
            links = []
            for cast in casts:
                found = re.findall(r'https://clawhub.ai/skill/[^\s\)]+', cast.get("text", ""))
                links.extend(found)
            return list(set(links))
    except Exception as e:
        print(f"Neynar Fehler: {e}")
        return []

if __name__ == "__main__":
    links = discover_via_farcaster()
    print(f"Gefundene Skill-Links via Farcaster: {len(links)}")
    for l in links:
        print(f" - {l}")
