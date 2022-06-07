import json
import os
import tweepy
from dotenv import load_dotenv
from logging import getLogger, DEBUG


load_dotenv()

logger = getLogger('werkzeug')
logger.setLevel(DEBUG)


# Customize tweepy.SteamListener
class MyStreamListener(tweepy.Stream):
    """
    Twitter listener, collects streaming tweets and output to a file
    """
    def __init__(self, api=None):
        super(MyStreamListener, self).__init__()


    def on_status(self, status):
        tweet = status._json
        print("Garaziii status: %s", tweet)
        

    def on_data(self, data):
        tweet = data._json
        print("Garaziii data: %s", tweet)



    def on_error(self, status):
        print(status)
        logger.error('Something happened fetching tweets: %s', status)


media = select_all_media()

follow = ["121183700", "14436030", "74453123"]

# Create you Stream object with authentication
auth = tweepy.OAuthHandler(os.getenv('TW_CONSUMER_KEY'), os.getenv('TW_CONSUMER_SECRET'))
auth.set_access_token(os.getenv('TW_ACCESS_TOKEN'), os.getenv('TW_ACCESS_TOKEN_SECRET'))
# Initialize Stream listener
l = MyStreamListener(i)

stream = tweepy.Stream(auth, l)
stream.filter(follow=follow, is_async=True)