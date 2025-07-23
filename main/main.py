import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from crawling.src import crawler
from scraping.src import scraper

def main():
    #crawler.crawl(crawler.baseUrl)
    scraper.scrapeAll()

if __name__ == "__main__":
    main()
