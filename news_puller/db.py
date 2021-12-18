import news_puller.config as cfg
from datetime import datetime, timedelta
from math import log
from logging import getLogger, DEBUG
import pymongo

logger = getLogger('werkzeug')
logger.setLevel(DEBUG)

class Database(object):
    
    URI = 'mongodb+srv://%s:%s@newscluster.3saws.mongodb.net/news?retryWrites=true&w=majority' % (cfg.MONGO_USERNAME, cfg.MONGO_PASSWORD)
    DATABASE = None

    def initialize():
        logger.debug('Connect with ' + Database.URI)
        client = pymongo.MongoClient(Database.URI)  # establish connection with database
        logger.debug('Connection done')
        Database.DATABASE = client['news']


    def calculate_idf(num_docs, title):
        idfs = {}
        for term in title.split():
            # Use the number of docs that contain the term to calculate the IDF
            term_docs = Database.DATABASE['news'].count({'title' : {'$regex' : term}})
            idfs[term] = log((num_docs - term_docs + 0.5) / (term_docs + 0.5))

            idfs = {k: v for k, v in idfs.items() if v > cfg.TF_IDF_MIN_WEIGHT}

        return list(idfs.keys())


    def save_news(news):
        try:
            logger.debug('Save ' + str(len(news)) + ' news in MONGO')
            # Get the total number of documents in the collection
            num_docs = Database.DATABASE.news.count()

            for new in news:
                new['idf'] = Database.calculate_idf(num_docs, new['title'])
                Database.DATABASE['news'].update_one( {'_id' : new['_id']}, {'$set' : new}, upsert=True)
        except:
            logger.error('There was an error while trying to save news')


    def save_tweets(tweets):
        try:
            logger.debug('Save ' + str(len(tweets)) + ' tweets in MONGO')
            Database.DATABASE['tweets'].insert_many(tweets, ordered = False)
        except:
            logger.error('There where some duplicated elements')
            

    def select_last_news(hour):
        last_hour_date_time = datetime.now() - timedelta(hours = hour)
        logger.debug('Return last ' + str(hour) + ' hours news in MONGO')
        
        mongo_db = Database.DATABASE['news']
        news = mongo_db.find({"published": {'$gte': str(last_hour_date_time)}})

        return list(news)


    def latest_tweet_id(url):
        since_id = 0

        try:
            mongo_db = Database.DATABASE['tweets']
            tweet = mongo_db.find_one({'new': url})
            if tweet:
                since_id = tweet['_id']

        except:
            logger.error('The collection does not exist')

        return since_id
