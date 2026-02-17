import urllib.request
import json
import os

GITHUB_TOKEN = os.environ.get("GITHUB_SEARCH_TOKEN")
def find_new_skills():
    print("Suche neue Skills auf GitHub...")
    # Suche nach Repositories, die "openclaw-skill" im Namen oder Beschreibung haben
    url = "https://api.github.com/search/repositories?q=openclaw+skill+created:>2026-02-01&sort=created&order=desc"
    req = urllib.request.Request(url, headers={"Authorization": f"token {GITHUB_TOKEN}"})
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            repos = data.get("items", [])
            return [r["html_url"] for r in repos]
    except Exception as e:
        print(f"GitHub Fehler: {e}")
        return []

if __name__ == "__main__":
    repos = find_new_skills()
    print(f"Gefundene neue Repos: {len(repos)}")
    for r in repos:
        print(f" - {r}")
