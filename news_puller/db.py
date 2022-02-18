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


    def save_news(news):
        try:
            mongo_db = Database.DATABASE['news']
            result = mongo_db.bulk_write([pymongo.UpdateOne({'_id': n['_id']},
                                                            {'$inc': {'tweetCount': n.pop('tweetCount', 0)}, '$set': n},
                                                            upsert=True) for n in news])

        except Exception as e:
            logger.error('There was an error while trying to save news: %s', e)


    def save_topics(topics, theme):
        try:
            mongo_db = Database.DATABASE['topics']
            result = mongo_db.bulk_write([pymongo.UpdateOne({'name': t, 'theme': theme},
                                                            {'$setOnInsert': {'name': t, 'theme': theme} , '$inc':{'usage': 1}},
                                                            upsert=True) for t in topics])

        except Exception as e:
            logger.error('There was an error while trying to save news: %s', e)


    def save_tweets(tweets):
        try:
            if len(tweets) > 0:
              mongo_db = Database.DATABASE['tweets']
              mongo_db.insert_many(tweets, ordered = False)
            
        except Exception as e:
            logger.error('There was an error while trying to save news: %s', e)


    def save_users(users):
        try:
            if len(users) > 0:
              mongo_db = Database.DATABASE['users']
              mongo_db.bulk_write([pymongo.UpdateOne(u,
                                                     {'$setOnInsert': u , '$inc':{'tweets': 1}},
                                                     upsert=True) for u in users])

        except Exception as e:
            logger.error('There was an error while trying to save news: %s', e)


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
        print("How many news has " + paper + "pupished for " + theme + " news?")
        return mongo_db.count_documents({'paper': paper, 'theme': theme})


    def last_new(paper, theme):
        mongo_db = Database.DATABASE['news']
        print("What is the last new for " + paper + " for " + theme + " news?")
        new = mongo_db.find_one({'paper' : paper, 'theme' : theme}, sort=[('published', pymongo.DESCENDING)])
        print("Last new: " + str(new))
        return new['published']

    def num_tweets(new):
        mongo_db = Database.DATABASE['tweets']
        return mongo_db.count_documents({'new': new})
