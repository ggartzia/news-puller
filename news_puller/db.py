import re
import news_puller.config as cfg
from datetime import datetime, timedelta
from logging import getLogger, DEBUG
import pymongo


logger = getLogger('werkzeug')
logger.setLevel(DEBUG)


class Database(object):
    
    URI = 'mongodb+srv://%s:%s@newscluster.3saws.mongodb.net/news?retryWrites=true&w=majority' % (cfg.MONGO_USERNAME, cfg.MONGO_PASSWORD)
    DATABASE = None
    PAGE_SIZE = 12

    def initialize():
        client = pymongo.MongoClient(Database.URI)  # establish connection with database
        Database.DATABASE = client['news']


    def save_new(new):
        try:
            mongo_db = Database.DATABASE['news']
            mongo_db.update_one({'_id': new['_id']}, {'$set': new}, upsert=True)

        except Exception as e:
            logger.error('There was an error while trying to save new: %s, %s', new, e)
            
            
    def save_topics(topics, theme):
        most_used_topics = []
        try:
            mongo_db = Database.DATABASE['topics']
            result = mongo_db.bulk_write([pymongo.UpdateOne({'name': t, 'theme': theme},
                                                            {'$setOnInsert': {'name': t, 'theme': theme} , '$inc':{'usage': 1}},
                                                            upsert=True) for t in topics])

            most_used_topics = mongo_db.find({'name': {'$in': topics},
                                              'theme': theme},
                                             sort=[('usage', pymongo.DESCENDING)]).limit(3)
        except Exception as e:
            logger.error('There was an error while trying to save topics: %s', e)

        return list(most_used_topics)


    def save_tweets(tweets):
        try:
            if tweets:
              mongo_db = Database.DATABASE['tweets']
              mongo_db.insert_many(tweets, ordered = False)
            
        except Exception as e:
            logger.error('There was an error while trying to save tweets: %s', e)


    def save_user(user):
        try:
            mongo_db = Database.DATABASE['users']
            mongo_db.update_one({'_id': user['id']}, {'$setOnInsert': user , '$inc':{'tweets': 1}}, upsert=True)

        except Exception as e:
            logger.error('There was an error while trying to save user: %s, %s', user, e)


    def search_new(id):
        new = None
        
        try:
            mongo_db = Database.DATABASE['news']
            new = mongo_db.find_one({'_id': id})
        except Exception as e:
            logger.error('There was an error fetching the data: %s', e)
            
        return new


    def select_last_news(hour, theme, page):
        last_hour_date_time = datetime.now() - timedelta(hours = hour)
        
        mongo_db = Database.DATABASE['news']
        news = mongo_db.find({'published': {'$gte': str(last_hour_date_time)},
                              'theme' : theme},
                             sort=[('published', pymongo.DESCENDING)]).skip(page * Database.PAGE_SIZE).limit(Database.PAGE_SIZE)

        return list(news)


    def select_trending_news(hour, page):
        last_hour_date_time = datetime.now() - timedelta(hours = hour)

        mongo_db = Database.DATABASE['news']
        news = mongo_db.find({'published': {'$gte': str(last_hour_date_time)}},
                             sort=[('tweetCount', pymongo.DESCENDING)]).skip(page * Database.PAGE_SIZE).limit(Database.PAGE_SIZE)

        return list(news)


    def select_topic_news(topic, page):
        mongo_db = Database.DATABASE['news']
        news = mongo_db.find({'topics': topic},
                             sort=[('published', pymongo.DESCENDING)]).skip(page * Database.PAGE_SIZE).limit(Database.PAGE_SIZE)

        return list(news)


    def select_related_news(id, page):
        mongo_db = Database.DATABASE['news']
        main_new = Database.search_new(id)

        if main_new:
            news = mongo_db.find({'topics': {'$all': main_new['topics']}},
                                 sort=[('published', pymongo.DESCENDING)]).skip(page * Database.PAGE_SIZE).limit(Database.PAGE_SIZE)

        return list(news) 


    def select_topics(theme, limit):
        mongo_db = Database.DATABASE['topics']

        topics = mongo_db.find({'theme': theme},
                               sort=[('usage', pymongo.DESCENDING)]).limit(limit)

        return list(topics)


    def select_tweets(new, page):
        mongo_db = Database.DATABASE['tweets']

        news = mongo_db.find({'new': new},
                             sort=[('created_at', pymongo.DESCENDING)]).skip(page * Database.PAGE_SIZE).limit(Database.PAGE_SIZE)

        return list(news)
    

    def num_news(paper, theme):
        mongo_db = Database.DATABASE['news']
        return mongo_db.count_documents({'paper': paper, 'theme': theme})


    def last_new(paper, theme):
        mongo_db = Database.DATABASE['news']
        new = mongo_db.find_one({'paper' : paper, 'theme' : theme}, sort=[('published', pymongo.DESCENDING)])
        
        if new is None:
            return None
        else:
            return new['published']

    def num_tweets(new):
        mongo_db = Database.DATABASE['tweets']
        return mongo_db.count_documents({'new': new})
