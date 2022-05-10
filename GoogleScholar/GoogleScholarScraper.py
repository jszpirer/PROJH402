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
        if html is None:
            return None
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
            year_text = article_info.select_one('.gsc_a_y').text
            if len(year_text)!=0:
                year = int(year_text)
                if year in dict_articles_peryear.keys():
                    dict_articles_peryear[year] += 1
                else:
                    dict_articles_peryear[year] = 1

        self.nb_total_citations = int(soup.select_one('.gsc_rsb_std').string)
        self.profile_name = soup.select_one('#gsc_prf_in').string
        self.list_of_coauthors = []
        for author in soup.select('#gsc_rsb_co.gsc_rsb_s.gsc_prf_pnl .gsc_rsb_a_desc'):
            self.list_of_coauthors.append(author.a.string)

        return dict_articles_peryear


    def __clickOnShowMore(self, link):
        self.browser.get(link)
        list_of_buttons = self.browser.find_elements_by_xpath("//*[@id='gsc_bpf_more']")
        if len(list_of_buttons)==0:
            return None
        python_button = list_of_buttons[0]
        python_button.click()
        time.sleep(1)
        python_button = self.browser.find_elements_by_xpath("//*[@id='gsc_bpf_more']")[0]
        python_button.click()
        time.sleep(1)
        return self.browser.page_source

    def create_artwork(self, link, output_path, drive, isGif):
        """Function that will take the Google Scholar information to make an artwork."""
        print(output_path)
        dict_years = self.get_articles(link)
        if dict_years is None:
            return None
        voronoiDiagram = ScipyVoronoi(output_path, self.nb_total_citations, self.list_of_coauthors, self.profile_name)
        if isGif:
            voronoiDiagram.make_gif_evolution(dict_years)
        else:
            voronoiDiagram.make_diagram(dict_years)
        drive.upload_file(voronoiDiagram.get_outputpath())
        return voronoiDiagram.get_outputpath()

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
