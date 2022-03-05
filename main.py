#Main script for project PROJH402
from Artwork.voronoi import voronoi
from Twitter import GoogleDriveProj
from GoogleScholar.GoogleScholarScraper import GoogleScholarScraper

#First, we ask which Google Scholar page should be analysed.
Link = input("Please enter the link :")
gglScraper = GoogleScholarScraper()
gglScraper.get_articles(Link)
#word = gglScraper.find_most_frequent_word()
#art = voronoi("test.png", word)

#DrawingWithPillow.line("Twitter/test.png")

