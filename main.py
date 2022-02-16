#Main script for project PROJH402
from Artwork import DrawingWithPillow
from Twitter import GoogleDriveProj

#First, we ask which Google Scholar page should be analysed.
#Link = input("Please enter the link :")

#html = ChargeArticles.clickOnShowMore(Link)

#GoogleScholarScraper.get_articles(html)

#DrawingWithPillow.line("Twitter/test.png")

gglDrive = GoogleDriveProj()
gglDrive.upload_file("C:\Users\hp\Desktop\PROJH402\Twitter\\test.png")