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
from news_puller.utils import create_unique_id
from news_puller.tfidf import TfIdfAnalizer


load_dotenv()

logger = getLogger('werkzeug')
logger.setLevel(DEBUG)


class TwitterStream(object):

  def __init__(self):
    media = select_all_media()
    self.FOLLOW = [str(m['twitter_id']) for m in media]
    self.TFIDF = TfIdfAnalizer()

    stream = FetchStatus(os.getenv('TW_CONSUMER_KEY'), 
                         os.getenv('TW_CONSUMER_SECRET'),
                         os.getenv('TW_ACCESS_TOKEN'),
                         os.getenv('TW_ACCESS_TOKEN_SECRET'))

    stream.filter(follow=self.FOLLOW, languages=['es'])


  class FetchStatus(tweepy.Stream):

    def on_connection_error(self):
        self.disconnect()

    def on_status(self, status):
        try:
          full_tweet = status._json
          tweet = {'_id': full_tweet['id_str'],
                   'created_at': full_tweet['created_at'],
                   'text': full_tweet['text'],
                   'user': full_tweet['user']['id']}

          user = {'id': full_tweet['user']['id'],
                  'name': full_tweet['user']['name'],
                  'screen_name': full_tweet['user']['screen_name'],
                  'image': full_tweet['user']['profile_image_url_https']}

          ## Save comments on the newspaper tweets
          reply_to = full_tweet['in_reply_to_user_id_str']
          if (reply_to is not None and 
              reply_to in self.FOLLOW):
            original = search_tweet(str(full_tweet['in_reply_to_status_id']))

            ## Only if the original comment is on a new
            if original is not None:
              tweet.update({'reply_to': original['_id'],
                            'new': original['new'],
                            ## Analizar sentimiento del comentario
                            'rating': self.TFIDF.rate_feeling(tweet['text'])})

              save_tweet(tweet)
              save_user(user)

          # Save tweet of the newspaper when sharing a new
          elif (full_tweet['entities'] is not None and
                len(full_tweet['entities']['urls']) > 0):

              url = full_tweet['entities']['urls'][0]
              tweet.update({'new': create_unique_id(url['expanded_url'])})

              save_tweet(tweet)
              save_user(user)

        except Exception as e:
            logger.error('Something happened fetching tweets: %s', e)
