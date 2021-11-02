import requests, lxml
from bs4 import BeautifulSoup
import os

headers = {
    'User-agent':
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
}

proxies = {
  'http': os.getenv('HTTP_PROXY')
}

def get_articles(link):
  #html = requests.get(link, headers=headers, proxies=proxies).text
  soup = BeautifulSoup(link, 'lxml')

  for article_info in soup.select('#gsc_a_b .gsc_a_tr'):
    title = article_info.select_one('.gsc_a_at').text
    title_link = f"https://scholar.google.com{article_info.select_one('.gsc_a_at')['href']}"
    authors = article_info.select_one('.gsc_a_at+ .gs_gray').text
    publications = article_info.select_one('.gs_gray+ .gs_gray').text
    citations = article_info.select_one('.gsc_a_c').text

    print(f'Title: {title}\nTitle link: {title_link}\nArticle Author(s): {authors}\nArticle Publication(s): {publications}\nCited by: {citations}')
