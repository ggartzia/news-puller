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


load_dotenv()

logger = getLogger('werkzeug')
logger.setLevel(DEBUG)

media = select_all_media()
follow = [m['twitter_id'] for m in media]
print("followwwww ----->>> %s", follow)


class FetchStatus(tweepy.Stream):

    def on_connection_error(self):
        print("on_connection_error")
        self.disconnect()

    def on_status(self, status):
        try:
            tweet = status._json
            tweet = {'_id': tweet['id_str'],
                     'created_at': tweet['created_at'],
                     'text': tweet['text'],
                     'user': tweet['user']['id']}

            user = {'id': tweet['user']['id'],
                    'name': tweet['user']['name'],
                    'screen_name': tweet['user']['screen_name'],
                    'image': tweet['user']['profile_image_url_https']}

            ## Save comments on the newspaper tweets
            reply_to = tweet['in_reply_to_user_id_str']
            if (reply_to is not None and 
                reply_to in follow):
              original = search_tweet(reply_to)

              ## Only if the original comment is on a new
              if original is not None:
                tweet.update({'reply_to': original['id'],
                              'new': original['new']})
                save_comment(tweet)
                save_user(user)

            # Save tweet of the newspaper when sharing a new
            else if (user['id'] in follow):
              print("----->>> %s", tweet['media'])
              url = tweet['media'][0]

              tweet.update({'new': create_unique_id(url)})
              save_tweet(tweet)
              save_user(user)

        except Exception as e:
            logger.error('Something happened fetching tweets: %s', e)


stream = FetchStatus(os.getenv('TW_CONSUMER_KEY'), 
                     os.getenv('TW_CONSUMER_SECRET'),
                     os.getenv('TW_ACCESS_TOKEN'),
                     os.getenv('TW_ACCESS_TOKEN_SECRET'))

stream.filter(follow=follow, languages=['es'])
