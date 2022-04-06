# Main script for project PROJH402

import time
from Twitter.TwitterScraper import TwitterScraper

scraper = TwitterScraper()

while True:
    time.sleep(3)
    print("Start again")
    scraper.start()




