# Main script for project PROJH402

from Twitter.TwitterScraper import TwitterScraper

from threading import Event


scraper = TwitterScraper()
stopFlag = Event()

while not stopFlag.wait(3):
    scraper.start()






