import news_puller.config as cfg
from datetime import datetime, timedelta
from logging import getLogger, DEBUG
import pymongo

log = getLogger('werkzeug')
log.setLevel(DEBUG)

class Database(object):
    
    URI = 'mongodb+srv://%s:%s@newscluster.3saws.mongodb.net/news?retryWrites=true&w=majority' % (cfg.MONGO_USERNAME, cfg.MONGO_PASSWORD)
    DATABASE = None

    def initialize():
        log.debug('Connect with ' + Database.URI)
        client = pymongo.MongoClient(Database.URI)  # establish connection with database
        log.debug('Connection done')
        Database.DATABASE = client['news']


    def save(collection, items):
        log.debug('Save ' + str(len(items)) + ' ' + collection + ' in MONGO')
        Database.DATABASE[collection].drop()
        Database.DATABASE[collection].insert_many(items)


    def select_last_news(hour):
        last_hour_date_time = datetime.now() - timedelta(hours = hour)
        log.debug('Return last ' + str(hour) + ' hours news in MONGO')
        mongo_db = Database.DATABASE['news']
        news = mongo_db.find({"published": {'$gte': str(last_hour_date_time)}})

        return list(news)
