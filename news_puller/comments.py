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

follow = ['121183700', '14436030', '74453123']

class FetchStatus(tweepy.Stream):

    def on_connection_error(self):
        print("on_connection_error")
        self.disconnect()

    def on_status(self, status):
        try:
            tweet = data._json
            print(tweet)
            comment = {'_id': tweet['id_str'],
                       'created_at': tweet['created_at'],
                       'text': tweet['text'],
                       'user': tweet['user']['id'],
                       'new': tweet['retweeted_status'], 
                       'media': tweet['user_mentions']}

            print(comment)
            save_comment(comment)
            save_user({'id': tweet['user']['id'],
                       'name': tweet['user']['name'],
                       'screen_name': tweet['user']['screen_name'],
                       'image': tweet['user']['profile_image_url_https']})


        except Exception as e:
            logger.error('Something happened fetching tweets: %s', e)


stream = FetchStatus(os.getenv('TW_CONSUMER_KEY'), 
                     os.getenv('TW_CONSUMER_SECRET'),
                     os.getenv('TW_ACCESS_TOKEN'),
                     os.getenv('TW_ACCESS_TOKEN_SECRET'))

stream.filter(follow=follow, languages=['es'])
