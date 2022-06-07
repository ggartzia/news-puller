import os
import tweepy
import json
from dotenv import load_dotenv
from logging import getLogger, DEBUG
from news_puller.db.comment import save_comment


load_dotenv()

logger = getLogger('werkzeug')
logger.setLevel(DEBUG)

# media = select_all_media()

follow = ["121183700", "14436030", "74453123"]

class FetchStatus(tweepy.Stream):

    def on_data(self, data):
        tweet = data.decode('utf8').replace("'", '"')
        comment = {key: tweet[key] for key in ["created_at", "id", "text", "user", "retweeted_status", "user_mentions"]}
        #The media?
        #The new?
        #Save user?
        save_comment(comment)

    def on_error(self, status):
        print(status)
        logger.error('Something happened fetching tweets: %s', status)


stream = FetchStatus(os.getenv('TW_CONSUMER_KEY'), 
                     os.getenv('TW_CONSUMER_SECRET'),
                     os.getenv('TW_ACCESS_TOKEN'),
                     os.getenv('TW_ACCESS_TOKEN_SECRET'))

stream.filter(follow=follow, languages=['es'])
