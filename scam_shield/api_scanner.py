import urllib.request
import json
import os

def scan_via_firecrawl():
    api_key = os.environ.get("FIRECRAWL_API_KEY")
    if not api_key:
        print("Fehler: FIRECRAWL_API_KEY nicht gesetzt.")
        return []
    
    url = "https://api.firecrawl.dev/v1/scrape"
    payload = {
        "url": "https://clawhub.ai/skills?sort=newest",
        "formats": ["links"],
        "onlyMainContent": True
    }
    
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode(),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        },
        method="POST"
    )
    
    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode())
            links = result.get("links", [])
            skill_links = [l for l in links if "/skill/" in l]
            return skill_links
    except Exception as e:
        print(f"Firecrawl Fehler: {e}")
        return []

if __name__ == "__main__":
    links = scan_via_firecrawl()
    print(f"Gefundene Skills: {len(links)}")
    for l in links[:5]:
        print(f" - {l}")
