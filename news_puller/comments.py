import json
import os
import tweepy
from dotenv import load_dotenv
from logging import getLogger, DEBUG


load_dotenv()

logger = getLogger('werkzeug')
logger.setLevel(DEBUG)


class MyStreamListener(tweepy.Stream):

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


# media = select_all_media()

follow = ["121183700", "14436030", "74453123"]

stream = tweepy.Stream(consumer_key=os.getenv('TW_CONSUMER_KEY'), 
                       consumer_secret=os.getenv('TW_CONSUMER_SECRET'),
                       access_token=os.getenv('TW_ACCESS_TOKEN'),
                       access_token_secret=os.getenv('TW_ACCESS_TOKEN_SECRET'),
                       MyStreamListener())

stream.filter(follow=follow, is_async=True)