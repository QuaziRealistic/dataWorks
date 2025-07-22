
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import re

def generate_code(url):
    id_part = urlparse(url).path.split("/")[-1].split("#")[0]
    return f"{id_part}-item1"

def extract_title(soup: BeautifulSoup):
    h = soup.find("h1")
    return h.get_text(strip=True) if h else ""

def extract_sector(soup: BeautifulSoup):
    el = soup.find(string=re.compile("Sector:", re.I))
    if el and el.parent:
        return el.parent.get_text(strip=True).split(":")[-1].strip()
    return ""

def extract_content(soup: BeautifulSoup):
    content = soup.find("div", class_=re.compile("content|text|article", re.I))
    return content.get_text(" ", strip=True) if content else ""

def extract_source_title(soup: BeautifulSoup):
    title = soup.find("title")
    return title.get_text(strip=True) if title else "Unknown Source Title"

def extract_download_url(soup: BeautifulSoup):
    a = soup.find("a", href=True, text=re.compile("Download", re.I))
    return a["href"] if a else ""

def extract_metadata(soup: BeautifulSoup):
    meta = {
        "issued_date": "",
        "effective_date": "",
        "gazette_date": "",
        "gazette_no": "",
        "legislation_state": "",
    }

    for row in soup.find_all("tr"):
        text = row.get_text(" ", strip=True).lower()
        if "issued" in text:
            meta["issued_date"] = text.split(":")[-1].strip()
        elif "effective" in text:
            meta["effective_date"] = text.split(":")[-1].strip()
        elif "gazette no" in text:
            meta["gazette_no"] = text.split(":")[-1].strip()
        elif "gazette date" in text:
            meta["gazette_date"] = text.split(":")[-1].strip()
        elif "status" in text or "state" in text:
            meta["legislation_state"] = text.split(":")[-1].strip()
    return meta

def extract_id_from_url(url):
    return url.split("/")[-1].split("#")[0]
