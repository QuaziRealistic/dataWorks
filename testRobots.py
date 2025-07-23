import requests
from urllib.robotparser import RobotFileParser
from urllib.parse import urlparse


def debug_robots_txt(url: str, user_agent: str = "*"):
    parsed_url = urlparse(url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
    robots_url = f"{base_url}/robots.txt"

    print(f"\n[INFO] Try: {robots_url}")

    try:
        response = requests.get(robots_url, timeout=10)
        print(f"[HTTP] Status: {response.status_code}")
        print("[robots.txt] Contents:\n")
        print(response.text)
    except Exception as e:
        print(f"[Error.txt]: {e}")
        return

    rp = RobotFileParser()
    rp.set_url(robots_url)
    try:
        rp.read()
    except Exception as e:
        print(f"[Error RobotFileParser.read()]: {e}")
        return

    result = rp.can_fetch(user_agent, url)
    print(f"\n[RESULT] can_fetch({user_agent}, {url}) = {result}")


if __name__ == "__main__":
    test_url = "https://rulebook.centralbank.ae/"
    debug_robots_txt(test_url)
