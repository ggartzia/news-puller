import logging
import pymongo
from news_puller.database import Database

tweet_db = Database.DATABASE['tweets']

def save_tweet(tweet):
    try:
        tweet_db.insert_one(tweet)
        
    except Exception as e:
        logging.error('There was an error while trying to save tweets: %s', e)


def count_new_tweets(new):
    return tweet_db.count_documents({'new': new, 'reply_to': { '$exists': True }})


def count_user_tweets(user):
    return tweet_db.count_documents({'user': user})


def search_tweet(id, original=False):
    tweet = None
    query = {'_id': id}

    if original:
      query['reply_to'] = { '$exists': False }

    try:
        tweet = tweet_db.find_one(query)

    except Exception as e:
        logging.error('There was an error fetching tweet: %s. %s', id,  e)

    return tweet


def select_tweets(new, user, page):
    query = {}
    if new is not None:
      query = {'new': new, 'reply_to': { '$exists': True }}
    elif user is not None:
      query = {'user': user}

    tweets = list(tweet_db.aggregate([
           {
              '$match': query
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


def select_all_tweets(new):
    tweets = tweet_db.find({'new': new}, {'_id': 0, 'new': 0, 'user': 0},
                            sort=[('created_at', pymongo.DESCENDING)])

    return list(tweets)
