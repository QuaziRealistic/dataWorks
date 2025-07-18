import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from crawling.src import crawler
from scraping.src import scraperGeneric

def main():
    crawler.crawl(crawler.baseUrl)
    scraperGeneric.scrapeAll()

if __name__ == "__main__":
    main()
