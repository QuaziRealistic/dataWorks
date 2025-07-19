
from src import crawler, scraper

def main():
    crawler.crawl(crawler.baseUrl)
    scraper.scrapeAll()

if __name__ == "__main__":
    main()
