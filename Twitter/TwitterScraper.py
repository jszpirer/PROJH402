import tweepy
import requests

APIkey = "BE9uFt8ziHWsPyYdCIkgIJjii"
APIkeysecret = "TRjWApU2ZOLFWbdFhyXseEqKFGXpWtUKqQxjPeNsgOTPg6PZnr"
AccessToken = "1464173540157149189-8cruyoxXxeyLWBrju21xdZ9IyCz3aZ"
AccessTokenSecret = "2CCloSe2jWEYTGnbj9G6ZqoGzyLhCduK2WCHitoT8ptEz"
BearerToken = "AAAAAAAAAAAAAAAAAAAAAJLSWAEAAAAAssCzmkhVbIbTj8fIacHFgpahioc" \
              "%3D6b7ePUesz042UHeWRWQwE57CB7wWx569M47h12pRJCz7VDAR9T"
image_headers = {
            'Authorization': 'Bearer {}'.format(AccessToken)
        }


class TwitterScraper:
    def __init__(self):
        """Creates the client that will tweet artworks."""
        self.client = tweepy.Client(bearer_token=BearerToken, consumer_key=APIkey, consumer_secret=APIkeysecret,
                                    access_token=AccessToken, access_token_secret=AccessTokenSecret)
        self.api = tweepy.API(auth="cououc")
        self.__tweets_with_hashtag()

    def update_status(self, tweet):
        self.client.create_tweet(tweet)

    def __tweets_with_hashtag(self):
        """Method that creates a dictionary with Tweet ID and tweet text associated."""
        tweets = self.client.search_recent_tweets(query="#PROJH402ART", max_results=10)
        tweets_to_return = {}
        if tweets.data is None:
            return tweets_to_return
        for tweet in tweets.data:
            tweets_to_return[tweet.id] = tweet.text
        return tweets_to_return

    def __extract_link_google_scholar(self, tweet_text):
        """Check if a Google Scholar link was in the tweet text to generate an artwork."""
        tweet_split = tweet_text.split()
        for word in tweet_split:
            if 'https://scholar.google.com/citations?user=' in word:
                return True
        return False

    def analyze_tweets_with_hashatag(self, tweets_dict):
        """For each tweet, checks if there is a Google Scholar link. If yes, creates the artwork and tweet it back."""
        for id in tweets_dict.keys():
            if self.__extract_link_google_scholar(tweets_dict[id]):
                # TODO : Appeler le google scholar scraper qui va renvoyer l'artwork
                artwork = ""
                self.tweet_artwork_in_response(artwork, id)

    def tweet_artwork_in_response(self, artwork_image, tweet_id):
        media_id = self.__upload_artwork_server(artwork_image)
        self.api.media_upload()
        tweet = {'status': 'hello world', 'media_ids': media_id}
        post_url = 'https://api.twitter.com/1.1/statuses/update.json'
        post_resp = requests.post(post_url, params=tweet, headers=image_headers)
        print(post_resp.status_code)

    def __upload_artwork_server(self, artwork_image):
        """Function that will upload the artwork on the Twitter server."""
        auth_data = {
            'grant_type': 'client_credentials'
        }
        file = open(artwork_image, 'rb')
        data = file.read()
        ressource_url = "https://upload.twitter.com/1.1/media/upload.json"
        upload_image = {
            'media': data,
            'media_category': 'tweet_image'}
        media_id = requests.post(ressource_url, headers=image_headers, params=upload_image)
        tweet_meta = {"media_id": media_id, "alt_text": {"text": "Artwork"}}
        metadata_url = 'https://upload.twitter.com/1.1/media/metadata/create.json'
        metadata_resp = requests.post(metadata_url, params=tweet_meta, headers=auth_data)
        print(metadata_resp.status_code)
        return media_id
