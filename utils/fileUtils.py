def getFileLinks(soup, baseUrl, extension):
    from urllib.parse import urljoin
    links = []
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if ".epub" in href.lower():  # не строгое окончание, а вхождение
            full_url = urljoin(baseUrl, href)
            links.append(full_url)
    return links

def downloadFile(fileUrl, saveDir, headers):
    import os, requests
    from urllib.parse import urlparse

    try:
        # follow redirects (default=True)
        response = requests.get(fileUrl, headers=headers, timeout=10, allow_redirects=True)
        response.raise_for_status()

        # получим финальный URL после всех редиректов
        final_url = response.url
        file_name = os.path.basename(urlparse(final_url).path)

        # если имя не оканчивается на .epub — добавим
        if not file_name.endswith(".epub"):
            file_name += ".epub"

        file_path = os.path.join(saveDir, file_name)
        with open(file_path, "wb") as f:
            f.write(response.content)

        print(f"[Downloaded] {fileUrl} → {file_name}")
        return file_name

    except Exception as e:
        print(f"[Error downloading {fileUrl}]: {e}")
        return None
