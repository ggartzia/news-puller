import os
from dotenv import load_dotenv
from news_puller.db.user import save_user
from news_puller.db.tweet import save_tweets
import tweepy
from logging import getLogger, DEBUG


load_dotenv()

logger = getLogger('werkzeug')
logger.setLevel(DEBUG)


auth = tweepy.OAuthHandler(os.getenv('TW_CONSUMER_KEY'), os.getenv('TW_CONSUMER_SECRET'))
auth.set_access_token(os.getenv('TW_ACCESS_TOKEN'), os.getenv('TW_ACCESS_TOKEN_SECRET'))

api = tweepy.API(auth)


def news_shares(new):
    tweet_list= []
    users = []

    try:
        nextTweet = int(new.get('lastTweet', 0)) + 1
        tweets = tweepy.Cursor(api.search_tweets,
                               q='url:' + new['fullUrl'],
                               since_id=nextTweet).items(100)

        for tweet in tweets:
            twt = tweet._json

            # Save user individually to upsert
            save_user({'id': twt['user']['id'],
                       'name': twt['user']['name'],
                       'screen_name': twt['user']['screen_name'],
                       'image': twt['user']['profile_image_url_https']})
            
            # Add tweet on a list and return the list
            tweet_list.append({'_id': twt['id_str'],
                               'created_at': twt['created_at'],
                               'text': twt['text'],
                               'new': new['id'],
                               'user': twt['user']['id']})

        save_tweets(tweet_list)
        
        return tweet_list
    
    except Exception as e:
        logger.error('Something happened fetching tweets: %s', e)
        return -1
