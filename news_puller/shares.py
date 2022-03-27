import news_puller.config as cfg
from news_puller.db import Database
import tweepy
from logging import getLogger, DEBUG


logger = getLogger('werkzeug')
logger.setLevel(DEBUG)


auth = tweepy.OAuthHandler(cfg.TW_CONSUMER_KEY, cfg.TW_CONSUMER_SECRET)
auth.set_access_token(cfg.TW_ACCESS_TOKEN, cfg.TW_ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)


def tweepy_shares(new):
    tweet_list= []
    users = []
    
    try:
        tweets = tweepy.Cursor(api.search_tweets,
                               q='url:' + new['fullUrl'],
                               since_id=new.get('lastTweet', 0) + 1).items(100)

        for tweet in tweets:
            twt = tweet._json
            
            # Save user individually to upsert
            Database.save_user({'id': twt['user']['id'],
                                'name': twt['user']['name'],
                                'screen_name': twt['user']['screen_name'],
                                'image': twt['user']['profile_image_url_https']})
            
            # Add tweet on a list and return the list
            tweet_list.append({'_id': twt['id'],
                               'created_at': twt['created_at'],
                               'text': twt['text'],
                               'new': new['id'],
                               'user': twt['user']['id']})

        Database.save_tweets(tweet_list)
        
        return tweet_list
    
    except Exception as e:
        logger.error('Something happened fetching tweets: %s', e)
        return -1
