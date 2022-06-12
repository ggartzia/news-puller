from logging import getLogger, DEBUG
import pymongo
from news_puller.database import Database
from datetime import datetime, timedelta
from news_puller.related import calculate_similarity
from news_puller.db.tweet import count_new_tweets
from news_puller.db.topic import update_topics

news_db = Database.DATABASE['news']

logger = getLogger('werkzeug')
logger.setLevel(DEBUG)


def num_news(paper, theme):
    return news_db.count_documents({'paper': paper, 'theme': theme})


def last_new(paper, theme):
    new = news_db.find_one({'paper' : paper, 'theme' : theme},
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
        logger.error('There was an error fetching new: %s. %s', id, e)
        
    return new


def save_new(new):
    try:
        news_db.update_one({'_id': new['id']},
        	               {'$set': new},
        	               upsert=True)

    except Exception as e:
        logger.error('There was an error while trying to save new: %s, %s', new, e)


def enrich_new(new, limit=3):
    new = update_topics(new, limit)
    new['tweetCount'] = count_new_tweets(new['id'])

    return new


def select_last_news(hour, theme, page):
    last_hour_date_time = datetime.now() - timedelta(hours = hour)
    query = {'published': {'$gte': str(last_hour_date_time)}, 'theme': theme}

    total = news_db.count_documents(query)

    news = news_db.find(query,
                        {'_id': 0},
                        sort=[('published', pymongo.DESCENDING)]).skip(page * Database.PAGE_SIZE).limit(Database.PAGE_SIZE)

    news = map(enrich_new, list(news))

    return {'total': total,
            'items': list(news)}


def select_trending_news(hour, page):
    last_hour_date_time = datetime.now() - timedelta(hours = hour)

    total = news_db.count_documents({'published': {'$gte': str(last_hour_date_time)}})

    news = list(news_db.aggregate([
           {
              '$match': {'published': {'$gte': str(last_hour_date_time)}}
           },
           {
              '$lookup': {
                 'from': 'tweets',
                 'localField': 'id',
                 'foreignField': 'new',
                 'as': 'tweets'
              }
           },
           {
              '$project': {
                'title':'$title',
                'description': '$description',
                'fullUrl':'$fullUrl',
                'image': '$image',
                'published': '$published',
                'paper': '$paper',
                'theme': '$theme',
                'tweetCount': {'$size': '$tweets'}
              }
           },
           {
              '$sort': {'tweetCount': pymongo.DESCENDING}
           }
        ]))

    newsFrom = page * Database.PAGE_SIZE
    newsTo = newsFrom + Database.PAGE_SIZE

    return {'total': total,
            'items': news[newsFrom:newsTo]}


def select_related_news(id):
    to_compare = []
    total = 300

    main_new = search_new(id)

    if main_new:
        # Search for less common topics
        main_new = enrich_new(main_new, 12)
        topics = [t.get("name") for t in main_new['topics']]

        to_compare = news_db.find({'theme': main_new['theme'],
                                   '_id': {'$ne': main_new['_id']},
                                   'topics': {'$in': topics}},
                                  sort=[('published', pymongo.DESCENDING)]).limit(total)

        news = calculate_similarity(main_new, to_compare)

    return {'new': main_new,
            'total': total,
            'items': list(news)}


def select_media_news(media, page):
    news = news_db.find({'paper': media},
                        {'_id': 0},
                        sort=[('published', pymongo.DESCENDING)]).skip(page * Database.PAGE_SIZE).limit(Database.PAGE_SIZE)

    news = map(enrich_new, list(news))

    total = news_db.count_documents({'paper': media})
    
    return {'total': total,
            'items': list(news)}


def select_topic_news(topic, page):
    news = news_db.find({'topics': topic},
                        {'_id': 0 },
                        sort=[('published', pymongo.DESCENDING)]).skip(page * Database.PAGE_SIZE).limit(Database.PAGE_SIZE)

    total = news_db.count_documents({'topics': topic})

    news = map(enrich_new, list(news))
    
    return {'total': total,
            'items': list(news)}