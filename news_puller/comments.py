import os
import tweepy
import json
from dotenv import load_dotenv
from logging import getLogger, DEBUG
from news_puller.db.user import save_user
from news_puller.db.comment import save_comment


load_dotenv()

logger = getLogger('werkzeug')
logger.setLevel(DEBUG)

# media = select_all_media()

follow = ["121183700", "14436030", "74453123"]

class FetchStatus(tweepy.Stream):

    def on_data(self, data):
        try:
            print(data)
            
            tweet = json.loads(data.decode('utf8'))
            print(tweet)
            print(data._json)
            comment = {"_id": tweet["id_str"],
                       "created_at": tweet["created_at"],
                       "text": tweet["text"],
                       "user": tweet['user']['id'],
                       "retweeted_status": tweet["retweeted_status"], 
                       "user_mentions": tweet["user_mentions"]}

            print(comment)
            save_user({'id': tweet['user']['id'],
                       'name': tweet['user']['name'],
                       'screen_name': tweet['user']['screen_name'],
                       'image': tweet['user']['profile_image_url_https']})

            #The media?
            #The new?
            save_comment(comment)

        except Exception as e:
            logger.error('Something happened fetching tweets: %s', e)

    def on_error(self, status):
        print(status)
        logger.error('Something happened fetching tweets: %s', status)


stream = FetchStatus(os.getenv('TW_CONSUMER_KEY'), 
                     os.getenv('TW_CONSUMER_SECRET'),
                     os.getenv('TW_ACCESS_TOKEN'),
                     os.getenv('TW_ACCESS_TOKEN_SECRET'))

stream.filter(follow=follow, languages=['es'])
