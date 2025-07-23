import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from collections import deque
from utils.utils import (
    getHeaders, sleepRandom, shouldCrawlUrl
)
from config import baseUrl, maxPages, maxDepth
from urllib.robotparser import RobotFileParser



outputFilePath = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "foundLinks.txt")
visitedUrls = set()
seenUrls = set()

def normalizeUrl(url):
    return url.split("#")[0].rstrip("/")

def isSameDomain(url1, url2):
    return urlparse(url1).netloc == urlparse(url2).netloc

def getCachedRobotsParser(startUrl):
    parsed = urlparse(startUrl)
    robotsUrl = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
    try:
        response = requests.get(robotsUrl, headers=getHeaders(), timeout=10)
        response.raise_for_status()
        rp = RobotFileParser()
        rp.parse(response.text.splitlines())
        print(f"[INFO] robots.txt loaded from {robotsUrl}")
        return rp
    except Exception as e:
        print(f"[WARNING] Could not fetch robots.txt: {e}")
        rp = RobotFileParser()
        rp.parse("")
        return rp

def crawl(startUrl):
    robotsParser = getCachedRobotsParser(startUrl)
    queue = deque([(startUrl, 0)])
    os.makedirs(os.path.dirname(outputFilePath), exist_ok=True)

    with open(outputFilePath, "w", encoding="utf-8") as f:
        pass

    while queue and len(visitedUrls) < maxPages:
        currentUrl, depth = queue.popleft()
        currentUrl = normalizeUrl(currentUrl)

        if currentUrl in visitedUrls or depth > maxDepth:
            continue

        if not robotsParser.can_fetch("*", currentUrl):
            print(f"[robots.txt blocked] {currentUrl}")
            continue

        if not shouldCrawlUrl(currentUrl, baseUrl):
            print(f"[Filtered out by config] {currentUrl}")
            continue

        print(f"[Crawling] Depth {depth} | Queue: {len(queue)} | URL: {currentUrl}")

        try:
            response = requests.get(currentUrl, headers=getHeaders(), timeout=10)
            response.raise_for_status()
            html = response.text
        except Exception as e:
            print(f"[Error] {currentUrl}: {e}")
            continue

        visitedUrls.add(currentUrl)

        with open(outputFilePath, "a", encoding="utf-8") as f:
            f.write(currentUrl + "\n")

        soup = BeautifulSoup(html, "html.parser")
        for tag in soup.find_all("a", href=True):
            href = tag["href"]
            absUrl = normalizeUrl(urljoin(currentUrl, href))

            if not isSameDomain(baseUrl, absUrl):
                continue
            if absUrl in visitedUrls or absUrl in seenUrls:
                continue

            seenUrls.add(absUrl)
            queue.append((absUrl, depth + 1))

        sleepRandom(1.5, 3.5)

if __name__ == "__main__":
    crawl(baseUrl)
