import requests
import re

def debug_fetch():
    # Wir versuchen es über eine andere bekannte ClawHub URL Struktur
    urls = [
        "https://clawhub.ai/skills",
        "https://clawhub.ai/api/skills",
        "https://clawhub.ai/explore"
    ]
    for url in urls:
        print(f"Prüfe {url}...")
        try:
            r = requests.get(url, timeout=10)
            print(f" Status: {r.status_code}, Länge: {len(r.text)}")
            if "/skill/" in r.text:
                print(f" Erfolg! Skill-Links in {url} gefunden.")
                links = re.findall(r'href="(/skill/[^"]+)"', r.text)
                print(f" Erste 3 Links: {links[:3]}")
        except Exception as e:
            print(f" Fehler bei {url}: {e}")

if __name__ == "__main__":
    debug_fetch()
