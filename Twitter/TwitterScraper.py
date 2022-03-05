import tweepy
from Twitter.GoogleDriveProj import GoogleDriveProj
from GoogleScholar.GoogleScholarScraper import GoogleScholarScraper

APIkey = ""
APIkeysecret = ""
AccessToken = ""
AccessTokenSecret = ""
BearerToken = ""
image_headers = {
            'Authorization': 'Bearer {}'.format(AccessToken)
        }


class TwitterScraper:
    gglScholarScraper = None
    gglDriveProj = None

    def __init__(self):
        """Creates the client that will tweet artworks."""
        self.client = tweepy.Client(bearer_token=BearerToken, consumer_key=APIkey, consumer_secret=APIkeysecret,
                                    access_token=AccessToken, access_token_secret=AccessTokenSecret)
        self.gglScholarScraper = GoogleScholarScraper()
        self.gglDriveProj = GoogleDriveProj()
        dict_tweets = self.__tweets_with_hashtag()
        self.analyze_tweets_with_hashtag(dict_tweets)

    def update_status(self, tweet):
        self.client.create_tweet(tweet)

    def __tweets_with_hashtag(self):
        """Method that creates a dictionary with Tweet ID and tweet text associated."""
        tweets = self.client.search_recent_tweets(query="#PROJH402ART", max_results=10)
        print(tweets)
        tweets_to_return = {}
        if tweets.data is None:
            return tweets_to_return
        for tweet in tweets.data:
            tweets_to_return[tweet.id] = tweet.text
        return tweets_to_return

    def __extract_link_google_scholar(self, tweet_text):
        """Check if a Google Scholar link was in the tweet text to generate an artwork."""
        tweet_split = tweet_text.split()
        print(tweet_split)
        for word in tweet_split:
            if 'https://t.co/' in word:
                self.link = word
                return True
        return False

    def analyze_tweets_with_hashtag(self, tweets_dict):
        """For each tweet, checks if there is a Google Scholar link. If yes, creates the artwork and tweet it back."""
        for id in tweets_dict.keys():
            if self.__extract_link_google_scholar(tweets_dict[id]):
                output_path = '../Pictures/' + str(id) + '.png'
                self.gglScholarScraper.create_artwork(self.link, output_path, self.gglDriveProj)
                artwork = self.gglDriveProj.get_id_from_name(output_path) #Id of the artwork in the Google Drive
                self.tweet_artwork_in_response(artwork, id)

    def tweet_artwork_in_response(self, artwork_image, tweet_id):
        """Tweets the sharing link Google Drive of the artwork"""
        text = self.gglDriveProj.share_link(artwork_image)
        self.client.create_tweet(in_reply_to_tweet_id=tweet_id, text=text)


