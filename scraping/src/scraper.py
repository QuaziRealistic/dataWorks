import os, json, requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from time import time
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
outputFile = os.path.join(dataDir, f"scraped{fileExtension.strip('.')}.json")

def getDownloadedFiles(fileDir):
    try:
        return set(os.listdir(fileDir))
    except FileNotFoundError:
        return set()

def scrapePage(url, robotsParser, downloadedFiles):
    try:
        response = requests.get(url, headers=getHeaders(), timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # Сначала — извлекаем информацию со страницы
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

        # Затем — скачиваем файлы (если есть ссылки и robots.txt разрешает)
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

        # При желании можно вернуть info о загруженных файлах
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

    robotsParser = getRobotsParser(urls[0])
    scraped = []

    downloadedFiles = getDownloadedFiles(fileDir)

    for i, url in enumerate(urls, 1):
        if not isUrlAllowed(url, robotsParser):
            print(f"[Blocked by robots.txt] {url}")
            continue

        print(f"[{i}/{len(urls)}] Scraping: {url}")
        data = scrapePage(url, robotsParser, downloadedFiles)
        if data and data["files"]:
            scraped.append(data)

        sleepRandom(2, 5)

    with open(outputFile, "w", encoding="utf-8") as f:
        json.dump(scraped, f, indent=2, ensure_ascii=False)

    print(f"\nExtracted from {len(scraped)} pages. Saved to {outputFile}")

if __name__ == "__main__":
    scrapeAll()
