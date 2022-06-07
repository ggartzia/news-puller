import json
import os
import tweepy
from dotenv import load_dotenv
from logging import getLogger, DEBUG


load_dotenv()

logger = getLogger('werkzeug')
logger.setLevel(DEBUG)


auth = tweepy.OAuthHandler(os.getenv('TW_CONSUMER_KEY'), os.getenv('TW_CONSUMER_SECRET'))
auth.set_access_token(os.getenv('TW_ACCESS_TOKEN'), os.getenv('TW_ACCESS_TOKEN_SECRET'))

api = tweepy.API(auth)

# Customize tweepy.SteamListener
class MyStreamListener(tweepy.StreamListener):
    """
    Twitter listener, collects streaming tweets and output to a file
    """
    def __init__(self, api=None):
        super(MyStreamListener, self).__init__()
        self.num_tweets = 0

    def on_status(self, status):
        tweet = status._json
        print("Garaziii tweet: %s", tweet)
        self.num_tweets += 1
        

    def on_error(self, status):
        print(status)
        logger.error('Something happened fetching tweets: %s', status)

media = select_all_media()
for i in range(media):
    # Initialize Stream listener
    l = MyStreamListener(i)

    # Create you Stream object with authentication
    stream = tweepy.Stream(auth, l)
    print("This is a paper:: %s", media[i])
    # Filter Twitter Streams to capture data by the keywords:
    stream.filter(follow=media[i].twitter_id, is_async=True)