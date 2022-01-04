from selenium import webdriver
import time

option = webdriver.ChromeOptions()
option.add_argument(" — incognito")

browser = webdriver.Chrome("chromedriver_win32\\chromedriver", chrome_options=option)
def clickOnShowMore(link):
    browser.get(link)
    python_button = browser.find_elements_by_xpath("//*[@id='gsc_bpf_more']")[0]
    python_button.click()
    time.sleep(1)
    return browser.page_source