import random
import time
import requests
from urllib.robotparser import RobotFileParser
from urllib.parse import urlparse

userAgents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:115.0) Gecko/20100101 Firefox/115.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.0.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Safari/605.1.15',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (Linux; Android 13; Pixel 7 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (Android 13; Mobile; rv:115.0) Gecko/115.0 Firefox/115.0',
]

def isInformationalUrl(url):

    blacklist_keywords = [
        "about", "faq", "contact", "help", "support", "terms", "privacy", "legal",
        "donate", "volunteer", "news", "blog", "jobs", "staff", "history", "press",
        "policy", "project"
    ]
    path = urlparse(url).path.lower()
    return any(f"/{kw}" in path or path.endswith(kw) for kw in blacklist_keywords)

def getHeaders():
    return {
        'User-Agent': random.choice(userAgents),
        'Accept-Language': 'en-US,en;q=0.9',
    }

def sleepRandom(minSec=2.0, maxSec=5.0):
    time.sleep(random.uniform(minSec, maxSec))

def getRobotsParser(baseUrl):
    parsedUrl = urlparse(baseUrl)
    robotsUrl = f"{parsedUrl.scheme}://{parsedUrl.netloc}/robots.txt"
    rp = RobotFileParser()
    rp.set_url(robotsUrl)
    try:
        rp.read()
    except Exception as e:
        print(f"[Warning] Could not fetch robots.txt from {robotsUrl}: {e}")
    return rp

def isUrlAllowed(url, rp):
    return rp.can_fetch("*", url)


