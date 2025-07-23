import requests
from urllib.parse import urlparse


def fetchRobotsTxt(url):

    from urllib.parse import urlparse

    parsed = urlparse(url)
    robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/115.0.0.0 Safari/537.36"
        ),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
    }

    try:
        print(f"[INFO] Fetching robots.txt: {robots_url}")
        response = requests.get(robots_url, headers=headers, timeout=10)
        print(f"[HTTP] Status Code: {response.status_code}")
        if response.status_code == 200:
            return response.text
        else:
            return None
    except Exception as e:
        print(f"[ERROR] {e}")
        return None



robots_cache = {}

def fetch_disallowed_paths(domain):
    robots_url = f"{domain}/robots.txt"
    try:
        resp = requests.get(robots_url, timeout=5)
        lines = resp.text.splitlines()
        disallowed = []
        user_agent = None
        for line in lines:
            line = line.strip()
            if line.lower().startswith('user-agent:'):
                user_agent = line.split(':', 1)[1].strip()
            elif user_agent == '*' and line.lower().startswith('disallow:'):
                path = line.split(':', 1)[1].strip()
                if path:
                    disallowed.append(path)
        return disallowed
    except Exception as e:
        print(f"[robots.txt ERROR] {e}")
        return []

def is_url_allowed(url):
    parsed = urlparse(url)
    domain = f"{parsed.scheme}://{parsed.netloc}"

    if domain not in robots_cache:
        robots_cache[domain] = fetch_disallowed_paths(domain)

    for rule in robots_cache[domain]:
        if parsed.path.startswith(rule):
            return False
    return True
