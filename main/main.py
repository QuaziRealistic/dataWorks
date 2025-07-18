import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from crawling.src import crawler
from scraping.src import scraper

def main():

    #print("Starting crawler test on OpenLibrary.org...")
    #crawler.crawl(crawler.baseUrl)

    #print("\nCrawler finished.")

    print("\nStarting scraper...")
    scraper.scrapeAll()   

    print("\nAll done.")

if __name__ == "__main__":
    main()