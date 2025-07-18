def getFileLinks(soup, baseUrl, extension):
    from urllib.parse import urljoin
    return [urljoin(baseUrl, a["href"]) for a in soup.find_all("a", href=True) if extension.lower() in a["href"].lower()]

def downloadFile(fileUrl, saveDir, headers):
    import os, requests
    from urllib.parse import urlparse
    try:
        response = requests.get(fileUrl, headers=headers, timeout=10)
        response.raise_for_status()
        fileName = os.path.basename(urlparse(fileUrl).path)
        filePath = os.path.join(saveDir, fileName)
        with open(filePath, "wb") as f:
            f.write(response.content)
        return fileName
    except Exception as e:
        print(f"[Error downloading {fileUrl}]: {e}")
        return None
