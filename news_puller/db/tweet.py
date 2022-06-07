from logging import getLogger, DEBUG
import pymongo
from news_puller.database import Database
from news_puller.db.user import search_user


tweet_db = Database.DATABASE['tweets']

logger = getLogger('werkzeug')
logger.setLevel(DEBUG)


def save_tweets(tweets):
    try:
        if tweets:
          tweet_db.insert_many(tweets,
                               ordered = False)
        
    except Exception as e:
        logger.error('There was an error while trying to save tweets: %s', e)


def save_tweet(tweet):
    try:
        tweet_db.insert_one(tweet)
        
    except Exception as e:
        logger.error('There was an error while trying to save tweets: %s', e)



def count_new_tweets(new):
    return tweet_db.count_documents({'new': new})


def count_user_tweets(user):
    return tweet_db.count_documents({'user': user})


def search_tweet(id):
    tweet = None

    try:
        tweet = tweet_db.find_one({'_id': id})

    except Exception as e:
        logger.error('There was an error fetching tweet: %s. %s', id,  e)

    return tweet


def select_tweets(id, page):
    tweets = list(tweet_db.aggregate([
           {
              '$match': {'new': id}
           },
           {
              '$lookup': {
                 'from': 'users',
                 'localField': 'user',
                 'foreignField': 'id',
                 'as': 'items'
              }
           },
           {
              '$replaceRoot': {'newRoot': {'$mergeObjects': [{'$arrayElemAt': ['$items', 0]}, '$$ROOT']}}
           },
           {
              '$project': {'items': 0, 'user': 0}
           },
           {
              '$sort': {'created_at': pymongo.DESCENDING}
           }
        ]))

    tweetsFrom = page * Database.PAGE_SIZE
    tweetsTo = tweetsFrom + Database.PAGE_SIZE

    return tweets[tweetsFrom:tweetsTo]


def select_user_tweets(user, page):
    tweets = tweet_db.find({'user': user},
                           {'_id': 0, 'new': 0, 'user': 0},
                           sort=[('created_at', pymongo.DESCENDING)])

    return {'user': search_user(user),
            'total': count_user_tweets(user),
            'items': list(tweets)}
