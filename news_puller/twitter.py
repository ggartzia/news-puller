import os
import tweepy
import json
from dotenv import load_dotenv
from logging import getLogger, DEBUG
from news_puller.db.media import select_all_media
from news_puller.db.tweet import search_tweet, save_tweet
from news_puller.db.user import save_user
from news_puller.db.comment import save_comment
from news_puller.db.new import search_new


load_dotenv()

logger = getLogger('werkzeug')
logger.setLevel(DEBUG)

media = select_all_media()
follow = [m['twitter_id'] for m in media]
 print("followwwww ----->>> %s", follow)


def save(comment, original):
    original = search_tweet(tweet['in_reply_to_status_id_str'])

    if original:
      save_comment({'_id': tweet['id_str'],
                    'created_at': tweet['created_at'],
                    'text': tweet['text'],
                    'user': tweet['user']['id'],
                    'reply_to': original['id'],
                    'new': original['new']})

    else:
      print("----->>> %s", tweet['media'])
      url = tweet['media'][0]
      new = search_new(create_unique_id(url))
      save_tweet({'_id': tweet['id_str'],
                  'created_at': tweet['created_at'],
                  'text': tweet['text'],
                  'new': new['id'],
                  'user': tweet['user']['id']})

    save_user({'id': tweet['user']['id'],
               'name': tweet['user']['name'],
               'screen_name': tweet['user']['screen_name'],
               'image': tweet['user']['profile_image_url_https']})


class FetchStatus(tweepy.Stream):

    def on_connection_error(self):
        print("on_connection_error")
        self.disconnect()

    def on_status(self, status):
        try:
            tweet = status._json

            if (tweet['in_reply_to_user_id_str'] in follow):
              

              save(tweet, tw)
            else if (tweet['user']['id'] in follow):



        except Exception as e:
            logger.error('Something happened fetching tweets: %s', e)


stream = FetchStatus(os.getenv('TW_CONSUMER_KEY'), 
                     os.getenv('TW_CONSUMER_SECRET'),
                     os.getenv('TW_ACCESS_TOKEN'),
                     os.getenv('TW_ACCESS_TOKEN_SECRET'))

stream.filter(follow=follow, languages=['es'])
