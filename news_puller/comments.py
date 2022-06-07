import json
import os
import tweepy
from tweepy import Stream
from tweepy.streaming import StreamListener
from dotenv import load_dotenv
from logging import getLogger, DEBUG


load_dotenv()

logger = getLogger('werkzeug')
logger.setLevel(DEBUG)


class StdOutListener(StreamListener):
    def on_data(self, data):
        clean_data = json.loads(data)
        print("This is a tweet: %s", clean_data)

    def setUpAuth():
        stream = tweepy.Stream(
            os.getenv('TW_CONSUMER_KEY'), os.getenv('TW_CONSUMER_SECRET'),
            os.getenv('TW_ACCESS_TOKEN'), os.getenv('TW_ACCESS_TOKEN_SECRET'))

        return stream

    def followStream():
        print("This is the follow stream")
        stream.filter(follow=["121183700"], is_async=True)


if __name__ == "__main__":
    followStream()
