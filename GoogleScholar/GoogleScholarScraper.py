from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from Artwork.ScipyVoronoi import ScipyVoronoi
import time

not_interesting_words = ["and", "the", "of", "into", "in"]


class GoogleScholarScraper():

    def __init__(self):
        self.titles = []

    def get_articles(self, link):
        self.option = webdriver.ChromeOptions()
        self.option.add_argument(" — incognito")
        self.browser = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=self.option)
        html = self.__clickOnShowMore(link)
        soup = BeautifulSoup(html, 'lxml')
        self.nb_articles = 0
        dict_articles_peryear = {}

        for article_info in soup.select('#gsc_a_b .gsc_a_tr'):
            # title = article_info.select_one('.gsc_a_at').text
            # self.titles.append(title)
            # self.title_link = f"https://scholar.google.com{article_info.select_one('.gsc_a_at')['href']}"
            # self.authors = article_info.select_one('.gsc_a_at+ .gs_gray').text
            # self.publications = article_info.select_one('.gs_gray+ .gs_gray').text
            # self.citations = article_info.select_one('.gsc_a_c').text
            year = int(article_info.select_one('.gsc_a_y').text)
            if year in dict_articles_peryear.keys():
                dict_articles_peryear[year] += 1
            else:
                dict_articles_peryear[year] = 1

        self.nb_total_citations = int(soup.select_one('.gsc_rsb_std').string)
        self.list_of_subjects = []
        for subject in soup.select('#gsc_prf_int.gsc_prf_il .gsc_prf_inta.gs_ibl'):
            new_subject = subject.string
            self.list_of_subjects.append(new_subject)

        return dict_articles_peryear


    def __clickOnShowMore(self, link):
        self.browser.get(link)
        python_button = self.browser.find_elements_by_xpath("//*[@id='gsc_bpf_more']")[0]
        python_button.click()
        time.sleep(1)
        python_button = self.browser.find_elements_by_xpath("//*[@id='gsc_bpf_more']")[0]
        python_button.click()
        time.sleep(1)
        return self.browser.page_source

    def create_artwork(self, link, output_path, drive):
        """Function that will take the Google Scholar information to make an artwork."""
        dict_years = self.get_articles(link)
        # most_frequent_word = self.__find_most_frequent_word()
        voronoiDiagram = ScipyVoronoi(output_path, self.nb_total_citations, self.list_of_subjects)
        voronoiDiagram.make_diagram(dict_years)
        # artwork = voronoi(output_path, most_frequent_word)
        drive.upload_file(output_path)

    def __find_most_frequent_word(self):
        """Function that finds the most frequent keyword in article titles."""
        dict_words = {}
        for title in self.titles:
            split_title = title.split()
            for word in split_title:
                if word in dict_words:
                    dict_words[word] += 1
                elif word in not_interesting_words:
                    continue
                else:
                    dict_words[word] = 1
        max_key = max(dict_words, key=dict_words.get)
        return max_key
