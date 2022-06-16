import logging
from news_puller.database import Database

tweet_db = Database.DATABASE['retweets']

def save_retweet(tweet):
    try:
        tweet_db.insert_one(tweet)
        
    except Exception as e:
        logging.error('There was an error while trying to save tweets: %s', e)
