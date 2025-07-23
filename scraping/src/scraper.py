import os
import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from time import sleep
from random import uniform
from config import fileExtension
from utils.utils import getHeaders, sleepRandom, getRobotsParser, isUrlAllowed
from utils.fileUtils import getFileLinks, downloadFile
from scraping.src.extractors import (
    generate_code, extract_title, extract_sector, extract_content,
    extract_source_title, extract_download_url, extract_metadata, extract_id_from_url
)

baseDir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
dataDir = os.path.join(baseDir, "scraping", "data")
fileDir = "/home/professor/Documents/scrapedDocs"
os.makedirs(fileDir, exist_ok=True)

linksFile = os.path.join(baseDir, "crawling", "data", "foundLinks.txt")
progressFile = os.path.join(dataDir, "scrape_progress.txt")
outputFile = os.path.join(dataDir, f"scraped{fileExtension.strip('.')}.json")


def getDownloadedFiles(fileDir):
    try:
        return set(os.listdir(fileDir))
    except FileNotFoundError:
        return set()


def readProgress():
    if not os.path.exists(progressFile):
        return 0
    with open(progressFile, "r") as f:
        pos = f.read()
        return int(pos) if pos.isdigit() else 0


def writeProgress(pos):
    with open(progressFile, "w") as f:
        f.write(str(pos))


def scrapePage(url, robotsParser, downloadedFiles):
    try:
        response = requests.get(url, headers=getHeaders(), timeout=(5, 15))
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        data = {
            "code": generate_code(url),
            "tags_en": [],
            "title_en": extract_title(soup),
            "sector_en": extract_sector(soup),
            "jurisdiction_en": "UAE",
            "source_url_en": url,
            "content_en": extract_content(soup),
            "metadata_en": extract_metadata(soup),
            "content_source_title_en": extract_source_title(soup),
            "content_source_en": "Federal",
            "file_url_en": extract_download_url(soup),
            "source_id": extract_id_from_url(url)
        }

        fileUrls = getFileLinks(soup, url, fileExtension)
        downloaded = []

        for fileUrl in fileUrls:
            if not isUrlAllowed(fileUrl, robotsParser):
                print(f"[Blocked by robots.txt] Skipping: {fileUrl}")
                continue

            fileName = os.path.basename(fileUrl)
            if fileName in downloadedFiles:
                print(f"[Already downloaded] Skipping: {fileName}")
                continue

            savedName = downloadFile(fileUrl, fileDir, getHeaders())
            if savedName:
                downloaded.append({"url": fileUrl, "savedAs": savedName})
                downloadedFiles.add(savedName)

        data["files"] = downloaded
        return data

    except Exception as e:
        print(f"[Error scraping {url}]: {e}")
        return None


def scrapeAll():
    with open(linksFile, "r", encoding="utf-8") as f:
        urls = [line.strip() for line in f if line.strip()]
    if not urls:
        print("[No URLs to scrape]")
        return

    start_pos = readProgress()
    if start_pos >= len(urls):
        print("[Info] All URLs have been processed.")
        return

    robotsParser = getRobotsParser(urls[0])
    downloadedFiles = getDownloadedFiles(fileDir)

    scraped = []
    if os.path.exists(outputFile):
        with open(outputFile, "r", encoding="utf-8") as f:
            scraped = json.load(f)

    for i in range(start_pos, len(urls)):
        url = urls[i]

        if not isUrlAllowed(url, robotsParser):
            print(f"[Blocked by robots.txt] {url}")
            continue

        print(f"[{i+1}/{len(urls)}] Scraping: {url}")
        data = scrapePage(url, robotsParser, downloadedFiles)
        if data and data["files"]:
            scraped.append(data)
            
        with open(outputFile, "w", encoding="utf-8") as f:
            json.dump(scraped, f, indent=2, ensure_ascii=False)
        writeProgress(i + 1)

        sleepRandom(2, 5)

    print(f"\nCompleted scraping all URLs. Results saved to {outputFile}")


if __name__ == "__main__":
    scrapeAll()
