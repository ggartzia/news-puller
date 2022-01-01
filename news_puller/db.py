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

    def initialize():
        print('Connect with ' + Database.URI)
        client = pymongo.MongoClient(Database.URI)  # establish connection with database
        print('Connection done')
        Database.DATABASE = client['news']


    def save_news(news):
        try:
            print('Save ' + str(len(news)) + ' news in MONGO')
            
            mongo_db = Database.DATABASE['news']

            result = mongo_db.bulk_write([pymongo.UpdateOne({'_id': n['_id']}, {"$set": n}, upsert=True) for n in news])
            #mongo_db.insert_many(news, ordered = False)

        except Exception as e:
            logger.error(e)
            logger.error('There was an error while trying to save news')


    def update(id, tweetCount):
        try:
            print('Update ' + id + ' new in MONGO')
            
            mongo_db = Database.DATABASE['news']
            mongo_db.update_one({ '_id': id }, { "$set": { 'tweetCount': tweetCount } })
            
        except Exception as e:
            logger.error(e)
            logger.error('There was an error while trying to update the new')


    def search_new(id):
        new = None
        
        try:
            print('Get ' + str(id) + ' new in MONGO')
            mongo_db = Database.DATABASE['news']
            new = mongo_db.find_one({'_id': id})
        except:
            logger.error('There was an error fetching the data')
            
        return new


    def select_last_news(hour, theme):
        last_hour_date_time = datetime.now() - timedelta(hours = hour)
        print('Return last ' + str(hour) + ' hours news in MONGO')
        
        mongo_db = Database.DATABASE['news']
        news = mongo_db.find({'published': {'$gte': str(last_hour_date_time)},
                              'theme' : theme},
                             sort=[('published', pymongo.DESCENDING)]).limit(100)

        return list(news)


    def select_trending_news(hour):
        last_hour_date_time = datetime.now() - timedelta(hours = hour)
        print('Return trending news in the last ' + str(hour) + ' hours in MONGO')

        mongo_db = Database.DATABASE['news']
        news = mongo_db.find({'published': {'$gte': str(last_hour_date_time)}},
                             sort=[('tweetCount', pymongo.DESCENDING)]).limit(100)

        return list(news)


    def select_topic_news(topic):
        mongo_db = Database.DATABASE['news']
        news = mongo_db.find({'topics': topic},
                             sort=[('published', pymongo.DESCENDING)]).limit(100)

        return list(news)


    def select_topics(hour):
        mongo_db = Database.DATABASE['news']
        last_hour_date_time = datetime.now() - timedelta(hours = hour)

        mongo_db = Database.DATABASE['news']
        topics = mongo_db.find({'published': {'$gte': str(last_hour_date_time)}}).distinct('topics')

        news_by_topic = map(lambda t: {'name': t,
                                       'numNews': mongo_db.count_documents({'topics': t})},
                            topics)

        sorted_topics = sorted(news_by_topic, key = lambda t: t['numNews'])

        return sorted_topics[:100]


    def num_news(filter):
        mongo_db = Database.DATABASE['news']
        num = mongo_db.count_documents(filter)
        
        return num


    def last_new(media, theme):
        mongo_db = Database.DATABASE['news']

        new = mongo_db.find_one({'paper' : media, 'theme' : theme}, sort=[('published', pymongo.DESCENDING)])

        return new['published']
