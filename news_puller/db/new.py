import logging
import pymongo
from news_puller.database import Database
from datetime import datetime, timedelta
from news_puller.related import calculate_similarity
from news_puller.db.tweet import count_new_tweets

news_db = Database.DATABASE['news']

def num_paper_news(paper):
    return news_db.count_documents({'paper': paper})


def last_new(paper):
    new = news_db.find_one({'paper' : paper},
    	                   sort=[('published', pymongo.DESCENDING)])
    
    if new is None:
        return None
    else:
        return new['published']


def search_new(id):
    new = None
    
    try:
        new = news_db.find_one({'_id': id})

        if new is not None:
            new['total'] = count_new_tweets(id)
        

    except Exception as e:
        logging.error('There was an error fetching new: %s. %s', id, e)
        
    return new


def save_new(new):
    try:
        news_db.insert_one(new)

    except Exception as e:
        logging.error('There was an error while trying to save new: %s, %s', new, e)


def retweet(id, tweet):
    try:
        news_db.update_one({'_id': id},
                           {'$set': {'retweet_count': tweet['retweet_count'],
                                     'favorite_count': tweet['favorite_count'],
                                     'reply_count': tweet['reply_count']}})
        
    except Exception as e:
        logging.error('There was an error while trying to save retweet of new: %s', e)


def aggregate_tweet_count(query, sort, page):
    news = list(news_db.aggregate([
           {
              '$match': query
           },
           {
              '$lookup': {
                 'from': 'tweets',
                 'localField': '_id',
                 'foreignField': 'new',
                 'as': 'tweets'
              }
           },
           {
              '$project': {
                '_id': '$_id',
                'title':'$title',
                'fullUrl':'$fullUrl',
                'image': '$image',
                'published': '$published',
                'paper': '$paper',
                'topics': '$topics',
                'tweetCount': {'$size': '$tweets'}
              }
           },
           {
              '$sort': sort
           }
        ]))

    newsFrom = page * Database.PAGE_SIZE
    newsTo = newsFrom + Database.PAGE_SIZE

    return news[newsFrom:newsTo]


def select_last_news(hour, theme, page):
    last_hour_date_time = datetime.now() - timedelta(hours = hour)
    query = {'published': {'$gte': str(last_hour_date_time)}, 'theme': theme}

    news = aggregate_tweet_count(query, {'published': pymongo.DESCENDING}, page)

    return {'total': news_db.count_documents(query),
            'items': news}


def select_trending_news(hour, page):
    last_hour_date_time = datetime.now() - timedelta(hours = hour)
    query = {'published': {'$gte': str(last_hour_date_time)}}

    news = aggregate_tweet_count(query, {'tweetCount': pymongo.DESCENDING}, page)

    return {'total': news_db.count_documents(query),
            'items': news}


def select_related_news(id, page):
    main_new = search_new(id)

    query = {'theme': main_new['theme'],
             '_id': {'$ne': main_new['_id']},
             'topics': {'$in': main_new['topics']}}

    news = aggregate_tweet_count(query, {'published': pymongo.DESCENDING}, page)

    return {'new': main_new,
            'total': news_db.count_documents(query),
            'items': calculate_similarity(main_new, news)}


def select_media_news(media, page):
    news = aggregate_tweet_count({'paper': media}, {'published': pymongo.DESCENDING}, page)

    return {'total': num_paper_news(media),
            'items': news}


def select_topic_news(topic, page):
    query = {'topics': topic}
    news = aggregate_tweet_count(query, {'published': pymongo.DESCENDING}, page)
    
    return {'total': news_db.count_documents(query),
            'items': news}