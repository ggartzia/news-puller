import re
import news_puller.config as cfg
from datetime import datetime, timedelta
from math import log
from logging import getLogger, DEBUG
import pymongo
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords


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


    def calculate_idf(num_docs, theme, title):
        topics = []
        
        try:
            idfs = {}
            
            title = title.lower()
            title = re.sub("[^a-zñáéíóú]", " ", title)
            sw = stopwords.words('spanish')

            for term in title.split():
                if term not in sw:
                    # Use the number of docs that contain the term to calculate the IDF
                    term_docs = Database.DATABASE['news'].count_documents({'theme': theme, 'title' : {'$regex' : term}})
                    idfs[term] = log((num_docs - term_docs + 0.5) / (term_docs + 0.5))

            idfs = {k: v for k, v in idfs.items() if v > cfg.TF_IDF_MIN_WEIGHT}
            
            topics = list(idfs.keys())
        
        except Exception as e:
            logger.error(e)
            
        return topics


    def save_news(news):
        try:
            print('Save ' + str(len(news)) + ' news in MONGO')
            
            mongo_db = Database.DATABASE['news']
            mongo_db.insert_many(news, ordered = False)
            
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
        tweet = None
        
        try:
            print('Get ' + str(id) + ' new in MONGO')
            mongo_db = Database.DATABASE['tweets']
            tweet = mongo_db.find_one({'_id': id})
        except:
            logger.error('There was an error fetching the data')
            
        return tweet


    def save_tweets(tweets):
        try:
            print('Save ' + str(len(tweets)) + ' tweets in MONGO')
            Database.DATABASE['tweets'].insert_many(tweets, ordered = False)
        except:
            logger.error('There where some duplicated elements')
            

    def select_last_news(hour, theme):
        last_hour_date_time = datetime.now() - timedelta(hours = hour)
        print('Return last ' + str(hour) + ' hours news in MONGO')
        
        mongo_db = Database.DATABASE['news']
        news = mongo_db.find({'published': {'$gte': str(last_hour_date_time)}, 'theme' : theme})

        return list(news)


    def num_news(media, theme):
        print('Return the number of documets in MONGO')

        filter = {}
        if media : 
            filter['paper'] = media
            
        if theme : 
            filter['theme'] = theme
        
        print('Filter by ' + str(filter))
        
        mongo_db = Database.DATABASE['news']
        num = mongo_db.count_documents(filter)

        print('The number is: ' + str(num))
        
        return num


    def last_new(media, theme):
        print('Return last fetched new from ' + media + ' from theme ' + theme + ' in MONGO')
        
        mongo_db = Database.DATABASE['news']

        new = mongo_db.find_one({'paper' : media, 'theme' : theme}, sort=[('published', pymongo.DESCENDING)])

        return new['published']
