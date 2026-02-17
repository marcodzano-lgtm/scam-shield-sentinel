import urllib.request
import re
import json

def fetch_skills():
    url = "https://clawhub.ai/skills"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as response:
            html = response.read().decode('utf-8')
            # Suche nach Skill-Links: /skill/name-slug
            links = re.findall(r'href=["\'](/skill/[^"\']+)["\']', html)
            # Duplikate entfernen und Basis-URL hinzufügen
            unique_links = list(set(["https://clawhub.ai" + l for l in links]))
            return unique_links
    except Exception as e:
        print(f"Fehler beim Crawlen: {e}")
        return []

if __name__ == "__main__":
    skills = fetch_skills()
    print(json.dumps(skills, indent=2))
