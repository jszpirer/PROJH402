#Main script for project PROJH402
import GoogleScholarScraper
import DrawingWithPillow
import ChargeArticles


#First, we ask which Google Scholar page should be analysed.
Link = input("Please enter the link :")
print("C:\\Users\\hp\\Desktop\\PROJH402\\venv\\Lib\\site-packages\\chromedriver")
html = ChargeArticles.clickOnShowMore(Link)

GoogleScholarScraper.get_articles(html)

#DrawingWithPillow.line("test.jpg")