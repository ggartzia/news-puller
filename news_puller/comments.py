import os
import tweepy
import json
from dotenv import load_dotenv
from logging import getLogger, DEBUG


load_dotenv()

logger = getLogger('werkzeug')
logger.setLevel(DEBUG)

# media = select_all_media()

follow = ["121183700", "14436030", "74453123"]

class FetchStatus(tweepy.Stream):

    def on_status(self, status):
        print("Garaziii data: %s", status)
        my_json = status.decode('utf8').replace("'", '"')
        print(my_json)
        data = json.loads(my_json)
        s = json.dumps(data, indent=4, sort_keys=True)
        print(s)

    def on_data(self, data):
        print("Garaziii data: %s", data)
        data = json.dumps(data)
        print(data)

    def on_error(self, status):
        print(status)
        logger.error('Something happened fetching tweets: %s', status)

print("Garaziii !!!!!!!!: START")

stream = FetchStatus(os.getenv('TW_CONSUMER_KEY'), 
                     os.getenv('TW_CONSUMER_SECRET'),
                     os.getenv('TW_ACCESS_TOKEN'),
                     os.getenv('TW_ACCESS_TOKEN_SECRET'))

stream.filter(follow=follow)

print("Garaziii !!!!!!!!: DONE")