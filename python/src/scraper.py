# python/src/scraper.py
import os
import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from time import time
from config import fileExtension
from utils.utils import getHeaders, sleepRandom, getRobotsParser, isUrlAllowed
from utils.fileUtils import getFileLinks, downloadFile

baseDir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
dataDir = os.path.join(baseDir, "data")
fileDir = os.path.join(baseDir, "scraped")
os.makedirs(fileDir, exist_ok=True)

linksFile = os.path.join(baseDir, "data", "rawUrls.csv")
outputFile = os.path.join(dataDir, f"scraped{fileExtension.strip('.')}.json")

def scrapePage(url, robotsParser):
    try:
        response = requests.get(url, headers=getHeaders(), timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        fileUrls = getFileLinks(soup, url, fileExtension)
        downloaded = []

        for fileUrl in fileUrls:
            if not isUrlAllowed(fileUrl, robotsParser):
                print(f"[Blocked by robots.txt] Skipping: {fileUrl}")
                continue

            fileName = downloadFile(fileUrl, fileDir, getHeaders())
            if fileName:
                downloaded.append({"url": fileUrl, "savedAs": fileName})

        return {"sourceUrl": url, "files": downloaded, "timestamp": time()}

    except Exception as e:
        print(f"[Error scraping {url}]: {e}")
        return None

def scrapeAll():
    if not os.path.exists(linksFile):
        print(f"[Error] Links file not found: {linksFile}")
        return

    with open(linksFile, "r", encoding="utf-8") as f:
        urls = [line.strip() for line in f if line.strip()]
    if not urls:
        print("[No URLs to scrape]")
        return

    robotsParser = getRobotsParser(urls[0])
    scraped = []

    for i, url in enumerate(urls, 1):
        if not isUrlAllowed(url, robotsParser):
            print(f"[Blocked by robots.txt] {url}")
            continue

        print(f"[{i}/{len(urls)}] Scraping: {url}")
        data = scrapePage(url, robotsParser)
        if data and data["files"]:
            scraped.append(data)

        sleepRandom(2, 5)

    with open(outputFile, "w", encoding="utf-8") as f:
        json.dump(scraped, f, indent=2, ensure_ascii=False)

    print(f"\nExtracted from {len(scraped)} pages. Saved to {outputFile}")

if __name__ == "__main__":
    scrapeAll()
