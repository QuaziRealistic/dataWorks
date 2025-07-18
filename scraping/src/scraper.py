import os
import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from time import time

from utils.utils import getHeaders, sleepRandom, getRobotsParser, isUrlAllowed

dataDir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
linksFile = os.path.join(dataDir, "foundLinks.txt")
outputFile = os.path.join(dataDir, "scrapedData.json")


def extractAllContent(soup):
    
    return {
        "title": soup.title.string.strip() if soup.title else None,
        "headings": {
            "h1": [h.get_text(strip=True) for h in soup.find_all("h1")],
            "h2": [h.get_text(strip=True) for h in soup.find_all("h2")],
        },
        "paragraphs": [p.get_text(strip=True) for p in soup.find_all("p") if p.get_text(strip=True)],
        "images": [img.get("src") for img in soup.find_all("img") if img.get("src")],
        "meta": {
            tag.get("name", tag.get("property")): tag.get("content")
            for tag in soup.find_all("meta")
            if tag.get("content") and (tag.get("name") or tag.get("property"))
        }
    }


def scrapePage(url):
    
    try:
        response = requests.get(url, headers=getHeaders(), timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        pageContent = extractAllContent(soup)

        return {
            "url": url,
            "domain": urlparse(url).netloc,
            "timestamp": time(),
            "content": pageContent
        }

    except Exception as e:
        print(f"[Error scraping {url}]: {e}")
        return None


def scrapeAll():
    with open(linksFile, "r", encoding="utf-8") as f:
        urls = [line.strip() for line in f if line.strip()]

    if not urls:
        print("[No URLs found]")
        return

    robotsParser = getRobotsParser(urls[0])
    scrapedData = []

    for i, url in enumerate(urls, 1):
        if not isUrlAllowed(url, robotsParser):
            print(f"[Blocked by robots.txt] {url}")
            continue

        print(f"[{i}/{len(urls)}] Scraping {url}")
        data = scrapePage(url)
        if data:
            scrapedData.append(data)

        sleepRandom(2, 5)

    with open(outputFile, "w", encoding="utf-8") as f:
        json.dump(scrapedData, f, indent=2, ensure_ascii=False)

    print(f"\nScraped {len(scrapedData)} pages. Saved to {outputFile}")


if __name__ == "__main__":
    scrapeAll()
