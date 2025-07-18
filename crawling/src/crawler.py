import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from collections import deque

from utils.utils import getHeaders, sleepRandom, getRobotsParser, isUrlAllowed

baseUrl = "https://openlibrary.org/"

maxPages = 100        # Max pages to crawl
maxDepth = 2          # Max crawl depth

outputFilePath = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "foundLinks.txt")

visitedUrls = set()

def isSameDomain(url1, url2):
    return urlparse(url1).netloc == urlparse(url2).netloc

def crawl(startUrl):
    robotsParser = getRobotsParser(startUrl)

    queue = deque([(startUrl, 0)])

    os.makedirs(os.path.dirname(outputFilePath), exist_ok=True)

    with open(outputFilePath, "w", encoding="utf-8") as f:
        pass  # Clear the file before writing

    while queue and len(visitedUrls) < maxPages:
        currentUrl, depth = queue.popleft()

        if currentUrl in visitedUrls:
            continue

        if depth > maxDepth:
            continue

        if not isUrlAllowed(currentUrl, robotsParser):
            print(f"[robots.txt blocked] {currentUrl}")
            continue

        print(f"[Crawling] Depth {depth}: {currentUrl}")

        try:
            response = requests.get(currentUrl, headers=getHeaders(), timeout=10)
            response.raise_for_status()
            html = response.text
            
        except Exception as e:
            print(f"[Error] Failed to fetch {currentUrl}: {e}")
            continue

        visitedUrls.add(currentUrl)

        with open(outputFilePath, "a", encoding="utf-8") as f:
            f.write(currentUrl + "\n")

        soup = BeautifulSoup(html, "html.parser")

        for aTag in soup.find_all("a", href=True):
            href = aTag["href"]
            absUrl = urljoin(currentUrl, href)
            if isSameDomain(baseUrl, absUrl) and absUrl not in visitedUrls:
                queue.append((absUrl, depth + 1))

        sleepRandom(2, 5)

if __name__ == "__main__":
    crawl(baseUrl)
