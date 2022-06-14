import os
import tweepy
from dotenv import load_dotenv
from logging import getLogger, DEBUG
from news_puller.db.media import select_all_media
from news_puller.db.tweet import search_tweet, save_tweet
from news_puller.db.user import save_user
from news_puller.scrapper import NewsScrapper


load_dotenv()

logger = getLogger('werkzeug')
logger.setLevel(DEBUG)

class TweetListener(object):

  def __init__(self):
      media = select_all_media()
      follow = [str(m['twitter_id']) for m in media]

      stream = self.MediaActivity(os.getenv('TW_CONSUMER_KEY'), 
                                  os.getenv('TW_CONSUMER_SECRET'),
                                  os.getenv('TW_ACCESS_TOKEN'),
                                  os.getenv('TW_ACCESS_TOKEN_SECRET'),
                                  follow)

      stream.filter(follow=follow, languages=['es'], threaded=True)


  class MediaActivity(tweepy.Stream):

      def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret, follow):
          super().__init__(consumer_key, consumer_secret, access_token, access_token_secret)

          self.FOLLOW = follow
          self.scrapper = NewsScrapper()


      def extract_tweet(self, full_tweet, new, reply=None):
          tweet = {'_id': full_tweet['id_str'],
                   'created_at': full_tweet['created_at'],
                   'text': full_tweet['text'],
                   'user': full_tweet['user']['id'],
                   'new': new}

          if reply is not None:
              tweet.update({'reply_to': reply,
                            ## Analizar sentimiento del comentario
                            'rating':self.TFIDF.rate_feeling(tweet['text'])})

          save_tweet(tweet)


      def extract_user(self, twuser):
          user = {'id': twuser['id'],
                  'name': twuser['name'],
                  'screen_name': twuser['screen_name'],
                  'image': twuser['profile_image_url_https']}

          save_user(user)


      def on_connection_error(self):
          self.disconnect()


      def on_status(self, status):
          try:
            tweet = status._json

            # Esto seria un tweet del periodico que puede estar compartiendo una noticia
            if (tweet['user']['id_str'] in self.FOLLOW and
                tweet['entities'] is not None and
                len(tweet['entities']['urls']) > 0):

              url = tweet['entities']['urls'][0]
              expanded_url = str(url['expanded_url']).split('?')[0]

              if "twitter.com" not in expanded_url:
                new_id = self.scrapper.scrap(expanded_url, tweet['user']['screen_name'])
                
                if new_id:
                  self.extract_tweet(tweet, new_id)

            ## Save comments on the newspaper tweets
            elif tweet['in_reply_to_status_id'] is not None:
              original = search_tweet(tweet['in_reply_to_status_id_str'])

              # Esto seria una contestacion a un tweet que tenemos guardado, podemos copiar el new
              # Ademas haremos un analisis de emociones y sentimientos
              if original is not None:
                self.extract_tweet(tweet, original['new'], original['_id'])
                self.extract_user(tweet['user'])

          except Exception as e:
              logger.error('Something happened fetching tweets: %s', e)
