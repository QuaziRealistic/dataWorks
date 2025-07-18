from crawling.src import crawler

def main():

    print("Starting crawler test on OpenLibrary.org...")
    crawler.crawl(crawler.baseUrl)

    print("Crawler finished.")

if __name__ == "__main__":
    main()