import logging
import pymongo
from news_puller.database import Database
from datetime import datetime, timedelta
from news_puller.related import calculate_similarity
from news_puller.db.tweet import count_new_tweets

news_db = Database.DATABASE['news']

def num_paper_news(paper):
    return news_db.count_documents({'paper': paper})


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


def select_last_news(hour, theme, page):
    last_hour_date_time = datetime.now() - timedelta(hours = hour)
    query = {'published': {'$gte': str(last_hour_date_time)}, 'theme': theme}

    news = news_db.find(query,
                        sort=[('published', pymongo.DESCENDING)]).skip(page * Database.PAGE_SIZE).limit(Database.PAGE_SIZE)

    return {'total': news_db.count_documents(query),
            'items': list(news)}


def select_trending_news(hour, page):
    last_hour_date_time = datetime.now() - timedelta(hours = hour)
    query = {'published': {'$gte': str(last_hour_date_time)}}

    news = news_db.find(query,
                        sort=[('favorite_count', pymongo.DESCENDING)]).skip(page * Database.PAGE_SIZE).limit(Database.PAGE_SIZE)

    return {'total': news_db.count_documents(query),
            'items': list(news)}


def select_related_news(id, page):
    main_new = search_new(id)

    query = {'theme': main_new['theme'],
             '_id': {'$ne': main_new['_id']},
             'topics': {'$in': main_new['topics']}}

    news = list(news_db.aggregate([
           {
              '$match': query
           },
           {
              '$unwind': {'path': '$topics'}
           },
           {
              '$match': query
           },
           {
              '$group': {
                  '_id': '$_id',
                  'matches': {'$sum': 1}
              }
           },
           {
              '$lookup': {
                 'from': 'news',
                 'localField': '_id',
                 'foreignField': '_id',
                 'as': 'new'
              }
           },
           {
              '$set': {'new': {'$first': '$new'}}
           },
           {
              '$sort': {'matches': pymongo.DESCENDING}
           }
        ]))

    newsFrom = page * Database.PAGE_SIZE
    newsTo = newsFrom + Database.PAGE_SIZE

    return {'new': main_new,
            'total': len(news),
            'items': news[newsFrom:newsTo]}


def select_media_news(media, page):
    news = news_db.find({'paper': media},
                        sort=[('published', pymongo.DESCENDING)]).skip(page * Database.PAGE_SIZE).limit(Database.PAGE_SIZE)

    return {'total': num_paper_news(media),
            'items': list(news)}


def select_topic_news(topic, page):
    query = {'topics': topic}
    news = news_db.find(query,
                        sort=[('published', pymongo.DESCENDING)]).skip(page * Database.PAGE_SIZE).limit(Database.PAGE_SIZE)

    return {'total': news_db.count_documents(query),
            'items': list(news)}


def select_media_stats(theme):
    news = news_db.aggregate([
       {
          '$match': {'theme': theme}
       },
       {
          '$group': {
            '_id': '$paper',
            'totalReply': { '$sum': '$reply_count' },
            'totalRetweet': { '$sum': '$retweet_count' },
            'totalFav': { '$sum': '$favorite_count' },
            'published': {'$first': '$published'},
            'news': { '$sum': 1 }
          }
       },
       {
          '$lookup': {
             'from': 'media',
             'localField': '_id',
             'foreignField': '_id',
             'as': 'media'
          }
       }
    ])

    return list(news)
